/* Coffre-fort local : toutes les données du centre, chiffrées (AES-GCM 256,
 * clé dérivée du mot de passe par PBKDF2-SHA256, 310 000 itérations) et
 * stockées dans le navigateur (IndexedDB). Rien n'est envoyé sur un serveur.
 * Sauvegarde = fichier .json chiffré, restaurable sur un autre ordinateur. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  // 600 000 itérations PBKDF2-HMAC-SHA256 : recommandation OWASP (2023) ; les coffres plus anciens gardent leur valeur
  const ITER = 600000, ITER_MIN = 100000, ITER_MAX = 5000000, BASE = "yeba-pilotage", MAGASIN = "coffre", CLE = "donnees", VERROU = "verrou";
  const TAILLE_SAUVEGARDE_MAX = 300 * 1024 * 1024;
  const enc = new TextEncoder(), dec = new TextDecoder();
  const b64 = (u8) => { let s = ""; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode(...u8.subarray(i, i + 0x8000)); return btoa(s); };
  const deb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

  function ouvrirBase() {
    return new Promise((ok, ko) => {
      let r;
      try { r = indexedDB.open(BASE, 1); } catch (e) { ko(e); return; }
      r.onupgradeneeded = () => r.result.createObjectStore(MAGASIN);
      r.onsuccess = () => ok(r.result);
      r.onerror = () => ko(r.error);
    });
  }
  async function idb(mode, fn) {
    const db = await ouvrirBase();
    return new Promise((ok, ko) => {
      const tx = db.transaction(MAGASIN, mode), st = tx.objectStore(MAGASIN);
      const req = fn(st);
      tx.oncomplete = () => ok(req && req.result);
      tx.onerror = () => ko(tx.error);
    });
  }
  async function deriver(mdp, sel, iterations = ITER) {
    const base = await crypto.subtle.importKey("raw", enc.encode(mdp), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey({ name: "PBKDF2", salt: sel, iterations, hash: "SHA-256" }, base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
  }
  async function chiffrer(cle, sel, objet, iterations) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cle, enc.encode(JSON.stringify(objet))));
    return { format: "yeba-pilotage-1", algo: "AES-GCM-256/PBKDF2-SHA256", iterations: iterations || ITER, sel: b64(sel), iv: b64(iv), donnees: b64(ct), date: new Date().toISOString() };
  }
  const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
  async function dechiffrer(mdp, paquet) {
    if (!paquet || typeof paquet !== "object" || paquet.format !== "yeba-pilotage-1") throw new Error("Ce fichier n'est pas une sauvegarde du logiciel.");
    // un fichier trafiqué ne doit ni bloquer l'ordinateur (itérations démesurées) ni affaiblir le coffre (itérations dérisoires)
    const it = Number(paquet.iterations || 310000);
    if (!Number.isInteger(it) || it < ITER_MIN || it > ITER_MAX) throw new Error("Sauvegarde invalide (paramètres de chiffrement anormaux).");
    for (const k of ["sel", "iv", "donnees"]) if (typeof paquet[k] !== "string" || !B64.test(paquet[k])) throw new Error("Sauvegarde invalide ou altérée.");
    const sel = deb64(paquet.sel), cle = await deriver(mdp, sel, it);
    try {
      const clair = await crypto.subtle.decrypt({ name: "AES-GCM", iv: deb64(paquet.iv) }, cle, deb64(paquet.donnees));
      return { cle, sel, iterations: it, donnees: JSON.parse(dec.decode(clair)) };
    } catch (e) { throw new Error("Mot de passe incorrect, ou fichier modifié."); }
  }
  const robuste = (m) => (m.length < 12 ? "12 caractères minimum." :
    [/[a-z]/, /[A-Z]/, /\d/, /[^A-Za-z0-9]/].filter((r) => r.test(m)).length < 3 ? "Mélangez au moins 3 familles : minuscules, majuscules, chiffres, symboles." : "");

  const Coffre = {
    cle: null, sel: null, iterations: ITER, donnees: null, echecs: 0, bloqueJusqua: 0,
    async existe() { try { return !!(await idb("readonly", (s) => s.get(CLE))); } catch (e) { return false; } },
    async creer(mdp, initiales) {
      const err = robuste(mdp);
      if (err) throw new Error(err);
      this.sel = crypto.getRandomValues(new Uint8Array(16)); this.iterations = ITER;
      this.cle = await deriver(mdp, this.sel);
      this.donnees = initiales;
      await this.enregistrer();
      try { await navigator.storage?.persist?.(); } catch (e) { /* facultatif */ }
    },
    async ouvrir(mdp) {
      // compteur d'échecs gardé dans le navigateur : recharger la page ne remet plus les essais à zéro
      const v = (await idb("readonly", (s) => s.get(VERROU)).catch(() => null)) || { echecs: 0, bloque: 0 };
      if (Date.now() < v.bloque) throw new Error(`Trop d'essais : patientez ${Math.ceil((v.bloque - Date.now()) / 1000)} s.`);
      const paquet = await idb("readonly", (s) => s.get(CLE));
      try {
        const r = await dechiffrer(mdp, paquet);
        Object.assign(this, { cle: r.cle, sel: r.sel, iterations: r.iterations, donnees: r.donnees, echecs: 0 });
        await idb("readwrite", (s) => s.put({ echecs: 0, bloque: 0 }, VERROU)).catch(() => {});
        // coffre créé avec moins d'itérations : re-chiffré avec le réglage actuel, dès l'ouverture
        if (r.iterations < ITER) { this.sel = crypto.getRandomValues(new Uint8Array(16)); this.iterations = ITER; this.cle = await deriver(mdp, this.sel); await this.reChiffrerPieces(r.cle); await this.enregistrer(); }
      } catch (e) {
        v.echecs++;
        if (v.echecs >= 5) v.bloque = Date.now() + Math.min(30000 * 2 ** (v.echecs - 5), 3600000);
        await idb("readwrite", (s) => s.put(v, VERROU)).catch(() => {});
        throw e;
      }
    },
    // après un changement de clé, les pièces jointes sont déchiffrées avec l'ancienne et re-chiffrées avec la nouvelle
    async reChiffrerPieces(ancienne) {
      for (const id of Object.keys(this.donnees.fichiers || {})) {
        const p = await idb("readonly", (st) => st.get("fichier:" + id));
        if (!p) continue;
        const clair = new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: deb64(p.iv) }, ancienne, deb64(p.donnees)));
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, this.cle, clair));
        await idb("readwrite", (st) => st.put({ iv: b64(iv), donnees: b64(ct) }, "fichier:" + id));
      }
    },
    async enregistrer() {
      if (!this.cle) throw new Error("Coffre verrouillé.");
      this.donnees.maj = new Date().toISOString();
      const paquet = await chiffrer(this.cle, this.sel, this.donnees, this.iterations);
      await idb("readwrite", (s) => s.put(paquet, CLE));
    },
    // Pièces jointes (conventions signées, justificatifs…) : chiffrées une à une
    async deposerFichier(nom, type, octets) {
      const id = "f" + crypto.getRandomValues(new Uint32Array(2)).join("");
      const iv = crypto.getRandomValues(new Uint8Array(12));
      const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, this.cle, octets));
      await idb("readwrite", (st) => st.put({ iv: b64(iv), donnees: b64(ct) }, "fichier:" + id));
      (this.donnees.fichiers = this.donnees.fichiers || {})[id] = { nom, type, taille: octets.byteLength, depose: new Date().toISOString() };
      await this.enregistrer();
      return id;
    },
    async lireFichier(id) {
      const p = await idb("readonly", (st) => st.get("fichier:" + id));
      if (!p) throw new Error("Pièce introuvable dans ce navigateur.");
      return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: deb64(p.iv) }, this.cle, deb64(p.donnees)));
    },
    async supprimerFichier(id) { await idb("readwrite", (st) => st.delete("fichier:" + id)); delete (this.donnees.fichiers || {})[id]; await this.enregistrer(); },
    async exporter() {
      const pieces = {};
      for (const id of Object.keys(this.donnees.fichiers || {})) {
        const p = await idb("readonly", (st) => st.get("fichier:" + id));
        if (p) pieces[id] = p;                       // déjà chiffrées : copiées telles quelles
      }
      const paquet = await chiffrer(this.cle, this.sel, this.donnees, this.iterations);
      paquet.pieces = pieces;
      return JSON.stringify(paquet);
    },
    async importer(texte, mdp) {
      if (typeof texte !== "string" || texte.length > TAILLE_SAUVEGARDE_MAX) throw new Error("Sauvegarde trop volumineuse ou illisible.");
      let paquet;
      try { paquet = JSON.parse(texte); } catch (e) { throw new Error("Ce fichier n'est pas une sauvegarde du logiciel."); }
      const r = await dechiffrer(mdp, paquet);
      // seules les pièces déclarées DANS les données chiffrées (donc authentifiées) sont reprises, avec un identifiant au bon format
      const attendues = new Set(Object.keys((r.donnees && r.donnees.fichiers) || {}).filter((id) => /^f\d{1,24}$/.test(id)));
      const pieces = paquet.pieces && typeof paquet.pieces === "object" ? paquet.pieces : {};
      Object.assign(this, { cle: r.cle, sel: r.sel, iterations: r.iterations, donnees: r.donnees });
      for (const id of attendues) {
        const p = pieces[id];
        if (p && typeof p.iv === "string" && typeof p.donnees === "string" && B64.test(p.iv) && B64.test(p.donnees)) await idb("readwrite", (st) => st.put({ iv: p.iv, donnees: p.donnees }, "fichier:" + id));
      }
      await this.enregistrer();
    },
    verrouiller() { this.cle = null; this.donnees = null; },
    async effacer() {
      const ids = Object.keys((this.donnees && this.donnees.fichiers) || {});
      for (const id of ids) await idb("readwrite", (s) => s.delete("fichier:" + id));      // les pièces jointes aussi
      await idb("readwrite", (s) => s.delete(CLE)); await idb("readwrite", (s) => s.delete(VERROU)).catch(() => {}); this.verrouiller();
    },
  };
  Object.assign(P, { Coffre, robuste });
})(typeof window !== "undefined" ? window : globalThis);

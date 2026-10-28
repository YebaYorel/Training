/* Coffre-fort local : toutes les données du centre, chiffrées (AES-GCM 256,
 * clé dérivée du mot de passe par PBKDF2-SHA256, 310 000 itérations) et
 * stockées dans le navigateur (IndexedDB). Rien n'est envoyé sur un serveur.
 * Sauvegarde = fichier .json chiffré, restaurable sur un autre ordinateur. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const ITER = 310000, BASE = "yeba-pilotage", MAGASIN = "coffre", CLE = "donnees";
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
  async function deriver(mdp, sel) {
    const base = await crypto.subtle.importKey("raw", enc.encode(mdp), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey({ name: "PBKDF2", salt: sel, iterations: ITER, hash: "SHA-256" }, base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
  }
  async function chiffrer(cle, sel, objet) {
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cle, enc.encode(JSON.stringify(objet))));
    return { format: "yeba-pilotage-1", algo: "AES-GCM-256/PBKDF2-SHA256", iterations: ITER, sel: b64(sel), iv: b64(iv), donnees: b64(ct), date: new Date().toISOString() };
  }
  async function dechiffrer(mdp, paquet) {
    if (!paquet || paquet.format !== "yeba-pilotage-1") throw new Error("Ce fichier n'est pas une sauvegarde du logiciel.");
    const sel = deb64(paquet.sel), cle = await deriver(mdp, sel);
    try {
      const clair = await crypto.subtle.decrypt({ name: "AES-GCM", iv: deb64(paquet.iv) }, cle, deb64(paquet.donnees));
      return { cle, sel, donnees: JSON.parse(dec.decode(clair)) };
    } catch (e) { throw new Error("Mot de passe incorrect, ou fichier modifié."); }
  }
  const robuste = (m) => (m.length < 12 ? "12 caractères minimum." :
    [/[a-z]/, /[A-Z]/, /\d/, /[^A-Za-z0-9]/].filter((r) => r.test(m)).length < 3 ? "Mélangez au moins 3 familles : minuscules, majuscules, chiffres, symboles." : "");

  const Coffre = {
    cle: null, sel: null, donnees: null, echecs: 0, bloqueJusqua: 0,
    async existe() { try { return !!(await idb("readonly", (s) => s.get(CLE))); } catch (e) { return false; } },
    async creer(mdp, initiales) {
      const err = robuste(mdp);
      if (err) throw new Error(err);
      this.sel = crypto.getRandomValues(new Uint8Array(16));
      this.cle = await deriver(mdp, this.sel);
      this.donnees = initiales;
      await this.enregistrer();
      try { await navigator.storage?.persist?.(); } catch (e) { /* facultatif */ }
    },
    async ouvrir(mdp) {
      if (Date.now() < this.bloqueJusqua) throw new Error(`Trop d'essais : patientez ${Math.ceil((this.bloqueJusqua - Date.now()) / 1000)} s.`);
      const paquet = await idb("readonly", (s) => s.get(CLE));
      try {
        const r = await dechiffrer(mdp, paquet);
        Object.assign(this, { cle: r.cle, sel: r.sel, donnees: r.donnees, echecs: 0 });
      } catch (e) {
        this.echecs++;
        if (this.echecs >= 5) this.bloqueJusqua = Date.now() + Math.min(30000 * 2 ** (this.echecs - 5), 3600000);
        throw e;
      }
    },
    async enregistrer() {
      if (!this.cle) throw new Error("Coffre verrouillé.");
      this.donnees.maj = new Date().toISOString();
      const paquet = await chiffrer(this.cle, this.sel, this.donnees);
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
      const paquet = await chiffrer(this.cle, this.sel, this.donnees);
      paquet.pieces = pieces;
      return JSON.stringify(paquet);
    },
    async importer(texte, mdp) {
      const paquet = JSON.parse(texte);
      const r = await dechiffrer(mdp, paquet);
      Object.assign(this, { cle: r.cle, sel: r.sel, donnees: r.donnees });
      for (const [id, p] of Object.entries(paquet.pieces || {})) await idb("readwrite", (st) => st.put(p, "fichier:" + id));
      await this.enregistrer();
    },
    verrouiller() { this.cle = null; this.donnees = null; },
    async effacer() { await idb("readwrite", (s) => s.delete(CLE)); this.verrouiller(); },
  };
  Object.assign(P, { Coffre, robuste });
})(typeof window !== "undefined" ? window : globalThis);

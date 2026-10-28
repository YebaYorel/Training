/* Interface de l'atelier : dépôt, réglages, génération, téléchargements. */
(function () {
  "use strict";
  const D = window.Decorticage;
  const $ = (id) => document.getElementById(id);
  const etat = { analyse: null, ctx: null, cache: {}, logo: null, exemple: true };
  const CLE_CHARTE = "decorticage.charte.v1";
  const lire = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const ecrire = (k, v) => { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } };

  // ---------------------------------------------------------------- messages
  function message(texte, type = "alerte") {
    const d = document.createElement("div");
    d.className = "message " + type;
    d.textContent = texte;
    $("messages").appendChild(d);
  }
  const viderMessages = () => { $("messages").replaceChildren(); };

  // ------------------------------------------------------------------ charte
  const CHAMPS_CHARTE = ["nom_organisme", "couleur_primaire", "couleur_secondaire", "couleur_claire", "couleur_texte", "police", "taille_texte"];
  function chargerCharte() {
    try {
      const c = JSON.parse(lire(CLE_CHARTE) || "null");
      if (!c) return;
      for (const k of CHAMPS_CHARTE) if (c[k] !== undefined) $(k).value = c[k];
      if (c.logo) definirLogo(c.logo, false);
      etat.couleursValidees = !!c.couleurs_validees;
    } catch (e) { /* charte par défaut */ }
  }
  function charte() {
    const hex = (v) => (/^#?[0-9a-f]{6}$/i.test(v) ? v.replace("#", "").toUpperCase() : "1F3A5F");
    return { nom_organisme: $("nom_organisme").value.trim().slice(0, 120) || "YEBA FORMATIONS", couleur_primaire: hex($("couleur_primaire").value),
      couleur_secondaire: hex($("couleur_secondaire").value), couleur_claire: hex($("couleur_claire").value), couleur_texte: hex($("couleur_texte").value),
      police: ($("police").value.replace(/[^A-Za-z0-9 \-]/g, "").slice(0, 40)) || "Arial",
      taille_texte: Math.min(28, Math.max(14, +$("taille_texte").value || 14)), taille_titre: Math.min(40, Math.max(22, (+$("taille_texte").value || 14) + 8)),
      couleurs_validees: !!etat.couleursValidees };
  }
  function sauverCharte() {
    etat.couleursValidees = true;
    const c = charte();
    c.couleurs_validees = true;
    if (etat.logo) c.logo = etat.logo.dataURL;
    if (!ecrire(CLE_CHARTE, JSON.stringify(c)) && etat.logo) { delete c.logo; ecrire(CLE_CHARTE, JSON.stringify(c)); }
  }
  function definirLogo(dataURL, sauver = true) {
    const img = new Image();
    img.onload = () => {
      // Ré-encodage en PNG via canvas : supprime métadonnées et contenu caché
      const echelle = Math.min(1, 1200 / Math.max(img.width, img.height));
      const cv = document.createElement("canvas");
      cv.width = Math.max(1, Math.round(img.width * echelle)); cv.height = Math.max(1, Math.round(img.height * echelle));
      cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
      const propre = cv.toDataURL("image/png"), b64 = propre.split(",")[1];
      const bin = atob(b64), oct = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) oct[i] = bin.charCodeAt(i);
      etat.logo = { dataURL: propre, base64: b64, ext: "png", octets: oct, ratio: cv.width / cv.height };
      $("logo-etat").textContent = `Logo chargé (${cv.width} × ${cv.height} px)`;
      etat.cache = {};
      if (sauver) sauverCharte();
    };
    img.onerror = () => message("Image de logo illisible : choisissez un PNG ou un JPEG.", "ko");
    img.src = dataURL;
  }
  $("logo").addEventListener("change", (e) => {
    const f = e.target.files[0];
    if (!f) return;
    if (!/\.(png|jpe?g)$/i.test(f.name) || f.size > 5 * 1024 * 1024) { message("Logo : PNG ou JPEG de 5 Mo maximum.", "ko"); return; }
    const r = new FileReader();
    r.onload = () => definirLogo(r.result);
    r.readAsDataURL(f);
  });
  $("retirer-logo").addEventListener("click", () => { etat.logo = null; $("logo-etat").textContent = "Aucun logo"; $("logo").value = ""; etat.cache = {}; sauverCharte(); });
  for (const k of CHAMPS_CHARTE) $(k).addEventListener("change", () => { etat.cache = {}; sauverCharte(); });

  // ------------------------------------------------------------- documents
  const LIB = { REAC: "REAC", RE: "RE / RC", FICHE: "Fiche France Compétences", INCONNU: "Non reconnu" };
  async function recevoir(liste) {
    const fichiers = [...liste].slice(0, 10);
    if (!fichiers.length) return;
    viderMessages();
    const ul = $("liste-fichiers");
    ul.replaceChildren();
    const lignes = fichiers.map((f) => {
      const li = document.createElement("li"), p = document.createElement("span"), n = document.createElement("span");
      p.className = "puce att"; p.textContent = "lecture…"; n.className = "nom"; n.textContent = f.name;
      li.append(p, n); ul.appendChild(li);
      return [f, p];
    });
    $("generer").disabled = true;
    try {
      const analyse = { reac: null, re: null, fiche: null, inconnus: [], noms: {}, erreurs: [] };
      const lus = [];
      for (const [f, p] of lignes) {
        try {
          const r = await D.lireFichier(f), type = D.detecterType(r.texte);
          lus.push([f.name, r, type]);
          p.textContent = LIB[type]; p.className = "puce " + (type === "INCONNU" ? "ko" : "ok");
        } catch (e) { p.textContent = "refusé"; p.className = "puce ko"; message(e.message || String(e), "ko"); }
      }
      for (const [nom, r, type] of lus) if (type === "REAC") { analyse.reac = D.analyserReac(r.texte, r.brut); analyse.noms.reac = nom; }
      for (const [nom, r, type] of lus) {
        if (type === "RE") { analyse.re = D.analyserRe(r.texte, analyse.reac); analyse.noms.re = nom; }
        else if (type === "FICHE") { analyse.fiche = D.analyserFiche(r.texte); analyse.noms.fiche = nom; }
        else if (type === "INCONNU") analyse.inconnus.push(nom);
      }
      if (!analyse.reac) { message("Aucun REAC reconnu : le REAC est indispensable pour décortiquer le titre.", "ko"); return; }
      etat.analyse = analyse; etat.exemple = false;
      $("bandeau-exemple").hidden = true;
      await generer();
    } finally { $("generer").disabled = false; }
  }
  const depot = $("depot");
  depot.addEventListener("click", () => $("fichiers").click());
  depot.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); $("fichiers").click(); } });
  depot.addEventListener("dragover", (e) => { e.preventDefault(); depot.classList.add("survol"); });
  depot.addEventListener("dragleave", () => depot.classList.remove("survol"));
  depot.addEventListener("drop", (e) => { e.preventDefault(); depot.classList.remove("survol"); recevoir(e.dataTransfer.files); });
  $("fichiers").addEventListener("change", (e) => recevoir(e.target.files));

  // -------------------------------------------------------------- réglages
  const NUM = ["heures_centre", "h_accueil", "h_ecf_par_at", "h_dossier_pro", "h_productions", "h_examen_blanc", "h_bilan"];
  const TXT = ["date_debut", "date_examen", "creneaux", "pauses", "jours", "rythme", "fermetures", "ordre_cp", "poids_cp", "commanditaire",
    "public", "prerequis", "lieu", "delai_acces", "referent_handicap", "modalites_pedagogiques"];
  function reglages() {
    const r = { heures_entreprise: 0 };
    for (const k of NUM) r[k] = Math.max(0, parseFloat(String($(k).value).replace(",", ".")) || 0);
    for (const k of TXT) r[k] = String($(k).value || "").slice(0, 2000);
    r.afficher_nom = $("afficher_nom").checked; r.afficher_logo = $("afficher_logo").checked;
    const aff = {};
    if ($("prix_inter").value.trim()) aff["Inter-entreprises (par stagiaire, HT)"] = $("prix_inter").value.trim().slice(0, 40);
    if ($("prix_intra").value.trim()) aff["Intra-entreprise (par jour, par groupe, HT)"] = $("prix_intra").value.trim().slice(0, 40);
    r.tarif_affichage = aff;
    return r;
  }

  // ------------------------------------------------------------ génération
  async function generer() {
    if (!etat.analyse) { message("Déposez d'abord vos documents (le REAC au minimum).", "ko"); return; }
    viderMessages();
    try {
      etat.ctx = D.construireContexte(etat.analyse, reglages(), charte(), etat.logo);
      etat.cache = {};
      rendre();
      if (!etat.exemple) message("Documents prêts : utilisez les boutons de téléchargement.", "ok");
      for (const a of etat.ctx.plan.avertissements.concat(etat.ctx.alertes, etat.ctx.hypotheses.map((h) => "Hypothèse à confirmer : " + h))) message(a, "alerte");
      for (const i of etat.analyse.inconnus) message(`Document non reconnu (ignoré) : ${i}`, "ko");
    } catch (e) { message(e.message || String(e), "ko"); }
  }
  $("generer").addEventListener("click", async () => {
    $("generer").disabled = true;
    try { await generer(); } finally { $("generer").disabled = false; }
  });

  // --------------------------------------------------------------- rendu
  const el = (tag, txt, cls) => { const e = document.createElement(tag); if (txt !== undefined) e.textContent = txt; if (cls) e.className = cls; return e; };
  function rendre() {
    const { reac, plan, fiche } = etat.ctx;
    const total = plan.lignes.reduce((t, l) => t + l.minutes, 0);
    const jours = new Set(plan.lignes.map((l) => D.iso(l.date))).size;
    const ch = $("chiffres");
    ch.replaceChildren();
    for (const [v, lib] of [[D.fmtDuree(total), "en centre"], [String(plan.seances.length), "séances"], [String(jours), "jours"],
      [plan.lignes.length ? D.fr(plan.lignes[0].date).slice(0, 5) + " → " + D.fr(plan.date_fin) : "—", "période"]]) {
      const c = el("div", undefined, lib === "période" ? "chiffre large" : "chiffre"); c.append(el("b", v), el("span", lib)); ch.appendChild(c);
    }
    const st = $("structure");
    st.replaceChildren(el("h3", ((fiche && fiche.code) ? fiche.code + " — " : "") + etat.ctx.titre));
    for (const at of reac.activites) {
      const b = el("div", undefined, "at");
      b.appendChild(el("b", `AT${at.numero} — ${at.intitule}`));
      const cps = el("div", undefined, "cps");
      for (const n of at.competences) {
        const s = el("span", undefined, "cp"), em = el("em", `CP${n}`);
        s.append(em, document.createTextNode(` ${D.simplifier(reac.competence(n).intitule)} · ${D.fmtDuree(plan.minutes_cp[n] || 0)}`));
        cps.appendChild(s);
      }
      b.appendChild(cps); st.appendChild(b);
    }
    vue(document.querySelector('#onglets [aria-selected="true"]').dataset.v);
  }

  function tableau(entetes, lignes) {
    const t = el("table"), th = el("thead"), tr = el("tr");
    entetes.forEach((h) => tr.appendChild(el("th", h)));
    th.appendChild(tr); t.appendChild(th);
    const tb = el("tbody");
    for (const l of lignes) {
      const r = el("tr");
      for (const c of l) {
        const td = el("td");
        if (c && typeof c === "object" && c.verbe !== undefined) {
          const t2 = c.texte;
          if (c.verbe && t2.toLowerCase().startsWith(c.verbe.toLowerCase())) { td.append(el("span", c.verbe, "verbe"), document.createTextNode(t2.slice(c.verbe.length))); }
          else td.textContent = t2;
        } else String(c ?? "").split("\n").forEach((ligne, i) => { if (i) td.appendChild(el("br")); td.appendChild(document.createTextNode(ligne)); });
        r.appendChild(td);
      }
      tb.appendChild(r);
    }
    t.appendChild(tb);
    return t;
  }
  function vue(v) {
    const { plan, reac, re, fiche } = etat.ctx, ap = $("apercu");
    let t;
    if (v === "jours") {
      const par = new Map();
      for (const l of plan.lignes) { const k = D.iso(l.date); if (!par.has(k)) par.set(k, []); par.get(k).push(l); }
      t = tableau(["Date", "Séances du jour", "Heures"], [...par.values()].map((ls) => {
        const ss = new Map();
        for (const x of ls) { if (!ss.has(x.seance.numero)) ss.set(x.seance.numero, []); ss.get(x.seance.numero).push(x); }
        return [`${D.JOURS[D.jourSem(ls[0].date)].slice(0, 3)} ${D.fr(ls[0].date)}`,
          [...ss.values()].map((xs) => `S${xs[0].seance.numero} · ${D.fmtHm(xs[0].debut)}-${D.fmtHm(xs[xs.length - 1].fin)} · ${xs[0].seance.titre}`).join("\n"),
          D.fmtDuree(ls.reduce((a, x) => a + x.minutes, 0))];
      }));
    } else if (v === "deco") {
      t = tableau(["Séance", "Objectif pédagogique", "Bloom", "Durée"], plan.seances.flatMap((s) => s.objectifs.map((o, k) =>
        [k === 0 ? `S${s.numero} — ${s.cp ? "CP" + s.cp + " · " : ""}${s.titre}` : "", { verbe: o.verbe, texte: o.texte }, D.NIVEAUX_BLOOM[o.niveau], D.fmtDuree(o.minutes)])));
    } else if (v === "examen") {
      const ex = D.construireExamen(reac, re, fiche);
      const frag = document.createDocumentFragment();
      if (ex.partie1.length > 1) frag.appendChild(tableau(ex.partie1[0], ex.partie1.slice(1)));
      frag.appendChild(tableau(["Compétence", "Ce que le jury attend"], ex.partie2.map((b) => [b.cp, b.attendus.map((a) => "✔ " + a).join("\n")])));
      t = frag;
    } else {
      const total = plan.lignes.reduce((a, l) => a + l.minutes, 0);
      const lignes = [];
      for (const at of reac.activites) for (const n of at.competences) {
        const ls = plan.lignes.filter((l) => l.seance.cp === n);
        if (ls.length) lignes.push([`AT${at.numero} · CP${n} — ${reac.competence(n).intitule}`, D.fr(ls[0].date), D.fr(ls[ls.length - 1].date), D.fmtDuree(plan.minutes_cp[n]), ((plan.minutes_cp[n] / total) * 100).toFixed(1).replace(".", ",") + " %"]);
      }
      t = tableau(["Compétence", "Début", "Fin", "Heures", "Part"], lignes);
    }
    ap.replaceChildren(t);
  }
  $("onglets").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-v]");
    if (!b || !etat.ctx) return;
    for (const x of $("onglets").children) x.setAttribute("aria-selected", String(x === b));
    vue(b.dataset.v);
  });

  // ----------------------------------------------------------- téléchargements
  let downloads;
  const capacite = () => {
    if (downloads !== undefined) return Promise.resolve(downloads);
    if (!window.claude || typeof window.claude.use !== "function") return Promise.resolve((downloads = null));
    return window.claude.use("downloads").then((d) => (downloads = d), () => (downloads = null));
  };
  async function enregistrer(nom, data) {
    const dl = await capacite();
    if (dl) {
      try { await dl.save({ filename: nom, data }); }
      catch (e) {
        const code = e && e.code;
        if (code === "declined") return;
        if (code === "rate_limited") message("Une demande d'enregistrement est déjà ouverte : répondez-y, puis recommencez.", "alerte");
        else message(`Téléchargement impossible ici (${code || "indisponible"}).`, "ko");
      }
      return;
    }
    if (window.claude) { message("Le téléchargement n'est pas disponible dans cet affichage. Ouvrez l'atelier dans claude.ai.", "ko"); return; }
    // Page ouverte comme fichier autonome : téléchargement classique du navigateur
    const url = URL.createObjectURL(data instanceof Blob ? data : new Blob([data]));
    const a = document.createElement("a");
    a.href = url; a.download = nom; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }
  async function fichier(f) {
    const ctx = etat.ctx, s = ctx.sigle;
    if (!etat.cache[f]) {
      if (f === "xlsx") etat.cache[f] = [`Decorticage_${s}.xlsx`, await D.classeur(ctx)];
      else if (f === "prog") etat.cache[f] = [`Programme_${s}.docx`, await D.programmeDocx(ctx)];
      else if (f === "exam") etat.cache[f] = [`Examen_simplifie_${s}.docx`, await D.examenDocx(ctx)];
      else if (f === "site") etat.cache[f] = [`Page_programme_${s}.html`, new Blob([D.pageSite(ctx)], { type: "text/html" })];
      else if (f === "tout") {
        const parts = [];
        for (const k of ["xlsx", "prog", "exam", "site"]) parts.push(await fichier(k));
        etat.cache[f] = [`Decorticage_${s}_complet.zip`, await D.toutEnZip(ctx, parts)];
      }
    }
    return etat.cache[f];
  }
  $("telech").addEventListener("click", async (e) => {
    const b = e.target.closest("button[data-f]");
    if (!b || !etat.ctx) return;
    const lib = b.firstElementChild.textContent;
    b.disabled = true; b.firstElementChild.textContent = "Préparation…";
    try { const [nom, data] = await fichier(b.dataset.f); await enregistrer(nom, data); }
    catch (err) { message("Erreur pendant la création du fichier : " + (err.message || err), "ko"); }
    finally { b.disabled = false; b.firstElementChild.textContent = lib; }
  });

  // ---------------------------------------------------------------- démarrage
  function exemple() {
    const E = window.EXEMPLE_MEM;
    if (!E) return;
    const reac = D.analyserReac(D.nettoyer(E.reac), E.reac);
    etat.analyse = { reac, re: D.analyserRe(D.nettoyer(E.re), reac), fiche: D.analyserFiche(D.nettoyer(E.fiche)), inconnus: [],
      noms: { reac: "REAC_MEM_V09 (exemple)", re: "REV2_MEM_V09 (exemple)", fiche: "RNCP41853 (exemple)" }, erreurs: [] };
    etat.exemple = true;
    generer();
  }
  chargerCharte();
  exemple();
})();

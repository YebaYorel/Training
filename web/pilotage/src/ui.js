/* Interface du Pilotage YEBA FORMATIONS. Toutes les valeurs affichées passent
 * par esc() (aucune injection HTML possible depuis les données saisies ou importées). */
(function () {
  "use strict";
  const D = window.Decorticage, P = window.Pilotage, C = P.Coffre;
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
  const auj = () => new Date().toISOString().slice(0, 10);
  const fr = (iso) => (iso ? D.fr(D.lireDate(iso)) : "—");
  const jours = (iso) => (iso ? Math.round((D.lireDate(iso) - D.lireDate(auj())) / 86400000) : null);
  const E = P.euros;
  const etat = { vue: "accueil", formationSel: null, actionSel: null, jourSel: null, generation: null, logo: null, dernierEnr: 0 };
  const d = () => C.donnees;

  // ------------------------------------------------------------ persistance
  let minuteur = null;
  function sauver() {
    clearTimeout(minuteur);
    minuteur = setTimeout(async () => { try { await C.enregistrer(); $("#etat-sauvegarde").textContent = "Enregistré " + new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" }); } catch (e) { toast("Enregistrement impossible : " + e.message, "ko"); } }, 400);
  }
  function toast(msg, type = "ok") {
    const t = document.createElement("div");
    t.className = "toast " + type; t.textContent = msg; $("#toasts").appendChild(t);
    while ($("#toasts").children.length > 3) $("#toasts").firstElementChild.remove();   // 3 messages au plus à l'écran
    setTimeout(() => t.remove(), 6000);
  }
  let inactif;
  const reveil = () => { clearTimeout(inactif); inactif = setTimeout(() => { if (C.cle) { C.verrouiller(); afficherConnexion("Verrouillé après 30 minutes d'inactivité."); } }, 30 * 60000); };
  ["click", "keydown"].forEach((ev) => document.addEventListener(ev, reveil));

  // ------------------------------------------------------------ téléchargement
  let dl;
  const capacite = async (n) => (window.claude && typeof window.claude.use === "function" ? window.claude.use(n).catch(() => null) : null);
  async function enregistrer(nom, data) {
    // noms de fichiers sans accents : lisibles partout (Windows, Mac, clé USB, messagerie)
    nom = String(nom).normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^A-Za-z0-9._-]+/g, "_");
    if (dl === undefined) dl = await capacite("downloads");
    if (dl) { try { await dl.save({ filename: nom, data }); } catch (e) { if (e && e.code !== "declined") toast(`Téléchargement impossible (${(e && e.code) || "indisponible"}).`, "ko"); } return; }
    if (window.claude) { toast("Téléchargement indisponible dans cet affichage : ouvrez la page dans claude.ai.", "ko"); return; }
    const url = URL.createObjectURL(data instanceof Blob ? data : new Blob([data]));
    const a = document.createElement("a"); a.href = url; a.download = nom; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 30000);
  }
  async function zip(nom, fichiers) {
    const z = new JSZip();
    for (const [n, b] of fichiers) z.file(n, b instanceof Blob ? await b.arrayBuffer() : b);
    return [nom, await z.generateAsync({ type: "blob", compression: "DEFLATE" })];
  }

  // ------------------------------------------------------------ charte et logo
  function appliquerCharte() {
    const c = d().charte, r = document.documentElement.style;
    r.setProperty("--marque", "#" + c.couleur_primaire); r.setProperty("--accent-marque", "#" + c.couleur_secondaire);
    etat.logo = null;
    const ln = $("#logo-nav"); if (ln) { ln.hidden = !c.logo; if (c.logo) { ln.src = c.logo; ln.alt = d().identite.nom; } }
    if (c.logo) chargerLogo(c.logo);
  }
  function chargerLogo(dataURL) {
    return new Promise((ok) => {
      const img = new Image();
      img.onload = () => {
        const k = Math.min(1, 1200 / Math.max(img.width, img.height)), cv = document.createElement("canvas");
        cv.width = Math.max(1, Math.round(img.width * k)); cv.height = Math.max(1, Math.round(img.height * k));
        cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
        const propre = cv.toDataURL("image/png"), b64 = propre.split(",")[1], bin = atob(b64), oct = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) oct[i] = bin.charCodeAt(i);
        etat.logo = { dataURL: propre, base64: b64, ext: "png", octets: oct, ratio: cv.width / cv.height };
        ok(propre);
      };
      img.onerror = () => ok(null);
      img.src = dataURL;
    });
  }
  const charteDoc = (nom) => Object.assign({ nom_organisme: nom || d().identite.nom }, d().charte);

  // ------------------------------------------------------------ connexion
  async function afficherConnexion(message) {
    $("#app").hidden = true; $("#connexion").hidden = false;
    const existe = await C.existe();
    $("#connexion").innerHTML = `
      <div class="carte-connexion">
        ${window.LOGO_YEBA ? `<img class="logo-connexion" src="${window.LOGO_YEBA}" alt="YEBA FORMATIONS">` : ""}
        <span class="etiquette">Pilotage du centre de formation</span>
        <h1>${existe ? "Déverrouiller" : "Créer votre coffre"}</h1>
        <p>${existe ? "Vos données sont chiffrées dans ce navigateur. Saisissez votre mot de passe." : "Toutes vos données (formations, actions, finances, Qualiopi) seront chiffrées avec ce mot de passe et resteront dans ce navigateur. Sans lui, personne ne peut les lire, pas même vous : notez-le en lieu sûr."}</p>
        ${message ? `<div class="message alerte">${esc(message)}</div>` : ""}
        <form id="f-connexion" class="pile">
          <label>Mot de passe<input id="mdp" type="password" autocomplete="${existe ? "current-password" : "new-password"}" required></label>
          ${existe ? "" : `<label>Confirmer<input id="mdp2" type="password" autocomplete="new-password" required></label>`}
          <button class="principal" type="submit">${existe ? "Ouvrir" : "Créer le coffre"}</button>
        </form>
        <details><summary>Restaurer une sauvegarde (autre ordinateur)</summary>
          <div class="pile"><label>Fichier de sauvegarde (.json)<input id="f-restaurer" type="file" accept=".json"></label>
          <label>Mot de passe de la sauvegarde<input id="mdp-restaurer" type="password"></label>
          <button type="button" class="second" id="b-restaurer">Restaurer</button></div></details>
      </div>`;
    $("#f-connexion").onsubmit = async (e) => {
      e.preventDefault();
      const m = $("#mdp").value;
      try {
        if (existe) await C.ouvrir(m);
        else { if (m !== $("#mdp2").value) throw new Error("Les deux mots de passe diffèrent."); await C.creer(m, P.initiales()); }
        demarrer();
      } catch (err) { afficherConnexion(err.message); }
    };
    $("#b-restaurer").onclick = async () => {
      const f = $("#f-restaurer").files[0];
      if (!f) return;
      try { await C.importer(await f.text(), $("#mdp-restaurer").value); demarrer(); } catch (err) { afficherConnexion(err.message); }
    };
    setTimeout(() => $("#mdp") && $("#mdp").focus(), 50);
  }
  function demarrer() {
    $("#connexion").hidden = true; $("#app").hidden = false;
    P.migrer(d()); P.synchroAttendus(d());
    appliquerCharte(); reveil();
    aller(location.hash.slice(1) || "accueil");
  }

  // ------------------------------------------------------------ navigation
  const VUES = { accueil: "Aujourd'hui", formations: "Formations", seance: "Séance", actions: "Actions", qualiopi: "Qualiopi", finances: "Finances", partenaires: "Partenaires", reglages: "Réglages" };
  function aller(v) {
    if (!VUES[v]) v = "accueil";
    etat.vue = v;
    if (location.hash.slice(1) !== v) history.replaceState(null, "", "#" + v);
    document.querySelectorAll("#nav a").forEach((a) => a.setAttribute("aria-current", a.dataset.v === v ? "page" : "false"));
    rendre();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", () => C.cle && aller(location.hash.slice(1)));
  function rendre() {
    const v = etat.vue, zone = $("#vue");
    zone.innerHTML = ({ accueil: vAccueil, formations: vFormations, seance: vSeance, actions: vActions, qualiopi: vQualiopi, finances: vFinances, partenaires: vPartenaires, reglages: vReglages })[v]();
    const apres = ({ formations: aFormations, seance: aSeance, actions: aActions, qualiopi: aQualiopi, finances: aFinances, partenaires: aPartenaires, reglages: aReglages, accueil: aAccueil })[v];
    if (apres) apres();
  }

  // ------------------------------------------------------------ calculs partagés
  function contexteF(f) { return Object.assign(P.contexteFormation(f, charteDoc(f.reglages.commanditaire), etat.logo), { pied: f.reglages.commanditaire ? "" : P.blocMarque(d().identite) }); }
  function prochaineSeance(f) {
    try { const ctx = contexteF(f), pr = P.planReel(f, ctx); return { ctx, pr, jour: P.journee(pr.futur) }; } catch (e) { return { erreur: e.message }; }
  }
  function aFaire() {
    const liste = [];
    for (const a of d().actions) {
      if (a.statut === "annulee") continue;
      for (const doc of P.documentsAttendus(a)) {
        if (doc.etat === "fait" || doc.etat === "na" || !doc.limite) continue;
        const j = jours(doc.limite);
        if (j <= 14) liste.push({ quand: doc.limite, j, texte: `${doc.titre} — ${a.intitule}`, action: a.id, type: "doc" });
      }
    }
    for (const x of d().attendus) if (P.etatAttendu(x) === "retard") liste.push({ quand: x.echeance, j: jours(x.echeance), texte: `Paiement en retard — ${x.payeur} : ${E(P.reste(x))} (${x.libelle})`, type: "paiement" });
    const nb = d().mouvements.filter((m) => m.etat === "a_confirmer").length;
    if (nb) liste.push({ quand: auj(), j: 0, texte: `${nb} virement(s) reçu(s) à confirmer`, type: "paiement" });
    for (const p of d().partenaires) if (p.relance && jours(p.relance) <= 3) liste.push({ quand: p.relance, j: jours(p.relance), texte: `Relancer ${p.nom}${p.objet ? " — " + p.objet : ""}`, partenaire: p.id, type: "relance" });
    const derniereVeille = d().veille.map((x) => x.date).sort().pop();
    if (!derniereVeille || jours(derniereVeille) < -30) liste.push({ quand: auj(), j: 0, texte: "Veille du mois à noter (Qualiopi 23, 24, 25)", type: "veille" });
    const derniereSauv = d().derniere_sauvegarde;
    if (!derniereSauv || jours(derniereSauv.slice(0, 10)) < -7) liste.push({ quand: auj(), j: 0, texte: "Faire une sauvegarde chiffrée (plus de 7 jours)", type: "sauvegarde" });
    const I = d().identite;
    if (I.qualiopi_validite && jours(I.qualiopi_validite) <= 120) liste.push({ quand: I.qualiopi_validite, j: jours(I.qualiopi_validite), texte: `Certificat Qualiopi valable jusqu'au ${fr(I.qualiopi_validite)} : vérifier la date de l'audit de renouvellement avec ${I.certificateur || "le certificateur"}`, type: "qualiopi" });
    return liste.sort((x, y) => x.quand.localeCompare(y.quand));
  }
  function couvertureQualiopi() {
    const q = d().qualiopi, tous = P.QUALIOPI.concat(q.ajouts || []);
    const concernes = tous.filter((i) => !(q.suivi[i.n] && q.suivi[i.n].na));
    const prets = concernes.filter((i) => q.suivi[i.n] && q.suivi[i.n].statut === "pret");
    return { total: concernes.length, prets: prets.length, taux: concernes.length ? prets.length / concernes.length : 0 };
  }

  // ------------------------------------------------------------ ACCUEIL
  function vAccueil() {
    const t = P.tresorerie(d()), tb = P.tableauBord(d()), q = couvertureQualiopi(), liste = aFaire();
    const audit = jours(d().identite.audit_debut);
    const cartesSeances = d().formations.filter((f) => !f.archivee).map((f) => {
      const ps = prochaineSeance(f);
      if (ps.erreur || !ps.jour) return `<div class="carte"><h3>${esc(f.titre)}</h3><p class="discret">${esc(ps.erreur || "Toutes les séances sont réalisées.")}</p></div>`;
      const objs = [...new Set(ps.jour.lignes.map((l) => l.objectif.texte))];
      const pack = f.packs && f.packs[ps.jour.date];
      return `<div class="carte seance-carte"><span class="etiquette">Prochaine séance · ${esc(D.JOURS[D.jourSem(D.lireDate(ps.jour.date))])} ${fr(ps.jour.date)} · ${D.fmtDuree(ps.jour.minutes)}</span>
        <h3>${esc(f.titre)}</h3><ul class="objs">${objs.slice(0, 5).map((o) => `<li>${verbe(o)}</li>`).join("")}${objs.length > 5 ? `<li class="discret">+ ${objs.length - 5} autres</li>` : ""}</ul>
        <div class="actions"><button data-act="ouvrir-seance" data-f="${esc(f.id)}" data-d="${esc(ps.jour.date)}" class="${pack ? "second" : "principal-court"}">${pack ? "Voir la séance préparée" : "Préparer la séance"}</button>
        <button class="second" data-act="noter-seance" data-f="${esc(f.id)}" data-d="${esc(ps.jour.date)}">Séance terminée : noter</button></div>
        ${ps.pr.ecartJours > 0 ? `<p class="message alerte">Retard cumulé : la fin de formation est décalée de ${ps.pr.ecartJours} jours (fin prévue le ${D.fr(ps.pr.finReelle)}).</p>` : ""}</div>`;
    }).join("") || `<div class="carte vide"><h3>Aucune formation</h3><p>Ajoutez une formation à partir de ses référentiels (REAC, RE/RC, fiche RNCP ou RS) pour voir ici vos prochaines séances.</p><button data-go="formations" class="principal-court">Ajouter une formation</button></div>`;
    return `<header class="titre-vue"><h1>Aujourd'hui</h1><p>${esc(new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" }))}</p></header>
      <div class="tuiles">
        ${tuile("Ce que j'ai aujourd'hui", E(tb.solde), t.autonomieJours !== null ? `${t.autonomieJours} jours d'autonomie` : "solde bancaire", t.sousSeuil ? "alerte" : "", "finances")}
        ${tuile("Ce qu'on me doit", E(tb.du), tb.nbRetard ? `dont ${E(tb.retard)} en retard` : `${tb.nbDu} somme(s) attendue(s)`, tb.nbRetard ? "alerte" : "", "finances")}
        ${tuile("Qualiopi", `${Math.round(q.taux * 100)} %`, `${q.prets}/${q.total} indicateurs prêts${audit !== null ? ` · audit dans ${audit} j` : ""}`, q.taux < 0.5 && audit !== null && audit < 120 ? "alerte" : "", "qualiopi")}
        ${tb.aConfirmer ? tuile("Virements à confirmer", String(tb.aConfirmer), "reçus sur le compte", "alerte", "finances") : tuile("Actions en cours", String(d().actions.filter((a) => ["convention_signee", "en_cours"].includes(a.statut)).length), `${d().actions.length} au total`, "", "actions")}
      </div>
      <div class="deux-colonnes"><section><h2>Séances</h2><div class="pile">${cartesSeances}</div></section>
      <section><h2>À faire (14 prochains jours)</h2>${liste.length ? `<ul class="todo">${liste.map((x) => `<li class="${x.j < 0 ? "retard" : x.j <= 2 ? "proche" : ""}"><span class="quand">${x.j < 0 ? `en retard de ${-x.j} j` : x.j === 0 ? "aujourd'hui" : `dans ${x.j} j`}</span><span>${esc(x.texte)}</span>${x.action ? `<button class="lien" data-act="voir-action" data-id="${esc(x.action)}">Ouvrir</button>` : x.type === "veille" || x.type === "qualiopi" ? `<button class="lien" data-go="qualiopi">Ouvrir</button>` : x.type === "paiement" ? `<button class="lien" data-go="finances">Voir</button>` : x.type === "sauvegarde" ? `<button class="lien" data-go="reglages">Sauvegarder</button>` : x.partenaire ? `<button class="lien" data-go="partenaires">Voir</button>` : ""}</li>`).join("")}</ul>` : `<p class="discret">Rien d'urgent. Profitez-en pour démarcher vos partenaires.</p>`}
      ${tresorerieSvg(t)}</section></div>`;
  }
  const tuile = (lib, val, sous, cls, go) => `<button class="tuile ${cls}" data-go="${go}"><span>${esc(lib)}</span><b>${esc(val)}</b><small>${esc(sous)}</small></button>`;
  const verbe = (o) => { const v = D.verbeInitial(o); return `<b class="verbe">${esc(v)}</b>${esc(o.slice(v.length))}`; };
  function tresorerieSvg(t) {
    if (!t.courbe.length) return "";
    const W = 560, H = 160, vals = t.courbe.map((c) => c.solde), min = Math.min(0, ...vals), max = Math.max(1, ...vals);
    const x = (i) => 40 + (i * (W - 50)) / Math.max(1, t.courbe.length - 1), y = (v) => 10 + ((max - v) * (H - 40)) / (max - min || 1);
    const pts = t.courbe.map((c, i) => `${x(i).toFixed(1)},${y(c.solde).toFixed(1)}`).join(" ");
    return `<figure class="graphe"><figcaption>Trésorerie prévue sur 90 jours (encaissements attendus, dépenses prévues, charges moyennes)</figcaption>
      <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Courbe de trésorerie prévisionnelle">
        <line x1="40" x2="${W - 10}" y1="${y(0)}" y2="${y(0)}" class="axe"/>
        <polyline points="${pts}" class="courbe"/>
        ${t.courbe.map((c, i) => (i % 3 === 0 ? `<text x="${x(i)}" y="${H - 8}" class="lib" text-anchor="middle">${fr(c.date).slice(0, 5)}</text>` : "")).join("")}
        <text x="36" y="${y(max) + 4}" class="lib" text-anchor="end">${Math.round(max)}</text><text x="36" y="${y(min) + 4}" class="lib" text-anchor="end">${Math.round(min)}</text>
        <circle cx="${x(t.courbe.indexOf(t.pointBas))}" cy="${y(t.pointBas.solde)}" r="5" class="point"/></svg>
      <p class="discret">Point bas : ${E(t.pointBas.solde)} le ${fr(t.pointBas.date)}.</p></figure>`;
  }
  function aAccueil() { lierCommun(); }

  // ------------------------------------------------------------ FORMATIONS
  const RYTHMES = { "1": "1 jour par semaine", "2": "2 jours par semaine", "3": "3 jours par semaine", "4": "4 jours par semaine", "5": "5 jours par semaine (lundi à vendredi)" };
  function champsReglages(r) {
    const jours = new Set(((r.jours || "1,2,3,4,5").match(/[1-7]/g) || []));
    const nomsJ = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"];
    return `<div class="grille-champs">
      <label>Durée en centre (heures)<input name="heures_centre" type="number" min="1" step="0.5" value="${esc(r.heures_centre || "")}" required><small>Fixée par la convention</small></label>
      <label>Date de début<input name="date_debut" type="date" value="${esc(r.date_debut || "")}" required></label>
      <fieldset class="jours"><legend>Jours de formation dans la semaine</legend>${nomsJ.map((n, i) => `<label class="coche"><input type="checkbox" name="jour" value="${i + 1}" ${jours.has(String(i + 1)) ? "checked" : ""}>${n}</label>`).join("")}
        <small>Exemple : un seul jour par semaine → cochez uniquement ce jour (ex. Mardi).</small></fieldset>
      <label>Alternance par semaines (facultatif)<input name="rythme" value="${esc(r.rythme || "")}" placeholder="ex. CCEE"><small>C = semaine en centre, E = semaine en entreprise</small></label>
      <label>Horaires<input name="creneaux" value="${esc(r.creneaux || "08:30-12:00, 13:00-16:30")}"></label>
      <label>Pauses (non comptées)<input name="pauses" value="${esc(r.pauses ?? "10:15-10:30, 14:45-15:00")}"></label>
      <label class="large">Fermetures et jours annulés<input name="fermetures" value="${esc(r.fermetures || "")}" placeholder="2027-02-15..2027-02-19 Vacances ; 2027-03-09 Alerte rouge"></label>
      <label>Pour un autre centre ?<input name="commanditaire" value="${esc(r.commanditaire || "")}" placeholder="ICCI, TETRANERGY…"><small>Si rempli : YEBA FORMATIONS et le logo disparaissent</small></label>
      <label>Public<input name="public" value="${esc(r.public || "")}"></label>
      <label>Date d'examen<input name="date_examen" type="date" value="${esc(r.date_examen || "")}"></label>
      <label>Ordre des compétences<input name="ordre_cp" value="${esc(r.ordre_cp || "")}" placeholder="ex. 5,6,7,1,2,3,4,8,9,10"></label></div>`;
  }
  function lireReglages(form, base) {
    const fd = new FormData(form), r = Object.assign({ h_accueil: 7, h_ecf_par_at: 3.5, h_dossier_pro: 14, h_productions: 21, h_examen_blanc: 0, h_bilan: 3.5, afficher_logo: true, afficher_nom: true,
      modalites_pedagogiques: "Présentiel, pédagogie active : apports, études de cas, mises en situation, jeux de rôle", poids_cp: "", heures_entreprise: 0, prerequis: "", lieu: "", delai_acces: "", referent_handicap: d().identite.referent_handicap }, base || {});
    for (const k of ["heures_centre", "date_debut", "rythme", "creneaux", "pauses", "fermetures", "commanditaire", "public", "date_examen", "ordre_cp"]) r[k] = String(fd.get(k) ?? "").slice(0, 2000);
    r.heures_centre = Math.max(0, parseFloat(String(r.heures_centre).replace(",", ".")) || 0);
    r.jours = fd.getAll("jour").join(",") || "1,2,3,4,5";
    return r;
  }
  function vFormations() {
    const f = d().formations.find((x) => x.id === etat.formationSel);
    if (f) return vFormation(f);
    return `<header class="titre-vue"><h1>Formations</h1><p>Chaque formation part de ses référentiels. Le planning est une hypothèse : il se recale à chaque séance notée.</p></header>
      <div class="pile">${d().formations.map((x) => { const ps = prochaineSeance(x); const pct = ps.pr ? Math.round((ps.pr.minutesFaites / ps.pr.total) * 100) : 0;
        return `<button class="ligne-liste" data-act="ouvrir-formation" data-id="${esc(x.id)}"><b>${esc(x.titre)}</b><span>${esc(x.code || "")} · ${esc(RYTHMES[(x.reglages.jours.match(/[1-7]/g) || []).length] || "")}</span><span class="jauge"><i style="width:${pct}%"></i></span><span>${pct} % réalisé</span></button>`; }).join("") || `<p class="discret">Aucune formation pour l'instant.</p>`}</div>
      <section class="carte"><h2>Ajouter une formation</h2>
        <form id="f-formation" class="pile">
          <label>Référentiels (REAC indispensable, RE/RC, fiche RNCP ou RS)<input id="docs" type="file" multiple accept=".pdf,.docx,.xlsx,.txt" required></label>
          <ul id="docs-etat" class="puces-docs"></ul>
          ${champsReglages({ jours: "2", date_debut: "", heures_centre: "" })}
          <button class="principal" type="submit">Décortiquer et planifier</button>
        </form></section>`;
  }
  function vFormation(f) {
    const ps = prochaineSeance(f);
    if (ps.erreur) return `<button class="lien" data-act="retour-formations">← Formations</button><div class="message ko">${esc(ps.erreur)}</div>`;
    const { ctx, pr } = ps, pct = Math.round((pr.minutesFaites / pr.total) * 100);
    const parJour = new Map();
    for (const l of pr.futur) { const k = D.iso(l.date); if (!parJour.has(k)) parJour.set(k, []); parJour.get(k).push(l); }
    const prochains = [...parJour.entries()].slice(0, 12);
    return `<button class="lien" data-act="retour-formations">← Formations</button>
      <header class="titre-vue"><h1>${esc(f.titre)}</h1><p>${esc(f.code || "")} · ${ctx.reac.activites.length} activités types · ${ctx.reac.competences.length} compétences · ${D.fmtDuree(pr.total)} en centre</p></header>
      <div class="tuiles">${tuile("Réalisé", pct + " %", `${D.fmtDuree(pr.minutesFaites)} sur ${D.fmtDuree(pr.total)}`, "", "formations")}
        ${tuile("Fin prévue", pr.finReelle ? D.fr(pr.finReelle) : "—", pr.ecartJours > 0 ? `retard de ${pr.ecartJours} jours` : "dans les temps", pr.ecartJours > 0 ? "alerte" : "", "formations")}
        ${tuile("Séances préparées", String(Object.keys(f.packs || {}).length), "avec preuves", "", "formations")}
        ${tuile("Journées notées", String((f.journal || []).length), "", "", "formations")}</div>
      <section class="carte"><h2>Prochaines journées (planning recalé)</h2><div class="defile"><table><thead><tr><th>Date</th><th>Séances et objectifs</th><th>Durée</th><th></th></tr></thead><tbody>
        ${prochains.map(([k, ls]) => `<tr><td>${esc(D.JOURS[D.jourSem(D.lireDate(k))].slice(0, 3))} ${fr(k)}</td><td>${[...new Set(ls.map((l) => `S${l.seance.numero} — ${l.seance.titre}`))].map(esc).join("<br>")}</td><td>${D.fmtDuree(ls.reduce((t, l) => t + l.minutes, 0))}</td>
          <td><button class="lien" data-act="ouvrir-seance" data-f="${esc(f.id)}" data-d="${esc(k)}">${f.packs && f.packs[k] ? "Séance prête" : "Préparer"}</button></td></tr>`).join("")}</tbody></table></div></section>
      <section class="carte"><h2>Documents du titre</h2><div class="actions">
        <button data-act="exp-f" data-k="xlsx" class="second">Décorticage complet (.xlsx)</button><button data-act="exp-f" data-k="prog" class="second">Programme (.docx)</button>
        <button data-act="exp-f" data-k="exam" class="second">Examen simplifié (.docx)</button><button data-act="exp-f" data-k="tout" class="second">Tout + agenda (.zip)</button></div></section>
      <section class="carte"><h2>Journal des séances réalisées</h2>${(f.journal || []).length ? `<ul class="todo">${f.journal.slice().reverse().map((j) => `<li><span class="quand">${fr(j.date)}</span><span>${D.fmtDuree(Object.values(j.faits).reduce((a, b) => a + b, 0))} réalisées sur ${D.fmtDuree(j.prevu || 0)} prévues${j.notes ? " — " + esc(j.notes) : ""}</span><button class="lien" data-act="annuler-journal" data-d="${esc(j.date)}">Annuler</button></li>`).join("")}</ul>` : `<p class="discret">Aucune séance notée.</p>`}</section>
      <details class="carte"><summary>Modifier le calendrier et les réglages</summary><form id="f-regl" class="pile">${champsReglages(f.reglages)}<button type="submit" class="principal-court">Enregistrer et recalculer</button></form></details>
      <p><button class="lien danger" data-act="suppr-formation">Supprimer cette formation</button></p>`;
  }
  function aFormations() {
    lierCommun();
    const form = $("#f-formation");
    if (form) form.onsubmit = async (e) => {
      e.preventDefault();
      const fichiers = [...$("#docs").files].slice(0, 10);
      const ul = $("#docs-etat"); ul.innerHTML = "";
      const lus = [];
      for (const fi of fichiers) {
        const li = document.createElement("li"); li.textContent = `${fi.name} : lecture…`; ul.appendChild(li);
        try { const r = await D.lireFichier(fi), t = D.detecterType(r.texte); lus.push([fi.name, r, t]); li.textContent = `${fi.name} : ${({ REAC: "REAC", RE: "RE / RC", FICHE: "fiche France Compétences", INCONNU: "non reconnu" })[t]}`; li.className = t === "INCONNU" ? "ko" : "ok"; }
        catch (err) { li.textContent = `${fi.name} : ${err.message}`; li.className = "ko"; }
      }
      const reac = lus.find((x) => x[2] === "REAC");
      if (!reac) { toast("Aucun REAC reconnu : il est indispensable.", "ko"); return; }
      const f = { id: uid(), textes: { reac: reac[1].brut, re: (lus.find((x) => x[2] === "RE") || [])[1]?.brut || "", fiche: (lus.find((x) => x[2] === "FICHE") || [])[1]?.brut || "" },
        noms: Object.fromEntries(lus.map(([n, , t]) => [t.toLowerCase(), n])), reglages: lireReglages(form), journal: [], packs: {}, cree: auj() };
      try {
        const ctx = contexteF(f);
        f.titre = ctx.titre; f.code = ctx.fiche ? ctx.fiche.code : ctx.reac.code_titre;
        delete f._analyse;
        d().formations.push(f); sauver(); etat.formationSel = f.id; rendre();
        toast(`Formation ajoutée : ${ctx.plan.seances.length} séances planifiées jusqu'au ${D.fr(ctx.plan.date_fin)}.`);
      } catch (err) { toast(err.message, "ko"); }
    };
    const fr_ = $("#f-regl");
    if (fr_) fr_.onsubmit = (e) => { e.preventDefault(); const f = formationCourante(); f.reglages = lireReglages(fr_, f.reglages); delete f._analyse; sauver(); rendre(); toast("Calendrier recalculé."); };
  }
  const formationCourante = () => d().formations.find((x) => x.id === etat.formationSel);
  const sansCache = (f) => { const c = Object.assign({}, f); delete c._analyse; return c; };

  // ------------------------------------------------------------ SÉANCE
  function vSeance() {
    const f = d().formations.find((x) => x.id === etat.formationSel);
    if (!f || !etat.jourSel) return `<header class="titre-vue"><h1>Séance</h1></header><p>Choisissez une séance depuis l'accueil ou une formation.</p>`;
    const ps = prochaineSeance(f), jour = ps.pr && P.journee(ps.pr.futur, etat.jourSel);
    const pack = f.packs && f.packs[etat.jourSel];
    if (!jour && !pack) return `<button class="lien" data-go="accueil">← Aujourd'hui</button><p class="message alerte">Cette journée n'est plus au planning (déjà notée ou recalée). Ouvrez la prochaine séance depuis l'accueil.</p>`;
    const objs = jour ? [...new Map(jour.lignes.map((l) => [l.objectif, l])).values()] : [];
    const gen = etat.generation;
    return `<button class="lien" data-go="accueil">← Aujourd'hui</button>
      <header class="titre-vue"><span class="etiquette">${esc(f.titre)}</span><h1>Séance du ${esc(D.JOURS[D.jourSem(D.lireDate(etat.jourSel))])} ${fr(etat.jourSel)}</h1>
      ${jour ? `<p>${D.fmtHm(jour.lignes[0].debut)} – ${D.fmtHm(jour.lignes[jour.lignes.length - 1].fin)} · ${D.fmtDuree(jour.minutes)} · ${[...new Set(jour.seances.map((s) => s.cp).filter(Boolean))].map((n) => "CP" + n).join(", ") || "modules transverses"}</p>` : ""}</header>
      <div class="deux-colonnes"><section class="carte"><h2>Objectifs du décorticage (REAC)</h2>
        <ul class="objs">${objs.map((l) => `<li>${verbe(l.objectif.texte)} <small class="discret">· ${D.fmtDuree(jour.lignes.filter((x) => x.objectif === l.objectif).reduce((t, x) => t + x.minutes, 0))}</small></li>`).join("")}</ul>
        ${jour ? `<form id="f-noter" class="pile"><h3>Séance terminée ? Notez ce qui a été fait</h3>${objs.map((l) => { const k = P.cleObjectif(l.seance, l.objectif);
          return `<div class="choix-etat"><span>${esc(l.objectif.texte)}</span><select name="${esc(k)}" aria-label="État"><option value="fait">Fait</option><option value="partiel">À moitié</option><option value="non">Pas fait</option></select></div>`; }).join("")}
          <label>Remarques (retards, adaptations, ressenti du groupe)<textarea name="notes" rows="2"></textarea></label>
          <label class="coche"><input type="checkbox" name="suivante" checked>Préparer automatiquement la séance suivante</label>
          <button class="principal-court" type="submit">Enregistrer la séance réalisée</button></form>` : ""}</section>
      <section class="carte"><h2>Outils de la séance</h2>
        ${pack ? `<p class="message ${pack.source === "claude" ? "ok" : "alerte"}">${pack.source === "claude" ? "Séance rédigée avec Claude le " + fr(pack.cree) + ". Relisez avant diffusion." : "Version de base (sans Claude) : " + esc(pack.raison || "") + ". Enrichissez-la ou relancez la rédaction."}</p>
          <h3>${esc(pack.contenu.titre)}</h3><ol class="objs">${pack.contenu.objectifs_seance.map((o) => `<li>${verbe(o)}</li>`).join("")}</ol>
          <p class="discret">${pack.contenu.diapositives.length} diapositives · ${pack.contenu.exercices.length} exercices · ressource de ${pack.contenu.ressource.sections.length} parties · grille de ${pack.contenu.grille.length} objectifs · quiz de ${pack.contenu.quiz.length} questions</p>
          <div class="telech">${[["tout", "Tout le dossier de séance (.zip)"], ["pptx", "Diaporama de séance (.pptx)"], ["exo", "Exercices apprenants (.docx)"], ["ress", "L'essentiel de la journée — apprenants (.docx)"],
            ["grille", "Grille critériée, 5 objectifs (.docx)"], ["quiz", "Quiz 10 questions — FORMATEUR (.docx)"], ["fiche", "Fiche de séance — preuve Qualiopi (.docx)"]].map(([k, l]) => `<button data-act="dl-pack" data-k="${k}" class="${k === "tout" ? "principal" : "second"}">${esc(l)}</button>`).join("")}</div>` : ""}
        ${jour ? `<div class="actions"><button class="${pack ? "second" : "principal-court"}" data-act="generer" ${gen ? "disabled" : ""}>${pack ? "Rédiger à nouveau avec Claude" : "Préparer la séance avec Claude"}</button>${gen ? `<button class="second" data-act="stop">Arrêter</button>` : ""}</div>
          <p id="gen-etat" class="discret" aria-live="polite">${gen ? esc(gen.message) : "Claude rédige le contenu à partir des objectifs ci-contre ; le logiciel fabrique les fichiers. Comptez 1 à 3 minutes."}</p>` : ""}
      </section></div>`;
  }
  async function genererSeance(f, date, silencieux) {
    if (etat.generation) return;
    const ps = prochaineSeance(f), jour = P.journee(ps.pr.futur, date);
    if (!jour) return;
    const ctl = new AbortController();
    etat.generation = { ctl, message: "Claude réfléchit… (la première fois, autorisez l'accès à Claude)" };
    if (etat.vue === "seance") rendre();
    let car = 0;
    try {
      const r = await P.redigerSeance(ps.ctx, jour, { public: f.reglages.public, signal: ctl.signal, onText: ({ text }) => { car = text.length; const e = $("#gen-etat"); if (e) e.textContent = `Claude rédige… ${car.toLocaleString("fr-FR")} caractères`; } });
      f.packs = f.packs || {};
      f.packs[date] = { date, titre: r.pack.titre, contenu: r.pack, source: r.source, raison: r.raison || "", cree: auj(), objectifs_reac: r.matiere.objectifs.map((o) => o.objectif) };
      sauver();
      toast(r.source === "claude" ? `Séance du ${fr(date)} prête.` : `Séance du ${fr(date)} : version de base (${r.raison}).`, r.source === "claude" ? "ok" : "alerte");
    } catch (e) { if (!(e && e.code === "cancelled")) toast("Rédaction interrompue.", "ko"); }
    finally { etat.generation = null; if (etat.vue === "seance" || !silencieux) rendre(); }
  }
  async function fichiersPack(f, date) {
    const pack = f.packs[date], ps = prochaineSeance(f);
    let jour = ps.pr && P.journee(ps.pr.futur, date);
    if (!jour) {   // séance déjà réalisée : on reconstitue la journée à partir du planning initial
      const lignes = ps.ctx.plan.lignes.filter((l) => D.iso(l.date) === date);
      jour = lignes.length ? { date, lignes, seances: [...new Set(lignes.map((l) => l.seance))], minutes: lignes.reduce((t, l) => t + l.minutes, 0) } : null;
    }
    if (!jour) throw new Error("Journée introuvable dans le planning.");
    return P.fabriquerSeance(ps.ctx, jour, pack.contenu, f.reglages.commanditaire ? null : etat.logo, d().identite);
  }
  function aSeance() {
    lierCommun();
    const f = d().formations.find((x) => x.id === etat.formationSel), form = $("#f-noter");
    if (form) form.onsubmit = (e) => {
      e.preventDefault();
      const ps = prochaineSeance(f), jour = P.journee(ps.pr.futur, etat.jourSel), fd = new FormData(form), etats = {};
      for (const l of jour.lignes) { const k = P.cleObjectif(l.seance, l.objectif); etats[k] = fd.get(k) || "fait"; }
      P.noterJournee(f, jour, etats, String(fd.get("notes") || "").slice(0, 2000));
      const suivante = fd.get("suivante");
      sauver();
      const nps = prochaineSeance(f);
      toast(`Séance notée.${nps.pr.ecartJours > 0 ? ` Planning recalé : fin le ${D.fr(nps.pr.finReelle)}.` : ""}`);
      if (nps.jour) { etat.jourSel = nps.jour.date; rendre(); if (suivante && !(f.packs && f.packs[nps.jour.date])) genererSeance(f, nps.jour.date); }
      else aller("formations");
    };
  }

  // ------------------------------------------------------------ ACTIONS
  const STATUTS = { prospect: "Prospect", devis: "Devis envoyé", convention_signee: "Convention signée", en_cours: "En cours", terminee: "Terminée", facturee: "Facturée", soldee: "Soldée", annulee: "Annulée" };
  function vActions() {
    const a = d().actions.find((x) => x.id === etat.actionSel);
    if (a) return vAction(a);
    return `<header class="titre-vue"><h1>Actions de formation</h1><p>Une action = une mission (convention, stagiaires, documents, facture). Saisissez-la une fois : tous les documents se remplissent.</p></header>
      <div class="actions"><button class="principal-court" data-act="nouvelle-action">Nouvelle action</button></div>
      <div class="defile"><table><thead><tr><th>Action</th><th>Client / donneur d'ordre</th><th>Dates</th><th>Montant HT</th><th>Statut</th><th>Documents</th></tr></thead><tbody>
      ${d().actions.slice().sort((x, y) => (y.debut || "").localeCompare(x.debut || "")).map((x) => { const docs = P.documentsAttendus(x), faits = docs.filter((k) => k.etat === "fait" || k.etat === "na").length;
        return `<tr><td><button class="lien" data-act="voir-action" data-id="${esc(x.id)}">${esc(x.intitule || "(sans titre)")}</button><br><small class="discret">${esc(P.TYPES_ACTION[x.type] || "")}</small></td><td>${esc(x.pour_centre || x.client?.raison || "")}</td><td>${fr(x.debut)} → ${fr(x.fin)}</td><td>${E(x.prix_ht)}</td><td><span class="puce ${x.statut === "soldee" ? "ok" : x.statut === "annulee" ? "ko" : "att"}">${esc(STATUTS[x.statut] || "")}</span></td><td>${faits}/${docs.length}</td></tr>`; }).join("") || `<tr><td colspan="6" class="discret">Aucune action. Créez votre première mission.</td></tr>`}</tbody></table></div>`;
  }
  const opt = (obj, val) => Object.entries(obj).map(([k, l]) => `<option value="${esc(k)}" ${k === val ? "selected" : ""}>${esc(l)}</option>`).join("");
  const champ = (lib, nom, val, type = "text", extra = "") => `<label>${esc(lib)}<input name="${nom}" type="${type}" value="${esc(val ?? "")}" ${extra}></label>`;
  function vAction(a) {
    const docs = P.documentsAttendus(a), cli = a.client || {}, ttc = P.totalTTC(a);
    const formations = Object.fromEntries([["", "— aucune —"]].concat(d().formations.map((f) => [f.id, f.titre])));
    const pieces = (a.pieces || []).map((id) => [id, (d().fichiers || {})[id]]).filter(([, m]) => m);
    return `<button class="lien" data-act="retour-actions">← Actions</button>
      <form id="f-action" class="pile"><header class="titre-vue"><h1>${esc(a.intitule || "Nouvelle action")}</h1>
        <p>${esc(STATUTS[a.statut] || "")} · ${E(a.prix_ht)} HT${a.tva === "tva" ? ` · ${E(ttc)} TTC` : ""}</p></header>
      <section class="carte"><h2>L'action</h2><div class="grille-champs">
        ${champ("Intitulé", "intitule", a.intitule, "text", "required")}
        <label>Formation (décorticage)<select name="formationId">${opt(formations, a.formationId || "")}</select></label>
        <label>Type<select name="type">${opt(P.TYPES_ACTION, a.type)}</select></label>
        <label>Statut<select name="statut">${opt(STATUTS, a.statut)}</select></label>
        ${champ("Réalisée pour un autre centre (sous-traitance)", "pour_centre", a.pour_centre, "text", 'placeholder="ICCI, GEM FORMATION…"')}
        <label>Financeur (origine BPF)<select name="origine">${opt(P.ORIGINES, a.origine)}</select></label>
        <label>Nature<select name="nature">${opt({ formation: "Action de formation", conseil: "Conseil, audit (RGPD, IA Act)", implementation: "Implémentation IA / workflow" }, a.nature || "formation")}</select><small>Le conseil n'est jamais exonéré de TVA</small></label>
        ${champ("Début", "debut", a.debut, "date")}${champ("Fin", "fin", a.fin, "date")}
        ${champ("Jours de formation (1 = lundi)", "jours_semaine", a.jours_semaine || "1,2,3,4,5")}${champ("Horaires", "horaires", a.horaires || "08:30-12:00, 13:00-16:30")}
        ${champ("Lieu", "lieu", a.lieu)}${champ("Heures par stagiaire", "heures", a.heures, "number", 'step="0.5" min="0"')}
        ${champ("Objectifs (résumé)", "objectifs", a.objectifs)}${champ("Frais à avancer (déplacements, salle…)", "frais_prevus", a.frais_prevus, "number", 'step="0.01" min="0"')}</div></section>
      <section class="carte"><h2>Client ou financeur</h2><div class="grille-champs">
        ${champ("Raison sociale", "c_raison", cli.raison)}${champ("SIRET", "c_siret", cli.siret)}${champ("Adresse", "c_adresse", cli.adresse)}
        ${champ("Représentant (nom, fonction)", "c_contact", cli.contact)}${champ("E-mail de facturation", "c_email", cli.email, "email")}
        ${champ("Délai de paiement habituel (jours)", "delai_paiement_jours", a.delai_paiement_jours || 45, "number")}</div></section>
      <section class="carte"><h2>Stagiaires</h2><p class="discret">RGPD : seules les informations nécessaires aux documents obligatoires (nom, prénom, statut, heures, résultat). Conservation : durée des obligations de preuve (contrôles, Qualiopi).</p>
        <div class="defile"><table id="t-stag"><thead><tr><th>Nom</th><th>Prénom</th><th>Statut (BPF)</th><th>Entreprise</th><th>Heures suivies</th><th>Résultat</th><th></th></tr></thead><tbody>
        ${(a.stagiaires || []).map((s, i) => ligneStag(s, i)).join("")}</tbody></table></div><button type="button" class="second" data-act="ajout-stag">+ Stagiaire</button></section>
      <section class="carte"><h2>Prix et facture</h2><div class="grille-champs">
        ${champ("Prix total HT (€)", "prix_ht", a.prix_ht, "number", 'step="0.01" min="0"')}
        <label>TVA<select name="tva">${opt(Object.assign({ "": `Automatique : ${P.REGIMES[P.regimeTva(Object.assign({}, a, { tva: "" })).code]}` }, P.REGIMES), a.tva || "")}</select><small>Franchise jusqu'au ${fr(D.iso(D.ajoutJours(D.lireDate(d().identite.tva_debut || "2027-02-01"), -1)))}, puis TVA ${String(d().identite.taux_tva || 8.5).replace(".", ",")} %</small></label>
        ${champ("Taux de TVA (%)", "taux_tva", a.taux_tva || d().identite.taux_tva || 8.5, "number", 'step="0.1"')}
        <label>Payé par<select name="canal">${opt(Object.fromEntries(Object.entries(P.CANAUX).map(([k, v]) => [k, v.lib])), a.canal || "")}</select><small>Sert à reconnaître le virement</small></label>
        ${champ("Montant pris en charge par un financeur (HT)", "prise_en_charge_ht", a.prise_en_charge_ht, "number", 'step="0.01" min="0"')}
        ${champ("Nom du financeur (OPCO, France Travail…)", "financeur_nom", a.financeur_nom, "text", 'placeholder="AKTO, OPCO EP, ATLAS…"')}
        <label>Canal du financeur<select name="canal_financeur">${opt(Object.fromEntries(Object.entries(P.CANAUX).filter(([k]) => !["entreprise", "particulier"].includes(k)).map(([k, v]) => [k, v.lib])), a.canal_financeur || "opco")}</select></label>
        ${champ("Modalités de règlement", "reglement", a.reglement || "Virement à 30 jours")}
        ${champ("N° de facture", "numero_facture", a.numero_facture)}${champ("Date de facture", "date_facture", a.date_facture, "date")}${champ("Échéance", "echeance_facture", a.echeance_facture, "date")}
        <label class="coche"><input type="checkbox" name="subrogation" ${a.subrogation ? "checked" : ""}>Subrogation de paiement (OPCO)</label></div>
        ${paiementsAction(a)}
        <p class="discret">${P.besoinMission(a).message}</p></section>
      <section class="carte"><h2>Résultats (indicateurs Qualiopi 2 et 30)</h2><div class="grille-champs">
        ${champ("Satisfaction à chaud (moyenne sur 4)", "satisfaction_chaud", a.satisfaction_chaud, "number", 'step="0.1" min="0" max="4"')}
        ${champ("Présentés à la certification", "presentes", a.presentes, "number", 'min="0"')}${champ("Admis", "admis", a.admis, "number", 'min="0"')}
        ${champ("Abandons", "abandons", a.abandons, "number", 'min="0"')}${champ("Réclamations reçues", "reclamations", a.reclamations, "number", 'min="0"')}</div></section>
      <div class="actions collant"><button type="submit" class="principal-court">Enregistrer</button><button type="button" class="lien danger" data-act="suppr-action">Supprimer l'action</button></div></form>
      <section class="carte"><h2>Documents de l'action</h2><p class="discret">Générés avec les données ci-dessus (enregistrez d'abord). Marquez « Fait » quand le document est signé ou remis.</p>
        <div class="defile"><table><thead><tr><th>Document</th><th>Pour le</th><th>Qualiopi</th><th>État</th><th></th></tr></thead><tbody>
        ${docs.map((x) => `<tr class="${x.etat !== "fait" && x.etat !== "na" && x.limite && x.limite < auj() ? "retard" : ""}"><td>${esc(x.titre)}</td><td>${fr(x.limite)}</td><td>${x.ind.map((n) => "I" + n).join(" ")}</td>
          <td><select data-act="etat-doc" data-doc="${esc(x.id)}" aria-label="État du document">${opt({ a_faire: "À faire", genere: "Généré", fait: "Fait / signé", na: "Non concerné" }, x.etat)}</select></td>
          <td><button class="lien" data-act="gen-doc" data-doc="${esc(x.id)}">Générer</button>${((d().bibliotheque[x.id] || {}).fichiers || []).filter((f) => (d().fichiers || {})[f]).slice(-1).map((f) => `<br><button class="lien" data-act="dl-piece" data-id="${esc(f)}">Ma version validée</button>`).join("")}</td></tr>`).join("")}</tbody></table></div>
        <div class="actions"><button class="second" data-act="gen-tous">Tous les documents (.zip)</button></div></section>
      <section class="carte"><h2>Pièces classées (conventions signées, justificatifs)</h2>
        <ul class="todo">${pieces.map(([id, m]) => `<li><span>${esc(m.nom)}</span><small class="discret">${Math.round(m.taille / 1024)} Ko · ${fr(m.depose.slice(0, 10))}</small><button class="lien" data-act="dl-piece" data-id="${esc(id)}">Télécharger</button><button class="lien danger" data-act="suppr-piece" data-id="${esc(id)}">Retirer</button></li>`).join("") || `<li class="discret">Aucune pièce.</li>`}</ul>
        <label>Ajouter une pièce (PDF, image, Word — 15 Mo max, chiffrée)<input type="file" id="piece" accept=".pdf,.png,.jpg,.jpeg,.docx,.xlsx"></label></section>`;
  }
  const ligneStag = (s, i) => `<tr data-i="${i}"><td><input name="s_nom" value="${esc(s.nom)}" aria-label="Nom"></td><td><input name="s_prenom" value="${esc(s.prenom)}" aria-label="Prénom"></td>
    <td><select name="s_statut" aria-label="Statut">${opt({ salarie: "Salarié", apprenti: "Apprenti", demandeur: "Demandeur d'emploi", particulier: "Particulier", autre: "Autre" }, s.statut)}</select></td>
    <td><input name="s_entreprise" value="${esc(s.entreprise)}" aria-label="Entreprise"></td><td><input name="s_heures" type="number" step="0.5" min="0" value="${esc(s.heures)}" aria-label="Heures"></td>
    <td><input name="s_resultat" value="${esc(s.resultat)}" aria-label="Résultat"></td><td><button type="button" class="lien danger" data-act="suppr-stag">Retirer</button></td></tr>`;
  function lireAction(form, a) {
    const fd = new FormData(form), g = (k) => String(fd.get(k) ?? "").trim().slice(0, 1000);
    for (const k of ["intitule", "formationId", "type", "statut", "pour_centre", "origine", "nature", "debut", "fin", "jours_semaine", "horaires", "lieu", "objectifs", "tva", "reglement", "numero_facture", "date_facture", "echeance_facture", "canal", "financeur_nom", "canal_financeur"]) a[k] = g(k);
    for (const k of ["heures", "frais_prevus", "delai_paiement_jours", "prix_ht", "taux_tva", "prise_en_charge_ht", "satisfaction_chaud", "presentes", "admis", "abandons", "reclamations"]) a[k] = P.num(fd.get(k));
    a.subrogation = !!fd.get("subrogation");
    a.client = { raison: g("c_raison"), siret: g("c_siret"), adresse: g("c_adresse"), contact: g("c_contact"), email: g("c_email") };
    a.stagiaires = [...form.querySelectorAll("#t-stag tbody tr")].map((tr) => ({ nom: $('[name="s_nom"]', tr).value.trim(), prenom: $('[name="s_prenom"]', tr).value.trim(), statut: $('[name="s_statut"]', tr).value,
      entreprise: $('[name="s_entreprise"]', tr).value.trim(), heures: P.num($('[name="s_heures"]', tr).value), resultat: $('[name="s_resultat"]', tr).value.trim() })).filter((s) => s.nom || s.prenom);
    if (a.date_facture && !a.numero_facture) a.numero_facture = `${a.date_facture.slice(0, 4)}-${String(d().actions.filter((x) => x.numero_facture && x.numero_facture.startsWith(a.date_facture.slice(0, 4))).length + 1).padStart(3, "0")}`;
    if (a.date_facture && !a.echeance_facture) a.echeance_facture = D.iso(D.ajoutJours(D.lireDate(a.date_facture), 30));
    P.synchroAttendus(d());
  }
  // Ce que l'action doit rapporter, part par part, et ce qui est déjà arrivé
  function paiementsAction(a) {
    const xs = d().attendus.filter((x) => x.actionId === a.id && !x.annule);
    if (!xs.length) return `<p class="discret">Les sommes attendues apparaissent dans Finances dès que l'action est « Convention signée » (ou facturée).</p>`;
    return `<h3>Paiements</h3><ul class="todo">${xs.map((x) => `<li class="${P.etatAttendu(x) === "retard" ? "retard" : ""}"><span class="quand">${esc(P.ETATS[P.etatAttendu(x)])}</span><span>${esc(x.payeur)} — ${E(P.recu(x))} reçu sur ${E(x.montant)}${P.reste(x) ? ` · reste ${E(P.reste(x))}` : ""}</span><button type="button" class="lien" data-go="finances">Finances</button></li>`).join("")}</ul>`;
  }
  function aActions() {
    lierCommun();
    const form = $("#f-action"), a = d().actions.find((x) => x.id === etat.actionSel);
    if (!form) return;
    form.onsubmit = (e) => { e.preventDefault(); lireAction(form, a); sauver(); rendre(); toast("Action enregistrée."); };
    $("#piece").onchange = async (e) => {
      const fi = e.target.files[0];
      if (!fi) return;
      if (fi.size > 15 * 1024 * 1024) { toast("15 Mo maximum.", "ko"); return; }
      const oct = new Uint8Array(await fi.arrayBuffer());
      const id = await C.deposerFichier(fi.name.slice(0, 120), fi.type, oct);
      (a.pieces = a.pieces || []).push(id); sauver(); rendre(); toast("Pièce classée et chiffrée.");
    };
  }

  // ------------------------------------------------------------ QUALIOPI
  function preuvesAuto(n) {
    const out = [], ind = P.QUALIOPI.find((i) => i.n === n);
    for (const id of (ind && ind.docs) || []) { const b = d().bibliotheque[id], m = P.BIBLIOTHEQUE.find((x) => x.id === id); if (b && (b.fichiers || []).length) out.push(`${m.titre}${m.ref ? " (" + m.ref + ")" : ""} — version déposée le ${fr(b.date)}`); }
    for (const a of d().actions) for (const doc of P.documentsAttendus(a)) if (doc.ind.includes(n) && (doc.etat === "fait" || doc.etat === "genere")) out.push(`${doc.titre} — ${a.intitule}`);
    for (const f of d().formations) {
      if ([5, 6, 7, 11, 19].includes(n) && Object.keys(f.packs || {}).length) out.push(`${Object.keys(f.packs).length} séance(s) préparée(s) avec supports — ${f.titre}`);
      if ([5, 6, 7].includes(n)) out.push(`Décorticage du référentiel (couverture des critères) — ${f.titre}`);
      if (n === 10 && (f.journal || []).length) out.push(`${f.journal.length} journée(s) notée(s) avec adaptations du planning — ${f.titre}`);
    }
    if ([23, 24, 25].includes(n)) { const v = d().veille.filter((x) => x.type === { 23: "legale", 24: "metiers", 25: "pedagogique" }[n]); if (v.length) out.push(`${v.length} entrée(s) de veille`); }
    if (n === 31 && d().reclamations.length) out.push(`${d().reclamations.length} réclamation(s) tracée(s)`);
    if (n === 32 && d().ameliorations.length) out.push(`${d().ameliorations.length} action(s) d'amélioration`);
    if (n === 2) { const r = P.resultats(d()); if (r.actions) out.push(`Indicateurs calculés sur ${r.actions} action(s) terminée(s)`); }
    if (n === 26 && d().partenaires.some((p) => /handicap|agefiph|cap emploi|mdph/i.test(p.nom + " " + (p.notes || "")))) out.push("Partenaires handicap identifiés");
    return out;
  }
  // indicateurs prouvés par chaque document de la bibliothèque
  const indicateursDe = (id) => P.QUALIOPI.filter((i) => i.docs.includes(id)).map((i) => i.n);
  const etatBiblio = (b) => { const v = d().bibliotheque[b.id] || {}; return (v.fichiers || []).length ? "ok" : v.statut === "en_vigueur" || (b.source === "app" && !v.statut) ? "att" : "ko"; };
  function vQualiopi() {
    const q = d().qualiopi, tous = P.QUALIOPI.concat(q.ajouts || []), cov = couvertureQualiopi(), audit = jours(d().identite.audit_debut), r = P.resultats(d()), I = d().identite;
    const alerteCertif = I.qualiopi_validite && I.audit_fin && I.qualiopi_validite < I.audit_fin
      ? `<p class="message ko"><b>À vérifier en priorité :</b> votre certificat est noté valable jusqu'au ${fr(I.qualiopi_validite)}, alors que la période d'audit indiquée court jusqu'au ${fr(I.audit_fin)}. L'audit de renouvellement doit avoir lieu <b>avant le ${fr(I.qualiopi_validite)}</b>, sinon la certification s'interrompt (et avec elle l'accès aux fonds publics et mutualisés, art. L6316-1). Confirmez la date avec ${esc(I.certificateur || "votre certificateur")}.</p>` : "";
    const bib = P.BIBLIOTHEQUE, presents = bib.filter((b) => etatBiblio(b) === "ok").length;
    return `<header class="titre-vue"><h1>Qualiopi</h1><p>${cov.prets}/${cov.total} indicateurs prêts${audit !== null ? ` · audit à partir du ${fr(I.audit_debut)} (dans ${audit} jours)` : ""}. Les preuves se remplissent avec ce que vous faites dans le logiciel.</p></header>
      <p class="message"><b>Référentiel V10 — 33 indicateurs</b> (décret n° 2026-728 du 1<sup>er</sup> août 2026), applicable à tout audit réalisé à partir du 1<sup>er</sup> novembre 2026. Libellés : texte de 2019 ; les modifications V10 sont résumées sous chaque indicateur concerné. Le texte exact de l'annexe est à confirmer sur Légifrance avant l'audit.</p>
      ${alerteCertif}
      <div class="tuiles">${tuile("Satisfaction", r.satisfaction ? r.satisfaction.toFixed(1).replace(".", ",") + " / 4" : "—", "indicateur 2", "", "qualiopi")}${tuile("Réussite", r.reussite !== null ? Math.round(r.reussite * 100) + " %" : "—", "certifications", "", "qualiopi")}
        ${tuile("Abandons", r.abandon !== null ? Math.round(r.abandon * 100) + " %" : "—", "", "", "qualiopi")}${tuile("Bibliothèque", `${presents} / ${bib.length}`, "documents déposés", presents < bib.length / 2 ? "alerte" : "", "qualiopi")}</div>
      ${Object.entries(P.CRITERES).map(([c, lib]) => `<details class="carte" ${c === "1" ? "open" : ""}><summary><b>Critère ${c}</b> — ${esc(lib)}</summary>
        ${tous.filter((i) => String(i.critere) === c).map((i) => { const s = q.suivi[i.n] || {}, auto = preuvesAuto(i.n);
          return `<div class="indicateur ${s.na ? "na" : s.statut || "a_faire"}" data-n="${i.n}"><div class="ind-tete"><b>Indicateur ${i.n}</b>${i.portee && i.portee !== "tous" ? `<span class="puce att">${esc(P.PORTEES[i.portee] || i.portee)}</span>` : ""}${i.v10 ? `<span class="puce ${i.n === 33 ? "ko" : "att"}">${i.n === 33 ? "nouveau V10" : "modifié V10"}</span>` : ""}
            <select data-act="statut-ind" aria-label="Statut">${opt({ a_faire: "À faire", en_cours: "En cours", pret: "Prêt pour l'audit" }, s.statut || "a_faire")}</select>
            <label class="coche"><input type="checkbox" data-act="na-ind" ${s.na ? "checked" : ""}>Non concerné</label></div>
            <p>${esc(i.libelle)}</p>${i.v10 ? `<p class="message alerte"><b>V10 :</b> ${esc(i.v10)}</p>` : ""}
            ${i.portee === "cfa" ? `<p class="discret">En sous-traitance pour un CFA, cet indicateur est audité chez le CFA : vous lui fournissez les preuves de vos séances.</p>` : ""}
            ${(i.docs || []).length ? `<p class="petit"><b>Documents attendus :</b></p><ul class="puces-docs">${i.docs.map((id) => { const b = bib.find((x) => x.id === id); return `<li><a class="puce ${etatBiblio(b)}" href="#bib-${esc(id)}" data-bib="${esc(id)}">${esc(b.titre)}</a></li>`; }).join("")}</ul>` : ""}
            ${auto.length ? `<ul class="preuves">${auto.map((x) => `<li>✔ ${esc(x)}</li>`).join("")}</ul>` : `<p class="discret">Aucune preuve automatique pour l'instant.</p>`}
            <textarea data-act="note-ind" rows="2" aria-label="Preuves et remarques" placeholder="Vos preuves complémentaires (où se trouve le document, procédure…)">${esc(s.note || "")}</textarea></div>`; }).join("")}</details>`).join("")}
      <section class="carte" id="bibliotheque"><h2>Bibliothèque documentaire</h2>
        <p>Chaque document exigé est déposé <b>une seule fois</b>, chiffré, puis réutilisé partout : preuves des indicateurs, dossier d'audit, documents des actions. Statuts relevés dans votre base Airtable (« DOCUMENTS OFFICIELS YEBA ») le 28/10/2026.</p>
        <div class="defile"><table><thead><tr><th>Document</th><th>Indicateurs</th><th>Statut</th><th>Reste à faire</th><th>Ma version</th><th></th></tr></thead><tbody>
        ${bib.map((b) => { const v = d().bibliotheque[b.id] || {}, f = (v.fichiers || []).map((id) => [id, (d().fichiers || {})[id]]).filter(([, m]) => m), st = v.statut ?? b.statut;
          return `<tr id="bib-${esc(b.id)}"><td><b>${esc(b.titre)}</b>${b.ref ? `<br><small class="discret">${esc(b.ref)}</small>` : ""}${b.source === "app" ? `<br><small class="discret">produit par le logiciel</small>` : ""}</td>
          <td>${indicateursDe(b.id).join(", ") || "—"}</td>
          <td><select data-act="statut-bib" data-id="${esc(b.id)}" aria-label="Statut du document">${opt(P.STATUTS_DOC, st)}</select></td>
          <td class="petit">${esc(v.note ?? b.reste)}</td>
          <td>${f.map(([id, m]) => `<button class="lien" data-act="dl-piece" data-id="${esc(id)}">${esc(m.nom)}</button>`).join("<br>") || `<span class="puce ${etatBiblio(b)}">${etatBiblio(b) === "ko" ? "manquant" : "aucun fichier"}</span>`}</td>
          <td><label class="second petit">Déposer<input type="file" data-act="depot-biblio" data-id="${esc(b.id)}" accept=".pdf,.docx,.doc,.odt,.xlsx,.png,.jpg,.jpeg" hidden></label>
            ${P.BIBLIO_GENERABLES.includes(b.id) ? `<button class="lien" data-act="gen-biblio" data-id="${esc(b.id)}">Générer le modèle</button>` : ""}</td></tr>`; }).join("")}</tbody></table></div></section>
      <section class="carte"><h2>Registres</h2><div class="trois">
        ${registre("veille", "Veille (indicateurs 23, 24, 25)", [["date", "date", "Date"], ["type", "select", "Type", { legale: "Légale et réglementaire", metiers: "Métiers et compétences", pedagogique: "Pédagogique et technologique" }], ["source", "text", "Source"], ["info", "text", "Information"], ["exploitation", "text", "Ce que je change"]])}
        ${registre("reclamations", "Réclamations et aléas (indicateur 31)", [["date", "date", "Date"], ["objet", "text", "Objet"], ["traitement", "text", "Traitement"], ["cloture", "date", "Clôturée le"]])}
        ${registre("ameliorations", "Améliorations (indicateur 32)", [["date", "date", "Date"], ["origine", "text", "Origine (avis, réclamation, risque…)"], ["action", "text", "Action"], ["echeance", "date", "Échéance"]])}</div>
        <h3>Risques qualité (V10, indicateur 32)</h3>
        ${registre("risques", "Registre des risques", [["date", "date", "Date de revue"], ["risque", "text", "Risque"], ["p", "select", "Probabilité", { Faible: "Faible", Moyenne: "Moyenne", Forte: "Forte" }], ["i", "select", "Impact", { Faible: "Faible", Moyen: "Moyen", Fort: "Fort" }], ["mesure", "text", "Mesure de prévention"]])}
        <p class="discret">Sources de veille : legifrance.gouv.fr · francecompetences.fr · centre-inffo.fr · travail-emploi.gouv.fr · deets.gouv.fr (La Réunion).</p></section>
      <section class="carte"><h2>Dossier d'audit</h2><p>Un document qui récapitule, indicateur par indicateur, vos preuves (automatiques, bibliothèque et saisies), les modifications V10 et les registres.</p>
        <div class="actions"><button class="principal-court" data-act="dossier-audit">Télécharger le dossier d'audit (.docx)</button>
        <button class="second" data-act="ajout-ind">Ajouter un indicateur</button></div></section>`;
  }
  function registre(cle, titre, champs) {
    const lignes = d()[cle] || [];
    return `<div><h3>${esc(titre)}</h3><ul class="todo">${lignes.slice(-5).reverse().map((x) => `<li><span class="quand">${fr(x.date)}</span><span>${esc(champs.slice(1).map(([k, t, , o]) => (t === "select" ? o[x[k]] : x[k])).filter(Boolean).join(" · "))}</span></li>`).join("") || `<li class="discret">Vide.</li>`}</ul>
      <form class="pile petit" data-registre="${cle}">${champs.map(([k, t, lib, o]) => t === "select" ? `<label>${esc(lib)}<select name="${k}">${opt(o, "")}</select></label>` : `<label>${esc(lib)}<input name="${k}" type="${t}" ${k === "date" ? `value="${auj()}"` : ""}></label>`).join("")}
      <button class="second" type="submit">Ajouter</button></form></div>`;
  }
  function aQualiopi() {
    lierCommun();
    document.querySelectorAll("form[data-registre]").forEach((f) => (f.onsubmit = (e) => {
      e.preventDefault(); const fd = new FormData(f), x = { id: uid() };
      for (const [k, v] of fd.entries()) x[k] = String(v).slice(0, 1000);
      d()[f.dataset.registre].push(x); sauver(); rendre(); toast("Ajouté au registre.");
    }));
  }
  async function dossierAudit() {
    const q = d().qualiopi, tous = P.QUALIOPI.concat(q.ajouts || []);
    const ctx = { charte: charteDoc(), nomOrg: d().identite.nom, logo: etat.logo };
    return D.docWord(ctx, `Dossier de preuves Qualiopi — ${d().identite.nom}`, (o) => {
      o.p(`Certificat n° ${d().identite.qualiopi} · NDA ${d().identite.nda} · SIRET ${d().identite.siret} · édité le ${fr(auj())}`);
      for (const [c, lib] of Object.entries(P.CRITERES)) {
        o.h2(`Critère ${c} — ${lib}`);
        o.tableau([["Indicateur", "Statut", "Preuves"]].concat(tous.filter((i) => String(i.critere) === c).map((i) => { const s = q.suivi[i.n] || {};
          return [`${i.n}. ${i.libelle}${i.v10 ? "\nV10 : " + i.v10 : ""}`, s.na ? "Non concerné" : ({ a_faire: "À faire", en_cours: "En cours", pret: "Prêt" })[s.statut || "a_faire"], preuvesAuto(i.n).concat(s.note ? [s.note] : []).map((x) => "• " + x).join("\n") || "—"]; })));
      }
      o.h2("Bibliothèque documentaire");
      o.tableau([["Document", "Indicateurs", "Statut", "Version déposée"]].concat(P.BIBLIOTHEQUE.map((b) => { const v = d().bibliotheque[b.id] || {};
        return [`${b.titre}${b.ref ? " (" + b.ref + ")" : ""}`, indicateursDe(b.id).join(", ") || "—", P.STATUTS_DOC[v.statut ?? b.statut] || "", (v.fichiers || []).length ? `oui, le ${fr(v.date)}` : "non"]; })));
      for (const [cle, lib] of [["veille", "Registre de veille"], ["reclamations", "Registre des réclamations"], ["ameliorations", "Plan d'amélioration"]]) {
        o.h2(lib); const l = d()[cle];
        if (l.length) o.tableau([Object.keys(l[0]).filter((k) => k !== "id")].concat(l.map((x) => Object.entries(x).filter(([k]) => k !== "id").map(([, v]) => v)))); else o.p("Aucune entrée.");
      }
    });
  }

  // ------------------------------------------------------------ FINANCES
  const canalLib = (k) => (P.CANAUX[k] || P.CANAUX.autre).lib;
  const TRIS = { echeance: "Échéance", reste: "Reste dû (du plus grand)", payeur: "Payeur (A → Z)", canal: "Canal de paiement", etat: "État" };
  const FILTRES = { a_recevoir: "Tout ce qui reste à recevoir", retard: "En retard seulement", solde: "Réglé", tous: "Tout" };
  function listeAttendus() {
    const f = etat.filtreAtt || "a_recevoir", t = etat.triAtt || "echeance", ordreEtat = { retard: 0, partiel: 1, a_venir: 2, solde: 3, annule: 4 };
    return d().attendus.filter((x) => !x.annule && (f === "tous" || (f === "solde" ? P.etatAttendu(x) === "solde" : f === "retard" ? P.etatAttendu(x) === "retard" : P.reste(x) > 0)))
      .sort((x, y) => t === "reste" ? P.reste(y) - P.reste(x) : t === "payeur" ? x.payeur.localeCompare(y.payeur, "fr") : t === "canal" ? canalLib(x.canal).localeCompare(canalLib(y.canal), "fr")
        : t === "etat" ? ordreEtat[P.etatAttendu(x)] - ordreEtat[P.etatAttendu(y)] : (x.echeance || "9999").localeCompare(y.echeance || "9999"));
  }
  function ligneAttendu(x) {
    const e = P.etatAttendu(x), ouvert = etat.paiementOuvert === x.id;
    return `<tr class="${e === "retard" ? "retard" : ""}"><td><b>${esc(x.payeur)}</b><br><small class="discret">${esc(x.libelle)}${x.reference ? " · facture " + esc(x.reference) : ""}</small></td>
      <td>${esc(canalLib(x.canal))}</td><td>${fr(x.echeance)}</td><td class="num">${E(x.montant)}</td><td class="num">${E(P.recu(x))}</td><td class="num"><b>${E(P.reste(x))}</b></td>
      <td><span class="puce ${e === "solde" ? "ok" : e === "retard" ? "ko" : "att"}">${esc(P.ETATS[e])}</span></td>
      <td>${P.reste(x) > 0 ? `<button class="lien" data-act="ouvrir-paiement" data-a="${esc(x.id)}">${ouvert ? "Fermer" : "Noter un paiement reçu"}</button>` : ""}${x.actionId ? `<br><button class="lien" data-act="voir-action" data-id="${esc(x.actionId)}">Action</button>` : `<br><button class="lien danger" data-act="suppr-attendu" data-a="${esc(x.id)}">Retirer</button>`}</td></tr>
      ${(x.encaissements || []).length ? `<tr><td colspan="8" class="petit discret">Reçu : ${x.encaissements.map((en) => `${fr(en.date)} ${E(en.montant)} (${esc(en.mode || "")}) <button class="lien danger" data-act="annuler-enc" data-a="${esc(x.id)}" data-e="${esc(en.id)}">annuler</button>`).join(" · ")}</td></tr>` : ""}
      ${ouvert ? `<tr><td colspan="8"><form id="f-paiement" class="grille-champs" data-a="${esc(x.id)}">${champ("Montant reçu (€)", "montant", P.reste(x), "number", 'step="0.01" min="0.01" required')}${champ("Date de réception", "date", auj(), "date", "required")}
        <label>Moyen<select name="mode">${opt({ virement: "Virement", cheque: "Chèque", especes: "Espèces", prelevement: "Prélèvement", autre: "Autre" }, "virement")}</select></label>
        <button class="principal-court" type="submit">Confirmer la réception</button></form><p class="discret petit">Si vous importez ensuite le relevé bancaire, le virement correspondant sera reconnu comme la même somme (pas de double comptage).</p></td></tr>` : ""}`;
  }
  function vFinances() {
    P.synchroAttendus(d());
    const tb = P.tableauBord(d()), t = P.tresorerie(d()), annee = new Date().getFullYear(), b = P.bpf(d(), annee - (new Date().getMonth() < 5 ? 1 : 0)), ec = d().ecritures.slice().sort((x, y) => y.date.localeCompare(x.date));
    const aConf = d().mouvements.filter((m) => m.etat === "a_confirmer").sort((x, y) => y.date.localeCompare(x.date));
    const ouverts = d().attendus.filter((x) => !x.annule && P.reste(x) > 0);
    const liste = listeAttendus(), grouper = !!etat.grouperAtt;
    const groupes = grouper ? Object.entries(liste.reduce((g, x) => ((g[x.canal] = g[x.canal] || []).push(x), g), {})) : [["", liste]];
    const optAttendus = ouverts.map((x) => `<option value="${esc(x.id)}">${esc(x.payeur)} — ${esc(x.libelle)} (reste ${esc(E(P.reste(x)))})</option>`).join("");
    return `<header class="titre-vue"><h1>Finances</h1><p>Ce que j'ai, ce qu'on me doit, ce qu'il me restera. Rien n'est marqué « reçu » sans votre confirmation.</p></header>
      <div class="tuiles tableau-bord">
        ${tuile("Ce que j'ai aujourd'hui", E(tb.solde), `solde bancaire au ${fr(auj())}`, tb.solde < P.num(d().tresorerie.seuil_alerte) ? "alerte" : "ok", "finances")}
        ${tuile("Ce qu'on me doit", E(tb.du), `${tb.nbDu} somme(s) pas encore réglée(s)`, "", "finances")}
        ${tuile("Dont en retard", E(tb.retard), tb.nbRetard ? `${tb.nbRetard} paiement(s) à relancer` : "aucun retard", tb.nbRetard ? "ko" : "ok", "finances")}
        ${tuile("Ce qu'il me restera", E(tb.restera), "si tout est payé, après dépenses prévues et TVA", tb.restera < 0 ? "ko" : "", "finances")}
        ${tuile(`Encaissé en ${annee}`, E(tb.encaisseAnnee), `dont ${E(tb.encaisseMois)} ce mois-ci`, "", "finances")}
        ${tuile("Virements à confirmer", String(tb.aConfirmer), tb.aConfirmer ? "reçus sur le compte, à rattacher" : "tout est rapproché", tb.aConfirmer ? "alerte" : "ok", "finances")}
        ${tb.tva || tb.tvaAVenir ? tuile("TVA à reverser (estimation)", E(tb.tva), `+ ${E(tb.tvaAVenir)} sur les sommes encore dues`, "", "finances") : ""}</div>
      <p class="discret petit">Ce qu'il me restera = ce que j'ai (${E(tb.solde)}) + ce qu'on me doit (${E(tb.du)}) + recettes prévues (${E(tb.recettesPrevues)}) − dépenses prévues (${E(tb.depensesPrevues)}) − TVA à reverser (${E(tb.tva + tb.tvaAVenir)}).</p>
      ${aConf.length ? `<section class="carte"><h2>Virements reçus à confirmer (${aConf.length})</h2>
        <p>Le logiciel compare le montant, le nom de l'émetteur (même écrit autrement : « VIR AKTO OPCO » pour « AKTO Réunion ») et le n° de facture. <b>Vous confirmez</b> ; il retient l'association pour la fois suivante.</p>
        ${aConf.some((m) => m.propositions && m.propositions[0] && m.propositions[0].score >= 0.9 && !(m.propositions[1] && m.propositions[1].score >= 0.6)) ? `<div class="actions"><button class="second" data-act="confirmer-surs">Confirmer toutes les correspondances sûres (≥ 90 %)</button></div>` : ""}
        <div class="pile">${aConf.map((m) => `<div class="carte rapprochement"><div class="ind-tete"><span class="quand">${fr(m.date)}</span><b class="num">${E(m.montant)}</b><span>${esc(m.libelle)}</span></div>
          ${(m.propositions || []).length ? `<ul class="propositions">${m.propositions.map((pr) => { const x = d().attendus.find((y) => y.id === pr.attenduId); if (!x) return "";
            return `<li><span class="score ${pr.score >= 0.9 ? "ok" : pr.score >= 0.6 ? "att" : "ko"}">${Math.round(pr.score * 100)} %</span><span><b>${esc(x.payeur)}</b> — ${esc(x.libelle)} · reste ${E(P.reste(x))}<br><small class="discret">${esc(pr.raisons.join(" · "))}</small></span><button class="principal-court" data-act="confirmer-rap" data-m="${esc(m.id)}" data-a="${esc(x.id)}">C'est bien ça</button></li>`; }).join("")}</ul>`
            : `<p class="discret">Aucune somme attendue ne correspond (montant et nom).</p>`}
          <div class="actions">${optAttendus ? `<label class="petit">Autre somme attendue<select id="sel-${esc(m.id)}">${optAttendus}</select></label><button class="second" data-act="confirmer-autre" data-m="${esc(m.id)}">Rattacher</button>` : ""}
            <label class="petit">Pas une facture<select id="cls-${esc(m.id)}">${opt(P.ORIGINES, "autres")}</select></label><button class="second" data-act="classer-mvt" data-m="${esc(m.id)}">Classer en autre recette</button>
            <button class="lien" data-act="ignorer-mvt" data-m="${esc(m.id)}">Ignorer (virement interne)</button></div></div>`).join("")}</div></section>` : ""}
      <section class="carte"><h2>Ce qu'on me doit</h2>
        <div class="actions"><label class="petit">Trier par<select data-act="tri-att">${opt(TRIS, etat.triAtt || "echeance")}</select></label>
          <label class="petit">Afficher<select data-act="filtre-att">${opt(FILTRES, etat.filtreAtt || "a_recevoir")}</select></label>
          <label class="coche petit"><input type="checkbox" data-act="grouper-att" ${grouper ? "checked" : ""}>Regrouper par canal (OPCO, CPF, entreprises…)</label></div>
        <div class="defile"><table><thead><tr><th>Qui me paie</th><th>Par quel canal</th><th>Échéance</th><th class="num">Attendu</th><th class="num">Reçu</th><th class="num">Reste</th><th>État</th><th></th></tr></thead><tbody>
        ${liste.length ? groupes.map(([k, xs]) => (grouper ? `<tr><th colspan="8">${esc(canalLib(k))} — reste ${E(xs.reduce((a, x) => a + P.reste(x), 0))}</th></tr>` : "") + xs.map(ligneAttendu).join("")).join("")
          : `<tr><td colspan="8" class="discret">Rien à afficher. Les sommes attendues se créent depuis les actions (dès « Convention signée ») ou avec le formulaire ci-dessous.</td></tr>`}</tbody></table></div>
        <details><summary><b>Ajouter une somme attendue hors action</b> (conseil, audit, implémentation, acompte…)</summary>
          <form id="f-attendu" class="grille-champs">${champ("Qui me paie", "payeur", "", "text", 'required placeholder="Nom de la structure"')}${champ("Pour quoi", "libelle", "", "text", 'required placeholder="Audit RGPD, workflow IA…"')}
          <label>Canal<select name="canal">${opt(Object.fromEntries(Object.entries(P.CANAUX).map(([k, v]) => [k, v.lib])), "entreprise")}</select></label>
          ${champ("Montant TTC attendu (€)", "montant", "", "number", 'step="0.01" min="0.01" required')}${champ("Échéance", "echeance", "", "date")}${champ("N° de facture", "reference", "")}${champ("Taux de TVA inclus (%)", "taux_tva", 0, "number", 'step="0.1" min="0"')}
          <button class="principal-court" type="submit">Ajouter</button></form></details></section>
      <div class="deux-colonnes"><section class="carte"><h2>Par canal de paiement</h2><div class="defile"><table><thead><tr><th>Canal</th><th class="num">Attendu</th><th class="num">Reçu</th><th class="num">Reste</th></tr></thead><tbody>
          ${Object.entries(tb.parCanal).map(([k, c]) => `<tr><td>${esc(canalLib(k))} <small class="discret">(${c.n})</small></td><td class="num">${E(c.attendu)}</td><td class="num">${E(c.recu)}</td><td class="num"><b>${E(c.reste)}</b></td></tr>`).join("") || `<tr><td colspan="4" class="discret">Aucune somme attendue.</td></tr>`}</tbody></table></div>
        <h3>Importer le relevé bancaire</h3>
        <p class="discret">Dans l'espace en ligne de votre banque : « Télécharger les opérations » au format <b>CSV</b> ou <b>OFX</b> (Money / Quicken). Les lignes déjà importées sont ignorées.</p>
        <input type="file" id="releve" accept=".csv,.ofx,.qfx,.txt" aria-label="Relevé bancaire CSV ou OFX">
        <h3>Réglages de trésorerie</h3><form id="f-treso" class="grille-champs">${champ("Solde bancaire de départ (€)", "solde_initial", d().tresorerie.solde_initial, "number", 'step="0.01"')}${champ("À la date du", "date_solde", d().tresorerie.date_solde, "date")}${champ("Seuil d'alerte (€)", "seuil_alerte", d().tresorerie.seuil_alerte, "number")}<button class="second" type="submit">Enregistrer</button></form></section>
      <section class="carte">${tresorerieSvg(t)}
        <h3>Besoin en fonds de roulement</h3><p>${E(t.bfr)}${t.bfrJours !== null ? ` · soit ${t.bfrJours} jours de chiffre d'affaires` : ""} · charges moyennes ${E(t.chargeMensuelle)} par mois${t.autonomieJours !== null ? ` · ${t.autonomieJours} jours d'autonomie` : ""}.</p>
        <h3>Nouvelle écriture (dépense, ou recette hors facture)</h3><form id="f-ecr" class="grille-champs">
        <label>Type<select name="sens"><option value="depense">Dépense</option><option value="recette">Recette</option></select></label>
        ${champ("Date", "date", auj(), "date", "required")}${champ("Montant (€)", "montant", "", "number", 'step="0.01" min="0" required')}${champ("Libellé", "libelle", "", "text", "required")}
        <label>Catégorie (dépenses)<select name="categorie">${P.CATEGORIES_DEPENSE.map((c) => `<option>${esc(c)}</option>`).join("")}</select></label>
        <label>Origine (recettes, BPF)<select name="origine">${opt(P.ORIGINES, "autres")}</select></label>
        <label>Statut<select name="statut"><option value="realise">Réalisé</option><option value="prevu">Prévu (à venir)</option></select></label>
        <button class="principal-court" type="submit">Ajouter</button></form></section></div>
      <section class="carte"><h2>Journal (${ec.length} écritures)</h2><div class="defile"><table><thead><tr><th>Date</th><th>Libellé</th><th>Origine / catégorie</th><th class="num">Recette</th><th class="num">Dépense</th><th>Statut</th><th></th></tr></thead><tbody>
        ${ec.slice(0, 200).map((e) => `<tr><td>${fr(e.date)}</td><td>${esc(e.libelle)}${e.source === "banque" ? ` <small class="discret">(banque)</small>` : ""}</td><td>${esc(e.sens === "recette" ? P.ORIGINES[e.origine] || "" : e.categorie || "")}</td><td class="num">${e.sens === "recette" ? E(e.montant) : ""}</td><td class="num">${e.sens === "depense" ? E(e.montant) : ""}</td><td>${e.statut === "prevu" ? "prévu" : "réalisé"}</td><td>${e.source === "banque" ? "" : `<button class="lien danger" data-act="suppr-ecr" data-id="${esc(e.id)}">Retirer</button>`}</td></tr>`).join("") || `<tr><td colspan="7" class="discret">Aucune écriture.</td></tr>`}</tbody></table></div>
        <div class="actions"><button class="second" data-act="exp-compta">Tableau comptable (.xlsx)</button></div></section>
      <section class="carte"><h2>Bilan pédagogique et financier ${b.annee} (préparation)</h2><p>À déclarer sur « Mon Activité Formation » avant le ${fr(b.echeance)}. Produits retenus hors TVA. Vérifiez chaque ligne : le calcul repose sur vos encaissements et vos actions.</p>
        <div class="deux-colonnes"><div><h3>Cadre C — Origine des produits</h3><table><tbody>${Object.entries(b.C).filter(([, v]) => v).map(([k, v]) => `<tr><td>${esc(P.ORIGINES[k])}</td><td class="num">${E(v)}</td></tr>`).join("") || `<tr><td class="discret">Aucune recette sur l'exercice.</td></tr>`}<tr><td><b>Total</b></td><td class="num"><b>${E(b.totalProduits)}</b></td></tr></tbody></table>
          <h3>Cadre D — Charges</h3><p>${E(b.charges)} (total des dépenses réalisées)</p></div>
        <div><h3>Cadre F — Stagiaires et heures</h3><table><thead><tr><th>Public</th><th class="num">Stagiaires</th><th class="num">Heures</th></tr></thead><tbody>${b.F1.map((x) => `<tr><td>${esc(x.lib)}</td><td class="num">${x.nombre}</td><td class="num">${x.heures}</td></tr>`).join("")}<tr><td><b>Total</b></td><td class="num"><b>${b.totalStagiaires}</b></td><td class="num"><b>${b.totalHeures}</b></td></tr></tbody></table>
          <p>Cadre E — heures de formation dispensées par vous : ${b.heuresFormateur} h · Cadre G — produits de sous-traitance : ${E(b.sousTraitanceRecue)}.</p></div></div>
        <button class="second" data-act="exp-bpf">Préparation BPF (.xlsx)</button></section>`;
  }
  function aFinances() {
    lierCommun();
    $("#f-ecr").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target), x = { id: uid() }; for (const [k, v] of fd.entries()) x[k] = String(v).slice(0, 300); x.montant = P.num(x.montant);
      if (x.sens === "depense") delete x.origine; else delete x.categorie; d().ecritures.push(x); sauver(); rendre(); toast("Écriture ajoutée."); };
    $("#f-treso").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target); d().tresorerie = { solde_initial: P.num(fd.get("solde_initial")), date_solde: String(fd.get("date_solde") || auj()), seuil_alerte: P.num(fd.get("seuil_alerte")) }; sauver(); rendre(); };
    $("#f-attendu").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target), g = (k) => String(fd.get(k) || "").trim().slice(0, 300);
      d().attendus.push({ id: uid(), payeur: g("payeur"), libelle: g("libelle"), canal: g("canal") || "entreprise", montant: P.num(fd.get("montant")), echeance: g("echeance"), reference: g("reference"), taux_tva: P.num(fd.get("taux_tva")), encaissements: [], cree: auj() });
      sauver(); rendre(); toast("Somme attendue ajoutée."); };
    const fp = $("#f-paiement");
    if (fp) fp.onsubmit = (e) => { e.preventDefault(); const fd = new FormData(fp);
      try { P.encaisserManuel(d(), fp.dataset.a, { montant: fd.get("montant"), date: String(fd.get("date")), mode: String(fd.get("mode")) }); etat.paiementOuvert = null; sauver(); rendre(); toast("Paiement enregistré : il est compté dans « Ce que j'ai »."); }
      catch (err) { toast(err.message, "ko"); } };
    $("#releve").onchange = async (e) => {
      const fi = e.target.files[0]; if (!fi) return;
      if (fi.size > 10 * 1024 * 1024) { toast("Fichier trop volumineux (10 Mo maximum).", "ko"); return; }
      const r = P.importerReleve(d(), await fi.text());
      sauver(); rendre();
      toast(r.lus ? `${r.nouveaux} opération(s) importée(s) (${r.recettes} recette(s), ${r.depenses} dépense(s))${r.doublons ? `, ${r.doublons} déjà connue(s)` : ""}. Confirmez les virements ci-dessus.` : "Aucune opération lue : vérifiez le format (CSV avec date, libellé, montant ; ou OFX).", r.lus ? "ok" : "ko");
    };
  }
  async function exportCompta() {
    const wb = new ExcelJS.Workbook(); wb.creator = d().identite.nom;
    const ws = wb.addWorksheet("Journal", { pageSetup: { orientation: "landscape", fitToPage: true, fitToWidth: 1, fitToHeight: 0 } });
    ws.columns = [{ header: "Date", key: "date", width: 12 }, { header: "Libellé", key: "libelle", width: 50 }, { header: "Origine / catégorie", key: "cat", width: 36 }, { header: "Recette TTC", key: "r", width: 14 }, { header: "dont HT", key: "ht", width: 12 }, { header: "dont TVA", key: "tva", width: 12 }, { header: "Dépense", key: "dp", width: 14 }, { header: "Statut", key: "s", width: 10 }];
    for (const e of d().ecritures.slice().sort((x, y) => x.date.localeCompare(y.date))) ws.addRow({ date: e.date, libelle: e.libelle, cat: e.sens === "recette" ? P.ORIGINES[e.origine] || "" : e.categorie || "", r: e.sens === "recette" ? e.montant : null, ht: e.sens === "recette" ? e.montant_ht ?? e.montant : null, tva: e.sens === "recette" ? e.tva || 0 : null, dp: e.sens === "depense" ? e.montant : null, s: e.statut === "prevu" ? "prévu" : "réalisé" });
    const at = wb.addWorksheet("Ce qu'on me doit", { pageSetup: { orientation: "landscape", fitToPage: true, fitToWidth: 1, fitToHeight: 0 } });
    at.columns = [{ header: "Payeur", key: "p", width: 32 }, { header: "Objet", key: "l", width: 40 }, { header: "Canal", key: "c", width: 26 }, { header: "Échéance", key: "e", width: 12 }, { header: "Attendu", key: "m", width: 13 }, { header: "Reçu", key: "r", width: 13 }, { header: "Reste", key: "x", width: 13 }, { header: "État", key: "s", width: 14 }];
    for (const x of d().attendus.filter((y) => !y.annule)) at.addRow({ p: x.payeur, l: x.libelle, c: (P.CANAUX[x.canal] || P.CANAUX.autre).lib, e: x.echeance, m: x.montant, r: P.recu(x), x: P.reste(x), s: P.ETATS[P.etatAttendu(x)] });
    at.getRow(1).font = { bold: true, color: { argb: "FFFFFFFF" }, size: 13 }; at.getRow(1).fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FF" + d().charte.couleur_primaire } };
    ws.getRow(1).font = { bold: true, color: { argb: "FFFFFFFF" }, size: 13 }; ws.getRow(1).fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FF" + d().charte.couleur_primaire } };
    const m = wb.addWorksheet("Synthèse mensuelle");
    m.columns = [{ header: "Mois", key: "m", width: 12 }, { header: "Recettes", key: "r", width: 14 }, { header: "Dépenses", key: "dp", width: 14 }, { header: "Résultat", key: "res", width: 14 }];
    const par = {};
    for (const e of d().ecritures) if (e.statut !== "prevu") { const k = e.date.slice(0, 7); par[k] = par[k] || { r: 0, dp: 0 }; par[k][e.sens === "recette" ? "r" : "dp"] += P.num(e.montant); }
    for (const k of Object.keys(par).sort()) m.addRow({ m: k, r: par[k].r, dp: par[k].dp, res: par[k].r - par[k].dp });
    m.getRow(1).font = { bold: true };
    return new Blob([await wb.xlsx.writeBuffer()]);
  }
  async function exportBpf() {
    const annee = new Date().getFullYear() - (new Date().getMonth() < 5 ? 1 : 0), b = P.bpf(d(), annee);
    const wb = new ExcelJS.Workbook(), ws = wb.addWorksheet(`BPF ${annee}`);
    ws.columns = [{ width: 60 }, { width: 18 }, { width: 18 }];
    ws.addRow([`Préparation du Bilan pédagogique et financier ${annee} — ${d().identite.nom} (NDA ${d().identite.nda})`]).font = { bold: true, size: 14 };
    ws.addRow(["À vérifier avant déclaration sur Mon Activité Formation (échéance " + fr(b.echeance) + ")"]);
    ws.addRow([]); ws.addRow(["Cadre C — Produits", "Montant HT"]).font = { bold: true };
    for (const [k, v] of Object.entries(b.C)) ws.addRow([P.ORIGINES[k], v]);
    ws.addRow(["Total des produits", b.totalProduits]).font = { bold: true };
    ws.addRow([]); ws.addRow(["Cadre D — Total des charges", b.charges]);
    ws.addRow([]); ws.addRow(["Cadre F — Public", "Stagiaires", "Heures-stagiaires"]).font = { bold: true };
    for (const x of b.F1) ws.addRow([x.lib, x.nombre, x.heures]);
    ws.addRow(["Total", b.totalStagiaires, b.totalHeures]).font = { bold: true };
    ws.addRow([]); ws.addRow(["Cadre E — Heures dispensées par le dirigeant formateur", b.heuresFormateur]); ws.addRow(["Cadre G — Produits reçus en sous-traitance", b.sousTraitanceRecue]);
    return [`BPF_preparation_${annee}.xlsx`, new Blob([await wb.xlsx.writeBuffer()])];
  }

  // ------------------------------------------------------------ PARTENAIRES
  function vPartenaires() {
    const ps = d().partenaires.slice().sort((x, y) => (x.relance || "9").localeCompare(y.relance || "9"));
    return `<header class="titre-vue"><h1>Partenaires</h1><p>Entreprises d'accueil, prescripteurs (France Travail, Missions Locales, Cap Emploi…), OPCO, organismes donneurs d'ordre. Votre temps le plus précieux : le logiciel vous rappelle qui relancer.</p></header>
      <div class="deux-colonnes"><section class="carte"><h2>Ajouter un partenaire</h2><form id="f-part" class="grille-champs">
        ${champ("Nom de la structure", "nom", "", "text", "required")}<label>Type<select name="type">${opt(P.TYPES_PARTENAIRE, "entreprise")}</select></label>
        ${champ("Contact (nom, fonction)", "contact", "")}${champ("Téléphone", "telephone", "", "tel")}${champ("E-mail", "email", "", "email")}
        ${champ("Prochaine relance", "relance", "", "date")}${champ("Objet de la relance", "objet", "")}${champ("Apprenants placés / orientés", "places", "0", "number", 'min="0"')}
        <label class="large">Notes<textarea name="notes" rows="2"></textarea></label><button class="principal-court" type="submit">Ajouter</button></form></section>
      <section class="carte"><h2>Messages prêts à copier</h2>${["relance_facture", "partenariat", "froid"].map((k) => `<button class="second" data-act="modele-mail" data-k="${k}">${esc({ relance_facture: "Relance de facture", partenariat: "Proposition de partenariat (entreprise d'accueil)", froid: "Questionnaire à froid (J+90)" }[k])}</button>`).join(" ")}
        <textarea id="mail" rows="9" aria-label="Message" readonly></textarea><button class="second" data-act="copier-mail">Copier</button></section></div>
      <div class="defile"><table><thead><tr><th>Structure</th><th>Type</th><th>Contact</th><th>Prochaine relance</th><th class="num">Placés</th><th></th></tr></thead><tbody>
      ${ps.map((p) => `<tr class="${p.relance && p.relance < auj() ? "retard" : ""}"><td><b>${esc(p.nom)}</b>${p.notes ? `<br><small class="discret">${esc(p.notes)}</small>` : ""}</td><td>${esc(P.TYPES_PARTENAIRE[p.type] || "")}</td><td>${esc(p.contact)}<br><small>${esc(p.telephone)} ${esc(p.email)}</small></td>
        <td><input type="date" value="${esc(p.relance || "")}" data-act="relance-part" data-id="${esc(p.id)}" aria-label="Prochaine relance"> ${esc(p.objet || "")}</td><td class="num">${esc(p.places || 0)}</td><td><button class="lien danger" data-act="suppr-part" data-id="${esc(p.id)}">Retirer</button></td></tr>`).join("") || `<tr><td colspan="6" class="discret">Aucun partenaire.</td></tr>`}</tbody></table></div>`;
  }
  const MAILS = {
    relance_facture: (I) => `Objet : Facture en attente de règlement\n\nBonjour,\n\nSauf erreur de notre part, la facture ${"[n°]"} d'un montant de ${"[montant]"} relative à la formation ${"[intitulé]"} reste à ce jour impayée (échéance du ${"[date]"}).\n\nPourriez-vous nous indiquer la date prévue de règlement ? Le RIB figure sur la facture.\n\nBien cordialement,\n${I.dirigeant}\n${I.nom} — ${I.telephone || ""}`,
    partenariat: (I) => `Objet : Accueil d'apprenants en entreprise — ${I.nom}\n\nBonjour,\n\n${I.nom}, organisme de formation certifié Qualiopi à La Réunion, forme des futurs professionnels motivés. Nous recherchons des entreprises partenaires pour accueillir nos apprenants en stage ou en alternance.\n\nPour vous : un recrutement préparé, un suivi régulier par le formateur, des aides possibles à l'embauche en alternance.\n\nSeriez-vous disponible pour un échange de 15 minutes cette semaine ?\n\nBien cordialement,\n${I.dirigeant}\n${I.telephone || ""} · ${I.email || ""}`,
    froid: (I) => `Objet : 3 minutes pour nous dire ce que la formation vous a apporté\n\nBonjour,\n\nIl y a trois mois, vous avez suivi une formation avec ${I.nom}. Votre retour nous aide à améliorer nos formations : 4 questions, 3 minutes.\n\n1. Utilisez-vous ce que vous avez appris dans votre travail ?\n2. La formation vous a-t-elle aidé à obtenir ou garder un emploi ?\n3. Avez-vous obtenu la certification visée ?\n4. Recommanderiez-vous cette formation ?\n\nMerci beaucoup,\n${I.dirigeant}`,
  };
  function aPartenaires() {
    lierCommun();
    $("#f-part").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target), x = { id: uid() }; for (const [k, v] of fd.entries()) x[k] = String(v).slice(0, 1000); d().partenaires.push(x); sauver(); rendre(); toast("Partenaire ajouté."); };
  }

  // ------------------------------------------------------------ RÉGLAGES
  function vReglages() {
    const I = d().identite, c = d().charte;
    return `<header class="titre-vue"><h1>Réglages</h1></header>
      <form id="f-ident" class="carte"><h2>Identité du centre (remplit tous les documents)</h2><div class="grille-champs">
        ${[["Nom", "nom"], ["Dirigeant / formateur", "dirigeant"], ["SIRET", "siret"], ["N° de déclaration d'activité (NDA)", "nda"], ["N° de certificat Qualiopi", "qualiopi"], ["Organisme certificateur", "certificateur"], ["Adresse", "adresse"], ["Code postal", "code_postal"], ["Ville", "ville"],
          ["Téléphone", "telephone"], ["E-mail", "email"], ["Site internet", "site"], ["IBAN (factures)", "iban"], ["BIC", "bic"], ["Référent handicap", "referent_handicap"], ["Délai d'accès aux formations", "delai_acces"], ["Horaires standard", "horaires"], ["N° de TVA intracommunautaire", "tva_intra"]].map(([l, k]) => champ(l, k, I[k])).join("")}
        ${champ("Certificat Qualiopi valable jusqu'au", "qualiopi_validite", I.qualiopi_validite, "date")}${champ("Début de la période d'audit", "audit_debut", I.audit_debut, "date")}${champ("Fin de la période d'audit", "audit_fin", I.audit_fin, "date")}
        ${champ("TVA appliquée à partir du", "tva_debut", I.tva_debut, "date")}${champ("Taux de TVA (La Réunion)", "taux_tva", I.taux_tva, "number", 'step="0.1"')}
        <label class="coche"><input type="checkbox" name="attestation_3511" ${I.attestation_3511 ? "checked" : ""}>J'ai l'attestation 3511-SD (formation exonérée de TVA, art. 261-4-4° a du CGI)</label></div>
        <p class="discret petit">Avant la date de TVA : « TVA non applicable — article 293 B du CGI » sur devis et factures. Après : TVA ${String(I.taux_tva || 8.5).replace(".", ",")} % (formation exonérée seulement avec l'attestation 3511-SD ; le conseil et l'implémentation restent soumis à la TVA).</p>
        <button class="principal-court" type="submit">Enregistrer</button></form>
      <form id="f-charte" class="carte"><h2>Charte graphique</h2>${c.couleurs_validees ? "" : `<p class="message alerte">Couleurs provisoires : saisissez les codes exacts de la charte YEBA FORMATIONS.</p>`}<div class="grille-champs">
        ${[["Couleur principale", "couleur_primaire"], ["Couleur d'accent", "couleur_secondaire"], ["Fond des bandes", "couleur_claire"], ["Texte", "couleur_texte"]].map(([l, k]) => `<label>${l}<input type="color" name="${k}" value="#${esc(c[k])}"></label>`).join("")}
        ${champ("Police des titres", "police_titres", c.police_titres || "Montserrat")}${champ("Police du texte", "police", c.police)}${champ("Taille du texte (14 minimum)", "taille_texte", c.taille_texte, "number", 'min="14" max="28"')}
        <label>Logo (PNG ou JPEG)<input type="file" id="logo" accept=".png,.jpg,.jpeg"><small>${c.logo ? "Logo enregistré" : "Aucun logo"}</small></label></div>
        ${c.logo ? `<p><img src="${esc(c.logo)}" alt="Logo actuel" class="apercu-logo"></p>` : ""}
        <p class="discret petit">Règle d'accessibilité appliquée automatiquement : l'or #${esc(c.couleur_secondaire)} n'est jamais utilisé en texte sur fond clair (contraste ${D.contraste(c.couleur_secondaire, "FFFFFF").toFixed(2).replace(".", ",")}:1, minimum 4,5:1) ; il reste réservé aux filets, aplats et au texte sur fond bleu (${D.contraste(c.couleur_secondaire, c.couleur_primaire).toFixed(2).replace(".", ",")}:1). Polices Montserrat et Inter : gratuites (licence SIL OFL), à installer sur l'ordinateur qui projette, sinon PowerPoint les remplace.</p>
        <div class="actions"><button class="principal-court" type="submit">Enregistrer</button>${c.logo ? `<button type="button" class="second" data-act="retirer-logo">Retirer le logo</button>` : ""}</div></form>
      <section class="carte"><h2>Sauvegarde et transfert</h2><p>La sauvegarde est un fichier chiffré : il ne s'ouvre qu'avec votre mot de passe. Gardez-en une copie sur une clé USB ou un stockage européen. ${d().derniere_sauvegarde ? "Dernière : " + fr(d().derniere_sauvegarde.slice(0, 10)) + "." : "Aucune sauvegarde pour l'instant."}</p>
        <div class="actions"><button class="principal-court" data-act="sauvegarde">Télécharger la sauvegarde chiffrée</button><button class="second" data-act="verrouiller">Verrouiller maintenant</button></div>
        <h3>Banque</h3><p class="discret">Import du relevé (CSV ou OFX) dans Finances : rapprochement automatique, toujours confirmé par vous. Une connexion bancaire directe (DSP2) passe obligatoirement par un agrégateur agréé par l'ACPR et un petit serveur : elle n'est pas activée dans cette version 100 % locale.</p></section>
      <section class="carte"><h2>Conformité</h2><ul>
        <li><b>RGPD</b> : données chiffrées dans votre navigateur (AES-256), jamais envoyées à un serveur. Seuls les objectifs pédagogiques d'une séance sont transmis à Claude quand vous demandez une rédaction, jamais les noms des stagiaires ni vos finances.</li>
        <li><b>IA Act</b> : la rédaction des séances utilise une IA générative (Claude). Vous restez l'auteur : relisez et validez chaque contenu (maîtrise de l'IA, article 4). Les apprenants doivent savoir que les supports ont été préparés avec l'aide d'une IA s'ils vous le demandent ; aucune décision les concernant n'est prise par l'IA.</li></ul>
        <button class="lien danger" data-act="effacer">Effacer toutes les données de ce navigateur</button></section>`;
  }
  function aReglages() {
    lierCommun();
    $("#f-ident").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target); for (const [k, v] of fd.entries()) d().identite[k] = String(v).slice(0, 300);
      d().identite.attestation_3511 = !!fd.get("attestation_3511"); d().identite.taux_tva = P.num(fd.get("taux_tva")) || 8.5; P.synchroAttendus(d()); sauver(); toast("Identité enregistrée."); };
    $("#f-charte").onsubmit = (e) => { e.preventDefault(); const fd = new FormData(e.target), c = d().charte;
      for (const k of ["couleur_primaire", "couleur_secondaire", "couleur_claire", "couleur_texte"]) c[k] = String(fd.get(k)).replace("#", "").toUpperCase();
      c.police = String(fd.get("police") || "Arial").replace(/[^A-Za-z0-9 \-]/g, "").slice(0, 40) || "Arial"; c.police_titres = String(fd.get("police_titres") || c.police).replace(/[^A-Za-z0-9 \-]/g, "").slice(0, 40) || c.police; c.taille_texte = Math.min(28, Math.max(14, P.num(fd.get("taille_texte")) || 14)); c.taille_titre = c.taille_texte + 8;
      c.couleurs_validees = true; sauver(); appliquerCharte(); rendre(); toast("Charte enregistrée."); };
    $("#logo").onchange = (e) => { const fi = e.target.files[0]; if (!fi || fi.size > 5e6) return; const r = new FileReader();
      r.onload = async () => { const propre = await chargerLogo(r.result); if (propre) { d().charte.logo = propre; sauver(); rendre(); toast("Logo enregistré."); } else toast("Image illisible.", "ko"); }; r.readAsDataURL(fi); };
  }

  // ------------------------------------------------------------ actions globales (délégation)
  function lierCommun() {}
  document.addEventListener("click", async (e) => {
    const go = e.target.closest("[data-go]");
    if (go) { e.preventDefault(); aller(go.dataset.go); return; }
    const b = e.target.closest("[data-act]");
    if (!b || b.tagName === "SELECT" || b.tagName === "TEXTAREA" || (b.tagName === "INPUT" && b.type !== "button")) return;
    const act = b.dataset.act;
    try {
      if (act === "ouvrir-formation") { etat.formationSel = b.dataset.id; rendre(); }
      else if (act === "retour-formations") { etat.formationSel = null; rendre(); }
      else if (act === "ouvrir-seance" || act === "noter-seance") { etat.formationSel = b.dataset.f; etat.jourSel = b.dataset.d; aller("seance"); if (act === "noter-seance") setTimeout(() => $("#f-noter")?.scrollIntoView({ behavior: "smooth" }), 50); }
      else if (act === "generer") { genererSeance(formationCourante(), etat.jourSel); }
      else if (act === "stop") { etat.generation?.ctl.abort(); }
      else if (act === "dl-pack") {
        const f = formationCourante(); b.disabled = true;
        const fichiers = await fichiersPack(f, etat.jourSel), idx = { pptx: 0, exo: 1, ress: 2, grille: 3, quiz: 4, fiche: 5 }[b.dataset.k];
        if (b.dataset.k === "tout") { const [n, z] = await zip(`Seance_${etat.jourSel}_${(f.code || "formation").toLowerCase()}.zip`, fichiers); await enregistrer(n, z); }
        else await enregistrer(...fichiers[idx]);
        b.disabled = false;
      }
      else if (act === "exp-f") {
        const f = formationCourante(), ctx = contexteF(f), s = ctx.sigle;
        const faire = { xlsx: async () => [`Decorticage_${s}.xlsx`, await D.classeur(ctx)], prog: async () => [`Programme_${s}.docx`, await D.programmeDocx(ctx)], exam: async () => [`Examen_simplifie_${s}.docx`, await D.examenDocx(ctx)] };
        if (b.dataset.k === "tout") { const parts = []; for (const k of ["xlsx", "prog", "exam"]) parts.push(await faire[k]()); parts.push([`Page_programme_${s}.html`, new Blob([D.pageSite(ctx)])]); await enregistrer(`Decorticage_${s}_complet.zip`, await D.toutEnZip(ctx, parts)); }
        else await enregistrer(...(await faire[b.dataset.k]()));
      }
      else if (act === "annuler-journal") { const f = formationCourante(); f.journal = f.journal.filter((j) => j.date !== b.dataset.d); sauver(); rendre(); toast("Saisie annulée : planning recalculé."); }
      else if (act === "suppr-formation") { if (b.dataset.confirme) { d().formations = d().formations.filter((x) => x.id !== etat.formationSel); etat.formationSel = null; sauver(); rendre(); } else { b.dataset.confirme = "1"; b.textContent = "Cliquez à nouveau pour confirmer la suppression"; } }
      else if (act === "nouvelle-action") { const a = { id: uid(), intitule: "", type: "continue", statut: "prospect", origine: "entreprises", tva: "", stagiaires: [], docs: {}, pieces: [] }; d().actions.push(a); etat.actionSel = a.id; aller("actions"); }
      else if (act === "voir-action") { etat.actionSel = b.dataset.id; aller("actions"); }
      else if (act === "retour-actions") { etat.actionSel = null; rendre(); }
      else if (act === "ajout-stag") { const tb = $("#t-stag tbody"); tb.insertAdjacentHTML("beforeend", ligneStag({}, tb.children.length)); }
      else if (act === "suppr-stag") { b.closest("tr").remove(); }
      else if (act === "suppr-action") { if (b.dataset.confirme) { d().actions = d().actions.filter((x) => x.id !== etat.actionSel); etat.actionSel = null; sauver(); rendre(); } else { b.dataset.confirme = "1"; b.textContent = "Cliquez à nouveau pour confirmer"; } }
      else if (act === "gen-doc" || act === "gen-tous") {
        const a = d().actions.find((x) => x.id === etat.actionSel); lireAction($("#f-action"), a);
        const ids = act === "gen-doc" ? [b.dataset.doc] : P.documentsAttendus(a).map((x) => x.id);
        const fichiers = [];
        for (const id of ids) { fichiers.push(await P.genererDocument(d(), a, id, etat.logo)); a.docs[id] = a.docs[id] || {}; if (a.docs[id].etat !== "fait") a.docs[id].etat = "genere"; }
        sauver();
        if (fichiers.length === 1) await enregistrer(...fichiers[0]); else await enregistrer(...(await zip(`Documents_${(a.intitule || "action").replace(/[^A-Za-z0-9]+/g, "_").slice(0, 40)}.zip`, fichiers)));
        rendre();
      }
      else if (act === "dl-piece") { const m = d().fichiers[b.dataset.id]; await enregistrer(m.nom, new Blob([await C.lireFichier(b.dataset.id)])); }
      else if (act === "suppr-piece") { const a = d().actions.find((x) => x.id === etat.actionSel); await C.supprimerFichier(b.dataset.id); a.pieces = a.pieces.filter((x) => x !== b.dataset.id); sauver(); rendre(); }
      else if (act === "dossier-audit") await enregistrer(`Dossier_preuves_Qualiopi_${auj()}.docx`, await dossierAudit());
      else if (act === "ajout-ind") { const q = d().qualiopi, n = 34 + (q.ajouts || []).length; (q.ajouts = q.ajouts || []).push({ n, critere: 7, portee: "tous", libelle: "Nouvel indicateur — saisissez son intitulé officiel dans les remarques" }); sauver(); rendre(); toast(`Indicateur ${n} ajouté au critère 7 (modifiable).`); }
      else if (act === "confirmer-rap") { P.confirmer(d(), b.dataset.m, b.dataset.a); sauver(); rendre(); toast("Virement rattaché. Le logiciel s'en souviendra pour ce payeur."); }
      else if (act === "confirmer-autre") { const sel = $("#sel-" + b.dataset.m); if (sel && sel.value) { P.confirmer(d(), b.dataset.m, sel.value); sauver(); rendre(); toast("Virement rattaché."); } }
      else if (act === "confirmer-surs") { let n = 0; for (const m of d().mouvements.filter((x) => x.etat === "a_confirmer")) { const [p1, p2] = m.propositions || []; if (p1 && p1.score >= 0.9 && !(p2 && p2.score >= 0.6)) { P.confirmer(d(), m.id, p1.attenduId); n++; } } sauver(); rendre(); toast(`${n} virement(s) rattaché(s).`); }
      else if (act === "classer-mvt") { P.classer(d(), b.dataset.m, ($("#cls-" + b.dataset.m) || {}).value || "autres"); sauver(); rendre(); toast("Classé en autre recette."); }
      else if (act === "ignorer-mvt") { P.classer(d(), b.dataset.m, "ignorer"); sauver(); rendre(); }
      else if (act === "ouvrir-paiement") { etat.paiementOuvert = etat.paiementOuvert === b.dataset.a ? null : b.dataset.a; rendre(); }
      else if (act === "annuler-enc") { P.annulerEncaissement(d(), b.dataset.a, b.dataset.e); sauver(); rendre(); toast("Encaissement annulé."); }
      else if (act === "suppr-attendu") { const x = d().attendus.find((y) => y.id === b.dataset.a); if (x && !P.recu(x)) { d().attendus = d().attendus.filter((y) => y !== x); sauver(); rendre(); } else toast("Annulez d'abord les paiements reçus.", "alerte"); }
      else if (act === "gen-biblio") { await enregistrer(...(await P.genererBiblio(d(), b.dataset.id, etat.logo))); }
      else if (act === "suppr-ecr") { d().ecritures = d().ecritures.filter((x) => x.id !== b.dataset.id); sauver(); rendre(); }
      else if (act === "exp-compta") await enregistrer(`Tableau_comptable_${auj()}.xlsx`, await exportCompta());
      else if (act === "exp-bpf") await enregistrer(...(await exportBpf()));
      else if (act === "suppr-part") { d().partenaires = d().partenaires.filter((x) => x.id !== b.dataset.id); sauver(); rendre(); }
      else if (act === "modele-mail") { $("#mail").value = MAILS[b.dataset.k](d().identite); }
      else if (act === "copier-mail") { const t = $("#mail"); try { await navigator.clipboard.writeText(t.value); toast("Copié."); } catch (err) { t.select(); toast("Sélectionné : faites Ctrl+C.", "alerte"); } }
      else if (act === "sauvegarde") { const txt = await C.exporter(); d().derniere_sauvegarde = new Date().toISOString(); sauver(); await enregistrer(`Sauvegarde_pilotage_${auj()}.json`, txt); rendre(); }
      else if (act === "verrouiller") { C.verrouiller(); afficherConnexion("Coffre verrouillé."); }
      else if (act === "retirer-logo") { d().charte.logo = ""; etat.logo = null; sauver(); rendre(); }
      else if (act === "effacer") { if (b.dataset.confirme) { await C.effacer(); afficherConnexion("Données effacées de ce navigateur."); } else { b.dataset.confirme = "1"; b.textContent = "Cliquez à nouveau : TOUT sera effacé (faites une sauvegarde avant)"; } }
    } catch (err) { b.disabled = false; toast(err.message || String(err), "ko"); }
  });
  document.addEventListener("change", (e) => {
    const el = e.target, act = el.dataset && el.dataset.act;
    if (!act) return;
    if (act === "etat-doc") { const a = d().actions.find((x) => x.id === etat.actionSel); a.docs = a.docs || {}; a.docs[el.dataset.doc] = Object.assign(a.docs[el.dataset.doc] || {}, { etat: el.value, date: auj() }); sauver(); }
    else if (act === "statut-ind" || act === "na-ind" || act === "note-ind") {
      const n = el.closest("[data-n]").dataset.n, s = (d().qualiopi.suivi[n] = d().qualiopi.suivi[n] || {});
      if (act === "statut-ind") s.statut = el.value; else if (act === "na-ind") s.na = el.checked; else s.note = el.value.slice(0, 4000);
      sauver();
      if (act !== "note-ind") rendre();
    }
    else if (act === "tri-att") { etat.triAtt = el.value; rendre(); }
    else if (act === "filtre-att") { etat.filtreAtt = el.value; rendre(); }
    else if (act === "grouper-att") { etat.grouperAtt = el.checked; rendre(); }
    else if (act === "statut-bib") { const v = (d().bibliotheque[el.dataset.id] = d().bibliotheque[el.dataset.id] || {}); v.statut = el.value; sauver(); }
    else if (act === "depot-biblio") {
      const fi = el.files[0]; if (!fi) return;
      if (fi.size > 15 * 1024 * 1024) { toast("15 Mo maximum.", "ko"); return; }
      (async () => { const id = await C.deposerFichier(fi.name.slice(0, 120), fi.type, new Uint8Array(await fi.arrayBuffer()));
        const v = (d().bibliotheque[el.dataset.id] = d().bibliotheque[el.dataset.id] || {}); (v.fichiers = v.fichiers || []).push(id); v.date = auj(); if (!v.statut || v.statut === "") v.statut = "en_vigueur";
        sauver(); rendre(); toast("Document déposé dans la bibliothèque (chiffré) : il prouve désormais les indicateurs liés."); })().catch((err) => toast(err.message, "ko"));
    }
    else if (act === "relance-part") { const p = d().partenaires.find((x) => x.id === el.dataset.id); p.relance = el.value; sauver(); }
  });

  // ------------------------------------------------------------ démarrage
  document.querySelectorAll("#nav a").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); if (C.cle) { if (a.dataset.v === "formations") etat.formationSel = null; if (a.dataset.v === "actions") etat.actionSel = null; aller(a.dataset.v); } }));
  afficherConnexion();
})();

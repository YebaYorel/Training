
// ------------------------------------------------------------------ RÈGLES PERMANENTES DE PROSPECTION (Aurélien, 22/11/2026)
// 1. Chaque message parle du MÉTIER du destinataire et lui permet de dire STOP (ou STP) ; une opposition bloque tout envoi.
// 2. Expéditeur : yebaformations@gmail.com uniquement (compte Gmail connecté), jamais l'adresse personnelle.
// 3. Aurélien seul décideur : Pilotage propose et ne crée que des BROUILLONS ; Aurélien valide puis envoie lui-même.
const EXPEDITEUR = "yebaformations@gmail.com", ADRESSE_PERSO = "aurelienlumeka@gmail.com";
const MOTS_STOP = /(^|[^a-zà-ÿ])(stop|stp)([^a-zà-ÿ]|$)/i;
const WEBMAILS = /^(gmail|yahoo|hotmail|outlook|orange|wanadoo|free|laposte|icloud|live|sfr)\./;
const domaineDe = (m) => String(m || "").trim().toLowerCase().split("@")[1] || "";
function estOppose(mail) {
  const m = String(mail || "").trim().toLowerCase(), dom = domaineDe(m);
  if (!m) return false;
  return (M.at.stop || []).some((o) => o.email === m || (o.domaine && o.domaine === dom));
}
function reglesMessage(e, objet, corps) {
  const err = [];
  if (!e.mail) err.push("Pas d'adresse e-mail pour ce prospect.");
  if (!e.secteur) err.push("Règle 1 : renseignez le métier / secteur du destinataire dans Airtable.");
  else {
    const mots = sansAccents(e.secteur).split(/[^a-z0-9]+/).filter((w) => w.length > 3);
    if (mots.length && !mots.some((w) => sansAccents(objet + " " + corps).includes(w))) err.push(`Règle 1 : le message ne parle pas de son métier (« ${e.secteur} »).`);
  }
  if (!MOTS_STOP.test(corps)) err.push("Règle 1 : la phrase « répondez STOP » manque.");
  if (estOppose(e.mail)) err.push("STOP : cette personne ou son entreprise a demandé à ne plus être contactée.");
  if (String(e.mail || "").toLowerCase().includes(ADRESSE_PERSO)) err.push("Règle 2 : adresse personnelle détectée.");
  return err;
}
const BANDEAU_REGLES = `<section class="carte ck-bloc"><div class="ck-bloc-tete"><h2>${ICONES.conformite} Vos 3 règles, toujours actives</h2></div><ol class="petit">
  <li><b>Son métier + STOP</b> : chaque message parle du métier du destinataire et lui permet de répondre STOP (ou STP) ; une opposition bloque tout nouvel envoi.</li>
  <li><b>Expéditeur</b> : ${EXPEDITEUR} uniquement (le compte Gmail connecté à claude.ai), jamais l'adresse personnelle.</li>
  <li><b>Vous décidez</b> : Pilotage propose et ne crée que des brouillons ; vous validez (double clic) puis vous envoyez vous-même depuis Gmail.</li></ol></section>`;

ACT["stop-ajouter"] = async (b) => {
  const mail = String(b.dataset.mail || "").trim().toLowerCase();
  if (!mail) { toast("Pas d'adresse e-mail : ajoutez-la dans Airtable, puis enregistrez le STOP.", "ko"); return; }
  if (!confirmer(b, "Confirmer le STOP")) return;
  const dom = domaineDe(mail), domaine = b.dataset.domaine === "1" && !WEBMAILS.test(dom) ? dom : undefined;
  await occupe(b, () => ecrire("stop", [{ fields: champs("stop", { email: mail, domaine, date: auj(), motif: b.dataset.motif || "Réponse STOP", entreprise: b.dataset.nom || undefined }) }], { creer: true }));
  await charger("stop", true).catch(() => {});
  toast(`${mail} ne sera plus contacté.`);
  monterCommercial();
};
ACT["stop-gmail"] = async (b) => {
  const zone = $("#ck-stop-gmail");
  if (!zone) return;
  zone.innerHTML = squelette(2);
  try {
    const r = await occupe(b, () => lireOutil("Gmail", "search_threads", { query: "in:inbox newer_than:180d (STOP OR STP OR désinscrire OR désabonner)", pageSize: 25 }, { staleTime: 0, gcTime: 60000, refresh: true }), "Recherche…");
    const pl = r.payload && typeof r.payload === "object" ? r.payload : {};
    const fils = (pl.threads || []).map(normFil).filter((f) => MOTS_STOP.test(f.extrait + " " + f.sujet) || /d[ée]sinscri|d[ée]sabonn/i.test(f.extrait));
    const vus = new Set(), nouveaux = [];
    for (const f of fils) { const mail = adresseDe(f.de).toLowerCase(); if (mail && mail !== EXPEDITEUR && !estOppose(mail) && !vus.has(mail)) { vus.add(mail); nouveaux.push({ f, mail }); } }
    poser(zone, nouveaux.length ? `<ul class="ck-liste">${nouveaux.map((x) => `<li class="ck-item"><b>${esc(nomDe(x.f.de))}</b><small class="discret">${esc(x.f.sujet)} · « ${esc(x.f.extrait.slice(0, 160))} »</small>
      <div class="actions"><button type="button" class="principal-court ck-mini" data-ck="stop-ajouter" data-mail="${esc(x.mail)}" data-motif="Réponse STOP (Gmail)">${ICONES.stop} Enregistrer le STOP</button>${lienExt(x.f.url, "Lire le message")}</div></li>`).join("")}</ul>
      <p class="petit discret">Relisez chaque réponse avant d'enregistrer : c'est vous qui décidez.</p>` : `<p class="discret">Aucune nouvelle réponse STOP dans Gmail (180 derniers jours).</p>`);
  } catch (e) { poser(zone, `<p class="message ko">${esc(msgGenerique(e))}</p>`); }
};
function comStop(r) {
  if (!r.stop) return bandeau(M.err.stop, "Airtable", "rafraichir");
  const L = r.stop.slice().sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  return `${BANDEAU_REGLES}<section class="carte ck-bloc"><div class="ck-bloc-tete"><h2>${ICONES.stop} Liste STOP (${L.length})</h2>${lienExt(`https://airtable.com/${BASE}/${T.stop}`, "Ouvrir dans Airtable")}</div>
    <p class="discret petit">Conservée pour respecter l'opposition (RGPD art. 21) : ces adresses, et les domaines bloqués, ne reçoivent plus aucun message de prospection.</p>
    <div class="actions"><button type="button" class="second" data-ck="stop-gmail">${ICONES.mail} Chercher les réponses STOP dans Gmail</button></div><div id="ck-stop-gmail"></div>
    <form class="ck-form-ligne" data-ckf="stop-manuel"><label class="ck-grand">Ajouter une adresse à la main<input name="mail" type="email" required placeholder="adresse@entreprise.re"></label>
      <label><input type="checkbox" name="domaine" value="1"> toute l'entreprise (même domaine)</label><button class="second" type="submit">${ICONES.plus} Ajouter</button></form>
    ${L.length ? `<ul class="ck-liste">${L.map((o) => `<li class="ck-item"><div class="ck-item-tete">${puce("STOP", "ko")}${o.domaine ? puce("domaine " + o.domaine, "att") : ""}</div><b>${esc(o.email)}</b>
      <small class="discret">${esc([o.entreprise, o.motif, o.date ? "le " + frDate(o.date) : ""].filter(Boolean).join(" · "))}</small></li>`).join("")}</ul>` : `<p class="discret">Personne n'a encore demandé STOP.</p>`}</section>`;
}
FORM["stop-manuel"] = async (f) => {
  const fd = new FormData(f), mail = String(fd.get("mail") || "").trim().toLowerCase(), b = $("button[type=submit]", f);
  if (!mail) return;
  const dom = domaineDe(mail), domaine = fd.get("domaine") && !WEBMAILS.test(dom) ? dom : undefined;
  await occupe(b, () => ecrire("stop", [{ fields: champs("stop", { email: mail, domaine, date: auj(), motif: "Ajout manuel" }) }], { creer: true }));
  await charger("stop", true).catch(() => {});
  toast(`${mail} ajouté à la liste STOP.`);
  monterCommercial();
};

// ------------------------------------------------------------------ APPELS D'OFFRES (veille BOAMP, décision d'Aurélien, réponse avec Remporte)
const BOAMP_API = "https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records";
const THEMES_AO = [["intelligence artificielle", 5], ["ia ", 3], ["numerique", 3], ["digital", 2], ["bureautique", 4], ["rgpd", 5], ["donnees personnelles", 4],
  ["cybersecurite", 4], ["management", 4], ["manager", 3], ["vente", 3], ["commercial", 3], ["relation client", 4], ["accueil", 2], ["soft skills", 4],
  ["communication", 2], ["competences transversales", 3], ["savoirs de base", 2], ["formation professionnelle", 2], ["formation continue", 2], ["formation", 1]];
function requeteBoamp(zone, jours) {
  const depuis = new Date(); depuis.setDate(depuis.getDate() - jours);
  const c = [`(search(objet,"formation") or descripteur_libelle="Formation")`, `dateparution>=date'${isoLocal(depuis)}'`];
  if (zone) c.push(`code_departement="${zone}"`);
  else c.push("(" + ["intelligence artificielle", "numérique", "bureautique", "RGPD", "management", "relation client", "vente", "cybersécurité"].map((m) => `search(objet,"${m}")`).join(" or ") + ")");
  return new URLSearchParams({ where: c.join(" and "), order_by: "dateparution desc", limit: "100",
    select: "idweb,objet,nomacheteur,dateparution,datelimitereponse,nature_libelle,descripteur_libelle,code_departement,url_avis,procedure_libelle" }).toString();
}
const aoOuvert = (a) => !!a.datelimitereponse && /avis de march/i.test(a.nature_libelle || "Avis de marché") && new Date(a.datelimitereponse) > new Date();
const joursAO = (iso) => (iso ? Math.ceil((new Date(iso) - new Date()) / 86400000) : null);
function scoreAvis(a) {
  const t = " " + sansAccents(`${a.objet} ${(a.descripteur_libelle || []).join(" ")}`) + " ", raisons = [];
  let s = 0;
  for (const [mot, p] of THEMES_AO) if (t.includes(mot)) { s += p; raisons.push(mot.trim()); }
  if ((a.code_departement || []).includes("974")) { s += 3; raisons.push("La Réunion"); }
  if (!aoOuvert(a)) s = Math.min(s, 2);
  return { s, raisons: [...new Set(raisons)] };
}
function propositionAO(a) {
  const { s } = scoreAvis(a), j = joursAO(a.datelimitereponse);
  if (!aoOuvert(a)) return "Clos ou résultat : utile pour connaître les acheteurs et les attributaires.";
  if (j !== null && j < 5) return `Moins de 5 jours (${j} j) : ne répondre que si le dossier est déjà prêt.`;
  if (s >= 7) return "Proposition : étudier le DCE en priorité (thème YEBA, délai suffisant).";
  if (s >= 4) return "Proposition : lire le règlement de consultation et vérifier les lots.";
  return "Proposition : peu aligné avec l'offre YEBA ; à écarter sauf lot précis.";
}
const BANDEAU_AO = `<section class="carte ck-bloc"><p class="petit">Pilotage <b>veille et propose</b> (score et règles visibles, jamais une décision). <b>Vous décidez</b> GO / NO-GO (double clic). Pour répondre : téléchargez le DCE sur la plateforme de l'acheteur, puis lancez <b>Remporte</b> dans Claude Code (commande copiée par le bouton) : il s'arrête pour vous faire valider l'analyse, le go/no-go et le plan.</p></section>`;
function comAO(r) {
  if (!r.ao) return bandeau(M.err.ao, "Airtable", "rafraichir");
  const zone = M.aoZone === undefined ? "974" : M.aoZone, jours = M.aoJours || 120, url = BOAMP_API + "?" + requeteBoamp(zone, jours);
  const suivis = r.ao.slice().sort((a, b) => (a.limite || "9").localeCompare(b.limite || "9"));
  return `${BANDEAU_AO}<section class="carte ck-bloc"><div class="ck-bloc-tete"><h2>${ICONES.loupe} Veille des marchés publics (BOAMP)</h2></div>
    <div class="ck-form-ligne"><label>Zone<select data-ckch="ao-zone"><option value="974"${zone === "974" ? " selected" : ""}>La Réunion (974) · toutes formations</option><option value=""${zone === "" ? " selected" : ""}>France entière · thèmes YEBA</option></select></label>
      <label>Parutions<select data-ckch="ao-jours">${[30, 60, 120, 365].map((n) => `<option value="${n}"${n === jours ? " selected" : ""}>${n === 365 ? "12 derniers mois" : n + " derniers jours"}</option>`).join("")}</select></label>
      <button type="button" class="principal-court" data-ck="ao-chercher">${ICONES.maj} Chercher les avis</button></div>
    <details class="petit"><summary>Si la recherche directe est bloquée par l'affichage</summary><p>1. ${lienExt(url, "Ouvrir la recherche BOAMP")} · 2. sur la page ouverte, tout sélectionner (Ctrl+A) et copier (Ctrl+C) · 3. coller ci-dessous.</p>
      <form data-ckf="ao-import"><label>Texte copié<textarea name="json" rows="3" placeholder='{"total_count": …, "results": [ … ]}'></textarea></label><button class="second" type="submit">Analyser</button></form></details>
    <div id="ck-ao-res">${M.aoRes ? rendreAvis(M.aoRes) : ""}</div>
    <p class="petit discret">Source : BOAMP, open data de la DILA (licence ouverte). Le BOAMP ne couvre pas les petits marchés publiés seulement sur le profil d'acheteur : gardez vos alertes sur les plateformes des acheteurs réunionnais.</p></section>
    <section class="carte ck-bloc"><div class="ck-bloc-tete"><h2>Marchés suivis (${suivis.length})</h2>${lienExt(`https://airtable.com/${BASE}/${T.ao}`, "Ouvrir dans Airtable")}</div>
    ${suivis.length ? `<ul class="ck-liste">${suivis.map(carteAO).join("")}</ul>` : `<p class="discret">Aucun marché suivi : cherchez les avis puis « Suivre ».</p>`}</section>`;
}
function rendreAvis(liste) {
  if (!liste.length) return `<p class="discret">Aucun avis sur cette période.</p>`;
  const suivis = new Set((M.at.ao || []).map((x) => x.ref));
  return `<ul class="ck-liste">${liste.map((a, i) => { const sc = scoreAvis(a), j = joursAO(a.datelimitereponse), ouv = aoOuvert(a);
    return `<li class="ck-item"><div class="ck-item-tete">${puce(ouv ? `ouvert · J-${j}` : (a.nature_libelle || "clos"), ouv ? (j <= 7 ? "ko" : "ok") : "")}${puce(`score ${sc.s}`, sc.s >= 7 ? "ok" : sc.s >= 4 ? "att" : "")}${suivis.has(a.idweb) ? puce("suivi", "ok") : ""}</div>
      <b>${esc(a.objet)}</b><small class="discret">${esc([a.nomacheteur, a.dateparution ? "paru le " + frDate(a.dateparution) : "", a.datelimitereponse ? "remise " + new Date(a.datelimitereponse).toLocaleString("fr-FR") : "", "n° " + a.idweb].filter(Boolean).join(" · "))}</small>
      <small>${esc(propositionAO(a))}${sc.raisons.length ? " (" + esc(sc.raisons.join(", ")) + ")" : ""}</small>
      <div class="actions">${suivis.has(a.idweb) ? "" : `<button type="button" class="second ck-mini" data-ck="ao-suivre" data-i="${i}">${ICONES.plus} Suivre</button>`}${lienExt(a.url_avis || `https://www.boamp.fr/pages/avis/?q=idweb:${a.idweb}`, "Lire l'avis")}</div></li>`; }).join("")}</ul>`;
}
function carteAO(x) {
  const j = joursAO(x.limite), go = x.decision === "GO", fini = /gagn|perdu|no-go/i.test(x.decision);
  return `<li class="ck-item"><div class="ck-item-tete">${puce(x.decision || "À étudier", go || /gagn/i.test(x.decision) ? "ok" : /no-go|perdu/i.test(x.decision) ? "ko" : "att")}${j !== null && !fini ? puce(j < 0 ? "date dépassée" : `J-${j}`, j <= 7 ? "ko" : "") : ""}${x.score ? puce(`score ${x.score}`) : ""}</div>
    <b>${esc(x.objet)}</b><small class="discret">${esc([x.acheteur, x.limite ? "remise " + new Date(x.limite).toLocaleString("fr-FR") : "", x.ref ? "n° " + x.ref : "", x.decideLe ? "décidé le " + frDate(x.decideLe) : ""].filter(Boolean).join(" · "))}</small>
    ${x.proposition ? `<small>${esc(x.proposition)}</small>` : ""}
    <div class="actions">${!x.decision || x.decision === "À étudier" ? `<button type="button" class="principal-court ck-mini" data-ck="ao-decider" data-id="${esc(x.id)}" data-d="GO">${ICONES.coche} Je décide : GO</button><button type="button" class="second ck-mini" data-ck="ao-decider" data-id="${esc(x.id)}" data-d="NO-GO">Je décide : NO-GO</button>` : ""}
      ${go || /réponse|dépos/i.test(x.decision) ? `<button type="button" class="second ck-mini" data-copier="/remporte:nouvel-ao ~/Téléchargements/DCE-${esc(x.ref || x.id)}.zip">${ICONES.copilote} Copier la commande Remporte</button>
        <select data-ckch="ao-statut" data-id="${esc(x.id)}" aria-label="Suivi de la réponse">${["GO", "Réponse en cours", "Déposé", "Gagné", "Perdu"].map((s) => `<option${s === x.decision ? " selected" : ""}>${s}</option>`).join("")}</select>` : ""}
      ${lienExt(x.url, "Lire l'avis")}${lienExt(urlFiche("ao", x.id), "Airtable")}</div></li>`;
}
SAISIE["ao-zone"] = (el) => { M.aoZone = el.value; M.aoRes = null; monterCommercial(); };
SAISIE["ao-jours"] = (el) => { M.aoJours = +el.value || 120; M.aoRes = null; monterCommercial(); };
SAISIE["ao-statut"] = async (el) => {
  try { await ecrire("ao", [{ id: el.dataset.id, fields: champs("ao", { decision: el.value }) }], { typecast: true }); await charger("ao", true); toast(`Suivi : ${el.value}.`); monterCommercial(); }
  catch (e) { toast(msgGenerique(e), "ko"); }
};
function lireAvisJson(texte) {
  const t = String(texte || ""), i = t.indexOf("{"), j = t.lastIndexOf("}");
  const o = JSON.parse(i >= 0 ? t.slice(i, j + 1) : t);
  return (o.results || []).filter((a) => a && a.idweb && a.objet).sort((a, b) => aoOuvert(b) - aoOuvert(a) || scoreAvis(b).s - scoreAvis(a).s);
}
ACT["ao-chercher"] = async (b) => {
  const zone = M.aoZone === undefined ? "974" : M.aoZone, url = BOAMP_API + "?" + requeteBoamp(zone, M.aoJours || 120), z = $("#ck-ao-res");
  if (z) z.innerHTML = squelette(3);
  try {
    const rep = await occupe(b, async () => { const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), 15000); try { return await fetch(url, { signal: ctl.signal, credentials: "omit", referrerPolicy: "no-referrer" }); } finally { clearTimeout(t); } }, "Veille…");
    if (!rep.ok) throw new Error("BOAMP a répondu " + rep.status);
    M.aoRes = lireAvisJson(await rep.text());
    poser(z, rendreAvis(M.aoRes));
  } catch (e) {
    poser(z, `<p class="message ko">La recherche directe est bloquée dans cet affichage. Utilisez « Si la recherche directe est bloquée » ci-dessus (2 clics et un coller).</p>`);
    const d = z && z.parentElement && z.parentElement.querySelector("details"); if (d) d.open = true;
  }
};
FORM["ao-import"] = async (f) => {
  const z = $("#ck-ao-res");
  try { M.aoRes = lireAvisJson(new FormData(f).get("json")); poser(z, rendreAvis(M.aoRes)); }
  catch (e) { poser(z, `<p class="message ko">Texte illisible : copiez toute la page BOAMP (elle commence par « { »).</p>`); }
};
ACT["ao-suivre"] = async (b) => {
  const a = M.aoRes && M.aoRes[+b.dataset.i];
  if (!a) return;
  const sc = scoreAvis(a);
  await occupe(b, () => ecrire("ao", [{ fields: champs("ao", { objet: String(a.objet).slice(0, 250), ref: a.idweb, acheteur: a.nomacheteur || undefined,
    limite: a.datelimitereponse || undefined, url: a.url_avis || `https://www.boamp.fr/pages/avis/?q=idweb:${a.idweb}`, departements: (a.code_departement || []).join(", ") || undefined,
    score: sc.s, proposition: propositionAO(a) + (sc.raisons.length ? " Critères : " + sc.raisons.join(", ") + "." : ""), decision: "À étudier" }) }], { creer: true, typecast: true }));
  await charger("ao", true).catch(() => {});
  toast("Marché suivi dans Airtable.");
  monterCommercial();
};
ACT["ao-decider"] = async (b) => {
  const d = b.dataset.d;
  if (!confirmer(b, d === "GO" ? "Je confirme : GO" : "Je confirme : NO-GO")) return;
  await occupe(b, () => ecrire("ao", [{ id: b.dataset.id, fields: champs("ao", { decision: d, decideLe: auj() }) }], { typecast: true }));
  await charger("ao", true).catch(() => {});
  toast(d === "GO" ? "GO enregistré : préparez la réponse avec Remporte." : "NO-GO enregistré.");
  monterCommercial();
};

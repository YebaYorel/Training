/* Finances d'un organisme de formation indépendant.
 *
 * Trois notions, volontairement séparées :
 *  - ce qu'on doit me payer : les SOMMES ATTENDUES (une par facture ou par part de financement :
 *    l'OPCO paie une part, l'entreprise le reste…), créées automatiquement depuis les actions ;
 *  - ce qui est arrivé sur le compte : les MOUVEMENTS BANCAIRES importés (relevé CSV ou OFX) ;
 *  - le lien entre les deux : une PROPOSITION de rapprochement (montant + ressemblance du nom +
 *    référence de facture), que VOUS confirmez toujours. Aucune somme n'est marquée reçue sans vous.
 * Le BPF (Cerfa 10443) se déclare sur « Mon Activité Formation » avant le 31 mai : les montants
 * calculés ici sont une PRÉPARATION, à vérifier ligne par ligne. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const D = G.Decorticage;
  const jourIso = () => new Date().toISOString().slice(0, 10);
  const num = (v) => { const n = parseFloat(String(v ?? "").replace(/[\s ]/g, "").replace(",", ".")); return isFinite(n) ? n : 0; };
  const arrondi = (n) => Math.round(n * 100) / 100;
  const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);
  const identite = () => (P.Coffre && P.Coffre.donnees && P.Coffre.donnees.identite) || {};

  // ------------------------------------------------------------------ TVA
  /* Régime applicable à une facture, selon sa date :
   *  - avant la date de passage (01/02/2027 par défaut) : franchise en base, « TVA non applicable, art. 293 B du CGI » ;
   *  - ensuite : TVA au taux normal de La Réunion (8,5 %), sauf exonération de la formation professionnelle
   *    (art. 261-4-4° a du CGI) si vous détenez l'attestation n° 3511-SD et qu'il s'agit d'une action de formation. */
  const REGIMES = { franchise: "Franchise en base (art. 293 B du CGI)", tva: "TVA applicable", exonere: "Exonéré (art. 261-4-4° a du CGI, attestation 3511-SD)" };
  function regimeTva(a, id = identite()) {
    const date = a.date_facture || a.fin || a.debut || jourIso();
    let code = a.tva && REGIMES[a.tva] ? a.tva : date >= (id.tva_debut || "2027-02-01") ? (id.attestation_3511 && a.nature !== "conseil" ? "exonere" : "tva") : "franchise";
    const taux = code === "tva" ? num(a.taux_tva || id.taux_tva || 8.5) : 0;
    const mention = code === "franchise" ? "TVA non applicable — article 293 B du code général des impôts"
      : code === "exonere" ? "Exonération de TVA — article 261-4-4° a du code général des impôts" : `TVA au taux de ${String(taux).replace(".", ",")} %`;
    return { code, taux, mention, auto: !a.tva };
  }
  function montantsAction(a) {
    const r = regimeTva(a), ht = num(a.prix_ht), tva = arrondi((ht * r.taux) / 100);
    return { ht, tva, ttc: arrondi(ht + tva), regime: r };
  }
  P.totalTTC = (a) => montantsAction(a).ttc;

  // ------------------------------------------------------------------ sommes attendues
  // Statuts d'action à partir desquels l'argent est « attendu » (la convention est signée)
  const ENGAGE = ["convention_signee", "en_cours", "terminee", "facturee", "soldee"];
  const recu = (x) => arrondi((x.encaissements || []).reduce((t, e) => t + num(e.montant), 0));
  const reste = (x) => (x.annule ? 0 : arrondi(Math.max(0, num(x.montant) - recu(x))));
  function etatAttendu(x, auj = jourIso()) {
    if (x.annule) return "annule";
    if (reste(x) <= 0.009) return "solde";
    if (x.echeance && x.echeance < auj) return "retard";
    return recu(x) > 0 ? "partiel" : "a_venir";
  }
  const ETATS = { a_venir: "À recevoir", partiel: "Reçu en partie", retard: "En retard", solde: "Réglé", annule: "Annulé" };

  /* Une action produit une ou deux sommes attendues :
   *  - sans prise en charge : tout est dû par le client (ou le centre donneur d'ordre en sous-traitance) ;
   *  - avec prise en charge (OPCO, France Travail…) : la part du financeur + le reste à charge du client.
   * Les encaissements déjà notés sont conservés quand l'action est modifiée. */
  function synchroAttendus(d) {
    for (const a of d.actions) {
      const m = montantsAction(a), engage = ENGAGE.includes(a.statut) || !!a.date_facture;
      const echeance = a.echeance_facture || (a.fin ? D.iso(D.ajoutJours(D.lireDate(a.fin), num(a.delai_paiement_jours || 30))) : "");
      const pec = Math.min(num(a.prise_en_charge_ht), m.ht), k = m.ht ? m.ttc / m.ht : 1;
      const parts = [];
      if (pec > 0) parts.push({ part: "financeur", payeur: a.financeur_nom || P.CANAUX[a.canal_financeur || "opco"].lib, canal: a.canal_financeur || "opco", montant: arrondi(pec * k), ht: pec });
      if (m.ht - pec > 0.009) parts.push({ part: "client", payeur: (a.pour_centre || (a.client && a.client.raison) || a.intitule || "Client").trim(), canal: a.canal || (pec > 0 ? canalReste(a) : canalParDefaut(a)), montant: arrondi((m.ht - pec) * k), ht: arrondi(m.ht - pec) });
      const existants = d.attendus.filter((x) => x.actionId === a.id);
      for (const p of parts) {
        let x = existants.find((e) => e.part === p.part);
        if (!x) { x = { id: uid(), actionId: a.id, part: p.part, encaissements: [], cree: jourIso() }; d.attendus.push(x); }
        Object.assign(x, { libelle: `${a.intitule || "Action"}${parts.length > 1 ? (p.part === "financeur" ? " — part financeur" : " — reste à charge") : ""}`,
          payeur: p.payeur, canal: p.canal, montant: p.montant, ht: p.ht, taux_tva: m.regime.taux, echeance, reference: a.numero_facture || "",
          annule: a.statut === "annulee" || !engage, origine_action: true });
      }
      // une part qui n'existe plus (prise en charge retirée) : annulée si rien n'a été reçu, sinon conservée
      for (const x of existants) if (!parts.find((p) => p.part === x.part)) { if (recu(x)) x.montant = recu(x); else x.annule = true; }
      a.encaisse = existants.length > 0 && existants.every((x) => x.annule || reste(x) <= 0.009) && existants.some((x) => !x.annule);
    }
    // les sommes d'une action supprimée disparaissent si rien n'a été reçu
    d.attendus = d.attendus.filter((x) => !x.actionId || d.actions.some((a) => a.id === x.actionId) || recu(x) > 0);
    return d.attendus;
  }
  // reste à charge après prise en charge : payé par l'entreprise, le centre donneur d'ordre ou le particulier
  const canalReste = (a) => (a.type === "soustraitance" || a.pour_centre ? "of" : a.type === "individuel" ? "particulier" : "entreprise");
  function canalParDefaut(a) {
    if (a.type === "soustraitance" || a.pour_centre) return "of";
    if (a.type === "individuel") return "particulier";
    return ({ opco_appr: "opco", opco_pro: "opco", opco_autres: "opco", cpf: "cpf", pouvoirs_publics: "france_travail", particuliers: "particulier", of: "of" })[a.origine] || "entreprise";
  }

  // ------------------------------------------------------------------ écritures liées aux encaissements
  function ecritureEncaissement(d, x, montant, date, libelle, mvtId) {
    const c = P.CANAUX[x.canal] || P.CANAUX.autre, a = d.actions.find((y) => y.id === x.actionId);
    const origine = a && a.type === "apprentissage" && x.canal === "opco" ? "opco_appr" : c.origine;
    const taux = num(x.taux_tva), ht = arrondi(montant / (1 + taux / 100));
    return { id: uid(), date, libelle, montant: arrondi(montant), montant_ht: ht, tva: arrondi(montant - ht), sens: "recette", origine, actionId: x.actionId || "", attenduId: x.id, mvtId: mvtId || "", statut: "realise" };
  }
  // Paiement reçu sans relevé bancaire (chèque, espèces, ou virement que vous confirmez à la main)
  function encaisserManuel(d, attenduId, { date, montant, mode }) {
    const x = d.attendus.find((y) => y.id === attenduId);
    if (!x) throw new Error("Somme attendue introuvable.");
    const m = arrondi(num(montant) || reste(x));
    if (m <= 0) throw new Error("Montant à préciser.");
    const e = ecritureEncaissement(d, x, m, date || jourIso(), `Reçu ${mode || "virement"} — ${x.payeur} — ${x.libelle}`, "");
    d.ecritures.push(e);
    x.encaissements.push({ id: uid(), date: e.date, montant: m, mode: mode || "virement", ecritureId: e.id });
    synchroAttendus(d);
    return x;
  }
  function annulerEncaissement(d, attenduId, encId) {
    const x = d.attendus.find((y) => y.id === attenduId), enc = x && x.encaissements.find((e) => e.id === encId);
    if (!enc) return;
    x.encaissements = x.encaissements.filter((e) => e !== enc);
    if (enc.mvtId) { const mv = d.mouvements.find((m) => m.id === enc.mvtId); if (mv) { mv.etat = "a_confirmer"; mv.attenduId = ""; mv.propositions = proposer(d, mv); } const ec = d.ecritures.find((e) => e.mvtId === enc.mvtId); if (ec) { ec.attenduId = ""; ec.origine = "autres"; } }
    else d.ecritures = d.ecritures.filter((e) => e.id !== enc.ecritureId);
    synchroAttendus(d);
  }

  // ------------------------------------------------------------------ ressemblance des noms
  const norm = (s) => D.normaliser(String(s || "")).replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
  const VIDES = new Set(["vir", "virement", "sepa", "recu", "de", "du", "des", "la", "le", "les", "et", "sarl", "sas", "sasu", "eurl", "sa", "ste", "societe", "inst", "instantane", "ref", "motif", "prlv", "cb", "carte", "facture", "fact", "fac", "paiement", "reglement", "ordre", "emetteur", "from", "to",
    // mots trop fréquents à La Réunion pour distinguer deux payeurs
    "reunion", "run", "ocean", "indien", "saint", "sainte", "denis", "pierre", "paul", "formation", "formations", "sud", "nord", "est", "ouest", "groupe", "centre"]);
  const mots = (s) => norm(s).split(" ").filter((m) => m.length >= 3 && !VIDES.has(m) && !/^\d+$/.test(m));
  const trigrammes = (s) => { const t = " " + norm(s).replace(/ /g, "") + " ", g = new Set(); for (let i = 0; i < t.length - 2; i++) g.add(t.slice(i, i + 3)); return g; };
  const dice = (a, b) => { const A = trigrammes(a), B = trigrammes(b); if (!A.size || !B.size) return 0; let n = 0; for (const x of A) if (B.has(x)) n++; return (2 * n) / (A.size + B.size); };
  /* Ressemblance entre le libellé bancaire et le nom du payeur (0 à 1) :
   * mots du nom retrouvés dans le libellé, ressemblance des lettres, alias appris, indices du canal (OPCO, Caisse des Dépôts…). */
  function ressemblance(d, libelle, x) {
    const L = norm(libelle), Lm = new Set(mots(libelle)), nom = mots(x.payeur);
    const appris = (d.alias[norm(x.payeur)] || []).some((al) => al && L.includes(al));
    if (appris) return { score: 1, raison: "libellé déjà associé à ce payeur" };
    const communs = nom.filter((m) => Lm.has(m) || [...Lm].some((l) => l.length >= 5 && (l.startsWith(m) || m.startsWith(l))));
    const partMots = nom.length ? communs.length / nom.length : 0;
    const lettres = dice(L, x.payeur);
    const canal = (P.CANAUX[x.canal] || { mots: [] }).mots.some((m) => L.includes(m)) ? 0.5 : 0;
    const score = Math.min(1, Math.max(partMots, lettres * 1.1, canal));
    const raison = communs.length ? `nom retrouvé : ${communs.join(", ")}` : canal ? `indice ${P.CANAUX[x.canal].lib}` : lettres > 0.35 ? `nom ressemblant (${Math.round(lettres * 100)} %)` : "";
    return { score, raison };
  }

  /* Propositions de rapprochement pour un virement reçu, de la plus probable à la moins probable.
   * Poids : montant 55 %, nom 35 %, date 10 % ; + bonus si le n° de facture figure dans le libellé. */
  function proposer(d, mv) {
    if (mv.sens !== "recette") return [];
    const auj = mv.date, out = [], L = norm(mv.libelle);
    for (const x of d.attendus) {
      if (x.annule) continue;
      const r = reste(x), raisons = [];
      // doublon : un paiement noté à la main du même montant, à ±15 jours, pas encore relié à la banque
      const manuel = x.encaissements.find((e) => !e.mvtId && Math.abs(num(e.montant) - mv.montant) < 0.01 && Math.abs(D.lireDate(e.date) - D.lireDate(mv.date)) <= 15 * 86400000);
      if (manuel) { out.push({ attenduId: x.id, score: 0.97, doublon: manuel.id, raisons: [`déjà noté reçu à la main le ${D.fr(D.lireDate(manuel.date))} : ce virement en est la trace bancaire`] }); continue; }
      if (r <= 0.009) continue;
      let sm = 0;
      if (Math.abs(r - mv.montant) < 0.01) { sm = 1; raisons.push("montant identique au reste dû"); }
      else if (Math.abs(num(x.montant) - mv.montant) < 0.01) { sm = 0.95; raisons.push("montant identique à la facture"); }
      else if (Math.abs(r - mv.montant) / r <= 0.02) { sm = 0.75; raisons.push("montant très proche (frais bancaires ?)"); }
      else if (mv.montant < r) { sm = 0.35; raisons.push(`paiement partiel possible (${Math.round((mv.montant / r) * 100)} % du reste)`); }
      const sn = ressemblance(d, mv.libelle, x); if (sn.raison) raisons.push(sn.raison);
      const ref = x.reference && norm(x.reference).length >= 3 && L.includes(norm(x.reference)) ? 0.25 : 0;
      if (ref) raisons.push(`référence ${x.reference} trouvée`);
      const ecart = x.echeance ? Math.abs(D.lireDate(auj) - D.lireDate(x.echeance)) / 86400000 : 60;
      const sd = ecart <= 30 ? 1 : ecart <= 90 ? 0.5 : 0.2;
      const score = Math.min(0.99, 0.55 * sm + 0.35 * sn.score + 0.1 * sd + ref);
      if (score >= 0.35 && (sm > 0 || sn.score >= 0.5 || ref)) out.push({ attenduId: x.id, score: Math.round(score * 100) / 100, raisons });
    }
    return out.sort((a, b) => b.score - a.score).slice(0, 4);
  }

  // ------------------------------------------------------------------ import du relevé bancaire
  function lireCsv(texte) {
    const lignes = texte.replace(/\r/g, "").split("\n").filter((l) => l.trim());
    if (lignes.length < 2) return [];
    const sep = [";", ",", "\t"].sort((a, b) => lignes[0].split(b).length - lignes[0].split(a).length)[0];
    const cellules = (l) => { const out = []; let cur = "", q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === sep && !q) { out.push(cur); cur = ""; } else cur += ch; } out.push(cur); return out.map((x) => x.trim()); };
    // l'en-tête n'est pas toujours la 1re ligne (certaines banques ajoutent le n° de compte au-dessus)
    let iT = lignes.findIndex((l) => /date/i.test(l) && /(montant|debit|débit|credit|crédit|amount)/i.test(l));
    if (iT < 0) iT = 0;
    const tete = cellules(lignes[iT]).map((x) => D.normaliser(x));
    const col = (...cles) => tete.findIndex((h) => cles.some((c) => h.includes(c)));
    const iD = col("date"), iL = col("libelle", "label", "description", "operation", "intitule", "nature"), iM = col("montant", "amount"), iDe = col("debit"), iCr = col("credit");
    const res = [];
    for (const l of lignes.slice(iT + 1)) {
      const c = cellules(l);
      const m = iM >= 0 ? num(c[iM]) : num(c[iCr]) - Math.abs(num(c[iDe]));
      const d = lireDateBanque(c[iD] || "");
      if (!d || !m) continue;
      res.push({ date: d, libelle: (c[iL] || "").slice(0, 200), montant: Math.abs(m), sens: m > 0 ? "recette" : "depense" });
    }
    return res;
  }
  function lireDateBanque(s) {
    const m = /(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})/.exec(s);
    if (m) return `${m[3].length === 2 ? "20" + m[3] : m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`;
    const m2 = /(\d{4})-?(\d{2})-?(\d{2})/.exec(s); return m2 ? `${m2[1]}-${m2[2]}-${m2[3]}` : "";
  }
  // OFX / QFX (export « Money / Quicken » proposé par la plupart des banques françaises)
  function lireOfx(texte) {
    const res = [], blocs = texte.split(/<STMTTRN>/i).slice(1);
    const champ = (b, t) => { const m = new RegExp(`<${t}>([^<\\r\\n]*)`, "i").exec(b); return m ? m[1].trim() : ""; };
    for (const b of blocs) {
      const m = num(champ(b, "TRNAMT")), d = lireDateBanque(champ(b, "DTPOSTED").slice(0, 8));
      const lib = [champ(b, "NAME"), champ(b, "MEMO")].filter(Boolean).join(" ").replace(/&amp;/g, "&");
      if (d && m) res.push({ date: d, libelle: lib.slice(0, 200), montant: Math.abs(m), sens: m > 0 ? "recette" : "depense", fitid: champ(b, "FITID") });
    }
    return res;
  }
  const lireReleve = (texte) => (/<OFX>|<STMTTRN>/i.test(texte) ? lireOfx(texte) : lireCsv(texte));

  const DEPENSES_MOTS = [[/loyer|bail/i, "Location de salle"], [/hotel|salle|seminaire/i, "Location de salle"], [/air austral|air france|corsair|carbu|total|essence|peage|parking|taxi|uber/i, "Déplacements"],
    [/assur|hiscox|axa|maif|macif/i, "Assurance"], [/urssaf|cipav|retraite|prevoyance/i, "Cotisations sociales"], [/dgfip|impot|cfe|tresor/i, "Impôts et taxes"],
    [/frais|commission|cotis.*carte|banque/i, "Banque"], [/orange|sfr|free|bouygues|zeop|canal/i, "Télécom"], [/ovh|baserow|brevo|adobe|microsoft|google|canva|abonnement/i, "Logiciels et abonnements"],
    [/qualitia|certif/i, "Certification Qualiopi"], [/comptab|expert|avocat|honorair/i, "Honoraires (comptable, avocat)"]];

  /* Importe un relevé : chaque ligne nouvelle devient une écriture réalisée (le solde est juste tout de suite) ;
   * chaque virement reçu reçoit des propositions et attend VOTRE confirmation. */
  function importerReleve(d, texte) {
    const lus = lireReleve(texte), cles = new Set(d.mouvements.map((m) => m.cle));
    let nouveaux = 0, recettes = 0, depenses = 0;
    for (const m of lus) {
      const cle = m.fitid || `${m.date}|${m.montant.toFixed(2)}|${norm(m.libelle)}`;
      if (cles.has(cle)) continue;
      cles.add(cle);
      const mv = Object.assign({ id: uid(), cle, importe: jourIso(), etat: m.sens === "recette" ? "a_confirmer" : "depense", attenduId: "" }, m);
      const ec = { id: uid(), date: m.date, libelle: m.libelle || "(sans libellé)", montant: m.montant, sens: m.sens, statut: "realise", mvtId: mv.id, source: "banque" };
      if (m.sens === "recette") { ec.origine = "autres"; recettes++; }
      else { ec.categorie = (DEPENSES_MOTS.find(([r]) => r.test(m.libelle)) || [null, "Autre"])[1]; depenses++; }
      d.mouvements.push(mv); d.ecritures.push(ec); nouveaux++;
    }
    for (const mv of d.mouvements) if (mv.etat === "a_confirmer") mv.propositions = proposer(d, mv);
    return { lus: lus.length, nouveaux, recettes, depenses, doublons: lus.length - nouveaux };
  }
  // Vous confirmez : ce virement paie (tout ou partie de) cette somme attendue
  function confirmer(d, mvtId, attenduId) {
    const mv = d.mouvements.find((m) => m.id === mvtId), x = d.attendus.find((y) => y.id === attenduId);
    if (!mv || !x) throw new Error("Rapprochement introuvable.");
    const prop = (mv.propositions || []).find((p) => p.attenduId === attenduId);
    const ec = d.ecritures.find((e) => e.mvtId === mv.id);
    if (prop && prop.doublon) {
      // le paiement noté à la main est remplacé par sa trace bancaire (pas de double comptage)
      const enc = x.encaissements.find((e) => e.id === prop.doublon);
      d.ecritures = d.ecritures.filter((e) => e.id !== enc.ecritureId);
      Object.assign(enc, { mvtId: mv.id, ecritureId: ec && ec.id, mode: "virement (banque)" });
    } else x.encaissements.push({ id: uid(), date: mv.date, montant: mv.montant, mode: "virement (banque)", mvtId: mv.id, ecritureId: ec && ec.id });
    if (ec) Object.assign(ec, ecritureEncaissement(d, x, mv.montant, mv.date, ec.libelle, mv.id), { id: ec.id, source: "banque" });
    Object.assign(mv, { etat: "rapproche", attenduId: x.id });
    apprendre(d, x.payeur, mv.libelle);
    synchroAttendus(d);
    for (const m of d.mouvements) if (m.etat === "a_confirmer") m.propositions = proposer(d, m);
    return x;
  }
  // Retient les mots du libellé bancaire pour reconnaître ce payeur la prochaine fois
  function apprendre(d, payeur, libelle) {
    const k = norm(payeur), cle = mots(libelle).slice(0, 3).join(" ");
    if (!cle) return;
    const l = (d.alias[k] = d.alias[k] || []);
    if (!l.includes(cle)) l.push(cle);
  }
  // Ce virement n'est pas une facture attendue : autre recette (subvention, remboursement…) ou à ignorer
  function classer(d, mvtId, origine) {
    const mv = d.mouvements.find((m) => m.id === mvtId);
    if (!mv) return;
    mv.etat = origine === "ignorer" ? "ignore" : "autre";
    const ec = d.ecritures.find((e) => e.mvtId === mv.id);
    if (ec) ec.origine = origine === "ignorer" ? "autres" : origine;
  }

  // ------------------------------------------------------------------ tableau de bord
  function soldeBancaire(d) {
    const t = d.tresorerie || {};
    return arrondi(num(t.solde_initial) + d.ecritures.filter((e) => e.statut !== "prevu" && e.date >= (t.date_solde || "0000")).reduce((s, e) => s + (e.sens === "recette" ? 1 : -1) * num(e.montant), 0));
  }
  function tableauBord(d) {
    synchroAttendus(d);
    const auj = jourIso(), id = d.identite || {}, actifs = d.attendus.filter((x) => !x.annule);
    const solde = soldeBancaire(d);
    const du = arrondi(actifs.reduce((t, x) => t + reste(x), 0));
    const retard = actifs.filter((x) => etatAttendu(x, auj) === "retard");
    const dep = d.ecritures.filter((e) => e.statut === "prevu" && e.sens === "depense").reduce((t, e) => t + num(e.montant), 0);
    const recPrev = d.ecritures.filter((e) => e.statut === "prevu" && e.sens === "recette").reduce((t, e) => t + num(e.montant), 0);
    // TVA encaissée sur des factures qui la mentionnent (prestations de services : exigible à l'encaissement ;
    // toute TVA facturée est due, art. 283-3 du CGI), non encore déclarée
    const tva = arrondi(d.ecritures.filter((e) => e.sens === "recette" && e.statut !== "prevu" && num(e.tva) > 0 && !e.tva_declaree).reduce((t, e) => t + num(e.tva), 0));
    const tvaAVenir = arrondi(actifs.reduce((t, x) => t + reste(x) * (num(x.taux_tva) / (100 + num(x.taux_tva))), 0));
    const parCanal = {};
    for (const x of actifs) { const c = (parCanal[x.canal] = parCanal[x.canal] || { attendu: 0, recu: 0, reste: 0, n: 0 }); c.attendu += num(x.montant); c.recu += recu(x); c.reste += reste(x); c.n++; }
    const annee = auj.slice(0, 4), mois = auj.slice(0, 7);
    const enc = d.ecritures.filter((e) => e.sens === "recette" && e.statut !== "prevu");
    return { solde, du, retard: arrondi(retard.reduce((t, x) => t + reste(x), 0)), nbRetard: retard.length, nbDu: actifs.filter((x) => reste(x) > 0).length,
      depensesPrevues: arrondi(dep), recettesPrevues: arrondi(recPrev), tva, tvaAVenir,
      restera: arrondi(solde + du + recPrev - dep - tva - tvaAVenir), parCanal,
      encaisseMois: arrondi(enc.filter((e) => e.date.startsWith(mois)).reduce((t, e) => t + num(e.montant), 0)),
      encaisseAnnee: arrondi(enc.filter((e) => e.date.startsWith(annee)).reduce((t, e) => t + num(e.montant), 0)),
      aConfirmer: d.mouvements.filter((m) => m.etat === "a_confirmer").length };
  }

  // Trésorerie prévisionnelle : solde + sommes attendues à leur échéance + écritures prévues − charges moyennes
  function tresorerie(d, horizon = 90) {
    synchroAttendus(d);
    const auj = jourIso(), solde = soldeBancaire(d);
    const realise = d.ecritures.filter((e) => e.statut !== "prevu");
    const mouvements = [];
    for (const x of d.attendus) { const r = reste(x); if (r > 0) mouvements.push({ date: !x.echeance || x.echeance < auj ? auj : x.echeance, montant: r }); }
    for (const e of d.ecritures.filter((y) => y.statut === "prevu")) mouvements.push({ date: (e.echeance || e.date) < auj ? auj : e.echeance || e.date, montant: (e.sens === "recette" ? 1 : -1) * num(e.montant) });
    const il3m = D.iso(D.ajoutJours(D.lireDate(auj), -90));
    const chargeJour = realise.filter((e) => e.sens === "depense" && e.date >= il3m).reduce((t, e) => t + num(e.montant), 0) / 90;
    mouvements.sort((a, b) => a.date.localeCompare(b.date));
    const courbe = [];
    let s = solde, k = 0;
    for (let j = D.lireDate(auj), n = 0; n <= horizon; j = D.ajoutJours(j, 7), n += 7) {
      const iso = D.iso(j);
      while (k < mouvements.length && mouvements[k].date <= iso) s += mouvements[k++].montant;
      courbe.push({ date: iso, solde: Math.round(s - chargeJour * n) });
    }
    const pointBas = courbe.reduce((m, c) => (c.solde < m.solde ? c : m), courbe[0]);
    const il12m = D.iso(D.ajoutJours(D.lireDate(auj), -365));
    const ca12 = realise.filter((e) => e.sens === "recette" && e.date >= il12m).reduce((t, e) => t + num(e.montant), 0);
    const totalCreances = d.attendus.reduce((t, x) => t + reste(x), 0);
    const dettes = d.ecritures.filter((e) => e.statut === "prevu" && e.sens === "depense").reduce((t, e) => t + num(e.montant), 0);
    const bfr = totalCreances - dettes;
    return { solde, totalCreances, dettes, bfr, bfrJours: ca12 ? Math.round((bfr / ca12) * 365) : null,
      autonomieJours: chargeJour > 0 ? Math.floor(solde / chargeJour) : null, chargeMensuelle: Math.round(chargeJour * 30), courbe, pointBas,
      sousSeuil: courbe.some((c) => c.solde < num(d.tresorerie.seuil_alerte)), ca12 };
  }

  // Besoin de financement d'une mission : frais avancés avant d'être payé
  function besoinMission(a) {
    const frais = num(a.frais_prevus), delai = num(a.delai_paiement_jours || 45);
    const duree = a.debut && a.fin ? Math.max(1, (D.lireDate(a.fin) - D.lireDate(a.debut)) / 86400000) : 1;
    return { avance: frais, joursAttente: Math.round(duree + delai), message: `Vous avancez ${P.euros(frais)} pendant environ ${Math.round(duree + delai)} jours avant d'être payé.` };
  }

  // Bilan pédagogique et financier (préparation) — exercice = année civile ; produits retenus hors TVA
  function bpf(d, annee) {
    const dans = (iso) => iso && iso.slice(0, 4) === String(annee);
    const actions = d.actions.filter((a) => dans(a.fin) || dans(a.debut));
    const C = {};
    for (const k of Object.keys(P.ORIGINES)) C[k] = 0;
    for (const e of d.ecritures) if (e.sens === "recette" && e.statut !== "prevu" && dans(e.date)) C[e.origine || "autres"] = arrondi((C[e.origine || "autres"] || 0) + num(e.montant_ht ?? e.montant));
    const charges = d.ecritures.filter((e) => e.sens === "depense" && e.statut !== "prevu" && dans(e.date)).reduce((t, e) => t + num(e.montant), 0);
    const st = (cat) => actions.flatMap((a) => (a.stagiaires || []).map((s) => ({ s, a }))).filter(({ s }) => (s.statut || "autre") === cat);
    const heuresDe = (x) => x.reduce((t, { s, a }) => t + num(s.heures || a.heures), 0);
    const cats = { salarie: "Salariés d'employeurs privés", apprenti: "Apprentis", demandeur: "Demandeurs d'emploi", particulier: "Particuliers à leurs propres frais", autre: "Autres stagiaires" };
    const F1 = Object.entries(cats).map(([k, lib]) => { const x = st(k); return { lib, nombre: x.length, heures: heuresDe(x) }; });
    const soustraite = actions.filter((a) => a.type === "soustraitance");
    const heuresFormateur = actions.reduce((t, a) => t + num(a.heures), 0);
    return { annee, actions: actions.length, C, totalProduits: Object.values(C).reduce((a, b) => a + b, 0), charges, F1,
      totalStagiaires: F1.reduce((t, x) => t + x.nombre, 0), totalHeures: F1.reduce((t, x) => t + x.heures, 0),
      heuresFormateur, sousTraitanceRecue: soustraite.reduce((t, a) => t + num(a.prix_ht), 0), echeance: `${annee + 1}-05-31` };
  }

  // Indicateurs de résultats (Qualiopi indicateur 2), avec la MÉTHODE DE CALCUL exigée par le V10
  function resultats(d) {
    const fin = d.actions.filter((a) => a.fin && a.fin <= jourIso() && a.statut !== "annulee");
    const stag = fin.reduce((t, a) => t + (a.stagiaires || []).length, 0);
    const avecNote = fin.filter((a) => num(a.satisfaction_chaud) > 0);
    const notes = avecNote.map((a) => num(a.satisfaction_chaud));
    const pres = fin.reduce((t, a) => t + num(a.presentes), 0), adm = fin.reduce((t, a) => t + num(a.admis), 0);
    const ab = fin.reduce((t, a) => t + num(a.abandons), 0);
    const dates = fin.map((a) => a.fin).sort();
    return { actions: fin.length, stagiaires: stag, satisfaction: notes.length ? notes.reduce((a, b) => a + b, 0) / notes.length : null,
      reussite: pres ? adm / pres : null, abandon: stag ? ab / stag : null, presentes: pres, admis: adm, abandons: ab,
      periode: dates.length ? [dates[0], dates[dates.length - 1]] : null, actionsNotees: avecNote.length };
  }

  Object.assign(P, { REGIMES, regimeTva, montantsAction, synchroAttendus, reste, recu, etatAttendu, ETATS, encaisserManuel, annulerEncaissement,
    ressemblance, proposer, lireReleve, importerReleve, confirmer, classer, tableauBord, tresorerie, soldeBancaire, besoinMission, bpf, resultats, num, jourIso });
})(typeof window !== "undefined" ? window : globalThis);

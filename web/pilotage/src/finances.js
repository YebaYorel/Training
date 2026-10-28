/* Finances d'un organisme de formation indépendant : trésorerie, BFR, BPF,
 * import de relevé bancaire et rapprochement des factures, indicateurs de résultats.
 * Le BPF (Cerfa 10443) se déclare sur « Mon Activité Formation » avant le 31 mai :
 * les montants calculés ici sont une PRÉPARATION, à vérifier ligne par ligne. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const D = G.Decorticage;
  const jourIso = () => new Date().toISOString().slice(0, 10);
  const num = (v) => { const n = parseFloat(String(v ?? "").replace(/\s/g, "").replace(/ /g, "").replace(",", ".")); return isFinite(n) ? n : 0; };

  // Écriture : {id, date, libelle, montant (>0), sens: "recette"|"depense", categorie, origine, actionId, statut: "prevu"|"realise", echeance}
  function tresorerie(d, horizon = 90) {
    const auj = jourIso();
    const realise = d.ecritures.filter((e) => e.statut !== "prevu");
    const solde = num(d.tresorerie.solde_initial) + realise.filter((e) => e.date >= d.tresorerie.date_solde)
      .reduce((t, e) => t + (e.sens === "recette" ? 1 : -1) * num(e.montant), 0);
    // créances : factures émises non encaissées ; dettes : dépenses engagées non payées
    const creances = d.actions.filter((a) => a.date_facture && !a.encaisse).map((a) => ({ a, montant: P.totalTTC(a), echeance: a.echeance_facture || a.date_facture }));
    const prevues = d.ecritures.filter((e) => e.statut === "prevu");
    const fin = D.iso(D.ajoutJours(D.lireDate(auj), horizon));
    const mouvements = [];
    for (const c of creances) mouvements.push({ date: c.echeance < auj ? auj : c.echeance, montant: c.montant, libelle: `Encaissement attendu — ${c.a.intitule}`, retard: c.echeance < auj });
    for (const e of prevues) mouvements.push({ date: (e.echeance || e.date) < auj ? auj : e.echeance || e.date, montant: (e.sens === "recette" ? 1 : -1) * num(e.montant), libelle: e.libelle });
    // charges récurrentes mensuelles : moyenne des 3 derniers mois de dépenses réalisées
    const il3m = D.iso(D.ajoutJours(D.lireDate(auj), -90));
    const dep3m = realise.filter((e) => e.sens === "depense" && e.date >= il3m).reduce((t, e) => t + num(e.montant), 0);
    const chargeJour = dep3m / 90;
    mouvements.sort((x, y) => x.date.localeCompare(y.date));
    const courbe = [];
    let s = solde, k = 0;
    for (let j = D.lireDate(auj), n = 0; n <= horizon; j = D.ajoutJours(j, 7), n += 7) {
      const iso = D.iso(j);
      while (k < mouvements.length && mouvements[k].date <= iso) s += mouvements[k++].montant;
      courbe.push({ date: iso, solde: Math.round(s - chargeJour * n) });
    }
    const pointBas = courbe.reduce((m, c) => (c.solde < m.solde ? c : m), courbe[0]);
    const totalCreances = creances.reduce((t, c) => t + c.montant, 0);
    const dettes = prevues.filter((e) => e.sens === "depense").reduce((t, e) => t + num(e.montant), 0);
    // CA des 12 derniers mois (recettes réalisées) → délai moyen de paiement et BFR en jours de CA
    const il12m = D.iso(D.ajoutJours(D.lireDate(auj), -365));
    const ca12 = realise.filter((e) => e.sens === "recette" && e.date >= il12m).reduce((t, e) => t + num(e.montant), 0);
    const bfr = totalCreances - dettes;
    return { solde: Math.round(solde * 100) / 100, creances, totalCreances, dettes, bfr, bfrJours: ca12 ? Math.round((bfr / ca12) * 365) : null,
      autonomieJours: chargeJour > 0 ? Math.floor(solde / chargeJour) : null, chargeMensuelle: Math.round(chargeJour * 30), courbe, pointBas, fin,
      sousSeuil: courbe.some((c) => c.solde < num(d.tresorerie.seuil_alerte)), ca12 };
  }

  P.totalTTC = (a) => num(a.prix_ht) * (a.tva === "tva" ? 1 + num(a.taux_tva || 8.5) / 100 : 1);

  // Besoin de financement d'une mission : frais avancés avant d'être payé
  function besoinMission(a) {
    const frais = num(a.frais_prevus), delai = num(a.delai_paiement_jours || 45);
    const duree = a.debut && a.fin ? Math.max(1, (D.lireDate(a.fin) - D.lireDate(a.debut)) / 86400000) : 1;
    return { avance: frais, joursAttente: Math.round(duree + delai), message: `Vous avancez ${P.euros(frais)} pendant environ ${Math.round(duree + delai)} jours avant d'être payé.` };
  }

  // Bilan pédagogique et financier (préparation) — exercice = année civile
  function bpf(d, annee) {
    const dans = (iso) => iso && iso.slice(0, 4) === String(annee);
    const actions = d.actions.filter((a) => dans(a.fin) || dans(a.debut));
    const C = {};
    for (const k of Object.keys(P.ORIGINES)) C[k] = 0;
    for (const e of d.ecritures) if (e.sens === "recette" && e.statut !== "prevu" && dans(e.date)) C[e.origine || "autres"] = (C[e.origine || "autres"] || 0) + num(e.montant);
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

  // Indicateurs de résultats (Qualiopi indicateur 2), calculés sur les actions terminées
  function resultats(d) {
    const fin = d.actions.filter((a) => a.fin && a.fin <= jourIso());
    const stag = fin.reduce((t, a) => t + (a.stagiaires || []).length, 0);
    const notes = fin.map((a) => num(a.satisfaction_chaud)).filter((x) => x > 0);
    const pres = fin.reduce((t, a) => t + num(a.presentes), 0), adm = fin.reduce((t, a) => t + num(a.admis), 0);
    const ab = fin.reduce((t, a) => t + num(a.abandons), 0);
    return { actions: fin.length, stagiaires: stag, satisfaction: notes.length ? (notes.reduce((a, b) => a + b, 0) / notes.length) : null,
      reussite: pres ? adm / pres : null, abandon: stag ? ab / stag : null };
  }

  // Import d'un relevé bancaire CSV (export de votre banque) → écritures, avec rapprochement des factures
  function lireReleve(texte) {
    const lignes = texte.replace(/\r/g, "").split("\n").filter((l) => l.trim());
    if (lignes.length < 2) return [];
    const sep = [";", ",", "\t"].sort((a, b) => lignes[0].split(b).length - lignes[0].split(a).length)[0];
    const cellules = (l) => { const out = []; let cur = "", q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === sep && !q) { out.push(cur); cur = ""; } else cur += ch; } out.push(cur); return out.map((x) => x.trim()); };
    const tete = cellules(lignes[0]).map((x) => D.normaliser(x));
    const col = (...cles) => tete.findIndex((h) => cles.some((c) => h.includes(c)));
    const iD = col("date"), iL = col("libelle", "label", "description", "operation", "intitule"), iM = col("montant", "amount"), iDe = col("debit"), iCr = col("credit");
    const date = (s) => { const m = /(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})/.exec(s) || null; if (m) return `${m[3].length === 2 ? "20" + m[3] : m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`;
      const m2 = /(\d{4})-(\d{2})-(\d{2})/.exec(s); return m2 ? m2[0] : ""; };
    const res = [];
    for (const l of lignes.slice(1)) {
      const c = cellules(l);
      let m = iM >= 0 ? num(c[iM]) : num(c[iCr]) - Math.abs(num(c[iDe]));
      const d = date(c[iD] || "");
      if (!d || !m) continue;
      res.push({ date: d, libelle: (c[iL] || "").slice(0, 200), montant: Math.abs(m), sens: m > 0 ? "recette" : "depense" });
    }
    return res;
  }
  function rapprocher(donnees, mouvement) {
    if (mouvement.sens !== "recette") return null;
    const candidates = donnees.actions.filter((a) => a.date_facture && !a.encaisse && Math.abs(P.totalTTC(a) - mouvement.montant) < 0.01);
    return candidates.length === 1 ? candidates[0] : null;
  }

  Object.assign(P, { tresorerie, besoinMission, bpf, resultats, lireReleve, rapprocher, num, jourIso });
})(typeof window !== "undefined" ? window : globalThis);

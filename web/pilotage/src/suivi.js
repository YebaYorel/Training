/* Suivi réel d'une formation : le planning initial est une HYPOTHÈSE ; à chaque
 * séance terminée, on note ce qui a été vraiment fait, et la suite se recale
 * automatiquement sur les prochains jours de formation (retards absorbés). */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const D = G.Decorticage;

  // Clé stable d'un objectif : n° de séance + texte (survit à une régénération à paramètres égaux)
  const cle = (s, o) => `${s.numero}|${o.texte}`;

  function analyse(formation) {
    if (formation._analyse) return formation._analyse;
    const t = formation.textes;
    const reac = D.analyserReac(D.nettoyer(t.reac), t.reac);
    const a = { reac, re: t.re ? D.analyserRe(D.nettoyer(t.re), reac) : null, fiche: t.fiche ? D.analyserFiche(D.nettoyer(t.fiche)) : null,
      inconnus: [], noms: formation.noms || {}, erreurs: [] };
    // cache non énumérable : jamais écrit dans le coffre (il se recalcule à l'ouverture)
    Object.defineProperty(formation, "_analyse", { value: a, configurable: true, writable: true, enumerable: false });
    return a;
  }

  function contexte(formation, charte, logo) {
    return D.construireContexte(analyse(formation), Object.assign({}, formation.reglages), charte, logo);
  }

  /* Planning réel : séances déjà faites (journal) + reste replanifié à partir du
   * prochain jour de formation qui suit la dernière séance notée. */
  function planReel(formation, ctx) {
    const plan = ctx.plan;
    const fait = new Map();                      // clé -> minutes faites
    for (const j of formation.journal || []) for (const [k, m] of Object.entries(j.faits || {})) fait.set(k, (fait.get(k) || 0) + m);
    const restant = [];
    for (const s of plan.seances) for (const o of s.objectifs) {
      if (!o.minutes) continue;
      const deja = fait.get(cle(s, o)) || 0;
      if (deja < o.minutes) restant.push([s, o, o.minutes - deja, deja > 0]);
    }
    const derniere = (formation.journal || []).map((j) => j.date).sort().pop();
    const p = D.parametresDepuis(formation.reglages, []);
    if (derniere) p.date_debut = D.ajoutJours(D.lireDate(derniere), 1);
    const futur = D.placer(restant, p).lignes;
    const minutesFaites = [...fait.values()].reduce((a, b) => a + b, 0);
    const total = plan.seances.reduce((t, s) => t + s.objectifs.reduce((u, o) => u + o.minutes, 0), 0);
    // écart = fin réelle prévue vs fin initiale
    const finInit = plan.date_fin, finReelle = futur.length ? futur[futur.length - 1].date : (derniere ? D.lireDate(derniere) : finInit);
    const ecartJours = finInit && finReelle ? Math.round((finReelle - finInit) / 86400000) : 0;
    return { futur, minutesFaites, total, finInit, finReelle, ecartJours, derniere };
  }

  // Lignes de la prochaine journée de formation (ou d'une date donnée)
  function journee(futur, dateIso) {
    if (!futur.length) return null;
    const cible = dateIso || D.iso(futur[0].date);
    const lignes = futur.filter((l) => D.iso(l.date) === cible);
    if (!lignes.length) return null;
    const seances = [], vues = new Set();
    for (const l of lignes) if (!vues.has(l.seance)) { vues.add(l.seance); seances.push(l.seance); }
    return { date: cible, lignes, seances, minutes: lignes.reduce((t, l) => t + l.minutes, 0) };
  }

  /* Noter une journée réalisée. `etats` : clé -> "fait" | "partiel" | "non".
   * « partiel » compte la moitié du temps prévu ce jour-là ; « non » ne compte rien. */
  function noterJournee(formation, jour, etats, notes) {
    const faits = {};
    for (const l of jour.lignes) {
      const k = cle(l.seance, l.objectif), e = etats[k] || "fait";
      const m = e === "fait" ? l.minutes : e === "partiel" ? Math.floor(l.minutes / 2 / 15) * 15 : 0;
      if (m) faits[k] = (faits[k] || 0) + m;
    }
    formation.journal = (formation.journal || []).filter((j) => j.date !== jour.date);
    formation.journal.push({ date: jour.date, faits, notes: notes || "", prevu: jour.minutes, note_le: new Date().toISOString() });
    formation.journal.sort((a, b) => a.date.localeCompare(b.date));
  }

  Object.assign(P, { cleObjectif: cle, analyseFormation: analyse, contexteFormation: contexte, planReel, journee, noterJournee });
})(typeof window !== "undefined" ? window : globalThis);

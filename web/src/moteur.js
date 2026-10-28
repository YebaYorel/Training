/* Chef d'orchestre : fichiers déposés → analyse → plan → contexte d'export. */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const NOM_YEBA = "YEBA FORMATIONS";
  const SOURCES = [
    "Taxonomie de Bloom révisée : Anderson L. W. & Krathwohl D. R. (2001), A Taxonomy for Learning, Teaching, and Assessing.",
    "Étayage : Wood D., Bruner J. S. & Ross G. (1976), « The role of tutoring in problem solving », Journal of Child Psychology and Psychiatry, 17.",
    "Modes de représentation et curriculum en spirale : Bruner J. S. (1966), Toward a Theory of Instruction.",
    "Jours fériés : Code du travail, art. L3133-1 ; 20 décembre à La Réunion : décret n° 83-1003 du 23/11/1983.",
    "Qualiopi : Référentiel national qualité (décret n° 2019-564) — indicateurs 1, 2, 5, 6, 7.",
  ];

  async function analyserFichiers(fichiers) {
    const res = { reac: null, re: null, fiche: null, inconnus: [], noms: {}, erreurs: [] };
    const lus = [];
    for (const f of fichiers) {
      try { const r = await D.lireFichier(f); lus.push([f.name, r, D.detecterType(r.texte)]); }
      catch (e) { res.erreurs.push(e.message || String(e)); }
    }
    for (const [nom, r, type] of lus) if (type === "REAC") { res.reac = D.analyserReac(r.texte, r.brut); res.noms.reac = nom; }
    for (const [nom, r, type] of lus) {
      if (type === "RE") { res.re = D.analyserRe(r.texte, res.reac); res.noms.re = nom; }
      else if (type === "FICHE") { res.fiche = D.analyserFiche(r.texte); res.noms.fiche = nom; }
      else if (type === "INCONNU") res.inconnus.push(nom);
    }
    return res;
  }

  function construireContexte(analyse, r, charte, logo) {
    const reac = analyse.reac;
    if (!reac || !reac.competences.length) throw new Error("Aucun REAC exploitable : le REAC est indispensable (activités types et compétences).");
    const hypotheses = [];
    const p = D.parametresDepuis(r, hypotheses);
    const plan = D.construirePlan(reac, analyse.re, p);
    const alertes = [...reac.avertissements];
    if (analyse.re) alertes.push(...analyse.re.avertissements); else alertes.push("Pas de RE/RC fourni : l'examen simplifié est construit depuis la fiche France Compétences.");
    if (analyse.fiche) alertes.push(...analyse.fiche.avertissements); else alertes.push("Pas de fiche France Compétences : le programme est incomplet (code, certificateur…).");
    if (!r.heures_entreprise && analyse.re) {
      const m = /(\d+)\s*heures pour le titre/.exec(analyse.re.periode_entreprise.join(" "));
      if (m) { r.heures_entreprise = +m[1]; hypotheses.push(`Période en entreprise : minimum réglementaire de ${m[1]} h repris du RE.`); }
    }
    if (!charte.couleurs_validees) alertes.push("Couleurs de charte provisoires : saisissez les codes exacts de votre charte (bouton « Charte »).");
    const commanditaire = (r.commanditaire || "").trim();
    const estYeba = !commanditaire || commanditaire.toUpperCase() === NOM_YEBA;
    const nomOrg = r.afficher_nom ? (estYeba ? charte.nom_organisme : commanditaire) : "";
    const fiche = analyse.fiche;
    const sources = Object.values(analyse.noms).map((n) => `Document source : ${n}`).concat(SOURCES);
    if (fiche && fiche.code) sources.unshift(`Fiche France Compétences : https://www.francecompetences.fr/recherche/${fiche.type_fiche.toLowerCase()}/${fiche.code.replace(/\D/g, "")}/`);
    const sigle = (reac.sigle || (fiche && fiche.code) || "titre").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    return { reac, re: analyse.re, fiche, plan, r, charte, nomOrg, estYeba, logo: estYeba && r.afficher_logo ? logo : null,
      tarif: r.tarif_affichage && Object.keys(r.tarif_affichage).length ? { affichage: r.tarif_affichage } : null,
      hypotheses, alertes, sources, sigle, titre: (fiche && fiche.intitule) || `TP ${reac.intitule}` };
  }

  Object.assign(D, { analyserFichiers, construireContexte, NOM_YEBA });
})(typeof window !== "undefined" ? window : globalThis);

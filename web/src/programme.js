/* Programme de formation et Examen simplifié — portage de programme.py
 * (mêmes contenus pour Excel, Word et la page web). */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const AC = "À compléter";
  const Sec = (titre) => ({ titre, paragraphes: [], puces: [], tableau: [] });

  function construireProgramme(reac, re, fiche, plan, r, tarif) {
    const f = fiche || { code: "", intitule: "", niveau: "", certificateur: "", nsf: [], formacodes: [], rome: [], date_echeance: "", objectifs: "",
      prerequis_entree: "", voies_acces: [], blocs: [], emplois: [], correspondances: [], statistiques: [], modalites_evaluation: "" };
    const intitule = (f.intitule || (reac.intitule ? `TP - ${reac.intitule}` : "")).trim() || AC;
    const S = [];
    let s = Sec("Identification de la certification");
    s.tableau = [["Élément", "Information"], ["Intitulé", intitule], ["Code France Compétences", f.code || AC],
      ["Niveau", f.niveau || (reac.niveau ? `Niveau ${reac.niveau}` : AC)], ["Certificateur", f.certificateur || AC],
      ["Code(s) NSF", f.nsf.join(" ; ") || AC], ["Formacode(s)", f.formacodes.join(" ; ") || AC], ["Code(s) ROME", f.rome.join(" ; ") || AC],
      ["Enregistrement valable jusqu'au", f.date_echeance || AC]];
    S.push(s);
    s = Sec("Objectifs de la formation");
    if (f.objectifs) s.paragraphes.push(f.objectifs);
    s.puces = reac.activites.map((a) => `AT${a.numero} — ${a.intitule}`);
    S.push(s);
    s = Sec("Public et prérequis");
    s.puces = [`Public : ${r.public || AC}`, `Prérequis : ${r.prerequis || f.prerequis_entree || "Aucun prérequis réglementaire indiqué sur la fiche — à définir par l’organisme (test de positionnement recommandé)"}`];
    const voies = f.voies_acces.filter(([, ok]) => ok).map(([v]) => v);
    if (voies.length) s.puces.push("Voies d'accès : " + voies.join(" ; "));
    S.push(s);
    s = Sec("Durée, rythme et lieu");
    const hc = plan ? plan.lignes.reduce((t, l) => t + l.minutes, 0) : 0;
    s.puces = [hc ? `Durée en centre : ${D.fmtDuree(hc)}` : `Durée en centre : ${AC}`,
      r.heures_entreprise ? `Période en entreprise : ${D.fmtDuree(r.heures_entreprise * 60)}` : "Période en entreprise obligatoire (voir « Validation »)",
      plan && plan.lignes.length ? `Dates : du ${D.fr(plan.lignes[0].date)} au ${D.fr(plan.date_fin)}` : `Dates : ${AC}`,
      `Horaires : ${r.creneaux}`, `Lieu : ${r.lieu || AC}`, `Délai d'accès : ${r.delai_acces || AC}`];
    S.push(s);
    s = Sec("Contenu de la formation (par compétence)");
    s.tableau = [["Bloc / Activité type", "Compétence", "Contenus clés", "Durée"]];
    for (const at of reac.activites)
      for (const n of at.competences) {
        const cp = reac.competence(n);
        const titres = [...new Set(plan.seances.filter((x) => x.cp === n && x.type_seance !== "evaluation").map((x) => x.titre.replace(/ \(partie \d+\/\d+\)$/, "")))];
        const courts = titres.map((t) => (t.length <= 70 ? t : t.slice(0, 70).replace(/\s+\S*$/, "") + "…"));
        const m = plan.minutes_cp[n] || 0;
        s.tableau.push([`AT${at.numero} — ${at.intitule}`, `CP${cp.numero} — ${cp.intitule}`, courts.map((t) => "• " + t).join("\n") || D.simplifier(cp.intitule), m ? D.fmtDuree(m) : ""]);
      }
    for (const [k, lib] of [["accueil", "Accueil et positionnement"], ["ecf", "Évaluations en cours de formation (ECF)"], ["dossier", "Dossier professionnel"],
      ["productions", "Productions d'examen"], ["examen", "Examen blanc"], ["bilan", "Bilan"]])
      if (plan.minutes_modules[k]) s.tableau.push(["Modules transverses", lib, "", D.fmtDuree(plan.minutes_modules[k])]);
    S.push(s);
    s = Sec("Modalités pédagogiques et moyens");
    s.puces = [r.modalites_pedagogiques, "Objectifs formulés selon la taxonomie de Bloom ; progression en spirale (démarche brunérienne)",
      "Supports projetés à fort contraste, police agrandie (accessibilité)"];
    S.push(s);
    s = Sec("Modalités d'évaluation et de certification");
    if (re && re.epreuves.length) {
      s.tableau = [["Épreuve", "Durée", "Compétences évaluées"]].concat(re.epreuves.map((e) => [e.modalite, e.duree, e.competences.map((n) => "CP" + n).join(", ") || "Toutes (échange sur le DP)"]));
      if (re.duree_totale) s.paragraphes.push(`Durée totale de l'épreuve pour le candidat : ${re.duree_totale}`);
    } else if (f.modalites_evaluation) s.paragraphes.push(f.modalites_evaluation);
    s.puces = ["Évaluations en cours de formation (ECF) à la fin de chaque activité type", "Validation totale (titre) ou partielle par blocs de compétences (CCP)"];
    S.push(s);
    if (f.blocs.length) { s = Sec("Blocs de compétences (validation partielle possible)"); s.tableau = [["Code", "Bloc", "Compétences"]].concat(f.blocs.map((b) => [b.code, b.intitule, b.competences.join(" • ")])); S.push(s); }
    s = Sec("Accessibilité aux personnes en situation de handicap");
    s.paragraphes.push(`Formation accessible : aménagements possibles du parcours et des épreuves (guide d'aménagement des sessions d'examen du ministère du Travail). Référent handicap : ${r.referent_handicap || AC}.`);
    S.push(s);
    s = Sec("Débouchés et suite de parcours");
    s.puces = f.emplois.slice(0, 15).length ? f.emplois.slice(0, 15) : [AC];
    if (f.correspondances.length) s.paragraphes.push("Équivalences partielles : " + f.correspondances.join(" | "));
    S.push(s);
    if (f.statistiques.length) {
      s = Sec("Indicateurs de résultats (France Compétences)");
      s.tableau = [["Année", "Certifiés", "Dont VAE", "Insertion globale 6 mois (%)", "Dans le métier 6 mois (%)", "Dans le métier 2 ans (%)"]]
        .concat(f.statistiques.map((x) => [x.annee, x.certifies, x.vae, x.insertion_6_mois, x.metier_6_mois, x.metier_2_ans]));
      s.paragraphes.push(`Source : fiche ${f.code} — francecompetences.fr (statistiques nationales).`);
      S.push(s);
    }
    s = Sec("Tarif");
    s.puces = tarif && tarif.affichage && Object.keys(tarif.affichage).length ? Object.entries(tarif.affichage).map(([k, v]) => `${k} : ${v}`)
      : ["Sur devis — nous consulter (prise en charge OPCO, CPF, France Travail selon éligibilité)"];
    S.push(s);
    return [intitule, S];
  }

  // ---- Critères « en clair » (participe → verbe d'action), original gardé sinon
  const IRR = { transmis: "transmettre", transmise: "transmettre", transmises: "transmettre", mis: "mettre", mise: "mettre", mises: "mettre",
    fait: "faire", faite: "faire", faites: "faire", pris: "prendre", prise: "prendre", prises: "prendre", suivi: "suivre", suivie: "suivre",
    suivis: "suivre", suivies: "suivre", prévu: "prévoir", prévue: "prévoir", prévus: "prévoir", prévues: "prévoir", tenu: "tenir", tenue: "tenir",
    tenus: "tenir", maintenu: "maintenir", obtenu: "obtenir", rendu: "rendre", rendus: "rendre", conduit: "conduire", conduite: "conduire",
    fournies: "fournir", fourni: "fournir", fournis: "fournir", remplis: "remplir", rempli: "remplir", répartie: "répartir", réparti: "répartir",
    réparties: "répartir", établi: "établir", établis: "établir", définis: "définir", défini: "définir", définie: "définir" };
  const ADJ = new Set(["efficace", "pertinente", "pertinent", "pertinents", "pertinentes", "cohérentes", "cohérente", "cohérent", "réalistes", "réaliste",
    "claire", "clair", "claires", "fiables", "fiable", "individualisés", "adaptée", "adaptées", "adaptés", "adapté", "conforme", "conformes", "structurée"]);
  const LOC = ["en compte", "en œuvre", "en place", "en avant", "en évidence"];
  function infinitif(mot) {
    let m = mot.toLowerCase().replace(/[;.]+$/, "");
    const virgule = m.endsWith(","); m = m.replace(/,+$/, "");
    let res = null;
    if (IRR[m]) res = IRR[m];
    else if (ADJ.has(m) && !m.startsWith("adapt")) return null;
    else for (const [fin, r] of [["ées", "er"], ["és", "er"], ["ée", "er"], ["é", "er"]]) if (m.endsWith(fin) && m.length > fin.length + 2) { res = m.slice(0, -fin.length) + r; break; }
    return res && virgule ? res + "," : res;
  }
  function criteresEnClair(critere) {
    const c = critere.trim().replace(/\.$/, "");
    const m = /^(Les|Le|La|L’|Une|Un|Des)\s*(.+?)\s+(?:sont|est)\s+(.+)$/.exec(c);
    if (!m || /(?<!\p{L})(font|fait|permet|répond|tient|respecte|correspond|prennent|valorisent)(?!\p{L})/u.test(m[2])) return c;
    const article = { Les: "les", Le: "le", La: "la", "L’": "l’", Un: "un", Une: "une", Des: "des" }[m[1]];
    const sujet = m[2].trim();
    let attribut = m[3], second = "";
    const m2 = /^(.*?)\s+et\s+((?:les|le|la|l’|des)\s*.+?\s+(?:sont|est)\s+.+)$/.exec(attribut);
    if (m2) {
      const phr = m2[2][0].toUpperCase() + m2[2].slice(1), conv = criteresEnClair(phr);
      attribut = m2[1];
      if (conv !== phr) second = " et " + conv[0].toLowerCase() + conv.slice(1); else attribut = m2[1] + " et " + m2[2];
    }
    const mots = attribut.split(/\s+/);
    const verbes = [];
    let i = 0;
    while (i < mots.length) {
      let inf = infinitif(mots[i]);
      if (!inf) break;
      i++;
      const suite = mots.slice(i, i + 2).join(" ");
      if (LOC.includes(suite)) { inf += " " + suite; i += 2; }
      verbes.push(inf);
      if (i < mots.length && mots[i] === "et" && i + 1 < mots.length && infinitif(mots[i + 1])) i++;
      else if (!mots[i - 1].endsWith(",")) break;
    }
    if (!verbes.length) return c;
    const v = verbes.map((x) => x.replace(/,$/, ""));
    const tete = v.length === 1 ? v[0] : v.slice(0, -1).join(", ") + " et " + v[v.length - 1];
    let reste = mots.slice(i).join(" ");
    for (const [fin, rempl] of [["et fiables", "de manière fiable"], ["et fiable", "de manière fiable"]]) if (reste.endsWith(fin)) reste = reste.slice(0, -fin.length).trim() + " " + rempl;
    const liaison = article.endsWith("’") ? "" : " ";
    return (`${tete[0].toUpperCase() + tete.slice(1)} ${article}${liaison}${sujet} ${reste}`.trim() + second).replace(/ {2}/g, " ");
  }

  function resumeEpreuve(modalite, detail) {
    const n = D.normaliser(modalite), d = D.normaliser(detail);
    if (n.startsWith("mise en situation")) return d.includes("etude de cas") ? "Étude de cas écrite sur ordinateur (traitement de texte + tableur), à partir d'un dossier papier et de modèles numériques. Travaux imprimés et corrigés par le jury." : "Mise en situation professionnelle devant le jury.";
    if (n.startsWith("entretien technique")) return "Préparation sans jury, puis présentation des travaux et échange avec le jury (cas pratiques possibles).";
    if (n.startsWith("questionnement")) return "Présentation des documents et diaporamas préparés AVANT l'examen, puis questions du jury (simulations possibles).";
    if (n.startsWith("entretien final")) return "Échange avec le jury, y compris sur le dossier professionnel.";
    if (n.startsWith("questionnaire")) return "Questionnaire écrit.";
    return "";
  }

  function construireExamen(reac, re, fiche) {
    const p1 = [["Épreuve", "Durée", "Compétences évaluées", "Comment ça se passe (en bref)"]];
    if (re && re.epreuves.length)
      for (const e of re.epreuves)
        p1.push([e.modalite, e.duree, e.competences.filter((n) => reac.competence(n)).map((n) => `CP${n} — ${D.simplifier(reac.competence(n).intitule)}`).join("\n") || "Échange avec le jury (dossier professionnel)", resumeEpreuve(e.modalite, e.detail)]);
    else if (fiche && fiche.blocs.length) for (const b of fiche.blocs) p1.push([`Bloc ${b.code}`, b.evaluation, b.competences.join("\n"), ""]);
    const prod = {};
    for (const p of re ? re.productions : []) prod[D.normaliser(p.competence).slice(0, 30)] = p;
    const p2 = reac.competences.map((cp) => {
      const cle = D.normaliser(cp.intitule).slice(0, 30);
      const p = prod[cle] || Object.entries(prod).find(([k]) => k.slice(0, 18) === cle.slice(0, 18))?.[1];
      return { cp: `CP${cp.numero} — ${cp.intitule}`, at: cp.at_numero, epreuves: re ? re.epreuves.filter((e) => e.competences.includes(cp.numero)).map((e) => e.modalite) : [],
        attendus: cp.criteres.map(criteresEnClair), production: p ? { pages: p.pages, themes: p.themes.map((t) => t[0]) } : null };
    });
    return { partie1: p1, partie2: p2, consignes: re ? re.documents.concat(re.diaporamas, re.periode_entreprise.slice(0, 1)) : [], duree_totale: re ? re.duree_totale : "" };
  }

  Object.assign(D, { construireProgramme, construireExamen, criteresEnClair });
})(typeof window !== "undefined" ? window : globalThis);

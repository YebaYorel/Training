/* Analyse des référentiels (REAC, RE/RC, fiche France Compétences) — portage
 * fidèle de decorticage/referentiels.py. Les Activités types et Compétences
 * sont reprises MOT POUR MOT. */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});

  function normaliser(s) {
    return (s || "").replace(/’/g, "'").normalize("NFKD").replace(/[̀-ͯ]/g, "")
      .replace(/[^\x00-\x7f]/g, "").toLowerCase().replace(/\s+/g, " ").trim();
  }
  // \b de JS ne connaît pas les lettres accentuées : on utilise \p{L} (drapeau u)
  const LIAISONS_FIN = /(?:[,;:(\-]|(?<!\p{L})(?:de|du|des|et|la|le|les|à|au|aux|en|un|une|par|pour|sur|avec|ou|dans|son|sa|ses|leur|leurs)|(?<!\p{L})[dl][’'])$/iu;
  const estMinuscule = (c) => c && c !== c.toUpperCase() && c === c.toLowerCase();
  const parOuv = (s) => (s.match(/\(/g) || []).length > (s.match(/\)/g) || []).length;

  function joindreItems(lignes) {
    const items = [];
    for (const brute of lignes) {
      let l = brute.trim();
      if (!l) continue;
      l = l.replace(/^-\s+/, "");
      const suite = items.length && (estMinuscule(l[0]) || "(…).".includes(l[0]) ||
        LIAISONS_FIN.test(items[items.length - 1]) || parOuv(items[items.length - 1]));
      if (suite) items[items.length - 1] += " " + l; else items.push(l);
    }
    return items.map((i) => i.replace(/\s+/g, " ").trim().replace(/\.$/, "").trim());
  }

  function decouperPhrases(lignes) {
    const blocs = [];
    for (const brute of lignes) {
      const l = brute.trim();
      if (!l) continue;
      const der = blocs[blocs.length - 1];
      if (blocs.length && (estMinuscule(l[0]) || LIAISONS_FIN.test(der) || parOuv(der))) blocs[blocs.length - 1] += " " + l;
      else blocs.push(l);
    }
    const phrases = [];
    for (const b of blocs)
      for (let p of b.split(/(?<=[.!?])\s+(?=[A-ZÀÂÉÈÊÎÔÛÇ])/)) {
        p = p.trim().replace(/\.$/, "").trim();
        if (p.length > 3) phrases.push(p);
      }
    return phrases;
  }

  // Texte entre `debut` et la première des `fins` (regex multilignes)
  function section(texte, debut, fins) {
    const m = new RegExp(debut, "im").exec(texte);
    if (!m) return "";
    const reste = texte.slice(m.index + m[0].length);
    let fin = reste.length;
    for (const f of fins) {
      const mm = new RegExp(f, "im").exec(reste);
      if (mm && mm.index < fin) fin = mm.index;
    }
    return reste.slice(0, fin);
  }

  function titreMultiligne(lignes, arret) {
    const re = new RegExp(arret, "i");
    const t = [];
    let i = 0;
    while (i < lignes.length && !re.test(lignes[i])) { if (lignes[i].trim()) t.push(lignes[i].trim()); i++; }
    return [t.join(" ").replace(/\s+/g, " ").trim(), lignes.slice(i)];
  }

  const SOUS = [
    ["sf_techniques", "^\\s*1\\s*[-–]\\s*Savoir-faire techniques"],
    ["sf_organisationnels", "^\\s*2\\s*[-–]\\s*Savoir-faire organisationnels"],
    ["sf_relationnels", "^\\s*3\\s*[-–]\\s*Savoir-faire relationnels"],
    ["savoirs", "^\\s*4\\s*[-–]\\s*Savoirs"],
  ];

  function parserCompetence(numero, bloc) {
    const [intitule, reste] = titreMultiligne(bloc.split("\n"), "^Description de la comp");
    const texte = reste.join("\n");
    const cp = { numero, intitule, at_numero: 0, description: [], contexte: "", criteres: [],
      sf_techniques: [], sf_organisationnels: [], sf_relationnels: [], savoirs: [] };
    cp.description = decouperPhrases(section(texte, "^Description de la comp.*$", ["^Contexte\\(s\\) professionnel"]).split("\n"));
    cp.contexte = section(texte, "^Contexte\\(s\\) professionnel.*$", ["^Crit[èe]res de performance"]).replace(/\s+/g, " ").trim();
    cp.criteres = joindreItems(section(texte, "^Crit[èe]res de performance\\s*$", ["^Savoir-faire techniques, savoir", "^\\s*1\\s*[-–]"]).split("\n"));
    SOUS.forEach(([attr, motif], i) => {
      const fins = SOUS.slice(i + 1).map((x) => x[1]).concat(["^FICHE ", "$(?![\\s\\S])"]);
      cp[attr] = joindreItems(section(texte, motif + ".*$", fins).split("\n"));
    });
    return cp;
  }
  const volume = (cp) => cp.sf_techniques.length + cp.sf_organisationnels.length + cp.sf_relationnels.length + cp.savoirs.length + cp.criteres.length;

  function analyserReac(texte, brut) {
    const reac = { intitule: "", sigle: "", niveau: "", code_titre: "", millesime: "", date_validation: "",
      activites: [], competences: [], transversales: [], avertissements: [] };
    const src = brut || texte;
    let m = /\b([A-Z]{2,6})\s+(?:REAC|RE|RC)\s+(TP-\d{5})\s+(\d{1,2})\s+(\d{2}\/\d{2}\/\d{4})/.exec(src);
    if (m) [, reac.sigle, reac.code_titre, reac.millesime, reac.date_validation] = m;
    m = /DU TITRE PROFESSIONNEL\s*\n\s*(.+?)\s*\n/.exec(src);
    if (m) reac.intitule = m[1].trim();
    m = /\bNiveau\s+(\d)\b/.exec(src);
    if (m) reac.niveau = m[1];

    const reAT = /^FICHE ACTIVIT[ÉE] TYPE N°\s*(\d+)\s*$/gm, reCP = /^FICHE COMP[ÉE]TENCE PROFESSIONNELLE N°\s*(\d+)\s*$/gm;
    const pAT = [...texte.matchAll(reAT)], pCP = [...texte.matchAll(reCP)];
    const premiereCP = pCP[0];
    pAT.forEach((m, k) => {
      const fin = k + 1 < pAT.length ? pAT[k + 1].index : (premiereCP ? premiereCP.index : texte.length);
      const bloc = texte.slice(m.index + m[0].length, fin);
      const [intitule] = titreMultiligne(bloc.split("\n"), "^D[ée]finition");
      reac.activites.push({ numero: +m[1], intitule, competences: [],
        description: section(bloc, "^D[ée]finition.*$", ["^R[ée]glementation", "^Liste des comp"]).replace(/\s+/g, " ").trim(),
        _liste: joindreItems(section(bloc, "^Liste des comp[ée]tences professionnelles.*$", ["^Comp[ée]tences transversales"]).split("\n")) });
    });
    let finGlobale = texte.length;
    if (pCP.length) {
      const re = /^(FICHE DES COMP[ÉE]TENCES TRANSVERSALES|FICHE COMP[ÉE]TENCES TRANSVERSALES|Glossaire)/gim;
      re.lastIndex = pCP[pCP.length - 1].index + 10;
      const f = re.exec(texte);
      if (f) finGlobale = f.index;
    }
    pCP.forEach((m, k) => {
      const fin = k + 1 < pCP.length ? pCP[k + 1].index : finGlobale;
      reac.competences.push(parserCompetence(+m[1], texte.slice(m.index + m[0].length, fin)));
    });
    for (const at of reac.activites) {
      for (const lib of at._liste) {
        const cle = normaliser(lib).slice(0, 45);
        for (const cp of reac.competences)
          if (normaliser(cp.intitule).slice(0, 45) === cle) { cp.at_numero = at.numero; if (!at.competences.includes(cp.numero)) at.competences.push(cp.numero); }
      }
      delete at._liste;
    }
    reac.transversales = joindreItems(section(texte, "^Comp[ée]tences transversales de l.emploi\\s*$", ["^Niveau et/ou", "^FICHE"]).split("\n"));
    if (!reac.activites.length) reac.avertissements.push("Aucune fiche « Activité type » trouvée : ce document est-il bien un REAC ?");
    if (!reac.competences.length) reac.avertissements.push("Aucune fiche « Compétence professionnelle » trouvée.");
    for (const cp of reac.competences) {
      if (!cp.at_numero) reac.avertissements.push(`CP${cp.numero} non rattachée à une activité type : vérifier.`);
      if (!cp.criteres.length) reac.avertissements.push(`CP${cp.numero} : critères de performance introuvables.`);
    }
    reac.competence = (n) => reac.competences.find((c) => c.numero === n);
    reac.activite = (n) => reac.activites.find((a) => a.numero === n);
    return reac;
  }

  // ------------------------------------------------------------------ RE / RC
  const MODALITES = ["Mise en situation professionnelle", "Présentation d'un projet réalisé en amont de la session",
    "Questionnement à partir de production(s)", "Questionnaire professionnel", "Entretien technique", "Entretien final",
    "Entretien technique final"];
  const RE_DUREE = /(\d{1,2})\s*h\s*(\d{2})\s*min/;
  const minutesDe = (s) => { const m = RE_DUREE.exec(s); return m ? +m[1] * 60 + +m[2] : 0; };

  function analyserRe(texte, reac) {
    const r = { epreuves: [], duree_totale: "", periode_entreprise: [], productions: [], documents: [], diaporamas: [], avertissements: [] };
    const norm = texte.replace(/'/g, "’");
    let tab = section(norm, "^\\s*3\\.1\\.?\\s*Modalités d’évaluation des compétences et organisation de l’épreuve", ["^Informations complémentaires", "^3\\.2\\."]);
    if (!tab) tab = section(norm, "^Modalités d’évaluation des compétences et organisation de l’épreuve\\s*$", ["^Informations complémentaires", "^3\\.2\\."]);
    if (!tab) r.avertissements.push("Tableau des modalités d'évaluation introuvable.");
    const debuts = [...tab.matchAll(/^\s*(?:-\s*)?(Mise en situation|Entretien technique|Questionnaire|Questionnement à partir|Entretien final|Présentation d’un projet)/gm)];
    const titres = (reac ? reac.competences : []).map((c) => [c.numero, normaliser(c.intitule).slice(0, 40)]);
    debuts.forEach((m, i) => {
      const morceau = tab.slice(m.index, i + 1 < debuts.length ? debuts[i + 1].index : tab.length);
      const tete = normaliser(morceau.replace(/^[\s-]+/, ""));
      const nom = MODALITES.find((x) => tete.startsWith(normaliser(x).slice(0, 18))) || m[1];
      const dm = RE_DUREE.exec(morceau);
      if (normaliser(morceau.slice(0, 200)).includes("sans objet") && !dm) return;
      const mn = normaliser(morceau);
      r.epreuves.push({ modalite: nom, duree: dm ? dm[0] : "", minutes: minutesDe(morceau),
        competences: titres.filter(([, t]) => t && mn.includes(t)).map(([n]) => n), detail: morceau.replace(/\s+/g, " ").trim().slice(0, 1500) });
    });
    let m = /Durée totale de l’épreuve pour le candidat\s*:?\s*(\d{1,2}\s*h\s*\d{2}\s*min)/.exec(norm);
    if (m) r.duree_totale = m[1];
    const per = section(norm, "^Période en entreprise\\s*:?\\s*$", ["^Production\\s*:?\\s*$", "^La période en entreprise est incluse"]);
    r.periode_entreprise = joindreItems(per.split("\n")).map((l) => l.replace(/^[- ]+/, "").trim()).filter(Boolean);

    const parties = [...norm.matchAll(/Cette partie comporte (entre \d+ et \d+ pages)\.\s*Elle se réfère à la compétence\s*«\s*([\s\S]+?)\s*»/g)];
    const vus = new Set();
    parties.forEach((m, i) => {
      const comp = m[2].replace(/\s+/g, " ").trim();
      if (vus.has(normaliser(comp))) return;
      vus.add(normaliser(comp));
      let corps = norm.slice(m.index + m[0].length, i + 1 < parties.length ? parties[i + 1].index : norm.length);
      const coupe = /^(Diaporama relatif|Document relatif|Précisions pour|\d\.\d\.)/m.exec(corps);
      if (coupe) corps = corps.slice(0, coupe.index);
      const partie = { competence: comp, pages: m[1], themes: [] };
      let courant = null;
      for (let l of corps.split("\n")) {
        l = l.trim();
        const t = /^(\d)\.\s+(.+?)\s*:?\s*$/.exec(l);
        if (t) { courant = [t[2].replace(/[ :]+$/, ""), []]; partie.themes.push(courant); }
        else if (l.startsWith("- ") && courant) courant[1].push(l.slice(2).trim());
        else if (courant && courant[1].length && l && estMinuscule(l[0])) courant[1][courant[1].length - 1] += " " + l;
      }
      r.productions.push(partie);
    });
    for (const m of norm.matchAll(/Ce document comporte (entre \d+ et \d+ pages)[^.]*\./g)) {
      const avant = norm.slice(Math.max(0, m.index - 300), m.index);
      const act = [...avant.matchAll(/Document relatif à l’activité\s*«\s*([\s\S]+?)\s*»/g)];
      const lib = act.length ? act[act.length - 1][1].replace(/\s+/g, " ") : "Document";
      const l = `${lib} : ${m[1]}`;
      if (!r.documents.includes(l)) r.documents.push(l);
    }
    for (const m of norm.matchAll(/diaporama de (\d+ à \d+ diapositives)/g)) {
      const avant = norm.slice(Math.max(0, m.index - 400), m.index);
      const act = [...avant.matchAll(/Diaporama relatif à l’activité\s*«\s*([\s\S]+?)\s*»/g)];
      const lib = act.length ? act[act.length - 1][1].replace(/\s+/g, " ") : "Diaporama";
      const l = `${lib} : ${m[1]}`;
      if (!r.diaporamas.includes(l)) r.diaporamas.push(l);
    }
    m = /police (Arial \d+, interligne [\d,]+)/.exec(norm);
    if (m) r.documents.push(`Mise en forme imposée : ${m[1]}`);
    return r;
  }

  // ------------------------------------------------- Fiche France Compétences
  function entre(t, debut, fins) {
    const i = t.indexOf(debut);
    if (i < 0) return "";
    const reste = t.slice(i + debut.length);
    let fin = reste.length;
    for (const f of fins) { const p = reste.indexOf(f); if (p > 0 && p < fin) fin = p; }
    return reste.slice(0, fin).replace(/^[\s:]+|[\s:]+$/g, "");
  }

  function analyserFiche(texte) {
    const t = texte.replace(/'/g, "’");
    const f = { code: "", type_fiche: "", intitule: "", etat: "", niveau: "", nsf: [], formacodes: [], rome: [], certificateur: "",
      date_debut: "", date_echeance: "", objectifs: "", activites_visees: "", competences_attestees: "", modalites_evaluation: "",
      blocs: [], secteurs: [], emplois: [], prerequis_entree: "", prerequis_validation: "", voies_acces: [], correspondances: [],
      statistiques: [], duree_formation: "", avertissements: [] };
    let m = /\b((RNCP|RS)\s?\d{3,6})\b/.exec(t);
    if (m) {
      f.code = m[1].replace(/ /g, ""); f.type_fiche = m[2];
      const e = /^\s*(Active|Inactive)/.exec(t.slice(m.index + m[0].length, m.index + m[0].length + 30));
      f.etat = e ? e[1] : "";
    }
    m = /Répertoire (?:national des certifications professionnelles|spécifique)\s+(.+?)\n/.exec(t);
    if (m) f.intitule = m[1].trim();
    m = /\b(Niveau \d)\b/.exec(t);
    if (m) f.niveau = m[1];
    const zone = entre(t, "Code(s) NSF", ["Date de début"]);
    f.nsf = [...zone.matchAll(/(\d{3}[a-z]\s*:\s*[^\n]+)/g)].map((x) => x[1]);
    f.formacodes = [...zone.matchAll(/(?:^|\s)(\d{5}\s*:\s*[^\n]+)/g)].map((x) => x[1].trim());
    m = /(\d{2}-\d{2}-\d{4})\s*\n?\s*parcours certifiants/.exec(t) || /parcours certifiants\s*(\d{2}-\d{2}-\d{4})/.exec(t);
    if (m) f.date_debut = m[1];
    m = /Date d’échéance\s*\n?\s*(?:de l’enregistrement\s*)?(\d{2}-\d{2}-\d{4})/.exec(t);
    if (m) f.date_echeance = m[1];
    const cert = entre(t, "Certificateur(s)", ["Résumé de la certification", "Objectifs et contexte"]);
    f.certificateur = cert.split("\n").map((l) => l.replace(/\b\d{5,}\b|\b\d\b|(^|\s)-(?=\s|$)/g, " ")
      .replace(/\b(Nom légal|Siret|Nom|Site|commercial|internet)\b/g, " ").trim()).filter(Boolean).join(" ")
      .replace(/\s+/g, " ").replace(/L’ /g, "L’").replace(/L' /g, "L'").trim();
    f.objectifs = entre(t, "Objectifs et contexte de la certification", ["Activités visées"]).replace(/\s*\n\s*/g, " ").trim();
    f.activites_visees = entre(t, "Activités visées", ["Résumé de la certification", "Compétences attestées"]).replace("Résumé de la certification", "").trim();
    f.competences_attestees = entre(t, "Compétences attestées", ["Modalités d’évaluation"]);
    f.modalites_evaluation = entre(t, "Modalités d’évaluation :", ["Blocs de compétences", `${f.code}BC01`]);
    // Blocs : depuis « Compétences attestées » (la source la plus propre)
    const groupes = [];
    for (let l of f.competences_attestees.split("\n")) {
      l = l.trim();
      if (!l) continue;
      if (l.startsWith("-")) { if (groupes.length) groupes[groupes.length - 1][1].push(l.replace(/^[- ]+/, "").replace(/\.$/, "").trim()); }
      else if (groupes.length && groupes[groupes.length - 1][1].length && estMinuscule(l[0])) { const g = groupes[groupes.length - 1][1]; g[g.length - 1] += " " + l; }
      else groupes.push([l, []]);
    }
    const blocsCodes = f.code ? [...t.matchAll(new RegExp(`^(${f.code}BC\\d{2})\\s*-\\s*(.+?)$`, "gm"))] : [];
    const vus = new Set();
    for (const bm of blocsCodes) {
      if (vus.has(bm[1])) continue;
      const g = groupes.find(([titre]) => normaliser(titre).slice(0, 35) === normaliser(bm[2]).slice(0, 35));
      if (!g) continue;
      vus.add(bm[1]);
      const apres = t.slice(bm.index, bm.index + 3000);
      const d = /Durée totale de l’épreuve pour le candidat\s*:\s*(\d{2} h \d{2} min)/.exec(apres);
      f.blocs.push({ code: bm[1], intitule: g[0], competences: g[1], evaluation: d ? d[1] : "" });
    }
    if (!f.blocs.length) groupes.forEach(([titre, comps], i) => f.blocs.push({ code: `${f.code}BC${String(i + 1).padStart(2, "0")}`, intitule: titre, competences: comps, evaluation: "" }));

    const lignesTirets = (s) => s.split("\n").filter((x) => x.trim().startsWith("-")).map((x) => x.replace(/^[\s-]+/, "").trim());
    f.secteurs = lignesTirets(entre(t, "Secteurs d’activités :", ["Type d’emplois", "Type d'emplois"]));
    f.emplois = lignesTirets(entre(t, "accessibles :", ["Code(s) ROME"]));
    f.rome = [...new Set([...t.matchAll(/([A-Z]\d{4}\s*-\s*.+)/g)].map((x) => x[1].trim()))];
    m = /prérequis à l’entrée en formation\s*:\s*([\s\S]*?)\n\s*Le cas éch[ée]?ant, prérequis à la validation/.exec(t);
    f.prerequis_entree = m ? m[1].replace(/\s+/g, " ").trim() : "";
    m = /prérequis à la validation de la certification\s*:\s*([\s\S]*?)(Pré-requis disctincts|Pré-requis distincts|Voie d’accès à)/.exec(t);
    if (m) f.prerequis_validation = m[1].replace(/^[A-Z]\d{4}\s*-.*$/gm, "").replace("Voie d’accès", "").replace(/\s+/g, " ").trim();
    let curseur = t.indexOf("Voie d’accès à");
    if (curseur >= 0)
      for (const [voie, cle] of [["Après un parcours de formation sous statut d’élève ou d’étudiant", "Après un parcours"],
        ["En contrat d’apprentissage", "En contrat"], ["Après un parcours de formation continue", "Après un parcours"],
        ["En contrat de professionnalisation", "En contrat de"], ["Par candidature individuelle", "Par candidature"],
        ["Par expérience (VAE)", "Par expérience"]]) {
        const i = t.indexOf(cle, curseur);
        if (i < 0) continue;
        const mx = /\bX\b(\s*-\s*-)?/.exec(t.slice(i, i + 250));
        if (mx) f.voies_acces.push([voie, !mx[1]]);
        curseur = i + cle.length;
      }
    const zc = entre(t, "Liens avec d’autres certifications", ["Base légale"]);
    const noms = {};
    for (const x of zc.matchAll(/(RNCP\d{5})\s+-\s+((?:BTS|TP|BUT|BP|CAP|Licence|Titre|Bac)[^\n]*?)(?=\s+RNCP\d|\n|$)/g)) if (!noms[x[1]]) noms[x[1]] = x[2].trim();
    const ext = {};
    for (const x of zc.matchAll(/(RNCP\d{5})(BC\d{2})/g)) if (x[1] !== f.code) { ext[x[1]] = ext[x[1]] || []; if (!ext[x[1]].includes(x[2])) ext[x[1]].push(x[2]); }
    for (const [code, bcs] of Object.entries(ext))
      f.correspondances.push(`${code}${noms[code] ? " – " + noms[code] : ""} : correspondance partielle (blocs ${bcs.sort().join(", ")}) — intitulé complet à vérifier sur la fiche`);
    const st = entre(t, "Statistiques :", ["Lien internet", "Pour plus"]);
    for (const x of st.matchAll(/^(20\d{2})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$/gm))
      f.statistiques.push({ annee: x[1], certifies: x[2], vae: x[3], insertion_6_mois: x[4], metier_6_mois: x[5], metier_2_ans: x[6] });
    m = /Durée (?:totale )?(?:de la )?formation\s*:?\s*([\d\s]+heures?)/i.exec(t);
    if (m) f.duree_formation = m[1].trim();
    else f.avertissements.push("La fiche France Compétences n'indique pas de durée de formation : la durée en centre doit être fixée par la convention avec l'organisme (ou par vous).");
    if (!f.prerequis_entree) f.avertissements.push("Aucun prérequis d'entrée indiqué sur la fiche : à définir par l'organisme (information obligatoire du programme, Qualiopi indicateur 1).");
    return f;
  }

  function detecterType(texte) {
    const debut = normaliser(texte.slice(0, 3000));
    if (debut.includes("referentiel emploi activites competences") || normaliser(texte.slice(0, 60000)).includes("fiche competence professionnelle"))
      if (!debut.includes("referentiel d'evaluation") && !debut.includes("referentiel de certification")) return "REAC";
    if (debut.includes("referentiel d'evaluation") || debut.includes("referentiel de certification")) return "RE";
    if (normaliser(texte).includes("francecompetences") || debut.includes("code de la fiche")) return "FICHE";
    return "INCONNU";
  }

  Object.assign(D, { normaliser, joindreItems, decouperPhrases, analyserReac, analyserRe, analyserFiche, detecterType, volume, estMinuscule });
})(typeof window !== "undefined" ? window : globalThis);

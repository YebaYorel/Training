/* Moteur pédagogique — portage de decorticage/pedagogie.py.
 * Bloom révisée (Anderson & Krathwohl, 2001) ; Bruner : modes enactif /
 * iconique / symbolique, spirale, 6 fonctions d'étayage (Wood, Bruner & Ross, 1976). */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const N = (s) => D.normaliser(s);

  const NIVEAUX_BLOOM = { 1: "Se souvenir", 2: "Comprendre", 3: "Appliquer", 4: "Analyser", 5: "Évaluer", 6: "Créer" };
  const VERBES = {
    1: ["identifier", "citer", "nommer", "lister", "reperer", "reconnaitre", "enumerer", "connaitre", "recenser", "localiser"],
    2: ["expliquer", "decrire", "distinguer", "illustrer", "interpreter", "reformuler", "situer", "resumer", "comprendre",
      "differencier", "classer", "presenter", "informer", "sensibiliser", "ecouter", "echanger"],
    3: ["appliquer", "utiliser", "mettre en oeuvre", "realiser", "executer", "calculer", "transmettre", "renseigner",
      "receptionner", "faire respecter", "faire appliquer", "respecter", "mener", "animer", "conduire", "communiquer",
      "accompagner", "assurer", "participer", "mettre a disposition", "mettre en place", "mettre en avant", "pratiquer",
      "adopter", "deleguer", "accueillir", "conseiller", "traiter", "gerer", "suivre", "tenir", "veiller", "remplir",
      "collecter", "mobiliser", "impliquer", "associer", "partager", "fideliser", "valoriser", "encourager",
      "responsabiliser", "consulter", "cooperer", "collaborer", "travailler", "maintenir", "rendre compte", "signaler",
      "alerter", "adapter", "reagir", "etre", "prendre en compte", "integrer", "favoriser", "implanter", "installer",
      "motiver", "federer", "manager", "entretenir", "developper", "corriger", "reajuster", "inventorier", "commander",
      "stocker", "approvisionner", "mettre a jour", "maitriser"],
    4: ["analyser", "comparer", "diagnostiquer", "structurer", "organiser", "hierarchiser", "detecter", "examiner",
      "synthetiser", "anticiper", "identifier les causes", "prioriser", "decomposer", "rapprocher", "mesurer",
      "evaluer la charge", "coordonner", "relier", "selectionner", "rechercher", "controler la coherence", "articuler"],
    5: ["evaluer", "controler", "verifier", "justifier", "argumenter", "arbitrer", "valider", "juger", "critiquer",
      "apprecier", "s'assurer", "assurer le suivi", "tester", "auditer"],
    6: ["elaborer", "concevoir", "planifier", "construire", "proposer", "formuler", "preparer", "creer", "produire",
      "definir", "formaliser", "rediger", "imaginer", "ameliorer", "optimiser", "contribuer a l'elaboration", "batir",
      "composer", "etablir", "parametrer"],
  };
  const INDEX = Object.entries(VERBES).flatMap(([n, vs]) => vs.map((v) => [v, +n])).sort((a, b) => b[0].length - a[0].length);

  function niveauBloom(phrase) {
    const p = N(phrase).replace(/^(savoir|pouvoir|etre capable de|etre en mesure de)\s+/, "");
    for (const [v, n] of INDEX) if (p.startsWith(v)) return n;
    return 3;
  }
  function verbeInitial(phrase) {
    const mots = phrase.split(/\s+/).filter(Boolean);
    if (!mots.length) return "";
    const p = N(phrase);
    for (const [v] of INDEX) if (p.startsWith(v + " ") || p === v) return mots.slice(0, v.split(" ").length).join(" ");
    return mots[0];
  }

  const REMPLISSAGE = ["de son périmètre", "du périmètre", "au sein de l’établissement marchand", "de l’établissement marchand",
    "dans l’établissement marchand", "de manière précise et adaptée à la situation", "de manière adaptée à la situation",
    "selon la procédure interne", "de l’enseigne", "en vigueur", "courants", "courant", "et plus particulièrement",
    "le cas échéant", "si nécessaire", "notamment", "également"];
  const MOTS_VIDES = new Set(`le la les un une des de du d l à au aux et ou en dans sur pour par avec sans sous son sa ses leur leurs
ce cette ces qui que dont il elle ils elles se est sont être a ont plus moins tout tous toute toutes afin ainsi selon entre vers
chez lors cas échéant etc ex notamment également aussi très bien mise lien liés liées lié liée relatif relative relatives relatifs
concernant matière niveau type types façon manière cadre ensemble différentes différents principales principaux connaissance
connaissances notions fonction fonctions place compte faire œuvre oeuvre rendre auprès face autres autre issues issus afin cela
elles leurs mettre mise place sein travers partir`.split(/\s+/).map(N));

  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  function simplifier(phrase, garderVerbe = true) {
    let s = phrase.trim().replace(/\.$/, "");
    s = s.replace(/^(Connaissance|Connaître|Notions?)\s+(?:sur\s+|des\s+|du\s+|de la\s+|de l’|de\s+|d’)?/i, "");
    s = s.replace(/\(([^()]{28,})\)/g, "").replace(/\((ex\.?|par exemple)[^)]*\)/gi, "");
    for (const r of REMPLISSAGE) s = s.replace(new RegExp(`(?<!\\p{L})${esc(r)}(?!\\p{L})`, "giu"), "");
    s = s.replace(/\s+,/g, ",").replace(/\s{2,}/g, " ").replace(/^[ ,;:-]+|[ ,;:-]+$/g, "");
    if (!garderVerbe) s = s.slice(verbeInitial(s).length).trim();
    return s ? s[0].toUpperCase() + s.slice(1) : s;
  }
  const racine = (m) => N(m).replace(/[^a-z0-9]/g, "").slice(0, 7);

  function motsCles(phrase, max = 5) {
    const s = simplifier(phrase, false);
    const mots = s.match(/[A-Za-zÀ-ÖØ-öø-ÿœŒ’'\-]{3,}|[A-Z]{2,}/g) || [];
    const res = [], vus = new Set();
    for (const m of mots) {
      const m2 = m.replace(/^(l|d|qu|s|n)[’']/i, "").replace(/^[’'-]+|[’'-]+$/g, "");
      const c = N(m2);
      if (MOTS_VIDES.has(c) || vus.has(c) || c.length < 3 || (c.endsWith("ment") && c.length > 6)) continue;
      if ((c.endsWith("er") || c.endsWith("ir")) && m2 !== m2.toUpperCase() && !["manager", "dossier", "fichier"].includes(c)) continue;
      vus.add(c);
      res.push(m2 === m2.toUpperCase() ? m2 : m2.toLowerCase());
      if (res.length >= max) break;
    }
    return res;
  }

  const FAMILLES = [
    ["entreti", "individ", "feedbac", "recadra", "evaluat", "potenti", "progres"],
    ["briefin", "debrief", "reunion", "animer", "animati"],
    ["consign", "informa", "transme", "communi", "procedu", "expliqu", "partage", "message"],
    ["motivat", "stimula", "challen", "team", "federer", "cohesio", "dynamiq", "mobilis", "engagem", "fideli", "valoris"],
    ["amelior", "correct", "precon", "solutio", "proposi", "continu", "pdca", "deming", "qualite"],
    ["profess", "formati", "compete", "tutorat", "former", "montee", "develop", "parcour"],
    ["projet", "etapes", "retropl", "hierarc", "jalons"],
    ["handica", "discrim", "inclusi", "amenage", "rqth", "agefiph", "referen"],
    ["plannin", "horaire", "planifi", "charge", "tache", "taches", "absence", "imprevu", "effecti"],
    ["risque", "securit", "prevent", "epi", "tms", "duerp", "hygiene", "qhse", "accident"],
    ["recrute", "candida", "selecti", "poste", "integra", "essai", "accueil", "recrue"],
    ["stock", "stocks", "command", "inventa", "approvi", "recepti", "livrais", "fournis", "rupture"],
    ["merchan", "implant", "lineair", "planogr", "vitrine", "balisag", "operati", "promoti"],
    ["client", "clients", "clientel", "satisfa", "omnican", "crm", "argumen", "vente", "conseil"],
    ["indicat", "tableau", "chiffre", "panier", "transfo", "kpi", "donnees", "reporti", "synthes"],
    ["marge", "rentabi", "couts", "cout", "demarqu", "budget", "economi", "financi"],
    ["ecart", "ecarts", "causes", "analyse", "analyser", "diagnos", "ishikaw", "pareto", "derive"],
    ["gaspill", "dechets", "vrac", "seconde", "reemplo", "ecologi", "rse", "durabil", "environ"],
    ["managem", "manager", "posture", "leaders", "pratiqu", "situati"],
    ["hierarc", "rendre", "alerte", "remonte", "signale"],
  ];
  const FAMILLE_DE = {};
  FAMILLES.forEach((f, i) => f.forEach((r) => { FAMILLE_DE[r] = "#f" + i; }));
  function jetons(phrase) {
    const r = new Set((phrase.replace(/’/g, " ").match(/[A-Za-zÀ-ÿœ]{3,}/g) || []).filter((m) => !MOTS_VIDES.has(N(m))).map(racine));
    for (const x of [...r]) if (FAMILLE_DE[x]) r.add(FAMILLE_DE[x]);
    return r;
  }

  const VERBES_SAVOIRS = [
    [["principe", "règle", "réglementation", "cadre légal", "obligation", "droit", "code du travail", "législation", "disposition"], "Expliquer"],
    [["outil", "technique", "méthode", "démarche", "procédure", "étape", "dispositif"], "Décrire"],
    [["indicateur", "ratio", "taux", "terme"], "Expliquer"],
    [["catégorie", "type", "famille", "motif", "forme", "différent", "style"], "Distinguer"],
    [["rôle", "acteur", "enjeu", "environnement", "politique", "stratégie"], "Situer"],
  ];
  function objectifDepuisSavoir(savoir) {
    let objet = simplifier(savoir);
    const n = N(objet);
    let verbe = "Identifier";
    for (const [ind, v] of VERBES_SAVOIRS) if (ind.some((i) => n.includes(N(i)))) { verbe = v; break; }
    const m = /^(Connaissance|Connaître|Notions?)\s+(sur\s+|des\s+|du\s+|de la\s+|de l’|de\s+|d’)?/i.exec(savoir.trim());
    const art = m && m[2] ? m[2].trim().toLowerCase() : "";
    const article = { des: "les", du: "le", "de la": "la", "de l’": "l’" }[art] || "";
    if (objet && article) objet = article + (article.endsWith("’") ? "" : " ") + objet[0].toLowerCase() + objet.slice(1);
    else if (objet) objet = objet[0].toLowerCase() + objet.slice(1);
    return `${verbe} ${objet}`.trim();
  }
  const formuler = (l) => (/^(Connaissance|Connaître|Notions?)(?!\p{L})/iu.test(l.trim()) ? objectifDepuisSavoir(l) : simplifier(l));

  const MODES = {
    enactif: "Enactif (agir : mise en situation, manipulation, jeu de rôle)",
    iconique: "Iconique (voir : schéma, carte mentale, visuel, vidéo)",
    symbolique: "Symbolique (formaliser : concept, règle, calcul, synthèse écrite)",
  };
  const ETAYAGE = [
    ["Enrôlement", "Accroche : situation vécue / question choc / exemple local"],
    ["Réduction des degrés de liberté", "Consigne courte, une seule tâche à la fois"],
    ["Maintien de l'orientation", "Rappel de l'objectif et du critère de réussite"],
    ["Signalisation des caractéristiques déterminantes", "Points clés mis en évidence (mots-clés REAC)"],
    ["Contrôle de la frustration", "Droit à l'erreur, aide graduée, binôme"],
    ["Démonstration", "Modèle montré par le formateur puis reproduit par le stagiaire"],
  ];
  function modeBruner(cat, niv) {
    if (cat === "savoir") return niv <= 2 ? MODES.iconique : MODES.symbolique;
    if (cat === "technique" || cat === "organisationnel") return niv === 4 || niv === 5 ? MODES.symbolique : MODES.enactif;
    if (cat === "relationnel" || cat === "critere") return MODES.enactif;
    return MODES.iconique;
  }
  const ACTIVITES = [
    [["briefing", "débriefing", "réunion"], "Simulation de briefing de 5 min (minuteur) puis débriefing croisé"],
    [["entretien"], "Jeu de rôle en trinôme : manager / collaborateur / observateur avec grille"],
    [["conflit"], "Jeu de rôle « conflit d'équipe » + méthode DESC (Décrire-Exprimer-Spécifier-Conséquences)"],
    [["planning", "plannings", "horaire", "planifier", "rétroplanning", "gantt", "pert"], "Atelier tableur : construire le planning d'une semaine avec contraintes (absences, livraison)"],
    [["handicap"], "Étude de cas d'aménagement + mise en situation de simulation (lunettes, gants)"],
    [["discrimin"], "Analyse de situations courtes : discriminant ou non ? (vote, puis règle de droit)"],
    [["risque", "sécurité", "prévention", "tms", "epi", "duerp"], "« Chasse aux risques » sur photos de surface de vente + mini-DUERP"],
    [["recrut", "candidat", "fiche de poste", "cv"], "Analyse de 3 CV fictifs avec grille de critères"],
    [["intégration", "tutorat", "période d’essai", "nouvelle recrue"], "Construire le parcours d'intégration J1-J30 d'une nouvelle recrue"],
    [["stock", "commande", "inventaire", "approvisionnement", "réception", "livraison"], "Cas chiffré sur tableur : calcul de commande (stock, ventes, délai, stock de sécurité)"],
    [["merchandising", "implantation", "planogramme", "linéaire", "vitrine", "balisage"], "Atelier planogramme / visite terrain photo d'un rayon + critique"],
    [["client", "accueil", "omnicanal", "crm", "fidélis", "satisfaction"], "Parcours client mystère + carte d'expérience client (moments de vérité)"],
    [["argumentaire", "argument", "vente"], "Construire un argumentaire CAP (Caractéristique-Avantage-Preuve) et le jouer"],
    [["marge", "rentabilité", "coût", "démarque", "budget", "économique", "seuil"], "Cas chiffré : calcul de marge, démarque et seuil de rentabilité sur tableur"],
    [["indicateur", "chiffre d’affaires", "panier", "transformation", "tableau de bord", "kpi"], "Construire un tableau de bord (CA, panier moyen, taux de transformation) N/N-1"],
    [["écart", "analyse", "diagnostic", "ishikawa", "pareto", "cause"], "Diagnostic en sous-groupes : Ishikawa (5M) puis Pareto sur un cas réel"],
    [["plan d’actions", "action corrective", "actions correctives", "ajustement"], "Bâtir un plan d'actions SMART + tableau de suivi (qui/quoi/quand/indicateur)"],
    [["motivation", "stimulation", "challenge", "team building", "fédérer", "cohésion"], "Concevoir un challenge d'équipe (objectif, règles, récompense) et le pitcher"],
    [["compétence", "formation", "progression", "développement professionnel", "potentiel"], "Matrice de compétences de l'équipe + plan de formation individualisé"],
    [["communication", "consigne", "écoute", "questionnement"], "Exercice « consigne en 3 phrases » + reformulation par le binôme"],
    [["rse", "gaspillage", "déchet", "vrac", "seconde main", "réemploi", "écologique"], "Atelier anti-gaspillage : plan de réduction des invendus et valorisation"],
    [["numérique", "digital", "média", "réseaux sociaux", "e-réputation"], "Audit d'e-réputation d'une enseigne (avis Google, réseaux sociaux)"],
  ];
  const EXEMPLES_LOCAUX = [
    [["stock", "commande", "approvisionnement", "rupture"], "Alerte cyclonique : anticiper la demande (eau, piles, conserves) et les délais de fret maritime"],
    [["livraison", "réception", "fournisseur", "anomalie"], "Conteneur arrivé au Port Est avec avaries : contrôler, signaler, réserver"],
    [["marge", "coût", "prix", "rentabilité"], "Prix de revient d'un produit importé : achat + fret + octroi de mer → impact sur la marge"],
    [["opération commerciale", "opérations commerciales", "promotion", "événement", "saison"], "Opération commerciale calée sur un temps fort local (Grand Raid, fêtes de fin d'année, 20 décembre)"],
    [["planning", "horaire", "imprévu", "absence"], "Fermeture anticipée en alerte orange cyclonique : replanifier l'équipe et informer les clients"],
    [["équipe", "intergénérationnelle", "diverse", "motivation", "fédérer"], "Équipe multigénérationnelle d'un supermarché de l'Est : motiver jeunes recrues et anciens"],
    [["client", "accueil", "communication"], "Accueil d'un client qui s'exprime en créole : adapter son langage et sa posture"],
    [["handicap"], "Accueil d'un client à mobilité réduite un samedi d'affluence en centre commercial"],
    [["risque", "sécurité", "tms", "chaleur"], "Mise en rayon en réserve non climatisée en plein été austral : prévenir la fatigue et les TMS"],
    [["gaspillage", "déchet", "vrac", "écologique", "rse"], "Fruits et légumes péi en fin de journée : réduire la casse et valoriser les invendus"],
    [["recrut", "intégration", "tutorat"], "Renforts saisonniers pour les fêtes : recruter et intégrer en 1 semaine"],
    [["indicateur", "chiffre d’affaires", "panier", "écart", "performance"], "Comparer le CA N/N-1 d'un magasin du Sud pendant une période de routes coupées"],
  ];
  function suggestion(table, phrase, defaut = "") {
    const n = N(phrase);
    for (const [mots, t] of table) if (mots.some((m) => n.includes(N(m)))) return t;
    return defaut;
  }

  const ORDRE_CAT = { savoir: 0, technique: 1, organisationnel: 2, relationnel: 3, critere: 4, module: 5 };
  const CATS = [["sf_techniques", "technique"], ["sf_organisationnels", "organisationnel"], ["sf_relationnels", "relationnel"]];

  function titreEtape(phrase) {
    let s = phrase.trim();
    const m = /^(Dans le respect|En collaboration|À partir|A partir|Selon|Sous|En lien|En fonction|Afin|Pour|En tenant|Au regard|En cas)(?!\p{L})[^,]*(,[^,]*)*?,\s+(?=[a-zéèêàâîôû]+(er|ir|re)(?!\p{L}))/u.exec(s);
    if (m) s = s.slice(m[0].length);
    s = simplifier(s);
    if (s.length > 120) s = s.slice(0, 120).replace(/\s+\S*$/, "").replace(/[,;: ]+$/, "") + "…";
    return s;
  }

  function objectif(o) {
    return Object.assign({ contenus: [], mots: [], associes: [], criteres: [], minutes: 0, mode: "", activite: "", exemple: "" }, o);
  }

  function construireSeances(cp) {
    const etapes = cp.description.length ? cp.description : [cp.intitule];
    const seances = etapes.map((e) => ({ titre: titreEtape(e), origine: e, objectifs: [], minutes: 0, numero: 0, cp: cp.numero, at: cp.at_numero, sequence: 0, sequence_titre: "", type_seance: "apprentissage" }));
    const je = etapes.map(jetons);
    const df = {};
    je.forEach((js) => js.forEach((j) => { df[j] = (df[j] || 0) + 1; }));
    const score = (js, i) => [...js].filter((j) => je[i].has(j)).reduce((s, j) => s + 1 / df[j], 0);
    const charge = seances.map(() => 0);
    for (const [attr, cat] of CATS)
      for (const ligne of cp[attr]) {
        const js = jetons(ligne);
        const sc = seances.map((_, i) => score(js, i));
        const best = sc.length ? Math.max(...sc) : 0;
        let i;
        if (best >= 0.5) i = sc.indexOf(best);
        else {
          let cand = sc.map((v, k) => (v >= best - 1e-9 ? k : -1)).filter((k) => k >= 0);
          if (!cand.length) cand = seances.map((_, k) => k);
          i = cand.reduce((a, k) => (charge[k] < charge[a] ? k : a), cand[0]);
        }
        charge[i]++;
        const texte = formuler(ligne), niv = niveauBloom(texte);
        seances[i].objectifs.push(objectif({ texte, verbe: verbeInitial(texte), niveau: niv, categorie: cat, origine: ligne, mots: motsCles(ligne),
          mode: modeBruner(cat, niv), activite: suggestion(ACTIVITES, ligne + " " + etapes[i], "Étude de cas guidée puis application en binôme"),
          exemple: suggestion(EXEMPLES_LOCAUX, ligne + " " + etapes[i]) }));
      }
    for (const s of seances)
      if (!s.objectifs.length) {
        const niv = niveauBloom(s.titre);
        s.objectifs.push(objectif({ texte: s.titre, verbe: verbeInitial(s.titre), niveau: niv, categorie: "technique", origine: s.origine,
          mots: motsCles(s.origine), mode: modeBruner("technique", niv), activite: suggestion(ACTIVITES, s.origine, "Étude de cas guidée puis application en binôme"),
          exemple: suggestion(EXEMPLES_LOCAUX, s.origine) }));
      }
    const tous = [];
    seances.forEach((s, si) => s.objectifs.forEach((o, oi) => tous.push([si, oi, jetons(o.origine + " " + s.origine)])));
    const fo = {};
    tous.forEach(([, , js]) => js.forEach((j) => { fo[j] = (fo[j] || 0) + 1; }));
    let rot = 0;
    for (const sav of cp.savoirs) {
      const js = jetons(sav);
      const notes = tous.map(([, , jo]) => [...js].filter((j) => jo.has(j)).reduce((s, j) => s + 1 / fo[j], 0));
      const best = Math.max(...notes);
      const k = best > 0 ? notes.indexOf(best) : rot++ % tous.length;
      const [si, oi] = tous[k];
      seances[si].objectifs[oi].contenus.push(simplifier(sav));
    }
    for (const s of seances) s.objectifs.sort((a, b) => ORDRE_CAT[a.categorie] - ORDRE_CAT[b.categorie] || a.niveau - b.niveau);
    if (cp.criteres.length) {
      const ev = { titre: `Entraînement à l'évaluation — ${simplifier(cp.intitule)}`, origine: "Critères de performance du REAC", objectifs: [],
        minutes: 0, numero: 0, cp: cp.numero, at: cp.at_numero, sequence: 0, sequence_titre: "", type_seance: "evaluation" };
      for (const c of cp.criteres)
        ev.objectifs.push(objectif({ texte: `Démontrer que : ${c[0].toLowerCase() + c.slice(1)}`, verbe: "Démontrer", niveau: 5, categorie: "critere",
          origine: c, criteres: [c], mots: motsCles(c), mode: modeBruner("critere", 5),
          activite: "Mise en situation type examen + auto-évaluation sur la grille du critère", exemple: suggestion(EXEMPLES_LOCAUX, c) }));
      seances.push(ev);
    }
    return seances;
  }

  const PAS = 15;
  function repartir(total, poids, minimum = PAS) {
    if (!poids.length) return [];
    const u = Math.floor(total / PAS), somme = poids.reduce((a, b) => a + b, 0) || 1;
    const bruts = poids.map((p) => (u * p) / somme);
    const plancher = u >= poids.length * (minimum / PAS) ? minimum / PAS : 0;
    const base = bruts.map((b) => Math.max(Math.floor(b), plancher));
    while (base.reduce((a, b) => a + b, 0) > u) { const i = base.indexOf(Math.max(...base)); base[i]--; }
    const restes = bruts.map((b, i) => [b - Math.floor(b), i]).sort((a, b) => b[0] - a[0]).map((x) => x[1]);
    let k = 0;
    while (base.reduce((a, b) => a + b, 0) < u) { base[restes[k % restes.length]]++; k++; }
    return base.map((b) => b * PAS);
  }
  const poidsObjectif = (o) => 1 + 0.15 * (o.niveau - 1) + 0.35 * o.contenus.length + 0.5 * o.associes.length;

  function fusionnerSiNecessaire(s, minutes, mini = 30) {
    const max = Math.max(1, Math.floor(minutes / mini));
    while (s.objectifs.length > max) {
      let best = null;
      for (let i = 0; i < s.objectifs.length - 1; i++) {
        const a = s.objectifs[i], b = s.objectifs[i + 1];
        if (a.categorie === b.categorie || best === null) {
          const p = poidsObjectif(a) + poidsObjectif(b) + (a.categorie === b.categorie ? 0 : 5);
          if (best === null || p < best[0]) best = [p, i];
        }
      }
      const i = best[1], a = s.objectifs[i], b = s.objectifs.splice(i + 1, 1)[0];
      if (b.niveau > a.niveau) {
        [a.texte, b.texte] = [b.texte, a.texte];
        a.verbe = b.verbe; a.niveau = b.niveau;
        [a.origine, b.origine] = [b.origine, a.origine];
      }
      a.associes.push(b.origine === b.texte ? b.texte : simplifier(b.origine), ...b.associes);
      a.contenus.push(...b.contenus);
      a.criteres.push(...b.criteres);
      for (const m of b.mots) if (!a.mots.includes(m) && a.mots.length < 7) a.mots.push(m);
    }
  }

  function decouperCompetence(cp, minutesCp, partEval = 0.12) {
    const seances = construireSeances(cp);
    const ev = seances.filter((s) => s.type_seance === "evaluation"), ap = seances.filter((s) => s.type_seance !== "evaluation");
    let mEval = 0;
    if (ev.length) {
      mEval = Math.max(PAS * 4, Math.round((minutesCp * partEval) / PAS) * PAS);
      mEval = Math.min(mEval, Math.floor(minutesCp / 3 / PAS) * PAS);
    }
    const durees = repartir(minutesCp - mEval, ap.map((s) => s.objectifs.reduce((t, o) => t + poidsObjectif(o), 0)), PAS * 2);
    ap.forEach((s, i) => { s.minutes = durees[i]; });
    ev.forEach((s) => { s.minutes = mEval; });
    for (const s of seances) {
      fusionnerSiNecessaire(s, s.minutes);
      const d = repartir(s.minutes, s.objectifs.map(poidsObjectif));
      s.objectifs.forEach((o, i) => { o.minutes = d[i]; });
      const garde = s.objectifs.filter((o) => o.minutes > 0);
      s.objectifs = garde.length ? garde : s.objectifs.slice(0, 1);
    }
    return seances.filter((s) => s.minutes > 0);
  }
  const poidsCompetences = (reac) => Object.fromEntries(reac.competences.map((c) => [c.numero, Math.max(D.volume(c), 1)]));

  Object.assign(D, { NIVEAUX_BLOOM, ETAYAGE, MODES, niveauBloom, verbeInitial, simplifier, motsCles, objectifDepuisSavoir, formuler,
    modeBruner, construireSeances, decouperCompetence, repartir, poidsCompetences, PAS, objectif });
})(typeof window !== "undefined" ? window : globalThis);

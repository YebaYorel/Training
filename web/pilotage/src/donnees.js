/* Données de référence : Qualiopi V10, bibliothèque documentaire, documents d'une action, structure du coffre.
 * Qualiopi : Référentiel national qualité modifié par le décret n° 2026-728 du 1er août 2026 (JO du 4 août 2026),
 * applicable aux audits réalisés à partir du 1er novembre 2026 : 7 critères, 33 indicateurs.
 * Les libellés ci-dessous reprennent le référentiel 2019 (décret n° 2019-564) ; pour les indicateurs signalés
 * « modifié V10 », la nouvelle exigence est résumée d'après des sources secondaires et votre base Airtable :
 * le texte exact de l'annexe doit être confirmé sur Légifrance (JORFTEXT000054608509). */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});

  // portée : "tous" ; "certif" (actions conduisant à une certification) ; "alternance" ; "cfa" (actions par apprentissage)
  // v10 : résumé de la modification apportée par le décret 2026-728 (vide = inchangé selon les sources consultées)
  // docs : identifiants de la BIBLIOTHEQUE qui prouvent l'indicateur
  const QUALIOPI = [
    [1, 1, "tous", "Le prestataire diffuse une information accessible au public, détaillée et vérifiable sur les prestations proposées : prérequis, objectifs, durée, modalités et délais d'accès, tarifs, contacts, méthodes mobilisées et modalités d'évaluation, accessibilité aux personnes handicapées.",
      "Mentionner explicitement les méthodes pédagogiques et les modes de financement mobilisables ; aucune mention de nature à induire en erreur sur l'accès, le contenu, le financement ou les débouchés (jamais « éligible CPF » sans code RNCP/RS).", ["programmes", "tarifs", "financements", "mentions", "cgv", "handicap"]],
    [2, 1, "tous", "Le prestataire diffuse des indicateurs de résultats adaptés à la nature des prestations mises en œuvre et des publics accueillis.",
      "Publier la méthode de calcul de chaque indicateur (période, nombre de répondants, formule) : un taux seul ne suffit plus.", ["methode_resultats", "froid", "chaud"]],
    [3, 1, "certif", "Lorsque le prestataire met en œuvre des prestations conduisant à une certification professionnelle, il informe sur les taux d'obtention des certifications préparées, les possibilités de valider un ou des blocs de compétences, ainsi que sur les équivalences, passerelles, suites de parcours et les débouchés.",
      "Préciser les suites de parcours (poursuites d'études, débouchés).", ["programmes", "methode_resultats"]],
    [4, 2, "tous", "Le prestataire analyse le besoin du bénéficiaire en lien avec l'entreprise et/ou le financeur concerné(s).", "", ["besoin", "financements"]],
    [5, 2, "tous", "Le prestataire définit les objectifs opérationnels et évaluables de la prestation.", "", ["programmes", "seances"]],
    [6, 2, "tous", "Le prestataire établit les contenus et les modalités de mise en œuvre de la prestation, adaptés aux objectifs définis et aux publics bénéficiaires.", "", ["programmes", "seances"]],
    [7, 2, "certif", "Lorsque le prestataire met en œuvre des prestations conduisant à une certification professionnelle, il s'assure de l'adéquation du ou des contenus de la prestation aux exigences de la certification visée.",
      "Démontrer la capacité à préparer à la certification visée, y compris en tant qu'organisme habilité.", ["decorticage", "programmes"]],
    [8, 2, "tous", "Le prestataire détermine les procédures de positionnement et d'évaluation des acquis à l'entrée de la prestation.", "", ["positionnement"]],
    [9, 3, "tous", "Le prestataire informe les publics bénéficiaires des conditions de déroulement de la prestation.", "", ["convocation", "reglement", "site_accueil"]],
    [10, 3, "tous", "Le prestataire met en œuvre et adapte la prestation, l'accompagnement et le suivi aux publics bénéficiaires.", "", ["seances", "handicap", "positionnement"]],
    [11, 3, "tous", "Le prestataire évalue l'atteinte par les publics bénéficiaires des objectifs de la prestation.", "", ["evaluation", "attestation", "realisation"]],
    [12, 3, "tous", "Le prestataire décrit et met en œuvre les mesures pour favoriser l'engagement des bénéficiaires et prévenir les ruptures de parcours.",
      "Renforcé : mesures pour prévenir les violences (dont sexistes et sexuelles), le harcèlement et les discriminations, et pour y réagir lorsqu'elles surviennent.", ["vss", "emargement", "reglement"]],
    [13, 3, "alternance", "Pour les formations en alternance, le prestataire, en lien avec l'entreprise, anticipe avec l'apprenant les missions confiées, à court, moyen et long terme, et assure la coordination et la progressivité des apprentissages réalisés en centre de formation et en entreprise.", "", ["tripartite"]],
    [14, 3, "cfa", "Le prestataire met en œuvre un accompagnement socio-professionnel, éducatif et relatif à l'exercice de la citoyenneté.",
      "Procédure de traitement sans délai des ruptures liées à des violences ou discriminations subies par l'apprenti.", ["vss", "preuves_cfa"]],
    [15, 3, "cfa", "Le prestataire informe les apprentis de leurs droits et devoirs en tant qu'apprentis et salariés ainsi que des règles applicables en matière de santé et de sécurité en milieu professionnel.",
      "Information des apprentis sur les dispositifs de prévention et de signalement des violences, du harcèlement et des discriminations.", ["vss", "preuves_cfa"]],
    [16, 3, "certif", "Lorsque le prestataire met en œuvre des formations conduisant à une certification professionnelle, il s'assure que les conditions de présentation des bénéficiaires à la certification respectent les exigences formelles de l'autorité de certification.", "", ["decorticage", "reglement"]],
    [17, 4, "tous", "Le prestataire met à disposition ou s'assure de la mise à disposition des moyens humains et techniques adaptés et d'un environnement approprié (conditions, locaux, équipements, plateaux techniques…).", "", ["moyens", "site_accueil"]],
    [18, 4, "tous", "Le prestataire mobilise et coordonne les différents intervenants internes et/ou externes (pédagogiques, administratifs, logistiques, commerciaux…).", "", ["coordination", "soustraitance"]],
    [19, 4, "tous", "Le prestataire met à disposition du bénéficiaire des ressources pédagogiques et permet à celui-ci de se les approprier.",
      "Suivi de l'effectivité des séquences à distance (preuve de connexion ou de réalisation) ; seuil relatif au référent pédagogique renvoyé à un arrêté.", ["seances", "distanciel"]],
    [20, 4, "cfa", "Le prestataire dispose d'un personnel dédié à l'appui à la mobilité nationale et internationale, d'un référent handicap et d'un conseil de perfectionnement.",
      "Seuil relatif aux intervenants permanents renvoyé à un arrêté.", ["handicap", "preuves_cfa"]],
    [21, 5, "tous", "Le prestataire détermine, mobilise et évalue les compétences des différents intervenants internes et/ou externes, adaptées aux prestations.", "", ["cv", "soustraitance", "charte_ia"]],
    [22, 5, "tous", "Le prestataire entretient et développe les compétences de ses salariés, adaptées aux prestations qu'il délivre.", "", ["plan_competences", "charte_ia"]],
    [23, 6, "tous", "Le prestataire réalise une veille légale et réglementaire sur le champ de la formation professionnelle et en exploite les enseignements.", "", ["registre_veille"]],
    [24, 6, "tous", "Le prestataire réalise une veille sur les évolutions des compétences, des métiers et des emplois dans ses secteurs d'intervention et en exploite les enseignements.", "", ["registre_veille"]],
    [25, 6, "tous", "Le prestataire réalise une veille sur les innovations pédagogiques et technologiques permettant une évolution de ses prestations et en exploite les enseignements.", "", ["registre_veille", "charte_ia"]],
    [26, 6, "tous", "Le prestataire mobilise les expertises, outils et réseaux nécessaires pour accueillir, accompagner/former ou orienter les publics en situation de handicap.", "", ["handicap", "partenaires_handicap"]],
    [27, 6, "tous", "Lorsque le prestataire fait appel à la sous-traitance ou au portage salarial, il s'assure du respect de la conformité au présent référentiel.",
      "La vérification de conformité du sous-traitant (et du salarié porté) doit être tracée dans le contrat de sous-traitance lui-même.", ["soustraitance", "registre_traitements"]],
    [28, 6, "alternance", "Lorsque les prestations dispensées au bénéficiaire comprennent des périodes de formation en situation de travail, le prestataire mobilise son réseau de partenaires socio-économiques pour co-construire l'ingénierie de formation et favoriser l'accueil en entreprise.", "", ["partenaires_reseau"]],
    [29, 6, "cfa", "Le prestataire développe des actions qui concourent à l'insertion professionnelle ou la poursuite d'étude par la voie de l'apprentissage ou par toute autre voie permettant de développer leurs connaissances et leurs compétences.", "", ["preuves_cfa"]],
    [30, 7, "tous", "Le prestataire recueille les appréciations des parties prenantes : bénéficiaires, financeurs, équipes pédagogiques et entreprises concernées.",
      "Listé parmi les indicateurs modifiés par certaines sources : exigence nouvelle non identifiée, à vérifier sur le texte officiel.", ["chaud", "froid"]],
    [31, 7, "tous", "Le prestataire met en œuvre des modalités de traitement des difficultés rencontrées par les parties prenantes, des réclamations exprimées par ces dernières, des aléas survenus en cours de prestation.",
      "Listé parmi les indicateurs modifiés par certaines sources (lien avec le traitement des violences et discriminations) : à vérifier sur le texte officiel.", ["reclamations_proc", "registre_reclamations", "vss"]],
    [32, 7, "tous", "Le prestataire met en œuvre des mesures d'amélioration à partir de l'analyse des appréciations et des réclamations.",
      "Renforcé : l'amélioration continue intègre une analyse des risques susceptibles d'altérer la qualité des actions, avec une boucle documentée et mesurée.", ["registre_risques", "plan_amelioration", "bilan"]],
    [33, 7, "cfa", "NOUVEL INDICATEUR (V10) — Actions de formation par apprentissage : évaluation des enseignements par les apprentis, distincte de l'enquête générale de satisfaction.",
      "Créé par le décret 2026-728. Libellé exact à reprendre de l'annexe publiée sur Légifrance.", ["eval_enseignements", "preuves_cfa"]],
  ].map(([n, critere, portee, libelle, v10, docs]) => ({ n, critere, portee, libelle, v10, docs }));
  const CRITERES = { 1: "Information du public", 2: "Objectifs et adaptation", 3: "Accueil, suivi, évaluation", 4: "Moyens pédagogiques",
    5: "Qualification des personnels", 6: "Environnement professionnel", 7: "Appréciations et réclamations" };
  const PORTEES = { tous: "Tous les organismes", certif: "Si action certifiante", alternance: "Si alternance / situation de travail", cfa: "Si apprentissage (CFA)" };

  /* Bibliothèque documentaire : chaque document exigé (ou utile) pour l'audit, déposé UNE fois puis réutilisé
   * partout (actions, dossier d'audit). ref = référence de votre socle documentaire (table « DOCUMENTS OFFICIELS YEBA »).
   * source : "app" = produit par le logiciel ; "modele" = modèle générable ici ; "depot" = votre version à déposer.
   * statut initial et reste à faire : relevés dans votre base Airtable le 28/10/2026. */
  const BIBLIOTHEQUE = [
    ["mentions", "YEBA-DOC-01", "Mentions légales", "depot", "incomplet", "Forme juridique, RCS ou RNE, NAF, n° TVA, hébergeur, médiateur de la consommation."],
    ["confidentialite", "YEBA-DOC-02", "Politique de confidentialité et de protection des données", "depot", "en_vigueur", "Documenter les transferts hors UE (Airtable, Google)."],
    ["cgv", "YEBA-DOC-03", "Conditions générales de vente et de prestation", "depot", "incomplet", "Médiateur de la consommation, forfait déplacement, validation de la grille tarifaire."],
    ["reglement", "YEBA-DOC-04", "Règlement intérieur applicable aux stagiaires", "depot", "en_vigueur", "Faire signer l'accusé de réception avant l'entrée en formation."],
    ["convention", "YEBA-DOC-05", "Convention de formation (modèle entreprise)", "depot", "incomplet", "Encart assurance (art. 10) et attestation en annexe 4."],
    ["contrat", "YEBA-DOC-06", "Contrat de formation (modèle particulier)", "depot", "incomplet", "Bloquant tant qu'aucun médiateur de la consommation n'est désigné."],
    ["soustraitance", "YEBA-DOC-07", "Convention de sous-traitance (volets A et B), avec clause de conformité RNQ", "depot", "en_vigueur", "V10 ind. 27 : tracer la vérification de conformité DANS le contrat."],
    ["handicap", "YEBA-DOC-08", "Politique handicap et accessibilité (référent : Aurélien LUMEKA)", "depot", "en_vigueur", "Formaliser un contact avec l'Agefiph Océan Indien ou Ressource Handicap Formation."],
    ["reclamations_proc", "YEBA-DOC-09", "Procédure de traitement des réclamations, difficultés et aléas", "depot", "incomplet", "Médiateur de la consommation à désigner."],
    ["charte_qualite", "YEBA-DOC-10", "Charte qualité et engagements de service", "depot", "a_valider", ""],
    ["charte_ia", "YEBA-DOC-11", "Charte d'usage de l'intelligence artificielle", "depot", "en_vigueur", "Signature par chaque formateur sous-traitant ; révision semestrielle (10/03/2027)."],
    ["tarifs", "YEBA-DOC-12", "Politique tarifaire", "depot", "en_vigueur", "Tarif conseil et audit à trancher."],
    ["financements", "YEBA-DOC-13", "Notice des financements mobilisables", "depot", "en_vigueur", "Jamais « éligible CPF » sans code RNCP/RS."],
    ["vss", "YEBA-DOC-14", "Procédure de prévention et de traitement des violences, du harcèlement et des discriminations", "depot", "a_valider", "V10 ind. 12 : registre des signalements à accès restreint, voie de recours externe."],
    ["site_accueil", "YEBA-DOC-15", "Fiche de reconnaissance d'un site d'accueil (hôtel, locaux tiers)", "depot", "en_vigueur", ""],
    ["registre_traitements", "YEBA-DOC-16", "Registre des activités de traitement (RGPD art. 30)", "depot", "incomplet", "Outils, hébergement, contrats art. 28."],
    ["attestation", "YEBA-DOC-17", "Attestation de fin de formation (modèle)", "app", "en_vigueur", ""],
    ["realisation", "YEBA-DOC-18", "Certificat de réalisation (modèle)", "app", "en_vigueur", ""],
    ["programmes", "", "Programmes de formation datés (catalogue)", "app", "", "Produits par le logiciel pour chaque formation et chaque action."],
    ["methode_resultats", "", "Indicateurs de résultats ET méthode de calcul (V10 ind. 2)", "modele", "", "Généré à partir de vos actions terminées."],
    ["registre_risques", "", "Registre des risques qualité (V10 ind. 32)", "modele", "", "Probabilité, impact, mesure, responsable, date de revue."],
    ["plan_competences", "", "Plan de développement des compétences du dirigeant-formateur", "modele", "", "Pré-rempli avec vos certifications."],
    ["moyens", "", "Fiche des moyens pédagogiques et techniques", "modele", "", ""],
    ["coordination", "", "Organisation et coordination des intervenants", "modele", "", ""],
    ["registre_veille", "", "Registre de veille (légale, métiers, pédagogique)", "app", "", "Alimenté dans l'écran Qualiopi."],
    ["registre_reclamations", "", "Registre des réclamations", "app", "", "Alimenté dans l'écran Qualiopi."],
    ["plan_amelioration", "", "Plan d'amélioration continue", "app", "", "Alimenté dans l'écran Qualiopi."],
    ["cv", "", "CV, diplômes et certifications des intervenants", "depot", "", "Google AI Specialist, Google Professional AI, SecNumacadémie ANSSI, MOOC CNIL, référent handicap…"],
    ["partenaires_handicap", "", "Contacts et conventions handicap (Agefiph, RHF, Cap emploi, MDPH)", "depot", "", ""],
    ["partenaires_reseau", "", "Conventions avec les partenaires socio-économiques (entreprises d'accueil)", "depot", "", ""],
    ["distanciel", "", "Preuves de connexion ou de réalisation des séquences à distance", "depot", "", "Uniquement si vous formez à distance."],
    ["decorticage", "", "Décorticage du référentiel de certification (couverture des critères)", "app", "", "Produit par le logiciel pour chaque titre préparé."],
    ["besoin", "", "Analyses du besoin", "app", "", ""], ["positionnement", "", "Tests de positionnement", "app", "", ""],
    ["convocation", "", "Convocations et livret d'accueil", "app", "", ""], ["emargement", "", "Feuilles d'émargement", "app", "", ""],
    ["seances", "", "Fiches de séance et supports", "app", "", ""], ["evaluation", "", "Évaluations des acquis (grilles, quiz)", "app", "", ""],
    ["chaud", "", "Questionnaires de satisfaction à chaud", "app", "", ""], ["froid", "", "Questionnaires à froid", "app", "", ""],
    ["bilan", "", "Bilans d'action", "app", "", ""], ["tripartite", "", "Entretiens tripartites (alternance)", "app", "", ""],
    ["eval_enseignements", "", "Évaluation des enseignements par les apprentis (V10 ind. 33)", "modele", "", "Fournie au CFA donneur d'ordre."],
    ["preuves_cfa", "", "Preuves remises au CFA donneur d'ordre (indicateurs CFA)", "depot", "", "En sous-traitance, ces indicateurs relèvent du CFA : vous lui fournissez les preuves."],
  ].map(([id, ref, titre, source, statut, reste]) => ({ id, ref, titre, source, statut, reste }));
  const STATUTS_DOC = { en_vigueur: "En vigueur", a_valider: "À valider", incomplet: "Incomplet", "": "À produire" };

  /* Canaux par lesquels l'argent arrive : sert au rapprochement bancaire (mots repérés dans le libellé du virement)
   * et au BPF (origine des produits, cadre C). Les mots-clés sont des indices, jamais une preuve : vous confirmez. */
  const CANAUX = {
    entreprise: { lib: "Entreprise (paiement direct)", origine: "entreprises", mots: [] },
    opco: { lib: "OPCO", origine: "opco_autres", mots: ["opco", "akto", "atlas", "constructys", "uniformation", "ocapiat", "afdas", "opcommerce", "opco ep", "opco 2i", "sante", "mobilites", "cohesion sociale"] },
    cpf: { lib: "CPF (Caisse des Dépôts)", origine: "cpf", mots: ["caisse des depots", "cdc", "mon compte formation", "moncompteformation"] },
    france_travail: { lib: "France Travail", origine: "pouvoirs_publics", mots: ["france travail", "pole emploi", "drfip"] },
    region: { lib: "Région Réunion", origine: "pouvoirs_publics", mots: ["region", "conseil regional", "drfip"] },
    etat: { lib: "État et autres fonds publics", origine: "pouvoirs_publics", mots: ["tresor public", "drfip", "dgfip", "deets"] },
    agefiph: { lib: "Agefiph", origine: "autres", mots: ["agefiph"] },
    of: { lib: "Autre organisme de formation (sous-traitance)", origine: "of", mots: ["formation", "institut", "cfa", "ecole"] },
    particulier: { lib: "Particulier", origine: "particuliers", mots: [] },
    autre: { lib: "Autre", origine: "autres", mots: [] },
  };

  // Documents d'une action de formation : remplis automatiquement à partir des données.
  // quand : relatif au début (debut), à la fin (fin) ; jours négatifs = avant.
  const DOCS = [
    { id: "besoin", titre: "Analyse du besoin", ind: [4], quand: ["debut", -21] },
    { id: "programme", titre: "Programme de formation", ind: [1, 5, 6, 7], quand: ["debut", -21] },
    { id: "convention", titre: "Convention de formation (entreprise / financeur)", ind: [9], quand: ["debut", -15], si: (a) => a.type !== "individuel" },
    { id: "contrat", titre: "Contrat de formation (personne physique)", ind: [9], quand: ["debut", -15], si: (a) => a.type === "individuel" },
    { id: "convocation", titre: "Convocation et livret d'accueil", ind: [9, 19], quand: ["debut", -7] },
    { id: "reglement", titre: "Règlement intérieur", ind: [9], quand: ["debut", -7] },
    { id: "positionnement", titre: "Test de positionnement à l'entrée", ind: [8], quand: ["debut", 0] },
    { id: "emargement", titre: "Feuilles d'émargement (par demi-journée)", ind: [11, 12], quand: ["debut", 0] },
    { id: "seances", titre: "Fiches de séance et supports (preuves de déroulé)", ind: [5, 6, 11, 19], quand: ["debut", 0] },
    { id: "evaluation", titre: "Évaluation des acquis (grille critériée, quiz)", ind: [11], quand: ["fin", 0] },
    { id: "chaud", titre: "Questionnaire de satisfaction à chaud", ind: [30], quand: ["fin", 0] },
    { id: "attestation", titre: "Attestation de fin de formation", ind: [11], quand: ["fin", 2] },
    { id: "realisation", titre: "Certificat de réalisation", ind: [11], quand: ["fin", 2] },
    { id: "facture", titre: "Facture", ind: [], quand: ["fin", 3] },
    { id: "froid", titre: "Questionnaire à froid (J+90)", ind: [2, 30], quand: ["fin", 90] },
    { id: "bilan", titre: "Bilan de l'action et pistes d'amélioration", ind: [32], quand: ["fin", 15] },
    { id: "tripartite", titre: "Entretien tripartite apprenti / tuteur / formateur", ind: [13, 15], quand: ["debut", 45], si: (a) => a.type === "apprentissage" },
    { id: "eval_enseignements", titre: "Évaluation des enseignements par les apprentis (Qualiopi V10, ind. 33)", ind: [33], quand: ["fin", 0], si: (a) => a.type === "apprentissage" },
  ];

  const TYPES_ACTION = {
    continue: "Formation continue (entreprise, OPCO)", inter: "Inter-entreprises", intra: "Intra-entreprise",
    apprentissage: "Apprentissage (pour un CFA ou en propre)", soustraitance: "Sous-traitance pour un autre organisme",
    individuel: "Particulier (CPF, autofinancement)", demandeurs: "Demandeurs d'emploi (France Travail, Région)",
  };
  // Origine des produits, alignée sur le cadre C du Bilan pédagogique et financier (à vérifier sur Mon Activité Formation)
  const ORIGINES = {
    entreprises: "Entreprises (plan de développement des compétences)", opco_appr: "OPCO — contrats d'apprentissage",
    opco_pro: "OPCO — contrats de professionnalisation", opco_autres: "OPCO — autres financements", cpf: "Caisse des dépôts (CPF)",
    pouvoirs_publics: "Pouvoirs publics (Région, État, France Travail)", particuliers: "Particuliers (autofinancement)",
    of: "Autres organismes de formation (sous-traitance)", autres: "Autres produits",
  };
  const CATEGORIES_DEPENSE = ["Déplacements", "Location de salle", "Matériel et supports", "Logiciels et abonnements", "Assurance", "Honoraires (comptable, avocat)",
    "Certification Qualiopi", "Sous-traitance", "Cotisations sociales", "Impôts et taxes", "Banque", "Télécom", "Formation du formateur", "Autre"];
  const TYPES_PARTENAIRE = { entreprise: "Entreprise d'accueil", prescripteur: "Prescripteur (France Travail, Mission Locale, Cap Emploi…)",
    of: "Organisme de formation donneur d'ordre", opco: "OPCO / financeur", institution: "Institution (Région, DREETS, AGEFIPH…)", autre: "Autre" };

  function initiales() {
    return {
      version: 2, cree: new Date().toISOString(),
      identite: identiteYeba(),
      charte: charteYeba(),
      formations: [], actions: [], ecritures: [], partenaires: [], relances: [],
      attendus: [], mouvements: [], alias: {}, bibliotheque: {},
      qualiopi: { ajouts: [], suivi: {} }, reclamations: [], ameliorations: [], veille: [], risques: [],
      tresorerie: { solde_initial: 0, date_solde: new Date().toISOString().slice(0, 10), seuil_alerte: 1500 },
    };
  }

  // Identité relevée dans la base Airtable (CONFIG SYSTEME) et l'adresse communiquée le 28/10/2026
  function identiteYeba() {
    return { nom: "YEBA FORMATIONS", dirigeant: "Aurélien LUMEKA", siret: "814 622 262 00032", nda: "04973676397",
      qualiopi: "25FOR02027.1", certificateur: "Qualitia (accrédité COFRAC)", qualiopi_validite: "2027-02-16",
      adresse: "Immeuble Rodrigues 2, 7 rue Henri Cornu, Technor", code_postal: "97490", ville: "Saint-Denis (La Réunion)",
      telephone: "0693 32 24 45", email: "yebaformations@gmail.com", site: "www.yebaformations.re",
      referent_handicap: "Aurélien LUMEKA", delai_acces: "15 jours ouvrés minimum", horaires: "08h30–12h00 / 13h00–16h30 (7 heures)",
      audit_debut: "2027-02-01", audit_fin: "2027-12-31", mentions_qualiopi: ["Actions de formation"], iban: "", bic: "",
      // TVA : franchise en base (art. 293 B du CGI) jusqu'au 31/01/2027, TVA à 8,5 % (La Réunion) à partir du 01/02/2027
      tva_debut: "2027-02-01", taux_tva: 8.5, attestation_3511: false, tva_intra: "" };
  }
  // Charte graphique YEBA FORMATIONS 2026 : bleu #1B3A6B, or #C9AB4C, noir #121212, blanc ; Montserrat (titres), Inter (texte)
  function charteYeba() {
    return { couleur_primaire: "1B3A6B", couleur_secondaire: "C9AB4C", couleur_claire: "EEF2F8", couleur_texte: "121212",
      police: "Inter", police_titres: "Montserrat", taille_texte: 14, taille_titre: 24, logo: G.LOGO_YEBA || "", couleurs_validees: true };
  }
  // Mise à niveau d'un coffre créé avec une version antérieure : on complète, on n'écrase jamais une saisie
  function migrer(d) {
    const id = identiteYeba(), ch = charteYeba();
    d.identite = d.identite || {};
    for (const [k, v] of Object.entries(id)) if (d.identite[k] === undefined || d.identite[k] === "") d.identite[k] = v;
    if (!d.identite.adresse || /Françoise Châtelain/i.test(d.identite.adresse)) Object.assign(d.identite, { adresse: id.adresse, code_postal: id.code_postal, ville: id.ville });
    d.charte = d.charte || {};
    if (!d.charte.couleurs_validees || d.charte.couleur_primaire === "1F3A5F") Object.assign(d.charte, ch, { logo: d.charte.logo || ch.logo });
    for (const [k, v] of Object.entries(ch)) if (d.charte[k] === undefined) d.charte[k] = v;
    for (const k of ["attendus", "mouvements", "formations", "actions", "ecritures", "partenaires", "reclamations", "ameliorations", "veille", "risques"]) d[k] = d[k] || [];
    d.alias = d.alias || {}; d.bibliotheque = d.bibliotheque || {}; d.qualiopi = d.qualiopi || { ajouts: [], suivi: {} };
    // l'ancien « indicateur 33 ajouté à la main » devient inutile : le V10 l'intègre
    d.qualiopi.ajouts = (d.qualiopi.ajouts || []).filter((x) => x.n !== 33);
    d.version = 2;
    return d;
  }

  Object.assign(P, { QUALIOPI, CRITERES, PORTEES, BIBLIOTHEQUE, STATUTS_DOC, CANAUX, DOCS, TYPES_ACTION, ORIGINES, CATEGORIES_DEPENSE, TYPES_PARTENAIRE, initiales, migrer, identiteYeba });
})(typeof window !== "undefined" ? window : globalThis);

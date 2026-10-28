/* Données de référence : Qualiopi, documents d'une action, structure du coffre.
 * Source Qualiopi : Référentiel national qualité (décret n° 2019-564 du 6 juin 2019,
 * arrêté du 6 juin 2019) et son guide de lecture — 7 critères, 32 indicateurs.
 * Si votre organisme certificateur annonce un référentiel modifié (ex. 33 indicateurs),
 * ajoutez l'indicateur dans l'écran Qualiopi : la liste est extensible. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});

  // portée : "tous", "certif" (actions certifiantes), "alternance" (CFA / apprentissage)
  const QUALIOPI = [
    [1, 1, "tous", "Information du public sur les prestations : prérequis, objectifs, durée, modalités et délais d'accès, tarifs, contacts, méthodes, évaluation, accessibilité handicap"],
    [2, 1, "tous", "Indicateurs de résultats adaptés à la nature des prestations et des publics"],
    [3, 1, "certif", "Taux d'obtention des certifications, poursuites d'études, insertion professionnelle"],
    [4, 2, "tous", "Analyse du besoin du bénéficiaire en lien avec l'entreprise ou le financeur"],
    [5, 2, "tous", "Objectifs opérationnels et évaluables de la prestation"],
    [6, 2, "tous", "Contenus et modalités de mise en œuvre adaptés aux objectifs et aux publics"],
    [7, 2, "certif", "Adéquation du contenu de la prestation aux exigences de la certification"],
    [8, 2, "tous", "Positionnement et évaluation des acquis à l'entrée"],
    [9, 3, "tous", "Information des publics sur les conditions de déroulement de la prestation"],
    [10, 3, "tous", "Adaptation de la prestation, accompagnement et suivi des bénéficiaires"],
    [11, 3, "tous", "Évaluation de l'atteinte des objectifs par les bénéficiaires"],
    [12, 3, "tous", "Engagement des bénéficiaires et prévention des ruptures de parcours"],
    [13, 3, "alternance", "Alternance : coordination avec l'employeur (missions, objectifs, suivi)"],
    [14, 3, "alternance", "Alternance : exercice de la citoyenneté et accompagnement socio-professionnel"],
    [15, 3, "alternance", "Alternance : information des apprentis sur leurs droits et devoirs, santé et sécurité"],
    [16, 3, "certif", "Information sur les conditions de présentation aux évaluations de la certification"],
    [17, 4, "tous", "Moyens humains et techniques adaptés, environnement approprié"],
    [18, 4, "tous", "Coordination des acteurs internes et externes"],
    [19, 4, "tous", "Ressources pédagogiques mises à disposition des bénéficiaires"],
    [20, 4, "alternance", "Alternance : référents handicap et mobilité, conseil de perfectionnement"],
    [21, 5, "tous", "Compétences des intervenants (pédagogiques, techniques…)"],
    [22, 5, "tous", "Développement et entretien des compétences des salariés et intervenants"],
    [23, 6, "tous", "Veille légale et réglementaire et exploitation des enseignements"],
    [24, 6, "tous", "Veille sur les compétences, métiers et emplois"],
    [25, 6, "tous", "Veille sur les innovations pédagogiques et technologiques"],
    [26, 6, "tous", "Mobilisation d'expertises et d'un réseau de partenaires pour le handicap"],
    [27, 6, "tous", "Sous-traitance ou portage salarial : respect du référentiel par le sous-traitant"],
    [28, 6, "alternance", "Formations en situation de travail : réseau de partenaires socio-économiques"],
    [29, 6, "alternance", "Alternance : insertion professionnelle ou poursuite d'études"],
    [30, 7, "tous", "Recueil des appréciations des parties prenantes"],
    [31, 7, "tous", "Traitement des difficultés, réclamations et aléas"],
    [32, 7, "tous", "Mesures d'amélioration à partir des appréciations et réclamations"],
  ].map(([n, critere, portee, libelle]) => ({ n, critere, portee, libelle }));
  const CRITERES = { 1: "Information du public", 2: "Objectifs et adaptation", 3: "Accueil, suivi, évaluation", 4: "Moyens pédagogiques",
    5: "Qualification des personnels", 6: "Environnement professionnel", 7: "Appréciations et réclamations" };

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
      version: 1, cree: new Date().toISOString(),
      identite: { nom: "YEBA FORMATIONS", dirigeant: "Aurélien LUMEKA", siret: "814 622 262 00032", nda: "04973676397",
        qualiopi: "25FOR02027.1", adresse: "", ville: "", telephone: "", email: "", site: "www.yebaformations.re",
        tva: "", referent_handicap: "Aurélien LUMEKA", audit_debut: "2027-02-01", audit_fin: "2027-12-31",
        mentions_qualiopi: ["Actions de formation"], iban: "" },
      charte: { couleur_primaire: "1F3A5F", couleur_secondaire: "E07A1F", couleur_claire: "EEF3F8", couleur_texte: "1A1A1A",
        police: "Arial", taille_texte: 14, taille_titre: 22, logo: "", couleurs_validees: false },
      formations: [], actions: [], ecritures: [], partenaires: [], relances: [],
      qualiopi: { ajouts: [], suivi: {} }, reclamations: [], ameliorations: [], veille: [],
      tresorerie: { solde_initial: 0, date_solde: new Date().toISOString().slice(0, 10), seuil_alerte: 1500 },
    };
  }

  Object.assign(P, { QUALIOPI, CRITERES, DOCS, TYPES_ACTION, ORIGINES, CATEGORIES_DEPENSE, TYPES_PARTENAIRE, initiales });
})(typeof window !== "undefined" ? window : globalThis);

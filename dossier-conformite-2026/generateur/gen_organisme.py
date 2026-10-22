"""Documents de l'organisme : présentation du centre, matrice Qualiopi, checklist centre d'examen."""
from calendrier import PROMOTIONS, fmt_court, planifier, session_examen
from lib import HORAIRES, ORGANISME, Doc
from titres import MEM, RPMS, heures_centre

O, H = ORGANISME, HORAIRES
DOSSIER = "06_Organisme"


def presentation():
    d = Doc("Présentation du centre de formation", "Dossier de référencement pour les financeurs et prescripteurs", code="PRES-01", couverture=True)
    d.h1("1. Identité")
    d.tableau(["Rubrique", "Information"], [
        ["Raison sociale", f"{O['nom']} — {O['forme']}"],
        ["SIRET", O["siret"]],
        ["Déclaration d'activité", f"NDA {O['nda']} — préfet de région de La Réunion"],
        ["Certification qualité", f"Qualiopi n° {O['qualiopi']} ({O['certificateur']}), {O['qualiopi_validite']} — catégories : {O['qualiopi_categories']}"],
        ["Dirigeant", f"{O['dirigeant']}, fondateur, directeur et formateur"],
        ["Création", "Avril 2021"],
        ["Lieu de formation", O["lieu"]],
        ["Siège", O["siege"]],
        ["Régime de TVA", O["tva"]],
        ["Assurance", O["assurance"]],
        ["Contact", f"{O['tel']} — {O['mail']}"],
    ], [5, 12])
    d.h1("2. Notre mission")
    d.p("Former des professionnels réunionnais opérationnels en vente, en management et dans l'usage responsable de l'intelligence artificielle, "
        "avec un accompagnement individuel qui réduit l'abandon en cours de parcours.")
    d.h1("3. Le dirigeant et ses certifications")
    d.puces(["Formateur en vente, management et compétences comportementales depuis 2021, dans plusieurs centres de formation",
             "Google AI Specialist ; Google Professional AI", "Référent handicap en organisme de formation",
             "SecNumacadémie de l'ANSSI (cybersécurité)", "MOOC de la CNIL (RGPD)"])
    d.h1("4. Notre offre certifiante")
    d.tableau(["Titre professionnel", "Niveau", "Durée", "Prochaine promotion"], [
        [f"{t['court']} ({t['rncp']})", "5", f"{heures_centre(t)} h + {t['pae']} h en entreprise",
         f"{fmt_court(planifier(c)[0][0][0])} → {fmt_court(planifier(c)[0][-1][0])}"]
        for c, t in (("MEM", MEM), ("RPMS", RPMS))
    ], [6.5, 1.8, 4.2, 4.5])
    d.p("Également : formations courtes en intra et inter-entreprises — intelligence artificielle, RGPD et IA Act, vente, management.")
    d.h1("5. Nos engagements")
    d.puces([
        "Recrutement sécurisé : information collective, positionnement, entretien individuel.",
        "Prévention du décrochage : réaction le jour même à une absence, entretiens réguliers, lien avec le prescripteur.",
        "Alternance courte centre / entreprise et productions d'examen préparées dès la période en entreprise.",
        "Accessibilité : référent handicap certifié, supports en gros caractères et contrastés, aménagements d'examen.",
        "Données personnelles : outils hébergés dans l'Union européenne, aucune décision prise par une IA.",
        "Transparence : résultats (satisfaction, réussite, insertion) publiés après chaque session.",
    ])
    d.h1("6. Organisation pratique")
    d.tableau(["", ""], [["Horaires", H["journee"]], ["Pauses", H["pauses"]], ["Déjeuner", H["dejeuner"]],
                         ["Lieu", O["lieu"]], ["Équipements", O["lieu_equipement"].capitalize()]], [4, 13])
    d.h1("7. Pièces administratives disponibles sur demande")
    d.puces(["Avis de situation INSEE / extrait RNE", "Récépissé de déclaration d'activité", "Certificat Qualiopi",
             "Attestation de vigilance URSSAF", "Attestation d'assurance", "Programmes, livret d'accueil, règlement intérieur, CGV"])
    d.p(O["nda_mention"], italic=True)
    return d.save(f"{DOSSIER}/PRES-01_Presentation_du_centre.docx")


# Indicateurs du référentiel national qualité : (n°, libellé abrégé, applicabilité, preuves YEBA)
INDICATEURS = [
    (1, "Information du public sur les prestations, délais d'accès et résultats", "Oui", "PRG-MEM, PRG-RPMS, PRES-01, CGV YEBA-DOC-03, site internet"),
    (2, "Indicateurs de résultats publiés", "Oui", "PIL-03 (indicateurs), page résultats du site"),
    (3, "Taux d'obtention des certifications", "Oui", "PIL-03, PRG (résultats nationaux puis YEBA)"),
    (4, "Analyse du besoin du bénéficiaire", "Oui", "FI-01, POS-02 (compte rendu d'entretien)"),
    (5, "Objectifs opérationnels et évaluables", "Oui", "REAC-MEM, REAC-RPMS (objectifs par séquence)"),
    (6, "Contenus et modalités adaptés aux objectifs", "Oui", "DP-MEM, DP-RPMS"),
    (7, "Adéquation du contenu aux exigences de la certification", "Oui", "REAC-MEM, REAC-RPMS (correspondance CP / modules / épreuves)"),
    (8, "Positionnement à l'entrée", "Oui", "POS-02"),
    (9, "Information sur les conditions de déroulement", "Oui", "LIV-MEM, LIV-RPMS, CONVOC-16, YEBA-DOC-04 et avenant RI-06"),
    (10, "Adaptation de la prestation, accompagnement et suivi", "Oui", "ABS-13, LIAI-17, bilan de mi-parcours (T6)"),
    (11, "Évaluation de l'atteinte des objectifs", "Oui", "Évaluations formatives (à concevoir avec les supports), épreuves blanches T5"),
    (12, "Engagement des bénéficiaires et prévention des abandons", "Oui", "ABS-13, PIL-03 (absences)"),
    (13, "Coordination centre / entreprise en alternance", "Oui (périodes en entreprise)", "GPE-MEM, GPE-RPMS, PAE-14"),
    (14, "Exercice de la citoyenneté (apprentis)", "Non (apprentis)", "—"),
    (15, "Droits et devoirs des apprentis", "Non (apprentis)", "—"),
    (16, "Conditions de présentation à la certification", "Oui", "PRG, LIV (épreuves et productions), AGR-03"),
    (17, "Moyens humains, techniques et locaux", "Oui", "PRES-01, fiche site tiers YEBA-DOC-15 remplie pour le Secrétariat Center"),
    (18, "Coordination des intervenants", "Oui", "Planning des intervenants, réunions pédagogiques (comptes rendus)"),
    (19, "Ressources pédagogiques mises à disposition", "Oui", "Supports de cours (à produire)"),
    (20, "Référents mobilité, handicap, conseil de perfectionnement (CFA)", "Non (apprentis)", "—"),
    (21, "Compétences des intervenants", "Oui", "CV, diplômes et certifications des formateurs"),
    (22, "Développement des compétences des intervenants", "Oui", "Plan de formation des formateurs, charte IA YEBA-DOC-11 signée"),
    (23, "Veille légale et réglementaire", "Oui", "Registre de veille (textes, arrêtés des titres)"),
    (24, "Veille sur les emplois, métiers et compétences", "Oui", "Registre de veille (REAC, données emploi)"),
    (25, "Veille sur les innovations pédagogiques et technologiques", "Oui", "Registre de veille (IA, outils)"),
    (26, "Accueil des personnes en situation de handicap", "Oui", "YEBA-DOC-08, HAND-12, convention ou contact Agefiph / RHF"),
    (27, "Respect du référentiel en cas de sous-traitance", "Si sous-traitance", "Convention de sous-traitance YEBA-DOC-07"),
    (28, "Mobilisation des acteurs du milieu professionnel (alternance)", "Oui (périodes en entreprise)", "Vivier d'entreprises d'accueil, GPE"),
    (29, "Insertion professionnelle (CFA)", "Non (apprentis)", "—"),
    (30, "Recueil des appréciations des parties prenantes", "Oui", "EVAL-10"),
    (31, "Traitement des réclamations et difficultés", "Oui", "YEBA-DOC-09, table ALERTES & TÂCHES"),
    (32, "Mesures d'amélioration continue", "Oui", "YEBA-DOC-09 (actions correctives), revue annuelle"),
]


def matrice_qualiopi():
    d = Doc("Matrice des preuves Qualiopi", "Quel document prouve quel indicateur", code="QUA-02", paysage=True)
    d.p(f"Certificat {O['qualiopi']}. Libellés abrégés : se référer au référentiel national qualité et à son guide de lecture pour la formulation exacte. "
        f"Périmètre : {O['qualiopi_categories']} ; validité {O['qualiopi_validite']}. "
        "Audit de surveillance à prévoir entre le 14e et le 22e mois, soit entre le 17/04/2027 et le 17/12/2027 [À VÉRIFIER avec Qualitia].")
    d.tableau(["N°", "Indicateur (libellé abrégé)", "Applicable", "Preuves dans le dossier", "Prête"],
              [[n, lib, app, preuve, "☐" if app != "Non (apprentis)" else "—"] for n, lib, app, preuve in INDICATEURS],
              [1.4, 9, 4.3, 9, 2])
    return d.save(f"{DOSSIER}/QUA-02_Matrice_preuves_Qualiopi.docx")


def checklist_examen():
    s_mem, _ = session_examen("MEM")
    d = Doc("Organiser la session d'examen", "Agrément de centre d'examen ou partenariat avec un centre agréé", code="AGR-03")
    d.h1("1. Les deux options")
    d.tableau(["Option", "Avantages", "Contraintes"], [
        ["A — Agrément DEETS de YEBA FORMATIONS", "Autonomie, image, maîtrise du calendrier, preuve pour le CPF",
         "Dossier à déposer au moins 7 mois avant la session ; agrément lié au titre, à une durée et à un site ; plateau technique ; responsable de session ; saisie dans CERES"],
        ["B — Partenariat avec un centre déjà agréé", "Démarrage plus rapide ; pas d'investissement d'examen",
         "Coût par candidat ; dépendance au calendrier du partenaire ; candidats examinés hors de vos locaux"],
    ], [4.5, 6, 6.5])
    d.p(f"Recommandation : option B pour la promotion MEM 1 (session vers le {fmt_court(s_mem)}), "
        "puis option A à partir de 2028 quand le matériel et les jurys seront en place.")
    d.h1("2. Exigences de la session MEM (référentiel d'évaluation v09)")
    d.cases([
        "Une salle pour l'étude de cas de 4 h : un poste informatique par candidat avec traitement de texte et tableur, et une imprimante.",
        "Un surveillant pendant l'étude de cas et pendant les 30 minutes de préparation de l'entretien technique.",
        "Une salle de jury équipée pour projeter les diaporamas (vérifiée avec chaque candidat avant la session).",
        "Présence du jury : 3 h 25 par candidat, plus au moins 1 h 30 par candidat pour la correction et la lecture des documents.",
        "Jury composé de professionnels du métier habilités par la DEETS.",
        "Preuve de la période en entreprise de chaque candidat, conservée dans son dossier.",
    ])
    d.h1("3. Exigences de la session RPMS")
    d.cases(["Une salle de jury avec vidéoprojecteur pour la présentation du projet (45 min par candidat).",
             "Dossier de projet imprimé remis au jury avant la présentation.",
             "[À VÉRIFIER : autres conditions dans le référentiel d'évaluation RPMS v08]"])
    d.h1("4. Pièces pour une demande d'agrément (option A)")
    d.cases([
        "Formulaire de la démarche en ligne « DEETS 974 — demande d'agrément pour organiser des sessions » (demarche.numerique.gouv.fr)",
        "Calendrier prévisionnel des sessions et nombre maximal de candidats",
        "Description d'une session type et du plateau technique",
        "Contrat de location ou attestation du bailleur pour la salle d'examen (Secrétariat Center), assurance des locaux",
        "Engagements du représentant légal",
        "[À VÉRIFIER : liste exacte des pièces sur la démarche en ligne de la DEETS 974]",
    ])
    d.h1("5. Pour une convention de partenariat (option B)")
    d.cases(["Identifier les centres agréés pour le MEM et le RPMS à La Réunion", "Comparer coût par candidat, dates et lieu",
             "Signer une convention précisant : dates, coût, transmission des dossiers, rôle de chaque partie, protection des données"])
    d.p("Le site certifié Qualiopi est le siège (9 rue Françoise Châtelain). La formation au Secrétariat Center est une salle louée : "
        "remplir la fiche site tiers YEBA-DOC-15 et informer Qualitia lors de l'audit de surveillance [À VÉRIFIER : besoin d'extension de périmètre de site pour un centre d'examen].")
    d.rgpd(["Les dossiers des candidats transmis au centre d'examen ou à la DEETS contiennent des données personnelles : transmission sécurisée et limitée au nécessaire."])
    return d.save(f"{DOSSIER}/AGR-03_Organiser_la_session_examen.docx")


SOCLE = [
    ("YEBA-DOC-02", "Politique de confidentialité", "En vigueur", "Remise à l'inscription ; annexe de la convention"),
    ("YEBA-DOC-03", "Conditions générales de vente", "Incomplet", "Annexe de la convention, avec les conditions particulières CP-05"),
    ("YEBA-DOC-04", "Règlement intérieur", "En vigueur", "Remis avant l'entrée, avec l'avenant RI-06 ; affiché dans la salle"),
    ("YEBA-DOC-05", "Convention de formation (formations courtes)", "Incomplet", "Remplacée par CONV-03 pour les parcours certifiants"),
    ("YEBA-DOC-06", "Contrat particulier (formations courtes)", "Incomplet", "Remplacé par CTR-04 pour les parcours certifiants"),
    ("YEBA-DOC-08", "Politique handicap et accessibilité", "En vigueur", "Remise à l'inscription ; complétée par HAND-12"),
    ("YEBA-DOC-09", "Procédure de réclamation", "Incomplet", "Remise à l'entrée ; annexe de la convention"),
    ("YEBA-DOC-11", "Charte d'usage de l'IA", "En vigueur", "Remise à l'entrée ; signée par les formateurs"),
    ("YEBA-DOC-14", "Procédure violences, harcèlement, discriminations", "À valider", "Citée dans SST-18 ; à valider avant la 1re promotion"),
    ("YEBA-DOC-15", "Fiche site d'accueil tiers", "En vigueur", "À remplir pour le Secrétariat Center avant la 1re session"),
    ("YEBA-DOC-16", "Registre des traitements", "Incomplet", "À compléter avec RGPD-01"),
    ("YEBA-DOC-17", "Attestation de fin de formation", "En vigueur", "Remise en fin de parcours (heures centre et entreprise, résultats par CCP)"),
    ("YEBA-DOC-18", "Certificat de réalisation", "En vigueur", "Remis au financeur"),
]

ECARTS = [
    ("Qualiopi — catégories", "Le bloc-marque de la charte et de tous les documents officiels indique « catégorie actions de formation »",
     "Le certificat couvre les 4 catégories : mettre à jour le bloc-marque (charte, DOC-02 à DOC-18, CONFIG SYSTÈME)"),
    ("Qualiopi — validité", "CONFIG SYSTÈME et DOC-10 indiquent une échéance au 16/02/2027",
     "Le certificat est valable jusqu'au 16/02/2029 ; audit de surveillance entre le 17/04/2027 et le 17/12/2027"),
    ("TVA", "DOC-05 et DOC-06 indiquent « exonération, art. 261-4-4° a du CGI »",
     "Remplacer par « TVA non applicable — article 293 B du CGI » (règle de CONFIG SYSTÈME et des CGV)"),
    ("Assurance", "DOC-05, article 10, garde des crochets [ASSUREUR]",
     "Reporter les données Hiscox (police HRCP300980) déjà présentes dans CONFIG SYSTÈME et les CGV"),
    ("Horaires", "Horaires standard 8 h 30 – 16 h 30 dans DOC-04, DOC-05, DOC-06",
     "Conserver pour les formations courtes ; les parcours certifiants suivent 8 h 00 – 16 h 00 (avenant RI-06)"),
    ("Délégués", "DOC-04, article 23 : « l'ensemble des formations du catalogue » dure moins de 500 heures",
     "Ajouter les titres professionnels (plus de 500 heures) à l'article 22, ou s'appuyer sur l'avenant RI-06"),
    ("Mention EI", "Le bloc-marque ne porte pas la mention « entrepreneur individuel »",
     "Ajouter « EI » ou « entrepreneur individuel » sur les factures, devis, site et courriels (loi n° 2022-172)"),
    ("Médiateur", "Aucun médiateur de la consommation désigné", "Adhérer avant toute signature d'un contrat avec un particulier"),
    ("CPF", "CONFIG SYSTÈME : « NON éligible — aucune certification RNCP/RS »",
     "Les titres MEM et RPMS sont des certifications RNCP : à mettre à jour dès leur publication sur Mon Compte Formation"),
    ("Logo", "La charte désigne le fichier « logo-yeba-sans-oeil.svg » (nœud de connexion) ; le dossier utilise le logo PNG transmis",
     "Confirmer le logo officiel ; un seul fichier pour tous les supports"),
    ("Assurance — IA", "Exclusion « intelligence artificielle » dans les conditions particulières Hiscox",
     "Obtenir du courtier une confirmation écrite que le module IA des parcours et le conseil sont couverts"),
]


def socle_et_ecarts():
    d = Doc("Socle documentaire et écarts à corriger", "Articulation avec les documents officiels YEBA et la base Airtable", code="SOC-04", paysage=True)
    d.p("La table « DOCUMENTS OFFICIELS YEBA » d'Airtable reste la source unique de vérité. Les documents du présent dossier la complètent "
        "pour les parcours certifiants, sans la dupliquer.")
    d.h1("1. Quel document officiel utiliser, et quand")
    d.tableau(["Référence", "Document", "Statut", "Usage dans les parcours certifiants"], [list(x) for x in SOCLE], [3.4, 7.5, 3, 11.8])
    d.h1("2. Écarts relevés le 22/10/2026")
    d.tableau(["Sujet", "Constat", "Correction proposée"], [list(x) for x in ECARTS], [3.8, 10, 11.9])
    return d.save(f"{DOSSIER}/SOC-04_Socle_documentaire_et_ecarts.docx")


def tout():
    return [presentation(), matrice_qualiopi(), checklist_examen(), socle_et_ecarts()]


if __name__ == "__main__":
    from lib import ERREURS_MISE_EN_PAGE
    for f in tout():
        print(f.name)
    print("\n".join(ERREURS_MISE_EN_PAGE) or "OK")

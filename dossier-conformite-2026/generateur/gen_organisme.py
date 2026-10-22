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
        ["Certification qualité", f"Qualiopi n° {O['qualiopi']} — catégorie : actions de formation [À VÉRIFIER : autres catégories]"],
        ["Dirigeant", f"{O['dirigeant']}, fondateur, directeur et formateur"],
        ["Création", "Avril 2021"],
        ["Lieu de formation", O["lieu"]],
        ["Siège", O["siege"]],
        ["Contact", f"{O['tel']} — {O['mail']} — {O['site']}"],
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
                         ["Lieu", O["lieu"]], ["Accessibilité", "[À VÉRIFIER : accès PMR du Secrétariat Center]"]], [4, 13])
    d.h1("7. Pièces administratives disponibles sur demande")
    d.puces(["Avis de situation INSEE / extrait RNE", "Récépissé de déclaration d'activité", "Certificat Qualiopi",
             "Attestation de vigilance URSSAF", "Attestation d'assurance", "Programmes, livret d'accueil, règlement intérieur, CGV"])
    d.p(O["nda_mention"], italic=True)
    return d.save(f"{DOSSIER}/PRES-01_Presentation_du_centre.docx")


# Indicateurs du référentiel national qualité : (n°, libellé abrégé, applicabilité, preuves YEBA)
INDICATEURS = [
    (1, "Information du public sur les prestations, délais d'accès et résultats", "Oui", "PRG-MEM, PRG-RPMS, PRES-01, site internet"),
    (2, "Indicateurs de résultats publiés", "Oui", "PIL-03 (indicateurs), page résultats du site"),
    (3, "Taux d'obtention des certifications", "Oui", "PIL-03, PRG (résultats nationaux puis YEBA)"),
    (4, "Analyse du besoin du bénéficiaire", "Oui", "FI-01, POS-02 (compte rendu d'entretien)"),
    (5, "Objectifs opérationnels et évaluables", "Oui", "REAC-MEM, REAC-RPMS (objectifs par séquence)"),
    (6, "Contenus et modalités adaptés aux objectifs", "Oui", "DP-MEM, DP-RPMS"),
    (7, "Adéquation du contenu aux exigences de la certification", "Oui", "REAC-MEM, REAC-RPMS (correspondance CP / modules / épreuves)"),
    (8, "Positionnement à l'entrée", "Oui", "POS-02"),
    (9, "Information sur les conditions de déroulement", "Oui", "LIV-MEM, LIV-RPMS, CONVOC-16, RI-06"),
    (10, "Adaptation de la prestation, accompagnement et suivi", "Oui", "ABS-13, LIAI-17, bilan de mi-parcours (T6)"),
    (11, "Évaluation de l'atteinte des objectifs", "Oui", "Évaluations formatives (à concevoir avec les supports), épreuves blanches T5"),
    (12, "Engagement des bénéficiaires et prévention des abandons", "Oui", "ABS-13, PIL-03 (absences)"),
    (13, "Coordination centre / entreprise en alternance", "Oui (périodes en entreprise)", "GPE-MEM, GPE-RPMS, PAE-14"),
    (14, "Exercice de la citoyenneté (apprentis)", "Non (CFA uniquement)", "—"),
    (15, "Droits et devoirs des apprentis", "Non (CFA uniquement)", "—"),
    (16, "Conditions de présentation à la certification", "Oui", "PRG, LIV (épreuves et productions), AGR-03"),
    (17, "Moyens humains, techniques et locaux", "Oui", "PRES-01, conditions de location du Secrétariat Center"),
    (18, "Coordination des intervenants", "Oui", "Planning des intervenants, réunions pédagogiques (comptes rendus)"),
    (19, "Ressources pédagogiques mises à disposition", "Oui", "Supports de cours (à produire)"),
    (20, "Référents mobilité, handicap, conseil de perfectionnement (CFA)", "Non (CFA uniquement)", "—"),
    (21, "Compétences des intervenants", "Oui", "CV, diplômes et certifications des formateurs"),
    (22, "Développement des compétences des intervenants", "Oui", "Plan de formation des formateurs, attestations"),
    (23, "Veille légale et réglementaire", "Oui", "Registre de veille (textes, arrêtés des titres)"),
    (24, "Veille sur les emplois, métiers et compétences", "Oui", "Registre de veille (REAC, données emploi)"),
    (25, "Veille sur les innovations pédagogiques et technologiques", "Oui", "Registre de veille (IA, outils)"),
    (26, "Accueil des personnes en situation de handicap", "Oui", "HAND-12, référent handicap certifié"),
    (27, "Respect du référentiel en cas de sous-traitance", "Si sous-traitance", "Contrats de sous-traitance, clause RGPD"),
    (28, "Mobilisation des acteurs du milieu professionnel (alternance)", "Oui (périodes en entreprise)", "Vivier d'entreprises d'accueil, GPE"),
    (29, "Insertion professionnelle (CFA)", "Non (CFA uniquement)", "—"),
    (30, "Recueil des appréciations des parties prenantes", "Oui", "EVAL-10"),
    (31, "Traitement des réclamations et difficultés", "Oui", "REC-11"),
    (32, "Mesures d'amélioration continue", "Oui", "REC-11 (registre), revue annuelle"),
]


def matrice_qualiopi():
    d = Doc("Matrice des preuves Qualiopi", "Quel document prouve quel indicateur", code="QUA-02", paysage=True)
    d.p(f"Certificat {O['qualiopi']}. Libellés abrégés : se référer au référentiel national qualité et à son guide de lecture pour la formulation exacte. "
        "[À VÉRIFIER : périmètre du certificat — la pièce jointe annoncée n'a pas été reçue.]")
    d.tableau(["N°", "Indicateur (libellé abrégé)", "Applicable", "Preuves dans le dossier", "Prête"],
              [[n, lib, app, preuve, "☐" if app != "Non (CFA uniquement)" else "—"] for n, lib, app, preuve in INDICATEURS],
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
    d.rgpd(["Les dossiers des candidats transmis au centre d'examen ou à la DEETS contiennent des données personnelles : transmission sécurisée et limitée au nécessaire."])
    return d.save(f"{DOSSIER}/AGR-03_Organiser_la_session_examen.docx")


def tout():
    return [presentation(), matrice_qualiopi(), checklist_examen()]


if __name__ == "__main__":
    from lib import ERREURS_MISE_EN_PAGE
    for f in tout():
        print(f.name)
    print("\n".join(ERREURS_MISE_EN_PAGE) or "OK")

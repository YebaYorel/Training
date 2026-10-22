"""Documents du parcours stagiaire propres aux parcours certifiants (MEM, RPMS).

Ils complètent le socle officiel YEBA (table DOCUMENTS OFFICIELS YEBA) sans le dupliquer :
CGV YEBA-DOC-03, règlement intérieur YEBA-DOC-04, politique de confidentialité YEBA-DOC-02,
politique handicap YEBA-DOC-08, réclamations YEBA-DOC-09, charte IA YEBA-DOC-11,
attestation de fin YEBA-DOC-17, certificat de réalisation YEBA-DOC-18.
"""
from lib import HORAIRES, ORGANISME, Doc

O, H = ORGANISME, HORAIRES
DOSSIER = "03_Parcours_stagiaire"
TITRES = "☐ TP Manager d'établissement marchand (RNCP41853)    ☐ TP Responsable de petite ou moyenne structure (RNCP38575)"
HORAIRE_TXT = "8 h 00 – 12 h 00 et 13 h 00 – 16 h 00 ; pauses de 10 h 00 à 10 h 15 et de 15 h 00 à 15 h 15 ; déjeuner de 12 h 00 à 13 h 00"
CYCLONE = ("Alerte cyclonique orange ou alerte rouge forte pluie : la session est suspendue immédiatement et chacun regagne son domicile ; "
           "alerte rouge : aucun déplacement ; la journée est reportée sans frais (règlement intérieur YEBA-DOC-04, article 5 ; CGV YEBA-DOC-03, article 6.5).")
SANS_IA = "Aucun système d'IA n'est utilisé pour évaluer, noter, classer ou sélectionner les stagiaires. La décision est prise exclusivement par une personne habilitée."
ANNEXES = [
    "Programme détaillé et daté (PRG-MEM ou PRG-RPMS) et calendrier de la promotion (CAL)",
    "Règlement intérieur YEBA-DOC-04 et son avenant pour les parcours certifiants RI-06",
    "Conditions générales de vente YEBA-DOC-03 et conditions particulières des parcours certifiants CP-05",
    "Politique de confidentialité YEBA-DOC-02",
    "Politique handicap et accessibilité YEBA-DOC-08 et procédure de réclamation YEBA-DOC-09",
    "Attestation d'assurance responsabilité civile professionnelle",
]


def fiche_inscription():
    d = Doc("Fiche d'inscription", "Dossier de candidature — parcours certifiant", code="FI-01")
    d.p(f"Formation souhaitée : {TITRES}")
    d.p(f"Session : [À COMPLÉTER : dates]   •   Lieu : {O['lieu']}")
    d.h2("1. Identité")
    d.champs(["Nom", "Prénom", "Date de naissance", "Adresse", "Code postal / Commune", "Téléphone", "E-mail"])
    d.h2("2. Situation actuelle")
    d.p("☐ Demandeur d'emploi — identifiant France Travail : __________   ☐ Suivi Mission Locale — conseiller : __________")
    d.p("☐ Salarié(e) — employeur : __________   ☐ Indépendant(e)   ☐ Autre : __________")
    d.p("Dernier diplôme ou niveau obtenu : __________   Expériences en lien avec la formation (années, postes) : __________")
    d.h2("3. Financement envisagé")
    d.p("☐ CPF   ☐ France Travail (AIF, AFC, POEI)   ☐ Région Réunion   ☐ OPCO / employeur   ☐ Transitions Pro   ☐ Financement personnel   ☐ Autre")
    d.h2("4. Projet professionnel (quelques lignes)")
    d.p("__________________________________________________________________________________")
    d.p("__________________________________________________________________________________")
    d.h2("5. Besoin d'aménagement (facultatif)")
    d.p("Avez-vous besoin d'un aménagement pour suivre la formation ou passer l'examen ?  ☐ Oui   ☐ Non")
    d.p("Vous n'avez pas à indiquer la nature d'un handicap : seul le besoin pratique est recueilli, lors d'un entretien confidentiel "
        "avec le référent handicap (politique YEBA-DOC-08). Ne joignez aucun document médical.", italic=True)
    d.h2("6. Pièces à joindre")
    d.cases(["Pièce d'identité en cours de validité (copie)", "CV à jour",
             "Justificatif de situation (attestation France Travail, ou bulletin de salaire si salarié)",
             "Pièces exigées par le financeur uniquement : [À COMPLÉTER selon le financeur, par exemple numéro de sécurité sociale pour une rémunération versée par la Région]"])
    d.h2("7. Engagement")
    d.p("Je certifie l'exactitude des informations fournies. J'ai reçu le programme, le règlement intérieur et la politique de confidentialité.")
    d.signatures(["Candidat(e)", f"Pour {O['nom']}"])
    d.rgpd([f"Vos données servent à étudier votre candidature, organiser votre formation et votre examen, et répondre aux obligations envers les financeurs "
            f"(politique de confidentialité YEBA-DOC-02). Droits : {O['contact_rgpd']} ; réclamation possible auprès de la CNIL.",
            "Minimisation : ni photo, ni situation familiale, ni donnée de santé, ni numéro de sécurité sociale sauf exigence écrite du financeur.",
            SANS_IA])
    return d.save(f"{DOSSIER}/FI-01_Fiche_inscription.docx")


def positionnement():
    d = Doc("Procédure d'admission et de positionnement", "Avant l'entrée en formation (Qualiopi indicateurs 4 et 8)", code="POS-02")
    d.p("Objectif : vérifier l'adéquation entre le projet du candidat et la formation, puis individualiser le parcours.")
    d.h2("Les étapes")
    d.tableau(["Étape", "Contenu", "Délai", "Trace conservée"], [
        ["1. Information collective", "Métier, titre, rythme, période en entreprise, financements", "3 à 1 mois avant", "Feuille de présence"],
        ["2. Dossier de candidature", "Fiche d'inscription FI-01, CV, justificatif de situation", "Avant l'entretien", "Dossier candidat"],
        ["3. Positionnement", "Situation des acquis par rapport au référentiel (outil conçu avec les supports de cours)", "Jour de l'entretien", "Résultat du positionnement"],
        ["4. Entretien individuel", "Projet, motivation, disponibilité, freins, financement, besoin d'aménagement", "Jour de l'entretien", "Compte rendu d'entretien"],
        ["5. Décision", "Admis, admis avec parcours adapté, ou réorientation motivée", "Sous 10 jours ouvrés", "Courrier ou e-mail au candidat"],
        ["6. Parcours individualisé", "Ajustements du parcours selon le positionnement", "Avant l'entrée", "Plan de parcours individualisé"],
    ], [3.6, 6.4, 3.2, 3.8])
    d.h2("Compte rendu d'entretien d'admission")
    d.champs(["Candidat (nom, prénom)", "Formation visée", "Projet professionnel", "Disponibilité sur toute la durée",
              "Freins identifiés (mobilité, garde, logement)", "Financement identifié", "Besoin d'aménagement (oui / non)",
              "Décision et motif", "Décision prise par (nom, fonction), date"])
    d.rgpd(["Candidat non retenu : données supprimées 2 ans après le dernier contact. Candidat admis : dossier stagiaire.", SANS_IA])
    return d.save(f"{DOSSIER}/POS-02_Procedure_admission.docx")


def convention():
    d = Doc("Convention de formation professionnelle — parcours certifiant", "Articles L.6353-1, L.6353-2 et D.6353-1 du code du travail", code="CONV-03")
    d.p("Modèle propre aux parcours certifiants longs. Pour les formations courtes, utiliser la convention YEBA-DOC-05.", italic=True)
    d.p(f"**Entre** {O['nom']}, {O['forme']}, {O['siege_court']}, SIRET {O['siret']}, déclaration d'activité n° {O['nda']} auprès du Préfet de La Réunion "
        f"(cet enregistrement ne vaut pas agrément de l'État), certification Qualiopi n° {O['qualiopi']}, représentée par {O['dirigeant']}, directeur, ci-après « l'Organisme »,")
    d.p("**Et** [À COMPLÉTER : raison sociale du client ou du financeur, SIRET, adresse, représentant, OPCO et numéro d'adhérent], ci-après « le Client ».")
    for titre, texte in [
        ("Article 1 — Objet", "L'Organisme réalise au bénéfice des stagiaires désignés en annexe l'action de formation « [À COMPLÉTER : intitulé du titre, RNCP] », "
                              "action de formation au sens de l'article L.6313-1 1° du code du travail, ayant pour objectif l'obtention du titre professionnel ou de certificats de compétences professionnelles (CCP)."),
        ("Article 2 — Durée, dates, horaires et lieu", f"Durée : [À COMPLÉTER] heures en centre et [À COMPLÉTER] heures en entreprise. Du [À COMPLÉTER] au [À COMPLÉTER]. "
                                                      f"Horaires : {HORAIRE_TXT}. Lieu : {O['lieu']} ({O['lieu_equipement']})."),
        ("Article 3 — Moyens pédagogiques, techniques et d'encadrement", "Pédagogie active, études de cas, mises en situation, alternance avec l'entreprise. Supports accessibles, "
                                                                         "disponibles en 16 points sur demande. Formateur : [À COMPLÉTER], compétences documentées au dossier qualité."),
        ("Article 4 — Suivi et sanction", "Émargement par demi-journée signé par le stagiaire et le formateur. Évaluations en cours de formation, épreuves blanches, session de validation "
                                          "organisée selon l'arrêté du 22 décembre 2015 modifié. Remise d'une attestation de fin de formation (YEBA-DOC-17) et d'un certificat de réalisation (YEBA-DOC-18)."),
        ("Article 5 — Prix et paiement", f"Prix : [À COMPLÉTER] € par stagiaire. {O['tva']}. Échéancier : [À COMPLÉTER : par exemple 30 % à l'entrée, 40 % à mi-parcours, 30 % à la fin], "
                                         "sur présentation des émargements. Paiement à 30 jours. En cas de refus ou de prise en charge partielle par un financeur, le Client reste redevable du prix (CGV, article 4.4)."),
        ("Article 6 — Absence, abandon, report", "Seules les heures réalisées sont facturées au financeur. En cas d'abandon, les heures réalisées sont dues. Conditions particulières : document CP-05. "
                                                 f"{CYCLONE}"),
        ("Article 7 — Données personnelles", "Chaque partie agit en responsable de traitement autonome. Données limitées au nécessaire (identité, présence, résultats), transmises par un canal sécurisé. "
                                             "Conservation : 5 ans pour les pièces d'exécution, 10 ans pour les pièces comptables (politique YEBA-DOC-02)."),
        ("Article 8 — Assurance", f"L'Organisme est assuré en responsabilité civile professionnelle : {O['assurance']}. Attestation en annexe."),
        ("Article 9 — Réclamations et litiges", f"Réclamation : {O['mail']} — accusé de réception sous 48 heures ouvrées, réponse motivée sous 15 jours ouvrés (YEBA-DOC-09). "
                                                "À défaut d'accord amiable, tribunaux de Saint-Denis de La Réunion."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.h3("Annexes")
    d.numeros(ANNEXES + ["Liste des stagiaires (nom, prénom, besoin d'aménagement oui / non)"])
    d.signatures([f"Pour {O['nom']}", "Pour le Client"])
    return d.save(f"{DOSSIER}/CONV-03_Convention_parcours_certifiant.docx")


def contrat_particulier():
    d = Doc("Contrat de formation professionnelle — parcours certifiant", "Personne finançant elle-même tout ou partie de sa formation — art. L.6353-3 à L.6353-7", code="CTR-04")
    d.encadre("Condition bloquante", [
        "Ce contrat ne peut pas être signé tant qu'aucun médiateur de la consommation n'est désigné (code de la consommation, art. L.612-1). "
        "Action à mener par le dirigeant : adhérer à un médiateur et reporter ses coordonnées à l'article 8.",
    ])
    d.p(f"Entre {O['nom']}, {O['forme']}, {O['siege_court']} (SIRET {O['siret']}, déclaration d'activité n° {O['nda']}) et M. / Mme [À COMPLÉTER], ci-après « le stagiaire ».")
    for titre, texte in [
        ("Article 1 — Objet", "Formation : [À COMPLÉTER : intitulé du titre, RNCP]. Objectifs, programme, moyens et modalités d'évaluation : programme annexé."),
        ("Article 2 — Niveau requis", "Conditions d'admission : voir programme. Positionnement réalisé le [À COMPLÉTER]."),
        ("Article 3 — Durée, dates et lieu", f"[À COMPLÉTER : heures et dates]. Horaires : {HORAIRE_TXT}. Lieu : {O['lieu']}."),
        ("Article 4 — Délai de rétractation", "Le stagiaire dispose de 10 jours à compter de la signature pour se rétracter, par lettre recommandée avec avis de réception (art. L.6353-5). "
                                              "Si le contrat est conclu à distance ou hors établissement, le délai de 14 jours du code de la consommation (art. L.221-18) s'applique ; le délai le plus favorable prévaut. "
                                              "Aucune somme ne peut être exigée avant l'expiration du délai (art. L.6353-6)."),
        ("Article 5 — Prix et échelonnement", f"Prix total : [À COMPLÉTER] €. {O['tva']}. À l'expiration du délai de rétractation, un premier versement de 30 % maximum peut être demandé ; "
                                              "le solde est échelonné au fur et à mesure du déroulement : [À COMPLÉTER : échéancier]."),
        ("Article 6 — Cessation anticipée", "En cas de cessation anticipée du fait du stagiaire, seules les prestations effectivement dispensées sont dues au prorata (art. L.6354-1). "
                                            f"Force majeure : résiliation, prestations dispensées seules dues. {CYCLONE}"),
        ("Article 7 — Règlement intérieur, handicap, données", "Règlement intérieur YEBA-DOC-04 et avenant RI-06 ; politique handicap YEBA-DOC-08 ; politique de confidentialité YEBA-DOC-02."),
        ("Article 8 — Réclamation et médiation", f"Réclamation : {O['mail']} (YEBA-DOC-09). Médiateur de la consommation : [À COMPLÉTER : nom et adresse de saisine du médiateur désigné]."),
        ("Article 9 — Litiges", "Le stagiaire peut saisir la juridiction de son lieu de résidence (code de la consommation, art. R.631-3)."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.h3("Annexes")
    d.numeros(["Programme détaillé et daté", "Règlement intérieur et avenant", "Formulaire de rétractation", "Politique de confidentialité",
               "Procédure de réclamation", "Attestation d'assurance responsabilité civile professionnelle"])
    d.signatures(["Le stagiaire (« Lu et approuvé »)", f"Pour {O['nom']}"])
    return d.save(f"{DOSSIER}/CTR-04_Contrat_particulier_parcours_certifiant.docx")


def conditions_particulieres():
    d = Doc("Conditions particulières des parcours certifiants", "Complément aux conditions générales de vente YEBA-DOC-03", code="CP-05")
    d.p("Les CGV YEBA-DOC-03 s'appliquent. Les présentes conditions particulières les complètent pour les parcours certifiants "
        "(titres professionnels MEM et RPMS) ; en cas de contradiction, elles prévalent pour ces parcours.")
    for titre, texte in [
        ("1. Effectif", "Par dérogation à l'article 6.3 des CGV : [À COMPLÉTER : minimum et maximum, par exemple 8 à 12 stagiaires]. "
                        "En deçà du minimum 15 jours ouvrés avant le démarrage, la session est reportée ; les stagiaires et financeurs en sont informés immédiatement."),
        ("2. Horaires et lieu", f"{HORAIRE_TXT}. Lieu : {O['lieu']} ; {O['lieu_equipement']}."),
        ("3. Période en entreprise", "La période en entreprise est obligatoire pour se présenter à l'examen (280 heures pour le MEM, 210 heures pour le RPMS). "
                                     "Le stagiaire recherche sa structure d'accueil avec l'aide de l'Organisme ; une convention tripartite est signée avant chaque période."),
        ("4. Examen", "La session de validation est organisée par l'Organisme s'il est agréé, ou par un centre agréé partenaire. "
                      "Le coût de l'examen est [À COMPLÉTER : inclus dans le prix / facturé en sus]."),
        ("5. Facturation", "Facturation selon l'échéancier de la convention ou du contrat, sur la base des heures réalisées et émargées. "
                           f"{O['tva']}. Les financements publics (CPF, France Travail, Région) suivent les règles de leur plateforme."),
        ("6. Abandon et absences", "Les heures non réalisées ne sont pas facturées au financeur. Le dédit de l'article 6.1 des CGV ne s'applique pas aux stagiaires financés par un financeur public. "
                                   "Toute absence est signalée le jour même ; le plan de prévention du décrochage (ABS-13) est mis en œuvre."),
        ("7. Force majeure", CYCLONE),
        ("8. Productions d'examen et intelligence artificielle", "Les productions d'examen restent le travail personnel du stagiaire. Tout usage d'un outil d'IA est déclaré, "
                                                                 "conformément à la charte YEBA-DOC-11. Aucune donnée de l'entreprise d'accueil n'est saisie dans un outil d'IA non validé."),
    ]:
        d.h3(titre)
        d.p(texte)
    return d.save(f"{DOSSIER}/CP-05_Conditions_particulieres_parcours_certifiants.docx")


def avenant_ri():
    d = Doc("Avenant au règlement intérieur", "Parcours certifiants de plus de 500 heures — complément à YEBA-DOC-04", code="RI-06")
    d.p("Le règlement intérieur YEBA-DOC-04 s'applique intégralement. Le présent avenant précise les points propres aux parcours certifiants MEM et RPMS.")
    for titre, texte in [
        ("Article A — Horaires (complète l'article 10)", f"Pour ces parcours, les horaires sont : {HORAIRE_TXT}. La journée compte 7 heures de formation."),
        ("Article B — Lieu", f"{O['lieu']} ; {O['lieu_equipement']}. Les consignes d'évacuation du site sont présentées le premier jour (article 4)."),
        ("Article C — Délégués des stagiaires (application de l'article 22)", "Ces actions dépassant 500 heures, un délégué titulaire et un délégué suppléant sont élus au scrutin uninominal "
                                                                               "à deux tours, entre la 20e et la 40e heure de formation. En l'absence de candidature, un procès-verbal de carence est établi et transmis au préfet de région."),
        ("Article D — Période en entreprise", "Pendant les périodes en entreprise, le stagiaire respecte le règlement et les consignes de sécurité de l'entreprise d'accueil ; "
                                              "la disposition la plus protectrice prévaut (article 1)."),
        ("Article E — Productions d'examen", "Les documents et diaporamas d'examen sont le travail personnel du stagiaire. L'usage d'un outil d'IA est déclaré (charte YEBA-DOC-11). "
                                             "Aucune donnée personnelle de salarié ou de client de l'entreprise d'accueil n'y figure."),
        ("Article F — Absences", "Toute absence est signalée avant 8 h 30 et justifiée sous 48 heures. Le financeur est informé selon ses règles."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.saut()
    d.h2("Procès-verbal d'élection des délégués des stagiaires")
    d.champs(["Action de formation et session", "Date du scrutin (entre la 20e et la 40e heure)", "Nombre d'inscrits et de votants",
              "Délégué titulaire élu", "Délégué suppléant élu", "Carence éventuelle (motif) — PV transmis au préfet le"])
    d.signatures(["Le directeur", "Les délégués élus"])
    d.h2("Accusé de réception")
    d.p("Je soussigné(e) ____________________, stagiaire du parcours « ____________________ », reconnais avoir reçu, lu et compris le règlement intérieur "
        "YEBA-DOC-04, le présent avenant, la politique de confidentialité et la procédure de réclamation.")
    d.signatures(["Le stagiaire"])
    return d.save(f"{DOSSIER}/RI-06_Avenant_reglement_interieur_et_PV_delegues.docx")


def emargement():
    d = Doc("Feuille d'émargement", "À signer par demi-journée par le stagiaire et le formateur", code="EMG-08", paysage=True)
    d.p("Formation : [À COMPLÉTER]   •   Semaine du ____ au ____   •   Module : ____   •   Formateur : ____")
    d.tableau(["Nom Prénom", "Lundi matin", "Lundi après-midi", "Mardi matin", "Mardi après-midi", "Mercredi matin", "Mercredi après-midi"],
              [[""] * 7 for _ in range(12)], [5.9, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3])
    d.tableau(["Nom Prénom", "Jeudi matin", "Jeudi après-midi", "Vendredi matin", "Vendredi après-midi", "Heures semaine", "Observations"],
              [[""] * 7 for _ in range(12)], [5.9, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3])
    d.p("Matin : 8 h 00 – 12 h 00 (4 h). Après-midi : 13 h 00 – 16 h 00 (3 h). Signature du formateur à chaque demi-journée : ______________________")
    d.rgpd(["Preuve légale de réalisation (code du travail, art. L.6362-1 et suivants) : conservée 5 ans après la fin de l'action, ou plus si le financeur l'exige.",
            "Émargement électronique éventuel : outil hébergé dans l'UE, horodatage, ni géolocalisation ni reconnaissance faciale."])
    return d.save(f"{DOSSIER}/EMG-08_Feuille_emargement.docx")


def attestations():
    d = Doc("Attestations d'entrée et de présence", "Complément aux modèles YEBA-DOC-17 et YEBA-DOC-18", code="ATT-09")
    d.p("Pour l'attestation de fin de formation et le certificat de réalisation, utiliser les modèles en vigueur YEBA-DOC-17 et YEBA-DOC-18, "
        "en y indiquant les heures en centre et en entreprise et les résultats par CCP.", italic=True)
    d.h2("A. Attestation d'entrée en formation")
    d.p(f"Je soussigné {O['dirigeant']}, directeur de {O['nom']}, atteste que M. / Mme __________ est entré(e) en formation "
        "« __________ » (RNCP ______) le ____ pour une durée prévue de ____ heures en centre et ____ heures en entreprise.")
    d.signatures(["Le directeur"])
    d.h2("B. Attestation mensuelle de présence (mois de ____________)")
    d.tableau(["Heures prévues", "Heures réalisées", "Absences justifiées", "Absences injustifiées"], [["", "", "", ""]], [4.25, 4.25, 4.25, 4.25])
    d.signatures(["Le directeur", "Le stagiaire"])
    return d.save(f"{DOSSIER}/ATT-09_Attestations_entree_et_presence.docx")


def evaluations():
    d = Doc("Questionnaires de satisfaction et suivi d'insertion", "À chaud • À froid • Insertion à 6 mois (Qualiopi indicateurs 2 et 30)", code="EVAL-10")
    d.h2("A. Questionnaire à chaud (dernier jour)")
    d.tableau(["Question", "1", "2", "3", "4"], [[q, "", "", "", ""] for q in [
        "Les objectifs annoncés ont été atteints", "Le contenu était adapté à mon projet", "Les formateurs étaient clairs et disponibles",
        "Les supports étaient lisibles et accessibles", "Les cas pratiques et les jeux m'ont aidé à comprendre",
        "L'accompagnement pendant la période en entreprise était utile", "Les locaux et le matériel étaient adaptés", "Je recommanderais cette formation"]],
        [9, 2, 2, 2, 2])
    d.p("1 = pas du tout d'accord … 4 = tout à fait d'accord. Ce que je retiens : ______  Ce qu'il faut améliorer : ______")
    d.h2("B. Questionnaire à froid (3 mois après)")
    d.puces(["Utilisez-vous les compétences acquises dans votre travail ? (oui / en partie / non)", "Exemple concret : ______", "Besoins complémentaires : ______"])
    d.h2("C. Enquête d'insertion à 6 mois")
    d.puces(["Situation : ☐ CDI ☐ CDD de 6 mois ou plus ☐ CDD de moins de 6 mois ☐ intérim ☐ création d'entreprise ☐ formation ☐ recherche d'emploi ☐ autre",
             "Emploi dans le métier visé ? ☐ oui ☐ non   Intitulé du poste : ______", "Titre obtenu ? ☐ complet ☐ partiel (CCP) ☐ non"])
    d.p("Questionnaire employeur et financeur (indicateur 30) : satisfaction, compétences observées, suggestions.")
    d.rgpd(["Résultats publiés uniquement sous forme agrégée ; réponses individuelles conservées 2 ans.",
            "Outil d'enquête hébergé dans l'UE ; aucune analyse des réponses par un outil d'IA non validé."])
    return d.save(f"{DOSSIER}/EVAL-10_Satisfaction_et_insertion.docx")


def handicap_examen():
    d = Doc("Aménagements de parcours et d'examen", "Complément à la politique handicap YEBA-DOC-08 pour les titres professionnels", code="HAND-12")
    d.p("La politique YEBA-DOC-08 s'applique (entretien sous 48 heures ouvrées, fiche d'adaptation sous 5 jours ouvrés, relais Agefiph, RHF, Cap emploi). "
        "Ce document précise ce qui est propre aux titres professionnels.")
    d.numeros([
        "Repérer le besoin dès l'entretien d'admission, sans demander la nature du handicap.",
        "Construire la fiche d'adaptation : rythme, supports en 16 points, poste de travail, pauses, périodes en entreprise adaptées.",
        "Aménagement des épreuves du titre : demande transmise au responsable de session dans les délais fixés par la DEETS, sur avis d'un médecin habilité, "
        "en s'appuyant sur le guide pratique d'aménagement des sessions d'examen du ministère du Travail (cité par le référentiel d'évaluation MEM v09).",
        "Exemples d'aménagements d'épreuve : temps majoré, pauses, matériel adapté, assistance humaine, salle séparée.",
        "Informer l'entreprise d'accueil uniquement de l'aménagement à appliquer, avec l'accord de la personne.",
        "Bilan en fin de parcours (indicateur 32).",
    ])
    d.h2("Fiche de suivi des aménagements d'examen")
    d.champs(["Stagiaire (nom, prénom)", "Aménagements de parcours décidés", "Aménagements d'épreuve demandés", "Date de transmission au responsable de session",
              "Réponse reçue le", "Accord pour informer l'entreprise d'accueil (oui / non, périmètre)"])
    d.rgpd(["Aucune donnée médicale n'est conservée par l'organisme : seul l'aménagement retenu est noté (RGPD, art. 9 ; politique YEBA-DOC-08)."])
    return d.save(f"{DOSSIER}/HAND-12_Amenagements_parcours_et_examen.docx")


def decrochage():
    d = Doc("Plan de prévention du décrochage", "Objectif : abaisser drastiquement le taux d'abandon", code="ABS-13")
    d.h2("1. Avant l'entrée : bien recruter")
    d.puces(["Information collective honnête sur le métier ; immersion d'une demi-journée en magasin ou en PME conseillée",
             "Entretien individuel : repérage des freins (mobilité, garde d'enfants, santé, logement, ressources)",
             "Vérification de la rémunération pendant la formation (allocation chômage, rémunération de formation, allocation CEJ) avant l'entrée",
             "Contrat d'engagement réciproque signé"])
    d.h2("2. Pendant : détecter tôt et agir vite")
    d.tableau(["Signal", "Délai de réaction", "Action"], [
        ["1 absence non prévenue", "Le jour même", "Appel ou SMS bienveillant du référent"],
        ["2 absences ou retards répétés", "Sous 48 h", "Entretien individuel et plan d'action écrit"],
        ["Baisse de résultats ou démotivation", "Dans la semaine", "Tutorat, binôme, adaptation du parcours"],
        ["Frein social identifié", "Sous 48 h", "Orientation Mission Locale, France Travail, CAF, Cap emploi (fiche LIAI-17)"],
        ["Intention d'abandon exprimée", "Immédiat", "Entretien avec le directeur et le prescripteur ; étudier une validation partielle (CCP)"],
    ], [5, 3.5, 8.5])
    d.h2("3. Leviers pédagogiques")
    d.puces(["Alternance courte centre / entreprise (4 semaines maximum en entreprise)", "Pédagogie active et ludique, réussites visibles dès la 1re semaine",
             "Validation possible par CCP : personne ne repart « sans rien »", "Rituel du lundi (objectifs) et du vendredi (réussites de la semaine)",
             "Parrainage par d'anciens stagiaires dès la 2e promotion"])
    d.h2("4. Indicateurs suivis chaque mois")
    d.puces(["Taux d'assiduité (heures réalisées / prévues)", "Nombre d'abandons et motifs", "Délai moyen de réaction après une absence"])
    d.h2("Contrat d'engagement réciproque")
    d.p(f"{O['nom']} s'engage à : accompagner individuellement, adapter le parcours, informer le prescripteur avec l'accord du stagiaire. "
        "Le stagiaire s'engage à : être présent et ponctuel, prévenir de toute absence, signaler tôt toute difficulté.")
    d.signatures(["Le stagiaire", f"Pour {O['nom']}", "Prescripteur (facultatif)"])
    d.rgpd(["Informations sur les freins limitées au strict nécessaire, partagées avec le prescripteur uniquement avec l'accord du stagiaire.",
            "IA Act, article 5 : aucun outil de reconnaissance des émotions ; aucun score de « risque d'abandon » calculé par une IA."])
    return d.save(f"{DOSSIER}/ABS-13_Prevention_decrochage.docx")


def convention_pae():
    d = Doc("Convention de période en entreprise", "Stagiaire de la formation professionnelle continue", code="PAE-14")
    d.p("Entre l'organisme de formation, l'entreprise d'accueil et le stagiaire. Si le stagiaire est demandeur d'emploi financé par France Travail ou par la Région, "
        "utiliser en priorité le modèle imposé par le financeur [À VÉRIFIER auprès du financeur].")
    d.champs(["Organisme de formation", "Entreprise d'accueil (raison sociale, SIRET, adresse)", "Tuteur (nom, fonction, contact)",
              "Stagiaire (nom, prénom)", "Formation et titre préparé", "Dates et horaires de la période", "Nombre d'heures",
              "Activités confiées (en lien avec les CCP)", "Objectifs de la période", "Suivi par l'organisme (appel ou visite à mi-période)"])
    d.h3("Clauses principales")
    d.puces([
        "Le stagiaire reste stagiaire de la formation professionnelle ; il n'occupe pas un poste de travail permanent.",
        "Gratification obligatoire au-delà de 2 mois de présence (308 heures) dans le même organisme d'accueil [À VÉRIFIER : applicabilité selon le statut du stagiaire].",
        "Couverture accidents du travail : [À VÉRIFIER selon le statut : financeur de la rémunération ou organisme de formation].",
        "L'entreprise respecte la durée du travail, la santé et la sécurité ; elle fournit les équipements de protection nécessaires.",
        "Confidentialité : anonymisation obligatoire dans les productions d'examen ; aucune donnée de l'entreprise dans un outil d'IA non validé.",
        "Une attestation de période en entreprise est remise le dernier jour (preuve exigée à l'ouverture de la session d'examen).",
    ])
    d.signatures(["Organisme de formation", "Entreprise d'accueil", "Stagiaire"])
    d.saut()
    d.h2("Fiche de suivi de la période en entreprise")
    d.champs(["Date de l'appel ou de la visite", "Interlocuteurs", "Activités réalisées par le stagiaire",
              "Points forts observés", "Difficultés éventuelles", "Actions décidées", "Suivi assuré par"])
    d.h2("Attestation de période en entreprise")
    d.p("L'entreprise ______ atteste que M. / Mme ______ a effectué une période en entreprise du ____ au ____, soit ____ heures.")
    d.signatures(["Le tuteur ou le représentant de l'entreprise"])
    return d.save(f"{DOSSIER}/PAE-14_Convention_et_suivi_periode_entreprise.docx")


def droit_image():
    d = Doc("Autorisation d'utilisation de l'image", "Facultative, révocable à tout moment", code="IMG-15")
    d.p(f"Je soussigné(e) ______ autorise / n'autorise pas (rayer la mention inutile) {O['nom']} à :")
    d.cases(["filmer mes mises en situation à des fins pédagogiques internes (visionnées par le groupe et le formateur, supprimées en fin de session)",
             "utiliser ma photo sur les réseaux sociaux et le site de l'organisme pendant 2 ans",
             "utiliser mon témoignage écrit (prénom uniquement) dans les supports de communication"])
    d.p(f"Refuser n'a aucune conséquence sur ma formation. Je peux retirer mon accord à tout moment auprès de {O['contact_rgpd']}.")
    d.signatures(["La personne"])
    d.rgpd(["Base légale : consentement (RGPD, art. 6.1.a et 7) ; droit à l'image (code civil, art. 9). Enregistrement soumis à l'accord de toutes les personnes filmées (YEBA-DOC-04, art. 14).",
            "IA Act, article 50 : toute image ou vidéo générée ou modifiée par IA et diffusée est signalée comme telle."])
    return d.save(f"{DOSSIER}/IMG-15_Autorisation_droit_image.docx")


def convocation():
    d = Doc("Convocation à l'entrée en formation", "À envoyer au moins 15 jours avant le démarrage", code="CONVOC-16")
    d.p("Madame, Monsieur [À COMPLÉTER : nom],")
    d.p("Nous avons le plaisir de vous confirmer votre admission à la formation « [À COMPLÉTER : intitulé du titre] ». "
        "Vous êtes attendu(e) le **[À COMPLÉTER : date] à 7 h 45** pour l'accueil ; la formation commence à 8 h 00.")
    d.tableau(["", ""], [
        ["Lieu", O["lieu"]],
        ["Accès", O["lieu_equipement"].capitalize()],
        ["Horaires", "8 h 00 – 12 h 00 et 13 h 00 – 16 h 00"],
        ["Pauses", "10 h 00 – 10 h 15 et 15 h 00 – 15 h 15 ; déjeuner de 12 h 00 à 13 h 00"],
        ["Durée", "[À COMPLÉTER : heures en centre + heures en entreprise]"],
        ["Contact", f"{O['dirigeant']} — {O['tel']} — {O['mail']}"],
    ], [4, 13])
    d.p("**Documents joints :** programme, livret d'accueil, règlement intérieur YEBA-DOC-04 et avenant RI-06, politique de confidentialité YEBA-DOC-02, charte IA YEBA-DOC-11.")
    d.p("**À apporter :** pièce d'identité, de quoi prendre des notes, CV à jour, identifiant France Travail le cas échéant.")
    d.p("Besoin d'un aménagement ? Le référent handicap est à votre écoute en toute confidentialité, sans avoir à préciser la nature d'un handicap.")
    d.p(f"{O['dirigeant']}, directeur de {O['nom']}")
    return d.save(f"{DOSSIER}/CONVOC-16_Convocation.docx")


def fiche_liaison():
    d = Doc("Fiche de liaison avec le prescripteur", "Mission Locale • France Travail • Cap emploi", code="LIAI-17")
    d.p("À compléter à l'entrée, à mi-parcours et à la sortie. Transmise au conseiller uniquement avec l'accord écrit du stagiaire.")
    d.champs(["Stagiaire (nom, prénom)", "Prescripteur (structure, conseiller, contact)", "Formation et dates",
              "Étape (entrée / mi-parcours / sortie / alerte)", "Assiduité (heures réalisées / prévues)",
              "Progression (sans note détaillée)", "Freins signalés par le stagiaire et accord pour les partager",
              "Action attendue du prescripteur", "Date et signature de l'organisme"])
    d.p("Accord du stagiaire pour la transmission de cette fiche :  ☐ Oui   ☐ Non     Signature : ____________")
    d.rgpd(["Transmission limitée au nécessaire, avec l'accord du stagiaire ; aucune information de santé ; envoi par messagerie sécurisée ou plateforme du prescripteur."])
    return d.save(f"{DOSSIER}/LIAI-17_Fiche_liaison_prescripteur.docx")


def sante_securite():
    d = Doc("Vos droits en santé et sécurité", "Fiche remise à chaque stagiaire le premier jour", code="SST-18")
    d.h2("Au centre de formation")
    d.puces(["Les consignes d'évacuation, les issues de secours et le point de rassemblement du Secrétariat Center sont présentés le premier jour.",
             "Signalez immédiatement tout accident, même bénin, ou toute situation dangereuse.", CYCLONE,
             "Fortes pluies : ne traversez jamais une ravine ou un radier submergé."])
    d.h2("En entreprise")
    d.puces(["L'entreprise vous informe des risques du poste et fournit les équipements de protection.",
             "Droit d'alerte et de retrait en cas de danger grave et imminent : prévenez votre tuteur et le centre.",
             "Gestes et postures : utilisez les aides à la manutention.",
             "Harcèlement, discrimination, violence : parlez-en au centre (procédure YEBA-DOC-14) ; vous pouvez aussi saisir l'inspection du travail ou le Défenseur des droits."])
    d.h2("Numéros utiles")
    d.tableau(["Service", "Numéro"], [["SAMU", "15"], ["Pompiers", "18"], ["Police", "17"], ["Urgence européenne", "112"],
                                       ["Urgence par SMS (personnes sourdes ou malentendantes)", "114"], [O["nom"], O["tel"]]], [11, 6])
    return d.save(f"{DOSSIER}/SST-18_Droits_sante_securite.docx")


def checklist_dossier():
    d = Doc("Contenu du dossier de chaque stagiaire", "Liste de contrôle — preuves pour les financeurs, la DEETS et Qualiopi", code="CHK-19")
    d.tableau(["Moment", "Pièce", "Présente"], [
        ["Avant", "Fiche d'inscription FI-01 et pièces justificatives", "☐"],
        ["Avant", "Compte rendu d'entretien d'admission et positionnement (POS-02)", "☐"],
        ["Avant", "Accord de financement (EDOF, KAIROS, OPCO, Région…)", "☐"],
        ["Avant", "Convention CONV-03 ou contrat CTR-04 signé ; convocation CONVOC-16", "☐"],
        ["Entrée", "Attestation d'entrée ; accusé de réception du règlement intérieur, de l'avenant et de la politique de confidentialité", "☐"],
        ["Entrée", "Contrat d'engagement (ABS-13) ; autorisation d'image IMG-15 (facultative)", "☐"],
        ["Pendant", "Feuilles d'émargement par demi-journée ; attestations mensuelles de présence", "☐"],
        ["Pendant", "Suivi des absences et actions menées", "☐"],
        ["Pendant", "Conventions de période en entreprise, fiches de suivi, attestations de période", "☐"],
        ["Pendant", "Bilan de mi-parcours ; fiches de liaison prescripteur", "☐"],
        ["Fin", "Questionnaire de satisfaction à chaud", "☐"],
        ["Fin", "Attestation de fin de formation YEBA-DOC-17 ; certificat de réalisation YEBA-DOC-18", "☐"],
        ["Fin", "Convocation et résultat de la session de validation", "☐"],
        ["Après", "Questionnaire à froid ; enquête d'insertion à 6 mois", "☐"],
        ["Séparé", "Fiche d'adaptation (sans donnée médicale), si concerné", "☐"],
    ], [2.6, 11.9, 2.5])
    d.rgpd(["Conservation : 5 ans après la fin de l'action pour les pièces d'exécution, 10 ans pour les pièces comptables, ou plus si le financeur l'exige.",
            "Stockage dans un espace chiffré hébergé dans l'Union européenne, accès limité aux personnes habilitées."])
    return d.save(f"{DOSSIER}/CHK-19_Contenu_dossier_stagiaire.docx")


def tout():
    return [f() for f in (fiche_inscription, positionnement, convention, contrat_particulier, conditions_particulieres, avenant_ri,
                          emargement, attestations, evaluations, handicap_examen, decrochage, convention_pae, droit_image,
                          convocation, fiche_liaison, sante_securite, checklist_dossier)]


if __name__ == "__main__":
    for f in tout():
        print(f.name)

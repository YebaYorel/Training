"""Documents du parcours stagiaire : avant, pendant, après la formation."""
from lib import Doc, ORGANISME

O = ORGANISME
DOSSIER = "03_Parcours_stagiaire"
TITRES = "☐ TP Manager d'établissement marchand (RNCP41853)    ☐ TP Responsable de petite ou moyenne structure (RNCP38575)"

MENTION_COURTE = (
    f"{O['nom']} traite vos données pour gérer votre candidature, votre formation et les obligations envers les financeurs et le "
    "ministère du Travail (bases légales : mesures précontractuelles / contrat et obligations légales — art. 6.1.b et 6.1.c RGPD). "
    "Destinataires : équipe pédagogique, financeur concerné, DEETS et jury du titre, plateformes publiques (Mon Compte Formation, KAIROS). "
    "Durées de conservation : voir la politique de conservation remise avec ce document. Vous pouvez exercer vos droits "
    f"(accès, rectification, effacement, limitation, opposition, portabilité) auprès de {O['contact_rgpd']} et saisir la CNIL (www.cnil.fr). "
    "Aucune décision vous concernant n'est prise par un système d'intelligence artificielle."
)


def fiche_inscription():
    d = Doc("Fiche d'inscription", "Dossier de candidature — formation certifiante", code="FI-01")
    d.p(f"Formation souhaitée : {TITRES}")
    d.p("Session : [À COMPLÉTER : dates]   •   Lieu : Secrétariat Center, 7 rue Henri Cornu, 97490 Saint-Denis")
    d.h2("1. Identité")
    d.champs(["Nom", "Prénom", "Date de naissance", "Adresse", "Code postal / Commune", "Téléphone", "E-mail"])
    d.h2("2. Situation actuelle")
    d.p("☐ Demandeur d'emploi — identifiant France Travail : __________   ☐ Suivi Mission Locale — conseiller : __________")
    d.p("☐ Salarié(e) — employeur : __________   ☐ Indépendant(e)   ☐ Autre : __________")
    d.p("Dernier diplôme ou niveau obtenu : __________   Expériences en lien avec la formation (années, postes) : __________")
    d.h2("3. Financement envisagé")
    d.p("☐ CPF   ☐ France Travail (AIF / AFC / POEI)   ☐ Région Réunion   ☐ OPCO / employeur   ☐ Transitions Pro   ☐ Financement personnel   ☐ Autre")
    d.h2("4. Projet professionnel (quelques lignes)")
    d.p("__________________________________________________________________________________")
    d.p("__________________________________________________________________________________")
    d.h2("5. Besoins d'adaptation (facultatif)")
    d.p("Souhaitez-vous un entretien confidentiel avec le référent handicap pour étudier des aménagements ?  ☐ Oui   ☐ Non")
    d.p("Ne joignez aucun document médical à ce dossier : les besoins sont étudiés lors de l'entretien, dans un dossier séparé et confidentiel.", italic=True)
    d.h2("6. Pièces à joindre")
    d.cases(["Pièce d'identité en cours de validité (copie)", "CV à jour",
             "Justificatif de situation (attestation France Travail, ou bulletin de salaire si salarié)",
             "Pièces exigées par le financeur uniquement : [À COMPLÉTER selon financeur, ex. n° de sécurité sociale si rémunération Région/ASP]"])
    d.h2("7. Engagement")
    d.p("Je certifie l'exactitude des informations fournies et j'ai pris connaissance du programme, du règlement intérieur et de la mention d'information ci-dessous.")
    d.signatures(["Candidat(e)", f"Pour {O['nom']}"])
    d.rgpd([MENTION_COURTE,
            "Minimisation : pas de numéro de sécurité sociale, de photo, de situation familiale ni de donnée de santé dans ce formulaire, sauf exigence écrite du financeur.",
            "Données de santé / handicap (art. 9 RGPD) : uniquement avec le consentement explicite de la personne, dans un dossier séparé accessible au seul référent handicap."])
    return d.save(f"{DOSSIER}/FI-01_Fiche_inscription.docx")


def positionnement():
    d = Doc("Procédure d'admission et de positionnement", "Avant l'entrée en formation (Qualiopi indicateurs 4 et 8)", code="POS-02")
    d.p("Objectif : vérifier l'adéquation entre le projet du candidat et la formation, puis individualiser le parcours. "
        "La décision d'admission est prise par une personne de l'équipe pédagogique, jamais par un outil automatisé.")
    d.h2("Les étapes")
    d.tableau(["Étape", "Contenu", "Délai", "Trace conservée"], [
        ["1. Information collective", "Présentation du métier, du titre, du rythme, des financements", "3 à 1 mois avant", "Feuille de présence"],
        ["2. Dossier de candidature", "Fiche d'inscription FI-01, CV, justificatif de situation", "Avant l'entretien", "Dossier candidat"],
        ["3. Positionnement", "Situation des acquis par rapport au référentiel (outil à concevoir avec les supports)", "Jour de l'entretien", "Résultat du positionnement"],
        ["4. Entretien individuel", "Projet, motivation, disponibilité, freins, financement, besoins d'adaptation", "Jour de l'entretien", "Compte rendu d'entretien"],
        ["5. Décision", "Admis, admis avec parcours adapté, ou réorientation motivée", "Sous 10 jours ouvrés", "Courrier ou e-mail au candidat"],
        ["6. Parcours individualisé", "Ajustements du parcours selon le positionnement", "Avant l'entrée", "Plan de parcours individualisé"],
    ], [3.6, 6.4, 3.2, 3.8])
    d.h2("Compte rendu d'entretien d'admission")
    d.champs(["Candidat (nom, prénom)", "Formation visée", "Projet professionnel", "Disponibilité sur toute la durée",
              "Freins identifiés (mobilité, garde, logement)", "Financement identifié", "Besoin d'entretien avec le référent handicap (oui / non)",
              "Décision et motif", "Décision prise par (nom, fonction), date"])
    d.rgpd(["Candidat non retenu : données supprimées 2 ans après le dernier contact. Candidat admis : dossier stagiaire.",
            "IA Act, annexe III point 3 : utiliser une IA pour décider de l'admission serait un usage à haut risque. YEBA FORMATIONS ne le fait pas."])
    return d.save(f"{DOSSIER}/POS-02_Procedure_admission.docx")

def convention():
    d = Doc("Convention de formation professionnelle", "Articles L.6353-1 et L.6353-2 du code du travail", code="CONV-03")
    d.p("**Entre** l'organisme de formation " + f"{O['nom']}, SIRET {O['siret']}, NDA {O['nda']} (enregistré auprès du préfet de région Réunion), "
        f"entreprise individuelle représentée par {O['dirigeant']}, {O['siege']},")
    d.p("**Et** [À COMPLÉTER : raison sociale du client / financeur, SIRET, adresse, représentant].")
    for titre, texte in [
        ("Article 1 — Objet", "Le client inscrit le(s) bénéficiaire(s) désigné(s) en annexe à l'action de formation : [À COMPLÉTER : intitulé, RNCP], ayant pour objectif l'obtention du titre professionnel ou de certificats de compétences professionnelles (CCP). Type d'action : action concourant au développement des compétences — action de formation (art. L.6313-1 1° du code du travail)."),
        ("Article 2 — Programme, durée, dates, lieu", "Programme joint (PRG). Durée : [À COMPLÉTER] heures en centre + [À COMPLÉTER] heures en entreprise. Du [À COMPLÉTER] au [À COMPLÉTER]. Horaires : 8 h 00 – 12 h 00 et 13 h 00 – 16 h 00. Lieu : Secrétariat Center, 7 rue Henri Cornu, 97490 Saint-Denis."),
        ("Article 3 — Moyens et modalités", "Moyens pédagogiques et techniques, modalités de suivi (feuilles d'émargement par demi-journée signées par le stagiaire et le formateur) et d'évaluation décrits au programme."),
        ("Article 4 — Sanction", "Session de validation du titre organisée selon l'arrêté du 22 décembre 2015 modifié. Remise d'une attestation de fin de formation et d'un certificat de réalisation."),
        ("Article 5 — Prix et paiement", "Coût : [À COMPLÉTER] € (exonéré de TVA — [À VÉRIFIER : attestation d'exonération]). Échéancier : [À COMPLÉTER : ex. 30 % à l'entrée, 40 % à mi-parcours, 30 % à la fin, sur présentation des émargements]."),
        ("Article 6 — Absence, abandon, annulation", "Seules les heures réalisées sont facturées au financeur public ; en cas d'abandon, les heures réalisées sont dues. Annulation par le client moins de [À COMPLÉTER] jours avant le début : [À COMPLÉTER]. En cas de force majeure (dont alerte cyclonique rouge), les heures sont reportées."),
        ("Article 7 — Données personnelles", "Chaque partie est responsable de ses propres traitements. Les données des stagiaires échangées sont limitées au nécessaire (identité, présence, résultats) et transmises par un canal sécurisé. L'organisme informe les stagiaires de leurs droits (art. 13 RGPD)."),
        ("Article 8 — Litiges", "Recherche d'une solution amiable ; à défaut, tribunal compétent de Saint-Denis (La Réunion)."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.p("Annexe : liste des bénéficiaires (nom, prénom uniquement).")
    d.signatures([f"Pour {O['nom']}", "Pour le client"])
    return d.save(f"{DOSSIER}/CONV-03_Convention_de_formation.docx")


def contrat_particulier():
    d = Doc("Contrat de formation professionnelle", "Personne finançant elle-même tout ou partie de sa formation — art. L.6353-3 à L.6353-7 du code du travail", code="CTR-04")
    d.p(f"Entre {O['nom']} (SIRET {O['siret']}, NDA {O['nda']}) et M./Mme [À COMPLÉTER], ci-après « le stagiaire ».")
    for titre, texte in [
        ("Article 1 — Objet", "Formation : [À COMPLÉTER : intitulé, RNCP]. Objectifs, programme, moyens, et modalités d'évaluation : voir programme joint."),
        ("Article 2 — Niveau requis", "Prérequis et conditions d'admission : voir programme. Le stagiaire a passé le positionnement le [À COMPLÉTER]."),
        ("Article 3 — Durée, dates et lieu", "[À COMPLÉTER : heures et dates]. Horaires : 8 h 00 – 12 h 00 et 13 h 00 – 16 h 00. Lieu : Secrétariat Center, 7 rue Henri Cornu, 97490 Saint-Denis."),
        ("Article 4 — Délai de rétractation", "Le stagiaire dispose de **10 jours** à compter de la signature pour se rétracter, par lettre recommandée avec accusé de réception (art. L.6353-5). Aucune somme ne peut être exigée avant l'expiration de ce délai (art. L.6353-6)."),
        ("Article 5 — Prix et paiement", "Prix total : [À COMPLÉTER] €. À l'issue du délai de rétractation, un acompte de 30 % maximum peut être demandé (art. L.6353-6) ; le solde est échelonné au fur et à mesure du déroulement de la formation : [À COMPLÉTER : échéancier]."),
        ("Article 6 — Interruption", "En cas d'abandon pour force majeure dûment reconnue, seules les prestations effectivement dispensées sont dues au prorata (art. L.6354-1). Dans les autres cas : [À COMPLÉTER]."),
        ("Article 7 — Données personnelles", "Voir la mention d'information RGPD remise au stagiaire."),
        ("Article 8 — Litiges", "Médiateur de la consommation : [À COMPLÉTER : nom et coordonnées du médiateur désigné]. À défaut d'accord, tribunal compétent."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.signatures(["Le stagiaire (« lu et approuvé »)", f"Pour {O['nom']}"])
    return d.save(f"{DOSSIER}/CTR-04_Contrat_formation_particulier.docx")


def cgv():
    d = Doc("Conditions générales de vente", "Formations inter, intra et certifiantes", code="CGV-05")
    for titre, texte in [
        ("1. Objet", f"Les présentes CGV s'appliquent aux prestations de formation de {O['nom']} (SIRET {O['siret']}, NDA {O['nda']} — {O['nda_mention']})."),
        ("2. Inscription", "Toute inscription est validée après positionnement, entretien et signature d'une convention (entreprise / financeur) ou d'un contrat (particulier)."),
        ("3. Prix", "Prix en euros, exonérés de TVA [À VÉRIFIER]. Les frais de repas, d'hébergement et de transport ne sont pas inclus sauf mention contraire."),
        ("4. Facturation et paiement", "Selon l'échéancier de la convention. Pénalités de retard pour les professionnels : taux légal en vigueur + indemnité forfaitaire de 40 € pour frais de recouvrement (art. L.441-10 du code de commerce)."),
        ("5. Annulation, report, absence", "[À COMPLÉTER : délais et conditions]. Alerte cyclonique orange/rouge ou décision préfectorale : report sans frais."),
        ("6. Propriété intellectuelle", "Les supports remis sont protégés ; usage personnel uniquement, pas de diffusion ni d'entraînement d'outils d'IA avec ces supports sans accord écrit."),
        ("7. Données personnelles", f"Traitements conformes au RGPD ; politique de confidentialité disponible sur demande ou sur [À COMPLÉTER : URL]. Contact : {O['contact_rgpd']}."),
        ("8. Réclamations", "Formulaire de réclamation disponible ; accusé de réception sous 48 h ouvrées, réponse sous 15 jours ouvrés."),
        ("9. Médiation et litiges", "Particuliers : médiateur de la consommation [À COMPLÉTER]. Droit français ; tribunaux de Saint-Denis (La Réunion)."),
    ]:
        d.h3(titre)
        d.p(texte)
    return d.save(f"{DOSSIER}/CGV-05_Conditions_generales_de_vente.docx")


def reglement_interieur():
    d = Doc("Règlement intérieur applicable aux stagiaires", "Articles L.6352-3 à L.6352-5 et R.6352-1 à R.6352-15 du code du travail", code="RI-06")
    for titre, texte in [
        ("Article 1 — Objet et champ", "Le présent règlement s'applique à toute personne inscrite à une action de formation de l'organisme, pendant toute sa durée, dans les locaux et lors des activités extérieures."),
        ("Article 2 — Hygiène et sécurité", "Respect des consignes de sécurité, d'incendie et d'évacuation affichées. Interdiction de fumer et de vapoter dans les locaux, d'y introduire de l'alcool ou des substances illicites. Tout accident, même bénin, est signalé immédiatement. Consignes cycloniques : en alerte orange, la formation est maintenue ou passe à distance selon décision de l'organisme ; en alerte rouge, les locaux sont fermés."),
        ("Article 3 — Horaires, absences, retards", "Horaires : 8 h 00 – 12 h 00 et 13 h 00 – 16 h 00 ; pauses de 10 h 00 à 10 h 15 et de 15 h 00 à 15 h 15. Émargement obligatoire par demi-journée. Toute absence est justifiée sous 48 h. Le financeur est informé des absences conformément à ses règles. À partir de [À COMPLÉTER : ex. 2] absences injustifiées, un entretien de suivi est organisé."),
        ("Article 4 — Comportement", "Respect des personnes, des opinions et des biens. Toute forme de harcèlement, de discrimination ou de violence est interdite et signalée. Téléphones en mode silencieux."),
        ("Article 5 — Usage du numérique et de l'IA", "Utilisation des outils d'IA uniquement selon la charte IA de l'organisme. Interdiction de saisir des données personnelles (clients, collègues, entreprise d'accueil) dans un outil d'IA non validé. Les productions d'examen doivent être personnelles ; tout usage d'IA est déclaré."),
        ("Article 6 — Sanctions", "Tout manquement peut donner lieu à : avertissement écrit, blâme, exclusion temporaire ou définitive. Le financeur est informé de toute sanction (art. R.6352-8)."),
        ("Article 7 — Procédure disciplinaire", "Aucune sanction sans que le stagiaire ait été informé des griefs. Pour une sanction ayant une incidence sur la présence en formation : convocation écrite précisant l'objet, la date, l'heure et le lieu de l'entretien, possibilité d'être assisté, décision motivée notifiée par écrit au plus tôt 1 jour franc et au plus tard 15 jours après l'entretien (art. R.6352-4 à R.6352-6)."),
        ("Article 8 — Représentation des stagiaires", "Pour les actions d'une durée supérieure à 500 heures (cas des deux titres professionnels), un délégué titulaire et un délégué suppléant sont élus au scrutin uninominal à deux tours, entre la 20e et la 40e heure de formation (art. R.6352-9 à R.6352-12). Les délégués font toute suggestion pour améliorer le déroulement des stages et présentent les réclamations."),
        ("Article 9 — Données personnelles et droit à l'image", "Les données des stagiaires sont traitées conformément au RGPD (mention d'information remise). Aucune photo ou vidéo d'un stagiaire n'est réalisée ou diffusée sans son autorisation écrite et révocable."),
        ("Article 10 — Publicité", "Le présent règlement est remis à chaque stagiaire avant l'entrée en formation et affiché dans les locaux."),
    ]:
        d.h3(titre)
        d.p(texte)
    d.p("Fait à [À COMPLÉTER], le [À COMPLÉTER].   Le directeur : " + O["dirigeant"])
    d.saut()
    d.h2("Procès-verbal d'élection des délégués des stagiaires")
    d.champs(["Action de formation / session", "Date du scrutin (entre 20e et 40e heure)", "Nombre d'inscrits / votants",
              "Délégué titulaire élu", "Délégué suppléant élu", "Carence éventuelle (motif)"])
    d.signatures(["Le directeur", "Les délégués élus"])
    return d.save(f"{DOSSIER}/RI-06_Reglement_interieur_et_PV_delegues.docx")


def emargement():
    d = Doc("Feuille d'émargement", "À signer par demi-journée par le stagiaire et le formateur", code="EMG-08", paysage=True)
    d.p("Formation : [À COMPLÉTER]   •   Semaine du ____ au ____   •   Module : ____   •   Formateur : ____")
    d.tableau(["Nom Prénom", "Lundi matin", "Lundi a-m", "Mardi matin", "Mardi a-m", "Mercredi matin", "Mercredi a-m"],
              [[""] * 7 for _ in range(12)], [5.9, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3])
    d.tableau(["Nom Prénom", "Jeudi matin", "Jeudi a-m", "Vendredi matin", "Vendredi a-m", "Heures semaine", "Observations"],
              [[""] * 7 for _ in range(12)], [5.7, 3.3, 3.3, 3.3, 3.3, 3.3, 3.5])
    d.p("Matin : 8 h 00 – 12 h 00 (4 h). Après-midi : 13 h 00 – 16 h 00 (3 h). Signature du formateur à chaque demi-journée : ______________________")
    d.rgpd(["Document justificatif pour les financeurs et contrôles DEETS : conservé 5 ans après la fin de l'action (ou durée exigée par le financeur, si plus longue).",
            "En cas d'émargement électronique : outil hébergé dans l'UE, horodatage, pas de géolocalisation ni de biométrie (reconnaissance faciale interdite)."])
    return d.save(f"{DOSSIER}/EMG-08_Feuille_emargement.docx")


def attestations():
    d = Doc("Attestations et certificat de réalisation", "Entrée • Assiduité • Fin de formation • Réalisation", code="ATT-09")
    d.h2("A. Attestation d'entrée en formation")
    d.p(f"Je soussigné {O['dirigeant']}, directeur de {O['nom']}, atteste que M./Mme __________ est entré(e) en formation "
        "« __________ » (RNCP ______) le ____ pour une durée prévue de ____ heures en centre et ____ heures en entreprise.")
    d.signatures(["Le directeur"])
    d.h2("B. Attestation mensuelle de présence (mois de ____________)")
    d.p("Heures prévues : ____   Heures réalisées : ____   Absences justifiées : ____   Absences injustifiées : ____")
    d.signatures(["Le directeur"])
    d.saut()
    d.h2("C. Attestation de fin de formation (art. L.6353-1 du code du travail)")
    d.p("M./Mme __________ a suivi la formation « __________ » du ____ au ____, soit ____ heures en centre et ____ heures en entreprise.")
    d.p("Objectifs de la formation : voir programme. Nature de l'action : action de formation (art. L.6313-1).")
    d.p("Résultats de l'évaluation des acquis :")
    d.tableau(["Bloc / CCP", "Résultat de l'évaluation formative", "Résultat session de validation"],
              [["CCP1", "", ""], ["CCP2", "", ""], ["CCP3", "", ""]], [6, 5.5, 5.5])
    d.signatures(["Le directeur", "Le stagiaire"])
    d.h2("D. Certificat de réalisation")
    d.p("Établi selon le modèle réglementaire en vigueur [À VÉRIFIER : utiliser le modèle officiel publié par le ministère du Travail]. Contenu minimal :")
    d.champs(["Organisme (raison sociale, NDA)", "Bénéficiaire", "Intitulé de l'action", "Nature de l'action (L.6313-1)",
              "Dates de réalisation", "Durée réalisée (heures)", "Assiduité (heures réalisées / prévues)", "Lieu et date, signature et cachet"])
    return d.save(f"{DOSSIER}/ATT-09_Attestations_et_certificat.docx")


def evaluations():
    d = Doc("Évaluations de satisfaction et suivi d'insertion", "À chaud • À froid • Insertion à 6 mois (Qualiopi indicateurs 2, 30, 31, 32)", code="EVAL-10")
    d.h2("A. Évaluation à chaud (dernier jour)")
    d.tableau(["Question", "1", "2", "3", "4"], [[q, "", "", "", ""] for q in [
        "Les objectifs annoncés ont été atteints", "Le contenu était adapté à mon projet", "Les formateurs étaient clairs et disponibles",
        "Les supports étaient lisibles et accessibles", "Les cas pratiques et jeux m'ont aidé à comprendre", "L'accompagnement en période en entreprise était utile",
        "Les locaux et le matériel étaient adaptés", "Je recommanderais cette formation"]], [9, 2, 2, 2, 2])
    d.p("1 = pas du tout d'accord … 4 = tout à fait d'accord. Ce que je retiens : ______  Ce qu'il faut améliorer : ______")
    d.h2("B. Évaluation à froid (3 mois après)")
    d.puces(["Utilisez-vous les compétences acquises dans votre travail ? (oui / en partie / non)", "Exemple concret d'utilisation : ______",
             "Quels besoins complémentaires ? ______"])
    d.h2("C. Enquête d'insertion à 6 mois")
    d.puces(["Situation : ☐ CDI ☐ CDD ≥ 6 mois ☐ CDD < 6 mois ☐ intérim ☐ création d'entreprise ☐ formation ☐ recherche d'emploi ☐ autre",
             "Emploi dans le métier visé par le titre ? ☐ oui ☐ non   Intitulé du poste : ______",
             "Titre obtenu ? ☐ complet ☐ partiel (CCP) ☐ non"])
    d.p("Questionnaire employeur / financeur (indicateur 30) : satisfaction, compétences observées, suggestions — modèle à adapter.")
    d.rgpd(["Questionnaires anonymisables : les résultats publiés sont agrégés (jamais nominatifs).",
            "Outil d'enquête en ligne hébergé dans l'UE (ex. solution française ou européenne) ; pas d'analyse des réponses par une IA non validée.",
            "Réponses individuelles conservées 2 ans, puis supprimées ; statistiques agrégées conservées sans limite."])
    return d.save(f"{DOSSIER}/EVAL-10_Evaluations_et_insertion.docx")


def reclamations():
    d = Doc("Procédure de traitement des réclamations et aléas", "Qualiopi indicateurs 31 et 32", code="REC-11")
    d.numeros([
        "Réception : par écrit (formulaire, e-mail) ou à l'oral (retranscrite par l'organisme). Tout public : stagiaire, entreprise, financeur, formateur.",
        "Accusé de réception sous 48 h ouvrées.",
        "Analyse par la direction ; échange avec la personne si besoin.",
        "Réponse écrite sous 15 jours ouvrés, avec les actions décidées.",
        "Enregistrement dans le registre des réclamations et des actions d'amélioration.",
        "Revue trimestrielle des réclamations et mise à jour des pratiques.",
    ])
    d.h2("Formulaire de réclamation")
    d.champs(["Date", "Nom (facultatif pour une suggestion)", "Qualité (stagiaire, entreprise, financeur…)", "Formation concernée",
              "Objet de la réclamation", "Solution souhaitée"])
    d.h2("Registre des réclamations et actions d'amélioration")
    d.tableau(["N°", "Date", "Origine", "Objet", "Réponse (date)", "Action d'amélioration", "Clôture"],
              [[""] * 7 for _ in range(6)], [1, 1.8, 2.2, 3.5, 2.5, 4, 2])
    return d.save(f"{DOSSIER}/REC-11_Reclamations.docx")


def handicap():
    d = Doc("Procédure d'accueil des personnes en situation de handicap", "Qualiopi indicateur 26 — Référent handicap", code="HAND-12")
    d.numeros([
        "Information dès la promotion : mention du référent handicap sur toutes les fiches programme et le site.",
        "Entretien confidentiel avant l'entrée, à la demande de la personne : besoins, compensations déjà en place (sans exiger de document médical).",
        "Construction du plan d'aménagement : rythme, supports (gros caractères, contrastes, version audio), poste adapté, pauses, accès PMR.",
        "Mobilisation des partenaires : Agefiph (aides techniques, humaines), Cap emploi, MDPH, ressource handicap formation (RHF) de La Réunion [À VÉRIFIER : coordonnées].",
        "Aménagement des épreuves du titre professionnel : demande à formuler dans les délais réglementaires auprès de la DEETS / du responsable de session, sur avis médical (règlement des sessions du titre).",
        "Suivi : point mensuel, ajustement du plan, information de l'entreprise d'accueil uniquement avec l'accord de la personne.",
        "Bilan en fin de parcours et amélioration de la procédure.",
    ])
    d.h2("Fiche confidentielle de besoins (dossier séparé)")
    d.champs(["Nom Prénom", "Besoins exprimés par la personne", "Aménagements pédagogiques décidés", "Aménagements matériels",
              "Aménagements d'examen à demander", "Partenaires mobilisés", "Accord pour informer l'entreprise d'accueil (oui/non, périmètre)"])
    d.signatures(["La personne", "Le référent handicap"])
    d.rgpd(["Donnée de santé = donnée sensible (art. 9 RGPD) : consentement explicite écrit, accès limité au référent handicap, armoire ou dossier chiffré séparé.",
            "Suppression à la fin du parcours (ou conservation de la seule preuve d'aménagement accordé, sans détail médical, avec le dossier stagiaire)."])
    return d.save(f"{DOSSIER}/HAND-12_Procedure_handicap.docx")


def decrochage():
    d = Doc("Plan de prévention du décrochage", "Objectif : abaisser drastiquement le taux d'abandon", code="ABS-13")
    d.h2("1. Avant l'entrée : bien recruter")
    d.puces(["Information collective honnête sur le métier (immersion d'une demi-journée en magasin ou PME conseillée)",
             "Entretien individuel : repérage des freins (mobilité, garde d'enfants, santé, logement, ressources financières)",
             "Vérification du statut et de la rémunération pendant la formation (ARE, rémunération de formation, allocation CEJ) avant l'entrée",
             "Contrat d'engagement réciproque signé"])
    d.h2("2. Pendant : détecter tôt et agir vite")
    d.tableau(["Signal", "Délai de réaction", "Action"], [
        ["1 absence non prévenue", "Le jour même", "Appel ou SMS bienveillant du référent"],
        ["2 absences ou retards répétés", "Sous 48 h", "Entretien individuel + plan d'action écrit"],
        ["Baisse de résultats / démotivation", "Dans la semaine", "Tutorat, binôme, adaptation du parcours"],
        ["Frein social identifié", "Sous 48 h", "Orientation Mission Locale / France Travail / CAF / Cap emploi"],
        ["Intention d'abandon exprimée", "Immédiat", "Entretien direction + conseiller prescripteur ; étudier suspension ou validation partielle (CCP)"],
    ], [5, 3.5, 8.5])
    d.h2("3. Leviers pédagogiques")
    d.puces(["Alternance courte centre / entreprise (4 semaines maximum en entreprise)", "Pédagogie active et ludique, réussites visibles dès la 1re semaine",
             "Validation possible par CCP : personne ne repart « sans rien »", "Rituel du lundi (objectifs) et du vendredi (réussites de la semaine)",
             "Parrainage par d'anciens stagiaires (dès la 2e promotion)"])
    d.h2("4. Indicateurs suivis chaque mois")
    d.puces(["Taux d'assiduité (heures réalisées / prévues)", "Nombre d'abandons et motifs", "Délai moyen de réaction après une absence"])
    d.h2("Contrat d'engagement réciproque")
    d.p(f"{O['nom']} s'engage à : accompagner individuellement, adapter le parcours, informer le prescripteur avec accord du stagiaire. "
        "Le stagiaire s'engage à : être présent et ponctuel, prévenir de toute absence, signaler tôt toute difficulté.")
    d.signatures(["Le stagiaire", f"Pour {O['nom']}", "Prescripteur (facultatif)"])
    d.rgpd(["Les informations sur les freins sociaux sont limitées au strict nécessaire, partagées avec le prescripteur uniquement avec l'accord du stagiaire.",
            "IA Act art. 5 : aucun outil de détection des émotions des stagiaires (pratique interdite dans l'éducation depuis le 2 février 2025). Aucun score de « risque d'abandon » calculé par IA."])
    return d.save(f"{DOSSIER}/ABS-13_Prevention_decrochage.docx")


def convention_pae():
    d = Doc("Convention de période en entreprise (stage)", "Stagiaire de la formation professionnelle continue", code="PAE-14")
    d.p("Entre l'organisme de formation, l'entreprise d'accueil et le stagiaire. [À VÉRIFIER : si le stagiaire est demandeur d'emploi financé par France Travail ou la Région, "
        "utiliser en priorité le modèle de convention imposé par le financeur.]")
    d.champs(["Organisme de formation", "Entreprise d'accueil (raison sociale, SIRET, adresse)", "Tuteur (nom, fonction, contact)",
              "Stagiaire (nom, prénom)", "Formation et titre préparé", "Dates et horaires de la période", "Nombre d'heures",
              "Activités confiées (en lien avec les CCP)", "Objectifs de la période", "Modalités de suivi (visite / appel à mi-période)"])
    d.h3("Clauses principales")
    d.puces([
        "Le stagiaire reste sous statut de stagiaire de la formation professionnelle ; il n'occupe pas un poste de travail permanent.",
        "Gratification obligatoire au-delà de 2 mois (soit 308 heures) de présence dans le même organisme d'accueil au cours d'une même année d'enseignement [À VÉRIFIER : applicabilité au statut du stagiaire].",
        "Protection accidents du travail : [À VÉRIFIER selon le statut : prise en charge par l'organisme financeur de la rémunération ou par l'organisme de formation].",
        "L'entreprise respecte la durée du travail, la santé et la sécurité ; elle fournit les EPI nécessaires.",
        "Confidentialité : le stagiaire ne réutilise pas de données personnelles de l'entreprise dans ses dossiers d'examen (anonymisation obligatoire) ni dans un outil d'IA.",
        "Une attestation de période en entreprise est remise en fin de période (preuve exigée à l'ouverture de la session d'examen).",
    ])
    d.signatures(["Organisme de formation", "Entreprise d'accueil", "Stagiaire"])
    d.saut()
    d.h2("Fiche de suivi de la période en entreprise")
    d.champs(["Date de l'appel ou de la visite", "Interlocuteurs", "Activités réalisées par le stagiaire",
              "Points forts observés", "Difficultés éventuelles", "Actions décidées", "Suivi assuré par"])
    d.h2("Attestation de période en entreprise")
    d.p("L'entreprise ______ atteste que M./Mme ______ a effectué une période en entreprise du ____ au ____, soit ____ heures.")
    d.signatures(["Le tuteur / représentant de l'entreprise"])
    return d.save(f"{DOSSIER}/PAE-14_Convention_et_suivi_periode_entreprise.docx")


def droit_image():
    d = Doc("Autorisation d'utilisation de l'image", "Facultative, révocable à tout moment", code="IMG-15")
    d.p("Je soussigné(e) ______ autorise / n'autorise pas (rayer la mention inutile) " + O["nom"] + " à :")
    d.cases(["filmer mes mises en situation à des fins pédagogiques internes (visionnées par le groupe et le formateur, supprimées en fin de session)",
             "utiliser ma photo sur les réseaux sociaux et le site de l'organisme pour une durée de 2 ans",
             "utiliser mon témoignage écrit (prénom uniquement) dans les supports de communication"])
    d.p("Refuser n'a aucune conséquence sur ma formation. Je peux retirer mon accord à tout moment auprès de " + O["contact_rgpd"] + ".")
    d.signatures(["La personne"])
    d.rgpd(["Base légale : consentement (art. 6.1.a et 7 RGPD) ; droit à l'image (art. 9 du code civil).",
            "IA Act art. 50 : toute image ou vidéo générée ou modifiée par IA et diffusée doit être signalée comme telle ; aucun « deepfake » d'un stagiaire."])
    return d.save(f"{DOSSIER}/IMG-15_Autorisation_droit_image.docx")


def convocation():
    d = Doc("Convocation à l'entrée en formation", "À envoyer 15 jours avant le démarrage", code="CONVOC-16")
    d.p("Madame, Monsieur [À COMPLÉTER : nom],")
    d.p("Nous avons le plaisir de vous confirmer votre admission à la formation « [À COMPLÉTER : intitulé du titre] ». "
        "Vous êtes attendu(e) le **[À COMPLÉTER : date] à 7 h 45** pour l'accueil (début de la formation à 8 h 00).")
    d.tableau(["", ""], [
        ["Lieu", O["lieu"]],
        ["Horaires", "8 h 00 – 12 h 00 et 13 h 00 – 16 h 00"],
        ["Pauses", "10 h 00 – 10 h 15 et 15 h 00 – 15 h 15 ; déjeuner de 12 h 00 à 13 h 00"],
        ["Durée", "[À COMPLÉTER : heures en centre + heures en entreprise]"],
        ["Contact", f"{O['dirigeant']} — {O['tel']}"],
    ], [4, 13])
    d.p("**Documents joints :** programme, livret d'accueil, règlement intérieur, charte IA, mention d'information sur vos données.")
    d.p("**À apporter :** pièce d'identité, de quoi prendre des notes, CV à jour, identifiant France Travail le cas échéant.")
    d.p("En cas d'empêchement, prévenez-nous au plus tôt. Si vous avez besoin d'un aménagement, le référent handicap est à votre écoute en toute confidentialité.")
    d.p(f"{O['dirigeant']}, directeur de {O['nom']}")
    return d.save(f"{DOSSIER}/CONVOC-16_Convocation.docx")


def fiche_liaison():
    d = Doc("Fiche de liaison avec le prescripteur", "Mission Locale • France Travail • Cap emploi", code="LIAI-17")
    d.p("À compléter à l'entrée, à mi-parcours et à la sortie. Transmise au conseiller uniquement avec l'accord écrit du stagiaire.")
    d.champs(["Stagiaire (nom, prénom)", "Prescripteur (structure, conseiller, contact)", "Formation et dates",
              "Étape (entrée / mi-parcours / sortie / alerte)", "Assiduité (heures réalisées / prévues)",
              "Progression (sans note détaillée)", "Freins signalés par le stagiaire et accord pour les partager",
              "Action attendue du prescripteur", "Date et signature YEBA FORMATIONS"])
    d.p("Accord du stagiaire pour la transmission de cette fiche :  ☐ Oui   ☐ Non     Signature : ____________")
    d.rgpd(["Base légale : exécution de la mission de suivi convenue avec le prescripteur et accord du stagiaire pour les informations sur ses freins personnels.",
            "Minimisation : aucune information de santé ; transmission par messagerie sécurisée ou plateforme du prescripteur."])
    return d.save(f"{DOSSIER}/LIAI-17_Fiche_liaison_prescripteur.docx")


def sante_securite():
    d = Doc("Vos droits en santé et sécurité", "Fiche remise à chaque stagiaire le premier jour", code="SST-18")
    d.h2("Au centre de formation")
    d.puces(["Repérez les sorties de secours et le point de rassemblement du Secrétariat Center.",
             "Signalez immédiatement tout accident, malaise ou situation dangereuse.",
             "Alerte cyclonique orange : vous êtes informé par SMS ou e-mail de la suite. Alerte rouge : ne vous déplacez pas, les locaux sont fermés.",
             "Fortes pluies : ne traversez jamais une ravine ou un radier submergé."])
    d.h2("En entreprise")
    d.puces(["L'entreprise doit vous informer des risques du poste et vous fournir les équipements de protection (chaussures, gants…).",
             "Vous avez un droit d'alerte et de retrait en cas de danger grave et imminent : prévenez votre tuteur et le centre.",
             "Gestes et postures : utilisez les aides à la manutention ; ne portez pas de charges excessives.",
             "Harcèlement, discrimination, violence : vous n'êtes pas seul. Parlez-en au centre ; vous pouvez aussi saisir l'inspection du travail ou le Défenseur des droits."])
    d.h2("Numéros utiles")
    d.tableau(["Service", "Numéro"], [["SAMU", "15"], ["Pompiers", "18"], ["Police", "17"], ["Urgence européenne", "112"],
                                       ["Urgence par SMS (personnes sourdes ou malentendantes)", "114"],
                                       ["YEBA FORMATIONS", O["tel"]]], [11, 6])
    return d.save(f"{DOSSIER}/SST-18_Droits_sante_securite.docx")


def checklist_dossier():
    d = Doc("Contenu du dossier de chaque stagiaire", "Liste de contrôle — preuves pour les financeurs, la DEETS et Qualiopi", code="CHK-19")
    d.tableau(["Moment", "Pièce", "Présente"], [
        ["Avant", "Fiche d'inscription et pièces justificatives", "☐"],
        ["Avant", "Compte rendu d'entretien d'admission et résultat du positionnement", "☐"],
        ["Avant", "Accord de financement (EDOF, KAIROS, OPCO, Région…) ou contrat de formation", "☐"],
        ["Avant", "Convention ou contrat signé ; convocation envoyée", "☐"],
        ["Entrée", "Attestation d'entrée ; accusé de réception du livret, du règlement et de la charte IA", "☐"],
        ["Entrée", "Contrat d'engagement réciproque ; autorisation d'image (facultative)", "☐"],
        ["Pendant", "Feuilles d'émargement par demi-journée ; attestations mensuelles de présence", "☐"],
        ["Pendant", "Suivi des absences et actions menées", "☐"],
        ["Pendant", "Conventions de période en entreprise, fiches de suivi, attestations de période", "☐"],
        ["Pendant", "Bilan de mi-parcours ; fiches de liaison prescripteur", "☐"],
        ["Fin", "Évaluation de satisfaction à chaud", "☐"],
        ["Fin", "Attestation de fin de formation ; certificat de réalisation", "☐"],
        ["Fin", "Convocation et résultat de la session de validation", "☐"],
        ["Après", "Questionnaire à froid ; enquête d'insertion à 6 mois", "☐"],
        ["Séparé", "Dossier handicap confidentiel (si concerné)", "☐"],
    ], [2.6, 11.9, 2.5])
    d.rgpd(["Conservation : durée de la formation + 5 ans, ou durée exigée par le financeur si elle est plus longue.",
            "Stockage dans un espace chiffré hébergé dans l'Union européenne, accès limité aux personnes habilitées."])
    return d.save(f"{DOSSIER}/CHK-19_Contenu_dossier_stagiaire.docx")


def tout():
    return [f() for f in (fiche_inscription, positionnement, convention, contrat_particulier, cgv, reglement_interieur,
                          emargement, attestations, evaluations, reclamations, handicap, decrochage, convention_pae, droit_image,
                          convocation, fiche_liaison, sante_securite, checklist_dossier)]


if __name__ == "__main__":
    for f in tout():
        print(f)

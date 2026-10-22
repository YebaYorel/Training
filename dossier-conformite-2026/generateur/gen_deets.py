"""Réponse au courriel de la DEETS (extension à l'apprentissage, art. L.6351-5)."""
from lib import Doc, ORGANISME

O = ORGANISME
DOSSIER = "01_Reponse_DEETS"


def courriels():
    d = Doc("Réponse à la DEETS — deux versions de courriel", "Service régional de contrôle — DEETS de La Réunion", code="DEETS-00")
    d.encadre("Recommandation", [
        "Votre objectif est la formation continue. Les titres professionnels MEM et RPMS se préparent en formation continue et en contrat de professionnalisation "
        "sans être CFA : l'extension à l'apprentissage n'est pas nécessaire.",
        "→ Envoyez la **version A** avant l'expiration du délai de 12 jours. Elle évite une instruction incomplète (et donc un refus inscrit au dossier) et laisse la porte ouverte.",
        "→ Gardez la **version B** et le dossier des 18 pièces pour le jour où vous déciderez de vous lancer dans l'apprentissage.",
        "Délai : courriel reçu le mardi 20 octobre 2026 ; 12 jours mènent au dimanche 1er novembre 2026 (Toussaint). **Envoyez au plus tard le vendredi 30 octobre 2026**, idéalement dès cette semaine, et gardez une copie de l'envoi.",
    ])
    d.h2("Version A (recommandée) — suspension de la demande d'extension")
    d.p("**Objet :** Votre courriel du 20 octobre 2026 — demande d'extension de la déclaration d'activité à l'apprentissage — NDA " + O["nda"])
    for par in [
        "Madame,",
        "Je vous remercie pour notre échange téléphonique et pour la liste des pièces nécessaires à l'instruction d'une extension de notre déclaration d'activité à l'apprentissage (article L.6351-5 du code du travail).",
        f"Après analyse, {O['nom']} (entreprise individuelle, SIRET {O['siret']}, NDA {O['nda']}) a décidé de développer en priorité son activité de formation professionnelle continue, notamment des parcours certifiants préparant aux titres professionnels du ministère du Travail (Manager d'établissement marchand — RNCP41853, Responsable de petite ou moyenne structure — RNCP38575), à destination des demandeurs d'emploi et des salariés, en lien avec France Travail et les Missions Locales.",
        "Je vous informe donc que je ne donne pas suite, à ce stade, à la demande d'extension à l'apprentissage. Je vous solliciterai de nouveau lorsque l'ensemble des conditions (moyens dédiés, locaux, accompagnement des apprentis, extension de la certification Qualiopi) seront réunies.",
        "Par ailleurs, pourriez-vous me confirmer le service à contacter pour l'agrément permettant d'organiser des sessions de validation des titres professionnels (article R.338-8 du code de l'éducation et arrêté du 21 juillet 2016), ainsi que les délais d'instruction pratiqués à La Réunion ?",
        "Je reste à votre disposition et vous prie d'agréer, Madame, mes salutations distinguées.",
        f"{O['dirigeant']}\nDirecteur — {O['nom']}\n{O['tel']}",
    ]:
        d.p(par)
    d.h2("Version B — transmission du dossier d'extension (si vous choisissez l'apprentissage)")
    for par in [
        "Madame,",
        "Suite à notre entretien téléphonique et à votre courriel du 20 octobre 2026, je vous prie de trouver ci-joint les pièces nécessaires à l'instruction de la modification de notre déclaration d'activité afin d'étendre notre activité à l'apprentissage (article L.6351-5 du code du travail).",
        "Le dossier comprend 18 pièces numérotées selon l'ordre de votre courriel (bordereau joint). Les pièces signalées « à transmettre après la première promotion » le seront à l'issue de celle-ci.",
        "Je vous informe également que l'extension de notre certification Qualiopi à la catégorie « actions de formation par apprentissage » est [À COMPLÉTER : engagée auprès de l'organisme certificateur / prévue le …].",
        "Je reste à votre disposition et vous prie d'agréer, Madame, mes salutations distinguées.",
        f"{O['dirigeant']}\nDirecteur — {O['nom']}",
    ]:
        d.p(par)
    d.rgpd(["Le bulletin n° 3 du casier judiciaire contient des données relatives aux infractions (art. 10 RGPD) : transmettez-le uniquement à la DEETS, par un canal sécurisé ; ne le conservez pas en copie après l'instruction.",
            "N'envoyez ni CV ni diplômes de formateurs sans les avoir informés de cette transmission (art. 13-14 RGPD)."])
    return d.save(f"{DOSSIER}/DEETS-00_Courriels_reponse.docx")


PIECES = [
    ("Statuts faisant mention de l'apprentissage", [
        "YEBA FORMATIONS est une **entreprise individuelle** : elle n'a pas de statuts. Ce point est à expliquer à la DEETS.",
        "Pièces de remplacement : extrait d'immatriculation au registre national des entreprises (RNE) ou avis de situation INSEE de moins de 3 mois, et attestation sur l'honneur du dirigeant décrivant l'activité (formation continue, et formation par apprentissage si l'extension est demandée).",
        "Vérifier que le code d'activité et la description de l'activité au RNE mentionnent la formation ; les mettre à jour si besoin sur le guichet unique des formalités d'entreprises."]),
    ("Bulletin n° 3 du casier judiciaire du dirigeant", [
        "À demander en ligne sur casier-judiciaire.justice.gouv.fr (gratuit, délivré sous quelques jours).",
        f"Concerne : {O['dirigeant']} et toute autre personne exerçant une fonction de direction.",
        "Pièce : bulletin n° 3 de moins de 3 mois [À VÉRIFIER : ancienneté maximale attendue par la DEETS]."]),
    ("Justificatifs des locaux et de leur aménagement", [
        "Bail (ou convention de mise à disposition / contrat de location de salle), attestation d'assurance des locaux, plan des locaux.",
        "Photos datées : salles de formation, toilettes, salle de pause / restauration, accès PMR, affichage sécurité et consignes cycloniques.",
        "Registre public d'accessibilité de l'établissement recevant du public (ERP) et attestation d'accessibilité [À VÉRIFIER : catégorie ERP].",
        "Lieu actuel : Secrétariat Center, 7 rue Henri Cornu, 97490 Saint-Denis, loué à la journée (100 € par jour). Joindre le contrat ou les conditions de location et une attestation du bailleur décrivant la salle, les sanitaires et l'espace de pause [À COMPLÉTER : surface, capacité, accessibilité].",
        "Vigilance : une location à la journée peut être jugée insuffisante pour un CFA (accueil permanent des apprentis). Elle convient à la formation continue."]),
    ("Titres et qualités des formateurs", [
        "Pour chaque intervenant : CV daté et signé, diplômes et certifications, justificatifs d'expérience professionnelle dans le métier visé (au moins [À COMPLÉTER] ans), contrat de travail ou de prestation.",
        f"{O['dirigeant']} : CV, certifications (Google AI Specialist, Google Professional AI, référent handicap, SecNumacadémie ANSSI, MOOC CNIL), expérience de formateur vente et management depuis 2021 et antérieure.",
        "Tableau de synthèse : formateur / modules / CCP / expérience métier / diplômes."]),
    ("Notice : aide à la recherche d'employeur et accompagnement en cas de rupture", [
        "Recherche d'employeur : chargé(e) de relations entreprises [À COMPLÉTER : salarié dédié avec CV et contrat de travail, ou contrat de sous-traitance + cahier des charges], fichier d'entreprises partenaires (commerce, PME), job datings trimestriels, ateliers CV / entretien, partenariats Missions Locales, France Travail, CCI, réseaux d'enseignes.",
        "Délai : jusqu'à 3 mois en formation sans contrat (statut de stagiaire de la formation professionnelle, art. L.6222-12-1) avec accompagnement renforcé hebdomadaire.",
        "Rupture : entretien dans les 48 h, information sur les droits, poursuite de la formation jusqu'à 6 mois pour trouver un nouvel employeur (art. L.6222-18-2), recherche active d'un nouvel employeur, orientation vers les partenaires."]),
    ("Notice : modalités et périodicité d'évaluation des compétences", [
        "Positionnement à l'entrée ; évaluation formative à la fin de chaque module (grilles critériées par CCP) ; bilan trimestriel avec le maître d'apprentissage ; épreuves blanches avant la session ; session de validation selon l'arrêté du 22 décembre 2015 modifié.",
        "Outils : livret de suivi, grilles critériées, carnet de liaison numérique. Aucune notation automatisée par IA."]),
    ("Notice : suivi des apprentis chez l'employeur et adéquation CFA / entreprise", [
        "Entretien tripartite dans les 2 mois suivant le début du contrat (vérification de l'adéquation et ajustements) ; visites ou visioconférences au moins une fois par trimestre ; appel mensuel au maître d'apprentissage.",
        "Livret d'apprentissage : activités confiées en entreprise mises en regard des compétences des CCP ; alerte et plan d'action si écart.",
        "Formation des maîtres d'apprentissage : voir pièce n° 17."]),
    ("Notice : mixité des métiers et égalité femmes-hommes", [
        "Communication non stéréotypée (visuels, écriture), témoignages de femmes et d'hommes managers, objectifs chiffrés de mixité par promotion [À COMPLÉTER], sensibilisation aux violences sexistes et sexuelles, procédure de signalement, référent égalité.",
        "Indicateurs : part de femmes / hommes inscrits, diplômés, insérés."]),
    ("Mobilité internationale des apprentis", [
        "Informations sur Erasmus+ (mobilité des apprentis), lien avec l'Agence Erasmus+ France, partenaires régionaux de la mobilité [À COMPLÉTER : accords éventuels].",
        "Référent mobilité : [À COMPLÉTER]. Si aucun accord n'est signé à ce jour, l'indiquer et présenter le plan d'action."]),
    ("Notice : accompagnement des apprentis en situation de handicap", [
        f"Référent handicap certifié : {O['dirigeant']}. Procédure HAND-12 jointe.",
        "Partenaires : Agefiph, Cap emploi, MDPH, ressource handicap formation. Majoration possible du niveau de prise en charge du contrat d'apprentissage par l'OPCO pour les apprentis en situation de handicap [À VÉRIFIER : modalités en vigueur].",
        "Aménagements pédagogiques, matériels et d'examen ; supports accessibles (gros caractères, contrastes)."]),
    ("Notice : prévention du décrochage", [
        "Plan ABS-13 joint : recrutement sécurisé, repérage des signaux faibles, délais de réaction, entretiens, orientation vers les partenaires sociaux, indicateurs mensuels.",
        "Interdiction des outils de détection des émotions (IA Act art. 5)."]),
    ("Notice : droits en santé, sécurité au travail et prévention des risques", [
        "Fiche « Vos droits en santé et sécurité » remise à l'entrée : visite d'information et de prévention, droit d'alerte et de retrait, EPI, travaux réglementés pour les mineurs, harcèlement, interlocuteurs (médecine du travail, inspection du travail, référent).",
        "Module de prévention des risques intégré au parcours (M1.1 / M1.3)."]),
    ("Promotion de l'insertion professionnelle après le diplôme", [
        "Ateliers emploi, job datings, réseau d'anciens, mise en relation avec les entreprises partenaires, enquête à 6 mois, publication des taux d'insertion."]),
    ("Suivi des anciens apprentis (à l'issue de la première promotion)", [
        "Enquêtes à 6 et 12 mois, réseau d'anciens, invitations aux événements — état descriptif à transmettre à l'issue de la 1re promotion."]),
    ("Sensibilisation à la création et à la reprise d'entreprise", [
        "Module T4 (création / reprise), intervention des réseaux d'accompagnement réunionnais [À COMPLÉTER : partenaires], témoignages de dirigeants, lien avec le titre RPMS."]),
    ("Activités culturelles et sportives", [
        "Programme annuel [À COMPLÉTER] : sortie culturelle par trimestre (patrimoine réunionnais), activité sportive collective, partenariats avec des associations locales ; budget et calendrier."]),
    ("Développement des compétences des tuteurs et maîtres d'apprentissage", [
        "Formation de 7 h proposée à chaque maître d'apprentissage (rôle, pédagogie de la transmission, évaluation, droit de l'apprenti, accueil du handicap) ; guide du maître d'apprentissage ; réunions annuelles.",
        "État récapitulatif à tenir : nom, entreprise, date, durée, émargement."]),
    ("Emplois du temps prévisionnels par titre", [
        "Joindre les calendriers CAL-MEM et CAL-RPMS et les déroulés DP-MEM et DP-RPMS, adaptés au rythme de l'alternance (ex. 1 semaine en centre / 3 semaines en entreprise) [À COMPLÉTER : rythme choisi avec les entreprises]."]),
]


def dossier_18():
    d = Doc("Dossier d'extension de la déclaration d'activité à l'apprentissage", "Article L.6351-5 du code du travail — 18 pièces", code="DEETS-01")
    d.p("Bordereau et contenu des notices, dans l'ordre exact du courriel de la DEETS. Chaque notice est un document signé et daté par le dirigeant.")
    d.tableau(["N°", "Pièce", "État"], [[str(i + 1), p[0], "☐ prête   ☐ à compléter"] for i, p in enumerate(PIECES)], [1.2, 11, 4.8])
    d.encadre("Points de vigilance avant tout envoi", [
        "Qualiopi : la certification doit couvrir la catégorie « actions de formation par apprentissage » — extension à demander à votre certificateur (audit).",
        "Moyens : la DEETS vérifiera l'existence réelle des moyens décrits (salarié dédié, locaux, partenariats). Ne décrivez que ce qui existe ou est contractualisé.",
        "Le financement de l'apprentissage repose sur les niveaux de prise en charge (NPEC) versés par les OPCO, par échéances : vérifiez le calendrier de versement et l'impact des ruptures sur votre trésorerie [À VÉRIFIER : règles 2026].",
    ])
    for i, (titre, contenu) in enumerate(PIECES, 1):
        d.h2(f"Pièce {i} — {titre}")
        d.puces(contenu)
    d.signatures([f"{O['dirigeant']}, directeur"])
    return d.save(f"{DOSSIER}/DEETS-01_Dossier_18_pieces_apprentissage.docx")


def tout():
    return [courriels(), dossier_18()]


if __name__ == "__main__":
    for f in tout():
        print(f)

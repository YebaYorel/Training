"""Note de synthèse : décisions, raisonnement, autocritique, questions."""
from calendrier import fmt, fmt_court, planifier, session_examen
from lib import HORAIRES, ORGANISME, Doc
from titres import MEM, RPMS, heures_centre, jours_centre

O, H = ORGANISME, HORAIRES


def note():
    m_j, _ = planifier("MEM")
    r_j, _ = planifier("RPMS")
    m_s, _ = session_examen("MEM")
    r_s, _ = session_examen("RPMS")
    loc_m = sum(1 for j in m_j if j[1] == "Centre") * H["location_jour"]
    loc_r = sum(1 for j in r_j if j[1] == "Centre") * H["location_jour"]
    d = Doc("Note de synthèse", "Votre année de formation continue avec les titres MEM et RPMS — version 2", code="NOTE-00",
            couverture=True, version="2026-10-v2")
    d.h1("1. Les décisions à retenir")
    d.numeros([
        "**DEETS** : envoyer la version A (suspension de l'extension à l'apprentissage) **au plus tard le vendredi 30 octobre 2026**. Le courriel est daté du 20 octobre ; le 12e jour tombe le dimanche 1er novembre (Toussaint).",
        f"**MEM — promotion 1** : du {fmt(m_j[0][0])} au {fmt(m_j[-1][0])} ; examen la semaine du {fmt_court(m_s)}.",
        f"**RPMS — promotion 1** : du {fmt(r_j[0][0])} au {fmt(r_j[-1][0])} ; examen la semaine du {fmt_court(r_s)}.",
        "**Examen** : passer par un centre déjà agréé pour la 1re session MEM, puis demander votre propre agrément.",
        "**Avant tout envoi** : compléter les champs en or foncé et vérifier les mentions « À VÉRIFIER ».",
    ])
    d.h1("2. Ce qui a changé depuis la version 1")
    d.tableau(["Sujet", "Changement"], [
        ["Statut", "Entreprise individuelle : pas de statuts ; extrait RNE ou avis INSEE et attestation sur l'honneur (pièce 1 de la DEETS)."],
        ["Horaires et lieu", f"{H['journee']}, pauses {H['pauses']}, déjeuner 12 h – 13 h ; {O['lieu']} ; location {H['location_jour']} € par jour."],
        ["Référentiel MEM", "Décorticage ligne par ligne sur le REAC v09 et le référentiel d'évaluation v09 : 10 compétences, critères officiels, productions exigées."],
        ["Référentiel RPMS", "Les documents transmis datent de 2016 (ancienne version) : le décorticage suit les 9 compétences officielles de la fiche RNCP38575."],
        ["Déroulé", f"Jour par jour avec dates réelles : MEM {jours_centre(MEM)} jours ({heures_centre(MEM)} h), RPMS {jours_centre(RPMS)} jours ({heures_centre(RPMS)} h)."],
        ["Livrets", "Un livret d'accueil par titre, avec le déroulé de l'année, les jalons, les épreuves et les productions."],
        ["Nouveaux outils", "Guides de période en entreprise, plan d'actions daté, budget et trésorerie, matrice Qualiopi, présentation du centre, organisation de l'examen, convocation, fiche de liaison prescripteur, fiche santé-sécurité, contenu du dossier stagiaire."],
        ["Retirés à votre demande", "Grilles d'évaluation, questions de positionnement et notations (elles viendront avec les supports de cours)."],
        ["Charte graphique", "Bleu marine et or du logo, aucune couleur parasite, couverture avec logo, contrôle automatique : aucun mot coupé dans les tableaux."],
    ], [4, 13])
    d.h1("3. Ce que nous apprend le REAC MEM v09")
    d.puces([
        "Le MEM est un manager de proximité : les prévisions économiques relèvent désormais du niveau 6 (Responsable d'établissement marchand).",
        "Les évaluations passées en cours de formation sont prises en compte par le jury : elles doivent être tracées dès le premier module.",
        "Les productions d'examen (deux documents et deux diaporamas) se construisent à partir de la période en entreprise : d'où le guide GPE et le choix de deux périodes de 140 h.",
        "L'épreuve se fait sur poste informatique (étude de cas de 4 h) : prévoir des ordinateurs portables dès le module T2 (budget).",
        "Le marché est porteur : tension de 3,7 sur les postes de manager de proximité (REAC v09, début 2025).",
        "Un concurrent réunionnais (ICCI Formations) diffuse déjà le REAC MEM v09 : différenciez-vous par l'IA, l'accompagnement individuel et l'accessibilité.",
    ])
    d.h1("4. Votre budget de salle")
    d.p(f"Location au Secrétariat Center : MEM {loc_m:,} € ; RPMS {loc_r:,} € (hors informations collectives, jury blanc et examen). ".replace(",", " ")
        + "Le classeur PIL-03 calcule le seuil de rentabilité et la trésorerie mois par mois dès que vous saisissez votre prix et vos effectifs.")
    d.p("Point d'attention : une location à la journée suffit pour la formation continue, mais elle serait fragile pour un CFA (accueil permanent) ou un agrément de centre d'examen (le site doit être stable).")
    d.h1("5. Autocritique et corrections")
    d.tableau(["Angle", "Faille", "Correction"], [
        ["Juridique", "RPMS bâti sans le REAC v08 officiel", "Signalé dans chaque document RPMS ; à confronter dès réception du REAC v08"],
        ["Juridique", "Indicateurs Qualiopi en libellés abrégés", "Renvoi au référentiel national qualité pour la formulation exacte"],
        ["Faisabilité", "Périodes en entreprise qui commencent en milieu de semaine", "Acceptable pour les entreprises ; ajustable en décalant la date de démarrage"],
        ["Faisabilité", "RPMS en décembre–février, pleine saison cyclonique", "Plan de continuité et formation à distance prévus ; décaler à août si vous préférez"],
        ["Économique", "Prix de vente inconnu", "Budget paramétrable ; aucun chiffre inventé"],
        ["Social", "Public Missions Locales sur un parcours de 6 mois", "Alternance courte, bilan de mi-parcours, fiche de liaison, réaction le jour même"],
        ["Sécurité", "Données des stagiaires dans des documents remplis", "Ne jamais les committer : dossier « dossiers-remplis » exclu de Git, stockage UE chiffré"],
        ["Écologique", "Impression des dossiers", "Dématérialisation, sauf travaux d'examen à imprimer selon le référentiel"],
        ["Politique", "Dépendance aux appels d'offres régionaux", "Mix CPF, France Travail, OPCO et formations courtes en intra"],
    ], [3, 6.5, 7.5])
    d.h1("6. Ce qu'il me manque")
    d.numeros([
        "Le certificat Qualiopi : la pièce jointe annoncée n'est pas arrivée (seuls les référentiels ont été reçus). J'en ai besoin pour le périmètre et la date d'audit.",
        "Le REAC et le référentiel d'évaluation RPMS millésime 08 (2023).",
        "Téléphone, e-mail, site, adresse du siège (si différente du Secrétariat Center).",
        "Accessibilité du Secrétariat Center (PMR, sanitaires, salle de pause) et équipement (vidéoprojecteur, connexion).",
        "Prix de vente par titre et par CCP, effectif cible.",
        "Les dates de démarrage proposées vous conviennent-elles (MEM le 1er mars 2027, RPMS le 6 septembre 2027) ?",
        "Les livrets réalisés pour Marilyn Institut : je n'ai pas accès à cette conversation. Si vous me les transmettez, j'aligne la présentation (sans jamais mêler les deux marques).",
    ])
    d.h1("7. Sources")
    d.puces([
        "REAC Manager d'établissement marchand, TP-00136, millésime 09 du 10/12/2025 (document transmis).",
        "Référentiel d'évaluation Manager d'établissement marchand, millésime 09 du 10/12/2025 (document transmis).",
        "Fiches France Compétences RNCP41853 et RNCP38575 (documents transmis, consultés le 21/10/2026).",
        "REAC et RC Responsable de petite et moyenne structure, RNCP35646, millésime 07 de 2016 (documents transmis — version remplacée).",
        "Période en entreprise RPMS de 210 h : référentiel d'évaluation RPMS v08 cité par plusieurs organismes (medef.nc, icademie.com, etudis.net).",
        "Agrément des sessions : démarche « DEETS 974 — demande d'agrément pour organiser des sessions » (demarche.numerique.gouv.fr).",
        "Code du travail ; RGPD (règlement UE 2016/679) ; IA Act (règlement UE 2024/1689).",
    ])
    d.rgpd(["RGPD : tous les modèles contiennent une information des personnes et respectent la minimisation ; registre et durées de conservation dans 04_RGPD_IA_Act.",
            "IA Act : aucun usage d'IA pour admettre, évaluer ou surveiller les stagiaires (annexe III, haut risque) ; formation de l'équipe à la maîtrise de l'IA (article 4)."])
    return d.save("00_NOTE_DE_SYNTHESE.docx")


if __name__ == "__main__":
    print(note())

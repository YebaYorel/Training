"""Par titre : programme, décorticage REAC, déroulé jour par jour, calendrier, livret d'accueil, guide de la période en entreprise."""
import datetime as dt

from calendrier import PROMOTIONS, fmt, fmt_court, periodes, planifier, semaines, session_examen
from lib import HORAIRES, ORGANISME, Doc
from titres import DUREE_JOUR, MEM, RPMS, heures, heures_centre, jours_centre

O, H = ORGANISME, HORAIRES

# Critères d'évaluation officiels — référentiel d'évaluation MEM v09, § 3.2
CRITERES_MEM = {
    "CP1": ["Les consignes sont transmises en donnant du sens aux actions à mener",
            "L'animation des briefings, des débriefings et des réunions est adaptée aux enjeux et à l'équipe",
            "Les outils et les techniques de stimulation et de motivation sont utilisés de manière adaptée au contexte",
            "La communication et l'animation sont adaptées aux différentes situations managériales",
            "L'équipe est impliquée dans l'amélioration continue et l'atteinte des objectifs"],
    "CP2": ["Les besoins humains sont anticipés et adaptés à l'activité prévue",
            "La charge de travail est évaluée de manière réaliste et répartie de façon optimale",
            "La planification des horaires et des tâches respecte la réglementation en vigueur",
            "Les plannings sont communiqués à l'équipe de façon adaptée",
            "La gestion des imprévus est adaptée au contexte",
            "L'organisation du travail tient compte de la prévention des risques professionnels"],
    "CP3": ["Le niveau de maîtrise des compétences, le degré d'implication et le potentiel des collaborateurs sont évalués de manière pertinente",
            "Les freins et les leviers motivationnels sont identifiés et pris en compte dans l'accompagnement",
            "Les plans d'accompagnement et de formation sont individualisés",
            "Les plans d'accompagnement correspondent aux besoins des collaborateurs"],
    "CP4": ["L'adéquation entre le profil du candidat et la fiche de poste est évaluée à partir des critères définis",
            "Le parcours d'intégration est individualisé en fonction des compétences de la nouvelle recrue",
            "Le tutorat est adapté aux besoins des nouvelles recrues et favorise leur montée en compétences",
            "Le suivi de la période d'essai est assuré et les difficultés éventuelles sont remontées à la hiérarchie"],
    "CP5": ["L'analyse des données d'approvisionnement permet d'anticiper les besoins",
            "Les inventaires sont réalisés dans le respect des procédures de l'entreprise",
            "Les quantités commandées sont fournies en fonction des stocks, des ventes et des réservations clients",
            "Les anomalies de livraison sont repérées, signalées et traitées suivant le contexte",
            "Les mesures de prévention des risques sont appliquées et leur application est contrôlée"],
    "CP6": ["Les consignes de l'offre concernant le merchandising d'implantation sont respectées",
            "L'implantation est efficace et cohérente avec les objectifs commerciaux, budgétaires et les indicateurs",
            "Les opérations commerciales sont en adéquation avec les objectifs définis",
            "L'analyse des résultats du merchandising est pertinente et permet d'identifier des actions correctives",
            "L'application des mesures de prévention des risques par l'équipe est contrôlée"],
    "CP7": ["L'identification des attentes clients et des tendances permet d'optimiser l'expérience client",
            "L'utilisation des outils de gestion de la relation client est efficace",
            "La réponse aux besoins de tout type de clientèle, dont celle en situation de handicap, est efficace",
            "L'offre est valorisée sur la surface de vente et via les supports numériques",
            "Les argumentaires prennent en compte la demande du client et valorisent l'offre",
            "Les performances font l'objet d'un suivi régulier et des propositions sont formulées à la hiérarchie"],
    "CP8": ["Les indicateurs clés de la performance commerciale, de la satisfaction client et leurs variations sont collectés, calculés et fiables",
            "Les écarts par rapport aux objectifs sont détectés, calculés et analysés",
            "L'analyse des résultats est communiquée de manière structurée, claire et argumentée",
            "Les alertes en cas de dérive sont transmises par le canal le plus adapté",
            "L'analyse est réalisée et transmise dans les délais requis"],
    "CP9": ["Les données économiques sont recueillies avec fiabilité et exactitude",
            "Les indicateurs clés de rentabilité sont sélectionnés selon les objectifs transmis",
            "Les écarts sont analysés avec rigueur et dans les délais prescrits",
            "Les causes des écarts sont identifiées",
            "Une synthèse claire et structurée est transmise à la hiérarchie",
            "Des pistes d'optimisation réalistes sont formulées"],
    "CP10": ["Les propositions d'actions sont cohérentes avec les objectifs visés et les données analysées",
             "Les propositions prennent en compte les moyens humains, matériels et financiers disponibles",
             "Les actions validées sont mises en œuvre et les résultats évalués",
             "Les écarts persistants sont identifiés",
             "Les propositions d'ajustement sont réalistes"],
}

# Résumé de la description REAC de chaque CP (MEM v09) ou de la fiche RNCP (RPMS)
RESUME_CP = {
    "MEM": {
        "CP1": "Mobiliser l'équipe et favoriser sa cohésion ; transmettre des consignes qui ont du sens ; animer briefings, débriefings et réunions ; impliquer l'équipe dans l'amélioration continue ; animer des actions de professionnalisation.",
        "CP2": "Anticiper les besoins humains à partir des prévisions ; élaborer et ajuster les plannings dans le respect de la réglementation et de la prévention ; tenir compte des besoins spécifiques (handicap) ; réguler l'activité face aux imprévus.",
        "CP3": "Évaluer compétences, implication et potentiel ; identifier freins et leviers de motivation ; mettre en place des plans d'accompagnement et de formation individualisés ; conduire les entretiens individuels.",
        "CP4": "Identifier les besoins en personnel ; contribuer à la sélection et aux entretiens ; préparer un parcours d'intégration et un tutorat ; suivre la période d'essai ; contribuer à l'adaptation des postes.",
        "CP5": "Anticiper les besoins d'approvisionnement ; suivre les stocks et réaliser les inventaires ; réceptionner et contrôler les livraisons ; appliquer les mesures de prévention et la démarche RSE (déchets, gaspillage).",
        "CP6": "Organiser et mettre en œuvre l'implantation de l'offre et les opérations commerciales ; respecter les règles de merchandising ; garantir l'accessibilité et la sécurité ; analyser les résultats et proposer des ajustements.",
        "CP7": "Identifier les attentes et parcours clients ; utiliser les outils de relation client et l'omnicanal ; répondre aux besoins de tout type de clientèle ; argumenter ; gérer réclamations et litiges ; valoriser l'offre en ligne.",
        "CP8": "Collecter les données d'activité ; analyser les indicateurs commerciaux et de satisfaction ; interpréter les résultats au regard des objectifs ; repérer les écarts et alerter la hiérarchie.",
        "CP9": "Collecter les données économiques ; choisir les indicateurs de rentabilité ; relier résultats et actions ; identifier les causes d'écarts ; transmettre une synthèse et des pistes d'amélioration.",
        "CP10": "Proposer des actions correctives réalistes ; contribuer à la mise en œuvre du plan validé ; informer et coordonner l'équipe ; évaluer les résultats et proposer des ajustements.",
    },
    "RPMS": {
        "CP1": "Développer une vision systémique de la structure dans son environnement (fiche RNCP38575, bloc 1).",
        "CP2": "Inscrire la structure dans son territoire (fiche RNCP38575, bloc 1).",
        "CP3": "Manager et animer une équipe (fiche RNCP38575, bloc 1).",
        "CP4": "Adapter l'offre de la structure à la demande (fiche RNCP38575, bloc 2).",
        "CP5": "Organiser et développer la diffusion de l'offre (fiche RNCP38575, bloc 2).",
        "CP6": "Organiser la production (fiche RNCP38575, bloc 2).",
        "CP7": "Analyser le bilan de la structure (fiche RNCP38575, bloc 3).",
        "CP8": "Analyser le compte de résultat de la structure (fiche RNCP38575, bloc 3).",
        "CP9": "Rédiger le rapport d'activité de la structure (fiche RNCP38575, bloc 3).",
    },
}

LARGEUR = 17.0


def _dossier(t):
    return f"02_{t['code']}"


# --------------------------------------------------------------------------
def programme(t):
    hc = heures_centre(t)
    jours, _ = planifier(t["code"])
    s1, s2 = session_examen(t["code"])
    d = Doc(f"Programme de formation", f"{t['intitule']} — {t['rncp']}", code=f"PRG-{t['code']}", couverture=True)
    d.h1("1. Identification de la certification")
    d.tableau(["Rubrique", "Information"], [
        ["Certification", f"{t['intitule']} — {t['rncp']}"],
        ["Certificateur", t["certificateur"]],
        ["Niveau", t["niveau"]],
        ["Texte de référence", t["arrete"]],
        ["Référentiels", t["reac"]],
        ["Codes ROME", t["rome"]],
        ["Code NSF", t["nsf"]],
        ["Formacodes", t["formacode"]],
        ["Organisme", f"{O['nom']} — {O['forme']} — SIRET {O['siret']} — NDA {O['nda']} — Qualiopi {O['qualiopi']}"],
    ], [4.5, 12.5])
    d.h1("2. Public, prérequis et admission")
    d.p(t["public"])
    d.puces(t["prerequis"])
    d.h3("Délais d'accès")
    d.puces([
        "Informations collectives : au moins deux, entre 3 et 1 mois avant le démarrage.",
        "Réponse écrite à chaque candidature sous 10 jours ouvrés après l'entretien.",
        "Délai d'accès : 15 jours ouvrés minimum entre l'inscription et le démarrage, sous réserve de places et de financement.",
        "Financement CPF : respect du délai imposé par Mon Compte Formation entre la proposition et l'entrée [À VÉRIFIER : délai en vigueur].",
    ])
    d.h1("3. Objectifs de la formation")
    d.p(f"À l'issue de la formation, le stagiaire est capable d'exercer l'emploi de {t['court'].lower()} et de se présenter "
        "aux épreuves du titre professionnel. Les objectifs reprennent les compétences professionnelles du référentiel :")
    for code, bc, lib, _ in t["blocs"]:
        d.h3(f"{code} — {lib}")
        d.puces([f"{m['intitule']} : {m['objectif']}" for m in t["modules"] if m["bloc"] == code])
    d.h3("Compétences complémentaires (plus-value YEBA FORMATIONS)")
    d.puces([f"{m['intitule']} ({heures(m)} h) : {m['objectif']}" for m in t["modules"] if m["bloc"] == "Transversal"])
    d.h1("4. Durée, dates, horaires et lieu")
    d.tableau(["Élément", "Valeur"], [
        ["Durée en centre", f"{hc} heures ({jours_centre(t)} jours de {DUREE_JOUR} h)"],
        ["Période en entreprise", f"{t['pae']} heures — {t['pae_source']}"],
        ["Durée totale", f"{hc + t['pae']} heures, hors session d'examen"],
        ["Dates proposées", f"du {fmt(jours[0][0])} au {fmt(jours[-1][0])}"],
        ["Session d'examen", f"semaine du {fmt_court(s1)} au {fmt_court(s2)} [À VÉRIFIER : date fixée avec la DEETS ou le centre agréé]"],
        ["Horaires", f"{H['journee']} — matin {H['matin']}, après-midi {H['apres_midi']}"],
        ["Pauses", f"{H['pauses']} ; déjeuner {H['dejeuner']}"],
        ["Lieu", O["lieu"]],
        ["Locaux", f"{O['lieu_equipement'].capitalize()}"],
        ["Effectif", "[À COMPLÉTER : minimum et maximum, par exemple 8 à 12 stagiaires]"],
        ["Modalité", "Présentiel"],
    ], [4.5, 12.5])
    d.h1("5. Contenu")
    d.tableau(["Code", "Module", "Rattachement", "Heures"],
              [[m["code"], m["intitule"], f"{m['bloc']} — {m['cp']}" if m["cp"] not in ("—",) else m["bloc"], heures(m)] for m in t["modules"]]
              + [["", "**Total en centre**", "", f"**{hc}**"], ["PAE", "Période en entreprise", "Tous les blocs", t["pae"]]],
              [1.8, 9.2, 3.8, 2.2])
    d.h1("6. Méthodes et moyens pédagogiques")
    d.puces([
        "Pédagogie active : études de cas réunionnais, jeux de rôle, simulations, ateliers, travail en sous-groupes.",
        "Alternance entre le centre et l'entreprise ; les productions d'examen sont construites à partir de la période en entreprise.",
        "Supports projetés en gros caractères et contrastés, transmis en version numérique accessible.",
        f"Salle de formation au Secrétariat Center : {O['lieu_equipement']} ; ordinateurs portables pour les ateliers de bureautique [À COMPLÉTER : achat ou location].",
        "Formateurs : professionnels du management, du commerce et de la gestion (CV et justificatifs tenus à disposition).",
    ])
    d.h1("7. Évaluation et validation")
    d.puces([
        "Positionnement à l'entrée, évaluations en cours de formation (prises en compte par le jury selon le référentiel d'évaluation), épreuves blanches.",
        f"Session de validation : {t['session']}.",
        "Le jury s'appuie aussi sur le dossier professionnel et sur l'entretien final.",
        "Validation totale (titre) ou partielle (un ou plusieurs CCP, capitalisables).",
        "Remise d'une attestation de fin de formation et d'un certificat de réalisation.",
    ])
    d.h1("8. Financements possibles")
    d.puces(["Compte personnel de formation (CPF)", "France Travail : AIF, action de formation conventionnée, POEI ou POEC",
             "Région Réunion : programme régional de formation [À VÉRIFIER : dispositif ouvert]",
             "OPCO de l'employeur : plan de développement des compétences, Pro-A, contrat de professionnalisation",
             "Transitions Pro Réunion : projet de transition professionnelle", "Agefiph : aides complémentaires"])
    d.p(f"Tarif : [À COMPLÉTER : prix du parcours complet, prix par CCP, coût horaire]. {O['tva']}.")
    d.h1("9. Accessibilité et handicap")
    d.p(f"Référent handicap : {O['ref_handicap']} — {O['tel']}. Un entretien confidentiel est proposé avant l'entrée pour étudier les "
        "aménagements de parcours et d'examen, avec l'Agefiph, Cap emploi et la MDPH.")
    d.h1("10. Débouchés et résultats")
    d.p(f"Emplois visés : {t['emplois']}.")
    d.p(f"Résultats nationaux : {t['insertion']}")
    d.p("Résultats YEBA FORMATIONS (satisfaction, abandon, réussite, insertion à 6 mois) : publiés après la première session.")
    d.h1("11. Contact")
    d.p(f"{O['nom']} — {O['dirigeant']} — {O['tel']} — {O['mail']}")
    d.p(O["nda_mention"], italic=True)
    d.rgpd(["RGPD : les données collectées à l'inscription servent uniquement à la gestion de la formation et aux obligations envers les financeurs (politique de confidentialité YEBA-DOC-02).",
            "IA Act : aucun système d'IA n'est utilisé pour évaluer, noter, classer ou sélectionner les stagiaires. La correction est réalisée exclusivement par le formateur."])
    return d.save(f"{_dossier(t)}/PRG-{t['code']}_Programme_de_formation.docx")


# --------------------------------------------------------------------------
def decorticage(t):
    d = Doc("Décorticage du référentiel", f"{t['intitule']} — du REAC aux objectifs pédagogiques", code=f"REAC-{t['code']}")
    d.p(f"Référence : {t['reac']}.")
    d.p("Ce document montre, compétence par compétence, comment le parcours couvre le référentiel : activité type (AT, qui correspond "
        "à un CCP), compétence professionnelle (CP), objectif pédagogique, séquences, heures et épreuve du titre. "
        "Il sert de preuve pour les indicateurs Qualiopi 5, 6 et 7 (adéquation des contenus aux exigences de la certification).")
    if t["code"] == "RPMS":
        d.encadre("Point de vigilance sur les référentiels RPMS", [
            "Les REAC et RC transmis portent sur l'ancienne version du titre (RNCP35646, millésime 07 de 2016 : 3 activités, 11 compétences).",
            "Le titre en vigueur (RNCP38575, arrêté du 5 décembre 2023) comporte 3 blocs et 9 compétences : ce décorticage suit les 9 compétences officielles de la fiche RNCP38575.",
            "Action : récupérer le REAC et le référentiel d'évaluation RPMS millésime 08 auprès de la DEETS ou sur le site du ministère du Travail, pour compléter les savoirs et les critères.",
        ])
    d.h1("1. Vue d'ensemble")
    lignes = []
    for code, bc, lib, epreuve in t["blocs"]:
        mods = [m for m in t["modules"] if m["bloc"] == code]
        lignes.append([f"**{code}**", f"**{lib}**", "", f"**{sum(heures(m) for m in mods)}**"])
        for m in mods:
            lignes.append([m["cp"], m["intitule"], m["code"], heures(m)])
    trans = [m for m in t["modules"] if m["bloc"] == "Transversal"]
    lignes.append(["**Hors CP**", "**Modules transversaux**", "", f"**{sum(heures(m) for m in trans)}**"])
    for m in trans:
        lignes.append(["—", m["intitule"], m["code"], heures(m)])
    lignes.append(["", "**Total en centre**", "", f"**{heures_centre(t)}**"])
    d.tableau(["CP", "Compétence ou module", "Module", "Heures"], lignes, [2.2, 10.3, 2.3, 2.2])
    d.h1("2. Compétence par compétence")
    for code, bc, lib, epreuve in t["blocs"]:
        d.h2(f"{code} — {lib}")
        d.p(f"**Code du bloc :** {bc}")
        d.p(f"**Épreuve du titre :** {epreuve}.")
        for m in [m for m in t["modules"] if m["bloc"] == code]:
            d.h3(f"{m['cp']} — {m['intitule']} ({heures(m)} h, module {m['code']})")
            d.p(f"**Ce que dit le référentiel :** {RESUME_CP[t['code']][m['cp']]}")
            if t["code"] == "MEM":
                d.p("**Critères d'évaluation officiels (référentiel d'évaluation v09) :**")
                d.puces(CRITERES_MEM[m["cp"]])
            else:
                d.p("**Critères d'évaluation officiels :** [À VÉRIFIER : à reprendre du référentiel d'évaluation RPMS v08].")
            d.p(f"**Objectif pédagogique général :** {m['objectif']}")
            d.p("**Objectifs pédagogiques opérationnels — à l'issue de chaque séquence, le stagiaire est capable de :**")
            d.tableau(["Jour", "Séquence", "Objectif opérationnel"],
                      [[f"J{k}", s, o] for k, (s, o) in enumerate(m["jours"], 1)], [1.5, 5.5, 10])
    d.h1("3. Compétences transversales de l'emploi")
    d.p("Selon le référentiel, les compétences transversales sont évaluées au travers des compétences professionnelles."
        if t["code"] == "MEM" else "Éléments transversaux décrits par la fiche RNCP38575.")
    d.tableau(["Compétence transversale", "Ce qui est attendu", "Où elle est travaillée"],
              [[c, desc, "Tous les modules ; mises en situation et productions"] for c, desc in t["transversales"]], [4.5, 8, 4.5])
    d.h1("4. Productions et période en entreprise exigées")
    d.puces(t["productions"])
    d.p(f"Période en entreprise : {t['pae_source']}.")
    return d.save(f"{_dossier(t)}/REAC-{t['code']}_Decorticage_referentiel_et_objectifs.docx")


# --------------------------------------------------------------------------
def deroule(t):
    jours, _ = planifier(t["code"])
    d = Doc("Déroulé pédagogique jour par jour", f"{t['intitule']} — {len(jours)} journées", code=f"DP-{t['code']}", paysage=True)
    d.p(f"Chaque journée dure {DUREE_JOUR} h : {H['matin']} et {H['apres_midi']}, pauses {H['pauses']}. "
        "Les dates tiennent compte des jours fériés (dont le 20 décembre) et de la fermeture de fin d'année. "
        "Supports de cours, ressources et grilles d'évaluation : à produire séparément.")
    courant, n = None, 0
    lignes = []

    def vider():
        if lignes:
            d.tableau(["N°", "Date", "Séquence", "Objectif pédagogique opérationnel", "Méthodes"], lignes, [1.4, 3.4, 6.2, 9.2, 5.5])
            lignes.clear()

    for date, lieu, m, k, titre, obj in jours:
        n += 1
        cle = m["code"] if m else "PAE"
        if cle != courant:
            vider()
            courant = cle
            if m:
                d.h2(f"{m['code']} — {m['intitule']} • {m['bloc']}{' — ' + m['cp'] if m['cp'] not in ('—',) else ''} • {heures(m)} h")
                d.p(f"**Objectif général :** {m['objectif']}   **Évaluation formative :** {m['evaluation']}.")
            else:
                d.h2("Période en entreprise")
                d.p("Mise en œuvre des compétences en situation réelle, sous la responsabilité d'un tuteur. "
                    "Voir le guide de la période en entreprise.")
        if m:
            lignes.append([f"J{n}", fmt_court(date), titre, obj, m["methodes"] if k == 1 else "Idem"])
        else:
            lignes.append([f"J{n}", fmt_court(date), titre, obj, "En entreprise"])
    vider()
    return d.save(f"{_dossier(t)}/DP-{t['code']}_Deroule_pedagogique_jour_par_jour.docx")


# --------------------------------------------------------------------------
def calendrier_doc(t):
    jours, sautes = planifier(t["code"])
    s1, s2 = session_examen(t["code"])
    d = Doc("Calendrier de la promotion", f"{PROMOTIONS[t['code']]['nom']} — du {fmt_court(jours[0][0])} au {fmt_court(jours[-1][0])}",
            code=f"CAL-{t['code']}")
    d.h1("1. Les grandes périodes")
    d.tableau(["Période", "Du", "Au", "Jours", "Heures", "Contenu"],
              [[lieu, fmt_court(a), fmt_court(b), nb, nb * DUREE_JOUR, ", ".join(mods) if mods else "Période en entreprise"]
               for lieu, a, b, nb, mods in periodes(t["code"])]
              + [["Examen", fmt_court(s1), fmt_court(s2), "—", "—", "Session de validation [À VÉRIFIER]"]],
              [2.6, 2.4, 2.4, 1.6, 2, 6])
    d.h1("2. Jours non travaillés pendant la formation")
    d.tableau(["Date", "Motif"], [[fmt(x), m] for x, m in sautes] or [["—", "Aucun"]], [6, 11])
    d.h1("3. Semaine par semaine")
    lignes = []
    for lundi, js in semaines(t["code"]):
        lieu = js[0][1] if all(j[1] == js[0][1] for j in js) else "Mixte"
        mods = []
        for _, l, m, _ in js:
            c = m["code"] if m else "PAE"
            if c not in mods:
                mods.append(c)
        lignes.append([fmt_court(lundi), lieu, len(js), len(js) * DUREE_JOUR, " + ".join(mods)])
    d.tableau(["Semaine du", "Lieu", "Jours", "Heures", "Modules"], lignes, [3, 3, 2, 2, 7])
    d.h1("4. Coût de location de la salle")
    nb = sum(1 for j in jours if j[1] == "Centre")
    d.p(f"{nb} journées en centre × {H['location_jour']} € = **{nb * H['location_jour']:,} €**".replace(",", " ")
        + " (hors jours d'information collective, de jury blanc et d'examen).")
    return d.save(f"{_dossier(t)}/CAL-{t['code']}_Calendrier_promotion.docx")


# --------------------------------------------------------------------------
def livret(t):
    jours, _ = planifier(t["code"])
    s1, s2 = session_examen(t["code"])
    d = Doc("Livret d'accueil du stagiaire", f"{t['intitule']} — {PROMOTIONS[t['code']]['nom']}", code=f"LIV-{t['code']}", couverture=True)
    d.h1("Bienvenue")
    d.p(f"Vous entrez en formation pour préparer le **{t['intitule'].lower()}**, un titre de niveau 5 délivré par le ministère du Travail. "
        f"Pendant {round(len(jours) / 21)} mois environ, vous allez alterner le centre de formation et l'entreprise. "
        "Ce livret rassemble tout ce qu'il faut savoir pour réussir. Gardez-le avec vous.")
    d.h1("1. Qui sommes-nous ?")
    d.p(f"{O['nom']} est un organisme de formation réunionnais créé en 2021 et dirigé par {O['dirigeant']}. "
        "Nos domaines : vente, management, compétences comportementales, intelligence artificielle et gouvernance des données.")
    d.tableau(["Nos références", ""], [
        ["Statut", f"{O['forme']} — SIRET {O['siret']}"],
        ["Déclaration d'activité", f"NDA {O['nda']} (préfet de région de La Réunion)"],
        ["Certification qualité", f"Qualiopi n° {O['qualiopi']}"],
        ["Directeur", O["dirigeant"]],
    ], [5, 12])
    d.h1("2. Vos interlocuteurs")
    d.tableau(["Rôle", "Nom", "Contact"], [
        ["Directeur et responsable pédagogique", O["dirigeant"], O["tel"]],
        ["Référent handicap", O["dirigeant"], O["tel"]],
        ["Formateurs", O["dirigeant"], O["mail"]],
        ["Données personnelles", "—", O["contact_rgpd"]],
        ["Vos délégués des stagiaires", "Élus entre la 20e et la 40e heure", "—"],
    ], [6, 5, 6])
    d.h1("3. Lieu, horaires et pauses")
    d.tableau(["", ""], [
        ["Adresse", O["lieu"]],
        ["Horaires", H["journee"]],
        ["Matin", H["matin"]],
        ["Après-midi", H["apres_midi"]],
        ["Pauses", H["pauses"]],
        ["Déjeuner", H["dejeuner"]],
        ["Accès", "[À COMPLÉTER : lignes de bus, stationnement]"],
        ["Équipements", O["lieu_equipement"].capitalize()],
        ["Repas", "Salle de pause sur place ; repas interdits dans la salle de formation"],
    ], [4, 13])
    d.h1("4. Le déroulé de votre année de formation")
    d.p(f"Début : **{fmt(jours[0][0])}** — fin : **{fmt(jours[-1][0])}** — examen : **semaine du {fmt_court(s1)}** [À VÉRIFIER].")
    d.tableau(["Étape", "Dates", "Ce que vous faites"],
              [[("Au centre" if lieu == "Centre" else "En entreprise"), f"du {fmt_court(a)} au {fmt_court(b)}",
                ", ".join(f"{t2['intitule']}" for t2 in [m for m in t["modules"] if m["code"] in mods]) or "Période en entreprise avec votre tuteur"]
               for lieu, a, b, nb, mods in periodes(t["code"])]
              + [["Examen", f"du {fmt_court(s1)} au {fmt_court(s2)}", "Session de validation du titre"],
                 ["Après", "à 3 et 6 mois", "Questionnaires de suivi et d'insertion"]],
              [3.2, 4.8, 9])
    d.h2("Les jalons à ne pas manquer")
    d.cases([
        "Semaine 1 : remise du règlement intérieur, de la charte IA et signature du contrat d'engagement.",
        "Entre la 20e et la 40e heure : élection de vos délégués.",
        "Avant la 1re période en entreprise : convention signée et objectifs écrits avec votre tuteur.",
        "Pendant les périodes en entreprise : recueillir les éléments de vos productions d'examen (voir le guide).",
        "Bilan de mi-parcours : entretien individuel avec le responsable pédagogique.",
        "Avant l'examen : dossier professionnel, productions et attestation de période en entreprise complets.",
    ])
    d.h1("5. Votre titre et vos épreuves")
    d.tableau(["Bloc", "Intitulé", "Comment il est évalué"], [[c, lib, ep] for c, bc, lib, ep in t["blocs"]], [2, 7, 8])
    d.p(f"Durée totale de l'épreuve : {t['session']}.")
    d.p("**À préparer avant l'examen :**")
    d.puces(t["productions"])
    d.h2("Les documents qui vous sont remis")
    d.puces(["Le programme et ce livret d'accueil",
             "Le règlement intérieur (YEBA-DOC-04) et son avenant pour les parcours certifiants (RI-06)",
             "La politique de confidentialité (YEBA-DOC-02) et la charte d'usage de l'IA (YEBA-DOC-11)",
             "La politique handicap et accessibilité (YEBA-DOC-08) et la procédure de réclamation (YEBA-DOC-09)",
             "La fiche « Vos droits en santé et sécurité » (SST-18)"])
    d.h1("6. Vos droits et vos devoirs")
    d.puces([
        "Être présent et ponctuel ; signer la feuille d'émargement chaque demi-journée.",
        "Prévenir le centre avant 8 h 30 en cas d'absence et fournir un justificatif sous 48 h.",
        "Respecter le règlement intérieur, les personnes et les locaux.",
        "Utiliser l'intelligence artificielle uniquement selon la charte IA : jamais de données personnelles dans un outil non validé ; vos productions d'examen restent votre travail personnel.",
        "Faire une réclamation à tout moment : formulaire disponible, réponse sous 15 jours ouvrés.",
        "Être accompagné en cas de handicap ou de difficulté : parlez-en au référent, en toute confidentialité.",
    ])
    d.h1("7. Santé et sécurité")
    d.puces([
        "Consignes d'évacuation affichées dans la salle ; repérez les sorties de secours.",
        "Alerte cyclonique orange ou alerte rouge forte pluie : la session est suspendue immédiatement et vous regagnez votre domicile. Alerte rouge : aucun déplacement. La journée est reportée sans frais (règlement intérieur YEBA-DOC-04, article 5).",
        "En entreprise : respect des consignes de sécurité, port des équipements de protection, droit d'alerte et de retrait en cas de danger grave et imminent.",
        "Tout accident, même léger, est signalé immédiatement au centre.",
    ])
    d.h1("8. Vos données personnelles")
    d.p("Vos données servent à gérer votre formation, votre examen et les obligations envers les financeurs. Elles ne sont jamais vendues ni "
        f"saisies dans un outil d'IA. Vous pouvez exercer vos droits auprès de {O['contact_rgpd']}. Aucune décision vous concernant n'est prise par une IA.")
    d.h1("9. Aides et partenaires")
    d.puces(["Mission Locale, France Travail, Cap emploi, Agefiph, MDPH", "CAF : aides à la garde d'enfants",
             "Aides à la mobilité : [À COMPLÉTER : dispositifs locaux]", "Numéros utiles : SAMU 15, pompiers 18, police 17, urgence européenne 112"])
    d.h1("10. Votre premier jour")
    d.cases(["Pièce d'identité", "Convocation", "De quoi prendre des notes", "Une clé USB ou un espace de stockage personnel",
             "Votre CV à jour", "Votre identifiant France Travail si vous êtes demandeur d'emploi"])
    d.signatures(["J'ai reçu ce livret — le stagiaire"])
    return d.save(f"{_dossier(t)}/LIV-{t['code']}_Livret_accueil_stagiaire.docx")


# --------------------------------------------------------------------------
ELEMENTS_PAE = {
    "MEM": [
        ("Présentation de l'établissement", "Une page : activité, taille, périmètre confié, organisation."),
        ("CP1 Animer l'équipe", "Exemples de consignes et leurs effets ; préparation et déroulé de briefings ; outils de motivation ; amélioration continue."),
        ("CP2 Planifier et coordonner", "Méthode d'évaluation des besoins ; exemple de planning (anonymisé) ; gestion d'un imprévu ; mesures de prévention."),
        ("CP3 Performance individuelle", "Méthode d'évaluation des compétences ; exemple de plan d'accompagnement (anonymisé)."),
        ("CP4 Recrutement et intégration", "Exemple de fiche de poste ; parcours d'intégration ; organisation du tutorat ; suivi de période d'essai."),
        ("CP8 Performance commerciale", "Indicateurs suivis, sources des données, écarts, alertes, rythme de reporting."),
        ("CP9 Rentabilité", "Données économiques disponibles, indicateurs, écarts et causes, pistes d'optimisation."),
        ("CP10 Plan d'actions", "Plan d'actions réel ou proposé, preuves de mise en œuvre (plannings, comptes rendus, photos sans personnes), résultats."),
    ],
    "RPMS": [
        ("Présentation de la structure", "Activité, forme juridique, gouvernance, effectif, territoire."),
        ("Bloc 1 Diriger une structure", "Diagnostic de la structure, parties prenantes, organisation de l'équipe, actions de management."),
        ("Bloc 2 Objet social", "Analyse de l'offre et du marché, actions commerciales, organisation de la production."),
        ("Bloc 3 Rapport d'activité", "Bilan et compte de résultat (avec accord du dirigeant), indicateurs, éléments du rapport d'activité."),
    ],
}


def guide_pae(t):
    blocs = [b for b in periodes(t["code"]) if b[0] == "Entreprise"]
    d = Doc("Guide de la période en entreprise", f"{t['intitule']} — pour le stagiaire et le tuteur", code=f"GPE-{t['code']}")
    d.h1("1. Pourquoi cette période ?")
    d.p(f"La période en entreprise est **obligatoire** pour se présenter à l'examen : {t['pae_source']}. "
        "Le stagiaire y met en œuvre ses compétences et recueille les éléments de ses productions d'examen. "
        "Il présente une preuve de cette période au responsable de session.")
    d.h1("2. Dates")
    d.tableau(["Période", "Du", "Au", "Heures"],
              [[f"Période n° {i}", fmt(a), fmt(b), nb * DUREE_JOUR] for i, (l, a, b, nb, _) in enumerate(blocs, 1)], [3, 5.5, 5.5, 3])
    d.p("Horaires : ceux de l'entreprise, dans la limite de 35 heures par semaine et des règles applicables aux stagiaires.")
    d.h1("3. Le rôle de chacun")
    d.tableau(["Acteur", "Engagements"], [
        ["Stagiaire", "Être présent et ponctuel ; respecter le règlement de l'entreprise ; tenir un carnet de bord ; recueillir les éléments listés ci-dessous ; prévenir le centre de toute difficulté."],
        ["Tuteur", "Accueillir et présenter l'entreprise ; confier des activités en lien avec le titre ; faire un point chaque semaine ; signer l'attestation de période en entreprise."],
        [O["nom"], "Signer la convention ; appeler ou visiter le tuteur à mi-période ; aider le stagiaire à exploiter ses observations ; traiter tout incident."],
    ], [3.5, 13.5])
    d.h1("4. Activités à confier et éléments à recueillir")
    d.tableau(["Domaine", "Éléments à recueillir pour les productions"], [list(x) for x in ELEMENTS_PAE[t["code"]]], [5, 12])
    d.h1("5. Confidentialité et données personnelles")
    d.puces([
        "Les documents d'examen n'affichent aucun nom de salarié ou de client : remplacer par des initiales ou des fonctions.",
        "Les chiffres de l'entreprise ne sont utilisés qu'avec l'accord du tuteur ; ils peuvent être arrondis ou indexés.",
        "Ne saisir aucune donnée de l'entreprise dans un outil d'intelligence artificielle non validé.",
        "Les photos de rayons ou de locaux ne montrent aucune personne identifiable.",
    ])
    d.h1("6. Suivi par le centre")
    d.cases(["Convention signée avant le premier jour", "Objectifs écrits et validés par le tuteur",
             "Appel ou visite à mi-période (compte rendu)", "Attestation de période en entreprise signée le dernier jour"])
    d.rgpd(["RGPD : le stagiaire réutilise des informations de l'entreprise ; anonymisation obligatoire dans les productions.",
            "IA Act : l'usage éventuel de l'IA dans les productions est déclaré par le stagiaire ; la décision reste humaine."])
    return d.save(f"{_dossier(t)}/GPE-{t['code']}_Guide_periode_en_entreprise.docx")


def tout():
    out = []
    for t in (MEM, RPMS):
        out += [programme(t), decorticage(t), deroule(t), calendrier_doc(t), livret(t), guide_pae(t)]
    return out


if __name__ == "__main__":
    from lib import ERREURS_MISE_EN_PAGE
    for f in tout():
        print(f.name)
    print("\n".join(ERREURS_MISE_EN_PAGE) or "Mise en page : aucun mot coupé")

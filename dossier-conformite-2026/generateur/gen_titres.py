"""Programme, déroulé pédagogique + grilles critériées, planning horaire par titre."""
from lib import Doc, ORGANISME
from titres import MEM, RPMS, heures_centre, planning

LIBELLES = None


def _libelles(t):
    return {m[0]: m[1] for m in t["modules"]} | {"PAE": "Période en entreprise (stage)"}


def programme(t):
    hc = heures_centre(t)
    d = Doc(f"Programme de formation — {t['intitule']}",
            f"{t['rncp']} • {t['niveau']} • {hc} h en centre + {t['pae']} h en entreprise",
            code=f"PRG-{t['code']}")
    d.h1("1. Identification")
    d.tableau(["Rubrique", "Information"], [
        ["Certification", f"{t['intitule']} — {t['rncp']}"],
        ["Certificateur", t["certificateur"]],
        ["Niveau", t["niveau"]],
        ["Texte de référence", t["arrete"]],
        ["Codes ROME", t["rome"]],
        ["Organisme de formation", f"{ORGANISME['nom']} — NDA {ORGANISME['nda']} — Qualiopi {ORGANISME['qualiopi']} (catégorie : actions de formation)"],
        ["Centre d'examen", "[À COMPLÉTER : YEBA FORMATIONS si agrément DEETS obtenu pour ce titre, sinon centre agréé partenaire]"],
    ], [5, 12])
    d.h1("2. Public et conditions d'accès")
    d.p(t["public"])
    d.h3("Prérequis et admission")
    d.puces(t["prerequis"])
    d.h3("Délais d'accès")
    d.puces([
        "Information collective : [À COMPLÉTER : dates] ; réponse à la candidature sous 10 jours ouvrés après l'entretien.",
        "Financement CPF : respect du délai minimal imposé par Mon Compte Formation entre la proposition et l'entrée en formation [À VÉRIFIER : délai en vigueur sur EDOF].",
        "Financement France Travail (AIF) : dépôt du devis sur KAIROS au moins 15 jours avant le démarrage [À VÉRIFIER : délai local France Travail Réunion].",
    ])
    d.h1("3. Objectifs — compétences visées")
    for code, lib in t["blocs"]:
        d.h3(f"{code} : {lib}")
        comps = [m for m in t["modules"] if m[3] == code.split(" ")[0]]
        d.puces([f"{m[1]} — {m[4]}" for m in comps])
    d.h3("Compétences transversales (plus-value YEBA FORMATIONS)")
    d.puces([f"{m[1]} ({m[2]} h)" for m in t["modules"] if m[3] == "Transversal"])
    d.h1("4. Durée, rythme et organisation")
    d.tableau(["Élément", "Valeur"], [
        ["Durée en centre", f"{hc} heures"],
        ["Période en entreprise", f"{t['pae']} heures — {t['pae_source']}"],
        ["Durée totale du parcours", f"{hc + t['pae']} heures (hors session d'examen)"],
        ["Rythme", "35 h / semaine — [À COMPLÉTER : horaires, ex. 8 h 00 – 12 h 00 / 13 h 00 – 16 h 00]"],
        ["Pauses", "[À COMPLÉTER : ex. 15 min le matin, 15 min l'après-midi]"],
        ["Dates de session", "[À COMPLÉTER : date de début — date de fin]"],
        ["Lieu", "[À COMPLÉTER : adresse des locaux ; accessibilité PMR]"],
        ["Effectif", "[À COMPLÉTER : minimum / maximum, ex. 8 à 14 stagiaires]"],
        ["Modalité", "Présentiel (possibilité de modules à distance synchrones : [À COMPLÉTER])"],
        ["Épreuves du titre", t["session"]],
    ], [5, 12])
    d.h1("5. Contenu (modules et volumes horaires)")
    d.tableau(["Code", "Module", "Bloc", "Heures"],
              [[m[0], m[1], m[3], m[2]] for m in t["modules"]] +
              [["", "**Total en centre**", "", f"**{hc}**"], ["PAE", "Période en entreprise", "Tous", t["pae"]]],
              [1.6, 10, 3, 2.2])
    d.h1("6. Méthodes et moyens pédagogiques")
    d.puces([
        "Pédagogie active : études de cas réunionnais, jeux de rôle, simulations, ateliers en sous-groupes, classe inversée.",
        "Projet fil rouge relié à la période en entreprise.",
        "Supports projetés en gros caractères, contrastés, transmis en version numérique accessible.",
        "Salle équipée : [À COMPLÉTER : postes informatiques, vidéoprojecteur, connexion, logiciels bureautiques].",
        "Formateurs : professionnels du management, du commerce et de la gestion — CV et justificatifs tenus à disposition (Qualiopi indicateur 21).",
    ])
    d.h1("7. Modalités d'évaluation et de validation")
    d.puces([
        "Positionnement à l'entrée (non éliminatoire), évaluations formatives à la fin de chaque module (grilles critériées), épreuves blanches.",
        f"Session de validation organisée selon l'arrêté du 22 décembre 2015 modifié : {t['session']}.",
        "Validation totale (titre) ou partielle (un ou plusieurs CCP capitalisables, sans limite de durée de validité dans le cadre du titre en vigueur).",
        "Délivrance : titre ou CCP délivré par le ministère chargé de l'emploi ; attestation de fin de formation et certificat de réalisation remis par l'organisme.",
    ])
    d.h1("8. Financements possibles")
    d.puces([
        "Compte personnel de formation (CPF) — titre éligible par principe (certification RNCP).",
        "France Travail : aide individuelle à la formation (AIF), action de formation conventionnée, préparation opérationnelle à l'emploi (POEI / POEC).",
        "Région Réunion : programme régional de formation des demandeurs d'emploi [À VÉRIFIER : marché ou dispositif ouvert en 2026-2027].",
        "OPCO de l'employeur : plan de développement des compétences, Pro-A, contrat de professionnalisation.",
        "Transitions Pro Réunion : projet de transition professionnelle (PTP).",
        "Agefiph : aides complémentaires pour les personnes en situation de handicap.",
    ])
    d.p("Tarif : [À COMPLÉTER : prix total TTC/exonéré ; prix par CCP ; coût horaire]. "
        "Exonération de TVA : [À VÉRIFIER : attestation d'exonération TVA formation professionnelle (art. 261-4-4° du CGI)].")
    d.h1("9. Accessibilité et handicap")
    d.p(f"Référent handicap : {ORGANISME['ref_handicap']} — {ORGANISME['tel']}. Entretien confidentiel avant l'entrée pour étudier les aménagements "
        "(rythme, supports agrandis, temps majoré aux épreuves selon la réglementation des titres professionnels, matériel adapté), "
        "en lien avec l'Agefiph, Cap emploi et la MDPH.")
    d.h1("10. Débouchés, suites de parcours et résultats")
    d.p(f"Emplois visés : {t['emplois']}.")
    d.p(f"Indicateurs nationaux : {t['insertion']}.")
    d.p("Indicateurs YEBA FORMATIONS (publiés et mis à jour après chaque session — Qualiopi indicateur 2) : taux de satisfaction, taux d'abandon, "
        "taux de réussite au titre, taux d'insertion à 6 mois : [À COMPLÉTER après la 1re session — ne jamais publier de chiffre estimé].")
    d.h1("11. Contact")
    d.p(f"{ORGANISME['nom']} — {ORGANISME['adresse']} — {ORGANISME['tel']} — {ORGANISME['mail']}")
    d.rgpd([
        "RGPD : les données collectées à l'inscription servent uniquement à la gestion de la formation et aux obligations envers les financeurs (art. 6.1.b et 6.1.c RGPD). Voir la mention d'information jointe à la fiche d'inscription.",
        "IA Act : aucune décision d'admission, d'orientation ou d'évaluation n'est prise par un système d'IA (ces usages relèvent de l'annexe III, point 3 — haut risque). Les décisions sont prises par une personne habilitée.",
    ])
    return d.save(f"02_{t['code']}/PRG-{t['code']}_Programme_de_formation.docx")


GRILLE_NIVEAUX = ["Non acquis (0)", "En cours (1)", "Acquis (2)", "Maîtrisé (3)"]


def deroule(t):
    d = Doc(f"Déroulé pédagogique et grilles critériées — {t['intitule']}", f"{t['rncp']} • Version formateur", code=f"DP-{t['code']}")
    d.p("Ce déroulé détaille, module par module, l'objectif opérationnel, les contenus, les méthodes (avec un exemple concret ou ludique), "
        "l'évaluation formative et la durée. Il sert de preuve pour les indicateurs Qualiopi 5, 6, 10 et 11.")
    for m in t["modules"]:
        code, lib, h, bloc, obj, contenus, methodes, evalu = m
        d.h2(f"{code} — {lib} ({h} h) • {bloc}")
        d.p(f"**Objectif opérationnel :** à l'issue du module, le stagiaire est capable de : {obj[0].lower() + obj[1:]}")
        d.p("**Contenus :**")
        d.puces(contenus)
        d.p(f"**Méthodes et exemple marquant :** {methodes}")
        d.p(f"**Évaluation formative :** {evalu}")
        d.p("**Supports :** diaporama en gros caractères (mots-clés), fiche mémo PDF accessible, cas pratiques. **Formateur :** [À COMPLÉTER]")
    d.saut()
    d.h1("Grilles critériées par bloc de compétences")
    d.p("Échelle : 0 = non acquis • 1 = en cours d'acquisition • 2 = acquis • 3 = maîtrisé. Seuil de réussite conseillé : aucune ligne à 0 et moyenne ≥ 2. "
        "La grille est remplie par le formateur ; le stagiaire la commente et la signe. Aucune notation automatisée par IA.")
    for code_bloc, lib in t["blocs"]:
        d.h2(f"{code_bloc} — {lib}")
        lignes = []
        for m in t["modules"]:
            if m[3] == code_bloc.split(" ")[0]:
                lignes.append([m[1], m[4], "", "", "", ""])
        d.tableau(["Compétence", "Critère observable"] + GRILLE_NIVEAUX, lignes, [3.5, 5.5, 2, 2, 2, 2])
        d.p("Commentaire du formateur : ____________________________________________")
        d.signatures(["Stagiaire", "Formateur"])
    return d.save(f"02_{t['code']}/DP-{t['code']}_Deroule_pedagogique_et_grilles.docx")


def planning_doc(t):
    lib = _libelles(t)
    pl = planning(t)
    hc = heures_centre(t)
    d = Doc(f"Décomposition des heures et planning — {t['intitule']}",
            f"{len(pl)} semaines • {hc} h centre + {t['pae']} h entreprise", code=f"PLN-{t['code']}")
    d.h1("1. Planning semaine par semaine (option A : temps plein 35 h)")
    lignes = []
    for n, ty, contenu in pl:
        tot = sum(h for _, h in contenu)
        txt = " + ".join(f"{c} {lib[c]} ({h} h)" for c, h in contenu)
        note = "" if tot == 35 else f"Semaine de {tot} h : temps restant = rattrapage / tutorat individuel"
        lignes.append([f"S{n}", "🏫 Centre" if ty == "Centre" else "🏢 Entreprise", txt, tot, note])
    lignes.append(["S" + str(len(pl) + 1), "📝 Examen", "Session de validation du titre", "—", t["session"]])
    d.tableau(["Sem.", "Lieu", "Contenu", "Heures", "Remarque"], lignes, [1.6, 2.8, 7.2, 2.0, 3.4])
    d.h1("2. Autres rythmes possibles (à trancher)")
    d.tableau(["Option", "Rythme", "Durée calendaire", "Pour qui"], [
        ["A (défaut)", "Temps plein 35 h / semaine", f"≈ {len(pl) + 1} semaines (≈ 6 mois)", "Demandeurs d'emploi (France Travail, Missions Locales, Région)"],
        ["B", "Temps partiel 21 h / semaine (3 jours)", f"≈ {round((hc) / 21 + t['pae'] / 35) + 1} semaines (≈ 9-10 mois)", "Parents, personnes avec contraintes de santé, salariés à temps partiel"],
        ["C", "Par blocs (CCP) séparés", "1 CCP par trimestre", "Salariés en CPF / plan de développement des compétences"],
    ], [2.2, 4.5, 4, 6.3])
    d.h1("3. Rétroplanning de l'organisme (étapes réalistes pour le dirigeant)")
    d.p("Chaque ligne = une action à cocher. Les échéances sont calculées à partir de la date d'examen (J) ou du démarrage (D).")
    d.cases([
        "J − 7 mois : déposer la demande d'agrément de session à la DEETS 974 (démarche en ligne « DEETS 974 — demande d'agrément pour organiser des sessions ») ou signer un partenariat avec un centre agréé.",
        "D − 3 mois : publier la fiche formation (site, Carif-Oref, EDOF / Mon Compte Formation, KAIROS France Travail) ; informer Missions Locales et agences France Travail.",
        "D − 2 mois : 2 informations collectives ; tests de positionnement ; entretiens individuels.",
        "D − 1 mois : valider les financements (devis, accords de prise en charge) ; constituer les dossiers stagiaires.",
        "D − 15 jours : envoyer convocations, livret d'accueil, règlement intérieur, programme ; vérifier salle et matériel.",
        "D − 3 jours : préparer les feuilles d'émargement, les supports du module M0, le kit de bienvenue.",
        "D : accueil, attestations d'entrée, déclaration d'entrée sur les plateformes financeurs (EDOF / KAIROS).",
        "Chaque vendredi : émargements numérisés, suivi des absences, relance immédiate en cas d'absence (prévention du décrochage).",
        "J − 3 mois et 1 jour : saisie de la session dans CERES (si centre agréé) [À VÉRIFIER : délai communiqué par la DEETS].",
        "Avant chaque période en entreprise : conventions signées, objectifs écrits, visite ou appel du tuteur à mi-période.",
        "J − 15 jours : dossiers professionnels complets ; preuves de période en entreprise réunies.",
        "J + 1 semaine : certificats de réalisation, attestations de fin de formation, évaluation à chaud ; facturation finale.",
        "J + 6 mois : enquête d'insertion ; mise à jour des indicateurs publiés.",
    ])
    d.encadre("💡 Plan B si vous êtes en retard sur le programme", [
        "1. Ne jamais supprimer d'heures facturées : basculer le contenu non traité sur les semaines incomplètes (rattrapage) ou sur la semaine T5.",
        "2. Priorité absolue aux compétences évaluées à l'examen (CCP) avant les modules de confort.",
        "3. Documenter tout changement (avenant au planning signé par les stagiaires) : c'est une preuve Qualiopi, pas une faute.",
        "4. Préparer chaque module 2 semaines à l'avance (supports + cas) : bloquer un créneau fixe dans votre agenda (ex. le mercredi 14 h – 17 h).",
    ])
    return d.save(f"02_{t['code']}/PLN-{t['code']}_Decomposition_heures_planning.docx")


def tout():
    out = []
    for t in (MEM, RPMS):
        out += [programme(t), deroule(t), planning_doc(t)]
    return out


if __name__ == "__main__":
    for f in tout():
        print(f)

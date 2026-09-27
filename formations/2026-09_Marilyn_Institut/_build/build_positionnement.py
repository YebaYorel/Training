"""Analyse des tests de positionnement — rapport interne, synthèse anonymisée, fiche Indicateur 8.

Source des réponses : exports Drag'n Survey déposés sur Drive le 27/09/2026 (5 répondantes sur 8).
"""
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import donnees as D
from docx_lib import Doc, BLEU, ROUGE, GRIS
from docx.shared import Cm

OUT = D.SORTIE / "01_POSITIONNEMENT_ET_INDICATEUR_8"


def repondantes():
    return [s for s in D.stagiaires() if s["test"]]


def stats_items():
    reps = repondantes()
    res = []
    for i, item in enumerate(D.AUTO_ITEMS):
        vals = [s["test"]["auto"][i] for s in reps]
        res.append({"item": item, "moy": st.mean(vals), "min": min(vals), "max": max(vals),
                    "ecart": st.pstdev(vals), "bas": sum(v <= 2 for v in vals), "vals": vals})
    return res


def graphique(chemin):
    s = stats_items()
    ordre = sorted(s, key=lambda x: x["moy"])
    prio = {x["item"] for x in ordre[:3]}
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=200)
    y = range(len(ordre))
    couleurs = ["#1B3A6B" if x["item"] in prio else "#7A8496" for x in ordre]
    ax.barh(list(y), [x["moy"] for x in ordre], color=couleurs, height=0.62)
    ax.set_yticks(list(y))
    ax.set_yticklabels([x["item"] for x in ordre], fontsize=10, color="#121212")
    for i, x in enumerate(ordre):
        lab = f"{x['moy']:.1f}".replace(".", ",") + ("   ← priorité" if x["item"] in prio else "")
        ax.text(x["moy"] + 0.06, i, lab, va="center", fontsize=10, color="#121212",
                fontweight="bold" if x["item"] in prio else "normal")
    ax.set_xlim(0, 5.9)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.tick_params(axis="x", colors="#5A5F6A", labelsize=9)
    ax.grid(axis="x", color="#E3E6EB", linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#BFC5CF")
    ax.set_xlabel("Aisance déclarée — moyenne sur 5 (5 répondantes)", fontsize=10, color="#5A5F6A")
    fig.tight_layout()
    fig.savefig(chemin)
    plt.close(fig)


def f1(x):
    return f"{x:.1f}".replace(".", ",")


# --------------------------------------------------------------------------- décisions
ADAPTATIONS = [
    ("« Parler du chiffre d'affaires et des objectifs de l'institut » : moyenne la plus basse (2,8/5) ; 3 répondantes sur 5 à 2 ou moins.",
     "Ajout d'un atelier de 10 min « Mon agenda, mes chiffres » : calculer sur un exemple fictif ce que rapporte une reprise de rendez-vous. Objectif 9 travaillé de façon concrète, sans chiffre réel de l'institut.",
     "Y — « Y revenir » (14h30)"),
    ("« Recevoir une remarque sans me braquer » : 3,0/5, avec une cotation à 1/5.",
     "Exercice « Le Boomerang » (méthode A.R.P.) joué d'abord en binôme, pas devant le groupe. Remarques graduées de « douce » à « ferme ». Droit au joker.",
     "N — « Nous » (15h40)"),
    ("« Recommander sans forcer » et « c'est trop cher » : 3,2/5 chacun ; deux cotations à 2/5.",
     "Séquence « Le Lien » portée à 75 minutes. Ajout du « Ring des objections » : 10 cartes à découper, chacune jouée 3 fois.",
     "L — « Le Lien » (13h15)"),
    ("Question « combien de produits recommander en fin de soin ? » : 2 réponses sur 5 donnent « 2 » au lieu d'« un seul ».",
     "Règle « UNE seule chose » (lettre R de P.E.R.L.E.) : une diapositive dédiée, une démonstration, et la question 5 du quiz.",
     "L — « Le Lien »"),
    ("« Soigner ma tenue, ma voix, ma posture » : 3,2/5. Deux répondantes veulent gagner en aisance orale (« savoir quoi répondre sans perdre mes moyens », « que ce soit fluide »).",
     "Création d'un carnet de « phrases d'appui » : formulations prêtes à l'emploi, lisibles pendant les jeux de rôle. Temps de préparation de 1 minute avant chaque scène. Personne ne joue devant le groupe sans l'avoir d'abord fait en binôme.",
     "M, A, L (toute la journée)"),
    ("« Proposer le prochain rendez-vous » : 4,8/5, point fort du groupe.",
     "Séquence « Y revenir » réduite (30 min au lieu de 35) : le groupe est expert et rédige lui-même le standard « La Phrase qui Rebooke ». Le temps gagné va au Ring des objections.",
     "Y — « Y revenir »"),
    ("Situation vécue : organisation entre deux rendez-vous quand le planning est plein et qu'on est seule à l'institut.",
     "Ajout de la « check-list 60 secondes entre deux clientes » dans la séquence Initiative et dans la ressource PDF.",
     "I — « Initiative » (15h15)"),
    ("Situations vécues : communication dans l'équipe, place laissée aux idées de chacune.",
     "Dans le jeu des 7 Merveilles, un des 10 standards communs est réservé à un rituel d'équipe (ex. : 5 minutes d'idées par semaine). Standard proposé à la direction, non imposé.",
     "N — « Nous »"),
    ("Niveaux hétérogènes : de 1 an à plus de 20 ans d'ancienneté ; une répondante cote tout à 5/5 et souhaite prendre des responsabilités.",
     "Binômes mixtes (ancienneté forte + récente). Rôle d'« observatrice experte » avec la grille critériée pour les plus expérimentées.",
     "Jeux de rôle (toute la journée)"),
    ("3 stagiaires sur 8 n'ont pas répondu au questionnaire.",
     "Fiche « Positionnement express » papier (10 situations, 2 minutes) remplie par toutes à 8h30 et de nouveau à 16h40 : positionnement des absentes au test ET mesure de la progression de chacune.",
     "Ouverture et clôture"),
    ("Aménagements : 3 répondantes sur 5 signalent un besoin sur leur poste de travail à l'institut (table et chaise de prothésie ongulaire). Aucune demande ne concerne la formation elle-même.",
     "En salle : chaises à dossier, toutes les activités se font assises ou debout, au choix, et chacune peut prendre une pause à tout moment (mesures valables pour tout le groupe). Pour les postes à l'institut : remontée collective et anonyme à l'employeur, avec l'accord des intéressées (obligation de sécurité de l'employeur, art. L.4121-1 du code du travail).",
     "Logistique et synthèse employeur"),
]


def rapport_interne():
    doc = Doc("Rapport d'analyse du positionnement", "Usage interne YEBA FORMATIONS — CONFIDENTIEL",
              f"Action {D.ACTION['reference']} — convention {D.ACTION['convention']}", corps=11, mention_eval=True)
    reps = repondantes()
    doc.encadre("Confidentialité", [
        "Document nominatif, réservé au formateur. Ne pas transmettre à l'employeur : seule la synthèse anonymisée lui est remise (convention, art. 9).",
        "Conservation : 3 ans au dossier de l'action, puis destruction. Aucune donnée de santé n'est reportée ici : seuls les aménagements le sont.",
    ], taille=10)
    doc.h1("1. Périmètre de l'analyse")
    doc.table([
        ["Élément", "Valeur"],
        ["Outil de collecte", "Drag'n Survey (éditeur français) — exports déposés sur Drive le 27/09/2026"],
        ["Questionnaires attendus", "8 (4 par session)"],
        ["Réponses reçues", f"{len(reps)} — " + ", ".join(D.nom_complet(s) for s in reps)],
        ["Non-répondantes", ", ".join(D.nom_complet(s) for s in D.stagiaires() if not s["test"])
         + " → positionnement express papier le jour J à 8h30"],
        ["Échelle", "Auto-positionnement de 1 (pas du tout à l'aise) à 5 (totalement à l'aise) sur 10 situations ; 5 questions de connaissances"],
        ["Date de l'analyse", "27/09/2026 — Aurélien LUMEKA"],
    ], [5, 12], taille=10)

    doc.h1("2. Auto-positionnement : le groupe")
    png = OUT / "_graphique_positionnement.png"
    OUT.mkdir(parents=True, exist_ok=True)
    graphique(png)
    doc.d.add_picture(str(png), width=Cm(17))
    lignes = [["Situation", "Moy.", "Min", "Max", "≤ 2"]]
    for x in sorted(stats_items(), key=lambda x: x["moy"]):
        lignes.append([x["item"], f1(x["moy"]), str(x["min"]), str(x["max"]), str(x["bas"])])
    doc.table(lignes, [10.5, 1.6, 1.4, 1.4, 1.5], taille=10, centre_cols=(1, 2, 3, 4))

    doc.h1("3. Connaissances (5 questions)")
    lignes = [["Notion", "Bonnes réponses", "Lecture"]]
    lecture = {
        "q_premiere_impression": "Acquis, à ancrer pour tout le groupe (séquence 0).",
        "q_caracteristique": "Acquis en théorie ; la pratique (transformer en bénéfice) reste à entraîner.",
        "q_trop_cher": "Bon réflexe connu ; l'aisance déclarée reste moyenne (3,2/5) : écart entre savoir et faire.",
        "q_un_produit": "Point faible : 2 sur 5 recommandent 2 produits → règle « une seule chose ».",
        "q_sante": "Acquis. Attention : la question posée (« produit issu du corps médical ») ne correspondait pas à la réponse attendue → question à corriger dans le formulaire.",
    }
    for cle, lib in D.QCM_ITEMS:
        n = sum(1 for s in reps if s["test"][cle])
        lignes.append([lib, f"{n} / {len(reps)}", lecture[cle]])
    doc.table(lignes, [6.5, 2.4, 8.5], taille=10, centre_cols=(1,))

    doc.h1("4. Profils individuels")
    for s in D.stagiaires():
        t = s["test"]
        doc.h2(f"{D.nom_complet(s)} — session {s['session']} ({D.SESSIONS[s['session']]['date_courte']})")
        if not t:
            doc.p(("Pas de réponse au questionnaire. ", {"b": True}),
                  "Positionnement express papier à 8h30 et échange individuel de 3 minutes pendant la séquence 0.")
            if s.get("presence_incertaine"):
                doc.p(("Présence non confirmée : ", {"b": True, "c": ROUGE}),
                      "Sarah MACHON a écrit le 23/09 « elle sera pas présente ». À confirmer avant 8h00.")
            continue
        forts = [D.AUTO_ITEMS[i] for i, v in enumerate(t["auto"]) if v >= 5]
        faibles = [D.AUTO_ITEMS[i] for i, v in enumerate(t["auto"]) if v <= 2]
        qcm = sum(1 for k, _ in D.QCM_ITEMS if t[k])
        doc.table([
            ["Rubrique", "Réponse"],
            ["Fonction / ancienneté", f"{s['fonction']} — {t['anciennete']}"],
            ["Aisance moyenne", f1(st.mean(t["auto"])) + " / 5"],
            ["Points d'appui (5/5)", ", ".join(forts) or "—"],
            ["Points à travailler (≤ 2/5)", ", ".join(faibles) or "—"],
            ["Connaissances", f"{qcm} / 5"],
            ["Veut progresser sur", t["progresser"]],
            ["Situation vécue (anonymisée)", t["situation"]],
            ["La journée vaudra le coup si…", t["valait_le_coup"]],
            ["Aménagement demandé", t["amenagement"]],
            ["Droit à l'image (questionnaire)", t["droit_image"]],
            ["Règlement intérieur signé", t["reglement_signe"]],
        ], [5.2, 12.2], taille=10)
        if t["consentement_preinscription"] == "Non":
            doc.p(("RGPD — action requise : ", {"b": True, "c": ROUGE}),
                  "cette stagiaire a répondu NON au consentement sur ses données de pré-inscription. Supprimer de Drag'n Survey "
                  "ses données non indispensables (date et lieu de naissance, nationalité, adresse, téléphone). Les données "
                  "nécessaires à la formation (nom, fonction, émargement, évaluation) reposent sur le contrat et l'obligation légale "
                  "(RGPD art. 6.1.b et 6.1.c), pas sur le consentement.", taille=10)
        if t["reglement_signe"] == "Non":
            doc.p(("À faire à 8h00 : ", {"b": True, "c": ROUGE}), "faire signer l'attestation de remise du règlement intérieur.", taille=10)
        if t["droit_image"] == "Non":
            doc.p(("Droit à l'image : REFUS. ", {"b": True, "c": ROUGE}),
                  "Aucune photo ni vidéo sur laquelle elle apparaît. Refus sans conséquence sur la formation.", taille=10)

    doc.h1("5. Constats de conformité sur le questionnaire lui-même")
    doc.puces([
        "Le formulaire collecte la nationalité et le lieu de naissance : ces données ne servent pas à la formation. À retirer (RGPD, minimisation, art. 5.1.c).",
        "La rubrique « Situation désobligeante (nécessitant un aménagement) » pousse à écrire la raison, donc parfois une donnée de santé. La renommer « Aménagement souhaité (sans indiquer la raison) » (RGPD, art. 9).",
        "Le consentement est demandé pour la pré-inscription : ce n'est pas la bonne base légale pour des données nécessaires à la formation. Le consentement ne doit viser que le facultatif (droit à l'image). (RGPD, art. 6 et 7)",
        "Le questionnaire ne remplace pas la fiche de droit à l'image signée : la faire signer le jour J (Code civil, art. 9 ; RGPD).",
        "Q7 : la question (« recommander un produit issu du corps médical ») ne correspond pas à la réponse proposée (données de santé). À réécrire.",
        "Drag'n Survey : éditeur français. Vérifier dans son contrat de sous-traitance (DPA) que l'hébergement reste dans l'Union européenne, pour que la mention « aucun transfert hors UE » de la convention reste exacte.",
    ], taille=10)
    return doc.enregistrer(OUT / "01_Rapport_positionnement_INTERNE_nominatif.docx")


def synthese_employeur():
    doc = Doc("Synthèse du positionnement", "Remise à MARILYN INSTITUT — données anonymisées",
              f"Action {D.ACTION['reference']} — convention {D.ACTION['convention']}", corps=12, mention_eval=True)
    reps = repondantes()
    doc.p(("Destinataire : ", {"b": True}), f"{D.CLIENT['representant']}, {D.CLIENT['qualite']} de {D.CLIENT['raison_sociale']}")
    doc.p(("Objet : ", {"b": True}), "ce que le questionnaire de positionnement nous a appris, et ce que nous changeons dans la journée.")
    doc.p(f"{len(reps)} salariées sur 8 ont répondu. Conformément à l'article 9 de la convention, les réponses individuelles ne sont pas "
          "transmises : vous trouverez ici uniquement des résultats de groupe.", taille=11)
    doc.h1("Ce que l'équipe maîtrise déjà")
    doc.puces(["Proposer le prochain rendez-vous (4,8/5) : c'est un vrai point fort.",
               "Occuper utilement un temps sans cliente (4,2/5) et accueillir une nouvelle cliente (4,0/5).",
               "Les réflexes de base sont connus : première impression, réponse au « c'est trop cher », prudence sur les données de santé."])
    doc.h1("Ce que l'équipe veut travailler")
    doc.puces(["Parler du chiffre d'affaires et des objectifs de l'institut (2,8/5).",
               "Recevoir une remarque sur son travail sans se braquer (3,0/5).",
               "Recommander sans avoir l'impression de forcer, et répondre au « c'est trop cher » (3,2/5).",
               "Gagner en aisance orale et en fluidité dans le conseil produit.",
               "Mieux communiquer dans l'équipe et faire une place aux idées de chacune."])
    doc.h1("Ce que nous changeons")
    doc.puces(["Plus de temps sur les objections et la recommandation (75 minutes, avec un jeu de cartes dédié).",
               "Un atelier « Mon agenda, mes chiffres » pour relier le travail de chacune aux résultats de l'institut.",
               "Des « phrases d'appui » prêtes à l'emploi pour gagner en aisance.",
               "Un standard d'équipe consacré aux idées de chacune, proposé à votre validation.",
               "Un positionnement express le matin et le soir : la progression sera mesurée."])
    doc.h1("Un point qui relève de l'employeur")
    doc.encadre("Postes de travail", [
        "Plusieurs salariées signalent que leur poste de travail à l'institut (table et chaise de prothésie ongulaire) mériterait d'être revu pour travailler confortablement.",
        "Nous vous transmettons ce constat de groupe, sans nom, avec l'accord des intéressées. Il relève de l'obligation de sécurité de l'employeur (art. L.4121-1 du code du travail). Nous pouvons en parler si vous le souhaitez.",
    ])
    doc.p(("Accord des intéressées recueilli le : ", {"b": True}), D.A_COMPLETER, taille=11)
    doc.signatures(["Pour YEBA FORMATIONS", "Aurélien LUMEKA, directeur", "Date :"],
                   ["Reçu pour MARILYN INSTITUT", "Sarah MACHON, gérante", "Date :"])
    return doc.enregistrer(OUT / "02_Synthese_positionnement_ANONYMISEE_pour_Marilyn_Institut.docx")


def fiche_indicateur8():
    doc = Doc("Fiche Indicateur 8 — Positionnement", "Preuve d'exploitation des résultats — Qualiopi, indicateurs 8 et 10",
              f"Action {D.ACTION['reference']} — « {D.ACTION['intitule']} »", corps=11, mention_eval=True)
    reps = repondantes()
    doc.encadre("À quoi sert cette fiche", [
        "Indicateur 8 : « Le prestataire détermine les procédures de positionnement et d'évaluation des acquis à l'entrée de la prestation. »",
        "L'auditeur ne cherche pas le questionnaire : il cherche la PREUVE que les réponses ont modifié la formation. Une procédure qui existe sans être appliquée, ou des résultats non pris en compte, est une non-conformité.",
        "Cette fiche relie chaque constat à une modification précise, datée, et à la séquence concernée. Elle prouve aussi l'indicateur 10 (adaptation de la prestation).",
    ], taille=10)
    doc.h1("1. Identification")
    doc.table([
        ["Rubrique", "Information"],
        ["Action", f"{D.ACTION['intitule']} — réf. {D.ACTION['reference']}"],
        ["Commanditaire", f"{D.CLIENT['raison_sociale']} ({D.CLIENT['forme']}) — SIREN {D.CLIENT['siren']} — {D.CLIENT['representant']}, {D.CLIENT['qualite']}"],
        ["Financeur", D.CLIENT["opco"]],
        ["Sessions", "Session 1 : lundi 28/09/2026 — Session 2 : mardi 29/09/2026 — 8h00-17h00 — C.R.E.P.S de Saint-Denis, salle « SEYCHELLES »"],
        ["Outil de positionnement", "Questionnaire en ligne Drag'n Survey (10 situations d'auto-positionnement, 5 questions de connaissances, attentes, aménagements)"],
        ["Questionnaires envoyés / reçus", f"8 / {len(reps)}"],
        ["Positionnement des non-répondantes", "Fiche papier « Positionnement express » à 8h30 le jour J"],
        ["Date de l'analyse", "27/09/2026"],
        ["Analyse réalisée par", "Aurélien LUMEKA, formateur et directeur"],
    ], [5, 12.4], taille=10)
    doc.h1("2. Résultats (synthèse anonymisée)")
    lignes = [["Situation", "Moyenne /5", "Réponses ≤ 2"]]
    for x in sorted(stats_items(), key=lambda x: x["moy"]):
        lignes.append([x["item"], f1(x["moy"]), str(x["bas"])])
    doc.table(lignes, [11, 3, 3.4], taille=10, centre_cols=(1, 2))
    lignes = [["Connaissance vérifiée", "Bonnes réponses"]]
    for cle, lib in D.QCM_ITEMS:
        lignes.append([lib, f"{sum(1 for s in reps if s['test'][cle])} / {len(reps)}"])
    doc.table(lignes, [13, 4.4], taille=10, centre_cols=(1,))
    doc.h1("3. Décisions d'adaptation — la partie qui compte")
    lignes = [["Ce que j'ai constaté", "Ce que je modifie concrètement", "Séquence"]]
    for c, m, s in ADAPTATIONS:
        lignes.append([c, m, s])
    doc.table(lignes, [6.2, 7.9, 3.3], taille=9.5)
    doc.h1("4. Attentes exprimées et réponse apportée")
    doc.table([
        ["Attente (reformulée)", "Réponse dans la journée"],
        ["Repartir avec des outils concrets, applicables dès le lendemain (3 réponses)", "Chaque séquence produit un livrable réutilisable : Charte d'Image, Carte du Voyage Cliente, Phrase qui Rebooke, Roue des Temps Creux, 10 standards communs, Ma Promesse Marilyn."],
        ["Être plus à l'aise pour conseiller (3 réponses)", "Méthodes S.O.I.N. et P.E.R.L.E., phrases d'appui, 3 passages minimum par stagiaire en jeu de rôle."],
        ["Échanger avec les collègues (2 réponses)", "Travail en binômes mixtes, restitutions collectives, standards communs aux deux instituts."],
        ["Mieux communiquer dans l'équipe (2 réponses)", "Méthode A.R.P. ; standard « rituel d'idées » soumis à la direction."],
    ], [7, 10.4], taille=10)
    doc.h1("5. Aménagements")
    doc.table([
        ["Demande reçue", "Aménagement mis en œuvre", "Vérifié le"],
        ["Poste de travail à l'institut (3 réponses) — hors formation", "Remontée collective et anonyme à l'employeur, avec l'accord des intéressées", ""],
        ["Confort pendant la journée (mesure pour tout le groupe)", "Chaises à dossier ; activités assises ou debout au choix ; pauses libres ; eau à disposition ; supports projetés en 28 pt minimum", ""],
    ], [6, 8.4, 3], taille=10)
    doc.p(("Règle appliquée : ", {"b": True}), "seul l'aménagement est consigné, jamais sa raison. Aucune donnée de santé n'est conservée (RGPD, art. 9).", taille=10)
    doc.h1("6. Conclusion — ce que je fais de tout cela")
    doc.p("Le groupe connaît déjà les bons réflexes : 4 connaissances sur 5 sont acquises par la majorité. Les réponses montrent surtout un écart "
          "entre savoir et faire : les stagiaires savent ce qu'il faut répondre à « c'est trop cher », mais ne se sentent pas à l'aise pour le faire. "
          "Des cours théoriques n'y changeraient rien. Il faut de la pratique répétée, en confiance.", taille=11)
    doc.p("Je maintiens donc le programme contractuel (10 objectifs, protocole M.A.R.I.L.Y.N.) et j'en modifie les dosages :", taille=11)
    doc.numeros([
        "Plus de temps sur la recommandation et les objections : séquence « Le Lien » portée à 75 minutes, avec le Ring des objections.",
        "Des chiffres rendus concrets : atelier « Mon agenda, mes chiffres », pour le point le plus faible du groupe (2,8/5).",
        "Une pratique sécurisée : binôme avant le groupe, phrases d'appui, droit au joker, observatrices expertes.",
        "Moins de temps sur ce qui est acquis : la reprise de rendez-vous passe de 35 à 30 minutes, et le groupe rédige lui-même son standard.",
        "Une mesure de la progression : le positionnement express du matin est refait en fin de journée ; l'écart figure dans le bilan et sur l'attestation (résultats de l'évaluation).",
        "Les besoins qui relèvent de l'employeur (postes de travail, communication d'équipe) sont transmis à la direction de façon anonyme, avec l'accord des intéressées.",
    ], taille=11)
    doc.p("Ces modifications sont visibles dans le support projeté, le conducteur de séance et le kit d'exercices datés du 27/09/2026.", taille=11)
    doc.signatures(["Établi à Sainte-Clotilde, le 27/09/2026", "Aurélien LUMEKA, directeur et formateur"],
                   ["Pièces jointes au dossier", "Exports Drag'n Survey (5)", "Fiches « Positionnement express » du jour J"])
    return doc.enregistrer(OUT / "03_Fiche_Qualiopi_Indicateur_8_positionnement_et_adaptation.docx")


def construire():
    return [rapport_interne(), synthese_employeur(), fiche_indicateur8()]


if __name__ == "__main__":
    for f in construire():
        print(f)

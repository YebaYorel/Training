"""Documents administratifs et d'évaluation — un fichier par stagiaire quand le document est individuel.

Règle de rangement : les documents d'une stagiaire dont la présence n'est pas confirmée vont dans un
sous-dossier « SI_PRESENTE_… » : on ne les utilise que si elle est bien là.
"""
import donnees as D
from docx_lib import Doc, ROUGE, BLEU
from docx.shared import Pt

A = D.A_COMPLETER
BASE = D.SORTIE / "03_ADMINISTRATIF"


def dossier(s, sous):
    d = BASE / sous
    if s.get("presence_incertaine"):
        d = d / f"SI_PRESENTE_{s['prenom']}_{s['nom'].replace(' ', '_')}"
    return d


def fichier(s, prefixe):
    return f"{prefixe}_S{s['session']}_{s['nom'].replace(' ', '_')}_{s['prenom']}.docx"


def etab_txt(s):
    if s["etablissement"]:
        nom, siret, _ = D.CLIENT["etablissements"][s["etablissement"]]
        return f"{nom} — SIRET {siret}"
    return A + " (MARILYN INSTITUT — SIRET 891 617 169 00018  ou  L'OR DES ÎLES — SIRET 891 617 169 00026)"


def bloc_session(doc, s):
    se = D.SESSIONS[s["session"]]
    doc.table([
        ["Rubrique", "Information"],
        ["Intitulé de l'action", D.ACTION["intitule"]],
        ["Nature", D.ACTION["nature"]],
        ["Session", f"Session {s['session']} — {se['groupe']} — {se['date']}"],
        ["Horaires", f"{D.ACTION['horaires']} — pauses 10h00-10h15 et 15h00-15h15 — déjeuner 12h00-13h00"],
        ["Durée", f"{D.ACTION['duree_h']} heures de formation (durée conventionnelle)"],
        ["Lieu", f"{D.ACTION['lieu_nom']} — {D.ACTION['lieu_adresse']}"],
        ["Modalité", D.ACTION["modalite"]],
        ["Formateur", D.ACTION["formateur"]],
    ], [4.6, 12.8], taille=11)


# ---------------------------------------------------------------- convocation
def convocation(s):
    se = D.SESSIONS[s["session"]]
    doc = Doc("Convocation à une action de formation", f"Session {s['session']} — {se['date']}",
              f"Convention {D.ACTION['convention']} — devis {se['devis']}", corps=12)
    doc.p(("Date d'envoi : ", {"b": True}), "......../......../2026")
    doc.p(("À l'attention de : ", {"b": True}), (D.nom_complet(s), {"b": True}), f" — {s['fonction']}")
    doc.p(f"Salariée de {D.CLIENT['raison_sociale']} ({D.CLIENT['forme']}) — SIREN {D.CLIENT['siren']}")
    doc.p(("Établissement de rattachement : ", {"b": True}), etab_txt(s))
    doc.p("Madame,")
    doc.p(f"Vous êtes convoquée à l'action de formation ci-dessous, organisée par YEBA FORMATIONS à la demande de votre employeur, "
          f"{D.CLIENT['raison_sociale']}, représenté par {D.CLIENT['representant']}, {D.CLIENT['qualite']}. "
          f"Cette formation est financée dans le cadre du plan de développement des compétences, avec une demande de prise en charge auprès de l'{D.CLIENT['opco']}.")
    bloc_session(doc, s)
    doc.h2("À savoir avant de venir")
    doc.puces([
        "Merci d'arriver à 7h50 : la formation commence à 8h00 précises.",
        D.ACTION["repas"],
        "Vous signerez la feuille d'émargement le matin et l'après-midi.",
        "Apportez de quoi écrire. Tout le reste est fourni.",
        "Tenue professionnelle ou confortable : nous ferons des mises en situation, assises ou debout, au choix.",
        "Pendant la formation, votre rémunération est maintenue par votre employeur.",
    ])
    doc.h2("Documents remis avec cette convocation")
    doc.puces(["Le livret d'accueil, qui contient le programme, le règlement intérieur et la notice sur vos données personnelles.",
               "La fiche d'autorisation de droit à l'image : facultative ; un refus est sans conséquence sur votre formation."])
    doc.encadre("Besoin d'un aménagement ?", [
        f"Contactez le référent handicap : {D.ORG['ref_handicap']}.",
        "Aucune raison à donner, aucun justificatif à fournir : indiquez seulement l'aménagement utile (place, supports agrandis, rythme, pauses…).",
    ])
    doc.p("Nous vous prions d'agréer, Madame, nos salutations distinguées.")
    doc.signatures(["Pour YEBA FORMATIONS", "Aurélien LUMEKA, directeur", "Fait à Sainte-Clotilde, le ......../......../2026"],
                   ["Contact", f"{D.ORG['tel']}", D.ORG["email"]], hauteur_cm=2.4)
    doc.p("Vos données sont traitées par YEBA FORMATIONS pour organiser la formation et en justifier la réalisation (RGPD, art. 6.1.b et 6.1.c). "
          f"Conservation : 3 ans. Vos droits : {D.ORG['email']}. Détails dans la notice du livret d'accueil.", taille=9, couleur=None)
    return doc.enregistrer(dossier(s, "01_Convocations") / fichier(s, "Convocation"))


# ------------------------------------------------------------ droit à l'image
def droit_image(s):
    doc = Doc("Autorisation de droit à l'image", "Facultative — libre — révocable à tout moment",
              f"Action {D.ACTION['reference']} — session {s['session']} du {D.SESSIONS[s['session']]['date_courte']}", corps=12)
    doc.p("Je soussignée ", (D.nom_complet(s), {"b": True}), f", participante à la formation « {D.ACTION['intitule']} » "
          f"du {D.SESSIONS[s['session']]['date']}, déclare :")
    doc.h2("1. Mon choix (cocher une seule case)")
    doc.p("☐  J'AUTORISE YEBA FORMATIONS à me photographier ou me filmer pendant la formation, pour les seuls usages cochés ci-dessous.", gras=True)
    doc.p("☐  JE REFUSE toute photo ou vidéo sur laquelle je suis reconnaissable.", gras=True)
    doc.p("Un refus n'a aucune conséquence sur ma participation, sur mon évaluation ni sur mon attestation.", italique=True, taille=11)
    doc.h2("2. Si j'autorise : usages acceptés (cocher)")
    doc.puces([
        "☐  Supports pédagogiques internes de YEBA FORMATIONS (non diffusés au public)",
        "☐  Site internet www.yebaformations.re",
        "☐  Réseaux sociaux de YEBA FORMATIONS",
        "☐  Documents remis à mon employeur, MARILYN INSTITUT (compte rendu de la formation)",
    ])
    doc.p("Aucun autre usage n'est autorisé. Aucune image ne sera cédée ni vendue à un tiers. Aucune image ne sera modifiée ou générée "
          "par une intelligence artificielle sans un nouvel accord écrit de ma part. Si une image était retouchée, elle serait signalée comme telle "
          "(règlement (UE) 2024/1689, art. 50).", taille=11)
    doc.h2("3. Durée")
    doc.cases(["1 an", "2 ans", "3 ans"], taille=12)
    doc.p("à compter de la signature. À l'échéance, les images sont retirées et supprimées.", taille=11)
    doc.h2("4. Mes droits")
    doc.p(f"Cette autorisation est gratuite. Je peux la retirer à tout moment, sans justification, par simple message à {D.ORG['email']} : "
          "les images sont alors retirées dans un délai d'un mois. Je dispose d'un droit d'accès, de rectification et d'effacement, "
          "et je peux saisir la CNIL (www.cnil.fr).", taille=11)
    doc.p("Fondements : article 9 du Code civil (droit à l'image) ; RGPD, articles 6.1.a, 7 et 17.", taille=9)
    doc.signatures([f"La participante — {D.nom_complet(s)}", "Fait à Saint-Denis, le ......../......../2026",
                    "Signature précédée de « Lu et approuvé »"],
                   ["Pour YEBA FORMATIONS", "Aurélien LUMEKA, directeur", "Signature"], hauteur_cm=3)
    return doc.enregistrer(dossier(s, "02_Droit_a_l_image") / fichier(s, "Droit_image"))


# ----------------------------------------------------------------- émargement
def emargement(n):
    se = D.SESSIONS[n]
    doc = Doc("Feuille d'émargement", f"Session {n} — {se['date']} — une signature par demi-journée",
              f"Convention {D.ACTION['convention']} — devis {se['devis']} — financeur : {D.CLIENT['opco']}",
              corps=11, paysage=True, compact=True)
    doc.table([
        ["Action", "Organisme", "Entreprise", "Lieu", "Formateur"],
        [D.ACTION["intitule"] + f" — {D.ACTION['nature']}",
         f"YEBA FORMATIONS — SIRET {D.ORG['siret']} — NDA {D.ORG['nda']}",
         f"{D.CLIENT['raison_sociale']} — SIREN {D.CLIENT['siren']}",
         f"{D.ACTION['lieu_nom']}, {D.ACTION['lieu_adresse']}",
         D.ACTION["formateur"]],
    ], [6.5, 5.3, 4.6, 5.8, 3.9], taille=9)
    lignes = [["Nom et prénom", "Fonction", "Établissement\n(SIRET)", "MATIN\n8h00 – 12h00\nSignature", "APRÈS-MIDI\n13h00 – 17h00\nSignature", "Observations\n(retard, départ, absence)"]]
    for s in D.par_session(n):
        etab = D.CLIENT["etablissements"][s["etablissement"]][1][-5:] if s["etablissement"] else "☐ 00018  ☐ 00026"
        nom = D.nom_complet(s)
        lignes.append([nom, s["fonction"], etab, "", "", ""])
    lignes.append(["Ajout éventuel (remplacement écrit)", "", "☐ 00018  ☐ 00026", "", "", ""])
    doc.table(lignes, [5.2, 4.8, 3.1, 4.3, 4.3, 4.4], taille=10, hauteur_cm=1.05, zebre=False)
    doc.table([
        ["Formateur — Aurélien LUMEKA", "Signature MATIN", "Signature APRÈS-MIDI", "Nombre de présentes"],
        ["J'atteste l'exactitude des présences ci-dessus.", "", "", "Matin : ....   Après-midi : ...."],
    ], [9.5, 5.3, 5.3, 6], taille=10, hauteur_cm=1.0, zebre=False)
    doc.p("Chaque stagiaire signe elle-même, à chaque demi-journée. Signer pour une autre personne est interdit (Code pénal, art. 441-1). "
          "Une case vide est barrée par le formateur avec la mention « absente ». Pièce justificative conservée par YEBA FORMATIONS et transmise à l'"
          f"{D.CLIENT['opco']} (code du travail, art. R.6332-26 ; Qualiopi, indicateur 11). Durée conventionnelle attestée : {D.ACTION['duree_h']} heures.",
          taille=8.5)
    return doc.enregistrer(BASE / "03_Emargement" / f"Emargement_Session_{n}_{se['date_courte'].replace('/', '-')}.docx")


# ---------------------------------------------------------- attestation fin
def attestation(s):
    se = D.SESSIONS[s["session"]]
    doc = Doc("Attestation de fin de formation", "Article L.6353-1 du code du travail",
              f"Action {D.ACTION['reference']} — convention {D.ACTION['convention']}", corps=11, mention_eval=True)
    doc.p("Je soussigné Aurélien LUMEKA, directeur de YEBA FORMATIONS, atteste que :")
    doc.table([
        ["Rubrique", "Information"],
        ["Stagiaire", D.nom_complet(s)],
        ["Fonction", s["fonction"]],
        ["Employeur", f"{D.CLIENT['raison_sociale']} — SIREN {D.CLIENT['siren']}"],
        ["Établissement", etab_txt(s)],
        ["a suivi l'action", D.ACTION["intitule"]],
        ["Nature", D.ACTION["nature"]],
        ["Date", f"{se['date']} ({D.ACTION['horaires']})"],
        ["Durée", f"{D.ACTION['duree_h']} heures prévues — durée suivie : ........ heures"],
        ["Lieu et modalité", f"{D.ACTION['lieu_nom']} — {D.ACTION['modalite']}"],
    ], [4.2, 13.2], taille=10)
    doc.h2("Objectifs de la formation et résultats de l'évaluation des acquis")
    lignes = [["Objectif — la stagiaire est capable de :", "Acquis", "En cours", "Non acquis"]]
    for o in D.OBJECTIFS:
        lignes.append([o, "☐", "☐", "☐"])
    doc.table(lignes, [12.2, 1.7, 1.8, 1.7], taille=9.5, centre_cols=(1, 2, 3))
    doc.table([
        ["Modalités d'évaluation", "Résultat"],
        ["Grille critériée d'observation en situation (13 critères — seuil 26/39, sans critère à 0)", "........ / 39"],
        ["Quiz de connaissances (10 questions — seuil 7/10)", "........ / 10"],
        ["Positionnement express : aisance moyenne à l'entrée → à la sortie", "........ → ........ / 5"],
        ["Conclusion", "☐ Objectifs atteints   ☐ Partiellement atteints   ☐ Non atteints"],
    ], [12.2, 5.2], taille=10)
    doc.signatures(["Fait à Saint-Denis, le ......../......../2026", "Aurélien LUMEKA, directeur de YEBA FORMATIONS", "Signature et cachet"],
                   ["Remise à la stagiaire", "Signature de la stagiaire"], hauteur_cm=2.6)
    return doc.enregistrer(dossier(s, "04_Attestations_fin_formation") / fichier(s, "Attestation_fin_formation"))


# ----------------------------------------------------- certificat réalisation
def certificat(s):
    se = D.SESSIONS[s["session"]]
    doc = Doc("Certificat de réalisation", "Action de formation — pièce justificative pour l'OPCO",
              f"Action {D.ACTION['reference']} — convention {D.ACTION['convention']} — devis {se['devis']}", corps=11)
    doc.p("Je soussigné Aurélien LUMEKA, représentant légal du dispensateur de l'action concourant au développement des compétences "
          f"YEBA FORMATIONS (SIRET {D.ORG['siret']}, déclaration d'activité n° {D.ORG['nda']}), atteste que :")
    doc.table([
        ["Rubrique", "Information"],
        ["Bénéficiaire", D.nom_complet(s)],
        ["Salariée de l'entreprise", f"{D.CLIENT['raison_sociale']} — SIREN {D.CLIENT['siren']} — {D.CLIENT['siege']}"],
        ["Établissement de rattachement", etab_txt(s)],
        ["a suivi l'action", D.ACTION["intitule"]],
        ["Nature de l'action (art. L.6313-1)", "☒ Action de formation   ☐ Bilan de compétences   ☐ Action de VAE   ☐ Action de formation par apprentissage"],
        ["Qui s'est déroulée le", se["date"] + f" — {D.ACTION['horaires']}"],
        ["Pour une durée de", f"........ heures réalisées, sur {D.ACTION['duree_h']} heures prévues"],
        ["Modalité", D.ACTION["modalite"] + f" — {D.ACTION['lieu_nom']}"],
        ["Financeur", D.CLIENT["opco"]],
    ], [5.4, 12], taille=10)
    doc.p("Sans préjudice des délais inhérents à l'instruction de la prise en charge, le bénéficiaire s'engage à conserver l'ensemble des "
          "pièces justificatives qui ont permis d'établir le présent certificat pendant une durée de 3 ans à compter de la fin de l'année du "
          "dernier paiement. En cas de cofinancement des fonds européens, la durée de conservation est étendue conformément aux obligations conventionnelles spécifiques.",
          taille=9)
    doc.signatures(["Fait à Saint-Denis, le ......../......../2026", "Aurélien LUMEKA, directeur", "Cachet et signature du dispensateur"],
                   ["Pièces jointes", "Feuille d'émargement de la session", f"Convention {D.ACTION['convention']}"], hauteur_cm=2.8)
    doc.p(f"À vérifier avant envoi : si l'{D.CLIENT['opco']} impose son propre modèle de certificat sur son espace en ligne, c'est ce modèle qui "
          "fait foi ; reporter alors ces informations à l'identique.", taille=9, italique=True)
    return doc.enregistrer(dossier(s, "05_Certificats_realisation") / fichier(s, "Certificat_realisation"))


# ------------------------------------------------------- évaluation à chaud
def eval_chaud(n):
    se = D.SESSIONS[n]
    doc = Doc("Votre avis sur la formation", f"Évaluation « à chaud » — session {n} — {se['date']}",
              D.ACTION["intitule"], corps=13, mention_eval=True)
    doc.p("Merci de répondre franchement : vos réponses servent à améliorer la formation. Le nom est facultatif. "
          "Échelle : 1 = pas du tout satisfaite · 2 = peu satisfaite · 3 = satisfaite · 4 = très satisfaite.", taille=12)
    doc.p(("Prénom et nom (facultatif) : ", {"b": True}), "..........................................................")

    def bloc(titre, items):
        doc.h2(titre)
        lignes = [["", "1", "2", "3", "4"]] + [[i, "☐", "☐", "☐", "☐"] for i in items]
        doc.table(lignes, [12.6, 1.2, 1.2, 1.2, 1.2], taille=12, centre_cols=(1, 2, 3, 4))

    bloc("1. L'organisation", ["Les informations reçues avant la formation (convocation, livret)",
                               "La salle, le confort, l'accessibilité", "Le respect des horaires et des pauses"])
    bloc("2. Le contenu", ["Le contenu correspond à mon métier en institut", "Les exercices et jeux m'ont aidée à progresser",
                           "La part de pratique était suffisante", "Les supports (écran, fiches, ressource) sont clairs et lisibles"])
    bloc("3. Le formateur", ["Il explique clairement", "Il écoute et s'adapte au groupe", "Il donne des retours utiles et bienveillants",
                             "Il maîtrise son sujet"])
    bloc("4. Les résultats", ["J'ai atteint les objectifs annoncés", "Je vais appliquer ce que j'ai appris dès demain",
                              "Je me sens plus à l'aise pour conseiller et vendre"])
    doc.h2("5. Recommanderiez-vous cette formation à une collègue ?")
    doc.cases(["Oui, sans hésiter", "Oui", "Plutôt non", "Non"], taille=13)
    doc.h2("6. En quelques mots")
    for q in ["Ce que j'ai le plus apprécié :", "Ce qui pourrait être amélioré :", "Ce que j'aimerais approfondir :"]:
        doc.p((q, {"b": True}), taille=12)
        doc.p("........................................................................................................................", taille=12)
        doc.p("........................................................................................................................", taille=12)
    doc.p("Réponses exploitées par YEBA FORMATIONS uniquement pour améliorer ses formations (Qualiopi, indicateur 30). Résultats transmis à "
          "l'employeur sous forme de synthèse de groupe, sans nom. Conservation : 3 ans.", taille=9)
    return doc.enregistrer(D.SORTIE / "05_EVALUATIONS" / f"Evaluation_a_chaud_Session_{n}.docx")


def eval_froid():
    doc = Doc("Évaluation « à froid »", "3 mois après la formation — ce qui a changé au quotidien",
              D.ACTION["intitule"], corps=13, mention_eval=True)
    doc.p("À envoyer fin décembre 2026 (3 mois après la session, convention art. 5). Nom facultatif.", taille=11, italique=True)
    lignes = [["Depuis la formation…", "Jamais", "Parfois", "Souvent", "Toujours"]]
    for i in ["J'applique la Charte d'Image Marilyn", "Je découvre le besoin avec S.O.I.N. avant de proposer",
              "Je recommande UNE seule chose, par le bénéfice", "Je traite « c'est cher » sans me justifier ni brader",
              "Je propose la reprise de rendez-vous en sortie de cabine", "J'utilise la Roue des Temps Creux",
              "Je reçois une remarque avec A.R.P.", "Je respecte les règles RGPD de la fiche cliente"]:
        lignes.append([i, "☐", "☐", "☐", "☐"])
    doc.table(lignes, [10.4, 1.7, 1.7, 1.7, 1.8], taille=11, centre_cols=(1, 2, 3, 4))
    for q in ["Un exemple concret de ce que je fais différemment :", "Ce qui m'empêche encore d'appliquer certains outils :",
              "Un besoin de formation complémentaire :"]:
        doc.p((q, {"b": True}), taille=12)
        doc.p("........................................................................................................................", taille=12)
    return doc.enregistrer(D.SORTIE / "05_EVALUATIONS" / "Evaluation_a_froid_3_mois_stagiaire.docx")


def eval_commanditaire():
    doc = Doc("Évaluation du commanditaire", "À retourner 30 jours après la formation (convention, art. 5)",
              f"Convention {D.ACTION['convention']} — action {D.ACTION['reference']}", corps=11)
    doc.table([
        ["Rubrique", "Information"],
        ["Entreprise", f"{D.CLIENT['raison_sociale']} ({D.CLIENT['forme']}) — SIREN {D.CLIENT['siren']}"],
        ["Établissements", "MARILYN INSTITUT (Saint-Denis) et L'OR DES ÎLES (Bras-Panon)"],
        ["Répondante", f"{D.CLIENT['representant']}, {D.CLIENT['qualite']}"],
        ["Action", D.ACTION["intitule"]],
        ["Sessions", "Session 1 : lundi 28/09/2026 — Session 2 : mardi 29/09/2026"],
        ["Date de la réponse", "......../......../2026"],
    ], [4.4, 13], taille=10)
    doc.p("Notez de 1 (pas du tout d'accord) à 4 (tout à fait d'accord).")
    lignes = [["Affirmation", "1", "2", "3", "4"]]
    for a in ["Mon besoin a été correctement analysé en amont", "Le programme répondait à ce besoin",
              "Le positionnement des salariées a été pris en compte", "L'organisation et la logistique ont été fluides",
              "Les documents administratifs ont été fournis à temps (convention, convocations, attestations)",
              "Les retours de mes équipes sont positifs", "Je constate des changements concrets dans les deux instituts",
              "Le niveau de service est plus homogène entre les deux instituts",
              "Les livrables produits (Charte d'Image, standards, Roue des Temps Creux…) sont utilisés",
              "Je referais appel à YEBA FORMATIONS"]:
        lignes.append([a, "☐", "☐", "☐", "☐"])
    doc.table(lignes, [12.6, 1.2, 1.2, 1.2, 1.2], taille=10.5, centre_cols=(1, 2, 3, 4))
    for q in ["Quels changements avez-vous observés depuis la formation ?", "Quel indicateur suivez-vous (taux de reprise de RDV, ventes produits…) ?",
              "Quel besoin reste non couvert ?", "Qu'est-ce qui aurait pu être mieux fait ?"]:
        doc.p((q, {"b": True}))
        doc.p("..........................................................................................................................")
    doc.signatures(["Pour MARILYN INSTITUT", f"{D.CLIENT['representant']}, {D.CLIENT['qualite']}", "Signature et cachet"],
                   ["Retour à", "Aurélien LUMEKA", D.ORG["email"]])
    doc.p("Réponses exploitées pour l'amélioration continue (Qualiopi, indicateurs 30 et 32). Conservation : 3 ans.", taille=9)
    return doc.enregistrer(D.SORTIE / "05_EVALUATIONS" / "Evaluation_commanditaire_Marilyn_Institut.docx")


def positionnement_express():
    doc = Doc("Positionnement express", "Matin (8h30) et soir (16h40) — 2 minutes", D.ACTION["intitule"], corps=13, mention_eval=True)
    doc.p(("Prénom : ", {"b": True}), "..............................   ", ("Session : ", {"b": True}), "☐ 28/09   ☐ 29/09")
    doc.p("Entourez votre niveau d'aisance : 1 = pas du tout à l'aise … 5 = totalement à l'aise. Pas de bonne ou de mauvaise réponse.", taille=12)
    lignes = [["Situation", "MATIN", "SOIR"]]
    for it in D.AUTO_ITEMS:
        lignes.append([it, "1  2  3  4  5", "1  2  3  4  5"])
    doc.table(lignes, [9.6, 3.9, 3.9], taille=12, centre_cols=(1, 2), hauteur_cm=1.05)
    doc.p(("Ce soir, l'outil que j'utilise en premier demain : ", {"b": True}), taille=12)
    doc.p(".........................................................................................................", taille=12)
    doc.p("Fiche conservée 3 ans au dossier de l'action (Qualiopi, indicateurs 8 et 11). Non transmise à l'employeur.", taille=9)
    return doc.enregistrer(D.SORTIE / "05_EVALUATIONS" / "Positionnement_express_matin_soir.docx")


def construire():
    out = []
    for s in D.stagiaires():
        out += [convocation(s), droit_image(s), attestation(s), certificat(s)]
    out += [emargement(1), emargement(2), eval_chaud(1), eval_chaud(2), eval_froid(), eval_commanditaire(), positionnement_express()]
    return out


if __name__ == "__main__":
    for f in construire():
        print(f.relative_to(D.SORTIE))

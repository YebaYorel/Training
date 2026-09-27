"""Livret d'accueil complet : accueil + programme + règlement intérieur + notice RGPD (annexes 1 à 3 de la convention).

Corrections apportées par rapport à la version du 23/09/2026 (Drive) :
- pauses 10h00-10h15 et 15h00-15h15 (et non 30 min) — consigne d'A. LUMEKA du 27/09 ;
- contact unique yebaformations@gmail.com ;
- délais de réclamation alignés sur la convention signée (AR 5 j ouvrés, réponse 15 j ouvrés) ;
- évaluation à froid à 3 mois (convention art. 5) ;
- IA : aucune notation par IA (cohérent avec quiz, grille et charte de marque) ;
- objectifs et programme = fiche FOR-0007 (annexe 1 de la convention), recalés sur 8h00-17h00.
"""
import donnees as D
from docx_lib import Doc

OUT = D.SORTIE / "02_LIVRET_ACCUEIL"


def construire():
    doc = Doc("Livret d'accueil de la stagiaire", D.ACTION["intitule"],
              "Remis avant l'entrée en formation (code du travail, art. L.6353-8) — version du 27/09/2026", corps=12,
              mention_eval=True)
    doc.p(("MARILYN INSTITUT — L'OR DES ÎLES", {"b": True, "t": 15}), align="c")
    doc.p("Session 1 : lundi 28 septembre 2026   •   Session 2 : mardi 29 septembre 2026", align="c", gras=True)
    doc.p("8h00 – 17h00   •   C.R.E.P.S de Saint-Denis, salle « SEYCHELLES »", align="c")
    doc.p("Stagiaire : ..........................................................", align="c")
    doc.p("Version en très gros caractères (16 points) disponible sur simple demande.", align="c", italique=True, taille=10)

    doc.h1("Sommaire")
    doc.numeros(["Bienvenue", "Vos interlocuteurs", "La formation en bref", "Objectifs", "Programme de la journée",
                 "Méthodes et évaluation", "Informations pratiques", "Handicap et accessibilité", "Tolérance zéro",
                 "Avis et réclamations", "Numéros utiles", "Annexe A — Règlement intérieur",
                 "Annexe B — Notice d'information sur vos données personnelles", "Attestation de remise (à signer)",
                 "Mon plan d'action"])
    doc.saut()

    # 1
    doc.h1("1. Bienvenue")
    doc.p("Vous accueillez chaque jour les clientes de MARILYN INSTITUT et de L'OR DES ÎLES. Vous êtes la première personne qu'elles voient, "
          "et souvent la raison pour laquelle elles reviennent.")
    doc.p("Cette journée a été construite pour votre métier, à partir de vos réponses au questionnaire de positionnement : l'accueil, "
          "le conseil en soins et en produits, les objections du quotidien (« c'est cher », « je vais réfléchir »), la reprise de rendez-vous, "
          "le travail en équipe.")
    doc.p(("Ici, pas de cours magistral : 70 % de pratique. ", {"b": True}),
          "Des jeux, des mises en situation en petit groupe, et des outils que vous utiliserez dès le lendemain, en cabine comme à l'accueil.")
    doc.p("Lisez ce livret avant la session et gardez-le : il vous servira aussi après. Je me réjouis de vous accueillir.")
    doc.p(("Aurélien LUMEKA", {"b": True}), " — directeur de YEBA FORMATIONS, formateur")

    # 2
    doc.h1("2. Vos interlocuteurs")
    doc.table([
        ["Rôle", "Interlocuteur", "Contact"],
        ["Formateur, référent pédagogique", "Aurélien LUMEKA", f"{D.ORG['tel']} — {D.ORG['email']}"],
        ["Référent handicap", "Aurélien LUMEKA", "9 rue Françoise Châtelain, 97490 Sainte-Clotilde — " + D.ORG["tel"]],
        ["Suivi administratif", "Aurélien LUMEKA", D.ORG["email"]],
        ["Votre employeur", f"{D.CLIENT['representant']}, {D.CLIENT['qualite']}", "MARILYN INSTITUT"],
        ["Si un fait concerne le formateur", f"{D.CLIENT['representant']}", "voir rubrique 9"],
    ], [5.2, 4.6, 7.6], taille=11)
    doc.p(f"YEBA FORMATIONS est un organisme de formation réunionnais créé en 2021. {D.ORG['qualiopi']}. {D.ORG['nda_mention']}", taille=10)

    # 3
    doc.h1("3. La formation en bref")
    doc.table([
        ["Élément", "Détail"],
        ["Intitulé", D.ACTION["intitule"]],
        ["Public", D.ACTION["public"]],
        ["Prérequis", D.ACTION["prerequis"]],
        ["Modalité", D.ACTION["modalite"] + " — 4 participantes par groupe"],
        ["Durée", f"1 journée — {D.ACTION['duree_h']} heures de formation"],
        ["Dates", "Groupe 1 : lundi 28 septembre 2026 — Groupe 2 : mardi 29 septembre 2026 — programme identique"],
        ["Horaires", "8h00 – 17h00 — pauses 10h00-10h15 et 15h00-15h15 — déjeuner 12h00-13h00"],
        ["Lieu", f"{D.ACTION['lieu_nom']} — {D.ACTION['lieu_adresse']}"],
        ["Financement", f"Plan de développement des compétences de MARILYN INSTITUT — prise en charge demandée à l'{D.CLIENT['opco']}"],
        ["Rémunération", "Vous restez salariée pendant la formation : votre rémunération est maintenue par votre employeur."],
    ], [3.8, 13.6], taille=11)

    # 4
    doc.h1("4. Objectifs")
    doc.p("À la fin de la journée, vous serez capable de :")
    doc.numeros(D.OBJECTIFS)

    # 5
    doc.h1("5. Programme de la journée — protocole M.A.R.I.L.Y.N.")
    doc.p("M comme Miroir · A comme Accueil · R comme Ressenti · I comme Initiative · L comme Lien · Y comme « Y revenir » · N comme Nous.", gras=True, taille=11)
    lignes = [["Horaire", "Séquence", "Ce que vous faites"]]
    for d, f, l, titre, contenu, _ in D.PROGRAMME:
        lignes.append([f"{d} – {f}", (f"{l} — " if l else "") + titre, contenu])
    doc.table(lignes, [2.8, 4.8, 9.8], taille=10)
    doc.p("Programme identique pour les deux groupes. Les séquences ont été ajustées selon vos réponses au positionnement "
          "(plus de temps sur les objections et la recommandation).", taille=10, italique=True)

    # 6
    doc.h1("6. Méthodes et évaluation")
    doc.puces([
        "30 % d'apports, 70 % de pratique : jeux de cartes, jeux de rôle en binôme, ateliers.",
        "Clientes fictives uniquement : aucune cliente réelle n'est citée.",
        "Diaporama accessible : mots-clés, très gros caractères, fort contraste.",
        "Ressource PDF complète remise après la session.",
        "Personne ne joue devant le groupe sans s'être d'abord entraînée en binôme. Vous avez droit au joker.",
    ], taille=11)
    doc.table([
        ["Quand ?", "Comment ?", "Pourquoi ?"],
        ["Avant", "Questionnaire de positionnement en ligne", "Adapter la journée à votre point de départ"],
        ["8h30 et 16h40", "Positionnement express (2 minutes)", "Mesurer votre progression"],
        ["Toute la journée", "Grille critériée : observation pendant les jeux de rôle", "Retours personnalisés, résultat sur l'attestation"],
        ["16h20", "Quiz de 10 questions, en équipes, sur l'écran", "Vérifier les connaissances clés"],
        ["17h00", "Questionnaire de satisfaction", "Améliorer la formation"],
        ["À 3 mois", "Questionnaire « à froid »", "Mesurer ce qui a changé au quotidien"],
    ], [3.2, 7.2, 7], taille=10.5)
    doc.p("Documents remis : avant — convocation et ce livret ; après — attestation de fin de formation (objectifs, nature, durée, résultats de "
          "l'évaluation) et ressource PDF. À votre employeur et à l'OPCO EP : feuilles d'émargement et certificat de réalisation.", taille=11)

    # 7
    doc.h1("7. Informations pratiques")
    doc.table([
        ["Sujet", "Information"],
        ["Adresse", f"{D.ACTION['lieu_nom']} — {D.ACTION['lieu_adresse']}"],
        ["Arrivée", "7h50 : la formation commence à 8h00 précises."],
        ["Repas", D.ACTION["repas"] + " Le repas se prend en dehors de la salle de formation."],
        ["Transport", "Par vos propres moyens. Le trajet relève de la législation sur les accidents de trajet."],
        ["Hébergement", "Aucun hébergement n'est prévu."],
        ["À apporter", "De quoi écrire. Tout le reste est fourni."],
        ["Tenue", "Professionnelle ou confortable. Toutes les activités se font assises ou debout, au choix."],
    ], [3.4, 14], taille=11)

    # 8
    doc.h1("8. Handicap et accessibilité")
    doc.p("Vous avez un besoin particulier, lié ou non à un handicap : vue, audition, mobilité, concentration, santé ? Contactez le référent handicap, "
          "avant la session si possible :")
    doc.encadre("Référent handicap", [D.ORG["ref_handicap"],
                                      "Vous n'avez pas à indiquer de raison ni de diagnostic : seul le besoin d'aménagement est utile.",
                                      "Votre information reste confidentielle : elle n'est pas transmise à votre employeur sans votre accord."])
    doc.p("Déjà prévu pour tout le groupe : chaises à dossier, activités assises ou debout au choix, pauses possibles à tout moment, "
          "eau à disposition, supports projetés en très gros caractères. Possibles sur demande : supports imprimés en 16 points, place près de l'écran, "
          "évaluation orale, rythme adapté.", taille=11)

    # 9
    doc.h1("9. Tolérance zéro")
    doc.p("YEBA FORMATIONS applique une tolérance zéro face aux violences sexistes et sexuelles, au harcèlement et aux discriminations. "
          "Chaque signalement est traité sous 48 heures, en toute confidentialité. Aucune personne qui signale de bonne foi, ou qui témoigne, "
          "ne peut subir de représailles.")
    doc.puces(["Parlez-en au formateur, pendant ou après la session.",
               f"Si les faits concernent le formateur : adressez-vous à {D.CLIENT['representant']}, {D.CLIENT['qualite']} de MARILYN INSTITUT.",
               "Si les faits concernent Mme MACHON : adressez-vous au formateur.",
               "Écoute : 3919 (gratuit, anonyme). Danger immédiat : 17 ou 112 ; par SMS : 114."], taille=11)

    # 10
    doc.h1("10. Avis et réclamations")
    doc.p("Votre avis compte : questionnaire de satisfaction en fin de journée, puis questionnaire « à froid » 3 mois plus tard.")
    doc.p(f"Réclamation : oralement au formateur, ou par écrit à {D.ORG['email']}. Accusé de réception sous 5 jours ouvrés, "
          "réponse motivée sous 15 jours ouvrés (convention de formation, art. 12). Chaque réclamation est enregistrée et analysée pour améliorer nos formations.")

    # 11
    doc.h1("11. Numéros utiles")
    doc.table([
        ["Service", "Numéro"],
        ["Votre formateur", D.ORG["tel"]],
        ["SAMU — urgence médicale", "15"], ["Pompiers", "18"], ["Police — gendarmerie", "17"],
        ["Numéro d'urgence européen", "112"], ["Urgence par SMS (personnes sourdes ou malentendantes)", "114"],
        ["Violences Femmes Info", "3919"], ["Défenseur des droits", "09 69 39 00 00"],
    ], [11, 6.4], taille=11)
    doc.saut()

    # ------------------------------------------------------- Règlement intérieur
    doc.h1("Annexe A — Règlement intérieur applicable aux stagiaires")
    doc.p("Établi en application des articles L.6352-3, L.6352-4 et R.6352-1 à R.6352-15 du code du travail. Annexe 2 de la convention "
          f"{D.ACTION['convention']}.", taille=10, italique=True)
    art = [
        ("Article 1 — Champ d'application",
         ["Le présent règlement s'applique à chaque stagiaire, pendant toute la durée de la formation et dans tous les lieux où elle se déroule "
          "(salle, espaces communs, abords du C.R.E.P.S), y compris pendant les pauses. Il fixe les règles de santé, d'hygiène et de sécurité, "
          "les règles de discipline, la nature et l'échelle des sanctions, et les garanties de procédure."]),
        ("Article 2 — Lieu de formation",
         ["YEBA FORMATIONS ne dispose pas de locaux propres. La formation se déroule au C.R.E.P.S de Saint-Denis. Conformément à l'article R.6352-1 "
          "du code du travail, les consignes de santé et de sécurité applicables sont celles de l'établissement d'accueil : consignes d'évacuation, "
          "zones autorisées, instructions du personnel. Le formateur les présente à l'ouverture de chaque session."]),
        ("Article 3 — Santé et sécurité",
         ["Chacune veille à sa propre sécurité et à celle des autres, et signale immédiatement toute situation dangereuse.",
          "Incendie : en cas d'alarme, quitter la salle sans reprendre ses affaires, suivre les instructions et rejoindre le point de rassemblement, "
          "où le formateur fait l'appel à l'aide de la feuille d'émargement.",
          "Accident ou malaise : le déclarer immédiatement au formateur. Le formateur alerte les secours si nécessaire (15, 18, 112) et prévient "
          "MARILYN INSTITUT le jour même. L'employeur effectue la déclaration d'accident du travail ou de trajet.",
          "Alcool, stupéfiants, tabac et vapotage sont interdits dans les locaux (code de la santé publique, art. L.3512-8 et L.3513-6).",
          "Les boissons non alcoolisées sont admises dans la salle ; les repas se prennent hors de la salle, pendant la pause déjeuner."]),
        ("Article 4 — Horaires, présence et émargement",
         ["Horaires : 8h00 – 17h00. Pauses : 10h00-10h15 et 15h00-15h15. Déjeuner : 12h00-13h00.",
          "Chaque stagiaire signe elle-même la feuille d'émargement, le matin et l'après-midi. Signer pour une autre personne, ou pour une "
          "demi-journée non suivie, est une faute grave et peut constituer un faux (code pénal, art. 441-1).",
          "Retard ou absence : prévenir le formateur et l'employeur au plus tôt. Les heures non suivies ne sont pas financées par l'OPCO EP.",
          "Départ anticipé : uniquement avec l'accord du formateur, avec mention de l'heure sur la feuille d'émargement."]),
        ("Article 5 — Comportement",
         ["Attitude respectueuse et bienveillante envers chacune. Sont interdits : propos injurieux, discriminatoires ou humiliants, violence, "
          "harcèlement, dégradation du matériel, introduction de personnes extérieures dans la salle."]),
        ("Article 6 — Téléphone",
         ["Téléphone en mode silencieux pendant les séquences ; utilisé seulement pour une activité demandée par le formateur. "
          "Une stagiaire qui doit rester joignable le signale en début de journée."]),
        ("Article 7 — Images et propriété intellectuelle",
         ["Il est interdit de photographier, filmer ou enregistrer la session, les autres stagiaires ou le formateur sans leur accord écrit. "
          "YEBA FORMATIONS ne photographie aucune stagiaire sans son autorisation écrite, libre et révocable ; un refus est sans conséquence.",
          "Les supports remis sont protégés par le code de la propriété intellectuelle et réservés à un usage professionnel au sein de MARILYN INSTITUT."]),
        ("Article 8 — Confidentialité",
         ["Ce qui est dit en formation reste en formation. On ne cite jamais le nom d'une cliente réelle, on ne montre aucune fiche cliente ni "
          "aucune information de santé d'une cliente. Les cas pratiques utilisent des profils fictifs."]),
        ("Article 9 — Violences, harcèlement, discriminations",
         ["Tolérance zéro (voir rubrique 9 du livret). Sont notamment interdits et pénalement sanctionnés : le harcèlement sexuel (code pénal, "
          "art. 222-33), le harcèlement moral (art. 222-33-2), l'outrage sexiste, toute discrimination (art. 225-1)."]),
        ("Article 10 — Données personnelles et intelligence artificielle",
         ["Les données des stagiaires sont traitées conformément au RGPD (voir Annexe B).",
          "Aucun système d'intelligence artificielle n'est utilisé pour évaluer, noter ou classer les stagiaires : la correction est réalisée "
          "par le formateur. Certains supports ont été conçus avec l'assistance d'une IA générative, puis vérifiés et validés par le formateur "
          "(règlement (UE) 2024/1689, art. 50)."]),
        ("Article 11 — Sanctions",
         ["Constitue une sanction toute mesure, autre qu'une observation verbale, prise par le directeur à la suite d'un agissement fautif "
          "(art. R.6352-3). Par ordre croissant : avertissement écrit ; blâme ; exclusion temporaire ; exclusion définitive. "
          "Les amendes et sanctions pécuniaires sont interdites.",
          "En cas d'urgence (violence, mise en danger, état d'ivresse, harcèlement), le formateur peut prononcer une exclusion temporaire "
          "immédiate à titre conservatoire (art. R.6352-7)."]),
        ("Article 12 — Garanties de procédure",
         ["Aucune sanction sans information préalable des griefs (R.6352-4). Convocation écrite à un entretien, avec possibilité d'être assistée "
          "(R.6352-5). Sanction écrite et motivée, notifiée entre un jour franc et 15 jours après l'entretien (R.6352-6). "
          "L'employeur et l'OPCO EP sont informés (R.6352-8). Pour une session d'une journée, la procédure se déroule après la session."]),
        ("Article 13 — Représentation des stagiaires",
         ["L'élection de délégués n'est obligatoire que pour les actions de plus de 500 heures (R.6352-9) : elle ne s'applique pas ici."]),
        ("Article 14 — Réclamations",
         [f"Par oral au formateur ou par écrit à {D.ORG['email']}. Accusé de réception sous 5 jours ouvrés, réponse motivée sous 15 jours ouvrés."]),
        ("Article 15 — Accessibilité",
         ["Toute personne ayant un besoin particulier peut contacter le référent handicap, sans avoir à indiquer de diagnostic."]),
        ("Article 16 — Entrée en vigueur",
         ["Le présent règlement est remis avant l'entrée en formation (art. L.6353-8) et rappelé à l'ouverture de la session. "
          "Il s'applique aux sessions des 28 et 29 septembre 2026."]),
    ]
    for titre, paras in art:
        doc.h2(titre)
        for x in paras:
            doc.p(x, taille=11)
    doc.p("Fait à Sainte-Clotilde, le 27 septembre 2026 — Aurélien LUMEKA, directeur de YEBA FORMATIONS", gras=True, taille=11)
    doc.saut()

    # ------------------------------------------------------------- Notice RGPD
    doc.h1("Annexe B — Notice d'information sur le traitement de vos données personnelles")
    doc.p("Articles 13 et 14 du règlement (UE) 2016/679 (RGPD) — Annexe 3 de la convention.", taille=10, italique=True)
    doc.p(("Responsable du traitement : ", {"b": True}),
          f"YEBA FORMATIONS, représentée par Aurélien LUMEKA, directeur — {D.ORG['adresse']}, {D.ORG['cp_ville']} — {D.ORG['email']}.")
    doc.table([
        ["Données", "Pourquoi ?", "Base légale", "Durée"],
        ["Identité, fonction, établissement, émargements, attestation", "Organiser la formation et justifier sa réalisation auprès de l'employeur et de l'OPCO EP",
         "Contrat et obligation légale (art. 6.1.b et 6.1.c ; code du travail L.6353-1)", "3 ans après la fin de l'action ; plus si une règle comptable ou de contrôle l'impose"],
        ["Réponses au positionnement, grille, quiz, plan d'action", "Adapter la formation, mesurer l'atteinte des objectifs",
         "Obligation légale (L.6353-1) et intérêt légitime (Qualiopi)", "3 ans"],
        ["Questionnaires de satisfaction", "Améliorer les formations", "Intérêt légitime", "3 ans"],
        ["Besoin d'aménagement", "Adapter la formation", "Votre demande ; seule la nature de l'aménagement est notée, jamais la raison", "Fin de la session"],
        ["Photo ou vidéo", "Uniquement les usages que vous avez cochés", "Votre consentement (art. 6.1.a) — retrait possible à tout moment", "Durée choisie dans l'autorisation"],
    ], [4.2, 4.8, 4.6, 3.8], taille=9.5)
    doc.h2("Qui reçoit vos données ?")
    doc.puces([
        "Votre employeur, MARILYN INSTITUT : présence, attestation, certificat. Vos réponses individuelles au positionnement et vos réponses libres "
        "ne lui sont PAS transmises : il ne reçoit qu'une synthèse anonymisée du groupe (convention, art. 9).",
        "L'OPCO EP : émargements et certificat de réalisation, pour le financement.",
        "L'organisme certificateur Qualiopi et les services de contrôle de l'État, uniquement en cas d'audit ou de contrôle.",
        "Les prestataires techniques de YEBA FORMATIONS (questionnaire en ligne, stockage), liés par contrat.",
    ], taille=11)
    doc.h2("Hébergement")
    doc.p("YEBA FORMATIONS privilégie des outils hébergés dans l'Union européenne. Le questionnaire de positionnement a été réalisé avec Drag'n Survey, "
          "éditeur français. Si un prestataire situé hors de l'Union intervient, le transfert est encadré par les garanties des articles 44 et suivants du RGPD, "
          "et vous en êtes informée.", taille=11)
    doc.h2("Aucune décision automatisée")
    doc.p("Aucune note, aucun classement et aucune décision vous concernant n'est produit par une intelligence artificielle ni de façon "
          "entièrement automatisée (RGPD, art. 22 ; règlement (UE) 2024/1689).", taille=11)
    doc.h2("Vos droits")
    doc.p(f"Accès, rectification, effacement, limitation, opposition, retrait du consentement : écrivez à {D.ORG['email']}. "
          "Réponse sous un mois. Vous pouvez aussi saisir la CNIL (www.cnil.fr — 3 place de Fontenoy, 75007 Paris).", taille=11)
    doc.saut()

    # ------------------------------------------------------------- Attestation
    doc.h1("Attestation de remise et de prise de connaissance")
    doc.p("Je soussignée, stagiaire de l'action « " + D.ACTION["intitule"] + " » organisée par YEBA FORMATIONS pour MARILYN INSTITUT, "
          "atteste avoir reçu, lu et compris le livret d'accueil, le règlement intérieur (Annexe A) et la notice d'information sur mes données "
          "personnelles (Annexe B), et m'engage à respecter le règlement intérieur.")
    doc.cases(["Session du lundi 28 septembre 2026", "Session du mardi 29 septembre 2026"])
    doc.signatures(["La stagiaire", "Nom et prénom :", "Date :", "Signature :"],
                   ["Pour YEBA FORMATIONS", "Aurélien LUMEKA, directeur", "Date :", "Signature :"], hauteur_cm=3.2)
    doc.p("Exemplaire conservé au dossier de la session (preuve de remise — Qualiopi, indicateur 9).", taille=9, italique=True)

    doc.h1("Mon plan d'action — « Ma Promesse Marilyn »")
    doc.p("À compléter en fin de journée, puis à relire avec votre responsable.", italique=True, taille=11)
    doc.table([
        ["Question", "Ma réponse"],
        ["Ce que je retiens de la journée", ""],
        ["Ce que j'applique dès demain en institut", ""],
        ["Quand, avec qui, et comment je mesure mon progrès", ""],
        ["Ma phrase qui rebooke", ""],
    ], [6.4, 11], taille=11, hauteur_cm=2.4)
    return [doc.enregistrer(OUT / "Livret_accueil_complet_programme_reglement_RGPD.docx")]


if __name__ == "__main__":
    print(construire())

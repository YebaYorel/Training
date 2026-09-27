"""Diaporama projeté — « Excellence de la relation cliente et vente-conseil en institut ».

Même support pour les deux groupes (programme identique). Aucun nom de stagiaire à l'écran (RGPD).
Les notes du présentateur contiennent le script, les timings et les questions de débriefing.
"""
import donnees as D
from ppt_lib import Deck, BLEU, VERT, ROUGE, OR
from pptx.dml.color import RGBColor

OUT = D.SORTIE / "04_PEDAGOGIE"


def construire():
    OUT.mkdir(parents=True, exist_ok=True)
    k = Deck(str(D.ICI / "logo_1200.png"), str(D.ICI / "logo_blanc_1200.png"))

    # ------------------------------------------------------------------ OUVERTURE
    k.couverture("Excellence de la relation cliente & vente-conseil en institut",
                 "MARILYN INSTITUT · L'OR DES ÎLES",
                 ["28 et 29 septembre 2026 · C.R.E.P.S de Saint-Denis", "Aurélien LUMEKA · YEBA FORMATIONS"],
                 note="7h45 : diapositive affichée à l'arrivée. NE PAS la commenter : à 8h00 précises, vous jouez « l'incident » "
                      "(voir diapositive 3) AVANT de vous présenter. Préparer : feuille d'émargement, positionnement express, kit de cartes, "
                      "post-it, paperboard, chrono visible, eau. Chaises à dossier pour toutes.")
    k.mots("Notre journée", ["8h00 → 17h00", "Pauses : 10h00 · 15h00", "Déjeuner : 12h00 → 13h00", "Téléphone : silencieux",
                             "Issues de secours : ici →"], taille=34,
           note="8h10 (après l'incident et le débriefing). Montrer physiquement les issues de secours et le point de rassemblement du C.R.E.P.S. "
                "Émargement du matin MAINTENANT si pas encore fait. Rappeler : repas à prévoir, pris hors de la salle. "
                "Pauses libres : chacune peut sortir quand elle en a besoin, sans demander. Faire signer l'attestation de remise du règlement intérieur "
                "par les stagiaires qui ne l'ont pas encore signée.")
    k.citation("Qu'avez-vous ressenti ?", "3 mots · 3 post-it", titre_access="Séquence 0 — l'incident",
               note="SÉQUENCE 0 — 8h00-8h15. Accueil volontairement raté pendant 2 minutes (téléphone en main, pas de regard, "
                    "« installez-vous, j'arrive », mastication…). Puis STOP. Distribuer 3 post-it à chacune : 3 mots sur ce qu'elles ont ressenti. "
                    "Collage au mur (« Le mur des ressentis »). Puis rejouer le même accueil aux standards (regard, sourire, se lever, prénom). "
                    "Question de débriefing : « Qu'est-ce qui a changé ? À quel moment votre avis était-il déjà fait ? » → réponse attendue : "
                    "avant même que je parle. C'est le fil de toute la journée.")
    k.mots("Je suis · Je fais · Ma fierté", ["Je suis… (prénom)", "Je fais… (mon métier, mon institut)",
                                             "Ma fierté… (un merci de cliente)"], taille=32,
           note="8h30-8h45. Tour de table rapide, 1 minute chacune, en commençant par vous. Positionnement express : distribuer la fiche, "
                "2 minutes, colonne MATIN. Les stagiaires qui n'ont pas répondu au questionnaire en ligne se positionnent ici.")
    k.consigne("Le Panier des attentes", ["3 post-it", "1 attente = 1 post-it", "Dans le panier !"], "3 min",
               "Post-it · panier",
               note="Recueil des attentes. Les attentes restent affichées toute la journée ; on y revient à 16h40 (dernière diapositive). "
                    "Attentes déjà exprimées dans le questionnaire (sans les attribuer) : des outils concrets, être plus à l'aise pour conseiller, "
                    "échanger avec les collègues, mieux communiquer dans l'équipe.")
    k.mots("Ce soir, vous saurez…", ["Soigner l'image · Accueillir", "Découvrir le besoin", "Conseiller sans forcer · Objections",
                                     "Faire revenir · Temps creux", "Feedback · Chiffres · RGPD"], taille=32,
           note="Les 10 objectifs contractuels (annexe 1 de la convention), regroupés en 5 lignes. Les lire tous à voix haute : "
                "1 Charte d'Image ; 2 parcours cliente ; 3 S.O.I.N. ; 4 P.E.R.L.E. ; 5 cinq objections ; 6 reprise de RDV ; "
                "7 temps creux ; 8 A.R.P. ; 9 contribution au CA et au remplissage des agendas ; 10 RGPD fiche cliente.")
    k.acronyme("Le protocole M.A.R.I.L.Y.N.", [("M", "Miroir : mon image"), ("A", "Accueil : le parcours"), ("R", "Ressenti : le besoin"),
                                                ("I", "Initiative : les temps creux"), ("L", "Lien : conseiller"),
                                                ("Y", "Y revenir : fidéliser"), ("N", "Nous : l'équipe")], colonnes=1, taille=32,
            note="Le fil rouge : 7 lettres, 7 réflexes, le nom de VOTRE institut. Dans la journée, on suit l'ordre M, A, R, L, Y, I, N "
                 "(I passe après la pause de l'après-midi). À la fin, chacune doit pouvoir réciter les 7 lettres.")
    k.compare("Ce que vous m'avez dit", ("Vos forces", ["Reprise de RDV : 4,8 / 5", "Temps creux : 4,2 / 5", "Accueil : 4,0 / 5"], VERT, "✔"),
              ("À travailler", ["Parler chiffres : 2,8", "Remarques : 3,0", "« C'est trop cher » : 3,2"], BLEU, "→"),
              note="Retour COLLECTIF et ANONYME du questionnaire de positionnement (5 répondantes sur 8). Ne jamais attribuer une réponse. "
                   "Message : « Vous savez déjà beaucoup. Aujourd'hui on transforme le savoir en réflexe. » Annoncer : plus de temps sur "
                   "les objections (le Ring !) et un atelier « Mon agenda, mes chiffres ». Cette diapositive est une preuve de l'indicateur 8.")
    k.mots("Nos règles du jeu", ["Bienveillance", "Droit à l'erreur · droit au joker", "D'abord en binôme, puis en groupe",
                                 "Ce qui est dit ici reste ici", "Aucune cliente réelle nommée"], taille=32,
           note="Règles co-validées : demander « d'accord ? » après chaque ligne. Le joker : chacune peut passer son tour une fois, sans justifier. "
                "Personne ne joue devant le groupe sans s'être entraînée en binôme. Phrases d'appui autorisées (cartes à lire) pendant les jeux de rôle.")
    k.mots("Transparence : vos données", ["Conservées 3 ans · YEBA FORMATIONS", "Employeur : synthèse anonyme",
                                          "Notes : par le formateur, pas par une IA", "Photo : seulement avec accord écrit",
                                          "Vos droits : yebaformations@gmail.com"], taille=28,
           note="5 minutes — RGPD (art. 13) et IA Act (art. 50). Les supports ont été conçus avec l'aide d'une IA générative puis vérifiés par moi. "
                "Aucune IA ne note, ne classe ni n'évalue. Distribuer les fiches de droit à l'image : facultatives, refus sans conséquence. "
                "Ne photographier personne qui n'a pas signé l'autorisation.")

    # ------------------------------------------------------------------ M
    k.section("M", "Le Miroir", "Tenue · présentation · attitude", "9h00 – 10h00",
              note="Séquence M — objectif 1 : appliquer les standards de la Charte d'Image Marilyn.")
    k.tuiles("L'image professionnelle", [("1", "Apparence"), ("2", "Langage"), ("3", "Comportement")], taille_grand=80, taille_petit=30,
             note="3 niveaux. Demander un exemple concret de chaque niveau vu dans un institut (sans nommer d'institut). "
                  "Apparence : tenue, cheveux, ongles. Langage : vocabulaire, voix, tutoiement. Comportement : téléphone, posture, regard, mastication.")
    k.compare("7 % · 38 % · 55 % : vrai ou faux ?", ("Ce qui est prouvé", ["Un sentiment ambigu", "Un mot isolé", "Voix et visage comptent"], VERT, "✔"),
              ("Ce qu'on lui fait dire", ["« Les mots : 7 % »", "Valable partout", "L'argument est inutile"], ROUGE, "✘"),
              note="A. Mehrabian, Silent Messages, 1971 : l'étude portait sur des mots isolés exprimant un sentiment, en laboratoire. "
                   "Elle ne dit PAS que les mots comptent pour 7 %. Retenir : quand la voix et le visage contredisent les mots, c'est la voix "
                   "et le visage qu'on croit. Une cliente entend « bienvenue » mais voit un visage fermé : elle croit le visage.")
    k.consigne("Le Photomaton inversé", ["En binôme, face à face", "3 secondes : je regarde ma binôme",
                                         "Ce que je crois montrer / ce qu'elle voit", "On échange les rôles"], "10 min",
               "Fiche Photomaton\n(kit, page 1)",
               note="9h15-9h25. Chacune note d'abord ce qu'elle CROIT montrer (« calme, souriante »), puis la binôme note ce qu'elle VOIT en 3 secondes. "
                    "Comparaison. Consigne de bienveillance : on décrit des faits observables (« bras croisés »), jamais un jugement (« tu as l'air fermée »).")
    k.mots("Charte d'Image Marilyn : on vote !", ["Tenue · cheveux · ongles", "Bijoux · chaussures", "Téléphone · mastication",
                                                  "Posture · regard", "Voix"], taille=34,
           note="9h25-9h50. LIVRABLE CO-CONSTRUIT n°1. Pour chacun des 10 points, le groupe écrit UNE règle concrète et vérifiable "
                "(ex. : « ongles : manucure impeccable, c'est notre vitrine » ; « téléphone : jamais visible en cabine »). Vote à main levée. "
                "Recopier au propre sur la trame du kit. Les deux groupes (lundi et mardi) produisent leur version : on les fusionne pour la direction.")
    k.mots("Ma voix au service de la cliente", ["Débit lent", "Sourire qui s'entend", "Phrases courtes", "Une pause avant le prix",
                                                "Mes phrases d'appui"], taille=34,
           note="9h50-10h00. Réponse à une attente du questionnaire (« savoir quoi répondre sans perdre mes moyens »). Distribuer les "
                "cartes « Phrases d'appui » du kit : elles peuvent être lues pendant les jeux de rôle. Exercice éclair : chacune dit "
                "« Bonjour, bienvenue chez Marilyn » 3 fois : vite, puis lentement, puis lentement en souriant. Le groupe vote la meilleure.")
    k.citation("Pause", "10h00 – 10h15", titre_access="Pause du matin", taille=80,
               note="Pause de 15 minutes. Afficher la Charte d'Image au mur pendant la pause.")

    # ------------------------------------------------------------------ A
    k.section("A", "L'Accueil", "Le parcours cliente de A à Z", "10h15 – 11h15",
              note="Séquence A — objectif 2 : conduire le parcours cliente en sécurisant les moments de vérité.")
    k.citation("Chaque contact est une note", "Les moments de vérité — J. Carlzon", fond=RGBColor(0xF7, 0xF7, 0xF5), taille=50,
               titre_access="Les moments de vérité",
               note="Jan Carlzon, Moments of Truth (1987) : chaque contact entre la cliente et l'entreprise est un « moment de vérité » où elle "
                    "se fait un avis. Question : « Combien de moments de vérité dans une épilation des jambes ? » Laisser compter. On en trouve plus de 10.")
    k.parcours("Le voyage de la cliente", ["Prise de RDV", "Arrivée, parking", "Porte", "Accueil", "Attente", "Vestiaire",
                                           "Installation", "Soin", "Sortie de cabine", "Conseil", "Encaissement", "Au revoir"],
               note="Les 12 étapes. Atelier « La Carte du Voyage Cliente » (10h30-10h45) : sur le paperboard, chaque binôme note chaque étape "
                    "avec 🙂 😐 ☹ pour SON institut, puis identifie 3 points noirs et 1 correctif par point noir. LIVRABLE n°2.")
    k.compare("La règle du pic et de la fin", ("On retient…", ["Le moment le plus fort", "Le tout dernier moment"], VERT, "✔"),
              ("On oublie…", ["La moyenne", "La durée"], ROUGE, "✘"),
              note="D. Kahneman et al., 1993 (« When more pain is preferred to less ») : la mémoire d'une expérience retient surtout le pic "
                   "et la fin. Conséquence : la sortie de cabine et l'encaissement pèsent plus lourd que le soin lui-même. "
                   "Or ce sont souvent les étapes les plus bâclées. Question : « Comment finit une visite chez Marilyn aujourd'hui ? »")
    k.acronyme("Les 7 premières secondes", [("1", "Je m'arrête"), ("2", "Je regarde"), ("3", "Je souris"), ("4", "« Bonjour »"),
                                            ("5", "Son prénom")], taille=34,
             note="Le rituel d'accueil. Même si je suis au téléphone ou en train de ranger : je m'interromps. Démonstration par vous, puis "
                  "chacune le fait une fois. Rappel du positionnement : la première impression se fait en quelques secondes (4 sur 5 l'ont dit).")
    k.consigne("Jeu n°1 — Les 8 Clientes", ["Je tire une carte cliente", "Ma binôme m'accueille : 3 min",
                                            "Les autres observent (grille)", "Débrief : le piège de la carte"], "20 min",
               "8 cartes Clientes\n(kit, jeu n°1)",
               note="10h50-11h10. La pressée, la muette, la comparatrice, la fidèle qui ne consomme plus, la mécontente, la première fois, "
                    "l'accompagnée, la V.I.P. Arrêter la scène dès que le comportement clé apparaît. Débriefing sur le « piège » écrit sur la carte. "
                    "Observatrices : critères 2 et 3 de la grille. Les plus expérimentées jouent l'« observatrice experte ».")

    # ------------------------------------------------------------------ R
    k.section("R", "Le Ressenti", "Découvrir le besoin avant de proposer", "11h15 – 12h00",
              note="Séquence R — objectif 3 : découverte structurée avec S.O.I.N.")
    k.tuiles("La méthode S.O.I.N.", [("S", "Situer"), ("O", "Observer"), ("I", "Interroger"), ("N", "Nommer")], taille_grand=90, taille_petit=30,
             note="Situer : le contexte (« c'est pour une occasion ? »). Observer : un indice concret (peau, ongles, attitude). "
                  "Interroger : au moins 3 questions ouvertes AVANT toute proposition. Nommer : reformuler le besoin avec SES mots. "
                  "C'est « Nommer » qui donne à la cliente le sentiment d'être comprise.")
    k.compare("Ouvrir ou fermer ?", ("Ouvre", ["« Qu'est-ce qui vous amène ? »", "« Racontez-moi votre routine »",
                                                            "« Qu'aimeriez-vous changer ? »"], VERT, "✔"),
              ("Ferme… ou vexe", ["« Vous voulez le forfait ? »", "« Vous avez pris du soleil ? »",
                                               "« Toujours pas racheté ? »"], ROUGE, "✘"), taille=26,
              note="Une question qui ferme trop tôt coûte la vente. Une question qui vexe coûte la vente ET la cliente.")
    k.consigne("Jeu n°2 — Les 12 Questions d'Or", ["12 cartes sur la table", "3 familles : ouvre · ferme · vexe", "Classez en équipe",
                                                   "Défendez vos choix"], "15 min", "12 cartes Questions\n(kit, jeu n°2)",
               note="11h25-11h40. Corrigé indicatif — OUVRENT : 1, 2, 4, 6, 8, 9, 11. FERMENT : 3, 12 (utiles pour conclure, jamais pour découvrir). "
                    "VEXENT : 5, 7, 10. Le formateur n'arbitre qu'à la fin : faire défendre chaque classement.")
    k.citation("Si je vous ai bien comprise, vous aimeriez…", "Reformuler avec SES mots", titre_access="Reformuler",
               note="Entraînement éclair : chacune reformule la situation d'une carte cliente en une phrase commençant par cette formule. "
                    "Piège : ajouter sa propre interprétation (« vous avez la peau abîmée »). On reprend les mots de la cliente, pas les nôtres.")
    k.compare("La fiche cliente & le RGPD", ("J'écris", ["Ce qui est utile au soin", "Les préférences (boisson, musique)",
                                                         "L'accord pour les SMS"], VERT, "✔"),
              ("Je n'écris pas", ["Un avis sur la personne", "Un diagnostic médical", "Une info de santé inutile"], ROUGE, "✘"),
              note="5 minutes. Une allergie ou une contre-indication est une DONNÉE DE SANTÉ (RGPD, art. 9) : on ne la note que si elle est "
                   "nécessaire au soin, accès réservé à l'équipe, jamais lue à voix haute devant une autre cliente, jamais envoyée par messagerie "
                   "personnelle. [RGPD] Quand une cliente demande « pourquoi vous notez ça ? », savoir répondre : « pour votre sécurité pendant le soin ».")
    k.citation("Bon appétit !", "12h00 – 13h00 · repas hors de la salle", titre_access="Pause déjeuner", taille=70,
               note="Pause déjeuner. Rappeler l'émargement de l'après-midi à 13h00.")

    # ------------------------------------------------------------------ Réveil + L
    k.consigne("Réveil : les 7 secondes", ["Je sors, je rentre", "Accueil parfait en 7 secondes", "Le groupe : 3 pouces ?"], "15 min",
               "Assise ou debout,\nau choix",
               note="13h00-13h15. ÉMARGEMENT DE L'APRÈS-MIDI d'abord. Chacune rejoue son accueil en 7 secondes chrono. "
                    "Évaluation par les pouces (1 à 3). Participation assise ou debout, au libre choix de chacune.")
    k.section("L", "Le Lien", "Conseiller sans forcer", "13h15 – 14h30",
              note="Séquence L — objectifs 4 et 5 : recommandation par le bénéfice (P.E.R.L.E.) et traitement des objections. "
                   "Séquence allongée à 75 minutes suite au positionnement (3,2/5 sur « recommander sans forcer » et « c'est trop cher »).")
    k.compare("Conseiller ou forcer ?", ("Je conseille", ["Je pars de SON besoin", "Je propose UNE chose", "Elle choisit"], VERT, "✔"),
              ("Je force", ["Je pars de MON stock", "J'empile les produits", "J'insiste"], ROUGE, "✘"),
              note="La frontière : qui décide ? Une cliente qui s'est sentie forcée ne revient pas, même si elle a acheté.")
    k.tuiles("Caractéristique → Bénéfice", [("Ce que c'est", "« Contient de la vitamine C »"), ("→", "« … ce qui veut dire pour vous… »"),
                                            ("Ce que ça change", "« Un teint plus lumineux, comme vous le souhaitiez »")],
             taille_grand=40, taille_petit=26,
             note="La phrase-pont : « … ce qui veut dire pour vous… ». Une caractéristique décrit le produit ; un bénéfice décrit la vie de la cliente. "
                  "Le meilleur bénéfice reprend un mot dit par la cliente pendant la découverte (S.O.I.N.).")
    k.consigne("Jeu n°3 — Bénéfice ?", ["20 cartes, 2 paquets", "Triez en 4 minutes", "Échangez, vérifiez",
                                                            "Transformez 3 cartes"], "12 min", "20 cartes\n(kit, jeu n°3)",
               note="13h25-13h37. Corrigé — BÉNÉFICES : cartes 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. Toutes les autres sont des caractéristiques "
                    "ou de la preuve sociale (carte 9 « meilleure vente du mois » n'est PAS un bénéfice). La 2e manche est la plus formatrice.")
    k.acronyme("La méthode P.E.R.L.E.", [("P", "Partir de son besoin"), ("E", "Expliquer le bénéfice"), ("R", "Recommander UNE chose"),
                                         ("L", "Laisser choisir"), ("E", "Encaisser sans se justifier")], taille=34,
             note="P : « Vous m'avez dit que… ». E : bénéfice pour elle. R : une seule recommandation. L : silence, elle choisit. "
                  "E : on annonce le prix sans s'excuser et on encaisse. Démonstration complète par vous en 90 secondes.")
    k.grand_nombre("1", ["UNE seule recommandation", ("Deux produits = deux doutes", {"t": 30, "c": RGBColor(0x5A, 0x5F, 0x6A)})],
                   titre_access="Une seule recommandation",
                   note="Au positionnement, 2 répondantes sur 5 recommanderaient 2 produits en fin de soin. La règle : UNE chose, la plus utile "
                        "pour le besoin nommé. Si elle en veut plus, c'est elle qui le demande.")
    k.compare("Promettre juste", ("Je peux dire", ["« Hydrate »", "« Apaise la sensation de tiraillement »", "« Illumine le teint »"], VERT, "✔"),
              ("Je ne dis jamais", ["« Guérit »", "« Soigne l'eczéma »", "« Fait disparaître les rides »"], ROUGE, "✘"), taille=26,
              note="Un produit cosmétique ne peut pas revendiquer d'effet thérapeutique ni tromper la cliente (règlement (CE) 1223/2009, art. 20 ; "
                   "règlement (UE) 655/2013 : critères communs des allégations). Promettre trop, c'est aussi perdre la confiance.")
    k.mots("Les 5 objections du quotidien", ["« C'est cher »", "« Je vais réfléchir »", "« J'en ai déjà »", "« Je ne suis pas sûre »",
                                             "« Il faut que j'en parle »"], taille=34,
           note="Faire deviner les 5 avant d'afficher. Une objection n'est pas un refus : c'est une demande d'information ou de réassurance.")
    k.acronyme("Répondre en 4 temps", [("1", "Accueillir : « Je comprends »"), ("2", "Questionner : « Par rapport à quoi ? »"),
                                       ("3", "Répondre par le bénéfice"), ("4", "Vérifier : « Cela vous convient ? »")], taille=32,
             note="Accueillir : « Je comprends ». Questionner : « Par rapport à quoi ? » / « Qu'est-ce qui vous fait hésiter ? ». "
                  "Répondre : revenir au bénéfice pour ELLE. Vérifier : « Est-ce que cela répond à votre question ? ». "
                  "Jamais : brader, se justifier sur les coûts de l'institut, critiquer un concurrent.")
    k.citation("C'est cher… par rapport à quoi ?", "Questionner avant de répondre", titre_access="Objection prix",
               note="La question distingue 3 situations : le prix (comparaison), le budget (moyen de payer), l'utilité (elle ne voit pas le bénéfice). "
                    "Trois réponses différentes. 5 répondantes sur 5 connaissaient ce réflexe : on passe du savoir au faire.")
    k.mots("Annoncer le prix", ["Voix stable", "Regard franc", "Pas d'excuse", "Puis… silence"], taille=38,
           note="Exercice éclair : chacune annonce « Le soin est à 65 euros » (prix fictif) en regardant sa binôme, puis se tait 3 secondes. "
                "Le silence après le prix est la chose la plus difficile — et la plus efficace.")
    k.consigne("Le Ring des objections", ["Je tire une carte objection", "Je réponds en 4 temps", "3 rounds de 2 min", "Le public note"],
               "25 min", "10 cartes Objections\n+ phrases d'appui",
               note="13h55-14h20. Nouveau jeu créé suite au positionnement. Rounds en binôme, puis 1 round devant le groupe (volontaires). "
                    "Les phrases d'appui peuvent être lues. Observatrices : critères 5, 6 et 7 de la grille. Relevez 1 point fort par passage.")

    # ------------------------------------------------------------------ Y
    k.section("Y", "Y revenir", "Fidéliser · reprendre rendez-vous", "14h30 – 15h00",
              note="Séquence Y — objectifs 6 et 9. Point fort du groupe (4,8/5) : le groupe écrit lui-même le standard.")
    k.grand_nombre("N°1", ["Le taux de reprise de rendez-vous", ("L'indicateur qui remplit l'agenda", {"t": 30, "c": RGBColor(0x5A, 0x5F, 0x6A)})],
                   titre_access="Indicateur numéro 1",
                   note="Taux de reprise = nombre de clientes qui reprennent RDV avant de partir / nombre de clientes reçues. "
                        "Question : « Qui connaît son taux ? » (réponse probable : personne — c'est normal, on l'apprend maintenant).")
    k.mots("Mes chiffres — exemple fictif", ["1 soin à 45 € toutes les 4 semaines", "= environ 13 visites par an",
                                                         "= environ 585 € par cliente fidèle", "1 reprise de RDV de plus par jour…",
                                                         "… combien sur un an ?"], taille=30,
           note="10 minutes. Atelier ajouté suite au positionnement (2,8/5 : point le plus faible). Chiffres FICTIFS, à le dire clairement. "
                "Calcul collectif au paperboard : 1 cliente fidélisée de plus par jour, 5 jours par semaine, pendant un an. "
                "Objectif 9 : chacune sait citer les 3 indicateurs sur lesquels son travail pèse : remplissage de son agenda, taux de reprise, ventes produits.")
    k.consigne("La Phrase qui Rebooke", ["J'écris 3 formulations", "On lit, on vote", "La gagnante = notre standard"], "15 min",
               "Post-it · paperboard",
               note="14h40-14h55. LIVRABLE n°3 : la formulation retenue devient le standard des deux instituts. Exemple à NE PAS donner avant : "
                    "« Pour garder ce résultat, je vous propose de revenir dans 4 semaines : plutôt le mardi ou le samedi ? » (question alternative).")
    k.compare("SMS de rappel & RGPD", ("Cliente existante", ["Soins analogues : OK", "« STOP » à chaque SMS",
                                                             "Informée à la collecte"], VERT, "✔"),
              ("Prospect", ["Accord préalable", "Case jamais pré-cochée", "Preuve de l'accord"], BLEU, "!"),
              taille=24,
              note="5 minutes. [RGPD + CPCE art. L.34-5] La prospection par SMS exige le consentement préalable, sauf pour une cliente existante "
                   "et des produits ou services analogues, à condition qu'elle ait été informée et puisse refuser simplement (STOP) à chaque envoi. "
                   "Le rappel d'un RDV déjà pris n'est pas de la prospection.")
    k.citation("Pause", "15h00 – 15h15", titre_access="Pause de l'après-midi", taille=80, note="Pause de 15 minutes.")

    # ------------------------------------------------------------------ I
    k.section("I", "L'Initiative", "Les temps creux deviennent utiles", "15h15 – 15h40",
              note="Séquence I — objectif 7. Point fort pour une partie du groupe (4,2/5), mais très hétérogène.")
    k.consigne("Les 20 Gestes de Valeur", ["Seules ou en binôme", "20 actions utiles en 10 min de creux", "On met tout en commun"], "8 min",
               "Post-it",
               note="Exemples si le groupe sèche : rappeler les clientes « en retard » de reprise, préparer les cabines du lendemain, "
                    "mettre à jour la vitrine, préparer des échantillons, vérifier les stocks, se former sur un produit, soigner les réseaux.")
    k.compare("Valeur ou effort ?", ("À faire d'abord", ["Forte valeur", "Faible effort"], VERT, "1"),
              ("À planifier", ["Forte valeur", "Effort important"], BLEU, "2"),
              note="Matrice valeur / effort : placer les 20 post-it. Les « faible valeur » sont écartés. LIVRABLE n°4 : la Roue des Temps Creux "
                   "(trame dans le kit), affichée en réserve dans les deux instituts.")
    k.mots("Entre deux clientes : 60 secondes", ["La cabine est prête", "La fiche est à jour", "Le prochain RDV est vérifié",
                                                 "Le produit conseillé est noté", "Je respire"], taille=32,
           note="Check-list ajoutée suite à une situation vécue du questionnaire : l'organisation quand le planning est plein et qu'on est seule. "
                "Elle est dans la ressource PDF.")

    # ------------------------------------------------------------------ N
    k.section("N", "Nous", "Feedback · équipe · deux instituts", "15h40 – 16h20",
              note="Séquence N — objectif 8 (A.R.P.) et cohérence des deux instituts. Remarques : 3,0/5 au positionnement → prudence et progressivité.")
    k.tuiles("Face à une remarque, on…", [("1", "se défend"), ("2", "se tait"), ("3", "se justifie"), ("4", "accueille")],
             taille_grand=80, taille_petit=30,
             note="Les 4 réactions spontanées. Toutes sont humaines. Seule la 4e fait avancer. Demander : « Laquelle est la vôtre, "
                  "les jours de fatigue ? » (réponse à main levée, facultative).")
    k.tuiles("La méthode A.R.P.", [("A", "Accuser réception"), ("R", "Reformuler"), ("P", "Proposer")], taille_grand=90, taille_petit=30,
             note="A : « D'accord, je note. » R : « Si je comprends bien, il faudrait… » P : « Je propose de… à partir de… ». "
                  "Ni justification, ni interruption. Démonstration par vous.")
    k.consigne("Le Boomerang", ["Je reçois une remarque", "Je réponds en A.R.P.", "D'abord en binôme", "Puis 1 volontaire"], "12 min",
               "Cartes Remarques\n(douce → ferme)",
               note="15h50-16h02. Remarques graduées, de douce à ferme. En binôme d'abord. Personne n'est obligée de passer devant le groupe. "
                    "Réponse à une attente exprimée : faire une place aux idées de chacune dans l'équipe.")
    k.consigne("Les 7 Merveilles de la Beauté", ["2-3 cartes par binôme", "Qu'installe-t-on lundi, sans budget ?", "2 min de restitution",
                                                 "Vote : nos 10 standards"], "18 min", "7 cartes Merveilles\n(kit, jeu n°4)",
               note="16h02-16h20. LIVRABLE n°5 : 10 standards communs aux deux instituts. Un standard est réservé à un rituel d'équipe "
                    "(ex. : 5 minutes d'idées par semaine) — proposé à la direction, non imposé. Une idée = une action + un responsable + une date.")

    # ------------------------------------------------------------------ CLÔTURE
    k.citation("Le quiz !", "10 questions · en équipes · sur l'écran", titre_access="Quiz d'évaluation", taille=80,
               note="16h20-16h40. Ouvrir le fichier « Quiz_interactif_Marilyn.html » (fonctionne SANS internet, aucune donnée collectée). "
                    "Deux équipes. Chaque stagiaire remplit AUSSI sa feuille-réponse individuelle (preuve pour l'attestation). "
                    "Correction commentée après chaque question. Seuil de réussite individuel : 7/10.")
    k.consigne("Ma Promesse Marilyn", ["Ce que j'applique demain", "Avec qui, quand", "Je signe"], "5 min", "Livret d'accueil,\ndernière page",
               note="16h40. Engagement individuel écrit, daté et signé. Puis positionnement express colonne SOIR (2 minutes).")
    k.mots("Retour au Panier des attentes", ["Attente atteinte ✔", "Attente en partie ↗", "Attente à suivre →"], taille=36,
           note="On relit chaque post-it du matin. Ce qui n'a pas été couvert est noté : il sera transmis (sans nom) dans le bilan.")
    k.fin("Merci !", ["Questionnaire de satisfaction · émargement", "Ressource PDF envoyée après la session",
                      "Aurélien LUMEKA · 06 93 32 24 45", "yebaformations@gmail.com"],
          note="16h50-17h00. Questionnaire de satisfaction à chaud (papier). Émargement de l'après-midi vérifié. Remettre la ressource PDF "
               "(ou l'envoyer par e-mail en Cci — jamais en copie visible). Récupérer les fiches de droit à l'image signées.")
    return k.enregistrer(OUT / "Diaporama_Marilyn_Institut_relation_cliente_vente_conseil.pptx")


if __name__ == "__main__":
    print(construire())

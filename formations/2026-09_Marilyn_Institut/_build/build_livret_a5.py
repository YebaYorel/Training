"""Livret d'accueil au format du livret « paysage » d'A. LUMEKA (22-23/09/2026) :
pages A5, imposées 2 par face sur A4 paysage, dans l'ordre d'un livret plié-agrafé.

Mise en forme reprise du livret paysage : couverture (logo, intitulé, groupes, « Apprendre, grandir, réussir »),
en-tête « YEBA FORMATIONS | Livret d'accueil – MARILYN INSTITUT », titres soulignés d'or, tableaux bleus,
encadrés, « Mon plan d'action » en fin de livret, dos avec les mentions légales.
Contenu : celui du livret complet (programme M.A.R.I.L.Y.N., règlement intérieur intégral, notice RGPD),
qui corrige les écarts de la version du 23/09 (pauses 15 min, contact, délais de réclamation, IA, OPCO).

Logo : celui du livret paysage, œil rogné (choix d'A. LUMEKA du 27/09/2026). Texte courant en 12 pt
(charte YEBA-IDENT-2026 : support imprimé stagiaire) ; règlement intérieur en 11 pt (≥ 10 pt, document contractuel).
"""
import base64
import html
import subprocess
from pathlib import Path

import pymupdf as fitz

import donnees as D

ICI = Path(__file__).resolve().parent
RES = ICI / "livret_a5"
OUT = D.SORTIE / "02_LIVRET_ACCUEIL"
A5 = (148, 210)  # mm


def typo(t):
    return t.replace(" :", "&nbsp;:").replace("« ", "«&nbsp;").replace(" »", "&nbsp;»").replace(" ?", "&nbsp;?")


def e(t):
    if "<" in t:
        return typo(t)
    return html.escape(t, quote=False).replace(" :", "&nbsp;:").replace("« ", "«&nbsp;").replace(" »", "&nbsp;»").replace(" ?", "&nbsp;?")


def tableau(lignes, largeurs=None, classe=""):
    h = f'<table class="{classe}">'
    if largeurs:
        h += "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in largeurs) + "</colgroup>"
    h += "<tr>" + "".join(f"<th>{e(c)}</th>" for c in lignes[0]) + "</tr>"
    for l in lignes[1:]:
        h += "<tr>" + "".join(f"<td>{e(str(c))}</td>" for c in l) + "</tr>"
    return h + "</table>"


def puces(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def encadre(titre, corps, ton="bleu"):
    return f'<div class="encadre {ton}"><div class="et">{e(titre)}</div>{corps}</div>'


# ------------------------------------------------------------------ pages
def pages():
    P = []
    S1, S2 = D.SESSIONS[1], D.SESSIONS[2]

    # 1. Couverture
    P.append(("couverture", f"""
      <div class="cv-logo"><img src="LOGO" alt="YEBA FORMATIONS"></div>
      <div class="cv-sur">Livret d'accueil de la stagiaire</div>
      <h1 class="cv-titre">{e(D.ACTION['intitule'])}</h1>
      <div class="cv-filet"></div>
      <div class="cv-bloc">Action de formation intra-entreprise<br><b>MARILYN INSTITUT · L'OR DES ÎLES</b></div>
      <div class="cv-dates"><b>Groupe 1 : lundi 28 septembre 2026</b><br><b>Groupe 2 : mardi 29 septembre 2026</b><br>
        8h00 – 17h00 · 7 heures de formation<br>C.R.E.P.S de Saint-Denis · salle «&nbsp;SEYCHELLES&nbsp;»</div>
      <div class="cv-stag">Stagiaire : ......................................................</div>
      <div class="cv-devise">Apprendre, grandir, réussir</div>"""))

    # 2. Sommaire (numéros remplis après coup)
    P.append(("sommaire", "SOMMAIRE"))

    P.append(("Bienvenue", f"""
      <p>Vous accueillez chaque jour les clientes de MARILYN INSTITUT et de L'OR DES ÎLES : vous êtes la première personne qu'elles
      voient, et souvent la raison pour laquelle elles reviennent.</p>
      <p>Cette journée a été construite <b>pour votre métier</b>, à partir de <b>vos réponses</b> au questionnaire de positionnement :
      l'accueil, le conseil en soins et en produits, les objections du quotidien (« c'est cher », « je vais réfléchir »),
      la reprise de rendez-vous et le travail en équipe.</p>
      <p>Ici, pas de cours magistral : <b>70 % de pratique</b>, des jeux, des mises en situation en petit groupe, et des outils
      que vous utiliserez dès le lendemain, en cabine comme à l'accueil.</p>
      <p>Lisez ce livret avant la session et gardez-le : il vous accompagnera aussi après la formation.</p>
      <p class="signature">Je me réjouis de vous accueillir.<br><b>Aurélien LUMEKA</b><br>Directeur de YEBA FORMATIONS, formateur</p>"""))

    P.append(("Vos interlocuteurs", f"""
      <p><b>YEBA FORMATIONS</b> est un organisme de formation réunionnais, créé en 2021, spécialisé en vente, management,
      relation client et intelligence artificielle. Il est <b>certifié Qualiopi</b> (n° 25FOR02027.1) au titre de la catégorie
      <b>actions de formation</b>.</p>
      {tableau([["Rôle", "Interlocuteur"],
                ["Formateur", "Aurélien LUMEKA"], ["Référent pédagogique", "Aurélien LUMEKA"], ["Référent handicap", "Aurélien LUMEKA"],
                ["Suivi administratif", "Aurélien LUMEKA"],
                ["Si un fait concerne le formateur", "Mme Sarah MACHON, gérante de MARILYN INSTITUT"]], [45, 55])}
      {encadre("Contact", f"<p>Tél. : <b>{D.ORG['tel']}</b><br>E-mail : <b>{D.ORG['email']}</b><br>Site : <b>{D.ORG['site']}</b></p>")}"""))

    P.append(("La formation en bref", f"""
      {tableau([["Élément", "Détail"],
                ["Intitulé", D.ACTION['intitule']],
                ["Public", "Esthéticiennes, prothésistes ongulaires, praticiennes et personnel d'accueil de MARILYN INSTITUT et de L'OR DES ÎLES"],
                ["Prérequis", "Aucun prérequis de niveau. Exercer une activité au contact de la clientèle."],
                ["Modalité", "Présentiel, intra-entreprise, groupe de 4 personnes"],
                ["Durée", "1 journée, <b>7 heures de formation</b>"],
                ["Dates", "Groupe 1 : <b>lundi 28 septembre 2026</b><br>Groupe 2 : <b>mardi 29 septembre 2026</b><br>Programme identique"]], [28, 72])}"""))

    P.append(("__La journée en pratique", f"""
      {tableau([["Élément", "Détail"],
                ["Horaires", "<b>8h00 – 17h00</b><br>Pause : 10h00 – 10h15<br>Déjeuner : 12h00 – 13h00<br>Pause : 15h00 – 15h15"],
                ["Lieu", "C.R.E.P.S de Saint-Denis, salle « SEYCHELLES »<br>24 route Philibert Tsiranana<br>CS 61115 — 97495 La Réunion"],
                ["Repas", "<b>À prévoir</b> par chaque participante, pris hors de la salle"],
                ["Formateur", "Aurélien LUMEKA — vente, management, relation client"],
                ["Financement", "Plan de développement des compétences de MARILYN INSTITUT"],
                ["Rémunération", "Vous restez salariée : votre rémunération est maintenue par votre employeur"]], [30, 70])}"""))

    P.append(("Objectifs", f"""
      <p class="chapeau">À la fin de la journée, vous serez capable de :</p>
      <ol class="obj">{''.join(f'<li>{e(o)}</li>' for o in D.OBJECTIFS)}</ol>"""))

    lettres = [("M", "Miroir", "mon image professionnelle"), ("A", "Accueil", "le parcours cliente"), ("R", "Ressenti", "découvrir le besoin"),
               ("I", "Initiative", "les temps creux"), ("L", "Lien", "conseiller sans forcer"), ("Y", "Y revenir", "fidéliser"), ("N", "Nous", "l'équipe")]
    P.append(("Le protocole M.A.R.I.L.Y.N.", f"""
      <p class="chapeau">Le fil rouge de la journée : 7 lettres, 7 réflexes… et le nom de votre institut.</p>
      <div class="marilyn">{''.join(f'<div class="ml"><span class="lt">{l}</span><span class="mt"><b>{m}</b><br>{e(d)}</span></div>' for l, m, d in lettres)}</div>"""))

    def prog(sel):
        lignes = [["Horaire", "Séquence"]]
        for d, f, l, t, c, _ in D.PROGRAMME:
            if sel(d):
                tt = (f"{l} — " if l else "") + t
                lignes.append([f"{d.replace('h', 'h')} – {f}", f"<b>{e(tt)}</b>" + (f"<br>{e(c)}" if c else "")])
        return tableau(lignes, [26, 74], "prog")
    P.append(("Programme de la journée", f"<h3 class='sous'>Le matin</h3>{prog(lambda d: D.minutes(d) < 12 * 60)}"))
    P.append(("__Programme — l'après-midi", f"{prog(lambda d: D.minutes(d) >= 12 * 60)}"))

    P.append(("Méthodes pédagogiques", f"""
      {puces(["<b>30 % d'apports, 70 % de pratique</b> : jeux de cartes, jeux de rôle en binôme, ateliers, retours personnalisés.",
              "<b>Cas pratiques tirés du quotidien d'un institut</b>, avec des clientes fictives : aucune cliente réelle n'est citée.",
              "<b>Diaporama accessible</b> : mots-clés, très grands caractères, fort contraste.",
              "<b>Phrases d'appui</b> : des formulations prêtes à l'emploi, que l'on a le droit de lire pendant les jeux de rôle.",
              "<b>D'abord en binôme, puis en groupe</b> : personne ne joue devant le groupe sans s'être entraînée. Droit au joker.",
              "<b>Ressource PDF complète</b> remise après la session."])}"""))

    P.append(("Évaluation et suivi", f"""
      {tableau([["Quand ?", "Comment et pourquoi ?"],
                ["Avant", "<b>Questionnaire de positionnement</b> : connaître votre point de départ et adapter la journée"],
                ["8h30 et 16h40", "<b>Positionnement express</b> (2 minutes) : mesurer votre progression"],
                ["Toute la journée", "<b>Observation</b> pendant les jeux de rôle, avec une grille critériée"],
                ["16h20", "<b>Quiz de 10 questions</b>, joué en équipes sur l'écran"],
                ["17h00", "<b>Questionnaire de satisfaction</b> « à chaud »"],
                ["À 3 mois", "<b>Questionnaire « à froid »</b> : ce qui a changé au quotidien"]], [30, 70])}"""))

    P.append(("Documents remis", f"""
      <h3>Avant la session</h3>{puces(["La convocation", "Ce livret d'accueil, avec le programme, le règlement intérieur et la notice sur vos données", "La fiche de droit à l'image (facultative)"])}
      <h3>Après la session</h3>{puces(["<b>L'attestation de fin de formation</b> : objectifs, nature, durée et résultats de l'évaluation (art. L.6353-1 du code du travail)", "La ressource PDF de la formation"])}
      <h3>À votre employeur</h3>{puces(["Les feuilles d'émargement, signées par demi-journée", "Le certificat de réalisation"])}"""))

    P.append(("Règles de vie", f"""
      <p class="chapeau">Le règlement intérieur complet figure en fin de livret. En résumé :</p>
      {tableau([["Règle", "Ce qui est attendu"],
                ["Ponctualité", "Arriver à l'heure ; signer soi-même la feuille de présence, matin et après-midi"],
                ["Absence, retard", "Prévenir le formateur et votre responsable au plus tôt"],
                ["Téléphone", "En mode silencieux ; utilisé seulement pour une activité demandée"],
                ["Respect", "Bienveillance, écoute, aucune moquerie ni propos discriminant"],
                ["Confidentialité", "Ce qui est dit en formation reste en formation"],
                ["Photos, vidéos", "Interdites sans l'accord écrit des personnes concernées"],
                ["Sécurité", "Suivre les consignes du C.R.E.P.S ; signaler tout accident ou danger"],
                ["Tabac, alcool", "Tabac, vapotage et alcool interdits dans les locaux"]], [30, 70])}"""))

    P.append(("Tolérance zéro", f"""
      <p>YEBA FORMATIONS applique une <b>tolérance zéro</b> face aux violences sexistes et sexuelles, au harcèlement et aux discriminations.</p>
      {encadre("Vous êtes victime ou témoin ?", puces([
          "Parlez-en <b>au formateur</b>, Aurélien LUMEKA, pendant ou après la session.",
          "<b>Si les faits concernent le formateur</b> : adressez-vous à <b>Mme Sarah MACHON</b>, gérante de MARILYN INSTITUT.",
          "<b>Si les faits concernent Mme MACHON</b> : adressez-vous au formateur.",
          "Écoute : <b>3919</b> (gratuit, anonyme) ou le <b>Défenseur des droits</b>.",
          "<b>Danger immédiat</b> : 17 ou 112 ; par SMS : 114."]), "or")}
      <p>Chaque signalement est <b>traité sous 48 heures</b>, en toute <b>confidentialité</b>. Aucune personne qui signale des faits de bonne foi,
      ou qui en témoigne, ne peut subir de représailles.</p>"""))

    P.append(("Infos pratiques", f"""
      {tableau([["Sujet", "Information"],
                ["Adresse", "C.R.E.P.S de Saint-Denis, salle « SEYCHELLES »<br>24 route Philibert Tsiranana<br>CS 61115 — 97495 La Réunion"],
                ["Arrivée", "Présentez-vous à <b>7h50</b> : la formation commence à <b>8h00 précises</b>"],
                ["Transport", "Par vos propres moyens. Le trajet relève de la législation sur les accidents de trajet."],
                ["Déjeuner", "De 12h00 à 13h00 : repas <b>à prévoir</b>, pris hors de la salle"],
                ["Hébergement", "Aucun hébergement n'est prévu"],
                ["À apporter", "De quoi écrire. Tout le reste est fourni."],
                ["Tenue", "Professionnelle ou confortable. Toutes les activités se font assises ou debout, au choix."]], [28, 72])}"""))

    P.append(("Handicap et accessibilité", f"""
      <p>Vous avez un besoin particulier, lié ou non à un handicap : vue, audition, mobilité, concentration, santé ?
      Contactez le <b>référent handicap</b>, avant la session si possible.</p>
      {encadre("Référent handicap", f"<p><b>Aurélien LUMEKA</b><br>9 rue Françoise Châtelain, 97490 Sainte-Clotilde<br>{D.ORG['tel']} · {D.ORG['email']}</p>")}
      {puces(["Vous n'avez <b>pas à indiquer de raison</b> ni de diagnostic : seul le besoin d'aménagement est utile.",
              "<b>Déjà prévu pour tout le groupe</b> : chaises à dossier, activités assises ou debout au choix, pauses à tout moment, eau à disposition.",
              "Sur demande : supports en 16 points, place près de l'écran, évaluation orale, rythme adapté.",
              "Votre information reste <b>confidentielle</b> : elle n'est pas transmise à votre employeur sans votre accord."])}"""))

    P.append(("Vos données (RGPD)", f"""
      <p><b>Responsable du traitement</b> : YEBA FORMATIONS, représentée par son directeur, Aurélien LUMEKA ({D.ORG['email']}).</p>
      {tableau([["Données", "Pourquoi ? Base légale", "Durée"],
                ["Identité, fonction, émargements, attestation", "Organiser la formation et justifier sa réalisation. Contrat et obligation légale.", "3 ans (plus si la loi l'impose)"],
                ["Positionnement, grille, quiz, plan d'action", "Adapter la formation, mesurer les acquis. Obligation légale (L.6353-1).", "3 ans"],
                ["Questionnaires de satisfaction", "Améliorer les formations. Intérêt légitime.", "3 ans"],
                ["Besoin d'aménagement", "Adapter la formation. Seul l'aménagement est noté, jamais la raison.", "Fin de la session"],
                ["Photo, vidéo", "Uniquement les usages que vous cochez. Votre consentement.", "Durée choisie"]], [30, 46, 24], "petit")}"""))

    P.append(("__Vos données (suite)", f"""
      {puces(["<b>Votre employeur</b>, MARILYN INSTITUT, reçoit votre présence, votre attestation et le certificat. Vos réponses individuelles au positionnement ne lui sont <b>pas</b> transmises : il ne reçoit qu'une synthèse anonyme du groupe.",
              "<b>L'organisme certificateur Qualiopi</b> et les services de contrôle de l'État, uniquement en cas d'audit ou de contrôle.",
              "<b>Les prestataires techniques</b> de YEBA FORMATIONS, liés par contrat. YEBA FORMATIONS privilégie des outils hébergés dans l'Union européenne ; tout transfert hors UE est encadré (RGPD, art. 44 et suivants) et vous en êtes informée.",
              "<b>Aucune donnée n'est vendue</b> ni utilisée à des fins publicitaires.",
              f"<b>Vos droits</b> : accès, rectification, effacement, limitation, opposition, retrait du consentement. Écrivez à {D.ORG['email']} : réponse sous un mois. Vous pouvez aussi saisir la <b>CNIL</b> (www.cnil.fr)."])}"""))

    P.append(("IA et évaluation", f"""
      {encadre("Transparence sur l'usage de l'IA", puces([
          "Certains supports de cette formation ont été conçus avec l'aide d'une <b>intelligence artificielle générative</b>, puis vérifiés et validés par le formateur (règlement européen sur l'IA, art. 50).",
          "<b>Aucune IA ne note, ne classe ni n'évalue</b> les stagiaires : la correction est faite par le formateur.",
          "<b>Aucune décision</b> vous concernant n'est prise de façon automatisée (RGPD, art. 22).",
          "Vous pouvez demander l'<b>explication</b> de votre résultat et le <b>contester</b> auprès du formateur."]))}"""))

    P.append(("Avis et réclamations", f"""
      {puces(["<b>Votre avis compte</b> : questionnaire de satisfaction en fin de journée, puis questionnaire « à froid » <b>3 mois</b> plus tard.",
              f"<b>Réclamation</b> : oralement au formateur, ou par e-mail à <b>{D.ORG['email']}</b>.",
              "<b>Accusé de réception sous 5 jours ouvrés</b>, <b>réponse motivée sous 15 jours ouvrés</b> (convention de formation, art. 12).",
              "Chaque avis et chaque réclamation sont analysés pour <b>améliorer</b> nos formations."])}"""))

    P.append(("Numéros utiles", f"""
      {tableau([["Service", "Numéro"], ["Votre formateur", D.ORG['tel']], ["SAMU — urgence médicale", "15"], ["Pompiers", "18"],
                ["Police — gendarmerie", "17"], ["Numéro d'urgence européen", "112"], ["Urgence par SMS (surdité)", "114"],
                ["Violences Femmes Info", "3919"], ["Défenseur des droits", "09 69 39 00 00"]], [65, 35])}"""))

    P.append(("Mémo des méthodes", f"""
      {tableau([["Méthode", "Les étapes"],
                ["S.O.I.N. — découvrir", "<b>S</b>ituer · <b>O</b>bserver · <b>I</b>nterroger (3 questions ouvertes) · <b>N</b>ommer le besoin avec SES mots"],
                ["P.E.R.L.E. — conseiller", "<b>P</b>artir de son besoin · <b>E</b>xpliquer le bénéfice · <b>R</b>ecommander UNE chose · <b>L</b>aisser choisir · <b>E</b>ncaisser sans se justifier"],
                ["Objections — 4 temps", "Accueillir · Questionner (« par rapport à quoi ? ») · Répondre par le bénéfice · Vérifier"],
                ["A.R.P. — remarque reçue", "<b>A</b>ccuser réception · <b>R</b>eformuler · <b>P</b>roposer"],
                ["7 premières secondes", "Je m'arrête · je regarde · je souris · « Bonjour » · son prénom"],
                ["Entre deux clientes", "Cabine prête · fiche à jour · prochain RDV vérifié · produit conseillé noté · je respire"]], [34, 66])}"""))
    import build_pedago
    P.append(("Mes phrases d'appui", tableau([["Moment", "Ma phrase"]] + [[t.capitalize().replace(' rdv', ' RDV'), x] for t, x in build_pedago.APPUI], [32, 68])))

    # Règlement intérieur intégral
    R = [
        ("Article 1 — Champ d'application", "Le présent règlement (code du travail, art. L.6352-3, L.6352-4, R.6352-1 à R.6352-15) s'applique à chaque stagiaire, pendant toute la formation, dans tous les lieux où elle se déroule, y compris pendant les pauses. Il fixe les règles de santé, d'hygiène et de sécurité, de discipline, les sanctions et les garanties de procédure."),
        ("Article 2 — Lieu de formation", "YEBA FORMATIONS ne dispose pas de locaux propres. La formation se déroule au C.R.E.P.S de Saint-Denis : les consignes de santé et de sécurité applicables sont celles de cet établissement (art. R.6352-1). Le formateur les présente à l'ouverture de chaque session."),
        ("Article 3 — Santé et sécurité", "Chacune veille à sa sécurité et à celle des autres et signale toute situation dangereuse. En cas d'alarme : quitter la salle sans reprendre ses affaires et rejoindre le point de rassemblement, où le formateur fait l'appel. Tout accident ou malaise est déclaré immédiatement au formateur, qui alerte les secours si besoin et prévient MARILYN INSTITUT le jour même ; l'employeur déclare l'accident du travail ou de trajet. Alcool, stupéfiants, tabac et vapotage sont interdits (code de la santé publique, art. L.3512-8 et L.3513-6). Les repas se prennent hors de la salle."),
        ("Article 4 — Horaires, présence, émargement", "Horaires : 8h00 – 17h00 ; pauses 10h00-10h15 et 15h00-15h15 ; déjeuner 12h00-13h00. Chaque stagiaire signe elle-même la feuille d'émargement, matin et après-midi. Signer pour une autre, ou pour une demi-journée non suivie, est une faute grave et peut constituer un faux (code pénal, art. 441-1). Retard ou absence : prévenir le formateur et l'employeur au plus tôt. Départ anticipé : avec l'accord du formateur, heure notée sur la feuille."),
        ("Article 5 — Comportement", "Attitude respectueuse et bienveillante envers chacune. Sont interdits : propos injurieux, discriminatoires ou humiliants, violence, harcèlement, dégradation du matériel, introduction de personnes extérieures."),
        ("Article 6 — Téléphone", "En mode silencieux pendant les séquences ; utilisé seulement pour une activité demandée. Une stagiaire qui doit rester joignable le signale en début de journée."),
        ("Article 7 — Images et propriété intellectuelle", "Interdiction de photographier, filmer ou enregistrer sans l'accord écrit des personnes concernées. YEBA FORMATIONS ne photographie aucune stagiaire sans son autorisation écrite, libre et révocable. Les supports sont protégés et réservés à un usage professionnel au sein de MARILYN INSTITUT."),
        ("Article 8 — Confidentialité", "Ce qui est dit en formation reste en formation. On ne cite jamais une cliente réelle et on ne montre aucune fiche cliente ni information de santé. Les cas pratiques utilisent des profils fictifs."),
        ("Article 9 — Violences, harcèlement, discriminations", "Tolérance zéro (rubrique 11). Sont notamment interdits et pénalement sanctionnés : harcèlement sexuel (code pénal, art. 222-33), harcèlement moral (art. 222-33-2), outrage sexiste, discriminations (art. 225-1)."),
        ("Article 10 — Données personnelles et IA", "Les données des stagiaires sont traitées conformément au RGPD (rubrique 14). Aucun système d'IA n'évalue, ne note ni ne classe les stagiaires ; certains supports ont été conçus avec l'aide d'une IA générative puis validés par le formateur (règlement (UE) 2024/1689, art. 50)."),
        ("Article 11 — Sanctions", "Toute mesure autre qu'une observation verbale, prise à la suite d'un agissement fautif (art. R.6352-3). Par ordre croissant : avertissement écrit, blâme, exclusion temporaire, exclusion définitive. Les amendes sont interdites. En cas d'urgence (violence, mise en danger, ivresse, harcèlement), exclusion temporaire immédiate à titre conservatoire (art. R.6352-7)."),
        ("Article 12 — Garanties de procédure", "Aucune sanction sans information préalable des griefs (R.6352-4) ; convocation écrite à un entretien, avec possibilité d'être assistée (R.6352-5) ; sanction écrite et motivée, notifiée entre un jour franc et 15 jours après l'entretien (R.6352-6). L'employeur et le financeur sont informés (R.6352-8). Pour une session d'une journée, la procédure se déroule après la session."),
        ("Article 13 — Représentation des stagiaires", "L'élection de délégués n'est obligatoire que pour les actions de plus de 500 heures (R.6352-9) : elle ne s'applique pas ici."),
        ("Article 14 — Réclamations", f"Par oral au formateur ou par écrit à {D.ORG['email']}. Accusé de réception sous 5 jours ouvrés, réponse motivée sous 15 jours ouvrés."),
        ("Article 15 — Accessibilité", "Toute personne ayant un besoin particulier peut contacter le référent handicap, sans avoir à indiquer de diagnostic."),
        ("Article 16 — Entrée en vigueur", "Le règlement est remis avant l'entrée en formation (art. L.6353-8) et rappelé à l'ouverture de la session. Il s'applique aux sessions des 28 et 29 septembre 2026. Fait à Sainte-Clotilde, le 27 septembre 2026 — Aurélien LUMEKA, directeur de YEBA FORMATIONS."),
    ]
    paquets, cour, taille = [], [], 0
    for t, x in R:  # ~1 400 caractères par page A5 en 11 pt
        if cour and taille + len(x) > 1350:
            paquets.append(cour); cour, taille = [], 0
        cour.append((t, x)); taille += len(x) + 60
    paquets.append(cour)
    for i, pq in enumerate(paquets):
        titre = "Règlement intérieur" if i == 0 else "Règlement intérieur (suite)"
        corps = ("<p class='mini'>Annexe 2 de la convention C-MAR-2026-01 — applicable aux stagiaires</p>" if i == 0 else "")
        corps += "".join(f"<h4>{e(t)}</h4><p class='regl'>{e(x)}</p>" for t, x in pq)
        P.append((titre if i == 0 else f"__{titre}", corps))

    P.append(("Attestation de remise", f"""
      <p>Je soussignée, stagiaire de l'action « {e(D.ACTION['intitule'])} » organisée par YEBA FORMATIONS pour MARILYN INSTITUT,
      atteste avoir reçu, lu et compris ce livret d'accueil, le <b>règlement intérieur</b> et la <b>notice d'information sur mes données</b>,
      et m'engage à respecter le règlement intérieur.</p>
      <p>☐ Session du lundi 28 septembre 2026 &nbsp;&nbsp; ☐ Session du mardi 29 septembre 2026</p>
      <div class="sign"><div><b>La stagiaire</b><br>Nom et prénom :<br><br>Date :<br>Signature :</div>
      <div><b>Pour YEBA FORMATIONS</b><br>Aurélien LUMEKA, directeur<br><br>Date :<br>Signature :</div></div>
      <p class="mini">Un exemplaire séparé de cette attestation est signé le jour J et conservé au dossier de la session (Qualiopi, indicateur 9).</p>"""))

    P.append(("Mon plan d'action", f"""
      <p class="chapeau"><i>« Ma Promesse Marilyn » — à compléter en fin de journée, puis à relire avec votre responsable.</i></p>
      <div class="case"><b>Ce que je retiens de la journée</b></div>
      <div class="case"><b>Ce que j'applique dès demain en institut</b></div>
      <div class="case"><b>Quand, avec qui, et comment je mesure mon progrès</b></div>
      <div class="case petite"><b>Ma phrase qui rebooke</b></div>"""))
    return P


def dos():
    return f"""
      <div class="ds-logo"><img src="LOGO" alt="YEBA FORMATIONS"></div>
      <div class="ds-nom">YEBA FORMATIONS</div>
      <div class="ds-adr">9 rue Françoise Châtelain<br>97490 Sainte-Clotilde — La Réunion<br><br>{D.ORG['tel']} · {D.ORG['email']}<br>{D.ORG['site']}</div>
      <div class="ds-leg">SIRET {D.ORG['siret']}<br>{e(D.ORG['nda_mention'])}<br>{e(D.ORG['qualiopi'])}.<br>
      Référent handicap : Aurélien LUMEKA.<br><br>Livret remis avant l'entrée en formation (code du travail, art. L.6353-8). Version du 27 septembre 2026.
      Version en 16 points sur simple demande.<br><br><i>Document conçu par le formateur avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689,
      art. 50), vérifié et validé par un humain.</i></div>"""


CSS = """
@page { size: 148mm 210mm; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Inter', Arial, sans-serif; color: #121212; font-size: 12pt; line-height: 1.35; }
.page { width: 148mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; padding: 17mm 11mm 13mm 11mm; background: #fff; }
.entete { position: absolute; top: 7mm; left: 11mm; right: 11mm; display: flex; justify-content: space-between; align-items: baseline;
          border-bottom: 0.6pt solid #C9A84C; padding-bottom: 1.2mm; font-size: 7.5pt; }
.entete b { font-family: 'Montserrat'; color: #1B3A6B; font-weight: 800; letter-spacing: .02em; }
.entete span { color: #5A5F6A; }
.num { position: absolute; bottom: 6mm; font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; font-size: 9pt; }
.num.g { left: 11mm; } .num.d { right: 11mm; }
h2 { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; font-size: 15.5pt; margin: 0 0 1.5mm; line-height: 1.2; }
h2::after { content: ""; display: block; width: 100%; height: 1.1pt; background: #C9A84C; margin-top: 1.6mm; }
h3.sous { margin-top: 0; }
h3 { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; font-size: 12.5pt; margin: 3mm 0 1mm; }
h4 { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; font-size: 10.5pt; margin: 2.2mm 0 .5mm; }
p { margin: 0 0 2.2mm; text-align: left; }
.chapeau { font-weight: 600; }
.mini { font-size: 8.5pt; color: #5A5F6A; }
.regl { font-size: 11pt; line-height: 1.3; margin-bottom: 1mm; }
table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 3mm; font-size: 11.5pt; }
table.petit { font-size: 10pt; }
table.prog { font-size: 11pt; }
th { background: #1B3A6B; color: #fff; text-align: left; font-family: 'Montserrat'; font-weight: 700; padding: 1.4mm 2mm; font-size: 10.5pt; }
td { padding: 1.3mm 2mm; border-bottom: 0.5pt solid #D5DAE2; vertical-align: top; }
tr:nth-child(odd) td { background: #F1F4F9; }
td:first-child { font-weight: 700; color: #1B3A6B; }
table.prog td:first-child { white-space: nowrap; }
ul { margin: 1mm 0 2.5mm; padding-left: 0; list-style: none; }
li { position: relative; padding-left: 4.5mm; margin-bottom: 1.6mm; }
ul li::before { content: ""; position: absolute; left: .4mm; top: 2.1mm; width: 1.8mm; height: 1.8mm; background: #C9A84C; }
ol.obj { margin: 1mm 0 0; padding-left: 0; list-style: none; counter-reset: o; font-size: 11pt; line-height: 1.3; }
ol.obj li { counter-increment: o; padding-left: 7mm; margin-bottom: 1.5mm; }
ol.obj li::before { content: counter(o); position: absolute; left: 0; top: 0; width: 5mm; height: 5mm; border-radius: 50%;
   background: #1B3A6B; color: #fff; font-family: 'Montserrat'; font-weight: 700; font-size: 8.5pt; text-align: center; line-height: 5mm; }
.encadre { border-left: 1.4mm solid #1B3A6B; background: #EEF2F8; padding: 2.2mm 3mm; margin: 2mm 0 3mm; }
.encadre.or { border-left-color: #C9A84C; background: #FAF5E8; }
.encadre .et { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; font-size: 11pt; margin-bottom: 1mm; }
.encadre p:last-child, .encadre ul:last-child { margin-bottom: 0; }
.signature { margin-top: 5mm; }
.marilyn { display: grid; grid-template-columns: 1fr; gap: 2mm; margin-top: 3mm; }
.ml { display: flex; align-items: center; gap: 3mm; }
.ml .lt { flex: 0 0 13mm; height: 13mm; background: #1B3A6B; color: #C9A84C; font-family: 'Montserrat'; font-weight: 800; font-size: 22pt;
          display: flex; align-items: center; justify-content: center; border-radius: 2mm; }
.ml .mt { font-size: 12pt; line-height: 1.25; }
.ml .mt b { font-family: 'Montserrat'; color: #1B3A6B; }
.sign { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin: 4mm 0; }
.sign div { border: 0.8pt solid #BFC5CF; padding: 3mm; min-height: 42mm; font-size: 11pt; }
.case { border: 0.8pt solid #BFC5CF; border-top: 1.4mm solid #1B3A6B; padding: 2mm 3mm; height: 36mm; margin-bottom: 3mm; color: #1B3A6B; font-size: 11pt; }
.case.petite { height: 22mm; }
.sommaire { list-style: none; padding: 0; margin: 2mm 0; font-size: 12pt; }
.sommaire li { display: flex; padding: 0 0 0 0; margin-bottom: 1.35mm; }
.sommaire li::before { display: none; }
.sommaire .n { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; width: 7mm; }
.sommaire .t { flex: 1; border-bottom: 0.8pt dotted #9AA3B2; margin-right: 2mm; }
.sommaire .p { font-family: 'Montserrat'; font-weight: 700; color: #1B3A6B; }
/* couverture */
.couverture { padding: 16mm 12mm 12mm; text-align: center; }
.cv-logo img { width: 44mm; }
.cv-sur { font-family: 'Montserrat'; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 8.5pt; color: #5A5F6A; margin-top: 7mm; }
.cv-titre { font-family: 'Montserrat'; font-weight: 800; color: #1B3A6B; font-size: 19pt; line-height: 1.2; margin: 3mm 0 0; }
.cv-filet { width: 40mm; height: 1.4pt; background: #C9A84C; margin: 5mm auto; }
.cv-bloc { font-size: 11.5pt; line-height: 1.45; }
.cv-bloc b { color: #1B3A6B; }
.cv-dates { font-size: 11.5pt; line-height: 1.5; margin-top: 5mm; }
.cv-stag { margin-top: 9mm; font-size: 11.5pt; }
.cv-devise { font-family: 'Poiret One'; font-size: 17pt; color: #1B3A6B; margin-top: 9mm; }
/* dos */
.dos { text-align: center; padding: 24mm 14mm 12mm; }
.ds-logo img { width: 30mm; }
.ds-nom { font-family: 'Montserrat'; font-weight: 800; color: #1B3A6B; font-size: 12pt; margin-top: 3mm; }
.ds-adr { font-size: 11pt; margin-top: 4mm; line-height: 1.45; }
.ds-leg { font-size: 8.5pt; color: #5A5F6A; margin-top: 10mm; line-height: 1.45; }
.notes { background: repeating-linear-gradient(#fff 0 8.5mm, #D5DAE2 8.5mm 8.8mm); height: 160mm; margin-top: 4mm; }
"""


def construire():
    OUT.mkdir(parents=True, exist_ok=True)
    logo = "data:image/png;base64," + base64.b64encode((RES / "logo_livret_sans_oeil.png").read_bytes()).decode()
    fonts = (RES / "fonts" / "fonts.css").read_text().replace("url(fonts/", f"url({(RES / 'fonts').as_uri()}/")
    P = pages()
    total_contenu = len(P) + 1  # + dos
    nb = -(-total_contenu // 4) * 4
    while len(P) + 1 < nb:
        P.append(("__Mes notes", "<div class='notes'></div>"))
    # numéros de page (page 1 = couverture)
    somm = [(t, i + 1) for i, (t, _) in enumerate(P) if i >= 2 and not t.startswith("__")]
    numero = {t: k + 1 for k, (t, _) in enumerate(somm)}
    corps = []
    for i, (titre, contenu) in enumerate(P):
        n = i + 1
        if titre == "couverture":
            corps.append(f'<section class="page couverture">{contenu}</section>')
            continue
        if titre == "sommaire":
            items = "".join(f'<li><span class="n">{numero[t]}.</span><span class="t">{e(t)}</span><span class="p">{p}</span></li>' for t, p in somm)
            contenu = f"<h2>Sommaire</h2><ul class='sommaire'>{items}</ul>"
        elif titre.startswith("__"):
            contenu = f"<h2>{e(titre[2:])}</h2>{contenu}"
        else:
            contenu = f"<h2>{numero[titre]}. {e(titre)}</h2>{contenu}"
        cote = "d" if n % 2 else "g"
        corps.append(f'<section class="page"><div class="entete"><b>YEBA FORMATIONS</b><span>Livret d\'accueil – MARILYN INSTITUT</span></div>'
                     f'{contenu}<div class="num {cote}">{n}</div></section>')
    corps.append(f'<section class="page dos">{dos()}</section>')
    html_doc = f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>Livret d'accueil</title><style>{fonts}{CSS}</style></head><body>{''.join(corps)}</body></html>".replace("LOGO", logo)
    src = RES / "livret.html"
    src.write_text(html_doc, encoding="utf-8")
    a5 = OUT / "Livret_accueil_A5_lecture_ecran.pdf"
    subprocess.run(["node", str(RES / "imprimer.js"), str(src), str(a5)], check=True)
    impose(a5, OUT / "Livret_accueil_A4_paysage_IMPRESSION_livret_plie.pdf")
    return [a5, OUT / "Livret_accueil_A4_paysage_IMPRESSION_livret_plie.pdf"]


def impose(src, dst):
    """Imposition livret (pli + agrafes) : face n = [dernière, première], [2, avant-dernière]…"""
    s = fitz.open(str(src))
    n = s.page_count
    assert n % 4 == 0, n
    out = fitz.open()
    W, H = 841.89, 595.28
    for k in range(n // 2):
        if k % 2 == 0:
            g, d = n - 1 - k, k
        else:
            g, d = k, n - 1 - k
        p = out.new_page(width=W, height=H)
        p.show_pdf_page(fitz.Rect(0, 0, W / 2, H), s, g)
        p.show_pdf_page(fitz.Rect(W / 2, 0, W, H), s, d)
    out.save(str(dst))


if __name__ == "__main__":
    print(construire())

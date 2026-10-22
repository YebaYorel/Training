"""Note de synthèse : décisions, constats, autocritique, questions."""
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
    d = Doc("Note de synthèse", "Votre année de formation continue avec les titres MEM et RPMS — version 3", code="NOTE-00", couverture=True)
    d.h1("1. Les décisions à retenir")
    d.numeros([
        "**DEETS** : envoyer la version A **au plus tard le vendredi 30 octobre 2026** (courriel du 20 octobre ; le 12e jour tombe le dimanche 1er novembre).",
        f"**MEM — promotion 1** : du {fmt(m_j[0][0])} au {fmt(m_j[-1][0])} ; examen la semaine du {fmt_court(m_s)}.",
        f"**RPMS — promotion 1** : du {fmt(r_j[0][0])} au {fmt(r_j[-1][0])} ; examen la semaine du {fmt_court(r_s)}.",
        "**Examen** : centre agréé partenaire pour la 1re session MEM, puis agrément propre.",
        "**Trois urgences avant d'encaisser** : désigner un médiateur de la consommation ; régler la question de la TVA avec l'expert-comptable ; "
        "faire confirmer par le courtier la couverture des activités liées à l'IA.",
    ])
    d.h1("2. Ce que révèlent le certificat Qualiopi et votre base Airtable")
    d.tableau(["Constat", "Conséquence"], [
        ["Le certificat 25FOR02027.1 couvre les 4 catégories, dont l'apprentissage", "L'extension Qualiopi n'est pas nécessaire si vous ouvrez un jour l'apprentissage ; les courriels à la DEETS sont mis à jour"],
        ["Validité du 17/02/2026 au 16/02/2029 (Airtable indique 2027)", "Audit de surveillance entre le 17/04/2027 et le 17/12/2027 : il tombera pendant la promotion MEM, préparez les preuves dès mars 2027"],
        ["Site certifié : le siège, 9 rue Françoise Châtelain", "Le Secrétariat Center est une salle louée : fiche site tiers YEBA-DOC-15 à remplir"],
        ["Charte graphique YEBA-IDENT-2026", "Appliquée : texte bleu ou noir, or réservé aux filets, interligne 1,3, bloc-marque et mention de transparence IA sur chaque document"],
        ["Documents officiels déjà en vigueur (règlement intérieur, CGV, politiques)", "Les documents du dossier les complètent sans les dupliquer (avenant RI-06, conditions particulières CP-05…)"],
        ["Plusieurs incohérences dans les documents officiels", "Liste et corrections proposées dans SOC-04"],
    ], [7, 10])
    d.h1("3. Le point fiscal à ne pas manquer")
    d.p("YEBA FORMATIONS est en franchise en base de TVA (article 293 B du CGI). Une seule promotion de titre professionnel peut faire dépasser "
        "le seuil de franchise sur l'année. En cas de dépassement, la formation ne reste sans TVA qu'avec l'attestation 3511-SD "
        "(exonération de la formation professionnelle continue) ; le conseil serait soumis à la TVA à 8,5 %. "
        "Votre base Airtable recommande déjà de demander cette attestation : faites-le avant les premières recettes des parcours. "
        "[À VÉRIFIER avec l'expert-comptable : seuil applicable à La Réunion.]")
    d.h1("4. Ce qui a changé dans cette version")
    d.tableau(["Sujet", "Changement"], [
        ["Coordonnées", f"{O['siege_court']} — {O['tel']} — {O['mail']} — mention entrepreneur individuel (EI)"],
        ["Locaux", f"Secrétariat Center : {O['lieu_equipement']}"],
        ["Qualiopi", "4 catégories, validité 2029, audit de surveillance planifié"],
        ["Assurance et TVA", "Données Hiscox et mention « TVA non applicable — article 293 B du CGI » reportées partout"],
        ["Alerte cyclonique", "Règle alignée sur le règlement intérieur YEBA-DOC-04 : alerte orange = suspension immédiate et report sans frais"],
        ["Documents stagiaires", "Convention et contrat propres aux parcours, conditions particulières CP-05, avenant au règlement intérieur, aménagements d'examen ; les doublons des documents officiels sont retirés"],
        ["Nouveau", "SOC-04 : articulation avec le socle officiel et écarts à corriger"],
    ], [4, 13])
    d.h1("5. Budget de salle")
    d.p(f"Secrétariat Center : MEM {loc_m:,} € ; RPMS {loc_r:,} € (hors informations collectives, jury blanc et examen). ".replace(",", " ")
        + f"Durées : MEM {jours_centre(MEM)} jours ({heures_centre(MEM)} h), RPMS {jours_centre(RPMS)} jours ({heures_centre(RPMS)} h). "
        "Le classeur PIL-03 calcule le seuil de rentabilité et la trésorerie dès que vous saisissez votre prix et vos effectifs.")
    d.h1("6. Autocritique")
    d.tableau(["Angle", "Faille", "Correction"], [
        ["Juridique", "RPMS bâti sans le REAC et le référentiel d'évaluation v08", "Signalé dans chaque document RPMS ; à confronter dès réception"],
        ["Juridique", "Documents officiels encore incomplets (CGV, convention, réclamations)", "Écarts listés dans SOC-04 ; aucun contrat particulier sans médiateur"],
        ["Économique", "Risque de sortie de franchise de TVA", "Action datée dans le plan PIL-01 ; avertissement dans le budget"],
        ["Faisabilité", "Audit Qualiopi pendant la 1re promotion", "Préparation dès mars 2027 avec la matrice QUA-02"],
        ["Souveraineté", "Airtable et Gmail hébergés hors UE", "Migration déjà décidée (Baserow chez OVHcloud, Brevo) ; numéro de sécurité sociale et RIB hors Airtable"],
        ["Identité", "Deux logos coexistaient (PNG transmis, SVG de la charte)", "PNG retenu et décliné : fond clair (FORMATIONS en bleu), fond bleu, carré réseaux sociaux, icône"],
        ["Sécurité", "Dossiers remplis contenant des données personnelles", "Jamais dans Git ; espace chiffré hébergé dans l'UE"],
    ], [3, 6.5, 7.5])
    d.h1("7. Ce qu'il me manque encore")
    d.numeros([
        "Le REAC et le référentiel d'évaluation RPMS millésime 08 (2023).",
        "Votre décision sur les prix : trois scénarios dans l'étude TAR-01 (recommandation : 4 900 € MEM, 4 950 € RPMS).",
        "Le seuil de maintien d'une session (nombre minimal de stagiaires) une fois le prix choisi.",
        "Votre vérification sur place des lignes de bus, des temps de marche et des prix des restaurants (fiche LIEU-01).",
        "Les livrets réalisés pour un autre organisme, quand vous voudrez (sans mêler les deux marques).",
    ])
    d.h1("8. Sources")
    d.puces([
        "Certificat Qualiopi n° 25FOR02027.1, Qualitia, émis le 17/02/2026 (document transmis).",
        "Base Airtable « YEBA FORMATIONS — Centre de formation (Adaptable) » : tables CONFIG SYSTÈME, DOCUMENTS OFFICIELS YEBA, FORMATEURS & PRESTATAIRES, consultées le 22/10/2026.",
        "REAC et référentiel d'évaluation Manager d'établissement marchand, millésime 09 du 10/12/2025 (documents transmis).",
        "Fiches France Compétences RNCP41853 et RNCP38575 (documents transmis).",
        "REAC et RC RPMS RNCP35646, millésime 07 de 2016 (documents transmis, version remplacée).",
        "Code du travail ; code général des impôts, art. 293 B et 261-4-4° a ; RGPD ; règlement (UE) 2024/1689.",
    ])
    d.rgpd(["RGPD : chaque modèle informe les personnes et limite les données ; le complément RGPD-01 est à reporter dans le registre YEBA-DOC-16.",
            "IA Act : aucun système d'IA n'évalue, ne note, ne classe ni ne sélectionne les stagiaires ; maîtrise de l'IA assurée par la charte YEBA-DOC-11."])
    return d.save("00_NOTE_DE_SYNTHESE.docx")


if __name__ == "__main__":
    print(note())

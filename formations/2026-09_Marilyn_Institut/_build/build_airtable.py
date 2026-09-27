"""Dossier « à déposer dans Airtable » : chaque fichier est copié et renommé avec sa destination exacte.

Pourquoi un dépôt manuel ? L'API Airtable n'accepte une pièce jointe que par URL publique, qu'Airtable
télécharge lui-même. Le seul hébergement disponible ici serait le dépôt GitHub, qui est PUBLIC : y placer
les documents, même quelques minutes, publierait des supports protégés (convention, art. 11) et, pour les
documents nominatifs, des données personnelles (RGPD). Le glisser-déposer dans Airtable reste donc la voie sûre.
"""
import csv
import shutil

import donnees as D
from docx_lib import Doc

BASE = "appQ2zqc80kkc6MR1"
S = D.SORTIE
OUT = S / "07_A_DEPOSER_DANS_AIRTABLE"

# (table, enregistrement, champ, fichier source relatif à livrables/, quand)
PLAN = [
    ("CATALOGUE FORMATIONS", "FOR-0007", "Programme PDF", "02_LIVRET_ACCUEIL/Livret_accueil_A5_lecture_ecran.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Support de formation", "04_PEDAGOGIE/Diaporama_Marilyn_Institut_relation_cliente_vente_conseil.pptx", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Support de formation", "04_PEDAGOGIE/Diaporama_Marilyn_Institut_relation_cliente_vente_conseil.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Support de formation", "04_PEDAGOGIE/Ressource_stagiaire_complete.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Support de formation", "04_PEDAGOGIE/Quiz_interactif_Marilyn.html", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Evaluation de positionnement", "05_EVALUATIONS/Positionnement_express_matin_soir.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Evaluation de positionnement", "01_POSITIONNEMENT_ET_INDICATEUR_8/03_Fiche_Qualiopi_Indicateur_8_positionnement_et_adaptation.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Grille d'évaluation", "04_PEDAGOGIE/Grille_criteriee_VIERGE.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Grille d'évaluation", "04_PEDAGOGIE/Quiz_papier_feuille_reponse_individuelle.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Doc - Règlement intérieur (version en vigueur)", "02_LIVRET_ACCUEIL/Livret_accueil_A5_lecture_ecran.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Doc - Procédure réclamations", "06_QUALIOPI_ET_OPCO/04_Fiche_et_registre_reclamations_Indicateur_31.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Mallette formateur (documents)", "04_PEDAGOGIE/Conducteur_de_seance_FORMATEUR.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Mallette formateur (documents)", "04_PEDAGOGIE/Kit_exercices_a_decouper_VENTE.pdf", "Maintenant"),
    ("CATALOGUE FORMATIONS", "FOR-0007", "Mallette formateur (documents)", "04_PEDAGOGIE/Quiz_corrige_commente_FORMATEUR.pdf", "Maintenant"),
    ("EVALUATIONS", "Positionnement initial — session 28/09", "Document d'évaluation (PDF)", "01_POSITIONNEMENT_ET_INDICATEUR_8/01_Rapport_positionnement_INTERNE_nominatif.pdf", "Maintenant"),
    ("EVALUATIONS", "Positionnement initial — session 29/09", "Document d'évaluation (PDF)", "01_POSITIONNEMENT_ET_INDICATEUR_8/01_Rapport_positionnement_INTERNE_nominatif.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateur 4", "Documents de preuve", "06_QUALIOPI_ET_OPCO/02_Fiche_analyse_du_besoin_Indicateur_4.pdf", "Après signature de Sarah MACHON"),
    ("INDICATEURS QUALIOPI", "Indicateur 8", "Documents de preuve", "01_POSITIONNEMENT_ET_INDICATEUR_8/03_Fiche_Qualiopi_Indicateur_8_positionnement_et_adaptation.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateur 10", "Documents de preuve", "01_POSITIONNEMENT_ET_INDICATEUR_8/03_Fiche_Qualiopi_Indicateur_8_positionnement_et_adaptation.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateur 26", "Documents de preuve", "06_QUALIOPI_ET_OPCO/03_Registre_des_amenagements_Indicateur_26.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateur 31", "Documents de preuve", "06_QUALIOPI_ET_OPCO/04_Fiche_et_registre_reclamations_Indicateur_31.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateur 32", "Documents de preuve", "06_QUALIOPI_ET_OPCO/01_Audit_indicateurs_Qualiopi_RNQ_V10_et_controles_OPCO.pdf", "Maintenant"),
    ("INDICATEURS QUALIOPI", "Indicateurs 2, 30 et 32", "Documents de preuve", "06_QUALIOPI_ET_OPCO/05_Bilan_session_et_amelioration_Indicateurs_2_30_32.pdf", "Après les sessions, une fois rempli"),
]


def apres_session():
    """Documents nominatifs : à déposer SIGNÉS, après la session (un fichier par stagiaire)."""
    lignes = []
    for s in D.stagiaires():
        nom = D.nom_complet(s)
        lignes += [
            ("INSCRIPTIONS", f"Session du {D.SESSIONS[s['session']]['date_courte']}", "Attestation PDF", f"Attestation de {nom} — version remplie et signée", "Après la session"),
            ("INSCRIPTIONS", f"Session du {D.SESSIONS[s['session']]['date_courte']}", "Règlement intérieur PDF signé", f"Attestation de remise signée par {nom} (dernière page du livret)", "Après signature"),
            ("APPRENANTS", nom, "Document droit à l'image (PDF)", f"Autorisation signée par {nom} (accord ou refus)", "Après signature"),
            ("EVALUATIONS", nom, "Document d'évaluation (PDF)", f"Grille critériée et quiz remplis de {nom}", "Après la session"),
        ]
    for n in (1, 2):
        lignes.append(("PRESENCES & EMARGEMENTS", f"Session du {D.SESSIONS[n]['date_courte']}", "Emargement apprenant (signature)",
                       f"Scan de la feuille d'émargement signée — session {n}", "Après la session"))
    return lignes


def construire():
    OUT.mkdir(parents=True, exist_ok=True)
    produits = []
    for i, (table, rec, champ, src, quand) in enumerate(PLAN, 1):
        f = S / src
        cible = OUT / f"{i:02d}__{table}__{rec}__{champ}__{f.name}".replace("/", "-").replace(" ", "_")
        shutil.copy(f, cible)
        produits.append(cible)
    with open(OUT / "Plan_de_classement_Airtable.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["N°", "Table", "Enregistrement", "Champ", "Fichier", "Quand"])
        for i, (t, r, c, src, q) in enumerate(PLAN, 1):
            w.writerow([i, t, r, c, src.split("/")[-1], q])
        for t, r, c, x, q in apres_session():
            w.writerow(["—", t, r, c, x, q])

    doc = Doc("Plan de classement Airtable", "Quel fichier dans quel champ — base YEBA FORMATIONS", "Action Marilyn Institut — 27/09/2026", corps=10,
              paysage=True, compact=True)
    doc.encadre("Mode d'emploi — 10 minutes", [
        "Les fichiers de ce dossier sont numérotés et nommés selon leur destination : N°__TABLE__ENREGISTREMENT__CHAMP__fichier.",
        "Dans Airtable, ouvrir l'enregistrement, cliquer sur le champ pièce jointe, puis glisser le fichier. Un champ peut recevoir plusieurs fichiers.",
        "Les documents nominatifs sont à déposer seulement une fois SIGNÉS (après la session) : un document vierge dans un champ « signé » serait une fausse preuve.",
        "Pourquoi pas automatiquement ? Airtable ne reçoit un fichier que par une URL publique. Le seul hébergement disponible ici est ton dépôt GitHub, qui est public : "
        "y mettre les documents, même quelques minutes, les publierait (propriété intellectuelle, convention art. 11 ; données personnelles, RGPD).",
    ], taille=10)
    doc.h2("À déposer maintenant")
    doc.table([["N°", "Table", "Enregistrement", "Champ", "Fichier"]] +
              [[str(i), t, r, c, src.split("/")[-1]] for i, (t, r, c, src, q) in enumerate(PLAN, 1) if q == "Maintenant"],
              [1, 4.2, 4.6, 5.4, 10.8], taille=8.5)
    doc.h2("À déposer plus tard")
    doc.table([["Quand", "Table", "Enregistrement", "Champ", "Document"]] +
              [[q, t, r, c, src.split("/")[-1]] for i, (t, r, c, src, q) in enumerate(PLAN, 1) if q != "Maintenant"] +
              [[q, t, r, c, x] for t, r, c, x, q in apres_session()],
              [3.6, 4.2, 4.6, 5.2, 8.4], taille=8.5)
    produits.append(doc.enregistrer(OUT / "00_Plan_de_classement_Airtable.docx"))
    return produits


if __name__ == "__main__":
    print(len(construire()))

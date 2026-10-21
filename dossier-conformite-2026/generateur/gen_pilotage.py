"""Pilotage annuel : pièces par financeur, calendrier des obligations, tableau de bord Excel."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from lib import Doc, ORGANISME, SORTIE
from titres import MEM, RPMS, heures_centre, planning

O = ORGANISME
DOSSIER = "05_Pilotage_annuel"

SOCLE = [
    "Extrait Kbis ou avis de situation INSEE / extrait RNE de moins de 3 mois",
    f"Récépissé de déclaration d'activité (NDA {O['nda']})",
    f"Certificat Qualiopi en cours de validité ({O['qualiopi']}) et périmètre (catégories)",
    "Attestation de vigilance URSSAF (à renouveler tous les 6 mois — obligatoire pour tout contrat ≥ 5 000 € HT, art. L.8222-1 et D.8222-5 du code du travail)",
    "Attestation de régularité fiscale (marchés publics)",
    "Attestation d'assurance responsabilité civile professionnelle et assurance des locaux",
    "RIB au nom de l'organisme",
    "Bilan pédagogique et financier (BPF) de l'année précédente déposé",
    "Attestation d'exonération de TVA [À VÉRIFIER]",
    "CV et justificatifs des formateurs ; contrats de sous-traitance",
    "Programme, règlement intérieur, livret d'accueil, CGV, procédures (handicap, réclamations)",
]

FINANCEURS = [
    ("Caisse des Dépôts — CPF (EDOF)", [
        "Compte organisme sur EDOF ; habilitation à proposer la certification [À VÉRIFIER : pour un titre professionnel, preuve d'agrément DEETS ou de partenariat avec un centre agréé]",
        "Fiche action complète (programme, prix, prérequis, modalités, accessibilité)",
        "Déclaration d'entrée, de sortie et du service fait dans les délais des conditions générales d'utilisation",
        "Preuves d'assiduité (émargements) et de passage de la certification",
        "Facturation : [À VÉRIFIER : possibilités d'acompte / facturation intermédiaire prévues par les CGU EDOF en vigueur]"]),
    ("France Travail (AIF, AFC, POEI / POEC)", [
        "Offre référencée dans la base du Carif-Oref Réunion (visibilité pour les conseillers)",
        "Devis sur KAIROS (AIF) ; attestation d'entrée et de présence mensuelle sur KAIROS",
        "Programme, calendrier, conventions de période en entreprise",
        "Attestation de fin de formation, résultats de certification"]),
    ("Missions Locales", [
        "Prescripteurs (pas financeurs directs en général) : fiche de présentation, calendrier des informations collectives, critères d'admission",
        "Retour d'information sur l'entrée, l'assiduité et la sortie (avec l'accord du jeune)",
        "Articulation avec le contrat d'engagement jeune (CEJ) [À VÉRIFIER : modalités locales]"]),
    ("Région Réunion", [
        "Achat de formation par marché public (programme régional de formation) : réponse aux appels d'offres (profil acheteur / BOAMP)",
        "Pièces de candidature : DC1, DC2 ou DUME, attestations fiscales et sociales, références, mémoire technique",
        "Exécution : bilans pédagogiques, émargements, suivi de la rémunération des stagiaires (ASP le cas échéant), indicateurs d'insertion",
        "Si cofinancement FSE+ : publicité européenne (logos), conservation renforcée des pièces [À VÉRIFIER : durée dans le marché]"]),
    ("OPCO (entreprises)", [
        "Convention de formation, programme, devis",
        "Demande de prise en charge déposée par l'entreprise avant le démarrage",
        "Émargements, certificat de réalisation, facture (subrogation possible)",
        "Contrat de professionnalisation : CERFA EJ20 [À VÉRIFIER : numéro en vigueur], forfait horaire de la branche"]),
    ("DEETS de La Réunion (contrôle)", [
        "Déclaration d'activité à jour (modification de toute information sous 30 jours)",
        "BPF annuel ; réponses aux contrôles administratifs et financiers (pièces justificatives de la réalité des actions)",
        "Agrément des sessions de titres professionnels (si centre d'examen) — démarche en ligne DEETS 974",
        "Règlement intérieur, élection des délégués (actions > 500 h)"]),
    ("URSSAF", [
        "Déclarations sociales (DSN mensuelle si salariés), contribution à la formation professionnelle",
        "Attestation de vigilance tous les 6 mois (demandée par vos clients et financeurs)",
        "Formateurs indépendants : vérifier leur attestation de vigilance (obligation de vigilance du donneur d'ordre)"]),
    ("Auditeur Qualiopi", [
        "Preuves des 32 indicateurs (dont 2 : résultats publiés ; 26 : handicap ; 30-32 : évaluations et réclamations)",
        "Audit de surveillance entre le 14e et le 22e mois suivant la certification initiale ; renouvellement à 3 ans"]),
]

CALENDRIER = [
    ("Janvier", "Mettre à jour les indicateurs de résultats publiés (année N-1) ; programme annuel des sessions ; veille appels d'offres Région"),
    ("Février", "Préparer le BPF (données N-1 : heures-stagiaires, produits par financeur) ; revue annuelle des réclamations"),
    ("Mars", "Renouveler l'attestation de vigilance URSSAF (semestrielle) ; plan de formation interne (maîtrise de l'IA, art. 4 IA Act)"),
    ("Avril", "Revue annuelle du registre RGPD et des sous-traitants ; purge des données dont la durée de conservation est échue"),
    ("Mai", "Déposer le BPF avant le 31 mai sur Mon Activité Formation"),
    ("Juin", "Bilan qualité de mi-année ; mise à jour des programmes (veille RNCP : versions des titres, dates d'échéance)"),
    ("Juillet", "Préparer les sessions de la rentrée : demandes d'agrément (≥ 7 mois avant l'examen), offre au Carif-Oref, EDOF"),
    ("Août", "Revue des contrats formateurs, CV et justificatifs ; vérification des assurances"),
    ("Septembre", "Renouveler l'attestation de vigilance URSSAF ; informations collectives avec Missions Locales et France Travail"),
    ("Octobre", "Préparer l'audit de surveillance / renouvellement Qualiopi selon votre date de certification [À COMPLÉTER]"),
    ("Novembre", "Exercice de crise cyclonique (plan de continuité, formation à distance) avant la saison cyclonique"),
    ("Décembre", "Clôture : facturation des heures réalisées, archivage des dossiers, enquêtes d'insertion à 6 mois de l'année"),
    ("Chaque mois", "Émargements et attestations de présence (KAIROS, financeurs) ; suivi des absences ; DSN ; indicateur d'abandon"),
    ("Chaque session", "Avant / pendant / après : voir le rétroplanning des documents PLN-MEM et PLN-RPMS"),
]


def doc_pilotage():
    d = Doc("Pièces exigées par financeur et contrôleur, et calendrier annuel", "OPCO • DEETS • France Travail • Missions Locales • URSSAF • Région Réunion • Caisse des Dépôts", code="PIL-01")
    d.h1("1. Socle commun à tenir toujours à jour")
    d.cases(SOCLE)
    d.h1("2. Pièces spécifiques par financeur ou contrôleur")
    for nom, items in FINANCEURS:
        d.h2(nom)
        d.cases(items)
    d.h1("3. Calendrier annuel des obligations")
    d.tableau(["Période", "Actions"], [list(c) for c in CALENDRIER], [3, 14])
    d.h1("4. Documents remis au stagiaire, étape par étape")
    d.tableau(["Moment", "Documents"], [
        ["Avant (information / inscription)", "Programme PRG, CGV, fiche d'inscription FI-01, mention RGPD, positionnement POS-02, convention CONV-03 ou contrat CTR-04, convocation"],
        ["Entrée", "Livret d'accueil LA-07, règlement intérieur RI-06, charte IA IA-03, contrat d'engagement ABS-13, autorisation d'image IMG-15 (facultative), attestation d'entrée ATT-09"],
        ["Pendant", "Émargements EMG-08, grilles critériées DP, conventions de période en entreprise PAE-14, attestations d'assiduité, PV d'élection des délégués"],
        ["Fin", "Évaluation à chaud EVAL-10, attestation de fin de formation et certificat de réalisation ATT-09, convocation à la session de validation"],
        ["Après", "Évaluation à froid, enquête d'insertion à 6 mois, questionnaire entreprise / financeur, traitement des réclamations REC-11"],
    ], [4.5, 12.5])
    return d.save(f"{DOSSIER}/PIL-01_Pieces_financeurs_et_calendrier.docx")


ENTETE = PatternFill("solid", fgColor="1B3A6B")
BLANC = Font(color="FFFFFF", bold=True, size=12, name="Arial")
NORMAL = Font(size=12, name="Arial")


def _feuille(ws, entetes, lignes, largeurs):
    ws.append(entetes)
    for c in ws[1]:
        c.fill, c.font = ENTETE, BLANC
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for l in lignes:
        ws.append(l)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = NORMAL
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(largeurs, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def classeur():
    wb = Workbook()
    ws = wb.active
    ws.title = "Calendrier annuel"
    _feuille(ws, ["Période", "Action", "Responsable", "Fait le", "Preuve (lien)"],
             [[p, a, O["dirigeant"], "", ""] for p, a in CALENDRIER], [16, 80, 20, 12, 30])
    for t in (MEM, RPMS):
        lib = {m[0]: m[1] for m in t["modules"]} | {"PAE": "Période en entreprise"}
        ws = wb.create_sheet(f"Heures {t['code']}")
        lignes = []
        for n, ty, contenu in planning(t):
            for code, h in contenu:
                lignes.append([f"S{n}", ty, code, lib[code], h, "", "", ""])
        _feuille(ws, ["Semaine", "Lieu", "Code", "Module", "Heures prévues", "Heures réalisées", "Écart", "Commentaire"],
                 lignes, [10, 12, 8, 55, 14, 14, 10, 30])
        last = len(lignes) + 1
        for r in range(2, last + 1):
            ws[f"G{r}"] = f'=IF(F{r}="","",F{r}-E{r})'
        ws[f"D{last + 1}"] = "TOTAL"
        ws[f"E{last + 1}"] = f"=SUM(E2:E{last})"
        ws[f"F{last + 1}"] = f"=SUM(F2:F{last})"
        ws[f"D{last + 1}"].font = ws[f"E{last + 1}"].font = Font(bold=True, size=12, name="Arial")
    ws = wb.create_sheet("Indicateurs session")
    _feuille(ws, ["Indicateur", "MEM", "RPMS", "Formule / source"], [
        ["Inscrits", "", "", "Saisie"], ["Entrés en formation", "", "", "Saisie"], ["Abandons", "", "", "Saisie"],
        ["Taux d'abandon", '=IF(B3="","",B4/B3)', '=IF(C3="","",C4/C3)', "Abandons / entrés"],
        ["Présentés à l'examen", "", "", "Saisie"], ["Titres complets obtenus", "", "", "Saisie"],
        ["Taux de réussite", '=IF(B6="","",B7/B6)', '=IF(C6="","",C7/C6)', "Titres / présentés"],
        ["Satisfaction moyenne (sur 4)", "", "", "EVAL-10"], ["En emploi à 6 mois", "", "", "Enquête"],
        ["Taux d'insertion à 6 mois", '=IF(B3="","",B10/(B3-B4))', '=IF(C3="","",C10/(C3-C4))', "En emploi / sortants"],
    ], [34, 14, 14, 30])
    for r in (5, 8, 11):
        for col in "BC":
            ws[f"{col}{r}"].number_format = "0%"
    ws = wb.create_sheet("Suivi absences")
    _feuille(ws, ["Date", "Stagiaire (initiales)", "Session", "Type", "Justifiée ?", "Contact le", "Action", "Partenaire mobilisé"],
             [], [12, 18, 12, 14, 12, 12, 40, 20])
    out = SORTIE / DOSSIER / "PIL-02_Tableau_de_bord_pilotage.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


def tout():
    return [doc_pilotage(), classeur()]


if __name__ == "__main__":
    for f in tout():
        print(f)

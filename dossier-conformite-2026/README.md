# Dossier de l'année 2026-2028 — YEBA FORMATIONS

Formation continue certifiante de niveau 5 : **TP Manager d'établissement marchand (RNCP41853)** et
**TP Responsable de petite ou moyenne structure (RNCP38575)**, plus la réponse au courriel de la DEETS.
Tout « l'à-côté » de la formation (hors supports de cours, ressources et grilles d'évaluation).

## Par où commencer

1. Lire `livrables/00_NOTE_DE_SYNTHESE.pdf`.
2. Envoyer à la DEETS la **version A** de `livrables/01_Reponse_DEETS/DEETS-00_Courriels_reponse.docx`
   **au plus tard le vendredi 30 octobre 2026**.
3. Suivre `livrables/05_Pilotage_annuel/PIL-01_Plan_actions_annee.pdf`, ligne par ligne.
4. Compléter les champs en **or foncé gras italique** `[À COMPLÉTER]` et vérifier les `[À VÉRIFIER]`.

## Contenu de `livrables/`

| Dossier | Contenu |
|---|---|
| `00_NOTE_DE_SYNTHESE` | Décisions, changements, autocritique, questions, sources |
| `01_Reponse_DEETS` | Courriels A/B, dossier des 18 pièces (entreprise individuelle) |
| `02_MEM`, `02_RPMS` | Programme, décorticage du référentiel, déroulé jour par jour, calendrier réel, livret d'accueil, guide de la période en entreprise |
| `03_Parcours_stagiaire` | 17 documents propres aux parcours certifiants, en complément des documents officiels YEBA |
| `04_RGPD_IA_Act` | Complément au registre YEBA-DOC-16 et règles IA Act des parcours |
| `05_Pilotage_annuel` | Plan d'actions daté, pièces par financeur, budget et trésorerie (Excel) |
| `06_Organisme` | Présentation du centre, matrice Qualiopi, organisation de l'examen, socle documentaire et écarts à corriger (SOC-04) |

Chaque document existe en `.docx` (modifiable) et en `.pdf`.

## Articulation avec Airtable

La table « DOCUMENTS OFFICIELS YEBA » de la base Airtable reste la source unique de vérité (règlement intérieur, CGV, politiques).
`sources/airtable_documents_officiels.json` en conserve un instantané du 22/10/2026. Le dossier applique la charte YEBA-IDENT-2026
(texte bleu ou noir, or réservé aux filets, bloc-marque et mention de transparence IA en fin de document).

## Régénérer

```bash
cd dossier-conformite-2026/generateur
python3 build.py   # python-docx, openpyxl, Pillow, python-dateutil et LibreOffice
```

- Modules, séquences et heures : `generateur/titres.py`.
- Dates de démarrage, jours fériés, fermetures : `generateur/calendrier.py`.
- Horaires, lieu, coordonnées : `generateur/lib.py` (`ORGANISME`, `HORAIRES`).

La génération s'arrête si un mot ne tient pas dans une colonne de tableau (aucun mot coupé).

## RGPD et IA Act

Les modèles ne contiennent aucune donnée de stagiaire. Une fois remplis, **ne les committez pas** :
rangez-les dans `dossier-conformite-2026/dossiers-remplis/` (exclu de Git) ou dans un espace chiffré hébergé dans l'UE.

# Dossier de conformité 2026 — YEBA FORMATIONS

Formation continue certifiante de niveau 5 : **TP Manager d'établissement marchand (RNCP41853)** et
**TP Responsable de petite ou moyenne structure (RNCP38575)**, plus la réponse au courriel de la DEETS.

## Par où commencer

1. Lire `livrables/00_NOTE_EXPERT_Choix_RNCP_et_strategie.pdf` (décisions, raisonnement, questions à trancher).
2. Envoyer à la DEETS la **version A** de `livrables/01_Reponse_DEETS/DEETS-00_Courriels_reponse.docx`, avant la fin du délai de 12 jours.
3. Compléter les champs **surlignés en jaune** `[À COMPLÉTER]` et vérifier les `[À VÉRIFIER]` dans les fichiers `.docx`.

## Contenu de `livrables/`

| Dossier | Contenu |
|---|---|
| `00_NOTE_EXPERT…` | Choix des RNCP, financement, trésorerie, stratégie DEETS, autocritique, sources |
| `01_Reponse_DEETS` | Courriels A/B, dossier des 18 pièces (apprentissage, si besoin un jour) |
| `02_MEM`, `02_RPMS` | Programme, déroulé pédagogique + grilles critériées, heures semaine par semaine + rétroplanning |
| `03_Parcours_stagiaire` | 15 documents, de l'inscription au suivi à 6 mois |
| `04_RGPD_IA_Act` | Registre art. 30, information, conservation, violations, charte IA et cartographie IA Act |
| `05_Pilotage_annuel` | Pièces par financeur et contrôleur, calendrier annuel, tableau de bord Excel |

Chaque document existe en `.docx` (modifiable) et en `.pdf`.

## Régénérer

```bash
cd dossier-conformite-2026/generateur
python3 build.py   # nécessite python-docx, openpyxl et LibreOffice
```

Pour modifier les modules ou les heures, éditez `generateur/titres.py`. Le planning et les tableaux sont recalculés automatiquement.

## RGPD et IA Act

Les modèles ne contiennent aucune donnée personnelle de stagiaire. Une fois remplis, **ne les committez pas** dans ce dépôt :
stockez-les dans un espace chiffré, hébergé dans l'UE, avec accès restreint (voir `RGPD-01`).

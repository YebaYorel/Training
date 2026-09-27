# Action MARILYN INSTITUT — « Excellence de la relation cliente et vente-conseil en institut »

Sessions : lundi 28 et mardi 29 septembre 2026 — C.R.E.P.S de Saint-Denis, salle « SEYCHELLES » — 8h00-17h00.
Convention C-MAR-2026-01 — devis D-MAR-2026-01 et -02 — financeur : OPCO EP.

## Régénérer tous les documents

```bash
pip install python-docx python-pptx matplotlib pymupdf cairosvg   # + LibreOffice (Writer, Impress) pour les PDF
cd _build && python build_all.py
```

Sortie : `livrables/` (Word + PDF + PPTX + quiz HTML) et une archive ZIP.

## Données personnelles — jamais sur GitHub

`_donnees_personnelles/` (stagiaires, réponses au positionnement, points de vigilance) et `livrables/`
sont exclus de Git (`.gitignore`). GitHub est hébergé hors UE : y déposer ces données contredirait
l'article 9 de la convention (« aucun transfert hors UE »). **[RGPD art. 5.1.f, 44]**

## Où est quoi

| Dossier de `livrables/` | Contenu |
|---|---|
| `01_POSITIONNEMENT_ET_INDICATEUR_8` | Rapport interne nominatif, synthèse anonymisée pour l'employeur, fiche Qualiopi Indicateur 8 |
| `02_LIVRET_ACCUEIL` | Livret complet : programme + règlement intérieur + notice RGPD + attestation de remise |
| `03_ADMINISTRATIF` | Convocations, droit à l'image (feuilles séparées), émargements, attestations, certificats de réalisation |
| `04_PEDAGOGIE` | Diaporama, quiz (HTML hors ligne, papier, corrigé), kit à découper, grilles, ressource, conducteur |
| `05_EVALUATIONS` | Positionnement express, évaluation à chaud, à froid, commanditaire |
| `06_QUALIOPI_ET_OPCO` | Audit des 32 indicateurs, analyse du besoin, registre des aménagements, réclamations, bilan |

## Règle de construction

`_build/donnees.py` est la source unique. Une information inconnue vaut `A_COMPLETER` et s'imprime
en rouge : rien n'est inventé. Le diaporama refuse de se générer si un texte ne tient pas dans sa
boîte à 24 pt minimum (aucun mot coupé, aucun débordement).

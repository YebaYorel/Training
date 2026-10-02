# Assistant IA perso : Piloter son activité en parlant à son téléphone

Formation YEBA FORMATIONS — 2 jours, 16 heures — présentiel, 4 à 8 stagiaires.
Fiche catalogue : base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) », table
CATALOGUE FORMATIONS (statut « En développement »).

## Contenu du dossier

| Fichier | Usage |
|---|---|
| `01_Programme_de_formation.pdf` | Programme public (objectifs SMART, contenu, évaluation, accessibilité) |
| `02_Deroule_pedagogique.pdf` | Déroulé séquence par séquence (horaires, méthodes, supports, évaluation) + matériel |
| `03_Support_projete.pptx` | Support projeté : 39 diapositives, mots-clés, corps ≥ 26 pt, notes formateur |
| `04_Ressource_stagiaire.pdf` | Livret ressource complet avec sources (20 pages) |
| `04_Ressource_stagiaire_GROS_CARACTERES.pdf` | Même livret en corps 16 (accessibilité) |
| `05_Grille_evaluation_criteriee.pdf` | Grille à 5 critères × 4 niveaux, C4 et C5 bloquants |
| `06_Quiz_evaluation_sommative.pdf` | Quiz stagiaire, 10 questions, seuil 7/10 |
| `07_Quiz_CORRIGE.pdf` | Corrigé commenté — réservé au formateur |
| `08_Jeux_pedagogiques.pdf` | 5 jeux : fiches formateur, cartes, variantes accessibles |

## Avant de diffuser

1. **Tarifs** : à fixer (le programme affiche « [À VALIDER PAR LE DIRIGEANT] »), puis à reporter
   dans la fiche Airtable.
2. **Liens des sources** : relevés le 02/10/2026, à revérifier avant chaque session.
3. **Environnement de démonstration KAZ'MARKET** (messagerie, agenda, base) : à créer et tester
   à J-3 ; aucune donnée réelle de client en séance.
4. Déposer les fichiers dans les champs pièces jointes de la fiche Airtable (Programme PDF,
   Support de formation, Grille d'évaluation, Mallette formateur).

## Régénérer les supports

```bash
pip install reportlab
python source/generer_pdf.py

npm install pptxgenjs react-icons react react-dom sharp
node source/generer_pptx.js
```

Le contenu est centralisé dans `source/contenu.py` (programme, objectifs, déroulé, grille, quiz,
jeux) et `source/ressource.py` (livret). La charte (bleu #1B3A6B, or #C9A84C, bloc-marque
normalisé) est dans `source/charte_yeba.py` : l'or n'est jamais utilisé en texte sur fond blanc.

# TP MEM : préparation aux activités-types (6 lundis, du 9/11 au 14/12/2026)

Ce dossier génère des supports de formation complets à partir des contenus `contenus/j1.py` à `j6.py`.
Le titre préparé est Manager d'établissement marchand, REAC TP-00136 v09.

| Lundi | Thème |
|---|---|
| 9/11 | Le métier de MEM : comprendre, se positionner, trouver sa place (avec l'IA) |
| 16/11 | Word, Excel, PowerPoint : les outils du manager et de l'examen |
| 23/11 | Les chiffres du commerce : prix, marges, indicateurs |
| 30/11 | Communiquer en manager : consignes, briefing, écoute, feedback |
| 7/12 | S'organiser et résoudre les problèmes, carnet de bord |
| 14/12 | Les règles du manager (travail, sécurité, RSE, RGPD, IA Act), bilan, cap sur l'AT1 |

Pour chaque lundi, le générateur produit :
- un PowerPoint formateur accessible, avec des notes détaillées ;
- une ressource apprenant ;
- une grille critériée sur 5 critères ;
- un quiz de 10 questions, en version apprenant et en corrigé ;
- un déroulé minute par minute.

Les journées J2 et J3 ont en plus leurs fichiers d'exercice Excel et Word.
Le journal pédagogique est fourni en `.docx` modifiable et en `.pdf`.

```bash
python3 generer.py          # les 6 lundis (ou : python3 generer.py 1 3)
python3 journal.py          # journal pédagogique
```

Les livrables vont dans `sortie/`. Ce dossier est ignoré par Git, car le dépôt est public.

La charte est neutre : la formation est animée pour un autre organisme, donc on n'y trouve ni nom, ni logo, ni couleur de YEBA FORMATIONS.
Si l'organisme fournit sa charte, on modifie `PALETTE` dans `moteur_pptx.py`.
Les entreprises citées dans les exercices sont fictives.

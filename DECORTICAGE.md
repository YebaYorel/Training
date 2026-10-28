# Logiciel de décorticage pédagogique — guide d'utilisation

Logiciel **personnel, local et hors ligne** : il lit les référentiels d'un titre
professionnel (REAC, RE/RC, fiche France Compétences RNCP ou RS) et produit
tout le déroulé de la formation, jour par jour et heure par heure.

## 1. Ce que le logiciel produit

| Fichier | Contenu |
|---|---|
| `Decorticage_<sigle>.xlsx` | Le classeur principal, en paysage, police 14 minimum (détail ci-dessous) |
| `Programme_<sigle>.docx` | Programme de formation modifiable, établi à partir de la fiche France Compétences |
| `Examen_simplifie_<sigle>.docx` | Partie 1 : tableau des épreuves. Partie 2 : ce que le jury attend, en clair |
| `Planning_<sigle>.ics` | Toutes les séances, à importer dans votre agenda (fuseau Indian/Reunion) |
| `Apercu_page_site_<sigle>.html` | Aperçu de la page web du programme |

Les feuilles du classeur :

1. **Accueil** : chiffres clés, sommaire cliquable, légende de Bloom, points à vérifier.
2. **Décorticage** : AT · CP (termes exacts du REAC), séance (étape du processus REAC),
   objectif (verbe d'action en COULEUR et MAJUSCULES), niveau de Bloom et mode de Bruner,
   contenus (savoirs REAC), durée.
3. **Planning détaillé** : chaque créneau réel (date, semaine, horaire, CP, séance, objectif,
   cumul, % avancé) avec une colonne « Réalisé ? » (liste déroulante) et des observations.
4. **Planning par jour** : les séances de chaque journée.
5. **Synthèses** : heures par AT, par CP, par mois et par semaine.
6. **Programme** : le programme de formation (feuille à part).
7. **Examen simplifié** : les épreuves et les attendus du jury.
8. **Couverture critères** : chaque critère d'évaluation est relié aux séances qui le
   travaillent. C'est une preuve directe pour **Qualiopi, indicateur 7** (adéquation du contenu aux
   exigences de la certification).
9. **Suivi journalier** : le texte « voilà ce que j'ai fait aujourd'hui », déjà rédigé pour
   chaque jour, à reprendre dans vos écrits.
10. **Préparation PowerPoint** : la trame de chaque séance (mots-clés des diapositives, déroulé
    selon les 6 fonctions d'étayage de Bruner, exercice, piste d'exemple réunionnais).
11. **Paramètres et sources** : hypothèses, jours exclus, sources.

Le logo est une image indépendante : cliquez dessus, puis « Suppr ». Aucune signature ni
mention d'outil n'apparaît dans les fichiers.

## 2. Installation (une seule fois) et déplacement

1. Installez Python 3.10 ou plus récent depuis python.org. Sous Windows, cochez
   « Add Python to PATH ».
2. Double-cliquez sur le lanceur :
   * Windows : `Lancer_Decorticage_Windows.bat`
   * Mac : `Lancer_Decorticage_Mac.command` (la première fois : clic droit → Ouvrir)
3. Le premier lancement installe les bibliothèques (connexion internet nécessaire, 2 à 3 minutes).
   Le navigateur s'ouvre ensuite. Créez votre mot de passe : 12 caractères minimum.

**Changer d'ordinateur** : copiez le dossier complet sur une clé USB, y compris
`donnees_yeba/` qui contient vos projets, votre charte et vos décisions. Sur le nouvel
ordinateur, double-cliquez sur le lanceur : l'environnement se réinstalle tout seul.

## 3. Utilisation

1. Menu **Charte** : saisissez vos codes couleur exacts et votre logo. Faites-le une seule fois.
2. Menu **Tarifs** (facultatif) : importez l'export CSV de votre base tarifs.
3. Menu **Nouveau titre** :
   * déposez le REAC (indispensable), le RE ou RC, et la fiche France Compétences ;
   * saisissez la **durée en centre**, que la fiche ne donne pas (elle vient de la convention) ;
   * indiquez la date de début, les jours de centre, les horaires, les pauses et le rythme
     d'alternance (`CCEE` = 2 semaines en centre, puis 2 semaines en entreprise) ;
   * si la formation est faite **pour un autre centre** (ICCI, TETRANERGY, PAM OI, GEM
     FORMATION…), saisissez son nom : **YEBA FORMATIONS et son logo disparaissent** de tous
     les documents.
4. Téléchargez les fichiers produits.
5. **Imprévu** (alerte cyclonique, formateur absent) : dans « Modifier et régénérer », ajoutez
   la date dans « Fermetures » (ex. `2027-02-08 Alerte rouge`). Tout le planning est recalculé.

Les jours fériés de La Réunion, dont le 20 décembre, sont exclus automatiquement.

Une utilisation sans interface est aussi possible :

```bash
python -m decorticage generer --reac REAC.pdf --re RE.pdf --fiche RNCP.pdf --heures 455 --debut 2027-01-04 --sortie ./sorties
```

## 4. Site internet : publication avec votre accord

Pour chaque programme, le logiciel vous pose la question, avec le prix suggéré, que vous
pouvez modifier :

* **Oui** : la page web (HTML + JSON) est générée dans `donnees_yeba/site_a_publier/` ;
* **Non (redemander)** : rien n'est publié, la question revient sur l'accueil ;
* **Non définitif** : jamais publié, plus jamais demandé, toute tentative est refusée.

Après un « Non », une page déjà générée est retirée. La **mise en ligne automatique**
n'est pas encore branchée : elle dépend de l'outil de votre site, qu'il reste à préciser.

## 5. Sécurité (menu « Sécurité » ou `python -m decorticage audit --corriger`)

* Visible **uniquement depuis votre ordinateur** (127.0.0.1), jamais depuis le réseau.
* Mot de passe haché (PBKDF2-SHA256, 600 000 itérations). Blocage progressif après 5 échecs.
* Session : cookie HttpOnly et SameSite=Strict, expiration après 30 min d'inactivité.
  Jeton anti-falsification (CSRF) sur chaque formulaire, contrôle des en-têtes Host et Origin.
* Pages sans aucun script, avec des en-têtes stricts (CSP, anti-iframe, nosniff).
* Fichiers reçus : vérification de la vraie signature (un .exe renommé en .pdf est refusé),
  refus des macros (.docm/.xlsm), protection contre les bombes ZIP et les chemins piégés,
  limite de taille. Le logo est ré-encodé, ce qui supprime tout contenu caché dans l'image.
* Excel : aucune formule ne peut être injectée par un document reçu.
* Fichiers privés (droits 600/700). Contrôle des versions des bibliothèques (failles CVE connues).
* À faire de votre côté : activer **BitLocker** (Windows) ou **FileVault** (Mac).

## 6. RGPD et IA Act

* **RGPD** : les référentiels sont des documents publics, sans donnée personnelle. Le
  logiciel ne collecte **aucune donnée de stagiaire**. N'écrivez pas de nom de stagiaire dans
  les colonnes « Observations » ou « Suivi journalier ». Sinon, ce classeur entre dans votre
  registre des traitements (finalité, durée de conservation, sécurité, art. 5, 30 et 32).
  Tout reste en local : il n'y a aucun transfert hors UE.
* **Airtable** (tarifs) : c'est un service américain, soumis au Cloud Act. Le logiciel ne s'y
  connecte pas : vous lui donnez seulement un export CSV de vos tarifs, sans donnée
  personnelle. Migrer cette base vers Baserow (UE), déjà relié à ce dépôt, est recommandé.
* **IA Act (règlement UE 2024/1689)** : le logiciel fonctionne par **règles fixes écrites à la
  main** (repérage des rubriques, dictionnaire des verbes de Bloom, calendrier). Il n'apprend
  rien des données et ne fait aucune inférence statistique. Selon les lignes directrices de la
  Commission sur la définition d'un système d'IA (février 2025), il ne relève donc pas de la
  définition de l'article 3(1). Il n'évalue pas non plus les apprenants, ce qui écarte l'annexe
  III, point 3. **À réévaluer** si un module d'IA générative est ajouté : obligations de
  transparence de l'article 50 et maîtrise de l'IA de l'article 4.

## 7. Limites connues (à vérifier par le formateur)

* Le rattachement de chaque savoir-faire à une étape du processus se fait par mots communs.
  Il est juste dans la grande majorité des cas, mais il faut le relire.
* Le passage des critères « en clair » garde la phrase d'origine dès qu'elle ne suit pas le
  modèle « X est/sont + participe ».
* Les pistes d'exemples locaux et les activités sont des **suggestions** à adapter.
* Un PDF scanné (une image, sans texte) est refusé : il faut la version numérique officielle.
* Les formats anciens `.doc` et `.xls` sont refusés : ouvrez-les puis enregistrez-les en
  `.docx` ou `.xlsx`.

## 8. Sources

* Taxonomie de Bloom révisée : Anderson L. W. & Krathwohl D. R. (2001), *A Taxonomy for
  Learning, Teaching, and Assessing*.
* Étayage : Wood D., Bruner J. S. & Ross G. (1976), « The role of tutoring in problem solving »,
  *Journal of Child Psychology and Psychiatry*, 17.
* Bruner J. S. (1966), *Toward a Theory of Instruction* : modes enactif, iconique et
  symbolique, curriculum en spirale.
* REAC et RE du titre MEM (TP-00136, millésime 09, 10/12/2025) : travail-emploi.gouv.fr.
  Fiche RNCP41853 : francecompetences.fr.
* Jours fériés : Code du travail, art. L3133-1. Le 20 décembre à La Réunion : décret
  n° 83-1003 du 23 novembre 1983.
* Qualiopi : Référentiel national qualité (décret n° 2019-564), indicateurs 1, 2, 5, 6 et 7.
* IA Act : règlement (UE) 2024/1689, eur-lex.europa.eu.
* Sécurité : recommandations de l'ANSSI (secnumacademie.gouv.fr) et OWASP (CSRF,
  injection de formules, téléversement de fichiers).

Tests automatiques : `python -m unittest discover -s tests -v`

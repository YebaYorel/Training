---
title: "Feuille 4 — Glossaire Make"
---

🔒 = point de cybersécurité.

| Terme | Définition technique | En simple |
|---|---|---|
| **Organisation** | Compte racine : abonnement, crédits, zone de données (EU1/EU2/US1/US2). | L'entreprise cliente chez Make. |
| **Équipe** (team) | Sous-espace avec ses scénarios, connexions et membres. 🔒 | Un service de l'entreprise. |
| **Zone de données** (data zone) | Région d'hébergement choisie à l'inscription ; EU1/EU2 pour l'Europe. 🔒 | Le pays où dort la donnée. |
| **Scénario** | Workflow automatisé : déclencheur + modules. | Une recette : « quand… alors… ». |
| **Module** | Une étape du scénario (action, recherche, déclencheur). | Une étape de la recette. |
| **Application** (app) | Ensemble de modules pour un service (Airtable, Mistral AI…). | La boîte à outils d'un logiciel. |
| **Connexion** | Authentification réutilisable vers un service (OAuth, clé API, jeton). 🔒 | Le badge que Make utilise pour entrer chez Airtable. |
| **Déclencheur** (trigger) | Premier module : **instantané** (webhook) ou **polling** (interrogation planifiée). | Ce qui lance la recette. |
| **Webhook** (Custom webhook) | URL unique qui reçoit une requête HTTP et lance le scénario immédiatement. 🔒 | Une sonnette. |
| **Polling** | Interrogation périodique d'une source (ex. « Watch Records » toutes les 15 min). | Aller voir la boîte aux lettres à heure fixe. |
| **Planification** (scheduling) | Fréquence d'exécution : intervalle, jours, heure. | L'horaire de tournée du facteur. |
| **Exécution** (run) | Un passage complet du scénario. | Une tournée. |
| **Bundle** (paquet) | Un lot de données qui traverse les modules ; un module s'exécute une fois par bundle. | Une lettre dans la sacoche. |
| **Opération / crédit** | Unité de facturation : 1 module exécuté ≈ 1 opération ; facturée en crédits (modules IA de Make : consommation variable). | Le ticket payé à chaque étape. |
| **Mapping** | Relier un champ de sortie d'un module à l'entrée d'un autre : `{{1.recordId}}`. | Brancher le bon fil sur la bonne prise. |
| **Fonctions** (IML) | Transformations dans le mapping : `formatDate`, `split`, `if`, `trim`… (0 opération). | Petits calculs faits au passage, gratuits. |
| **Filtre** | Condition entre deux modules ; arrête le bundle s'il ne correspond pas. | Un videur à la porte. |
| **Router** | Duplique le flux vers plusieurs routes (chacune avec son filtre). | Un aiguillage à plusieurs voies. |
| **If-else / Merge** | Choix exclusif (première condition vraie) puis regroupement des branches. | « Si… sinon… », puis on se retrouve. |
| **Iterator** | Découpe un tableau en bundles séparés. | Ouvrir un colis et traiter chaque objet. |
| **Aggregator** (texte, tableau, numérique) | Regroupe plusieurs bundles en un seul (texte, tableau, somme). | Remettre toutes les lettres dans une enveloppe. |
| **Data store** | Petite base interne à Make (mémoire entre exécutions). | Un carnet de notes de Make. |
| **Data structure** | Schéma JSON décrivant des données attendues. | Le plan d'un formulaire. |
| **Variables** | Valeurs stockées pendant l'exécution (`Set/Get variable`). | Un pense-bête. |
| **JSON** | Format texte des données échangées (`{"clé": "valeur"}`). | La langue des logiciels. |
| **Module HTTP** | Appel d'API libre (GET/POST) quand l'app n'existe pas. | Téléphoner directement au service. |
| **Clé API / jeton** | Secret d'authentification. 🔒 | Un mot de passe pour logiciel. |
| **Erreur 429 / quota** | Trop de requêtes en peu de temps ; il faut ralentir et réessayer. | « Ligne occupée, rappelez plus tard. » |
| **Gestionnaire d'erreurs** (error handler) | Route spéciale attachée à un module qui échoue. | Le plan B. |
| **Break** | Stocke l'exécution et **réessaie** automatiquement (nombre, intervalle). | Réessayer plus tard. |
| **Resume** | Continue avec une valeur de remplacement. | Utiliser la roue de secours. |
| **Ignore** | Abandonne ce bundle et continue les autres. | Mettre la lettre de côté. |
| **Commit / Rollback** | Arrête en validant / en annulant ce qui est annulable. | Tout garder / tout défaire. |
| **Exécutions incomplètes** | Exécutions en échec mises en attente de reprise. | Les lettres en souffrance. |
| **Historique / journaux** (history, logs) | Trace de chaque exécution, de ses bundles et de ses erreurs. 🔒 | La boîte noire. |
| **Paramètres du scénario** | Traitement séquentiel, nombre d'erreurs consécutives, stockage des incomplètes, **données confidentielles** (ne pas conserver le contenu dans les journaux). 🔒 | Les réglages de sécurité de la recette. |
| **Run once** | Exécution manuelle de test. | Faire un essai. |
| **Blueprint** | Export JSON d'un scénario, réimportable ; sert de sauvegarde versionnée. 🔒 | La photocopie de la recette. |
| **Sous-scénario** | Scénario appelé par un autre (modularité). | Une sous-recette réutilisable. |
| **Make AI Agents / AI Tools** | Fonctions IA natives de Make (crédits variables ; certains traitements hors UE). | L'IA maison de Make. |
| **MCP** (Model Context Protocol) | Protocole qui permet à un assistant IA de piloter Make (créer, lancer des scénarios). | Une télécommande pour l'IA. |

*Sources : help.make.com (AI providers and data zones) ; dépôt github.com/integromat/make-skills (références flow-control et error-handling) ; tarifs/limites d'après comparatifs 2026 (activepieces.com, eesel.ai) — à revérifier sur make.com/pricing.*

# Catalogue — les IA utilisées et les solutions à reproduire

> Ce catalogue sert de référence à tous les mémos par structure. Chaque solution (S1 à S11) est
> décrite comme une **recette** : ce que c'est, l'explication simple, les outils, les étapes pour la
> refaire chez n'importe quelle entreprise, la consigne donnée à l'IA, et les points RGPD / IA Act.
> L'installation technique est dans `00-guide-installation-plateforme.md`.

---

## 1. Les IA (et outils) retenus

| Outil | Éditeur, pays | Payant ? | Prix trouvé (oct. 2026) | À quoi il sert ici |
|---|---|---|---|---|
| **API Mistral** (La Plateforme) | Mistral AI, France | Oui, à l'usage | Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens (entrée / sortie) ; Mistral Large 3 ≈ 0,50 $ / 1,50 $ — **à vérifier sur mistral.ai/pricing** | Le « cerveau » : rédiger, résumer, répondre, reformuler |
| **Le Chat Pro / Team** (renommé « Vibe » selon plusieurs sources **[À VÉRIFIER]**) | Mistral AI, France | Oui | Pro ≈ 14,99 $/mois ; Team ≈ 24,99 $/utilisateur/mois (19,99 $ en annuel) **[À VÉRIFIER]** | Usage individuel sans installation. **Jamais la version gratuite** avec des données de travail |
| **Albert API / Assistant IA** | DINUM (État français) | Non pour l'administration | Gratuit, dans la limite des capacités (2024) **[conditions 2026 À VÉRIFIER]** | Le « cerveau » pour les collectivités et services publics |
| **Voxtral** (transcription) | Mistral AI, France | Oui (API) ; version *Realtime* à poids ouverts (Apache 2.0) | ≈ 0,003 $/minute (Mini Transcribe 2) | Transformer la parole en texte |
| **faster-whisper** (via Speaches) | open source | Non | Gratuit (coût = serveur) | Transcription **sur votre serveur** : le son ne sort jamais |
| **Open WebUI** | open source | Non | Gratuit (logo à conserver au-delà de 50 utilisateurs) | La « fenêtre de discussion » de l'assistant |
| **n8n** | n8n GmbH, Allemagne | Non (auto-hébergé) | Gratuit ; une instance par client | Les « automates » qui enchaînent les tâches |
| **Baserow** | Baserow B.V., Pays-Bas | Non (auto-hébergé) ; Premium en option | Premium ≈ 10 $/utilisateur/mois (source tierce) | Le « grand cahier rangé » (base de données, CRM, indicateurs) |
| **Logiciel PIA** | CNIL, France | Non | Gratuit, open source | Les analyses d'impact RGPD |
| **Brevo** | Brevo, France | Gratuit puis payant | 300 emails/jour gratuits ; Starter dès ≈ 9 $/mois | Envoyer les emails automatiques |
| **La Suite numérique** (Visio, Tchap, Docs) | DINUM (État) | Non pour les agents publics | Gratuit ; ouverte aux collectivités **[conditions À VÉRIFIER]** | Visio avec transcription pour les administrations |
| **NVDA** | NV Access (open source) | Non | Gratuit | Lecteur d'écran pour les stagiaires malvoyants |

**Règle de souveraineté** : pas d'outil américain (ChatGPT, Copilot, Gemini…) pour traiter des données de
clients. Vos certifications Google restent un atout de compétence ; elles ne vous obligent pas à
recommander Google à un client public.

**Exemple de calcul de coût IA** (Mistral Small 4) : 1 000 requêtes par mois × (2 000 tokens en entrée +
500 tokens en sortie) = 2 millions de tokens en entrée × 0,15 $ + 0,5 million en sortie × 0,60 $ =
**0,60 $ par mois**. Le coût réel d'une mission, c'est votre temps, pas l'IA.

---

## 2. Les solutions (recettes)

### S1 — Assistant IA souverain avec les documents de la structure
- **Expliqué simplement** : « C'est un robot qui a lu tous les classeurs du bureau. Quand on lui pose une question, il va chercher la bonne page et répond avec des mots simples. Il garde les secrets dans la maison. »
- **Outils** : Open WebUI + API Mistral (ou Albert pour une administration).
- **Étapes pour la refaire** :
  1. Installer la plateforme (guide, étapes 1 à 9).
  2. Rassembler les documents **sans données personnelles** (procédures, guides, délibérations publiques, catalogues).
  3. Open WebUI → *Espace de travail* → *Connaissances* → créer une collection, y déposer les documents.
  4. Créer un *Modèle* (assistant) relié à cette collection, avec la consigne ci-dessous.
  5. Créer les comptes utilisateurs (pas d'inscription libre), afficher la bannière IA.
  6. Former les utilisateurs (2 h) : ce qu'on peut demander, ce qu'on ne doit jamais coller.
- **Consigne (prompt système)** :
  > Tu es l'assistant de [STRUCTURE]. Tu réponds en français simple, en t'appuyant uniquement sur les documents fournis. Si l'information n'est pas dans les documents, dis « Je ne trouve pas cette information dans les documents disponibles » et propose à qui s'adresser. Cite toujours le document source. Ne donne jamais d'avis juridique ou médical définitif. Refuse de traiter des données personnelles sensibles (santé, handicap, situation sociale).
- **RGPD** : pas de données personnelles dans la base documentaire ; journaux limités (6 mois). **IA Act** : risque minimal ; bannière de transparence recommandée (et obligatoire si l'assistant est ouvert au public, art. 50).

### S2 — Comptes rendus de réunion automatiques
- **Expliqué simplement** : « C'est un robot qui écoute la réunion comme un petit secrétaire, puis écrit sur une feuille : ce qu'on a décidé, qui doit faire quoi, et pour quand. »
- **Outils** : faster-whisper (local) ou Voxtral + Mistral + n8n (automatisation A1) + Baserow.
- **Étapes** :
  1. Guide, étapes 7, 8 et 10.
  2. Importer l'automatisation **A1** dans n8n.
  3. Créer une table Baserow « Comptes rendus » (Date, Réunion, Participants, Décisions, Actions, Responsable, Échéance, Statut).
  4. Tester avec un enregistrement fictif.
  5. Rédiger la **mention d'information** lue en début de réunion.
- **Consigne** :
  > À partir de cette transcription, rédige un compte rendu structuré : 1) décisions prises, 2) actions avec responsable et échéance (tableau), 3) points en suspens. Style neutre, phrases courtes. N'invente rien : si un responsable ou une date n'est pas mentionné, écris « à préciser ».
- **RGPD** : informer les participants **avant** d'enregistrer ; supprimer l'audio après transcription (ex. 7 jours). **IA Act** : risque minimal.

### S3 — Parcours administratif automatisé (inscriptions, convocations, émargement, enquêtes)
- **Expliqué simplement** : « C'est un robot facteur. Quand quelqu'un s'inscrit, il envoie la lettre de bienvenue, rappelle le rendez-vous la veille, demande si c'était bien, et range tout dans le grand cahier. Personne n'oublie personne. »
- **Outils** : n8n (automatisation A2) + Baserow + Brevo.
- **Étapes** :
  1. Tables Baserow : *Personnes* (minimum : nom, prénom, email), *Sessions*, *Inscriptions* (liens), *Enquêtes*.
  2. Formulaire d'inscription (n8n *Form Trigger* ou formulaire Baserow) avec mention RGPD.
  3. Importer **A2**, régler les délais (J-1, J+1, J+60).
  4. Modèles d'emails Brevo (convocation, rappel, enquête).
  5. Vue Baserow « indicateurs » (taux de présence, satisfaction, mise en œuvre à J+60).
- **Intérêt Qualiopi** : preuves automatiques pour les indicateurs de satisfaction et de suivi.
- **RGPD** : minimisation (pas de date de naissance ni de situation sociale si inutile) ; durée de conservation définie. **IA Act** : pas d'IA dans la décision.

### S4 — Base de pilotage / CRM
- **Expliqué simplement** : « C'est un grand cahier très bien rangé. Chaque chose a sa case, et on retrouve tout en une seconde, au lieu de chercher dans dix tableaux Excel. »
- **Outils** : Baserow (+ client Python et serveur MCP du dépôt `Training`).
- **Étapes** :
  1. Lister les questions que la structure se pose (« combien de… ? », « qui n'a pas… ? »).
  2. En déduire les tables et les liens (ex. *Entreprises* ↔ *Contacts* ↔ *Actions*).
  3. Créer le schéma d'un coup (`create_table_with_schema`), avec des listes déroulantes pour les statuts.
  4. Importer les données existantes (CSV), nettoyer les doublons.
  5. Créer les vues (par statut, par territoire, par échéance) et les droits d'accès.
- **RGPD** : uniquement les champs nécessaires. **IA Act** : non concerné.

### S5 — Tableau de bord et rapport automatique
- **Expliqué simplement** : « Chaque lundi matin, un robot regarde le grand cahier, compte tout, et écrit au chef une petite lettre de dix lignes : ce qui va bien, ce qui ne va pas, ce qu'il faut faire. »
- **Outils** : Baserow + n8n (automatisation A3) + Mistral.
- **Étapes** : définir 5 à 8 indicateurs avec le commanditaire → vues Baserow → importer **A3** → valider la première synthèse à la main pendant 4 semaines.
- **Consigne** :
  > Voici les indicateurs de la semaine et ceux de la semaine précédente. Rédige une synthèse de 10 lignes maximum : évolutions notables (avec chiffres), alertes, une recommandation. N'interprète pas au-delà des chiffres fournis.

### S6 — Chatbot public transparent (site internet)
- **Expliqué simplement** : « C'est un robot d'accueil sur le site. Il dit d'abord : “Bonjour, je suis un robot.” Puis il répond aux questions avec les papiers officiels, et s'il ne sait pas, il passe la main à une vraie personne. »
- **Outils** : n8n (automatisation A4 : *Chat Trigger* intégrable) + Mistral/Albert + documents **publics**.
- **Étapes** : rassembler les pages et FAQ publiques → importer **A4** → message d'accueil obligatoire → bouton « contacter un agent » → test avec 20 questions réelles → intégration sur le site (balise fournie par n8n).
- **Consigne** :
  > Tu es l'assistant d'accueil automatique de [STRUCTURE]. Commence toujours par indiquer que tu es un assistant automatique. Réponds uniquement à partir des informations publiques fournies. Ne demande jamais de données personnelles. Si la question concerne une situation personnelle, oriente vers [contact humain].
- **IA Act** : **art. 50, applicable depuis le 02/08/2026** : l'utilisateur doit savoir qu'il parle à une IA. **RGPD** : ne pas collecter de données ; journaux 30 jours.

### S7 — Kit conformité RGPD & IA Act
- **Expliqué simplement** : « On fait la liste de tous les robots de la maison, on écrit les règles du jeu (ce qu'ils ont le droit de faire, et ce qui est interdit), et on vérifie qu'aucun ne raconte les secrets des gens. »
- **Outils** : Baserow (cartographie), modèle de registre CNIL, logiciel PIA (CNIL), Mistral (aide à la rédaction, relue par vous).
- **Étapes** :
  1. Entretiens (1 à 2 h par service) : quels outils IA sont utilisés, par qui, avec quelles données ?
  2. Cartographie dans Baserow : outil, éditeur, pays, données traitées, catégorie IA Act.
  3. Classement IA Act : interdit / haut risque (annexe III, au 02/12/2027) / transparence (art. 50) / minimal.
  4. Mise à jour du registre RGPD ; AIPD (logiciel PIA) si données sensibles.
  5. Charte d'usage de l'IA (2 pages, validée par le DPO) + liste des outils autorisés.
  6. Formation des agents ou salariés ; **mesures de maîtrise de l'IA (art. 4)** documentées.
- **Livrables** : cartographie, charte, registre à jour, AIPD le cas échéant, plan d'action.

### S8 — Accessibilité et FALC
- **Expliqué simplement** : « Le robot réécrit les papiers compliqués avec des mots faciles et en gros, pour que tout le monde comprenne, même ceux qui voient mal ou qui lisent difficilement. »
- **Outils** : Mistral (automatisation A5) + supports en gros caractères + NVDA (lecteur d'écran gratuit).
- **Étapes** : choisir 5 documents clés → réécriture FALC par l'IA → **relecture humaine obligatoire** (idéalement par une personne concernée) → mise en page accessible (taille 18 minimum, contraste fort, une idée par phrase).
- **Consigne** :
  > Réécris ce texte en FALC : phrases de 15 mots maximum, une idée par phrase, mots courants, pas d'abréviations, pas de pourcentages (dis « 1 personne sur 2 »). Conserve toutes les informations importantes. Ajoute un petit lexique pour les mots indispensables difficiles.

### S9 — Recrutement responsable assisté (sans tri automatique)
- **Expliqué simplement** : « Le robot aide le patron à bien écrire son annonce et à préparer de bonnes questions pour l'entretien. Mais c'est toujours le patron, une vraie personne, qui choisit. Le robot ne trie jamais les gens. »
- **Outils** : Mistral (Le Chat Team ou Open WebUI).
- **Étapes** : atelier ½ journée → réécriture de l'annonce (compétences réelles, pas de critère discriminatoire) → grille d'entretien structurée → règle écrite : **aucune IA pour classer ou écarter des candidats**.
- **IA Act** : le tri ou la notation de candidats est **à haut risque (annexe III, point 4)** → on l'exclut volontairement. **RGPD** : pas de CV dans une IA non maîtrisée.

### S10 — Prospection commerciale assistée (pour les TPE)
- **Expliqué simplement** : « Le robot aide à écrire de jolies lettres aux clients, une par une. Le patron relit toujours avant d'envoyer, et si quelqu'un dit “non merci”, le robot ne lui écrit plus jamais. »
- **Outils** : Baserow (CRM) + n8n (automatisation A6) + Mistral + Brevo.
- **Étapes** : CRM Baserow → import des prospects **professionnels** → brouillons par l'IA → validation humaine → envoi Brevo avec désinscription → relance unique à J+7.
- **RGPD** : B2B, intérêt légitime, en lien avec la fonction de la personne ; information + opposition dans chaque message. **IA Act** : risque minimal.

### S11 — Socle de sécurité
- **Expliqué simplement** : « On met une bonne serrure sur la porte, un gardien qui chasse les voleurs, un coffre pour les clés, et une photocopie de tout dans une autre maison au cas où il y aurait un incendie. »
- **Outils** : CrowdSec, pare-feu, Vaultwarden, double authentification, restic.
- **Étapes** : guide, étapes 3, 11, 13, 14 et 18.

---

## Sources
Voir les sources du guide d'installation ; ajouts :
- IA Act, Omnibus (règlement 2026/1744, haut risque reporté au 02/12/2027, art. 50 au 02/08/2026) — extrait de [aiactinsight.eu](https://aiactinsight.eu/fr/ai-act/digital-omnibus/) et [spicyadvisory.com](https://spicyadvisory.com/blog/digital-omnibus-ai-act-2026-what-changed)
- La Suite numérique ouverte aux collectivités — extrait de [siecledigital.fr](https://siecledigital.fr/2025/12/01/suite-numerique-letat-accelere-sa-revolution-tech-avec-une-alternative-souveraine-aux-geants-americains/) et [acteurspublics.fr](https://acteurspublics.fr/articles/la-dinum-demande-aux-ministeres-de-mettre-la-main-au-portefeuille-pour-developper-sa-suite-numerique/)

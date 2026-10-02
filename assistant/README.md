# Assistant YEBA — votre assistant IA personnel, à la voix, depuis l'iPhone

**Choix retenu (02/10/2026)** : s'appuyer sur l'abonnement Claude existant → **0 € de plus par mois**.
Pas de serveur à payer, pas d'API facturée à l'usage.

```
📱 iPhone — application Claude (mode vocal)
   │   Projet « Assistant YEBA » = instructions C.A.D.R.E. (INSTRUCTIONS_PROJET_CLAUDE.md)
   │   Connecteurs : Gmail · Google Agenda · Google Drive · Airtable
   ▼
🛠️ Claude Code (onglet Code de l'app, ou claude.ai/code) sur ce dépôt
       CLAUDE.md + compétences .claude/skills/ :
       brief-du-matin · echeancier-abonnements · fuseau-horaire · controle-qualiopi-bpf
       Outils : assistant/outils/echeancier.py · assistant/outils/fuseau.py
       Routines programmées (ex. brief chaque jour ouvré à 6h45, heure de La Réunion)
```

## Installation sur l'iPhone (20 minutes)

1. Mettre à jour l'application **Claude** (éditeur : Anthropic) depuis l'App Store.
2. **Réglages du compte** : activer la double authentification ; dans Confidentialité, vérifier que
   l'utilisation des conversations pour l'entraînement des modèles est désactivée.
3. **Connecteurs** (Réglages → Connecteurs) : vérifier que Gmail, Google Agenda, Google Drive et
   Airtable sont connectés au compte **yebaformations@gmail.com** et à la base YEBA. Accorder la
   lecture ; refuser ce qui n'est pas nécessaire.
4. **Projet** : créer « Assistant YEBA » et coller le contenu de `INSTRUCTIONS_PROJET_CLAUDE.md` dans
   les instructions du projet. Y déposer les documents de référence (catalogue, CGV, règlement
   intérieur) — **jamais** d'export de la table APPRENANTS.
5. **Mode vocal** : ouvrir le projet, toucher l'icône de la voix, tester :
   « Quel est mon prochain rendez-vous ? » · « Résume mes courriels non lus » ·
   « Combien d'inscrits sur la prochaine session ? »
6. **Raccourci** : maintenir l'icône Claude sur l'écran d'accueil, ou créer un raccourci iOS
   (app Raccourcis) « Dis Siri, assistant YEBA » qui ouvre l'application.
7. **Tâches lourdes** (contrôle Qualiopi, échéancier, préparation BPF) : onglet **Code** de l'app,
   sur ce dépôt — les compétences ci-dessus s'y chargent automatiquement.

> Les noms exacts des menus peuvent changer avec les mises à jour de l'application : en cas de
> doute, centre d'aide https://support.claude.com.

## Vos 10 demandes : ce qui est faisable, comment, et ce qu'il faut savoir

| # | Demande | Faisable ? | Comment | Conformité |
|---|---------|-----------|---------|-----------|
| 1 | Gérer la boîte mail | ✅ Oui, en **brouillons** | Connecteur Gmail : tri, résumés, brouillons. Vous envoyez. | **RGPD** (données de stagiaires et clients ; Google LLC, transfert hors UE — déjà signalé dans CONFIG SYSTEME, cible Brevo pour les envois automatiques) |
| 2 | Google Agenda | ✅ Oui | Connecteur Agenda ; création ou déplacement après « je confirme » | **RGPD** (noms des participants) |
| 3 | Airtable (centre de formation) | ✅ Oui | Connecteur Airtable sur la base `appQ2zqc80kkc6MR1` | **RGPD** (APPRENANTS) ; **IA Act** : jamais de notation ou de tri d'apprenants (annexe III, point 3) |
| 4 | Documents à portée de main, remplissables | ✅ Oui | Connecteur Drive + table DOCUMENTS OFFICIELS YEBA ; l'assistant pré-remplit, vous signez | **RGPD** si le document est nominatif |
| 5 | Mise à jour Qualiopi et BPF | ⚠️ Préparer, pas déposer | Compétence `controle-qualiopi-bpf` : pièces manquantes, chiffres du BPF. Dépôt par vous sur Mon Activité Formation | **RGPD** (chiffres agrégés) |
| 6 | WhatsApp Business | ❌ Pas de connecteur | L'assistant rédige le message, vous le copiez. Une automatisation passe par l'interface professionnelle payante de Meta : non retenue (budget, données hors UE) | **RGPD** (Meta, hors UE) |
| 7 | Site internet (formulaire, mails) | ⚠️ Pas de site à ce jour (02/10/2026) | À construire chez OVHcloud (décision CONFIG du 23/09/2026) : formulaire → table Airtable → brouillon de réponse. Vérifier le site « YEBA Formations Portal » sur blink.new signalé dans CONFIG | **RGPD** : mention d'information sous le formulaire (art. 13) ; mentions légales LCEN |
| 8 | Trajets Google Maps | ❌ Pas de connecteur | L'assistant calcule l'heure de départ à partir de vos rendez-vous et d'une durée donnée ; l'application de cartes fait le trajet | **RGPD** (position = donnée personnelle) |
| 9 | Suivi comptable (URSSAF, compta) | ⚠️ Préparer, pas déclarer | Pas de logiciel à ce jour : choisir un outil de facturation relié à une **plateforme agréée** (facturation électronique). Depuis DEVIS & FACTURES : CA encaissé, impayés, échéances | **RGPD** si clients particuliers |
| 10 | Abonnements : échéancier + prévisionnel | ✅ Oui | Compétence `echeancier-abonnements` + `outils/echeancier.py`. **La table CHARGES & ABONNEMENTS est vide** : la remplir d'abord | Aucune donnée personnelle |
| + | Fuseaux horaires des interlocuteurs | ✅ Oui | Règle « deux heures » dans les instructions + `outils/fuseau.py` (heure d'été comprise) | — |

## Routine programmée

- **Brief du matin YEBA** : du lundi au vendredi à **7h28** (heure de La Réunion), notification
  sur l'iPhone. Lecture seule. Identifiant : `trig_01LMngvJgESC3EEdjKssSoh6`.
- ⚠️ Créée sans connecteurs : les ajouter (Gmail, Google Agenda, Airtable) dans la routine depuis
  claude.ai, sinon le brief signalera qu'il ne peut pas lire les sources.

## Outils en ligne de commande

```bash
python assistant/outils/echeancier.py abonnements.csv              # mois prochain
python assistant/outils/echeancier.py abonnements.csv --mois 2026-11 --sur 3
python assistant/outils/fuseau.py 2026-11-12 14:00 paris          # 14h Réunion → 11h Paris
python assistant/outils/fuseau.py 2026-11-12 09:00 montreal --depuis
```

Aucune dépendance : Python 3.9 ou plus récent (module standard `zoneinfo`).

## Sécurité — règles non négociables

- Double authentification sur Google, Airtable et Claude (également exigée par votre assurance
  cyber — voir CONFIG SYSTEME, contrat HRCP300980).
- Brouillons seulement ; aucune suppression ; confirmation avant toute écriture.
- Révision trimestrielle des accès des applications connectées (compte Google → Sécurité).
- Ligne « Assistant IA personnel » à ajouter au registre des traitements (YEBA-DOC-16) : modèle
  dans le livret de la formation, chapitre 9.

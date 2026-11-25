# Comp AI (trycompai/comp) — dossier d'installation pour YEBA

Objectif : un outil de pilotage de la conformité (RGPD, ISO 27001, SOC 2) pour les
audits « gouvernance RGPD & IA Act » des clients de YEBA.

Source lue le 25/11/2026 : dépôt github.com/trycompai/comp, fichiers `README.md`,
`SELF_HOSTING.md`, `docker-compose.yml`, `apps/app/.env.example`.

## Ce que c'est (et ce que ce n'est pas)

- Plateforme open source de conformité : collecte de preuves, politiques, contrôles,
  portail fournisseurs. Référentiels : SOC 2, ISO 27001, HIPAA, GDPR.
- Interface en **anglais**. Aucun référentiel français prêt à l'emploi (pas de modèle CNIL, pas d'IA Act).
- **Licence AGPL-3.0** : si YEBA modifie le code **et** le fait utiliser à ses clients
  par Internet, YEBA doit publier ces modifications. Usage interne ou sans modification :
  aucune obligation. [point juridique à respecter]
- Pas d'annuaire d'entreprises : ne remplace pas Pappers (voir `scripts/fiche_entreprise.py`).

## Pourquoi ce n'est pas installé « tout de suite » dans la session cloud

1. Le conteneur de Claude Code est **éphémère** : il est effacé après la session. Une
   instance installée ici disparaîtrait avec les données des clients. Il faut un serveur durable.
2. Le guide officiel exige des services externes (tableau ci-dessous). Aucun compte n'existe à ce jour.
3. Il faut deux adresses web (application + portail) avec HTTPS.

## Services exigés et localisation des données

| Service | Rôle | Obligatoire | Localisation / alternative souveraine |
|---|---|---|---|
| PostgreSQL 14+ avec SSL | base de données | oui | OVHcloud (France) : base managée ou sur le serveur |
| Resend | envoi des e-mails de connexion | oui (dans le code) | États-Unis → transfert hors UE (RGPD chap. V). Remplacement par Brevo (France) = modification du code (AGPL) |
| Trigger.dev | tâches de fond | oui | cloud par défaut ; version auto-hébergeable sur le même serveur |
| Stockage S3 (`APP_AWS_*`, `APP_AWS_ENDPOINT`) | fichiers de preuve | selon usage | OVHcloud Object Storage (compatible S3, France) |
| OpenAI / Anthropic / Groq | fonctions IA | non | à laisser vide au départ : aucune donnée client envoyée à un modèle américain |
| PostHog, Vercel, Stripe, Upstash, Firecrawl, Novu, Fleet | statistiques, hébergement, paiement… | non | ne pas renseigner (mode `NEXT_PUBLIC_SELF_HOSTED=true`) |
| Google / Microsoft / GitHub (connexion) | authentification | non | connexion par e-mail suffit |

## Architecture recommandée (souveraine)

- 1 serveur OVHcloud en France (le compte OVHcloud existe déjà, mail du 04/11/2026),
  4 vCPU / 8 Go de RAM minimum pour la compilation du projet (monorepo Next.js).
- Docker (`docker compose build`, `migrator`, `seeder`, `up -d app portal`), suivant `SELF_HOSTING.md`.
- Sous-domaines proposés : `conformite.yebaformations.re` (application) et `portail.yebaformations.re`.
- Sauvegarde quotidienne chiffrée de la base (RGPD art. 32).

## Ce qu'Aurélien doit fournir (décision dans Airtable > DÉCISIONS DU DIRIGEANT)

1. Accord sur le serveur OVHcloud (coût mensuel à vérifier sur ovhcloud.com avant commande).
2. Accès DNS du domaine yebaformations.re pour les deux sous-domaines.
3. Accord sur Resend (américain) **ou** sur la modification du code pour Brevo.
4. Création des comptes : se fera avec request_credential / dans l'environnement, jamais en clair dans le dépôt.

## En attendant : l'outil de la CNIL, dès ce soir

Pour les analyses d'impact (AIPD, RGPD art. 35), le **logiciel PIA de la CNIL** est gratuit,
libre, en français et fonctionne sur le poste, sans serveur (cnil.fr, rubrique « Outil PIA »).
Il couvre la partie « preuve RGPD » des audits clients pendant que Comp est préparé.

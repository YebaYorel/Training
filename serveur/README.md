# Serveur YEBA Studio

Petit serveur Node (aucune dépendance) : **paiement Mollie**, **délivrance des licences**, **relais IA Mistral**.
À héberger dans l'Union européenne (Scaleway, OVHcloud VPS, Clever Cloud…), derrière HTTPS.

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `LICENCE_CLE_PRIVEE` | Clé privée Ed25519 (créée par `npm run licence -- cles`). **Secret.** |
| `MOLLIE_API_KEY` | Clé API Mollie (`test_…` pour essayer, `live_…` en production). **Secret.** |
| `MISTRAL_API_KEY` | Clé API Mistral AI (La Plateforme). **Secret.** |
| `MISTRAL_MODELE` | Modèle (défaut `mistral-small-latest`). |
| `ORIGINES` | Adresses autorisées à appeler le serveur, ex. `https://www.yebaformations.re`. |
| `URL_APPLI` | Adresse du logiciel, ex. `https://www.yebaformations.re/studio`. |
| `AIRTABLE_TOKEN` | Facultatif : enregistre chaque licence vendue dans « STUDIO — LICENCES » (portée `data.records:write` sur cette seule table). |
| `QUOTA_IA_JOUR` | Demandes IA par licence et par jour (défaut 60). |
| `PORT`, `HOTE` | Défaut 8787 / 127.0.0.1 (mettre un reverse proxy HTTPS devant). |

## Lancer et tester

```bash
npm run serveur          # démarre
node serveur/test.mjs    # 14 tests avec de faux Mollie / Mistral (aucun appel réel)
```

## Brancher le logiciel sur le serveur

```bash
VITE_STUDIO_API=https://api.votre-domaine.re npm run build:tout
```

Puis ajouter l'adresse du serveur à `connect-src` dans `site/public/.htaccess`.

## Sans serveur

Le logiciel fonctionne quand même : la commande part par e-mail pré-rempli (avec le code poste),
vous encaissez par un **lien de paiement Mollie** créé dans votre tableau de bord, puis vous émettez la licence :

```bash
npm run licence -- emettre --offre bpf --poste XXXX-XXXX-XXXX --nom "Nom Prénom" --email x@y.re --organisme "OF"
```

CARBURANT fonctionne alors avec ses règles et des modèles de textes (pas d'IA générative).

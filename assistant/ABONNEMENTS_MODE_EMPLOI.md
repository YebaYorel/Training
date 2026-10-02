# Remplir la table CHARGES & ABONNEMENTS — mode d'emploi (20 minutes)

Base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) » → table **CHARGES & ABONNEMENTS**.
Une ligne par prélèvement récurrent. Le champ « Coût annualisé estimé » se calcule tout seul.

## Étape 1 — Retrouver vos abonnements (4 sources, dans cet ordre)

1. **Relevés bancaires des 12 derniers mois** (compte professionnel) : surlignez chaque prélèvement
   qui revient (mensuel) ou qui est apparu une seule fois avec un libellé d'éditeur (souvent annuel).
2. **Gmail** : tapez dans la barre de recherche :
   `subject:(facture OR reçu OR receipt OR invoice OR renouvellement OR abonnement OR subscription) newer_than:1y`
3. **iPhone** : Réglages → touchez votre nom → **Abonnements** (tout ce qui est payé via l'App Store).
4. **Comptes en ligne** : PayPal (Paiements automatiques), Google (Paiements et abonnements).

À ne pas oublier dans votre cas (montants à relever sur vos factures, je ne les connais pas) :
abonnement Claude · Airtable · nom de domaine · hébergement du site (OVHcloud si souscrit) ·
téléphone et box · assurance RC Pro Hiscox (annuelle, échéance le **10/09**) · audit de surveillance
Qualiopi (ponctuel) · médiateur de la consommation (annuel, dès l'adhésion) · banque (frais de tenue
de compte) · logiciels de conception (Canva, etc.).

## Étape 2 — Saisir une ligne par abonnement

| Champ | Ce que vous saisissez | Exemple |
|---|---|---|
| **Nom du service** | Le nom tel qu'il apparaît sur la facture | Claude — abonnement |
| **Catégorie** | Automatisation / IA · Communication · Hébergement · Logiciel de gestion · Autre | Automatisation / IA |
| **Coût** | Le montant **TTC réellement prélevé** (vous êtes en franchise de TVA : la TVA payée n'est pas récupérable) | 21,60 € |
| **Fréquence** | Mensuel · Annuel · Ponctuel | Mensuel |
| **Prochain renouvellement** | La date du **prochain** prélèvement (pas celle du dernier) | 12/11/2026 |
| **Statut** | Actif · En pause · Résilié | Actif |
| **Notes** | Moyen de paiement (« CB pro », « prélèvement »), date limite de résiliation | Résiliable à tout moment |

Le montant de l'exemple est fictif.

> ⚠️ **Sécurité / RGPD** : ne saisissez **jamais** de numéro de carte, d'IBAN ou d'identifiant de
> connexion dans cette table. Le nom du moyen de paiement suffit.

## Étape 3 — Dicter plutôt que taper (depuis l'iPhone)

Dans l'application Claude, projet « Assistant YEBA », dites par exemple :

> « Ajoute dans mes abonnements : Airtable, catégorie logiciel de gestion, 24 euros, mensuel,
> prochain prélèvement le 15 novembre, actif. »

L'assistant vous relit la ligne et attend « je confirme » avant d'écrire.

## Étape 4 — Obtenir l'échéancier

Dites : « Quel est mon prévisionnel d'abonnements pour le mois prochain ? »
(Ou, dans Claude Code : compétence `echeancier-abonnements`.)

Pensez à mettre à jour la date de « Prochain renouvellement » après chaque prélèvement annuel :
l'assistant vous le proposera.

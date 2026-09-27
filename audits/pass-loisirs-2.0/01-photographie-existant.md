# PASS LOISIRS 2.0 — Étape 1 : photographie de l'existant (lecture seule)

- **Date** : 27/09/2026
- **Périmètre lu** : workspace Airtable « Pass Loisirs 2.0 », base `PASS LOISIRS 2.0 — ACM (2026-2027)` (`appGyK0pp3tlRABVA`)
- **Méthode** : lecture via le connecteur Airtable, **aucune écriture** (ni donnée, ni structure, ni automatisation).
- **Source de toutes les constatations** : extrait de la base Airtable `appGyK0pp3tlRABVA` (schéma, descriptions de tables, table « Paramètres », interfaces, automatisations).

> **Erratum du 27/09/2026 (après les correctifs)** : voir `02-rapport-ASTRA6.md`, section 5.
> - Le constat P0-2 était mal localisé. Le tableau de bord 01 ne montrait qu'une ligne, à cause d'un filtre caché ; le code était exposé sur la page Direction « Paramètres et points à trancher ». Il est corrigé.
> - Le texte des formules **est** lisible : elles ont été auditées.
> - P0-1, P0-2 et le calcul des soldes sont corrigés.

---

## 1. Chiffres vérifiés

| Élément | Constat |
|---|---|
| Tables | **36** (dont 2 marquées « DÉPRÉCIÉE ») |
| Champs | **631** — dont 82 formules, 40 cumuls, 19 recherches, 100 liens entre tables, 6 pièces jointes |
| Tables les plus lourdes | Enfants (58 champs), Inscriptions (56), Factures (33), Liens personne-enfant (30), Devis (29), Présences (28) |
| Interfaces | **6** (Animateur, Responsable ACM, Administratif, Comptabilité, Direction, « Anim'Loisirs 974 — Pilote ACM ») — 25 pages publiées + 1 brouillon |
| Automatisations | **9**, toutes **non déployées** (`undeployed`) |
| Données | **Fictives** : 16 enfants préfixés « TEST », 16 personnes avec des alias `+…@` de la boîte projet. Paramètre `MODE_DONNEES = FICTIF` |
| Paramètres | 40 lignes, dont **13 « À RENSEIGNER »** et 7 « À VALIDER » |
| Code applicatif | **Absent** de ce dépôt. La base cite un fichier `SECURITE_APPLICATION.md` « dans le dépôt » : ce dépôt ne le contient pas |

## 2. Ce qui est solide (à conserver)

- Le **droit de récupération porté par le lien personne-enfant**, daté et révocable, et non par une case.
- La **séparation encaissement / affectation** qui évite le double comptage.
- Des **e-mails automatiques sans nom d'enfant ni donnée de santé** (compteurs + liens).
- Registre des traitements, journal d'audit, registre des violations avec délai de 72 h.
- Allergènes en **liste fermée INCO (14)** croisés avec le menu du jour.
- Gardes anti-doublon posées **avant** chaque envoi.

Le prototype métier est mûr sur le plan conceptuel. Les faiblesses sont surtout dans **l'exécution et les droits**.

## 3. Constats classés

### P0 — bloquant avant toute donnée réelle

| # | Constat | Preuve dans la base | Cadre |
|---|---|---|---|
| P0-1 | Dans l'interface **Animateur**, le champ « Liens personne-enfant » de la fiche enfant est **modifiable**, et la création d'enfants en ligne est **autorisée**. Un animateur peut donc toucher à la chaîne qui fonde un départ sécurisé. | Page `Enfants du jour — consignes utiles` : `isEditable: true`, `canCreateRecordsInline: true` | RGPD art. 32 (sécurité) + sécurité des mineurs |
| P0-2 | Le tableau de bord « 01 · Vue d'ensemble » affiche **Clé / Valeur / Statut de tous les Paramètres**, y compris le **code d'accès physique du portail**. | Élément `pelUD234Uq5cl6omZ` | Sécurité physique, RGPD art. 32 |
| P0-3 | Des **pièces jointes sensibles** restent dans 5 tables : preuve de restriction judiciaire, dérogation de départ, justificatif d'hospitalisation (donnée de santé), documents enfant, dossiers. La base reconnaît elle-même que la situation n'est **pas conforme** aujourd'hui. | Paramètre `PJ_MEDICALES_VIA_SERVEUR = « Non - NON CONFORME »` ; description de la table « Paie » | RGPD art. 9 et 32 |
| P0-4 | La table **Enfants** contient une recherche « ⚠️ Alerte santé (DÉTAIL MÉDICAL) ». Le détail médical est donc visible par tout collaborateur de la base et par l'API, ce qui contredit la règle écrite dans la table Santé. | Schéma Enfants | RGPD art. 9 (minimisation, habilitation) |
| P0-5 | **Aucun cloisonnement entre associations** : pas de table « Structure/Organisateur » ni de clé de rattachement. Un produit vendu à plusieurs ACM mélangerait leurs données. | Schéma complet | RGPD art. 5, 24 et 28 |
| P0-6 | Les **fondations juridiques** ne sont pas renseignées : responsable de traitement, DPA signé, région d'hébergement, qualification HDS, AIPD, mécanisme de transfert hors UE, test de restauration, MFA. | Paramètres `RESPONSABLE_TRAITEMENT`, `DPA_CONCLU`, `HEBERGEMENT_REGION`, `HDS_QUALIFICATION`, `AIPD_STATUT`, `MECANISME_TRANSFERT`, `SAUVEGARDE_RESTAURATION_TESTEE`, `MFA_OBLIGATOIRE` | RGPD art. 28, 30, 35, 44+ |
| P0-7 | **Souveraineté** : les adresses d'expédition et d'alerte sont chez Gmail (Google) et l'outil (Airtable) est un éditeur américain. Le transfert hors UE n'est ni qualifié ni encadré. | `EMAIL_EXPEDITEUR`, `EMAIL_ALERTES`, `MECANISME_TRANSFERT` | RGPD chap. V |

### P1 — à corriger pour que les parcours fonctionnent réellement

| # | Constat | Preuve |
|---|---|---|
| P1-1 | **Aucune automatisation n'est déployée.** Les parcours formulaire → devis → confirmation → facture → relance n'ont jamais tourné en conditions réelles. | 9 × `deploymentStatus: undeployed` |
| P1-2 | Le lien du formulaire et le pack PDF manquent. Si l'automatisation « Envoi du formulaire » était activée, 15 enfants « A ENVOYER » recevraient un lien vide. | `URL_FORMULAIRE_INSCRIPTION = « À COLLER ICI »`, `PACK_INSCRIPTION_PDF = « À DÉPOSER »` |
| P1-3 | Le **plan gratuit** est évoqué dans une automatisation. S'il est confirmé, ses quotas (enregistrements par base, exécutions mensuelles) ne tiennent pas une saison réelle : 34 mercredis × 40 places représentent 1 360 présences à eux seuls. | Description de l'automatisation « Veille quotidienne » — **quotas à vérifier sur airtable.com/pricing** |
| P1-4 | **Doublons de modèle** laissés en place : Responsables et Personnes autorisées (dépréciées mais toujours reliées), Familles et Personnes (adresse en double), Dossiers et Documents, Présences « Récupéré par / Autorisé » (texte libre) et Mouvements de départ, « Santé repérée (DÉPRÉCIÉ) ». | Schéma |
| P1-5 | **Deux modèles de prix coexistent** (« Tarif final » et « Montant à facturer » via les lignes), avec plusieurs soldes : Reste dû, Reste à payer (net), Total encaissé, Total affecté. Le tableau de bord utilise l'ancien modèle et la page « 10 · Soldes fiables » est restée en brouillon. | Tableaux de bord 01 et 09 ; brouillon `pag6fcIH4tdqh8hrT` |
| P1-6 | Le journal d'audit et la numérotation des factures ne sont **pas infalsifiables** dans Airtable. La base le reconnaît elle-même. | Descriptions « Journal d'audit » et « Factures » |

### P2 — hygiène

- Deux champs portent le même nom, « Mouvements de départ », dans **Équipe** (`fldhcNAJpF98JD61z`, `fldWMS3gbflph8jEx`).
- Coquille « Allèrgènes » dans 4 champs.
- Deux identités coexistent : l'interface « Anim'Loisirs 974 » et la base « PASS LOISIRS 2.0 ». Cela rejoint la question du responsable de traitement (P0-6).

## 4. Limites de cette lecture (à ne pas surinterpréter)

- Le connecteur ne renvoie **pas le texte des 82 formules**, seulement leur type. Leur logique n'est donc **pas auditée**.
- Les éléments suivants sont **invisibles** via le connecteur : collaborateurs et rôles, partages publics, forfait, région, historique des révisions et paramétrage MFA. Ils doivent être vérifiés à l'écran, dans les réglages de la base et du workspace.
- Seuls les enregistrements de 3 tables ont été lus : Paramètres, Enfants (noms) et Personnes (e-mails).
- Sans le **code** de l'application, la pile technique, l'hébergement, l'authentification et la gestion des jetons ne sont **pas auditables**.

## 5. Aucune modification effectuée

Aucune correction n'a été appliquée. Les corrections P0-1 et P0-2 (droits d'interface) sont rapides, mais elles attendent la validation d'Aurélien.

---
title: "Feuille 2 — 10 questions d'examinateurs + 3 questions à leur poser"
---

Format de chaque réponse : **Technique** (ce que j'ai fait, avec les mots du métier) → **Simple** (comme à ma mère). Viser 45 à 60 secondes par réponse.

## Q1. Pourquoi 12 tables, et comment sont-elles reliées ?

**Technique** — Une table = un objet métier. J'ai les 6 tables du sujet, plus Pointages et Achats parce que l'annexe calcule le coût par Σ(heures × coût horaire) et Σ(achats HT) : il faut une ligne par dépense. Demandes et Rapports terrain reçoivent les formulaires ; Interactions et Logs assurent la traçabilité. CHANTIERS est la table pivot : relations 1-N (un client → plusieurs chantiers ; un chantier → plusieurs factures). Les champs *lien* créent automatiquement le champ inverse ; les *lookups* lisent une valeur liée, les *rollups* l'agrègent.
**Simple** — Un tiroir par sorte de papier, et des ficelles entre les tiroirs : je tire la ficelle d'un chantier, j'ai son client, ses factures et ses heures.

## Q2. Comment la marge est-elle calculée ? Donnez un exemple.

**Technique** — Pointages : *Coût MO = Heures × Coût horaire* (rollup depuis Ressources). Chantier : rollups *Coût MO*, *Coût achats*, *CA facturé* ; formules *Coût total = MO + achats*, *Marge = CA − coût total*, *Taux = marge ÷ CA × 100*. Chantier C1 : 900 + 600 = 1 500 € de MO ; 800 + 1 200 = 2 000 € d'achats ; 3 500 € de coût ; 5 000 € facturés ; marge 1 500 € ; **30 %**.
**Simple** — On additionne ce que le chantier a coûté, on le retire de ce qu'on a facturé : il reste 1 500 €, soit 30 centimes gagnés par euro facturé.

## Q3. Comment Airtable et Make communiquent-ils ?

**Technique** — Deux modes. *Polling* : le module Make « Watch Records » interroge Airtable à intervalle fixe (15 min minimum en offre gratuite) et exige un champ *Created time* ou *Last modified time*. *Webhook* : une automatisation Airtable (« Exécuter un script ») envoie un POST vers un webhook Make dès l'événement. J'ai choisi le webhook pour S1, S2, S6 (temps réel, aucune opération à vide) et la planification quotidienne pour S3, S4, S5. Toutes les écritures retour utilisent l'**API Airtable** via une connexion Make. *Source exigence champ : apps.make.com, « Airtable modules ».*
**Simple** — Soit Make passe voir toutes les 15 minutes s'il y a du courrier, soit Airtable sonne chez Make quand une lettre arrive. J'ai mis une sonnette.

## Q4. Comment avez-vous limité la consommation Make ?

**Technique** — 1 module exécuté = 1 opération. (1) Webhooks au lieu du polling : ≈ 610 opérations/mois au lieu de ≈ 9 250, et le script Airtable envoie toutes les données utiles dans le webhook (pas de relecture). (2) Calculs faits par les **formules Airtable** (gratuites), pas par Make. (3) **Filtres** en début de scénario, sur des champs déjà calculés (« Alerte devis = À relancer »). (4) **Agrégateur de texte** : 1 email de synthèse au lieu d'un par chantier. (5) Planification à 8 h les jours ouvrés seulement (22 exécutions/mois). (6) Case « Traité par Make » : anti-doublon.
**Simple** — Le facteur ne se déplace que s'il y a vraiment du courrier, et il met toutes les lettres du patron dans une seule enveloppe.

## Q5. Comment gérez-vous les erreurs ?

**Technique** — Trois familles. *Connexion/API et quota (429)* : gestionnaire d'erreur **Break** → réessai automatique 3 fois toutes les 15 min, exécution stockée en « incomplete execution ». *Données manquantes* (email absent) : **filtre** en amont + **Ignore** avec ligne dans LOGS ERREURS. *IA indisponible* : **Resume** avec un texte de relance standard pré-écrit. Chaque erreur crée un enregistrement dans LOGS ERREURS et envoie un email à Zineb. Réglage du scénario : notifications d'erreur activées, nombre d'erreurs consécutives avant désactivation surveillé.
**Simple** — Si la Poste est en grève, on réessaie plus tard ; si l'adresse manque, on met la lettre de côté et on prévient Zineb ; rien ne se perd en silence.

## Q6. Comment l'IA est-elle intégrée, et comment éviter qu'elle invente ?

**Technique** — Module Mistral AI « Create a Chat Completion » : prompt **system** (rôle, format imposé, interdiction d'inventer, « non précisé » si information absente), prompt **user** avec uniquement les champs utiles, **température 0,2**. Sortie découpée par `split()` (fonction de mapping, 0 opération). Relances de niveau 3 : aucune émission automatique, alerte à Paul (**humain dans la boucle**). Chaque texte IA est tracé dans INTERACTIONS (« Généré par IA »).
**Simple** — L'IA a une fiche de poste très stricte : résumer, ne rien inventer, rester polie. Et pour les lettres sensibles, c'est le patron qui décide.

## Q7. Airtable et Make sont-ils conformes au RGPD ?

**Technique** — Ce sont des **sous-traitants** (art. 28) : signer leur DPA (clauses contractuelles types pour les transferts). Airtable stocke par défaut aux États-Unis (AWS US-East-1), résidence UE seulement en Enterprise Scale. Make propose les zones de données **EU1/EU2**, mais certaines fonctions IA peuvent être traitées aux États-Unis. Côté NéoBâti : registre des traitements (art. 30), minimisation (aucune donnée de santé : j'ai supprimé l'option « Arrêt maladie » de l'ancienne base), durées (prospect : 3 ans après le dernier contact, champ « Date de purge RGPD » ; factures : 10 ans), case « Opposition aux relances » (art. 21), information sur le formulaire (art. 13). *Sources : support.airtable.com (GDPR at Airtable, Data residency FAQs) ; help.make.com (AI providers and data zones in Make).*
**Simple** — Les données des clients sont confiées à des prestataires : on signe un contrat qui les oblige à les protéger, on ne garde que l'utile, et on efface quand ça ne sert plus.

## Q8. Quel est le niveau de risque au sens de l'IA Act ?

**Technique** — Usage = génération et résumé de textes métier : **risque limité/minimal**, pas un système à haut risque. Il le deviendrait si l'IA évaluait ou classait les artisans (emploi, annexe III) : je l'ai exclu. Obligation applicable dès maintenant : **art. 4, maîtrise de l'IA** (former les utilisateurs — fait pendant la passation). Bonne pratique : mention et validation humaine des textes IA.
**Simple** — L'IA écrit des lettres, elle ne juge personne. Elle n'est pas dangereuse, mais l'équipe doit savoir s'en servir.

## Q9. Comment sécurisez-vous les accès ?

**Technique** — Comptes **nominatifs** au domaine du client, **2FA** obligatoire, rôles au moindre privilège (artisans : formulaire + page Terrain en lecture), **Personal Access Token** Airtable limité aux scopes `data.records:read/write` et `schema.bases:read` et à **une seule base**, jeton secret dans le corps des webhooks (filtre Make), aucun secret écrit en clair dans les modules, gestionnaire de mots de passe, procédure de départ d'un salarié. *Référence : ANSSI, Guide d'hygiène informatique.*
**Simple** — Chaque personne a sa clé, il faut aussi un code reçu sur le téléphone, et chacun n'ouvre que les portes dont il a besoin.

## Q10. Comment le client devient-il autonome après votre départ ?

**Technique** — Propriété : tous les comptes (Airtable, Make, Mistral, emails) au nom et sur la carte bancaire de NéoBâti ; je ne suis qu'invité, puis retiré. Livrables : guide utilisateur par rôle, fiches scénarios, export des **blueprints** Make (versionnés), *snapshot* Airtable. Exploitation : Zineb vérifie LOGS ERREURS et l'historique Make 5 min par semaine ; runbook « que faire si… ». Formation par rôle.
**Simple** — Je rends les clés de la maison, le mode d'emploi et le carnet d'entretien. Je peux revenir, mais ils n'ont pas besoin de moi pour vivre dedans.

---

## 3 questions à poser aux examinateurs (en fin d'oral)

1. « Sur vos missions TPE, préférez-vous des **webhooks déclenchés par une automatisation Airtable** (qui demande une offre payante pour l'action script) ou le **polling** Make, quand le client veut rester en gratuit ? »
2. « Depuis que Make facture en **crédits**, avec des modules IA à consommation variable, comment conseillez-vous de **budgéter l'IA** pour un client comme NéoBâti ? »
3. « Avec l'**article 4 de l'IA Act** (maîtrise de l'IA) et le RGPD, intégrez-vous la **documentation des prompts et des validations humaines** au dossier de conformité remis au client ? »

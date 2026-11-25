---
name: yeba-prospection
description: Prospection YEBA en un geste. Aurélien donne seulement le NOM d'une entreprise (ou remplit « Entreprise » dans la table Airtable PROSPECTION avec le statut « À préparer ») ; le skill fait tout le reste : fiche légale gratuite (API officielle Recherche d'entreprises, à la place de Pappers), contrôle des oppositions, mail de contact conforme (CPCE L34-5, LCEN art. 20, RGPD art. 6.1.f et 14), relance J+7, liste des pièces à joindre, brouillon Gmail, écriture dans Airtable et ligne de preuve dans JOURNAL DES PREUVES.
---

# Prospection en un geste — « je cite le nom, tu fais tout »

Base Airtable : `appQ2zqc80kkc6MR1` (YEBA FORMATIONS - Centre de formation (Adaptable)).
Tables : PROSPECTION `tblBOsfbP4qaM5brL` · Oppositions STOP `tblO5XJLAIJxKEvR7` ·
ENTREPRISES & CLIENTS `tblVLHyTCywkNtmvr` · CONFIG SYSTEME `tblQJDUCikyk9zCjq` ·
JOURNAL DES PREUVES `tblmdeNVCQhf9NW4T`.

## 1. Déclencheurs

- « Prospecte <entreprise> », « prépare un mail pour <entreprise> ».
- Lignes de PROSPECTION au statut « À préparer » : les traiter toutes, une par une.

## 2. Contrôles AVANT d'écrire (bloquants)

1. **Opposition** : chercher le nom et le domaine dans « Oppositions STOP ». Présent → statut « STOP (opposition) », on n'écrit rien d'autre.
2. **Déjà client ou en discussion** : chercher dans ENTREPRISES & CLIENTS et BOÎTE DE RÉCEPTION. Présent → ne pas envoyer de prospection à froid ; le noter et le dire à Aurélien.
3. **Fiche légale** : `python scripts/fiche_entreprise.py "<nom>"` (974 par défaut ; `--dep ""` pour toute la France).
   - Champ `opposition_prospection = true` → **NE PAS CONTACTER** (statut STOP, motif « opposition INSEE »).
   - Plusieurs résultats → demander à Aurélien lequel (ne jamais choisir au hasard).
   - API en panne → page annuaire-entreprises.data.gouv.fr via l'agent web-fetch ; Pappers seulement si Aurélien l'accepte (payant).

## 3. Adresse e-mail : règles (RGPD + CNIL)

- Priorité : adresse **générique** (contact@, accueil@, direction@) trouvée sur le site de l'entreprise ou ses mentions légales. Source notée dans « Source de l'email ».
- Adresse nominative d'un salarié : uniquement si elle est publiée par l'entreprise et que le message concerne **sa fonction** (CNIL, prospection B2B). Jamais de devinette du type prenom.nom@.
- Aucune adresse trouvée → laisser vide, statut « Prêt à envoyer » quand même, noter « email à trouver (formulaire de contact ou téléphone) ».
- Jamais de collecte par scraping de LinkedIn ni d'outil hors UE avec des données de personnes (règle CLAUDE.md).

## 4. Le mail (structure imposée, 150 mots maximum)

Objet : court, concret, sans majuscules criardes ni « gratuit !!! » (filtres anti-spam). Ex. : « <Entreprise> : l'IA au quotidien de vos équipes, sans risque RGPD ».

Corps :
1. Salutation (« Madame, Monsieur, » ou dirigeant public : « Monsieur DUPONT, »).
2. **Une phrase sur eux** tirée de la fiche (secteur NAF, taille, ville) : preuve qu'on ne fait pas d'envoi de masse.
3. **Le problème** dans leur métier + **l'obligation** : depuis le 2 février 2025, l'article 4 de l'IA Act demande aux entreprises qui utilisent l'IA de former leurs équipes (maîtrise de l'IA).
4. **L'offre YEBA** en 2 lignes, adaptée à la colonne « Offre à pousser ».
5. **Preuves** : Qualiopi n° 25FOR02027.1 (catégorie actions de formation), NDA 04973676397, certifications d'Aurélien utiles au sujet. Prise en charge possible par leur OPCO (« OPCO probable » de la fiche, à confirmer).
6. **Un seul appel à l'action** : 20 minutes d'échange (lien Calendly de CONFIG SYSTEME s'il est rempli, sinon téléphone).
7. Signature : Aurélien LUMEKA, Directeur — YEBA FORMATIONS · 0693 32 24 45 · SIRET 814 622 262 00032.
8. **Pied légal obligatoire** (LCEN art. 20 + RGPD art. 14) :
   > Vous recevez ce message car votre activité correspond à nos formations professionnelles. Vos coordonnées professionnelles proviennent de <source>. Responsable : YEBA FORMATIONS (EI), 9 rue Françoise Châtelain, 97490 Sainte-Clotilde. Base légale : intérêt légitime (RGPD art. 6.1.f). Conservation : 3 ans après le dernier contact. Vous pouvez demander l'accès, la rectification ou l'effacement, ou vous opposer à tout moment en répondant **STOP** ; réclamation possible auprès de la CNIL (cnil.fr).

Relance J+7 : 60 mots, une nouvelle information utile (un exemple concret de leur secteur), même pied légal. Une seule relance ; pas de réponse après la relance → statut « Pas intéressé », plus aucun envoi.

## 5. Pièces à joindre : des LIENS, pas des fichiers

Leçon du 19/11/2026 : un mail de 26 Mo à la mairie de Saint-Denis a été rejeté (limite Gmail 25 Mo). Toujours des liens :
- catalogue (CONFIG SYSTEME « Lien catalogue (prospection) ») ;
- carte de visite numérique (CONFIG SYSTEME « Lien carte de visite (vCard) ») ;
- fiche offre IA d'une page en PDF léger (< 2 Mo), si elle existe.
Valeur vide dans CONFIG SYSTEME → l'écrire dans « Pièces à joindre » comme « à fournir par Aurélien », ne jamais inventer d'URL.

## 6. Écriture

1. Mettre à jour la ligne PROSPECTION : fiche, objet, mail, relance, pièces, « Contrôle légal » (liste cochée des points 2 à 4), « Préparé le », statut « Prêt à envoyer ».
2. Créer un **brouillon** Gmail (jamais d'envoi sans le « oui » d'Aurélien dans la conversation) ; coller le lien dans « Brouillon Gmail ».
3. JOURNAL DES PREUVES : une ligne « Prospection préparée — <entreprise> », section Prospection, volet RGPD, lien de la fiche annuaire-entreprises.
4. Réponse « STOP » reçue → ligne dans « Oppositions STOP » (e-mail, domaine, date, motif) **et** statut STOP. Délai légal pour traiter une opposition : sans délai (art. 21 RGPD).

## 7. Réflexe conformité à signaler à chaque usage

- **RGPD** : fichier prospects = traitement à inscrire au registre (art. 30), finalité « prospection B2B », durée 3 ans.
- **Transfert hors UE** : Airtable et Gmail sont hébergés aux États-Unis (cadre EU-US Data Privacy Framework, RGPD chap. V) ; ne stocker que des données professionnelles nécessaires. Alternative UE déjà prévue dans le dépôt : Baserow (Pays-Bas). Envoi en nombre : Brevo (France) gère seul les désinscriptions.
- **IA Act** : rédiger un mail avec l'IA n'est pas un système à haut risque ; aucun scoring automatique de prospects sans validation humaine.

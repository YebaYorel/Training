# Journal des corrections — base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) »

23/09/2026 — corrections demandées par Aurélien LUMEKA. Aucune donnée personnelle n'a été lue ; seules des données ont été **effacées** (minimisation).

## 1. TVA et tarifs
- **A-04 (devis + convention)** : la phrase « YEBA FORMATIONS est titulaire de l'attestation prévue à l'art. 261-4-4° a » (fausse) est remplacée par « TVA non applicable — article 293 B du code général des impôts ». Automatisation toujours **désactivée** : à réactiver par le dirigeant.
- A-01 et A-03 vérifiées : aucune mention de TVA erronée.
- Catalogue : descriptions de « Tarif inter », « Tarif intra » et « Barème tarifaire » réécrites (anciens barèmes 390 / 425 / 490 € et 1 400 / 1 300 / 1 500 € retirés, TVA 293 B).
- CONFIG « N° TVA intracommunautaire » : phrase erronée « formation exonérée / conseil à TVA » corrigée.
- ⚠️ **Incohérence de prix à trancher** : la grille « validée le 22/09 » (CONFIG) et les fiches du catalogue ne donnent pas les mêmes montants (ex. ALLUMAGE 350 € contre 790 €).

## 2. Qualiopi — référentiel V10 (décret n° 2026-728, audits au 01/11/2026)
- Indicateur **33** créé (spécifique CFA → non applicable).
- Indicateurs modifiés annotés : 1, 2, 3, 7, 9 (ou 30, selon les sources), 12, 14, 15, 19, 20, 27, 32.
- **Libellés réalignés** : les lignes 3, 7, 10, 11, 12, 14, 15, 16, 26, 27, 28 portaient le texte d'un autre indicateur.
- Passés « Non applicable » avec justification : 3, 7, 14, 15, 16, 20, 28, 33 (13 et 29 l'étaient déjà).
- Libellés marqués « Synthèse — texte exact à reprendre du décret » : à remplacer par le texte Légifrance.

## 3. Charte IA (YEBA-DOC-11) → version 1.1
- Règlement (UE) 2026/1744 intégré : art. 4 réécrit (« prendre des mesures pour favoriser »), annexe III reportée au 02/12/2027, règle « aucune évaluation par IA » maintenue.
- Interdiction écrite des arguments « formation obligatoire » / « garantit la conformité ».

## 4. Offre IA → 2 formations
- **ALLUMAGE-TURBO** (FOR-0011, 3 jours / 24 h) : fusion, 12 objectifs SMART en 3 blocs, entretien de cadrage, classe virtuelle J+30, dossier de preuve pour l'entreprise. Prix provisoire = somme des fiches (1 680 € inter / 4 380 € intra) **à valider**.
- **PILOTE AUTOMATIQUE** (FOR-0013, 2 jours / 16 h) : renforcée (revue de mise en production J+30, kit de gouvernance des agents).
- **Supprimées** : TURBO seule (ex-FOR-0012) et PASSEPORT IA PÉI (ex-FOR-0016). Aucune session ni aucun devis n'y était rattaché. Les supports de TURBO sont rattachés à ALLUMAGE-TURBO. La ressource « règlement d'épreuve PASSEPORT IA PÉI » reste orpheline dans RESSOURCES PÉDAGOGIQUES.
- « AI Act, art. 4 » retiré de tous les intitulés.

## 5. RGPD stagiaires
- « Consentement RGPD donné » → **« Information RGPD remise (art. 13) »** (base légale : contrat + obligation légale). Champs liés renommés, formule « 🧭 Contrôle dossier stagiaire » corrigée.
- « Situation de handicap (RQTH) » → **« Besoin d'aménagement (oui/non) »** ; « Déclaration handicap » → « Questionnaire besoins d'aménagement ».
- **Données effacées** pour les 16 stagiaires, champs préfixés « 🗑️ À SUPPRIMER » : Nationalité, Lieu de naissance, N° CPF, Photo, Field 47, Type de handicap, Document RQTH. L'API ne permet pas de supprimer un champ : **suppression manuelle** (clic droit → Supprimer le champ).

## 6. Obligations légales (CONFIG SYSTEME)
- Médiateur : recommandation **CM2C** (alternatives MEDICYS, AME Conso) + procédure. À signer par le dirigeant.
- Forme juridique / capital / RCS : non renseignés (registre inaccessible depuis l'outil) ; point d'expert ajouté sur l'entreprise individuelle (mention « EI », pas de capital, RNE au lieu du RCS).
- Hébergeur : OVHcloud proposé ; alerte sur un site « YEBA Formations Portal » hébergé sur blink.new.
- Gmail → Brevo : étapes de migration décrites.
- RC Pro : en attente du contrat.

## 7. Passeport Formateur Conforme (prototype)
- Tables créées : « PASSEPORT FORMATEUR — PIÈCES », « PASSEPORT — AUTORISATIONS DE PARTAGE ».
- Fiche formateur : « 🛂 Passeport — nb pièces valides ». Un premier compteur erroné a été renommé « 🗑️ À SUPPRIMER ».

## Champs à supprimer à la main dans Airtable (8)
APPRENANTS : les 7 champs « 🗑️ À SUPPRIMER — … » · FORMATEURS & PRESTATAIRES : « 🗑️ À SUPPRIMER — ancien compteur passeport (erroné) ».

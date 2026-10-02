---
name: echeancier-abonnements
description: Calcule l'échéancier des abonnements et charges récurrentes et le prévisionnel des règlements du mois suivant, à partir de la table CHARGES & ABONNEMENTS d'Airtable. À utiliser pour « mes abonnements », « qu'est-ce qui sera prélevé », « prévisionnel du mois prochain ».
---

# Échéancier des abonnements

1. Lire la table **CHARGES & ABONNEMENTS** (`tblU5DphvZLflSiGg`) de la base `appQ2zqc80kkc6MR1` avec
   le connecteur Airtable (champs : Nom du service, Catégorie, Coût, Fréquence, Prochain
   renouvellement, Statut).
2. Écrire les lignes dans un fichier JSON temporaire du répertoire de travail temporaire
   (liste d'objets aux noms de champs Airtable ; les dates au format AAAA-MM-JJ).
3. Lancer : `python assistant/outils/echeancier.py <fichier.json>` (mois prochain par défaut),
   ou `--mois AAAA-MM --sur 3` pour un prévisionnel sur 3 mois.
4. Restituer : liste datée des prélèvements, total par mois, total à provisionner, puis les lignes
   ignorées (coût ou date manquants) à compléter.
5. Proposer (sans l'exécuter) la mise à jour du champ « Prochain renouvellement » des lignes échues,
   et attendre « je confirme ».

Si la table est vide : le dire et proposer à Aurélien de dicter ses abonnements (service, coût,
fréquence, date du prochain prélèvement) pour les enregistrer après confirmation.

Conformité : pas de donnée personnelle dans cette table (ni RGPD, ni IA Act). Ne jamais y saisir
de numéro de carte ou d'IBAN.

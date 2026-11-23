# Ajouts au Pilotage YEBA FORMATIONS

Pilotage vit dans un Artifact claude.ai (https://claude.ai/artifact/G5GzUwhVYpqS1uFmsjvGsF), relié à Airtable.
Ce dossier garde la source des modules greffés, pour relecture et historique.

- `prospection-ao.js` (2026-11-22, version 8 de l'Artifact) : règles permanentes de prospection (métier + STOP/STP,
  expéditeur yebaformations@gmail.com, brouillons seulement), liste STOP (table `Oppositions STOP`),
  veille BOAMP et suivi des appels d'offres (table `Appels d'offres`, décision GO / NO-GO d'Aurélien, commande Remporte).
  Greffé dans le menu Clients (onglets Prospection, Appels d'offres, Liste STOP).
- `missions-contrats.js` (2026-11-23, version 9) : écran « Missions & contrats » (menu Formations) et bloc
  « Missions : à faire » sur Aujourd'hui. Contrats reçus (Gmail, PDF, Word, liens de signature) lus par Claude puis
  validés ; ajout manuel (jury, formation sans contrat…) ; facture du mois datée du dernier jour (heure, jour ou
  forfait, jours non réalisés exclus, jamais en double) ; décorticage (Atelier pédagogique) ; progression et déroulé
  de chaque jour (.docx, horaires et pauses saisis, jamais supposés) ; suggestions de règles et de Claude.
  Table Airtable « MISSIONS & CONTRATS » (`tbl1gThEYdf0xZAaV`).
- `factures-carnet-decorticage.js` (2026-11-23, version 10) : « Voir / modifier » sur chaque devis et facture
  (aperçu exact du PDF, modification des brouillons seulement : une facture émise se corrige par avoir) ;
  confirmation du destinataire avant TOUT brouillon Gmail, avec carnet d'adresses mémorisé dans le coffre chiffré
  (adresse personnelle et liste STOP refusées) ; « Décortiquer sans dates » (REAC via le moteur de Pilotage, syllabus
  via Claude) : progression et séances, sans dates ni contenu de cours, export Word.

# Pilotage YEBA FORMATIONS (version web)

Logiciel personnel en un seul fichier HTML : `web/pilotage/dist/Pilotage.html`
(ouvrir dans Chrome, Edge, Firefox ou Safari ; PC ou Mac). Reconstruire :

    python web/pilotage/construire.py

## Ce qu'il fait
- **Formations** : dépôt REAC + RE/RC + fiche RNCP → décorticage, planning sur les jours cochés
  (ex. mardi seul = 1 jour/semaine), alternance (CCEE), fermetures. Le planning est une hypothèse :
  il se recale à chaque séance notée (fait / à moitié / pas fait).
- **Séance** : à la fin du cours, « Enregistrer la séance réalisée » prépare la séance suivante :
  diaporama (.pptx), exercices, l'essentiel de la journée, grille critériée (5 objectifs),
  quiz 10 questions (formateur), fiche de séance (preuve). Rédaction par Claude dans claude.ai,
  version de base sans Claude ailleurs.
- **Actions** : client, stagiaires, prix, TVA, facture → convention ou contrat, convocation,
  règlement, émargements, attestations, certificat de réalisation, facture, questionnaires…
  Pièces signées classées et chiffrées.
- **Qualiopi** : 32 indicateurs (+ ajouts), preuves automatiques, registres, dossier d'audit.
- **Finances** : trésorerie 90 jours, BFR, import du relevé CSV avec rapprochement des factures,
  tableau comptable, préparation du BPF (Cerfa 10443, avant le 31 mai).
- **Partenaires** : entreprises, France Travail, Missions Locales, OPCO ; relances et modèles d'e-mail.

## Données
Chiffrées (AES-GCM 256, PBKDF2 310 000 itérations) dans le navigateur (IndexedDB). Rien sur un serveur.
Sauvegarde chiffrée : Réglages → Télécharger une sauvegarde ; restauration depuis l'écran de connexion.
Mot de passe perdu = données illisibles.

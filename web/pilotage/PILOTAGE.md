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
- **Qualiopi V10** (décret n° 2026-728, audits à partir du 01/11/2026) : 33 indicateurs, modifications V10
  signalées (texte exact à confirmer sur Légifrance), bibliothèque documentaire (dépôt chiffré unique,
  réutilisé dans les actions et le dossier d'audit), modèles générés (méthode de calcul des résultats,
  registre des risques, plan de compétences…), registres, dossier d'audit.
- **Marque blanche** : action « pour un autre centre » → aucun nom, SIRET, NDA ni n° Qualiopi YEBA sur les
  documents stagiaires ; seule la facture au donneur d'ordre porte l'identité YEBA.
- **Finances** : tableau de bord « ce que j'ai / ce qu'on me doit / dont en retard / ce qu'il me restera ».
  Chaque action produit ses sommes attendues (part financeur OPCO, France Travail… et reste à charge).
  Import du relevé CSV ou OFX : chaque virement reçoit des propositions (montant, ressemblance du nom,
  n° de facture) que vous confirmez ; le logiciel retient l'association. Paiement noté à la main reconnu
  ensuite dans le relevé (pas de double comptage). TVA : franchise (art. 293 B du CGI) jusqu'au 31/01/2027,
  8,5 % ensuite. Trésorerie 90 jours, BFR, tableau comptable, préparation du BPF (avant le 31 mai).
- **Partenaires** : entreprises, France Travail, Missions Locales, OPCO ; relances et modèles d'e-mail.

## Données
Chiffrées (AES-GCM 256, PBKDF2 310 000 itérations) dans le navigateur (IndexedDB). Rien sur un serveur.
Sauvegarde chiffrée : Réglages → Télécharger une sauvegarde ; restauration depuis l'écran de connexion.
Mot de passe perdu = données illisibles.

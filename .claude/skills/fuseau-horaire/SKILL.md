---
name: fuseau-horaire
description: Convertit une heure entre La Réunion et le fuseau d'un interlocuteur (heure d'été comprise) et rédige l'heure double pour une invitation. À utiliser dès qu'un rendez-vous implique quelqu'un hors de La Réunion (métropole, Maurice, Mayotte, Canada…).
---

# Fuseaux horaires

- La Réunion : `Indian/Reunion`, UTC+4 toute l'année. L'écart avec Paris est de **3 h en heure
  d'hiver** (fin octobre → fin mars) et de **2 h en heure d'été**.
- Ne jamais calculer de tête : lancer
  `python assistant/outils/fuseau.py AAAA-MM-JJ HH:MM <fuseau|raccourci>` (heure de La Réunion
  vers l'interlocuteur) ou ajouter `--depuis` si l'heure donnée est celle de l'interlocuteur.
  Raccourcis : `python assistant/outils/fuseau.py --liste`.
- Déterminer le fuseau de l'interlocuteur à partir de sa signature, de son adresse ou de l'indicatif
  téléphonique ; en cas de doute, **demander**.
- Formulation pour une invitation : « 14h00, heure de La Réunion — 11h00 à Paris ».
- Dans Google Agenda, créer l'événement avec le fuseau `Indian/Reunion` (après confirmation).

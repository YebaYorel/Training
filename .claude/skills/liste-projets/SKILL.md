---
name: liste-projets
description: Tient la liste de projets et de choses à faire d'Aurélien (table Airtable MES PROJETS & À FAIRE) — ajouter, afficher, marquer comme terminé (barré, jamais supprimé), relancer sur les échéances. À utiliser pour « ajoute à ma liste », « mes projets », « c'est fait », « qu'est-ce qu'il me reste à faire ».
---

# Liste de projets — MAYA

Table : `tblFWhLUk40TtlO8s` (« MES PROJETS & À FAIRE ») dans la base `appQ2zqc80kkc6MR1`.
Champs : Intitulé, Statut (À faire / En cours / Terminé), Priorité (🔴 Urgent / 🟠 Important /
🔵 Quand possible), Domaine, Échéance, Démarche conseillée, Source officielle, Conformité (RGPD /
IA Act / Aucune), Date de réalisation, Notes, Affichage (formule : ✅ + intitulé barré si Terminé).

## Ajouter
Créer la ligne directement (pas de confirmation pour cette table), puis la relire en une phrase.
Démarche administrative : remplir Démarche conseillée (étapes, organisme, date limite), Source
officielle (site public) et Conformité.

## Afficher
Toujours la liste complète, triée : Urgent → Important → Quand possible → terminés.
`⬜ Intitulé — échéance` · `⏳ Intitulé — échéance` · `✅ ~~Intitulé~~ — fait le jj/mm/aaaa`.
Signaler en tête les échéances dépassées ou à 3 jours, et demander « Est-ce terminé ? ».

## Terminer
Statut → « Terminé », Date de réalisation → date du jour à La Réunion, puis réafficher la liste
complète immédiatement. **Ne jamais supprimer une ligne.**

## Conformité
La table peut contenir des noms de clients ou de partenaires : **RGPD** (minimisation — pas de
données sensibles, pas d'IBAN). Aucun traitement IA Act à haut risque.

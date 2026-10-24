# Missions locales de La Réunion (Nord, Est, Ouest, Sud)

> **Décideur identifié** : Directions (non identifiées) [À VÉRIFIER] — Directeurs et présidents  
> **Fiabilité de l'information** : —  
> Tout ce qui est marqué [À VÉRIFIER] doit être confirmé (appel au standard) avant l'envoi.

---

## 1. Le courriel (prêt à envoyer)

**À :** Mission locale Nord : 6 bis av. Desbassyns, BP 30339, 97494 Sainte-Clotilde Cedex [À VÉRIFIER]  
**Objet :** Rendre du temps à vos conseillers malgré la baisse des crédits — formation financée par Uniformation  
**Pièces jointes :** CV d'Aurélien LUMEKA · Note de proposition (parties 2 à 8 de ce mémo, en PDF)

> Madame, Monsieur le Directeur,  
>
> Vos élus l'ont exprimé à Bras-Panon le 15 octobre : les crédits de l'État baissent encore dans le projet de loi de finances 2027, après un recul d'environ 15 % en 2025 et 2026 — alors que les Missions locales de La Réunion ont accompagné 28 153 jeunes en 2025, dont 14 769 vers un emploi, une formation, une alternance ou une immersion.  
>
> Je ne viens pas vous demander de budget. Je vous propose deux actions financées en dehors de vos crédits d'accompagnement :  
>
> • « Conseiller augmenté » (2 jours par Mission locale) : former vos conseillers à l'IA pour alléger les comptes rendus, la préparation des entretiens et la prospection d'entreprises — sans jamais saisir de données de jeunes dans un outil non maîtrisé. Cette formation relève du plan de développement des compétences de vos salariés, financé par votre OPCO, Uniformation ;  
> • des modules courts pour les jeunes (« décrocher son premier job », « l'IA pour son CV », savoir-être professionnel), mobilisables avec les financeurs de la formation des jeunes.  
>
> Formateur en soft skills, vente et management, Référent handicap, YEBA FORMATIONS est certifié Qualiopi ; je me consacre depuis 2026 à l'IA appliquée et à la protection des données.  
>
> Pourrions-nous en parler 20 minutes le [date 1] ou le [date 2] ? Mon CV et une note sont joints.  
>
> Je vous prie d'agréer l'expression de mes salutations distinguées.  
>
> Aurélien LUMEKA  
> Directeur — YEBA FORMATIONS  
> Organisme de formation certifié Qualiopi (n° 25FOR02027.1) — NDA 04973676397 — SIRET 814 622 262 00032  
> [Téléphone] · [Adresse email] · [Site internet]  

*Vos coordonnées professionnelles proviennent de sources publiques. Elles sont traitées par YEBA FORMATIONS, sur la base de son intérêt légitime, pour vous présenter son offre, et conservées 3 ans après notre dernier échange. Vous pouvez vous y opposer à tout moment en répondant « STOP », et exercer vos droits d'accès, de rectification et d'effacement à [adresse email] ; vous pouvez aussi saisir la CNIL.*

---

## 2. Ce que vit la structure (constat chiffré)

- 28 153 jeunes accompagnés en 2025, 14 769 sorties positives.
- Crédits d'État -15 % environ en 2025-2026, nouvelle baisse au PLF 2027.
- Séminaire des élus des Missions locales Réunion-Mayotte le 15/10/2026.

## 3. Comment je vous aide — expliqué simplement

*(comme à un enfant de 5 ans)*

> Les conseillers des Missions locales aident les jeunes à trouver leur chemin. Mais ils passent beaucoup de temps à écrire des papiers, et moins de temps avec les jeunes. Moi, je leur apprends à se servir d'un robot qui écrit les papiers à leur place, sans jamais lui donner les secrets des jeunes. Comme ça, ils ont plus de temps pour aider. Et j'apprends aux jeunes à préparer leur premier travail.

## 4. Les IA et outils utilisés

| Outil | Éditeur, pays | Payant ? | Prix indicatif | Pourquoi ici |
|---|---|---|---|---|
| Le Chat Pro / Team (« Vibe » [À VÉRIFIER]) | Mistral AI, France | Oui | Pro ≈ 14,99 $/mois ; Team ≈ 24,99 $/utilisateur/mois [À VÉRIFIER] | Outil des conseillers (offre Team, données non utilisées pour l'entraînement) |
| faster-whisper (transcription locale) | Open source | Non | Gratuit (tourne sur le serveur) | Comptes rendus de réunions d'équipe |
| API Mistral (La Plateforme) | Mistral AI, France | Oui, à l'usage | Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens (source tierce, à vérifier) | Prospection d'entreprises assistée |

Les prix sont ceux d'octobre 2026, à reconfirmer avant devis. Aucun outil américain n'est utilisé pour traiter des données : souveraineté européenne.

## 5. Les solutions mises en place

Chaque solution est détaillée pas à pas (recette reproductible en entreprise, consigne donnée à l'IA, points RGPD / IA Act) dans `00-catalogue-ia-et-solutions.md`.

- **S2 — Comptes rendus de réunion automatiques** : Comptes rendus des réunions d'équipe et des comités.
- **S10 — Prospection commerciale assistée** : Prospection d'entreprises partenaires.
- **S7 — Kit conformité RGPD & IA Act** : Charte : ce qu'un conseiller ne saisit jamais dans une IA.
- **S8 — Accessibilité et FALC** : Supports FALC pour les jeunes.

## 6. Déroulé de la mission

| Période | Ce qui se passe | Livrable |
|---|---|---|
| Mois 1 | Diagnostic des tâches chronophages | Liste |
| Mois 2-5 | 4 × 2 jours (une session par Mission locale) | Conseillers formés |
| Mois 6 | Mesure avant / après | Temps gagné |

## 7. Indicateurs de résultat

- Temps administratif gagné par conseiller (déclaratif, avant / après)
- Charte adoptée
- Satisfaction

## 8. RGPD et IA Act

- **RGPD** : Données de jeunes, parfois mineurs : interdiction de les saisir dans un outil non validé ; charte.
- **IA Act** : Art. 4 : la formation documente les mesures de maîtrise de l'IA.

---

## 9. Mise en place technique — ordre d'exécution *(pour Aurélien, ne pas transmettre)*

Installation de la plateforme : `00-guide-installation-plateforme.md` (étapes 0 à 20). Spécifique à cette structure :

1. Vérifier avec Uniformation les critères de prise en charge.
2. Kit de consignes (prompts) validées pour conseillers.
3. Démonstration A1 (comptes rendus) sur votre plateforme.

## 10. Questions à poser au rendez-vous

- Quelles tâches prennent le plus de temps à vos conseillers ?
- Utilisez-vous déjà des outils d'IA ?

## 11. Risques et parades

| Risque | Parade |
|---|---|
| Sujet budgétaire sensible | Ne parler que de financements hors enveloppe d'accompagnement |

## Sources

- outremers360.com (15/10/2026)
- banquedesterritoires.fr
- Détail des URL : onglet « Preuves » du classeur `Prospection_Acteurs_Formation_Reunion.xlsx`.

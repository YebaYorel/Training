---
title: "Feuille 1 — Oral de 20 minutes : NEOBATI (Airtable + Make + IA)"
---

**Candidat** : Aurélien LUMEKA — freelance spécialisé en automatisation No-Code, mandaté par **Atelier NéoBâti** (Nantes, fondé en 2015 par **Paul Durieux**).
**Titre visé** : Product Builder No-Code — RNCP 39108, niveau 6 (Bac+3/4). *Source : brochure École Cube, p. 4, 6 et 26.*

> **Règle d'or** : chaque phrase technique est suivie de sa traduction simple (« pour ma mère »).

## 1. Déroulé minuté

| Min. | Séquence | Ce que je montre à l'écran |
|---|---|---|
| 0–1 | Présentation + mission | Titre du projet |
| 1–3 | Le problème de NéoBâti | Brief de Paul Durieux |
| 3–8 | **Airtable** : base, calculs, vues, interfaces, formulaires | Base « NEOBATI – Gestion des chantiers (v2 examen) » |
| 8–14 | **Make** : 6 scénarios + gestion d'erreurs | Schéma des scénarios (feuille 6) |
| 14–16 | **IA** : résumé terrain + relances | Rapport C2 avant / après |
| 16–18 | Sécurité, RGPD, IA Act, coûts | Chiffres clés ci-dessous |
| 18–20 | Bilan, limites, évolutions | Encadré « limites » |

*Si les 20 minutes incluent les questions : 12 min de présentation (garder les séquences 2, 3, 4) + 8 min de questions.*

## 2. Le texte, séquence par séquence

**① Le problème (1–3 min)**

- *Technique* : « Les données de NéoBâti sont **silotées** : devis et factures sous Excel, plannings dans Google Calendar, photos par SMS/WhatsApp, relances par emails isolés. Il n'y a **pas de source unique de vérité**, donc pas de pilotage en temps réel ni de calcul de marge par chantier. »
- *Simple* : « Les infos sont rangées dans six tiroirs différents. Personne ne sait où est la bonne version, et le patron ne sait pas si un chantier lui fait gagner ou perdre de l'argent. »

**② Airtable — la base (3–8 min)**

- *Technique* : « J'ai modélisé une **base relationnelle de 12 tables** : les **6 tables du sujet** (Clients, Devis, Chantiers, Étapes, Ressources, Factures), **2 tables de coûts** (Pointages, Achats) indispensables aux formules de l'annexe, **2 tables de saisie** alimentées par formulaires (Demandes, Rapports terrain) et **2 tables de traçabilité** (Interactions, Logs erreurs). CHANTIERS est la **table pivot** : relations **1-N** vers devis, factures, coûts et étapes. Les indicateurs sont calculés par **rollups** (agrégations) et **formules**. »
- *Simple* : « C'est un grand classeur intelligent : chaque fiche chantier est reliée à son client, ses devis, ses factures et ses heures. Les calculs se font tout seuls, comme une calculatrice branchée sur les bonnes cases. »
- **Démonstration chiffrée (chantier C1, exemple de l'annexe)** :
  - Main-d'œuvre : 20 h menuisier × 45 € = **900 €** ; 15 h peintre × 40 € = **600 €** → **1 500 €**
  - Achats : fournitures **800 €** + électricien sous-traitant **1 200 €** → **2 000 €**
  - Coût total = 1 500 + 2 000 = **3 500 €**
  - Devis signé = CA facturé = **5 000 € HT** → marge brute = 5 000 − 3 500 = **1 500 €** → taux de marge = 1 500 ÷ 5 000 = **30 %**
  - Trésorerie nette chantier = acompte perçu 1 500 − (MO 1 500 + achats payés 800) = **− 800 €** → « l'entreprise a avancé 800 € de sa poche ».
- *Vues et interfaces* : 2 interfaces cloisonnées : « NEOBATI – Pilotage » (pages **Direction** et **Administratif**) et « NEOBATI – Terrain (artisans) », pour que les artisans ne voient jamais les marges, + 2 **formulaires** (Nouvelle demande client, Rapport terrain mobile).
- *Simple* : « Chacun a son écran : le patron voit l'argent et les retards, l'assistante voit les factures, les artisans voient seulement leurs tâches sur le téléphone. »

**③ Make — les automatisations (8–14 min)**

- *Technique* : « 6 **scénarios** + 1 **gestionnaire d'erreurs**. Les événements terrain arrivent par **webhook instantané** (Airtable déclenche Make), les relances tournent en **planification quotidienne** à 8 h les jours ouvrés. Des **filtres** stoppent tôt les bundles inutiles, un **agrégateur de texte** envoie **un seul** email de synthèse au lieu de N alertes. »
- *Simple* : « Make, c'est un facteur automatique : dès qu'un artisan envoie son rapport, le facteur part tout de suite ; pour les relances, il fait sa tournée une fois par matin. »
- Les 6 scénarios : **S1** nouvelle demande → fiche client + accusé de réception ; **S2** rapport terrain → résumé IA + mise à jour avancement + alerte si problème ; **S3** relance devis (J-5 avant expiration, 2 relances max) ; **S4** relance factures (3 niveaux : 1–15 j courtoise, 16–30 j ferme, > 30 j escalade humaine) ; **S5** synthèse direction (retards, dépassements, acomptes non reçus) ; **S6** notification d'affectation aux artisans ; **S0** journal d'erreurs.
- **Optimisation** : estimation **≈ 620 opérations / mois** avec webhooks, contre **≈ 9 260** si les 3 scénarios événementiels interrogeaient Airtable toutes les 15 min (3 × 2 880 = 8 640 vérifications à vide).
- *Simple* : « Au lieu d'aller voir la boîte aux lettres toutes les 15 minutes pour rien, on attend que la sonnette sonne. On paie 15 fois moins de déplacements. »

**④ IA (14–16 min)**

- *Technique* : « J'utilise un **LLM** (Mistral AI, éditeur français) via un module Make, avec un **prompt système** cadré, une **température basse** (0,2) et la consigne de ne rien inventer. Je n'envoie au modèle que les données **strictement nécessaires** (minimisation). Les relances de niveau 3 ne partent jamais sans **validation humaine**. »
- *Simple* : « L'IA est un secrétaire qui met au propre les notes griffonnées des artisans et prépare des lettres polies. Mais pour les cas délicats, c'est Paul qui signe. »
- Démo : notes brutes du rapport C2 (« plaques de plâtre abîmées… l'électricien ne peut pas commencer… ») → résumé en 3 phrases + 3 points de suivi.

**⑤ Sécurité, RGPD, IA Act, coûts (16–18 min)** — voir feuilles 2 et 5.

- « Comptes **au nom du client**, **double authentification**, **jeton d'accès Airtable restreint** à une seule base, **jeton secret** sur les webhooks, journal des erreurs. »
- « **RGPD** : Airtable (États-Unis) et Make sont des **sous-traitants** (art. 28) : DPA à signer, données minimales, durées de conservation (prospect 3 ans, factures 10 ans). **IA Act** : usage à **risque limité** (rédaction de textes), pas de notation des artisans par IA (ce serait du haut risque, annexe III). »

**⑥ Bilan (18–20 min)**

- Gain de temps estimé : **≈ 13 h 40 / mois** (hypothèses ci-dessous), relances systématiques, marges visibles par chantier.
- *Simple* : « On rend presque deux journées de travail par mois à l'équipe, et plus aucune facture n'est oubliée. »

## 3. Chiffres clés à retenir (cohérents avec la base de démonstration)

| Indicateur | Valeur | Calcul |
|---|---|---|
| Effectif | **9 permanents** | 1 dirigeant + 1 assistante + 1 chargé d'affaires + 3 binômes (6 artisans) |
| Tables | **12** | 6 sujet + 2 coûts + 2 saisie + 2 traçabilité |
| Chantiers de démo | **5** | 2 terminés, 2 en cours, 1 en attente |
| CA facturé total | **17 200 € HT** | 1 500 + 3 000 + 3 600 + 2 400 + 3 500 + 3 200 |
| Encaissé | **6 900 € HT** | 1 500 + 3 000 + 2 400 |
| Reste dû par les clients | **10 300 € HT** | 17 200 − 6 900 |
| Marge moyenne (chantiers terminés) | **1 125 €** | (1 500 + 750) ÷ 2 |
| Chantiers déficitaires (terminés) | **0 sur 2** | — |
| Répartition des coûts | **MO 50,4 % / achats 49,6 %** | 10 600 € / 10 450 € sur 21 050 € |
| C4 cuisine | **dépassement de 400 €** | coût 8 400 € > devis 8 000 € |
| Opérations Make | **≈ 620 / mois** | détail feuille 6 |
| Gain de temps | **≈ 13 h 40 / mois** | 200 + 300 + 240 + 80 = 820 min |

*Hypothèses du gain de temps (à valider avec Paul Durieux)* : 20 relances × 10 min = 200 min ; 60 rapports terrain × 5 min de ressaisie = 300 min ; tableau de bord hebdomadaire 4 × 60 min = 240 min ; 8 fiches clients × 10 min = 80 min.

> ⚠️ Les retards se calculent avec la date du jour (`TODAY()`). Au 26/10/2026, C2 a **10 jours** de retard ; le jour de l'examen, le chiffre aura augmenté. Dire : « au moment de la démonstration ».

## 4. Limites assumées (montrent la maturité)

1. **Souveraineté** : Airtable héberge par défaut aux États-Unis (AWS US-East-1) ; la résidence UE (Francfort) n'existe qu'en offre Enterprise Scale. *Source : support.airtable.com, « European Data Residency FAQs ».* Alternative souveraine : Baserow (Pays-Bas) + n8n auto-hébergé.
2. **Formule de trésorerie de l'annexe** : elle n'utilise que les acomptes ; elle n'a de sens que **pendant** le chantier.
3. **Marge en cours de chantier** : provisoire (C2 affiche − 3 360 € car seul l'acompte est facturé). Je pilote les chantiers ouverts avec l'**écart budget** (devis − coût total).
4. Le sujet parle de « tâches » : chez Make on parle d'**opérations**, facturées en **crédits**.

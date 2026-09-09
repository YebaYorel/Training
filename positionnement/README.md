# Tests de positionnement — système complet

Dispositif de positionnement à l'entrée, de la conception du formulaire jusqu'à
la décision pédagogique, pour le catalogue de formations
(Airtable `appQ2zqc80kkc6MR1` → `CATALOGUE FORMATIONS`).

**Qualiopi indicateur 8** — positionnement et évaluation des acquis à l'entrée.

---

## Démarrage rapide

```bash
python3 positionnement/analyse/scoring.py --autotest
```

Puis, sur des réponses réelles :

```bash
python3 positionnement/analyse/scoring.py \
    --formation FOR-0001 \
    --reponses mes_reponses.json
```

---

## Ce que contient ce dossier

| Fichier | Contenu |
|---|---|
| [`00-ARCHITECTURE.md`](00-ARCHITECTURE.md) | **À lire en premier** — principe, blocs, calculs, tables Airtable à créer |
| [`formulaires/FOR-0001_IA-Generative.md`](formulaires/FOR-0001_IA-Generative.md) | Formulaire complet + corrigé + notes formateur |
| [`formulaires/FOR-0002_Automatisation.md`](formulaires/FOR-0002_Automatisation.md) | idem |
| [`formulaires/FOR-0003_RGPD-Cybersecurite.md`](formulaires/FOR-0003_RGPD-Cybersecurite.md) | idem |
| [`formulaires/FOR-0004_Vente-Initiation.md`](formulaires/FOR-0004_Vente-Initiation.md) | idem |
| [`formulaires/_GABARIT-NOUVELLE-FORMATION.md`](formulaires/_GABARIT-NOUVELLE-FORMATION.md) | Blocs communs + méthode pour les formations suivantes |
| [`analyse/referentiels.json`](analyse/referentiels.json) | Corrigés, domaines, poids horaires, seuils |
| [`analyse/scoring.py`](analyse/scoring.py) | Moteur — individuel, groupe, décisions, réallocation |
| [`analyse/modeles-de-synthese.md`](analyse/modeles-de-synthese.md) | Fiche individuelle, synthèse formateur, retour stagiaire |
| [`automatisations/A1-envoi-positionnement.md`](automatisations/A1-envoi-positionnement.md) | Envoi J-15, relance J-8, alerte J-4 + formules Airtable |
| [`automatisations/A2-ingestion-et-analyse.md`](automatisations/A2-ingestion-et-analyse.md) | Voie en ligne, voie papier (OCR), analyse, validation |
| [`conformite/RGPD-IA-ACT.md`](conformite/RGPD-IA-ACT.md) | **Obligatoire avant mise en service** |

---

## Le principe en trois phrases

1. **Une structure unique, N formations.** 5 blocs identiques partout ; seuls
   les items changent. Un seul moteur d'analyse, donc.
2. **On mesure ce que le stagiaire croit savoir ET ce qu'il sait.** L'écart
   entre les deux est l'information la plus exploitable en salle.
3. **La machine calcule, l'humain décide.** Aucune synthèse ne sort sans
   validation — c'est à la fois la garantie pédagogique et la frontière
   juridique (IA Act, annexe III point 3).

---

## Couverture du catalogue

| Réf | Formation | Statut |
|---|---|---|
| FOR-0001 | IA Générative | ✅ Complet |
| FOR-0002 | Automatisation | ✅ Complet — *durée à confirmer* |
| FOR-0003 | RGPD & Cybersécurité | ✅ Complet — *durée à confirmer* |
| FOR-0004 | Vente : Initiation à la vente | ✅ Complet |
| FOR-0005 | Management de proximité en institut | ⏸️ **Programme manquant** |
| FOR-0006 | Copilot | ⏸️ **Programme manquant** |
| FOR-0007 | Vente : excellence relation client en institut | ⏸️ **Programme manquant** |

Le champ `Programme détaillé` du catalogue est **vide sur les 7 formations**.
Les quatre premières ont été construites à partir de leurs **objectifs
pédagogiques**, qui sont formulés en capacités observables — c'est d'ailleurs
la bonne base pour un positionnement. Les trois dernières n'ont ni objectifs ni
programme renseignés.

---

## Avant la première mise en service

- [ ] Lire [`conformite/RGPD-IA-ACT.md`](conformite/RGPD-IA-ACT.md) en entier
- [ ] Supprimer les deux champs art. 9 dans `APPRENANTS` (et non les masquer)
- [ ] Créer les tables `POSITIONNEMENT — RÉPONSES` et `— SYNTHÈSE SESSION`
- [ ] Créer le rollup `Date début session` sur `INSCRIPTIONS`
- [ ] Créer les 3 formules + 2 cases à cocher (A1)
- [ ] Vérifier le libellé exact de l'option `Confirmée` dans `Statut Inscription`
- [ ] Créer la fiche de registre des traitements
- [ ] Rédiger la note d'analyse de risque IA Act (une page)
- [ ] Signer et archiver les DPA : Airtable, Tally, Mistral
- [ ] Tester A1 sur une session fictive **avant** de l'activer en production

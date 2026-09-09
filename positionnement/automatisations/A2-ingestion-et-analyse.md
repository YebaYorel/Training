# Automatisation A2 — Ingestion des réponses et production de l'analyse

Deux entrées, **un seul traitement**. C'est tout l'intérêt de l'architecture :
la voie papier et la voie numérique convergent sur le même JSON, donc sur le
même moteur, donc sur la même synthèse.

```
  VOIE 1 — numérique (90 % des cas visés)
  Formulaire en ligne ──webhook──┐
                                 │
  VOIE 2 — papier (secours)      ├──► JSON normalisé ──► scoring.py ──► synthèse
  Scan A4 ──► OCR structuré ─────┘                              │
                                                                ▼
                                                   ⛔ VALIDATION HUMAINE ⛔
                                                                │
                                                                ▼
                                              Airtable + PDF mallette formateur
```

---

## Voie 1 — Réponse en ligne

1. **Déclencheur :** webhook du formulaire (Tally) vers n8n.
2. **Normaliser** : construire le JSON attendu par `scoring.py`
   (`ref_inscription`, `auto`, `qcm`, `ouvertes`, `amenagement`).
3. **Écrire** une ligne dans `POSITIONNEMENT — RÉPONSES`
   (canal = En ligne, statut = Reçu, confiance = 100 %).
4. **Cocher** `Positionnement reçu` sur l'INSCRIPTION correspondante.
5. Passer à l'**analyse** (commune, plus bas).

> Le champ caché `ref_inscription` est pré-rempli par l'URL envoyée en A1
> (`?ref=INS-00042`). Sans lui, impossible de rattacher la réponse sans
> demander le nom — donc sans collecter une donnée qu'on n'a pas besoin de
> collecter deux fois.

---

## Voie 2 — Feuille A4 papier

C'est la partie que tu voulais automatiser. Elle est réalisable **parce que le
formulaire papier a été conçu pour ça** — pas l'inverse.

### Ce qui rend l'extraction fiable

| Choix de conception | Effet sur l'extraction |
|---|---|
| QR code portant `INS-xxxxx` | Identification **sans OCR** d'écriture manuscrite |
| Blocs B et C = **cases à cocher uniquement** | On lit des marques, pas des mots |
| Nombre d'items connu à l'avance (8 + 12) | Toute extraction ≠ 20 réponses est rejetée automatiquement |
| Modalités connues (0-3, puis a/b/c) | Toute valeur hors domaine est rejetée |
| Bloc D manuscrit **non scoré** | L'écriture libre ne pollue jamais le calcul |

L'écriture manuscrite ne sert donc qu'aux questions ouvertes, qui sont
transcrites « pour information » et signalées à relire. **Aucun score ne dépend
d'une lecture d'écriture.** C'est ce qui fait tomber le taux d'erreur exploitable
à un niveau acceptable.

### Chaîne technique

1. **Dépôt** : tu photographies ou scannes les feuilles (une PDF multi-pages
   suffit) et tu déposes le fichier dans le champ `Scan original` d'une ligne
   `POSITIONNEMENT — RÉPONSES`, ou dans un dossier surveillé.
2. **Découpe** : n8n sépare le PDF en pages — **une page = un stagiaire**.
3. **Lecture du QR** → `ref_inscription`. Échec de lecture ⇒ statut « À valider »
   et arrêt, sans deviner.
4. **Extraction structurée** : appel à **Mistral Document AI (OCR)** — France,
   hébergement européen — avec un **schéma de sortie imposé** :

```json
{
  "ref_inscription": "INS-00042",
  "auto": {"B1": 0, "B2": 3, "B3": 2, "B4": 1,
           "B5": 2, "B6": 3, "B7": 0, "B8": 1},
  "qcm": {"C1": "b", "C2": "c", "C3": "a", "C4": "b", "C5": "c", "C6": "a",
          "C7": "b", "C8": "c", "C9": "a", "C10": "c", "C11": "b", "C12": "a"},
  "ouvertes": {"D1": "...", "D2": "...", "D3": "..."},
  "amenagement": false,
  "confiance": 0.94,
  "cases_ambigues": ["B5"]
}
```

5. **Contrôles automatiques de rejet** (avant tout calcul) :
   - `auto` ne contient pas exactement 8 clés, ou une valeur hors `0-3`
   - `qcm` ne contient pas exactement 12 clés, ou une valeur hors `a/b/c`
   - une case du bloc B ou C porte **deux marques** ou **aucune**
   - `confiance < 0,90`

   Tout rejet ⇒ statut **« À valider »**, aucun score écrit. Rien n'est deviné.

6. **Écriture** dans `POSITIONNEMENT — RÉPONSES` (canal = Papier).
7. Passer à l'**analyse**.

### Coût réel — l'arbitrage à faire honnêtement

Mistral OCR est facturé environ **4 $ pour 1 000 pages** (2 $ en mode batch)
— soit **moins d'un centime par feuille**. Le coût de l'API est négligeable.

**Ce n'est pas là que se joue la rentabilité.** Le vrai coût, c'est la
construction et l'entretien du scénario n8n. Ordre de grandeur : une journée de
mise en place, puis de la maintenance à chaque changement de formulaire.

> ⚠️ **Arbitrage à trancher avec toi.** Ressaisir manuellement une feuille de
> 20 cases prend **1 à 2 minutes**. Si tu traites 8 stagiaires × 10 sessions par
> an, la voie papier représente environ **2 h 30 de saisie annuelle**. Une
> journée de développement ne se rembourse pas.
>
> **La voie 2 devient rentable au-delà d'environ 300 feuilles papier par an**
> — ou immédiatement si tes sessions en CFA se font massivement sur papier.
> **Il me manque ton volume annuel pour trancher** (question 6 en fin de
> réponse). En attendant, je recommande de **démarrer sur la voie 1 seule**,
> avec ressaisie manuelle du papier, et de n'automatiser la voie 2 qu'une fois
> le volume constaté. Concevoir maintenant, construire quand ça paie.

---

## Analyse (commune aux deux voies)

1. **Scorer l'individu** : `scoring.py` → scores auto/réel/calibration par
   domaine, niveau global.
2. **Écrire** les scores dans `POSITIONNEMENT — RÉPONSES`.
3. **Recalculer la synthèse de session** dès qu'une réponse arrive : moyennes,
   écarts-types, décisions APPUYER / AJUSTER / ALLÉGER / DIFFÉRENCIER,
   réallocation de temps.
4. **Écrire** dans `POSITIONNEMENT — SYNTHÈSE SESSION`, statut
   **« À valider »**.

### ⛔ Le point de contrôle humain — non négociable

**Aucune synthèse ne part au formateur sans que tu l'aies relue et fait passer
en « Validée ».** Ce n'est pas de la prudence décorative, c'est ce qui :

- **maintient le système hors du régime « haut risque »** de l'IA Act
  (annexe III, point 3 — voir `../conformite/RGPD-IA-ACT.md`) ;
- **te protège pédagogiquement** : une extraction fausse sur un stagiaire, et tu
  construis ta journée sur un profil qui n'existe pas ;
- **est ta preuve Qualiopi** : l'auditeur veut voir que le positionnement est
  *exploité par un humain*, pas seulement collecté.

Écran de validation : la synthèse à gauche, le scan ou les réponses brutes à
droite. Les lignes marquées « À valider » ou « incomplet » remontent en tête.

### Déclenchement de la synthèse finale

- **À J-2**, la synthèse validée est jointe automatiquement à l'e-mail
  **mallette formateur** que ton système envoie déjà
  (`Mallette due (J-2)`, `flds5ZM5d3o8G3IQX`). Un seul envoi, pas deux.
- Si la synthèse n'est **pas encore validée** à J-2 : la mallette part sans
  elle, **et** une ligne `ALERTES & TÂCHES` est créée. Jamais d'envoi
  automatique d'une synthèse non relue.

---

## Briques retenues, et pourquoi

| Besoin | Outil | Pays / hébergement | Pourquoi celui-là |
|---|---|---|---|
| Orchestration | **n8n** | Allemagne — **auto-hébergé** chez toi (OVHcloud, Scaleway, Clever Cloud) | Alternative à Make/Zapier (US). Auto-hébergé, aucune donnée ne sort de ton infrastructure. |
| Formulaire | **Tally** | Belgique, hébergement UE | Tu l'utilises déjà (champ `Lien formulaire` de ta table EVALUATIONS). Chiffrement en transit et au repos. **DPA à signer et à archiver.** |
| OCR structuré | **Mistral Document AI (OCR 4)** | France, datacenters européens | Le seul OCR de ce niveau soumis au droit européen. Sortie JSON schématisée. ~4 $/1 000 pages. |
| Base | **Airtable** | 🇺🇸 **États-Unis** | Ton existant. **Point faible du dispositif** — voir la critique en fin de réponse. |
| Base cible | **Baserow** | Pays-Bas | Déjà l'objet de ce dépôt. Le moteur y est portable sans réécriture. |

### Alternatives souveraines si tu veux aller plus loin

- **docTR** (Mindee, France) — OCR open source **auto-hébergeable** : zéro
  transfert, zéro coût à la page. Moins bon que Mistral sur les documents
  complexes, mais tes feuilles sont structurées et à format connu : c'est
  précisément le cas d'usage où il tient la route.
- **LimeSurvey** (Allemagne) ou **Yakforms** (France, associatif) —
  formulaires auto-hébergeables, si tu veux sortir de Tally.
- **Grist** — tableur-base auto-hébergeable, présent dans l'offre publique
  française ; alternative sérieuse à Airtable côté interface.
- **Paperless-ngx** — archivage indexé des scans, auto-hébergé.
- **Stirling PDF** — génération et fusion des PDF A4, auto-hébergé.

> ⚠️ **Infomaniak** (souvent cité comme « souverain ») est **suisse**, pas
> européen. Une décision d'adéquation rend le transfert licite, mais ce n'est
> pas de l'UE. À ne pas présenter comme tel à un client.

---

## Modes de panne à surveiller

| Panne | Détection | Conduite à tenir |
|---|---|---|
| QR illisible (pli, photo floue) | Aucun `ref_inscription` | Statut « À valider », rattachement manuel |
| Deux cases cochées sur un item | Contrôle de rejet | « À valider » — ne jamais choisir à la place du stagiaire |
| Stagiaire répond deux fois | `ref_inscription` déjà présent | Conserver la **première** réponse, archiver la seconde |
| Libellé `Statut Inscription` modifié dans Airtable | `Positionnement dû` reste « NON » partout | Vérifier chaque trimestre que la vue n'est pas vide à tort |
| Taux de réponse < 50 % à J-4 | Vue `Positionnement en souffrance` | Appels, puis passation papier en ouverture |
| n8n indisponible | Webhook perdu, **silencieusement** | Réconciliation quotidienne : comparer réponses reçues et `Positionnement envoyé` |

> La dernière ligne est la plus dangereuse : un webhook perdu ne produit aucune
> erreur visible. Prévoir un contrôle quotidien de cohérence, sinon tu
> découvriras le problème le matin de la formation.

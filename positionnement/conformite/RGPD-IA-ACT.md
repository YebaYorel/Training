# Conformité du dispositif de positionnement — RGPD & IA Act

À lire **avant** mise en service. Signalé spontanément, comme convenu.

---

## 1. IA Act — le point le plus important de ce dossier

### Ton dispositif est dans le périmètre de l'annexe III

L'**annexe III, point 3** du règlement (UE) 2024/1689 vise les systèmes d'IA
destinés à :

- déterminer l'**accès ou l'admission** à un organisme d'éducation ou de
  formation professionnelle ;
- **évaluer les acquis d'apprentissage**, y compris lorsque ces résultats
  servent à orienter le processus d'apprentissage ;
- **évaluer le niveau d'éducation approprié** qu'une personne recevra ou auquel
  elle pourra accéder.

*(source : [artificialintelligenceact.eu — annexe III](https://artificialintelligenceact.eu/annex/3/))*

Un test de positionnement dont les réponses sont analysées automatiquement pour
produire un niveau et orienter le contenu **coche les deuxième et troisième
tirets**. Ce n'est pas discutable, et c'est le piège dans lequel tombent la
plupart des organismes qui « mettent de l'IA » dans leur positionnement.

### Pourquoi le dispositif conçu ici n'est pas à haut risque

L'article 6 §3 prévoit une dérogation lorsque le système **n'influence pas
matériellement le résultat de la décision** — par exemple s'il se borne à une
tâche procédurale étroite, ou à préparer une évaluation qu'un humain conduit.

Trois choix d'architecture placent le dispositif dans cette dérogation :

1. **Le scoring n'est pas de l'IA.** `scoring.py` est une somme de points et un
   écart-type, sur un corrigé écrit par un humain. Aucun modèle, aucun
   apprentissage. Ce n'est pas un « système d'IA » au sens de l'article 3.1.
2. **L'IA n'intervient que pour lire une feuille de papier.** L'OCR transcrit
   des cases cochées. Il ne juge pas, il ne classe pas, il ne recommande rien.
3. **Aucune décision n'est prise par la machine.** La synthèse est en statut
   « À valider » tant que tu ne l'as pas relue. Le test **ne conditionne jamais
   l'accès** à la formation : personne n'est refusé, retardé ou réorienté sur
   la base d'un score.

> ⚠️ **Ce qui ferait basculer le dispositif en haut risque.** Trois évolutions,
> chacune suffisante à elle seule :
> - refuser, ajourner ou réorienter un candidat sur la base du score ;
> - utiliser le score comme **note** ou comme évaluation des acquis ;
> - laisser un modèle génératif rédiger la synthèse **et** l'envoyer au
>   formateur sans relecture.
>
> Les deux premières sont des décisions de gestion. La troisième est une
> tentation d'efficacité — c'est la plus probable. Le point de validation
> humaine de l'automatisation A2 n'est donc pas un confort : c'est la
> **frontière juridique** du dispositif.

### Ce qui s'applique, et quand

Le **Digital Omnibus, règlement (UE) 2026/1744**, entré en vigueur le
**27 juillet 2026**, a **reporté au 2 décembre 2027** les obligations de fond
applicables aux systèmes à haut risque de l'annexe III (initialement au
2 août 2026).

**En revanche, ceci s'applique déjà aujourd'hui :**

| Obligation | Applicable depuis | Ce que tu dois faire |
|---|---|---|
| **Art. 50 — transparence** | 2 août 2026 | Informer les stagiaires qu'un traitement automatisé intervient. → mention prévue au bloc E du formulaire |
| **Art. 4 — maîtrise de l'IA** | 2 février 2025 | Toute personne exploitant l'outil (toi, tes formateurs vacataires) doit disposer d'un niveau de littératie IA suffisant. **À tracer** : la formation de tes propres formateurs est une preuve. |
| Interdictions (art. 5) | 2 février 2025 | Sans objet ici. |

> **Ne présente pas le report comme une dispense.** Le report porte sur les
> obligations de fond des systèmes à haut risque — pas sur la transparence, pas
> sur la littératie. C'est exactement le contresens que font tes concurrents,
> et c'est un argument différenciant si tu le tiens correctement en clientèle.

### Document à produire et à conserver

Une **note d'analyse de risque IA Act**, une page, datée et signée, qui
établit : (1) le système est visé par l'annexe III point 3 ; (2) il relève de la
dérogation de l'article 6 §3 pour les trois motifs ci-dessus ; (3) la
validation humaine est documentée à chaque session.

Cette note est ta protection **et** ton argument commercial : c'est exactement
le livrable que tu peux vendre à tes clients TPE-PME qui déploient de l'IA sans
savoir où ils se situent.

---

## 2. RGPD

### Registre des traitements — fiche à créer

| Rubrique | Contenu |
|---|---|
| **Finalité** | Positionner le stagiaire à l'entrée pour adapter le contenu (Qualiopi ind. 8) |
| **Base légale** | Art. 6.1.b — exécution du contrat de formation. **Pas de consentement** : le positionnement fait partie de la prestation. |
| **Personnes concernées** | Stagiaires inscrits |
| **Données** | Réf. inscription, réponses (auto-positionnement, QCM, questions ouvertes), besoin d'aménagement (oui/non + nature du besoin), scores |
| **Données sensibles** | **Aucune.** Le besoin d'aménagement est collecté sans sa cause. |
| **Destinataires** | Responsable pédagogique + formateur de la session. **Ni l'entreprise cliente, ni l'OPCO.** |
| **Sous-traitants** | Airtable Inc. (🇺🇸), Tally (🇧🇪), Mistral AI (🇫🇷), hébergeur n8n |
| **Transferts hors UE** | **Oui — Airtable Inc.** Voir section 3. |
| **Conservation** | Réponses individuelles : **3 ans** après la fin de la formation. ⚠️ *Durée usuelle, à confirmer* : elle dépend du financeur (OPCO, CPF, Région, France Travail), dont les délais de contrôle diffèrent. Vérifier auprès de chacun et retenir la plus longue. Synthèses de session anonymisées : conservation libre. |
| **Sécurité** | Accès nominatif, table sans identité directe, secrets hors base |

### Article 22 — décision individuelle automatisée

L'article 22 du RGPD interdit qu'une personne fasse l'objet d'une décision
fondée **exclusivement** sur un traitement automatisé produisant des effets
juridiques ou l'affectant de manière significative.

Le dispositif y échappe pour la même raison qu'il échappe au haut risque IA
Act : **aucune décision n'est produite par la machine**. Le score n'ouvre ni ne
ferme l'accès à la formation, ne conditionne aucun financement, et la synthèse
est validée par un humain avant tout usage.

> Les deux régimes — art. 22 RGPD et annexe III de l'IA Act — sont **cumulatifs
> et distincts**. Ils se trouvent ici neutralisés par le même choix
> d'architecture, mais une évolution du dispositif devra être réexaminée au
> regard des deux, pas d'un seul.

### Sous-traitance : qui est responsable de traitement ?

Pour tes formations propres, tu es **responsable de traitement**.

Pour les prestations réalisées **pour le compte d'un autre centre** (les
formations « en institut » du catalogue semblent en relever), c'est en principe
le **donneur d'ordre** qui est responsable de traitement, et toi son
**sous-traitant** (art. 28). Conséquences concrètes :

- tu ne peux pas réutiliser librement les réponses collectées ;
- la mention d'information doit porter **son** identité, pas la tienne ;
- le contrat de sous-traitance doit prévoir ce traitement ;
- la durée de conservation est **la sienne**.

**À clarifier par écrit avant la première session concernée.** C'est aussi ce
qui commande la variable `[ORGANISME]` du bloc E.

### Minimisation appliquée (art. 5.1.c)

- La table `POSITIONNEMENT — RÉPONSES` ne contient **ni nom, ni e-mail, ni
  téléphone** : uniquement le lien vers `INSCRIPTIONS`.
- Le bloc E demande **le besoin d'aménagement, jamais la cause**.
- Les questions ouvertes portent sur des **situations de travail**, pas sur la
  personne.

### 🔴 Deux champs à supprimer dans ta base, sans attendre

La table `APPRENANTS` contient :

- `⚠️ NE PAS REMPLIR — Type de handicap (à supprimer, RGPD art.9)`
  (`fldMT7cDobHZJhMb2`)
- `⚠️ NE PAS REMPLIR — Document RQTH (à supprimer, RGPD art.9)`
  (`fldOeC2WWOvkOVPSX`)

Ils sont neutralisés par leur libellé, mais **existent toujours**. Un champ
neutralisé reste un champ : il peut être rempli par erreur, il apparaît dans les
exports, et un contrôle CNIL le verra. **Les supprimer, pas les masquer** — et
vérifier d'abord qu'ils sont vides, ou purger leur contenu avant suppression.

### Ce que tu dois pouvoir montrer

- La mention d'information (bloc E) telle qu'elle apparaît au stagiaire
- La fiche de registre ci-dessus
- La procédure d'effacement à 3 ans (et sa trace d'exécution)
- Le DPA signé avec chaque sous-traitant : Airtable, Tally, Mistral

---

## 3. Souveraineté — la faiblesse assumée du dispositif

**Je ne vais pas te la présenter comme réglée, parce qu'elle ne l'est pas.**

`Airtable Inc.` est une société américaine, soumise au **CLOUD Act**. Ta base
contient déjà, dans `APPRENANTS` : nom, prénom, date et lieu de naissance,
nationalité, adresse, téléphone, numéro CPF, statut RQTH. Le positionnement y
ajoute des données d'évaluation.

C'est en contradiction directe avec l'exigence de souveraineté que tu poses, et
avec le `CLAUDE.md` de ce dépôt qui prescrit Baserow (Pays-Bas).

### Ce que j'ai fait, faute de pouvoir tout résoudre

Je n'ai pas proposé de tout migrer : tu as construit sur Airtable un système
Qualiopi complet (16 tables, formules, automatisations). Une migration en bloc
te coûterait des semaines et casserait ta conformité pendant la transition.
Ce serait un mauvais conseil.

J'ai donc fait en sorte que **la partie positionnement soit portable** :

- le référentiel est un **JSON**, pas une table Airtable ;
- le moteur est un **script Python autonome**, sans dépendance à un éditeur ;
- la table `POSITIONNEMENT — RÉPONSES` est **pseudonymisée** ;
- Airtable n'est qu'une **destination d'écriture**, jamais le lieu du calcul.

Migrer ce bloc vers Baserow demande de réécrire les appels d'écriture. Pas le
reste.

### À faire de ton côté

1. **Vérifier le statut d'Airtable Inc.** : DPA signé, clauses contractuelles
   types en vigueur, et certification au *Data Privacy Framework* UE-US. Je n'ai
   pas vérifié ce dernier point — **ne l'affirme pas sans l'avoir constaté**.
2. **Décider et écrire** ta position : soit tu assumes Airtable en documentant
   le transfert, soit tu planifies la bascule. Les deux se défendent. **Ne rien
   décider est la seule option intenable** — surtout pour quelqu'un qui vend de
   l'audit de gouvernance.
3. **Cohérence commerciale.** Tu vends du conseil RGPD à des TPE-PME
   réunionnaises. Le jour où un client te demandera où sont tes propres données,
   « Airtable, aux États-Unis » sera une réponse coûteuse. À l'inverse, « voici
   ma cartographie, voici mon arbitrage, voici mon plan de bascule » est un
   argument de vente. C'est ton métier : applique-le à toi-même.

> 🔌 **Note technique.** Le serveur MCP `baserow` de ce dépôt **n'a pas pu se
> connecter** durant cette session (`CONNECTION_CLOSED`). Je n'ai donc pas pu
> préparer la structure côté Baserow, ni tester la portabilité en conditions
> réelles. À relancer quand tu voudras que je m'en occupe.

---

## Sources

- Règlement (UE) 2024/1689 (IA Act) — [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- Annexe III, point 3 (éducation et formation professionnelle) — [artificialintelligenceact.eu](https://artificialintelligenceact.eu/annex/3/)
- Report des obligations haut risque au 2 décembre 2027 (Digital Omnibus, règlement (UE) 2026/1744) — [Quantic Avocats](https://www.quantic-avocats.com/2026/07/22/ai-act-digital-omnibus-report-obligations-haut-risque/) · [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- Ce qui reste applicable au 2 août 2026 (art. 50) — [Komanche](https://www.komanche.fr/3109-2/)
- Qualiopi, indicateur 8 (positionnement à l'entrée) — [Digiforma](https://www.digiforma.com/certification-qualiopi/criteres/critere-2/indicateur-8-positionnement-entree/) · [Certifopac](https://certifopac.fr/qualiopi/referentiel/2-objectif-adaptation-prestations/8-positionnement-entree/)
- Mistral OCR 4, hébergement européen et tarification — [Cyloé](https://cyloe.com/mistral-ocr-4-extraction-structuree-documents/) · [Eden AI](https://www.edenai.co/post/mistral-ocr-4-vs-top-document-parsing-apis-features-benchmarks-and-integration-guide)
- Tally, hébergement Belgique et chiffrement — [La Fabrique du Net](https://www.lafabriquedunet.fr/logiciel/tally)
- RGPD, texte de référence — [CNIL](https://www.cnil.fr)

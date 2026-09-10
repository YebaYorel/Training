# YEBA FORMATIONS — SOCLE DOCUMENTAIRE

Édition du 10/09/2026 | Dirigeant et référent : **Aurélien LUMEKA**

Ce dossier contient l'intégralité des documents institutionnels, juridiques, qualité et
commerciaux de YEBA FORMATIONS, écrits selon **une trame unique**.

**Le même corpus est stocké en texte intégral dans la base Airtable, table
`DOCUMENTS OFFICIELS YEBA`.** Les deux doivent rester synchronisés : Git fait foi pour
l'historique des versions, Airtable pour l'usage quotidien.

---

## Où commencer

| Vous voulez… | Ouvrez |
|---|---|
| Savoir ce qui ne va pas et quoi faire | `audit/RAPPORT-AUDIT-ET-PLAN-ACTION.md` |
| Produire un support conforme à la marque | `identite/charte-graphique.md` |
| Vendre à une entreprise | `documents/05-convention-de-formation.md` + `03-conditions-generales-de-vente.md` |
| Vendre à un particulier | `documents/06-contrat-formation-particulier.md` — **jamais la convention** |
| Faire intervenir un formateur externe | `documents/07-convention-sous-traitance-formateur.md`, volet A |
| Intervenir pour un autre organisme | `documents/07-…`, **volet B** — marque blanche |
| Répondre à un auditeur Qualiopi | `documents/10-charte-qualite.md` + `09-procedure-reclamations.md` |
| Répondre à une question RGPD d'un client | `documents/02-politique-de-confidentialite.md` + `11-charte-usage-ia.md` |
| Alimenter le site internet | `documents/12-politique-tarifaire.md` + `13-financements-mobilisables.md` + `01-mentions-legales.md` |

---

## Contenu

```
yeba/
├── identite/
│   ├── charte-graphique.md            Palette, contrastes WCAG, typographie, bloc-marque
│   └── logo-yeba-sans-oeil.svg        Logo vectoriel — l'œil a été retiré
├── documents/
│   ├── 01-mentions-legales.md
│   ├── 02-politique-de-confidentialite.md
│   ├── 03-conditions-generales-de-vente.md
│   ├── 04-reglement-interieur.md
│   ├── 05-convention-de-formation.md
│   ├── 06-contrat-formation-particulier.md
│   ├── 07-convention-sous-traitance-formateur.md
│   ├── 08-politique-handicap-accessibilite.md
│   ├── 09-procedure-reclamations.md
│   ├── 10-charte-qualite.md
│   ├── 11-charte-usage-ia.md
│   ├── 12-politique-tarifaire.md
│   └── 13-financements-mobilisables.md
└── audit/
    └── RAPPORT-AUDIT-ET-PLAN-ACTION.md
```

---

## Les trois règles qui gouvernent tout le corpus

**1. Le bloc-marque clôt chaque document.** Reproduit à l'identique, il porte la mention
obligatoire « Cet enregistrement ne vaut pas agrément de l'État » (code du travail, art. L.6352-12).

**2. La marque blanche l'emporte sur la marque.** Sur les actions réalisées en sous-traitance
(FOR-0005, FOR-0007), **rien de YEBA FORMATIONS n'apparaît** sur les supports remis au client
final. Le champ « Marque / Confidentialité contractuelle » du catalogue fait foi, fiche par fiche.

**3. Un crochet `[ … ]` signifie : ne pas diffuser.** Tant qu'un document contient un marqueur
entre crochets — assureur, médiateur, RCS, hébergeur — il n'est pas remis à un client.
Le champ « Éléments manquants à fournir » de la base liste, document par document, ce qui reste dû.

---

## Ce qui bloque aujourd'hui

| Priorité | Action | Effet |
|---|---|---|
| **1** | Désigner un médiateur de la consommation | Débloque la vente aux particuliers — obligation légale |
| **1** | Fournir l'attestation d'assurance RC Pro | Débloque 5 documents |
| **1** | Confirmer le n° Qualiopi sur le certificat papier | Deux sources sur trois indiquaient `25FOF02027.1` |
| **2** | Valider la grille tarifaire, ligne par ligne | Débloque la publication du site |
| **2** | Reprendre les 32 lignes de `INDICATEURS QUALIOPI` | Toutes déclarées non conformes à ce jour |

Détail et justification : `audit/RAPPORT-AUDIT-ET-PLAN-ACTION.md`.

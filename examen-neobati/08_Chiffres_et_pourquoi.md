---
title: "Feuille 8 — Les chiffres de l'examen, et le pourquoi de chaque choix"
---

Chaque bloc suit le même ordre : **Ce que j'ai fait** (technique) → **Pourquoi** → **Pour ma mère** (simple).

# Partie A — Pourquoi Airtable, et pourquoi Make ?

| | **Airtable** | **Make** |
|---|---|---|
| **Son rôle ici** | La **mémoire** et la **calculatrice** de NéoBâti : toutes les données des chantiers au même endroit, les marges calculées toutes seules, un écran par métier. | Les **mains** et l'**horloge** : il agit sans qu'on lui demande (chaque matin, ou dès qu'un rapport arrive), fait parler les outils entre eux et appelle l'IA. |
| **Ce qu'il résout dans le brief de Paul** | « On s'y perd entre Excel, Google, SMS, WhatsApp » → **une seule source de vérité**. « Les marges sont difficiles à calculer » → **formules automatiques**. | « Relances pas systématiques » → **relances automatiques**. « Je veux voir tout de suite si un chantier prend du retard » → **alerte chaque matin**. « L'IA pour les textes et résumés » → **Mistral appelé par Make**. |
| **Ce qu'il ne fait pas bien** | Agir seul sur la durée (automatisations limitées, pas de vrai planificateur multi-étapes avec IA et gestion d'erreurs fine). | Stocker et afficher des données (pas de base, pas d'écran pour l'équipe). |
| **Pour ma mère** | « Le grand classeur intelligent du bureau. » | « Le secrétaire qui passe chaque matin et qui fait le courrier tout seul. » |

**La phrase à dire à l'oral** : « Airtable *sait* (il stocke et calcule), Make *agit* (il déclenche, transporte et rédige). Je mets chaque calcul dans Airtable, parce que c'est gratuit et visible par l'équipe, et chaque action dans Make, parce que c'est là qu'on gère l'horloge, l'IA et les erreurs. »

# Partie B — Pourquoi ces relations (liens) entre les tables ?

**Ce que j'ai fait** : des champs « **lien vers une autre table** ». Quand je relie un chantier à un client, Airtable crée automatiquement le lien inverse (le client voit ses chantiers).
**Pourquoi** : sans lien, il faudrait recopier le nom du client dans chaque devis et chaque facture : doublons, fautes de frappe, et **aucun calcul possible entre tables**. C'était le défaut n° 1 de l'ancienne base.
**Pour ma mère** : « Au lieu de recopier l'adresse du client sur chaque papier, je tends une ficelle entre le papier et sa fiche. Si l'adresse change, elle change partout. »

| Lien | Type | Pourquoi ce lien existe (besoin du sujet) |
|---|---|---|
| CHANTIERS → CLIENTS | N chantiers pour 1 client | « Gestion des clients : historique de chantiers » |
| DEVIS → CLIENTS et → CHANTIERS | 1 devis pour 1 chantier | Le devis accepté devient le **budget** du chantier |
| FACTURES → CHANTIERS | N factures pour 1 chantier | Acompte, intermédiaire, solde → **CA facturé** |
| POINTAGES → CHANTIERS et → RESSOURCES | 1 ligne = 1 artisan × 1 chantier | Annexe 1 : heures × coût horaire **de cet artisan** |
| ACHATS → CHANTIERS | N achats pour 1 chantier | Annexe 2 : fournitures + sous-traitance |
| ETAPES → CHANTIERS et → RESSOURCES | N étapes pour 1 chantier | « Jalons et étapes clés, responsables » |
| CHANTIERS → RESSOURCES (équipe, chef) | N-N | « Artisans affectés, disponibilités » + notification d'affectation |
| RAPPORTS TERRAIN → CHANTIERS | N rapports pour 1 chantier | « Remontée terrain », résumé IA |
| INTERACTIONS → CLIENTS et → CHANTIERS | historique | « Historisation des interactions clients » |
| DEMANDES → CLIENTS | 1 demande crée ou retrouve 1 client | Formulaire « nouvelle demande client » |

# Partie C — Lookup, rollup, formule, count : à quoi sert chacun ?

| Outil Airtable | Ce que ça fait | Exemple NEOBATI | Pour ma mère |
|---|---|---|---|
| **Lookup** (recherche) | Lit une information au bout du lien, sans la recopier. | Dans FACTURES, *Email client* : facture → chantier → client → email. Make s'en sert pour relancer. | « Je tire la ficelle et je lis ce qui est écrit au bout. » |
| **Rollup** (agrégation) | Lit **et calcule** sur tous les enregistrements liés (somme, moyenne…). | Dans CHANTIERS, *Coût main-d'œuvre* = SOMME des coûts de tous les pointages liés. | « Je tire toutes les ficelles d'un coup et j'additionne. » |
| **Formule** | Calcule à partir des champs de la même fiche. | *Marge brute* = CA facturé − coût total. | « La calculatrice collée sur la fiche. » |
| **Count** | Compte les enregistrements liés. | Dans CLIENTS, *Nombre de chantiers*. | « Je compte les ficelles. » |

**Pourquoi cet ordre (lien → rollup → formule)** : la formule ne peut lire que sa propre fiche. Il faut donc d'abord **ramener** les montants sur la fiche chantier (rollup), puis **calculer** (formule). C'est la chaîne : *pointages → rollup → coût MO → formule → marge*.

**Pourquoi les calculs dans Airtable et pas dans Make** : une formule Airtable ne coûte **aucune opération Make**, se recalcule à chaque modification, et l'équipe la voit à l'écran. Make se contente de lire des champs déjà prêts (« Alerte devis », « Niveau de relance », « Alerte pilotage »).

# Partie D — Les 9 formules de l'annexe, pas à pas, sur le chantier C1

**Chiffres donnés par le sujet (annexe)** : 20 h menuisier × 45 € ; 15 h peintre × 40 € ; fournitures 800 € ; électricien sous-traitant 1 200 €.
**Seules hypothèses ajoutées par moi** (le sujet n'en donne pas) : devis accepté **5 000 € HT** ; acompte de 30 % (**1 500 €**) payé ; électricien sous-traitant **pas encore payé**.

| N° annexe | Formule | Calcul C1 | Résultat | Où dans Airtable |
|---|---|---|---|---|
| 1 | Coût MO = Σ(heures × coût horaire) | 20 × 45 = 900 ; 15 × 40 = 600 ; 900 + 600 | **1 500 €** | POINTAGES (formule) → CHANTIERS (rollup) |
| 2 | Coût achats = Σ(achats HT) | 800 + 1 200 | **2 000 €** | ACHATS → CHANTIERS (rollup) |
| 3 | Coût total = MO + achats | 1 500 + 2 000 | **3 500 €** | CHANTIERS (formule) |
| 4 | CA facturé = Σ(factures HT) | acompte 1 500 + solde 3 500 | **5 000 €** | FACTURES → CHANTIERS (rollup) |
| 5 | Marge brute = CA − coût total | 5 000 − 3 500 | **1 500 €** | CHANTIERS (formule) |
| 6 | Taux de marge = marge ÷ CA × 100 | 1 500 ÷ 5 000 × 100 | **30 %** | CHANTIERS (formule) |
| 7a | Solde client = factures − paiements | 5 000 − 1 500 | **3 500 €** restant dû | CHANTIERS (formule) |
| 7b | Trésorerie nette = acomptes − coûts payés | 1 500 − (1 500 MO + 800 fournitures) | **− 800 €** | CHANTIERS (formule) |
| 8a | Écart budget = devis − coût total | 5 000 − 3 500 | **+ 1 500 €** | CHANTIERS (formule) |
| 8b | % avancement financier = coûts ÷ CA × 100 | 3 500 ÷ 5 000 × 100 | **70 %** | CHANTIERS (formule) |
| 8c | % facturation = factures ÷ devis × 100 | 5 000 ÷ 5 000 × 100 | **100 %** | CHANTIERS (formule) |
| 9 | Indicateurs globaux | voir Partie E | | Interface Direction |

**Comment lire ces chiffres (à dire à l'oral)** :
- *30 %* : « sur 100 € facturés, il reste 30 € de marge à NéoBâti. »
- *− 800 €* : « pendant le chantier, l'acompte n'a pas couvert les dépenses déjà payées : l'entreprise a avancé 800 €. C'est pour ça qu'on relance les acomptes. »
- *70 %* : « les coûts représentent 70 % de ce qui est facturé » (formule de l'annexe ; ce n'est **pas** l'avancement physique des travaux, qui vient des rapports terrain).

# Partie E — Les 5 chantiers de démonstration (chiffres arrondis, faciles à retenir)

Tarifs horaires : menuisier **45 €**, peintre **40 €** (annexe), électricien **40 €** (hypothèse, même tarif que le peintre).

| Chantier | Statut | Devis | MO | Achats | Coût total | Facturé | Marge | À retenir |
|---|---|---|---|---|---|---|---|---|
| C1 Appartement T3 | Terminé | 5 000 | 1 500 | 2 000 | 3 500 | 5 000 | **+1 500 (30 %)** | l'exemple de l'annexe |
| C2 Bureaux | En cours | 12 000 | 3 900 | 3 000 | 6 900 | 3 600 | provisoire | **retard** + **acompte non payé** |
| C3 Salle de bain | En attente | 4 000 (envoyé) | 0 | 0 | 0 | 0 | — | **devis à relancer** |
| C4 Cuisine | En cours | 8 000 | 3 600 | 4 800 | 8 400 | 5 600 | provisoire | **dépassement : 8 400 > 8 000 (−400 €)** |
| C5 Cage d'escalier | Terminé | 3 000 | 1 600 | 650 | 2 250 | 3 000 | **+750 (25 %)** | terminé avec 4 jours de retard |

*Détail des MO* : C2 = 60 h × 45 + 30 h × 40 = 2 700 + 1 200 ; C4 = 80 h × 45 ; C5 = 40 h × 40.

**Indicateurs globaux (annexe 9)** :
- Marge moyenne des chantiers terminés = (1 500 + 750) ÷ 2 = **1 125 €**.
- Taux de chantiers déficitaires (terminés) = 0 ÷ 2 = **0 %**.
- Classement par marge : C1 (1 500 €) puis C5 (750 €).
- Répartition des coûts : MO 1 500 + 3 900 + 3 600 + 1 600 = **10 600 €** ; achats 2 000 + 3 000 + 4 800 + 650 = **10 450 €** ; total **21 050 €** → MO **50,4 %**, achats **49,6 %**.
- Trésorerie : facturé **17 200 €**, encaissé **6 900 €**, reste dû **10 300 €**.

**Pourquoi la marge de C2 et C4 est « provisoire »** : l'annexe calcule la marge sur le CA *facturé*. Un chantier en cours n'est pas encore entièrement facturé, sa marge paraît donc négative. Pour piloter un chantier ouvert, je regarde l'**écart budget** (devis − coût total) : C2 = 12 000 − 6 900 = **+5 100 €** (sain), C4 = 8 000 − 8 400 = **−400 €** (alerte).

# Partie F — Le chiffre Make, simplement

« 1 module qui s'exécute = 1 opération. Avec la sonnette (webhook), Make ne travaille que quand il se passe quelque chose : **≈ 620 opérations par mois**. S'il allait vérifier toutes les 15 minutes : 4 vérifications par heure × 24 h × 30 jours = **2 880** par scénario, × 3 scénarios = **8 640** opérations à vide en plus. Soit **≈ 9 260** au total, **15 fois plus**. » (détail : feuille 6)

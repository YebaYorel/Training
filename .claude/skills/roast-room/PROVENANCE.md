# Compétence « roast-room » (conseil de conseillers) : provenance et règles YEBA

Ce fichier est propre à YEBA FORMATIONS. Il ne fait pas partie de l'œuvre copiée et ne la modifie pas.

## Origine et licence

- **Source** : https://github.com/nateherkai/roast-room, commit `e40f40652d5690c4d9f928c4794c673a99f2cd0e`
  (21/10/2026). Copie faite le 13/11/2026.
- **Auteur et licence** : AI Automation Society (Nate Herk), licence **MIT**. Le fichier `LICENSE` est joint et doit
  rester avec la copie.
- **Copié à l'identique** :
  - ce dossier : `SKILL.md`, `brains/` (12 conseillers), `references/`, `roster.json`, `scripts/check_quotes.py` ;
  - les 12 conseillers `.claude/agents/council-*.md`.
- **Fichiers YEBA séparés** : ce `PROVENANCE.md` et `mettre-a-jour.sh`.

## Ce qui a été relu avant l'installation (13/11/2026)

- Uniquement des textes d'instructions.
- Les 12 conseillers sont en **lecture seule** : leurs outils sont `Read`, `Grep` et `Glob`.
- Un seul script, `check_quotes.py`, en Python standard. Il compare les citations d'une séance aux « cerveaux » des
  conseillers. Il ne fait aucun appel réseau et n'écrit rien.
- Aucun hook, aucune clé d'API.

## Ce qui n'a pas été copié

- **`newroaster`**, la compétence qui ajoute un conseiller. Deux de ses étapes posent problème :
  - pour les sous-titres YouTube, elle interroge l'API interne de YouTube en se faisant passer pour l'application
    Android, ce qui est contraire aux conditions d'utilisation de YouTube ;
  - elle envoie la photo d'une personne réelle au service kie.ai, hors UE, pour en faire une caricature. C'est un
    transfert d'image de personne hors UE (RGPD) et une question de droit à l'image.

  Elle ne sera réinstallée que si Aurélien le demande, et alors sans l'étape portrait.
- **La salle visuelle** (`app/`) : la table animée sur http://localhost:4730, avec ses caricatures de personnes réelles.
  Le lanceur `roast-room-app` la récupère à la demande, hors de ce dépôt public.
- **Les 3 séances d'exemple** (`sessions/`) : elles se trouvent dans le cache du lanceur.

## À quoi il sert chez YEBA

Il soumet une décision difficile à un conseil de « sièges » simulés à partir des travaux publics de chaque expert.
Exemples de décisions : le prix d'une formation, une nouvelle offre, un recrutement, un partenariat, un événement, une
dépense.

**Composition par défaut**

| Siège | Domaine |
|---|---|
| Alex Hormozi | offres, prix, vente |
| Paul Graham, cofondateur de **Y Combinator** | produit, demande réelle, croissance |
| **Gary Vaynerchuk** | marketing, attention, distribution |
| Jeff Bezos | stratégie, réversibilité |
| Warren Buffett | risque, capital |
| Dan Martell | équipe, temps du dirigeant |
| Gino Wickman | organisation (EOS) |

Cinq autres sièges sont disponibles sur appel : Naval Ravikant, Codie Sanchez, Leila Hormozi, Sara Blakely, Elon Musk.

**Déroulé** : trois tours (positions, débat, vote), puis un verdict chiffré, l'avis minoritaire et les prochaines étapes.

**Commandes**

| Commande | Effet |
|---|---|
| `/roast-room <décision>` | conseil complet |
| `--quick` | 4 sièges, pour une décision réversible |
| `--seats hormozi,graham,garyvee` | seulement ces sièges |
| `ask hormozi <question>` | consultation d'un seul siège |
| `/roast-room board` | changer la composition par défaut |

## Garde-fous YEBA

- **Langue** : les « cerveaux » sont en anglais. Le brief, le verdict et le rapport destinés à Aurélien sont rédigés en
  français.
- **Simulations, pas des personnes** : un siège n'est jamais la vraie personne.
  - Ne jamais attribuer une phrase à Hormozi, Graham ou Vaynerchuk dans un support, une publication ou une offre YEBA,
    sauf citation exacte avec sa source.
  - Risques en cas d'écart :
    - droit de la personnalité (art. 9 du Code civil) ;
    - pratiques commerciales trompeuses (Code de la consommation, art. L.121-2 et suivants).
- **Données** :
  - les séances sont enregistrées dans `sessions/`, que Git ignore (le dépôt est public) ;
  - le brief ne contient que des données d'entreprise, jamais de données personnelles de stagiaire ou de client.
- **RGPD** : le brief et les débats passent par Claude (Anthropic, États-Unis). C'est une raison de plus pour n'y mettre
  aucune donnée personnelle.
- **IA Act** :
  - c'est une aide à la décision du dirigeant, pas une décision automatisée ;
  - ne jamais s'en servir pour classer des candidats (annexe III, point 4) ni pour évaluer des stagiaires (annexe III,
    point 3) : ce sont des usages à haut risque ;
  - la décision reste à Aurélien.
- **Coût** : un conseil complet demande trois passages par siège, soit 21 pour 7 sièges. Cela représente environ
  1 million de jetons du forfait Claude. `--quick` suffit pour une décision réversible.

## Mettre à jour

Lancer `bash .claude/skills/roast-room/mettre-a-jour.sh`, puis relire le diff avant de committer. Points à vérifier :
- de nouveaux outils pour les conseillers (autres que `Read`, `Grep`, `Glob`) ;
- un nouveau script ;
- un appel réseau.

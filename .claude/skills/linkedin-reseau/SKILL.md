---
name: linkedin-reseau
description: Construire et animer le réseau LinkedIn professionnel d'Aurélien LUMEKA / YEBA FORMATIONS auprès des TPE-PME de La Réunion (dirigeants, RH, OPCO, CCI, CMA, réseaux d'entreprises) — ciblage, messages d'invitation personnalisés, relances, routine hebdomadaire, suivi dans Baserow — dans le respect des conditions d'utilisation de LinkedIn et du RGPD. À utiliser pour toute demande de développement de réseau, prospection ou messages LinkedIn.
---

# Réseau LinkedIn — YEBA FORMATIONS

## Règle n° 1 : pas d'automatisation du compte

Les conditions d'utilisation de LinkedIn interdisent les robots, scripts et
extensions qui envoient des invitations/messages ou extraient des contacts
automatiquement (Contrat d'utilisation LinkedIn, section 8.2 — source :
linkedin.com/legal/user-agreement). Risque : restriction ou fermeture du compte.

Donc Claude **prépare** (cibles, messages, calendrier, suivi) et **Aurélien
envoie lui-même** depuis LinkedIn. Aucun outil d'automatisation type
« auto-connect » ou « scraping » ne doit être proposé.

## 1. Cartographie du réseau cible (La Réunion)

Construire la liste par segments, sans inventer de noms de personnes :

| Segment | Exemples de profils | Intérêt pour YEBA |
|---|---|---|
| Dirigeants TPE-PME | gérants, fondateurs (BTP, commerce, tourisme, services) | clients intra-entreprise, audits RGPD / IA Act |
| RH / responsables formation | PME de 20 à 250 salariés | plan de développement des compétences |
| Financeurs & prescripteurs | conseillers OPCO, CCI Réunion, CMA, France Travail | orientation de clients, financement |
| Réseaux d'entreprises | clubs d'entrepreneurs, associations de dirigeants | événements, visibilité |
| Lieux d'accueil | hôtels et salles de séminaire | formations inter-entreprises |
| Partenaires tech / juridiques | DPO externes, avocats numériques, ESN locales | co-traitance, recommandations |

Demander à l'utilisateur quels organismes et personnes il connaît déjà avant
de proposer une liste nominative.

## 2. Messages (toujours personnalisés, ≤ 300 caractères pour l'invitation)

Modèle d'invitation :
> Bonjour [Prénom], je vois que vous dirigez [entreprise] à [ville]. J'accompagne
> les TPE-PME réunionnaises sur l'IA au quotidien et la conformité RGPD. Ravi
> d'échanger entre acteurs du 974 !

Règles :
- Un élément personnel réel (publication récente, secteur, ville) par message.
- **Pas de pitch commercial dans l'invitation.**
- Relance J+7 après acceptation : apporter de la valeur (ressource, retour
  d'expérience), pas une offre.
- Proposition d'échange seulement au 2ᵉ ou 3ᵉ contact, avec opposition facile
  (« si ce n'est pas le bon moment, dites-le-moi simplement »).

## 3. Routine hebdomadaire (≈ 20 min/jour)

- Lundi : 10 invitations ciblées (un segment par semaine).
- Mardi–jeudi : 1 post (skill `linkedin-post`) + 5 commentaires utiles sur les
  publications de la cible.
- Vendredi : relances, remerciements, mise à jour du suivi.
- Rester sous le volume hebdomadaire d'invitations toléré par LinkedIn
  (chiffre non officiel → ne pas l'affirmer ; viser la qualité, ~50/semaine max).

## 4. Suivi dans Baserow (cloud UE)

Table « Réseau LinkedIn » via le MCP `baserow` (`create_table_with_schema`) :
`Prénom`, `Nom`, `Entreprise`, `Fonction`, `Segment` (single_select),
`URL du profil`, `Statut` (single_select : À inviter / Invité / Connecté /
Échange / Client), `Date du dernier contact` (date), `Prochaine action`,
`Opposition` (booléen).

## 5. Conformité (à signaler à chaque livrable)

- **RGPD** : le fichier de suivi contient des données personnelles →
  finalité = prospection B2B ; base légale = intérêt légitime (art. 6.1.f) ;
  minimisation (pas de téléphone perso, pas de données sensibles) ; information
  de la personne dès le premier contact hors LinkedIn (art. 14) ; durée de
  conservation (ex. 3 ans après le dernier contact) ; respect immédiat de toute
  opposition ; inscription au registre des traitements.
- **Prospection par e-mail** après LinkedIn : en B2B, autorisée sans
  consentement préalable si l'offre est liée à la fonction de la personne, avec
  lien de désinscription (source : cnil.fr, « La prospection commerciale par
  courrier électronique »).
- **IA Act** : rédiger des messages avec l'IA n'est pas un usage à haut risque.
  Un **scoring automatisé** des prospects reste hors annexe III, mais doit être
  transparent et relu par un humain ; ne jamais trier des **candidats ou
  stagiaires** par IA sans analyse (annexe III, points 3 et 4 : haut risque).

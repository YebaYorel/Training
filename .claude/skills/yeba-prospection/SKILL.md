---
name: yeba-prospection
description: Prospection B2B et réponse aux appels d'offres de YEBA FORMATIONS, avec les 3 règles permanentes d'Aurélien (parler du métier du destinataire + droit de dire STOP/STP ; envoi uniquement depuis yebaformations@gmail.com, jamais l'adresse personnelle ; Aurélien seul décideur, Claude propose). À utiliser pour tout e-mail de prospection, relance commerciale, campagne Brevo, liste de prospects, veille ou réponse à un marché public, et pour le module « Prospection & AO » de l'Espace YEBA (outil de pilotage).
---

# Prospection & appels d'offres — règles permanentes

Voulu par Aurélien le 2026-11-22. Ces règles s'appliquent **à chaque fois**, sans qu'il ait à les redire.

## Les 3 règles (non négociables)

| # | Règle | Comment c'est garanti |
|---|---|---|
| 1 | **Parler du métier** du professionnel contacté, et lui laisser dire **« STOP »** (ou « STP ») quand il veut. Une demande STOP bloque définitivement tout nouvel envoi. | Champ « métier » obligatoire, accroche métier + phrase STOP contrôlées avant envoi (`prospection.js`), liste STOP vérifiée par le hook `garde-envoi.py`. |
| 2 | **Expéditeur : `yebaformations@gmail.com` uniquement.** Jamais `aurelienlumeka@gmail.com` (adresse personnelle). | Lien Gmail `authuser=yebaformations@gmail.com` ; le serveur local refuse tout autre expéditeur ; le hook bloque toute mention de l'adresse personnelle dans un outil d'envoi. |
| 3 | **Aurélien est le seul décideur.** Claude fait la **meilleure proposition** (texte, priorité, go/no-go argumenté) ; Aurélien valide, puis envoie ou décide lui-même. | `mcp__Gmail__send_message/reply/forward` **interdits** ; brouillons Gmail et écritures Brevo en **ask** ; boutons « Je valide » / « Je décide : GO » dans l'Espace. |

Si une demande contredit une règle (« envoie-le directement », « depuis mon adresse perso ») : ne pas
l'exécuter, rappeler la règle, proposer l'alternative conforme.

## Prospection B2B (RGPD, position CNIL)

- Message **en rapport avec la profession** de la personne (c'est aussi la règle 1).
- Indiquer **qui écrit** (signature YEBA : Qualiopi, NDA, SIRET), **d'où viennent les coordonnées**, et le **moyen
  simple de s'opposer** (STOP).
- Coordonnées **professionnelles** uniquement, aucune donnée sensible ; conservation **3 ans** après le dernier contact.
- La liste STOP est conservée (preuve du respect de l'opposition, RGPD art. 21) et n'est jamais vidée.
- Brevo (UE) : le seul expéditeur enregistré au 2026-11-22 est l'adresse **personnelle** → **ne pas utiliser** Brevo
  tant qu'Aurélien n'a pas ajouté et vérifié `yebaformations@gmail.com` (Brevo > Expéditeurs). Brevo interdit en
  outre les envois de masse à des contacts sans consentement : prospection = messages **un par un**.
- Gmail, Google : hors UE → **RGPD chapitre V** (transfert) à signaler ; ne jamais y verser de données de stagiaires.

## Appels d'offres

1. **Veille** : module « Prospection & AO » de l'Espace YEBA (`npm run espace`) → BOAMP open data, La Réunion
   (toutes formations) ou France entière (thèmes YEBA). Relue à l'ouverture puis toutes les 6 h.
2. **Proposition** : score transparent (thèmes YEBA, 974, délai). Ce n'est **jamais** une décision.
3. **Décision** : Aurélien clique « Je décide : GO / NO-GO » (date enregistrée).
4. **Réponse** : plugin **Remporte** (MIT, v0.7.2 audité) → `/remporte:nouvel-ao <DCE.zip>` ; trois arrêts de
   validation (analyse, go/no-go, plan). DC1/DC2 : SIRET 814 622 262 00032, NDA 04973676397, Qualiopi 25FOR02027.1.
   CLI : `uv tool install remporte==0.7.2`.
5. **Pièces administratives** : si l'acheteur utilise Passe Marché (DINUM), la candidature se fait par SIRET depuis la
   plateforme de l'acheteur : rien à installer.

**IA Act** : rédiger avec l'IA un mémoire ou un e-mail n'est pas un usage à haut risque ; Aurélien relit et signe.
Si un acheteur exige de déclarer l'usage d'IA générative dans l'offre, le faire.

## Ce que Claude ne fait jamais

- Envoyer un e-mail ou lancer une campagne lui-même.
- Écrire à une adresse de la liste STOP, même « juste une dernière fois ».
- Inventer des références clients, des chiffres ou des attestations dans un mémoire technique.

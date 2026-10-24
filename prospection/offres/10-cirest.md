# CIREST

> **Décideur identifié** : Joé BÉDIER — Président (élu le 09/04/2026), maire de Saint-André  
> **Fiabilité de l'information** : Outremers 360 (04/2026)  
> Tout ce qui est marqué [À VÉRIFIER] doit être confirmé (appel au standard) avant l'envoi.

---

## 1. Le courriel (prêt à envoyer)

**À :** Cabinet du Président — CIREST (adresse [À VÉRIFIER])  
**Objet :** CIREST — Plan « IA responsable » en 90 jours : gagner du temps sans exposer les données des administrés  
**Pièces jointes :** CV d'Aurélien LUMEKA · Note de proposition (parties 2 à 8 de ce mémo, en PDF)

> Monsieur le Président,  
>
> Une nouvelle mandature s'ouvre pour la CIREST, et elle arrive avec deux réalités très concrètes. D'une part, depuis le 2 août 2026, les obligations de transparence de l'IA Act (article 50) s'appliquent : un assistant conversationnel ou un contenu généré par IA mis à disposition du public doit être identifié comme tel. D'autre part, comme dans la plupart des collectivités, des agents utilisent très probablement déjà des outils d'IA grand public, parfois avec des données d'administrés, sans cadre défini — alors que le RGPD vous impose un délégué à la protection des données et une maîtrise de vos traitements. Vous avez appelé, lors de votre investiture, à ouvrir « un nouveau chapitre » : l'encadrement de l'IA peut en faire partie.  
>
> Je vous propose un Plan « IA responsable » en 90 jours, en trois temps :  
>
> • Audit des usages (3 jours) : quels outils, quels services, quelles données — une cartographie claire, classée selon l'IA Act ;  
> • Charte d'usage de l'IA (2 jours), co-rédigée avec votre DPO, et la liste des outils autorisés, souverains (Mistral, Albert de l'État) ;  
> • Formation des agents (6 sessions d'une journée) : rédiger un courrier, résumer un dossier, préparer un compte rendu en quelques minutes — sans jamais exposer une donnée personnelle.  
>
> En option, un assistant IA hébergé en France, nourri de vos procédures internes, et des comptes rendus de réunion automatiques.  
>
> Le montant de ce plan se situe sous le seuil de 60 000 € HT de dispense de procédure (article R2122-8 du Code de la commande publique, depuis le 1er avril 2026), ce qui permet une décision rapide dans le respect des règles de la commande publique.  
>
> Organisme de formation certifié Qualiopi, j'interviens en vente, management et intelligence artificielle, avec une double compétence en gouvernance RGPD et IA Act (formé par l'ANSSI — SecNumAcadémie — et par la CNIL ; certifications Google AI). Je suis également Référent handicap : mes supports sont lisibles par tous vos agents.  
>
> Je serais heureux de présenter ce plan à votre DGS et à votre DPO en 30 minutes, le [date 1] ou le [date 2]. Vous trouverez ci-joint mon CV et une note de proposition détaillée.  
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

- Nouvelle équipe élue après les municipales de mars 2026 : moment idéal pour fixer les règles.
- IA Act, article 50 (transparence), applicable depuis le 02/08/2026.
- RGPD : délégué à la protection des données obligatoire pour toute autorité publique (art. 37).
- Usages d'IA grand public par les agents, rarement encadrés (constat général, à confirmer par l'audit).

## 3. Comment je vous aide — expliqué simplement

*(comme à un enfant de 5 ans)*

> Dans la mairie, les gens commencent à utiliser des robots qui écrivent à leur place. C'est pratique, mais parfois ils racontent les secrets des habitants à des robots qui habitent très loin. Moi, je viens d'abord faire la liste de tous les robots utilisés. Ensuite, on écrit ensemble les règles du jeu : quels robots ont le droit d'entrer, et ce qu'on ne doit jamais leur dire. Puis j'apprends à chacun à se servir d'un robot gentil qui habite en France et qui garde les secrets. À la fin, tout le monde travaille plus vite, et les secrets des habitants restent dans la mairie.

## 4. Les IA et outils utilisés

| Outil | Éditeur, pays | Payant ? | Prix indicatif | Pourquoi ici |
|---|---|---|---|---|
| Albert API / Assistant IA de l'État | DINUM, France | Non (administrations) | Gratuit dans la limite des capacités (2024) — conditions 2026 [À VÉRIFIER] | Assistant des agents (si l'accès est ouvert à la collectivité) |
| API Mistral (La Plateforme) | Mistral AI, France | Oui, à l'usage | Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens (source tierce, à vérifier) | Alternative à Albert, hébergée en France |
| Open WebUI (fenêtre de l'assistant) | Open source | Non | Gratuit | Fenêtre de discussion pour les agents |
| faster-whisper (transcription locale) | Open source | Non | Gratuit (tourne sur le serveur) | Comptes rendus de réunion sans faire sortir le son |
| n8n (automates) | n8n GmbH, Allemagne | Non (auto-hébergé) | Gratuit — une instance par client | Automatisation des comptes rendus |
| Baserow (base de données) | Baserow B.V., Pays-Bas | Non (option Premium) | Gratuit ; Premium ≈ 10 $/utilisateur/mois (source tierce) | Cartographie des usages IA |
| Logiciel PIA | CNIL, France | Non | Gratuit | Analyse d'impact si données sensibles |
| La Suite numérique (Visio, Tchap) | DINUM, France | Non (secteur public) | Gratuit [À VÉRIFIER] | Visio et transcription déjà proposées par l'État |

Les prix sont ceux d'octobre 2026, à reconfirmer avant devis. Aucun outil américain n'est utilisé pour traiter des données : souveraineté européenne.

## 5. Les solutions mises en place

Chaque solution est détaillée pas à pas (recette reproductible en entreprise, consigne donnée à l'IA, points RGPD / IA Act) dans `00-catalogue-ia-et-solutions.md`.

- **S7 — Kit conformité RGPD & IA Act** : Cœur de la mission : audit, cartographie, charte, mesures de maîtrise de l'IA (art. 4).
- **S1 — Assistant IA souverain avec les documents de la structure** : Option : assistant nourri des procédures internes et délibérations publiques.
- **S2 — Comptes rendus de réunion automatiques** : Option : comptes rendus des réunions de service et commissions.
- **S6 — Chatbot public transparent** : Option : chatbot d'accueil du site, avec mention « assistant automatique ».
- **S11 — Socle de sécurité** : Socle de sécurité si la collectivité héberge la plateforme.

## 6. Déroulé de la mission

| Période | Ce qui se passe | Livrable |
|---|---|---|
| Semaines 1-3 | Audit des usages : entretiens par service, questionnaire anonyme aux agents | Cartographie IA classée |
| Semaines 4-5 | Charte d'usage avec le DPO, liste des outils autorisés | Charte + registre à jour |
| Semaines 6-11 | 6 sessions de formation d'une journée | Agents formés, attestations |
| Semaine 12 | Restitution aux élus et à la direction | Plan d'action 12 mois |

## 7. Indicateurs de résultat

- Charte adoptée par l'exécutif
- 100 % des usages IA cartographiés et classés
- Part des agents formés
- Temps gagné déclaré par les agents (questionnaire avant / après)
- Zéro donnée personnelle saisie dans un outil non autorisé (contrôle à 6 mois)

## 8. RGPD et IA Act

- **RGPD** : Collectivité = responsable de traitement ; vous êtes sous-traitant (art. 28) si vous hébergez ou traitez des données. Le DPO est associé dès le début. Aucune donnée d'administré dans les exercices de formation.
- **IA Act** : Art. 4 : la formation constitue une mesure de maîtrise de l'IA documentée. Art. 50 : transparence de tout outil ouvert au public. Annexe III (haut risque, au 02/12/2027) : à vérifier si l'IA intervient dans l'accès à des prestations sociales ou à des services publics essentiels.

---

## 9. Mise en place technique — ordre d'exécution *(pour Aurélien, ne pas transmettre)*

Installation de la plateforme : `00-guide-installation-plateforme.md` (étapes 0 à 20). Spécifique à cette structure :

1. Avant le rendez-vous : préparer la grille d'audit (table Baserow « Usages IA ») sur votre propre plateforme.
2. Signature : bon de commande + contrat de sous-traitance RGPD.
3. Audit : questionnaire en ligne (formulaire Baserow), puis entretiens.
4. Si l'option assistant est retenue : la collectivité commande son VPS (guide, étape 2) et demande un accès Albert à la DINUM ; vous déroulez le guide, étapes 1 à 15, puis l'étape 17.
5. Formation : supports en gros caractères, exercices sur documents fictifs.

## 10. Questions à poser au rendez-vous

- Qui est votre DPO (interne ou mutualisé) ?
- Avez-vous déjà une charte informatique à compléter ?
- Vos agents ont-ils accès à La Suite numérique ou à Albert ?
- Votre site a-t-il un chatbot ? Est-il signalé comme tel ?

## 11. Risques et parades

| Risque | Parade |
|---|---|
| Fractionnement (découper pour rester sous 60 000 €) | Un seul besoin, un seul bon de commande, chiffré honnêtement |
| Résistance des agents (« on va nous surveiller ») | Questionnaire anonyme, discours sur le gain de temps |
| Accès Albert non ouvert | Basculer sur l'API Mistral, avec DPA signé |

## Sources

- outremers360.com (présidents d'intercommunalités 2026)
- blog.landot-avocats.net (seuil de 60 000 €)
- aiactinsight.eu (Omnibus IA Act)
- Détail des URL : onglet « Preuves » du classeur `Prospection_Acteurs_Formation_Reunion.xlsx`.

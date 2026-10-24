# France Travail — Direction régionale La Réunion

> **Décideur identifié** : Francicia COURTOIS — Directrice régionale depuis le 01/04/2026 (adjointe opérations : Astrid COMBEMOREL)  
> **Fiabilité de l'information** : Bulletin officiel de France Travail 2026  
> Tout ce qui est marqué [À VÉRIFIER] doit être confirmé (appel au standard) avant l'envoi.

---

## 1. Le courriel (prêt à envoyer)

**À :** Direction régionale — Centre d'affaires Cadjee, Bât. C, 62 bd du Chaudron, CS 52008, 97744 Saint-Denis Cedex 9  
**Objet :** « Embauche augmentée 974 » : des parcours courts avec des employeurs déjà engagés, pour transformer chaque formation en embauche  
**Pièces jointes :** CV d'Aurélien LUMEKA · Note de proposition (parties 2 à 8 de ce mémo, en PDF)

> Madame la Directrice régionale,  
>
> Avec un chômage remonté à 19 % au deuxième trimestre 2026 et des crédits nationaux en baisse de 12 %, chaque euro de formation doit produire une embauche. Je vous adresse mes félicitations pour votre prise de fonctions, et une proposition concrète pour y contribuer.  
>
> « Embauche augmentée 974 » est un dispositif de 18 mois dans lequel j'apporte les deux bouts de la chaîne :  
>
> • les employeurs : je prospecte chaque semaine des TPE-PME réunionnaises ; j'arrive avec leurs offres d'emploi et leur engagement d'embauche, avant même l'entrée en formation ;  
> • des parcours courts (environ 100 heures), par cohortes de 12 : relation client, vente, savoir-être professionnel, et les outils d'IA du quotidien (rédiger un email, préparer un devis, répondre à un client), pour des candidats opérationnels dès le premier jour ;  
> • une immersion en entreprise pendant le parcours ;  
> • un suivi à 3 et 6 mois : vous fixez avec moi l'objectif de sortie en emploi, et vous le mesurez, cohorte par cohorte.  
>
> Ce dispositif s'appuie sur les outils que vous connaissez — POEI et AFPR en agence, POEC avec l'OPCO de la branche — sans création de procédure nouvelle. En parallèle, je propose aux employeurs TPE des ateliers « Recruter mieux, sans discriminer », qui alimentent vos offres d'emploi.  
>
> Chef des ventes pendant 15 ans et formateur en vente et management, je connais le terrain des TPE réunionnaises. YEBA FORMATIONS est certifié Qualiopi ; je suis Référent handicap, et je me consacre depuis 2026 à l'IA appliquée et à la conformité RGPD / IA Act.  
>
> Pourrions-nous en parler 30 minutes avec vos responsables formation et relation entreprises, le [date 1] ou le [date 2] ? Mon CV et une note de proposition sont joints.  
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

- Chômage BIT : 19 % au T2 2026 (+3 points en un an).
- Crédits France Travail 2026 : -12 % (subvention 1,16 Md€ contre 1,35 Md€).
- Loi pour le plein emploi : accompagnement intensif des inscrits.
- Nouvelle directrice régionale depuis le 01/04/2026.

## 3. Comment je vous aide — expliqué simplement

*(comme à un enfant de 5 ans)*

> Beaucoup de gens cherchent du travail, et beaucoup de petites entreprises cherchent quelqu'un. Mais ils ne se trouvent pas, comme deux enfants qui jouent à cache-cache dans des pièces différentes. Moi, je vais voir les entreprises et je leur demande : « De qui as-tu besoin ? » Puis j'apprends aux personnes qui cherchent du travail exactement ce que l'entreprise attend : parler aux clients, être à l'heure, et se servir d'un petit robot qui aide à écrire. À la fin, l'entreprise embauche la personne. Et on compte combien de personnes ont trouvé un travail.

## 4. Les IA et outils utilisés

| Outil | Éditeur, pays | Payant ? | Prix indicatif | Pourquoi ici |
|---|---|---|---|---|
| Le Chat Pro / Team (« Vibe » [À VÉRIFIER]) | Mistral AI, France | Oui | Pro ≈ 14,99 $/mois ; Team ≈ 24,99 $/utilisateur/mois [À VÉRIFIER] | Outil enseigné aux stagiaires (offre payante) |
| API Mistral (La Plateforme) | Mistral AI, France | Oui, à l'usage | Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens (source tierce, à vérifier) | Exercices et automatisations |
| Baserow (base de données) | Baserow B.V., Pays-Bas | Non (option Premium) | Gratuit ; Premium ≈ 10 $/utilisateur/mois (source tierce) | Suivi des cohortes, des employeurs et des sorties en emploi |
| n8n (automates) | n8n GmbH, Allemagne | Non (auto-hébergé) | Gratuit — une instance par client | Suivi automatique à 3 et 6 mois |
| Brevo (emails) | Brevo, France | Gratuit puis payant | 300 emails/jour gratuits ; Starter ≈ 9 $/mois | Emails de suivi |

Les prix sont ceux d'octobre 2026, à reconfirmer avant devis. Aucun outil américain n'est utilisé pour traiter des données : souveraineté européenne.

## 5. Les solutions mises en place

Chaque solution est détaillée pas à pas (recette reproductible en entreprise, consigne donnée à l'IA, points RGPD / IA Act) dans `00-catalogue-ia-et-solutions.md`.

- **S4 — Base de pilotage / CRM** : Base « employeurs ↔ offres ↔ cohortes ↔ candidats » pour piloter le dispositif.
- **S3 — Parcours administratif automatisé (inscriptions, convocations, enquêtes)** : Convocations, émargement, enquêtes et suivi à 3 et 6 mois automatisés.
- **S5 — Tableau de bord et rapport automatique** : Rapport automatique des sorties en emploi par cohorte.
- **S9 — Recrutement responsable assisté (sans tri automatique)** : Ateliers employeurs : annonces et entretiens structurés, sans tri automatique des candidats.
- **S8 — Accessibilité et FALC** : Supports accessibles (publics éloignés, handicap).

## 6. Déroulé de la mission

| Période | Ce qui se passe | Livrable |
|---|---|---|
| Mois 1-2 | Prospection des employeurs, montage de la 1re cohorte avec l'agence | Offres d'emploi engagées |
| Mois 3-17 | 6 cohortes de 12 (environ 15 jours chacune) + immersions | 72 candidats formés |
| +3 et +6 mois | Suivi automatisé | Taux de sortie en emploi |
| Mois 18 | Bilan | Rapport et préconisations |

## 7. Indicateurs de résultat

- Taux de sortie en emploi à 6 mois (cible fixée avec France Travail)
- Taux d'abandon < 10 %
- Nombre d'employeurs engagés
- Délai entre offre et embauche

## 8. RGPD et IA Act

- **RGPD** : Données des candidats (dont RQTH = donnée de santé, art. 9) : convention avec France Travail, minimisation, accès restreint.
- **IA Act** : Aucun outil ne classe ni n'oriente les candidats (le profilage de demandeurs d'emploi serait à haut risque, annexe III). Décisions 100 % humaines.

---

## 9. Mise en place technique — ordre d'exécution *(pour Aurélien, ne pas transmettre)*

Installation de la plateforme : `00-guide-installation-plateforme.md` (étapes 0 à 20). Spécifique à cette structure :

1. Votre plateforme : guide, étapes 0 à 19.
2. Tables Baserow : Employeurs, Offres, Cohortes, Candidats (minimum de données), Suivi.
3. Automatisations A2 et A3.
4. Prospection des employeurs (automatisation A6) avant chaque cohorte.
5. Montage administratif POEI / POEC avec l'agence et l'OPCO.

## 10. Questions à poser au rendez-vous

- Quels métiers ou secteurs souhaitez-vous prioriser ?
- Quelles agences sont les plus en tension ?
- Comment l'objectif de sortie en emploi est-il mesuré chez vous ?

## 11. Risques et parades

| Risque | Parade |
|---|---|
| Pas d'employeurs engagés à temps | Démarrer la prospection 2 mois avant chaque cohorte |
| Achats encadrés | S'appuyer sur la POEI / AFPR, décidées en agence offre par offre |

## Sources

- bo.francetravail.org (BO 2026)
- assemblee-nationale.fr (CF1896)
- insee.fr ; outremers360.com
- Détail des URL : onglet « Preuves » du classeur `Prospection_Acteurs_Formation_Reunion.xlsx`.

# Département de La Réunion

> **Décideur identifié** : Cyrille MELCHIOR — Président du Conseil départemental [À VÉRIFIER]  
> **Fiabilité de l'information** : Wikipédia (non daté) — à reconfirmer  
> Tout ce qui est marqué [À VÉRIFIER] doit être confirmé (appel au standard) avant l'envoi.

---

## 1. Le courriel (prêt à envoyer)

**À :** Hôtel du Département (Palais de la Source), 2 rue de la Source, 97400 Saint-Denis  
**Objet :** Bénéficiaires du RSA : un parcours de 12 mois pour une remise en mouvement durable  
**Pièces jointes :** CV d'Aurélien LUMEKA · Note de proposition (parties 2 à 8 de ce mémo, en PDF)

> Monsieur le Président,  
>
> La loi du 18 décembre 2023 pour le plein emploi impose désormais une activité hebdomadaire réelle aux bénéficiaires du RSA. Le Département a porté 99 000 actions individuelles et collectives sur son précédent plan d'insertion : le défi n'est plus le volume, c'est la remise en mouvement durable de personnes souvent très éloignées de l'emploi — sur un territoire où l'illettrisme touche près de trois fois plus de personnes qu'en métropole.  
>
> Je vous propose « Remobilisation & autonomie numérique », un parcours de 12 mois organisé dans les quatre micro-régions :  
>
> • 8 cohortes de 12 personnes, 10 journées par cohorte ;  
> • confiance en soi et codes de l'entreprise, par le jeu et la mise en situation ;  
> • autonomie numérique : le smartphone, les démarches en ligne, et un assistant d'IA pour rédiger une lettre ou préparer un entretien ;  
> • des supports accessibles et des consignes simplifiées (Facile à lire et à comprendre) ;  
> • un bilan mensuel transmis à vos services : présence, entrées en emploi ou en formation qualifiante.  
>
> Je propose de commencer par un pilote sur un territoire, avec des indicateurs mensuels, afin que vos équipes jugent sur pièces.  
>
> Formateur en soft skills, vente et management, Référent handicap, YEBA FORMATIONS est certifié Qualiopi. Je me consacre également à l'IA responsable et à la protection des données : les personnes accompagnées n'auront jamais à confier leur situation à un outil d'IA.  
>
> Pourriez-vous m'indiquer quel service pilote le prochain appel à projets insertion ? Je serais heureux de le présenter le [date 1] ou le [date 2]. Mon CV et une note de proposition sont joints.  
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

- Plan départemental d'insertion 2022-2024 : 99 000 actions prévues.
- Loi plein emploi : durée d'activité hebdomadaire minimale.
- Illettrisme ≈ 3 fois la métropole (données anciennes, ordre de grandeur).

## 3. Comment je vous aide — expliqué simplement

*(comme à un enfant de 5 ans)*

> Certaines personnes n'ont pas travaillé depuis longtemps, et elles ont un peu perdu confiance, comme quelqu'un qui n'a pas fait de vélo depuis des années. Moi, je les aide à remonter sur le vélo, doucement, avec des jeux. On apprend aussi à se servir du téléphone pour faire les papiers, et un petit robot aide à écrire une lettre pour un patron. Mais on ne raconte jamais nos secrets au robot. Chaque mois, je dis au Département combien de personnes sont venues et combien ont trouvé un travail ou une formation.

## 4. Les IA et outils utilisés

| Outil | Éditeur, pays | Payant ? | Prix indicatif | Pourquoi ici |
|---|---|---|---|---|
| Le Chat Pro / Team (« Vibe » [À VÉRIFIER]) | Mistral AI, France | Oui | Pro ≈ 14,99 $/mois ; Team ≈ 24,99 $/utilisateur/mois [À VÉRIFIER] | Démonstration d'un assistant pour rédiger lettre et CV (sans donnée personnelle sensible) |
| API Mistral (La Plateforme) | Mistral AI, France | Oui, à l'usage | Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens (source tierce, à vérifier) | Réécriture des supports en FALC |
| Baserow (base de données) | Baserow B.V., Pays-Bas | Non (option Premium) | Gratuit ; Premium ≈ 10 $/utilisateur/mois (source tierce) | Suivi de présence et des sorties |
| n8n (automates) | n8n GmbH, Allemagne | Non (auto-hébergé) | Gratuit — une instance par client | Rappels de séance par SMS ou email, bilan mensuel |
| NVDA (lecteur d'écran) | NV Access, open source | Non | Gratuit | Accessibilité |

Les prix sont ceux d'octobre 2026, à reconfirmer avant devis. Aucun outil américain n'est utilisé pour traiter des données : souveraineté européenne.

## 5. Les solutions mises en place

Chaque solution est détaillée pas à pas (recette reproductible en entreprise, consigne donnée à l'IA, points RGPD / IA Act) dans `00-catalogue-ia-et-solutions.md`.

- **S8 — Accessibilité et FALC** : Supports et consignes en FALC, relus par des personnes concernées.
- **S3 — Parcours administratif automatisé (inscriptions, convocations, enquêtes)** : Rappels avant chaque séance (réduit l'absentéisme) et émargement.
- **S5 — Tableau de bord et rapport automatique** : Bilan mensuel automatique pour le Département.
- **S4 — Base de pilotage / CRM** : Suivi des parcours avec un minimum de données.

## 6. Déroulé de la mission

| Période | Ce qui se passe | Livrable |
|---|---|---|
| Mois 1 | Pilote : 1 territoire, 1 cohorte | Bilan du pilote |
| Mois 2-12 | 7 cohortes supplémentaires dans les 4 micro-régions | 96 personnes accompagnées |
| Chaque mois | Bilan automatique | Indicateurs |
| +6 mois | Suivi des sorties | Taux d'entrée en emploi ou formation |

## 7. Indicateurs de résultat

- Taux de présence ≥ 80 %
- Entrées en emploi ou formation qualifiante à 6 mois
- Progression de l'autonomie numérique (grille avant / après)
- Satisfaction des participants

## 8. RGPD et IA Act

- **RGPD** : Données sociales (RSA) très sensibles : convention de traitement, AIPD recommandée (logiciel PIA), hébergement à valider avec le Département (un hébergement qualifié SecNumCloud peut être exigé).
- **IA Act** : Aucun usage d'IA sur la situation des personnes (l'accès aux prestations sociales relève du haut risque, annexe III).

---

## 9. Mise en place technique — ordre d'exécution *(pour Aurélien, ne pas transmettre)*

Installation de la plateforme : `00-guide-installation-plateforme.md` (étapes 0 à 20). Spécifique à cette structure :

1. Clarifier avec le Département l'exigence d'hébergement (SecNumCloud ou non) avant tout chiffrage.
2. Tables Baserow : Participants (minimum), Séances, Présences, Sorties.
3. Automatisations A2 (rappels) et A3 (bilan).
4. Réécriture FALC des supports (A5) et relecture humaine.
5. AIPD avec le logiciel PIA.

## 10. Questions à poser au rendez-vous

- Quel est le calendrier du prochain appel à projets insertion ?
- Quelles exigences d'hébergement pour les données des bénéficiaires ?
- Quels territoires sont prioritaires ?

## 11. Risques et parades

| Risque | Parade |
|---|---|
| Public fragile, absentéisme | Rappels automatiques, pédagogie par le jeu, relais avec les référents sociaux |
| Exigence SecNumCloud | Ne pas héberger de données sociales sur un VPS classique ; suivi papier ou outil du Département |

## Sources

- outremers360.com (PDI)
- insee.fr (illettrisme)
- Détail des URL : onglet « Preuves » du classeur `Prospection_Acteurs_Formation_Reunion.xlsx`.

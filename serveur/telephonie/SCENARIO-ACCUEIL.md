# Accueil téléphonique automatique — scénario « IFA » (YEBA FORMATIONS)

Statut : **scénario prêt, non branché**. Aucun numéro, aucun opérateur ni abonnement n'est engagé.
Document public : aucun secret ni numéro personnel ici.

## Phrases (à faire lire par une voix de synthèse française)

**Accueil**
> « YEBA FORMATIONS, bonjour ! Bienvenue sur la plateforme d'accueil. Je suis IFA, l'assistant virtuel automatique
> de YEBA FORMATIONS : vous parlez à un système automatisé, pas à une personne. Cet appel n'est pas enregistré.
> Tapez le chiffre dont vous avez besoin. Tapez 1 pour les programmes et informations sur les formations.
> Tapez 2 pour les horaires de formation. Tapez 3 pour prendre rendez-vous. Tapez 0 pour laisser un message à Aurélien. »

**1 — Programmes** : proposer d'envoyer par SMS/mail le lien vers le catalogue (page publique du site), jamais de tarif
oral si le bloc public de la fiche commence par ⛔ (règle CONFIG SYSTEME).

**2 — Horaires**
> « Les formations ont lieu de 8 heures à 16 heures, avec une pause méridienne de 12 heures à 13 heures. »
(horaires donnés par Aurélien ; à adapter session par session)

**3 — Rendez-vous** : choix du sujet (1 formation, 2 automatisation / IA, 3 gouvernance d'entreprise RGPD et IA Act),
puis nom, numéro de rappel, créneau souhaité. Message de fin : « Aurélien vous rappelle pour confirmer. »

## Pourquoi j'ai modifié ta formulation (obligations légales)
- **IA Act, art. 50** : toute personne qui interagit avec un système d'IA doit être informée qu'il s'agit d'une IA
  (sauf évidence). « Je suis IFA » ne suffit pas : la phrase dit « assistant virtuel automatique ».
- **RGPD, art. 13** : l'option 3 collecte un nom et un numéro. Il faut une information au moment de la collecte :
  finalité (te rappeler), durée de conservation (proposition : 3 mois sans suite), contact, droits.
  Phrase à ajouter avant l'option 3 : « Vos coordonnées servent uniquement à vous rappeler et sont supprimées sous
  trois mois. Détails sur le site, page confidentialité. »
- **Pas d'enregistrement audio** : sinon consentement et durée de conservation à prévoir.

## Branchement (décisions à prendre par Aurélien)
1. Le numéro 06 est un mobile : il ne peut pas porter lui-même un serveur vocal. Il faut un **numéro virtuel** et
   un **renvoi d'appel** (sur occupation / sans réponse) depuis le mobile vers ce numéro.
2. Choix de l'opérateur voix : à valider (coût mensuel, numéro disponible, hébergement des données en UE).
3. Où est stockée la demande de rendez-vous : ligne `Source = Téléphone` dans BOÎTE DE RÉCEPTION (Airtable).

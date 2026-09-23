# Plateforme YEBA — architecture cible et cadre juridique

Version 1.0 — 23/09/2026. Décisions validées par Aurélien LUMEKA le 23/09/2026.
Document interne : ne contient aucune donnée personnelle.

> Chaque point est étiqueté **[RGPD]**, **[IA Act]** ou **[Qualiopi]** quand il en relève.

---

## 1. Deux produits, deux fondations

| | Outil interne YEBA (back-office) | Plateforme vendue aux centres (SaaS + mise en relation) |
|---|---|---|
| Rôle | Gérer YEBA FORMATIONS au quotidien | Passeport Formateur Conforme + gestion pour d'autres centres |
| Fondation | **Baserow auto-hébergé chez OVHcloud** (France) | **PostgreSQL hébergé en France** (OVHcloud) + application web |
| Pourquoi | Migration rapide depuis Airtable, même logique de tables | Baserow ne sait pas cloisonner proprement les données d'un client à l'autre |
| Statut RGPD de YEBA | Responsable de traitement | **Sous-traitant** (art. 28) pour les données des stagiaires des centres clients ; responsable de traitement pour les comptes formateurs |

**Écarté : Firebase.** Service de Google LLC, soumis au CLOUD Act américain même hébergé en UE, et base « documents » mal adaptée aux relations entre tables (sessions ↔ inscriptions ↔ émargements). Incompatible avec l'exigence de souveraineté YEBA **[RGPD, art. 44 et suivants]**.

---

## 2. Architecture technique de la plateforme

```
Navigateur (centre / formateur / YEBA)
        │ HTTPS (TLS 1.3), cookies de session HttpOnly + Secure + SameSite=Strict
        ▼
Application web (OVHcloud, France)
  ├─ Authentification : mot de passe + double authentification obligatoire pour les comptes centres
  ├─ Contrôle d'accès par rôle : YEBA-admin / centre / formateur
  └─ Journal d'audit : qui a consulté ou modifié quoi, quand (non modifiable)
        │
        ▼
PostgreSQL (OVHcloud, France)
  ├─ Cloisonnement STRICT par client : colonne « centre_id » sur chaque table
  │   + Row Level Security activée → un centre ne peut techniquement pas lire les lignes d'un autre
  ├─ Chiffrement au repos (disques) + chiffrement applicatif des champs sensibles
  └─ Sauvegardes chiffrées, 3-2-1, test de restauration trimestriel
        │
        ├─ Stockage objets (OVHcloud Object Storage, France) : PDF, pièces du passeport
        │   URL signées à durée courte, jamais de lien public permanent
        ├─ Yousign (France) : signature électronique des conventions, contrats, autorisations de partage
        ├─ Brevo (France) : envoi des courriels transactionnels (mis en place par Aurélien)
        └─ Indy (plateforme agréée, compte existant) : facturation électronique
```

Règles non négociables :
1. **Aucune donnée de production dans un environnement de test.** Données fictives uniquement.
2. **Secrets** (clés API Brevo, Yousign, Indy) dans un coffre ou des variables d'environnement, jamais dans le code ni dans Git.
3. **Réversibilité** : export complet des données d'un centre en CSV + PDF sur simple demande (fin de contrat, art. 28-3 g RGPD).
4. **Mesure d'audience** : Matomo auto-hébergé, configuré selon la liste d'exemption de la CNIL (pas de consentement requis). Bandeau cookies **uniquement** si des cookies non essentiels sont ajoutés un jour.

---

## 3. Juridique propre à la plateforme

| Document | Fondement | Contenu clé |
|---|---|---|
| **Contrat de sous-traitance RGPD** avec chaque centre client | RGPD art. 28 | Objet, durée, nature des traitements, sous-traitants ultérieurs (OVHcloud, Brevo, Yousign), sécurité, notification de violation sous 48 h, restitution / suppression en fin de contrat |
| **CGU de la plateforme** | Droit commun + C. conso L.111-7 | Rôle d'intermédiaire, critères de classement des formateurs rendus publics, absence de lien capitalistique ou de rémunération influençant le classement |
| **Conditions P2B** | Règlement (UE) 2019/1150 | Pour les formateurs professionnels inscrits : motifs de suspension, préavis de 30 jours avant résiliation, paramètres de classement, système interne de traitement des plaintes |
| **Déclaration DAC7** | Directive (UE) 2021/514, CGI art. 1649 ter A à E | Déclaration annuelle à l'administration fiscale des revenus perçus par les formateurs via la plateforme, et information de chaque formateur |
| **Paiements** | Code monétaire et financier | Si l'argent d'un tiers transite par YEBA → obligatoirement via un prestataire agréé (ex. **Mangopay, Luxembourg**). YEBA ne doit jamais encaisser pour le compte d'autrui sur son propre compte |
| **Politique de confidentialité plateforme** | RGPD art. 13 et 14 | Distincte de celle du centre de formation |

**[IA Act]** Si un algorithme **classe ou recommande des formateurs** pour une mission, il peut relever de l'annexe III, point 4 (relations de travail, attribution de tâches). Règle YEBA : l'outil **propose**, le centre **décide** ; critères affichés ; aucun classement automatique fondé sur des traits personnels. Obligations haut risque applicables au 02/12/2027 (règlement (UE) 2026/1744).

---

## 4. Le « Passeport Formateur Conforme »

### Le problème résolu
Depuis le référentiel Qualiopi V10 (décret n° 2026-728, audits au 01/11/2026), **l'indicateur 27** exige que la vérification de conformité du sous-traitant (et du salarié porté) soit **tracée dans le contrat de sous-traitance**. Aujourd'hui, chaque formateur indépendant renvoie les mêmes pièces à chaque centre, qui les archive séparément et ne suit pas leur expiration. **[Qualiopi]**

### La solution
Un dossier de preuves **vérifié une fois**, **partagé sur autorisation** du formateur, **révocable**, avec alerte d'expiration.

### Prototype en place (Airtable, base YEBA, 23/09/2026)
- `PASSEPORT FORMATEUR — PIÈCES` : une ligne par pièce, type limité à 12 catégories, date d'expiration, statut de vérification, **méthode de vérification**, indicateurs RNQ prouvés, validité calculée (alerte à 30 jours).
- `PASSEPORT — AUTORISATIONS DE PARTAGE` : formateur → centre → pièces → finalité → date → preuve → révocation.
- Fiche formateur : compteur « 🛂 Passeport — nb pièces valides » (socle attendu : 8).

### Socle de pièces d'un sous-traitant (8)
CV daté et signé · diplôme ou certification · attestation URSSAF de vigilance (< 6 mois, contrats ≥ 5 000 € HT, c. trav. L.8222-1 et D.8222-5) · avis de situation SIRENE · attestation RC Pro · charte IA YEBA v1.1 signée · contrat de sous-traitance avec clause RNQ · accord RGPD art. 28.

### Interdits **[RGPD]**
Casier judiciaire (art. 10) · données de santé (art. 9) · copie de pièce d'identité conservée après vérification · numéro de sécurité sociale.

### Modèle économique (hypothèse à valider auprès de 5 centres réunionnais avant tout développement)
- Formateur : gratuit (il apporte les pièces).
- Centre : abonnement pour consulter les passeports autorisés et recevoir les alertes d'expiration.
- Mise en relation : les centres qui viennent pour la conformité trouvent ensuite des formateurs vérifiés.

---

## 5. Les trois modules d'accompagnement

1. **Registre « mesures IA » pour TPE** **[IA Act art. 4, rédaction 2026/1744]** — inventaire des outils d'IA utilisés, mesures prises (formation, charte, fiche de poste), preuves. Alimente naturellement ALLUMAGE-TURBO. Argument : « nous vous aidons à prouver les mesures prises » — jamais « formation obligatoire ».
2. **Trésorerie après la fin de la subrogation OPCO (01/10/2026)** — suivi des demandes de remboursement OPCO et échéancier du reste à charge. **Limite** : faire crédit ou encaisser pour le compte de tiers est réglementé ; toute fonction de paiement passe par un prestataire agréé.
3. **Séminaires « clé en main » avec les hôtels en basse saison** — partage de revenus. **Non chiffré** : il manque les contacts hôteliers et les taux de remplissage.

---

## 6. Prochaines étapes (ordre recommandé)

1. Interroger 5 centres de formation réunionnais sur le Passeport (15 jours).
2. Migrer l'outil interne vers Baserow sur OVHcloud (schéma identique, sans les champs supprimés).
3. Brevo : domaine d'envoi + SPF/DKIM/DMARC, puis remplacement de Gmail dans les automatisations.
4. Rédiger les 5 documents juridiques de la plateforme (section 3) avant la première inscription d'un centre.
5. Développer le Passeport sur PostgreSQL (France) une fois la demande validée.

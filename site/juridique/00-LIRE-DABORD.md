# Pack juridique du site — mode d'emploi

Cinq documents à publier avant toute mise en ligne. Ils couvrent ce qui peut
réellement te mettre en difficulté : identification de l'éditeur, données
personnelles, cookies, et surtout **les règles propres à la vente de formation
à un particulier**, que la quasi-totalité des sites d'organismes ignore.

| Fichier | Obligation | Sanction encourue si absent |
|---|---|---|
| `mentions-legales.md` | LCEN art. 6 III | Jusqu'à 75 000 € d'amende et 1 an d'emprisonnement pour une personne physique |
| `politique-confidentialite.md` | RGPD art. 12 à 14 | Amende administrative CNIL |
| `politique-cookies.md` + bandeau | RGPD + art. 82 loi Informatique et Libertés | La CNIL a déjà sanctionné lourdement des manquements cookies |
| `cgv.md` | Code de la consommation + Code du travail | Nullité de clauses, remboursement, litiges |
| `contrat-formation-particulier.md` | Code du travail art. L6353-3 à L6353-7 | **Nullité du contrat** |

---

## ⚠️ Le point que presque personne ne respecte

Quand **une personne physique finance elle-même** sa formation (pas son
employeur, pas un OPCO, pas France Travail), tu ne signes pas une convention de
formation : tu signes un **contrat de formation professionnelle**, régi par les
articles L6353-3 à L6353-7 du Code du travail. Il impose :

1. **Un délai de rétractation de 10 jours** à compter de la signature, par
   lettre recommandée avec avis de réception.
2. **Aucune somme exigible avant l'expiration de ce délai.** Aucune. Pas
   d'acompte, pas de « frais de dossier », pas de « réservation ».
3. **Au maximum 30 % du prix** encaissables à l'expiration du délai.
4. **Le solde échelonné** au fur et à mesure du déroulement de l'action.
5. Des **clauses obligatoires** : nature, durée, programme et objet de
   l'action ; niveau de connaissances préalables ; conditions de déroulement ;
   diplômes et titres des formateurs ; modalités de paiement et conditions
   financières en cas de cessation anticipée ou d'abandon.

*(Sources : [Légifrance, art. L6353-3 à L6353-7](https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006189927) ·
[art. L6353-5](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006904415) ·
[DREETS Occitanie](https://occitanie.dreets.gouv.fr/Quand-un-particulier-achete-une-formation-professionnelle-continue) ·
[Centre Inffo](https://www.centre-inffo.fr/site-droit-formation/actualites-droit/le-droit-de-retractation-et-le-contrat-de-formation-professionnelle))*

**Un bouton « Payer et réserver ma place » sur ton site, pour un particulier,
est illégal en l'état.** C'est le risque n°1 de ton projet, très au-dessus de
n'importe quelle faille technique. Le parcours doit être : demande d'inscription
→ envoi du contrat → signature → 10 jours → encaissement de 30 % maximum.

> Ne confonds pas avec le droit de rétractation de 14 jours du Code de la
> consommation : ce sont deux régimes distincts. Pour la formation
> professionnelle achetée par un particulier, c'est le délai de 10 jours du Code
> du travail qui s'applique. En cas de doute sur l'articulation des deux sur une
> vente en ligne, fais trancher par un avocat — c'est le seul point de ce pack
> où je te recommande formellement de ne pas te fier à un document type.

---

## Informations qu'il me manque pour finaliser

Chaque occurrence de `[[…]]` dans les documents est un trou à combler. Liste
complète :

| Marqueur | Ce qu'il faut | Où le trouver |
|---|---|---|
| `[[FORME_JURIDIQUE]]` | SARL, SASU, EURL, entreprise individuelle… | Extrait Kbis |
| `[[CAPITAL]]` | Montant du capital social (ou « sans capital social » si EI) | Kbis |
| `[[RCS]]` | Ville et numéro d'immatriculation RCS | Kbis |
| `[[ADRESSE_SIEGE]]` | Adresse postale complète du siège | Kbis |
| `[[TELEPHONE]]` | Numéro de téléphone de contact | — |
| `[[TVA_INTRA]]` | Numéro de TVA intracommunautaire, ou mention du régime | Comptable |
| `[[REGIME_TVA]]` | Franchise en base (art. 293 B) **ou** exonération formation (art. 261-4-4° a) — **pas les deux** | Comptable |
| `[[HEBERGEUR]]` | Nom, raison sociale, adresse et téléphone de l'hébergeur | À l'issue du choix (OVHcloud, Infomaniak…) |
| `[[MEDIATEUR]]` | Nom, adresse et site du médiateur de la consommation | Adhésion à souscrire |
| `[[ASSUREUR_RCP]]` | Assureur en responsabilité civile professionnelle et n° de police | Contrat d'assurance |
| `[[DELAI_ACCES]]` | Délai moyen d'accès à la formation | Tes programmes indiquent 10 jours ouvrés |

### La médiation de la consommation n'est pas optionnelle

Si tu vends, ne serait-ce qu'une fois, à un **particulier** (CPF, financement
personnel), tu dois **adhérer à un médiateur de la consommation agréé** et
publier ses coordonnées. C'est une obligation légale, contrôlée par la DGCCRF,
et son absence est sanctionnable. Coût courant : quelques dizaines à quelques
centaines d'euros par an. **À faire avant la mise en ligne**, pas après.

---

## RGPD & IA Act — signalé spontanément

- **Formulaire de contact et de pré-inscription** = traitement de données
  personnelles. Finalité, base légale, durée de conservation et information
  doivent être écrites : c'est fait dans `politique-confidentialite.md`.
- **Cookies de mesure d'audience** : consentement requis, **sauf** configuration
  exemptée par la CNIL. Le bandeau fourni traite les deux cas.
- **Si tu ajoutes un chatbot IA sur le site** : l'article 50 de l'AI Act impose
  d'informer clairement l'utilisateur qu'il parle à une machine. Applicable
  depuis le 2 août 2026. La mention est déjà prévue dans les documents.
- **Aucun tri ou scoring automatisé de candidats** ne doit être branché sur le
  formulaire sans réexamen : cela ferait basculer le traitement sous l'annexe III
  de l'AI Act et l'article 22 du RGPD.

---

## Ordre d'exécution recommandé

1. Rassembler les informations `[[…]]` ci-dessus.
2. Adhérer à un médiateur de la consommation.
3. Faire relire `cgv.md` et `contrat-formation-particulier.md` par un
   professionnel du droit — c'est là que se situe l'argent.
4. Publier les cinq documents, avec un lien vers chacun **dans le pied de page
   de toutes les pages**.
5. Installer le bandeau cookies **avant** tout script de mesure d'audience.
6. Appliquer les en-têtes de sécurité (`../securite/`).
7. Mettre en ligne.

> Ces documents sont des trames de travail conformes à l'état du droit au
> 9 septembre 2026. Ils ne constituent pas une consultation juridique. Sur les
> CGV et le contrat de formation, une relecture par un avocat est un
> investissement de quelques centaines d'euros face à un risque de plusieurs
> milliers.

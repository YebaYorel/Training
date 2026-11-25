# Comp AI × Brevo — correctif YEBA

Correctif qui fait envoyer les e-mails de Comp AI (github.com/trycompai/comp) par
**Brevo** (Sendinblue SAS, France) au lieu de Resend (États-Unis). Décision d'Aurélien
du 25/11/2026.

## Contenu

| Fichier | Rôle |
|---|---|
| `brevo.ts` | Adaptateur : même interface que le SDK Resend (`emails.send`, `batch.send`), appelle l'API Brevo `POST /v3/smtp/email` |
| `brevo.patch` | Correctif complet à appliquer sur Comp (5 fichiers) |

## Application

```bash
git clone --depth 1 https://github.com/trycompai/comp.git && cd comp
git apply /chemin/vers/Training/outils/comp/brevo.patch
```

Puis, dans `apps/app/.env`, `apps/portal/.env` et l'environnement de l'API :

```
BREVO_API_KEY=<clé API Brevo — jamais dans le dépôt>
RESEND_FROM_SYSTEM=YEBA Conformité <noreply@conformite.yebaformations.re>
RESEND_FROM_DEFAULT=YEBA Conformité <noreply@conformite.yebaformations.re>
# RESEND_API_KEY : laisser vide
```

Les noms `RESEND_FROM_*` sont conservés pour ne pas toucher au reste du code :
ils contiennent l'expéditeur Brevo.

## Comportement

- `BREVO_API_KEY` défini → Brevo. Sinon `RESEND_API_KEY` → Resend (comportement d'origine). Sinon erreur claire.
- E-mails React rendus en HTML avec `@react-email/render` (déjà dépendance de Comp).
- En-têtes conservés, dont la désinscription en un clic (`List-Unsubscribe`, RFC 8058).
- Pièces jointes converties en base64 ; envoi groupé = un appel par message.

## Tests

11 tests unitaires (API Brevo simulée) passés le 25/11/2026 : adresses, copie,
en-têtes, pièces jointes, identifiant de message, message vide, envoi groupé, erreur 400.
Non testé : la compilation complète du monorepo Comp et un envoi réel (il faut le
serveur, la clé API et un domaine authentifié dans Brevo).

## Prérequis Brevo (compte vérifié le 25/11/2026)

- Compte « YEBA FORMATIONS », offre gratuite : 300 e-mails par jour.
- **Aucun domaine authentifié** ; seul expéditeur : une adresse Gmail. Les messageries
  rejettent ou classent en indésirables un expéditeur `@gmail.com` envoyé par un tiers
  (DMARC). Il faut authentifier `yebaformations.re` dans Brevo (enregistrements DKIM,
  SPF et DMARC à ajouter chez l'hébergeur du domaine).

## Licence

Comp AI est sous AGPL-3.0 : ce correctif est publié ici (dépôt public), ce qui couvre
l'obligation de mise à disposition du code modifié si l'instance est ouverte à des clients.

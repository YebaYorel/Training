# Assistant vocal IA — YEBA FORMATIONS

## 1. Le raisonnement étape par étape

### Contraintes
| Contrainte | Conséquence |
|---|---|
| Souveraineté des données UE (votre exigence) | Pas de Vapi, Retell, Bland, Twilio (sociétés US, soumises au *Cloud Act*). |
| n8n **ne gère pas l'audio en temps réel** | Il faut un « moteur vocal » (téléphonie → reconnaissance vocale → IA → synthèse vocale) qui appelle n8n pour les **actions**. |
| Validation **obligatoire** par vous avant toute sous-traitance | L'assistant n'a pas accès à l'agenda en écriture ; seul votre clic de validation pose l'option. |
| Transfert vers vous si l'IA ne sait pas | Outil `transfert` + transfert SIP vers votre mobile. |
| IA Act art. 50 §1 + RGPD | Annonce « je suis une IA » dès la première phrase ; pas d'enregistrement audio ; résumé minimal. |
| Public en situation de handicap | Alternative écrite (email), transfert humain toujours possible, voix claire et lente. |

### Options évaluées
| Option | Souveraineté | Effort | Coût mensuel estimé | Verdict |
|---|---|---|---|---|
| **A. Pipecat (open source) auto-hébergé** chez Scaleway ou OVHcloud + **Mistral** (Voxtral pour la voix, Mistral pour le raisonnement) + **trunk SIP OVHcloud** | 🟢 tout en UE, éditeurs français | Élevé (un développeur, 3-5 j) | Serveur ≈ 20-40 € + minutes Mistral + ligne SIP (tarifs à vérifier) | ✅ **Recommandé** |
| B. Plateforme gérée « no-code » (ex. Synthflow, société de Berlin — un connecteur existe dans votre espace Claude) | 🟠 à vérifier : lieu d'hébergement, sous-traitants et modèles utilisés (souvent US) | Faible | Abonnement + minutes | Seulement après lecture de son DPA |
| C. Standard téléphonique français (Ringover, Aircall) + leur IA intégrée | 🟠 éditeurs français, mais modèles IA souvent US | Faible | Abonnement | Possible si DPA et localisation UE confirmés |

Sources : Mistral, Voxtral Realtime et Voxtral TTS — extraits de [docs.mistral.ai/studio/audio](https://docs.mistral.ai/studio/audio) ; services Mistral dans Pipecat — extraits de [docs.pipecat.ai (STT Mistral)](https://docs.pipecat.ai/api-reference/server/services/stt/mistral) et [TTS Mistral](https://docs.pipecat.ai/api-reference/server/services/tts/mistral) ; trunk SIP et portabilité — extrait de [ovhcloud.com/fr/phone/sip-trunk](https://www.ovhcloud.com/fr/phone/sip-trunk/).

## 2. Architecture retenue (option A)

```
Appelant ──► Votre numéro (porté chez OVHcloud, trunk SIP)
                 │
                 ▼
     Moteur vocal Pipecat (serveur Scaleway / OVH, France)
     · Voxtral Realtime (écoute)  · Mistral (raisonnement + outils)
     · Voxtral TTS (voix)          · prompt_systeme.md + outils_assistant.json
                 │  appel d'outil (HTTPS + secret)
                 ▼
     n8n auto-hébergé (même serveur UE)  ── workflow_n8n_assistant_yeba.json
     ├─ infos_formations ─► Baserow « Formations »
     ├─ inscription ──────► Baserow « Inscriptions » + email à vous
     ├─ sous_traitance ───► Baserow « Demandes sous-traitance » + email À VALIDER
     │                        └─ votre clic ✅ ─► page de confirmation ─► option dans l'agenda (CalDAV) + email au donneur d'ordre
     ├─ infos_legales ────► CGV / mentions / confidentialité (résumé + lien)
     └─ transfert ────────► renvoi d'appel vers votre mobile + email
     Fin d'appel ─────────► Baserow « Journal des appels » (résumé de 3 lignes, pas d'audio)
```

## 3. Mise en route (ordre conseillé)
1. **Baserow** : `python examples/creer_base_prospection.py --workspace <ID>` → notez les IDs des tables, remplissez « Formations » (cochez *Publié*).
2. **n8n** (auto-hébergé UE, ou n8n Cloud — hébergé à Francfort, à vérifier dans leur DPA) : *Import from file* → `workflow_n8n_assistant_yeba.json`.
3. Remplissez les trois nœuds « Config » (IDs, emails, numéro de transfert, URLs).
4. Créez les identifiants n8n : *Header Auth* « Baserow Database Token » (`Authorization` = `Token VOTRE_JETON`), *Header Auth* « Secret assistant vocal » (en-tête au choix, valeur longue et aléatoire), *SMTP* (hébergeur UE : Infomaniak, OVH, Brevo SMTP), *Basic Auth* CalDAV (Infomaniak Agenda, Nextcloud, OVH).
5. **Moteur vocal** : un développeur branche `prompt_systeme.md` + `outils_assistant.json` dans Pipecat, configure le trunk SIP et le transfert (SIP REFER) vers votre mobile.
6. **Tests** : 10 appels fictifs (un par scénario, plus « je ne comprends pas », « je veux parler à Aurélien », « question RGPD »). Activez le workflow seulement après.
7. **Connecteur n8n pour Claude** : il existe dans le catalogue de votre espace Claude (non installé). Une fois connecté, je pourrai lire les exécutions et corriger le workflow à votre place.

## 4. Points de vigilance
- **Liens dans les emails** : les antivirus de messagerie ouvrent automatiquement les liens. Le lien « Accepter » ouvre donc seulement une page avec un bouton **Confirmer** ; rien n'est fait sans ce clic.
- **Pas de dates fournies** : l'option est posée à J+7 et la page de confirmation vous le signale. Corrigez-la dans l'agenda.
- **Email du donneur d'ordre absent** : l'étape « Email au donneur d'ordre » échoue. Rappelez-le vous-même (amélioration possible : branche conditionnelle).
- **Numéro réunionnais (0262 / 0692 / 0693)** : je n'ai pas trouvé de confirmation qu'OVHcloud attribue ou porte des numéros des DOM. ➜ **Question à poser à OVHcloud avant de commencer.** Si ce n'est pas possible : renvoi d'appel de votre ligne actuelle vers un numéro métropolitain du trunk.

## 5. Réflexe réglementaire
| Point | Texte |
|---|---|
| Annonce « vous parlez à une IA » dès le début | **IA Act art. 50 §1** (obligation de transparence des systèmes qui interagissent avec des personnes) |
| Le système ne trie ni ne note les personnes, ne décide rien seul → pas de haut risque (annexe III) | **IA Act** |
| Information des appelants (finalité, durée, droits) | **RGPD art. 13** |
| Pas d'enregistrement audio, résumé de 3 lignes, purge à 12 mois conseillée | **RGPD art. 5 (minimisation, durée de conservation)** |
| Contrats de sous-traitance RGPD avec OVH, Scaleway, Mistral, Baserow, l'hébergeur n8n | **RGPD art. 28** |
| Inscription au registre des traitements « Accueil téléphonique automatisé » | **RGPD art. 30** |
| Pas de question sur la santé ou le handicap ; seul l'aménagement souhaité est noté | **RGPD art. 9** |
| Votre propre formation à l'outil, documentée | **IA Act art. 4** (maîtrise de l'IA) |

## 6. Autocritique et corrections apportées
| Faille | Correction |
|---|---|
| Validation par lien GET exposée aux scanners d'emails | Page de confirmation + bouton (POST), jeton aléatoire à usage unique |
| Risque d'« hallucination » d'un prix ou d'une prise en charge OPCO | Règle absolue dans le prompt + toute réponse vient uniquement de Baserow |
| Dépendance à un développeur pour Pipecat | Option B documentée, mais conditionnée à la lecture du DPA |
| Coût des minutes IA non chiffré précisément | Tarifs Mistral et OVH à relever le jour de la commande (ils évoluent) ; je ne les invente pas |
| Accessibilité (personnes sourdes ou malentendantes) | Alternative email systématique ; à terme, un formulaire sur le site |

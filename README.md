# Connexion Baserow ↔ Claude Code — YEBA FORMATIONS

Intégration **souveraine** (données hébergées dans l'UE) permettant à Claude
Code de concevoir et remplir des bases de données Baserow : bases, tables,
champs, lignes — sans qu'aucune donnée ne transite par un service tiers.

> **Pourquoi Baserow ?** Édité par **Baserow B.V. (Pays-Bas)**, cloud hébergé
> dans l'UE. C'est l'alternative souveraine à Airtable/Notion (États-Unis, donc
> soumis au *Cloud Act*). Choix cohérent avec votre exigence de souveraineté.

---

## 1. Prérequis (une seule fois)

### a. Compte de service Baserow (pour la STRUCTURE)
Dans Baserow, créez un utilisateur **dédié** (pas votre compte perso), invitez-le
dans votre workspace avec le rôle **Builder**. Il servira uniquement à Claude.
→ email + mot de passe = `BASEROW_EMAIL` / `BASEROW_PASSWORD`.

### b. Database Token (pour les DONNÉES)
Baserow → *Paramètres* → *Jetons de base de données* → créez un jeton avec les
permissions voulues (create/read/update/delete). → `BASEROW_TOKEN`.

### c. Configuration locale
```bash
cp .env.example .env      # puis remplissez .env (JAMAIS committé)
pip install -r requirements.txt
```

---

## 2. Vérifier la connexion
```bash
python -m baserow.cli check
```
Doit afficher `"jwt": true` et la liste de vos workspaces. Notez le `workspace_id`.

---

## 3. Brancher à Claude Code (MCP)

Le fichier `.mcp.json` enregistre le serveur `baserow`. Au prochain lancement de
Claude Code dans ce dossier, approuvez le serveur MCP. Claude dispose alors des
outils : `create_database`, `create_table_with_schema`, `create_field`,
`list_rows`, `create_rows`, `update_row`, `delete_row`, `baserow_health_check`…

Exemple de demande à Claude :
> « Crée une base *Suivi Qualiopi* avec une table des actions de formation
>   (intitulé, date, nombre de stagiaires, satisfaction, statut) et relie-la à
>   une table Formateurs. »

Exemple scripté fourni : `python examples/exemple_crm.py --workspace <ID>`.

---

## 4. Ce que Claude peut créer

| Outil | Rôle |
|---|---|
| `create_database` | Nouvelle base |
| `create_table_with_schema` | Table + schéma complet en une passe |
| `create_field` | Champ (text, number, date, single_select, link_row, formula…) |
| `create_rows` / `update_row` / `delete_row` | Données |
| `list_*` / `baserow_health_check` | Lecture & diagnostic |

---

## 5. Conformité — RGPD & IA Act (lecture obligatoire)

Cette intégration manipule potentiellement des **données personnelles**
(prospects, stagiaires). Points à tenir, en tant que responsable de traitement :

**RGPD**
- **Localisation** : Baserow cloud héberge dans l'UE → pas de transfert hors UE
  par défaut. Vérifiez/documentez la région dans votre contrat Baserow.
- **Minimisation (art. 5)** : ne créez que les champs nécessaires à la finalité.
- **Base légale (art. 6)** : intérêt légitime (prospection B2B) ou consentement.
- **Sécurité (art. 32)** : secrets dans `.env` non committé, compte de service
  dédié et révocable, jeton à permissions restreintes.
- **Registre & durée** : inscrivez ces traitements au registre ; définissez une
  durée de conservation (ex. prospects non convertis : 3 ans après dernier contact).
- **Sous-traitance (art. 28)** : signez un **DPA** avec Baserow B.V.

**IA Act (règlement UE 2024/1689)**
- Une simple base de données n'est pas un « système d'IA » → **hors périmètre**
  IA Act tant qu'il n'y a pas de traitement algorithmique décisionnel.
- ⚠️ Si vous branchez ensuite un **scoring/tri automatisé** (ex. classer des
  candidats, décider d'une admission en formation) sur ces données, cela peut
  devenir un usage **à haut risque** (annexe III) → obligations renforcées.
  À réévaluer au cas par cas au moment d'ajouter de l'IA décisionnelle.

*(Ce point est signalé spontanément, comme demandé, pour chaque livrable
touchant à des données ou à de l'IA.)*

---

## Sources
- Modèle d'authentification (JWT vs Database Token) :
  [baserow.io/user-docs/personal-api-tokens](https://baserow.io/user-docs/personal-api-tokens)
- API base de données Baserow :
  [baserow.io/user-docs/database-api](https://baserow.io/user-docs/database-api)
- RGPD, texte de référence : [cnil.fr](https://www.cnil.fr) (MOOC CNIL)
- IA Act : Règlement (UE) 2024/1689 —
  [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

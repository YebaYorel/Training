// Génère site/espace/src/modeles-qualiopi-demo.js : la version PUBLIQUE des modèles du Pack Qualiopi.
//
// Le Pack Qualiopi est vendu avec YEBA Studio. Toute version publiée sur Internet (démo, essai) est
// du code exécuté dans le navigateur du visiteur : rien de ce qu'elle contient ne peut être caché.
// Elle ne reçoit donc que l'intitulé, la catégorie, les indicateurs et le SOMMAIRE de chaque modèle.
// Le texte complet n'existe que dans la version client (npm run build:client), remise après achat.
//
//   node site/scripts/modeles-demo.mjs        (lancé automatiquement par build:studio et espace:apercu)
import { writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = dirname(fileURLToPath(import.meta.url))
const { MODELES } = await import(resolve(ICI, '../espace/src/modeles-qualiopi.js'))

const apercu = MODELES.map((m) => ({
  id: m.id,
  titre: m.titre,
  indicateurs: m.indicateurs,
  categorie: m.categorie,
  sommaire: m.blocs({}).filter(Boolean).filter((b) => b.h2).map((b) => b.h2),
}))

const code = `// FICHIER GÉNÉRÉ par site/scripts/modeles-demo.mjs — ne pas modifier à la main.
// Version publique (démo / essai) : sommaire des modèles uniquement, sans leur contenu.
const APERCU = ${JSON.stringify(apercu, null, 1)}

const MENTION = 'Aperçu de démonstration : le modèle complet, rédigé et pré-rempli avec votre fiche organisme, est fourni avec la licence YEBA Studio (Pack Qualiopi).'

export const MODELES = APERCU.map((m) => ({
  id: m.id,
  titre: m.titre,
  indicateurs: m.indicateurs,
  categorie: m.categorie,
  blocs: () => [
    { h1: m.titre },
    { p: MENTION },
    ...(m.sommaire.length ? [{ h2: 'Contenu du modèle complet' }, ...m.sommaire.map((t) => ({ li: t }))] : []),
  ],
}))

export const CATEGORIES = [...new Set(MODELES.map((m) => m.categorie))]
`
writeFileSync(resolve(ICI, '../espace/src/modeles-qualiopi-demo.js'), code)
console.log(`Modèles de démonstration : ${apercu.length} (sommaires seulement).`)

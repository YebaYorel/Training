import { defineConfig, loadEnv } from 'vite'
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { resolve } from 'node:path'

// Espace YEBA — outil de pilotage PRIVÉ, lancé sur votre poste uniquement.
//   npm run espace          → http://127.0.0.1:5180 (données fictives, ou vos données Airtable si AIRTABLE_TOKEN est dans .env)
//   npm run espace:apercu   → un fichier HTML autonome de DÉMONSTRATION (données fictives uniquement)
// Il n'est jamais déployé sur le site public (absent de `npm run build`, bloqué par .htaccess).
const BASE_AUTORISEE = '/v0/appQ2zqc80kkc6MR1/'
const TABLES_AUTORISEES = new Set([
  'tblBAwsuKf6Nw8w8Z', 'tblSCxGvNSDdH3Blt', 'tblg3KHANR7nq4cH6', 'tblUWW5ken5sAUDJk', 'tblUF2NHzUmDECDIW',
  'tbllQ4ydL7V62z4kC', 'tbl6oAUGfGVBRy7Jl', 'tblVLHyTCywkNtmvr', 'tblgqWIeM7l5qWV8H', 'tblm9YJud4dK7gD9d',
])
const ENTETES = {
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
  'Cache-Control': 'no-store',
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Resource-Policy': 'same-origin',
}

/** Garde du proxy : lecture seule, une seule base, tables listées, même origine, jeton jamais renvoyé. */
function gardeAirtable(jeton) {
  return {
    name: 'garde-airtable',
    configureServer(server) {
      // Enregistré AVANT les middlewares internes de Vite (dont le proxy) : rien ne passe sans contrôle.
      server.middlewares.use((req, res, next) => {
        if (!req.url.startsWith('/airtable')) return next()
        const refuser = (code, msg) => {
          res.statusCode = code
          res.setHeader('Content-Type', 'application/json')
          res.end(JSON.stringify({ erreur: msg }))
        }
        // Anti-CSRF / anti-rebond DNS : seules les requêtes de la page elle-même sont acceptées.
        if (req.headers['sec-fetch-site'] && req.headers['sec-fetch-site'] !== 'same-origin') return refuser(403, 'Origine refusée')
        const hote = (req.headers.host || '').split(':')[0]
        if (!['127.0.0.1', 'localhost'].includes(hote)) return refuser(403, 'Hôte refusé')
        if (req.method !== 'GET') return refuser(405, 'Lecture seule')
        if (req.url === '/airtable/etat') {
          res.setHeader('Content-Type', 'application/json')
          return res.end(JSON.stringify({ jeton: Boolean(jeton) }))
        }
        if (!jeton) return refuser(503, 'AIRTABLE_TOKEN absent du fichier .env')
        let chemin
        try {
          chemin = decodeURIComponent(req.url.slice('/airtable'.length).split('?')[0])
        } catch {
          return refuser(400, 'Adresse invalide')
        }
        const table = chemin.slice(BASE_AUTORISEE.length)
        if (!chemin.startsWith(BASE_AUTORISEE) || !TABLES_AUTORISEES.has(table)) return refuser(403, 'Ressource non autorisée')
        next()
      })
    },
  }
}

/** Prospection & appels d'offres (poste de YEBA uniquement, `npm run espace`) :
 *  • /boamp/records : veille BOAMP (open data DILA), GET seulement, un seul jeu de données, même origine ;
 *  • /prospection/etat : fichier local site/espace/.prospection/etat.json (ignoré par Git), jamais publié.
 *  Règle 2 vérifiée ici aussi : l'expéditeur enregistré ne peut être que l'adresse de travail. */
const EXPEDITEUR = 'yebaformations@gmail.com'
function prospectionLocale() {
  const dossier = resolve(__dirname, 'site/espace/.prospection')
  const fichier = resolve(dossier, 'etat.json')
  return {
    name: 'prospection-locale',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const veille = req.url.startsWith('/boamp/')
        const etat = req.url === '/prospection/etat'
        if (!veille && !etat) return next()
        const refuser = (code, msg) => {
          res.statusCode = code
          res.setHeader('Content-Type', 'application/json')
          res.end(JSON.stringify({ erreur: msg }))
        }
        if (req.headers['sec-fetch-site'] && req.headers['sec-fetch-site'] !== 'same-origin') return refuser(403, 'Origine refusée')
        const hote = (req.headers.host || '').split(':')[0]
        if (!['127.0.0.1', 'localhost'].includes(hote)) return refuser(403, 'Hôte refusé')
        if (veille) {
          if (req.method !== 'GET') return refuser(405, 'Lecture seule')
          if (req.url.split('?')[0] !== '/boamp/records') return refuser(403, 'Ressource non autorisée')
          return next()
        }
        if (req.method === 'GET') {
          res.setHeader('Content-Type', 'application/json')
          return res.end(existsSync(fichier) ? readFileSync(fichier, 'utf8') : 'null')
        }
        if (req.method !== 'PUT') return refuser(405, 'Méthode refusée')
        let corps = ''
        req.on('data', (c) => {
          corps += c
          if (corps.length > 2_000_000) req.destroy()
        })
        req.on('end', () => {
          let d
          try {
            d = JSON.parse(corps)
          } catch {
            return refuser(400, 'JSON invalide')
          }
          if (!d || d.version !== 1 || !Array.isArray(d.prospects) || !Array.isArray(d.oppositions)) return refuser(400, 'Structure invalide')
          if (String(d.expediteur || '').toLowerCase() !== EXPEDITEUR) return refuser(422, 'Règle 2 : expéditeur autorisé = ' + EXPEDITEUR)
          mkdirSync(dossier, { recursive: true })
          writeFileSync(fichier + '.tmp', JSON.stringify(d, null, 1))
          renameSync(fichier + '.tmp', fichier)
          res.setHeader('Content-Type', 'application/json')
          res.end('{"ok":true}')
        })
      })
    },
  }
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '') // variables SANS préfixe VITE_ : jamais injectées dans le code client
  const jeton = env.AIRTABLE_TOKEN || ''
  const publiee = mode === 'studio' || mode === 'apercu'
  return {
    root: 'site/espace',
    base: './',
    envPrefix: 'VITE_STUDIO_', // seules VITE_STUDIO_API / VITE_STUDIO_* (non secrètes) sont exposées au navigateur
    plugins: [
      react(),
      gardeAirtable(jeton),
      prospectionLocale(),
      {
        name: 'csp-api',
        // Autorise le serveur YEBA Studio (paiement, IA) dans la politique de sécurité, s'il est configuré
        transformIndexHtml: (html) => (env.VITE_STUDIO_API ? html.replace("connect-src 'self'", `connect-src 'self' ${new URL(env.VITE_STUDIO_API).origin}`) : html),
      },
      {
        // En ligne (dist/studio/), le .htaccess du site imposerait connect-src 'self' et bloquerait le serveur
        // YEBA Studio (paiement, licences, IA). Ce dossier reçoit donc sa propre politique : identique, plus la
        // seule origine du serveur YEBA Studio si elle est configurée.
        name: 'htaccess-studio',
        apply: 'build',
        closeBundle() {
          if (mode !== 'studio') return
          const api = env.VITE_STUDIO_API ? ' ' + new URL(env.VITE_STUDIO_API).origin : ''
          const csp = `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'${api}; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests`
          writeFileSync(
            resolve(__dirname, 'dist/studio/.htaccess'),
            `# Généré par vite.espace.config.js : politique de sécurité propre au logiciel YEBA Studio\n<IfModule mod_headers.c>\n  Header always set Content-Security-Policy "${csp}"\n  Header always set Referrer-Policy "no-referrer"\n  Header always set Cache-Control "no-store"\n</IfModule>\n`,
          )
        },
      },
      ...(mode === 'apercu' ? [viteSingleFile()] : [])],
    // Versions distribuées : le module Airtable interne est remplacé par un module vide (rien à découvrir dans le code).
    // Versions PUBLIQUES (démo, essai) : les modèles du Pack Qualiopi sont remplacés par leur seul sommaire,
    // car tout code envoyé au navigateur est lisible. Le texte complet n'est que dans la version client.
    resolve: publiee || mode === 'client'
      ? {
          alias: [
            { find: /^\.\/donnees\.js$/, replacement: resolve(__dirname, 'site/espace/src/donnees-vide.js') },
            { find: /^\.\/Prospection\.jsx$/, replacement: resolve(__dirname, 'site/espace/src/prospection-vide.jsx') },
            ...(publiee ? [{ find: /^\.\/modeles-qualiopi\.js$/, replacement: resolve(__dirname, 'site/espace/src/modeles-qualiopi-demo.js') }] : []),
          ],
        }
      : undefined,
    server: {
      host: '127.0.0.1',
      port: 5180,
      strictPort: true,
      cors: false,
      headers: ENTETES,
      proxy: {
        '/boamp': {
          target: 'https://boamp-datadila.opendatasoft.com',
          changeOrigin: true,
          secure: true,
          rewrite: (p) => p.replace(/^\/boamp\/records/, '/api/explore/v2.1/catalog/datasets/boamp/records'),
          configure(proxy) {
            proxy.on('proxyReq', (req) => {
              req.removeHeader('cookie')
              req.removeHeader('origin')
              req.removeHeader('referer')
            })
            proxy.on('proxyRes', (res) => {
              delete res.headers['set-cookie']
            })
          },
        },
        '/airtable': {
          target: 'https://api.airtable.com',
          changeOrigin: true,
          secure: true,
          rewrite: (p) => p.replace(/^\/airtable/, ''),
          configure(proxy) {
            proxy.on('proxyReq', (req) => {
              req.setHeader('Authorization', `Bearer ${jeton}`)
              req.removeHeader('cookie')
              req.removeHeader('origin')
              req.removeHeader('referer')
            })
            proxy.on('proxyRes', (res) => {
              delete res.headers['set-cookie']
            })
          },
        },
      },
    },
    build: {
      outDir: resolve(__dirname, mode === 'apercu' ? 'apercu-espace' : mode === 'studio' ? 'dist/studio' : mode === 'client' ? 'dist-client' : 'dist-espace'),
      emptyOutDir: true,
      chunkSizeWarningLimit: 700,
    },
  }
})

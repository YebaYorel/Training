import { defineConfig, loadEnv } from 'vite'
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

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '') // variables SANS préfixe VITE_ : jamais injectées dans le code client
  const jeton = env.AIRTABLE_TOKEN || ''
  return {
    root: 'site/espace',
    base: './',
    envPrefix: 'ESPACE_PUBLIC_', // aucune variable de .env n'est exposée au navigateur
    plugins: [react(), gardeAirtable(jeton), ...(mode === 'apercu' ? [viteSingleFile()] : [])],
    server: {
      host: '127.0.0.1',
      port: 5180,
      strictPort: true,
      cors: false,
      headers: ENTETES,
      proxy: {
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
      outDir: resolve(__dirname, mode === 'apercu' ? 'apercu-espace' : 'dist-espace'),
      emptyOutDir: true,
      chunkSizeWarningLimit: 700,
    },
  }
})

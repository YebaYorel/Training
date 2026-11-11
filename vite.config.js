import { defineConfig, loadEnv } from 'vite'
import { existsSync, readFileSync, writeFileSync } from 'node:fs'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { resolve } from 'node:path'

// `npm run build`   → site statique multi-fichiers dans dist/ (à déposer chez l'hébergeur)
// `npm run apercu`  → un seul fichier HTML autonome dans apercu/ (pour relire le site hors ligne)

// Si le formulaire de rappel d'IFA est branché sur un service externe (VITE_RAPPEL_ENDPOINT, en https),
// son origine — et elle seule — est ajoutée à la directive connect-src de la politique de sécurité (.htaccess).
// Sans cela, le navigateur bloquerait l'envoi sans prévenir le visiteur.
function cspFormulaire(mode) {
  return {
    name: 'csp-formulaire',
    apply: 'build',
    closeBundle() {
      const point = loadEnv(mode, process.cwd(), 'VITE_').VITE_RAPPEL_ENDPOINT
      const fichier = resolve(__dirname, 'dist/.htaccess')
      if (!point || !existsSync(fichier)) return
      const url = new URL(point)
      if (url.protocol !== 'https:') throw new Error('VITE_RAPPEL_ENDPOINT doit être en https://')
      const htaccess = readFileSync(fichier, 'utf8')
      writeFileSync(fichier, htaccess.replace("connect-src 'self'", `connect-src 'self' ${url.origin}`))
    },
  }
}

export default defineConfig(({ mode }) => ({
  root: 'site',
  base: './',
  // Mêmes en-têtes de sécurité qu'en production (voir site/public/.htaccess) pour tester en local
  preview: {
    headers: {
      'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; media-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'",
      'X-Frame-Options': 'DENY',
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
    },
  },
  plugins: [react(), cspFormulaire(mode), ...(mode === 'apercu' ? [viteSingleFile()] : [])],
  build: {
    outDir: resolve(__dirname, mode === 'apercu' ? 'apercu' : 'dist'),
    emptyOutDir: true,
    // ~160 Ko compressés : React + Framer Motion + Lenis. L'assistante IFA est chargée à part, au premier clic.
    chunkSizeWarningLimit: 600,
    rollupOptions:
      mode === 'apercu'
        ? undefined
        : {
            input: {
              main: resolve(__dirname, 'site/index.html'),
              mentions: resolve(__dirname, 'site/mentions-legales.html'),
              confidentialite: resolve(__dirname, 'site/confidentialite.html'),
              cgvLogiciels: resolve(__dirname, 'site/cgv-logiciels.html'),
            },
          },
  },
}))

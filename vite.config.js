import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { resolve } from 'node:path'

// `npm run build`   → site statique multi-fichiers dans dist/ (à déposer chez l'hébergeur)
// `npm run apercu`  → un seul fichier HTML autonome dans apercu/ (pour relire le site hors ligne)
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
  plugins: [react(), ...(mode === 'apercu' ? [viteSingleFile()] : [])],
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
            },
          },
  },
}))

import { StrictMode } from 'react'
import { createRoot, hydrateRoot } from 'react-dom/client'
// Polices auto-hébergées : aucun appel à Google Fonts (transfert d'IP hors UE évité — RGPD)
import '@fontsource/montserrat/700.css'
import '@fontsource/montserrat/800.css'
import '@fontsource/montserrat/900.css'
import '@fontsource/atkinson-hyperlegible/400.css'
import '@fontsource/atkinson-hyperlegible/700.css'
import './styles.css'
import App from './App.jsx'
import Intro from './intro.jsx'

// L'intro du logo vit dans sa propre racine : elle n'existe que dans le navigateur.
createRoot(document.getElementById('intro-racine')).render(<Intro />)

// La page est pré-rendue au moment de la construction (scripts/prerender.mjs) : React se branche sur
// le HTML déjà affiché (hydratation) au lieu de le reconstruire. En développement, rendu classique.
const racine = document.getElementById('racine')
const app = (
  <StrictMode>
    <App />
  </StrictMode>
)
if (racine.hasChildNodes()) hydrateRoot(racine, app)
else createRoot(racine).render(app)

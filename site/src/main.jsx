import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Polices auto-hébergées : aucun appel à Google Fonts (transfert d'IP hors UE évité — RGPD)
import '@fontsource/montserrat/700.css'
import '@fontsource/montserrat/800.css'
import '@fontsource/montserrat/900.css'
import '@fontsource/atkinson-hyperlegible/400.css'
import '@fontsource/atkinson-hyperlegible/700.css'
import './styles.css'
import App from './App.jsx'

createRoot(document.getElementById('racine')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

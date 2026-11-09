// Pré-rendu au moment de la construction : produit le HTML complet de la page
// d'accueil pour que moteurs de recherche, IA et réseaux sociaux lisent le contenu
// sans exécuter JavaScript, et que le visiteur voie le texte immédiatement.
import { StrictMode } from 'react'
import { renderToString } from 'react-dom/server'
import App from './App.jsx'

export function render() {
  return renderToString(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}

// Coordonnées reprises par le pré-rendu (données structurées, llms.txt) : une seule source de vérité.
export { ENTREPRISE } from './data.js'
export { slugFormation } from './liens.js'
export { FORMATIONS, AGENDA } from './data.js'

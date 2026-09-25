import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@fontsource/montserrat/700.css'
import '@fontsource/montserrat/800.css'
import '@fontsource/atkinson-hyperlegible/400.css'
import '@fontsource/atkinson-hyperlegible/700.css'
import './espace.css'
import App from './App.jsx'

createRoot(document.getElementById('racine')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

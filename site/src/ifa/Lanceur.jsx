import { Suspense, lazy, useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { X } from 'lucide-react'
import Avatar from './Avatar.jsx'

// Le panneau (moteur de réponses + agenda) n'est téléchargé qu'au premier clic : page d'accueil plus légère.
const Panneau = lazy(() => import('./Panneau.jsx'))

function dejaSalue() {
  try {
    return sessionStorage.getItem('ifa-salut') === '1'
  } catch {
    return false
  }
}

export default function Lanceur() {
  const [ouvert, setOuvert] = useState(false)
  const [bulle, setBulle] = useState(false)
  const bouton = useRef(null)

  // Petite bulle d'accueil, une seule fois par visite, après 9 secondes
  useEffect(() => {
    if (dejaSalue()) return
    const t = setTimeout(() => setBulle(true), 9000)
    return () => clearTimeout(t)
  }, [])
  function fermerBulle() {
    setBulle(false)
    try {
      sessionStorage.setItem('ifa-salut', '1')
    } catch {
      /* sans importance */
    }
  }
  function ouvrir() {
    fermerBulle()
    setOuvert(true)
  }
  function fermer() {
    setOuvert(false)
    requestAnimationFrame(() => bouton.current?.focus())
  }

  return (
    <>
      <AnimatePresence>
        {bulle && !ouvert && (
          <motion.div
            className="ifa-bulle"
            role="status"
            initial={{ opacity: 0, y: 16, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 380, damping: 26 }}
          >
            <button className="ifa-bulle-texte" onClick={ouvrir}>
              Bonjour, je suis <strong>IFA</strong>. Une question sur nos formations ?
            </button>
            <button className="ifa-bulle-fermer" onClick={fermerBulle} aria-label="Masquer ce message">
              <X size={16} />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
      <motion.button
        ref={bouton}
        className="ifa-lanceur"
        onClick={() => (ouvert ? fermer() : ouvrir())}
        aria-expanded={ouvert}
        aria-controls="ifa-panneau"
        aria-label={ouvert ? 'Fermer IFA, l’assistante virtuelle' : 'Ouvrir IFA, l’assistante virtuelle'}
        initial={{ x: -120 }}
        animate={{ x: 0 }}
        transition={{ type: 'spring', stiffness: 200, damping: 22, delay: 1.2 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.96 }}
      >
        <Avatar taille={52} />
        <span className="ifa-lanceur-nom">IFA</span>
        <span className="ifa-pastille-en-ligne" aria-hidden="true" />
      </motion.button>
      <AnimatePresence>
        {ouvert && (
          <Suspense key="panneau" fallback={null}>
            <Panneau onFermer={fermer} />
          </Suspense>
        )}
      </AnimatePresence>
    </>
  )
}

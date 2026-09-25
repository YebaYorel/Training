import { useEffect, useMemo, useState } from 'react'
import { AnimatePresence, MotionConfig, motion } from 'framer-motion'
import { ClipboardCheck, FileSpreadsheet, LayoutDashboard, Lock, RefreshCw, ShieldCheck, Users } from 'lucide-react'
import { DEMO } from './demo.js'
import { chargerDirect, proxyDisponible } from './donnees.js'
import Tableau from './Tableau.jsx'
import Coffre from './Coffre.jsx'
import Parcours from './Parcours.jsx'
import Bpf from './Bpf.jsx'

const MODULES = [
  { id: 'tableau', libelle: 'Tableau de bord', Icone: LayoutDashboard, C: Tableau },
  { id: 'coffre', libelle: 'Coffre Qualiopi', Icone: ShieldCheck, C: Coffre },
  { id: 'parcours', libelle: 'Parcours', Icone: Users, C: Parcours },
  { id: 'bpf', libelle: 'BPF', Icone: FileSpreadsheet, C: Bpf },
]

function moduleInitial() {
  const h = location.hash.slice(1)
  return MODULES.some((m) => m.id === h) ? h : 'tableau'
}

export default function App() {
  const [module, setModule] = useState(moduleInitial)
  const [db, setDb] = useState(DEMO)
  const [direct, setDirect] = useState(false)
  const [etat, setEtat] = useState('')

  useEffect(() => {
    proxyDisponible().then(setDirect)
    const h = () => setModule(moduleInitial())
    addEventListener('hashchange', h)
    return () => removeEventListener('hashchange', h)
  }, [])

  async function basculer() {
    if (db.mode === 'direct') return setDb(DEMO)
    setEtat('Lecture d’Airtable…')
    try {
      setDb(await chargerDirect())
      setEtat('')
    } catch (e) {
      setEtat(e.message)
    }
  }

  function aller(id) {
    history.replaceState(null, '', '#' + id)
    setModule(id)
    document.getElementById('espace-contenu')?.focus()
  }

  const Actif = MODULES.find((m) => m.id === module).C
  return (
    <MotionConfig reducedMotion="user">
      <a className="evitement" href="#espace-contenu">Aller au contenu</a>
      <div className="espace">
        <aside className="barre">
          <div className="marque">
            <span className="marque-logo" aria-hidden="true">Y</span>
            <span>
              <strong>Espace YEBA</strong>
              <small>Pilotage interne</small>
            </span>
          </div>
          <nav aria-label="Modules">
            <ul>
              {MODULES.map(({ id, libelle, Icone }) => (
                <li key={id}>
                  <button className={'module' + (module === id ? ' actif' : '')} aria-current={module === id ? 'page' : undefined} onClick={() => aller(id)}>
                    {module === id && <motion.span layoutId="module-actif" className="module-fond" transition={{ type: 'spring', stiffness: 420, damping: 36 }} />}
                    <Icone size={22} aria-hidden="true" />
                    <span>{libelle}</span>
                  </button>
                </li>
              ))}
            </ul>
          </nav>
          <div className="barre-pied">
            <Lock size={16} aria-hidden="true" /> Local · lecture seule
          </div>
        </aside>

        <div className="principal">
          <header className="entete">
            <div>
              <p className="fil">YEBA FORMATIONS · {MODULES.find((m) => m.id === module).libelle}</p>
              <p className={'mode ' + db.mode}>
                {db.mode === 'demo' ? 'Données fictives de démonstration' : `Données Airtable · lues à ${new Date(db.charge).toLocaleTimeString('fr-FR')}`}
              </p>
            </div>
            <div className="entete-actions">
              {etat && <span className="etat" role="status">{etat}</span>}
              {direct ? (
                <button className="bouton" onClick={basculer}>
                  <RefreshCw size={18} aria-hidden="true" /> {db.mode === 'direct' ? 'Revenir à la démo' : 'Charger mes données'}
                </button>
              ) : (
                <span className="indice" title="Lancez « npm run espace » avec AIRTABLE_TOKEN dans .env pour lire vos données">
                  <ClipboardCheck size={16} aria-hidden="true" /> Mode démo
                </span>
              )}
            </div>
          </header>
          <main id="espace-contenu" tabIndex={-1}>
            <AnimatePresence mode="wait">
              <motion.div key={module + db.mode} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.28 }}>
                <Actif db={db} aller={aller} />
              </motion.div>
            </AnimatePresence>
          </main>
        </div>
      </div>
    </MotionConfig>
  )
}

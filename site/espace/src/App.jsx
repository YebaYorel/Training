// YEBA Studio — application des organismes de formation (et Espace YEBA interne sur le poste de YEBA).
// Trois modes :
//   • demo    : organisme fictif, tout ouvert, rien n'est enregistré ;
//   • local   : l'espace chiffré du client, modules ouverts selon ses licences (ou l'essai de 14 jours) ;
//   • interne : lecture d'Airtable via le proxy local (poste de YEBA uniquement, `npm run espace`).
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { AnimatePresence, MotionConfig, motion } from 'framer-motion'
import { BadgeCheck, Database, FileSpreadsheet, FileText, Flame, LayoutDashboard, Lock, LogOut, RefreshCw, Settings, ShieldCheck, Sparkles, Users } from 'lucide-react'
import { DEMO } from './demo.js'
import { demoDonnees } from './demo-donnees.js'
import { versDb } from './modele.js'
import { OFFRES, modulesOuverts, verifier } from './licence.js'
import { codePoste, charger, enregistrer, ecrire, lire } from './stockage.js'
import { recupererLicence, sante, API } from './api.js'
import Verrou from './Verrou.jsx'
import Tableau from './Tableau.jsx'
import Coffre from './Coffre.jsx'
import Parcours from './Parcours.jsx'
import Bpf from './Bpf.jsx'
import Donnees from './Donnees.jsx'
import Modeles from './Modeles.jsx'
import Carburant from './Carburant.jsx'
import Licences from './Licences.jsx'
import Reglages from './Reglages.jsx'

const MODULES = [
  { id: 'tableau', libelle: 'Tableau de bord', Icone: LayoutDashboard, libre: true },
  { id: 'donnees', libelle: 'Mes données', Icone: Database },
  { id: 'parcours', libelle: 'Parcours', Icone: Users },
  { id: 'bpf', libelle: 'BPF', Icone: FileSpreadsheet },
  { id: 'coffre', libelle: 'Coffre Qualiopi', Icone: ShieldCheck },
  { id: 'modeles', libelle: 'Modèles Word', Icone: FileText },
  { id: 'carburant', libelle: 'CARBURANT', Icone: Flame, ia: true },
  { id: 'licences', libelle: 'Licences', Icone: BadgeCheck, libre: true },
  { id: 'reglages', libelle: 'Réglages', Icone: Settings, libre: true },
]
const MODULES_INTERNES = ['tableau', 'coffre', 'parcours', 'bpf']
// Le lien Airtable interne n'existe que sur le poste de YEBA : absent des versions publiées (studio, aperçu).
const INTERNE = import.meta.env.MODE !== 'studio' && import.meta.env.MODE !== 'apercu'
const ESSAI_JOURS = 14
const VERROU_MINUTES = 15

function moduleDemande() {
  const h = location.hash.slice(1)
  return MODULES.some((m) => m.id === h) ? h : 'tableau'
}

/* Module fermé : ce qu'il apporte, et comment l'ouvrir */
function ModuleFerme({ id, aller }) {
  const offres = Object.entries(OFFRES).filter(([, o]) => o.modules.includes(id))
  const m = MODULES.find((x) => x.id === id)
  return (
    <div className="module-ferme carte">
      <Lock size={34} aria-hidden="true" />
      <h1>{m.libelle}</h1>
      <p>Ce module s’ouvre avec l’une de ces offres :</p>
      <ul>{offres.map(([k, o]) => <li key={k}><strong>{o.nom}</strong> — {o.libellePrix}</li>)}</ul>
      <button className="bouton" onClick={() => aller('licences', offres[0]?.[0])}>Voir les offres</button>
    </div>
  )
}

export default function App() {
  const [mode, setMode] = useState(null) // null (accueil) | demo | local | interne
  const [module, setModule] = useState(moduleDemande)
  const [offreVisee, setOffreVisee] = useState(null)
  const [donnees, setDonnees] = useState(null)
  const [dbInterne, setDbInterne] = useState(null)
  const [interneDispo, setInterneDispo] = useState(false)
  const [poste, setPoste] = useState('')
  const [licences, setLicences] = useState([])
  const [essai, setEssai] = useState(null)
  const [iaServeur, setIaServeur] = useState(false)
  const [etat, setEtat] = useState('')
  const [autreOnglet, setAutreOnglet] = useState(false)
  const cle = useRef(null)
  const minuteur = useRef(null)
  const sauvegarde = useRef(null)
  const canal = useRef(null)
  const idOnglet = useRef(Math.random().toString(36).slice(2))

  /* ---------- Démarrage ---------- */
  useEffect(() => {
    codePoste().then(setPoste)
    if (INTERNE) import('./donnees.js').then((m) => m.proxyDisponible().then(setInterneDispo))
    sante().then((s) => setIaServeur(!!(s.ok && s.ia)))
    const h = () => setModule(moduleDemande())
    addEventListener('hashchange', h)
    return () => removeEventListener('hashchange', h)
  }, [])

  const chargerLicences = useCallback(async (p) => {
    const codes = (await lire('licences')) || []
    setLicences(await Promise.all(codes.map(async (code) => ({ code, ...(await verifier(code, p)) }))))
  }, [])

  /* ---------- Une seule session ouverte à la fois (onglets) ---------- */
  useEffect(() => {
    if (!('BroadcastChannel' in window)) return
    canal.current = new BroadcastChannel('yeba-studio')
    canal.current.onmessage = (e) => {
      if (e.data?.type === 'ouverture' && e.data.id !== idOnglet.current && cle.current) {
        verrouiller()
        setAutreOnglet(true)
      }
    }
    return () => canal.current?.close()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  /* ---------- Verrouillage automatique après inactivité ---------- */
  const verrouiller = useCallback(() => {
    cle.current = null
    setDonnees(null)
    setMode(null)
    setEtat('')
  }, [])
  useEffect(() => {
    if (mode !== 'local') return
    const relancer = () => {
      clearTimeout(minuteur.current)
      minuteur.current = setTimeout(verrouiller, VERROU_MINUTES * 60000)
    }
    const evts = ['pointerdown', 'keydown', 'wheel', 'touchstart']
    evts.forEach((e) => addEventListener(e, relancer, { passive: true }))
    relancer()
    return () => {
      clearTimeout(minuteur.current)
      evts.forEach((e) => removeEventListener(e, relancer))
    }
  }, [mode, verrouiller])

  /* ---------- Ouverture de l'espace local ---------- */
  async function ouvrirLocal(k, nouveau) {
    cle.current = k
    const d = await charger(k)
    let e = await lire('essai')
    if (!e && nouveau) await ecrire('essai', (e = { debut: new Date().toISOString() }))
    const jours = e ? Math.max(0, ESSAI_JOURS - Math.floor((Date.now() - new Date(e.debut)) / 86400000)) : 0
    setEssai(e ? { ...e, jours } : null)
    await chargerLicences(poste || (await codePoste()))
    setDonnees(d)
    setMode('local')
    setAutreOnglet(false)
    canal.current?.postMessage({ type: 'ouverture', id: idOnglet.current })
    // Retour de paiement : récupérer les licences payées
    const attentes = (await lire('paiements')) || []
    if (attentes.length) {
      setEtat('Vérification de votre paiement…')
      const restantes = []
      for (const p of attentes) {
        try {
          const r = await recupererLicence(p)
          if (r.licence) await ajouterLicence(r.licence)
          else if (['open', 'pending', 'authorized'].includes(r.etat)) restantes.push(p)
        } catch {
          restantes.push(p)
        }
      }
      await ecrire('paiements', restantes)
      setEtat(restantes.length ? 'Paiement en cours de confirmation : revenez dans quelques minutes.' : '')
    }
  }

  async function ajouterLicence(code) {
    const p = poste || (await codePoste())
    const r = await verifier(code, p)
    if (!r.ok) return r
    const codes = (await lire('licences')) || []
    if (!codes.includes(code)) await ecrire('licences', [...codes, code])
    await chargerLicences(p)
    return r
  }

  /* ---------- Modification des données (toutes les écritures passent ici) ---------- */
  const modifier = useCallback(
    (fn, message) => {
      setDonnees((prec) => {
        const d = structuredClone(prec)
        fn(d)
        if (message) d.journal = [{ date: new Date().toISOString(), message }, ...(d.journal || [])].slice(0, 300)
        if (mode === 'local' && cle.current) {
          clearTimeout(sauvegarde.current)
          const k = cle.current
          sauvegarde.current = setTimeout(() => enregistrer(k, d).catch(() => setEtat('⚠️ Enregistrement impossible sur ce poste.')), 300)
        }
        return d
      })
    },
    [mode],
  )

  async function passerInterne() {
    setEtat('Lecture d’Airtable…')
    try {
      const { chargerDirect } = await import('./donnees.js')
      setDbInterne(await chargerDirect())
      setMode('interne')
      setEtat('')
    } catch (e) {
      setEtat(e.message)
    }
  }

  const aller = useCallback((id, offre) => {
    history.replaceState(null, '', '#' + id)
    setModule(id)
    if (offre) setOffreVisee(offre)
    requestAnimationFrame(() => document.getElementById('espace-contenu')?.focus())
  }, [])

  /* ---------- Droits d'accès ---------- */
  const valides = licences.filter((l) => l.ok)
  const ouverts = useMemo(() => {
    if (mode === 'demo' || mode === 'interne') return new Set(MODULES.map((m) => m.id))
    const s = modulesOuverts(valides)
    if (essai?.jours > 0) MODULES.forEach((m) => s.add(m.id))
    MODULES.filter((m) => m.libre).forEach((m) => s.add(m.id))
    return s
  }, [mode, licences, essai]) // eslint-disable-line react-hooks/exhaustive-deps
  const enEssai = mode === 'local' && essai?.jours > 0 && !valides.some((l) => ['studio'].includes(l.charge.off))
  const essaiPour = (id) => enEssai && !modulesOuverts(valides).has(id)

  const db = useMemo(() => (mode === 'interne' ? dbInterne : donnees ? versDb(donnees) : null), [mode, dbInterne, donnees])
  const licenceIa = valides.find((l) => ['carburant', 'parcours', 'studio'].includes(l.charge.off))
  const ia = { disponible: !!(API && iaServeur && licenceIa), licence: licenceIa?.code, poste }

  /* ---------- Écran d'accueil ---------- */
  if (!mode) {
    return (
      <MotionConfig reducedMotion="user">
        {autreOnglet && <p className="bandeau-info" role="alert">Votre espace a été ouvert dans un autre onglet : celui-ci a été verrouillé (une seule session à la fois).</p>}
        <Verrou poste={poste} onDemo={() => (setDonnees(demoDonnees()), setMode('demo'))} onOuvert={ouvrirLocal} />
        {interneDispo && (
          <p className="acces-interne">
            <button className="lien-discret" onClick={passerInterne}><RefreshCw size={14} aria-hidden="true" /> Espace YEBA interne (Airtable)</button> {etat}
          </p>
        )}
      </MotionConfig>
    )
  }

  const liste = mode === 'interne' ? MODULES.filter((m) => MODULES_INTERNES.includes(m.id)) : MODULES
  const actif = liste.some((m) => m.id === module) ? module : 'tableau'
  const titreOrg = mode === 'interne' ? 'YEBA FORMATIONS' : donnees?.organisme?.nom || 'Mon organisme'
  const props = { db, donnees: mode === 'interne' ? null : donnees, modifier: mode === 'interne' ? null : modifier, aller, essai: essaiPour(actif) }

  let contenu
  if (!ouverts.has(actif)) contenu = <ModuleFerme id={actif} aller={aller} />
  else
    contenu = {
      tableau: <Tableau db={db} donnees={props.donnees} aller={aller} ouverts={ouverts} />,
      donnees: <Donnees donnees={donnees} modifier={modifier} />,
      parcours: <Parcours {...props} />,
      bpf: <Bpf {...props} />,
      coffre: <Coffre db={db} donnees={props.donnees} modifier={props.modifier} aller={aller} />,
      modeles: <Modeles donnees={donnees} essai={essaiPour('modeles')} aller={aller} />,
      carburant: <Carburant donnees={donnees} modifier={modifier} ia={ia} essai={essaiPour('carburant')} aller={aller} />,
      licences: <Licences poste={poste} licences={licences} essai={mode === 'local' ? essai : null} ajouterLicence={ajouterLicence} organisme={donnees?.organisme} offreVisee={offreVisee} />,
      reglages: <Reglages donnees={donnees} demo={mode === 'demo'} verrouiller={verrouiller} remplacer={(d) => modifier((x) => Object.assign(x, d), 'Sauvegarde restaurée')} />,
    }[actif]

  return (
    <MotionConfig reducedMotion="user">
      <a className="evitement" href="#espace-contenu">Aller au contenu</a>
      <div className="espace">
        <aside className="barre">
          <div className="marque">
            <span className="marque-logo" aria-hidden="true">Y</span>
            <span>
              <strong>{mode === 'interne' ? 'Espace YEBA' : 'YEBA Studio'}</strong>
              <small>{mode === 'interne' ? 'Pilotage interne' : 'Formation · Qualiopi · IA'}</small>
            </span>
          </div>
          <nav aria-label="Modules">
            <ul>
              {liste.map(({ id, libelle, Icone, ia: estIa }) => (
                <li key={id}>
                  <button className={'module' + (actif === id ? ' actif' : '') + (ouverts.has(id) ? '' : ' ferme')} aria-current={actif === id ? 'page' : undefined} onClick={() => aller(id)}>
                    {actif === id && <motion.span layoutId="module-actif" className="module-fond" transition={{ type: 'spring', stiffness: 420, damping: 36 }} />}
                    <Icone size={20} aria-hidden="true" />
                    <span>{libelle}</span>
                    {estIa && <Sparkles className="etoile-ia" size={14} aria-label="IA" />}
                    {!ouverts.has(id) && <Lock className="cadenas" size={13} aria-label="verrouillé" />}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
          <div className="barre-pied">
            {mode === 'local' ? (
              <button className="lien-barre" onClick={verrouiller}><Lock size={15} aria-hidden="true" /> Verrouiller</button>
            ) : (
              <button className="lien-barre" onClick={() => (setMode(null), setDonnees(null))}><LogOut size={15} aria-hidden="true" /> Quitter {mode === 'demo' ? 'la démo' : ''}</button>
            )}
            {valides[0] && <small className="filigrane">Licence : {valides[0].charge.nom} · poste {poste}</small>}
          </div>
        </aside>

        <div className="principal">
          <header className="entete">
            <div>
              <p className="fil">{titreOrg} · {liste.find((m) => m.id === actif)?.libelle}</p>
              <p className={'mode ' + (mode === 'local' ? 'direct' : mode === 'interne' ? 'direct' : 'demo')}>
                {mode === 'demo' ? 'Démo — organisme fictif, rien n’est enregistré' : mode === 'interne' ? `Données Airtable · lues à ${new Date(db.charge).toLocaleTimeString('fr-FR')}` : enEssai ? `Essai gratuit : encore ${essai.jours} jour(s)` : 'Espace chiffré sur ce poste'}
              </p>
            </div>
            <div className="entete-actions">
              {etat && <span className="etat" role="status">{etat}</span>}
              {mode === 'demo' && <button className="bouton" onClick={() => (setMode(null), setDonnees(null))}>Créer mon espace</button>}
              {mode === 'local' && enEssai && <button className="bouton" onClick={() => aller('licences')}>Choisir une offre</button>}
            </div>
          </header>
          <main id="espace-contenu" tabIndex={-1}>
            <AnimatePresence mode="wait">
              <motion.div key={actif + mode} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.25 }}>
                {contenu}
              </motion.div>
            </AnimatePresence>
          </main>
        </div>
      </div>
    </MotionConfig>
  )
}

// Garde la démo historique importable par d'autres modules (tests, aperçu)
export { DEMO }

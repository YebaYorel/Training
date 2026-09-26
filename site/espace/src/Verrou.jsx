// Écran d'entrée : démo, création de l'espace (code personnel + clé de secours), ou déverrouillage.
import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { Eye, KeyRound, Lock, ShieldCheck, Sparkles } from 'lucide-react'
import { changerPin, creerCoffre, etatCoffre, ouvrirCoffre, stockageEphemere } from './stockage.js'
import { donneesVides } from './modele.js'
import { telecharger } from './ui.jsx'

const PIN = /^\d{8,12}$/

export default function Verrou({ onDemo, onOuvert, poste }) {
  const [etat, setEtat] = useState(null) // nouveau | verrouille
  const [etape, setEtape] = useState('choix') // choix | creer | secours-affiche | ouvrir | secours
  const [pin, setPin] = useState('')
  const [pin2, setPin2] = useState('')
  const [secours, setSecours] = useState('')
  const [note, setNote] = useState(false)
  const [erreur, setErreur] = useState('')
  const [attente, setAttente] = useState(false)
  const echecs = useRef(0)
  const ouvert = useRef(null)

  useEffect(() => {
    etatCoffre().then(setEtat)
  }, [])

  async function creer(e) {
    e.preventDefault()
    if (!PIN.test(pin)) return setErreur('Le code personnel doit contenir 8 à 12 chiffres.')
    if (pin !== pin2) return setErreur('Les deux codes ne correspondent pas.')
    setAttente(true)
    const { cle, secours: s } = await creerCoffre(pin, donneesVides())
    ouvert.current = cle
    setSecours(s)
    setAttente(false)
    setErreur('')
    setEtape('secours-affiche')
  }

  async function ouvrir(e) {
    e.preventDefault()
    if (echecs.current >= 5) return setErreur('Trop d’essais : patientez 30 secondes.')
    setAttente(true)
    try {
      const { cle } = await ouvrirCoffre(pin)
      echecs.current = 0
      onOuvert(cle)
    } catch (err) {
      echecs.current++
      if (echecs.current >= 5) setTimeout(() => (echecs.current = 0), 30000)
      setErreur(err.message)
    } finally {
      setAttente(false)
      setPin('')
    }
  }

  async function recuperer(e) {
    e.preventDefault()
    if (!PIN.test(pin)) return setErreur('Choisissez un nouveau code de 8 à 12 chiffres.')
    setAttente(true)
    try {
      const { cle, brut } = await ouvrirCoffre(secours, true)
      await changerPin(brut, pin)
      onOuvert(cle)
    } catch (err) {
      setErreur(err.message)
    } finally {
      setAttente(false)
    }
  }

  const carte = (children) => (
    <motion.div className="verrou-carte" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} key={etape}>
      {children}
      {erreur && <p className="erreur" role="alert">{erreur}</p>}
    </motion.div>
  )
  const champPin = (valeur, set, libelle, id, auto = 'off') => (
    <label className="champ" htmlFor={id}>
      <span>{libelle}</span>
      <input id={id} type="password" inputMode="numeric" autoComplete={auto} pattern="\d*" maxLength={12} value={valeur} onChange={(e) => set(e.target.value.replace(/\D/g, ''))} required />
    </label>
  )

  return (
    <div className="verrou">
      <div className="verrou-marque">
        <span className="marque-logo" aria-hidden="true">Y</span>
        <div>
          <h1>YEBA Studio</h1>
          <p>Qualiopi, BPF, gestion des formations et IA — pour les organismes de formation.</p>
        </div>
      </div>

      {etape === 'choix' &&
        carte(
          <>
            <div className="choix-entree">
              <button className="entree" onClick={onDemo}>
                <Eye aria-hidden="true" />
                <strong>Découvrir la démo</strong>
                <span>Un organisme fictif, tous les modules ouverts. Rien n’est enregistré.</span>
              </button>
              <button className="entree principale" disabled={!etat} onClick={() => setEtape(etat === 'nouveau' ? 'creer' : 'ouvrir')}>
                <Lock aria-hidden="true" />
                <strong>{etat === 'verrouille' ? 'Ouvrir mon espace' : 'Créer mon espace'}</strong>
                <span>{etat === 'verrouille' ? 'Avec votre code personnel.' : 'Vos données restent chiffrées sur ce PC. 14 jours d’essai offerts.'}</span>
              </button>
            </div>
            {stockageEphemere() && <p className="note">⚠️ Ce navigateur n’autorise pas l’enregistrement : l’espace sera perdu à la fermeture.</p>}
            <p className="poste">Code de ce poste : <code>{poste}</code></p>
          </>,
        )}

      {etape === 'creer' &&
        carte(
          <form onSubmit={creer}>
            <h2><ShieldCheck aria-hidden="true" /> Créer votre espace</h2>
            <p className="note">Choisissez un code personnel de 8 à 12 chiffres. Il chiffre vos données : sans lui, personne ne peut les lire.</p>
            {champPin(pin, setPin, 'Code personnel', 'pin', 'new-password')}
            {champPin(pin2, setPin2, 'Confirmez le code', 'pin2', 'new-password')}
            <div className="ligne-actions">
              <button type="button" className="bouton secondaire" onClick={() => setEtape('choix')}>Retour</button>
              <button className="bouton" disabled={attente}>{attente ? 'Chiffrement…' : 'Créer mon espace'}</button>
            </div>
          </form>,
        )}

      {etape === 'secours-affiche' &&
        carte(
          <>
            <h2><KeyRound aria-hidden="true" /> Votre clé de secours</h2>
            <p>Si vous oubliez votre code personnel, <strong>seule cette clé</strong> permet de retrouver vos données. Nous ne la connaissons pas et ne pourrons pas la retrouver.</p>
            <p className="cle-secours" aria-label="Clé de secours">{secours}</p>
            <div className="ligne-actions">
              <button className="bouton secondaire" onClick={() => telecharger('YEBA-Studio-cle-de-secours.txt', `YEBA Studio — clé de secours\nPoste : ${poste}\nCréée le : ${new Date().toLocaleDateString('fr-FR')}\n\n${secours}\n\nConservez ce fichier hors de ce PC (clé USB, coffre-fort).`, 'text/plain;charset=utf-8')}>
                Télécharger la clé
              </button>
              <button className="bouton secondaire" onClick={() => print()}>Imprimer</button>
            </div>
            <label className="champ-case">
              <input type="checkbox" checked={note} onChange={(e) => setNote(e.target.checked)} /> J’ai noté ma clé de secours en lieu sûr
            </label>
            <button className="bouton large" disabled={!note} onClick={() => onOuvert(ouvert.current, true)}>
              <Sparkles size={18} aria-hidden="true" /> Entrer dans mon espace
            </button>
          </>,
        )}

      {etape === 'ouvrir' &&
        carte(
          <form onSubmit={ouvrir}>
            <h2><Lock aria-hidden="true" /> Ouvrir mon espace</h2>
            {champPin(pin, setPin, 'Code personnel', 'pin', 'current-password')}
            <div className="ligne-actions">
              <button type="button" className="lien-discret" onClick={() => (setEtape('secours'), setErreur(''))}>Code oublié ?</button>
              <button className="bouton" disabled={attente}>{attente ? 'Vérification…' : 'Ouvrir'}</button>
            </div>
            <button type="button" className="lien-discret" onClick={() => setEtape('choix')}>← Retour</button>
          </form>,
        )}

      {etape === 'secours' &&
        carte(
          <form onSubmit={recuperer}>
            <h2><KeyRound aria-hidden="true" /> Récupérer mon espace</h2>
            <label className="champ" htmlFor="secours">
              <span>Clé de secours</span>
              <input id="secours" value={secours} onChange={(e) => setSecours(e.target.value.toUpperCase())} placeholder="XXXX-XXXX-XXXX-XXXX-XXXX" maxLength={24} autoComplete="off" required />
            </label>
            {champPin(pin, setPin, 'Nouveau code personnel', 'pin-n', 'new-password')}
            <div className="ligne-actions">
              <button type="button" className="bouton secondaire" onClick={() => setEtape('ouvrir')}>Retour</button>
              <button className="bouton" disabled={attente}>{attente ? 'Vérification…' : 'Récupérer'}</button>
            </div>
          </form>,
        )}
    </div>
  )
}

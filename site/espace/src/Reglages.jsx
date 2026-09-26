// Réglages : sauvegarde chiffrée, restauration, code personnel, journal, verrouillage.
import { useRef, useState } from 'react'
import { DatabaseBackup, History, KeyRound, Lock, Trash2, Upload } from 'lucide-react'
import { changerPin, exporterSauvegarde, importerSauvegarde, ouvrirCoffre, reinitialiser } from './stockage.js'
import { telecharger } from './ui.jsx'

export default function Reglages({ donnees, remplacer, verrouiller, demo }) {
  const [mdp, setMdp] = useState('')
  const [message, setMessage] = useState(null)
  const [ancien, setAncien] = useState('')
  const [nouveau, setNouveau] = useState('')
  const fichier = useRef(null)
  const dire = (ok, texte) => setMessage({ ok, texte })

  async function sauvegarder(e) {
    e.preventDefault()
    if (mdp.length < 8) return dire(false, 'Mot de passe de sauvegarde : 8 caractères minimum.')
    telecharger(`YEBA-Studio-sauvegarde-${new Date().toISOString().slice(0, 10)}.yeba`, await exporterSauvegarde(donnees, mdp), 'application/octet-stream')
    dire(true, 'Sauvegarde téléchargée. Rangez-la hors de ce PC (clé USB, cloud européen) avec son mot de passe.')
  }
  async function restaurer(e) {
    const f = e.target.files?.[0]
    e.target.value = ''
    if (!f) return
    try {
      const d = await importerSauvegarde(await f.text(), mdp)
      if (!confirm(`Remplacer toutes les données actuelles par la sauvegarde (${d.sessions?.length ?? 0} sessions, ${d.apprenants?.length ?? 0} stagiaires) ?`)) return
      remplacer(d)
      dire(true, 'Sauvegarde restaurée.')
    } catch (err) {
      dire(false, err.message)
    }
  }
  async function pin(e) {
    e.preventDefault()
    if (!/^\d{8,12}$/.test(nouveau)) return dire(false, 'Le nouveau code doit contenir 8 à 12 chiffres.')
    try {
      const { brut } = await ouvrirCoffre(ancien)
      await changerPin(brut, nouveau)
      setAncien('')
      setNouveau('')
      dire(true, 'Code personnel modifié.')
    } catch (err) {
      dire(false, err.message)
    }
  }
  async function effacerTout() {
    if (prompt('Tapez EFFACER pour supprimer définitivement toutes les données de ce poste.') !== 'EFFACER') return
    await reinitialiser()
    location.reload()
  }

  return (
    <div className="reglages">
      <div className="titre-module">
        <div>
          <h1>Réglages et sauvegardes</h1>
          <p className="chapo">Vos données ne quittent jamais ce PC, sauf si vous exportez une sauvegarde (elle-même chiffrée).</p>
        </div>
        {!demo && <button className="bouton secondaire" onClick={verrouiller}><Lock size={18} aria-hidden="true" /> Verrouiller maintenant</button>}
      </div>
      {message && <p className={message.ok ? 'succes' : 'erreur'} role="status">{message.texte}</p>}
      {demo ? (
        <p className="avertissement">Démo : rien n’est enregistré. Créez votre espace pour sauvegarder vos données.</p>
      ) : (
        <div className="bpf-grille">
          <section className="carte">
            <h2><DatabaseBackup size={20} aria-hidden="true" /> Sauvegarde</h2>
            <p className="note">Faites-en une chaque mois : si ce PC tombe en panne, c’est votre seule copie.</p>
            <form onSubmit={sauvegarder}>
              <label className="champ" htmlFor="mdp-s">
                <span>Mot de passe de la sauvegarde</span>
                <input id="mdp-s" type="password" value={mdp} onChange={(e) => setMdp(e.target.value)} autoComplete="new-password" minLength={8} maxLength={128} />
              </label>
              <div className="ligne-actions">
                <button type="button" className="bouton secondaire" onClick={() => fichier.current.click()} disabled={mdp.length < 8}><Upload size={18} aria-hidden="true" /> Restaurer</button>
                <button className="bouton">Télécharger la sauvegarde</button>
              </div>
              <input ref={fichier} type="file" accept=".yeba,application/json" hidden onChange={restaurer} />
            </form>
          </section>
          <section className="carte">
            <h2><KeyRound size={20} aria-hidden="true" /> Code personnel</h2>
            <form onSubmit={pin}>
              <label className="champ" htmlFor="pin-a"><span>Code actuel</span><input id="pin-a" type="password" inputMode="numeric" value={ancien} onChange={(e) => setAncien(e.target.value.replace(/\D/g, ''))} maxLength={12} autoComplete="current-password" /></label>
              <label className="champ" htmlFor="pin-n2"><span>Nouveau code</span><input id="pin-n2" type="password" inputMode="numeric" value={nouveau} onChange={(e) => setNouveau(e.target.value.replace(/\D/g, ''))} maxLength={12} autoComplete="new-password" /></label>
              <button className="bouton">Changer le code</button>
            </form>
          </section>
          <section className="carte large">
            <h2><History size={20} aria-hidden="true" /> Journal</h2>
            <ul className="journal">
              {donnees.journal.slice(0, 30).map((j, k) => <li key={k}><time>{new Date(j.date).toLocaleString('fr-FR')}</time> {j.message}</li>)}
              {!donnees.journal.length && <li className="note">Aucune action enregistrée.</li>}
            </ul>
          </section>
          <section className="carte large zone-danger">
            <h2><Trash2 size={20} aria-hidden="true" /> Zone sensible</h2>
            <p className="note">Supprime définitivement l’espace de ce poste (vos licences restent valables et réutilisables ici).</p>
            <button className="bouton danger" onClick={effacerTout}>Effacer toutes les données de ce poste</button>
          </section>
        </div>
      )}
    </div>
  )
}

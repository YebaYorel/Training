// « Mes données » : tout ce que l'organisme saisit une fois, et qui nourrit Parcours, le BPF, CARBURANT et les documents.
import { useState } from 'react'
import { Building2, CheckCircle2 } from 'lucide-react'
import Collection, { Champ } from './Collection.jsx'
import { CHAMPS_ORGANISME, SCHEMAS } from './modele.js'
import { Jauge } from './ui.jsx'

const ONGLETS = [['organisme', 'Mon organisme'], ...['formations', 'formateurs', 'clients', 'apprenants', 'sessions', 'inscriptions', 'factures'].map((k) => [k, SCHEMAS[k].titre])]

export function completudeOrganisme(o = {}) {
  const requis = CHAMPS_ORGANISME.filter((c) => c.requis)
  const faits = requis.filter((c) => String(o[c.cle] ?? '').trim())
  return { taux: (faits.length / requis.length) * 100, manquants: requis.filter((c) => !faits.includes(c)).map((c) => c.libelle) }
}

function FicheOrganisme({ donnees, modifier }) {
  const [o, setO] = useState(donnees.organisme)
  const [ok, setOk] = useState(false)
  const c = completudeOrganisme(o)
  function enregistrer(e) {
    e.preventDefault()
    modifier((d) => (d.organisme = { ...o, siret: String(o.siret || '').replace(/\s/g, '') }), 'Fiche organisme mise à jour')
    setOk(true)
    setTimeout(() => setOk(false), 2500)
  }
  return (
    <form className="carte fiche-organisme" onSubmit={enregistrer} noValidate>
      <div className="titre-bloc">
        <Building2 aria-hidden="true" />
        <div>
          <h2>Mon organisme</h2>
          <p className="note">Ces informations remplissent automatiquement vos documents Word, convocations et attestations.</p>
        </div>
      </div>
      <Jauge valeur={c.taux} libelle="Fiche complète" />
      {c.manquants.length > 0 && <p className="note">Il manque : {c.manquants.join(', ')}.</p>}
      <div className="grille-champs">
        {CHAMPS_ORGANISME.map((ch) => <Champ key={ch.cle} id={'o-' + ch.cle} champ={ch} valeur={o[ch.cle]} donnees={donnees} onChange={(v) => setO({ ...o, [ch.cle]: v })} />)}
      </div>
      <div className="ligne-actions">
        <span role="status">{ok && <><CheckCircle2 size={18} aria-hidden="true" className="ok" /> Enregistré</>}</span>
        <button className="bouton" type="submit">Enregistrer</button>
      </div>
    </form>
  )
}

export default function Donnees({ donnees, modifier }) {
  const [onglet, setOnglet] = useState('organisme')
  return (
    <div>
      <div className="titre-module">
        <div>
          <h1>Mes données</h1>
          <p className="chapo">Saisies une fois, réutilisées partout. Chiffrées sur ce poste : personne d’autre n’y a accès, pas même YEBA FORMATIONS.</p>
        </div>
      </div>
      <div className="onglets-module defilant" role="tablist" aria-label="Catégories">
        {ONGLETS.map(([id, l]) => (
          <button key={id} role="tab" aria-selected={onglet === id} className="onglet-module" onClick={() => setOnglet(id)}>
            {l}{id !== 'organisme' && <span className="compteur">{donnees[id].length}</span>}
          </button>
        ))}
      </div>
      <div className="espace-onglet">
        {onglet === 'organisme' ? <FicheOrganisme donnees={donnees} modifier={modifier} /> : <Collection key={onglet} collection={onglet} donnees={donnees} modifier={modifier} />}
      </div>
    </div>
  )
}

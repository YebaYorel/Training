// Pack Qualiopi V10 : 24 modèles Word, pré-remplis avec la fiche organisme, régénérables à volonté.
import { useState } from 'react'
import { AlertTriangle, Download, FileText, Package } from 'lucide-react'
import { CATEGORIES, MODELES } from './modeles-qualiopi.js'
import { genererDocx, nomFichier, telechargerBlob } from './word.js'
import { completudeOrganisme } from './Donnees.jsx'

export default function Modeles({ donnees, essai, aller }) {
  const [formation, setFormation] = useState(donnees.formations[0]?.id || '')
  const [etat, setEtat] = useState('')
  const o = donnees.organisme
  const c = completudeOrganisme(o)
  const ctx = { formation: donnees.formations.find((f) => f.id === formation) }

  async function un(m) {
    setEtat(`Préparation de « ${m.titre} »…`)
    const blob = await genererDocx({ titre: m.titre, organisme: o, blocs: m.blocs(o, ctx), essai, sujet: `Qualiopi — indicateurs ${m.indicateurs.join(', ')}` })
    telechargerBlob(nomFichier(m.titre), blob)
    setEtat('')
  }

  async function tout() {
    setEtat('Préparation du pack complet…')
    const { default: JSZip } = await import('jszip')
    const zip = new JSZip()
    for (const [i, m] of MODELES.entries()) {
      setEtat(`Préparation ${i + 1}/${MODELES.length} : ${m.titre}`)
      const blob = await genererDocx({ titre: m.titre, organisme: o, blocs: m.blocs(o, ctx), essai })
      zip.folder(m.categorie).file(nomFichier(m.titre), blob)
    }
    zip.file('LISEZ-MOI.txt', `Pack Qualiopi V10 — ${o.nom || ''}\nGénéré le ${new Date().toLocaleDateString('fr-FR')} avec YEBA Studio.\n\nLes zones surlignées en jaune « [À COMPLÉTER : …] » sont à renseigner.\nCes modèles sont à adapter à votre activité ; la conformité est appréciée par votre organisme certificateur.\n`)
    telechargerBlob(nomFichier('Pack-Qualiopi-' + (o.nom || 'organisme')).replace('.docx', '.zip'), await zip.generateAsync({ type: 'blob' }))
    setEtat('')
  }

  return (
    <div className="modeles">
      <div className="titre-module">
        <div>
          <h1>Pack Qualiopi V10</h1>
          <p className="chapo">{MODELES.length} modèles Word modifiables, remplis avec votre fiche organisme. Régénérez-les à chaque changement.</p>
        </div>
        <div className="actions">
          <button className="bouton" onClick={tout} disabled={!!etat}><Package size={18} aria-hidden="true" /> Tout télécharger (.zip)</button>
        </div>
      </div>
      {c.taux < 100 && (
        <p className="avertissement">
          <AlertTriangle size={18} aria-hidden="true" /> Fiche organisme complète à {Math.round(c.taux)} % : les informations manquantes apparaîtront surlignées en jaune dans Word.{' '}
          <button className="lien-discret" onClick={() => aller('donnees')}>Compléter ma fiche</button>
        </p>
      )}
      {essai && <p className="avertissement"><AlertTriangle size={18} aria-hidden="true" /> Essai : les documents portent la mention « document d’essai, non valable ».</p>}
      <label className="champ-select">
        <span>Formation utilisée pour le modèle de programme</span>
        <select value={formation} onChange={(e) => setFormation(e.target.value)}>
          <option value="">— modèle vierge —</option>
          {donnees.formations.map((f) => <option key={f.id} value={f.id}>{f.intitule}</option>)}
        </select>
      </label>
      {etat && <p className="note" role="status">{etat}</p>}
      {CATEGORIES.map((cat) => (
        <section key={cat} className="critere-bloc">
          <h2>{cat}</h2>
          <ul className="liste-modeles">
            {MODELES.filter((m) => m.categorie === cat).map((m) => (
              <li key={m.id} className="carte">
                <FileText size={26} aria-hidden="true" />
                <div>
                  <strong>{m.titre}</strong>
                  <span>Indicateur{m.indicateurs.length > 1 ? 's' : ''} {m.indicateurs.join(', ')}</span>
                </div>
                <button className="bouton secondaire" onClick={() => un(m)} disabled={!!etat} aria-label={'Télécharger ' + m.titre}>
                  <Download size={18} aria-hidden="true" /> Word
                </button>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  )
}

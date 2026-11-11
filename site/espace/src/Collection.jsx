// Liste + formulaire générique, piloté par les schémas de modele.js. Import / export CSV inclus.
import { useMemo, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Download, Pencil, Plus, Search, Trash2, Upload, X } from 'lucide-react'
import { SCHEMAS, dateIso, lireCsv, nombre, nouvelId, versCsv } from './modele.js'
import { telecharger } from './ui.jsx'

const normaliser = (t) => String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '')

export function Champ({ champ, valeur, onChange, donnees, id }) {
  const commun = { id, value: valeur ?? '', onChange: (e) => onChange(e.target.value), required: champ.requis, 'aria-describedby': champ.aide ? id + '-aide' : undefined }
  let saisie
  switch (champ.type) {
    case 'textarea':
      saisie = <textarea rows={3} maxLength={4000} {...commun} />
      break
    case 'select':
      saisie = (
        <select {...commun}>
          <option value="">— choisir —</option>
          {champ.options.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
      )
      break
    case 'ref': {
      const s = SCHEMAS[champ.ref]
      saisie = (
        <select {...commun}>
          <option value="">— choisir —</option>
          {(donnees[champ.ref] || []).map((x) => <option key={x.id} value={x.id}>{s.affichage(x, donnees)}</option>)}
        </select>
      )
      break
    }
    case 'bool':
      saisie = <input type="checkbox" id={id} checked={!!valeur} onChange={(e) => onChange(e.target.checked)} />
      break
    case 'number':
      saisie = <input type="number" step="any" inputMode="decimal" {...commun} onChange={(e) => onChange(e.target.value === '' ? '' : Number(e.target.value))} />
      break
    case 'color':
      saisie = <input type="color" {...commun} value={valeur || '#1B3A6B'} />
      break
    default:
      saisie = <input type={champ.type || 'text'} maxLength={300} {...commun} />
  }
  return (
    <label className={'champ' + (champ.type === 'bool' ? ' champ-case' : '')} htmlFor={id}>
      <span>{champ.libelle}{champ.requis && <abbr title="obligatoire"> *</abbr>}</span>
      {saisie}
      {champ.aide && <small id={id + '-aide'}>{champ.aide}</small>}
    </label>
  )
}

function Fiche({ schema, collection, element, donnees, onValider, onFermer }) {
  const [v, setV] = useState(element || {})
  const [erreur, setErreur] = useState('')
  function valider(e) {
    e.preventDefault()
    const manque = schema.champs.filter((c) => c.requis && (v[c.cle] === undefined || v[c.cle] === ''))
    if (manque.length) return setErreur('À compléter : ' + manque.map((c) => c.libelle).join(', '))
    if (collection === 'sessions' && v.fin && v.debut && v.fin < v.debut) return setErreur('La date de fin précède la date de début.')
    onValider({ ...v, id: v.id || nouvelId() })
  }
  return (
    <motion.div className="fond-fiche" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={(e) => e.target === e.currentTarget && onFermer()}>
      <motion.form className="fiche" noValidate onSubmit={valider} role="dialog" aria-modal="true" aria-labelledby="fiche-t" initial={{ x: 40 }} animate={{ x: 0 }} exit={{ x: 40 }} data-lenis-prevent>
        <div className="fiche-tete">
          <h2 id="fiche-t">{element ? 'Modifier' : 'Ajouter'} {schema.singulier === 'inscription' ? 'une inscription' : `un${['formation', 'session', 'facture'].includes(schema.singulier) ? 'e' : ''} ${schema.singulier}`}</h2>
          <button type="button" className="bouton-icone" onClick={onFermer} aria-label="Fermer"><X size={20} /></button>
        </div>
        <div className="fiche-corps">
          {schema.champs.map((c) => <Champ key={c.cle} id={'f-' + c.cle} champ={c} valeur={v[c.cle]} donnees={donnees} onChange={(x) => setV({ ...v, [c.cle]: x })} />)}
        </div>
        {erreur && <p className="erreur" role="alert">{erreur}</p>}
        <div className="fiche-pied">
          <button type="button" className="bouton secondaire" onClick={onFermer}>Annuler</button>
          <button type="submit" className="bouton">Enregistrer</button>
        </div>
      </motion.form>
    </motion.div>
  )
}

/** Import CSV : les colonnes sont reconnues par leur libellé ou leur clé ; les références par leur nom. */
export function importerCsv(texte, collection, donnees) {
  const schema = SCHEMAS[collection]
  const [entete, ...lignes] = lireCsv(texte)
  if (!entete) throw new Error('Fichier vide.')
  const colonnes = entete.map((h) => schema.champs.find((c) => [normaliser(c.libelle), normaliser(c.cle)].includes(normaliser(h)) || normaliser(c.libelle).startsWith(normaliser(h)) && normaliser(h).length > 3))
  if (!colonnes.some(Boolean)) throw new Error('Aucune colonne reconnue. Utilisez le modèle CSV (bouton « Modèle »).')
  const ajouts = []
  const rejets = []
  lignes.forEach((l, n) => {
    const x = { id: nouvelId() }
    colonnes.forEach((c, i) => {
      if (!c) return
      let val = (l[i] ?? '').trim()
      if (c.type === 'number') val = nombre(val) ?? ''
      else if (c.type === 'date') val = dateIso(val)
      else if (c.type === 'bool') val = /^(oui|vrai|x|1|true)$/i.test(val)
      else if (c.type === 'ref') {
        const cible = (donnees[c.ref] || []).find((r) => normaliser(SCHEMAS[c.ref].affichage(r, donnees)) === normaliser(val) || normaliser(r.nom || r.intitule || r.numero) === normaliser(val))
        val = cible?.id || ''
      } else if (c.type === 'select') val = c.options.find((o) => normaliser(o) === normaliser(val)) || ''
      x[c.cle] = val
    })
    const manque = schema.champs.filter((c) => c.requis && (x[c.cle] === '' || x[c.cle] === undefined))
    if (manque.length) rejets.push(`Ligne ${n + 2} : ${manque.map((c) => c.libelle).join(', ')} manquant(s) ou non reconnu(s)`)
    else ajouts.push(x)
  })
  return { ajouts, rejets }
}

export default function Collection({ collection, donnees, modifier, filtre }) {
  const schema = SCHEMAS[collection]
  const [edition, setEdition] = useState(null)
  const [recherche, setRecherche] = useState('')
  const [message, setMessage] = useState('')
  const fichier = useRef(null)
  const liste = useMemo(
    () => (donnees[collection] || []).filter((x) => (!filtre || filtre(x)) && (!recherche || normaliser(schema.affichage(x, donnees)).includes(normaliser(recherche)))),
    [donnees, collection, recherche, filtre, schema],
  )
  const visibles = schema.champs.filter((c) => !['textarea'].includes(c.type)).slice(0, 5)
  const afficher = (c, x) => {
    const v = x[c.cle]
    if (c.type === 'ref') return (donnees[c.ref] || []).find((r) => r.id === v) ? SCHEMAS[c.ref].affichage(donnees[c.ref].find((r) => r.id === v), donnees) : '—'
    if (c.type === 'date') return v ? new Date(v + 'T12:00:00').toLocaleDateString('fr-FR') : '—'
    if (c.type === 'bool') return v ? 'Oui' : '—'
    if (c.type === 'number' && v !== '' && v != null) return Number(v).toLocaleString('fr-FR')
    return v || '—'
  }

  function enregistrer(x) {
    modifier((d) => {
      const l = d[collection]
      const i = l.findIndex((y) => y.id === x.id)
      if (i >= 0) l[i] = x
      else l.push(x)
    }, `${schema.singulier} ${edition === 'nouveau' ? 'ajouté(e)' : 'modifié(e)'}`)
    setEdition(null)
  }
  function supprimer(x) {
    const liees = collection === 'sessions' ? donnees.inscriptions.filter((i) => i.session === x.id).length : collection === 'apprenants' ? donnees.inscriptions.filter((i) => i.apprenant === x.id).length : 0
    if (!confirm(`Supprimer « ${schema.affichage(x, donnees)} » ?${liees ? `\n${liees} inscription(s) liée(s) seront aussi supprimées.` : ''}`)) return
    modifier((d) => {
      d[collection] = d[collection].filter((y) => y.id !== x.id)
      if (collection === 'sessions') d.inscriptions = d.inscriptions.filter((i) => i.session !== x.id)
      if (collection === 'apprenants') d.inscriptions = d.inscriptions.filter((i) => i.apprenant !== x.id)
      const restantes = new Set(d.inscriptions.map((i) => i.id))
      d.presences = d.presences.filter((p) => restantes.has(p.inscription))
    }, `${schema.singulier} supprimé(e)`)
  }
  async function importer(e) {
    const f = e.target.files?.[0]
    e.target.value = ''
    if (!f) return
    if (f.size > 2_000_000) return setMessage('Fichier trop lourd (2 Mo maximum).')
    try {
      const { ajouts, rejets } = importerCsv(await f.text(), collection, donnees)
      if (ajouts.length) modifier((d) => d[collection].push(...ajouts), `${ajouts.length} ligne(s) importée(s)`)
      setMessage(`${ajouts.length} ligne(s) importée(s).${rejets.length ? ` ${rejets.length} ignorée(s) : ${rejets.slice(0, 3).join(' · ')}` : ''}`)
    } catch (err) {
      setMessage(err.message)
    }
  }
  const exporter = (modele) =>
    telecharger(
      `${collection}${modele ? '-modele' : ''}.csv`,
      versCsv([schema.champs.map((c) => c.libelle), ...(modele ? [] : (donnees[collection] || []).map((x) => schema.champs.map((c) => (c.type === 'ref' || c.type === 'date' || c.type === 'bool' ? afficher(c, x) : x[c.cle]))))]),
    )

  return (
    <section className="collection" aria-label={schema.titre}>
      <div className="barre-outils">
        <label className="recherche">
          <Search size={18} aria-hidden="true" />
          <span className="sr-only">Rechercher</span>
          <input type="search" placeholder={`Rechercher (${(donnees[collection] || []).length})`} value={recherche} onChange={(e) => setRecherche(e.target.value)} maxLength={60} />
        </label>
        <div className="actions">
          <button className="bouton" onClick={() => setEdition('nouveau')}><Plus size={18} aria-hidden="true" /> Ajouter</button>
          <button className="bouton secondaire" onClick={() => fichier.current.click()}><Upload size={18} aria-hidden="true" /> Importer</button>
          <button className="bouton secondaire" onClick={() => exporter(false)}><Download size={18} aria-hidden="true" /> Exporter</button>
          <button className="lien-discret" onClick={() => exporter(true)}>Modèle CSV</button>
          <input ref={fichier} type="file" accept=".csv,text/csv" hidden onChange={importer} />
        </div>
      </div>
      {message && <p className="note" role="status">{message}</p>}
      {liste.length ? (
        <div className="table-defile carte">
          <table>
            <thead>
              <tr>{visibles.map((c) => <th key={c.cle}>{c.libelle}</th>)}<th><span className="sr-only">Actions</span></th></tr>
            </thead>
            <tbody>
              {liste.map((x) => (
                <tr key={x.id}>
                  {visibles.map((c, k) => (k === 0 ? <th scope="row" key={c.cle}>{afficher(c, x)}</th> : <td key={c.cle}>{afficher(c, x)}</td>))}
                  <td className="actions-ligne">
                    <button className="bouton-icone" onClick={() => setEdition(x)} aria-label={'Modifier ' + schema.affichage(x, donnees)}><Pencil size={16} /></button>
                    <button className="bouton-icone danger" onClick={() => supprimer(x)} aria-label={'Supprimer ' + schema.affichage(x, donnees)}><Trash2 size={16} /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="vide-etat carte">
          <p><strong>Aucun{['formation', 'session', 'facture', 'inscription'].includes(schema.singulier) ? 'e' : ''} {schema.singulier} pour l’instant.</strong></p>
          <p className="note">Ajoutez-en un{['formation', 'session', 'facture', 'inscription'].includes(schema.singulier) ? 'e' : ''}, ou importez votre fichier Excel enregistré en CSV (le « Modèle CSV » donne les colonnes attendues).</p>
        </div>
      )}
      <AnimatePresence>
        {edition && <Fiche schema={schema} collection={collection} element={edition === 'nouveau' ? null : edition} donnees={donnees} onValider={enregistrer} onFermer={() => setEdition(null)} />}
      </AnimatePresence>
    </section>
  )
}

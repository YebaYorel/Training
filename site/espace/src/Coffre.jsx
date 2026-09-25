// Coffre Qualiopi : les 33 indicateurs du RNQ, leurs preuves, et les documents officiels.
import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { ChevronDown, Download, FileText, Paperclip, Printer, Search } from 'lucide-react'
import { Jauge, dateFr, telecharger } from './ui.jsx'
import { preparationQualiopi } from './Tableau.jsx'

const FILTRES = [
  ['tous', 'Tous'],
  ['Non conforme', 'Non conformes'],
  ['En cours', 'En cours'],
  ['✅ Conforme', 'Conformes'],
  ['Non applicable', 'Non applicables'],
]
const classeStatut = (s) => (s.includes('Non conforme') ? 'rouge' : s.includes('En cours') ? 'jaune' : s.includes('Non applicable') ? 'gris' : s.includes('Conforme') ? 'vert' : 'gris')

function csvIndicateurs(ind) {
  const c = (v) => `"${String(v ?? '').replace(/"/g, '""').replace(/^([=+\-@])/, "'$1")}"`
  const l = [['Indicateur', 'Critère', 'Statut', 'Score', 'Dernière vérification', 'Documents', 'Responsable', 'Actions correctives']]
  for (const i of ind) l.push([i.n, i.critere, i.statut, i.score, i.verif || '', i.documents.join(' '), i.responsable, i.actions])
  return '﻿' + l.map((x) => x.map(c).join(';')).join('\r\n')
}

export default function Coffre({ db }) {
  const [vue, setVue] = useState('indicateurs')
  const [filtre, setFiltre] = useState('tous')
  const [recherche, setRecherche] = useState('')
  const [ouvert, setOuvert] = useState(null)
  const q = preparationQualiopi(db.indicateurs)
  const prochain = db.indicateurs.map((i) => i.prochainAudit).filter(Boolean).sort()[0]
  const docsParRef = useMemo(() => Object.fromEntries(db.documents.flatMap((d) => [[d.ref, d], [d.id, d]])), [db])
  const liste = db.indicateurs.filter(
    (i) =>
      (filtre === 'tous' || i.statut.includes(filtre)) &&
      (!recherche || `${i.n} ${i.libelle} ${i.preuves}`.toLowerCase().includes(recherche.toLowerCase())),
  )
  const criteres = [...new Set(db.indicateurs.map((i) => i.critere))].filter(Boolean).sort()
  const compte = (s) => db.indicateurs.filter((i) => i.statut.includes(s)).length

  return (
    <div className="coffre">
      <div className="titre-module">
        <div>
          <h1>Coffre Qualiopi</h1>
          <p className="chapo">Référentiel national qualité · 33 indicateurs · décret n° 2026-728 (audits à partir du 01/11/2026)</p>
        </div>
        <div className="actions">
          <button className="bouton secondaire" onClick={() => telecharger('coffre-qualiopi.csv', csvIndicateurs(db.indicateurs))}>
            <Download size={18} aria-hidden="true" /> Exporter (CSV)
          </button>
          <button className="bouton secondaire" onClick={() => print()}>
            <Printer size={18} aria-hidden="true" /> Imprimer
          </button>
        </div>
      </div>

      <div className="bandeau-preparation carte">
        <div>
          <strong>{Math.round(q.taux)} % prêt pour l’audit</strong>
          <Jauge valeur={q.taux} libelle="Préparation" />
        </div>
        <ul className="pastilles-statut">
          <li className="vert">{compte('✅ Conforme')} conformes</li>
          <li className="jaune">{compte('En cours')} en cours</li>
          <li className="rouge">{compte('Non conforme')} non conformes</li>
          <li className="gris">{compte('Non applicable')} non applicables</li>
        </ul>
        <p>Prochain audit : <strong>{dateFr(prochain)}</strong></p>
      </div>

      <div className="onglets-module" role="tablist">
        {[['indicateurs', 'Indicateurs et preuves'], ['documents', `Documents officiels (${db.documents.length})`]].map(([id, l]) => (
          <button key={id} role="tab" aria-selected={vue === id} className="onglet-module" onClick={() => setVue(id)}>{l}</button>
        ))}
      </div>

      {vue === 'indicateurs' ? (
        <>
          <div className="barre-outils">
            <label className="recherche">
              <Search size={18} aria-hidden="true" />
              <span className="sr-only">Rechercher un indicateur</span>
              <input type="search" placeholder="Rechercher (n°, mot-clé…)" value={recherche} onChange={(e) => setRecherche(e.target.value)} maxLength={60} />
            </label>
            <div className="filtres-module" role="group" aria-label="Filtrer par statut">
              {FILTRES.map(([id, l]) => (
                <button key={id} aria-pressed={filtre === id} className="puce" onClick={() => setFiltre(id)}>{l}</button>
              ))}
            </div>
          </div>
          {criteres.map((c) => {
            const lignes = liste.filter((i) => i.critere === c)
            if (!lignes.length) return null
            const titre = db.indicateurs.find((i) => i.critere === c)?.critereTexte || ''
            return (
              <section key={c} className="critere-bloc" aria-label={`Critère ${c}`}>
                <h2><span className="num">{c}</span> {titre.replace(/^Critère \d+ — /, '')}</h2>
                <ul className="indicateurs">
                  {lignes.map((i) => (
                    <li key={i.n} className={'indicateur ' + classeStatut(i.statut)}>
                      <button className="indicateur-tete" aria-expanded={ouvert === i.n} onClick={() => setOuvert(ouvert === i.n ? null : i.n)}>
                        <span className="ind-num">{i.n}</span>
                        <span className="ind-lib">{i.libelle}</span>
                        <span className={'badge-statut ' + classeStatut(i.statut)}>{i.statut.replace(/^[^\p{L}]+/u, '')}</span>
                        <span className="ind-docs" title="Documents rattachés"><Paperclip size={15} aria-hidden="true" /> {i.nbDocs + i.fichiers.length}</span>
                        <ChevronDown className="chevron" size={20} aria-hidden="true" />
                      </button>
                      <AnimatePresence initial={false}>
                        {ouvert === i.n && (
                          <motion.div className="indicateur-corps" initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.25 }}>
                            <dl>
                              {i.preuves && (<><dt>Preuves attendues</dt><dd className="pre">{i.preuves}</dd></>)}
                              {i.score && (<><dt>Auto-évaluation</dt><dd>{i.score}</dd></>)}
                              <dt>Dernière vérification</dt><dd>{dateFr(i.verif)}{i.responsable && ` · ${i.responsable}`}</dd>
                              {i.observations && (<><dt>Observations</dt><dd className="pre">{i.observations}</dd></>)}
                              {i.actions && (<><dt>Actions correctives</dt><dd className="pre">{i.actions}</dd></>)}
                            </dl>
                            {(i.documents.length > 0 || i.fichiers.length > 0) && (
                              <ul className="preuves">
                                {i.documents.map((r) => {
                                  const d = docsParRef[r]
                                  return (
                                    <li key={r}><FileText size={16} aria-hidden="true" /> {d ? `${d.ref} — ${d.titre} (v${d.version})` : r}</li>
                                  )
                                })}
                                {i.fichiers.map((f) => (
                                  <li key={f.nom}>
                                    <Paperclip size={16} aria-hidden="true" />{' '}
                                    {f.url ? <a href={f.url} target="_blank" rel="noopener noreferrer">{f.nom}</a> : f.nom}
                                  </li>
                                ))}
                              </ul>
                            )}
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </li>
                  ))}
                </ul>
              </section>
            )
          })}
          {!liste.length && <p className="vide">Aucun indicateur ne correspond.</p>}
        </>
      ) : (
        <div className="table-defile carte">
          <table>
            <thead>
              <tr><th>Réf.</th><th>Document</th><th>Version</th><th>Date</th><th>Statut</th><th>Indicateurs</th></tr>
            </thead>
            <tbody>
              {db.documents.slice().sort((a, b) => a.ref.localeCompare(b.ref)).map((d) => {
                const age = d.date ? (Date.now() - new Date(d.date)) / 86400000 : 0
                return (
                  <tr key={d.id}>
                    <th scope="row">{d.ref}</th>
                    <td>{d.titre}</td>
                    <td>{d.version}</td>
                    <td>{dateFr(d.date)}{age > 365 && <span className="badge-statut jaune">à réviser</span>}</td>
                    <td><span className={'badge-statut ' + (d.statut === 'En vigueur' ? 'vert' : d.statut.startsWith('Incomplet') ? 'rouge' : 'jaune')}>{d.statut}</span></td>
                    <td>{d.rnq}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

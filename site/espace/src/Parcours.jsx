// Parcours : planning, dossiers stagiaires, émargements, évaluations et documents — session par session.
// Mode local (client) : tout se modifie ici et s'enregistre chiffré. Mode Airtable interne : lecture seule.
import { useMemo, useState } from 'react'
import { Check, ChevronLeft, ChevronRight, Download, FileText, Minus, Plus, UserPlus, X } from 'lucide-react'
import { PIECES } from './pieces.js'
import { FINANCEMENTS, nouvelId } from './modele.js'
import { Jauge, dateFr, telecharger, useIndex } from './ui.jsx'
import { DOCS_STAGIAIRE, emargementSession } from './documents-session.js'
import { genererDocx, nomFichier, telechargerBlob } from './word.js'

const JOURS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
const iso = (d) => d.toISOString().slice(0, 10)
function joursEntre(debut, fin) {
  const r = []
  if (!debut) return r
  for (let d = new Date(debut + 'T12:00:00'); iso(d) <= (fin || debut); d.setDate(d.getDate() + 1)) r.push(iso(d))
  return r
}
const resultatDe = (note, max = 20) => (note == null || note === '' ? '' : note / max >= 0.7 ? 'Acquis' : note / max >= 0.5 ? 'En cours d’acquisition' : 'Non acquis')

export default function Parcours({ db, donnees, modifier, essai, aller }) {
  const index = useIndex(db)
  const [vue, setVue] = useState('planning')
  const trie = useMemo(() => db.sessions.filter((s) => s.debut).sort((a, b) => b.debut.localeCompare(a.debut)), [db])
  const [choisie, setChoisie] = useState(() => trie.find((s) => s.statut === 'Terminée')?.id || trie[0]?.id)
  const session = index.sessions[choisie]

  return (
    <div className="parcours">
      <div className="titre-module">
        <div>
          <h1>Parcours</h1>
          <p className="chapo">Planning, dossiers, émargements, évaluations et documents — session par session.</p>
        </div>
        <div className="actions">
          {modifier && <button className="bouton secondaire" onClick={() => aller('donnees')}><Plus size={18} aria-hidden="true" /> Nouvelle session</button>}
          <div className="onglets-module" role="tablist">
            {[['planning', 'Planning'], ['sessions', 'Sessions']].map(([id, l]) => (
              <button key={id} role="tab" aria-selected={vue === id} className="onglet-module" onClick={() => setVue(id)}>{l}</button>
            ))}
          </div>
        </div>
      </div>

      {!trie.length ? (
        <div className="vide-etat carte">
          <p><strong>Aucune session pour l’instant.</strong></p>
          <p className="note">Créez une formation puis une session dans « Mes données » : elle apparaîtra ici avec son planning, ses dossiers et ses émargements.</p>
          {modifier && <button className="bouton" onClick={() => aller('donnees')}>Créer ma première session</button>}
        </div>
      ) : (
        <div className="parcours-grille">
          <div className="carte">
            {vue === 'planning' ? (
              <Calendrier sessions={trie} choisie={choisie} onChoisir={setChoisie} />
            ) : (
              <ul className="liste-sessions">
                {trie.map((s) => (
                  <li key={s.id}>
                    <button className={'ligne-session' + (s.id === choisie ? ' actif' : '')} aria-pressed={s.id === choisie} onClick={() => setChoisie(s.id)}>
                      <span className="ls-date">{dateFr(s.debut)}</span>
                      <strong>{s.formation}</strong>
                      <span>{s.type} · {(index.inscritsPar[s.id] || []).length} stagiaire(s) · {s.statut}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          {session && <DetailSession key={session.id} db={db} donnees={donnees} modifier={modifier} essai={essai} s={session} inscrits={index.inscritsPar[session.id] || []} />}
        </div>
      )}
    </div>
  )
}

function Calendrier({ sessions, choisie, onChoisir }) {
  const [mois, setMois] = useState(() => {
    const d = new Date()
    return new Date(d.getFullYear(), d.getMonth(), 1)
  })
  const premier = (mois.getDay() + 6) % 7
  const nb = new Date(mois.getFullYear(), mois.getMonth() + 1, 0).getDate()
  const cases = [...Array(premier).fill(null), ...Array.from({ length: nb }, (_, i) => new Date(mois.getFullYear(), mois.getMonth(), i + 1, 12))]
  const parJour = {}
  for (const s of sessions) for (const j of joursEntre(s.debut, s.fin)) (parJour[j] ||= []).push(s)
  const decaler = (n) => setMois(new Date(mois.getFullYear(), mois.getMonth() + n, 1))
  const auj = iso(new Date())
  return (
    <div className="calendrier">
      <div className="cal-tete">
        <button className="bouton-icone" onClick={() => decaler(-1)} aria-label="Mois précédent"><ChevronLeft size={20} /></button>
        <h2 aria-live="polite">{mois.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}</h2>
        <button className="bouton-icone" onClick={() => decaler(1)} aria-label="Mois suivant"><ChevronRight size={20} /></button>
      </div>
      <div className="cal-grille" role="grid" aria-label="Planning du mois">
        {JOURS.map((j) => <div key={j} className="cal-jour-nom" role="columnheader">{j}</div>)}
        {cases.map((d, k) =>
          d ? (
            <div key={k} role="gridcell" className={'cal-case' + (iso(d) === auj ? ' aujourdhui' : '')}>
              <span className="cal-num">{d.getDate()}</span>
              {(parJour[iso(d)] || []).map((s) => (
                <button key={s.id} className={'cal-session' + (s.id === choisie ? ' actif' : '')} onClick={() => onChoisir(s.id)} title={s.formation}>
                  {s.formation.split(' — ')[0]}
                </button>
              ))}
            </div>
          ) : (
            <div key={k} className="cal-case vide" aria-hidden="true" />
          ),
        )}
      </div>
    </div>
  )
}

function DetailSession({ db, donnees, modifier, essai, s, inscrits }) {
  const [onglet, setOnglet] = useState('dossiers')
  const [nouvel, setNouvel] = useState({ apprenant: '', financement: 'Plan PDC' })
  const [etat, setEtat] = useState('')
  const edition = !!modifier
  const jours = joursEntre(s.debut, s.fin)
  const nomDe = (i) => db.apprenants[i.apprenant]?.nom || '—'
  const client = db.clients[s.client]
  const pieces = inscrits.flatMap((i) => Object.values(i.pieces))
  const taux = pieces.length ? (pieces.filter(Boolean).length / pieces.length) * 100 : 0

  function piece(ins, k) {
    modifier((d) => {
      const i = d.inscriptions.find((x) => x.id === ins.id)
      i.pieces = { ...(i.pieces || {}), [k]: !i.pieces?.[k] }
    }, null)
  }
  // Cycle d'une case : vide → présent → absent → absence justifiée → vide
  function emarger(ins, jour, demi) {
    modifier((d) => {
      let p = d.presences.find((x) => x.inscription === ins.id && x.date === jour)
      if (!p) {
        d.presences.push({ id: nouvelId(), inscription: ins.id, apprenant: ins.apprenant, session: s.id, date: jour, matin: demi === 'matin', apresMidi: demi === 'apresMidi', motif: '' })
        return
      }
      const cleMotif = demi === 'matin' ? 'motifMatin' : 'motifApresMidi'
      if (p[demi]) {
        p[demi] = false
        p[cleMotif] = ''
      } else if (!p[cleMotif]) p[cleMotif] = 'Justifiée'
      else {
        p[cleMotif] = ''
        if (!p.matin && !p.apresMidi && !p.motifMatin && !p.motifApresMidi) d.presences = d.presences.filter((x) => x !== p)
        return
      }
      p.motif = p.motifMatin || p.motifApresMidi || ''
    }, null)
  }
  function noter(ins, type, valeur) {
    modifier((d) => {
      let e = d.evaluations.find((x) => x.inscription === ins.id && x.type === type)
      const score = valeur === '' ? null : Math.max(0, Math.min(20, Number(valeur)))
      if (!e) d.evaluations.push((e = { id: nouvelId(), inscription: ins.id, apprenant: ins.apprenant, session: s.id, type, max: 20 }))
      e.score = score
      e.resultat = type === 'Evaluation finale' ? resultatDe(score) : ''
      const i = d.inscriptions.find((x) => x.id === ins.id)
      i.pieces = { ...(i.pieces || {}), [type === 'Evaluation finale' ? 'evalChaud' : 'positionnement']: i.pieces?.[type === 'Evaluation finale' ? 'evalChaud' : 'positionnement'] || score != null }
    }, null)
  }
  function inscrire(e) {
    e.preventDefault()
    if (!nouvel.apprenant) return
    modifier((d) => d.inscriptions.push({ id: nouvelId(), session: s.id, apprenant: nouvel.apprenant, statut: 'Confirmé', financement: nouvel.financement, pieces: {} }), 'Stagiaire inscrit')
    setNouvel({ ...nouvel, apprenant: '' })
  }

  async function document(type, ins) {
    setEtat('Préparation du document…')
    const def = DOCS_STAGIAIRE[type]
    const blob = await genererDocx({ titre: def.titre, organisme: donnees.organisme, blocs: def.blocs(donnees, ins), essai })
    telechargerBlob(nomFichier(`${def.titre}-${nomDe(ins)}`), blob)
    const cle = { convocation: 'convocation', attestation: 'attestation', certificat: 'attestation' }[type]
    modifier((d) => {
      const i = d.inscriptions.find((x) => x.id === ins.id)
      i.pieces = { ...(i.pieces || {}), [cle]: true }
    }, `${def.titre} générée`)
    setEtat('')
  }
  async function feuille() {
    setEtat('Préparation de la feuille d’émargement…')
    const brute = donnees.sessions.find((x) => x.id === s.id)
    telechargerBlob(nomFichier(`Emargement-${s.formation}-${s.debut}`), await genererDocx({ titre: 'Feuille d’émargement', organisme: donnees.organisme, blocs: emargementSession(donnees, brute), essai }))
    setEtat('')
  }

  function exporterEmargement() {
    const l = [['Stagiaire', ...jours.flatMap((j) => [`${dateFr(j)} matin`, `${dateFr(j)} après-midi`])]]
    for (const i of inscrits) {
      l.push([nomDe(i), ...jours.flatMap((j) => {
        const p = db.presences.find((x) => x.inscription === i.id && x.date === j)
        return ['matin', 'apresMidi'].map((demi) => (p?.[demi] ? 'Présent' : p?.[demi === 'matin' ? 'motifMatin' : 'motifApresMidi'] ? 'Absence justifiée' : p ? 'Absent' : ''))
      })])
    }
    const c = (v) => `"${String(v).replace(/"/g, '""').replace(/^([=+\-@])/, "'$1")}"`
    telecharger(`emargement-${s.debut}.csv`, '﻿' + l.map((x) => x.map(c).join(';')).join('\r\n'))
  }

  const evals = (i, type) => db.evaluations.find((e) => (e.inscription ? e.inscription === i.id : e.apprenant === i.apprenant && e.session === s.id) && e.type === type)
  const dejaInscrits = new Set(inscrits.map((i) => i.apprenant))
  return (
    <section className="carte detail-session" aria-labelledby="ds-titre">
      <p className="ls-date">{dateFr(s.debut)}{s.fin !== s.debut && ` → ${dateFr(s.fin)}`} · {s.heures} h</p>
      <h2 id="ds-titre">{s.formation}</h2>
      <p className="ds-meta">{s.type} · {s.lieu || 'Lieu à préciser'} · {client?.nom || 'Client non renseigné'} · <strong>{s.statut}</strong></p>
      <div className="onglets-module petit" role="tablist">
        {[['dossiers', 'Dossiers'], ['emargement', 'Émargement'], ['evaluations', 'Évaluations'], ...(edition ? [['documents', 'Documents']] : [])].map(([id, l]) => (
          <button key={id} role="tab" aria-selected={onglet === id} className="onglet-module" onClick={() => setOnglet(id)}>{l}</button>
        ))}
      </div>
      {etat && <p className="note" role="status">{etat}</p>}

      {onglet === 'dossiers' && (
        <>
          <Jauge valeur={taux} libelle="Complétude des dossiers" />
          <div className="table-defile">
            <table className="matrice">
              <thead>
                <tr><th>Stagiaire</th>{PIECES.map(([k, l]) => <th key={k}><span className="vertical">{l}</span></th>)}</tr>
              </thead>
              <tbody>
                {inscrits.map((i) => (
                  <tr key={i.id}>
                    <th scope="row">{nomDe(i)}<small>{i.financement}</small></th>
                    {PIECES.map(([k, l]) => (
                      <td key={k}>
                        {edition ? (
                          <button className={'case-emarg ' + (i.pieces[k] ? 'ok' : 'vide')} onClick={() => piece(i, k)} aria-pressed={!!i.pieces[k]} aria-label={`${nomDe(i)} — ${l}`}>
                            {i.pieces[k] ? <Check size={16} aria-hidden="true" /> : '·'}
                          </button>
                        ) : (
                          <span aria-label={`${l} : ${i.pieces[k] ? 'fait' : 'manquant'}`}>{i.pieces[k] ? <Check className="ok" size={18} aria-hidden="true" /> : <Minus className="ko" size={18} aria-hidden="true" />}</span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {edition && (
            <form className="inscrire" onSubmit={inscrire}>
              <label className="champ-select">
                <span>Inscrire un stagiaire</span>
                <select value={nouvel.apprenant} onChange={(e) => setNouvel({ ...nouvel, apprenant: e.target.value })}>
                  <option value="">— choisir —</option>
                  {donnees.apprenants.filter((a) => !dejaInscrits.has(a.id)).map((a) => <option key={a.id} value={a.id}>{a.nom}</option>)}
                </select>
              </label>
              <label className="champ-select">
                <span>Financement</span>
                <select value={nouvel.financement} onChange={(e) => setNouvel({ ...nouvel, financement: e.target.value })}>
                  {FINANCEMENTS.map((f) => <option key={f}>{f}</option>)}
                </select>
              </label>
              <button className="bouton" disabled={!nouvel.apprenant}><UserPlus size={18} aria-hidden="true" /> Inscrire</button>
            </form>
          )}
        </>
      )}

      {onglet === 'emargement' && (
        <>
          <div className="ligne-actions">
            <p className="note">{edition ? 'Cliquez une case : présent → absent → absence justifiée → vide.' : 'Lecture seule : les signatures se font dans Airtable ou votre outil d’émargement.'}</p>
            <div className="actions">
              {edition && <button className="bouton secondaire" onClick={feuille}><FileText size={18} aria-hidden="true" /> Feuille à signer (Word)</button>}
              <button className="bouton secondaire" onClick={exporterEmargement}><Download size={18} aria-hidden="true" /> Exporter</button>
            </div>
          </div>
          <div className="table-defile">
            <table className="matrice">
              <thead>
                <tr>
                  <th>Stagiaire</th>
                  {jours.map((j) => <th key={j} colSpan={2}>{new Date(j).toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' })}</th>)}
                </tr>
                <tr className="sous-tete">
                  <th><span className="sr-only">Demi-journée</span></th>
                  {jours.flatMap((j) => [<th key={j + 'm'}>Matin</th>, <th key={j + 'a'}>Ap.-midi</th>])}
                </tr>
              </thead>
              <tbody>
                {inscrits.map((i) => (
                  <tr key={i.id}>
                    <th scope="row">{nomDe(i)}</th>
                    {jours.flatMap((j) =>
                      ['matin', 'apresMidi'].map((demi) => {
                        const p = db.presences.find((x) => x.inscription === i.id && x.date === j)
                        const ok = p?.[demi]
                        const justif = p?.[demi === 'matin' ? 'motifMatin' : 'motifApresMidi']
                        const etatCase = ok ? 'présent' : justif ? 'absence justifiée' : p ? 'absent' : 'non émargé'
                        return (
                          <td key={j + demi}>
                            <button className={'case-emarg ' + (ok ? 'ok' : justif ? 'justif' : p ? 'ko' : 'vide')} disabled={!edition} onClick={() => emarger(i, j, demi)}
                              aria-label={`${nomDe(i)}, ${dateFr(j)} ${demi === 'matin' ? 'matin' : 'après-midi'} : ${etatCase}`}>
                              {ok ? <Check size={16} aria-hidden="true" /> : justif ? 'J' : p ? <X size={16} aria-hidden="true" /> : '·'}
                            </button>
                          </td>
                        )
                      }),
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {onglet === 'evaluations' && (
        <ul className="progressions">
          {inscrits.map((i) => {
            const a = evals(i, 'Positionnement initial')
            const b = evals(i, 'Evaluation finale')
            return (
              <li key={i.id} className={edition ? 'editable' : ''}>
                <span className="pg-nom">{nomDe(i)}</span>
                {edition && (
                  <span className="notes">
                    <label>Entrée <input type="number" min="0" max="20" value={a?.score ?? ''} onChange={(e) => noter(i, 'Positionnement initial', e.target.value)} aria-label={`Positionnement de ${nomDe(i)} sur 20`} /></label>
                    <label>Fin <input type="number" min="0" max="20" value={b?.score ?? ''} onChange={(e) => noter(i, 'Evaluation finale', e.target.value)} aria-label={`Évaluation finale de ${nomDe(i)} sur 20`} /></label>
                  </span>
                )}
                {a?.score != null && b?.score != null ? (
                  <>
                    <div className="pg-piste" role="img" aria-label={`Positionnement ${a.score}/${a.max || 20}, final ${b.score}/${b.max || 20}`}>
                      <span className="pg-avant" style={{ width: (a.score / (a.max || 20)) * 100 + '%' }} />
                      <span className="pg-apres" style={{ width: (b.score / (b.max || 20)) * 100 + '%' }} />
                    </div>
                    <span className="pg-res">{a.score} → <strong>{b.score}</strong>/{b.max || 20} · {b.resultat}</span>
                  </>
                ) : (
                  !edition && <span className="note">Évaluations non saisies</span>
                )}
              </li>
            )
          })}
          {edition && <li className="note">Le résultat (acquis ≥ 14/20, en cours ≥ 10/20) est une aide : la décision reste celle du formateur.</li>}
        </ul>
      )}

      {onglet === 'documents' && (
        <div className="docs-session">
          <p className="note">Générés avec vos données : aucune ressaisie. Chaque document coche la pièce correspondante du dossier.</p>
          <div className="table-defile">
            <table>
              <thead><tr><th>Stagiaire</th><th>Convocation</th><th>Attestation de fin</th><th>Certificat de réalisation</th></tr></thead>
              <tbody>
                {inscrits.map((i) => (
                  <tr key={i.id}>
                    <th scope="row">{nomDe(i)}</th>
                    {['convocation', 'attestation', 'certificat'].map((t) => (
                      <td key={t}><button className="puce" onClick={() => document(t, donnees.inscriptions.find((x) => x.id === i.id))}><FileText size={14} aria-hidden="true" /> Word</button></td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button className="bouton secondaire" onClick={feuille}><FileText size={18} aria-hidden="true" /> Feuille d’émargement à signer</button>
        </div>
      )}
    </section>
  )
}

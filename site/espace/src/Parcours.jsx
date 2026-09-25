// Parcours : planning, dossiers stagiaires, émargements et évaluations (esprit « gestion de centre »).
import { useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, Download, Check, X, Minus } from 'lucide-react'
import { PIECES } from './donnees.js'
import { Jauge, dateFr, telecharger, useIndex } from './ui.jsx'

const JOURS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
const iso = (d) => d.toISOString().slice(0, 10)
function joursEntre(debut, fin) {
  const r = []
  for (let d = new Date(debut + 'T12:00:00'); iso(d) <= (fin || debut); d.setDate(d.getDate() + 1)) r.push(iso(d))
  return r
}

export default function Parcours({ db }) {
  const index = useIndex(db)
  const [vue, setVue] = useState('planning')
  const trie = useMemo(() => db.sessions.filter((s) => s.debut).sort((a, b) => b.debut.localeCompare(a.debut)), [db])
  const [choisie, setChoisie] = useState(() => trie.find((s) => s.statut === 'Terminée')?.id || trie[0]?.id)
  const [presences, setPresences] = useState(db.presences)
  const session = index.sessions[choisie]

  return (
    <div className="parcours">
      <div className="titre-module">
        <div>
          <h1>Parcours</h1>
          <p className="chapo">Planning, dossiers, émargements et évaluations — session par session.</p>
        </div>
        <div className="onglets-module" role="tablist">
          {[['planning', 'Planning'], ['sessions', 'Sessions']].map(([id, l]) => (
            <button key={id} role="tab" aria-selected={vue === id} className="onglet-module" onClick={() => setVue(id)}>{l}</button>
          ))}
        </div>
      </div>

      <div className="parcours-grille">
        <div className="carte">
          {vue === 'planning' ? (
            <Calendrier sessions={trie} choisie={choisie} onChoisir={setChoisie} />
          ) : (
            <ul className="liste-sessions">
              {trie.map((s) => {
                const ins = index.inscritsPar[s.id] || []
                return (
                  <li key={s.id}>
                    <button className={'ligne-session' + (s.id === choisie ? ' actif' : '')} aria-pressed={s.id === choisie} onClick={() => setChoisie(s.id)}>
                      <span className="ls-date">{dateFr(s.debut)}</span>
                      <strong>{s.formation}</strong>
                      <span>{s.type} · {ins.length} stagiaire(s) · {s.statut}</span>
                    </button>
                  </li>
                )
              })}
            </ul>
          )}
        </div>
        {session && <DetailSession key={session.id} db={db} s={session} inscrits={index.inscritsPar[session.id] || []} presences={presences} setPresences={setPresences} />}
      </div>
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

function DetailSession({ db, s, inscrits, presences, setPresences }) {
  const [onglet, setOnglet] = useState('dossiers')
  const demo = db.mode === 'demo'
  const jours = joursEntre(s.debut, s.fin)
  const nomDe = (i) => db.apprenants[i.apprenant]?.nom || '—'
  const client = db.clients[s.client]
  const pieces = inscrits.flatMap((i) => Object.values(i.pieces))
  const taux = pieces.length ? (pieces.filter(Boolean).length / pieces.length) * 100 : 0

  function basculer(ins, jour, demi) {
    if (!demo) return
    setPresences((ps) => {
      const p = ps.find((x) => x.inscription === ins.id && x.date === jour)
      if (!p) return [...ps, { id: 'n' + ps.length, inscription: ins.id, apprenant: ins.apprenant, session: s.id, date: jour, matin: demi === 'matin', apresMidi: demi === 'apresMidi', motif: '' }]
      return ps.map((x) => (x === p ? { ...x, [demi]: !x[demi] } : x))
    })
  }

  function exporterEmargement() {
    const l = [['Stagiaire', ...jours.flatMap((j) => [`${dateFr(j)} matin`, `${dateFr(j)} après-midi`])]]
    for (const i of inscrits) {
      l.push([nomDe(i), ...jours.flatMap((j) => {
        const p = presences.find((x) => x.inscription === i.id && x.date === j)
        return [p?.matin ? 'Présent' : p ? 'Absent' : '', p?.apresMidi ? 'Présent' : p ? 'Absent' : '']
      })])
    }
    const c = (v) => `"${String(v).replace(/"/g, '""').replace(/^([=+\-@])/, "'$1")}"`
    telecharger(`emargement-${s.debut}.csv`, '﻿' + l.map((x) => x.map(c).join(';')).join('\r\n'))
  }

  const evals = (i, type) => db.evaluations.find((e) => e.apprenant === i.apprenant && e.session === s.id && e.type === type)
  return (
    <section className="carte detail-session" aria-labelledby="ds-titre">
      <p className="ls-date">{dateFr(s.debut)}{s.fin !== s.debut && ` → ${dateFr(s.fin)}`} · {s.heures} h</p>
      <h2 id="ds-titre">{s.formation}</h2>
      <p className="ds-meta">{s.type} · {s.lieu} · {client?.nom || 'Client non renseigné'} · <strong>{s.statut}</strong></p>
      <div className="onglets-module petit" role="tablist">
        {[['dossiers', 'Dossiers'], ['emargement', 'Émargement'], ['evaluations', 'Évaluations']].map(([id, l]) => (
          <button key={id} role="tab" aria-selected={onglet === id} className="onglet-module" onClick={() => setOnglet(id)}>{l}</button>
        ))}
      </div>

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
                      <td key={k} aria-label={`${l} : ${i.pieces[k] ? 'fait' : 'manquant'}`}>
                        {i.pieces[k] ? <Check className="ok" size={18} aria-hidden="true" /> : <Minus className="ko" size={18} aria-hidden="true" />}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {onglet === 'emargement' && (
        <>
          <div className="ligne-actions">
            <p className="note">{demo ? 'Démo : cliquez une case pour simuler une signature.' : 'Lecture seule : les signatures se font dans Airtable ou votre outil d’émargement.'}</p>
            <button className="bouton secondaire" onClick={exporterEmargement}><Download size={18} aria-hidden="true" /> Exporter</button>
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
                        const p = presences.find((x) => x.inscription === i.id && x.date === j)
                        const ok = p?.[demi]
                        return (
                          <td key={j + demi}>
                            <button className={'case-emarg ' + (ok ? 'ok' : p ? 'ko' : 'vide')} disabled={!demo} onClick={() => basculer(i, j, demi)}
                              aria-label={`${nomDe(i)}, ${dateFr(j)} ${demi === 'matin' ? 'matin' : 'après-midi'} : ${ok ? 'présent' : p ? 'absent' : 'non émargé'}`}>
                              {ok ? <Check size={16} aria-hidden="true" /> : p ? <X size={16} aria-hidden="true" /> : '·'}
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
              <li key={i.id}>
                <span className="pg-nom">{nomDe(i)}</span>
                {a && b ? (
                  <>
                    <div className="pg-piste" role="img" aria-label={`Positionnement ${a.score}/${a.max}, final ${b.score}/${b.max}`}>
                      <span className="pg-avant" style={{ width: (a.score / a.max) * 100 + '%' }} />
                      <span className="pg-apres" style={{ width: (b.score / b.max) * 100 + '%' }} />
                    </div>
                    <span className="pg-res">{a.score} → <strong>{b.score}</strong>/{b.max} · {b.resultat}</span>
                  </>
                ) : (
                  <span className="note">Évaluations non saisies</span>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}

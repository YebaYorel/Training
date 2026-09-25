// Préparation du BPF : calcul automatique à partir des factures, sessions et émargements.
import { useMemo, useState } from 'react'
import { AlertTriangle, Download, Info } from 'lucide-react'
import { RUBRIQUES_C, bpfEnCsv, calculerBpf, rubriqueClient } from './bpf.js'
import { euros, telecharger } from './ui.jsx'

export default function Bpf({ db }) {
  const annees = useMemo(() => {
    const a = new Set([new Date().getFullYear(), new Date().getFullYear() - 1])
    for (const s of db.sessions) if (s.debut) a.add(Number(s.debut.slice(0, 4)))
    return [...a].sort((x, y) => y - x)
  }, [db])
  const [exercice, setExercice] = useState(annees[0])
  const [base, setBase] = useState('factures')
  const [charges, setCharges] = useState({ total: '', salairesFormateurs: '', achatsPrestations: '' })
  const [nsf, setNsf] = useState({})
  const [reclassement, setReclassement] = useState({})
  const b = useMemo(() => calculerBpf(db, exercice, { base, charges, nsf, reclassement }), [db, exercice, base, charges, nsf, reclassement])
  const aClasser = Object.entries(db.clients).filter(([, c]) => rubriqueClient(c.type) === 'a-classer')
  const jours = Math.ceil((b.echeance - new Date()) / 86400000)
  const nombre = (v) => v.replace(/[^\d,.]/g, '').replace(',', '.').slice(0, 12)

  return (
    <div className="bpf">
      <div className="titre-module">
        <div>
          <h1>Bilan Pédagogique et Financier</h1>
          <p className="chapo">
            Préparation de la déclaration (cerfa n° 10443) · à télédéclarer sur Mon Activité Formation avant le 31/05/{exercice + 1}
            {jours > 0 && ` · J-${jours}`}
          </p>
        </div>
        <div className="actions">
          <label className="champ-select">
            <span>Exercice</span>
            <select value={exercice} onChange={(e) => setExercice(Number(e.target.value))}>
              {annees.map((a) => <option key={a} value={a}>{a}</option>)}
            </select>
          </label>
          <button className="bouton" onClick={() => telecharger(`bpf-${exercice}-preparation.csv`, bpfEnCsv(b))}>
            <Download size={18} aria-hidden="true" /> Exporter (CSV)
          </button>
        </div>
      </div>

      <p className="avertissement">
        <Info size={18} aria-hidden="true" /> Outil de préparation : les rubriques suivent la structure du formulaire. Vérifiez chaque ligne avec la notice officielle (cerfa n° 50199) avant de télédéclarer.
      </p>

      {b.alertes.length > 0 && (
        <ul className="alertes carte">
          {b.alertes.map((a, k) => (
            <li key={k} className={'alerte niv-' + a.niveau}>
              {a.niveau === 'info' ? <Info size={20} aria-hidden="true" /> : <AlertTriangle size={20} aria-hidden="true" />}
              <div><strong>{a.texte}</strong></div>
            </li>
          ))}
        </ul>
      )}

      <div className="bpf-grille">
        <section className="carte cadre" aria-labelledby="c-c">
          <h2 id="c-c"><span className="lettre">C</span> Produits de l’exercice</h2>
          <div className="bascule" role="group" aria-label="Base de calcul">
            {[['factures', 'Factures émises'], ['encaissements', 'Encaissements']].map(([id, l]) => (
              <button key={id} aria-pressed={base === id} className="puce" onClick={() => setBase(id)}>{l}</button>
            ))}
          </div>
          <table className="cadre-table">
            <tbody>
              {RUBRIQUES_C.filter((r) => b.cadreC.produits[r.id] || r.id !== 'a-classer').map((r) => (
                <tr key={r.id} className={r.id === 'a-classer' ? 'a-classer' : b.cadreC.produits[r.id] ? '' : 'nul'}>
                  <th scope="row">{r.libelle}</th>
                  <td>{euros(b.cadreC.produits[r.id])}</td>
                </tr>
              ))}
              <tr className="total"><th scope="row">Total des produits</th><td>{euros(b.cadreC.total)}</td></tr>
            </tbody>
          </table>
          {aClasser.length > 0 && (
            <div className="reclasser">
              <h3>Clients à classer</h3>
              {aClasser.map(([id, c]) => (
                <label key={id} className="champ-select">
                  <span>{c.nom} <small>({c.type || 'type vide'})</small></span>
                  <select value={reclassement[id] || ''} onChange={(e) => setReclassement({ ...reclassement, [id]: e.target.value || undefined })}>
                    <option value="">— choisir —</option>
                    {RUBRIQUES_C.filter((r) => r.id !== 'a-classer').map((r) => <option key={r.id} value={r.id}>{r.libelle}</option>)}
                  </select>
                </label>
              ))}
            </div>
          )}
        </section>

        <section className="carte cadre" aria-labelledby="c-d">
          <h2 id="c-d"><span className="lettre">D</span> Charges de l’exercice</h2>
          <p className="note">Montants issus de votre comptabilité (livre des recettes / registre des achats).</p>
          {[
            ['total', 'Total des charges liées à l’activité de formation'],
            ['salairesFormateurs', 'dont salaires des formateurs'],
            ['achatsPrestations', 'dont achats de prestations de formation'],
          ].map(([k, l]) => (
            <label key={k} className="champ">
              <span>{l}</span>
              <input inputMode="decimal" value={charges[k]} onChange={(e) => setCharges({ ...charges, [k]: nombre(e.target.value) })} placeholder="0" />
            </label>
          ))}
          {b.cadreD.suggestionAchats > 0 && (
            <p className="note">Suggestion : {euros(b.cadreD.suggestionAchats)} de coûts de formateurs externes sur les sessions de l’exercice.</p>
          )}
        </section>

        <section className="carte cadre" aria-labelledby="c-e">
          <h2 id="c-e"><span className="lettre">E</span> Formateurs</h2>
          <table className="cadre-table">
            <thead><tr><th /><th>Nombre</th><th>Heures</th></tr></thead>
            <tbody>
              <tr><th scope="row">Personnes de l’organisme</th><td>{b.cadreE.internes.nombre}</td><td>{b.cadreE.internes.heures}</td></tr>
              <tr><th scope="row">Intervenants extérieurs</th><td>{b.cadreE.externes.nombre}</td><td>{b.cadreE.externes.heures}</td></tr>
            </tbody>
          </table>
        </section>

        <section className="carte cadre large" aria-labelledby="c-f">
          <h2 id="c-f"><span className="lettre">F</span> Stagiaires et heures-stagiaires</h2>
          <p className="note">Heures calculées depuis les émargements (demi-journée émargée = durée journalière ÷ 2).</p>
          <table className="cadre-table">
            <thead><tr><th>F-1 · Type de stagiaires</th><th>Stagiaires</th><th>Heures</th></tr></thead>
            <tbody>
              {b.cadreF.f1.map((l) => (
                <tr key={l.id} className={l.stagiaires ? '' : 'nul'}><th scope="row">{l.libelle}</th><td>{l.stagiaires}</td><td>{l.heures}</td></tr>
              ))}
              <tr className="total"><th scope="row">Total</th><td>{b.cadreF.totalStagiaires}</td><td>{b.cadreF.totalHeures}</td></tr>
            </tbody>
          </table>
          <table className="cadre-table">
            <thead><tr><th>F-3 · Objectif</th><th>Stagiaires</th><th>Heures</th></tr></thead>
            <tbody>
              {b.cadreF.f3.map((l) => <tr key={l.libelle}><th scope="row">{l.libelle}</th><td>{l.stagiaires}</td><td>{l.heures}</td></tr>)}
            </tbody>
          </table>
          <table className="cadre-table">
            <thead><tr><th>F-4 · Spécialité (formation)</th><th>Code NSF</th><th>Stagiaires</th><th>Heures</th></tr></thead>
            <tbody>
              {b.cadreF.f4.map((l) => (
                <tr key={l.formation}>
                  <th scope="row">{l.formation}</th>
                  <td>
                    <input className="nsf" aria-label={`Code NSF pour ${l.formation}`} value={nsf[l.formation] || ''} maxLength={4}
                      onChange={(e) => setNsf({ ...nsf, [l.formation]: e.target.value.replace(/[^\dA-Za-z]/g, '') })} placeholder="ex. 326" />
                  </td>
                  <td>{l.stagiaires}</td>
                  <td>{l.heures}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="carte cadre" aria-labelledby="c-g">
          <h2 id="c-g"><span className="lettre">G</span> Formations confiées à un autre organisme</h2>
          <table className="cadre-table">
            <tbody>
              <tr><th scope="row">Stagiaires</th><td>{b.cadreG.stagiaires}</td></tr>
              <tr><th scope="row">Heures-stagiaires</th><td>{b.cadreG.heures}</td></tr>
            </tbody>
          </table>
        </section>
      </div>
    </div>
  )
}

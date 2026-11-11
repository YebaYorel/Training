// BPF : l'assistant pose les questions et remplit les cadres C à G à partir des factures, sessions et émargements.
import { useEffect, useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { AlertTriangle, ArrowLeft, ArrowRight, CheckCircle2, Download, Info, Lock, Printer, Sparkles, Wand2 } from 'lucide-react'
import { RUBRIQUES_C, bpfEnCsv, calculerBpf, rubriqueClient } from './bpf.js'
import { euros, telecharger } from './ui.jsx'
import { libelleNsf, suggererNsf } from './nsf.js'
import { completudeOrganisme } from './Donnees.jsx'

const nombre = (v) => String(v).replace(/[^\d,.]/g, '').replace(',', '.').slice(0, 12)
const OPTIONS_VIDES = { base: 'factures', charges: { total: '', salairesFormateurs: '', achatsPrestations: '' }, nsf: {}, reclassement: {} }

/* ---------- Cadres (partagés entre l'assistant et la vue complète) ---------- */
function CadreC({ b, opt, maj, clients }) {
  const aClasser = Object.entries(clients).filter(([, c]) => rubriqueClient(c.type) === 'a-classer')
  return (
    <section className="carte cadre" aria-labelledby="c-c">
      <h2 id="c-c"><span className="lettre">C</span> Produits de l’exercice</h2>
      <div className="bascule" role="group" aria-label="Base de calcul">
        {[['factures', 'Factures émises'], ['encaissements', 'Encaissements']].map(([id, l]) => (
          <button key={id} aria-pressed={opt.base === id} className="puce" onClick={() => maj({ base: id })}>{l}</button>
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
              <select value={opt.reclassement[id] || ''} onChange={(e) => maj({ reclassement: { ...opt.reclassement, [id]: e.target.value || undefined } })}>
                <option value="">— choisir —</option>
                {RUBRIQUES_C.filter((r) => r.id !== 'a-classer').map((r) => <option key={r.id} value={r.id}>{r.libelle}</option>)}
              </select>
            </label>
          ))}
        </div>
      )}
    </section>
  )
}

function CadreD({ b, opt, maj }) {
  return (
    <section className="carte cadre" aria-labelledby="c-d">
      <h2 id="c-d"><span className="lettre">D</span> Charges de l’exercice</h2>
      <p className="note">Montants issus de votre comptabilité (livre des recettes / registre des achats).</p>
      {[['total', 'Total des charges liées à l’activité de formation'], ['salairesFormateurs', 'dont salaires des formateurs'], ['achatsPrestations', 'dont achats de prestations de formation']].map(([k, l]) => (
        <label key={k} className="champ">
          <span>{l}</span>
          <input inputMode="decimal" value={opt.charges[k] ?? ''} onChange={(e) => maj({ charges: { ...opt.charges, [k]: nombre(e.target.value) } })} placeholder="0" />
        </label>
      ))}
      {b.cadreD.suggestionAchats > 0 && (
        <p className="note">
          <Sparkles size={14} aria-hidden="true" /> Suggestion : {euros(b.cadreD.suggestionAchats)} de coûts de formateurs externes sur l’exercice.{' '}
          <button className="lien-discret" onClick={() => maj({ charges: { ...opt.charges, achatsPrestations: String(b.cadreD.suggestionAchats) } })}>Reprendre ce montant</button>
        </p>
      )}
    </section>
  )
}

function CadreE({ b }) {
  return (
    <section className="carte cadre" aria-labelledby="c-e">
      <h2 id="c-e"><span className="lettre">E</span> Formateurs</h2>
      <table className="cadre-table">
        <thead><tr><th /><th>Nombre</th><th>Heures</th></tr></thead>
        <tbody>
          <tr><th scope="row">Personnes de l’organisme</th><td>{b.cadreE.internes.nombre}</td><td>{b.cadreE.internes.heures}</td></tr>
          <tr><th scope="row">Intervenants extérieurs</th><td>{b.cadreE.externes.nombre}</td><td>{b.cadreE.externes.heures}</td></tr>
        </tbody>
      </table>
      <p className="note">Le dirigeant qui forme lui-même compte parmi les « personnes de l’organisme ».</p>
    </section>
  )
}

function CadreF({ b, opt, maj }) {
  const suggestions = b.cadreF.f4.map((l) => ({ ...l, sugg: suggererNsf(l.formation) }))
  const manquantes = suggestions.filter((l) => !opt.nsf[l.formation] && l.sugg)
  return (
    <section className="carte cadre large" aria-labelledby="c-f">
      <h2 id="c-f"><span className="lettre">F</span> Stagiaires et heures-stagiaires</h2>
      <p className="note">Heures calculées depuis les émargements (demi-journée émargée = durée journalière ÷ 2).</p>
      <table className="cadre-table">
        <thead><tr><th>F-1 · Type de stagiaires</th><th>Stagiaires</th><th>Heures</th></tr></thead>
        <tbody>
          {b.cadreF.f1.map((l) => <tr key={l.id} className={l.stagiaires ? '' : 'nul'}><th scope="row">{l.libelle}</th><td>{l.stagiaires}</td><td>{l.heures}</td></tr>)}
          <tr className="total"><th scope="row">Total</th><td>{b.cadreF.totalStagiaires}</td><td>{b.cadreF.totalHeures}</td></tr>
        </tbody>
      </table>
      <table className="cadre-table">
        <thead><tr><th>F-3 · Objectif</th><th>Stagiaires</th><th>Heures</th></tr></thead>
        <tbody>{b.cadreF.f3.map((l) => <tr key={l.libelle}><th scope="row">{l.libelle}</th><td>{l.stagiaires}</td><td>{l.heures}</td></tr>)}</tbody>
      </table>
      {manquantes.length > 0 && (
        <button className="puce" onClick={() => maj({ nsf: { ...opt.nsf, ...Object.fromEntries(manquantes.map((l) => [l.formation, l.sugg.code])) } })}>
          <Wand2 size={14} aria-hidden="true" /> Appliquer les {manquantes.length} code(s) NSF suggéré(s)
        </button>
      )}
      <table className="cadre-table">
        <thead><tr><th>F-4 · Spécialité (formation)</th><th>Code NSF</th><th>Stagiaires</th><th>Heures</th></tr></thead>
        <tbody>
          {suggestions.map((l) => (
            <tr key={l.formation}>
              <th scope="row">{l.formation}{opt.nsf[l.formation] && <small className="nsf-lib">{libelleNsf(opt.nsf[l.formation])}</small>}</th>
              <td>
                <input className="nsf" aria-label={`Code NSF pour ${l.formation}`} value={opt.nsf[l.formation] || ''} maxLength={4}
                  onChange={(e) => maj({ nsf: { ...opt.nsf, [l.formation]: e.target.value.replace(/[^\dA-Za-z]/g, '') } })} placeholder={l.sugg ? `suggéré ${l.sugg.code}` : 'ex. 326'} />
              </td>
              <td>{l.stagiaires}</td>
              <td>{l.heures}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}

function CadreG({ b }) {
  return (
    <section className="carte cadre" aria-labelledby="c-g">
      <h2 id="c-g"><span className="lettre">G</span> Formations confiées à un autre organisme</h2>
      <table className="cadre-table">
        <tbody>
          <tr><th scope="row">Stagiaires</th><td>{b.cadreG.stagiaires}</td></tr>
          <tr><th scope="row">Heures-stagiaires</th><td>{b.cadreG.heures}</td></tr>
        </tbody>
      </table>
    </section>
  )
}

function Alertes({ b }) {
  if (!b.alertes.length) return <p className="vide"><CheckCircle2 aria-hidden="true" /> Aucune incohérence détectée.</p>
  return (
    <ul className="alertes">
      {b.alertes.map((a, k) => (
        <li key={k} className={'alerte niv-' + a.niveau}>
          {a.niveau === 'info' ? <Info size={20} aria-hidden="true" /> : <AlertTriangle size={20} aria-hidden="true" />}
          <div><strong>{a.texte}</strong></div>
        </li>
      ))}
    </ul>
  )
}

/* ---------- Assistant pas à pas ---------- */
const ETAPES = ['Vérification', 'Produits (C)', 'Charges (D)', 'Formateurs (E)', 'Stagiaires (F)', 'Sous-traitance (G)', 'Récapitulatif']

function Assistant({ b, opt, maj, db, donnees, exercice, exporter, essai, aller, declarer }) {
  const [etape, setEtape] = useState(0)
  const org = donnees ? completudeOrganisme(donnees.organisme) : { taux: 100, manquants: [] }
  const bloquants = b.alertes.filter((a) => a.niveau === 'bloquant').length
  const questions = [
    <div key="0">
      <h2>Vos données sont-elles prêtes ?</h2>
      <p className="note">L’assistant a relu toute votre année {exercice}. Voici ce qu’il a trouvé :</p>
      {org.taux < 100 && <p className="alerte niv-alerte"><AlertTriangle size={20} aria-hidden="true" /><span>Fiche organisme incomplète : {org.manquants.join(', ')}. <button className="lien-discret" onClick={() => aller('donnees')}>Compléter</button></span></p>}
      <Alertes b={b} />
      <p className="note">{bloquants ? `${bloquants} point(s) bloquant(s) : corrigez-les (Parcours ou Mes données), l’assistant se met à jour tout seul.` : 'Vous pouvez continuer.'}</p>
    </div>,
    <div key="1"><h2>D’où vient votre chiffre d’affaires formation ?</h2><p className="note">Chaque facture est classée automatiquement selon le type de client. Choisissez la base, puis classez les clients inconnus.</p><CadreC b={b} opt={opt} maj={maj} clients={db.clients} /></div>,
    <div key="2"><h2>Quelles ont été vos charges ?</h2><p className="note">Trois montants, à reprendre de votre comptabilité. Micro-entreprise : total des dépenses liées à la formation.</p><CadreD b={b} opt={opt} maj={maj} /></div>,
    <div key="3"><h2>Qui a formé, et combien d’heures ?</h2><p className="note">Calculé depuis vos sessions réalisées et le statut de chaque formateur.</p><CadreE b={b} /><button className="lien-discret" onClick={() => aller('donnees')}>Corriger un statut de formateur</button></div>,
    <div key="4"><h2>Combien de stagiaires, pour quelles spécialités ?</h2><p className="note">L’assistant suggère les codes NSF à partir de l’intitulé : vérifiez-les.</p><CadreF b={b} opt={opt} maj={maj} /></div>,
    <div key="5"><h2>Avez-vous confié des formations à un autre organisme ?</h2><p className="note">Renseigné par le champ « Confiée à un autre organisme » de chaque session.</p><CadreG b={b} /></div>,
    <div key="6">
      <h2>Votre BPF {exercice} est prêt à recopier</h2>
      <p className="note">Ouvrez Mon Activité Formation, puis recopiez cadre par cadre. Gardez cet export avec vos pièces justificatives.</p>
      <div className="recap-grille">
        <div><span>Produits</span><strong>{euros(b.cadreC.total)}</strong></div>
        <div><span>Charges</span><strong>{euros(b.cadreD.total)}</strong></div>
        <div><span>Stagiaires</span><strong>{b.cadreF.totalStagiaires}</strong></div>
        <div><span>Heures-stagiaires</span><strong>{b.cadreF.totalHeures}</strong></div>
      </div>
      {essai ? (
        <p className="avertissement"><Lock size={18} aria-hidden="true" /> Export disponible avec la licence BPF Facile (l’essai permet de tout préparer).</p>
      ) : (
        <div className="ligne-actions">
          <button className="bouton" onClick={exporter}><Download size={18} aria-hidden="true" /> Exporter (CSV)</button>
          <button className="bouton secondaire" onClick={() => print()}><Printer size={18} aria-hidden="true" /> Fiche de recopie</button>
          {donnees && <button className="bouton secondaire" onClick={declarer}><CheckCircle2 size={18} aria-hidden="true" /> {opt.declareLe ? `Déclaré le ${new Date(opt.declareLe).toLocaleDateString('fr-FR')}` : 'J’ai télédéclaré'}</button>}
        </div>
      )}
    </div>,
  ]
  return (
    <div className="assistant">
      <ol className="etapes" aria-label="Étapes">
        {ETAPES.map((e, k) => (
          <li key={e} className={k === etape ? 'en-cours' : k < etape ? 'faite' : ''}>
            <button onClick={() => setEtape(k)} aria-current={k === etape ? 'step' : undefined}><span>{k + 1}</span> {e}</button>
          </li>
        ))}
      </ol>
      <AnimatePresence mode="wait">
        <motion.div key={etape} className="etape-corps" initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }} transition={{ duration: 0.25 }}>
          {questions[etape]}
        </motion.div>
      </AnimatePresence>
      <div className="ligne-actions">
        <button className="bouton secondaire" disabled={etape === 0} onClick={() => setEtape(etape - 1)}><ArrowLeft size={18} aria-hidden="true" /> Précédent</button>
        {etape < ETAPES.length - 1 && <button className="bouton" onClick={() => setEtape(etape + 1)}>Suivant <ArrowRight size={18} aria-hidden="true" /></button>}
      </div>
    </div>
  )
}

export default function Bpf({ db, donnees, modifier, essai, aller }) {
  const annees = useMemo(() => {
    const a = new Set([new Date().getFullYear(), new Date().getFullYear() - 1])
    for (const s of db.sessions) if (s.debut) a.add(Number(s.debut.slice(0, 4)))
    return [...a].sort((x, y) => y - x)
  }, [db])
  const [exercice, setExercice] = useState(annees[0])
  const [vue, setVue] = useState(donnees ? 'assistant' : 'complete')
  const [local, setLocal] = useState(OPTIONS_VIDES)
  // Les réponses sont gardées par exercice dans l'espace chiffré (ou en mémoire en mode interne)
  const enregistrees = donnees?.parametres?.bpf?.[exercice]
  const opt = { ...OPTIONS_VIDES, ...(donnees ? enregistrees : local) }
  opt.charges = { ...OPTIONS_VIDES.charges, ...opt.charges }
  const nsfFormations = useMemo(() => Object.fromEntries((donnees?.formations || []).filter((f) => f.nsf).map((f) => [f.intitule, f.nsf])), [donnees])
  const optCalc = { ...opt, nsf: { ...nsfFormations, ...opt.nsf } }
  const maj = (partiel) => {
    if (!modifier) return setLocal((l) => ({ ...l, ...partiel }))
    modifier((d) => {
      d.parametres.bpf ||= {}
      d.parametres.bpf[exercice] = { ...OPTIONS_VIDES, ...d.parametres.bpf[exercice], ...partiel }
      if (partiel.nsf) for (const f of d.formations) if (partiel.nsf[f.intitule]) f.nsf = partiel.nsf[f.intitule]
    }, null)
  }
  useEffect(() => setLocal(OPTIONS_VIDES), [exercice])
  const b = useMemo(() => calculerBpf(db, exercice, optCalc), [db, exercice, JSON.stringify(optCalc)]) // eslint-disable-line react-hooks/exhaustive-deps
  const jours = Math.ceil((b.echeance - new Date()) / 86400000)
  const exporter = () => telecharger(`bpf-${exercice}-preparation.csv`, bpfEnCsv(b))

  return (
    <div className="bpf">
      <div className="titre-module">
        <div>
          <h1>Bilan Pédagogique et Financier</h1>
          <p className="chapo">Préparation de la déclaration (cerfa n° 10443) · à télédéclarer sur Mon Activité Formation avant le 31/05/{exercice + 1}{jours > 0 && ` · J-${jours}`}</p>
        </div>
        <div className="actions">
          <label className="champ-select">
            <span>Exercice</span>
            <select value={exercice} onChange={(e) => setExercice(Number(e.target.value))}>
              {annees.map((a) => <option key={a} value={a}>{a}</option>)}
            </select>
          </label>
          <div className="onglets-module" role="tablist">
            {[['assistant', 'Assistant'], ['complete', 'Vue complète']].map(([id, l]) => (
              <button key={id} role="tab" aria-selected={vue === id} className="onglet-module" onClick={() => setVue(id)}>{l}</button>
            ))}
          </div>
          {vue === 'complete' && !essai && <button className="bouton" onClick={exporter}><Download size={18} aria-hidden="true" /> Exporter (CSV)</button>}
        </div>
      </div>

      <p className="avertissement">
        <Info size={18} aria-hidden="true" /> Outil de préparation : les rubriques suivent la structure du formulaire. Vérifiez chaque ligne avec la notice officielle (cerfa n° 50199) avant de télédéclarer.
      </p>

      {vue === 'assistant' ? (
        <Assistant b={b} opt={opt} maj={maj} db={db} donnees={donnees} exercice={exercice} exporter={exporter} essai={essai} aller={aller} declarer={() => maj({ declareLe: new Date().toISOString().slice(0, 10) })} />
      ) : (
        <>
          {b.alertes.length > 0 && <div className="carte"><Alertes b={b} /></div>}
          <div className="bpf-grille">
            <CadreC b={b} opt={opt} maj={maj} clients={db.clients} />
            <CadreD b={b} opt={opt} maj={maj} />
            <CadreE b={b} />
            <CadreF b={b} opt={opt} maj={maj} />
            <CadreG b={b} />
          </div>
        </>
      )}
    </div>
  )
}

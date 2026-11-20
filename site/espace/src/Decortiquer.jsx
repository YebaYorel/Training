// Ingénierie — « Décortiquer » : un dossier complet (REAC, fiche RNCP, référentiel, syllabus…) → plan de formation.
// Tout est lu dans le navigateur : aucun fichier ne quitte le poste (RGPD). Sans document, le sujet suffit.
import { useMemo, useRef, useState } from 'react'
import { AlertTriangle, Clipboard, FolderArchive, FolderOpen, Download, FileSearch, Wand2 } from 'lucide-react'
import { HEURES_PAR_JOUR, arborescenceZip, cleDate, construirePlan, extraire, fichiersDepuisDepot, formatH, lireTout, planMarkdown, typeDocument } from './decortiquer.js'
import { telechargerBlob } from './word.js'
import { telecharger } from './ui.jsx'

const taille = (o) => (o > 1048576 ? (o / 1048576).toFixed(1) + ' Mo' : Math.max(1, Math.round(o / 1024)) + ' Ko')

export default function Decortiquer() {
  const [docs, setDocs] = useState([])
  const [progres, setProgres] = useState(null)
  const [sujet, setSujet] = useState('')
  const [nomProgramme, setNomProgramme] = useState('')
  const [seqParAt, setSeqParAt] = useState(3)
  const [restreindre, setRestreindre] = useState(false)
  const [dureeTotale, setDureeTotale] = useState('')
  const [dates, setDates] = useState({})
  const [message, setMessage] = useState('')
  const [survol, setSurvol] = useState(false)
  const champDossier = useRef(null)
  const champFichiers = useRef(null)

  const extraction = useMemo(() => extraire(docs), [docs])
  const plan = useMemo(() => construirePlan(extraction, sujet, { seqParAt, restreindre, nomProgramme, dureeTotale: Number(dureeTotale) || 0 }), [extraction, sujet, seqParAt, restreindre, nomProgramme, dureeTotale])
  const lus = docs.filter((d) => d.texte)
  const ignores = docs.filter((d) => d.ignore)

  async function traiter(fichiers) {
    if (!fichiers.length) return
    setMessage('')
    setProgres({ faits: 0, total: fichiers.length })
    const resultat = await lireTout(fichiers, (faits, total) => setProgres({ faits, total }))
    setDocs((avant) => [...avant.filter((d) => !resultat.some((r) => r.chemin === d.chemin)), ...resultat])
    setProgres(null)
    const n = resultat.filter((r) => r.texte).length
    setMessage(`${n} document(s) lu(s) sur ${fichiers.length}.`)
  }

  const surDepot = async (e) => {
    e.preventDefault()
    setSurvol(false)
    traiter(await fichiersDepuisDepot(e.dataTransfer))
  }

  async function zip() {
    telechargerBlob(`${plan.programme} — arborescence.zip`.replace(/[\\/:*?"<>|]/g, '-'), await arborescenceZip(plan, dates))
  }
  async function copier() {
    try {
      await navigator.clipboard.writeText(planMarkdown(plan, dates))
      setMessage('Plan copié.')
    } catch {
      setMessage('Copie impossible : utilisez « Télécharger le plan ».')
    }
  }

  return (
    <div className="dec">
      <h1>Ingénierie de formation</h1>
      <p className="dec-intro">
        Déposez le <strong>dossier complet</strong> : REAC, référentiel d’évaluation (RE), référentiel de certification (RC), fiche RNCP, fiche RS, syllabus, programme…
        Vous pouvez <strong>mélanger</strong> plusieurs documents (ex. REAC + RE, RNCP + RC) : séances, progression, préparation des dossiers et de l’examen sont harmonisées.
        Plusieurs centaines de fichiers sont acceptés et tout est lu <strong>sur ce poste</strong> (rien n’est envoyé). Sans document, le sujet suffit.
      </p>

      <section className="carte" aria-labelledby="dec-sujet">
        <h2 id="dec-sujet">1 · Votre sujet</h2>
        <label htmlFor="dec-sujet-champ">Sujet ou intitulé de la formation (facultatif si un REAC est déposé)</label>
        <textarea id="dec-sujet-champ" rows={2} value={sujet} onChange={(e) => setSujet(e.target.value)} placeholder="Ex. : manager une équipe commerciale, Excel pour la gestion de stock, RGPD et IA Act en entreprise…" />
        <div className="dec-grille">
          <div>
            <label htmlFor="dec-prog">Nom du programme (facultatif)</label>
            <input id="dec-prog" value={nomProgramme} onChange={(e) => setNomProgramme(e.target.value)} placeholder="Ex. : TP MEM" />
          </div>
          <div>
            <label htmlFor="dec-duree">Durée totale connue (h)</label>
            <input id="dec-duree" type="number" min="0" step="0.5" inputMode="decimal" value={dureeTotale} onChange={(e) => setDureeTotale(e.target.value)} placeholder="Facultatif" />
          </div>
          <div>
            <label htmlFor="dec-seq">Séquences par activité type</label>
            <select id="dec-seq" value={seqParAt} onChange={(e) => setSeqParAt(Number(e.target.value))}>
              {[1, 2, 3, 4, 5].map((n) => <option key={n} value={n}>{n}</option>)}
            </select>
          </div>
        </div>
        <label className="dec-case">
          <input type="checkbox" checked={restreindre} onChange={(e) => setRestreindre(e.target.checked)} />
          Ne garder que ce qui concerne mon sujet (si le REAC en contient)
        </label>
      </section>

      <section className="carte" aria-labelledby="dec-fichiers">
        <h2 id="dec-fichiers">2 · Les documents</h2>
        <div
          className={'dec-depot' + (survol ? ' survol' : '')}
          onDragOver={(e) => (e.preventDefault(), setSurvol(true))}
          onDragLeave={() => setSurvol(false)}
          onDrop={surDepot}
        >
          <FileSearch size={34} aria-hidden="true" />
          <p>Glissez ici un dossier ou des fichiers</p>
          <p className="dec-formats">PDF · Word · Excel · PowerPoint · OpenDocument · HTML · texte</p>
          <div className="dec-boutons">
            <button className="bouton" onClick={() => champDossier.current.click()}><FolderOpen size={18} aria-hidden="true" /> Sélectionner un dossier</button>
            <button className="bouton secondaire" onClick={() => champFichiers.current.click()}>Sélectionner des fichiers</button>
          </div>
          <input ref={champDossier} type="file" hidden webkitdirectory="" directory="" multiple onChange={(e) => (traiter([...e.target.files]), (e.target.value = ''))} />
          <input ref={champFichiers} type="file" hidden multiple accept=".pdf,.docx,.docm,.odt,.ods,.odp,.pptx,.xlsx,.txt,.md,.csv,.html,.htm,.rtf,.json,.xml" onChange={(e) => (traiter([...e.target.files]), (e.target.value = ''))} />
        </div>
        <p role="status" aria-live="polite" className="dec-etat">
          {progres ? `Lecture… ${progres.faits} / ${progres.total}` : message}
        </p>
        {docs.length > 0 && (
          <details open={docs.length <= 12}>
            <summary>{lus.length} document(s) lu(s){ignores.length ? ` · ${ignores.length} ignoré(s)` : ''}</summary>
            <ul className="dec-liste">
              {docs.map((d) => (
                <li key={d.chemin} className={d.ignore ? 'ignore' : ''}>
                  <span>{d.chemin}</span>
                  <small>{d.ignore ? <><AlertTriangle size={13} aria-hidden="true" /> {d.ignore}</> : `${typeDocument(d.texte, d.nom)} · ${taille(d.taille)}`}</small>
                </li>
              ))}
            </ul>
            <button className="lien-discret" onClick={() => (setDocs([]), setMessage('Documents retirés.'))}>Tout retirer</button>
          </details>
        )}
      </section>

      <section className="carte" aria-labelledby="dec-plan">
        <h2 id="dec-plan">3 · Le plan de formation</h2>
        <p className="dec-origine">
          <Wand2 size={16} aria-hidden="true" /> {plan.origine}
          {plan.rncp && ` · RNCP${plan.rncp}`}
          {plan.rs && ` · RS${plan.rs}`}
          {plan.niveau && ` · niveau ${plan.niveau}`}
        </p>
        {plan.types.length > 1 && <p className="dec-croise">Documents croisés : {plan.types.join(' + ')}</p>}
        <div className="dec-kpis">
          <div className="kpi"><strong>{formatH(plan.heures.total)}</strong><span>durée {plan.heures.source.startsWith('Estimation') ? 'estimée' : 'répartie'}</span></div>
          <div className="kpi"><strong>{plan.heures.jours} j</strong><span>de {HEURES_PAR_JOUR} h (8h-12h, 13h-16h)</span></div>
          <div className="kpi"><strong>{plan.progression.length}</strong><span>séquences</span></div>
        </div>
        <p className="dec-note">{plan.heures.source}</p>
        <div className="dec-examen" role="note">
          <h3>Comment se passera l’examen</h3>
          <ul>{plan.examen.map((x) => <li key={x}>{x}</li>)}</ul>
        </div>
        {plan.origine.startsWith('Squelette') && (
          <p className="dec-alerte" role="note">
            <AlertTriangle size={16} aria-hidden="true" /> Squelette généré à partir du sujet seul, sans référentiel : il structure le travail mais doit être validé (contenus, volumes, évaluation).
          </p>
        )}
        <h3 className="dec-racine">{plan.programme}</h3>
        <ul className="dec-arbre">
          {plan.noeuds.map((n) => (
            <li key={n.nom}>
              <strong>{n.nom} <span className="dec-h">{formatH(n.heures)}</span></strong>
              {n.sequences && (
                <ul>
                  {n.sequences.map((s) => (
                    <li key={s.nom}>
                      <div className="dec-seq">
                        <span>{s.nom} <span className="dec-h">{formatH(s.heures)}</span></span>
                        <label>
                          <span className="dec-visuel-cache">Date de {s.nom}</span>
                          <input type="date" value={dates[cleDate(n, s)] || ''} onChange={(e) => setDates((d) => ({ ...d, [cleDate(n, s)]: e.target.value }))} />
                        </label>
                      </div>
                      <small>{s.competences.join(' · ')}</small>
                      {s.evaluations?.length > 0 && <small className="dec-eval">Évaluée par : {s.evaluations.join(', ')}</small>}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
        <details>
          <summary>Progression pédagogique ({plan.progression.length} séquences)</summary>
          <div className="dec-tableau">
            <table>
              <thead><tr><th scope="col">Bloc</th><th scope="col">Séquence</th><th scope="col">Durée</th><th scope="col">Jour(s)</th></tr></thead>
              <tbody>
                {plan.progression.map((p) => (
                  <tr key={p.bloc + p.sequence}><td>{p.bloc}</td><td>{p.sequence}</td><td>{formatH(p.heures)}</td><td>{p.jourDebut === p.jourFin ? `J${p.jourDebut}` : `J${p.jourDebut} à J${p.jourFin}`}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
        {plan.evaluation.length > 0 && (
          <details>
            <summary>Modalités d’évaluation repérées</summary>
            <ul>{plan.evaluation.map((e) => <li key={e}>{e}</li>)}</ul>
          </details>
        )}
        <div className="dec-boutons">
          <button className="bouton" onClick={zip}><FolderArchive size={18} aria-hidden="true" /> Arborescence ZIP (pour Drive)</button>
          <button className="bouton secondaire" onClick={copier}><Clipboard size={18} aria-hidden="true" /> Copier le plan</button>
          <button className="bouton secondaire" onClick={() => telecharger(`${plan.programme} — plan.md`, planMarkdown(plan, dates), 'text/markdown;charset=utf-8')}><Download size={18} aria-hidden="true" /> Télécharger le plan</button>
        </div>
        <p className="dec-note">
          Les dossiers portent un nom court et la date ; les supports (diaporama, ressource PDF, grille critériée, évaluation de 10 questions) se préparent ensuite dans chaque dossier.
          Pour un autre centre de formation, la marque YEBA n’apparaît pas.
        </p>
      </section>
    </div>
  )
}

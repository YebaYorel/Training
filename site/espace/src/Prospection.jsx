// Prospection & appels d'offres — module interne de l'Espace YEBA (poste d'Aurélien, `npm run espace`).
// L'outil VEILLE et PROPOSE ; Aurélien DÉCIDE (GO / NO-GO, validation des messages) et ENVOIE lui-même,
// depuis yebaformations@gmail.com uniquement. Les oppositions « STOP » bloquent tout nouvel envoi.
import { useEffect, useMemo, useRef, useState } from 'react'
import { AlertTriangle, Ban, CheckCircle2, ClipboardCopy, ExternalLink, Mail, RefreshCw, Send, ShieldCheck, Target, UserPlus } from 'lucide-react'
import {
  EXPEDITEUR, ETAT_VIDE, METIERS, STATUTS_AO, STATUTS_PROSPECT, aPurger, controlesEnvoi, detecterStop, enregistrerOpposition,
  estOppose, joursRestants, journaliser, lienGmail, normaliserAvis, proposition, redigerEmail, requeteBoamp, scoreAvis,
} from './prospection.js'

const SOURCES = ['Site web de l’entreprise', 'Annuaire professionnel (Pages Jaunes, CCI…)', 'Salon, réseau, événement', 'Recommandation', 'Carte de visite reçue', 'Autre (préciser dans les notes)']
const date = (d) => (d ? new Date(d).toLocaleDateString('fr-FR') : '—')
const couleurNiveau = { fort: 'vert', moyen: 'jaune', attention: 'rouge', faible: 'gris', info: 'gris' }

async function lireEtat() {
  const r = await fetch('/prospection/etat', { credentials: 'same-origin' })
  if (!r.ok) throw new Error('Serveur local indisponible : lancez « npm run espace ».')
  return (await r.json()) || structuredClone(ETAT_VIDE)
}
async function ecrireEtat(etat) {
  const r = await fetch('/prospection/etat', { method: 'PUT', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(etat) })
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).erreur || 'Enregistrement refusé')
}

function Regles() {
  return (
    <div className="carte regles-prospection" role="note" aria-label="Règles permanentes">
      <ShieldCheck size={22} aria-hidden="true" />
      <ol>
        <li><strong>Son métier, et STOP :</strong> chaque message parle du métier du destinataire et lui permet de répondre « STOP » (ou « STP ») ; sa demande bloque tout envoi suivant.</li>
        <li><strong>Expéditeur :</strong> {EXPEDITEUR} uniquement. Jamais l’adresse personnelle.</li>
        <li><strong>Vous décidez :</strong> l’outil veille et propose ; vous validez chaque message et chaque GO / NO-GO, puis vous envoyez vous-même.</li>
      </ol>
    </div>
  )
}

/* ───────────── Appels d'offres ───────────── */
function AppelsOffres({ etat, maj }) {
  const [zone, setZone] = useState('974')
  const [jours, setJours] = useState(120)
  const [avis, setAvis] = useState(null)
  const [erreur, setErreur] = useState('')
  const [charge, setCharge] = useState(false)
  const [copie, setCopie] = useState('')

  async function veille() {
    setCharge(true)
    setErreur('')
    try {
      const r = await fetch('/boamp/records?' + requeteBoamp({ departement: zone, jours }), { credentials: 'same-origin' })
      const j = await r.json()
      if (!r.ok) throw new Error(j.erreur || j.message || 'BOAMP indisponible')
      const liste = j.results.map((x) => ({ ...normaliserAvis(x), ...scoreAvis(x), brut: x }))
      liste.sort((a, b) => b.ouvert - a.ouvert || b.score - a.score)
      setAvis(liste)
      const connus = etat.ao || {}
      const nouveaux = liste.filter((a) => !connus[a.idweb])
      if (nouveaux.length) {
        maj((e) => {
          const ao = { ...(e.ao || {}) }
          for (const a of nouveaux) ao[a.idweb] = { statut: 'nouveau', vu: new Date().toISOString(), objet: a.objet, acheteur: a.acheteur, limite: a.limite }
          return journaliser({ ...e, ao, derniereVeille: new Date().toISOString() }, `Veille BOAMP : ${nouveaux.length} nouvel(s) avis`)
        })
      } else maj((e) => ({ ...e, derniereVeille: new Date().toISOString() }))
    } catch (e) {
      setErreur(e.message)
    } finally {
      setCharge(false)
    }
  }
  useEffect(() => { veille() }, [zone, jours]) // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    const t = setInterval(veille, 6 * 3600 * 1000) // veille automatique toutes les 6 h tant que l'Espace est ouvert
    return () => clearInterval(t)
  }, [zone, jours]) // eslint-disable-line react-hooks/exhaustive-deps

  function decider(a, statut) {
    const verbe = statut === 'go' ? 'GO (je réponds)' : 'NO-GO (je ne réponds pas)'
    if (!confirm(`Vous décidez ${verbe} pour :\n« ${a.objet} »\n${a.acheteur}\n\nCette décision est la vôtre et sera enregistrée.`)) return
    maj((e) => journaliser({ ...e, ao: { ...e.ao, [a.idweb]: { ...(e.ao?.[a.idweb] || {}), statut, decisionPar: 'Aurélien', decisionLe: new Date().toISOString() } } }, `Décision ${statut.toUpperCase()} : ${a.idweb}`))
  }
  function statut(a, s) {
    maj((e) => journaliser({ ...e, ao: { ...e.ao, [a.idweb]: { ...(e.ao?.[a.idweb] || {}), statut: s } } }, `Statut ${STATUTS_AO[s]} : ${a.idweb}`))
  }
  async function preparer(a) {
    const cmd = `/remporte:nouvel-ao ~/Téléchargements/DCE-${a.idweb}.zip`
    await navigator.clipboard?.writeText(cmd).catch(() => {})
    setCopie(a.idweb)
    statut(a, 'reponse')
  }

  return (
    <section aria-label="Appels d'offres">
      <div className="barre-outils ligne-actions-ao">
        <label className="champ-select">Zone
          <select value={zone} onChange={(e) => setZone(e.target.value)}>
            <option value="974">La Réunion (974) · toutes formations</option>
            <option value="">France entière · thèmes YEBA (IA, RGPD, management, vente…)</option>
          </select>
        </label>
        <label className="champ-select">Parutions des
          <select value={jours} onChange={(e) => setJours(Number(e.target.value))}>
            <option value={30}>30 derniers jours</option><option value={60}>60 derniers jours</option><option value={120}>120 derniers jours</option><option value={365}>12 derniers mois</option>
          </select>
        </label>
        <button className="bouton" onClick={veille} disabled={charge}><RefreshCw size={16} aria-hidden="true" /> {charge ? 'Veille en cours…' : 'Actualiser la veille'}</button>
      </div>
      <p className="note">Source : BOAMP (open data DILA), relu automatiquement à l’ouverture puis toutes les 6 h. Dernière veille : {etat.derniereVeille ? new Date(etat.derniereVeille).toLocaleString('fr-FR') : '—'}. Le BOAMP ne couvre pas les marchés sous les seuils publiés seulement sur le profil d’acheteur : gardez aussi vos alertes sur les plateformes des acheteurs réunionnais.</p>
      {erreur && <p className="erreur" role="alert"><AlertTriangle size={16} aria-hidden="true" /> {erreur}</p>}
      {avis && !avis.length && <p className="vide-etat">Aucun avis sur cette période.</p>}
      <ul className="liste-ao">
        {(avis || []).map((a) => {
          const suivi = etat.ao?.[a.idweb] || {}
          const p = proposition(a.brut)
          const j = joursRestants(a.brut)
          return (
            <li key={a.idweb} className={'carte ao' + (a.ouvert ? ' ouvert' : ' clos')}>
              <div className="ao-tete">
                <strong>{a.objet}</strong>
                <span className={'badge-statut ' + (a.ouvert ? (j <= 7 ? 'rouge' : 'vert') : 'gris')}>{a.ouvert ? `Ouvert · J-${j}` : a.nature || 'Clos'}</span>
                {suivi.statut && <span className="badge-statut gris">{STATUTS_AO[suivi.statut]}</span>}
              </div>
              <p className="ao-meta">{a.acheteur} · parution {date(a.parution)} · remise {a.limite ? new Date(a.limite).toLocaleString('fr-FR') : '—'} · {a.procedure || ''} · n° {a.idweb}</p>
              <p className={'ao-proposition badge-statut ' + couleurNiveau[p.niveau]}>Proposition automatique (score {a.score}{a.raisons.length ? ' : ' + a.raisons.join(', ') : ''}) — {p.texte}</p>
              {suivi.decisionPar && <p className="note">Décision : <strong>{STATUTS_AO[suivi.statut]}</strong> le {date(suivi.decisionLe)}.</p>}
              <div className="actions">
                <a className="bouton secondaire" href={a.url} target="_blank" rel="noopener noreferrer"><ExternalLink size={15} aria-hidden="true" /> Lire l’avis (BOAMP)</a>
                {a.ouvert && <button className="bouton" onClick={() => decider(a, 'go')}><CheckCircle2 size={15} aria-hidden="true" /> Je décide : GO</button>}
                {a.ouvert && <button className="bouton secondaire" onClick={() => decider(a, 'no_go')}><Ban size={15} aria-hidden="true" /> Je décide : NO-GO</button>}
                {suivi.statut === 'go' && <button className="bouton" onClick={() => preparer(a)}><ClipboardCopy size={15} aria-hidden="true" /> Préparer la réponse (Remporte)</button>}
                {['reponse', 'depose', 'gagne', 'perdu'].includes(suivi.statut) && (
                  <label className="champ-select">Suivi
                    <select value={suivi.statut} onChange={(e) => statut(a, e.target.value)}>
                      {['reponse', 'depose', 'gagne', 'perdu'].map((s) => <option key={s} value={s}>{STATUTS_AO[s]}</option>)}
                    </select>
                  </label>
                )}
              </div>
              {copie === a.idweb && (
                <p className="succes" role="status">Commande copiée. 1) Téléchargez le DCE sur la plateforme de l’acheteur et enregistrez-le sous <code>DCE-{a.idweb}.zip</code>. 2) Dans Claude Code, collez la commande : Remporte lit le DCE et s’arrête pour vous faire valider l’analyse, le go/no-go et le plan.</p>
              )}
            </li>
          )
        })}
      </ul>
    </section>
  )
}

/* ───────────── Prospects ───────────── */
const PROSPECT_VIDE = { entreprise: '', metier: '', metierPrecis: '', contactNom: '', email: '', commune: '', source: '', notes: '' }

function Prospects({ etat, maj }) {
  const [f, setF] = useState(PROSPECT_VIDE)
  const [ouvert, setOuvert] = useState(null)
  const [reponse, setReponse] = useState('')
  const [domaineEntier, setDomaineEntier] = useState(false)
  const [msg, setMsg] = useState('')
  const purge = useMemo(() => aPurger(etat), [etat])

  function ajouter(e) {
    e.preventDefault()
    if (estOppose(f.email, etat)) return setMsg('Cette adresse (ou son entreprise) a demandé STOP : ajout refusé.')
    const p = { ...f, id: crypto.randomUUID(), email: f.email.trim().toLowerCase(), statut: 'brouillon', cree: new Date().toISOString() }
    maj((x) => journaliser({ ...x, prospects: [p, ...x.prospects] }, `Prospect ajouté : ${p.entreprise}`))
    setF(PROSPECT_VIDE)
    setMsg('')
  }
  const changer = (id, fn, message) => maj((x) => journaliser({ ...x, prospects: x.prospects.map((p) => (p.id === id ? fn(p) : p)) }, message))

  function rediger(p) {
    try {
      const m = redigerEmail(p)
      changer(p.id, (x) => ({ ...x, message: m, statut: 'a_valider' }), `Brouillon rédigé : ${p.entreprise}`)
      setOuvert(p.id)
    } catch (e) {
      setMsg(e.message)
    }
  }
  const editer = (p, champ, v) => changer(p.id, (x) => ({ ...x, message: { ...x.message, [champ]: v }, statut: x.statut === 'envoye' ? x.statut : 'a_valider' }), null)
  function valider(p) {
    const erreurs = controlesEnvoi({ ...p, statut: 'valide' }, p.message, etat)
    if (erreurs.length) return setMsg(erreurs.join(' · '))
    if (!confirm(`Vous validez ce message pour ${p.entreprise} (${p.email}).\nIl partira de ${EXPEDITEUR}, quand VOUS cliquerez sur Envoyer dans Gmail.`)) return
    changer(p.id, (x) => ({ ...x, statut: 'valide', valideLe: new Date().toISOString() }), `Message validé par Aurélien : ${p.entreprise}`)
    setMsg('')
  }
  function stop(p) {
    maj((x) => journaliser(enregistrerOpposition(x, p.email, { toutLeDomaine: domaineEntier }), `STOP enregistré : ${p.email}${domaineEntier ? ' (+ domaine)' : ''}`))
    setReponse('')
  }

  return (
    <section aria-label="Prospects">
      <form className="carte" onSubmit={ajouter}>
        <h2><UserPlus size={18} aria-hidden="true" /> Nouveau prospect (professionnel)</h2>
        <div className="grille-champs">
          <label className="champ">Entreprise <abbr title="obligatoire">*</abbr><input required value={f.entreprise} onChange={(e) => setF({ ...f, entreprise: e.target.value })} /></label>
          <label className="champ">Métier du destinataire <abbr title="obligatoire">*</abbr>
            <select required value={f.metier} onChange={(e) => setF({ ...f, metier: e.target.value })}>
              <option value="">Choisir…</option>
              {Object.entries(METIERS).map(([k, m]) => <option key={k} value={k}>{m.libelle}</option>)}
            </select>
          </label>
          <label className="champ">Métier précis <small>(ex. « boulangerie », « hôtel 3 étoiles »)</small><input value={f.metierPrecis} onChange={(e) => setF({ ...f, metierPrecis: e.target.value })} /></label>
          <label className="champ">Nom du contact <small>(facultatif)</small><input value={f.contactNom} onChange={(e) => setF({ ...f, contactNom: e.target.value })} /></label>
          <label className="champ">E-mail professionnel <abbr title="obligatoire">*</abbr><input required type="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} /></label>
          <label className="champ">Commune<input value={f.commune} onChange={(e) => setF({ ...f, commune: e.target.value })} /></label>
          <label className="champ">Origine des coordonnées (RGPD) <abbr title="obligatoire">*</abbr>
            <select required value={f.source} onChange={(e) => setF({ ...f, source: e.target.value })}>
              <option value="">Choisir…</option>
              {SOURCES.map((s) => <option key={s}>{s}</option>)}
            </select>
          </label>
        </div>
        <button className="bouton" type="submit">Ajouter</button>
        <p className="note">Minimisation RGPD : uniquement des coordonnées <strong>professionnelles</strong> ; aucune donnée sensible. Conservation : 3 ans après le dernier contact.</p>
      </form>
      {msg && <p className="erreur" role="alert"><AlertTriangle size={16} aria-hidden="true" /> {msg}</p>}
      {purge.length > 0 && (
        <div className="alerte niv-alerte"><AlertTriangle size={18} aria-hidden="true" /><div><strong>{purge.length} prospect(s) sans contact depuis plus de 3 ans</strong><span>RGPD : à supprimer.</span></div>
          <button className="bouton secondaire" onClick={() => maj((x) => journaliser({ ...x, prospects: x.prospects.filter((p) => !purge.includes(p)) }, `Purge RGPD : ${purge.length} prospect(s)`))}>Supprimer</button>
        </div>
      )}
      <ul className="liste-ao">
        {etat.prospects.map((p) => {
          const erreurs = p.message ? controlesEnvoi(p, p.message, etat) : []
          return (
            <li key={p.id} className="carte ao">
              <div className="ao-tete">
                <strong>{p.entreprise}</strong>
                <span className={'badge-statut ' + (p.statut === 'stop' ? 'rouge' : p.statut === 'valide' ? 'vert' : p.statut === 'envoye' ? 'gris' : 'jaune')}>{STATUTS_PROSPECT[p.statut]}</span>
              </div>
              <p className="ao-meta">{METIERS[p.metier]?.libelle}{p.metierPrecis ? ' · ' + p.metierPrecis : ''} · {p.email} · {p.commune || '—'} · source : {p.source}</p>
              {p.statut !== 'stop' && (
                <div className="actions">
                  {!p.message && <button className="bouton" onClick={() => rediger(p)}><Mail size={15} aria-hidden="true" /> Proposer un message</button>}
                  {p.message && <button className="bouton secondaire" onClick={() => setOuvert(ouvert === p.id ? null : p.id)}>{ouvert === p.id ? 'Fermer' : 'Voir / modifier le message'}</button>}
                </div>
              )}
              {ouvert === p.id && p.message && p.statut !== 'stop' && (
                <div className="espace-onglet">
                  <p className="note">De : <strong>{EXPEDITEUR}</strong> (imposé) · À : {p.email}</p>
                  <label className="champ">Objet<input value={p.message.objet} onChange={(e) => editer(p, 'objet', e.target.value)} disabled={p.statut === 'envoye'} /></label>
                  <label className="champ">Message<textarea rows={16} value={p.message.corps} onChange={(e) => editer(p, 'corps', e.target.value)} disabled={p.statut === 'envoye'} /></label>
                  {erreurs.filter((x) => !x.startsWith('Règle 3')).length > 0 && (
                    <ul className="erreur">{erreurs.filter((x) => !x.startsWith('Règle 3')).map((x) => <li key={x}>{x}</li>)}</ul>
                  )}
                  <div className="actions">
                    {p.statut === 'a_valider' && <button className="bouton" onClick={() => valider(p)}><CheckCircle2 size={15} aria-hidden="true" /> Je valide ce message</button>}
                    {p.statut === 'valide' && (
                      <a className={'bouton' + (erreurs.length ? ' desactive' : '')} aria-disabled={erreurs.length > 0} href={erreurs.length ? undefined : lienGmail(p, p.message)} target="_blank" rel="noopener noreferrer">
                        <Send size={15} aria-hidden="true" /> Ouvrir dans Gmail ({EXPEDITEUR})
                      </a>
                    )}
                    {p.statut === 'valide' && <button className="bouton secondaire" onClick={() => changer(p.id, (x) => ({ ...x, statut: 'envoye', dernierContact: new Date().toISOString() }), `Envoyé par Aurélien : ${p.entreprise}`)}>J’ai envoyé</button>}
                  </div>
                </div>
              )}
              {['envoye', 'repondu'].includes(p.statut) && (
                <div className="espace-onglet">
                  <label className="champ">Coller sa réponse <small>(détection automatique de STOP / STP)</small><textarea rows={3} value={ouvert === 'rep-' + p.id ? reponse : ''} onFocus={() => setOuvert('rep-' + p.id)} onChange={(e) => setReponse(e.target.value)} /></label>
                  {ouvert === 'rep-' + p.id && detecterStop(reponse) && <p className="erreur" role="alert">Réponse « STOP » détectée : enregistrez l’opposition.</p>}
                  <div className="actions">
                    <label className="champ-case"><input type="checkbox" checked={domaineEntier} onChange={(e) => setDomaineEntier(e.target.checked)} /> Toute l’entreprise (même domaine)</label>
                    <button className="bouton" onClick={() => stop(p)}><Ban size={15} aria-hidden="true" /> Il a dit STOP</button>
                    <button className="bouton secondaire" onClick={() => changer(p.id, (x) => ({ ...x, statut: 'repondu', dernierContact: new Date().toISOString() }), `Réponse reçue : ${p.entreprise}`)}>Il a répondu (intéressé)</button>
                  </div>
                </div>
              )}
            </li>
          )
        })}
      </ul>
      {!etat.prospects.length && <p className="vide-etat">Aucun prospect pour l’instant.</p>}
    </section>
  )
}

function Oppositions({ etat }) {
  return (
    <section className="carte" aria-label="Oppositions STOP">
      <h2><Ban size={18} aria-hidden="true" /> Liste STOP ({etat.oppositions.length})</h2>
      <p className="note">Conservée pour respecter l’opposition (RGPD art. 21) : ces adresses ne peuvent plus être ajoutées ni contactées.</p>
      <table><thead><tr><th>Adresse</th><th>Domaine bloqué</th><th>Date</th><th>Motif</th></tr></thead>
        <tbody>{etat.oppositions.map((o) => <tr key={o.email}><td>{o.email}</td><td>{o.domaine || '—'}</td><td>{o.date}</td><td>{o.motif}</td></tr>)}</tbody>
      </table>
    </section>
  )
}

export default function Prospection() {
  const [etat, setEtat] = useState(null)
  const [vue, setVue] = useState('ao')
  const [erreur, setErreur] = useState('')
  const pret = useRef(false)
  useEffect(() => {
    lireEtat().then((e) => { setEtat({ ...structuredClone(ETAT_VIDE), ...e, expediteur: EXPEDITEUR }); pret.current = true }).catch((e) => setErreur(e.message))
  }, [])
  useEffect(() => {
    if (!pret.current || !etat) return
    const t = setTimeout(() => ecrireEtat(etat).catch((e) => setErreur(e.message)), 400)
    return () => clearTimeout(t)
  }, [etat])
  const maj = (fn) => setEtat((e) => fn(e))

  if (erreur && !etat) return <p className="erreur" role="alert">{erreur}</p>
  if (!etat) return <p className="note">Chargement…</p>
  const ouverts = Object.values(etat.ao || {}).filter((a) => a.limite && new Date(a.limite) > new Date() && !['no_go', 'perdu'].includes(a.statut)).length
  return (
    <div>
      <div className="titre-module">
        <div>
          <h1><Target size={24} aria-hidden="true" /> Prospection & appels d’offres</h1>
          <p className="chapo">Veille automatique des marchés publics, prospects B2B, oppositions STOP. L’outil propose, vous décidez.</p>
        </div>
        <div className="onglets-module" role="tablist">
          {[['ao', `Appels d’offres (${ouverts} ouverts suivis)`], ['prospects', `Prospects (${etat.prospects.length})`], ['stop', `STOP (${etat.oppositions.length})`], ['journal', 'Journal']].map(([id, l]) => (
            <button key={id} role="tab" aria-selected={vue === id} className="onglet-module" onClick={() => setVue(id)}>{l}</button>
          ))}
        </div>
      </div>
      <Regles />
      {erreur && <p className="erreur" role="alert">{erreur}</p>}
      {vue === 'ao' && <AppelsOffres etat={etat} maj={maj} />}
      {vue === 'prospects' && <Prospects etat={etat} maj={maj} />}
      {vue === 'stop' && <Oppositions etat={etat} />}
      {vue === 'journal' && (
        <ul className="carte journal">{(etat.journal || []).map((j, i) => <li key={i}><small>{new Date(j.date).toLocaleString('fr-FR')}</small> {j.message}</li>)}</ul>
      )}
    </div>
  )
}

// CARBURANT — l'IA qui fait rentrer l'argent des OPCO.
import { useEffect, useMemo, useState } from 'react'
import { animate, motion } from 'framer-motion'
import { AlertTriangle, Bot, Check, Clipboard, FileCheck2, Flame, Mail, ScanText, Sparkles, Wand2 } from 'lucide-react'
import { analyser, lireAccordLocal, relanceModele } from './carburant.js'
import { demanderIa } from './api.js'
import { DOCS_STAGIAIRE } from './documents-session.js'
import { genererDocx, nomFichier, telechargerBlob } from './word.js'
import { SCHEMAS } from './modele.js'

const euros = (n) => (n || 0).toLocaleString('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })
const OBJECTIF_GARANTIE = 10 * 49 * 12

function Compteur({ valeur }) {
  const [v, setV] = useState(0)
  useEffect(() => {
    const c = animate(0, valeur, { duration: 1.2, ease: [0.22, 1, 0.36, 1], onUpdate: (x) => setV(x) })
    return () => c.stop()
  }, [valeur])
  return <>{euros(Math.round(v))}</>
}

export default function Carburant({ donnees, modifier, ia, essai, aller }) {
  const { alertes, total } = useMemo(() => analyser(donnees), [donnees])
  const [texte, setTexte] = useState(null) // { titre, contenu, source, destinataire }
  const [accord, setAccord] = useState('')
  const [lecture, setLecture] = useState(null)
  const [cible, setCible] = useState('')
  const [attente, setAttente] = useState('')
  const [erreur, setErreur] = useState('')
  const securise = donnees.parametres.carburant?.securise || []
  const totalSecurise = securise.reduce((a, x) => a + x.montant, 0)

  // Une alerte qui disparaît = de l'argent sécurisé (mesure de la garantie « 10× »)
  useEffect(() => {
    const ouvertes = donnees.parametres.carburant?.ouvertes || {}
    const actuelles = Object.fromEntries(alertes.map((a) => [a.cle, a.montant]))
    const resolues = Object.entries(ouvertes).filter(([k]) => !(k in actuelles))
    const nouvelles = Object.keys(actuelles).some((k) => !(k in ouvertes))
    if (resolues.length || nouvelles) {
      modifier((d) => {
        d.parametres.carburant ||= { securise: [] }
        d.parametres.carburant.securise ||= []
        for (const [cle, montant] of resolues) if (montant > 0) d.parametres.carburant.securise.push({ cle, montant, date: new Date().toISOString().slice(0, 10) })
        d.parametres.carburant.ouvertes = actuelles
      }, null)
    }
  }, [alertes]) // eslint-disable-line react-hooks/exhaustive-deps

  async function viaIa(tache, contenu) {
    if (!ia.disponible) return null
    const r = await demanderIa({ tache, contenu, licence: ia.licence, poste: ia.poste })
    return r
  }

  async function relance(a) {
    const f = donnees.factures.find((x) => x.id === a.facture)
    const c = donnees.clients.find((x) => x.id === f.client) || {}
    setErreur('')
    setAttente(a.cle)
    try {
      const faits = `Organisme : ${donnees.organisme.nom}. Facture n° ${f.numero} du ${f.date}, montant restant dû ${a.montant} €. Destinataire : ${c.type === 'Particulier' ? 'un particulier' : c.nom} (${c.type || 'client'}). Retard : ${a.titre}. Signataire : ${donnees.organisme.dirigeant || ''}.`
      const r = await viaIa('relance', faits)
      setTexte({ titre: `Relance — facture ${f.numero}`, contenu: r?.texte || relanceModele(donnees, f), source: r ? 'IA Mistral — à relire avant envoi' : 'Modèle YEBA (IA non connectée)', destinataire: c.email })
    } catch (e) {
      setTexte({ titre: `Relance — facture ${f.numero}`, contenu: relanceModele(donnees, f), source: 'Modèle YEBA (IA indisponible : ' + e.message + ')', destinataire: c.email })
    } finally {
      setAttente('')
    }
  }

  async function certificat(a) {
    const ins = donnees.inscriptions.find((x) => x.id === a.inscription)
    const blob = await genererDocx({ titre: 'Certificat de réalisation', organisme: donnees.organisme, blocs: DOCS_STAGIAIRE.certificat.blocs(donnees, ins), essai })
    const nom = donnees.apprenants.find((x) => x.id === ins.apprenant)?.nom || 'stagiaire'
    telechargerBlob(nomFichier('Certificat-realisation-' + nom), blob)
    modifier((d) => {
      const i = d.inscriptions.find((x) => x.id === ins.id)
      i.pieces = { ...(i.pieces || {}), attestation: true }
    }, 'Certificat de réalisation émis')
  }

  function deposee(a) {
    modifier((d) => {
      d.inscriptions.find((x) => x.id === a.inscription).dateDepot = new Date().toISOString().slice(0, 10)
    }, 'Demande de prise en charge marquée comme déposée')
  }

  async function expliquer(a) {
    setAttente(a.cle)
    try {
      const r = await viaIa('expliquer', `${a.titre}. ${a.detail}`)
      setTexte({ titre: a.titre, contenu: r?.texte || a.detail, source: r ? 'IA Mistral' : 'Explication YEBA' })
    } catch (e) {
      setErreur(e.message)
    } finally {
      setAttente('')
    }
  }

  async function lireAccord() {
    setErreur('')
    setAttente('accord')
    try {
      // Pseudonymisation avant envoi : noms des stagiaires connus, emails et téléphones sont masqués
      let t = accord.slice(0, 5500)
      for (const a of donnees.apprenants) if (a.nom?.length > 2) t = t.split(new RegExp(a.nom.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')).join('[STAGIAIRE]')
      t = t.replace(/[\w.+-]+@[\w-]+\.[\w.]+/g, '[EMAIL]').replace(/(?:\+?\d[\s.]?){9,14}/g, (m) => (/\d{2}[\s.]?\d{2}/.test(m) ? '[TÉLÉPHONE]' : m))
      const r = await viaIa('accord', t)
      setLecture({ ...(r?.donnees || lireAccordLocal(accord)), source: r?.donnees ? 'IA Mistral' : 'Règles locales' })
    } catch {
      setLecture({ ...lireAccordLocal(accord), source: 'Règles locales (IA indisponible)' })
    } finally {
      setAttente('')
    }
  }
  function appliquer() {
    modifier((d) => {
      const i = d.inscriptions.find((x) => x.id === cible)
      if (lecture.numero_dossier) i.numeroDossier = lecture.numero_dossier
      if (lecture.montant_accorde_ht) i.montantAccord = lecture.montant_accorde_ht
      i.dateDepot ||= new Date().toISOString().slice(0, 10)
    }, 'Accord de prise en charge enregistré')
    setLecture(null)
    setAccord('')
  }

  return (
    <div className="carburant">
      <div className="titre-module">
        <div>
          <h1><Flame className="flamme" aria-hidden="true" /> CARBURANT</h1>
          <p className="chapo">Chaque heure réalisée doit devenir une facture payée. CARBURANT repère ce qui bloque, avant le financeur.</p>
        </div>
        <span className={'badge-ia ' + (ia.disponible ? 'on' : '')}>
          <Bot size={16} aria-hidden="true" /> {ia.disponible ? 'IA Mistral connectée (France)' : 'IA hors ligne : règles et modèles'}
        </span>
      </div>

      <div className="carburant-hero">
        <div className="jauge-argent">
          <span>Argent en jeu</span>
          <strong><Compteur valeur={total} /></strong>
          <small>{alertes.length} point(s) à traiter · estimation à partir de vos accords et prix</small>
        </div>
        <div className="jauge-argent secure">
          <span>Déjà sécurisé grâce à CARBURANT</span>
          <strong><Compteur valeur={totalSecurise} /></strong>
          <div className="piste-garantie" role="img" aria-label={`Garantie 10× : ${Math.round((totalSecurise / OBJECTIF_GARANTIE) * 100)} % de l’objectif annuel`}>
            <motion.span initial={{ width: 0 }} animate={{ width: Math.min(100, (totalSecurise / OBJECTIF_GARANTIE) * 100) + '%' }} transition={{ duration: 1 }} />
          </div>
          <small>Garantie « 10× » : objectif {euros(OBJECTIF_GARANTIE)} sur 12 mois</small>
        </div>
      </div>

      {erreur && <p className="erreur" role="alert">{erreur}</p>}

      <div className="colonnes-f">
        <section className="carte" aria-labelledby="c-alertes">
          <h2 id="c-alertes">À traiter, par ordre d’urgence</h2>
          {alertes.length === 0 ? (
            <p className="vide"><Check aria-hidden="true" /> Rien ne bloque vos paiements. Le plein est fait !</p>
          ) : (
            <ul className="alertes">
              {alertes.map((a) => (
                <li key={a.cle} className={'alerte niv-' + a.niveau}>
                  <AlertTriangle size={20} aria-hidden="true" />
                  <div>
                    <strong>{a.titre}{a.montant > 0 && <span className="montant"> · {euros(a.montant)}</span>}</strong>
                    <span>{a.detail}</span>
                    <div className="actions-alerte">
                      {a.type === 'relance' && <button className="puce" onClick={() => relance(a)} disabled={attente === a.cle}><Wand2 size={14} aria-hidden="true" /> {attente === a.cle ? 'Rédaction…' : 'Rédiger la relance'}</button>}
                      {a.type === 'certificat' && <button className="puce" onClick={() => certificat(a)}><FileCheck2 size={14} aria-hidden="true" /> Émettre le certificat</button>}
                      {a.type === 'depot' && <button className="puce" onClick={() => deposee(a)}><Check size={14} aria-hidden="true" /> C’est déposé</button>}
                      {['emargement', 'facture', 'ecart'].includes(a.type) && <button className="puce" onClick={() => aller(a.type === 'emargement' ? 'parcours' : 'donnees')}>Ouvrir</button>}
                      <button className="puce" onClick={() => expliquer(a)} disabled={attente === a.cle}><Sparkles size={14} aria-hidden="true" /> Pourquoi ?</button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        <div className="pile">
          {texte && (
            <section className="carte texte-ia" aria-labelledby="t-ia">
              <h2 id="t-ia">{texte.titre}</h2>
              <p className="note"><Bot size={14} aria-hidden="true" /> {texte.source}</p>
              <textarea rows={12} value={texte.contenu} onChange={(e) => setTexte({ ...texte, contenu: e.target.value })} aria-label="Texte proposé, modifiable" />
              <div className="ligne-actions">
                <button className="bouton secondaire" onClick={() => navigator.clipboard?.writeText(texte.contenu)}><Clipboard size={16} aria-hidden="true" /> Copier</button>
                {texte.destinataire && (
                  <a className="bouton" href={`mailto:${texte.destinataire}?subject=${encodeURIComponent(texte.contenu.split('\n')[0].replace(/^Objet\s*:\s*/i, ''))}&body=${encodeURIComponent(texte.contenu.split('\n').slice(1).join('\n').trim())}`}>
                    <Mail size={16} aria-hidden="true" /> Ouvrir dans ma messagerie
                  </a>
                )}
              </div>
            </section>
          )}
          <section className="carte" aria-labelledby="t-accord">
            <h2 id="t-accord"><ScanText size={20} aria-hidden="true" /> Lire un accord de prise en charge</h2>
            <p className="note">Collez le texte de l’accord reçu de l’OPCO : montant, n° de dossier et dates sont extraits et rattachés à l’inscription.</p>
            <textarea rows={5} value={accord} onChange={(e) => setAccord(e.target.value)} maxLength={6000} placeholder="Collez ici le texte de l’accord…" aria-label="Texte de l’accord" />
            <button className="bouton" onClick={lireAccord} disabled={accord.length < 20 || attente === 'accord'}>{attente === 'accord' ? 'Lecture…' : 'Lire l’accord'}</button>
            {lecture && (
              <div className="lecture">
                <p className="note">{lecture.source} — vérifiez chaque valeur.</p>
                <dl>
                  <dt>N° de dossier</dt><dd>{lecture.numero_dossier || '—'}</dd>
                  <dt>Montant accordé HT</dt><dd>{lecture.montant_accorde_ht != null ? euros(lecture.montant_accorde_ht) : '—'}</dd>
                  <dt>Dates</dt><dd>{lecture.date_debut || '—'} → {lecture.date_fin || '—'}</dd>
                  <dt>Heures</dt><dd>{lecture.heures ?? '—'}</dd>
                </dl>
                <label className="champ-select">
                  <span>Rattacher à l’inscription</span>
                  <select value={cible} onChange={(e) => setCible(e.target.value)}>
                    <option value="">— choisir —</option>
                    {donnees.inscriptions.map((i) => <option key={i.id} value={i.id}>{SCHEMAS.inscriptions.affichage(i, donnees)}</option>)}
                  </select>
                </label>
                <button className="bouton" disabled={!cible} onClick={appliquer}>Enregistrer sur l’inscription</button>
              </div>
            )}
          </section>
        </div>
      </div>
      <p className="note">Les textes produits par l’IA sont des brouillons à relire (IA Act, art. 50 : transparence). Seules des informations nécessaires sont envoyées au modèle Mistral (hébergé en France) ; aucun nom de stagiaire.</p>
    </div>
  )
}

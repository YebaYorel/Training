// Licences et achats : code poste, offres, paiement (Mollie via le serveur) ou commande par e-mail, saisie de licence.
import { useEffect, useState } from 'react'
import { BadgeCheck, Clipboard, CreditCard, KeyRound, Mail, Sparkles } from 'lucide-react'
import { OFFRES } from './licence.js'
import { commander, sante } from './api.js'
import { ecrire, lire } from './stockage.js'

export const EMAIL_YEBA = 'yebaformations@gmail.com'
const LIBELLES_MODULES = { coffre: 'Coffre Qualiopi', modeles: '20 modèles Word', donnees: 'Mes données', parcours: 'Parcours', bpf: 'Assistant BPF', carburant: 'CARBURANT (IA)' }
const PROMESSES = {
  qualiopi: 'Vos documents Qualiopi 2026 remplis à votre nom, en Word, et le suivi des 33 indicateurs.',
  bpf: 'Vos données de l’année au propre, et un BPF rempli par l’assistant en 20 minutes.',
  parcours: 'Planning, dossiers, émargements, évaluations et documents officiels. BPF inclus.',
  carburant: 'L’IA qui détecte ce qui bloque vos paiements OPCO et rédige vos relances.',
  studio: 'Tout YEBA Studio, pour un seul prix.',
}

export function lienCommandeEmail(offre, poste, organisme = {}) {
  const o = OFFRES[offre]
  const corps = `Bonjour,\n\nJe souhaite acheter : ${o.nom} (${o.libellePrix}).\n\nCode poste : ${poste}\nOrganisme : ${organisme.nom || ''}\nSIRET : ${organisme.siret || ''}\nUtilisateur (nom, prénom) :\nEmail :\n\nMerci de m’envoyer le lien de paiement puis ma licence.`
  return `mailto:${EMAIL_YEBA}?subject=${encodeURIComponent('Commande YEBA Studio — ' + o.nom)}&body=${encodeURIComponent(corps)}`
}

export default function Licences({ poste, licences, essai, ajouterLicence, organisme, offreVisee }) {
  const [code, setCode] = useState('')
  const [message, setMessage] = useState(null)
  const [serveur, setServeur] = useState(null)
  const [achat, setAchat] = useState(offreVisee || null)
  const [infos, setInfos] = useState({ nom: '', email: organisme?.email || '', organisme: organisme?.nom || '', siret: organisme?.siret || '' })
  const [attente, setAttente] = useState(false)

  useEffect(() => {
    sante().then((s) => setServeur(s.ok && s.paiement))
  }, [])

  async function coller(e) {
    e.preventDefault()
    const r = await ajouterLicence(code.trim())
    setMessage(r.ok ? { ok: true, texte: `Licence ${OFFRES[r.charge.off].nom} activée. Merci !` } : { ok: false, texte: r.raison })
    if (r.ok) setCode('')
  }

  async function payer(e) {
    e.preventDefault()
    setAttente(true)
    try {
      const r = await commander({ offre: achat, poste, ...infos, siret: infos.siret.replace(/\s/g, '') })
      const attentes = (await lire('paiements')) || []
      await ecrire('paiements', [...attentes, r.paiement])
      location.href = r.url
    } catch (err) {
      setMessage({ ok: false, texte: err.message })
      setAttente(false)
    }
  }

  const actives = licences.filter((l) => l.ok)
  return (
    <div className="licences">
      <div className="titre-module">
        <div>
          <h1>Licences et achats</h1>
          <p className="chapo">Une licence = un utilisateur, sur ce PC. Elle est liée au code poste ci-dessous.</p>
        </div>
      </div>

      <div className="colonnes-f">
        <section className="carte">
          <h2>Ce poste</h2>
          <p className="code-poste">
            <code>{poste}</code>
            <button className="bouton-icone" onClick={() => navigator.clipboard?.writeText(poste)} aria-label="Copier le code poste"><Clipboard size={16} /></button>
          </p>
          {essai && (
            <p className={'note ' + (essai.jours > 0 ? '' : 'erreur')}>
              {essai.jours > 0 ? `Essai gratuit : encore ${essai.jours} jour(s), tous les modules ouverts (documents marqués « ESSAI »).` : 'Période d’essai terminée.'}
            </p>
          )}
          <h3>Licences actives</h3>
          {actives.length ? (
            <ul className="liste-licences">
              {actives.map((l) => (
                <li key={l.code}>
                  <BadgeCheck className="ok" size={20} aria-hidden="true" />
                  <div>
                    <strong>{OFFRES[l.charge.off].nom}</strong>
                    <span>{l.charge.nom}{l.charge.org && ` · ${l.charge.org}`} — {l.charge.fin ? `jusqu’au ${new Date(l.charge.fin).toLocaleDateString('fr-FR')}` : 'sans limite de durée'}</span>
                    {l.enGrace && <span className="erreur">Échue : renouvelez sous {7} jours pour ne rien perdre.</span>}
                    {!l.enGrace && l.expireBientot && <span className="attention-texte">Échéance dans {l.jours} jour(s).</span>}
                  </div>
                  {l.charge.fin && <button className="lien-discret" onClick={() => setAchat(l.charge.off)}>Renouveler</button>}
                </li>
              ))}
            </ul>
          ) : (
            <p className="note">Aucune licence pour l’instant.</p>
          )}
          <form onSubmit={coller} className="coller-licence">
            <label className="champ" htmlFor="lic">
              <span><KeyRound size={16} aria-hidden="true" /> J’ai reçu une licence</span>
              <textarea id="lic" rows={3} value={code} onChange={(e) => setCode(e.target.value)} placeholder="YEBA1.…" maxLength={2000} />
            </label>
            <button className="bouton" disabled={!code.trim()}>Activer</button>
          </form>
          {message && <p className={message.ok ? 'succes' : 'erreur'} role="status">{message.texte}</p>}
        </section>

        <section className="offres-grille" aria-label="Offres">
          {Object.entries(OFFRES).map(([k, o]) => (
            <article key={k} className={'offre carte' + (achat === k ? ' choisie' : '') + (k === 'carburant' ? ' vedette' : '')}>
              {k === 'carburant' && <span className="ruban"><Sparkles size={14} aria-hidden="true" /> Pionniers 974 : 1er mois à 1 €</span>}
              <h3>{o.nom}</h3>
              <p className="prix">{o.libellePrix}</p>
              <p>{PROMESSES[k]}</p>
              <ul className="inclus">{o.modules.map((m) => <li key={m}>{LIBELLES_MODULES[m]}</li>)}</ul>
              {achat === k ? (
                serveur ? (
                  <form onSubmit={payer} className="form-achat">
                    {[['nom', 'Utilisateur (nom, prénom)'], ['email', 'Email'], ['organisme', 'Organisme'], ['siret', 'SIRET']].map(([c, l]) => (
                      <label key={c} className="champ" htmlFor={'a-' + c}>
                        <span>{l}</span>
                        <input id={'a-' + c} type={c === 'email' ? 'email' : 'text'} value={infos[c]} onChange={(e) => setInfos({ ...infos, [c]: e.target.value })} required maxLength={120} />
                      </label>
                    ))}
                    <p className="note">Paiement sécurisé par Mollie (Pays-Bas). Votre licence s’active automatiquement au retour.</p>
                    <button className="bouton large" disabled={attente}><CreditCard size={18} aria-hidden="true" /> {attente ? 'Redirection…' : `Payer ${o.libellePrix.split(' —')[0]}`}</button>
                  </form>
                ) : (
                  <a className="bouton large" href={lienCommandeEmail(k, poste, organisme)}><Mail size={18} aria-hidden="true" /> Commander (e-mail pré-rempli)</a>
                )
              ) : (
                <button className="bouton secondaire large" onClick={() => setAchat(k)}>Choisir</button>
              )}
            </article>
          ))}
        </section>
      </div>
      <p className="note">Prix nets de taxe (TVA non applicable, art. 293 B du CGI). Licences soumises aux conditions générales de vente de YEBA FORMATIONS.</p>
    </div>
  )
}

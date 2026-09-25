import { useEffect, useMemo, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowLeft, CalendarCheck, Phone, Send, X } from 'lucide-react'
import Avatar from './Avatar.jsx'
import { AGENDA_RAPPEL, CONSERVATION, IFA } from './config.js'
import { SUGGESTIONS_ACCUEIL, creneaux, libelleJour, repondre } from './connaissances.js'
import { ENTREPRISE } from '../data.js'

const EASE = [0.22, 1, 0.36, 1]
// Raccourcis des boutons de suggestion vers une question comprise par IFA
const RACCOURCIS = {
  'Voir les formations': 'catalogue des formations',
  'Les tarifs': 'tarifs',
  'Le financement': 'financement',
  'Être rappelé': 'être rappelé',
  'Faire le diagnostic': 'diagnostic',
  'Et le CPF ?': 'cpf',
}
let compteur = 0
const nouvelId = () => ++compteur

function allerA(cible) {
  const el = document.querySelector(cible)
  if (!el) return
  if (window.__lenis) window.__lenis.scrollTo(el, { offset: -100 })
  else el.scrollIntoView()
}

export default function Panneau({ onFermer }) {
  const [messages, setMessages] = useState([])
  const [ecrit, setEcrit] = useState(false)
  const [saisie, setSaisie] = useState('')
  const fil = useRef(null)
  const champ = useRef(null)

  function repondreAvecDelai(rep, delai = 700) {
    setEcrit(true)
    setTimeout(() => {
      setEcrit(false)
      setMessages((m) => [...m, { id: nouvelId(), de: 'ifa', ...rep }])
    }, delai)
  }

  useEffect(() => {
    repondreAvecDelai({
      texte: [
        'Bonjour, je suis IFA, l’assistante virtuelle de YEBA FORMATIONS.',
        'Je réponds à vos questions sur nos formations, nos tarifs et les financements, et je peux organiser un rappel avec Aurélien.',
      ],
      suggestions: SUGGESTIONS_ACCUEIL,
    }, 600)
    champ.current?.focus()
    const touche = (e) => e.key === 'Escape' && onFermer()
    document.addEventListener('keydown', touche)
    return () => document.removeEventListener('keydown', touche)
  }, [])

  // Toujours afficher le dernier message
  useEffect(() => {
    fil.current?.scrollTo({ top: fil.current.scrollHeight, behavior: 'smooth' })
  }, [messages, ecrit])

  function poser(question) {
    const q = question.trim()
    if (!q) return
    setSaisie('')
    setMessages((m) => [...m, { id: nouvelId(), de: 'moi', texte: [q] }])
    const rep = repondre(RACCOURCIS[q] ?? q)
    const longueur = rep.texte.join(' ').length
    repondreAvecDelai(rep, Math.min(450 + longueur * 4, 1500))
  }

  return (
    <motion.aside
      id="ifa-panneau"
      className="ifa-panneau"
      role="dialog"
      aria-labelledby="ifa-titre"
      initial={{ x: '-110%', opacity: 0.6 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: '-110%', opacity: 0.6 }}
      transition={{ type: 'spring', stiffness: 260, damping: 30 }}
    >
      <header className="ifa-tete">
        <Avatar taille={54} parle={ecrit} />
        <div>
          <h2 id="ifa-titre">IFA</h2>
          <p>{IFA.role} · réponses programmées, pas une personne</p>
        </div>
        <button className="ifa-fermer" onClick={onFermer} aria-label="Fermer IFA">
          <X size={24} />
        </button>
      </header>

      <div className="ifa-fil" ref={fil} data-lenis-prevent aria-live="polite">
        {messages.map((m) => (
          <Message key={m.id} m={m} onPoser={poser} onFermer={onFermer} ajouter={(rep) => setMessages((x) => [...x, { id: nouvelId(), de: 'ifa', ...rep }])} />
        ))}
        <AnimatePresence>
          {ecrit && (
            <motion.div className="ifa-msg ifa-de-ifa ifa-ecrit" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <span className="sr-only">IFA écrit…</span>
              {[0, 1, 2].map((i) => (
                <motion.i key={i} animate={{ y: [0, -5, 0] }} transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.15 }} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <form
        className="ifa-saisie"
        onSubmit={(e) => {
          e.preventDefault()
          poser(saisie)
        }}
      >
        <label htmlFor="ifa-question" className="sr-only">
          Votre question
        </label>
        <input
          id="ifa-question"
          ref={champ}
          value={saisie}
          onChange={(e) => setSaisie(e.target.value)}
          placeholder="Posez votre question…"
          autoComplete="off"
          maxLength={300}
        />
        <button type="submit" aria-label="Envoyer" disabled={!saisie.trim()}>
          <Send size={20} />
        </button>
      </form>
      <p className="ifa-mention">IFA ne conserve pas vos messages. <a href="confidentialite.html">Confidentialité</a></p>
    </motion.aside>
  )
}

function Message({ m, onPoser, onFermer, ajouter }) {
  return (
    <motion.div
      className={'ifa-msg ' + (m.de === 'ifa' ? 'ifa-de-ifa' : 'ifa-de-moi')}
      initial={{ opacity: 0, y: 12, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.35, ease: EASE }}
    >
      {m.texte.map((t, k) => (
        <p key={k}>{t}</p>
      ))}
      {m.action === 'rdv' && <Agenda ajouter={ajouter} />}
      {m.action === 'diagnostic' && (
        <button
          className="ifa-lien"
          onClick={() => {
            onFermer()
            setTimeout(() => allerA('#diagnostic'), 300)
          }}
        >
          Ouvrir le diagnostic
        </button>
      )}
      {m.lien && (
        <button
          className="ifa-lien"
          onClick={() => {
            onFermer()
            setTimeout(() => allerA(m.lien), 300)
          }}
        >
          Voir le catalogue
        </button>
      )}
      {m.suggestions && (
        <div className="ifa-suggestions">
          {m.suggestions.map((s) => (
            <button key={s} onClick={() => onPoser(s)}>
              {s}
            </button>
          ))}
        </div>
      )}
    </motion.div>
  )
}

/* ---------- Prise de rendez-vous de rappel ---------- */
const SUJETS = ['Une formation', 'Une solution d’IA pour mon entreprise', 'Un audit RGPD / IA Act', 'Autre chose']
const telephoneValide = (t) => /^(?:\+262|\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4}$/.test(t.trim())

function Agenda({ ajouter }) {
  const jours = useMemo(() => creneaux(AGENDA_RAPPEL), [])
  const [jour, setJour] = useState(null)
  const [heure, setHeure] = useState(null)
  const [etat, setEtat] = useState('choix') // choix | formulaire | envoi | envoye | courriel
  const [champs, setChamps] = useState({ nom: '', tel: '', entreprise: '', email: '', sujet: SUJETS[0], accord: false })
  const [erreur, setErreur] = useState('')
  const maj = (k) => (e) => setChamps((c) => ({ ...c, [k]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }))

  const resume = jour && heure ? `${libelleJour(jour, true)} à ${heure.replace(':', 'h')} (heure de La Réunion)` : ''
  const corpsMail = encodeURIComponent(
    `Bonjour,\n\nJe souhaite être rappelé(e) le ${resume}.\n\nNom : ${champs.nom}\nTéléphone : ${champs.tel}\nEntreprise : ${champs.entreprise}\nSujet : ${champs.sujet}\n`,
  )

  async function envoyer(e) {
    e.preventDefault()
    if (!champs.nom.trim()) return setErreur('Indiquez votre nom pour que nous sachions qui rappeler.')
    if (!telephoneValide(champs.tel)) return setErreur('Ce numéro semble incomplet : 10 chiffres, par exemple 0692 12 34 56.')
    if (!champs.accord) return setErreur('Cochez la case d’accord : sans elle, nous ne pouvons pas utiliser votre numéro.')
    setErreur('')
    if (!IFA.endpointRappel) return setEtat('courriel')
    setEtat('envoi')
    try {
      const rep = await fetch(IFA.endpointRappel, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: jour,
          heure,
          fuseau: AGENDA_RAPPEL.fuseau,
          nom: champs.nom.trim(),
          telephone: champs.tel.trim(),
          entreprise: champs.entreprise.trim(),
          email: champs.email.trim(),
          sujet: champs.sujet,
          consentement: true,
          consentement_le: new Date().toISOString(),
          source: 'IFA — site internet',
        }),
      })
      if (!rep.ok) throw new Error(String(rep.status))
      setEtat('envoye')
      ajouter({ texte: [`C’est noté ! Aurélien vous rappelle le ${resume}.`, 'Bonne journée, et à très vite !'] })
    } catch {
      setEtat('courriel')
    }
  }

  if (etat === 'envoye')
    return (
      <p className="ifa-ok">
        <CalendarCheck size={18} aria-hidden="true" /> Demande enregistrée : {resume}.
      </p>
    )

  if (etat === 'courriel')
    return (
      <div className="ifa-agenda">
        <p>Dernière étape : envoyez la demande depuis votre messagerie, elle est déjà rédigée.</p>
        <a className="ifa-action" href={`mailto:${ENTREPRISE.email}?subject=${encodeURIComponent('Demande de rappel — ' + resume)}&body=${corpsMail}`}>
          Envoyer ma demande par e-mail
        </a>
        <p className="ifa-petit">
          Ou appelez directement : <strong>{ENTREPRISE.telAffiche}</strong>
        </p>
      </div>
    )

  if (etat === 'formulaire' || etat === 'envoi')
    return (
      <form className="ifa-agenda" onSubmit={envoyer} noValidate>
        <button type="button" className="ifa-retour" onClick={() => setEtat('choix')}>
          <ArrowLeft size={16} aria-hidden="true" /> {resume}
        </button>
        <label htmlFor="ifa-nom">Nom et prénom *</label>
        <input id="ifa-nom" value={champs.nom} onChange={maj('nom')} autoComplete="name" required />
        <label htmlFor="ifa-tel">Téléphone *</label>
        <input id="ifa-tel" value={champs.tel} onChange={maj('tel')} autoComplete="tel" inputMode="tel" placeholder="0692 12 34 56" required />
        <label htmlFor="ifa-entreprise">Entreprise</label>
        <input id="ifa-entreprise" value={champs.entreprise} onChange={maj('entreprise')} autoComplete="organization" />
        <label htmlFor="ifa-sujet">C’est au sujet de…</label>
        <select id="ifa-sujet" value={champs.sujet} onChange={maj('sujet')}>
          {SUJETS.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
        <label className="ifa-accord" htmlFor="ifa-accord">
          <input id="ifa-accord" type="checkbox" checked={champs.accord} onChange={maj('accord')} />
          <span>
            J’accepte que YEBA FORMATIONS utilise ces informations pour me rappeler. Conservation : {CONSERVATION}. Je peux
            demander leur suppression à tout moment. *
          </span>
        </label>
        {erreur && (
          <p className="ifa-erreur" role="alert">
            {erreur}
          </p>
        )}
        <button type="submit" className="ifa-action" disabled={etat === 'envoi'}>
          <Phone size={18} aria-hidden="true" /> {etat === 'envoi' ? 'Envoi…' : 'Être rappelé'}
        </button>
      </form>
    )

  return (
    <div className="ifa-agenda">
      <p className="ifa-petit">Choisissez un jour :</p>
      <div className="ifa-jours" data-lenis-prevent>
        {jours.map((j) => (
          <button key={j.date} aria-pressed={jour === j.date} onClick={() => (setJour(j.date), setHeure(null))}>
            {libelleJour(j.date)}
          </button>
        ))}
      </div>
      <AnimatePresence>
        {jour && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} style={{ overflow: 'hidden' }}>
            <p className="ifa-petit">Puis une heure (heure de La Réunion) :</p>
            <div className="ifa-heures">
              {jours
                .find((j) => j.date === jour)
                .heures.map((h) => (
                  <button key={h} aria-pressed={heure === h} onClick={() => setHeure(h)}>
                    {h.replace(':', 'h')}
                  </button>
                ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <button className="ifa-action" disabled={!jour || !heure} onClick={() => setEtat('formulaire')}>
        Continuer
      </button>
    </div>
  )
}

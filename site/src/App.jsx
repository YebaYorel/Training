import { useEffect, useRef, useState } from 'react'
import {
  AnimatePresence,
  LayoutGroup,
  MotionConfig,
  motion,
  useReducedMotion,
  useScroll,
  useSpring,
  useTransform,
} from 'framer-motion'
import {
  Accessibility,
  ArrowDown,
  ArrowRight,
  BadgeCheck,
  Bot,
  Building2,
  CalendarClock,
  Check,
  Clock,
  Cpu,
  Database,
  Globe,
  GraduationCap,
  HeartHandshake,
  LayoutDashboard,
  Mail,
  MapPin,
  Menu,
  Phone,
  ShieldCheck,
  Timer,
  Users,
  Workflow,
  X,
} from 'lucide-react'
import { CERTIFS, ENTREPRISE, FILTRES, FORMATIONS } from './data.js'
import { CarteInclinee, Compteur, Pitons, ReseauPitons, Reveal, TitreAnime } from './anim.jsx'

const EASE = [0.22, 1, 0.36, 1]
const SECTIONS = [
  { id: 'metiers', label: 'Métiers' },
  { id: 'formations', label: 'Formations' },
  { id: 'implementation', label: 'Solutions IA' },
  { id: 'gouvernance', label: 'RGPD & IA Act' },
  { id: 'apropos', label: 'Qui suis-je' },
  { id: 'contact', label: 'Contact' },
]

/* ---------- Préférences d'accessibilité (propres au visiteur, sans cookie) ---------- */
function lirePref(cle, defaut) {
  try {
    return localStorage.getItem('yeba-' + cle) ?? defaut
  } catch {
    return defaut
  }
}
function ecrirePref(cle, val) {
  try {
    localStorage.setItem('yeba-' + cle, val)
  } catch {
    /* navigation privée : sans importance */
  }
}

export default function App() {
  const [taille, setTaille] = useState(() => lirePref('taille', '1'))
  const [contraste, setContraste] = useState(() => lirePref('contraste', '0'))
  const [calme, setCalme] = useState(() => lirePref('calme', '0'))

  useEffect(() => {
    const h = document.documentElement
    h.dataset.taille = taille
    h.dataset.contraste = contraste
    h.dataset.calme = calme
    ecrirePref('taille', taille)
    ecrirePref('contraste', contraste)
    ecrirePref('calme', calme)
  }, [taille, contraste, calme])

  return (
    <MotionConfig reducedMotion={calme === '1' ? 'always' : 'user'}>
      <a className="lien-evitement" href="#contenu">
        Aller au contenu
      </a>
      <Progression />
      <Nav />
      <main id="contenu">
        <Hero calmeForce={calme === '1'} />
        <Bandeau />
        <Metiers />
        <Chiffres />
        <Catalogue />
        <Implementation />
        <Methode />
        <Gouvernance />
        <APropos />
        <Pratique />
        <Contact />
      </main>
      <Pied />
      <PanneauAcces
        taille={taille}
        setTaille={setTaille}
        contraste={contraste}
        setContraste={setContraste}
        calme={calme}
        setCalme={setCalme}
      />
    </MotionConfig>
  )
}

/* ---------- Barre de progression de lecture ---------- */
function Progression() {
  const { scrollYProgress } = useScroll()
  const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 25 })
  return <motion.div className="progression" style={{ scaleX }} aria-hidden="true" />
}

/* ---------- Navigation ---------- */
function Nav() {
  const [ouvert, setOuvert] = useState(false)
  const [actif, setActif] = useState('')
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entrees) => entrees.forEach((e) => e.isIntersecting && setActif(e.target.id)),
      { rootMargin: '-45% 0px -50% 0px' },
    )
    SECTIONS.forEach((s) => {
      const el = document.getElementById(s.id)
      if (el) obs.observe(el)
    })
    return () => obs.disconnect()
  }, [])
  return (
    <motion.nav
      className="nav"
      aria-label="Navigation principale"
      initial={{ y: -100, x: '-50%', opacity: 0 }}
      animate={{ y: 0, x: '-50%', opacity: 1 }}
      transition={{ duration: 0.9, delay: 0.2, ease: EASE }}
    >
      <a className="nav-logo" href="#" aria-label="YEBA FORMATIONS — retour en haut">
        <img src="media/logo-yeba.png" alt="YEBA FORMATIONS" width="54" height="46" style={{ width: 'auto' }} />
      </a>
      <ul className={'nav-liens' + (ouvert ? ' ouvert' : '')} id="menu">
        {SECTIONS.map((s) => (
          <li key={s.id}>
            <a href={'#' + s.id} aria-current={actif === s.id} onClick={() => setOuvert(false)}>
              {s.label}
            </a>
          </li>
        ))}
      </ul>
      <a className="btn btn-bleu btn-petit" href="#contact">
        Parlons-en <ArrowRight size={18} aria-hidden="true" />
      </a>
      <button
        className="nav-burger"
        aria-expanded={ouvert}
        aria-controls="menu"
        aria-label={ouvert ? 'Fermer le menu' : 'Ouvrir le menu'}
        onClick={() => setOuvert((o) => !o)}
      >
        {ouvert ? <X size={26} /> : <Menu size={26} />}
      </button>
    </motion.nav>
  )
}

/* ---------- Hero ---------- */
const ROTATION = ['former', 'équiper', 'sécuriser']

function Hero({ calmeForce }) {
  const ref = useRef(null)
  const video = useRef(null)
  const systemeCalme = useReducedMotion()
  const calme = calmeForce || systemeCalme
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] })
  const echelle = useTransform(scrollYProgress, [0, 1], [1, 1.25])
  const yTexte = useTransform(scrollYProgress, [0, 1], ['0%', '35%'])
  const opacite = useTransform(scrollYProgress, [0, 0.8], [1, 0])
  const [i, setI] = useState(0)

  useEffect(() => {
    if (calme) return
    const t = setInterval(() => setI((n) => (n + 1) % ROTATION.length), 2600)
    return () => clearInterval(t)
  }, [calme])

  useEffect(() => {
    const v = video.current
    if (!v) return
    if (calme) v.pause()
    else v.play().catch(() => {})
  }, [calme])

  const titre = ["L'IA", 'au', 'service', 'de', 'vos', 'équipes.', 'Sous', 'contrôle', 'humain.']
  return (
    <section className="hero" ref={ref} aria-labelledby="titre-hero">
      <motion.video
        ref={video}
        className="hero-video"
        style={calme ? undefined : { scale: echelle }}
        poster="media/hero-poster.jpg"
        autoPlay={!calme}
        muted
        loop
        playsInline
        preload="metadata"
        aria-hidden="true"
      >
        <source src="media/hero-ia.mp4" type="video/mp4" />
        <source src="media/hero-ia.webm" type="video/webm" />
      </motion.video>
      <div className="hero-voile" />
      <ReseauPitons className="hero-reseau" />
      <motion.div className="conteneur hero-contenu" style={calme ? undefined : { y: yTexte, opacity: opacite }}>
        <motion.p
          className="surtitre"
          style={{ color: 'var(--or)' }}
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          Formation · IA · Gouvernance — La Réunion
        </motion.p>
        <h1 id="titre-hero" aria-label="L'IA au service de vos équipes. Sous contrôle humain.">
          {titre.map((m, k) => (
            <span key={k} aria-hidden="true" style={{ display: 'inline-block', overflow: 'hidden', verticalAlign: 'top' }}>
              <motion.span
                className={'mot' + (k >= 6 ? ' accent' : '')}
                initial={{ y: '110%', rotate: 4 }}
                animate={{ y: '0%', rotate: 0 }}
                transition={{ duration: 1, delay: 0.5 + k * 0.08, ease: EASE }}
              >
                {m}
              </motion.span>
            </span>
          ))}
        </h1>
        <motion.div
          className="hero-rotateur"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4, duration: 0.8 }}
        >
          <span className="fixe">Nous venons</span>
          <span className="fenetre" aria-live="off">
            <AnimatePresence mode="popLayout" initial={false}>
              <motion.span
                key={ROTATION[i]}
                initial={{ y: '100%', opacity: 0 }}
                animate={{ y: '0%', opacity: 1 }}
                exit={{ y: '-100%', opacity: 0 }}
                transition={{ duration: 0.5, ease: EASE }}
              >
                {ROTATION[i]}
              </motion.span>
            </AnimatePresence>
          </span>
          <span className="fixe">votre entreprise.</span>
        </motion.div>
        <motion.p
          className="accroche"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.6, duration: 0.8 }}
        >
          Formation, mise en place de solutions d’IA et gouvernance RGPD &amp; IA Act pour les TPE-PME de La Réunion.
          Des outils qui font gagner du temps. Des preuves que tout est maîtrisé.
        </motion.p>
        <motion.div
          className="hero-actions"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.8, duration: 0.8 }}
        >
          <a className="btn btn-or" href="#formations">
            Voir les formations <ArrowRight size={20} aria-hidden="true" />
          </a>
          <a className="btn btn-contour" href="#contact">
            Parler de mon projet
          </a>
        </motion.div>
      </motion.div>
      <motion.a
        className="hero-defiler"
        href="#metiers"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.4 }}
      >
        Découvrir
        <motion.span animate={calme ? {} : { y: [0, 8, 0] }} transition={{ duration: 1.6, repeat: Infinity }}>
          <ArrowDown size={22} aria-hidden="true" />
        </motion.span>
      </motion.a>
      <p className="mention-ia">Vidéo d’ambiance générée par IA</p>
    </section>
  )
}

/* ---------- Bandeau défilant des gages de confiance ---------- */
function Bandeau() {
  const calme = useReducedMotion()
  const items = CERTIFS.map((c) => (
    <span className="bandeau-item" key={c}>
      <BadgeCheck size={24} aria-hidden="true" /> {c}
    </span>
  ))
  return (
    <div className="bandeau" role="region" aria-label="Certifications et attestations">
      {calme ? (
        <div className="conteneur" style={{ display: 'flex', flexWrap: 'wrap', gap: '14px 40px' }}>
          {items}
        </div>
      ) : (
        <motion.div
          className="bandeau-piste"
          animate={{ x: ['0%', '-50%'] }}
          transition={{ duration: 38, ease: 'linear', repeat: Infinity }}
        >
          {items}
          <span aria-hidden="true" style={{ display: 'contents' }}>
            {CERTIFS.map((c) => (
              <span className="bandeau-item" key={'b' + c}>
                <BadgeCheck size={24} /> {c}
              </span>
            ))}
          </span>
        </motion.div>
      )}
    </div>
  )
}

/* ---------- Trois métiers ---------- */
const METIERS = [
  {
    icone: GraduationCap,
    titre: 'Former',
    texte: 'Des formations concrètes, qui partent de vos vrais dossiers. Vos équipes repartent avec des outils prêts à servir.',
    puces: ['Intra dans vos locaux', 'Inter en salle de séminaire', 'IA, vente, management'],
  },
  {
    icone: Workflow,
    titre: 'Implémenter',
    texte: 'Workflows automatisés, assistants IA, sites internet, bases de données : on construit avec vous, pour vous.',
    puces: ['Temps gagné mesuré', 'Outils européens privilégiés', 'Vous restez autonome'],
  },
  {
    icone: ShieldCheck,
    titre: 'Sécuriser',
    texte: 'Conseil et audit de gouvernance RGPD et IA Act. Nous vous aidons à prouver les mesures prises.',
    puces: ['Registre des traitements', 'Charte d’usage de l’IA', 'Dossier de preuve'],
  },
]

function Metiers() {
  return (
    <section id="metiers" className="bloc clair" aria-labelledby="titre-metiers">
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Trois métiers, un seul interlocuteur</p>
        </Reveal>
        <TitreAnime id="titre-metiers" texte="De la formation à la mise en place, sans perdre le contrôle." />
        <div className="metiers">
          {METIERS.map((m, k) => (
            <Reveal key={m.titre} delay={k * 0.15}>
              <CarteInclinee className="carte-metier">
                <span className="num" aria-hidden="true">
                  0{k + 1}
                </span>
                <motion.div
                  className="icone-ronde"
                  initial={{ rotate: -20, scale: 0.6 }}
                  whileInView={{ rotate: 0, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ type: 'spring', stiffness: 180, damping: 12, delay: 0.2 + k * 0.15 }}
                >
                  <m.icone size={36} aria-hidden="true" />
                </motion.div>
                <h3>{m.titre}</h3>
                <p>{m.texte}</p>
                <ul className="puces">
                  {m.puces.map((p) => (
                    <li key={p}>
                      <Check size={20} aria-hidden="true" /> {p}
                    </li>
                  ))}
                </ul>
              </CarteInclinee>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ---------- Chiffres clés ---------- */
function Chiffres() {
  return (
    <section className="sombre" aria-labelledby="titre-chiffres">
      <Pitons couleur="var(--bleu-nuit)" fond="var(--creme)" />
      <div className="conteneur" style={{ paddingBottom: 'clamp(70px, 9vw, 120px)', paddingTop: 30 }}>
        <Reveal>
          <p className="surtitre">Ce qui change avec nous</p>
        </Reveal>
        <TitreAnime id="titre-chiffres" texte="Une journée de formation qui en donne plus." />
        <div className="chiffres">
          <Reveal className="chiffre" delay={0}>
            <Compteur vers={8} suffixe=" h" />
            <span>de formation par journée, là où beaucoup en comptent 7.</span>
          </Reveal>
          <Reveal className="chiffre" delay={0.1}>
            <Compteur vers={15} />
            <span>jours ouvrés minimum entre l’inscription et le démarrage.</span>
          </Reveal>
          <Reveal className="chiffre" delay={0.2}>
            <Compteur vers={10} />
            <span>stagiaires au plus par groupe : chacun sur son poste.</span>
          </Reveal>
          <Reveal className="chiffre" delay={0.3}>
            <Compteur vers={FORMATIONS.length} />
            <span>formations au catalogue, de l’initiation au séminaire dirigeants.</span>
          </Reveal>
        </div>
      </div>
      <Pitons couleur="var(--creme)" fond="var(--bleu-nuit)" />
    </section>
  )
}

/* ---------- Catalogue ---------- */
function Catalogue() {
  const [filtre, setFiltre] = useState('tout')
  const [ouverte, setOuverte] = useState(null)
  const liste = FORMATIONS.filter((f) => filtre === 'tout' || f.cat === filtre)
  return (
    <section id="formations" className="bloc clair" aria-labelledby="titre-formations" style={{ paddingTop: 40 }}>
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Le garage à compétences</p>
        </Reveal>
        <TitreAnime id="titre-formations" texte="Votre entreprise est un moteur. On la règle." />
        <Reveal>
          <p className="intro">
            Allumage, turbo, pilote automatique… Chaque formation porte le nom de la pièce qu’elle améliore. Cliquez sur une
            carte pour voir ce que vos équipes sauront faire en repartant.
          </p>
        </Reveal>
        <LayoutGroup>
          <div className="filtres" role="group" aria-label="Filtrer les formations">
            {FILTRES.map((f) => (
              <button key={f.id} className="filtre" aria-pressed={filtre === f.id} onClick={() => setFiltre(f.id)}>
                {filtre === f.id && (
                  <motion.span layoutId="pastille" className="pastille" transition={{ type: 'spring', stiffness: 400, damping: 32 }} />
                )}
                <span>{f.label}</span>
              </button>
            ))}
          </div>
          <motion.ul className="grille-formations" layout style={{ listStyle: 'none' }} aria-live="polite">
            <AnimatePresence mode="popLayout">
              {liste.map((f) => (
                <motion.li
                  key={f.ref}
                  layout
                  initial={{ opacity: 0, scale: 0.9, y: 30 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.45, ease: EASE }}
                  style={{ display: 'flex' }}
                >
                  <CarteFormation f={f} onOuvrir={() => setOuverte(f)} />
                </motion.li>
              ))}
            </AnimatePresence>
          </motion.ul>
        </LayoutGroup>
        <Reveal>
          <p className="note" style={{ marginTop: 36 }}>
            Tarifs sur devis, en inter comme en intra. Organisme certifié Qualiopi : votre OPCO peut examiner une demande de
            prise en charge, selon ses propres critères.
          </p>
        </Reveal>
      </div>
      <AnimatePresence>{ouverte && <FicheFormation f={ouverte} onFermer={() => setOuverte(null)} />}</AnimatePresence>
    </section>
  )
}

function CarteFormation({ f, onOuvrir }) {
  return (
    <motion.button
      className="formation"
      onClick={onOuvrir}
      whileHover={{ y: -8 }}
      transition={{ type: 'spring', stiffness: 300, damping: 22 }}
      aria-haspopup="dialog"
      aria-label={`${f.nom} — ${f.sousTitre}. Voir le détail`}
    >
      <motion.div className="formation-tete" layoutId={'tete-' + f.ref}>
        {f.badge && <span className="badge">{f.badge}</span>}
        <h3>{f.nom}</h3>
        <p>{f.sousTitre}</p>
      </motion.div>
      <div className="formation-corps">
        <div className="meta">
          <span>
            <CalendarClock size={16} aria-hidden="true" /> {f.jours} j · {f.heures} h
          </span>
          <span>
            <Users size={16} aria-hidden="true" /> {f.effectif}
          </span>
        </div>
        <ul className="cles">
          {f.cles.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
        <div className="formation-pied">
          Voir le programme
          <span className="fleche">
            <ArrowRight size={22} aria-hidden="true" />
          </span>
        </div>
      </div>
    </motion.button>
  )
}

function FicheFormation({ f, onFermer }) {
  const ref = useRef(null)
  useEffect(() => {
    const avant = document.activeElement
    ref.current?.focus()
    const touche = (e) => e.key === 'Escape' && onFermer()
    document.addEventListener('keydown', touche)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', touche)
      document.body.style.overflow = ''
      avant?.focus?.()
    }
  }, [onFermer])
  return (
    <motion.div
      className="fond-modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={(e) => e.target === e.currentTarget && onFermer()}
    >
      <motion.div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="fiche-titre"
        tabIndex={-1}
        ref={ref}
        initial={{ y: 60, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        transition={{ duration: 0.45, ease: EASE }}
      >
        <motion.div className="formation-tete" layoutId={'tete-' + f.ref} style={{ position: 'relative' }}>
          <button className="fermer" onClick={onFermer} aria-label="Fermer la fiche">
            <X size={26} />
          </button>
          {f.badge && <span className="badge">{f.badge}</span>}
          <h3 id="fiche-titre">{f.nom}</h3>
          <p>{f.sousTitre}</p>
        </motion.div>
        <div className="modal-corps">
          <div className="meta">
            <span>
              <CalendarClock size={16} aria-hidden="true" /> {f.jours} jour{f.jours > 1 ? 's' : ''} · {f.heures} heures
            </span>
            <span>
              <Users size={16} aria-hidden="true" /> {f.effectif}
            </span>
            <span>
              <Building2 size={16} aria-hidden="true" /> {f.format}
            </span>
          </div>
          <div>
            <h4>Pour qui ?</h4>
            <p>{f.public}</p>
          </div>
          {f.objectifs ? (
            <div>
              <h4>En repartant, vous saurez :</h4>
              <ol>
                {f.objectifs.map((o, k) => (
                  <motion.li
                    key={o}
                    initial={{ opacity: 0, x: -16 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.25 + k * 0.05 }}
                  >
                    {o}
                  </motion.li>
                ))}
              </ol>
            </div>
          ) : (
            <p className="note">Programme détaillé en cours de finalisation. Contactez-nous pour être prévenu de l’ouverture.</p>
          )}
          <p className="note">
            Horaires : 08h00–12h00 / 13h00–17h00. Accès : 15 jours ouvrés minimum après inscription. Besoin d’un
            aménagement ? Notre référent handicap étudie chaque demande. Fiche programme complète sur demande — réf. {f.ref}.
          </p>
          <a className="btn btn-bleu" href={`mailto:${ENTREPRISE.email}?subject=${encodeURIComponent('Demande — ' + f.nom)}`}>
            Demander un devis <ArrowRight size={20} aria-hidden="true" />
          </a>
          <button className="btn btn-contour-bleu" onClick={onFermer}>
            Fermer la fiche
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

/* ---------- Implémentation : schéma de flux animé ---------- */
function Implementation() {
  return (
    <section id="implementation" className="sombre" aria-labelledby="titre-impl">
      <Pitons couleur="var(--bleu-nuit)" fond="var(--creme)" />
      <div className="conteneur bloc" style={{ paddingTop: 40 }}>
        <div className="impl">
          <div>
            <Reveal>
              <p className="surtitre">Solutions d’IA sur mesure</p>
            </Reveal>
            <TitreAnime id="titre-impl" texte="On ne s’arrête pas à la formation : on construit." />
            <Reveal>
              <p className="intro">
                Vous nous décrivez la tâche qui vous coûte des heures. Nous la transformons en outil qui tourne tout seul,
                avec un humain qui garde la main là où ça compte.
              </p>
            </Reveal>
            <div className="realisations">
              {[
                [Workflow, 'Workflows automatisés', 'Devis, relances, inscriptions : sans ressaisie.'],
                [Bot, 'Assistants IA métiers', 'Entraînés sur vos documents, cadrés par vos règles.'],
                [Globe, 'Sites internet', 'Rapides, accessibles, conformes dès la mise en ligne.'],
                [Database, 'Bases de données', 'Vos informations enfin réunies au même endroit.'],
                [Cpu, 'IA locale', 'Pour les données qui ne doivent jamais sortir.'],
                [LayoutDashboard, 'Tableaux de bord', 'Vos indicateurs clés, lisibles d’un coup d’œil.'],
              ].map(([Icone, t, d], k) => (
                <Reveal key={t} delay={k * 0.07} className="realisation">
                  <Icone size={30} aria-hidden="true" />
                  <div>
                    <strong>{t}</strong>
                    <span>{d}</span>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
          <Reveal y={60}>
            <SchemaFlux />
            <FluxMobile />
          </Reveal>
        </div>
      </div>
      <Pitons couleur="var(--creme)" fond="var(--bleu-nuit)" />
    </section>
  )
}

function SchemaFlux() {
  const calme = useReducedMotion()
  const noeuds = [
    { x: 90, y: 90, t: 'Demande client', s: 'formulaire, mail' },
    { x: 330, y: 90, t: 'Base de données', s: 'hébergée en UE' },
    { x: 330, y: 270, t: 'Agent IA', s: 'rédige, classe' },
    { x: 90, y: 270, t: 'Validation', s: 'humaine' },
    { x: 210, y: 420, t: 'Envoi + trace', s: 'journal horodaté' },
  ]
  const chemins = [
    'M150 90 L270 90',
    'M330 120 L330 240',
    'M270 270 L150 270',
    'M100 300 L190 392',
  ]
  return (
    <figure className="flux flux-large">
      <svg viewBox="0 0 440 480" role="img" aria-labelledby="flux-titre flux-desc">
        <title id="flux-titre">Exemple de workflow automatisé</title>
        <desc id="flux-desc">
          Une demande client arrive, elle est enregistrée dans une base hébergée en Europe, un agent IA prépare la réponse, un
          humain la valide, puis l’envoi est tracé.
        </desc>
        <defs>
          <linearGradient id="gflux" x1="0" x2="1">
            <stop offset="0" stopColor="#5b8bd6" />
            <stop offset="1" stopColor="#C9A84C" />
          </linearGradient>
        </defs>
        {chemins.map((d, k) => (
          <g key={k}>
            <path d={d} stroke="rgba(255,255,255,0.12)" strokeWidth="6" fill="none" strokeLinecap="round" />
            <motion.path
              d={d}
              stroke="url(#gflux)"
              strokeWidth="6"
              fill="none"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              whileInView={{ pathLength: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7, delay: 0.3 + k * 0.45, ease: 'easeInOut' }}
            />
            {!calme && (
              <circle r="7" fill="#e3c979">
                <animateMotion dur="2.4s" repeatCount="indefinite" begin={`${k * 0.6}s`} path={d} />
              </circle>
            )}
          </g>
        ))}
        {noeuds.map((n, k) => (
          <motion.g
            key={n.t}
            initial={{ opacity: 0, scale: 0.6 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 200, damping: 14, delay: 0.1 + k * 0.45 }}
            style={{ transformOrigin: `${n.x}px ${n.y}px` }}
          >
            <rect
              x={n.x - 72}
              y={n.y - 34}
              width="144"
              height="68"
              rx="18"
              fill={k === 3 ? '#C9A84C' : '#132b54'}
              stroke={k === 3 ? '#e3c979' : 'rgba(201,168,76,0.55)'}
              strokeWidth="2"
            />
            <text
              x={n.x}
              y={n.y - 4}
              textAnchor="middle"
              fontFamily="Montserrat, sans-serif"
              fontWeight="800"
              fontSize="16"
              fill={k === 3 ? '#0b1830' : '#ffffff'}
            >
              {n.t}
            </text>
            <text x={n.x} y={n.y + 19} textAnchor="middle" fontSize="14" fill={k === 3 ? '#0b1830' : '#c9d4e6'}>
              {n.s}
            </text>
          </motion.g>
        ))}
      </svg>
      <figcaption className="flux-legende">
        <span>
          <i style={{ background: '#C9A84C' }} /> Point d’arrêt humain obligatoire
        </span>
        <span>
          <i style={{ background: '#132b54', border: '2px solid #C9A84C' }} /> Étape automatisée
        </span>
      </figcaption>
    </figure>
  )
}

/* Version verticale du schéma pour les petits écrans : texte à taille réelle, pas d'SVG réduit */
function FluxMobile() {
  const calme = useReducedMotion()
  const etapes = [
    ['Demande client', 'formulaire, mail'],
    ['Base de données', 'hébergée en UE'],
    ['Agent IA', 'rédige, classe'],
    ['Validation humaine', 'point d’arrêt obligatoire'],
    ['Envoi + trace', 'journal horodaté'],
  ]
  return (
    <ol className="flux-mobile" aria-label="Exemple de workflow automatisé">
      {etapes.map(([t, s], k) => (
        <motion.li
          key={t}
          className={k === 3 ? 'humain' : undefined}
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.6 }}
          transition={{ duration: 0.5, delay: 0.05 * k }}
        >
          <strong>{t}</strong>
          <span>{s}</span>
          {k < etapes.length - 1 && (
            <span className="flux-mobile-lien" aria-hidden="true">
              {!calme && (
                <motion.i
                  animate={{ top: ['0%', '100%'], opacity: [0, 1, 0] }}
                  transition={{ duration: 1.4, repeat: Infinity, delay: k * 0.35, ease: 'easeInOut' }}
                />
              )}
            </span>
          )}
        </motion.li>
      ))}
    </ol>
  )
}

/* ---------- Méthode : ligne de temps tracée au défilement ---------- */
const ETAPES = [
  ['Diagnostic', 'On part de votre réalité : les tâches qui vous coûtent du temps, les données que vous manipulez, vos contraintes.'],
  ['Formation', 'Vos équipes apprennent sur leurs propres dossiers, en journées de 8 heures, en groupe réduit.'],
  ['Mise en place', 'On construit les outils avec vous : workflows, assistants, bases de données, sites.'],
  ['Preuve', 'Charte d’usage, registre, dossier de preuve des mesures prises : vous êtes prêts si on vous le demande.'],
]

function Methode() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 70%', 'end 60%'] })
  const echelle = useSpring(scrollYProgress, { stiffness: 90, damping: 22 })
  return (
    <section className="bloc clair" aria-labelledby="titre-methode" style={{ paddingTop: 40 }}>
      <div className="conteneur" style={{ maxWidth: 900 }}>
        <Reveal>
          <p className="surtitre">La méthode</p>
        </Reveal>
        <TitreAnime id="titre-methode" texte="Quatre étapes. Aucune boîte noire." />
        <div className="methode" ref={ref}>
          <div className="methode-rail" aria-hidden="true">
            <motion.div className="methode-rail-plein" style={{ scaleY: echelle }} />
          </div>
          <ol className="methode-liste">
          {ETAPES.map(([t, d], k) => (
            <li className="etape" key={t}>
              <motion.span
                className="etape-num"
                aria-hidden="true"
                initial={{ scale: 0.4, opacity: 0 }}
                whileInView={{ scale: 1, opacity: 1 }}
                viewport={{ once: true, amount: 1 }}
                transition={{ type: 'spring', stiffness: 260, damping: 16 }}
              >
                {k + 1}
              </motion.span>
              <Reveal className="etape-carte" y={0} initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }}>
                <h3>
                  <span className="sr-only">Étape {k + 1} : </span>
                  {t}
                </h3>
                <p>{d}</p>
              </Reveal>
            </li>
          ))}
          </ol>
        </div>
      </div>
    </section>
  )
}

/* ---------- Gouvernance ---------- */
function Gouvernance() {
  const listes = [
    {
      titre: 'RGPD',
      ref: 'Règlement (UE) 2016/679',
      items: ['Registre des traitements', 'Durées de conservation', 'Tri des données saisies dans l’IA', 'Procédure en cas de violation'],
    },
    {
      titre: 'IA Act',
      ref: 'Règlement (UE) 2024/1689',
      items: ['Inventaire de vos usages d’IA', 'Niveau de risque de chaque usage', 'Mentions de transparence', 'Supervision humaine documentée'],
    },
  ]
  return (
    <section id="gouvernance" className="sombre" aria-labelledby="titre-gouv">
      <Pitons couleur="var(--bleu-nuit)" fond="var(--creme)" />
      <div className="conteneur bloc" style={{ paddingTop: 40 }}>
        <Reveal>
          <p className="surtitre">Conseil & audit de gouvernance</p>
        </Reveal>
        <TitreAnime id="titre-gouv" texte="Utiliser l’IA, oui. Pouvoir le prouver, surtout." />
        <Reveal>
          <p className="intro">
            Nous ne vendons pas de « mise en conformité » miracle. Nous vous aidons à savoir ce que vous faites, à le
            documenter et à prouver les mesures prises.
          </p>
        </Reveal>
        <div className="gouv">
          {listes.map((l, i) => (
            <Reveal key={l.titre} delay={i * 0.15} className="gouv-carte">
              <h3>
                <ShieldCheck size={34} color="#C9A84C" aria-hidden="true" /> {l.titre}
              </h3>
              <span className="ref">{l.ref}</span>
              <ul className="coches">
                {l.items.map((it, k) => (
                  <motion.li
                    key={it}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, amount: 1 }}
                    transition={{ delay: 0.2 + k * 0.15 }}
                  >
                    <motion.span
                      className="coche"
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      viewport={{ once: true, amount: 1 }}
                      transition={{ type: 'spring', stiffness: 400, damping: 12, delay: 0.35 + k * 0.15 }}
                    >
                      <Check size={20} strokeWidth={3} aria-hidden="true" />
                    </motion.span>
                    {it}
                  </motion.li>
                ))}
              </ul>
            </Reveal>
          ))}
        </div>
        <Reveal className="souverain">
          <Globe size={48} color="#C9A84C" aria-hidden="true" />
          <p>
            <strong>Souveraineté des données.</strong> Nous privilégions des outils hébergés dans l’Union européenne,
            ou installés chez vous, pour que vos données et celles de vos clients restent sous votre contrôle.
          </p>
        </Reveal>
      </div>
      <Pitons couleur="var(--creme)" fond="var(--bleu-nuit)" />
    </section>
  )
}

/* ---------- À propos ---------- */
function APropos() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] })
  const y = useTransform(scrollYProgress, [0, 1], [30, -30])
  const yCadre = useTransform(scrollYProgress, [0, 1], [-30, 30])
  return (
    <section id="apropos" className="bloc clair" aria-labelledby="titre-apropos" ref={ref} style={{ paddingTop: 40 }}>
      <div className="conteneur apropos">
        <figure className="portrait">
          <motion.div className="portrait-cadre" style={{ y: yCadre }} aria-hidden="true" />
          <motion.picture style={{ y, display: 'block' }}>
            <source srcSet="media/aurelien-lumeka.webp" type="image/webp" />
            <img
              src="media/aurelien-lumeka.jpg"
              alt="Aurélien LUMEKA, souriant, en costume beige"
              width="640"
              height="800"
              loading="lazy"
            />
          </motion.picture>
          <figcaption>Portrait réalisé avec l’aide de l’IA.</figcaption>
        </figure>
        <div>
          <Reveal>
            <p className="surtitre">Qui suis-je</p>
          </Reveal>
          <TitreAnime id="titre-apropos" texte="Aurélien LUMEKA, formateur et dirigeant." />
          <Reveal>
            <p className="intro">
              Formateur en vente, management et compétences comportementales, j’interviens depuis 2021 dans plusieurs centres
              de formation. Depuis 2026, j’accompagne les TPE-PME réunionnaises sur l’intelligence artificielle : je forme
              les équipes, je mets en place les outils, et je sécurise leur usage.
            </p>
          </Reveal>
          <Reveal>
            <blockquote className="citation">L’IA ne remplace pas vos équipes. Elle leur rend du temps.</blockquote>
          </Reveal>
          <ul className="certifs">
            {CERTIFS.slice(0, 6).map((c, k) => (
              <motion.li
                key={c}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: k * 0.07 }}
              >
                <BadgeCheck size={18} aria-hidden="true" /> {c}
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}

/* ---------- Infos pratiques ---------- */
function Pratique() {
  const cartes = [
    [Clock, 'Horaires', '08h00–12h00 et 13h00–17h00. Deux pauses incluses, à 10h et 15h.'],
    [MapPin, 'Où ?', 'Dans vos locaux (intra), ou en salle de séminaire sur l’île (inter).'],
    [Timer, 'Délai d’accès', '15 jours ouvrés minimum entre l’inscription et le démarrage.'],
    [Accessibility, 'Handicap', 'Un référent handicap étudie avec vous chaque besoin d’aménagement.'],
  ]
  return (
    <section className="bloc clair" aria-labelledby="titre-pratique" style={{ paddingTop: 0 }}>
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Infos pratiques</p>
        </Reveal>
        <TitreAnime id="titre-pratique" texte="Simple à organiser." />
        <div className="pratique">
          {cartes.map(([Icone, t, d], k) => (
            <Reveal key={t} delay={k * 0.1} className="pratique-carte">
              <Icone size={38} aria-hidden="true" />
              <h3>{t}</h3>
              <p>{d}</p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ---------- Contact ---------- */
function Contact() {
  const calme = useReducedMotion()
  return (
    <section id="contact" className="bloc clair" aria-labelledby="titre-contact" style={{ paddingTop: 0 }}>
      <div className="conteneur">
        <Reveal y={80} className="contact">
          {!calme && (
            <motion.div
              aria-hidden="true"
              style={{
                position: 'absolute', right: -120, top: -120, width: 420, height: 420, borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(201,168,76,0.45), transparent 65%)',
              }}
              animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 6, repeat: Infinity }}
            />
          )}
          <div style={{ position: 'relative' }}>
            <p className="surtitre" style={{ color: 'var(--or)' }}>
              Contact
            </p>
            <h2 id="titre-contact">Une tâche vous prend trop de temps ? Parlons-en.</h2>
            <p>
              Un premier échange permet de voir si une formation, un outil ou un audit vous fera gagner du temps. Sans
              engagement.
            </p>
            <div className="contact-actions">
              <motion.a className="btn btn-or" href={ENTREPRISE.telLien} whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                <Phone size={22} aria-hidden="true" /> {ENTREPRISE.telAffiche}
              </motion.a>
              <motion.a className="btn btn-contour" href={'mailto:' + ENTREPRISE.email} whileHover={{ scale: 1.03 }}>
                <Mail size={22} aria-hidden="true" /> Écrire un e-mail
              </motion.a>
            </div>
            <p style={{ fontSize: '0.95rem', marginTop: 26 }}>
              <HeartHandshake size={18} aria-hidden="true" style={{ display: 'inline', verticalAlign: '-3px' }} /> Sainte-Clotilde —
              interventions dans toute La Réunion.
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  )
}

/* ---------- Pied de page : bloc-marque normalisé (CONFIG SYSTEME) ---------- */
function Pied() {
  const e = ENTREPRISE
  return (
    <footer className="pied">
      <div className="conteneur">
        <div className="pied-grille">
          <img className="pied-logo" src="media/logo-yeba.png" alt="YEBA FORMATIONS" width="220" height="190" loading="lazy" />
          <address className="bloc-marque" style={{ fontStyle: 'normal' }}>
            <strong>YEBA FORMATIONS</strong> — {e.dirigeant} EI, entrepreneur individuel
            <br />
            {e.adresse}
            <br />
            Tél. <a href={e.telLien}>{e.telAffiche}</a> — <a href={'mailto:' + e.email}>{e.email}</a>
            <br />
            SIRET {e.siret}
            <br />
            Déclaration d’activité n° {e.nda} auprès du Préfet de La Réunion. Cet enregistrement ne vaut pas agrément de
            l’État.
            <br />
            Certification Qualiopi n° {e.qualiopi} délivrée au titre de la catégorie actions de formation — organisme
            certificateur {e.certificateur}.
            <br />
            Référent handicap : {e.dirigeant} — {e.email}
          </address>
        </div>
        <nav className="pied-liens" aria-label="Informations légales">
          <a href="mentions-legales.html">Mentions légales</a>
          <a href="confidentialite.html">Politique de confidentialité</a>
          <span>Site sans cookie ni traceur publicitaire.</span>
          <span>Vidéo d’ambiance et portrait réalisés avec l’aide de l’IA.</span>
        </nav>
      </div>
    </footer>
  )
}

/* ---------- Panneau d'accessibilité ---------- */
function PanneauAcces({ taille, setTaille, contraste, setContraste, calme, setCalme }) {
  const [ouvert, setOuvert] = useState(false)
  return (
    <>
      <AnimatePresence>
        {ouvert && (
          <motion.div
            className="acces-panneau"
            id="panneau-acces"
            role="region"
            aria-labelledby="titre-acces"
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
          >
            <h2 id="titre-acces">Confort de lecture</h2>
            <div className="acces-ligne">
              <span>Taille du texte</span>
              <div className="acces-choix">
                {['1', '2', '3'].map((t, k) => (
                  <button key={t} aria-pressed={taille === t} onClick={() => setTaille(t)} style={{ fontSize: 16 + k * 4 }}>
                    A<span className="sr-only"> taille {k + 1}</span>
                  </button>
                ))}
              </div>
            </div>
            <div className="acces-ligne">
              <span>Contraste renforcé</span>
              <div className="acces-choix">
                <button aria-pressed={contraste === '0'} onClick={() => setContraste('0')}>Normal</button>
                <button aria-pressed={contraste === '1'} onClick={() => setContraste('1')}>Renforcé</button>
              </div>
            </div>
            <div className="acces-ligne">
              <span>Animations</span>
              <div className="acces-choix">
                <button aria-pressed={calme === '0'} onClick={() => setCalme('0')}>Activées</button>
                <button aria-pressed={calme === '1'} onClick={() => setCalme('1')}>En pause</button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <button
        className="acces-bouton"
        aria-expanded={ouvert}
        aria-controls="panneau-acces"
        aria-label="Options d’accessibilité"
        onClick={() => setOuvert((o) => !o)}
      >
        {ouvert ? <X size={30} /> : <Accessibility size={32} />}
      </button>
    </>
  )
}

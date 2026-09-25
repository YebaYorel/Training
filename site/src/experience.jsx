import { useMemo, useState } from 'react'
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion'
import { ArrowLeft, ArrowRight, Compass, Gauge, Plus, RotateCcw, TriangleAlert } from 'lucide-react'
import { ALERTES, DIAGNOSTIC, ENTREPRISE, FAQ, FINANCEURS, FORMATIONS, PROFILS, SYNCHRO } from './data.js'
import { Pitons, Reveal, TitreAnime } from './anim.jsx'

const EASE = [0.22, 1, 0.36, 1]
const nomDe = (ref) => FORMATIONS.find((f) => f.ref === ref)

/* ---------- Parcours par profil + diagnostic express ---------- */
export function Parcours({ onChoisir }) {
  return (
    <section id="diagnostic" className="bloc clair" aria-labelledby="titre-parcours" style={{ paddingTop: 0 }}>
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Par où commencer ?</p>
        </Reveal>
        <TitreAnime id="titre-parcours" texte="Dites-nous qui vous êtes. On vous montre le chemin." accent={[6, 7, 8]} />
        <div className="profils">
          {PROFILS.map((p, k) => (
            <Reveal key={p.id} delay={k * 0.08}>
              <button className="profil" onClick={() => onChoisir(p.id)}>
                <span className="profil-titre">{p.titre}</span>
                <span className="profil-texte">{p.texte}</span>
                <span className="profil-lien">
                  {p.refs.length} formations conseillées <ArrowRight size={18} aria-hidden="true" />
                </span>
              </button>
            </Reveal>
          ))}
        </div>
        <Diagnostic />
      </div>
    </section>
  )
}

function Diagnostic() {
  const [etape, setEtape] = useState(-1) // -1 : accueil ; DIAGNOSTIC.length : résultat
  const [reponses, setReponses] = useState([])
  const fini = etape >= DIAGNOSTIC.length

  function repondre(i) {
    const r = [...reponses.slice(0, etape), i]
    setReponses(r)
    setEtape(etape + 1)
  }
  function recommencer() {
    setReponses([])
    setEtape(0)
  }

  const resultat = useMemo(() => {
    if (!fini) return null
    const choix = reponses.map((i, q) => DIAGNOSTIC[q].r[i])
    const max = DIAGNOSTIC.reduce((s, q) => s + Math.max(...q.r.map((r) => r.m)), 0)
    const score = Math.round((choix.reduce((s, c) => s + c.m, 0) / max) * 100)
    const compte = {}
    choix.forEach((c, q) => c.refs.forEach((ref, k) => (compte[ref] = (compte[ref] ?? 0) + 3 - k + (q === 5 ? 2 : 0))))
    const refs = Object.entries(compte)
      .sort((a, b) => b[1] - a[1])
      .map(([r]) => r)
      .filter((r) => nomDe(r))
      .slice(0, 3)
    const alertes = [...new Set(choix.map((c) => c.alerte).filter(Boolean))].map((a) => ALERTES[a])
    return { score, refs, alertes }
  }, [fini, reponses])

  const niveau = resultat && (resultat.score < 35 ? 'Démarrage' : resultat.score < 70 ? 'En construction' : 'Avancé')
  const corpsMail =
    resultat &&
    encodeURIComponent(
      `Bonjour,\n\nJ'ai fait le diagnostic express sur votre site.\nNiveau : ${niveau} (${resultat.score}/100)\nFormations suggérées : ${resultat.refs
        .map((r) => nomDe(r).nom)
        .join(', ')}\n\nPouvons-nous en parler ?\n`,
    )

  return (
    <Reveal className="diagnostic" y={60}>
      <div className="diag-tete">
        <Compass size={30} aria-hidden="true" />
        <div>
          <h3>Diagnostic IA express</h3>
          <p>6 questions, 1 minute. Le calcul se fait dans votre navigateur : aucune réponse ne nous est envoyée.</p>
        </div>
      </div>
      {etape >= 0 && !fini && (
        <div className="diag-progression" aria-hidden="true">
          <motion.span animate={{ width: `${(etape / DIAGNOSTIC.length) * 100}%` }} transition={{ ease: EASE }} />
        </div>
      )}
      <div className="diag-scene" aria-live="polite">
        <AnimatePresence mode="wait" initial={false}>
          {etape === -1 && (
            <motion.div key="accueil" {...glisse}>
              <button className="btn btn-or" onClick={() => setEtape(0)}>
                Commencer le diagnostic <ArrowRight size={20} aria-hidden="true" />
              </button>
            </motion.div>
          )}
          {etape >= 0 && !fini && (
            <motion.fieldset key={'q' + etape} {...glisse} className="diag-question">
              <legend>
                <span className="diag-num">
                  Question {etape + 1} sur {DIAGNOSTIC.length}
                </span>
                {DIAGNOSTIC[etape].q}
              </legend>
              <div className="diag-choix">
                {DIAGNOSTIC[etape].r.map((r, i) => (
                  <button key={r.t} className="choix" onClick={() => repondre(i)} aria-pressed={reponses[etape] === i}>
                    {r.t}
                  </button>
                ))}
              </div>
              {etape > 0 && (
                <button className="retour-diag" onClick={() => setEtape(etape - 1)}>
                  <ArrowLeft size={18} aria-hidden="true" /> Question précédente
                </button>
              )}
            </motion.fieldset>
          )}
          {fini && resultat && (
            <motion.div key="resultat" {...glisse} className="diag-resultat">
              <Jauge score={resultat.score} niveau={niveau} />
              <div>
                <h4>Nos conseils pour vous</h4>
                <ol className="diag-reco">
                  {resultat.refs.map((r, k) => {
                    const f = nomDe(r)
                    return (
                      <motion.li key={r} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 + k * 0.12 }}>
                        <strong>{f.nom}</strong> — {f.sousTitre}
                      </motion.li>
                    )
                  })}
                </ol>
                {resultat.alertes.map((a) => (
                  <p key={a} className="diag-alerte">
                    <TriangleAlert size={20} aria-hidden="true" /> {a}
                  </p>
                ))}
                <div className="diag-actions">
                  <a className="btn btn-or" href={`mailto:${ENTREPRISE.email}?subject=${encodeURIComponent('Mon diagnostic IA')}&body=${corpsMail}`}>
                    Recevoir mon plan d’action <ArrowRight size={20} aria-hidden="true" />
                  </a>
                  <button className="btn btn-contour" onClick={recommencer}>
                    <RotateCcw size={18} aria-hidden="true" /> Recommencer
                  </button>
                </div>
                <p className="discret-sombre">
                  Indicatif : ce diagnostic applique des règles simples et ne remplace pas l’entretien de cadrage.
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Reveal>
  )
}

const glisse = {
  initial: { opacity: 0, x: 40 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -40 },
  transition: { duration: 0.35, ease: EASE },
}

function Jauge({ score, niveau }) {
  const calme = useReducedMotion()
  const C = 2 * Math.PI * 70
  return (
    <figure className="jauge">
      <svg viewBox="0 0 180 180" role="img" aria-label={`Maturité IA : ${score} sur 100, niveau ${niveau}`}>
        <circle cx="90" cy="90" r="70" fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth="16" />
        <motion.circle
          cx="90"
          cy="90"
          r="70"
          fill="none"
          stroke="url(#gjauge)"
          strokeWidth="16"
          strokeLinecap="round"
          transform="rotate(-90 90 90)"
          strokeDasharray={C}
          initial={{ strokeDashoffset: calme ? C * (1 - score / 100) : C }}
          animate={{ strokeDashoffset: C * (1 - score / 100) }}
          transition={{ duration: 1.4, ease: EASE, delay: 0.2 }}
        />
        <defs>
          <linearGradient id="gjauge" x1="0" x2="1">
            <stop offset="0" stopColor="#5b8bd6" />
            <stop offset="1" stopColor="#C9A84C" />
          </linearGradient>
        </defs>
        <text x="90" y="92" textAnchor="middle" fill="#fff" fontFamily="Montserrat, sans-serif" fontWeight="900" fontSize="42">
          {score}
        </text>
        <text x="90" y="118" textAnchor="middle" fill="#dbe3f0" fontSize="14">
          sur 100
        </text>
      </svg>
      <figcaption>
        <Gauge size={18} aria-hidden="true" /> Maturité IA : <strong>{niveau}</strong>
      </figcaption>
    </figure>
  )
}

/* ---------- Résultats (RNQ ind. 2) et financement ---------- */
export function Resultats() {
  const avecDonnees = FORMATIONS.filter((f) => f.indicateurs?.stagiaires || f.indicateurs?.satisfaction != null)
  const financeurs = [...new Set(FORMATIONS.flatMap((f) => f.financements ?? []))]
  return (
    <section id="financement" className="bloc clair" aria-labelledby="titre-resultats" style={{ paddingTop: 40 }}>
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Résultats & financement</p>
        </Reveal>
        <TitreAnime id="titre-resultats" texte="Des chiffres vérifiables. Des financements possibles." />
        <div className="resultats">
          <Reveal className="resultats-carte">
            <h3>Nos indicateurs de résultats</h3>
            <p>
              Publiés formation par formation, et mis à jour depuis notre base à chaque session (dernière mise à jour le{' '}
              {new Date(SYNCHRO).toLocaleDateString('fr-FR')}).
            </p>
            <div className="table-defilante">
            <table>
              <caption className="sr-only">Indicateurs de résultats par formation</caption>
              <thead>
                <tr>
                  <th scope="col">Formation</th>
                  <th scope="col">Stagiaires formés</th>
                  <th scope="col">Satisfaction</th>
                  <th scope="col">Réussite</th>
                </tr>
              </thead>
              <tbody>
                {avecDonnees.map((f) => (
                  <tr key={f.ref}>
                    <th scope="row">{f.nom}</th>
                    <td>{f.indicateurs.stagiaires ?? '—'}</td>
                    <td>{f.indicateurs.satisfaction != null ? f.indicateurs.satisfaction + ' %' : 'à venir'}</td>
                    <td>{f.indicateurs.reussite != null ? f.indicateurs.reussite + ' %' : 'à venir'}</td>
                  </tr>
                ))}
                <tr>
                  <th scope="row">Autres formations</th>
                  <td colSpan={3}>Récentes : premiers résultats publiés après leurs premières sessions.</td>
                </tr>
              </tbody>
            </table>
            </div>
          </Reveal>
          <Reveal className="resultats-carte" delay={0.12}>
            <h3>Qui peut financer ?</h3>
            <ul className="financeurs">
              {financeurs.map((n) => (
                <li key={n}>
                  <strong>{n}</strong> — {FINANCEURS[n] ?? 'selon les critères du financeur.'}
                </li>
              ))}
            </ul>
            <p className="note">Certifiés Qualiopi : c’est la condition demandée par les financeurs publics et paritaires.</p>
          </Reveal>
        </div>
      </div>
    </section>
  )
}

/* ---------- La Réunion : carte stylisée des interventions ---------- */
// Contour approché à partir de coordonnées réelles (projection simple lon/lat → viewBox 400×320).
const CONTOUR = [
  [150, 24], [178, 30], [211, 41], [244, 46], [265, 72], [304, 108], [342, 160], [347, 248], [331, 279], [290, 292], [249, 290],
  [210, 282], [173, 269], [140, 252], [113, 233], [84, 206], [64, 181], [44, 150], [31, 119], [44, 104], [58, 93], [64, 56],
  [96, 51], [122, 34],
]
function lisser(points) {
  const m = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
  let d = `M${m(points.at(-1), points[0]).join(' ')}`
  points.forEach((p, i) => {
    const suiv = points[(i + 1) % points.length]
    d += ` Q${p.join(' ')} ${m(p, suiv).join(' ')}`
  })
  return d + 'Z'
}
const VILLES = [
  { n: 'Sainte-Clotilde', x: 178, y: 36, siege: true },
  { n: 'Le Port', x: 69, y: 61 },
  { n: 'Saint-Paul', x: 58, y: 98 },
  { n: 'Saint-Leu', x: 69, y: 181 },
  { n: 'Saint-Pierre', x: 173, y: 269 },
  { n: 'Saint-Joseph', x: 249, y: 288 },
  { n: 'Saint-Benoît', x: 298, y: 108 },
  { n: 'Saint-André', x: 262, y: 74 },
]
const PITONS = [
  { n: 'Piton des Neiges', x: 173, y: 144 },
  { n: 'Piton de la Fournaise', x: 298, y: 217 },
]

export function Reunion() {
  const calme = useReducedMotion()
  const siege = VILLES[0]
  return (
    <section className="sombre" aria-labelledby="titre-reunion">
      <Pitons couleur="var(--bleu-nuit)" fond="var(--creme)" />
      <div className="conteneur reunion" style={{ paddingBlock: '30px clamp(70px, 9vw, 120px)' }}>
        <div>
          <Reveal>
            <p className="surtitre">Partout sur l’île</p>
          </Reveal>
          <TitreAnime id="titre-reunion" texte="Du Nord au Sud, on vient à vous." accent={[3, 4]} />
          <Reveal>
            <p className="intro">
              Basés à Sainte-Clotilde, nous intervenons dans vos locaux partout à La Réunion, et réunissons les sessions
              inter-entreprises en salle de séminaire, au plus près des participants.
            </p>
          </Reveal>
          <ul className="villes-liste">
            {VILLES.map((v) => (
              <li key={v.n}>{v.n}</li>
            ))}
          </ul>
        </div>
        <Reveal y={40}>
          <svg className="carte-ile" viewBox="0 0 400 320" aria-hidden="true">
            <defs>
              <radialGradient id="relief" cx="0.45" cy="0.5" r="0.6">
                <stop offset="0" stopColor="#1f4a86" />
                <stop offset="1" stopColor="#0f2346" />
              </radialGradient>
            </defs>
            <motion.path
              d={lisser(CONTOUR)}
              fill="url(#relief)"
              stroke="#C9A84C"
              strokeWidth="3"
              initial={{ pathLength: calme ? 1 : 0, fillOpacity: calme ? 1 : 0 }}
              whileInView={{ pathLength: 1, fillOpacity: 1 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ pathLength: { duration: 2, ease: 'easeInOut' }, fillOpacity: { duration: 0.8, delay: 1.4 } }}
            />
            {PITONS.map((p, k) => (
              <motion.g
                key={p.n}
                initial={{ opacity: calme ? 1 : 0, y: calme ? 0 : 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 1.6 + k * 0.2 }}
              >
                <path d={`M${p.x - 16} ${p.y + 12} L${p.x} ${p.y - 14} L${p.x + 16} ${p.y + 12} Z`} fill="none" stroke="#8fb0e3" strokeWidth="2.5" strokeLinejoin="round" />
              </motion.g>
            ))}
            {VILLES.slice(1).map((v, k) => (
              <motion.path
                key={'l' + v.n}
                d={`M${siege.x} ${siege.y} Q${(siege.x + v.x) / 2 + 20} ${(siege.y + v.y) / 2 - 10} ${v.x} ${v.y}`}
                fill="none"
                stroke="#e3c979"
                strokeWidth="1.6"
                strokeDasharray="4 5"
                initial={{ pathLength: calme ? 1 : 0, opacity: 0.7 }}
                whileInView={{ pathLength: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 1, delay: 2 + k * 0.12 }}
              />
            ))}
            {VILLES.map((v, k) => (
              <motion.g
                key={v.n}
                initial={{ scale: calme ? 1 : 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 300, damping: 14, delay: 2.2 + k * 0.1 }}
                style={{ transformOrigin: `${v.x}px ${v.y}px` }}
              >
                {v.siege && !calme && (
                  <motion.circle cx={v.x} cy={v.y} r="8" fill="none" stroke="#C9A84C" strokeWidth="2" animate={{ r: [8, 24], opacity: [0.9, 0] }} transition={{ duration: 2, repeat: Infinity }} />
                )}
                <circle cx={v.x} cy={v.y} r={v.siege ? 8 : 5.5} fill={v.siege ? '#C9A84C' : '#ffffff'} />
              </motion.g>
            ))}
            <text x={siege.x + 12} y={siege.y - 8} fill="#ffffff" fontFamily="Montserrat, sans-serif" fontWeight="800" fontSize="15">
              YEBA
            </text>
          </svg>
        </Reveal>
      </div>
      <Pitons couleur="var(--creme)" fond="var(--bleu-nuit)" />
    </section>
  )
}

/* ---------- Questions fréquentes ---------- */
export function Questions() {
  const [ouverte, setOuverte] = useState(0)
  return (
    <section id="faq" className="bloc clair" aria-labelledby="titre-faq" style={{ paddingTop: 40 }}>
      <div className="conteneur" style={{ maxWidth: 900 }}>
        <Reveal>
          <p className="surtitre">Questions fréquentes</p>
        </Reveal>
        <TitreAnime id="titre-faq" texte="Les questions qu’on nous pose le plus." />
        <div className="faq">
          {FAQ.map(([q, r], k) => (
            <Reveal key={q} delay={k * 0.04} className={'faq-item' + (ouverte === k ? ' ouvert' : '')}>
              <h3>
                <button aria-expanded={ouverte === k} aria-controls={'faq-' + k} id={'faq-q-' + k} onClick={() => setOuverte(ouverte === k ? -1 : k)}>
                  {q}
                  <motion.span animate={{ rotate: ouverte === k ? 45 : 0 }} className="faq-plus" aria-hidden="true">
                    <Plus size={24} />
                  </motion.span>
                </button>
              </h3>
              <AnimatePresence initial={false}>
                {ouverte === k && (
                  <motion.div
                    id={'faq-' + k}
                    role="region"
                    aria-labelledby={'faq-q-' + k}
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.35, ease: EASE }}
                    style={{ overflow: 'hidden' }}
                  >
                    <p>{r}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

import { useEffect, useRef, useState } from 'react'
import {
  animate,
  motion,
  useInView,
  useMotionValue,
  useReducedMotion,
  useSpring,
  useTransform,
} from 'framer-motion'

const EASE = [0.22, 1, 0.36, 1]

/** Apparition au défilement : montée + fondu. */
export function Reveal({ children, delay = 0, y = 40, as = 'div', ...rest }) {
  const M = motion[as]
  return (
    <M
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.8, delay, ease: EASE }}
      {...rest}
    >
      {children}
    </M>
  )
}

/** Titre dont chaque mot surgit d'un masque (effet « grands sites »).
 *  Le déclenchement est porté par le titre entier : un mot masqué par son cadre
 *  n'est jamais « visible » pour l'IntersectionObserver. */
export function TitreAnime({ texte, as = 'h2', id, accent = [] }) {
  const T = motion[as]
  const mots = texte.split(' ')
  return (
    <T
      id={id}
      aria-label={texte}
      initial="cache"
      whileInView="visible"
      viewport={{ once: true, amount: 0.5 }}
      transition={{ staggerChildren: 0.06 }}
    >
      {mots.map((mot, i) => (
        <span
          key={i}
          aria-hidden="true"
          style={{ display: 'inline-block', overflow: 'hidden', verticalAlign: 'top', paddingBottom: '0.08em' }}
        >
          <motion.span
            style={{ display: 'inline-block', marginRight: '0.24em' }}
            className={accent.includes(i) ? 'accent-titre' : undefined}
            variants={{ cache: { y: '110%' }, visible: { y: '0%', transition: { duration: 0.9, ease: EASE } } }}
          >
            {mot}
          </motion.span>
        </span>
      ))}
    </T>
  )
}

/** Compteur qui s'anime quand il entre à l'écran. */
export function Compteur({ vers, suffixe = '', duree = 1.6 }) {
  const ref = useRef(null)
  const vu = useInView(ref, { once: true, amount: 0.8 })
  const calme = useReducedMotion()
  const [val, setVal] = useState(calme ? vers : 0)
  useEffect(() => {
    if (!vu) return
    if (calme) return setVal(vers)
    const c = animate(0, vers, { duration: duree, ease: EASE, onUpdate: (v) => setVal(Math.round(v)) })
    return () => c.stop()
  }, [vu, vers, duree, calme])
  return (
    <strong ref={ref}>
      {val}
      {suffixe}
    </strong>
  )
}

/** Carte qui s'incline en 3D sous la souris (désactivé si mouvements réduits). */
export function CarteInclinee({ children, className, ...rest }) {
  const calme = useReducedMotion()
  const x = useMotionValue(0.5)
  const y = useMotionValue(0.5)
  const rx = useSpring(useTransform(y, [0, 1], [7, -7]), { stiffness: 200, damping: 20 })
  const ry = useSpring(useTransform(x, [0, 1], [-7, 7]), { stiffness: 200, damping: 20 })
  function bouge(e) {
    if (calme || e.pointerType !== 'mouse') return
    const r = e.currentTarget.getBoundingClientRect()
    x.set((e.clientX - r.left) / r.width)
    y.set((e.clientY - r.top) / r.height)
  }
  function sort() {
    x.set(0.5)
    y.set(0.5)
  }
  return (
    <motion.div
      className={className}
      style={calme ? undefined : { rotateX: rx, rotateY: ry, transformPerspective: 900 }}
      onPointerMove={bouge}
      onPointerLeave={sort}
      {...rest}
    >
      {children}
    </motion.div>
  )
}

/** Séparateur de section en forme de trois pitons — rappel du logo. */
export function Pitons({ couleur, fond, inverse = false }) {
  return (
    <svg
      className="pitons"
      viewBox="0 0 1440 130"
      preserveAspectRatio="none"
      aria-hidden="true"
      style={{ background: fond, transform: inverse ? 'scaleY(-1)' : undefined }}
    >
      <motion.path
        fill={couleur}
        initial={{ d: 'M0 132 L0 132 L360 132 L560 132 L720 132 L900 132 L1080 132 L1440 132 L1440 132 Z' }}
        whileInView={{ d: 'M0 132 L0 110 L360 40 L560 96 L720 8 L900 92 L1080 34 L1440 104 L1440 132 Z' }}
        viewport={{ once: true, amount: 0.9 }}
        transition={{ duration: 1.2, ease: EASE }}
      />
    </svg>
  )
}

/** Réseau neuronal posé sur trois pitons, tracé à l'écran — reprise animée du logo. */
export function ReseauPitons({ className }) {
  const calme = useReducedMotion()
  const ref = useRef(null)
  // Les halos ne tournent que lorsque le réseau est à l'écran : rien ne se recalcule pendant le défilement ailleurs
  const visible = useInView(ref, { amount: 0.2 })
  const triangles = [
    { d: 'M40 380 L200 140 L360 380 Z', c: '#3d6bb3' },
    { d: 'M200 380 L380 40 L560 380 Z', c: '#8f8a6a' },
    { d: 'M400 380 L560 140 L720 380 Z', c: '#C9A84C' },
  ]
  const noeuds = [
    [150, 240], [245, 290], [110, 320], [330, 150], [300, 250], [430, 170], [390, 290], [470, 270], [540, 230], [620, 300], [580, 340], [255, 330],
  ]
  const liens = [
    [0, 1], [0, 2], [1, 4], [3, 4], [3, 5], [4, 6], [5, 6], [5, 7], [6, 7], [7, 8], [8, 9], [9, 10], [1, 11], [6, 11], [2, 11], [7, 10],
  ]
  return (
    <svg ref={ref} className={className} viewBox="0 0 760 400" aria-hidden="true">
      <defs>
        <linearGradient id="grad-reseau" x1="0" x2="1">
          <stop offset="0" stopColor="#5b8bd6" />
          <stop offset="1" stopColor="#C9A84C" />
        </linearGradient>
      </defs>
      {triangles.map((t, i) => (
        <motion.path
          key={i}
          d={t.d}
          fill="none"
          stroke={t.c}
          strokeWidth="10"
          strokeLinejoin="round"
          initial={{ pathLength: calme ? 1 : 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.6, delay: 0.4 + i * 0.25, ease: EASE }}
        />
      ))}
      {liens.map(([a, b], i) => (
        <motion.line
          key={i}
          x1={noeuds[a][0]}
          y1={noeuds[a][1]}
          x2={noeuds[b][0]}
          y2={noeuds[b][1]}
          stroke="url(#grad-reseau)"
          strokeWidth="3"
          initial={{ pathLength: calme ? 1 : 0, opacity: 0.2 }}
          animate={{ pathLength: 1, opacity: 0.85 }}
          transition={{ duration: 0.8, delay: 1.2 + i * 0.07 }}
        />
      ))}
      {noeuds.map(([x, y], i) => (
        <motion.circle
          key={i}
          cx={x}
          cy={y}
          r="9"
          fill={x < 330 ? '#5b8bd6' : '#C9A84C'}
          initial={{ scale: calme ? 1 : 0 }}
          animate={calme ? { scale: 1 } : { scale: [0, 1.4, 1], opacity: [1, 1, 0.9] }}
          transition={{ duration: 0.6, delay: 1.4 + i * 0.08 }}
        />
      ))}
      {!calme &&
        visible &&
        noeuds
          .filter((_, i) => i % 2 === 0)
          .map(([x, y], i) => (
            <motion.circle
              key={'halo' + i}
              cx={x}
              cy={y}
              r="9"
              fill="none"
              stroke="#e3c979"
              strokeWidth="2"
              style={{ transformBox: 'fill-box', transformOrigin: 'center' }}
              initial={{ scale: 1, opacity: 0 }}
              animate={{ scale: [1, 2.8], opacity: [0.8, 0] }}
              transition={{ duration: 2.4, repeat: Infinity, delay: 1 + i * 0.45, ease: 'easeOut' }}
            />
          ))}
    </svg>
  )
}

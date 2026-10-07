// Ouverture du site : le logo se dessine dans le noir, trait par trait, puis s'illumine et laisse place au site.
// Une fois par onglet (sessionStorage), jamais si l'utilisateur demande moins d'animations ; un clic ou une touche l'abrège.
// Décoratif : aria-hidden, le contenu du site est déjà dans la page derrière.
import { useEffect, useState } from 'react'

const CLE = 'yeba-intro-vue'
const FIN = 3300 // ms : le site commence à apparaître (le héros démarre ici)
const RETRAIT = 3900 // ms : l'intro quitte le DOM

let terminee = false
const abonnes = new Set()
function terminer() {
  if (terminee) return
  terminee = true
  abonnes.forEach((f) => f())
  abonnes.clear()
}

function doitJouer() {
  try {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return false
    if (sessionStorage.getItem(CLE)) return false
    sessionStorage.setItem(CLE, '1')
  } catch {
    /* stockage indisponible (navigation privée, aperçu) : on joue l'intro */
  }
  return true
}
const JOUER = typeof window !== 'undefined' && doitJouer()
if (!JOUER) terminee = true

/** Vrai quand le site doit commencer ses propres animations d'entrée. */
export function useIntroTerminee() {
  const [fini, setFini] = useState(terminee)
  useEffect(() => {
    if (terminee) return setFini(true)
    const f = () => setFini(true)
    abonnes.add(f)
    return () => abonnes.delete(f)
  }, [])
  return fini
}

// Géométrie du logo (repère 520 × 443, celui de logo-yeba.png)
const TRIANGLES = ['M48 222 L148 76 L250 222 Z', 'M158 222 L243 38 L345 222 Z', 'M248 222 L348 78 L452 222 Z']
const NOEUDS = [
  [143, 139], [113, 188], [165, 177], [244, 98], [214, 134], [276, 134], [248, 160], [208, 183], [292, 178], [346, 139], [322, 177], [377, 188],
]
const LIENS = [
  [0, 1], [0, 2], [1, 2], [2, 7], [0, 4], [3, 4], [3, 5], [4, 6], [5, 6], [4, 7], [6, 7], [6, 8], [5, 8], [5, 9], [8, 10], [9, 10], [9, 11], [10, 11],
]
const BORDS = [
  [[143, 139], [117, 124]], [[113, 188], [70, 190]], [[113, 188], [100, 222]], [[165, 177], [160, 222]], [[244, 98], [243, 52]],
  [[208, 183], [200, 222]], [[292, 178], [300, 222]], [[346, 139], [384, 128]], [[377, 188], [418, 196]], [[322, 177], [330, 222]],
]
const LETTRES = [['Y', 92], ['E', 196], ['B', 300], ['A', 410]]

export default function Intro() {
  const [etat, setEtat] = useState(JOUER ? 'attente' : 'fini') // attente → joue → sortie → fini

  useEffect(() => {
    document.querySelector('.intro-voile')?.remove()
    if (!JOUER) return
    const racine = document.documentElement
    racine.classList.add('intro-active')
    let minuteries = []
    let parti = false
    const partir = () => {
      if (parti) return
      parti = true
      setEtat('joue')
      minuteries = [
        setTimeout(() => (setEtat('sortie'), terminer()), FIN),
        setTimeout(() => setEtat('fini'), RETRAIT),
      ]
    }
    // Les triangles n'ont pas besoin de police : on démarre tout de suite ; la police (locale) arrive avant les lettres.
    document.fonts?.load('900 128px Montserrat').catch(() => {})
    requestAnimationFrame(partir)

    const abreger = () => {
      minuteries.forEach(clearTimeout)
      parti = true
      setEtat('sortie')
      terminer()
      minuteries = [setTimeout(() => setEtat('fini'), 450)]
    }
    addEventListener('keydown', abreger, { once: true })
    addEventListener('pointerdown', abreger, { once: true })
    addEventListener('wheel', abreger, { once: true, passive: true })
    return () => {
      minuteries.forEach(clearTimeout)
      removeEventListener('keydown', abreger)
      removeEventListener('pointerdown', abreger)
      removeEventListener('wheel', abreger)
      racine.classList.remove('intro-active')
    }
  }, [])

  useEffect(() => {
    if (etat === 'fini') document.documentElement.classList.remove('intro-active')
  }, [etat])

  if (etat === 'fini') return null
  return (
    <div className={'ouverture ' + etat} aria-hidden="true">
      <div className="intro-lumiere" />
      <svg className="intro-logo" viewBox="0 0 520 443" role="presentation" focusable="false">
        <defs>
          <linearGradient id="intro-trait" x1="60" y1="0" x2="460" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#7fa6ea" />
            <stop offset="0.5" stopColor="#c8c6b4" />
            <stop offset="1" stopColor="#f3dc96" />
          </linearGradient>
          <linearGradient id="intro-vrai" x1="120" y1="0" x2="400" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#1B3A6B" />
            <stop offset="0.5" stopColor="#6f6f5e" />
            <stop offset="1" stopColor="#C9A84C" />
          </linearGradient>
          <filter id="intro-halo" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="flou" />
            <feMerge>
              <feMergeNode in="flou" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* 1. Le tracé lumineux, dans le noir */}
        <g className="intro-trace" filter="url(#intro-halo)" stroke="url(#intro-trait)" fill="none" strokeLinecap="round" strokeLinejoin="round">
          {TRIANGLES.map((d, k) => (
            <path key={d} d={d} pathLength="1" className="trace-triangle" style={{ '--d': k * 0.2 + 's' }} />
          ))}
          {LIENS.map(([a, b], k) => (
            <line key={'l' + k} x1={NOEUDS[a][0]} y1={NOEUDS[a][1]} x2={NOEUDS[b][0]} y2={NOEUDS[b][1]} pathLength="1" className="trace-lien" style={{ '--d': 0.75 + k * 0.05 + 's' }} />
          ))}
          {BORDS.map(([[x1, y1], [x2, y2]], k) => (
            <line key={'b' + k} x1={x1} y1={y1} x2={x2} y2={y2} pathLength="1" className="trace-lien" style={{ '--d': 1.05 + k * 0.05 + 's' }} />
          ))}
          {NOEUDS.map(([x, y], k) => (
            <circle key={'n' + k} cx={x} cy={y} r="6.5" className="trace-noeud" style={{ '--d': 1.45 + k * 0.035 + 's' }} />
          ))}
          {LETTRES.map(([l, x], k) => (
            <text key={l} x={x} y="338" textAnchor="middle" className="trace-lettre trace-yeba" style={{ '--d': 1.0 + k * 0.12 + 's' }}>
              {l}
            </text>
          ))}
          <text x="260" y="402" textAnchor="middle" textLength="418" lengthAdjust="spacingAndGlyphs" className="trace-lettre trace-formations" style={{ '--d': '1.55s' }}>
            FORMATIONS
          </text>
        </g>

        {/* 2. Le logo réel, qui s'allume */}
        <g className="intro-vrai">
          <g stroke="url(#intro-vrai)" fill="none" strokeLinejoin="round">
            {TRIANGLES.map((d) => (
              <path key={d} d={d} strokeWidth="10" />
            ))}
            {[...LIENS.map(([a, b]) => [NOEUDS[a], NOEUDS[b]]), ...BORDS].map(([[x1, y1], [x2, y2]], k) => (
              <line key={k} x1={x1} y1={y1} x2={x2} y2={y2} strokeWidth="3" />
            ))}
          </g>
          <g fill="url(#intro-vrai)">
            {NOEUDS.map(([x, y], k) => (
              <circle key={k} cx={x} cy={y} r="6.5" />
            ))}
          </g>
          {LETTRES.map(([l, x]) => (
            <text key={l} x={x} y="338" textAnchor="middle" className="vrai-yeba">
              {l}
            </text>
          ))}
          <text x="260" y="402" textAnchor="middle" textLength="418" lengthAdjust="spacingAndGlyphs" className="vrai-formations">
            FORMATIONS
          </text>
        </g>
      </svg>
    </div>
  )
}

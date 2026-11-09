import { motion, useReducedMotion } from 'framer-motion'

// Portrait illustré d'IFA : jeune femme noire, cheveux afro, créoles dorées, micro-casque.
// Personnage fictif dessiné en vecteurs (aucune photo, aucune personne réelle).
// Animations : clignement des yeux, légère respiration, bouche qui bouge quand elle « parle ».
export default function Avatar({ taille = 56, parle = false, className }) {
  const calme = useReducedMotion()
  const peau = '#8a5638'
  const peauOmbre = '#6f412a'
  const cheveux = '#1a110d'
  const boucles = [
    [22, 40], [18, 55], [22, 70], [30, 26], [44, 16], [60, 12], [76, 16], [90, 26], [98, 40], [102, 55], [98, 70],
    [34, 80], [86, 80], [28, 50], [92, 50],
  ]
  return (
    <svg className={className} width={taille} height={taille} viewBox="0 0 120 120" role="img" aria-label="IFA, assistante virtuelle">
      <defs>
        <clipPath id="ifa-rond">
          <circle cx="60" cy="60" r="60" />
        </clipPath>
        <radialGradient id="ifa-fond" cx="0.5" cy="0.35" r="0.75">
          <stop offset="0" stopColor="#2b5aa0" />
          <stop offset="1" stopColor="#0b1830" />
        </radialGradient>
        <linearGradient id="ifa-peau" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="#95603f" />
          <stop offset="1" stopColor={peau} />
        </linearGradient>
      </defs>
      <g clipPath="url(#ifa-rond)">
        <rect width="120" height="120" fill="url(#ifa-fond)" />
        <motion.g
          animate={calme ? undefined : { y: [0, -1.2, 0] }}
          transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
        >
          {/* Chevelure afro, derrière la tête */}
          <circle cx="60" cy="48" r="38" fill={cheveux} />
          {boucles.map(([x, y], i) => (
            <circle key={i} cx={x} cy={y} r="11" fill={cheveux} />
          ))}
          {/* Buste et haut bleu à col doré */}
          <path d="M14 120 C18 100 36 94 60 94 C84 94 102 100 106 120 Z" fill="#1B3A6B" />
          <path d="M46 95 L60 110 L74 95" fill="none" stroke="#C9A84C" strokeWidth="3" strokeLinejoin="round" />
          {/* Cou */}
          <path d="M51 78 L51 97 C55 101 65 101 69 97 L69 78 Z" fill={peauOmbre} />
          {/* Oreilles et créoles */}
          <ellipse cx="38.5" cy="62" rx="4.5" ry="6.5" fill={peauOmbre} />
          <ellipse cx="81.5" cy="62" rx="4.5" ry="6.5" fill={peauOmbre} />
          <circle cx="38" cy="75" r="6" fill="none" stroke="#e3c979" strokeWidth="2.2" />
          <circle cx="82" cy="75" r="6" fill="none" stroke="#e3c979" strokeWidth="2.2" />
          {/* Visage */}
          <path d="M39 56 C39 38 49 32 60 32 C71 32 81 38 81 56 C81 72 72 86 60 86 C48 86 39 72 39 56 Z" fill="url(#ifa-peau)" />
          {/* Racine des cheveux */}
          <path d="M37 54 C37 34 48 26 60 26 C72 26 83 34 83 54 C78 44 70 39 60 40 C50 39 42 44 37 54 Z" fill={cheveux} />
          {/* Sourcils */}
          <path d="M46 50 C49 47 53 47 56 49" fill="none" stroke={cheveux} strokeWidth="2.2" strokeLinecap="round" />
          <path d="M64 49 C67 47 71 47 74 50" fill="none" stroke={cheveux} strokeWidth="2.2" strokeLinecap="round" />
          {/* Yeux (clignement) */}
          <motion.g
            style={{ transformBox: 'fill-box', transformOrigin: 'center' }}
            animate={calme ? undefined : { scaleY: [1, 1, 0.08, 1, 1] }}
            transition={{ duration: 4.5, repeat: Infinity, times: [0, 0.9, 0.93, 0.96, 1] }}
          >
            <path d="M44.5 57 C47.5 52.4 54 52.4 57 57 C54 60.2 47.5 60.2 44.5 57 Z" fill="#fff" />
            <path d="M63 57 C66 52.4 72.5 52.4 75.5 57 C72.5 60.2 66 60.2 63 57 Z" fill="#fff" />
            <circle cx="50.8" cy="56.6" r="3.2" fill="#3a2016" />
            <circle cx="69.2" cy="56.6" r="3.2" fill="#3a2016" />
            <circle cx="50.8" cy="56.6" r="1.5" fill="#120a07" />
            <circle cx="69.2" cy="56.6" r="1.5" fill="#120a07" />
            <circle cx="52" cy="55.3" r="1.1" fill="#fff" />
            <circle cx="70.4" cy="55.3" r="1.1" fill="#fff" />
            <path d="M44.2 56.8 C47.5 52 54 52 57.3 56.4 M62.7 56.4 C66 52 72.5 52 75.8 56.8" fill="none" stroke="#120a07" strokeWidth="1.7" strokeLinecap="round" />
            <path d="M44.4 56.4 L42.4 54.6 M45.6 54.5 L44.2 52.5 M47.6 53.3 L46.9 51.2 M75.6 56.4 L77.6 54.6 M74.4 54.5 L75.8 52.5 M72.4 53.3 L73.1 51.2" stroke="#120a07" strokeWidth="1.1" strokeLinecap="round" />
          </motion.g>
          {/* Nez */}
          <path d="M58 60 C57.5 65 56 67 57.5 68.5 C59 69.3 61 69.3 62.5 68.5 C64 67 62.5 65 62 60" fill="none" stroke={peauOmbre} strokeWidth="1.6" strokeLinecap="round" />
          {/* Pommettes */}
          <circle cx="47" cy="66" r="4.5" fill="#c46a5a" opacity="0.28" />
          <circle cx="73" cy="66" r="4.5" fill="#c46a5a" opacity="0.28" />
          {/* Reflet sur l'arête du nez */}
          <ellipse cx="60" cy="63" rx="1.3" ry="3" fill="#a8714d" opacity="0.6" />
          {/* Sourire : lèvre supérieure, dents, lèvre inférieure (s'ouvre quand IFA « parle ») */}
          <path d="M50 72.4 C53 70.3 57 70 60 71.5 C63 70 67 70.3 70 72.4 C66 73.4 54 73.4 50 72.4 Z" fill="#6e2e2a" />
          <path d="M51 72.9 C55 76.4 65 76.4 69 72.9 C64.5 73.9 55.5 73.9 51 72.9 Z" fill="#fbf6f0" />
          <motion.path
            d="M51 72.9 C54 80 66 80 69 72.9 C65 77 55 77 51 72.9 Z"
            fill="#8e3f38"
            style={{ transformBox: 'fill-box', transformOrigin: 'top' }}
            animate={parle && !calme ? { scaleY: [1, 1.45, 0.95, 1.35, 1] } : { scaleY: 1 }}
            transition={parle ? { duration: 0.6, repeat: Infinity } : { duration: 0.2 }}
          />
          <path d="M49.3 71.6 C49.8 72.3 50.3 72.6 51 72.8 M70.7 71.6 C70.2 72.3 69.7 72.6 69 72.8" fill="none" stroke={peauOmbre} strokeWidth="1" strokeLinecap="round" />
          {/* Micro-casque doré */}
          <path d="M81 64 C85 71 82 79 73 80" fill="none" stroke="#C9A84C" strokeWidth="2" strokeLinecap="round" />
          <circle cx="72" cy="80" r="2.4" fill="#e3c979" />
        </motion.g>
      </g>
    </svg>
  )
}

import React from "react";
import { evolvePath } from "@remotion/paths";
import { OR, OR_CLAIR } from "../charte";
import { aleatoire, EXPO, lerp, p, TAU } from "./motion";

// ───────────────────────── Constellation des trois pitons (emblème YEBA) ─────────────────────────

/** Nœuds cibles (repère 1920 × 1080) : trois pitons triangulés + réseau intérieur. */
export const NOEUDS_PITONS: [number, number][] = [
  [700, 390], [470, 740], [930, 740], // piton gauche
  [960, 300], [690, 740], [1230, 740], // piton central
  [1220, 390], [990, 740], [1450, 740], // piton droit
  [640, 575], [775, 620], [868, 482], [960, 528], [1052, 482], [960, 652], [1145, 620], [1280, 575], [560, 690], [1360, 690],
];

export const LIENS_PITONS: [number, number][] = [
  [0, 1], [0, 2], [3, 4], [3, 5], [6, 7], [6, 8], [1, 8],
  [0, 9], [9, 17], [9, 10], [10, 11], [11, 3], [11, 12], [12, 13], [13, 3], [12, 14], [10, 14],
  [14, 15], [13, 15], [15, 16], [16, 6], [16, 18], [9, 11], [15, 13],
];

/** Positions « dispersées » initiales des nœuds (explosion depuis l'étincelle). */
export const noeudsDisperses = (graine = 11): [number, number][] => {
  const r = aleatoire(graine);
  return NOEUDS_PITONS.map(() => {
    const a = r() * TAU;
    const d = 260 + r() * 620;
    return [960 + Math.cos(a) * d * 1.45, Math.min(800, Math.max(150, 540 + Math.sin(a) * d * 0.8))];
  });
};

export const Constellation: React.FC<{
  positions: [number, number][];
  liens: [number, number][];
  progresLien: (i: number) => number;
  apparitionNoeud: (i: number) => number;
  epaisseur?: number;
  opacite?: number;
  lueur?: boolean;
}> = ({ positions, liens, progresLien, apparitionNoeud, epaisseur = 2.2, opacite = 1, lueur = true }) => (
  <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, opacity: opacite, overflow: "visible" }}>
    {lueur && (
      <defs>
        <filter id="lueur-or" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3.5" result="flou" />
          <feMerge>
            <feMergeNode in="flou" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
    )}
    <g filter={lueur ? "url(#lueur-or)" : undefined}>
      {liens.map(([a, b], i) => {
        const t = progresLien(i);
        if (t <= 0) return null;
        const [x1, y1] = positions[a];
        const [x2, y2] = positions[b];
        return (
          <line
            key={i}
            x1={x1}
            y1={y1}
            x2={lerp(x1, x2, t)}
            y2={lerp(y1, y2, t)}
            stroke={OR}
            strokeWidth={epaisseur}
            strokeLinecap="round"
            opacity={0.85}
          />
        );
      })}
      {positions.map(([x, y], i) => {
        const s = apparitionNoeud(i);
        if (s <= 0) return null;
        return <circle key={i} cx={x} cy={y} r={(i % 3 === 0 ? 8 : 6) * s} fill={i % 4 === 0 ? "#FFF6DA" : OR_CLAIR} />;
      })}
    </g>
  </svg>
);

// ───────────────────────── Baobab tracé au trait (repère 1000 × 1000) ─────────────────────────

export const BAOBAB_SOL = "M 150 930 L 850 930";
export const BAOBAB_TRONC = [
  "M 330 930 C 312 820 340 640 418 512",
  "M 670 930 C 688 820 660 640 582 512",
  "M 418 512 C 470 490 530 490 582 512",
  "M 330 930 C 300 924 268 932 236 930",
  "M 670 930 C 700 924 732 932 764 930",
];
export const BAOBAB_BRANCHES = [
  "M 424 508 C 372 478 312 466 246 476",
  "M 440 498 C 404 448 378 418 336 392",
  "M 478 492 C 470 444 458 404 440 362",
  "M 522 492 C 532 446 548 408 572 372",
  "M 560 498 C 598 452 630 426 668 404",
  "M 576 508 C 630 478 690 468 756 478",
];
export const BAOBAB_RAMEAUX = [
  "M 300 470 C 284 444 276 424 270 402", "M 246 476 L 208 456", "M 246 476 L 214 498",
  "M 380 420 C 360 404 342 398 318 402", "M 336 392 L 312 362",
  "M 452 400 C 474 378 488 364 496 342", "M 440 362 L 420 330",
  "M 548 408 C 528 384 518 370 512 350", "M 572 372 L 590 338",
  "M 624 428 C 640 404 650 388 656 366", "M 668 404 L 700 382",
  "M 700 470 C 718 446 732 430 742 410", "M 756 478 L 792 458", "M 756 478 L 786 500",
];
export const BAOBAB_ECORCE = [
  "M 430 905 C 420 800 440 690 470 600",
  "M 570 905 C 580 800 560 690 530 600",
  "M 500 905 C 500 800 500 700 500 610",
];
export const BAOBAB_FEUILLES: [number, number][] = [
  [270, 402], [208, 456], [214, 498], [318, 402], [312, 362], [496, 342], [420, 330],
  [512, 350], [590, 338], [656, 366], [700, 382], [742, 410], [792, 458], [786, 500],
  [246, 476], [336, 392], [440, 362], [572, 372], [668, 404], [756, 478],
];

const Trait: React.FC<{ d: string; t: number; couleur?: string; epaisseur?: number; opacite?: number }> = ({
  d,
  t,
  couleur = OR,
  epaisseur = 5,
  opacite = 1,
}) => {
  if (t <= 0) return null;
  const { strokeDasharray, strokeDashoffset } = evolvePath(Math.min(1, t), d);
  return (
    <path
      d={d}
      fill="none"
      stroke={couleur}
      strokeWidth={epaisseur}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={strokeDasharray}
      strokeDashoffset={strokeDashoffset}
      opacity={opacite}
    />
  );
};

/**
 * Baobab qui se dessine : sol → tronc → branches → rameaux → feuilles.
 * `f` est l'image courante, `debut` l'image où le tracé commence.
 */
export const BaobabTrace: React.FC<{
  f: number;
  debut: number;
  x: number;
  y: number;
  hauteur: number;
  vitesse?: number;
  opacite?: number;
  epaisseur?: number;
}> = ({ f, debut, x, y, hauteur, vitesse = 1, opacite = 1, epaisseur = 5 }) => {
  const k = 1 / vitesse;
  const t = (d: number, duree: number) => p(f, debut + d * k, duree * k, EXPO);
  const echelle = hauteur / 1000;
  return (
    <svg
      viewBox="0 0 1000 1000"
      width={hauteur}
      height={hauteur}
      style={{ position: "absolute", left: x - hauteur / 2, top: y - hauteur * 0.93, opacity: opacite, overflow: "visible" }}
    >
      <defs>
        <filter id="lueur-baobab" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation={6 / echelle} result="flou" />
          <feMerge>
            <feMergeNode in="flou" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g filter="url(#lueur-baobab)">
        <Trait d={BAOBAB_SOL} t={t(0, 40)} epaisseur={epaisseur * 0.7} opacite={0.7} />
        {BAOBAB_TRONC.map((d, i) => (
          <Trait key={`t${i}`} d={d} t={t(8 + i * 4, 46)} epaisseur={epaisseur * (i < 3 ? 1.3 : 0.8)} />
        ))}
        {BAOBAB_ECORCE.map((d, i) => (
          <Trait key={`e${i}`} d={d} t={t(40 + i * 6, 40)} epaisseur={epaisseur * 0.5} opacite={0.45} />
        ))}
        {BAOBAB_BRANCHES.map((d, i) => (
          <Trait key={`b${i}`} d={d} t={t(38 + i * 4, 40)} epaisseur={epaisseur * 1.05} />
        ))}
        {BAOBAB_RAMEAUX.map((d, i) => (
          <Trait key={`r${i}`} d={d} t={t(66 + i * 1.4, 22)} epaisseur={epaisseur * 0.65} />
        ))}
        {BAOBAB_FEUILLES.map(([cx, cy], i) => {
          const s = t(82 + (i % 14) * 1.8, 24);
          return s <= 0 ? null : (
            <circle key={`f${i}`} cx={cx} cy={cy} r={(i >= 14 ? 8 : 12) * s} fill={i % 3 === 0 ? OR_CLAIR : OR} />
          );
        })}
      </g>
    </svg>
  );
};

// ───────────────────────── Pictogrammes au trait (repère 100 × 100) ─────────────────────────

export const ICONES: Record<string, string[]> = {
  livre: [
    "M 50 28 C 40 22 24 20 12 22 L 12 78 C 24 76 40 78 50 84",
    "M 50 28 C 60 22 76 20 88 22 L 88 78 C 76 76 60 78 50 84",
    "M 50 28 L 50 84",
  ],
  reseau: [
    "M 22 30 L 50 50 L 78 30", "M 50 50 L 50 82", "M 22 30 L 22 70 L 50 82 L 78 70 L 78 30",
    "M 22 30 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0",
    "M 78 30 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0",
    "M 50 50 m -5 0 a 5 5 0 1 0 10 0 a 5 5 0 1 0 -10 0",
  ],
  bouclier: ["M 50 12 L 82 24 L 82 50 C 82 70 68 84 50 90 C 32 84 18 70 18 50 L 18 24 Z", "M 34 50 L 46 62 L 68 38"],
  soleil: ["M 50 30 m -18 0 a 18 18 0 1 0 36 0 a 18 18 0 1 0 -36 0"],
};

export const Icone: React.FC<{ nom: string; t: number; taille: number; couleur?: string; epaisseur?: number }> = ({
  nom,
  t,
  taille,
  couleur = OR,
  epaisseur = 3.2,
}) => (
  <svg viewBox="0 0 100 100" width={taille} height={taille} style={{ overflow: "visible" }}>
    {ICONES[nom].map((d, i) => (
      <Trait key={i} d={d} t={Math.max(0, Math.min(1, t * 1.25 - i * 0.12))} couleur={couleur} epaisseur={epaisseur} />
    ))}
  </svg>
);

/** Anneaux de sceau en pointillés qui tournent (périodiques si `boucle` > 0). */
export const AnneauxSceau: React.FC<{ f: number; x: number; y: number; rayon: number; boucle?: number; opacite?: number }> = ({
  f,
  x,
  y,
  rayon,
  boucle = 360,
  opacite = 0.5,
}) => {
  const anneaux = [
    { r: rayon, n: 72, sens: 1, ep: 2, o: 0.55 },
    { r: rayon * 0.82, n: 36, sens: -1, ep: 3, o: 0.4 },
    { r: rayon * 0.64, n: 120, sens: 1, ep: 1.5, o: 0.6 },
  ];
  return (
    <svg width={rayon * 2.4} height={rayon * 2.4} style={{ position: "absolute", left: x - rayon * 1.2, top: y - rayon * 1.2, opacity: opacite }}>
      {anneaux.map((a, i) => {
        const circ = TAU * a.r;
        const pas = circ / a.n;
        const rotation = (a.sens * (360 / a.n) * 2 * f) / boucle;
        return (
          <circle
            key={i}
            cx={rayon * 1.2}
            cy={rayon * 1.2}
            r={a.r}
            fill="none"
            stroke={OR}
            strokeWidth={a.ep}
            strokeDasharray={`${pas * 0.45} ${pas * 0.55}`}
            opacity={a.o}
            transform={`rotate(${rotation} ${rayon * 1.2} ${rayon * 1.2})`}
          />
        );
      })}
    </svg>
  );
};

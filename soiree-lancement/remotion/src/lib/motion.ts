import { Easing, interpolate } from "remotion";

// Courbes de la « bible » motion YEBA : entrées en expo-out, mouvements de caméra en quint-in-out.
export const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const QUINT = Easing.bezier(0.83, 0, 0.17, 1);
export const DOUX = Easing.bezier(0.45, 0, 0.55, 1);
export const ENTREE = Easing.bezier(0.55, 0, 1, 0.45);
export const TAU = Math.PI * 2;

/** Progression 0 → 1 entre `debut` et `debut + duree` (bornée). */
export const p = (f: number, debut: number, duree: number, easing = EXPO) =>
  interpolate(f, [debut, debut + duree], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Fenêtre d'opacité : apparaît sur `entree` images, disparaît sur `sortie` images. */
export const fenetre = (f: number, de: number, a: number, entree = 18, sortie = 18) =>
  Math.min(p(f, de, entree, DOUX), 1 - p(f, a - sortie, sortie, DOUX));

/** Générateur pseudo-aléatoire déterministe (mulberry32) : même rendu à chaque image. */
export const aleatoire = (graine: number) => {
  let s = graine >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** Impulsion douce centrée sur `centre` (largeur en images). */
export const impulsion = (f: number, centre: number, largeur: number) =>
  Math.exp(-((f - centre) ** 2) / (2 * largeur * largeur));

/** Secousse de caméra amortie après chaque impact. */
export const secousse = (f: number, impacts: { f: number; force: number }[]) => {
  let x = 0;
  let y = 0;
  for (const i of impacts) {
    const t = f - i.f;
    if (t < 0 || t > 20) continue;
    const amp = 9 * i.force * Math.exp(-t / 5);
    x += Math.sin(t * 2.7 + i.f) * amp;
    y += Math.cos(t * 3.1 + i.f) * amp * 0.7;
  }
  return { x, y };
};

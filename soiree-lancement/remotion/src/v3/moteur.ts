// Moteur du générique v3 « La graine » : particules en 3D, morphoses de formes, caméra continue (plan-séquence).
// Tout est fonction du temps t (secondes) : rendu identique à chaque image, quel que soit l'ordre de calcul.
import { noise3D } from "@remotion/noise";
import F from "./formes.json";
import T from "./timeline3.json";

export const W = 1920;
export const H = 1080;
export const CX = W / 2;
export const CY = H / 2;
export const FOCALE = 1500;
export type V3 = [number, number, number];

// ───────────────────────── formes ─────────────────────────
type Brute = { p: number[]; c: number[]; g: number[]; t: number[]; a: number[]; h?: number[] };
export type Forme = {
  p: Float32Array; c: Uint8Array; g: Uint8Array; t: Float32Array; a: Uint32Array; h?: Float32Array;
  bmin: V3; bmax: V3;
};
export const N: number = F.N;
export const PALETTE: [number, number, number][] = (F.palette as string[]).map((h) => [
  parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16),
]);

const decoder = (b: Brute): Forme => {
  const p = Float32Array.from(b.p);
  const bmin: V3 = [Infinity, Infinity, Infinity];
  const bmax: V3 = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < p.length; i += 3) {
    for (let k = 0; k < 3; k++) {
      bmin[k] = Math.min(bmin[k], p[i + k]);
      bmax[k] = Math.max(bmax[k], p[i + k]);
    }
  }
  return {
    p, c: Uint8Array.from(b.c), g: Uint8Array.from(b.g), t: Float32Array.from(b.t), a: Uint32Array.from(b.a),
    h: b.h ? Float32Array.from(b.h) : undefined, bmin, bmax,
  };
};
export const FORMES: Record<string, Forme> = Object.fromEntries(
  Object.entries(F.formes as unknown as Record<string, Brute>).map(([k, v]) => [k, decoder(v)])
);

// ───────────────────────── outils ─────────────────────────
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lisse = (x: number) => { const u = clamp(x); return u * u * (3 - 2 * u); };
export const entreeSortie = (x: number) => { const u = clamp(x); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
export const sortieExpo = (x: number) => { const u = clamp(x); return u >= 1 ? 1 : 1 - Math.pow(2, -10 * u); };
export const sortieCube = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
export const entreeCube = (x: number) => Math.pow(clamp(x), 3);
export const fenetre = (t: number, a: number, b: number, entree = 0.5, sortie = 0.45) =>
  Math.min(lisse((t - a) / entree), 1 - lisse((t - (b - sortie)) / sortie));
const fract = (x: number) => x - Math.floor(x);
const alea = (i: number, s: number) => fract(Math.sin(i * 127.1 + s * 311.7) * 43758.5453);
const ALEA1 = Float32Array.from({ length: N }, (_, i) => alea(i, 1));
const ALEA2 = Float32Array.from({ length: N }, (_, i) => alea(i, 2));
const ALEA3 = Float32Array.from({ length: N }, (_, i) => alea(i, 3));

const sub = (a: V3, b: V3): V3 => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a: V3, b: V3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a: V3): V3 => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
const lerp3 = (a: V3, b: V3, u: number): V3 => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];

// ───────────────────────── étapes (morphoses) ─────────────────────────
export type Etape = {
  forme: string; debut: number; duree: number; etalement?: number; tourbillon?: number; decalage: number[];
  inclinaison?: number[]; par_groupe?: boolean; origine?: string; implosion?: boolean; chute?: boolean;
  aligner_logo?: boolean; echelle?: number;
};
export const ETAPES = T.etapes as Etape[];

const rotation = (e: number[] = [0, 0, 0]) => {
  const [a, b, c] = e;
  const ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(b), sb = Math.sin(b), cc = Math.cos(c), sc = Math.sin(c);
  // R = Rz · Ry · Rx
  return [
    cb * cc, sa * sb * cc - ca * sc, ca * sb * cc + sa * sc,
    cb * sc, sa * sb * sc + ca * cc, ca * sb * sc - sa * cc,
    -sb, sa * cb, ca * cb,
  ];
};
const ROT = ETAPES.map((e) => rotation(e.inclinaison));

// Alignement final : l'emblème de particules se pose exactement sur l'emblème du logo officiel (fichier, jamais redessiné).
const EMB = F.meta.embleme.dans_logo as { logo_w: number; logo_h: number; x0: number; x1: number; y0: number; y1: number };
export const LOGO = {
  largeur: T.logo.largeur_px,
  haut: T.logo.haut_px,
  hauteur: (T.logo.largeur_px * EMB.logo_h) / EMB.logo_w,
  gauche: CX - T.logo.largeur_px / 2,
};
const sLogo = T.logo.largeur_px / EMB.logo_w;
const eX0 = LOGO.gauche + EMB.x0 * sLogo;
const eX1 = LOGO.gauche + EMB.x1 * sLogo;
const eY0 = LOGO.haut + EMB.y0 * sLogo;
const eY1 = LOGO.haut + EMB.y1 * sLogo;
const formeEmb = FORMES.embleme;
export const D_FINAL = (FOCALE * (formeEmb.bmax[0] - formeEmb.bmin[0])) / (eX1 - eX0);
const DECALAGE_EMBLEME: V3 = [
  ((eX0 + eX1) / 2 - CX) * (D_FINAL / FOCALE) - (formeEmb.bmin[0] + formeEmb.bmax[0]) / 2,
  -((eY0 + eY1) / 2 - CY) * (D_FINAL / FOCALE) - (formeEmb.bmin[1] + formeEmb.bmax[1]) / 2,
  0,
];

const VITESSE_ANNEAUX = [0.22, -0.16, 0.1, -0.07];
export const relief = (t: number) => entreeSortie((t - T.relief[0]) / (T.relief[1] - T.relief[0]));

/** Position (monde) du point i de l'étape e à l'instant t, avec la vie propre de chaque forme. */
const pointMonde = (k: number, i: number, t: number, out: V3) => {
  const e = ETAPES[k];
  const f = FORMES[e.forme];
  let x = f.p[3 * i], y = f.p[3 * i + 1], z = f.p[3 * i + 2];
  const s = e.echelle ?? 1;
  const dt = t - e.debut;
  switch (e.forme) {
    case "reseau": {
      const a = 0.05 * dt;
      const c = Math.cos(a), sn = Math.sin(a);
      [x, z] = [x * c + z * sn, -x * sn + z * c];
      break;
    }
    case "baobab": {
      const h = Math.max(0, y - 0.3);
      x += 0.035 * h * Math.sin(0.7 * t + 0.4 * z);
      break;
    }
    case "ile": {
      y += 1.7 * (f.h ? f.h[i] : 0) * relief(t);   // relief exagéré pour la lecture (pitons)
      break;
    }
    case "sceau": {
      const a = VITESSE_ANNEAUX[f.g[i]] * dt;
      const c = Math.cos(a), sn = Math.sin(a);
      [x, y] = [x * c - y * sn, x * sn + y * c];
      break;
    }
    case "graine": {
      const pouls = 1 + 0.9 * battement(t);
      x *= pouls; y *= pouls; z *= pouls;
      break;
    }
    default:
  }
  x *= s; y *= s; z *= s;
  if (e.inclinaison) {
    const r = ROT[k];
    [x, y, z] = [r[0] * x + r[1] * y + r[2] * z, r[3] * x + r[4] * y + r[5] * z, r[6] * x + r[7] * y + r[8] * z];
  }
  const d = e.aligner_logo ? DECALAGE_EMBLEME : e.decalage;
  // respiration : la matière n'est jamais figée
  const amp = e.forme === "embleme" ? 0.0 : 0.035;
  out[0] = x + d[0] + amp * noise3D("rx", i * 0.37, t * 0.35, 0);
  out[1] = y + d[1] + amp * noise3D("ry", i * 0.37, t * 0.35, 0);
  out[2] = z + d[2] + amp * noise3D("rz", i * 0.37, t * 0.35, 0);
};

/** Battement de cœur de la graine (pics doubles « lub-dub »). */
export const battement = (t: number) => {
  let v = 0;
  for (const b of T.son.battements) v += Math.exp(-Math.pow((t - b - 0.04) / 0.07, 2)) * (b % 1 > 0.2 && b % 1 < 0.4 ? 0.7 : 1);
  return v;
};

export const etapeCourante = (t: number) => {
  let k = 0;
  for (let j = 0; j < ETAPES.length; j++) if (ETAPES[j].debut <= t) k = j;
  return k;
};

// ───────────────────────── caméra ─────────────────────────
export type Camera = { oeil: V3; cible: V3; r: V3; u: V3; f: V3; focale: number; mise_au_point: number };

const cheminPos = (s: number): V3 => [
  3.0 * Math.sin(2 * Math.PI * 0.7 * s),
  -0.4 + 1.0 * s + 0.35 * Math.sin(4 * Math.PI * s),
  -34.0 * s,
];
export const sCamera = (t: number) => clamp(0.125 * (t - 42.52), 0, 0.96) * lisse((t - 41.6) / 1.4);
// Visée décalée à gauche du chemin : le chemin et ses jalons passent dans le tiers droit de l'image,
// les années (écrites à gauche) restent dégagées. Valeur vérifiée par la sonde de composition.
const VISEE_CHEMIN: V3 = [-2.7, 0.25, 0];

type Cle = { t: number; oeil: V3; cible: V3 };
const CLES: Cle[] = (() => {
  const out: Cle[] = [];
  const brutes = T.camera as { t: number; oeil?: number[]; cible?: number[]; chemin?: number; logo?: boolean }[];
  for (let j = 0; j < brutes.length; j++) {
    const c = brutes[j];
    if (c.chemin !== undefined) {
      const suiv = brutes[j + 1];
      if (suiv && suiv.chemin !== undefined) {
        for (let tt = c.t; tt < suiv.t; tt += 0.5) {
          const s = sCamera(tt);
          out.push({ t: tt, oeil: cheminPos(s).map((v, k) => v + [0.9, 1.3, 4.2][k]) as V3, cible: cheminPos(Math.min(1, s + 0.13)).map((v, k) => v + VISEE_CHEMIN[k]) as V3 });
        }
      } else {
        const s = sCamera(c.t);
        out.push({ t: c.t, oeil: cheminPos(s).map((v, k) => v + [0.9, 1.3, 4.2][k]) as V3, cible: cheminPos(Math.min(1, s + 0.13)).map((v, k) => v + VISEE_CHEMIN[k]) as V3 });
      }
    } else if (c.logo) {
      out.push({ t: c.t, oeil: [0, 0, D_FINAL], cible: [0, 0, 0] });
    } else {
      out.push({ t: c.t, oeil: c.oeil as V3, cible: c.cible as V3 });
    }
  }
  // la pose finale (alignée sur le logo) est tenue dès l'explosion de l'emblème
  const finale = out.findIndex((k) => k.t >= 74.2);
  if (finale >= 0) out[finale] = { t: out[finale].t, oeil: [0, 0, D_FINAL], cible: [0, 0, 0] };
  return out.sort((a, b) => a.t - b.t);
})();

const hermite = (t: number, cle: (k: Cle) => V3): V3 => {
  const n = CLES.length;
  if (t <= CLES[0].t) return cle(CLES[0]);
  if (t >= CLES[n - 1].t) return cle(CLES[n - 1]);
  let k = 0;
  while (k < n - 2 && CLES[k + 1].t <= t) k++;
  const a = CLES[k], b = CLES[k + 1];
  const h = b.t - a.t;
  const u = (t - a.t) / h;
  const pente = (j: number): V3 => {
    const p = CLES[Math.max(0, j - 1)], q = CLES[Math.min(n - 1, j + 1)];
    const d = q.t - p.t || 1;
    return sub(cle(q), cle(p)).map((v) => (0.8 * v) / d) as V3;
  };
  const ma = pente(k), mb = pente(k + 1);
  const u2 = u * u, u3 = u2 * u;
  const h00 = 2 * u3 - 3 * u2 + 1, h10 = u3 - 2 * u2 + u, h01 = -2 * u3 + 3 * u2, h11 = u3 - u2;
  const pa = cle(a), pb = cle(b);
  return [0, 1, 2].map((i) => h00 * pa[i] + h10 * h * ma[i] + h01 * pb[i] + h11 * h * mb[i]) as V3;
};

export const camera = (t: number): Camera => {
  const flottement = t < 74.2 ? 1 : 1 - lisse((t - 74.2) / 0.8);
  const oeil = hermite(t, (k) => k.oeil);
  oeil[0] += 0.05 * flottement * noise3D("cx", t * 0.18, 0, 0);
  oeil[1] += 0.04 * flottement * noise3D("cy", t * 0.18, 0, 0);
  const cible = hermite(t, (k) => k.cible);
  const f = norm(sub(cible, oeil));
  const r = norm(cross(f, [0, 1, 0]));
  const u = cross(r, f);
  return { oeil, cible, r, u, f, focale: FOCALE, mise_au_point: Math.hypot(...sub(cible, oeil)) };
};

/** Projection perspective : renvoie [x écran, y écran, profondeur] ou null derrière la caméra. */
export const projeter = (c: Camera, p: V3): V3 | null => {
  const d = sub(p, c.oeil);
  const z = dot(d, c.f);
  if (z < 0.25) return null;
  return [CX + (c.focale * dot(d, c.r)) / z, CY - (c.focale * dot(d, c.u)) / z, z];
};

// ───────────────────────── particules ─────────────────────────
export type Etat = {
  x: Float32Array; y: Float32Array; z: Float32Array; px: Float32Array; py: Float32Array;
  r: Float32Array; v: Float32Array; b: Float32Array; taille: Float32Array; alpha: Float32Array; visible: Uint8Array;
  k: number; u: number;
};
export const nouvelEtat = (): Etat => ({
  x: new Float32Array(N), y: new Float32Array(N), z: new Float32Array(N), px: new Float32Array(N), py: new Float32Array(N),
  r: new Float32Array(N), v: new Float32Array(N), b: new Float32Array(N), taille: new Float32Array(N),
  alpha: new Float32Array(N), visible: new Uint8Array(N), k: 0, u: 1,
});

const A: V3 = [0, 0, 0];
const B: V3 = [0, 0, 0];

/** Position monde + couleur + taille + éclat de la particule i à l'instant t. */
export type Sortie = { p: V3; ca: number; cb: number; m: number; taille: number; eclat: number };
export const particule = (i: number, t: number, out: Sortie) => {
  const k = etapeCourante(t);
  const e = ETAPES[k];
  const u = (t - e.debut) / e.duree;
  const fB = FORMES[e.forme];
  pointMonde(k, i, t, B);
  let eI = 1;
  if (k > 0 && u < 1) {
    pointMonde(k - 1, i, t, A);
    const etal = e.etalement ?? 0.4;
    const fB_g = fB.g[i];
    const cle = e.par_groupe ? clamp(0.72 * (fB_g / Math.max(1, groupesMax(e.forme))) + 0.28 * ALEA1[i]) : ALEA1[i];
    const ui = clamp((u - etal * cle) / (1 - etal));
    if (e.origine === "explosion") eI = sortieCube(ui);
    else if (e.implosion) eI = entreeCube(ui);
    else eI = entreeSortie(ui);
    if (e.chute) {
      // pluie de graines : horizontal en douceur, vertical en chute accélérée
      const eh = entreeSortie(ui), ev = Math.pow(ui, 1.8);
      out.p[0] = A[0] + (B[0] - A[0]) * eh;
      out.p[1] = A[1] + (B[1] - A[1]) * ev;
      out.p[2] = A[2] + (B[2] - A[2]) * eh;
    } else {
      out.p[0] = A[0] + (B[0] - A[0]) * eI;
      out.p[1] = A[1] + (B[1] - A[1]) * eI;
      out.p[2] = A[2] + (B[2] - A[2]) * eI;
    }
    const tour = (e.tourbillon ?? 1) * Math.sin(Math.PI * eI) * (0.55 + 0.9 * ALEA2[i]);
    out.p[0] += tour * noise3D("tx", i * 0.11, t * 0.3, k);
    out.p[1] += tour * noise3D("ty", i * 0.11, t * 0.3, k);
    out.p[2] += tour * 0.6 * noise3D("tz", i * 0.11, t * 0.3, k);
    const fA = FORMES[ETAPES[k - 1].forme];
    out.ca = fA.c[i];
    out.cb = fB.c[i];
    out.m = eI;
    out.taille = fA.t[i] + (fB.t[i] - fA.t[i]) * eI;
  } else {
    out.p[0] = B[0]; out.p[1] = B[1]; out.p[2] = B[2];
    out.ca = fB.c[i];
    out.cb = fB.c[i];
    out.m = 1;
    out.taille = fB.t[i];
  }
  out.eclat = eclat(i, t, k, eI);
  const fa = k > 0 && eI < 1 ? (TAILLE_FORME[ETAPES[k - 1].forme] ?? 1) : 1;
  const fb = TAILLE_FORME[e.forme] ?? 1;
  out.taille *= fa + (fb - fa) * eI;
};
const TAILLE_FORME: Record<string, number> = { yeba: 1.38, ile: 1.12, metiers: 1.15, embleme: 1.1 };

const GROUPES_MAX: Record<string, number> = {};
const groupesMax = (nom: string) => {
  if (GROUPES_MAX[nom] === undefined) GROUPES_MAX[nom] = FORMES[nom].g.reduce((m, g) => Math.max(m, g), 0);
  return GROUPES_MAX[nom];
};

const ETOILES = F.meta.etoiles as { famille: string; x: number; y: number }[];
const FAMILLES_T: Record<string, number> = Object.fromEntries(
  ((T.textes.find((x) => x.id === "formations") as { familles: { texte: string; t: number }[] }).familles).map((f) => [f.texte, f.t])
);
const VERBES_T = ((T.textes.find((x) => x.id === "verbes") as { verbes: { t: number }[] }).verbes).map((v) => v.t);
const JALONS_T = ((T.textes.find((x) => x.id === "j2021") as { jalons: { t: number }[] }).jalons).map((j) => j.t);

/** Éclat (multiplicateur de lumière) : graine qui naît, mots qui s'allument, étoiles qui scintillent… */
const eclat = (i: number, t: number, k: number, eI: number) => {
  const e = ETAPES[k];
  const f = FORMES[e.forme];
  const g = f.g[i];
  // graine : 2 000 points superposés → chacun très faible, sinon la graine sature en blanc
  const dense = (nom: string) => nom === "graine";
  const prev = k > 0 ? ETAPES[k - 1].forme : "graine";
  let base = 1;
  if (dense(e.forme) && k === 0) base = 0.03 * lisse((t - 0.4) / 0.9);
  else if (dense(prev) && eI < 1) base = 0.03 + 0.97 * lisse(eI * 1.4);
  else if (dense(e.forme)) base = 1 - 0.97 * lisse(eI);
  switch (e.forme) {
    case "yeba": {
      const choc = Math.exp(-Math.pow((t - 15.75) / 0.18, 2));
      base *= 1.25 * (1 + 0.9 * choc);
      break;
    }
    case "ile": {
      if (g === 1) base *= 1.7;
      break;
    }
    case "metiers": {
      const tv = VERBES_T[g] ?? 0;
      base *= t < tv ? 0.55 : 1 + 0.6 * Math.exp(-(t - tv) / 0.35);
      break;
    }
    case "etoiles": {
      const fam = ETOILES[g]?.famille ?? "";
      const tf = FAMILLES_T[fam] ?? 99;
      const scint = 0.85 + 0.25 * noise3D("sc", g * 3.1, t * 1.6, i * 0.01);
      if (g === 11) base *= 0.32 + 0.12 * Math.sin(t * 3);
      else base *= scint * (t < tf ? 0.75 : 1 + 0.7 * Math.exp(-(t - tf) / 0.4));
      break;
    }
    case "chemin": {
      if (g > 0) {
        const tj = JALONS_T[g - 1] ?? 99;
        base *= t < tj ? 0.7 : 1 + 0.9 * Math.exp(-(t - tj) / 0.5);
      }
      break;
    }
    case "embleme": {
      const [f0, f1] = T.logo.fondu;
      base *= 1 - 0.92 * lisse((t - f0) / (f1 - f0));
      break;
    }
    default:
  }
  return base;
};

// Poussières d'ambiance (bokeh) réparties dans tout le décor : donnent la profondeur quand la caméra bouge.
export const POUSSIERES = Array.from({ length: 1100 }, (_, j) => ({
  p: [-12 + 28 * alea(j, 11), -7 + 18 * alea(j, 12), -40 + 54 * alea(j, 13)] as V3,
  taille: 0.6 + 1.8 * alea(j, 14) ** 2,
  teinte: alea(j, 15) < 0.75 ? 0 : 3,
}));

export { cheminPos, ALEA3 };

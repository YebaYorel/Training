// Typographie du générique v3 : grands mots, révélés par masque, jamais traversés par un trait.
// Le même calcul de mise en page sert au rendu (DOM) et aux « réserves » découpées dans le calque des particules.
import React from "react";
import { BLANC, OR, OR_CLAIR } from "../charte";
import T from "./timeline3.json";
import { camera, clamp, fenetre, FORMES, lisse, projeter, sortieExpo, V3 } from "./moteur";

export const OR_POLI = `linear-gradient(180deg, #F6E7B0 0%, ${OR} 48%, #A8873A 100%)`;

type Style = { famille: "Montserrat" | "Inter"; poids: number; taille: number; interligne: number; couleur?: string; or?: boolean; espacement?: number };
export const STYLES: Record<string, Style> = {
  titre: { famille: "Montserrat", poids: 800, taille: 104, interligne: 1.08, couleur: BLANC },
  titre_or: { famille: "Montserrat", poids: 800, taille: 104, interligne: 1.08, or: true },
  geant: { famille: "Montserrat", poids: 900, taille: 300, interligne: 0.95, or: true },
  annee: { famille: "Montserrat", poids: 900, taille: 190, interligne: 1.0, or: true },
  compteur: { famille: "Montserrat", poids: 900, taille: 300, interligne: 0.92, or: true },
  sous_or: { famille: "Inter", poids: 600, taille: 64, interligne: 1.2, couleur: OR },
  sous: { famille: "Inter", poids: 600, taille: 60, interligne: 1.2, couleur: BLANC },
  prefixe: { famille: "Inter", poids: 600, taille: 52, interligne: 1.2, couleur: OR_CLAIR },
  verbe: { famille: "Montserrat", poids: 800, taille: 72, interligne: 1.1, couleur: BLANC },
  famille: { famille: "Inter", poids: 600, taille: 56, interligne: 1.25, couleur: BLANC },
  preuve: { famille: "Montserrat", poids: 800, taille: 88, interligne: 1.05, or: true },
  preuve1: { famille: "Inter", poids: 600, taille: 56, interligne: 1.2, couleur: BLANC },
  preuve2: { famille: "Inter", poids: 500, taille: 44, interligne: 1.25, couleur: "#D9DCE3" },
  slogan: { famille: "Montserrat", poids: 700, taille: 54, interligne: 1.25, couleur: BLANC },
  slogan_or: { famille: "Montserrat", poids: 700, taille: 54, interligne: 1.25, or: true },
  kicker: { famille: "Inter", poids: 600, taille: 44, interligne: 1.2, couleur: OR, espacement: 0.2 },
};

// ───────────── mesure (canvas, mêmes polices que le DOM) ─────────────
let ctxMesure: CanvasRenderingContext2D | null = null;
const cache = new Map<string, number>();
export const largeur = (texte: string, st: Style) => {
  const cle = `${st.famille}|${st.poids}|${st.taille}|${st.espacement ?? 0}|${texte}`;
  const v = cache.get(cle);
  if (v !== undefined) return v;
  if (!ctxMesure) ctxMesure = document.createElement("canvas").getContext("2d");
  const c = ctxMesure!;
  c.font = `${st.poids} ${st.taille}px ${st.famille}`;
  const w = c.measureText(texte).width + (st.espacement ?? 0) * st.taille * texte.length;
  cache.set(cle, w);
  return w;
};
export const viderMesures = () => cache.clear();

// ───────────── éléments posés à l'écran ─────────────
export type Element = {
  cle: string; texte: string; style: Style; x: number; y: number; w: number; h: number;
  apparition: number; opacite: number; montee: number; flou: number; puce?: string;
};
export type Boite = { x: number; y: number; w: number; h: number; a: number };

const entree = (t: number, t0: number) => {
  const p = sortieExpo((t - t0) / 0.8);
  return { p, opa: lisse((t - t0) / 0.35), flou: 10 * (1 - lisse((t - t0) / 0.45)) };
};

type Ligne = { texte: string; style: string; t: number; meme_ligne?: boolean };
type Cue = {
  id: string; t0: number; t1: number; x?: number; y?: number; align?: string; lignes?: Ligne[];
  verbes?: { texte: string; t: number; groupe: number }[];
  jalons?: { t: number; annee: string; texte: string; prefixe?: string }[];
  compteur?: [number, number, number];
  familles?: { texte: string; couleur: string; t: number }[];
  preuves?: { t: number; titre: string; ligne1: string; ligne2: string }[];
};
const CUES = T.textes as Cue[];

const sortie = (t: number, c: Cue) => 1 - lisse((t - (c.t1 - 0.45)) / 0.45);

const coupe = (texte: string, st: Style, max: number) => {
  // retour à la ligne entre mots (jamais au milieu d'un mot)
  const mots = texte.split(" ");
  const lignes: string[] = [];
  let cur = "";
  for (const m of mots) {
    const essai = cur ? `${cur} ${m}` : m;
    if (largeur(essai, st) <= max || !cur) cur = essai;
    else { lignes.push(cur); cur = m; }
  }
  if (cur) lignes.push(cur);
  return lignes;
};

/** Mise en page complète de l'instant t : liste d'éléments typographiques (position, état d'animation). */
export const miseEnPage = (t: number): Element[] => {
  const els: Element[] = [];
  const pousser = (cle: string, texte: string, sty: string | Style, x: number, y: number, t0: number, opaGlobale: number, align = "gauche", puce?: string) => {
    const st = typeof sty === "string" ? STYLES[sty] : sty;
    const w = largeur(texte, st) + (puce ? st.taille * 0.9 : 0);
    const h = st.taille * st.interligne;
    const xx = align === "centre" ? x - w / 2 : x;
    const a = entree(t, t0);
    if (t < t0 || opaGlobale <= 0.001) return h;
    els.push({ cle, texte, style: st, x: xx, y, w, h, apparition: a.p, opacite: a.opa * opaGlobale, montee: (1 - a.p) * 1.05, flou: a.flou, puce });
    return h;
  };

  for (const c of CUES) {
    if (t < c.t0 - 0.01 || t > c.t1 + 0.01) continue;
    const opa = sortie(t, c);
    const x = c.x ?? 132;
    let y = c.y ?? 400;
    const align = c.align ?? "gauche";

    if (c.lignes) {
      const memeLigne = c.lignes.filter((l) => l.meme_ligne);
      if (memeLigne.length) {
        const ws = memeLigne.map((l) => largeur(l.texte, STYLES[l.style]));
        const esp = 0.3 * STYLES[memeLigne[0].style].taille;
        const total = ws.reduce((s, v) => s + v, 0) + esp * (ws.length - 1);
        let xx = align === "centre" ? x - total / 2 : x;
        memeLigne.forEach((l, j) => {
          pousser(`${c.id}-${j}`, l.texte, l.style, xx, y, l.t, opa);
          xx += ws[j] + esp;
        });
        y += STYLES[memeLigne[0].style].taille * STYLES[memeLigne[0].style].interligne;
      }
      let yy = y;
      if (c.compteur) {
        const [a, b, n] = c.compteur;
        const v = Math.round(n * clamp((t - a) / (b - a)));
        const st = STYLES.compteur;
        if (t >= a) {
          const ent = entree(t, a);
          els.push({ cle: `${c.id}-n`, texte: String(v), style: st, x, y: yy, w: largeur("11", st), h: st.taille * st.interligne, apparition: ent.p, opacite: ent.opa * opa, montee: (1 - ent.p) * 1.05, flou: ent.flou });
        }
        yy += st.taille * st.interligne;
      }
      c.lignes.filter((l) => !l.meme_ligne).forEach((l, j) => {
        yy += pousser(`${c.id}-${j}`, l.texte, l.style, x, yy, l.t, opa, align);
      });
      if (c.familles) {
        yy += 26;
        c.familles.forEach((f, j) => {
          yy += pousser(`${c.id}-f${j}`, f.texte, "famille", x, yy, f.t, opa, "gauche", `#${f.couleur}`);
        });
      }
      if (c.preuves) {
        yy += 44;
        c.preuves.forEach((p, j) => {
          if (t < p.t) return;
          yy += pousser(`${c.id}-p${j}t`, p.titre, "preuve", x, yy, p.t, opa);
          yy += pousser(`${c.id}-p${j}a`, p.ligne1, "preuve1", x, yy, p.t + 0.15, opa);
          for (const [m, morceau] of coupe(p.ligne2, STYLES.preuve2, 760).entries()) {
            yy += pousser(`${c.id}-p${j}b${m}`, morceau, "preuve2", x, yy, p.t + 0.3 + 0.08 * m, opa);
          }
          yy += 34;
        });
      }
    }

    if (c.verbes) {
      const cam = camera(t);
      const f = FORMES.metiers;
      let ymin = Infinity;
      for (let i = 0; i < f.g.length; i++) ymin = Math.min(ymin, f.p[3 * i + 1]);
      c.verbes.forEach((v) => {
        // centre du pictogramme (groupe) projeté à l'écran : le verbe suit la caméra, même ligne de base pour les trois
        let sx = 0, n = 0;
        for (let i = 0; i < f.g.length; i += 7) {
          if (f.g[i] !== v.groupe) continue;
          sx += f.p[3 * i]; n++;
        }
        const dec = (T.etapes.find((e) => e.forme === "metiers")!.decalage) as number[];
        const p = projeter(cam, [sx / n + dec[0], ymin + dec[1] - 0.55, dec[2]] as V3);
        if (!p) return;
        pousser(`${c.id}-${v.groupe}`, v.texte, "verbe", p[0], p[1], v.t, opa, "centre");
      });
    }

    if (c.jalons) {
      // jalon courant : l'année « roule » d'un jalon au suivant (odomètre)
      let j = -1;
      c.jalons.forEach((jl, q) => { if (t >= jl.t) j = q; });
      if (j < 0) continue;
      const jl = c.jalons[j];
      const prec = j > 0 ? c.jalons[j - 1] : null;
      const p = sortieExpo((t - jl.t) / 0.7);
      const stA = STYLES.annee;
      let yy = y;
      if (jl.prefixe) {
        yy += pousser(`${c.id}-pre${j}`, jl.prefixe, "prefixe", x, yy, jl.t, opa);
      } else {
        yy += STYLES.prefixe.taille * STYLES.prefixe.interligne;
      }
      const hA = stA.taille * stA.interligne;
      const wA = Math.max(largeur(jl.annee, stA), prec ? largeur(prec.annee, stA) : 0);
      if (prec && p < 1) {
        els.push({ cle: `${c.id}-a${j - 1}`, texte: prec.annee, style: stA, x, y: yy, w: wA, h: hA, apparition: 1, opacite: opa * (1 - lisse(p * 1.6)), montee: -0.9 * p, flou: 6 * p });
      }
      els.push({ cle: `${c.id}-a${j}`, texte: jl.annee, style: stA, x, y: yy, w: wA, h: hA, apparition: p, opacite: opa * lisse(p * 1.4), montee: prec ? 0.9 * (1 - p) : (1 - p) * 1.05, flou: 8 * (1 - p) });
      yy += hA + 8;
      pousser(`${c.id}-l${j}`, jl.texte, "sous", x, yy, jl.t + 0.18, opa);
    }
  }
  return els;
};

/** Réserves (zones interdites aux particules et aux traits) : boîtes des textes visibles, marges comprises. */
export const reserves = (els: Element[]): Boite[] =>
  els
    .filter((e) => e.opacite > 0.01)
    .map((e) => {
      const m = Math.max(18, e.style.taille * 0.22);
      return { x: e.x - m, y: e.y - m * 0.6, w: e.w + 2 * m, h: e.h + m * 1.2, a: clamp(e.opacite * 1.4) };
    });

export const Typo: React.FC<{ els: Element[] }> = ({ els }) => (
  <>
    {els.map((e) => {
      const st = e.style;
      const rempli: React.CSSProperties = st.or
        ? { backgroundImage: OR_POLI, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }
        : { color: st.couleur };
      return (
        <div key={e.cle} style={{ position: "absolute", left: e.x, top: e.y, height: e.h, overflow: "hidden", whiteSpace: "nowrap", opacity: e.opacite }}>
          <div
            style={{
              transform: `translateY(${e.montee * 100}%)`,
              filter: e.flou > 0.05 ? `blur(${e.flou}px)` : undefined,
              fontFamily: `${st.famille}, sans-serif`,
              fontWeight: st.poids,
              fontSize: st.taille,
              lineHeight: `${e.h}px`,
              letterSpacing: st.espacement ? `${st.espacement}em` : st.taille > 150 ? "-0.02em" : "-0.005em",
              fontFeatureSettings: '"tnum" 1',
              display: "flex",
              alignItems: "center",
              gap: st.taille * 0.35,
            }}
          >
            {e.puce && <span style={{ width: st.taille * 0.36, height: st.taille * 0.36, borderRadius: "50%", background: e.puce, boxShadow: `0 0 ${st.taille * 0.4}px ${e.puce}`, flex: "none" }} />}
            <span style={rempli}>{e.texte}</span>
          </div>
        </div>
      );
    })}
  </>
);

export const fenetreLogo = (t: number) => fenetre(t, T.logo.fondu[0], 999, T.logo.fondu[1] - T.logo.fondu[0], 0.1);

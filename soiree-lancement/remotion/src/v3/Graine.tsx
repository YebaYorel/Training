// Générique v3 « La graine » — plan-séquence de 80 s : une graine de lumière devient réseau, YEBA, baobab,
// La Réunion (974), chemin, 3 métiers, 11 formations, sceau de confiance, puis l'emblème officiel.
import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { AbsoluteFill, Audio, continueRender, delayRender, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Grain, Vignette } from "../lib/calques";
import {
  camera, Camera, CX, CY, D_FINAL, ETAPES, etapeCourante, fenetre, FORMES, H, LOGO, lisse, N, PALETTE, particule,
  POUSSIERES, projeter, Sortie, V3, W,
} from "./moteur";
import { Boite, fenetreLogo, miseEnPage, reserves, Typo, viderMesures } from "./textes";
import T from "./timeline3.json";

// ───────────── polices locales (aucun appel réseau) ─────────────
const FONTES: [string, number, string][] = [
  ["Montserrat", 700, "montserrat-latin-700-normal.woff2"], ["Montserrat", 800, "montserrat-latin-800-normal.woff2"],
  ["Montserrat", 900, "montserrat-latin-900-normal.woff2"], ["Inter", 500, "inter-latin-500-normal.woff2"],
  ["Inter", 600, "inter-latin-600-normal.woff2"], ["Inter", 700, "inter-latin-700-normal.woff2"],
];
const CSS_FONTES = FONTES.map(([f, w, fichier]) => `@font-face{font-family:${f};font-weight:${w};src:url(${staticFile(`fonts/${fichier}`)}) format('woff2');}`).join("");
const useFontes = () => {
  const [pret, setPret] = useState(false);
  const [poignee] = useState(() => delayRender("Polices v3"));
  useEffect(() => {
    Promise.all(FONTES.map(([f, w]) => document.fonts.load(`${w} 48px ${f}`)))
      .then(() => { viderMesures(); setPret(true); continueRender(poignee); })
      .catch(() => { setPret(true); continueRender(poignee); });
  }, [poignee]);
  return pret;
};

// ───────────── lutins lumineux (un par couleur de palette) ─────────────
let LUTINS: HTMLCanvasElement[] | null = null;
const lutins = () => {
  if (LUTINS) return LUTINS;
  LUTINS = PALETTE.map(([r, g, b]) => {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const x = c.getContext("2d")!;
    const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    const blanc = (k: number) => `rgba(${Math.round(r + (255 - r) * k)},${Math.round(g + (255 - g) * k)},${Math.round(b + (255 - b) * k)},`;
    gr.addColorStop(0, `${blanc(0.75)}1)`);
    gr.addColorStop(0.1, `${blanc(0.3)}0.95)`);
    gr.addColorStop(0.24, `rgba(${r},${g},${b},0.42)`);
    gr.addColorStop(0.5, `rgba(${r},${g},${b},0.1)`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    x.fillStyle = gr;
    x.fillRect(0, 0, 64, 64);
    return c;
  });
  return LUTINS;
};

const sortieVide = (): Sortie => ({ p: [0, 0, 0], ca: 0, cb: 0, m: 1, taille: 1, eclat: 1 });
const S1 = sortieVide();
const S0 = sortieVide();
const ECRAN_X = new Float32Array(N);
const ECRAN_Y = new Float32Array(N);
const ECRAN_A = new Float32Array(N);

const OR_RVB = "201,171,76";

/** Dessine le monde (poussières, liens, particules, traînées) puis découpe les réserves des textes. */
const dessiner = (ctx: CanvasRenderingContext2D, t: number, cam: Camera, trous: Boite[], dt: number) => {
  const L = lutins();
  ctx.clearRect(0, 0, W, H);
  ctx.globalCompositeOperation = "lighter";
  const fo = cam.mise_au_point;

  // 1. poussières d'ambiance (bokeh)
  for (const m of POUSSIERES) {
    const q = projeter(cam, m.p);
    if (!q || q[0] < -80 || q[0] > W + 80 || q[1] < -80 || q[1] > H + 80) continue;
    const flou = Math.abs(q[2] - fo) / fo;
    const d = Math.min(140, (m.taille * 95) / q[2] * (1 + 2.2 * flou * flou));
    ctx.globalAlpha = Math.min(0.28, 0.5 / (1 + 5 * flou * flou)) * lisse((t - 0.2) / 2);
    ctx.drawImage(L[m.teinte], q[0] - d / 2, q[1] - d / 2, d, d);
  }

  // 2. particules : position écran, traînées de vitesse, lutins
  const k = etapeCourante(t);
  const traines: Path2D[] = PALETTE.map(() => new Path2D());
  for (let i = 0; i < N; i++) {
    particule(i, t, S1);
    const q = projeter(cam, S1.p);
    if (!q) { ECRAN_A[i] = 0; continue; }
    const flou = Math.abs(q[2] - fo) / fo;
    const diam = Math.min(90, (S1.taille * 130) / q[2] * (1 + 2.5 * flou * flou));
    const alpha = Math.min(1, S1.eclat) / (1 + 5 * flou * flou);
    ECRAN_X[i] = q[0]; ECRAN_Y[i] = q[1]; ECRAN_A[i] = alpha;
    if (q[0] < -100 || q[0] > W + 100 || q[1] < -100 || q[1] > H + 100 || alpha < 0.004) continue;
    // traînée : position un instant plus tôt (flou de mouvement)
    particule(i, t - dt * 1.6, S0);
    const q0 = projeter(cam, S0.p);
    if (q0) {
      const dx = q[0] - q0[0], dy = q[1] - q0[1];
      if (dx * dx + dy * dy > 16) {
        const c = S1.m > 0.5 ? S1.cb : S1.ca;
        traines[c].moveTo(q0[0], q0[1]);
        traines[c].lineTo(q[0], q[1]);
      }
    }
    const surplus = Math.max(1, S1.eclat);
    if (S1.ca === S1.cb || S1.m >= 0.98) {
      ctx.globalAlpha = Math.min(1, alpha * surplus);
      ctx.drawImage(L[S1.cb], q[0] - diam / 2, q[1] - diam / 2, diam, diam);
    } else {
      ctx.globalAlpha = Math.min(1, alpha * surplus * (1 - S1.m));
      ctx.drawImage(L[S1.ca], q[0] - diam / 2, q[1] - diam / 2, diam, diam);
      ctx.globalAlpha = Math.min(1, alpha * surplus * S1.m);
      ctx.drawImage(L[S1.cb], q[0] - diam / 2, q[1] - diam / 2, diam, diam);
    }
  }
  ctx.lineCap = "round";
  ctx.lineWidth = 1.6;
  ctx.globalAlpha = 0.42;
  traines.forEach((p, c) => {
    const [r, g, b] = PALETTE[c];
    ctx.strokeStyle = `rgb(${r},${g},${b})`;
    ctx.stroke(p);
  });

  // 3. liens (constellations) : la forme courante apparaît quand elle est posée, la précédente s'efface au départ
  const liens = (kk: number, force: number) => {
    if (force <= 0.01 || kk < 0) return;
    const a = FORMES[ETAPES[kk].forme].a;
    const seaux = [new Path2D(), new Path2D(), new Path2D()];
    for (let j = 0; j < a.length; j += 2) {
      const p = a[j], q = a[j + 1];
      const al = Math.min(ECRAN_A[p], ECRAN_A[q]);
      if (al < 0.05) continue;
      const dx = ECRAN_X[p] - ECRAN_X[q], dy = ECRAN_Y[p] - ECRAN_Y[q];
      if (dx * dx + dy * dy > 220 * 220) continue;
      const s = al > 0.66 ? 2 : al > 0.33 ? 1 : 0;
      seaux[s].moveTo(ECRAN_X[p], ECRAN_Y[p]);
      seaux[s].lineTo(ECRAN_X[q], ECRAN_Y[q]);
    }
    ctx.lineWidth = 1.25;
    ctx.strokeStyle = `rgb(${OR_RVB})`;
    seaux.forEach((p, s) => { ctx.globalAlpha = force * [0.14, 0.3, 0.46][s]; ctx.stroke(p); });
  };
  const e = ETAPES[k];
  const u = (t - e.debut) / e.duree;
  const suiv = ETAPES[k + 1];
  const finSuivante = suiv ? 1 - lisse((t - suiv.debut) / 0.4) : 1;
  liens(k, lisse((u - 0.72) / 0.45) * finSuivante * (e.forme === "embleme" ? 1 - lisse((t - T.logo.fondu[0]) / 0.6) : 1));
  if (k > 0 && u < 0.35) liens(k - 1, 1 - lisse(u / 0.3));

  // 4. graine : halo, battements, ondes de choc
  const centre = projeter(cam, [0, 0, 0] as V3);
  if (centre) {
    const graineVisible = Math.max(fenetre(t, 0.4, 5.6, 0.8, 1.2), fenetre(t, 73.0, 74.9, 0.8, 0.5));
    if (graineVisible > 0.01) {
      const pouls = 1 + 0.6 * T.son.battements.reduce((v, b) => v + Math.exp(-Math.pow((t - b - 0.04) / 0.09, 2)), 0);
      const R = 110 * pouls * (FOCALE_REF / Math.max(1, cam.mise_au_point));
      const g = ctx.createRadialGradient(centre[0], centre[1], 0, centre[0], centre[1], R);
      g.addColorStop(0, `rgba(255,244,214,${0.95 * graineVisible})`);
      g.addColorStop(0.08, `rgba(246,231,176,${0.8 * graineVisible})`);
      g.addColorStop(0.3, `rgba(${OR_RVB},${0.22 * graineVisible})`);
      g.addColorStop(1, "rgba(201,171,76,0)");
      ctx.globalAlpha = 1;
      ctx.fillStyle = g;
      ctx.fillRect(centre[0] - R, centre[1] - R, 2 * R, 2 * R);
      // étoile à quatre branches (aucun texte à l'écran pendant la graine ; les réserves l'effaceraient sinon)
      for (const [dx, dy, L] of [[1, 0, 2.6], [0, 1, 1.6]] as [number, number, number][]) {
        const lg = ctx.createLinearGradient(centre[0] - dx * R * L, centre[1] - dy * R * L, centre[0] + dx * R * L, centre[1] + dy * R * L);
        lg.addColorStop(0, "rgba(246,231,176,0)");
        lg.addColorStop(0.5, `rgba(255,248,226,${0.75 * graineVisible})`);
        lg.addColorStop(1, "rgba(246,231,176,0)");
        ctx.fillStyle = lg;
        const ep = 3 * pouls;
        ctx.fillRect(centre[0] - dx * R * L - dy * ep / 2, centre[1] - dy * R * L - dx * ep / 2, dx * 2 * R * L + dy * ep, dy * 2 * R * L + dx * ep);
      }
    }
    for (const [t0, force] of [[T.son.anneau, 0.55], [ETAPES[1].debut, 1], [74.25, 1]] as [number, number][]) {
      const v = (t - t0) / 1.4;
      if (v <= 0 || v >= 1) continue;
      ctx.globalAlpha = (1 - v) * 0.55 * force;
      ctx.strokeStyle = `rgb(246,231,176)`;
      ctx.lineWidth = 2 + 6 * (1 - v);
      ctx.beginPath();
      ctx.arc(centre[0], centre[1], 30 + v * 900 * force, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  // 5. halo lumineux (bloom) : copie floutée à mi-résolution, ajoutée en lumière
  if (!BLOOM) { BLOOM = document.createElement("canvas"); BLOOM.width = W / 2; BLOOM.height = H / 2; }
  const bc = BLOOM.getContext("2d")!;
  bc.globalCompositeOperation = "copy";
  bc.filter = "blur(7px)";
  bc.drawImage(ctx.canvas, 0, 0, W / 2, H / 2);
  bc.filter = "none";
  ctx.globalCompositeOperation = "lighter";
  ctx.globalAlpha = 0.55;
  ctx.drawImage(BLOOM, 0, 0, W, H);

  // 6. réserves : aucune particule, aucun trait, aucune onde sous un mot (bords fondus)
  ctx.globalCompositeOperation = "destination-out";
  ctx.fillStyle = "#000";
  // halo d'effacement progressif (flou gaussien) : aucune coupure nette visible autour d'un mot
  ctx.filter = "blur(10px)";
  for (const b of trous) {
    ctx.globalAlpha = b.a;
    ctx.beginPath();
    ctx.roundRect(b.x - 12, b.y - 12, b.w + 24, b.h + 24, 40);
    ctx.fill();
  }
  ctx.filter = "none";
  // cœur : effacement total sous le mot et sa marge
  for (const b of trous) {
    ctx.globalAlpha = b.a;
    ctx.beginPath();
    ctx.roundRect(b.x, b.y, b.w, b.h, 28);
    ctx.fill();
  }
  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
};
const FOCALE_REF = 4.0;
let BLOOM: HTMLCanvasElement | null = null;

// ───────────── fond : nuit profonde, teintes d'ambiance, lumière derrière le sujet ─────────────
type Ambiance = { t: number; haut: number[]; bas: number[]; halo: number[]; force: number };
const AMB: Ambiance[] = [
  { t: 0, haut: [7, 7, 10], bas: [7, 7, 10], halo: [201, 171, 76], force: 0.0 },
  { t: 5, haut: [8, 12, 24], bas: [8, 8, 12], halo: [79, 127, 196], force: 0.22 },
  { t: 13, haut: [10, 9, 8], bas: [9, 8, 7], halo: [201, 171, 76], force: 0.3 },
  { t: 21, haut: [16, 11, 7], bas: [22, 14, 8], halo: [201, 140, 60], force: 0.32 },
  { t: 31, haut: [7, 14, 26], bas: [10, 10, 14], halo: [79, 127, 196], force: 0.26 },
  { t: 42, haut: [12, 10, 8], bas: [8, 8, 11], halo: [201, 171, 76], force: 0.24 },
  { t: 51, haut: [8, 10, 16], bas: [8, 8, 11], halo: [201, 171, 76], force: 0.22 },
  { t: 58.5, haut: [7, 12, 26], bas: [8, 9, 14], halo: [127, 167, 224], force: 0.24 },
  { t: 66.3, haut: [9, 20, 40], bas: [8, 12, 22], halo: [201, 171, 76], force: 0.28 },
  { t: 73.5, haut: [8, 8, 11], bas: [8, 8, 11], halo: [201, 171, 76], force: 0.42 },
  { t: 80, haut: [8, 8, 11], bas: [8, 8, 11], halo: [201, 171, 76], force: 0.42 },
];
const ambiance = (t: number) => {
  let j = 0;
  while (j < AMB.length - 2 && AMB[j + 1].t <= t) j++;
  const a = AMB[j], b = AMB[j + 1];
  const u = lisse((t - a.t) / Math.max(0.01, b.t - a.t) * 1.0);
  const mix = (x: number[], y: number[]) => x.map((v, i) => Math.round(v + (y[i] - v) * u));
  return { haut: mix(a.haut, b.haut), bas: mix(a.bas, b.bas), halo: mix(a.halo, b.halo), force: a.force + (b.force - a.force) * u };
};

const centreSujet = (t: number, cam: Camera) => {
  const k = etapeCourante(t);
  const e = ETAPES[k];
  const f = FORMES[e.forme];
  const ech = e.echelle ?? 1;
  const c: V3 = [0, 1, 2].map((i) => ((f.bmin[i] + f.bmax[i]) / 2) * ech + (e.decalage[i] ?? 0)) as V3;
  if (e.forme === "chemin") return [CX + 400, CY * 0.9]; // le chemin passe dans le tiers droit (VISEE_CHEMIN)
  if (e.aligner_logo) return [CX, LOGO.haut + 170];
  const q = projeter(cam, c);
  return q ? [q[0], q[1]] : [CX, CY];
};

export const GeneriqueV3: React.FC<{ avecSon?: boolean }> = ({ avecSon = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pret = useFontes();
  const ref = useRef<HTMLCanvasElement>(null);
  const cam = useMemo(() => camera(t), [t]);
  const els = useMemo(() => (pret ? miseEnPage(t) : []), [pret, t]);
  const trous = useMemo(() => reserves(els), [els]);

  useLayoutEffect(() => {
    const c = ref.current;
    if (!c || !pret) return;
    dessiner(c.getContext("2d")!, t, cam, trous, 1 / fps);
  }, [t, cam, trous, pret, fps]);

  const amb = ambiance(t);
  const [hx, hy] = centreSujet(t, cam);
  const logoA = fenetreLogo(t);
  const final = lisse((t - 76) / 4);
  const eclair = (t0: number, d = 0.5) => Math.exp(-Math.pow((t - t0) / d, 2));
  const flash = Math.max(eclair(4.5, 0.18) * 0.35, eclair(15.75, 0.16) * 0.45, eclair(74.25, 0.2) * 0.6);
  // le reflet horizontal ne passe jamais sur un mot : ni texte à l'écran, ni mot formé de particules (YEBA)
  const reflet = Math.max(eclair(4.5, 0.18) * 0.35, eclair(74.25, 0.2) * 0.6);
  // reflets horizontaux : seulement quand AUCUN texte n'est à l'écran (règle : aucun trait ne traverse un mot)
  const sansTexte = els.length === 0;

  return (
    <AbsoluteFill style={{ background: "#07070A", overflow: "hidden" }}>
      <style>{CSS_FONTES}</style>
      {avecSon && <Audio src={staticFile("audio/generique-v3.wav")} />}
      <AbsoluteFill style={{ transform: `scale(${1 + 0.035 * final})`, transformOrigin: `${CX}px ${LOGO.haut + 260}px` }}>
        <AbsoluteFill
          style={{
            background: [
              `radial-gradient(ellipse 46% 52% at ${hx}px ${hy}px, rgba(${amb.halo.join(",")},${amb.force}) 0%, rgba(${amb.halo.join(",")},0) 70%)`,
              `radial-gradient(ellipse 80% 70% at 18% 8%, rgba(${amb.haut.map((v) => v * 2).join(",")},0.9) 0%, rgba(0,0,0,0) 70%)`,
              `linear-gradient(180deg, rgb(${amb.haut.join(",")}) 0%, rgb(${amb.bas.join(",")}) 100%)`,
            ].join(","),
          }}
        />
        <canvas ref={ref} width={W} height={H} style={{ position: "absolute", left: 0, top: 0, width: W, height: H }} />
        {logoA > 0.001 && (
          <>
            <div style={{ position: "absolute", left: CX - 520, top: LOGO.haut - 140, width: 1040, height: 760, opacity: logoA * 0.85,
              background: "radial-gradient(ellipse 50% 50% at 50% 45%, rgba(201,171,76,0.22) 0%, rgba(201,171,76,0) 70%)" }} />
            <Img src={staticFile("logo-yeba-fond-sombre.png")} style={{ position: "absolute", left: LOGO.gauche, top: LOGO.haut, width: LOGO.largeur, opacity: logoA }} />
          </>
        )}
        <Typo els={els} />
      </AbsoluteFill>
      {flash > 0.01 && <AbsoluteFill style={{ background: `radial-gradient(ellipse 60% 50% at 50% 50%, rgba(255,240,205,${flash}) 0%, rgba(255,240,205,0) 70%)`, mixBlendMode: "screen" }} />}
      {sansTexte && reflet > 0.05 && (
        <div style={{ position: "absolute", left: 0, top: CY - 3, width: W, height: 6, opacity: reflet,
          background: "linear-gradient(90deg, rgba(246,231,176,0) 0%, rgba(246,231,176,0.9) 50%, rgba(246,231,176,0) 100%)", filter: "blur(2px)" }} />
      )}
      <Grain opacite={0.1} />
      <Vignette force={0.58} />
      <div style={{ display: "none" }}>{D_FINAL.toFixed(2)}</div>
    </AbsoluteFill>
  );
};

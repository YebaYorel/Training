// Fonds vivants v3 du PowerPoint (boucles parfaites de 12 s) et pré-générique v3 : même matière que le générique.
// Règle de composition : le sujet (baobab, réseau, sceau) occupe une zone que la slide laisse VIDE de texte ;
// partout ailleurs, seulement des poussières floues (aucun trait derrière un mot).
import { noise3D } from "@remotion/noise";
import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, Img, staticFile, useCurrentFrame } from "remotion";
import { Grain, Vignette } from "../lib/calques";
import { FORMES, N, PALETTE, V3 } from "./moteur";

const W = 1920;
const H = 1080;
const FOC = 1500;

type Preset = {
  teinte: "noir" | "bleu" | "terre"; sujet?: string; ecran?: [number, number]; hauteur_px?: number;
  inclinaison?: [number, number, number]; graine?: [number, number]; halo: [number, number]; force: number;
};
export const PRESETS: Record<string, Preset> = {
  nuit: { teinte: "noir", halo: [0.72, 0.42], force: 0.16 },
  "nuit-bleu": { teinte: "bleu", halo: [0.7, 0.45], force: 0.2 },
  "nuit-terre": { teinte: "terre", halo: [0.3, 0.6], force: 0.2 },
  graine: { teinte: "noir", graine: [960, 300], halo: [0.5, 0.28], force: 0.2 },
  baobab: { teinte: "terre", sujet: "baobab", ecran: [1455, 575], hauteur_px: 860, halo: [0.76, 0.5], force: 0.26 },
  reseau: { teinte: "bleu", sujet: "reseau", ecran: [1470, 540], hauteur_px: 820, halo: [0.77, 0.5], force: 0.22 },
  sceau: { teinte: "bleu", sujet: "sceau", ecran: [1440, 565], hauteur_px: 660, inclinaison: [0.2, -0.45, 0], halo: [0.75, 0.52], force: 0.26 },
};
const FONDS: Record<string, [string, string]> = {
  noir: ["#0C0C10", "#07070A"],
  bleu: ["#0F2346", "#07080E"],
  terre: ["#1C130C", "#0A0806"],
};

const fract = (x: number) => x - Math.floor(x);
const alea = (i: number, s: number) => fract(Math.sin(i * 127.1 + s * 311.7) * 43758.5453);
const POUSSIERES = Array.from({ length: 170 }, (_, j) => ({
  x: alea(j, 1) * W, y: alea(j, 2) * H, prof: 0.25 + 0.75 * alea(j, 3), r: 18 + 60 * alea(j, 4), ph: alea(j, 5) * Math.PI * 2,
  teinte: alea(j, 6) < 0.78 ? 0 : 3,
}));

let LUTINS: HTMLCanvasElement[] | null = null;
const lutins = () => {
  if (LUTINS) return LUTINS;
  LUTINS = PALETTE.map(([r, g, b]) => {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const x = c.getContext("2d")!;
    const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, `rgba(${Math.round(r + (255 - r) * 0.7)},${Math.round(g + (255 - g) * 0.7)},${Math.round(b + (255 - b) * 0.7)},1)`);
    gr.addColorStop(0.1, `rgba(${r},${g},${b},0.95)`);
    gr.addColorStop(0.25, `rgba(${r},${g},${b},0.4)`);
    gr.addColorStop(0.5, `rgba(${r},${g},${b},0.09)`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    x.fillStyle = gr;
    x.fillRect(0, 0, 64, 64);
    return c;
  });
  return LUTINS;
};
let BLOOM: HTMLCanvasElement | null = null;
const SX = new Float32Array(N);
const SY = new Float32Array(N);
const SA = new Float32Array(N);

/** Dessin d'une image de boucle : `ph` = phase (0 → 2π sur la boucle), donc la fin raccorde le début. */
const dessiner = (ctx: CanvasRenderingContext2D, p: Preset, ph: number) => {
  const L = lutins();
  ctx.clearRect(0, 0, W, H);
  ctx.globalCompositeOperation = "lighter";
  // poussières : orbite lente, période = la boucle
  for (const m of POUSSIERES) {
    const a = ph + m.ph;
    const x = m.x + Math.cos(a) * 26 * m.prof;
    const y = m.y + Math.sin(a) * 16 * m.prof;
    const d = m.r * (1.4 - m.prof);
    ctx.globalAlpha = 0.12 + 0.18 * m.prof * (0.6 + 0.4 * Math.sin(a * 2 + m.ph));
    ctx.drawImage(L[m.teinte], x - d / 2, y - d / 2, d, d);
  }
  if (p.sujet && p.ecran && p.hauteur_px) {
    const f = FORMES[p.sujet];
    const hW = f.bmax[1] - f.bmin[1];
    const D = (FOC * hW) / p.hauteur_px;
    const cx = (f.bmin[0] + f.bmax[0]) / 2, cy = (f.bmin[1] + f.bmax[1]) / 2, cz = (f.bmin[2] + f.bmax[2]) / 2;
    const lacet = 0.07 * Math.sin(ph);
    const tangage = 0.025 * Math.cos(ph);
    const [ia, ib, ic] = p.inclinaison ?? [0, 0, 0];
    const rot = (v: V3, ax: number, ay: number, az: number): V3 => {
      let [x, y, z] = v;
      [y, z] = [y * Math.cos(ax) - z * Math.sin(ax), y * Math.sin(ax) + z * Math.cos(ax)];
      [x, z] = [x * Math.cos(ay) + z * Math.sin(ay), -x * Math.sin(ay) + z * Math.cos(ay)];
      [x, y] = [x * Math.cos(az) - y * Math.sin(az), x * Math.sin(az) + y * Math.cos(az)];
      return [x, y, z];
    };
    const vit = [0.22, -0.16, 0.1, -0.07];
    for (let i = 0; i < N; i++) {
      let v: V3 = [f.p[3 * i] - cx, f.p[3 * i + 1] - cy, f.p[3 * i + 2] - cz];
      if (p.sujet === "sceau") {
        // anneaux : un tour entier (ou un multiple) par boucle, sens alternés → raccord parfait
        const a = (Math.sign(vit[f.g[i]]) * ph) / (f.g[i] + 2);
        v = [v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a), v[2]];
      }
      const b = 0.04;
      v = [v[0] + b * noise3D("bx", i * 0.37, Math.cos(ph) * 0.8, Math.sin(ph) * 0.8), v[1] + b * noise3D("by", i * 0.37, Math.cos(ph) * 0.8, Math.sin(ph) * 0.8), v[2]];
      v = rot(v, ia, ib, ic);
      v = rot(v, tangage, lacet, 0);
      const z = D - v[2];
      if (z < 0.5) { SA[i] = 0; continue; }
      SX[i] = p.ecran[0] + (FOC * v[0]) / z;
      SY[i] = p.ecran[1] - (FOC * v[1]) / z;
      const diam = Math.min(60, (f.t[i] * 130) / z * (D / 12));
      SA[i] = 0.9;
      ctx.globalAlpha = 0.9;
      ctx.drawImage(L[f.c[i]], SX[i] - diam / 2, SY[i] - diam / 2, diam, diam);
    }
    const a = f.a;
    const chemin = new Path2D();
    for (let j = 0; j < a.length; j += 2) {
      const u = a[j], w = a[j + 1];
      if (SA[u] < 0.05 || SA[w] < 0.05) continue;
      const dx = SX[u] - SX[w], dy = SY[u] - SY[w];
      if (dx * dx + dy * dy > 200 * 200) continue;
      chemin.moveTo(SX[u], SY[u]);
      chemin.lineTo(SX[w], SY[w]);
    }
    ctx.globalAlpha = 0.34;
    ctx.lineWidth = 1.25;
    ctx.strokeStyle = "rgb(201,171,76)";
    ctx.stroke(chemin);
  }
  if (p.graine) {
    const [gx, gy] = p.graine;
    const pouls = 1 + 0.35 * Math.pow(Math.max(0, Math.sin(ph * 2)), 8);
    const R = 260 * pouls;
    const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, R);
    g.addColorStop(0, "rgba(246,231,176,0.30)");
    g.addColorStop(0.3, "rgba(201,171,76,0.12)");
    g.addColorStop(1, "rgba(201,171,76,0)");
    ctx.globalAlpha = 1;
    ctx.fillStyle = g;
    ctx.fillRect(gx - R, gy - R, 2 * R, 2 * R);
  }
  if (!BLOOM) { BLOOM = document.createElement("canvas"); BLOOM.width = W / 2; BLOOM.height = H / 2; }
  const bc = BLOOM.getContext("2d")!;
  bc.globalCompositeOperation = "copy";
  bc.filter = "blur(7px)";
  bc.drawImage(ctx.canvas, 0, 0, W / 2, H / 2);
  bc.filter = "none";
  ctx.globalCompositeOperation = "lighter";
  ctx.globalAlpha = 0.5;
  ctx.drawImage(BLOOM, 0, 0, W, H);
  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
};

const Monde: React.FC<{ preset: Preset; ph: number }> = ({ preset, ph }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    if (ref.current) dessiner(ref.current.getContext("2d")!, preset, ph);
  }, [preset, ph]);
  const [a, b] = FONDS[preset.teinte];
  const [hx, hy] = preset.halo;
  return (
    <>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 50% 55% at ${hx * 100}% ${hy * 100}%, rgba(201,171,76,${preset.force}) 0%, rgba(201,171,76,0) 70%), linear-gradient(180deg, ${a} 0%, ${b} 100%)` }} />
      <canvas ref={ref} width={W} height={H} style={{ position: "absolute", left: 0, top: 0, width: W, height: H }} />
    </>
  );
};

export const FondV3: React.FC<{ preset: string; boucle?: number }> = ({ preset, boucle = 360 }) => {
  const f = useCurrentFrame();
  const ph = (2 * Math.PI * (f % boucle)) / boucle;
  return (
    <AbsoluteFill style={{ background: "#07070A" }}>
      <Monde preset={PRESETS[preset] ?? PRESETS.nuit} ph={ph} />
      <Grain opacite={0.08} />
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};

// ───────────── pré-générique v3 : logo, invitation à patienter (boucle de 20 s) ─────────────
const CSS = [
  ["Montserrat", 700, "montserrat-latin-700-normal.woff2"], ["Inter", 600, "inter-latin-600-normal.woff2"],
].map(([fam, w, fic]) => `@font-face{font-family:${fam};font-weight:${w};src:url(${staticFile(`fonts/${fic}`)}) format('woff2');}`).join("");

export const PreShowV3: React.FC<{ boucle?: number }> = ({ boucle = 600 }) => {
  const f = useCurrentFrame();
  const ph = (2 * Math.PI * (f % boucle)) / boucle;
  const [poignee] = useState(() => delayRender("Polices pré-générique"));
  useEffect(() => {
    Promise.all([document.fonts.load("700 48px Montserrat"), document.fonts.load("600 44px Inter")])
      .finally(() => continueRender(poignee));
  }, [poignee]);
  const respir = 0.92 + 0.08 * Math.sin(ph);
  return (
    <AbsoluteFill style={{ background: "#07070A" }}>
      <style>{CSS}</style>
      <Monde preset={{ ...PRESETS.graine, graine: [960, 330] }} ph={ph} />
      <Img src={staticFile("logo-yeba-fond-sombre.png")} style={{ position: "absolute", left: 960 - 310, top: 132, width: 620, opacity: respir }} />
      <div style={{ position: "absolute", left: 0, top: 772, width: W, textAlign: "center", fontFamily: "Montserrat", fontWeight: 700, fontSize: 56, color: "#FFFFFF" }}>
        La soirée commence dans quelques instants
      </div>
      <div style={{ position: "absolute", left: 0, top: 880, width: W, textAlign: "center", fontFamily: "Inter", fontWeight: 600, fontSize: 44, letterSpacing: "0.2em", color: "#C9AB4C" }}>
        SAISON 1 · SOIRÉE DE LANCEMENT
      </div>
      <Grain opacite={0.08} />
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};

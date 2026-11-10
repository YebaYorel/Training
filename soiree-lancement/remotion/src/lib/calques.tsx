import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { OR } from "../charte";
import { aleatoire, DOUX, impulsion, p, TAU } from "./motion";

/** Grain argentique animé (8 tuiles de bruit qui alternent toutes les 2 images). */
export const Grain: React.FC<{ opacite?: number }> = ({ opacite = 0.32 }) => {
  const f = useCurrentFrame();
  const i = Math.floor(f / 2) % 8;
  return (
    <AbsoluteFill style={{ opacity: opacite, mixBlendMode: "overlay", pointerEvents: "none" }}>
      <Img src={staticFile(`grain/grain-${i}.png`)} style={{ width: 1920, height: 1080 }} />
    </AbsoluteFill>
  );
};

/** Vignettage : assombrit les bords, concentre le regard au centre. */
export const Vignette: React.FC<{ force?: number }> = ({ force = 0.7 }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,${force}) 100%)`,
      pointerEvents: "none",
    }}
  />
);

/** Bandes cinéma (format 2,39:1 quand hauteur = 138 px). */
export const Bandes: React.FC<{ hauteur: number }> = ({ hauteur }) =>
  hauteur <= 0.5 ? null : (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: hauteur, background: "#000" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: hauteur, background: "#000" }} />
    </AbsoluteFill>
  );

/** Éclair blanc/or sur les impacts. */
export const Eclair: React.FC<{ f: number; impacts: { f: number; force: number }[] }> = ({ f, impacts }) => {
  let o = 0;
  for (const i of impacts) {
    const t = f - i.f;
    if (t >= 0 && t < 14) o = Math.max(o, 0.55 * i.force * Math.exp(-t / 3.2));
  }
  return o < 0.01 ? null : (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 50%, #FFF7DA 0%, rgba(201,168,76,0.6) 45%, rgba(0,0,0,0) 80%)",
        opacity: o,
        mixBlendMode: "screen",
        pointerEvents: "none",
      }}
    />
  );
};

/** Halo lumineux doux. */
export const Halo: React.FC<{
  x: number;
  y: number;
  rayon: number;
  couleur?: string;
  opacite?: number;
}> = ({ x, y, rayon, couleur = "201,168,76", opacite = 0.35 }) => (
  <div
    style={{
      position: "absolute",
      left: x - rayon,
      top: y - rayon,
      width: rayon * 2,
      height: rayon * 2,
      borderRadius: "50%",
      background: `radial-gradient(circle, rgba(${couleur},${opacite}) 0%, rgba(${couleur},${opacite * 0.35}) 35%, rgba(${couleur},0) 70%)`,
      pointerEvents: "none",
    }}
  />
);

/** Onde de choc circulaire (impact). */
export const OndeDeChoc: React.FC<{ f: number; debut: number; x?: number; y?: number; rayonMax?: number }> = ({
  f,
  debut,
  x = 960,
  y = 540,
  rayonMax = 1100,
}) => {
  const t = p(f, debut, 42);
  if (t <= 0 || t >= 1) return null;
  const r = rayonMax * t;
  return (
    <div
      style={{
        position: "absolute",
        left: x - r,
        top: y - r,
        width: r * 2,
        height: r * 2,
        borderRadius: "50%",
        border: `${6 * (1 - t) + 1}px solid rgba(233,215,160,${0.55 * (1 - t)})`,
        boxShadow: `0 0 ${40 * (1 - t)}px rgba(201,168,76,${0.5 * (1 - t)})`,
      }}
    />
  );
};

/**
 * Particules lumineuses (bokeh). En mode « boucle », chaque particule suit une orbite
 * périodique de période `boucle` images : la vidéo se répète sans couture.
 */
export const Poussieres: React.FC<{
  n?: number;
  graine?: number;
  couleur?: string;
  tailleMin?: number;
  tailleMax?: number;
  opacite?: number;
  boucle?: number;
  derive?: number;
  zone?: [number, number, number, number];
}> = ({
  n = 50,
  graine = 7,
  couleur = "201,168,76",
  tailleMin = 3,
  tailleMax = 18,
  opacite = 0.45,
  boucle = 0,
  derive = 0.35,
  zone = [0, 0, 1920, 1080],
}) => {
  const f = useCurrentFrame();
  const r = aleatoire(graine);
  const parts = Array.from({ length: n }, () => ({
    x: zone[0] + r() * (zone[2] - zone[0]),
    y: zone[1] + r() * (zone[3] - zone[1]),
    t: tailleMin + r() ** 2 * (tailleMax - tailleMin),
    a: 20 + r() * 90,
    k: 1 + Math.floor(r() * 2),
    ph: r() * TAU,
    o: 0.25 + r() * 0.75,
    v: 0.4 + r() * 1.2,
  }));
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {parts.map((q, i) => {
        let x: number;
        let y: number;
        let scint: number;
        if (boucle > 0) {
          const ang = (TAU * q.k * f) / boucle + q.ph;
          x = q.x + Math.cos(ang) * q.a;
          y = q.y + Math.sin(ang * 1) * q.a * 0.6;
          scint = 0.65 + 0.35 * Math.sin((TAU * 2 * f) / boucle + q.ph * 3);
        } else {
          x = q.x + Math.sin(f * 0.01 * q.v + q.ph) * q.a * 0.4;
          y = q.y - f * derive * q.v;
          y = ((((y - zone[1]) % (zone[3] - zone[1])) + (zone[3] - zone[1])) % (zone[3] - zone[1])) + zone[1];
          scint = 0.7 + 0.3 * Math.sin(f * 0.08 * q.v + q.ph);
        }
        const s = q.t;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x - s,
              top: y - s,
              width: s * 2,
              height: s * 2,
              borderRadius: "50%",
              background: `radial-gradient(circle, rgba(${couleur},${opacite * q.o * scint}) 0%, rgba(${couleur},0) 70%)`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/** Balayage de lumière dorée en diagonale. Toujours placé SOUS des panneaux opaques et rogné hors des titres :
 *  il ne passe jamais sur un mot. */
export const BalayageOr: React.FC<{ f: number; debut: number; duree?: number; zone?: [number, number] }> = ({ f, debut, duree = 26, zone }) => {
  const t = p(f, debut, duree, DOUX);
  if (t <= 0 || t >= 1) return null;
  const x = -900 + t * 3600;
  // zone [haut, bas] : le reflet est rogné à cette bande horizontale (jamais sur un titre).
  const rognage = zone ? `inset(${zone[0]}px 0px ${1080 - zone[1]}px 0px)` : undefined;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen", overflow: "hidden", clipPath: rognage }}>
      <div
        style={{
          position: "absolute",
          top: -400,
          left: x,
          width: 520,
          height: 1900,
          transform: "rotate(18deg)",
          background:
            "linear-gradient(90deg, rgba(201,168,76,0) 0%, rgba(201,168,76,0.35) 35%, rgba(255,246,214,0.9) 50%, rgba(201,168,76,0.35) 65%, rgba(201,168,76,0) 100%)",
          filter: "blur(8px)",
          opacity: impulsion(t, 0.5, 0.3) * 1.2,
        }}
      />
    </AbsoluteFill>
  );
};

/**
 * Pétales de lumière tournants : 6 lobes très flous (aucun trait net, donc jamais une « ligne »
 * qui traverserait un mot). Rotation de 60° par boucle : la boucle est sans couture.
 */
export const Rayons: React.FC<{ x: number; y: number; boucle: number; opacite?: number; portee?: number }> = ({
  x,
  y,
  boucle,
  opacite = 0.22,
  portee = 60,
}) => {
  const f = useCurrentFrame();
  const angle = (60 * f) / boucle;
  return (
    <div
      style={{
        position: "absolute",
        left: x - 1400,
        top: y - 1400,
        width: 2800,
        height: 2800,
        borderRadius: "50%",
        transform: `rotate(${angle}deg)`,
        background: `repeating-conic-gradient(from 0deg, rgba(201,168,76,${opacite}) 0deg, rgba(201,168,76,0) 22deg, rgba(201,168,76,0) 38deg, rgba(201,168,76,${opacite}) 60deg)`,
        filter: "blur(38px)",
        WebkitMaskImage: `radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.5) ${portee * 0.42}%, rgba(0,0,0,0) ${portee}%)`,
        maskImage: `radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.5) ${portee * 0.42}%, rgba(0,0,0,0) ${portee}%)`,
      }}
    />
  );
};

/** Ligne de flare anamorphique (trait horizontal lumineux). */
export const Flare: React.FC<{ x: number; y: number; largeur?: number; opacite?: number }> = ({
  x,
  y,
  largeur = 900,
  opacite = 0.8,
}) => (
  <div
    style={{
      position: "absolute",
      left: x - largeur / 2,
      top: y - 3,
      width: largeur,
      height: 6,
      borderRadius: 3,
      background: `linear-gradient(90deg, rgba(255,240,200,0) 0%, rgba(255,240,200,${opacite}) 50%, rgba(255,240,200,0) 100%)`,
      boxShadow: `0 0 24px rgba(201,168,76,${opacite * 0.8})`,
      mixBlendMode: "screen",
    }}
  />
);

export const COULEUR_OR = OR;

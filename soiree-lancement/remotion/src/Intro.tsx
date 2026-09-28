import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { BLANC, NOIR, OR, Polices } from "./charte";

// Réseau de points reliés (clin d'œil au logo : trois pitons en réseau), tracé progressivement.
const POINTS: [number, number][] = [
  [360, 760], [560, 420], [760, 760], [960, 250], [1160, 760], [1360, 420], [1560, 760],
  [660, 590], [860, 520], [1060, 520], [1260, 590], [960, 640],
];
const LIENS: [number, number][] = [
  [0, 1], [1, 2], [0, 2], [2, 3], [3, 4], [2, 4], [4, 5], [5, 6], [4, 6],
  [1, 7], [7, 8], [8, 3], [3, 9], [9, 10], [10, 5], [8, 11], [9, 11], [7, 11], [11, 10],
];

const Reseau: React.FC<{ frame: number }> = ({ frame }) => (
  <svg width={1920} height={1080} style={{ position: "absolute" }}>
    {LIENS.map(([a, b], i) => {
      const [x1, y1] = POINTS[a];
      const [x2, y2] = POINTS[b];
      const long = Math.hypot(x2 - x1, y2 - y1);
      const p = interpolate(frame, [i * 3, i * 3 + 25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return (
        <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={OR} strokeWidth={4} strokeLinecap="round"
          strokeDasharray={long} strokeDashoffset={long * (1 - p)} opacity={0.9} />
      );
    })}
    {POINTS.map(([x, y], i) => {
      const r = interpolate(frame, [i * 4, i * 4 + 12], [0, 12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return <circle key={i} cx={x} cy={y} r={r} fill={i % 3 === 0 ? BLANC : OR} />;
    })}
  </svg>
);

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 0–90 : le réseau se trace ; 90–120 : il s'efface ; 105+ : le logo arrive.
  const reseauOpacite = interpolate(frame, [90, 125], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const logo = spring({ frame: frame - 105, fps, config: { damping: 14, mass: 0.9 } });
  const slogan1 = interpolate(frame, [165, 190], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const slogan2 = interpolate(frame, [195, 220], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sortie = interpolate(frame, [275, 300], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });

  return (
    <AbsoluteFill style={{ backgroundColor: NOIR, fontFamily: "Montserrat", opacity: sortie }}>
      <Polices />
      <AbsoluteFill style={{ opacity: reseauOpacite }}>
        <Reseau frame={frame} />
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 90 }}>
        <Img src={staticFile("logo-yeba-fond-sombre.png")}
          style={{ width: 620, opacity: logo, transform: `scale(${0.7 + 0.3 * logo}) translateY(${(1 - logo) * 60}px)` }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 110, textAlign: "center" }}>
        <div style={{ color: BLANC, fontWeight: 800, fontSize: 64, opacity: slogan1, transform: `translateY(${(1 - slogan1) * 30}px)` }}>
          Sous le baobab de la connaissance,
        </div>
        <div style={{ color: OR, fontWeight: 800, fontSize: 64, opacity: slogan2, transform: `translateY(${(1 - slogan2) * 30}px)` }}>
          les graines du savoir.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

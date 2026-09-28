import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { BLANC, BLEU, NOIR, OR, Polices } from "./charte";

type Props = { numero: string; titre: string; accroche: string };

// Transition de partie : un compte-tours monte en régime, puis le titre de la partie s'impose.
export const SectionTitle: React.FC<Props> = ({ numero, titre, accroche }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const regime = spring({ frame: frame - 10, fps, config: { damping: 9, stiffness: 60 } });
  const angle = interpolate(regime, [0, 1], [-135, 70]);
  const texte = spring({ frame: frame - 45, fps, config: { damping: 16 } });
  const r = 300;
  const arc = (a0: number, a1: number) => {
    const p = (a: number) => [960 + 520 + r * Math.cos((a * Math.PI) / 180), 540 + r * Math.sin((a * Math.PI) / 180)];
    const [x0, y0] = p(a0);
    const [x1, y1] = p(a1);
    return `M ${x0} ${y0} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}`;
  };
  return (
    <AbsoluteFill style={{ background: `linear-gradient(120deg, ${NOIR} 55%, ${BLEU})`, fontFamily: "Montserrat" }}>
      <Polices />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <path d={arc(135, 405)} stroke={OR} strokeOpacity={0.25} strokeWidth={22} fill="none" strokeLinecap="round" />
        <path d={arc(135, 135 + 270 * regime * 0.78)} stroke={OR} strokeWidth={22} fill="none" strokeLinecap="round" />
        <g transform={`translate(1480 540) rotate(${angle})`}>
          <line x1={0} y1={0} x2={0} y2={-230} stroke={BLANC} strokeWidth={12} strokeLinecap="round" />
        </g>
        <circle cx={1480} cy={540} r={26} fill={OR} />
      </svg>
      <div style={{ position: "absolute", left: 140, top: 250, opacity: texte, transform: `translateX(${(1 - texte) * -80}px)` }}>
        <div style={{ color: OR, fontWeight: 900, fontSize: 260, lineHeight: 1 }}>{numero}</div>
        <div style={{ color: BLANC, fontWeight: 800, fontSize: 110, marginTop: 10 }}>{titre}</div>
        <div style={{ color: OR, fontWeight: 800, fontSize: 56, marginTop: 30 }}>{accroche}</div>
      </div>
    </AbsoluteFill>
  );
};

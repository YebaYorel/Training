import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { BLANC, OR, Polices, TEINTES } from "./charte";
import { AnneauxSceau, BaobabTrace, Constellation, LIENS_PITONS, NOEUDS_PITONS } from "./lib/traces";
import { BalayageOr, Bandes, Grain, Halo, Poussieres, Vignette } from "./lib/calques";
import { LettresMontantes, Resserre } from "./lib/texte";
import { aleatoire, DOUX, EXPO, lerp, p, TAU } from "./lib/motion";

export type EpisodeProps = { numero: number; titre: string; sujet: string; motif: string; teinte: string; avecSon?: boolean };

const Projecteurs: React.FC<{ f: number }> = ({ f }) => (
  <AbsoluteFill>
    {[0, 1, 2].map((i) => {
      const angle = Math.sin(f * 0.035 + i * 2.1) * 14 + (i - 1) * 16;
      return (
        <div
          key={i}
          style={{
            position: "absolute",
            left: 1200 + i * 230 - 260,
            top: -80,
            width: 520,
            height: 1300,
            transformOrigin: "260px 0px",
            transform: `rotate(${angle}deg)`,
            background: "linear-gradient(180deg, rgba(255,240,200,0.22) 0%, rgba(255,240,200,0.05) 60%, rgba(255,240,200,0) 100%)",
            clipPath: "polygon(46% 0%, 54% 0%, 100% 100%, 0% 100%)",
            filter: "blur(6px)",
          }}
        />
      );
    })}
  </AbsoluteFill>
);

const ReseauAleatoire: React.FC<{ f: number }> = ({ f }) => {
  const r = aleatoire(31);
  const noeuds: [number, number][] = Array.from({ length: 22 }, () => [1160 + r() * 660, 170 + r() * 740]);
  const liens: [number, number][] = [];
  noeuds.forEach(([x, y], i) => {
    const proches = noeuds
      .map(([x2, y2], j) => ({ j, d: Math.hypot(x2 - x, y2 - y) }))
      .filter((o) => o.j !== i)
      .sort((a, b) => a.d - b.d)
      .slice(0, 2);
    proches.forEach((o) => liens.push([i, o.j]));
  });
  return (
    <Constellation
      positions={noeuds}
      liens={liens}
      progresLien={(i) => p(f, 4 + i * 0.9, 26, EXPO)}
      apparitionNoeud={(i) => p(f, 2 + i * 1.6, 14, EXPO)}
      epaisseur={1.6}
      opacite={0.55}
    />
  );
};

const Interface: React.FC<{ f: number }> = ({ f }) => {
  const cadres = [
    [1150, 250, 640, 460],
    [1190, 300, 250, 170],
    [1470, 300, 280, 56],
    [1470, 380, 280, 56],
    [1190, 500, 560, 160],
  ];
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.5 }}>
      {cadres.map(([x, y, w, h], i) => {
        const t = p(f, 4 + i * 6, 30, EXPO);
        const per = 2 * (w + h);
        return (
          <rect key={i} x={x} y={y} width={w} height={h} rx={14} fill="none" stroke={OR} strokeWidth={2.5} strokeDasharray={per} strokeDashoffset={per * (1 - t)} />
        );
      })}
    </svg>
  );
};

const Radar: React.FC<{ f: number }> = ({ f }) => {
  const angle = (f * 4) % 360;
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.45 }}>
        {[120, 230, 340].map((rr) => (
          <circle key={rr} cx={1500} cy={540} r={rr} fill="none" stroke={OR} strokeWidth={1.6} opacity={0.6} />
        ))}
        <line x1={1150} y1={540} x2={1850} y2={540} stroke={OR} strokeWidth={1} opacity={0.4} />
        <line x1={1500} y1={190} x2={1500} y2={890} stroke={OR} strokeWidth={1} opacity={0.4} />
      </svg>
      <div
        style={{
          position: "absolute",
          left: 1500 - 340,
          top: 540 - 340,
          width: 680,
          height: 680,
          borderRadius: "50%",
          transform: `rotate(${angle}deg)`,
          background: "conic-gradient(from 0deg, rgba(201,171,76,0.45) 0deg, rgba(201,171,76,0) 70deg, rgba(201,171,76,0) 360deg)",
        }}
      />
    </AbsoluteFill>
  );
};

const Motif: React.FC<{ motif: string; f: number }> = ({ motif, f }) => {
  switch (motif) {
    case "casting":
      return <Projecteurs f={f} />;
    case "baobab":
      return <BaobabTrace f={f} debut={0} x={1500} y={960} hauteur={880} vitesse={1.7} opacite={0.45} epaisseur={4} />;
    case "sceau":
      return <AnneauxSceau f={f * 3} x={1500} y={540} rayon={330} opacite={0.42} />;
    case "reseau":
      return <ReseauAleatoire f={f} />;
    case "outils":
      return <Interface f={f} />;
    case "radar":
      return <Radar f={f} />;
    default:
      return (
        <AbsoluteFill style={{ transform: `translateX(540px) scale(${lerp(0.82, 0.68, p(f, 0, 120, DOUX))})`, opacity: 0.45 }}>
          <Constellation positions={NOEUDS_PITONS} liens={LIENS_PITONS} progresLien={(i) => p(f, i * 1.2, 22, EXPO)} apparitionNoeud={(i) => p(f, i, 12, EXPO)} />
        </AbsoluteFill>
      );
  }
};

/** Carte-titre d'épisode : 4,5 s, bandes cinéma, filet or, titre qui monte, sting sonore. */
export const Episode: React.FC<EpisodeProps> = ({ numero, titre, sujet, motif, teinte, avecSon = true }) => {
  const f = useCurrentFrame();
  const num = String(numero).padStart(2, "0");
  const fond = TEINTES[teinte] ?? TEINTES.noir;
  const couleurHalo = teinte === "terre" ? "205,118,58" : teinte === "bleu" ? "90,130,200" : "201,171,76";
  return (
    <AbsoluteFill style={{ background: fond, fontFamily: "Montserrat, sans-serif" }}>
      <Polices />
      {avecSon && <Audio src={staticFile("audio/sting.wav")} />}
      <Halo x={1500} y={540} rayon={820} couleur={couleurHalo} opacite={0.22} />
      <Motif motif={motif} f={f} />
      <Poussieres n={30} graine={numero * 13} tailleMin={2} tailleMax={9} opacite={0.4} derive={0.3} zone={[1080, 120, 1920, 960]} />
      <div
        style={{
          position: "absolute",
          left: 150,
          top: 470,
          width: 860 * p(f, 6, 26, EXPO),
          height: 2,
          background: `linear-gradient(90deg, ${OR} 0%, #F6E7B0 45%, rgba(201,171,76,0) 100%)`,
          boxShadow: "0 0 18px rgba(201,171,76,0.6)",
        }}
      />
      <div style={{ position: "absolute", left: 150, top: 396, color: OR, fontWeight: 800, fontSize: 30 }}>
        <Resserre texte={`ÉPISODE\u00a0${num}`} f={f} debut={14} duree={34} de={0.9} a={0.45} />
      </div>
      <div style={{ position: "absolute", left: 146, top: 500, color: BLANC, fontWeight: 800, fontSize: 112, lineHeight: "130px" }}>
        <LettresMontantes texte={titre} f={f} debut={24} decalage={1.5} />
      </div>
      <div style={{ position: "absolute", left: 152, top: 664, color: OR, fontWeight: 700, fontSize: 40, opacity: p(f, 52, 20, DOUX) }}>
        {sujet}
      </div>
      <BalayageOr f={f} debut={92} duree={28} />
      <Grain opacite={0.16} />
      <Vignette force={0.6} />
      <Bandes hauteur={120} />
      <AbsoluteFill style={{ background: "#000", opacity: p(f, 118, 17, DOUX) }} />
    </AbsoluteFill>
  );
};

export const EPISODE_DUREE = 135;
export const TAU_ = TAU;

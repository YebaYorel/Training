import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { evolvePath } from "@remotion/paths";
import { BLANC, BLEU, BLEU_NUIT, GRIS, NUIT, OR, OR_CLAIR, Polices, TERRE } from "./charte";
import { BalayageOr, Flare, Grain, Halo, Poussieres, Rayons, Vignette } from "./lib/calques";
import { AnneauxSceau, BaobabTrace } from "./lib/traces";
import { aleatoire, DOUX, lerp, p, TAU } from "./lib/motion";
import type { Horaires } from "./Generique";

// Toutes les boucles sont « sans couture » : chaque mouvement a une période qui divise la durée.

const DEGRADES: Record<string, string> = {
  noir: `linear-gradient(135deg, #0E0E12 0%, ${NUIT} 55%, #16120A 100%)`,
  bleu: `linear-gradient(135deg, ${BLEU} 0%, #132A50 50%, ${BLEU_NUIT} 100%)`,
  terre: `linear-gradient(135deg, #22160D 0%, ${TERRE} 55%, #120C08 100%)`,
};
const HALOS: Record<string, string> = { noir: "201,171,76", bleu: "110,150,220", terre: "205,118,58" };

/** Pré-show : boucle de 20 s pendant l'accueil (sans son). */
export const PreShow: React.FC<{ boucle?: number }> = ({ boucle = 600 }) => {
  const f = useCurrentFrame();
  const souffle = 1 + 0.022 * Math.sin((TAU * 2 * f) / boucle);
  const pouls = 0.5 + 0.5 * Math.sin((TAU * f) / boucle);
  return (
    <AbsoluteFill style={{ background: DEGRADES.noir, fontFamily: "Montserrat, sans-serif" }}>
      <Polices />
      <Rayons x={960} y={360} boucle={boucle} opacite={0.16} portee={30} />
      <Halo x={960} y={360} rayon={620} opacite={0.16 + 0.1 * pouls} />
      <Poussieres n={70} graine={3} boucle={boucle} tailleMin={2} tailleMax={12} opacite={0.42} />
      <div style={{ position: "absolute", left: 960 - 270, top: 120, width: 540, transform: `scale(${souffle})`, filter: "drop-shadow(0 0 40px rgba(201,171,76,0.35))" }}>
        <Img src={staticFile("logo-yeba-fond-sombre.png")} style={{ width: 540 }} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 700, textAlign: "center", color: BLANC, fontWeight: 700, fontSize: 46 }}>
        La soirée commence dans quelques instants
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 790, textAlign: "center", color: OR, fontWeight: 800, fontSize: 26, letterSpacing: "0.45em" }}>
        SAISON 1 · SOIRÉE DE LANCEMENT
      </div>
      <BalayageOr f={f % (boucle / 2)} debut={boucle / 2 - 70} duree={50} />
      <Grain opacite={0.14} />
      <Vignette force={0.55} />
    </AbsoluteFill>
  );
};

/** Ambiance vivante (fond des slides de contenu) : lueurs lentes + poussières d'or. */
export const Ambiance: React.FC<{ teinte: string; boucle?: number }> = ({ teinte, boucle = 360 }) => {
  const f = useCurrentFrame();
  const c = HALOS[teinte] ?? HALOS.noir;
  const a = (TAU * f) / boucle;
  return (
    <AbsoluteFill style={{ background: DEGRADES[teinte] ?? DEGRADES.noir }}>
      <Halo x={1500 + 220 * Math.cos(a)} y={220 + 120 * Math.sin(2 * a)} rayon={760} couleur={c} opacite={0.15} />
      <Halo x={260 + 160 * Math.sin(a + 1)} y={900 + 90 * Math.cos(a)} rayon={680} couleur={c} opacite={0.1} />
      <Halo x={960 + 300 * Math.sin(2 * a + 2)} y={560 + 80 * Math.cos(a + 0.5)} rayon={900} couleur={c} opacite={0.05} />
      <Poussieres n={42} graine={teinte.length * 17} boucle={boucle} tailleMin={2} tailleMax={14} opacite={0.32} couleur={teinte === "bleu" ? "190,210,255" : "201,171,76"} />
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};

/** Couverture : rayons dorés lents derrière le logo (le logo et le slogan sont dans PowerPoint). */
export const FondCover: React.FC<{ boucle?: number }> = ({ boucle = 360 }) => {
  const f = useCurrentFrame();
  const pouls = 0.5 + 0.5 * Math.sin((TAU * f) / boucle);
  return (
    <AbsoluteFill style={{ background: DEGRADES.noir }}>
      <Rayons x={960} y={262} boucle={boucle} opacite={0.2} portee={26} />
      <Halo x={960} y={262} rayon={560} opacite={0.14 + 0.08 * pouls} />
      <Poussieres n={60} graine={8} boucle={boucle} tailleMin={2} tailleMax={12} opacite={0.38} />
      <Vignette force={0.55} />
    </AbsoluteFill>
  );
};

/** Baobab : l'arbre se dessine à droite, des graines tombent (image finale tenue). */
export const FondBaobab: React.FC = () => {
  const f = useCurrentFrame();
  const BX = 1500;
  const BY = 990;
  const BH = 900;
  const feuille = (lx: number, ly: number): [number, number] => [BX - BH / 2 + lx * (BH / 1000), BY - 0.93 * BH + ly * (BH / 1000)];
  const sources: [number, number][] = [[270, 402], [318, 402], [496, 342], [590, 338], [656, 366], [742, 410], [208, 456], [786, 500], [420, 330]];
  return (
    <AbsoluteFill style={{ background: DEGRADES.terre }}>
      <Halo x={BX} y={BY} rayon={820} couleur="205,118,58" opacite={0.32 * p(f, 0, 60, DOUX)} />
      <Poussieres n={26} graine={4} couleur="233,190,120" tailleMin={2} tailleMax={8} opacite={0.3} derive={0.2} zone={[1050, 0, 1920, 1080]} />
      <BaobabTrace f={f} debut={4} x={BX} y={BY} hauteur={BH} vitesse={1.25} />
      {sources.map(([lx, ly], i) => {
        const [x0, y0] = feuille(lx, ly);
        const t = f - (104 + i * 7);
        if (t < 0) return null;
        const y = y0 + 0.04 * t * t;
        return y > BY - 4 ? null : (
          <div key={i} style={{ position: "absolute", left: x0 + Math.sin(t * 0.09 + i) * 16 - 5, top: y - 5, width: 10, height: 10, borderRadius: "50%", background: OR_CLAIR, boxShadow: "0 0 14px rgba(233,215,160,0.9)" }} />
        );
      })}
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};

/** Conversion « 08h30 » → 8,5. */
export const heure = (h: string) => {
  const [hh, mm] = h.split("h").map(Number);
  return hh + (mm || 0) / 60;
};
/** Position horizontale (px, repère 1920) d'une heure sur la frise de la journée. */
export const xHeure = (h: number, horaires: Horaires) => {
  const h0 = heure(horaires.debut);
  const h1 = heure(horaires.fin);
  return 260 + ((h - h0) / (h1 - h0)) * 1400;
};
export const FRISE_Y = 860;

/** Journée : le soleil parcourt l'arc de 08h30 à 16h30 au-dessus d'une frise qui se remplit. */
export const FondJournee: React.FC<{ horaires: Horaires }> = ({ horaires }) => {
  const f = useCurrentFrame();
  const t = p(f, 16, 140, DOUX);
  const arc = "M 260 760 Q 960 -100 1660 760";
  const { strokeDasharray, strokeDashoffset } = evolvePath(Math.max(0.0001, t), arc);
  const sx = 260 + 1400 * t;
  const sy = (1 - t) ** 2 * 760 + 2 * t * (1 - t) * -100 + t ** 2 * 760;
  const hCourante = lerp(heure(horaires.debut), heure(horaires.fin), t);
  const xp0 = xHeure(heure(horaires.pause_debut), horaires);
  const xp1 = xHeure(heure(horaires.pause_fin), horaires);
  const xs = xHeure(hCourante, horaires);
  const aube = Math.max(0, 1 - Math.abs(t - 0) / 0.18) + Math.max(0, 1 - Math.abs(t - 1) / 0.18);
  const apparition = p(f, 0, 24, DOUX);
  const segment = (a: number, b: number, couleur: string, tirets = false) => {
    const fin = Math.min(b, Math.max(a, xs));
    return (
      <>
        <div style={{ position: "absolute", left: a, top: FRISE_Y - 3, width: b - a, height: 6, borderRadius: 3, background: tirets ? "repeating-linear-gradient(90deg, rgba(184,188,198,0.45) 0 10px, rgba(0,0,0,0) 10px 18px)" : "rgba(255,255,255,0.12)" }} />
        {!tirets && fin > a && <div style={{ position: "absolute", left: a, top: FRISE_Y - 3, width: fin - a, height: 6, borderRadius: 3, background: couleur, boxShadow: "0 0 14px rgba(201,171,76,0.7)" }} />}
      </>
    );
  };
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, #0D1424 0%, ${NUIT} 70%)`, opacity: apparition }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 100%, rgba(214,120,60,0.35) 0%, rgba(0,0,0,0) 60%)", opacity: aube }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <path d={arc} fill="none" stroke="rgba(184,188,198,0.25)" strokeWidth={2} strokeDasharray="6 12" />
        <path d={arc} fill="none" stroke={OR} strokeWidth={3} strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} opacity={0.85} />
        {[horaires.debut, horaires.pause_debut, horaires.pause_fin, horaires.fin].map((h) => (
          <line key={h} x1={xHeure(heure(h), horaires)} y1={FRISE_Y - 16} x2={xHeure(heure(h), horaires)} y2={FRISE_Y + 16} stroke={GRIS} strokeWidth={2} opacity={0.7} />
        ))}
      </svg>
      {segment(260, xp0, `linear-gradient(90deg, ${OR} 0%, ${OR_CLAIR} 100%)`)}
      {segment(xp0, xp1, GRIS, true)}
      {segment(xp1, 1660, `linear-gradient(90deg, ${OR} 0%, ${OR_CLAIR} 100%)`)}
      <Halo x={sx} y={sy} rayon={220} couleur="246,220,150" opacite={0.5} />
      <div style={{ position: "absolute", left: sx - 34, top: sy - 34, width: 68, height: 68, borderRadius: "50%", background: "radial-gradient(circle at 40% 35%, #FFF6DA 0%, #F2D27E 45%, #C9AB4C 100%)", boxShadow: "0 0 50px 14px rgba(242,210,126,0.55)" }} />
      <Poussieres n={24} graine={12} tailleMin={2} tailleMax={7} opacite={0.25} derive={0.1} zone={[0, 0, 1920, 700]} />
      <Vignette force={0.45} />
    </AbsoluteFill>
  );
};

/** Sceau : anneaux dorés lents derrière le panneau Qualiopi (masqués par le panneau opaque). */
export const FondSceau: React.FC<{ boucle?: number }> = ({ boucle = 360 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: DEGRADES.bleu }}>
      <AnneauxSceau f={f} x={529} y={547} rayon={300} boucle={boucle} opacite={0.42} />
      <Halo x={529} y={547} rayon={620} couleur="201,171,76" opacite={0.1 + 0.05 * Math.sin((TAU * f) / boucle)} />
      <Poussieres n={36} graine={6} boucle={boucle} tailleMin={2} tailleMax={10} opacite={0.3} couleur="220,230,255" />
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};

/** Flux de données : traits lumineux en haut et en bas de l'écran uniquement (jamais derrière le texte). */
export const FondFlux: React.FC<{ boucle?: number }> = ({ boucle = 360 }) => {
  const f = useCurrentFrame();
  const r = aleatoire(14);
  const voies = Array.from({ length: 14 }, (_, i) => {
    const haut = i < 6;
    const y = haut ? 40 + i * 26 : 936 + (i - 6) * 18;
    const a = 18 + Math.floor(r() * 60);
    const b = 40 + Math.floor(r() * 120);
    const k = 1 + Math.floor(r() * 3);
    const or = r() < 0.22;
    return { y, a, b, k, or, o: 0.12 + r() * 0.22, e: 1 + r() * 2 };
  });
  return (
    <AbsoluteFill style={{ background: DEGRADES.bleu }}>
      <Halo x={1500 + 160 * Math.cos((TAU * f) / boucle)} y={540} rayon={820} couleur="110,150,220" opacite={0.14} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {voies.map((v, i) => (
          <line
            key={i}
            x1={-200}
            y1={v.y}
            x2={2120}
            y2={v.y}
            stroke={v.or ? OR : "#CFE0FF"}
            strokeWidth={v.e}
            strokeLinecap="round"
            strokeDasharray={`${v.a} ${v.b}`}
            strokeDashoffset={-((f / boucle) * v.k * 4 * (v.a + v.b))}
            opacity={v.o}
          />
        ))}
      </svg>
      <Poussieres n={30} graine={15} boucle={boucle} tailleMin={2} tailleMax={10} opacite={0.25} couleur="200,215,255" />
      <Vignette force={0.45} />
    </AbsoluteFill>
  );
};

/** Bande-annonce : fuite de lumière et flare horizontal en bas de l'écran. */
export const FondBientot: React.FC<{ boucle?: number }> = ({ boucle = 360 }) => {
  const f = useCurrentFrame();
  const a = (TAU * f) / boucle;
  return (
    <AbsoluteFill style={{ background: DEGRADES.noir }}>
      <Halo x={1700 + 120 * Math.sin(a)} y={300 + 140 * Math.cos(a)} rayon={760} couleur="214,140,70" opacite={0.2} />
      <Halo x={200 + 120 * Math.cos(a)} y={900} rayon={600} couleur="201,171,76" opacite={0.1} />
      <Flare x={960 + 760 * Math.sin(a)} y={1000} largeur={1100} opacite={0.55} />
      <Poussieres n={50} graine={22} boucle={boucle} tailleMin={2} tailleMax={12} opacite={0.36} />
      <Vignette force={0.5} />
    </AbsoluteFill>
  );
};


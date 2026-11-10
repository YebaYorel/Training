import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from "remotion";
import { NUIT, Polices } from "./charte";
import { BalayageOr, Bandes, Eclair, Grain, Vignette } from "./lib/calques";
import { DOUX, p, secousse } from "./lib/motion";
import { Baobab, Chemin, ColdOpen, Confiance, Final, Formations, Ici, Metiers, Yeba } from "./generique/Scenes";
import T from "./timeline.json";

export type Horaires = { debut: string; pause_debut: string; pause_fin: string; fin: string; heures_par_jour: number };

const SC = T.scenes as unknown as Record<string, [number, number]>;
const seq = (nom: string) => ({ from: SC[nom][0], durationInFrames: SC[nom][1] - SC[nom][0] });

/** « YEBA — Saison 1 » : générique d'ouverture de 80 s, bande-son synchronisée sur timeline.json. */
export const Generique: React.FC<{ horaires: Horaires; avecSon?: boolean }> = ({ horaires, avecSon = true }) => {
  const f = useCurrentFrame();
  const choc = secousse(f, T.impacts);
  const [o0, o1] = T.bandes_ouverture;
  const bandes = 138 * (1 - p(f, o0, o1 - o0, DOUX)) + 18 * p(f, 560, 38, DOUX) * (1 - p(f, 600, 30, DOUX));
  return (
    <AbsoluteFill style={{ background: NUIT }}>
      <Polices />
      {avecSon && <Audio src={staticFile("audio/generique.wav")} />}
      <AbsoluteFill style={{ transform: `translate(${choc.x}px, ${choc.y}px)` }}>
        <Sequence {...seq("coldOpen")}><ColdOpen /></Sequence>
        <Sequence {...seq("ici")}><Ici /></Sequence>
        <Sequence {...seq("yeba")}><Yeba /></Sequence>
        <Sequence {...seq("baobab")}><Baobab /></Sequence>
        <Sequence {...seq("chemin")}><Chemin /></Sequence>
        <Sequence {...seq("metiers")}><Metiers /></Sequence>
        <Sequence {...seq("formations")}><Formations /></Sequence>
        <Sequence {...seq("confiance")}><Confiance horaires={horaires} /></Sequence>
        <Sequence {...seq("final")}><Final /></Sequence>
      </AbsoluteFill>
      {/* Seul reflet global : au passage ColdOpen → Ici, quand AUCUN texte n'est à l'écran. */}
      <BalayageOr f={f} debut={T.whooshes[0] - 8} duree={30} />
      <Eclair f={f} impacts={T.impacts} />
      <Grain opacite={0.16} />
      <Vignette force={0.62} />
      <Bandes hauteur={bandes} />
    </AbsoluteFill>
  );
};

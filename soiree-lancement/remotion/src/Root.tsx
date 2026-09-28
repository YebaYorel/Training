import React from "react";
import { Composition } from "remotion";
import { Intro } from "./Intro";
import { SectionTitle } from "./SectionTitle";

// Vidéos motion design YEBA FORMATIONS — 1920 × 1080, 30 images/s.
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Intro" component={Intro} durationInFrames={300} fps={30} width={1920} height={1080} />
    <Composition
      id="SectionTitle"
      component={SectionTitle}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ numero: "04", titre: "Nos formations", accroche: "Votre entreprise est un moteur." }}
    />
  </>
);

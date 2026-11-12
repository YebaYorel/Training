import React from "react";
import { Composition } from "remotion";
import { Generique } from "./Generique";
import { Episode, EPISODE_DUREE } from "./Episode";
import { GeneriqueV3 } from "./v3/Graine";
import { FondV3, PreShowV3 } from "./v3/FondV3";
import { Ambiance, FondBaobab, FondBientot, FondCover, FondFlux, FondJournee, FondSceau, PreShow } from "./Fonds";

// Valeurs par défaut (Studio). Le script scripts/rendre.mjs injecte les vraies valeurs depuis contenu/slides.json.
const HORAIRES = { debut: "08h30", pause_debut: "12h00", pause_fin: "13h00", fin: "16h30", heures_par_jour: 7 };
const CERTIFS = { qualiopi: "25FOR02027.1", nda: "04973676397" };
const V = { fps: 30, width: 1920, height: 1080 };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="GeneriqueV3" component={GeneriqueV3} durationInFrames={4800} fps={60} width={1920} height={1080} defaultProps={{ avecSon: true }} />
    <Composition id="FondV3" component={FondV3} durationInFrames={360} {...V} defaultProps={{ preset: "baobab", boucle: 360 }} />
    <Composition id="PreShowV3" component={PreShowV3} durationInFrames={600} {...V} defaultProps={{ boucle: 600 }} />
    <Composition id="Generique" component={Generique} durationInFrames={2400} {...V} defaultProps={{ horaires: HORAIRES, certifs: CERTIFS, avecSon: true }} />
    <Composition
      id="Episode"
      component={Episode}
      durationInFrames={EPISODE_DUREE}
      {...V}
      defaultProps={{ numero: 2, titre: "Les racines", sujet: "Histoire", motif: "baobab", teinte: "terre", avecSon: true }}
    />
    <Composition id="PreShow" component={PreShow} durationInFrames={600} {...V} defaultProps={{ boucle: 600 }} />
    <Composition id="Ambiance" component={Ambiance} durationInFrames={360} {...V} defaultProps={{ teinte: "noir", boucle: 360 }} />
    <Composition id="FondCover" component={FondCover} durationInFrames={360} {...V} defaultProps={{ boucle: 360 }} />
    <Composition id="FondBaobab" component={FondBaobab} durationInFrames={180} {...V} />
    <Composition id="FondJournee" component={FondJournee} durationInFrames={180} {...V} defaultProps={{ horaires: HORAIRES }} />
    <Composition id="FondSceau" component={FondSceau} durationInFrames={360} {...V} defaultProps={{ boucle: 360 }} />
    <Composition id="FondFlux" component={FondFlux} durationInFrames={360} {...V} defaultProps={{ boucle: 360 }} />
    <Composition id="FondBientot" component={FondBientot} durationInFrames={360} {...V} defaultProps={{ boucle: 360 }} />
  </>
);

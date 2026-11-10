import React from "react";
import { Composition } from "remotion";
import { Generique } from "./Generique";
import { Episode, EPISODE_DUREE } from "./Episode";
import { Ambiance, FondBaobab, FondBientot, FondCover, FondFlux, FondJournee, FondSceau, PreShow } from "./Fonds";

// Valeurs par défaut (Studio). Le script scripts/rendre.mjs injecte les vraies valeurs depuis contenu/slides.json.
const HORAIRES = { debut: "08h30", pause_debut: "12h00", pause_fin: "13h00", fin: "16h30", heures_par_jour: 7 };
const CERTIFS = { qualiopi: "25FOR02027.1", nda: "04973676397" };
const V = { fps: 30, width: 1920, height: 1080 };

export const RemotionRoot: React.FC = () => (
  <>
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

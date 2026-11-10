import React from "react";
import { AbsoluteFill, Img, spring, staticFile, useCurrentFrame } from "remotion";
import { BLANC, BLEU_NUIT, GRIS, NUIT, OR, OR_CLAIR, OR_POLI, TERRE } from "../charte";
import { AnneauxSceau, BaobabTrace, Constellation, Icone, LIENS_PITONS, NOEUDS_PITONS, noeudsDisperses } from "../lib/traces";
import { BalayageOr, Halo, OndeDeChoc, Poussieres } from "../lib/calques";
import { MotsMontants, Odometre, Resserre } from "../lib/texte";
import { aleatoire, DOUX, ENTREE, EXPO, fenetre, impulsion, lerp, p, QUINT } from "../lib/motion";
import T from "../timeline.json";

const NB = " ";
const SC = T.scenes as unknown as Record<string, [number, number]>;
const useG = (scene: string) => useCurrentFrame() + SC[scene][0];
const TEXTE: React.CSSProperties = { fontFamily: "Montserrat, sans-serif", color: BLANC };

// ───────────────────────────── 1. Ouverture à froid : l'étincelle devient les pitons ─────────────────────────────
export const ColdOpen: React.FC = () => {
  const g = useG("coldOpen");
  const disp = noeudsDisperses(11);
  const n = T.pops.length;
  const formation = p(g, 176, 70, QUINT);
  const position = (i: number, image: number): [number, number] => {
    const vol = p(image, T.pops[i % n], 30, EXPO);
    const forme = p(image, 176, 70, QUINT);
    const x = lerp(960, disp[i][0], vol);
    const y = lerp(540, disp[i][1], vol);
    return [lerp(x, NOEUDS_PITONS[i][0], forme), lerp(y, NOEUDS_PITONS[i][1], forme)];
  };
  const positions = NOEUDS_PITONS.map((_, i) => position(i, g));
  // Le réseau ne se tisse qu'une fois les étoiles en place : pas de traits qui balaient l'écran.
  const progresLien = (i: number) => p(g, 214 + i * 1.4, 24, EXPO);
  const apparition = (i: number) => p(g, T.pops[i % n], 12, EXPO);
  const etincelle = p(g, 18, 26, EXPO);
  const battement = impulsion(g, T.battements[0], 3.2) + impulsion(g, T.battements[1], 3.2);
  const zoom = lerp(1, 1.08, p(g, 40, 190, DOUX));
  const rot = lerp(-2.5, 0, p(g, 40, 190, DOUX));
  // Raccord de mouvement : les pitons glissent exactement à leur place de la scène suivante.
  const raccord = p(g, 232, 38, QUINT);
  const transformation = `translate(${lerp(0, 546, raccord)}px, ${lerp(0, 30, raccord)}px) scale(${lerp(zoom, 0.9, raccord)}) rotate(${rot}deg)`;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ transform: transformation, opacity: lerp(1, 0.32, raccord) }}>
        <Halo x={960} y={540} rayon={280 + 220 * battement} opacite={(0.16 * etincelle + 0.3 * battement) * (1 - formation)} />
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
          {NOEUDS_PITONS.map((_, i) => {
            const t0 = T.pops[i % n];
            if (g < t0 || g > t0 + 40) return null;
            const [x1, y1] = position(i, g - 5);
            const [x2, y2] = position(i, g);
            return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#F6E7B0" strokeWidth={2.5} strokeLinecap="round" opacity={1 - (g - t0) / 40} />;
          })}
        </svg>
        <Constellation positions={positions} liens={LIENS_PITONS} progresLien={progresLien} apparitionNoeud={apparition} />
        <div
          style={{
            position: "absolute",
            left: 950,
            top: 530,
            width: 20,
            height: 20,
            borderRadius: "50%",
            background: "#FFF6DA",
            boxShadow: `0 0 ${36 + 70 * battement}px ${12 + 24 * battement}px rgba(233,215,160,0.85)`,
            transform: `scale(${etincelle * (1 + 0.9 * battement)})`,
            opacity: 1 - p(g, 150, 36, DOUX),
          }}
        />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 868, textAlign: "center", ...TEXTE, color: OR, fontWeight: 800, fontSize: 30, opacity: fenetre(g, 58, 236, 24, 30) }}>
        <Resserre texte={`LA RÉUNION${NB}·${NB}974`} f={g} debut={58} duree={56} de={0.95} a={0.48} />
      </div>
    </AbsoluteFill>
  );
};

// ───────────────────────────── 2. « Ici, le savoir se partage. » ─────────────────────────────
export const Ici: React.FC = () => {
  const g = useG("ici");
  const [de] = SC.ici;
  const pousse = p(g, 430, 50, ENTREE);
  const derive = Math.sin((g - 270) * 0.012) * 14;
  return (
    <AbsoluteFill
      style={{
        opacity: p(g, de, 26, DOUX) * (1 - p(g, 454, 26, DOUX)),
        transform: `scale(${1 + pousse * 0.55})`,
        filter: `blur(${pousse * 14}px)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: -300,
          right: -300,
          bottom: -620,
          height: 1300,
          background:
            "radial-gradient(ellipse at 50% 100%, rgba(205,118,58,0.55) 0%, rgba(201,168,76,0.22) 38%, rgba(0,0,0,0) 70%)",
          opacity: p(g, de, 130, DOUX),
          transform: `translateY(${lerp(220, 0, p(g, de, 180, DOUX))}px)`,
        }}
      />
      <AbsoluteFill style={{ transform: `translate(${546 + derive}px, 30px) scale(0.9)`, opacity: 0.32 * p(g, 262, 10, DOUX) }}>
        <Constellation positions={NOEUDS_PITONS} liens={LIENS_PITONS} progresLien={() => 1} apparitionNoeud={() => 1} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 160, top: 250, ...TEXTE, fontWeight: 800, fontSize: 124, lineHeight: 1.1 }}>
        <MotsMontants texte="Ici," f={g} debut={262} sortie={408} />
        <br />
        <MotsMontants texte="le savoir" f={g} debut={280} decalage={6} sortie={412} />
        <br />
        <MotsMontants texte="se partage." f={g} debut={298} decalage={6} couleurs={[OR, OR]} sortie={416} />
      </div>
    </AbsoluteFill>
  );
};

// ───────────────────────────── 3. YEBA tombe du ciel ─────────────────────────────
const LETTRES = ["Y", "E", "B", "A"];
const LARGEURS = [300, 250, 285, 315];
const X0 = 960 - (LARGEURS.reduce((a, b) => a + b, 0) + 3 * 18) / 2;
const CENTRES = LARGEURS.map((w, i) => X0 + LARGEURS.slice(0, i).reduce((a, b) => a + b, 0) + i * 18 + w / 2);

export const Yeba: React.FC = () => {
  const g = useG("yeba");
  const [de, fin] = SC.yeba;
  const impact = T.impacts[0].f;
  const anticipation = p(g, 560, 38, ENTREE) * (1 - p(g, impact, 4));
  const r = aleatoire(5);
  const eclats = Array.from({ length: 46 }, () => ({ x: 380 + r() * 1160, vx: (r() - 0.5) * 22, vy: -6 - r() * 16, s: 2 + r() * 5 }));
  const tY = p(g, 752, 42, QUINT);
  return (
    <AbsoluteFill style={{ opacity: p(g, de, 22, DOUX) }}>
      <Poussieres n={60} graine={21} couleur="233,190,120" tailleMin={2} tailleMax={10} opacite={0.35} derive={0.25} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 420, textAlign: "center", ...TEXTE, fontWeight: 800, fontSize: 70, lineHeight: 1.25, opacity: 1 - p(g, 572, 20, DOUX) }}>
        <MotsMontants texte="En lingala," f={g} debut={470} />
        <br />
        <MotsMontants texte={`un seul mot dit «${NB}savoir${NB}».`} f={g} debut={492} decalage={6} couleurs={[undefined, undefined, undefined, undefined, OR]} />
      </div>
      <AbsoluteFill style={{ background: "#000", opacity: 0.55 * anticipation }} />
      <OndeDeChoc f={g} debut={impact} y={470} />
      {g >= impact &&
        eclats.map((e, i) => {
          const t = g - impact;
          const o = Math.max(0, 1 - t / 34);
          return o <= 0 ? null : (
            <div
              key={i}
              style={{
                position: "absolute",
                left: e.x + e.vx * t,
                top: 600 + e.vy * t + 0.55 * t * t,
                width: e.s,
                height: e.s,
                borderRadius: "50%",
                background: OR_CLAIR,
                opacity: o,
                boxShadow: "0 0 8px rgba(233,215,160,0.9)",
              }}
            />
          );
        })}
      {LETTRES.map((l, i) => {
        const s = spring({ frame: g - (impact - 13 + i * 3), fps: 30, config: { damping: 13, stiffness: 175, mass: 0.85 } });
        const chute = i === 0 ? 0 : p(g, 742 + i * 4, 26, ENTREE);
        const x = i === 0 ? lerp(CENTRES[0], 960, tY) : CENTRES[i];
        const echelle = i === 0 ? lerp(1, 1.45, tY) : 1;
        const lueur = impulsion(g, impact + 4, 10);
        return (
          <div
            key={l}
            style={{
              position: "absolute",
              left: x - LARGEURS[i] / 2,
              top: 300,
              width: LARGEURS[i],
              textAlign: "center",
              fontFamily: "Montserrat, sans-serif",
              fontWeight: 900,
              fontSize: 380,
              lineHeight: "380px",
              transform: `translateY(${(1 - s) * -560 + chute * 340}px) rotate(${(i - 1.5) * 9 * chute}deg) scale(${echelle})`,
              opacity: g < impact - 13 + i * 3 ? 0 : 1 - chute,
              filter: `drop-shadow(0 0 ${30 + 60 * lueur}px rgba(201,168,76,${0.35 + 0.4 * lueur}))`,
            }}
          >
            <span style={{ backgroundImage: OR_POLI, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }}>{l}</span>
            <span
              style={{
                position: "absolute",
                inset: 0,
                backgroundImage: "linear-gradient(105deg, rgba(255,255,255,0) 42%, rgba(255,250,230,0.95) 50%, rgba(255,255,255,0) 58%)",
                backgroundSize: "320% 100%",
                backgroundPosition: `${lerp(130, -40, p(g, 636 + i * 3, 40, DOUX))}% 0`,
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
                mixBlendMode: "screen",
              }}
            >
              {l}
            </span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 790, textAlign: "center", ...TEXTE, opacity: fenetre(g, 640, 760, 26, 22) }}>
        <div style={{ fontWeight: 800, fontSize: 54 }}>
          <MotsMontants texte={`«${NB}Savoir, connaître${NB}»`} f={g} debut={642} />
        </div>
        <div style={{ color: OR, fontWeight: 800, fontSize: 28, marginTop: 14 }}>
          <Resserre texte="LINGALA" f={g} debut={660} de={1.1} a={0.5} />
        </div>
      </div>
      <AbsoluteFill style={{ opacity: 1 - p(g, fin - 20, 20, DOUX), pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};

// ───────────────────────────── 4. Le baobab pousse depuis le Y ─────────────────────────────
const BX = 1440;
const BY = 905;
const BH = 780;
const feuilleGlobale = (lx: number, ly: number): [number, number] => [BX - BH / 2 + lx * (BH / 1000), BY - 0.93 * BH + ly * (BH / 1000)];

export const Baobab: React.FC = () => {
  const g = useG("baobab");
  const [de, fin] = SC.baobab;
  const tY = p(g, 770, 40, QUINT);
  const zoom = p(g, 1030, 50, ENTREE);
  const graine = feuilleGlobale(496, 342);
  const cible: [number, number] = [graine[0] + 6, graine[1] + 180];
  const sources: [number, number][] = [[270, 402], [318, 402], [496, 342], [590, 338], [656, 366], [742, 410], [208, 456], [786, 500]];
  return (
    <AbsoluteFill
      style={{
        opacity: p(g, de, 18, DOUX),
        transformOrigin: `${cible[0]}px ${cible[1]}px`,
        transform: `scale(${1 + zoom * 7})`,
        filter: `blur(${zoom * 10}px)`,
      }}
    >
      <AbsoluteFill style={{ background: `linear-gradient(180deg, ${NUIT} 0%, ${TERRE} 70%, #2A170C 100%)`, opacity: p(g, de, 60, DOUX) }} />
      <Halo x={BX} y={BY + 40} rayon={760} couleur="205,118,58" opacite={0.38 * p(g, 780, 90, DOUX)} />
      <div style={{ position: "absolute", left: lerp(960, BX, tY) - 150, top: 300, width: 300, textAlign: "center", fontFamily: "Montserrat, sans-serif", fontWeight: 900, fontSize: 380, lineHeight: "380px", transform: `scale(${lerp(1.45, 1, tY)})`, opacity: 1 - p(g, 796, 40, DOUX) }}>
        <span style={{ backgroundImage: OR_POLI, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }}>Y</span>
      </div>
      <BaobabTrace f={g} debut={788} x={BX} y={BY} hauteur={BH} vitesse={1.05} />
      {sources.map(([lx, ly], i) => {
        const [x0, y0] = feuilleGlobale(lx, ly);
        const t0 = 918 + i * 9;
        const t = g - t0;
        if (t < 0) return null;
        const y = y0 + 0.045 * t * t;
        const x = x0 + Math.sin(t * 0.09 + i) * 18;
        return (
          <div key={i} style={{ position: "absolute", left: x - 5, top: y - 5, width: 10, height: 10, borderRadius: "50%", background: OR_CLAIR, boxShadow: "0 0 14px rgba(233,215,160,0.9)", opacity: y > BY ? 0 : 1 }} />
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 330, ...TEXTE, fontWeight: 800, fontSize: 98, lineHeight: 1.1 }}>
        <MotsMontants texte="Sous le baobab," f={g} debut={858} decalage={6} />
        <br />
        <MotsMontants texte="on transmet." f={g} debut={880} decalage={6} couleurs={[OR, OR]} />
      </div>
      <div style={{ position: "absolute", left: 156, top: 600, ...TEXTE, color: GRIS, fontWeight: 700, fontSize: 30, opacity: p(g, 930, 30, DOUX) }}>
        <Resserre texte={`HISTOIRES${NB}·${NB}VÉRITÉS${NB}·${NB}GÉNÉRATIONS`} f={g} debut={930} de={0.6} a={0.28} />
      </div>
      <AbsoluteFill style={{ background: "#FFF6DA", opacity: p(g, fin - 18, 18, ENTREE) }} />
    </AbsoluteFill>
  );
};

// ───────────────────────────── 5. Le chemin : 2021 → 2026 ─────────────────────────────
export const Chemin: React.FC = () => {
  const g = useG("chemin");
  const [de, fin] = SC.chemin;
  const sortie = p(g, fin - 34, 34, ENTREE);
  const ligne = p(g, 1088, 44, EXPO);
  const point = lerp(160, 1760, p(g, 1100, 270, DOUX));
  const avant = ["Création", "Vente", "Management", `Soft${NB}skills`];
  const apres = ["IA", "RGPD", `IA${NB}Act`];
  return (
    <AbsoluteFill style={{ opacity: 1 - sortie, transform: `translateY(${-sortie * 60}px)` }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 30%, ${BLEU_NUIT} 0%, ${NUIT} 75%)` }} />
      <AbsoluteFill style={{ background: "#FFF6DA", opacity: 1 - p(g, de, 20, DOUX) }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 170, display: "flex", justifyContent: "center", ...TEXTE, fontWeight: 900, fontSize: 230 }}>
        <Odometre f={g} cibles={[[1086, "2021"], [1236, "2026"]]} taille={230} duree={44} />
      </div>
      <div style={{ position: "absolute", left: 160, top: 760, width: 1600 * ligne, height: 3, background: `linear-gradient(90deg, ${OR} 0%, ${OR_CLAIR} 100%)`, boxShadow: "0 0 18px rgba(201,168,76,0.6)" }} />
      <div style={{ position: "absolute", left: point - 9, top: 752, width: 18, height: 18, borderRadius: "50%", background: "#FFF6DA", boxShadow: "0 0 26px 8px rgba(233,215,160,0.8)", opacity: ligne }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 540, textAlign: "center", ...TEXTE, fontWeight: 800, fontSize: 64 }}>
        <span style={{ opacity: 1 - p(g, 1262, 16, DOUX) }}>
          {avant.map((m, i) => (
            <span key={m} style={{ display: "inline-block", margin: "0 22px", transform: `translateY(${lerp(40, 0, p(g, T.mots[i], 18, EXPO))}px)`, opacity: p(g, T.mots[i], 12, EXPO) }}>
              {m}
            </span>
          ))}
        </span>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 540, textAlign: "center", ...TEXTE, color: OR, fontWeight: 800, fontSize: 72 }}>
        {apres.map((m, i) => (
          <span key={m} style={{ display: "inline-block", margin: "0 30px", transform: `translateY(${lerp(50, 0, p(g, T.mots[4 + i], 18, EXPO))}px)`, opacity: p(g, T.mots[4 + i], 12, EXPO) }}>
            {m}
          </span>
        ))}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 830, textAlign: "center", ...TEXTE, fontWeight: 700, fontSize: 40, opacity: p(g, 1330, 20, DOUX) }}>
        <MotsMontants texte={`Ce soir${NB}: une nouvelle équipe.`} f={g} debut={1330} couleurs={[undefined, undefined, OR, OR, OR]} />
      </div>
    </AbsoluteFill>
  );
};

// ───────────────────────────── 6. Trois métiers, un seul interlocuteur ─────────────────────────────
const METIERS = [
  { verbe: "Former", detail: `Intra · Inter · Séminaires`, icone: "livre" },
  { verbe: "Implémenter", detail: `Workflows · Sites · Applications`, icone: "reseau" },
  { verbe: "Sécuriser", detail: `RGPD · IA${NB}Act · Audit`, icone: "bouclier" },
];

export const Metiers: React.FC = () => {
  const g = useG("metiers");
  const [de, fin] = SC.metiers;
  const sortie = p(g, fin - 40, 40, ENTREE);
  return (
    <AbsoluteFill style={{ opacity: p(g, de, 18, DOUX) * (1 - sortie) }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 0%, #15233F 0%, ${NUIT} 70%)` }} />
      <BalayageOr f={g} debut={1500} duree={44} zone={[300, 1080]} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 168, textAlign: "center", ...TEXTE, fontWeight: 800, fontSize: 70 }}>
        <MotsMontants texte={`3 métiers. 1 seul interlocuteur.`} f={g} debut={1360} couleurs={[undefined, undefined, OR, OR, OR]} />
      </div>
      {METIERS.map((m, i) => {
        const t = p(g, T.panneaux[i], 30, EXPO);
        const x = 170 + i * 540;
        return (
          <div
            key={m.verbe}
            style={{
              position: "absolute",
              left: x,
              top: 310,
              width: 500,
              height: 560,
              borderRadius: 30,
              background: "linear-gradient(160deg, #1C2333 0%, #10141D 100%)", // opaque : le reflet passe DESSOUS
              border: "1.5px solid rgba(201,168,76,0.55)",
              boxShadow: "0 30px 80px rgba(0,0,0,0.45)",
              transform: `translateY(${lerp(170, 0, t)}px) scale(${lerp(1, 0.92, sortie)})`,
              opacity: t,
              padding: "56px 44px",
              boxSizing: "border-box",
              ...TEXTE,
            }}
          >
            <Icone nom={m.icone} t={p(g, T.panneaux[i] + 18, 56, EXPO)} taille={128} />
            <div style={{ fontWeight: 800, fontSize: 58, marginTop: 40 }}>{m.verbe}</div>
            <div style={{ color: OR, fontWeight: 700, fontSize: 32, marginTop: 18, lineHeight: 1.35 }}>{m.detail}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ───────────────────────────── 7. Montage des 11 formations, sur le tempo ─────────────────────────────
export const FORMATIONS_MONTAGE: [string, string][] = [
  ["IA générative au travail", "IA AU QUOTIDIEN"],
  ["Copilot Microsoft 365", "IA AU QUOTIDIEN"],
  ["Agents IA", "IA AVANCÉE"],
  ["IA souveraine", "IA AVANCÉE"],
  ["Automatisation sans code", "IA AVANCÉE"],
  ["Site internet IA", "VISIBILITÉ"],
  ["Emailing IA", "VISIBILITÉ"],
  [`Conformité RGPD & IA${NB}Act`, "GOUVERNANCE"],
  ["Séminaire dirigeants IA", "GOUVERNANCE"],
  ["Vente & négociation", "HUMAIN"],
  ["Manager au quotidien", "HUMAIN"],
];

export const Formations: React.FC = () => {
  const g = useG("formations");
  const [de, fin] = SC.formations;
  const { debut, pas, n } = T.montage;
  const k = Math.floor((g - debut) / pas);
  const t = g - (debut + k * pas);
  const enMontage = k >= 0 && k < n;
  const valeur = Math.round(11 * p(g, T.compteur[0], T.compteur[1] - T.compteur[0], EXPO));
  const sortieCompteur = p(g, 1664, 16, ENTREE);
  const flash = enMontage ? 0.22 * Math.exp(-t / 4) : 0;
  return (
    <AbsoluteFill style={{ opacity: p(g, de, 16, DOUX) * (1 - p(g, fin - 14, 14, DOUX)) }}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 50%, rgba(201,168,76,${flash}) 0%, rgba(0,0,0,0) 55%)` }} />
      {g < 1682 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 230, textAlign: "center", ...TEXTE, opacity: (1 - sortieCompteur) * p(g, 1600, 14, DOUX), transform: `scale(${1 + sortieCompteur * 0.4})` }}>
          <div style={{ fontWeight: 900, fontSize: 360, lineHeight: "360px" }}>
            <span style={{ backgroundImage: OR_POLI, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }}>{valeur}</span>
          </div>
          <div style={{ fontWeight: 800, fontSize: 54, marginTop: 20 }}>
            <MotsMontants texte="formations au catalogue" f={g} debut={1628} />
          </div>
        </div>
      )}
      {enMontage && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 410, textAlign: "center", ...TEXTE }}>
          <div style={{ color: OR, fontWeight: 800, fontSize: 30, letterSpacing: "0.42em", opacity: Math.min(1, t / 3) }}>{FORMATIONS_MONTAGE[k][1]}</div>
          <div
            style={{
              fontWeight: 800,
              fontSize: 104,
              marginTop: 26,
              transform: `scale(${lerp(1.22, 1, p(t, 0, 10, EXPO))}) translateY(${(k % 2 === 0 ? -1 : 1) * lerp(14, 0, p(t, 0, 10, EXPO))}px)`,
              filter: `blur(${lerp(9, 0, p(t, 0, 6, EXPO))}px)`,
              opacity: Math.min(1, t / 2.5) * (1 - p(t, 12.5, 2.5, DOUX)),
              whiteSpace: "nowrap",
            }}
          >
            {FORMATIONS_MONTAGE[k][0]}
          </div>
        </div>
      )}
      {k >= 0 && (
        <div style={{ position: "absolute", left: 360, right: 360, top: 860, display: "flex", gap: 10, opacity: 1 - p(g, 1840, 10, DOUX) }}>
          {Array.from({ length: n }, (_, j) => (
            <div key={j} style={{ flex: 1, height: 6, borderRadius: 3, background: j <= k ? OR : "rgba(255,255,255,0.12)", boxShadow: j <= k ? "0 0 12px rgba(201,168,76,0.7)" : undefined }} />
          ))}
        </div>
      )}
      {g >= T.bientot - 2 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 400, textAlign: "center", ...TEXTE, opacity: p(g, T.bientot, 10, EXPO) }}>
          <span style={{ display: "inline-block", padding: "10px 28px", borderRadius: 40, border: `2px solid ${OR}`, color: OR, fontWeight: 800, fontSize: 30, letterSpacing: "0.3em" }}>BIENTÔT</span>
          <div style={{ fontWeight: 800, fontSize: 96, marginTop: 30, transform: `scale(${lerp(1.15, 1, p(g, T.bientot, 12, EXPO))})` }}>Assistant IA perso</div>
        </div>
      )}
    </AbsoluteFill>
  );
};

// ───────────────────────────── 8. La confiance se prouve : Qualiopi, NDA, horaires ─────────────────────────────
export type Certifs = { qualiopi: string; nda: string };
export const Confiance: React.FC<{
  horaires: { debut: string; pause_debut: string; pause_fin: string; fin: string; heures_par_jour: number };
  certifs: Certifs;
}> = ({ horaires, certifs }) => {
  const g = useG("confiance");
  const [de, fin] = SC.confiance;
  const sortie = p(g, fin - 40, 22, ENTREE); // panneaux partis avant les fils de la constellation finale
  const tuiles = [
    { titre: "QUALIOPI", l1: certifs.qualiopi, l2: `Actions de formation${NB}· Qualitia${NB}(COFRAC)`, petit: true },
    { titre: "NDA", l1: certifs.nda, l2: "Cet enregistrement ne vaut pas agrément de l'État.", petit: true },
    { titre: `${horaires.heures_par_jour}${NB}h${NB}/${NB}jour`, l1: `${horaires.debut}${NB}→${NB}${horaires.pause_debut}`, l2: `${horaires.pause_fin}${NB}→${NB}${horaires.fin}`, petit: false },
  ];
  return (
    <AbsoluteFill style={{ opacity: p(g, de, 18, DOUX) * (1 - sortie) }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 30% 60%, #13284A 0%, ${NUIT} 75%)` }} />
      <AnneauxSceau f={g} x={410} y={600} rayon={290} opacite={0.32 * p(g, de, 60, DOUX)} />
      <BalayageOr f={g} debut={T.scintillements[0]} duree={60} zone={[330, 1080]} />
      <div style={{ position: "absolute", left: 150, top: 170, ...TEXTE, fontWeight: 800, fontSize: 84 }}>
        <MotsMontants texte="La confiance se prouve." f={g} debut={1878} couleurs={[undefined, undefined, OR, OR]} />
      </div>
      {tuiles.map((u, i) => {
        const t = p(g, T.tuiles_confiance[i], 30, EXPO);
        return (
          <div
            key={u.titre}
            style={{
              position: "absolute",
              left: 150 + i * 550,
              top: 360,
              width: 520,
              height: 440,
              borderRadius: 28,
              background: "linear-gradient(160deg, #18294A 0%, #0D1A31 100%)",
              border: "1.5px solid rgba(201,168,76,0.55)",
              boxShadow: "0 30px 80px rgba(0,0,0,0.5)",
              padding: "50px 40px",
              boxSizing: "border-box",
              transform: `translateY(${lerp(140, 0, t) + sortie * 90}px)`,
              opacity: t,
              ...TEXTE,
            }}
          >
            <div style={{ fontWeight: 900, fontSize: 78, lineHeight: 1 }}>
              <span style={{ backgroundImage: OR_POLI, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }}>{u.titre}</span>
            </div>
            <div style={{ fontWeight: 800, fontSize: u.petit ? 46 : 38, marginTop: 40, fontVariantNumeric: "tabular-nums" }}>{u.l1}</div>
            <div style={{ fontWeight: 700, fontSize: u.petit ? 27 : 38, marginTop: 18, color: u.petit ? GRIS : BLANC, lineHeight: 1.35 }}>{u.l2}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ───────────────────────────── 9. Final : le logo, le slogan, « À suivre… » ─────────────────────────────
export const Final: React.FC = () => {
  const g = useG("final");
  const [de] = SC.final;
  const impact = T.impacts[2].f;
  const conv = p(g, 2134, 40, QUINT);
  const revele = p(g, 2170, 36, EXPO);
  const lueur = impulsion(g, impact + 6, 14);
  const suivre = g >= 2328 ? (Math.floor(g / 3) % 2 === 0 || g > 2346 ? 1 : 0.25) : 0;
  return (
    <AbsoluteFill style={{ opacity: p(g, de, 20, DOUX) * (1 - p(g, 2372, 28, DOUX)) }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 38%, #1B1609 0%, ${NUIT} 70%)` }} />
      <AbsoluteFill
        style={{
          transformOrigin: "960px 520px",
          transform: `translateY(${lerp(0, -120, conv)}px) scale(${lerp(1, 0.46, conv)})`,
          opacity: 1 - p(g, 2152, 20, DOUX),
        }}
      >
        <Constellation positions={NOEUDS_PITONS} liens={LIENS_PITONS} progresLien={(i) => p(g, 2112 + i, 16, EXPO)} apparitionNoeud={(i) => p(g, 2106 + i * 0.8, 12, EXPO)} />
      </AbsoluteFill>
      <Halo x={960} y={380} rayon={560 + 260 * lueur} opacite={0.18 + 0.35 * lueur} />
      <OndeDeChoc f={g} debut={impact} y={380} rayonMax={1250} />
      <div style={{ position: "absolute", left: 960 - 330, top: 120, width: 660, clipPath: `circle(${lerp(0, 85, revele)}% at 50% 42%)`, filter: `drop-shadow(0 0 ${20 + 50 * lueur}px rgba(201,168,76,0.55))` }}>
        <Img src={staticFile("logo-yeba-fond-sombre.png")} style={{ width: 660 }} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 742, textAlign: "center", ...TEXTE, fontWeight: 800, fontSize: 50, lineHeight: 1.3 }}>
        <MotsMontants texte="Sous le baobab de la connaissance," f={g} debut={2236} decalage={4} />
        <br />
        <MotsMontants texte="les graines du savoir." f={g} debut={2258} decalage={4} couleurs={[OR, OR, OR, OR]} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 918, textAlign: "center", ...TEXTE, color: OR, fontWeight: 800, fontSize: 26, opacity: p(g, 2290, 30, DOUX) }}>
        <Resserre texte={`SAISON${NB}1${NB}·${NB}SOIRÉE DE LANCEMENT`} f={g} debut={2290} de={0.9} a={0.42} />
      </div>
      <div style={{ position: "absolute", right: 90, top: 990, ...TEXTE, fontWeight: 800, fontSize: 32, letterSpacing: "0.12em", opacity: suivre }}>À SUIVRE…</div>
    </AbsoluteFill>
  );
};

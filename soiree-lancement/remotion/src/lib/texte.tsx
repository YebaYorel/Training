import React from "react";
import { DOUX, EXPO, lerp, p } from "./motion";

/**
 * Mots qui montent un à un depuis un masque (typographie cinétique).
 * Les espaces insécables ( ) restent collés au mot.
 */
export const MotsMontants: React.FC<{
  texte: string;
  f: number;
  debut: number;
  decalage?: number;
  duree?: number;
  style?: React.CSSProperties;
  couleurs?: (string | undefined)[];
  sortie?: number;
}> = ({ texte, f, debut, decalage = 5, duree = 24, style, couleurs, sortie }) => {
  const mots = texte.split(" ");
  return (
    <span style={{ display: "inline", ...style }}>
      {mots.map((m, i) => {
        const t = p(f, debut + i * decalage, duree, EXPO);
        const s = sortie === undefined ? 0 : p(f, sortie + i * 2, 16, DOUX);
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              overflow: "hidden",
              verticalAlign: "top",
              paddingBottom: "0.12em",
              marginBottom: "-0.12em",
              marginRight: i < mots.length - 1 ? "0.26em" : 0,
            }}
          >
            <span
              style={{
                display: "inline-block",
                transform: `translateY(${lerp(105, 0, t) - s * 105}%)`,
                opacity: Math.min(1, t * 1.6) * (1 - s),
                color: couleurs?.[i],
              }}
            >
              {m}
            </span>
          </span>
        );
      })}
    </span>
  );
};

/** Texte qui « se resserre » : espacement large → normal, flou → net. */
export const Resserre: React.FC<{
  texte: string;
  f: number;
  debut: number;
  duree?: number;
  de?: number;
  a?: number;
  style?: React.CSSProperties;
}> = ({ texte, f, debut, duree = 40, de = 0.7, a = 0.32, style }) => {
  const t = p(f, debut, duree, EXPO);
  return (
    <span
      style={{
        display: "inline-block",
        letterSpacing: `${lerp(de, a, t)}em`,
        opacity: t,
        filter: `blur(${lerp(10, 0, t)}px)`,
        whiteSpace: "nowrap",
        ...style,
      }}
    >
      {texte}
    </span>
  );
};

/** Lettres qui montent une à une au-dessus d'une ligne (cartes d'épisode). */
export const LettresMontantes: React.FC<{
  texte: string;
  f: number;
  debut: number;
  decalage?: number;
  style?: React.CSSProperties;
}> = ({ texte, f, debut, decalage = 1.6, style }) => (
  <span style={{ display: "inline-block", overflow: "hidden", paddingBottom: "0.1em", whiteSpace: "nowrap", ...style }}>
    {Array.from(texte).map((c, i) => {
      const t = p(f, debut + i * decalage, 22, EXPO);
      return (
        <span
          key={i}
          style={{
            display: "inline-block",
            transform: `translateY(${lerp(110, 0, t)}%)`,
            opacity: t,
            whiteSpace: "pre",
          }}
        >
          {c}
        </span>
      );
    })}
  </span>
);

/**
 * Odomètre : chaque chiffre est une colonne 0–9 qui défile jusqu'à sa cible.
 * `cibles` : liste de [image, nombre] — le compteur roule d'une valeur à la suivante.
 */
export const Odometre: React.FC<{
  f: number;
  cibles: [number, string][];
  duree?: number;
  taille: number;
  style?: React.CSSProperties;
}> = ({ f, cibles, duree = 36, taille, style }) => {
  const nb = cibles[0][1].length;
  const hauteur = taille * 1.0;
  return (
    <div style={{ display: "flex", height: hauteur, overflow: "hidden", lineHeight: `${hauteur}px`, ...style }}>
      {Array.from({ length: nb }, (_, col) => {
        // position (en « crans ») de la colonne : interpole entre cibles successives
        let pos = 0;
        let precedent = 0;
        cibles.forEach(([image, nombre], k) => {
          const chiffre = Number(nombre[col]);
          // premier roulement : un tour complet en plus, pour l'effet compteur
          const cible = k === 0 ? chiffre + 10 : precedent + ((chiffre - (precedent % 10) + 10) % 10);
          const t = p(f, image + col * 4, duree, EXPO);
          pos = k === 0 ? cible * t : lerp(pos, cible, t);
          precedent = cible;
        });
        return (
          <div key={col} style={{ position: "relative", width: taille * 0.66, height: hauteur }}>
            <div style={{ position: "absolute", left: 0, right: 0, top: -pos * hauteur }}>
              {Array.from({ length: 40 }, (_, d) => (
                <div key={d} style={{ height: hauteur, textAlign: "center" }}>
                  {d % 10}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export const fondu = (f: number, de: number, duree = 20) => p(f, de, duree, DOUX);

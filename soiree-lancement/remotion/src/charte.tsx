import React, { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

// Charte YEBA FORMATIONS (contrastes WCAG : or sur noir 8,2:1 — blanc sur bleu 11,3:1).
export const NOIR = "#121212";
export const NUIT = "#0B0B0E";
export const BLEU = "#1B3A6B";
export const BLEU_NUIT = "#0E2140";
export const TERRE = "#1A120C";
export const OR = "#C9A84C";
export const OR_CLAIR = "#E9D7A0";
export const OR_PROFOND = "#8E7330";
export const BLANC = "#FFFFFF";
export const GRIS = "#B8BCC6";

export const TEINTES: Record<string, string> = {
  noir: NUIT,
  terre: TERRE,
  bleu: BLEU_NUIT,
  bleu_clair: BLEU,
};

/** Dégradé « or poli » pour les grands mots (rempli par background-clip: text). */
export const OR_POLI = `linear-gradient(180deg, #F6E7B0 0%, ${OR} 46%, ${OR_PROFOND} 100%)`;

const POIDS = [400, 700, 800, 900];
const css = POIDS.map(
  (w) =>
    `@font-face{font-family:Montserrat;font-weight:${w};src:url(${staticFile(
      `fonts/montserrat-latin-${w}-normal.woff2`
    )}) format('woff2');}`
).join("");

// Charge Montserrat depuis /public (aucun appel réseau) avant de rendre la première image.
export const Polices: React.FC = () => {
  const [handle] = useState(() => delayRender("Chargement Montserrat"));
  useEffect(() => {
    document.fonts.ready
      .then(() => Promise.all(POIDS.map((w) => document.fonts.load(`${w} 40px Montserrat`))))
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  return <style>{css}</style>;
};

export const POLICE: React.CSSProperties = { fontFamily: "Montserrat, sans-serif" };

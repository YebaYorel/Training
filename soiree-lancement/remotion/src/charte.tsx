import React, { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

// Charte YEBA FORMATIONS (contrastes WCAG : or sur noir 8,2:1, blanc sur bleu 11,3:1).
export const NOIR = "#121212";
export const BLEU = "#1B3A6B";
export const OR = "#C9A84C";
export const BLANC = "#FFFFFF";

const css = [400, 800, 900]
  .map(
    (w) =>
      `@font-face{font-family:Montserrat;font-weight:${w};src:url(${staticFile(
        `montserrat-latin-${w}-normal.woff2`
      )}) format('woff2');}`
  )
  .join("");

// Charge Montserrat depuis /public (aucun appel réseau) avant de rendre la première image.
export const Polices: React.FC = () => {
  const [handle] = useState(() => delayRender("Chargement Montserrat"));
  useEffect(() => {
    document.fonts.ready.then(() =>
      Promise.all([400, 800, 900].map((w) => document.fonts.load(`${w} 40px Montserrat`)))
    ).then(() => continueRender(handle));
  }, [handle]);
  return <style>{css}</style>;
};

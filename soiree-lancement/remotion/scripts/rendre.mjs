// Rendu groupé des vidéos de la soirée (Remotion), 100 % local.
//   node scripts/rendre.mjs                 → tout
//   node scripts/rendre.mjs generique ep-2  → seulement certains travaux (préfixes)
//   node scripts/rendre.mjs --images 0,600,1200 generique → images fixes de contrôle (scratch)
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ICI = path.dirname(fileURLToPath(import.meta.url));
const REMOTION = path.resolve(ICI, "..");
const RACINE = path.resolve(REMOTION, "..");
const contenu = JSON.parse(fs.readFileSync(path.join(RACINE, "contenu", "slides.json"), "utf8"));
const horaires = contenu.meta.horaires;
const SORTIE = path.join(RACINE, "dist", "videos");
fs.mkdirSync(SORTIE, { recursive: true });

// Navigateur : variable REMOTION_BROWSER, sinon Chromium « headless shell » préinstallé (environnement cloud),
// sinon Remotion télécharge le sien (poste local).
const trouverNavigateur = () => {
  if (process.env.REMOTION_BROWSER) return process.env.REMOTION_BROWSER;
  const base = "/opt/pw-browsers";
  if (!fs.existsSync(base)) return undefined;
  for (const d of fs.readdirSync(base).filter((x) => x.startsWith("chromium_headless_shell")).sort().reverse()) {
    for (const c of ["chrome-headless-shell-linux64/chrome-headless-shell", "chrome-linux/headless_shell"]) {
      const p = path.join(base, d, c);
      if (fs.existsSync(p)) return p;
    }
  }
  return undefined;
};
const browserExecutable = trouverNavigateur();

// Grain et bande-son : générés si absents (non versionnés, reproductibles à l'identique).
if (!fs.existsSync(path.join(REMOTION, "public", "grain", "grain-7.png"))) {
  execFileSync("python3", [path.join(ICI, "grain.py")], { stdio: "inherit" });
}
if (!["generique.wav", "sting.wav"].every((f) => fs.existsSync(path.join(REMOTION, "public", "audio", f)))) {
  execFileSync("python3", [path.join(REMOTION, "audio", "composer.py")], { stdio: "inherit" });
}

const travaux = [
  { nom: "preshow", id: "PreShow", props: { boucle: 600 }, muet: true, crf: 24, affiche: 300 },
  { nom: "generique", id: "Generique", props: { horaires, avecSon: true }, crf: 20, affiche: 2300, fichier: "yeba-saison1-generique" },
  ...contenu.episodes.map((e) => ({
    nom: `ep-${e.numero}`,
    id: "Episode",
    props: { numero: e.numero, titre: e.titre, sujet: e.sujet, motif: e.motif, teinte: e.teinte, avecSon: true },
    crf: 21,
    affiche: 80,
    fichier: `yeba-episode-${e.numero}`,
  })),
  { nom: "fond-ambiance-noir", id: "Ambiance", props: { teinte: "noir", boucle: 360 }, muet: true, crf: 25, affiche: 120 },
  { nom: "fond-ambiance-bleu", id: "Ambiance", props: { teinte: "bleu", boucle: 360 }, muet: true, crf: 25, affiche: 120 },
  { nom: "fond-ambiance-terre", id: "Ambiance", props: { teinte: "terre", boucle: 360 }, muet: true, crf: 25, affiche: 120 },
  { nom: "fond-cover", id: "FondCover", props: { boucle: 360 }, muet: true, crf: 24, affiche: 120 },
  { nom: "fond-baobab", id: "FondBaobab", props: {}, muet: true, crf: 23, affiche: 179 },
  { nom: "fond-journee", id: "FondJournee", props: { horaires }, muet: true, crf: 23, affiche: 179 },
  { nom: "fond-sceau", id: "FondSceau", props: { boucle: 360 }, muet: true, crf: 25, affiche: 120 },
  { nom: "fond-flux", id: "FondFlux", props: { boucle: 360 }, muet: true, crf: 25, affiche: 120 },
  { nom: "fond-bientot", id: "FondBientot", props: { boucle: 360 }, muet: true, crf: 25, affiche: 120 },
];

const args = process.argv.slice(2);
let images = null;
const iImages = args.indexOf("--images");
if (iImages >= 0) {
  images = args[iImages + 1].split(",").map(Number);
  args.splice(iImages, 2);
}
const choisis = args.length ? travaux.filter((t) => args.some((a) => t.nom.startsWith(a))) : travaux;
if (!choisis.length) {
  console.error("Aucun travail ne correspond. Noms :", travaux.map((t) => t.nom).join(", "));
  process.exit(1);
}

console.log(`Préparation du projet Remotion… (navigateur : ${browserExecutable ?? "téléchargé par Remotion"})`);
const serveUrl = await bundle({ entryPoint: path.join(REMOTION, "src", "index.ts") });

for (const t of choisis) {
  const fichier = t.fichier ?? `yeba-${t.nom}`.replace("yeba-fond-", "fond-");
  if (images) t.props = { ...t.props, avecSon: false };
  const composition = await selectComposition({ serveUrl, id: t.id, inputProps: t.props, browserExecutable });
  if (images) {
    const dossier = process.env.DOSSIER_IMAGES ?? path.join(RACINE, "..", "controle-images");
    fs.mkdirSync(dossier, { recursive: true });
    for (const frame of images.filter((x) => x < composition.durationInFrames)) {
      const out = path.join(dossier, `${t.nom}-${String(frame).padStart(4, "0")}.jpg`);
      await renderStill({ composition, serveUrl, output: out, frame, inputProps: t.props, imageFormat: "jpeg", jpegQuality: 88, browserExecutable });
    }
    console.log(`✓ images ${t.nom}`);
    continue;
  }
  const sortie = path.join(SORTIE, `${fichier}.mp4`);
  const debut = Date.now();
  await renderMedia({
    composition,
    serveUrl,
    codec: "h264",
    outputLocation: sortie,
    inputProps: t.props,
    crf: t.crf,
    muted: Boolean(t.muet),
    pixelFormat: "yuv420p",
    imageFormat: "jpeg",
    jpegQuality: 92,
    concurrency: Number(process.env.CONCURRENCE ?? 4),
    browserExecutable,
    onProgress: ({ progress }) => process.stdout.write(`\r  ${t.nom} ${(progress * 100).toFixed(0)} %   `),
  });
  await renderStill({
    composition,
    serveUrl,
    output: path.join(SORTIE, `${fichier}.jpg`),
    frame: Math.min(t.affiche, composition.durationInFrames - 1),
    inputProps: t.props,
    imageFormat: "jpeg",
    jpegQuality: 88,
    browserExecutable,
  });
  const taille = (fs.statSync(sortie).size / 1e6).toFixed(1);
  console.log(`\r✓ ${t.nom} → dist/videos/${fichier}.mp4 (${taille} Mo, ${((Date.now() - debut) / 1000).toFixed(0)} s)`);
}

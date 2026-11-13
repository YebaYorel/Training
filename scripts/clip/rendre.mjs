// Rend le clip YEBA image par image (Playwright), puis l'assemble en MP4 (ffmpeg).
// Usage : node scripts/clip/rendre.mjs generique|attente [--apercu 3,10,20]
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const { chromium } = createRequire(import.meta.url)("playwright"); // installé globalement dans la session cloud
const ici = dirname(fileURLToPath(import.meta.url));
const mode = process.argv[2] === "attente" ? "attente" : "generique";
const iApercu = process.argv.indexOf("--apercu");
const sortie = resolve(ici, "../../livrables-prives/clip");
mkdirSync(sortie, { recursive: true });
const IPS = 25;

const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(`file://${resolve(ici, "clip.html")}?mode=${mode}`);
await page.waitForFunction("window.pret === true");
const duree = await page.evaluate("window.DUREE");

if (iApercu > 0) {
  for (const t of process.argv[iApercu + 1].split(",").map(Number)) {
    await page.evaluate((x) => window.setT(x), t);
    await page.screenshot({ path: `${sortie}/apercu-${mode}-${String(t).padStart(2, "0")}.jpg`, type: "jpeg", quality: 80 });
  }
} else {
  const fichier = `${sortie}/YEBA-${mode === "attente" ? "publicite-attente-boucle-20s" : "generique-saison-1"}.mp4`;
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(IPS), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", fichier], { stdio: ["pipe", "inherit", "inherit"] });
  const fini = new Promise((ok, ko) => ff.on("close", (c) => (c === 0 ? ok() : ko(new Error(`ffmpeg ${c}`)))));
  for (let i = 0; i < duree * IPS; i++) {
    await page.evaluate((x) => window.setT(x), i / IPS);
    const img = await page.screenshot({ type: "jpeg", quality: 95 });
    if (!ff.stdin.write(img)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  await fini;
  console.log(fichier);
}
await nav.close();

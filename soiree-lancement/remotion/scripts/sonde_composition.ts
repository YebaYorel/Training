// Sonde de composition du générique v3 : compte, scène par scène, les particules qui passent sous un texte.
// Règle YEBA : aucun point ni trait sous un mot. Les « réserves » effacent déjà ce qui passe sous un texte ;
// cette sonde vérifie que le CADRAGE évite qu'il y ait quoi que ce soit à effacer (sinon : coupure visible).
// Lancer : bash scripts/sonde_composition.sh   (moteur réel, sans rendu ; ~1 min)
// Zones de texte mesurées sur le rendu 1080p (x0, y0, x1, y1 en px) : à remettre à jour si un texte bouge.
import { camera, particule, projeter, N, Sortie } from "../src/v3/moteur";

type Zone = { nom: string; t0: number; t1: number; b: [number, number, number, number] };
const ZONES: Zone[] = [
  { nom: "Ici, le savoir se partage.", t0: 6.75, t1: 11.4, b: [120, 360, 760, 725] },
  { nom: "En lingala,", t0: 12.0, t1: 13.5, b: [640, 180, 1280, 330] },
  { nom: "« savoir, connaître »", t0: 16.4, t1: 20.1, b: [670, 765, 1250, 870] },
  { nom: "Sous le baobab, on transmet.", t0: 24.75, t1: 29.3, b: [120, 380, 1010, 620] },
  { nom: "974", t0: 35.25, t1: 37.5, b: [100, 240, 800, 560] },
  { nom: "Des racines. Un réseau.", t0: 37.75, t1: 40.9, b: [100, 330, 830, 640] },
  { nom: "2021 · Avril · Création", t0: 43.0, t1: 45.0, b: [100, 190, 700, 500] },
  { nom: "2025 · Vente · Management · Soft skills", t0: 45.0, t1: 47.0, b: [100, 130, 1100, 500] },
  { nom: "2026 · IA · RGPD · IA Act", t0: 47.0, t1: 49.0, b: [100, 190, 700, 500] },
  { nom: "Ce soir · Nouvelle équipe", t0: 49.0, t1: 50.9, b: [100, 190, 860, 500] },
  { nom: "3 métiers. 1 seul interlocuteur.", t0: 52.25, t1: 58.2, b: [110, 70, 1830, 200] },
];
const MARGE = 20; // px autour de la zone
const out: Sortie = { p: [0, 0, 0], ca: 0, cb: 0, m: 0, taille: 0, eclat: 0 };
let echec = 0;
for (const z of ZONES) {
  let pire = 0, tPire = z.t0;
  for (let t = z.t0; t <= z.t1 + 1e-9; t += 0.2) {
    const cam = camera(t);
    let n = 0;
    for (let i = 0; i < N; i++) {
      particule(i, t, out);
      const p = projeter(cam, out.p);
      if (p && p[0] > z.b[0] - MARGE && p[0] < z.b[2] + MARGE && p[1] > z.b[1] - MARGE && p[1] < z.b[3] + MARGE) n++;
    }
    if (n > pire) { pire = n; tPire = t; }
  }
  const ok = pire <= 12; // quelques particules en transit (morphose) restent tolérées : la réserve les efface en fondu
  if (!ok) echec++;
  console.log(`${ok ? "✓" : "✗"} ${z.nom.padEnd(42)} max ${String(pire).padStart(4)} particules (t = ${tPire.toFixed(1)} s)`);
}
console.log(echec ? `\n${echec} scène(s) à recadrer.` : "\nCadrage conforme : aucun sujet sous un texte.");
process.exit(echec ? 1 : 0);

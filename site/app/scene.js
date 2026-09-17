/* Scène animée du héros — YEBA FORMATIONS
 *
 * Des stagiaires quittent une salle de formation : sourires, gestes vers le
 * visiteur, entraide autour d'une table. Dessinée au code, image par image.
 *
 * POURQUOI PAS DES PHOTOGRAPHIES
 * 1. Des photos de banque d'images sont le cliché du site de formation, et
 *    elles se reconnaissent au premier coup d'œil.
 * 2. Des photos de vrais stagiaires sont des DONNÉES PERSONNELLES : droit à
 *    l'image, consentement écrit de chacun, et article 9 du RGPD si un
 *    handicap y est visible. Une scène dessinée n'engage rien de tout cela.
 *
 * Carnations : six teintes réelles, réparties aléatoirement à chaque
 * chargement, sans qu'aucune ne soit traitée comme la valeur par défaut.
 */

export const CARNATIONS = ['#8D5524', '#C68642', '#E0AC69', '#F1C27D', '#5C3A21', '#A9714B'];
const VETEMENTS = ['#1B3A6B', '#2E5694', '#C9A84C', '#8A6F22', '#3D5A80', '#6B4E71'];

const hasard = (n) => Math.floor(Math.random() * n);
const choix = (liste) => liste[hasard(liste.length)];

/** Une personne : position, allure, et ce qu'elle fait. */
function personne(x, y, echelle, role) {
  return {
    x, y, echelle, role,
    peau: choix(CARNATIONS),
    habit: choix(VETEMENTS),
    phase: Math.random() * Math.PI * 2,
    vitesse: 0.6 + Math.random() * 0.5,
  };
}

/* Dessin d'une silhouette. Le style est volontairement simple et chaleureux :
   des formes pleines, une tête ronde, un sourire tracé à l'arc. */
function dessinerPersonne(ctx, p, t) {
  const e = p.echelle;
  const balance = Math.sin(t * p.vitesse + p.phase);
  const respire = Math.sin(t * 1.4 + p.phase) * 0.6;

  ctx.save();
  ctx.translate(p.x, p.y + respire);

  // Jambes — un balancement de marche pour ceux qui avancent
  const pas = p.role === 'marche' ? balance * 7 * e : 0;
  ctx.strokeStyle = '#16233B';
  ctx.lineWidth = 5 * e;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(0, 0); ctx.lineTo(-pas, 26 * e);
  ctx.moveTo(0, 0); ctx.lineTo(pas, 26 * e);
  ctx.stroke();

  // Buste
  ctx.fillStyle = p.habit;
  ctx.beginPath();
  ctx.moveTo(-11 * e, 0);
  ctx.lineTo(-9 * e, -30 * e);
  ctx.quadraticCurveTo(0, -35 * e, 9 * e, -30 * e);
  ctx.lineTo(11 * e, 0);
  ctx.closePath();
  ctx.fill();

  // Bras — le geste dépend du rôle
  ctx.strokeStyle = p.peau;
  ctx.lineWidth = 4.5 * e;
  ctx.beginPath();
  if (p.role === 'salue') {
    // Un bras levé, la main ouverte vers le visiteur
    const agite = Math.sin(t * 3 + p.phase) * 0.35;
    ctx.moveTo(-9 * e, -26 * e);
    ctx.lineTo(-16 * e, -6 * e);
    ctx.moveTo(9 * e, -26 * e);
    ctx.lineTo(20 * e + agite * 6 * e, -44 * e - agite * 4 * e);
    ctx.stroke();
    ctx.fillStyle = p.peau;
    ctx.beginPath();
    ctx.arc(21 * e + agite * 6 * e, -46 * e - agite * 4 * e, 4.6 * e, 0, Math.PI * 2);
    ctx.fill();
  } else if (p.role === 'entraide') {
    // Penché sur la table, un bras tendu vers le voisin
    ctx.moveTo(-9 * e, -26 * e);
    ctx.lineTo(-20 * e, -12 * e);
    ctx.moveTo(9 * e, -26 * e);
    ctx.lineTo(24 * e, -16 * e + balance * 2 * e);
    ctx.stroke();
  } else {
    ctx.moveTo(-9 * e, -26 * e);
    ctx.lineTo(-13 * e - balance * 4 * e, -4 * e);
    ctx.moveTo(9 * e, -26 * e);
    ctx.lineTo(13 * e + balance * 4 * e, -4 * e);
    ctx.stroke();
  }

  // Tête
  ctx.fillStyle = p.peau;
  ctx.beginPath();
  ctx.arc(0, -44 * e, 11 * e, 0, Math.PI * 2);
  ctx.fill();

  // Sourire, toujours — c'est le sujet de la scène
  ctx.strokeStyle = 'rgba(20,14,10,0.55)';
  ctx.lineWidth = 1.6 * e;
  ctx.beginPath();
  ctx.arc(0, -45 * e, 5.4 * e, 0.28 * Math.PI, 0.72 * Math.PI);
  ctx.stroke();

  // Yeux
  ctx.fillStyle = 'rgba(20,14,10,0.7)';
  ctx.beginPath();
  ctx.arc(-4 * e, -48 * e, 1.5 * e, 0, Math.PI * 2);
  ctx.arc(4 * e, -48 * e, 1.5 * e, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

/** La porte de la salle, d'où sort la lumière. */
function dessinerPorte(ctx, x, y, h, t) {
  const l = h * 0.58;
  const lueur = ctx.createLinearGradient(x, y - h, x, y);
  lueur.addColorStop(0, 'rgba(201,168,76,0.42)');
  lueur.addColorStop(1, 'rgba(201,168,76,0.06)');
  ctx.fillStyle = lueur;
  ctx.fillRect(x - l / 2, y - h, l, h);

  ctx.strokeStyle = 'rgba(201,168,76,0.75)';
  ctx.lineWidth = 2.5;
  ctx.strokeRect(x - l / 2, y - h, l, h);

  // Faisceau projeté au sol, qui respire doucement
  const pulse = 0.5 + Math.sin(t * 0.7) * 0.12;
  const sol = ctx.createLinearGradient(x, y, x, y + h * 0.5);
  sol.addColorStop(0, `rgba(201,168,76,${0.26 * pulse})`);
  sol.addColorStop(1, 'rgba(201,168,76,0)');
  ctx.fillStyle = sol;
  ctx.beginPath();
  ctx.moveTo(x - l / 2, y);
  ctx.lineTo(x - l * 1.5, y + h * 0.5);
  ctx.lineTo(x + l * 1.5, y + h * 0.5);
  ctx.lineTo(x + l / 2, y);
  ctx.closePath();
  ctx.fill();
}

/** La table de travail autour de laquelle on s'entraide. */
function dessinerTable(ctx, x, y, larg) {
  ctx.fillStyle = 'rgba(27,58,107,0.85)';
  ctx.beginPath();
  ctx.ellipse(x, y, larg, larg * 0.22, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = 'rgba(201,168,76,0.5)';
  ctx.lineWidth = 2;
  ctx.stroke();
  // Deux feuilles posées dessus
  ctx.fillStyle = 'rgba(238,242,250,0.9)';
  ctx.fillRect(x - larg * 0.34, y - larg * 0.1, larg * 0.26, larg * 0.17);
  ctx.fillRect(x + larg * 0.06, y - larg * 0.06, larg * 0.24, larg * 0.15);
}

/**
 * Démarre la scène. Retourne une fonction d'arrêt.
 * Si le visiteur a demandé moins d'animations, une image fixe est rendue.
 */
export function demarrerScene(canvas, { anime = true } = {}) {
  const ctx = canvas.getContext('2d');
  let personnes = [], w = 0, h = 0, brut = null, t0 = performance.now();

  function composer() {
    const r = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = r.width; h = r.height;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const e = Math.min(1.5, Math.max(0.62, w / 1100));
    const sol = h * 0.86;
    personnes = [];

    // Le groupe qui sort de la salle et avance vers le visiteur
    personnes.push(personne(w * 0.26, sol - 6, e * 0.9, 'marche'));
    personnes.push(personne(w * 0.33, sol + 6, e * 1.05, 'salue'));
    personnes.push(personne(w * 0.41, sol - 2, e * 0.95, 'marche'));
    personnes.push(personne(w * 0.19, sol + 2, e * 0.8, 'salue'));

    // Le groupe attablé, qui s'entraide
    if (w > 700) {
      personnes.push(personne(w * 0.71, sol - 4, e * 0.88, 'entraide'));
      personnes.push(personne(w * 0.82, sol - 4, e * 0.88, 'entraide'));
      personnes.push(personne(w * 0.765, sol - 26, e * 0.72, 'entraide'));
    }
  }

  function rendre(ms) {
    const t = (ms - t0) / 1000;
    ctx.clearRect(0, 0, w, h);
    const sol = h * 0.86;

    dessinerPorte(ctx, w * 0.33, sol, Math.min(h * 0.62, 260), anime ? t : 0);
    if (w > 700) dessinerTable(ctx, w * 0.765, sol + 4, Math.min(w * 0.1, 110));

    // Les personnes attablées passent derrière la table, les autres devant
    personnes
      .slice()
      .sort((a, b) => a.y - b.y)
      .forEach((p) => dessinerPersonne(ctx, p, anime ? t : 1.2));

    if (anime) brut = requestAnimationFrame(rendre);
  }

  composer();
  rendre(performance.now());

  let minuteur;
  const auRedimensionnement = () => {
    clearTimeout(minuteur);
    minuteur = setTimeout(() => {
      if (brut) cancelAnimationFrame(brut);
      composer();
      t0 = performance.now();
      rendre(t0);
    }, 180);
  };
  window.addEventListener('resize', auRedimensionnement);

  return function arreter() {
    if (brut) cancelAnimationFrame(brut);
    clearTimeout(minuteur);
    window.removeEventListener('resize', auRedimensionnement);
  };
}

/* Générateur de séance : à partir des objectifs REAC planifiés pour une journée,
 * Claude rédige le contenu (via la capacité « sample » de la page, sur le compte
 * du formateur), puis la page fabrique : PowerPoint de séance, exercices
 * apprenants, ressource de fin de journée, grille critériée (5 objectifs),
 * quiz de 10 questions (document formateur) et fiche de séance (preuve).
 * Sans Claude, une version de base est construite à partir du REAC. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const D = G.Decorticage;

  function matiere(ctx, jour) {
    const reac = ctx.reac, cps = [...new Set(jour.seances.map((s) => s.cp).filter(Boolean))];
    const objectifs = [], vus = new Set();
    for (const l of jour.lignes) {
      if (vus.has(l.objectif)) continue;
      vus.add(l.objectif);
      objectifs.push({ seance: `S${l.seance.numero} — ${l.seance.titre}`, objectif: l.objectif.texte, bloom: D.NIVEAUX_BLOOM[l.objectif.niveau],
        contenus: l.objectif.contenus.slice(0, 6), criteres: l.objectif.criteres.slice(0, 4), activite: l.objectif.activite, exemple: l.objectif.exemple, minutes: l.minutes });
    }
    return {
      formation: ctx.titre, niveau: reac.niveau ? `Niveau ${reac.niveau}` : "", date: jour.date, duree_minutes: jour.minutes,
      horaires: `${D.fmtHm(jour.lignes[0].debut)} – ${D.fmtHm(jour.lignes[jour.lignes.length - 1].fin)}`,
      competences: cps.map((n) => { const c = reac.competence(n); return { code: `CP${n}`, intitule: c.intitule, criteres: c.criteres }; }),
      objectifs,
    };
  }

  function consigne(m, public_) {
    return `Tu es un ingénieur pédagogique expert de la formation professionnelle des adultes à La Réunion (titres professionnels du ministère du Travail).
Prépare la séance de formation complète décrite ci-dessous, pour le formateur. Écris en français simple, concret, bienveillant.

PUBLIC : ${public_ || "adultes en formation qualifiante ou en apprentissage, niveaux hétérogènes, à La Réunion"}.
PÉDAGOGIE IMPOSÉE :
- Objectifs commençant par un verbe d'action de la taxonomie de Bloom, repris des termes du REAC.
- Démarche de Bruner : déroulé selon les 6 fonctions d'étayage (enrôlement, réduction des degrés de liberté, maintien de l'orientation, signalisation des caractéristiques déterminantes, contrôle de la frustration, démonstration) et passage enactif → iconique → symbolique.
- Les apprenants sont EN MOUVEMENT : ils comprennent en faisant, en jouant un rôle, en s'amusant, en s'interrogeant, en comparant. Exercices très simples à animer, sans matériel coûteux.
- Exemples tirés de La Réunion (commerces, saisons, cyclones, fret, octroi de mer, événements locaux) quand c'est pertinent.
- Diapositives : MOTS-CLÉS uniquement, jamais de phrases ; 5 mots-clés maximum par diapositive, 4 mots maximum par mot-clé (lisible par un public malvoyant).
- Citation : seulement si tu es CERTAIN de l'auteur ; sinon un proverbe sans auteur, ou rien.
- Images et vidéos : ne donne AUCUNE adresse web ; donne seulement des mots de recherche (pour des banques libres de droits) et le type de média.
- Aucune donnée personnelle.

SÉANCE (données du décorticage REAC) :
${JSON.stringify(m, null, 1)}

Réponds UNIQUEMENT par un objet JSON de cette forme exacte :
{"titre":"titre court de la séance","accroche":"question ou situation d'accroche (1 phrase)","citation":{"texte":"","auteur":""},
"objectifs_seance":["5 objectifs de séance, verbe d'action en tête, qui répondent aux objectifs REAC ci-dessus"],
"deroule":[{"debut":"08h30","fin":"09h00","phase":"Enrôlement","activite":"…","modalite":"individuel|binôme|groupe|plénière","objectif":1}],
"diapositives":[{"titre":"2 à 5 mots","mots_cles":["…"],"schema":{"type":"etapes|cycle|comparaison|aucun","elements":["…"]},"notes":"ce que dit le formateur (2-4 phrases)","illustration":"mots de recherche d'image"}],
"exercices":[{"titre":"…","verbe":"faire|être|jouer|s'interroger|comparer","duree_minutes":20,"modalite":"…","consigne":"consigne courte pour les apprenants","etapes":["…"],"materiel":"…","objectif":1,"corrige":"éléments de réponse pour le formateur"}],
"ressource":{"introduction":"…","sections":[{"titre":"…","texte":"3 à 6 phrases simples","points_cles":["…"]}],"schema":{"titre":"…","type":"etapes|cycle|comparaison","elements":["…"]},"tableau":{"titre":"…","entetes":["…"],"lignes":[["…"]]},"a_retenir":["…"],"medias":[{"type":"vidéo|image|lecture","titre":"…","recherche":"mots de recherche"}]},
"grille":[{"objectif":"objectif de séance n°1","criteres":["3 critères observables"],"niveaux":{"non_acquis":"…","en_cours":"…","acquis":"…","maitrise":"…"}}],
"quiz":[{"question":"…","choix":["A","B","C","D"],"bonne":0,"explication":"…","objectif":1}]}
Quantités : 10 à 14 diapositives, 4 à 6 exercices de types variés, 3 à 5 sections dans la ressource, EXACTEMENT 5 objectifs et 5 lignes de grille, EXACTEMENT 10 questions de quiz. Le déroulé couvre toute la durée (${m.horaires}), pauses comprises.`;
  }

  const tab = (x) => (Array.isArray(x) ? x : []);
  const txt = (x, max = 400) => String(x ?? "").replace(/\s+/g, " ").trim().slice(0, max);
  function normaliser(r, m) {
    const o = r && typeof r === "object" ? r : {};
    const objs = tab(o.objectifs_seance).map((x) => txt(x, 200)).filter(Boolean);
    const base = m.objectifs.map((x) => x.objectif);
    while (objs.length < 5 && base.length) objs.push(base[objs.length % base.length]);
    const pack = {
      titre: txt(o.titre, 120) || m.objectifs[0]?.seance || "Séance", accroche: txt(o.accroche, 300),
      citation: o.citation && txt(o.citation.texte) ? { texte: txt(o.citation.texte, 250), auteur: txt(o.citation.auteur, 80) } : null,
      objectifs_seance: objs.slice(0, 5),
      deroule: tab(o.deroule).slice(0, 20).map((d) => ({ debut: txt(d.debut, 8), fin: txt(d.fin, 8), phase: txt(d.phase, 60), activite: txt(d.activite, 400), modalite: txt(d.modalite, 40), objectif: +d.objectif || 1 })),
      diapositives: tab(o.diapositives).slice(0, 18).map((d) => ({ titre: txt(d.titre, 60), mots_cles: tab(d.mots_cles).slice(0, 5).map((x) => txt(x, 40)).filter(Boolean),
        schema: d.schema && tab(d.schema.elements).length ? { type: txt(d.schema.type, 20), elements: tab(d.schema.elements).slice(0, 6).map((x) => txt(x, 40)) } : null,
        notes: txt(d.notes, 900), illustration: txt(d.illustration, 80) })).filter((d) => d.titre),
      exercices: tab(o.exercices).slice(0, 8).map((e) => ({ titre: txt(e.titre, 100), verbe: txt(e.verbe, 30), duree_minutes: +e.duree_minutes || 20, modalite: txt(e.modalite, 60),
        consigne: txt(e.consigne, 600), etapes: tab(e.etapes).slice(0, 8).map((x) => txt(x, 300)), materiel: txt(e.materiel, 200), objectif: +e.objectif || 1, corrige: txt(e.corrige, 900) })),
      ressource: (() => { const rs = o.ressource || {};
        return { introduction: txt(rs.introduction, 800), sections: tab(rs.sections).slice(0, 6).map((s) => ({ titre: txt(s.titre, 100), texte: txt(s.texte, 1500), points_cles: tab(s.points_cles).slice(0, 6).map((x) => txt(x, 200)) })),
          schema: rs.schema && tab(rs.schema.elements).length ? { titre: txt(rs.schema.titre, 100), type: txt(rs.schema.type, 20), elements: tab(rs.schema.elements).slice(0, 8).map((x) => txt(x, 60)) } : null,
          tableau: rs.tableau && tab(rs.tableau.entetes).length ? { titre: txt(rs.tableau.titre, 100), entetes: tab(rs.tableau.entetes).slice(0, 5).map((x) => txt(x, 60)), lignes: tab(rs.tableau.lignes).slice(0, 12).map((l) => tab(l).slice(0, 5).map((x) => txt(x, 200))) } : null,
          a_retenir: tab(rs.a_retenir).slice(0, 8).map((x) => txt(x, 200)), medias: tab(rs.medias).slice(0, 8).map((x) => ({ type: txt(x.type, 20), titre: txt(x.titre, 120), recherche: txt(x.recherche, 80) })) }; })(),
      grille: tab(o.grille).slice(0, 5).map((g, i) => ({ objectif: txt(g.objectif, 200) || objs[i], criteres: tab(g.criteres).slice(0, 4).map((x) => txt(x, 200)),
        niveaux: Object.assign({ non_acquis: "", en_cours: "", acquis: "", maitrise: "" }, g.niveaux || {}) })),
      quiz: tab(o.quiz).slice(0, 10).map((q) => ({ question: txt(q.question, 300), choix: tab(q.choix).slice(0, 4).map((x) => txt(x, 200)), bonne: Math.max(0, Math.min(3, +q.bonne || 0)), explication: txt(q.explication, 400), objectif: +q.objectif || 1 }))
        .filter((q) => q.question && q.choix.length >= 2),
    };
    return pack;
  }

  // Version de base, sans Claude : construite à partir du REAC (à enrichir par le formateur)
  function versionDeBase(m) {
    const o = m.objectifs;
    const objs = [...new Set(o.map((x) => x.objectif))].slice(0, 5);
    // moins de 5 objectifs REAC dans la journée : on complète par des objectifs de consolidation (jamais de doublon)
    const complements = ["Expliquer avec ses mots l'essentiel de la journée", "Appliquer les acquis du jour à une situation de son entreprise",
      "Comparer sa pratique actuelle avec les repères vus en séance", "Identifier un point fort et un axe de progrès personnels", "Restituer les mots-clés de la séance"];
    for (const c of complements) if (objs.length < 5) objs.push(c);
    return {
      titre: o[0] ? o[0].seance.replace(/^S\d+ — /, "") : "Séance", accroche: (o.find((x) => x.exemple) || {}).exemple || "Qu'avez-vous déjà vécu en entreprise sur ce thème ?",
      citation: null, objectifs_seance: objs,
      deroule: [{ debut: m.horaires.split(" – ")[0], fin: "", phase: "Enrôlement", activite: "Accroche et rappel de la séance précédente (spirale)", modalite: "plénière", objectif: 1 }]
        .concat(o.map((x, i) => ({ debut: "", fin: "", phase: D.ETAYAGE[(i % 5) + 1][0], activite: x.activite, modalite: "binôme", objectif: Math.min(5, i + 1) }))),
      diapositives: o.map((x) => ({ titre: x.objectif.split(" ").slice(0, 5).join(" "), mots_cles: D.motsCles(x.objectif + " " + x.contenus.join(" "), 5), schema: null, notes: x.contenus.join(" ; "), illustration: D.motsCles(x.objectif, 2).join(" ") })),
      exercices: o.slice(0, 5).map((x, i) => ({ titre: `Exercice ${i + 1}`, verbe: "faire", duree_minutes: 20, modalite: "binôme", consigne: x.activite, etapes: [], materiel: "", objectif: Math.min(5, i + 1), corrige: x.contenus.join(" ; ") })),
      ressource: { introduction: `Cette fiche reprend l'essentiel de la journée du ${D.fr(D.lireDate(m.date))}.`, sections: o.map((x) => ({ titre: x.objectif, texte: "", points_cles: x.contenus })),
        schema: null, tableau: { titre: "Récapitulatif", entetes: ["Objectif", "Mots-clés"], lignes: o.map((x) => [x.objectif, D.motsCles(x.objectif, 4).join(", ")]) }, a_retenir: o.map((x) => x.objectif), medias: [] },
      grille: objs.map((x, i) => ({ objectif: x, criteres: (o[i] && o[i].criteres.length ? o[i].criteres : m.competences.flatMap((c) => c.criteres)).slice(0, 3),
        niveaux: { non_acquis: "Ne réalise pas", en_cours: "Réalise avec aide", acquis: "Réalise seul", maitrise: "Réalise et explique / transfère" } })),
      quiz: Array.from({ length: 10 }, (_, i) => {
        const x = o[i % Math.max(1, o.length)] || { objectif: objs[i % 5], contenus: [] }, n = (objs.indexOf(x.objectif) + 1) || (i % 5) + 1;
        const modeles = [`Citez deux éléments clés pour : ${x.objectif.toLowerCase()}`, `Donnez un exemple concret vécu en entreprise pour : ${x.objectif.toLowerCase()}`,
          `Quelle erreur fréquente faut-il éviter pour : ${x.objectif.toLowerCase()} ?`, `Expliquez à un nouveau collègue comment : ${x.objectif.toLowerCase()}`];
        return { question: modeles[Math.floor(i / Math.max(1, o.length)) % 4], choix: ["Réponse ouverte"], bonne: 0, explication: x.contenus.join(" ; ") || "Voir la ressource de la journée", objectif: Math.min(5, n) };
      }),
      _base: true,
    };
  }

  async function rediger(ctx, jour, opts = {}) {
    const m = matiere(ctx, jour);
    const sample = window.claude && typeof window.claude.use === "function" ? await window.claude.use("sample") : null;
    if (!sample) return { pack: versionDeBase(m), matiere: m, source: "base", raison: "Claude n'est pas disponible dans cet affichage" };
    try {
      const r = await sample.json(consigne(m, opts.public), { modelTier: "default", signal: opts.signal, cache: false, onText: opts.onText });
      const pack = normaliser(r, m);
      if (!pack.diapositives.length || pack.quiz.length < 5) throw { code: "incomplet" };
      return { pack, matiere: m, source: "claude" };
    } catch (e) {
      if (e && e.code === "cancelled") throw e;
      return { pack: versionDeBase(m), matiere: m, source: "base", raison: e && e.code ? `réponse de Claude indisponible (${e.code})` : "réponse de Claude inutilisable" };
    }
  }

  // ------------------------------------------------------------- PowerPoint
  function powerpoint(ctx, jour, pack, logo) {
    const c = ctx.charte, pptx = new G.PptxGenJS();
    pptx.layout = "LAYOUT_WIDE";            // 13,33 × 7,5 pouces
    pptx.author = ctx.nomOrg || ""; pptx.company = ctx.nomOrg || ""; pptx.title = pack.titre;
    const F = c.police || "Arial", FT = c.police_titres || F, P1 = c.couleur_primaire, P2 = c.couleur_secondaire, CL = c.couleur_claire, TX = c.couleur_texte;
    const A2 = D.accentTexte(c);              // accent lisible en texte sur fond blanc (l'or n'y atteint pas 4,5:1)
    // largeur moyenne d'un caractère gras, en fraction de la taille : Montserrat est large, on prend de la marge
    const chasse = (f) => (/montserrat/i.test(f) ? 0.68 : /inter/i.test(f) ? 0.62 : 0.58);
    const pied = `${ctx.nomOrg ? ctx.nomOrg + " · " : ""}${D.fr(D.lireDate(jour.date))}`;
    pptx.defineSlideMaster({ title: "YEBA", background: { color: "FFFFFF" },
      objects: [{ rect: { x: 0, y: 0, w: 13.33, h: 0.22, fill: { color: P1 } } },
        { text: { text: pied, options: { x: 0.4, y: 6.95, w: 9, h: 0.4, fontFace: F, fontSize: 14, color: "5B6B7C" } } }],
      slideNumber: { x: 12.3, y: 6.95, w: 0.8, h: 0.4, fontFace: F, fontSize: 14, color: "5B6B7C" } });
    /* Taille de police qui fait tenir le texte dans la boîte SANS couper un mot :
     * le mot le plus long doit tenir sur une ligne, et toutes les lignes dans la hauteur. */
    const taille = (texte, w, h, max, min = 18, police = F) => {
      const mots = String(texte).split(/\s+/).filter(Boolean);
      for (let fs = max; fs >= min; fs -= 2) {
        const parLigne = Math.floor(((w - 0.3) * 72) / (fs * chasse(police)));
        if (Math.max(...mots.map((m) => m.length), 1) > parLigne) continue;
        let lignes = 1, cour = 0;
        for (const m of mots) { if (cour && cour + 1 + m.length > parLigne) { lignes++; cour = m.length; } else cour += (cour ? 1 : 0) + m.length; }
        if (lignes * fs * 1.25 / 72 <= h - 0.15) return fs;
      }
      return min;
    };
    const texte = (s, t, o) => s.addText(t, Object.assign({ fontFace: o.fontFace || F, valign: "middle", margin: 8, fontSize: taille(t, o.w, o.h, o.max || 32, o.min || 18, o.fontFace || F) }, o));
    const nouvelle = (titre) => {
      const s = pptx.addSlide({ masterName: "YEBA" });
      if (titre) texte(s, titre, { x: 0.5, y: 0.45, w: 12.3, h: 1.1, max: 40, min: 28, bold: true, color: P1, fontFace: FT });
      return s;
    };
    const puces = (s, mots, y = 1.8) => {
      const n = Math.max(mots.length, 1), h = Math.min(1.0, 4.6 / n - 0.15);
      mots.forEach((m, i) => texte(s, m, { x: 0.9, y: y + i * (h + 0.18), w: 11.5, h, max: 32, min: 22, bold: true, color: TX,
        fill: { color: CL }, rectRadius: 0.12, shape: pptx.ShapeType.roundRect, margin: 14 }));
    };
    const schema = (s, sc, y = 1.9) => {
      const el = sc.elements.slice(0, 6), n = el.length;
      if (sc.type === "comparaison" && n >= 2) {
        const moitie = Math.ceil(n / 2);
        [el.slice(0, moitie), el.slice(moitie)].forEach((col, k) => col.forEach((t, i) => texte(s, t, { x: 0.8 + k * 6.1, y: y + i * 1.15, w: 5.7, h: 0.95, max: 28, min: 18,
          bold: true, color: k ? D.texteSur(P1, c) : TX, fill: { color: k ? P1 : CL }, shape: pptx.ShapeType.roundRect, rectRadius: 0.1, align: "center" })));
        return;
      }
      // Étapes / cycle : blocs séparés par une flèche placée ENTRE les blocs (jamais sur le texte)
      const fl = 0.45, w = (12.2 - (n - 1) * fl) / n;
      const fs = Math.min(...el.map((t) => taille(t, w, 1.7, 28, 16)));
      const fond = (i) => (i % 2 ? P2 : P1);
      el.forEach((t, i) => {
        const x = 0.55 + i * (w + fl);
        s.addText(t, { x, y: y + 0.5, w, h: 1.7, fontFace: F, fontSize: fs, bold: true, color: D.texteSur(fond(i), c), fill: { color: fond(i) },
          shape: pptx.ShapeType.roundRect, rectRadius: 0.12, align: "center", valign: "middle", margin: 8 });
        if (i < n - 1) s.addText(sc.type === "cycle" && i === n - 2 ? "→" : "→", { x: x + w, y: y + 0.5, w: fl, h: 1.7, fontFace: F, fontSize: 30, bold: true, color: P1, align: "center", valign: "middle", margin: 0 });
      });
      if (sc.type === "cycle") s.addText("↺ et on recommence", { x: 0.55, y: y + 2.35, w: 12.2, h: 0.6, fontFace: F, fontSize: 22, color: P1, align: "center", valign: "middle" });
    };
    // 1. Titre
    let s = pptx.addSlide();
    s.background = { color: P1 };
    texte(s, pack.titre, { x: 0.7, y: 1.6, w: 11.9, h: 2.2, max: 48, min: 30, bold: true, color: D.texteSur(P1, c), fontFace: FT });
    s.addText(`${ctx.titre}\n${D.JOURS[D.jourSem(D.lireDate(jour.date))]} ${D.fr(D.lireDate(jour.date))} · ${jour.lignes.length ? D.fmtHm(jour.lignes[0].debut) + "–" + D.fmtHm(jour.lignes[jour.lignes.length - 1].fin) : ""}`,
      { x: 0.7, y: 4.1, w: 11.9, h: 1.4, fontFace: F, fontSize: 24, color: D.texteSur(P1, c), valign: "top" });
    if (ctx.nomOrg) s.addText(ctx.nomOrg, { x: 0.7, y: 6.3, w: 8, h: 0.6, fontFace: FT, fontSize: 20, bold: true, color: D.contraste(P2, P1) >= 4.5 ? P2 : D.texteSur(P1, c) });
    if (logo) s.addImage({ data: logo.dataURL, x: 11.2, y: 0.4, w: 1.6 * Math.min(1.6, logo.ratio), h: 1.6, sizing: { type: "contain", w: 1.6 * Math.min(1.6, logo.ratio), h: 1.6 } });
    // 2. Objectifs
    s = nouvelle("Objectifs de la séance");
    pack.objectifs_seance.forEach((o, i) => {
      const v = D.verbeInitial(o), reste = o.slice(v.length);
      s.addText([{ text: v.toUpperCase(), options: { bold: true, color: A2 } }, { text: reste, options: { color: TX } }],
        { x: 0.8, y: 1.75 + i * 0.98, w: 11.8, h: 0.88, fontFace: F, fontSize: taille(o, 11.8, 0.88, 26, 18), valign: "middle" });
    });
    // 3. Accroche
    if (pack.accroche) {
      s = nouvelle("Pour commencer");
      texte(s, pack.accroche, { x: 0.9, y: 1.9, w: 11.5, h: 3.2, max: 36, min: 24, bold: true, color: P1, fill: { color: CL }, shape: pptx.ShapeType.roundRect, rectRadius: 0.15, margin: 24, align: "center" });
      if (pack.citation) { const ci = `« ${pack.citation.texte} »${pack.citation.auteur ? " — " + pack.citation.auteur : ""}`; texte(s, ci, { x: 0.9, y: 5.4, w: 11.5, h: 1.2, max: 24, min: 18, italic: true, color: "4B5967", align: "center" }); }
    }
    // 4. Diapositives de contenu
    for (const d of pack.diapositives) {
      s = nouvelle(d.titre);
      if (d.schema && d.schema.type !== "aucun") { schema(s, d.schema, 1.7); if (d.mots_cles.length) texte(s, d.mots_cles.slice(0, 3).join("  ·  "), { x: 0.8, y: 5.6, w: 11.8, h: 0.9, max: 28, min: 20, bold: true, color: P1, align: "center" }); }
      else puces(s, d.mots_cles);
      const medias = d.illustration ? `\n\nIllustration libre de droits à chercher : « ${d.illustration} » (Pixabay, Wikimedia Commons, Unsplash — vérifier la licence).` : "";
      s.addNotes((d.notes || "") + medias);
    }
    // 5. Exercices
    for (const e of pack.exercices) {
      s = nouvelle(`À vous ! ${e.titre}`);
      texte(s, e.consigne, { x: 0.8, y: 1.75, w: 11.8, h: 2.6, max: 32, min: 22, color: TX, valign: "top" });
      texte(s, `${e.duree_minutes} min · ${e.modalite || ""}`.trim(), { x: 0.8, y: 4.6, w: 5.5, h: 0.9, max: 28, min: 18, bold: true, color: D.texteSur(P2, c), fill: { color: P2 }, shape: pptx.ShapeType.roundRect, rectRadius: 0.1, align: "center" });
      if (e.materiel) texte(s, `Matériel : ${e.materiel}`, { x: 6.6, y: 4.6, w: 6, h: 0.9, max: 22, min: 16, color: "4B5967" });
      s.addNotes([...e.etapes.map((x, i) => `${i + 1}. ${x}`), e.corrige ? "Éléments de réponse : " + e.corrige : ""].filter(Boolean).join("\n"));
    }
    // 6. À retenir
    s = nouvelle("À retenir");
    puces(s, (pack.ressource.a_retenir.length ? pack.ressource.a_retenir : pack.objectifs_seance).slice(0, 5).map((x) => x.split(" ").slice(0, 7).join(" ")));
    s = nouvelle("Questions ?");
    texte(s, "Quiz et évaluation de la séance", { x: 0.9, y: 2.4, w: 11.5, h: 2, max: 40, bold: true, color: P1, align: "center" });
    return pptx.write({ outputType: "blob" });
  }

  // ---------------------------------------------------------------- Word
  const docCtx = (ctx, logo) => Object.assign({}, ctx, { logo });
  const recherche = (q) => [
    ["Pixabay (images libres)", `https://pixabay.com/fr/images/search/${encodeURIComponent(q)}/`],
    ["Wikimedia Commons", `https://commons.wikimedia.org/w/index.php?search=${encodeURIComponent(q)}`],
    ["YouTube (vidéos)", `https://www.youtube.com/results?search_query=${encodeURIComponent(q)}`]];

  function exercicesDocx(ctx, jour, pack, logo) {
    return D.docWord(docCtx(ctx, logo), `Exercices — ${pack.titre}`, (o) => {
      o.p(`${ctx.titre} · ${D.fr(D.lireDate(jour.date))}`);
      pack.exercices.forEach((e, i) => {
        o.h2(`${i + 1}. ${e.titre} (${e.duree_minutes} min${e.modalite ? ", " + e.modalite : ""})`);
        o.p(e.consigne);
        e.etapes.forEach((x) => o.puce(x));
        if (e.materiel) o.p(`Matériel : ${e.materiel}`);
        o.p(`Objectif travaillé : ${pack.objectifs_seance[e.objectif - 1] || ""}`);
      });
    });
  }
  function ressourceDocx(ctx, jour, pack, logo) {
    const r = pack.ressource;
    return D.docWord(docCtx(ctx, logo), `L'essentiel de la journée — ${pack.titre}`, (o) => {
      o.p(`${ctx.titre} · ${D.fr(D.lireDate(jour.date))}`);
      if (r.introduction) o.p(r.introduction);
      o.encadre("Ce que vous savez faire maintenant", pack.objectifs_seance);
      for (const s of r.sections) { o.h2(s.titre); if (s.texte) o.p(s.texte); s.points_cles.forEach((x) => o.puce(x)); }
      if (r.schema) { o.h2(r.schema.titre || "Schéma"); o.tableau([r.schema.elements.map((_, i) => (r.schema.type === "comparaison" ? (i % 2 ? "B" : "A") : `Étape ${i + 1}`)), r.schema.elements.map((x, i) => (i < r.schema.elements.length - 1 && r.schema.type !== "comparaison" ? x + "  →" : x))]); }
      if (r.tableau && r.tableau.lignes.length) { o.h2(r.tableau.titre || "Tableau récapitulatif"); o.tableau([r.tableau.entetes].concat(r.tableau.lignes)); }
      if (r.a_retenir.length) o.encadre("À retenir", r.a_retenir);
      if (r.medias.length) {
        o.h2("Pour aller plus loin (ressources libres)");
        for (const m of r.medias) { o.p(`${m.type ? m.type[0].toUpperCase() + m.type.slice(1) : "Ressource"} : ${m.titre}`); const [lib, url] = recherche(m.recherche || m.titre)[m.type === "vidéo" ? 2 : 0]; o.lien(`→ Rechercher sur ${lib} : « ${m.recherche || m.titre} »`, url); }
        o.p("Vérifiez la licence de chaque média avant de le diffuser.");
      }
    });
  }
  function grilleDocx(ctx, jour, pack, logo) {
    return D.docWord(docCtx(ctx, logo), `Grille critériée — ${pack.titre}`, (o) => {
      o.p(`${ctx.titre} · ${D.fr(D.lireDate(jour.date))} · Apprenant : ……………………………`);
      o.tableau([["Objectif de séance", "Critères observables", "Non acquis", "En cours", "Acquis", "Maîtrisé"]].concat(pack.grille.map((g) =>
        [g.objectif, g.criteres.map((c) => "• " + c).join("\n"), "☐ " + (g.niveaux.non_acquis || ""), "☐ " + (g.niveaux.en_cours || ""), "☐ " + (g.niveaux.acquis || ""), "☐ " + (g.niveaux.maitrise || "")])));
      o.p("Compétences REAC visées : " + [...new Set(jour.seances.map((s) => s.cp).filter(Boolean))].map((n) => `CP${n} — ${ctx.reac.competence(n).intitule}`).join(" ; "));
      o.p("Signature du formateur :                                  Signature de l'apprenant :");
    });
  }
  function quizDocx(ctx, jour, pack, logo) {
    const L = "ABCD";
    return D.docWord(docCtx(ctx, logo), `Quiz — ${pack.titre} — DOCUMENT FORMATEUR`, (o) => {
      o.encadre("Document réservé au formateur", ["Contient les réponses : ne pas distribuer.", "Version apprenant : recopier les questions sans les réponses."]);
      pack.quiz.forEach((q, i) => {
        o.h2(`Question ${i + 1}`);
        o.p(q.question);
        if (q.choix.length > 1) q.choix.forEach((c, k) => o.puce(`${L[k]}. ${c}${k === q.bonne ? "   ✔ BONNE RÉPONSE" : ""}`));
        else o.p("Question ouverte (réponse orale ou écrite).");
        if (q.explication) o.p(`${q.choix.length > 1 ? "Explication" : "Éléments de réponse attendus"} : ${q.explication}`);
        o.p(`Objectif évalué : ${pack.objectifs_seance[q.objectif - 1] || ""}`);
      });
    });
  }
  function ficheSeanceDocx(ctx, jour, pack, logo, identite) {
    return D.docWord(docCtx(ctx, logo), `Fiche de séance — ${D.fr(D.lireDate(jour.date))}`, (o) => {
      o.tableau([["Élément", "Information"], ["Formation", ctx.titre], ["Date et horaires", `${D.fr(D.lireDate(jour.date))} · ${D.fmtHm(jour.lignes[0].debut)} – ${D.fmtHm(jour.lignes[jour.lignes.length - 1].fin)}`],
        ["Durée", D.fmtDuree(jour.minutes)], ["Formateur", identite.dirigeant || ""], ["Séances du décorticage", jour.seances.map((s) => `S${s.numero} — ${s.titre}`).join("\n")],
        ["Compétences REAC", [...new Set(jour.seances.map((s) => s.cp).filter(Boolean))].map((n) => `CP${n} — ${ctx.reac.competence(n).intitule}`).join("\n")]]);
      o.h2("Objectifs de la séance");
      pack.objectifs_seance.forEach((x) => o.puce(x));
      o.h2("Déroulé");
      if (pack.deroule.length) o.tableau([["Horaire", "Phase (Bruner)", "Activité", "Modalité"]].concat(pack.deroule.map((d) => [`${d.debut}${d.fin ? "–" + d.fin : ""}`, d.phase, d.activite, d.modalite])));
      o.h2("Supports et outils remis");
      ["Diaporama de séance", "Fiche d'exercices apprenants", "Ressource « L'essentiel de la journée »", "Grille critériée (5 objectifs)", "Quiz de 10 questions (évaluation)"].forEach((x) => o.puce(x));
      o.h2("Bilan de séance (à compléter)");
      o.tableau([["Objectifs atteints", "Écarts / adaptations", "Émargement vérifié"], ["", "", "☐ oui"]]);
      o.p("Preuves Qualiopi : indicateurs 5 (objectifs), 6 (contenus et modalités), 11 (évaluation), 19 (ressources pédagogiques).");
    });
  }

  async function fabriquer(ctx, jour, pack, logo, identite) {
    const base = `${jour.date}_${ctx.sigle}`;
    return [
      [`Seance_${base}.pptx`, await powerpoint(ctx, jour, pack, logo)],
      [`Exercices_${base}.docx`, await exercicesDocx(ctx, jour, pack, logo)],
      [`Essentiel_journee_${base}.docx`, await ressourceDocx(ctx, jour, pack, logo)],
      [`Grille_criteriee_${base}.docx`, await grilleDocx(ctx, jour, pack, logo)],
      [`Quiz_FORMATEUR_${base}.docx`, await quizDocx(ctx, jour, pack, logo)],
      [`Fiche_seance_preuve_${base}.docx`, await ficheSeanceDocx(ctx, jour, pack, logo, identite)],
    ];
  }

  Object.assign(P, { matiereSeance: matiere, consigneSeance: consigne, normaliserPack: normaliser, packDeBase: versionDeBase, redigerSeance: rediger, fabriquerSeance: fabriquer });
})(typeof window !== "undefined" ? window : globalThis);

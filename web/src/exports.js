/* Exports générés dans le navigateur : Excel (ExcelJS), Word (docx),
 * agenda .ics, page web du programme. Même mise en page que le logiciel :
 * paysage, police 14 minimum, verbes Bloom en exergue, logo supprimable. */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const CTRL = /[\x00-\x08\x0b\x0c\x0e-\x1f]/g;
  const propre = (v) => (typeof v === "string" ? v.replace(CTRL, "") : v);

  function lignesNecessaires(texte, largeur, taille) {
    if (texte === null || texte === undefined) return 1;
    const parLigne = Math.max(4, ((largeur * 11) / taille) * 0.95);
    let total = 0;
    for (const morceau of String(texte).split("\n")) {
      let lignes = 1, cour = 0;
      for (const m of morceau.split(" ")) { const L = m.length + 1; if (cour + L > parLigne && cour > 0) { lignes++; cour = L; } else cour += L; }
      total += lignes;
    }
    return total;
  }

  class Feuille {
    constructor(wb, nom, st, largeurs, titre, sousTitre, nomOrg) {
      this.st = st; this.largeurs = largeurs; this.ligne = 1;
      this.ws = wb.addWorksheet(nom.slice(0, 31), {
        views: [{ showGridLines: false, zoomScale: 90 }],
        pageSetup: { orientation: "landscape", paperSize: 9, fitToPage: true, fitToWidth: 1, fitToHeight: 0, horizontalCentered: true,
          margins: { left: 0.4, right: 0.4, top: 0.5, bottom: 0.5, header: 0.3, footer: 0.3 } },
        headerFooter: { oddFooter: (nomOrg ? `&L&12${nomOrg.replace(/&/g, "&&")}` : "") + "&R&12Page &P / &N" },
      });
      largeurs.forEach((w, i) => { this.ws.getColumn(i + 1).width = w; });
      if (titre) this.titre(titre, sousTitre);
    }
    fusion(r, nb) {
      const l = this.largeurs.slice(0, nb);
      if (nb > 0 && nb < this.largeurs.length) { this.ws.mergeCells(r, nb, r, this.largeurs.length); l[nb - 1] = this.largeurs.slice(nb - 1).reduce((a, b) => a + b, 0); }
      return l;
    }
    titre(t, st) {
      const n = this.largeurs.length;
      this.ws.mergeCells(this.ligne, 1, this.ligne, n);
      const c = this.ws.getCell(this.ligne, 1);
      c.value = propre(t); c.font = this.st.titre; c.alignment = { vertical: "middle", wrapText: true };
      this.ws.getRow(this.ligne).height = this.st.c.taille_titre * 2;
      this.ligne++;
      if (st) {
        this.ws.mergeCells(this.ligne, 1, this.ligne, n);
        const c2 = this.ws.getCell(this.ligne, 1);
        c2.value = propre(st); c2.font = this.st.sousTitre; c2.alignment = { vertical: "middle", wrapText: true };
        this.ws.getRow(this.ligne).height = (this.st.c.taille_texte + 3) * 1.8;
        this.ligne++;
      }
      this.ligne++;
    }
    entetes(vals, repeter = true, figer = true) {
      const r = this.ligne, L = this.fusion(r, vals.length);
      vals.forEach((v, i) => { const c = this.ws.getCell(r, i + 1); c.value = propre(v); c.font = this.st.entete; c.fill = this.st.fondEntete; c.alignment = this.st.centre; c.border = this.st.bord; });
      const h = Math.max(...vals.map((v, i) => lignesNecessaires(v, L[i], this.st.c.taille_texte + 1)));
      this.ws.getRow(r).height = h * (this.st.c.taille_texte + 1) * 1.6 + 10;
      if (repeter) this.ws.pageSetup.printTitlesRow = `${r}:${r}`;
      if (figer) this.ws.views = [{ state: "frozen", ySplit: r, showGridLines: false, zoomScale: 90 }];
      this.debut = r; this.ligne++;
    }
    rangee(vals, { bande = false, gras = false, fond = null } = {}) {
      const r = this.ligne, L = this.fusion(r, vals.length);
      let nb = 1;
      vals.forEach((v, i) => {
        const c = this.ws.getCell(r, i + 1);
        let texte = v;
        if (v && typeof v === "object" && v.richText) { c.value = v; texte = v.richText.map((x) => x.text).join(""); }
        else c.value = propre(v ?? "");
        c.font = gras ? this.st.gras : this.st.normal; c.alignment = this.st.retour; c.border = this.st.bord;
        if (fond) c.fill = fond; else if (bande) c.fill = this.st.fondClair;
        nb = Math.max(nb, lignesNecessaires(texte, L[i], this.st.c.taille_texte));
      });
      this.ws.getRow(r).height = Math.min(409, nb * this.st.c.taille_texte * 1.42 + 8);
      this.ligne++;
      return r;
    }
    paragraphe(t, police, fond) {
      const r = this.ligne;
      this.ws.mergeCells(r, 1, r, this.largeurs.length);
      const c = this.ws.getCell(r, 1);
      c.value = propre(t); c.font = police || this.st.normal; c.alignment = this.st.retour;
      if (fond) c.fill = fond;
      const n = lignesNecessaires(t, this.largeurs.reduce((a, b) => a + b, 0) * 0.85, this.st.c.taille_texte);
      this.ws.getRow(r).height = Math.min(409, n * this.st.c.taille_texte * 1.45 + 8);
      this.ligne++;
    }
    filtre(nb) { this.ws.autoFilter = { from: { row: this.debut, column: 1 }, to: { row: this.ligne - 1, column: nb } }; }
  }

  function style(c) {
    const t = c.taille_texte, argb = (h) => "FF" + h;
    const fin = { style: "thin", color: { argb: "FF9AA5B1" } };
    return { c, police: c.police,
      normal: { name: c.police, size: t, color: { argb: argb(c.couleur_texte) } },
      gras: { name: c.police, size: t, bold: true, color: { argb: argb(c.couleur_texte) } },
      entete: { name: c.police, size: t + 1, bold: true, color: { argb: "FFFFFFFF" } },
      titre: { name: c.police, size: c.taille_titre, bold: true, color: { argb: argb(c.couleur_primaire) } },
      sousTitre: { name: c.police, size: t + 3, bold: true, color: { argb: argb(c.couleur_secondaire) } },
      fondEntete: { type: "pattern", pattern: "solid", fgColor: { argb: argb(c.couleur_primaire) } },
      fondClair: { type: "pattern", pattern: "solid", fgColor: { argb: argb(c.couleur_claire) } },
      fondAccent: { type: "pattern", pattern: "solid", fgColor: { argb: argb(c.couleur_secondaire) } },
      bord: { top: fin, left: fin, bottom: fin, right: fin },
      retour: { wrapText: true, vertical: "top" }, centre: { wrapText: true, vertical: "middle", horizontal: "center" } };
  }

  function riche(st, verbe, texte) {
    const t = propre(texte);
    const debut = verbe && t.toLowerCase().startsWith(verbe.toLowerCase()) ? t.slice(0, verbe.length) : "";
    const parts = [];
    if (debut) parts.push({ font: { name: st.police, size: st.c.taille_texte, bold: true, color: { argb: "FF" + st.c.couleur_secondaire } }, text: debut.toUpperCase() });
    parts.push({ font: { name: st.police, size: st.c.taille_texte, color: { argb: "FF" + st.c.couleur_texte } }, text: t.slice(debut.length) });
    return { richText: parts };
  }

  const groupe = (arr, cle) => { const m = new Map(); for (const x of arr) { const k = cle(x); if (!m.has(k)) m.set(k, []); m.get(k).push(x); } return m; };
  const uniques = (a) => [...new Set(a)];
  const pct = (x, d = 0) => (x * 100).toFixed(d).replace(".", ",") + " %";

  async function classeur(ctx) {
    const { reac, re, fiche, plan, r, charte, nomOrg, logo } = ctx;
    const st = style(charte);
    const titreF = (fiche && fiche.intitule) || `TP ${reac.intitule}`;
    const code = (fiche && fiche.code) || reac.code_titre || "";
    const wb = new G.ExcelJS.Workbook();
    wb.creator = nomOrg || ""; wb.lastModifiedBy = nomOrg || ""; wb.title = `Décorticage — ${titreF}`; wb.company = nomOrg || "";
    const total = plan.lignes.reduce((t, l) => t + l.minutes, 0);
    const imgId = logo ? wb.addImage({ base64: logo.base64, extension: logo.ext }) : null;
    const poserLogo = (f) => { if (imgId === null) return; f.ws.getRow(1).height = 60; f.ws.addImage(imgId, { tl: { col: 0, row: 0 }, ext: { width: Math.round(70 * logo.ratio), height: 70 } }); f.ligne = 2; };

    // Accueil
    let f = new Feuille(wb, "Accueil", st, [34, 40, 34, 40], "", "", nomOrg);
    poserLogo(f);
    f.titre(`Décorticage pédagogique — ${titreF}`, [code, reac.niveau ? `Niveau ${reac.niveau}` : "", nomOrg].filter(Boolean).join(" • "));
    const infos = [["Durée en centre", D.fmtDuree(total)], ["Période", plan.lignes.length ? `du ${D.fr(plan.lignes[0].date)} au ${D.fr(plan.date_fin)}` : "—"],
      ["Activités types", String(reac.activites.length)], ["Compétences", String(reac.competences.length)], ["Séances", String(plan.seances.length)],
      ["Jours de formation", String(new Set(plan.lignes.map((l) => D.iso(l.date))).size)],
      ["REAC", `${reac.sigle} ${reac.code_titre} — millésime ${reac.millesime} du ${reac.date_validation}`.trim()],
      ["Période en entreprise", r.heures_entreprise ? D.fmtDuree(r.heures_entreprise * 60) : "voir Examen"]];
    for (let i = 0; i < infos.length; i += 2) {
      const rr = f.rangee(infos.slice(i, i + 2).flat());
      for (const col of [1, 3]) { f.ws.getCell(rr, col).font = st.gras; f.ws.getCell(rr, col).fill = st.fondClair; }
    }
    f.ligne++;
    f.paragraphe("Sommaire (cliquer pour ouvrir)", st.sousTitre);
    for (const nom of ["Décorticage", "Planning détaillé", "Planning par jour", "Synthèses", "Programme", "Examen simplifié", "Couverture critères", "Suivi journalier", "Préparation PowerPoint", "Paramètres et sources"]) {
      f.ws.mergeCells(f.ligne, 1, f.ligne, 4);
      const c = f.ws.getCell(f.ligne, 1);
      c.value = { text: `→ ${nom}`, hyperlink: `#'${nom}'!A1` };
      c.font = { name: st.police, size: charte.taille_texte + 1, color: { argb: "FF" + charte.couleur_primaire }, underline: true };
      f.ws.getRow(f.ligne).height = 26; f.ligne++;
    }
    f.ligne++;
    f.paragraphe("Légende — Taxonomie de Bloom (verbe d'action en COULEUR et MAJUSCULES dans les tableaux)", st.sousTitre);
    const ex = { 1: "identifier, citer", 2: "expliquer, décrire", 3: "appliquer, utiliser", 4: "analyser, organiser", 5: "évaluer, contrôler", 6: "élaborer, planifier" };
    for (let n = 1; n <= 6; n++) f.rangee([`Niveau ${n}`, D.NIVEAUX_BLOOM[n], ex[n]], { bande: n % 2 === 0 });
    const alertes = plan.avertissements.concat(ctx.alertes);
    if (alertes.length) { f.ligne++; f.paragraphe("Points à vérifier", st.sousTitre); for (const a of alertes) f.paragraphe("⚠ " + a); }

    // Décorticage
    f = new Feuille(wb, "Décorticage", st, [24, 8, 25, 37, 17, 32, 9], `Décorticage — ${titreF}`,
      "Activités types et compétences : termes exacts du REAC. Objectifs : verbe d'action (Bloom) + mots clés du REAC.", nomOrg);
    f.entetes(["Activité type · Compétence (REAC)", "N°", "Étape du processus (REAC)", "Objectif pédagogique", "Bloom · Bruner", "Contenus (savoirs REAC)", "Durée"]);
    let cpPrec = null, bande = false;
    for (const s of plan.seances)
      s.objectifs.forEach((o, k) => {
        if (s.cp !== cpPrec) { bande = !bande; cpPrec = s.cp; }
        const cp = s.cp ? reac.competence(s.cp) : null;
        let cont = o.contenus.map((c) => "• " + c).join("\n");
        if (o.associes.length) cont = "Aussi : " + o.associes.join(" ; ") + (cont ? "\n" + cont : "");
        f.rangee([cp ? (k === 0 ? `AT${s.at} · CP${cp.numero} — ${cp.intitule}` : `AT${s.at} · CP${cp.numero}`) : (k === 0 ? s.sequence_titre : "Module"),
          `S${s.numero}`, k === 0 ? s.titre : "", riche(st, o.verbe, o.texte), `${o.niveau} - ${D.NIVEAUX_BLOOM[o.niveau]}\n${o.mode.split(" (")[0]}`, cont, D.fmtDuree(o.minutes)], { bande });
      });
    f.filtre(7);

    // Planning détaillé
    f = new Feuille(wb, "Planning détaillé", st, [18, 15, 8, 7, 29, 40, 13, 11, 13], `Planning heure par heure — ${titreF}`,
      "Chaque ligne = un créneau réel (pauses exclues). Colonne « Réalisé » : liste déroulante.", nomOrg);
    f.entetes(["Date · semaine", "Horaire", "Durée", "CP", "Séance", "Objectif pédagogique", "Cumul · % avancé", "Réalisé ?", "Observations"]);
    let jp = null; bande = false;
    for (const l of plan.lignes) {
      const s = l.seance, o = l.objectif, d = l.date;
      if (D.iso(d) !== jp) { bande = !bande; jp = D.iso(d); }
      const rr = f.rangee([`${D.JOURS[D.jourSem(d)].slice(0, 3).replace(/^./, (x) => x.toUpperCase())} ${D.fr(d)}\nSem. ${D.semaineIso(d)[1]}`,
        `${D.fmtHm(l.debut)} – ${D.fmtHm(l.fin)}`, D.fmtDuree(l.minutes), s.cp ? `CP${s.cp}` : "—", `S${s.numero} — ${s.titre}`,
        riche(st, o.verbe, o.texte + (l.suite ? " (suite)" : "")), `${D.fmtDuree(l.cumul)}\n${pct(l.pourcentage)}`, "", ""], { bande });
      f.ws.getCell(rr, 8).dataValidation = { type: "list", allowBlank: true, formulae: ['"Oui,Partiel,Non,Reporté"'] };
    }
    f.filtre(9);

    // Planning par jour
    const parJour = groupe(plan.lignes, (l) => D.iso(l.date));
    f = new Feuille(wb, "Planning par jour", st, [16, 12, 8, 16, 70, 12, 12], "Séances prévues par jour", "", nomOrg);
    f.entetes(["Date", "Jour", "Sem.", "Mois", "Séances et objectifs du jour", "Heures", "Cumul"]);
    let cumul = 0, i = 0;
    for (const [, ls] of parJour) {
      const d = ls[0].date, mn = ls.reduce((t, x) => t + x.minutes, 0);
      cumul += mn;
      const ss = groupe(ls, (x) => x.seance.numero);
      const txt = [...ss.values()].map((xs) => `S${xs[0].seance.numero} — ${xs[0].seance.titre} (${D.fmtHm(xs[0].debut)}-${D.fmtHm(xs[xs.length - 1].fin)})`).join("\n");
      f.rangee([D.fr(d), D.JOURS[D.jourSem(d)].replace(/^./, (x) => x.toUpperCase()), D.semaineIso(d)[1], `${D.MOIS[d.getUTCMonth()].replace(/^./, (x) => x.toUpperCase())} ${d.getUTCFullYear()}`, txt, D.fmtDuree(mn), D.fmtDuree(cumul)], { bande: i++ % 2 === 1 });
    }

    // Synthèses
    f = new Feuille(wb, "Synthèses", st, [46, 16, 16, 14, 12, 38], "Synthèses : par activité type, compétence, mois et semaine", "", nomOrg);
    f.paragraphe("Par activité type et compétence", st.sousTitre);
    f.entetes(["Activité type / Compétence", "Début", "Fin", "Heures", "% du total", "Séances"], false, false);
    const ligneSyn = (lib, ls, opts) => { const m = ls.reduce((t, l) => t + l.minutes, 0); f.rangee([lib, D.fr(ls[0].date), D.fr(ls[ls.length - 1].date), D.fmtDuree(m), pct(m / total, 1), String(new Set(ls.map((l) => l.seance.numero)).size)], opts); };
    for (const at of reac.activites) {
      const la = plan.lignes.filter((l) => l.seance.at === at.numero);
      if (la.length) ligneSyn(`AT${at.numero} — ${at.intitule}`, la, { gras: true, fond: st.fondClair });
      for (const n of at.competences) { const lc = plan.lignes.filter((l) => l.seance.cp === n); if (lc.length) ligneSyn(`   CP${n} — ${reac.competence(n).intitule}`, lc); }
    }
    const autres = plan.lignes.filter((l) => !l.seance.cp);
    if (autres.length) { const m = autres.reduce((t, l) => t + l.minutes, 0); f.rangee(["Modules transverses (accueil, ECF, DP, examen blanc, bilan)", "", "", D.fmtDuree(m), pct(m / total, 1), String(new Set(autres.map((l) => l.seance.numero)).size)], { gras: true, fond: st.fondClair }); }
    f.rangee(["TOTAL", plan.lignes.length ? D.fr(plan.lignes[0].date) : "", plan.date_fin ? D.fr(plan.date_fin) : "", D.fmtDuree(total), "100 %", String(plan.seances.length)], { gras: true, fond: st.fondAccent });
    f.ligne++;
    f.paragraphe("Par mois", st.sousTitre);
    f.entetes(["Mois", "Jours de formation", "Heures", "Cumul", "% avancé", "Compétences travaillées"], false, false);
    cumul = 0; i = 0;
    for (const [, ls] of groupe(plan.lignes, (l) => `${l.date.getUTCFullYear()}-${l.date.getUTCMonth()}`)) {
      const mn = ls.reduce((t, l) => t + l.minutes, 0); cumul += mn;
      const cps = uniques(ls.filter((l) => l.seance.cp).map((l) => l.seance.cp)).sort((a, b) => a - b);
      f.rangee([`${D.MOIS[ls[0].date.getUTCMonth()].replace(/^./, (x) => x.toUpperCase())} ${ls[0].date.getUTCFullYear()}`, String(new Set(ls.map((l) => D.iso(l.date))).size), D.fmtDuree(mn), D.fmtDuree(cumul), pct(cumul / total), cps.map((c) => "CP" + c).join(", ") || "Modules"], { bande: i++ % 2 === 1 });
    }
    f.ligne++;
    f.paragraphe("Par semaine", st.sousTitre);
    f.entetes(["Semaine", "Du … au …", "Heures", "Cumul", "% avancé", "Séances"], false, false);
    cumul = 0; i = 0;
    for (const [, ls] of groupe(plan.lignes, (l) => D.semaineIso(l.date).join("-"))) {
      const mn = ls.reduce((t, l) => t + l.minutes, 0); cumul += mn;
      const nums = uniques(ls.map((l) => l.seance.numero)).sort((a, b) => a - b), [a, w] = D.semaineIso(ls[0].date);
      f.rangee([`S${w} — ${a}`, `${D.fr(ls[0].date).slice(0, 5)} → ${D.fr(ls[ls.length - 1].date).slice(0, 5)}`, D.fmtDuree(mn), D.fmtDuree(cumul), pct(cumul / total), nums.length > 1 ? `S${nums[0]} à S${nums[nums.length - 1]}` : `S${nums[0]}`], { bande: i++ % 2 === 1 });
    }

    // Programme
    const [intitule, sections] = D.construireProgramme(reac, re, fiche, plan, r, ctx.tarif);
    f = new Feuille(wb, "Programme", st, [30, 36, 48, 14, 12, 12], "", "", nomOrg);
    poserLogo(f);
    f.titre(`Programme de formation — ${intitule}`, nomOrg);
    for (const s of sections) {
      f.paragraphe(s.titre, st.sousTitre);
      s.paragraphes.forEach((p) => f.paragraphe(p));
      s.puces.forEach((p) => f.paragraphe("•  " + p));
      if (s.tableau.length) { f.entetes(s.tableau[0], false, false); s.tableau.slice(1).forEach((row, k) => f.rangee(row, { bande: k % 2 === 1 })); }
      f.ligne++;
    }
    f.paragraphe(`Mise à jour : ${D.fr(new Date(Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())))}`);

    // Examen simplifié
    const exm = D.construireExamen(reac, re, fiche);
    f = new Feuille(wb, "Examen simplifié", st, [32, 18, 50, 52], "", "", nomOrg);
    poserLogo(f);
    f.titre(`L'examen en clair — ${titreF}`, exm.duree_totale ? `Durée totale pour le candidat : ${exm.duree_totale}` : "");
    f.paragraphe("PARTIE 1 — Les épreuves", st.sousTitre);
    if (exm.partie1.length > 1) { f.entetes(exm.partie1[0], false, false); exm.partie1.slice(1).forEach((row, k) => f.rangee(row, { bande: k % 2 === 1 })); }
    exm.consignes.forEach((c) => f.paragraphe("•  " + c));
    f.ligne++;
    f.paragraphe("PARTIE 2 — Ce que le jury attend, compétence par compétence", st.sousTitre);
    f.entetes(["Compétence", "Évaluée par", "Ce qu'il faut savoir faire (critères en clair)", "À préparer avant l'examen"], false, false);
    exm.partie2.forEach((b, k) => f.rangee([b.cp, b.epreuves.join("\n") || "—", b.attendus.map((a) => "✔ " + a).join("\n"),
      b.production ? `Partie de document (${b.production.pages}) :\n` + b.production.themes.map((t) => "• " + t).join("\n") : ""], { bande: k % 2 === 1 }));

    // Couverture critères
    f = new Feuille(wb, "Couverture critères", st, [30, 62, 40, 18], "Couverture des critères d'évaluation", "Chaque critère du REAC/RE est relié aux séances qui le travaillent.", nomOrg);
    f.entetes(["Compétence", "Critère de performance / d'évaluation", "Séances", "Statut"]);
    for (const cp of reac.competences)
      for (const crit of cp.criteres) {
        const ss = plan.seances.filter((s) => s.objectifs.some((o) => o.criteres.includes(crit)) || (s.type_seance === "evaluation" && !s.cp && s.at === cp.at_numero));
        const couvre = uniques(ss.map((s) => "S" + s.numero)).join(", ");
        f.rangee([`CP${cp.numero} — ${cp.intitule}`, crit, couvre || "—", couvre ? "Couvert ✔" : "À COUVRIR ✖"], { fond: couvre ? null : st.fondAccent });
      }

    // Suivi journalier
    f = new Feuille(wb, "Suivi journalier", st, [14, 9, 80, 30, 18], "Suivi journalier — texte prêt à reprendre", "Le texte du jour est pré-rédigé à partir du décorticage. Ajustez seulement ce qui a changé.", nomOrg);
    f.entetes(["Date", "Heures", "Ce qui a été fait aujourd'hui (pré-rédigé)", "Écarts / adaptations", "Émargement vérifié"]);
    i = 0;
    for (const [, ls] of parJour) {
      const objs = uniques(ls.map((x) => x.objectif.texte)), ss = uniques(ls.map((x) => `S${x.seance.numero} « ${x.seance.titre} »`));
      const cps = uniques(ls.filter((x) => x.seance.cp).map((x) => x.seance.cp)).sort((a, b) => a - b);
      f.rangee([D.fr(ls[0].date), D.fmtDuree(ls.reduce((t, x) => t + x.minutes, 0)),
        `Séance(s) ${ss.join(", ")}${cps.length ? " — " + cps.map((c) => "CP" + c).join(", ") : ""}. Objectifs travaillés : ${objs.map((o) => o[0].toLowerCase() + o.slice(1)).join(" ; ")}.`, "", ""], { bande: i++ % 2 === 1 });
    }

    // Préparation PowerPoint
    f = new Feuille(wb, "Préparation PowerPoint", st, [8, 30, 36, 40, 38], "Trame de diaporama par séance", "Étayage de Bruner : la trame suit les 6 fonctions de tutelle (Wood, Bruner & Ross, 1976).", nomOrg);
    f.entetes(["N°", "Titre de la séance", "Diapositives clés (mots-clés REAC)", "Déroulé (étayage brunérien)", "Exercices et exemples"]);
    plan.seances.forEach((s, k) => {
      const diapos = s.objectifs.slice(0, 8).map((o) => `• ${o.verbe.toUpperCase()} : ${o.mots.slice(0, 4).join(", ")}`).join("\n") + "\nModes : " + uniques(s.objectifs.map((o) => o.mode.split(" (")[0])).sort().join(", ");
      const exemple = (s.objectifs.find((o) => o.exemple) || {}).exemple, activite = (s.objectifs.find((o) => o.activite) || {}).activite;
      const mots = uniques(s.objectifs.flatMap((o) => o.mots)).slice(0, 6);
      const E = D.ETAYAGE;
      const der = [`1. ${E[0][0]} : ${exemple || "question d’accroche sur le vécu en entreprise"}`, `2. ${E[1][0]} : une consigne, une tâche — « ${s.objectifs[0].texte} »`,
        `3. ${E[2][0]} : rappel de l'objectif et du critère de réussite`, `4. ${E[3][0]} : ${mots.join(", ")}`, `5. ${E[4][0]} : binôme, aide graduée, droit à l'erreur`,
        `6. ${E[5][0]} : ${activite || "modèle montré puis reproduit"}`].join("\n");
      f.rangee([`S${s.numero}`, `${s.titre}\n(${D.fmtDuree(s.minutes)})`, diapos, der, uniques(s.objectifs.flatMap((o) => [o.activite, o.exemple]).filter(Boolean)).join("\n")], { bande: k % 2 === 1 });
    });

    // Paramètres et sources
    f = new Feuille(wb, "Paramètres et sources", st, [44, 100], "Paramètres, hypothèses et sources", "", nomOrg);
    f.entetes(["Paramètre", "Valeur"], false, false);
    for (const [k, v] of [["Durée en centre (h)", String(r.heures_centre)], ["Date de début", r.date_debut], ["Jours de centre", r.jours], ["Créneaux", r.creneaux],
      ["Pauses (exclues des heures)", r.pauses], ["Rythme d'alternance", r.rythme || "aucun"], ["Fermetures", r.fermetures || "aucune"],
      ["Jours fériés", "La Réunion (dont 20 décembre), automatiques"],
      ["Accueil / ECF par AT / DP / Productions / Examen blanc / Bilan (h)", `${r.h_accueil} / ${r.h_ecf_par_at} / ${r.h_dossier_pro} / ${r.h_productions} / ${r.h_examen_blanc} (0 = durée du RE) / ${r.h_bilan}`],
      ["Pondération des compétences", r.poids_cp || "automatique (volume du REAC)"]]) f.rangee([k, v]);
    if (plan.jours_exclus.length) f.rangee(["Jours exclus du calendrier", plan.jours_exclus.map(([d, m]) => `${D.fr(d)} — ${m}`).join("\n")]);
    for (const h of ctx.hypotheses) f.rangee(["HYPOTHÈSE À CONFIRMER", h], { fond: st.fondAccent });
    f.ligne++;
    f.paragraphe("Sources", st.sousTitre);
    ctx.sources.forEach((s) => f.paragraphe("•  " + s));
    return new Blob([await wb.xlsx.writeBuffer()], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
  }

  // ------------------------------------------------------------------ Word
  function docWord(ctx, titre, construire) {
    const X = G.docx, c = ctx.charte, t = c.taille_texte * 2;
    const enfants = [];
    if (ctx.logo) enfants.push(new X.Paragraph({ children: [new X.ImageRun({ data: ctx.logo.octets, transformation: { width: Math.round(83 * ctx.logo.ratio), height: 83 } })] }));
    enfants.push(new X.Paragraph({ text: titre, heading: X.HeadingLevel.HEADING_1 }));
    if (ctx.nomOrg) enfants.push(new X.Paragraph({ text: ctx.nomOrg }));
    const outils = {
      h2: (s) => enfants.push(new X.Paragraph({ text: s, heading: X.HeadingLevel.HEADING_2 })),
      p: (s) => enfants.push(new X.Paragraph({ text: s })),
      puce: (s, niveau = 0) => enfants.push(new X.Paragraph({ text: s, bullet: { level: niveau } })),
      tableau: (lignes) => {
        const total = 15000;
        const poids = lignes[0].map((h, j) => { const L = lignes.map((r) => String(r[j] ?? "").length); const motLong = Math.max(...lignes.flatMap((r) => String(r[j] ?? "").split(/\s+/).map((m) => m.length)));
          return Math.min(45, Math.max(14, String(h).length + 6, motLong + 3, L.reduce((a, b) => a + b, 0) / L.length)); });
        const larg = poids.map((w) => Math.round((total * w) / poids.reduce((a, b) => a + b, 0)));
        enfants.push(new X.Table({ width: { size: total, type: X.WidthType.DXA }, columnWidths: larg,
          rows: lignes.map((row, i) => new X.TableRow({ tableHeader: i === 0, children: row.map((v, j) => new X.TableCell({
            width: { size: larg[j], type: X.WidthType.DXA },
            shading: i === 0 ? { fill: c.couleur_primaire, type: X.ShadingType.CLEAR, color: "auto" } : undefined,
            children: String(v ?? "").split("\n").map((ligne) => new X.Paragraph({ children: [new X.TextRun({ text: propre(ligne), bold: i === 0, color: i === 0 ? "FFFFFF" : c.couleur_texte, size: t })] })) })) })) }));
        enfants.push(new X.Paragraph({ text: "" }));
      },
    };
    construire(outils);
    const doc = new X.Document({
      creator: ctx.nomOrg || "", lastModifiedBy: ctx.nomOrg || "", title: titre, description: "",
      styles: { default: { document: { run: { font: c.police, size: t, color: c.couleur_texte } } },
        paragraphStyles: [
          { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: c.police, size: c.taille_titre * 2, bold: true, color: c.couleur_primaire }, paragraph: { spacing: { before: 240, after: 160 } } },
          { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: c.police, size: (c.taille_texte + 4) * 2, bold: true, color: c.couleur_secondaire }, paragraph: { spacing: { before: 240, after: 120 } } }] },
      sections: [{ properties: { page: { size: { width: 11906, height: 16838, orientation: X.PageOrientation.LANDSCAPE }, margin: { top: 907, bottom: 907, left: 907, right: 907 } } }, children: enfants }],
    });
    return X.Packer.toBlob(doc);
  }

  function programmeDocx(ctx) {
    const [intitule, sections] = D.construireProgramme(ctx.reac, ctx.re, ctx.fiche, ctx.plan, ctx.r, ctx.tarif);
    return docWord(ctx, `Programme de formation — ${intitule}`, (o) => {
      for (const s of sections) { o.h2(s.titre); s.paragraphes.forEach(o.p); s.puces.forEach((x) => o.puce(x)); if (s.tableau.length) o.tableau(s.tableau); }
      o.p(`Mise à jour : ${D.fr(new Date(Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())))}`);
    });
  }
  function examenDocx(ctx) {
    const ex = D.construireExamen(ctx.reac, ctx.re, ctx.fiche);
    const titre = (ctx.fiche && ctx.fiche.intitule) || ctx.reac.intitule;
    return docWord(ctx, `L'examen en clair — ${titre}`, (o) => {
      if (ex.duree_totale) o.p(`Durée totale pour le candidat : ${ex.duree_totale}`);
      o.h2("Partie 1 — Les épreuves");
      if (ex.partie1.length > 1) o.tableau(ex.partie1);
      ex.consignes.forEach((x) => o.puce(x));
      o.h2("Partie 2 — Ce que le jury attend");
      for (const b of ex.partie2) {
        o.h2(b.cp);
        if (b.epreuves.length) o.p("Évaluée par : " + b.epreuves.join(", "));
        b.attendus.forEach((a) => o.puce(a));
        if (b.production) { o.p(`À préparer avant l'examen — partie de document (${b.production.pages}) :`); b.production.themes.forEach((t) => o.puce(t, 1)); }
      }
    });
  }

  // ------------------------------------------------------------ Agenda .ics
  const icsTxt = (s) => s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n").replace(/[\x00-\x1f]/g, "");
  function pli(l) {
    const enc = new TextEncoder(), out = [];
    let cour = "";
    for (const ch of l) { if (enc.encode(cour + ch).length > 74) { out.push(cour); cour = " " + ch; } else cour += ch; }
    out.push(cour);
    return out.join("\r\n");
  }
  function ics(ctx) {
    const L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Decorticage//FR", "CALSCALE:GREGORIAN", "BEGIN:VTIMEZONE", "TZID:Indian/Reunion", "BEGIN:STANDARD",
      "DTSTART:19700101T000000", "TZOFFSETFROM:+0400", "TZOFFSETTO:+0400", "TZNAME:RET", "END:STANDARD", "END:VTIMEZONE"];
    const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
    const ymd = (d) => D.iso(d).replace(/-/g, ""), hh = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}${String(m % 60).padStart(2, "0")}00`;
    for (const [, ls] of groupe(ctx.plan.lignes, (l) => D.iso(l.date) + "#" + l.seance.numero)) {
      const s = ls[0].seance, deb = ls[0].debut, fin = ls[ls.length - 1].fin;
      L.push("BEGIN:VEVENT", `UID:${ctx.sigle}-${ymd(ls[0].date)}-s${s.numero}-${deb}@decorticage.local`, `DTSTAMP:${stamp}`,
        `DTSTART;TZID=Indian/Reunion:${ymd(ls[0].date)}T${hh(deb)}`, `DTEND;TZID=Indian/Reunion:${ymd(ls[0].date)}T${hh(fin)}`,
        pli("SUMMARY:" + icsTxt(`S${s.numero} — ${s.titre}`)), pli("DESCRIPTION:" + icsTxt(`${D.fmtHm(deb)}-${D.fmtHm(fin)}\n` + uniques(ls.map((x) => "- " + x.objectif.texte)).join("\n"))), "END:VEVENT");
    }
    L.push("END:VCALENDAR");
    return L.join("\r\n") + "\r\n";
  }

  // ------------------------------------------------------- Page web (site)
  const h = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  function pageSite(ctx) {
    const [intitule, sections] = D.construireProgramme(ctx.reac, ctx.re, ctx.fiche, ctx.plan, ctx.r, ctx.tarif);
    const c = ctx.charte, nom = ctx.nomOrg;
    const corps = sections.map((s) => `<section><h2>${h(s.titre)}</h2>${s.paragraphes.map((p) => `<p>${h(p)}</p>`).join("")}` +
      (s.puces.length ? `<ul>${s.puces.map((p) => `<li>${h(p)}</li>`).join("")}</ul>` : "") +
      (s.tableau.length ? `<div class="t"><table><thead><tr>${s.tableau[0].map((x) => `<th scope="col">${h(x)}</th>`).join("")}</tr></thead><tbody>${s.tableau.slice(1).map((r) => `<tr>${r.map((x) => `<td>${h(x).replace(/\n/g, "<br>")}</td>`).join("")}</tr>`).join("")}</tbody></table></div>` : "") + "</section>").join("\n");
    const ld = JSON.stringify(Object.fromEntries(Object.entries({ "@context": "https://schema.org", "@type": "Course", name: intitule, courseCode: ctx.fiche ? ctx.fiche.code : "", educationalCredentialAwarded: intitule, provider: nom ? { "@type": "Organization", name: nom } : null, inLanguage: "fr" }).filter(([, v]) => v))).replace(/</g, "\\u003c");
    return `<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:">
<title>${h(intitule)}</title><script type="application/ld+json">${ld}</script>
<style>:root{--p:#${c.couleur_primaire};--s:#${c.couleur_secondaire};--c:#${c.couleur_claire};--t:#${c.couleur_texte}}
body{font-family:${h(c.police)},Arial,sans-serif;font-size:1.25rem;line-height:1.6;color:var(--t);margin:0;background:#fff}
header{background:var(--p);color:#fff;padding:1.5rem 1rem}header h1{margin:0;font-size:2rem}main{max-width:1100px;margin:0 auto;padding:1rem}
h2{color:var(--p);border-left:.4rem solid var(--s);padding-left:.6rem;margin-top:2rem}.t{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:1.1rem}
th{background:var(--p);color:#fff;text-align:left}th,td{border:1px solid #9aa5b1;padding:.5rem;vertical-align:top}tr:nth-child(even) td{background:var(--c)}</style>
</head><body><header><h1>${h(intitule)}</h1>${nom ? `<p>${h(nom)}</p>` : ""}</header><main>
${corps}
<p><small>Mise à jour : ${D.fr(new Date(Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())))}</small></p></main></body></html>`;
  }

  async function toutEnZip(ctx, fichiers) {
    const z = new G.JSZip(), dossier = z.folder(`Decorticage_${ctx.sigle}`);
    for (const [nom, contenu] of fichiers) dossier.file(nom, contenu instanceof Blob ? await contenu.arrayBuffer() : contenu);
    dossier.file(`Planning_${ctx.sigle}.ics`, ics(ctx));
    return z.generateAsync({ type: "blob", compression: "DEFLATE" });
  }

  Object.assign(D, { classeur, programmeDocx, examenDocx, ics, pageSite, toutEnZip, echapper: h });
})(typeof window !== "undefined" ? window : globalThis);

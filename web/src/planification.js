/* Planification jour par jour, heure par heure — portage de planification.py.
 * Jours fériés : Code du travail art. L3133-1 ; 20 décembre à La Réunion (décret n° 83-1003). */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  const JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

  // Dates « calendaires » sans fuseau : objets {a, m, j} manipulés via UTC
  const date = (a, m, j) => new Date(Date.UTC(a, m - 1, j));
  const ajout = (d, n) => new Date(d.getTime() + n * 86400000);
  const iso = (d) => d.toISOString().slice(0, 10);
  const jourSem = (d) => (d.getUTCDay() + 6) % 7; // 0 = lundi
  const fr = (d) => `${String(d.getUTCDate()).padStart(2, "0")}/${String(d.getUTCMonth() + 1).padStart(2, "0")}/${d.getUTCFullYear()}`;
  function semaineIso(d) {
    const t = new Date(d.getTime());
    t.setUTCDate(t.getUTCDate() + 3 - jourSem(t));
    const a = t.getUTCFullYear(), p = date(a, 1, 4);
    return [a, 1 + Math.round(((t - p) / 86400000 - 3 + jourSem(p)) / 7)];
  }
  function paques(a) {
    const A = a % 19, b = Math.floor(a / 100), c = a % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25);
    const g = Math.floor((b - f + 1) / 3), h = (19 * A + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4;
    const l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((A + 11 * h + 22 * l) / 451);
    const mois = Math.floor((h + l - 7 * m + 114) / 31), jour = ((h + l - 7 * m + 114) % 31) + 1;
    return date(a, mois, jour);
  }
  function feries(a) {
    const p = paques(a), r = {};
    r[iso(date(a, 1, 1))] = "Jour de l'An"; r[iso(ajout(p, 1))] = "Lundi de Pâques"; r[iso(date(a, 5, 1))] = "Fête du Travail";
    r[iso(date(a, 5, 8))] = "Victoire 1945"; r[iso(ajout(p, 39))] = "Ascension"; r[iso(ajout(p, 50))] = "Lundi de Pentecôte";
    r[iso(date(a, 7, 14))] = "Fête nationale"; r[iso(date(a, 8, 15))] = "Assomption"; r[iso(date(a, 11, 1))] = "Toussaint";
    r[iso(date(a, 11, 11))] = "Armistice 1918"; r[iso(date(a, 12, 20))] = "Fête de l'abolition de l'esclavage (La Réunion)";
    r[iso(date(a, 12, 25))] = "Noël";
    return r;
  }
  const hm = (s) => { const [h, m] = s.trim().replace("h", ":").split(":"); return +h * 60 + +(m || 0); };
  const fmtHm = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}h${String(m % 60).padStart(2, "0")}`;
  const fmtDuree = (m) => { const h = Math.floor(m / 60), r = m % 60; return r ? `${h} h ${String(r).padStart(2, "0")}` : `${h} h`; };

  function fenetres(p) {
    const res = [], pauses = p.pauses.map(([a, b]) => [hm(a), hm(b)]).sort((x, y) => x[0] - y[0]);
    for (const [a, b] of p.creneaux) {
      const deb = hm(a), fin = hm(b);
      let cur = deb;
      for (const [pa, pb] of pauses) if (pa >= deb && pa < fin) { if (pa > cur) res.push([cur, pa]); cur = Math.max(cur, pb); }
      if (fin > cur) res.push([cur, fin]);
    }
    return res;
  }
  function jourOuvre(p, j) {
    if (!p.jours_semaine.includes(jourSem(j))) return [false, "jour non travaillé en centre"];
    if (p.feries) { const f = feries(j.getUTCFullYear())[iso(j)]; if (f) return [false, "férié : " + f]; }
    for (const [a, b, motif] of p.fermetures) if (j >= a && j <= b) return [false, motif || "fermeture"];
    if (p.rythme) {
      const lundi0 = ajout(p.date_debut, -jourSem(p.date_debut));
      const s = Math.floor((j - lundi0) / 86400000 / 7);
      if (p.rythme[s % p.rythme.length].toUpperCase() !== "C") return [false, "semaine en entreprise"];
    }
    return [true, ""];
  }
  function* creneaux(p, requis) {
    const f = fenetres(p);
    if (!f.length) throw new Error("Aucun créneau horaire valide : vérifiez les horaires et les pauses.");
    let total = 0, j = p.date_debut;
    for (let n = 0; n < 1500; n++, j = ajout(j, 1))
      if (jourOuvre(p, j)[0]) for (const [a, b] of f) { yield [j, a, b]; total += b - a; if (total >= requis) return; }
  }

  const O = (texte, niveau, activite, categorie = "module", criteres = []) => D.objectif({ texte, verbe: D.verbeInitial(texte), niveau, categorie,
    origine: texte, mots: D.motsCles(texte), mode: D.modeBruner("technique", niveau), activite, criteres });
  const S = (titre, origine, type_seance, objectifs, extra = {}) => Object.assign({ titre, origine, type_seance, objectifs, minutes: 0, numero: 0, cp: 0, at: 0, sequence: 0, sequence_titre: "" }, extra);

  function construirePlan(reac, re, p) {
    const plan = { seances: [], lignes: [], minutes_cp: {}, minutes_modules: {}, date_fin: null, jours_exclus: [], avertissements: [] };
    const PAS = D.PAS, total = Math.round((p.heures_centre * 60) / PAS) * PAS;
    if (total <= 0) throw new Error("La durée en centre doit être supérieure à 0 heure.");
    let mExam = p.h_examen_blanc * 60;
    if (!mExam) { mExam = (re ? re.epreuves.reduce((t, e) => t + e.minutes, 0) : 0) || 420; mExam = Math.ceil(mExam / PAS) * PAS; }
    const aProd = re && (re.documents.length || re.productions.length);
    let mod = { accueil: p.h_accueil * 60, ecf: p.h_ecf_par_at * 60 * reac.activites.length, dossier: p.h_dossier_pro * 60,
      productions: aProd ? p.h_productions * 60 : 0, examen: mExam, bilan: p.h_bilan * 60 };
    for (const k in mod) mod[k] = Math.round(mod[k] / PAS) * PAS;
    const somme = Object.values(mod).reduce((a, b) => a + b, 0);
    if (somme > total * 0.4) {
      plan.avertissements.push("Les modules transverses dépassent 40 % de la durée : ils ont été réduits proportionnellement.");
      for (const k in mod) mod[k] = Math.floor((mod[k] * total * 0.4) / somme / PAS) * PAS;
    }
    plan.minutes_modules = mod;
    const reste = total - Object.values(mod).reduce((a, b) => a + b, 0);
    let ordre = p.ordre_cp.length ? [...p.ordre_cp] : reac.activites.flatMap((at) => reac.competences.filter((c) => c.at_numero === at.numero).map((c) => c.numero));
    ordre = ordre.filter((n) => reac.competence(n));
    for (const c of reac.competences) if (!ordre.includes(c.numero)) ordre.push(c.numero);
    const poids = Object.assign(D.poidsCompetences(reac), Object.fromEntries(Object.entries(p.poids_cp).filter(([, v]) => v > 0)));
    const durees = D.repartir(reste, ordre.map((n) => poids[n]), PAS * 8);
    ordre.forEach((n, i) => { plan.minutes_cp[n] = durees[i]; });

    const seqs = [];
    seqs.push(["Accueil et positionnement", [S("Accueil, présentation du titre et positionnement", "Module d'accueil", "module", [
      O("Identifier le déroulé de la formation, les règles de vie et les interlocuteurs", 1, "Tour de table + livret d'accueil + règlement intérieur"),
      O(`Situer les ${reac.activites.length} activités types et ${reac.competences.length} compétences du titre`, 2, "Carte mentale collective du titre (AT → CP)"),
      O("Décrire les épreuves de l'examen et le dossier professionnel", 2, "Présentation de la fiche « Examen simplifié »"),
      O("Évaluer ses acquis de départ (positionnement)", 5, "Test de positionnement + entretien individuel (adaptations handicap si besoin)")], { minutes: mod.accueil })]]);
    const vus = [];
    ordre.forEach((n, idx) => {
      const cp = reac.competence(n);
      seqs.push([`CP${cp.numero} — ${cp.intitule}`, D.decouperCompetence(cp, plan.minutes_cp[n], p.part_evaluation_cp)]);
      const at = cp.at_numero;
      const restantes = ordre.slice(idx + 1).filter((m) => reac.competence(m).at_numero === at);
      if (!restantes.length && !vus.includes(at) && mod.ecf) {
        vus.push(at);
        const crit = reac.competences.filter((x) => x.at_numero === at).flatMap((x) => x.criteres);
        const a = reac.activite(at);
        seqs.push([`ECF AT${at}`, [S(`ECF — Évaluation en cours de formation AT${at}`, a ? a.intitule : "", "evaluation", [
          O(`Démontrer les compétences de l'AT${at} en situation type examen`, 5, "Étude de cas chronométrée sur le modèle de l'épreuve", "critere", crit),
          O("Analyser ses résultats et fixer ses axes de progrès", 4, "Correction collective + auto-positionnement sur les critères")],
          { at, minutes: Math.floor(mod.ecf / Math.max(reac.activites.length, 1)) })]]);
      }
    });
    const prods = [S("Dossier professionnel (DP) : rédaction accompagnée", "Arrêté du 22 décembre 2015 — dossier professionnel", "module", [
      O("Sélectionner les exemples de pratique professionnelle par activité type", 4, "Atelier : du vécu en entreprise à l'exemple rédigé (méthode STAR)"),
      O("Rédiger les exemples de pratique professionnelle du DP", 6, "Rédaction guidée + relecture croisée"),
      O("Vérifier la complétude du DP avant la session", 5, "Check-list de conformité")], { minutes: mod.dossier })];
    if (aProd)
      prods.push(S("Productions d'examen : documents et diaporamas", "Référentiel d'évaluation", "module",
        re.documents.filter((d) => !d.includes("Mise en forme")).map((d) => O(`Construire le plan du document : ${d}`, 6, "Plan détaillé validé par le formateur"))
          .concat(re.diaporamas.map((d) => O(`Concevoir le diaporama : ${d}`, 6, "Atelier diaporama : 1 idée = 1 diapositive")))
          .concat([O("S'entraîner à la présentation orale et au questionnement du jury", 3, "Oral blanc filmé + grille d'auto-évaluation")]), { minutes: mod.productions }));
    seqs.push(["Dossier professionnel et productions d'examen", prods.filter((s) => s.minutes)]);
    const ex = S("Examen blanc dans les conditions de la session", "Référentiel d'évaluation", "evaluation",
      re && re.epreuves.length ? re.epreuves.map((e) => O(`Réaliser l'épreuve « ${e.modalite} » (${e.duree})`, 5, "Conditions réelles : temps, consignes, jury simulé", "critere"))
        : [O("Réaliser les épreuves dans les conditions de la session", 5, "Conditions réelles", "critere")], { minutes: mod.examen });
    const bil = S("Bilan de formation et préparation à la session", "Module de clôture", "module", [
      O("Évaluer l'atteinte des objectifs de la formation", 5, "Questionnaire de satisfaction + bilan individuel"),
      O("Préparer la logistique et le mental du jour de l'examen", 3, "Check-list J-1 / Jour J")], { minutes: mod.bilan });
    seqs.push(["Examen blanc et bilan", [ex, bil].filter((s) => s.minutes)]);

    let num = 0;
    seqs.forEach(([titre, seances], k) => {
      const fin = [];
      for (const s of seances) {
        if (s.type_seance === "module" || !s.objectifs.some((o) => o.minutes)) {
          const d = D.repartir(s.minutes, s.objectifs.map(() => 1));
          s.objectifs.forEach((o, i) => { o.minutes = d[i]; });
        }
        fin.push(...scinder(s, p.max_minutes_seance));
      }
      for (const s of fin) { s.numero = ++num; s.sequence = k + 1; s.sequence_titre = titre; plan.seances.push(s); }
    });

    const file = plan.seances.flatMap((s) => s.objectifs.filter((o) => o.minutes > 0).map((o) => [s, o]));
    const aPlacer = file.reduce((t, [, o]) => t + o.minutes, 0);
    let cumul = 0, idx = 0, resteObj = file.length ? file[0][1].minutes : 0;
    const commences = new Set();
    for (const [j, deb, fin] of creneaux(p, aPlacer)) {
      let cur = deb;
      while (cur < fin && idx < file.length) {
        const [s, o] = file[idx], duree = Math.min(resteObj, fin - cur);
        cumul += duree;
        plan.lignes.push({ date: j, debut: cur, fin: cur + duree, minutes: duree, seance: s, objectif: o, suite: commences.has(o), cumul, pourcentage: aPlacer ? cumul / aPlacer : 0 });
        commences.add(o);
        cur += duree; resteObj -= duree;
        if (resteObj <= 0 && ++idx < file.length) resteObj = file[idx][1].minutes;
      }
      if (idx >= file.length) break;
    }
    plan.date_fin = plan.lignes.length ? plan.lignes[plan.lignes.length - 1].date : null;
    if (idx < file.length) plan.avertissements.push("Calendrier insuffisant : toutes les séances n'ont pas pu être placées.");
    if (plan.date_fin)
      for (let j = p.date_debut; j <= plan.date_fin; j = ajout(j, 1)) {
        const [ok, motif] = jourOuvre(p, j);
        if (!ok && motif !== "jour non travaillé en centre" && motif !== "semaine en entreprise") plan.jours_exclus.push([j, motif]);
      }
    if (p.date_examen && plan.date_fin && plan.date_fin >= p.date_examen)
      plan.avertissements.push(`La fin des cours (${fr(plan.date_fin)}) dépasse la date d'examen (${fr(p.date_examen)}) : revoir le calendrier ou la durée.`);
    return plan;
  }

  function scinder(s, max) {
    if (s.minutes <= max || s.objectifs.length < 2) return [s];
    const parties = [];
    let cour = [], t = 0;
    for (const o of s.objectifs) { if (cour.length && t + o.minutes > max) { parties.push(cour); cour = []; t = 0; } cour.push(o); t += o.minutes; }
    if (cour.length) parties.push(cour);
    if (parties.length === 1) return [s];
    return parties.map((objs, i) => Object.assign({}, s, { titre: `${s.titre} (partie ${i + 1}/${parties.length})`, objectifs: objs, minutes: objs.reduce((a, o) => a + o.minutes, 0) }));
  }

  // ---- Paramètres saisis → paramètres du plan
  function lireDate(s) {
    s = (s || "").trim();
    let m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
    if (m) return date(+m[1], +m[2], +m[3]);
    m = /^(\d{2})[/-](\d{2})[/-](\d{4})$/.exec(s);
    if (m) return date(+m[3], +m[2], +m[1]);
    return null;
  }
  const plages = (s) => (s || "").split(/[,;]/).map((x) => /^\s*(\d{1,2}[:h]\d{2})\s*-\s*(\d{1,2}[:h]\d{2})\s*$/.exec(x)).filter(Boolean).map((m) => [m[1].replace("h", ":"), m[2].replace("h", ":")]);

  function parametresDepuis(r, hypotheses) {
    let debut = lireDate(r.date_debut);
    if (!debut) {
      const t = new Date(), auj = date(t.getFullYear(), t.getMonth() + 1, t.getDate());
      debut = ajout(auj, 7 - jourSem(auj));
      hypotheses.push(`Date de début non fournie : lundi ${fr(debut)} retenu par défaut.`);
    }
    if (!(r.heures_centre > 0)) throw new Error("Indiquez la durée en centre (en heures) : la fiche France Compétences ne la donne pas.");
    const fermetures = [];
    for (const morceau of (r.fermetures || "").split(/[;\n]/)) {
      const m = /^\s*(\S+?)(?:\.\.(\S+))?\s*(.*)$/.exec(morceau);
      if (m && lireDate(m[1])) { const a = lireDate(m[1]); fermetures.push([a, (m[2] && lireDate(m[2])) || a, m[3].trim() || "fermeture"]); }
    }
    const jours = [...new Set(((r.jours || "").match(/[1-7]/g) || []).map((x) => +x - 1))].sort();
    return {
      date_debut: debut, heures_centre: +r.heures_centre, creneaux: plages(r.creneaux).length ? plages(r.creneaux) : [["08:30", "12:00"], ["13:00", "16:30"]],
      pauses: plages(r.pauses), jours_semaine: jours.length ? jours : [0, 1, 2, 3, 4], rythme: (r.rythme || "").replace(/[^CEce]/g, ""),
      fermetures, feries: true, date_examen: lireDate(r.date_examen), ordre_cp: ((r.ordre_cp || "").match(/\d+/g) || []).map(Number),
      poids_cp: Object.fromEntries([...(r.poids_cp || "").matchAll(/(\d+)\s*=\s*([\d.]+)/g)].map((m) => [+m[1], +m[2]])),
      h_accueil: +r.h_accueil, h_ecf_par_at: +r.h_ecf_par_at, h_dossier_pro: +r.h_dossier_pro, h_productions: +r.h_productions,
      h_examen_blanc: +r.h_examen_blanc, h_bilan: +r.h_bilan, part_evaluation_cp: 0.12, max_minutes_seance: 420,
    };
  }

  Object.assign(D, { MOIS, JOURS, construirePlan, parametresDepuis, fmtHm, fmtDuree, fr, iso, semaineIso, jourSem, paques, feries, lireDate, fenetres });
})(typeof window !== "undefined" ? window : globalThis);

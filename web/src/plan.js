/* Plan de cours d'une compétence, selon la méthode de décorticage YEBA FORMATIONS :
 *
 *  1. La « Description de la compétence – processus de mise en œuvre » est découpée en ACTIONS :
 *     une action commence par un verbe d'action et se termine par une virgule ou un point
 *     (« Mobiliser l'équipe et favoriser la cohésion autour des objectifs de l'établissement marchand. »).
 *     Un début de phrase de contexte (« Dans le respect des consignes…, ») est gardé à part, comme cadre.
 *  2. Les actions proches sont RASSEMBLÉES en grandes parties cohérentes (I, II, III…), dans l'ordre du
 *     REAC, pour que la formation soit « buvable » ; chaque action devient une petite partie (1, 2, 3…).
 *  3. Sous chaque petite partie, les sous-parties regroupent ce qui s'y rattache :
 *     a) savoirs, b) savoir-faire techniques, c) savoir-faire organisationnels, d) savoir-faire relationnels.
 *  4. Chaque grande partie est reliée aux critères de performance (REAC), aux épreuves (RE / RC)
 *     et au bloc de compétences (fiche RNCP) : c'est la base du suivi quotidien.
 * Le regroupement est automatique (ressemblance des mots et familles de notions) : il est
 * MODIFIABLE par le formateur, qui reste le seul juge de la cohérence pédagogique. */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const N = (s) => D.normaliser(s);

  const ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
  const SOUS_PARTIES = [["savoirs", "a", "Savoirs"], ["sf_techniques", "b", "Savoir-faire techniques"],
    ["sf_organisationnels", "c", "Savoir-faire organisationnels"], ["sf_relationnels", "d", "Savoir-faire relationnels"]];
  // mots en -er / -ir / -re qui ne sont pas des verbes à l'infinitif
  const PAS_VERBES = new Set(["notre", "votre", "entre", "autre", "contre", "titre", "ordre", "cadre", "centre", "offre", "membre", "nombre",
    "chiffre", "libre", "propre", "lettre", "registre", "manager", "dossier", "fichier", "premier", "dernier", "particulier", "metier",
    "chantier", "papier", "atelier", "calendrier", "quartier", "plusieurs", "leur", "leurs", "pour", "sur", "par", "hier", "fer", "mer",
    "super", "inter", "cher", "fier", "amer", "hiver", "partenaire", "matiere", "maniere", "primaire", "necessaire", "affaire",
    "tutoire", "inventaire", "horaire", "salaire", "barriere", "carriere", "frontiere", "derniere", "premiere", "filiere", "lumiere",
    "gestionnaire", "fournisseur", "noir", "soir", "espoir", "devoir", "pouvoir", "savoir", "avoir", "loisir", "desir", "plaisir", "avenir",
    "dire", "lire", "rire", "pire", "sire", "faire", "boire", "croire", "joindre"].map(N));
  const VERBES_COURTS = new Set(["faire", "dire", "lire", "etre", "avoir", "savoir", "pouvoir", "devoir", "joindre", "boire", "croire"].map(N));

  // « Mobiliser… », « S'assurer… », « Faire appliquer… » : le segment commence-t-il par un infinitif ?
  function commenceParVerbe(seg) {
    const m = /^\s*(?:s[’']|se\s+)?([A-Za-zÀ-ÿœ]+)/.exec(seg);
    if (!m) return false;
    const w = N(m[1]);
    if (VERBES_COURTS.has(w) && /^\s*(faire|etre)\s/i.test(N(seg))) return true;
    if (PAS_VERBES.has(w) || w.length < 4) return false;
    return /(er|ir|re|oir)$/.test(w);
  }
  const majuscule = (s) => (s ? s[0].toUpperCase() + s.slice(1) : s);
  // Découpe aux virgules hors parenthèses
  function segments(phrase) {
    const out = []; let cur = "", prof = 0;
    for (const ch of phrase) {
      if (ch === "(") prof++; else if (ch === ")") prof = Math.max(0, prof - 1);
      if (ch === "," && !prof) { out.push(cur.trim()); cur = ""; } else cur += ch;
    }
    if (cur.trim()) out.push(cur.trim());
    return out.filter(Boolean);
  }

  /* Étape 1 — actions. Chaque action garde sa phrase d'origine (traçabilité REAC) et son éventuel cadre. */
  function actions(cp) {
    const res = [];
    (cp.description || []).forEach((phrase, iPhrase) => {
      const segs = segments(phrase.replace(/\.$/, ""));
      let cadre = [], cour = null, local = [];
      const pousser = () => { if (cour) { cour.texte = majuscule(cour.texte.replace(/\s+(et|ou)$/i, "").trim()); res.push(cour); cour = null; } };
      segs.forEach((seg, k) => {
        if (commenceParVerbe(seg)) {
          pousser();
          cour = { texte: seg, cadre: cadre.concat(local).join(", "), origine: phrase, phrase: iPhrase };
          local = [];
        } else if (!cour) cadre.push(seg);
        // « …engagées et, en cas d'écarts persistants, proposer… » : le segment est le cadre de l'action suivante
        else if (/\s(et|ou)$/i.test(cour.texte) && segs.slice(k + 1).some(commenceParVerbe)) local.push(seg);
        else cour.texte += ", " + seg;
      });
      pousser();
      if (!res.some((a) => a.phrase === iPhrase)) res.push({ texte: majuscule(phrase.replace(/\.$/, "")), cadre: "", origine: phrase, phrase: iPhrase });
    });
    return res.map((a, i) => Object.assign(a, { index: i, verbe: D.verbeInitial(a.texte), niveau: D.niveauBloom(a.texte) }));
  }

  /* Thèmes métier : relient une action du processus aux savoirs qui la servent, même quand les mots diffèrent
   * (« Préparer et animer une réunion » ↔ « Organiser et animer des briefings »). Fragments cherchés dans le texte normalisé. */
  const THEMES = {
    communication: ["communi", "consign", "inform", "transmet", "expliq", "partag", "message", "ecoute", "questionnement", "interpersonnel", "rendre compte", "reformul", "procedure"],
    reunion: ["reunion", "briefing", "debriefing", "animer", "animation"],
    motivation: ["motiv", "stimul", "challeng", "concours", "team building", "cohesion", "feder", "dynamique", "engag", "mobilis", "impliq", "valoris", "reconnaiss", "leadership", "responsabilis"],
    posture: ["posture", "pratique managerial", "style", "techniques de management", "fondamentaux du management", "bienveill", "conflit", "adapter sa", "situations managerial", "dynamique de groupe", "intergeneration"],
    competences: ["competence", "professionnalis", "formation", "tutorat", "montee", "gpec", "developpement des", "potentiel", "accompagn", "progres", "fiche de poste", "fonctions"],
    entretien: ["entretien", "evaluat", "feedback", "recadr", "appreciation", "individuel"],
    projet: ["projet", "changement", "etape", "jalon", "experiment", "participati", "anticip"],
    amelioration: ["amelior", "correct", "preconis", "solution", "pdca", "deming", "qualite", "lean", "audit", "retour d", "continue", "dysfonction", "proposition"],
    organisation: ["planning", "planifi", "organis", "tache", "deleg", "charge de travail", "gestion du temps", "delai", "priorit", "coordon", "ressources", "horaire", "absence", "imprevu", "regul", "date butoir", "moyens humains"],
    cadre_legal: ["code du travail", "legislation", "reglement", "legal", "convention", "instance", "representati", "negociation", "droit", "responsabilite civile", "penale", "juridique", "contrat", "periode d", "politique rh", "conventionnel", "confidentialit"],
    sante_securite: ["securit", "hygiene", "prevention", "risque", "rps", "psychosoc", "qhse", "accident", "ergonom", "sante", "issues de secours", "manutention", "ohsas", "iso"],
    handicap: ["handicap", "discrimin", "inclusion", "rqth", "agefiph", "amenagement", "accessibil", "divers", "egalite", "pep", "referent"],
    numerique: ["numerique", "digital", "medias sociaux", "reseaux sociaux", "e-reputation", "image de marque", "personal branding", "applicatif", "bureautique", "systeme d", "logiciel", "collaborati", "tracabil", "omnicanal", "crm", "site", "outils de travail"],
    donnees: ["donnee", "indicateur", "tableau de bord", "analys", "synthes", "statisti", "ecart", "ratio", "kpi", "interpret", "calcul", "collecter", "collecte ", "resultat"],
    rentabilite: ["rentabil", "marge", "cout", "budget", "chiffre d", "demarque", "financ", "prix", "compte de resultat", "frais", "economique", "seuil"],
    client: ["client", "satisf", "fidelis", "argument", "vente", "conseil", "parcours d", "reclamation", "litige", "incivilit", "accueil", "attente", "consommation"],
    stock: ["stock", "approvision", "command", "inventaire", "reception", "livraison", "fournisseur", "rupture", "logisti", "entrepos", "reserve", "rangement"],
    merchandising: ["merchandis", "implant", "lineaire", "planogram", "vitrine", "balisage", "operations commerciales", "promotion", "theatralis", "signaletique", "assortiment", "offre de produits", "allee"],
    rse: ["rse", "gaspill", "dechet", "environnement", "durable", "valorisation des"],
    recrutement: ["recrut", "candidat", "selection", "integration", "nouvelle recrue", "onboarding", "profil", "besoins en ressources humaines", "embauche"],
  };
  const THEMES_REG = { cadre_legal: 1, sante_securite: 1, handicap: 1 };
  function themes(texte) {
    const n = " " + N(texte).replace(/[’']/g, " ").replace(/[^a-z0-9]+/g, " ") + " ";
    // un fragment doit commencer un mot (« collecter » ne doit pas attraper « négociation collective »)
    return new Set(Object.entries(THEMES).filter(([, frags]) => frags.some((f) => n.includes(" " + f))).map(([k]) => k));
  }
  // Signature d'un texte : racines de 5 lettres + thèmes (préfixés « # »)
  const VIDES = new Set("dans pour avec sans sous leur leurs entre selon afin ainsi notamment etre faire mettre oeuvre place partir compte cadre ensemble connaissance connaissances notions principes principales differents differentes techniques outils etablissement marchand marchands perimetre entreprise enseigne contexte adapte adaptee adaptes adaptees situation situations ensemble".split(" "));
  function signature(texte) {
    const r = new Set((N(texte).replace(/[’']/g, " ").match(/[a-z]{4,}/g) || []).filter((m) => !VIDES.has(m)).map((m) => m.slice(0, 5)));
    for (const t of themes(texte)) r.add("#" + t);
    return r;
  }
  // Poids : les marques rares dans la compétence comptent plus ; un thème partagé compte double
  function ponderation(listes) {
    const df = {};
    for (const js of listes) for (const j of js) df[j] = (df[j] || 0) + 1;
    return (j) => (j.startsWith("#") ? 2 : 1) / Math.sqrt(df[j] || 1);
  }
  const proximite = (a, b, w) => { let s = 0; for (const j of a) if (b.has(j)) s += w(j); return s; };

  /* Étape 2 — grandes parties : on découpe la suite des phrases du REAC (son ordre logique) en 2 à 5 blocs
   * consécutifs qui maximisent la proximité interne (programmation dynamique). Les actions d'une même
   * phrase restent ensemble ; une grande partie d'une seule phrase est pénalisée (« buvabilité »). */
  function regrouper(acts) {
    const unites = [];
    for (const a of acts) { const u = unites.find((x) => x.phrase === a.phrase); if (u) u.idx.push(a.index); else unites.push({ phrase: a.phrase, idx: [a.index] }); }
    const n = unites.length;
    if (n <= 2) return [acts.map((a) => a.index)];
    const sig = unites.map((u) => { const s = new Set(); for (const i of u.idx) for (const j of signature(acts[i].texte)) s.add(j); return s; });
    const w = ponderation(sig);
    const sim = sig.map((a) => sig.map((b) => proximite(a, b, w)));
    const cible = Math.max(2, Math.min(5, Math.round(n / 2.3)));
    const maxTaille = Math.max(2, Math.ceil(n / cible) + 1);
    const valeur = (i, j) => {                      // unités i..j incluses
      const t = j - i + 1;
      if (t > maxTaille) return -Infinity;
      if (t === 1) return -0.6;
      let s = 0, c = 0;
      for (let a = i; a <= j; a++) for (let b = a + 1; b <= j; b++) { s += sim[a][b]; c++; }
      return (s / c) * (t - 1);
    };
    // best[k][j] : meilleur découpage des unités 0..j-1 en k blocs
    const best = Array.from({ length: cible + 1 }, () => Array(n + 1).fill(-Infinity)), choix = Array.from({ length: cible + 1 }, () => Array(n + 1).fill(-1));
    best[0][0] = 0;
    for (let k = 1; k <= cible; k++)
      for (let j = 1; j <= n; j++)
        for (let i = k - 1; i < j; i++) {
          if (best[k - 1][i] === -Infinity) continue;
          const v = best[k - 1][i] + valeur(i, j - 1);
          if (v > best[k][j]) { best[k][j] = v; choix[k][j] = i; }
        }
    let k = cible;
    while (k > 1 && best[k][n] === -Infinity) k--;
    const bornes = [];
    for (let j = n; k > 0; k--) { const i = choix[k][j]; bornes.unshift([i, j - 1]); j = i; }
    return bornes.map(([i, j]) => unites.slice(i, j + 1).flatMap((u) => u.idx));
  }

  // Titre d'une grande partie : l'action la plus représentative, réduite à sa proposition principale (jamais de mot coupé)
  function titreGrande(membres) {
    let rep = membres[0];
    if (membres.length > 2) {
      const sg = membres.map((m) => signature(m.texte)), w = ponderation(sg);
      let best = -1;
      membres.forEach((m, i) => { const s = sg.reduce((t, o, k) => t + (k === i ? 0 : proximite(sg[i], o, w)), 0); if (s > best) { best = s; rep = m; } });
    }
    let t = rep.texte.replace(/\s+(afin d[e’']|pour |en vue d|en s[’']appuyant|en tenant|en expliquant|en utilisant|en concertation|en collaboration|en coordination|à partir d|dans le respect|en intégrant|en fonction d|dans le but)[\s\S]*$/i, "");
    t = D.simplifier(t.replace(/\s*\([^)]*\)/g, ""));
    // titre = proposition principale ENTIÈRE : on coupe seulement à une virgule, jamais au milieu d'une proposition ni d'un mot
    const v = t.indexOf(", ");
    if (t.length > 95 && v >= 35) t = t.slice(0, v);
    return majuscule(t);
  }

  /* Étape 3 — sous-parties : chaque savoir / savoir-faire va sous l'action qui le sert le plus (thèmes + mots).
   * Sans lien avec aucune action : les repères réglementaires (droit du travail, prévention, handicap) forment
   * une grande partie « Cadre et repères » ; les autres rejoignent l'action la plus proche, même faiblement. */
  function repartirItems(cp, acts) {
    const items = SOUS_PARTIES.flatMap(([attr]) => (cp[attr] || []).map((texte) => ({ attr, texte })));
    const ja = acts.map((a) => signature(a.texte + " " + (a.cadre || ""))), ji = items.map((it) => signature(it.texte));
    const w = ponderation(ja.concat(ji));
    const charge = acts.map(() => 0), orphelins = [];
    const affect = acts.map(() => Object.fromEntries(SOUS_PARTIES.map(([attr]) => [attr, []])));
    items.forEach((it, k) => {
      const sc = ja.map((a) => proximite(ji[k], a, w)), best = Math.max(...sc);
      const reglementaire = [...themes(it.texte)].some((t) => THEMES_REG[t]);
      if (best < 1.6 && reglementaire) { orphelins.push(it); return; }
      let i = sc.indexOf(best);
      if (best <= 0) i = charge.indexOf(Math.min(...charge));
      affect[i][it.attr].push(it.texte); charge[i]++;
    });
    return { affect, orphelins, charge };
  }

  // Étape 4 — liens avec l'évaluation : épreuves (RE / RC) et bloc RNCP de la compétence
  function liensEvaluation(cp, re, fiche) {
    const epreuves = re && re.epreuves ? re.epreuves.filter((e) => (e.competences || []).includes(cp.numero)).map((e) => `${e.modalite} (${e.duree})`) : [];
    let bloc = null;
    if (fiche && fiche.blocs) {
      const cle = N(cp.intitule).replace(/[^a-z0-9]+/g, " ").trim();
      bloc = fiche.blocs.find((b) => (b.competences || []).some((c) => { const k = N(c).replace(/[^a-z0-9]+/g, " ").replace(/\s*…$/, "").trim(); return k && (cle.startsWith(k.slice(0, 40)) || k.startsWith(cle.slice(0, 40))); })) || null;
    }
    const questions = re && re.productions ? re.productions.filter((p) => N(p.competence) === N(cp.intitule)).flatMap((p) => p.themes.map((t) => t[0])) : [];
    return { epreuves, bloc: bloc ? { code: bloc.code, intitule: bloc.intitule } : null, themes_jury: questions };
  }

  function planCompetence(cp, re, fiche) {
    const acts = actions(cp);
    if (!acts.length) acts.push({ texte: cp.intitule, cadre: "", origine: cp.intitule, phrase: 0, index: 0, verbe: D.verbeInitial(cp.intitule), niveau: D.niveauBloom(cp.intitule) });
    const groupes = regrouper(acts);
    const { affect, orphelins } = repartirItems(cp, acts);
    const parties = groupes.map((g, gi) => {
      const membres = g.map((i) => acts[i]);
      return { numero: ROMAINS[gi] || String(gi + 1), titre: titreGrande(membres), criteres: [],
        petites: membres.map((a, k) => ({ numero: k + 1, texte: a.texte, cadre: a.cadre, verbe: a.verbe, niveau: a.niveau, origine: a.origine,
          sous: SOUS_PARTIES.map(([attr, lettre, lib]) => ({ attr, lettre, titre: lib, items: affect[a.index][attr] })) })) };
    });
    // items sans lien : grande partie « cadre et repères » (souvent : réglementation, handicap, risques) ou action la moins chargée
    if (orphelins.length >= 3) {
      parties.push({ numero: ROMAINS[parties.length] || String(parties.length + 1), titre: "Appliquer le cadre réglementaire : droit du travail, prévention des risques, handicap et non-discrimination", criteres: [], reperes: true,
        petites: [{ numero: 1, texte: "Appliquer et faire appliquer les règles, la prévention et l'inclusion dans son périmètre", cadre: "", verbe: "Appliquer", niveau: 3, origine: "Savoirs et savoir-faire réglementaires du REAC, sans action dédiée dans la description",
          sous: SOUS_PARTIES.map(([attr, lettre, lib]) => ({ attr, lettre, titre: lib, items: orphelins.filter((o) => o.attr === attr).map((o) => o.texte) })) }] });
    } else for (const o of orphelins) {
      const toutes = parties.flatMap((p) => p.petites);
      const cible = toutes.reduce((m, p) => (p.sous.reduce((t, s) => t + s.items.length, 0) < m.sous.reduce((t, s) => t + s.items.length, 0) ? p : m), toutes[0]);
      cible.sous.find((s) => s.attr === o.attr).items.push(o.texte);
    }
    // critères de performance → grande partie la plus proche (la dernière à défaut)
    const jp = parties.map((p) => signature(p.titre + " " + p.petites.map((x) => x.texte + " " + x.sous.flatMap((z) => z.items).join(" ")).join(" ")));
    const wc = ponderation(jp);
    for (const c of cp.criteres || []) {
      const jc = signature(c), sc = jp.map((x) => proximite(jc, x, wc)), best = Math.max(...sc);
      parties[best > 0 ? sc.indexOf(best) : parties.length - 1].criteres.push(c);
    }
    return Object.assign({ cp: cp.numero, at: cp.at_numero, intitule: cp.intitule, parties, nbActions: acts.length,
      nbItems: SOUS_PARTIES.reduce((t, [attr]) => t + (cp[attr] || []).length, 0) }, liensEvaluation(cp, re, fiche));
  }

  // Plan complet du titre : AT → CP → I, II… → 1, 2… → a) b) c) d)
  function planDeCours(reac, re, fiche) {
    return reac.activites.map((at) => ({ numero: at.numero, intitule: at.intitule,
      competences: reac.competences.filter((c) => c.at_numero === at.numero).map((c) => planCompetence(c, re, fiche)) }));
  }

  // Contrôle d'exhaustivité : chaque savoir / savoir-faire / critère du REAC apparaît exactement une fois
  function controlePlan(cp, plan) {
    const vus = plan.parties.flatMap((p) => p.petites.flatMap((x) => x.sous.flatMap((s) => s.items)));
    const attendus = SOUS_PARTIES.flatMap(([attr]) => cp[attr] || []);
    return { complet: vus.length === attendus.length && attendus.every((a) => vus.includes(a)), items: vus.length, attendus: attendus.length,
      criteres: plan.parties.reduce((t, p) => t + p.criteres.length, 0) === (cp.criteres || []).length };
  }

  Object.assign(D, { THEMES, themesTexte: themes, actionsCompetence: actions, planCompetence, planDeCours, controlePlan, ROMAINS, SOUS_PARTIES });
})(typeof window !== "undefined" ? window : globalThis);

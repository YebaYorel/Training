const fs = require('fs'), path = require('path');
const NM = '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/'; const req = require('module').createRequire(NM + 'x.js');
globalThis.ExcelJS = req('exceljs'); globalThis.docx = req('docx'); globalThis.JSZip = req('jszip'); globalThis.PptxGenJS = req('pptxgenjs'); global.window = globalThis;
for (const f of ['referentiels', 'extraction', 'pedagogie', 'plan', 'planification', 'programme', 'exports', 'moteur']) require('/home/user/Training/web/src/' + f + '.js');
for (const f of ['donnees', 'suivi', 'generateur', 'documents', 'finances']) require('/home/user/Training/web/pilotage/src/' + f + '.js');
const D = globalThis.Decorticage, P = globalThis.Pilotage, COURS = require('./cours_v3.js'), SEQ = require('./seq.json');
(async () => {
  const lire = (n) => fs.readFileSync(NM + n, 'utf8'), brut = lire('js_REAC.txt');
  const analyse = { reac: D.analyserReac(brut, brut), fiche: D.analyserFiche(lire('js_FICHE.txt')), noms: {} }; analyse.re = D.analyserRe(lire('js_RE.txt'), analyse.reac);
  const identite = P.identiteYeba(), charte = Object.assign({ nom_organisme: 'YEBA FORMATIONS' }, P.initiales().charte);
  const png = fs.readFileSync('/home/user/Training/web/pilotage/src/logo_yeba.png');
  const logo = { dataURL: '', base64: '', ext: 'png', octets: new Uint8Array(png), ratio: 520 / 443 };
  const ctx = Object.assign(D.construireContexte(analyse, { heures_centre: 455, date_debut: '2026-11-02', jours: '1', creneaux: '08:00-12:00, 13:00-16:00', pauses: '10:00-10:15, 14:30-14:45', afficher_nom: true, afficher_logo: true }, charte, logo), { pied: P.blocMarque(identite) });
  const blob = await D.docWord({ charte, nomOrg: 'YEBA FORMATIONS', logo, pied: ctx.pied }, 'TP Manager d\'établissement marchand — Guide du formateur : séquençage annuel et 4 premiers cours', (o) => {
    o.encadre('Repères', ['Titre : TP Manager d\'établissement marchand (RNCP41853, niveau 5) — REAC TP-MEM V09 du 10/12/2025', 'Journée type : 08h00–12h00 et 13h00–16h00, pauses 10h00–10h15 et 14h30–14h45, soit 6 h 30 de formation effective',
      'Rythme : 1 journée par semaine, le lundi, sur 12 mois (au plus 52 lundis, soit 338 h avant jours fériés et fermetures). Action réalisée en sous-traitance pour Form\'à ou (Saint-Louis).', 'Délégués : élection obligatoire si l\'action dépasse 500 h (C. trav., R6352-9), organisée sous la responsabilité du directeur de l\'organisme (R6352-11) : à vérifier avec Form\'à ou ; sinon, désignation volontaire de représentants (cours 4).', 'Formateur et référent handicap : Aurélien LUMEKA']);
    o.h2('1. Comment raisonne un professionnel avant d\'écrire la première séance');
    [['Lire les référentiels avant le contenu', 'REAC (ce que fait le professionnel), RE/RC (comment il est évalué), fiche RNCP (blocs, débouchés). Les épreuves dictent les priorités : la mise en situation de 4 h porte sur l\'AT2, les productions écrites sur les AT1 et AT3.'],
     ['Connaître le public', 'Positionnement dès le 1er jour : expérience en magasin, aisance à l\'oral et à l\'écrit, niveau numérique, besoins d\'aménagement. On adapte le rythme, pas l\'exigence.'],
     ['Construire la sécurité avant l\'apprentissage', 'Un adulte n\'apprend pas s\'il a peur d\'être jugé. Le 1er jour sert à se connaître, à poser le cadre et à oser parler : c\'est un investissement, pas du temps perdu.'],
     ['Donner la carte du voyage', 'Les apprenants doivent voir tôt le titre entier, l\'examen et le dossier professionnel : le sens précède l\'effort.'],
     ['Architecturer en spirale', 'Chaque notion revient plusieurs fois, de plus en plus exigeante (Bruner). Chaque cours commence par 15 à 20 minutes de rappel actif du cours précédent.'],
     ['Tisser des fils rouges', 'Le dossier professionnel (un peu à chaque cours), le numérique (Word → Excel → PowerPoint → IA, placé juste avant d\'en avoir besoin), l\'entraînement aux épreuves.'],
     ['Évaluer pour faire progresser', 'Quiz éclair, grilles critériées, ECF à la fin de chaque activité type, examen blanc : on mesure souvent, on note peu, on corrige tout de suite.'],
     ['Réguler chaque semaine', 'Ce qui n\'est pas acquis est repris ; le planning se recale (le logiciel le fait à chaque séance notée). Les preuves Qualiopi naissent du travail réel.']].forEach(([t, x]) => { o.puce(t); o.note(x); });
    o.h2('2. L\'articulation de l\'année (12 mois)');
    o.p('Choix d\'ordre recommandé : AT1 (l\'équipe, utilisée tous les jours en entreprise), puis AT3 (les chiffres, qui nourrissent les décisions), puis AT2 (les opérations commerciales, évaluées en mise en situation de 4 h : on les place près de l\'examen pour qu\'elles soient fraîches et entraînées). L\'ordre du REAC (AT1, AT2, AT3) reste possible : le logiciel accepte les deux (réglage « Ordre des compétences »).');
    o.p('Le détail session par session est dans « Sequencage_MEM_48_sessions » (Excel et Word). Synthèse par mois :');
    const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'], parMois = new Map();
    for (const l of SEQ.lignes) { const d = new Date(l.date + 'T00:00:00Z'), k = `${MOIS[d.getUTCMonth()]} ${d.getUTCFullYear()}`; if (!parMois.has(k)) parMois.set(k, []); parMois.get(k).push(l); }
    o.tableau([['Mois', 'Sessions', 'Contenus', 'Évaluations']].concat([...parMois].map(([m, ls]) => [m, ls.map((l) => l.n).join(', '), [...new Set(ls.map((l) => l.titre.replace(/ \(\d+\/\d+\)$/, '')))].join(' ; '), [...new Set(ls.map((l) => l.evaluation).filter((e) => !/^Quiz éclair/.test(e)))].join(' ; ') || 'Quiz éclair et grilles'])));
    o.h2('3. La mise à niveau, les évaluations et leur traçabilité');
    o.p('Pourquoi avant l\'AT1 : les productions écrites, le dossier professionnel, les tableaux de bord de l\'AT3 et l\'oral reposent sur Word, Excel, PowerPoint et des sauvegardes fiables. Un stagiaire qui perd ses fichiers la veille d\'un examen blanc, ou qui ne sait pas calculer une évolution, échoue pour une raison qui n\'a rien à voir avec ses compétences de manager.');
    o.tableau([['Étape', 'Quand', 'Outil', 'Trace'], ['Positionnement (diagnostique)', 'Cours 2', '6 défis de 10 min', 'Classeur, onglet Positionnement'], ['Formatives', 'Cours 2, 3, 4', 'Quiz, page DP, mini-cas Excel, mini-oral, sauvegarde vérifiée chaque lundi', 'Onglet Formatives'],
      ['Sommative', 'Cours 4', 'Sujet de 60 min, barème /100, seuil 70 % par domaine', 'Onglet Sommative + grille signée'], ['Remédiation', 'Cours 5 et 6', 'Binôme, exercice ciblé, réévaluation', 'Onglet Remédiation'], ['Synthèse', 'Après le cours 4', 'Tableau de bord du groupe', 'Onglet Synthèse (bilan, donneur d\'ordre, audit)']]);
    o.p('La règle des sauvegardes (3 copies, 2 supports, 1 hors du centre) est vérifiée en ouverture de CHAQUE cours pendant tout le mois 1 : c\'est le scénario de l\'ordinateur 15 qu\'on veut rendre impossible.');
    o.h2('4. Les 4 premiers cours (sessions 1 à 4)');
    COURS.forEach((c, k) => {
      o.saut(); o.h3(`Cours ${k + 1} — ${D.fr(D.lireDate(c.date))} — ${c.pack.titre}`);
      if (c.module) o.p(`Module : ${c.module}`);
      if (c.seance.cp) o.p(`Activité type 1 · Compétence 1 « Animer l'équipe de son périmètre » · Grande partie ${c.seance.partie} (plan de cours du logiciel).`);
      o.p('Objectifs de séance :'); c.pack.objectifs_seance.forEach((x, i) => o.puce(`${i + 1}. ${x}`));
      o.tableau([['Horaire', 'Fonction d\'étayage', 'Activité', 'Modalité']].concat(c.pack.deroule.map((d) => [`${d.debut} – ${d.fin}`, d.phase, d.activite, d.modalite])));
      o.p('Critères de performance du FORMATEUR (je vérifie en fin de journée) :'); c.formateur.forEach((x) => o.puce('☐ ' + x));
    });
    o.saut(); o.h2('5. Critères de performance du REAC, par compétence et par grande partie');
    o.p('Repris mot pour mot du REAC. Le rattachement à une grande partie vient du plan de cours du logiciel (ajustable) : il indique où le critère est principalement travaillé ; tous les critères d\'une compétence sont évalués ensemble à l\'ECF.');
    for (const at of ctx.planCours) {
      o.h3(`AT${at.numero} — ${at.intitule}`);
      for (const pc of at.competences) {
        o.encadre(`CP${pc.cp} — ${pc.intitule}`, [`Évaluée par : ${pc.epreuves.join(' ; ') || 'voir RE'}`, `Bloc : ${pc.bloc ? pc.bloc.code : '—'}`].concat(analyse.reac.competence(pc.cp).criteres.map((c) => '✔ ' + c)));
        o.tableau([['Grande partie', 'Critères de performance rattachés']].concat(pc.parties.map((g) => [`${g.numero}. ${g.titre}`, g.criteres.length ? g.criteres.map((c) => '• ' + c).join('\n') : 'Prépare les critères des autres parties (voir encadré)'])));
      }
    }
    o.h2('6. Sources');
    ['REAC TP-MEM V09 du 10/12/2025 ; RE du TP MEM ; fiche France Compétences RNCP41853 (documents fournis)', 'Code du travail, art. L6352-3 (règlement intérieur) ; R6352-9 à R6352-14 (délégués des stagiaires) — Légifrance via la base JusticeLibre, consultée le 01/11/2026',
      'Bruner J. S. (1966), Toward a Theory of Instruction ; Wood, Bruner & Ross (1976) — étayage', 'Tuckman B. W. (1965), « Developmental sequence in small groups », Psychological Bulletin, 63(6) — étapes de vie d\'une équipe',
      'Leavitt H. J. & Mueller R. A. H. (1951), « Some effects of feedback on communication », Human Relations, 4 — communication à sens unique / double sens'].forEach((s) => o.puce(s));
  });
  const dest = process.argv[2];
  fs.writeFileSync(path.join(dest, 'Guide_formateur_MEM_sequencage_et_cours_1_a_4.docx'), Buffer.from(await blob.arrayBuffer()));
  console.log('guide ok');
})().catch((e) => { console.error(e); process.exit(1); });

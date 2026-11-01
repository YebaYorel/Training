const fs = require('fs'), path = require('path');
const NM = '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/'; const req = require('module').createRequire(NM + 'x.js');
globalThis.docx = req('docx'); global.window = globalThis;
for (const f of ['referentiels', 'pedagogie', 'planification', 'exports']) require('/home/user/Training/web/src/' + f + '.js');
for (const f of ['donnees', 'documents']) require('/home/user/Training/web/pilotage/src/' + f + '.js');
const D = globalThis.Decorticage, P = globalThis.Pilotage;
const png = fs.readFileSync('/home/user/Training/web/pilotage/src/logo_yeba.png');
const ctx = { charte: Object.assign({}, P.initiales().charte), nomOrg: 'YEBA FORMATIONS', logo: { octets: new Uint8Array(png), ratio: 520 / 443 }, pied: P.blocMarque(P.identiteYeba()) };
const EP = [
  ['Épreuve 1 — Word', 20, 15, 'Ouvrez « Sommative_procedure_a_mettre_en_forme.docx ». Mettez-la en forme comme une procédure professionnelle, puis exportez-la en PDF.',
    [['Styles : Titre 1 pour le titre, Titre 2 pour les 3 parties', 6], ['Étapes en listes numérotées', 4], ['Tableau « Qui / Quoi / Quand » construit', 4], ['En-tête avec NOM Prénom et numéros de page', 3], ['Export PDF', 3]]],
  ['Épreuve 2 — Excel', 25, 20, 'Ouvrez « Sommative_donnees_ventes.xlsx ». Complétez le tableau et réalisez un graphique.',
    [['Total des ventes N-1 et N avec SOMME', 5], ['Moyenne avec MOYENNE', 4], ['Évolution de chaque rayon, au format %', 6], ['Part des ventes N avec une référence absolue ($)', 5], ['Histogramme des ventes N par rayon, avec titre', 5]]],
  ['Épreuve 3 — PowerPoint', 20, 10, 'Créez 2 diapositives « Les résultats de mon rayon » à partir de vos calculs Excel, puis exportez-les en PDF.',
    [['Une idée par diapositive', 5], ['Mots-clés, pas de phrases', 5], ['Texte de 28 pt minimum, bon contraste', 4], ['Graphique Excel ou image libre avec sa source', 3], ['Export PDF', 3]]],
  ['Épreuve 4 — Sauvegarde', 20, 5, 'Pendant toute l\'évaluation : nommez et sauvegardez vos 3 fichiers selon la règle 3-2-1.',
    [['Noms normés sur les 3 fichiers (NOM_Prénom_Sujet_Version_Date)', 6], ['Copie sur la clé USB', 4], ['Copie dans l\'espace en ligne', 4], ['Vérification : le formateur rouvre un fichier depuis la clé', 3], ['Clé éjectée proprement', 3]]],
  ['Épreuve 5 — IA et dossier professionnel', 15, 10, 'Rédigez une demande à l\'IA pour qu\'elle vous pose 5 questions sur une situation de travail (méthode STAR). Lisez sa réponse et notez une limite ou une erreur. Sans IA disponible : demande écrite sur papier et critique de la réponse imprimée fournie.',
    [['Demande avec rôle, tâche, contexte et format', 5], ['Aucune donnée personnelle (sinon 0 sur ce critère)', 5], ['Une limite ou une erreur de la réponse est repérée et expliquée', 5]]],
];
(async () => {
  const sujet = await D.docWord(ctx, 'Évaluation sommative de mise à niveau — Sujet stagiaire', (o) => {
    o.encadre('Consignes', ['Durée : 60 minutes. Même sujet, même durée et même barème pour tous.', 'Barème sur 100 points. Seuil d\'acquisition : 70 % dans CHAQUE domaine.', 'En dessous du seuil dans un domaine : un plan de remise à niveau personnalisé (pas une sanction).', 'Aménagements : prévus en amont avec le référent handicap.', 'Code stagiaire : ……   Date : 23/11/2026']);
    for (const [t, pts, mn, cons] of EP) { o.h2(`${t} — ${pts} points — ${mn} minutes conseillées`); o.p(cons); }
    o.p('Avant de rendre : vos 3 fichiers sont nommés, copiés sur la clé ET en ligne, et rouverts une fois.');
  });
  const grille = await D.docWord(ctx, 'Évaluation sommative de mise à niveau — Grille de correction FORMATEUR', (o) => {
    o.encadre('Document réservé au formateur', ['Reporter les points de chaque domaine dans l\'onglet « Sommative » du classeur de traçabilité.', 'Seuils : Word 14/20 · Excel 18/25 (arrondi de 17,5) · PowerPoint 14/20 · Sauvegarde 14/20 · IA 11/15 (arrondi de 10,5).']);
    for (const [t, pts, , , crit] of EP) { o.h2(`${t} — ${pts} points`); o.tableau([['Critère observable', 'Points', 'Obtenu']].concat(crit.map(([c, p]) => [c, String(p), ''])).concat([['Total du domaine', String(pts), ''], ['Seuil 70 % atteint ?', '', '☐ Oui   ☐ Non']])); }
    o.h2('Décision'); o.tableau([['Total /100', 'Domaines non acquis', 'Remédiation prévue (cours 5 et 6)', 'Signature formateur'], ['', '', '', '']]);
  });
  const dest = process.argv[2];
  fs.writeFileSync(path.join(dest, 'Sommative_sujet_stagiaire_cours4.docx'), Buffer.from(await sujet.arrayBuffer()));
  fs.writeFileSync(path.join(dest, 'Sommative_grille_correction_FORMATEUR_cours4.docx'), Buffer.from(await grille.arrayBuffer()));
  console.log('sommative ok');
})().catch((e) => { console.error(e); process.exit(1); });

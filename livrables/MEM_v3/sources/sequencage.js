/* Séquençage du TP MEM : 48 lundis du 02/11/2026 au 25/10/2027, 6 h 30 par session (312 h). */
const fs = require('fs');
const NM = '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/';
global.window = globalThis;
for (const f of ['referentiels', 'extraction', 'pedagogie', 'plan']) require('/home/user/Training/web/src/' + f + '.js');
const D = globalThis.Decorticage;
const brut = fs.readFileSync(NM + 'js_REAC.txt', 'utf8'), reac = D.analyserReac(brut, brut);
const re = D.analyserRe(fs.readFileSync(NM + 'js_RE.txt', 'utf8'), reac), fi = D.analyserFiche(fs.readFileSync(NM + 'js_FICHE.txt', 'utf8'));
// dates : lundis, hors lundi de Pâques (29/03/2027), lundi de Pentecôte (17/05/2027) et fermeture de fin d'année supposée (21 et 28/12/2026)
const exclus = { '2026-12-21': 'Fermeture de fin d\'année (hypothèse à confirmer avec Form\'à ou)', '2026-12-28': 'Fermeture de fin d\'année (hypothèse)', '2027-03-29': 'Lundi de Pâques (férié)', '2027-05-17': 'Lundi de Pentecôte (férié)' };
const dates = []; for (let d = new Date(Date.UTC(2026, 10, 2)); dates.length < 48; d.setUTCDate(d.getUTCDate() + 7)) { const iso = d.toISOString().slice(0, 10); if (!exclus[iso]) dates.push(iso); }
// sessions par compétence (ordre AT1 → AT3 → AT2) ; volumes REAC : CP1 98, CP2 85, CP3 46, CP4 62, CP5 70, CP6 68, CP7 48, CP8 52, CP9 53, CP10 66 ; AT2 renforcée (mise en situation de 4 h)
const NB = { 1: 4, 2: 3, 3: 2, 4: 3, 8: 2, 9: 3, 10: 2, 5: 3, 6: 3, 7: 3 };
const FIL = { 1: 'DP : situation STAR « j\'anime mon équipe »', 2: 'Excel : planning hebdomadaire, heures, couverture des créneaux ; DP', 3: 'Word : trame d\'entretien individuel ; DP', 4: 'Word : fiche de poste, parcours d\'intégration ; DP',
  8: 'Excel : tableau de bord, indicateurs, graphiques ; IA pour synthétiser (sans données personnelles)', 9: 'Excel : marges, frais de personnel, démarque, écarts', 10: 'PowerPoint : présenter un plan d\'actions à sa hiérarchie ; Word : production AT3',
  5: 'Excel : stocks, couverture, commandes ; DP AT2', 6: 'PowerPoint : implantation illustrée ; photos avant / après', 7: 'IA et numérique : omnicanal, avis clients, réseaux sociaux (règles RGPD) ; DP AT2' };
function decouper(cp, n) {
  const p = D.planCompetence(reac.competence(cp), re, fi), poids = p.parties.map((g) => 1 + g.petites.reduce((t, x) => t + x.sous.reduce((u, s) => u + s.items.length, 0), 0));
  // découpage en n blocs CONSÉCUTIFS (ordre du plan respecté) qui minimise le bloc le plus lourd (programmation dynamique)
  const m = p.parties.length, k = Math.min(n, m), pre = [0]; poids.forEach((w) => pre.push(pre[pre.length - 1] + w));
  const best = Array.from({ length: k + 1 }, () => Array(m + 1).fill(Infinity)), cut = Array.from({ length: k + 1 }, () => Array(m + 1).fill(0)); best[0][0] = 0;
  for (let g = 1; g <= k; g++) for (let j = g; j <= m; j++) for (let i = g - 1; i < j; i++) { const v = Math.max(best[g - 1][i], pre[j] - pre[i]); if (v < best[g][j]) { best[g][j] = v; cut[g][j] = i; } }
  const bornes = []; for (let g = k, j = m; g > 0; g--) { const i = cut[g][j]; bornes.unshift([i, j]); j = i; }
  const groupes = bornes.map(([i, j]) => p.parties.slice(i, j));
  return groupes.map((gs, r) => ({ cp, plan: p, parties: gs, rang: r + 1, sur: groupes.length }));
}
const S = [];
const add = (phase, at, cp, titre, contenu, fil, evaluation, criteres, epreuve) => S.push({ phase, at, cp, titre, contenu, fil, evaluation, criteres: criteres || [], epreuve: epreuve || '' });
add('Intégration', '', '', 'Bienvenue dans l\'aventure MEM', 'Cohésion (ABCDLettre, chaîne des prénoms), règlement intérieur, visite et sécurité, RGPD et référent handicap, portrait du manager, charte de groupe, positionnement sur les 10 compétences', 'Oral : éloquence', 'Positionnement métier (cible 1 à 4)');
add('Mise à niveau', '', '', 'Le titre, l\'examen, les sauvegardes et les pannes', 'Carte du titre et des 4 épreuves, dossier professionnel et méthode STAR, scénario de l\'ordinateur 15, règle 3-2-1, nommage des fichiers, fiche réflexe pannes', 'Arborescence MEM, sauvegarde réelle', 'Positionnement numérique (diagnostique) + quiz formatif');
add('Mise à niveau', '', '', 'Word et Excel : les outils du manager', 'Styles, navigation, tableau, PDF, page modèle du DP ; Excel : tableau, SOMME, MOYENNE, part (référence absolue), évolution, graphiques', 'Sauvegarde vérifiée', 'Formatives : page DP Word, mini-cas Excel');
add('Mise à niveau', '', '', 'PowerPoint, IA pour le dossier professionnel, évaluation sommative', 'Règles du diaporama accessible, masque, oral de 3 minutes ; IA : interviewer, structurer, reformuler sans données personnelles, versions v1-v2-v3 ; représentants du groupe', 'Sauvegarde vérifiée', 'SOMMATIVE de mise à niveau (/100, seuil 70 % par domaine)');
const bloc = (cps, at) => { for (const cp of cps) for (const s of decouper(cp, NB[cp])) add(`AT${at} · CP${cp}`, at, cp, `CP${cp} — ${reac.competence(cp).intitule} (${s.rang}/${s.sur})`,
  s.parties.map((g) => `${g.numero}. ${g.titre} : ` + g.petites.map((x) => `${g.numero}.${x.numero} ${x.texte}`).join(' ; ')).join('\n'),
  'Rituel spirale (rappel de la session précédente) ; ' + FIL[cp] + (s.rang === 1 && cp === 1 ? ' ; remédiation numérique ciblée' : ''), s.rang === s.sur ? `Quiz de compétence CP${cp} (10 questions) + grille critériée` : 'Quiz éclair + grille critériée', s.parties.flatMap((g) => g.criteres), s.plan.epreuves.join(' ; ')); };
bloc([1, 2, 3, 4], 1);
add('Révision AT1', 1, '', 'Révision de l\'activité type 1', 'Carte mentale AT1, cas transversaux (équipe démotivée, planning en crise, entretien difficile, intégration), remédiation sur les critères non acquis', 'DP : relecture des situations AT1', 'Évaluation formative AT1');
add('ECF AT1', 1, '', 'Évaluation en cours de formation — AT1', 'Étude de cas écrite et entretien sur le modèle du questionnement à partir de productions ; correction et auto-positionnement', 'Word', 'ECF AT1 (sommative) + satisfaction', reac.competences.filter((c) => c.at_numero === 1).flatMap((c) => c.criteres), 'Questionnement à partir de production(s)');
bloc([8, 9, 10], 3);
add('Révision AT3 + bilan', 3, '', 'Révision de l\'activité type 3 et bilan à mi-parcours', 'Cas chiffré complet (indicateurs → rentabilité → plan d\'actions) ; nouvelle cible des 10 compétences ; entretiens individuels de mi-parcours', 'Excel, PowerPoint', 'Bilan à mi-parcours (cible) + formative AT3');
add('ECF AT3', 3, '', 'Évaluation en cours de formation — AT3', 'Analyse d\'un tableau de bord, calculs de rentabilité, plan d\'actions présenté ; correction', 'Excel, PowerPoint', 'ECF AT3 (sommative)', reac.competences.filter((c) => c.at_numero === 3).flatMap((c) => c.criteres), 'Questionnement à partir de production(s)');
add('Productions', '', '', 'Productions écrites AT1 et AT3 — atelier 1', 'Cahier des charges des productions (RE), plan détaillé, choix des situations d\'entreprise, rédaction accompagnée', 'Word, IA (reformulation sans données personnelles)', 'Plan validé par le formateur');
add('Productions', '', '', 'Productions écrites AT1 et AT3 — atelier 2', 'Rédaction, relecture croisée, annexes, mise en forme, entraînement au questionnement par le jury', 'Word', 'Grille de conformité des productions');
bloc([5, 6, 7], 2);
add('ECF AT2', 2, '', 'Mise en situation blanche AT2 (ECF)', 'Mise en situation professionnelle de 4 h + entretien technique de 1 h 30, dans les conditions de l\'examen', 'Sauvegardes, Excel', 'ECF AT2 (sommative)', reac.competences.filter((c) => c.at_numero === 2).flatMap((c) => c.criteres), 'Mise en situation professionnelle ; Entretien technique');
add('Révision AT2', 2, '', 'Révision de l\'activité type 2 et remédiation', 'Retour détaillé sur la mise en situation blanche, ateliers ciblés approvisionnement / merchandising / expérience client', 'DP AT2', 'Remédiation tracée');
add('Productions et DP', '', '', 'Finalisation des productions', 'Relecture finale, cohérence avec le REAC, conformité RE, impression et sauvegarde', 'Word, PDF, 3-2-1', 'Productions finalisées');
add('Productions et DP', '', '', 'Finalisation du dossier professionnel', 'Relecture des exemples pour chaque activité type, preuves, annexes, déclaration sur l\'honneur', 'Word, PDF', 'DP complet');
add('Examen blanc', '', '', 'Examen blanc — jour 1', 'Mise en situation professionnelle (4 h) + entretien technique (1 h 30)', 'Conditions réelles', 'Examen blanc (sommative)', [], 'Mise en situation professionnelle ; Entretien technique');
add('Examen blanc', '', '', 'Examen blanc — jour 2', 'Questionnement à partir des productions (2 h 10) + entretien final (15 min) + restitution individuelle', 'Conditions réelles', 'Examen blanc (sommative)', [], 'Questionnement à partir de production(s) ; Entretien final');
add('Remédiation', '', '', 'Remédiation après l\'examen blanc', 'Ateliers par besoin (groupes de niveau), reprises ciblées sur les critères non acquis', 'Selon besoins', 'Formative ciblée');
add('Oral', '', '', 'Préparation à l\'oral', 'Entretien final : parcours, projet ; entretien technique : questions types ; gestion du stress, posture', 'Oral filmé (avec accord écrit)', 'Grille d\'oral');
add('Révisions', '', '', 'Révisions générales', 'Quiz géant sur les 10 compétences, mises en situation flash, fiches mémo', 'Fiches mémo', 'Formative globale');
add('Clôture', '', '', 'Bilan de formation et préparation de la session d\'examen', 'Logistique du jour J (convocation, pièces, horaires), bilan individuel et collectif, satisfaction à chaud, attestation', '—', 'Satisfaction + bilan');
if (S.length !== 48) throw new Error('Nombre de sessions : ' + S.length);
const lignes = S.map((s, i) => Object.assign({ n: i + 1, date: dates[i], heures: 6.5, cumul: (i + 1) * 6.5 }, s));
fs.writeFileSync(process.argv[2], JSON.stringify({ lignes, exclus, total: 48 * 6.5 }, null, 1));
console.log('sessions', lignes.length, 'du', dates[0], 'au', dates[47], '—', 48 * 6.5, 'h');
for (const l of lignes) console.log(String(l.n).padStart(2), l.date, l.phase.padEnd(22), l.titre.slice(0, 90));

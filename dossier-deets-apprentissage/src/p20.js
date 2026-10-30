const rdv = require('./rdv');
const cal = require('./cal');
const R = (m) => { const r = rdv.find((x) => x.mois === m); return `**${r.date}** — ${r.titre}`; };
const C = (m) => { const x = cal.mois.find((y) => y.mois === m); const mo = m.split(' ')[0].toLowerCase(); return `Mardis ${x.cours.map((d) => (d === '1' ? '1er' : d)).join(', ')} ${mo}${x.intensive ? ` ; semaine intensive ${x.intensive}` : ''}`; };
const H = ['Période', 'Au CFA (cours)', 'Pédagogie, évaluations, dossier professionnel', 'Apprentis : suivi et accompagnement', 'Entreprises et maîtres d’apprentissage', 'Rendez-vous du mois', 'Pilotage et obligations de YEBA FORMATIONS'];
const W = [1250, 1750, 2450, 2450, 2400, 1950, 2320];
module.exports = {
  num: '20',
  slug: '20_Planning_annuel_promotion_MEM_2027-2028',
  title: 'Planning annuel — Promotion MEM 2027-2028',
  objet: 'Planning complet de la préparation (novembre 2026) à l’après-formation (2028) : mardis de formation, semaines intensives, évaluations, dossier professionnel, suivi des apprentis, actions auprès des entreprises et des partenaires, Rendez-vous du mois et obligations de l’organisme.',
  landscape: true,
  blocks: [
    ['h1', '1. Repères de l’année'],
    ['table', ['Repère', 'Date'], [
      ['Contrats d’apprentissage (12 mois)', 'Du 1er mars 2027 au 29 février 2028'],
      ['Rythme', '**Chaque mardi au CFA**, 8 h – 12 h et 13 h – 16 h (pauses de 15 minutes à 10 h et à 15 h) ; les quatre autres jours en entreprise'],
      ['Mardis de cours', `${cal.nbCours} mardis (${cal.heures.mardis} heures)`],
      ['Rendez-vous du mois', `Un mardi par mois (12 × 7 heures = ${cal.heures.rdv} heures ; pièce n° 19)`],
      ['Semaines intensives (fin de formation)', 'Du 24 au 28 janvier 2028 et du 7 au 11 février 2028 (70 heures)'],
      ['Total de la formation au CFA', `${cal.heures.total} heures (minimum légal : environ 402 heures, art. L.6211-2 du Code du travail)`],
      ['Évaluations passées en cours de formation (ECF)', 'CCP 1 : mardi 29 juin 2027 — CCP 2 : mardi 26 octobre 2027 — CCP 3 : jeudi 27 janvier 2028 — examen blanc : vendredi 28 janvier 2028'],
      ['Entretiens trimestriels individuels', 'Mai, août, novembre 2027 et février 2028, en entreprise ou en visio, hors mardis (45 minutes)'],
      ['Visites en entreprise', 'Du 12 avril au 7 mai 2027 (avant la fin des 45 premiers jours de formation pratique) et septembre 2027, plus toute visite sur alerte'],
      ['Session de validation du titre', 'Semaine du 21 février 2028 [[date fixée après agrément de la DEETS]]'],
    ], [4500, 10070]],

    ['h1', '2. Préparation : novembre 2026 – février 2027'],
    ['table', H, [
      ['Nov. – déc. 2026', '—', 'Finalisation du programme, du livret d’apprentissage, des supports et du guide du dossier professionnel', 'Recrutement : réunions d’information tous les 15 jours, entretiens, tests de positionnement ; job dating en décembre', 'Prospection (15 contacts qualifiés par semaine) ; petits-déjeuners « Recruter un apprenti » ; lettres d’intention ; présentation du rythme du mardi', '—', 'Suivi du dossier DEETS ; recherche de l’intervenant expert CCP 3 et du sous-traitant placement ; information de QUALITIA sur le lieu de formation de Technor'],
      ['Janvier 2027', '—', 'Préparation des journées d’intégration ; banque d’études de cas de commerces réunionnais', 'Entretiens ; préparation des candidats aux entretiens d’embauche ; job dating', 'Fiche « Adéquation poste / référentiel » ; désignation des maîtres d’apprentissage ; signature des premiers contrats', 'Sollicitation des intervenants de mars à juin', '**Dépôt de la demande d’agrément MEM** auprès de la DEETS (janvier – mars) ; règlement intérieur, DUERP, assurance, registre des traitements RGPD'],
      ['Février 2027', '—', 'Calendrier des mardis remis à chaque apprenti', 'Finalisation des contrats ; information des jeunes encore sans employeur sur le démarrage sans contrat (3 mois au plus)', '**Réunion de lancement des maîtres d’apprentissage** (mardi 16 février, 17 h – 19 h) ; conventions de formation avec le calendrier annexé', 'Confirmation écrite des intervenants de mars et avril', 'Liste définitive des apprentis ; contrats de sous-traitance signés ; cartes d’étudiant des métiers'],
    ], W],

    ['h1', '3. Année de formation : mars 2027 – février 2028'],
    ['table', H, [
      ['Mars 2027', C('Mars 2027'), 'Journées d’intégration (2 et 9 mars) : statut d’apprenti, droits, santé-sécurité, égalité, positionnement ; démarrage du CCP 1', 'Livret d’accueil, règlement intérieur ; **carte d’étudiant des métiers** ; binômes d’entraide ; jeunes sans employeur : recherche d’emploi accompagnée chaque semaine', 'Appel à chaque maître d’apprentissage (semaine du 8 mars) ; **contrats transmis à l’OPCO par l’employeur au plus tard le samedi 6 mars** ; visites médicales d’embauche à programmer', R('Mars 2027'), 'Émargements ; questionnaires à chaud ; relevé mensuel d’assiduité aux employeurs'],
      ['Avril 2027', C('Avril 2027'), 'CCP 1 ; présentation du dossier professionnel (6 avril) ; **élection des délégués** (13 avril)', 'Point hebdomadaire avec les jeunes sans contrat', '**1res visites en entreprise** (12 avril – 7 mai) ; **formation des maîtres d’apprentissage** (jeudi 29 avril)', R('Avril 2027'), 'Demande d’agrément déposée ; vérification des visites médicales'],
      ['Mai 2027', C('Mai 2027'), 'CCP 1', '**Entretien trimestriel n° 1** ; 31 mai : fin des 3 mois sans contrat, bilan et réorientation si besoin (Mission locale, France Travail)', 'Point téléphonique avec chaque maître d’apprentissage', R('Mai 2027'), 'Bilan pédagogique et financier 2026 [[échéance à vérifier]]'],
      ['Juin 2027', C('Juin 2027'), 'CCP 1 ; **ECF du CCP 1** (mardi 29 juin) ; activité type 1 du dossier professionnel', 'Retours individuels ; plans de remédiation', 'Résultats de l’ECF ; **rappel : congés hors mardis et semaines intensives**', R('Juin 2027'), '**Conseil de perfectionnement** (mardi 29 juin, 16 h 30 – 18 h)'],
      ['Juillet 2027', C('Juillet 2027'), 'CCP 2', 'Préparation du tournoi solidaire', 'Rappel du calendrier du second semestre', R('Juillet 2027'), 'Préparation du questionnaire de mi-parcours'],
      ['Août 2027', C('Août 2027'), 'CCP 2 ; bilan collectif de mi-parcours (31 août)', '**Entretien trimestriel n° 2** ; **questionnaire de satisfaction de mi-parcours**', 'Point téléphonique avec chaque maître d’apprentissage ; lots pour le tournoi', R('Août 2027'), '**Date limite de la demande d’agrément pour l’examen : 21 août 2027** (6 mois avant la session)'],
      ['Sept. 2027', C('Septembre 2027'), 'CCP 2', 'Entretien « Et après ? » sur le projet de fin de contrat', '**2es visites en entreprise** ; réunion des maîtres d’apprentissage (mardi 14 septembre, 16 h 30 – 18 h)', R('Septembre 2027'), '**Lancement du recrutement de la promotion 2028**'],
      ['Oct. 2027', C('Octobre 2027'), 'CCP 2 ; **ECF du CCP 2** (mardi 26 octobre) ; activité type 2 du dossier professionnel', 'Retours individuels ; plans de remédiation', 'Point avec chaque employeur sur une éventuelle embauche après le contrat', R('Octobre 2027'), 'Confirmation de la date de session avec la DEETS ; recrutement 2028'],
      ['Nov. 2027', C('Novembre 2027'), 'CCP 3 ; module « Esprit d’entreprendre » (mardi 16 novembre)', '**Entretien trimestriel n° 3** ; CV de manager et pitch', 'Invitation au job dating ; **rappel : congés de fin d’année hors mardis**', R('Novembre 2027'), 'Constitution du jury de la session [[selon le règlement des sessions]]'],
      ['Déc. 2027', C('Décembre 2027'), 'CCP 3 ; activité type 3 du dossier professionnel', 'Collecte solidaire dans les magasins (1er – 13 décembre)', 'Accord des employeurs pour la collecte', R('Décembre 2027'), '**Conseil de perfectionnement** (mardi 7 décembre, 16 h 30 – 18 h) ; inscription des candidats à la session ; fin de la fenêtre de l’**audit de surveillance Qualiopi**'],
      ['Janv. 2028', C('Janvier 2028'), 'CCP 3 ; **ECF du CCP 3** (jeudi 27) ; **examen blanc** (vendredi 28)', 'Plan de révision individuel', 'Réunion des maîtres d’apprentissage (mardi 11 janvier, 16 h 30 – 18 h) ; **questionnaire de satisfaction des maîtres d’apprentissage**', R('Janvier 2028'), 'Livret d’ECF ; convocations à la session'],
      ['Févr. 2028', C('Février 2028'), 'Révisions ; remise des dossiers professionnels (vendredi 11) ; oraux blancs ; **session de validation** (semaine du 21)', '**Entretien trimestriel n° 4** (bilan final) ; **questionnaire de fin de formation**', '**Questionnaire de satisfaction des employeurs** ; fin des contrats le 29 février', R('Février 2028'), 'Organisation de la session ; attestations de fin de formation ; ouverture de la promotion 2028 (1er mars)'],
    ], W],

    ['h1', '4. Après la formation'],
    ['table', ['Période', 'Action', 'Responsable'], [
      ['Mars 2028', 'Résultats de la session et remise des titres', 'YEBA FORMATIONS'],
      ['Mai 2028', 'Bilan pédagogique et financier 2027 [[échéance à vérifier]]', 'YEBA FORMATIONS'],
      ['Août 2028', '**Enquête d’insertion à 6 mois** ; **publication des indicateurs de résultats** (art. L.6111-8 du Code du travail)', 'YEBA FORMATIONS'],
      ['Février 2029 et février 2030', 'Enquêtes de suivi des anciens à 12 et 24 mois (pièce n° 14)', 'YEBA FORMATIONS'],
      ['Chaque année', 'Rencontre des anciens et des apprentis en cours ; témoignages lors des réunions d’information', 'YEBA FORMATIONS, anciens volontaires'],
    ], [3000, 8570, 3000]],

    ['h1', '5. Qui fait quoi ?'],
    ['table', ['Acteur', 'Engagements pendant l’année'], [
      ['Apprentis', ['Être présents et ponctuels chaque mardi, aux Rendez-vous du mois et aux deux semaines intensives (émargement).', 'Tenir à jour le livret d’apprentissage et rédiger le dossier professionnel au fil de l’année.', 'Passer les trois ECF, l’examen blanc et la session de validation.', 'Préparer les rencontres (questions, CV, pitch) et participer à l’organisation du tournoi et de la collecte de Noël.', 'Signaler sans attendre toute difficulté au référent ou aux délégués.']],
      ['Employeurs et maîtres d’apprentissage', ['Confier des missions couvrant les trois activités types, dont l’encadrement d’un périmètre.', 'Libérer l’apprenti chaque mardi et pendant les deux semaines intensives.', 'Participer à la réunion de lancement, à la formation des maîtres d’apprentissage, aux visites et aux points trimestriels.', 'Compléter le livret et valider les situations décrites dans le dossier professionnel.', 'Transmettre le contrat et la convention à l’OPCO dans les 5 jours ouvrables suivant le début du contrat, et organiser la visite d’information et de prévention.']],
      ['Partenaires et intervenants', ['Animer un Rendez-vous du mois à la date convenue.', 'Adapter leur intervention au métier de manager d’établissement marchand.', 'Respecter les règles de protection des données et du droit à l’image.']],
      ['YEBA FORMATIONS', [`Dispenser les ${cal.heures.enseignement} heures d’enseignement et organiser les 12 Rendez-vous du mois.`, 'Assurer le suivi individuel : entretiens trimestriels, visites, alertes, remédiation.', 'Organiser les ECF et la session de validation, sous réserve de l’agrément de la DEETS.', 'Accompagner la recherche d’employeur, la gestion des ruptures et l’insertion après le titre.', 'Piloter la qualité : satisfaction, conseil de perfectionnement, indicateurs, Qualiopi.']],
    ], [3000, 11570]],

    ['h1', '6. Échéancier des obligations et des temps forts'],
    ['table', ['Obligation ou temps fort', 'Échéance', 'Responsable', 'Référence'], [
      ['Convention de formation avec le calendrier annexé (mardis, Rendez-vous du mois, semaines intensives)', 'Avant le 1er mars 2027', 'CFA et employeur', 'Art. L.6353-1 C. trav.'],
      ['**Transmission des contrats à l’OPCO** (avec la convention de formation)', 'Au plus tard 5 jours ouvrables après le début du contrat, soit le samedi 6 mars 2027', 'Employeur, avec l’appui du CFA', 'Art. L.6224-1 et D.6224-1 C. trav.'],
      ['**Carte d’étudiant des métiers**', 'Remise lors des journées d’intégration (mardis 2 et 9 mars 2027)', 'CFA', '[[Référence à vérifier]]'],
      ['**Visite médicale d’embauche** (visite d’information et de prévention)', 'Dans les délais réglementaires suivant l’embauche, au plus tard fin avril 2027 [[délai à vérifier]]', 'Employeur', 'Code du travail, santé au travail'],
      ['Information des apprentis sur leurs droits, la santé et la sécurité', 'Journées d’intégration (2 et 9 mars 2027)', 'CFA', 'Art. L.6231-2 C. trav.'],
      ['**Congés des apprentis à poser hors des mardis et des semaines intensives**', 'Rappel à la signature, puis en juin et en novembre 2027', 'Employeur, sur rappel du CFA', '—'],
      ['**Audit de surveillance Qualiopi** (certificat QUALITIA n° 25FOR02027.1, valable jusqu’au 16/02/2029)', 'Entre février et décembre 2027 [[date à fixer avec QUALITIA]]', 'CFA', 'Art. L.6316-1 C. trav.'],
      ['**Questionnaires de satisfaction**', 'À chaud : chaque mardi de cours (court), chaque Rendez-vous et chaque semaine intensive ; mi-parcours : août 2027 ; fin de formation : février 2028 ; maîtres d’apprentissage : janvier 2028 ; employeurs : février 2028', 'CFA', 'Référentiel national qualité'],
      ['**Conseil de perfectionnement**', 'Mardi 29 juin et mardi 7 décembre 2027, 16 h 30 – 18 h', 'CFA, avec délégués, employeurs et maîtres d’apprentissage', '[[Article à vérifier]]'],
      ['**Date limite de la demande d’agrément pour l’examen**', 'Au plus tard 6 mois avant la session, soit le 21 août 2027 (dépôt visé dès le premier trimestre 2027)', 'CFA', 'Arrêtés du 22 décembre 2015 et du 21 juillet 2016'],
      ['**Recrutement de la promotion 2028**', 'À partir de septembre 2027 (réunions d’information, prospection, job dating)', 'CFA', '—'],
      ['**Enquête d’insertion à 6 mois**', 'Août 2028', 'CFA', 'Art. L.6111-8 C. trav.'],
      ['**Indicateurs de résultats à publier** (taux d’obtention, d’insertion, de rupture, de poursuite d’études…)', 'Chaque année, après les résultats de la promotion [[calendrier national à vérifier]]', 'CFA', 'Art. L.6111-8 C. trav.'],
      ['Registre des traitements, information des apprentis, autorisations de droit à l’image', 'Avant le 1er mars 2027', 'CFA', 'RGPD, art. 13 et 30'],
    ], [5200, 4300, 2600, 2470]],
    ['rgpd', [
      '**RGPD** — Le planning implique des données d’apprentis mineurs et majeurs, de maîtres d’apprentissage et d’intervenants : le registre des traitements recense chaque usage (suivi, évaluations, événements, enquêtes d’insertion), sa durée de conservation et ses destinataires. Les outils de suivi sont hébergés dans l’Union européenne.',
      '**IA Act** — Aucune décision concernant un apprenti (évaluation, alerte de décrochage, présentation à un employeur) n’est confiée à un système d’IA.',
    ]],
  ],
};

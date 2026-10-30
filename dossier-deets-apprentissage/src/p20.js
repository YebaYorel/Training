const rdv = require('./rdv');
const R = (m) => { const r = rdv.find((x) => x.mois === m); return `**${r.date.replace(/^Mardi /, 'Mar. ')}** — ${r.titre}`; };
const H = ['Période', 'Semaine au CFA', 'Pédagogie, évaluations, dossier professionnel', 'Apprentis : suivi et accompagnement', 'Entreprises et maîtres d’apprentissage', 'Rendez-vous du mois', 'Pilotage et obligations de YEBA FORMATIONS'];
const W = [1350, 1450, 2550, 2550, 2450, 1900, 2320];
module.exports = {
  num: '20',
  slug: '20_Planning_annuel_promotion_MEM_2027-2028',
  title: 'Planning annuel — Promotion MEM 2027-2028',
  objet: 'Planning complet de la préparation (novembre 2026) à l’après-formation (2028) : semaines au CFA, évaluations, dossier professionnel, suivi des apprentis, actions auprès des entreprises et des partenaires, Rendez-vous du mois et obligations de l’organisme.',
  landscape: true,
  blocks: [
    ['h1', '1. Repères de l’année'],
    ['table', ['Repère', 'Date'], [
      ['Contrats d’apprentissage (12 mois)', 'Du 1er mars 2027 au 29 février 2028'],
      ['Semaines au CFA (12 × 35 heures)', '1er mars, 5 avril, 10 mai, 7 juin, 5 juillet, 2 août, 6 septembre, 4 octobre, 15 novembre, 6 décembre 2027, 10 janvier, 7 février 2028'],
      ['Rendez-vous du mois (12 × 7 heures)', 'Un mardi par mois, 8 h – 12 h et 13 h – 16 h, pendant une semaine en entreprise (pièce n° 19)'],
      ['Évaluations passées en cours de formation (ECF)', 'CCP 1 : 11 juin 2027 — CCP 2 : 8 octobre 2027 — CCP 3 : 13 janvier 2028 — examen blanc : 14 janvier 2028'],
      ['Entretiens trimestriels individuels', 'Mai, août, novembre 2027 et février 2028, pendant les semaines en entreprise (45 minutes, sur site ou en visio)'],
      ['Visites en entreprise', 'Du 12 au 30 avril 2027 (avant la fin des 45 premiers jours) et septembre 2027, plus toute visite sur alerte'],
      ['Session de validation du titre', 'Semaine du 21 février 2028 [[date fixée après agrément de la DEETS]]'],
    ], [4500, 10070]],

    ['h1', '2. Préparation : novembre 2026 – février 2027'],
    ['table', H, [
      ['Nov. – déc. 2026', '—', 'Finalisation du programme, du livret d’apprentissage, des supports et du guide du dossier professionnel', 'Recrutement : réunions d’information tous les 15 jours, entretiens, tests de positionnement ; job dating en décembre', 'Prospection (15 contacts qualifiés par semaine) ; petits-déjeuners « Recruter un apprenti » ; recueil des lettres d’intention', '—', 'Suivi du dossier DEETS ; question écrite aux OPCO sur le financement avant l’audit d’extension Qualiopi ; recherche de l’intervenant expert CCP 3 et du sous-traitant placement'],
      ['Janvier 2027', '—', 'Préparation de la semaine d’intégration ; banque d’études de cas de commerces réunionnais', 'Entretiens ; préparation des candidats aux entretiens d’embauche ; job dating', 'Fiche « Adéquation poste / référentiel » ; désignation des maîtres d’apprentissage ; signature des premiers contrats', 'Sollicitation des intervenants des Rendez-vous de mars à juillet', '**Dépôt de la demande d’agrément MEM** auprès de la DEETS (janvier – mars) ; règlement intérieur, DUERP, assurance, registre des traitements RGPD'],
      ['Février 2027', '—', 'Calendrier remis à chaque apprenti', 'Finalisation des contrats ; information des jeunes encore sans employeur sur le démarrage sans contrat (3 mois au plus)', '**Réunion de lancement des maîtres d’apprentissage** (mardi 16 février, 17 h – 19 h) ; signature des conventions de formation avec le calendrier annexé', 'Confirmation écrite des intervenants de mars et avril', 'Liste définitive des apprentis ; contrats de sous-traitance signés ; préparation de l’accueil'],
    ], W],

    ['h1', '3. Année de formation : mars 2027 – février 2028'],
    ['table', H, [
      ['Mars 2027', '1er – 5 mars', 'Intégration : statut d’apprenti, droits, santé-sécurité, égalité ; positionnement ; démarrage du CCP 1', 'Livret d’accueil, règlement intérieur, fiches « droits » ; carte d’étudiant des métiers ; **binômes d’entraide** ; pour les jeunes sans employeur : 2 demi-journées par semaine de recherche d’emploi au CFA', 'Appel au maître d’apprentissage (semaine du 8 mars) ; l’employeur transmet le contrat à l’OPCO et organise la visite d’information et de prévention', R('Mars 2027'), 'Émargements ; satisfaction à chaud ; relevé mensuel d’assiduité aux employeurs ; demande d’audit d’extension Qualiopi'],
      ['Avril 2027', '5 – 9 avril', 'CCP 1 ; **présentation du dossier professionnel** ; **élection des délégués** (vendredi 9 avril)', 'Recherche d’employeur renforcée pour les jeunes sans contrat (point hebdomadaire)', '**Formation des maîtres d’apprentissage** (mardi 27 avril) ; **1re visite en entreprise** (12 – 30 avril)', R('Avril 2027'), 'Audits Qualiopi (surveillance et extension « apprentissage ») entre février et décembre 2027 [[dates à fixer avec le certificateur]]'],
      ['Mai 2027', '10 – 14 mai', 'CCP 1', '**Entretien trimestriel n° 1** ; **31 mai : fin des 3 mois sans contrat** : bilan et réorientation si besoin, avec la Mission locale ou France Travail', 'Point téléphonique avec chaque maître d’apprentissage', R('Mai 2027'), 'Bilan pédagogique et financier 2026 [[échéance à vérifier]]'],
      ['Juin 2027', '7 – 11 juin', 'CCP 1 ; **ECF du CCP 1** (vendredi 11 juin) ; rédaction de l’activité type 1 du dossier professionnel', 'Retours individuels après l’ECF ; plans de remédiation', 'Information des maîtres d’apprentissage sur les résultats de l’ECF', R('Juin 2027'), '**Conseil de perfectionnement** (mardi 29 juin, 16 h 30 – 18 h) avec délégués, employeurs et maîtres d’apprentissage ; sollicitation des intervenants d’août à février'],
      ['Juillet 2027', '5 – 9 juillet', 'CCP 2', 'Rappel : congés payés à poser hors des semaines au CFA et des Rendez-vous', 'Rappel aux employeurs du calendrier et des congés', R('Juillet 2027'), 'Préparation du questionnaire de mi-parcours'],
      ['Août 2027', '2 – 6 août', 'CCP 2 ; **bilan collectif de mi-parcours** ; préparation du tournoi solidaire', '**Entretien trimestriel n° 2** ; questionnaire de satisfaction de mi-parcours', 'Point téléphonique avec chaque maître d’apprentissage ; lots pour le tournoi', R('Août 2027'), '**Date limite de dépôt de la demande d’agrément** (6 mois avant la session) : vérifier que le dossier est déposé'],
      ['Sept. 2027', '6 – 10 sept.', 'CCP 2', 'Entretien « Et après ? » sur le projet de fin de contrat', '**2e visite en entreprise** ; **réunion d’échange des maîtres d’apprentissage** (mardi 14 septembre)', R('Septembre 2027'), 'Lancement du recrutement de la promotion 2028 (réunions d’information, prospection)'],
      ['Oct. 2027', '4 – 8 oct.', 'CCP 2 ; **ECF du CCP 2** (vendredi 8 octobre) ; rédaction de l’activité type 2 du dossier professionnel', 'Retours individuels ; plans de remédiation', 'Point avec chaque employeur sur une éventuelle embauche à l’issue du contrat', R('Octobre 2027'), 'Confirmation de la date de session avec la DEETS ; recrutement de la promotion 2028'],
      ['Nov. 2027', '15 – 19 nov.', 'CCP 3 ; module « Esprit d’entreprendre »', '**Entretien trimestriel n° 3** ; ateliers « valoriser son expérience » (CV de manager, pitch)', 'Invitation des employeurs au job dating ; point téléphonique avec chaque maître d’apprentissage', R('Novembre 2027'), 'Constitution du jury de la session selon le règlement des sessions [[à confirmer avec la DEETS]]'],
      ['Déc. 2027', '6 – 10 déc.', 'CCP 3 ; rédaction de l’activité type 3 du dossier professionnel', 'Collecte solidaire dans les magasins (1er – 15 décembre)', 'Accord des employeurs pour la collecte en magasin', R('Décembre 2027'), '**Conseil de perfectionnement** (mardi 7 décembre, 16 h 30 – 18 h) ; inscription des candidats à la session [[délai à confirmer]]'],
      ['Janvier 2028', '10 – 14 janv.', 'CCP 3 ; **ECF du CCP 3** (jeudi 13 janvier) ; **examen blanc** (vendredi 14 janvier)', 'Plan de révision individuel', '**Réunion des maîtres d’apprentissage** (mardi 11 janvier) ; questionnaire de satisfaction des maîtres d’apprentissage', R('Janvier 2028'), 'Livret d’ECF complété ; convocations à la session'],
      ['Février 2028', '7 – 11 févr.', 'Révisions ; **remise du dossier professionnel** (vendredi 11 février) ; préparation à l’entretien avec le jury', '**Entretien trimestriel n° 4** (bilan final) ; **session de validation** (semaine du 21 février) ; questionnaire de fin de formation', 'Questionnaire de satisfaction des employeurs ; fin des contrats le 29 février', R('Février 2028'), 'Organisation matérielle de la session ; attestations de fin de formation ; bilan de l’année'],
    ], W],

    ['h1', '4. Après la formation'],
    ['table', ['Période', 'Action', 'Responsable'], [
      ['Mars 2028', 'Résultats de la session et remise des titres ; ouverture de la promotion 2028', 'YEBA FORMATIONS'],
      ['Mai 2028', 'Bilan pédagogique et financier 2027 [[échéance à vérifier]]', 'YEBA FORMATIONS'],
      ['Août 2028', 'Enquête d’insertion à 6 mois ; publication des indicateurs de résultats (art. L.6111-8 du Code du travail)', 'YEBA FORMATIONS'],
      ['Février 2029 et février 2030', 'Enquêtes de suivi des anciens à 12 et 24 mois (pièce n° 14)', 'YEBA FORMATIONS'],
      ['Chaque année', 'Rencontre des anciens et des apprentis en cours ; témoignages lors des réunions d’information', 'YEBA FORMATIONS, anciens volontaires'],
    ], [3000, 8570, 3000]],

    ['h1', '5. Qui fait quoi ?'],
    ['table', ['Acteur', 'Engagements pendant l’année'], [
      ['Apprentis', ['Être présents et ponctuels aux semaines au CFA et aux Rendez-vous du mois (émargement).', 'Tenir à jour le livret d’apprentissage et rédiger le dossier professionnel au fil de l’année.', 'Passer les trois ECF, l’examen blanc et la session de validation.', 'Préparer les rencontres (questions, CV, pitch) et participer à l’organisation du tournoi et de la collecte de Noël.', 'Signaler sans attendre toute difficulté au référent ou aux délégués.']],
      ['Employeurs et maîtres d’apprentissage', ['Confier des missions couvrant les trois activités types, dont l’encadrement d’un périmètre.', 'Libérer l’apprenti pour les semaines au CFA, les Rendez-vous du mois et les entretiens trimestriels.', 'Participer à la réunion de lancement, à la formation des maîtres d’apprentissage, aux visites et aux points trimestriels.', 'Compléter le livret et valider les situations décrites dans le dossier professionnel.', 'Transmettre le contrat à l’OPCO et organiser la visite d’information et de prévention dans les délais réglementaires.']],
      ['Partenaires et intervenants', ['Animer un Rendez-vous du mois à la date convenue.', 'Adapter leur intervention au métier de manager d’établissement marchand.', 'Respecter les règles de protection des données et du droit à l’image.']],
      ['YEBA FORMATIONS', ['Dispenser les 420 heures d’enseignement et organiser les 12 Rendez-vous du mois.', 'Assurer le suivi individuel : entretiens trimestriels, visites, alertes, remédiation.', 'Organiser les ECF et la session de validation, sous réserve de l’agrément de la DEETS.', 'Accompagner la recherche d’employeur, la gestion des ruptures et l’insertion après le titre.', 'Piloter la qualité : satisfaction, conseil de perfectionnement, indicateurs, Qualiopi.']],
    ], [3000, 11570]],

    ['h1', '6. Échéancier des obligations et des temps forts'],
    ['table', ['Obligation ou temps fort', 'Échéance', 'Responsable', 'Référence'], [
      ['Convention de formation avec le calendrier annexé (semaines au CFA et Rendez-vous du mois)', 'Avant le 1er mars 2027', 'CFA et employeur', '—'],
      ['**Transmission des contrats à l’OPCO**', 'Dans les jours ouvrables qui suivent le début du contrat, soit dès le 1er mars 2027 [[délai à vérifier]]', 'Employeur, avec l’appui du CFA', 'Art. L.6224-1 C. trav.'],
      ['**Carte d’étudiant des métiers**', 'Remise pendant la semaine d’intégration (1er – 5 mars 2027)', 'CFA', '[[Référence à vérifier]]'],
      ['**Visite médicale d’embauche** (visite d’information et de prévention)', 'Dans les délais réglementaires suivant l’embauche, au plus tard fin avril 2027 [[délai à vérifier]]', 'Employeur', 'Code du travail, santé au travail'],
      ['Information des apprentis sur leurs droits, la santé et la sécurité', 'Semaine d’intégration (1er – 5 mars 2027)', 'CFA', 'Art. L.6231-2 C. trav.'],
      ['**Congés des apprentis à poser hors des semaines au CFA** et des Rendez-vous du mois', 'Rappel à la signature, puis en juin et en novembre 2027', 'Employeur, sur rappel du CFA', '—'],
      ['**Audits Qualiopi** (surveillance et extension « apprentissage »)', 'Entre février et décembre 2027 [[dates à fixer avec le certificateur]]', 'CFA', 'Art. L.6316-1 C. trav.'],
      ['**Questionnaires de satisfaction**', 'À chaud : fin de chaque semaine au CFA et de chaque Rendez-vous ; mi-parcours : août 2027 ; fin de formation : février 2028 ; maîtres d’apprentissage : janvier 2028 ; employeurs : février 2028', 'CFA', 'Référentiel national qualité'],
      ['**Conseil de perfectionnement**', 'Mardi 29 juin et mardi 7 décembre 2027, 16 h 30 – 18 h', 'CFA, avec délégués, employeurs et maîtres d’apprentissage', '[[Article à vérifier]]'],
      ['**Date limite de la demande d’agrément pour l’examen**', 'Au plus tard 6 mois avant la session, soit avant le 21 août 2027 (dépôt visé dès le premier trimestre 2027)', 'CFA', 'Arrêtés du 22 décembre 2015 et du 21 juillet 2016'],
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

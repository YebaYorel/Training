const rdv = require('./rdv');
// Dates relatives à un Rendez-vous, reculées au vendredi si elles tombent un week-end.
const jour = (iso, delta) => {
  const d = new Date(iso + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() + delta);
  if (d.getUTCDay() === 6) d.setUTCDate(d.getUTCDate() - 1);
  if (d.getUTCDay() === 0) d.setUTCDate(d.getUTCDate() - 2);
  return d.toLocaleDateString('fr-FR', { timeZone: 'UTC', day: '2-digit', month: '2-digit', year: 'numeric' });
};
const M = ['Mois', 'Apprentis et candidats', 'Entreprises et maîtres d’apprentissage', 'Partenaires et intervenants', 'Administratif, qualité, DEETS, OPCO'];
const MW = [1500, 3300, 3300, 3100, 3370];
module.exports = {
  num: 'NI',
  slug: 'NOTE_INTERNE_mon_planning_de_pilotage_2026-2028',
  title: 'Mon planning de pilotage — Promotion MEM 2027-2028',
  objet: 'Planning personnel d’Aurélien LUMEKA pour réaliser, seul, tout ce qui est prévu pour les apprentis, les entreprises, les maîtres d’apprentissage et les partenaires, de novembre 2026 à août 2028.',
  landscape: true,
  blocks: [
    ['h1', '1. Ma semaine type'],
    ['table', ['Jour', 'Semaine au CFA (1 par mois)', 'Semaine en entreprise (3 par mois)'], [
      ['Lundi', 'Enseignement 8 h – 16 h ; 16 h – 17 h 30 : émargements dans Baserow, préparation du lendemain', 'Prospection et relation entreprises : recrutement de la promotion suivante, suivi des employeurs, recherche d’employeur pour les jeunes sans contrat'],
      ['Mardi', 'Enseignement ; conseil de perfectionnement les 29 juin et 7 décembre (16 h 30 – 18 h)', 'Un mardi par mois : **Rendez-vous du mois** (8 h – 16 h). Les autres mardis : réunions des maîtres d’apprentissage en fin de journée, ou préparation pédagogique'],
      ['Mercredi', 'Enseignement ; point avec les délégués à 16 h (10 minutes)', 'Préparation pédagogique : supports, sujets d’ECF, corrections, relecture des dossiers professionnels'],
      ['Jeudi', 'Enseignement', 'Visites en entreprise et entretiens trimestriels (sur site ou en visio)'],
      ['Vendredi', 'Enseignement ; 16 h : questionnaire à chaud, relevé d’assiduité envoyé à chaque employeur, bilan de la semaine', 'Administratif et qualité : Qualiopi, facturation OPCO, indicateurs, veille réglementaire ; autres activités de YEBA FORMATIONS'],
    ], [1500, 5800, 7270]],
    ['box', 'Charge estimée par mois (à ajuster après les premiers mois)', [
      'Enseignement : 5 jours ; Rendez-vous du mois : 1 jour ; préparation pédagogique et corrections : 2 jours ; visites, entretiens et suivi : 2 jours ; prospection, partenaires et administratif : 2 jours. Soit **environ 12 jours par mois** pour l’apprentissage, et **8 à 10 jours** disponibles pour les autres activités de YEBA FORMATIONS (formation continue, conseil IA, RGPD et IA Act).',
      'Les pics de charge sont en février-mars 2027 (ouverture), en janvier-février 2028 (examen blanc, session, cérémonie) et à partir de septembre 2027 (recrutement de la promotion 2028). Le sous-traitant prévu pour le placement soulage ces périodes.',
    ]],

    ['h1', '2. Ma routine pour chaque Rendez-vous du mois'],
    ['table', ['Rendez-vous', 'Solliciter l’intervenant (J – 60)', 'Confirmation écrite (J – 30)', 'Rappel employeurs et logistique (J – 15)', 'Rappel apprentis, questions à préparer (J – 7)', 'Remerciements et bilan (J + 2)'],
      rdv.map((r) => [`**${r.date}** — ${r.titre}`, jour(r.iso, -60), jour(r.iso, -30), jour(r.iso, -15), jour(r.iso, -7), jour(r.iso, 2)]), [4070, 2100, 2100, 2100, 2100, 2100]],
    ['ul', [
      'J – 1 : vérifier la salle ou le lieu, le matériel, la liste d’émargement, l’activité de repli (pluie, alerte cyclonique, désistement).',
      'Jour J : émargement matin et après-midi ; questionnaire de satisfaction de 2 minutes à 15 h 45.',
      'J + 8 : vérifier que chaque apprenti a écrit sa demi-page dans le livret ; relancer sinon.',
    ]],

    ['h1', '3. Ma routine pour chaque semaine au CFA'],
    ['table', ['Quand', 'Ce que je fais'], [
      ['J – 14', 'Préparer les supports et les études de cas ; vérifier la salle et le matériel'],
      ['J – 7', 'Rappel aux apprentis et aux employeurs (dates, horaires, documents à apporter) ; préparer le sujet d’ECF si la semaine en comporte une'],
      ['Chaque jour', 'Émargement à 8 h et à 13 h ; appel le jour même pour toute absence ; saisie dans Baserow'],
      ['Vendredi 16 h', 'Questionnaire à chaud ; relevé d’assiduité envoyé à chaque employeur ; bilan de la semaine'],
      ['J + 3', 'Retours individuels écrits ; mise à jour des plans de remédiation ; missions de la période en entreprise envoyées aux maîtres d’apprentissage'],
    ], [2500, 12070]],

    ['h1', '4. Mon planning mois par mois'],
    ['h2', 'Préparation'],
    ['table', M, [
      ['Nov. 2026', 'Réunions d’information tous les 15 jours ; entretiens et tests de positionnement ; ouverture du fichier des candidats dans Baserow', '15 contacts qualifiés par semaine ; petit-déjeuner « Recruter un apprenti » ; recueil des lettres d’intention', 'Rechercher l’intervenant expert CCP 3 et le sous-traitant placement', 'Suivre la réponse de la DEETS ; écrire aux OPCO (financement avant extension Qualiopi) ; contacter le service des titres professionnels de la DEETS'],
      ['Déc. 2026', 'Entretiens ; job dating ; préparation des candidats aux entretiens d’embauche', 'Prospection ; présentation du calendrier (semaines au CFA et Rendez-vous) aux employeurs intéressés', 'Choisir les prestataires du team building et de la cérémonie', 'Règlement intérieur ; DUERP ; assurance ; registre des traitements RGPD ; livret d’apprentissage'],
      ['Janv. 2027', 'Entretiens ; job dating ; suivi des candidats en attente d’employeur', 'Fiches « Adéquation poste / référentiel » ; désignation des maîtres d’apprentissage ; premières signatures', '**Solliciter les intervenants de mars à juin** (voir § 2)', '**Déposer la demande d’agrément MEM** (janvier – mars) ; préparer les audits Qualiopi'],
      ['Févr. 2027', 'Liste définitive ; information des jeunes encore sans employeur ; convocations à la semaine d’intégration', '**Réunion de lancement des maîtres d’apprentissage** (mardi 16 février) ; conventions de formation avec calendrier ; rappel congés hors semaines au CFA', 'Confirmation écrite des intervenants de mars et avril ; signature des contrats de sous-traitance', 'Commander les cartes d’étudiant des métiers ; préparer émargements, autorisations de droit à l’image, information RGPD des apprentis'],
    ], MW],
    ['h2', 'Année de formation'],
    ['table', M, [
      ['Mars 2027', 'Semaine d’intégration (1er – 5) : carte d’étudiant des métiers, droits, sécurité, égalité ; binômes d’entraide ; jeunes sans employeur : 2 demi-journées de recherche d’emploi par semaine', 'Appel à chaque maître d’apprentissage (semaine du 8) ; vérifier la transmission des contrats à l’OPCO et la programmation des visites médicales', 'Rendez-vous du 16 mars ; solliciter l’intervenant de mai', 'Relevé d’assiduité ; facturation OPCO ; audits Qualiopi : fixer les dates'],
      ['Avril 2027', 'Semaine au CFA (5 – 9) ; élection des délégués (vendredi 9) ; point hebdomadaire avec les jeunes sans contrat', '**1res visites en entreprise** (12 – 30 avril) ; **formation des maîtres d’apprentissage** (mardi 27 avril)', 'Rendez-vous du 20 avril', 'Vérifier les visites médicales réalisées ; demande d’agrément déposée'],
      ['Mai 2027', 'Semaine au CFA (10 – 14) ; **entretiens trimestriels n° 1** ; 31 mai : fin des 3 mois sans contrat, bilan et réorientation', 'Point téléphonique avec chaque maître d’apprentissage', 'Rendez-vous du 25 mai ; solliciter les intervenants de juillet à octobre', 'Bilan pédagogique et financier [[échéance à vérifier]]'],
      ['Juin 2027', 'Semaine au CFA (7 – 11) ; **ECF du CCP 1** (vendredi 11) ; retours individuels', 'Résultats de l’ECF aux maîtres d’apprentissage ; rappel des congés hors semaines au CFA', 'Rendez-vous du 22 juin', '**Conseil de perfectionnement** (mardi 29 juin) : compte rendu'],
      ['Juillet 2027', 'Semaine au CFA (5 – 9)', 'Rappel du calendrier du second semestre', 'Rendez-vous du 20 juillet', 'Préparer le questionnaire de mi-parcours'],
      ['Août 2027', 'Semaine au CFA (2 – 6) ; bilan de mi-parcours ; **entretiens trimestriels n° 2** ; questionnaire de mi-parcours', 'Point téléphonique avec chaque maître d’apprentissage ; lots pour le tournoi', 'Rendez-vous du 24 août ; solliciter les intervenants de novembre à février', '**Date limite de dépôt de la demande d’agrément (21 août)** : vérifier'],
      ['Sept. 2027', 'Semaine au CFA (6 – 10) ; entretiens « Et après ? »', '**2es visites en entreprise** ; réunion des maîtres d’apprentissage (mardi 14)', 'Rendez-vous du 21 septembre', '**Lancement du recrutement de la promotion 2028**'],
      ['Oct. 2027', 'Semaine au CFA (4 – 8) ; **ECF du CCP 2** (vendredi 8)', 'Point avec chaque employeur sur une embauche après le contrat', 'Rendez-vous du 19 octobre', 'Confirmer la date de session avec la DEETS ; recrutement 2028'],
      ['Nov. 2027', 'Semaine au CFA (15 – 19) ; **entretiens trimestriels n° 3** ; ateliers CV et pitch', 'Invitation au job dating ; rappel des congés de fin d’année hors semaines au CFA', 'Rendez-vous du 23 novembre', 'Constituer le jury de la session [[selon le règlement des sessions]]'],
      ['Déc. 2027', 'Semaine au CFA (6 – 10) ; collecte solidaire (1er – 14)', 'Accord des employeurs pour la collecte', 'Rendez-vous du 14 décembre', '**Conseil de perfectionnement** (mardi 7 décembre) ; inscription des candidats à la session ; fin de la fenêtre des audits Qualiopi'],
      ['Janv. 2028', 'Semaine au CFA (10 – 14) ; **ECF du CCP 3** (jeudi 13) ; **examen blanc** (vendredi 14)', 'Réunion des maîtres d’apprentissage (mardi 11) ; questionnaire de satisfaction des maîtres d’apprentissage', 'Rendez-vous du 18 janvier ; invitations à la cérémonie', 'Livret d’ECF ; convocations à la session'],
      ['Févr. 2028', 'Semaine au CFA (7 – 11) ; remise des dossiers professionnels (vendredi 11) ; **entretiens trimestriels n° 4** ; session (semaine du 21)', 'Questionnaire de satisfaction des employeurs ; fin des contrats le 29 février', 'Cérémonie du 29 février', 'Organisation de la session ; attestations de fin de formation ; ouverture de la promotion 2028 (1er mars)'],
    ], MW],
    ['h2', 'Après la formation'],
    ['table', ['Période', 'Ce que je fais'], [
      ['Mars – avril 2028', 'Communiquer les résultats ; féliciter les lauréats ; accompagner les candidats ajournés vers une nouvelle session'],
      ['Mai 2028', 'Bilan pédagogique et financier 2027 [[échéance à vérifier]]'],
      ['Août 2028', '**Enquête d’insertion à 6 mois** ; calcul et **publication des indicateurs de résultats**'],
      ['Février 2029 et février 2030', 'Enquêtes de suivi des anciens à 12 et 24 mois'],
    ], [3000, 11570]],

    ['h1', '5. Mon tableau de bord mensuel'],
    ['p', 'Chaque dernier vendredi du mois, je mets à jour dans Baserow : taux d’assiduité, absences non justifiées, alertes de décrochage et plans d’action en cours, contrats rompus, entretiens et visites réalisés, satisfaction des apprentis et des intervenants, nombre d’entreprises contactées pour la promotion suivante. Tout indicateur en dégradation deux mois de suite déclenche une action écrite.'],
    ['rgpd', [
      '**RGPD** — Baserow est hébergé dans l’Union européenne ; les données des apprentis (dont mineurs) ne sont accessibles qu’à moi et au sous-traitant pour ce qui le concerne. Les noms de mes contacts partenaires ne figurent dans aucun document transmis à des tiers.',
      '**IA Act** — Si j’utilise une IA pour préparer des supports ou des courriels, aucune donnée personnelle d’apprenti n’y est saisie, et aucune décision concernant un apprenti n’est prise par l’IA.',
    ]],
  ],
};

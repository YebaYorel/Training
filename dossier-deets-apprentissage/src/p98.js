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
    ['table', ['Jour', 'Semaine ordinaire', 'Semaine intensive (24 – 28 janvier et 7 – 11 février 2028)'], [
      ['Lundi', 'Prospection et relation entreprises : recrutement de la promotion suivante, suivi des employeurs, recherche d’employeur pour les jeunes sans contrat ; préparation du mardi', 'Enseignement 8 h – 16 h'],
      ['Mardi', '**Au CFA, 8 h – 16 h** : cours, ou Rendez-vous du mois une fois par mois. 16 h – 16 h 30 : émargements dans Baserow, questionnaire à chaud. En fin de journée, selon le calendrier : conseil de perfectionnement ou réunion des maîtres d’apprentissage (16 h 30 – 18 h)', 'Enseignement 8 h – 16 h'],
      ['Mercredi', 'Corrections, retours individuels écrits, missions de la semaine envoyées aux maîtres d’apprentissage ; relevé d’assiduité aux employeurs', 'Enseignement 8 h – 16 h'],
      ['Jeudi', 'Visites en entreprise et entretiens trimestriels (sur site ou en visio) ; formation des maîtres d’apprentissage le 29 avril 2027', 'Enseignement 8 h – 16 h ; ECF du CCP 3 le 27 janvier'],
      ['Vendredi', 'Administratif et qualité : Qualiopi, facturation OPCO, indicateurs, veille réglementaire ; autres activités de YEBA FORMATIONS', 'Enseignement 8 h – 16 h ; examen blanc le 28 janvier ; remise des dossiers professionnels le 11 février'],
    ], [1500, 7270, 5800]],
    ['box', 'Charge estimée par mois (à ajuster après les premiers mois)', [
      'Mardis au CFA : 4 à 5 jours ; préparation pédagogique et corrections : 2 jours ; visites, entretiens et suivi : 2 jours ; prospection, partenaires et administratif : 2 jours. Soit **environ 10 à 11 jours par mois** pour l’apprentissage, et **environ 10 jours** disponibles pour les autres activités de YEBA FORMATIONS (formation continue, conseil IA, RGPD et IA Act).',
      'Pics de charge : février – mars 2027 (ouverture), septembre 2027 (recrutement de la promotion 2028) et janvier – février 2028 (deux semaines intensives, session, cérémonie). Le sous-traitant prévu pour le placement soulage ces périodes.',
    ]],

    ['h1', '2. Ma routine pour chaque Rendez-vous du mois'],
    ['table', ['Rendez-vous', 'Solliciter l’intervenant (J – 60)', 'Confirmation écrite (J – 30)', 'Rappel employeurs et logistique (J – 15)', 'Rappel apprentis, questions à préparer (J – 7)', 'Remerciements et bilan (J + 2)'],
      rdv.map((r) => [`**${r.date}** — ${r.titre}`, jour(r.iso, -60), jour(r.iso, -30), jour(r.iso, -15), jour(r.iso, -7), jour(r.iso, 2)]), [4070, 2100, 2100, 2100, 2100, 2100]],
    ['ul', [
      'J – 1 : vérifier la salle ou le lieu, le matériel, la liste d’émargement, l’activité de repli (pluie, alerte cyclonique, désistement).',
      'Jour J : émargement matin et après-midi ; questionnaire de satisfaction de 2 minutes à 15 h 45.',
      'J + 8 : vérifier que chaque apprenti a écrit sa demi-page dans le livret ; relancer sinon.',
    ]],

    ['h1', '3. Ma routine pour chaque mardi de cours'],
    ['table', ['Quand', 'Ce que je fais'], [
      ['Vendredi ou lundi précédent', 'Préparer les supports et les études de cas ; vérifier la salle et le matériel ; préparer le sujet d’ECF si le mardi en comporte une'],
      ['Mardi 8 h et 13 h', 'Émargement ; appel le jour même pour toute absence ; saisie dans Baserow'],
      ['Mardi 15 h 45', 'Questionnaire à chaud de 2 minutes ; mission de la semaine pour l’entreprise'],
      ['Mercredi', 'Retours individuels écrits ; mise à jour des plans de remédiation ; relevé d’assiduité envoyé à chaque employeur'],
    ], [3000, 11570]],
    ['h1', '4. Mon planning mois par mois'],
    ['h2', 'Préparation'],
    ['table', M, [
      ['Nov. 2026', 'Réunions d’information tous les 15 jours ; entretiens et tests de positionnement ; ouverture du fichier des candidats dans Baserow', '15 contacts qualifiés par semaine ; petit-déjeuner « Recruter un apprenti » ; recueil des lettres d’intention', 'Rechercher l’intervenant expert CCP 3 et le sous-traitant placement', 'Suivre la réponse de la DEETS ; contacter le service des titres professionnels de la DEETS ; informer QUALITIA du lieu de formation de Technor'],
      ['Déc. 2026', 'Entretiens ; job dating ; préparation des candidats aux entretiens d’embauche', 'Prospection ; présentation du rythme du mardi et des Rendez-vous aux employeurs intéressés', 'Choisir les prestataires du team building et de la cérémonie', 'Règlement intérieur ; DUERP ; assurance ; registre des traitements RGPD ; livret d’apprentissage'],
      ['Janv. 2027', 'Entretiens ; job dating ; suivi des candidats en attente d’employeur', 'Fiches « Adéquation poste / référentiel » ; désignation des maîtres d’apprentissage ; premières signatures', '**Solliciter les intervenants de mars à juin** (voir § 2)', '**Déposer la demande d’agrément MEM** (janvier – mars)'],
      ['Févr. 2027', 'Liste définitive ; information des jeunes encore sans employeur ; convocations au mardi 2 mars', '**Réunion de lancement des maîtres d’apprentissage** (mardi 16 février) ; conventions de formation avec calendrier ; rappel congés hors mardis et semaines intensives', 'Confirmation écrite des intervenants de mars et avril ; signature des contrats de sous-traitance', 'Commander les cartes d’étudiant des métiers ; préparer émargements, autorisations de droit à l’image, information RGPD des apprentis'],
    ], MW],
    ['h2', 'Année de formation'],
    ['table', M, [
      ['Mars 2027', 'Mardis 2, 9, 23, 30 ; intégration (2 et 9) : carte d’étudiant des métiers, droits, sécurité, égalité ; binômes d’entraide ; recherche d’emploi chaque semaine pour les jeunes sans employeur', 'Appel à chaque maître d’apprentissage (semaine du 8) ; vérifier la transmission des contrats à l’OPCO **avant le samedi 6 mars** et la programmation des visites médicales', 'Rendez-vous du 16 mars ; solliciter l’intervenant de mai', 'Relevé d’assiduité ; facturation OPCO ; fixer la date de l’audit de surveillance Qualiopi avec QUALITIA'],
      ['Avril 2027', 'Mardis 6, 13, 27 ; présentation du dossier professionnel (6) ; élection des délégués (13) ; point hebdomadaire avec les jeunes sans contrat', '**1res visites en entreprise** (12 avril – 7 mai) ; **formation des maîtres d’apprentissage** (jeudi 29 avril)', 'Rendez-vous du 20 avril', 'Vérifier les visites médicales réalisées ; demande d’agrément déposée'],
      ['Mai 2027', 'Mardis 4, 11, 18 ; **entretiens trimestriels n° 1** ; 31 mai : fin des 3 mois sans contrat, bilan et réorientation', 'Point téléphonique avec chaque maître d’apprentissage', 'Rendez-vous du 25 mai ; solliciter les intervenants de juillet à octobre', 'Bilan pédagogique et financier [[échéance à vérifier]]'],
      ['Juin 2027', 'Mardis 1er, 8, 15, 29 ; **ECF du CCP 1** (29) ; retours individuels', 'Résultats de l’ECF ; rappel des congés hors mardis et semaines intensives', 'Rendez-vous du 22 juin', '**Conseil de perfectionnement** (mardi 29 juin, 16 h 30) : compte rendu'],
      ['Juillet 2027', 'Mardis 6, 13, 27 ; préparation du tournoi', 'Rappel du calendrier du second semestre', 'Rendez-vous du 20 juillet', 'Préparer le questionnaire de mi-parcours'],
      ['Août 2027', 'Mardis 3, 10, 17, 31 ; bilan de mi-parcours (31) ; **entretiens trimestriels n° 2** ; questionnaire de mi-parcours', 'Point téléphonique avec chaque maître d’apprentissage ; lots pour le tournoi', 'Rendez-vous du 24 août ; solliciter les intervenants de novembre à février', '**Date limite de la demande d’agrément : 21 août** — vérifier'],
      ['Sept. 2027', 'Mardis 7, 14, 28 ; entretiens « Et après ? »', '**2es visites en entreprise** ; réunion des maîtres d’apprentissage (mardi 14, 16 h 30)', 'Rendez-vous du 21 septembre', '**Lancement du recrutement de la promotion 2028**'],
      ['Oct. 2027', 'Mardis 5, 12, 26 ; **ECF du CCP 2** (26)', 'Point avec chaque employeur sur une embauche après le contrat', 'Rendez-vous du 19 octobre', 'Confirmer la date de session avec la DEETS ; recrutement 2028'],
      ['Nov. 2027', 'Mardis 2, 9, 16, 30 ; « Esprit d’entreprendre » (16) ; **entretiens trimestriels n° 3** ; CV et pitch', 'Invitation au job dating ; rappel des congés de fin d’année hors mardis', 'Rendez-vous du 23 novembre', 'Constituer le jury de la session [[selon le règlement des sessions]]'],
      ['Déc. 2027', 'Mardis 7, 21, 28 ; collecte solidaire (1er – 13)', 'Accord des employeurs pour la collecte', 'Rendez-vous du 14 décembre', '**Conseil de perfectionnement** (mardi 7, 16 h 30) ; inscription des candidats à la session ; audit de surveillance Qualiopi réalisé'],
      ['Janv. 2028', 'Mardis 4, 11 ; **semaine intensive n° 1** (24 – 28) : ECF du CCP 3 (jeudi 27), examen blanc (vendredi 28)', 'Réunion des maîtres d’apprentissage (mardi 11, 16 h 30) ; questionnaire de satisfaction des maîtres d’apprentissage', 'Rendez-vous du 18 janvier ; invitations à la cérémonie', 'Livret d’ECF ; convocations à la session'],
      ['Févr. 2028', 'Mardis 1er, 15, 22 ; **semaine intensive n° 2** (7 – 11) : remise des dossiers professionnels (vendredi 11) ; **entretiens trimestriels n° 4** ; session (semaine du 21)', 'Questionnaire de satisfaction des employeurs ; fin des contrats le 29 février', 'Cérémonie du mardi 29 février', 'Organisation de la session ; attestations de fin de formation ; ouverture de la promotion 2028 (1er mars)'],
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

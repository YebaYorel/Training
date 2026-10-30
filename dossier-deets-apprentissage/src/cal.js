// Calendrier unique de la promotion MEM 2027-2028 (contrats du 1er mars 2027 au 29 février 2028).
// Rythme : chaque mardi au CFA (cours), dont un mardi par mois consacré au Rendez-vous du mois,
// et deux semaines intensives en fin de formation. Horaires : 8 h – 12 h et 13 h – 16 h,
// pauses de 15 minutes à 10 h et à 15 h (7 heures par jour). Aucun mardi n'est férié sur la période.
// Repris par les pièces 06, 07, 15, 16, 18, 19, 20 et les notes internes : ne modifier les dates qu'ici.
const mois = [
  { mois: 'Mars 2027', cours: ['2', '9', '23', '30'], rdv: '16', dominante: 'Intégration (2 et 9 mars) ; CCP 1' },
  { mois: 'Avril 2027', cours: ['6', '13', '27'], rdv: '20', dominante: 'CCP 1 ; présentation du dossier professionnel (6 avril) ; élection des délégués (13 avril)' },
  { mois: 'Mai 2027', cours: ['4', '11', '18'], rdv: '25', dominante: 'CCP 1' },
  { mois: 'Juin 2027', cours: ['1', '8', '15', '29'], rdv: '22', dominante: 'CCP 1 ; **ECF du CCP 1** (mardi 29 juin)' },
  { mois: 'Juillet 2027', cours: ['6', '13', '27'], rdv: '20', dominante: 'CCP 2' },
  { mois: 'Août 2027', cours: ['3', '10', '17', '31'], rdv: '24', dominante: 'CCP 2 ; bilan collectif de mi-parcours (31 août)' },
  { mois: 'Septembre 2027', cours: ['7', '14', '28'], rdv: '21', dominante: 'CCP 2' },
  { mois: 'Octobre 2027', cours: ['5', '12', '26'], rdv: '19', dominante: 'CCP 2 ; **ECF du CCP 2** (mardi 26 octobre)' },
  { mois: 'Novembre 2027', cours: ['2', '9', '16', '30'], rdv: '23', dominante: 'CCP 3 ; module « Esprit d’entreprendre » (mardi 16 novembre)' },
  { mois: 'Décembre 2027', cours: ['7', '21', '28'], rdv: '14', dominante: 'CCP 3' },
  { mois: 'Janvier 2028', cours: ['4', '11'], rdv: '18', intensive: 'du lundi 24 au vendredi 28 janvier', dominante: 'CCP 3 ; **semaine intensive n° 1** : fin du CCP 3, **ECF du CCP 3** (jeudi 27 janvier), **examen blanc** (vendredi 28 janvier)' },
  { mois: 'Février 2028', cours: ['1', '15', '22'], rdv: '29', intensive: 'du lundi 7 au vendredi 11 février', dominante: 'Révisions ; **semaine intensive n° 2** : finalisation et remise du dossier professionnel (vendredi 11 février), oraux blancs, préparation à l’entretien avec le jury ; session de validation la semaine du 21 février' },
];
const nbCours = mois.reduce((n, m) => n + m.cours.length, 0); // 39 mardis de cours
const heures = { mardis: nbCours * 7, intensives: 2 * 35, rdv: 12 * 7 };
heures.enseignement = heures.mardis + heures.intensives; // 343
heures.total = heures.enseignement + heures.rdv; // 427
module.exports = { mois, nbCours, heures };

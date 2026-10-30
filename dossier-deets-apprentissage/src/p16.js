const rdv = require('./rdv');
const choix = rdv.filter((r) => /artistique|culturelle|Sport|Team|Solidarité/.test(r.type));
module.exports = {
  num: '16',
  slug: '16_Modalites_activites_culturelles_et_sportives',
  title: 'Modalités de promotion et de réalisation d’activités culturelles et sportives au bénéfice des apprentis',
  objet: 'Activités culturelles, artistiques et sportives proposées à la promotion MEM 2027-2028 : programme, organisation, accessibilité et financement.',
  blocks: [
    ['h1', '1. Intention'],
    ['p', 'Les activités culturelles et sportives renforcent la cohésion de la promotion, la confiance en soi et le sentiment d’appartenance, trois leviers reconnus de la persévérance (pièce n° 11). Elles valorisent aussi la culture réunionnaise et développent des compétences directement utiles à un manager d’établissement marchand : prendre la parole, fédérer une équipe, conduire un projet.'],
    ['p', 'Ces activités s’inscrivent dans les **Rendez-vous du mois** : une demi-journée par mois, le jeudi de 13 h à 17 h, en dehors des semaines au CFA (programme complet en pièce n° 19). Elles ne réduisent donc pas les 420 heures de formation.'],
    ['h1', '2. Programme 2027-2028'],
    ['table', ['Date', 'Activité', 'Contenu', 'Lien avec la formation'], choix.map((r) => [r.date, `**${r.titre}** (${r.type.toLowerCase()})`, r.contenu, r.lien]), [1700, 1900, 4000, 2038]],
    ['h1', '3. Organisation'],
    ['ul', [
      '**Référent vie de l’apprenti** : Aurélien LUMEKA. Le programme est présenté à la promotion dès la semaine d’intégration ; les **délégués**, élus en avril 2027, peuvent proposer des ajustements ou une activité de remplacement.',
      '**Statut des Rendez-vous** : ils sont inscrits au calendrier de formation annexé à la convention de formation signée avec l’employeur. Ce temps est du temps de formation, rémunéré comme tel ; la présence est obligatoire et fait l’objet d’un émargement.',
      '**Accessibilité** : chaque activité est vérifiée au regard des besoins des apprentis ; une alternative est proposée si nécessaire (pièce n° 10).',
      '**Sécurité** : assurance responsabilité civile de l’organisme vérifiée pour chaque activité extérieure ; autorisation des représentants légaux pour les mineurs ; plan de repli en cas d’intempéries ou d’alerte cyclonique.',
      '**Budget** prévisionnel annuel : [[montant]] € ; recherche de partenaires (collectivités, associations, entreprises d’accueil) pour réduire le coût des activités.',
    ]],
    ['rgpd', ['**RGPD** — Droit à l’image : aucune photo ni vidéo d’apprenti n’est publiée sans autorisation écrite (et celle des représentants légaux pour un mineur). La liste des participants transmise à un partenaire se limite au nom et au prénom.']],
  ],
};

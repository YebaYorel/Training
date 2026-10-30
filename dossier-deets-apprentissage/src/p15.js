const rdv = require('./rdv');
module.exports = {
  num: '15',
  slug: '15_Etat_descriptif_sensibilisation_creation_reprise_entreprise',
  title: 'État descriptif — Sensibilisation des apprentis à la création ou à la reprise d’entreprise',
  objet: 'Actions de sensibilisation et d’orientation des apprentis vers l’entrepreneuriat.',
  blocks: [
    ['h1', '1. Pourquoi c’est pertinent pour nos apprentis'],
    ['p', 'Le métier de manager d’établissement marchand est un tremplin naturel vers l’entrepreneuriat : piloter un point de vente, c’est déjà gérer une équipe, un chiffre d’affaires, des stocks et une marge. À La Réunion, de nombreuses TPE devront par ailleurs trouver un repreneur dans les années à venir ([[donnée chiffrée CCI Réunion / INSEE à insérer si disponible]]). Le dirigeant de YEBA FORMATIONS, à la tête de l’entreprise depuis 2021, témoigne de ce parcours. Ouvrir son propre commerce, reprendre une boutique ou devenir franchisé sont des projets fréquents chez les managers de magasin expérimentés.'],
    ['h1', '2. Programme de sensibilisation'],
    ['p', 'La sensibilisation combine un module de formation et trois Rendez-vous du mois (un mardi par mois) consacrés à l’entrepreneuriat (pièce n° 19). Elle forme un parcours progressif : comprendre l’écosystème, savoir financer un projet, puis poser des fondations solides.'],
    ['table', ['Date', 'Action', 'Contenu'], [
      ...rdv.filter((r) => /entrepreneuriat/.test(r.type)).map((r) => [r.date, `Rendez-vous « ${r.titre} » (journée)`, `Matin : ${r.matin} Après-midi : ${r.apresmidi}`]),
      ['Semaine du 15 novembre 2027', 'Module « Esprit d’entreprendre » (7 heures)', 'Du projet à l’entreprise : idée, client, offre, prix, compte de résultat prévisionnel d’un magasin, en lien avec le CCP 3 (rentabilité).'],
      ['Toute l’année', 'Orientation individuelle', 'Mise en relation avec les réseaux d’accompagnement pour tout apprenti porteur d’un projet, à sa demande.'],
    ], [2300, 2700, 4638]],
    ['h1', '3. Partenaires sollicités'],
    ['p', 'CCI Réunion, tribunal mixte de commerce de Saint-Denis, Bpifrance Réunion, Initiative Réunion, réseaux d’accompagnement à la création, un cabinet d’expertise comptable et un assureur. **Aucun partenariat n’est formalisé à ce jour** : les sollicitations seront adressées entre janvier et mars 2027, avec un courrier de présentation de la promotion et des dates proposées.'],
    ['rgpd', ['**RGPD** — La mise en relation avec un réseau d’accompagnement se fait à l’initiative de l’apprenti ou avec son accord explicite.']],
  ],
};

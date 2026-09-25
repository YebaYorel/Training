// Réglages d'IFA — assistante virtuelle de YEBA FORMATIONS.
// Tout se modifie ici, sans toucher au reste du code.

export const IFA = {
  nom: 'IFA',
  role: 'Assistante virtuelle de YEBA FORMATIONS',
  // Adresse qui reçoit les demandes de rappel (formulaire Baserow, webhook n8n…).
  // Laissez vide tant qu'aucune base n'est branchée : IFA prépare alors un e-mail pré-rempli.
  // Se règle au moment de la compilation : VITE_RAPPEL_ENDPOINT=https://... npm run build
  endpointRappel: import.meta.env.VITE_RAPPEL_ENDPOINT ?? '',
  // Format du corps envoyé : 'json' (webhook n8n) ou 'baserow' (formulaire public Baserow)
  formatEnvoi: import.meta.env.VITE_RAPPEL_FORMAT ?? 'json',
}

// Agenda de rappel : heure de La Réunion (UTC+4, pas d'heure d'été)
export const AGENDA_RAPPEL = {
  fuseau: 'Indian/Reunion',
  joursAffiches: 10, // jours ouvrés proposés
  delaiMinHeures: 4, // pas de créneau à moins de 4 h
  plages: [
    ['08:30', '11:30'],
    ['13:30', '16:30'],
  ],
  pasMinutes: 30,
}

// Durée de conservation des demandes de rappel : référentiel CNIL « gestion commerciale »,
// 3 ans à compter du dernier contact avec le prospect. À confirmer par le dirigeant.
export const CONSERVATION = '3 ans après notre dernier échange'

// Suggestion du code NSF (nomenclature des spécialités de formation) à partir de l'intitulé.
// Aide à la saisie du cadre F-4 du BPF : la liste officielle fait foi, vérifiez le code proposé.
export const NSF = [
  ['326', 'Informatique, traitement de l’information, réseaux de transmission', ['ia', 'intelligence artificielle', 'informatique', 'numerique', 'digital', 'automatis', 'n8n', 'donnees', 'site internet', 'web', 'excel', 'microsoft', 'bureautique avancee', 'cyber', 'agent', 'no code']],
  ['324', 'Secrétariat, bureautique', ['secretariat', 'bureautique', 'word', 'traitement de texte', 'accueil telephonique']],
  ['312', 'Commerce, vente', ['vente', 'vendre', 'negoci', 'commercial', 'prospection', 'relation client']],
  ['310', 'Spécialités plurivalentes des échanges et de la gestion', ['management', 'manager', 'gestion d equipe', 'pilotage', 'dirigeant', 'strategie']],
  ['315', 'Ressources humaines, gestion du personnel, gestion de l’emploi', ['ressources humaines', 'rh', 'recrutement', 'paie', 'entretien annuel']],
  ['314', 'Comptabilité, gestion', ['comptab', 'gestion financiere', 'tresorerie', 'facturation']],
  ['128', 'Droit, sciences politiques', ['droit', 'juridique', 'rgpd', 'ia act', 'conformite', 'reglementation', 'gouvernance']],
  ['320', 'Spécialités plurivalentes de la communication', ['communication', 'emailing', 'marketing', 'reseaux sociaux', 'redaction']],
  ['333', 'Enseignement, formation', ['formateur', 'formation de formateurs', 'pedagogi', 'animer une formation']],
  ['334', 'Accueil, hôtellerie, tourisme', ['hotel', 'tourisme', 'accueil', 'restauration']],
  ['344', 'Sécurité des biens et des personnes, police, surveillance', ['securite', 'sst', 'incendie', 'secourisme', 'prevention des risques']],
  ['413', 'Développement des capacités comportementales et relationnelles', ['soft skills', 'communication interpersonnelle', 'gestion du stress', 'assertivite', 'confiance en soi', 'relationnel']],
  ['414', 'Développement des capacités individuelles d’organisation', ['organisation', 'gestion du temps', 'productivite', 'priorites']],
  ['136', 'Langues vivantes, civilisations étrangères et régionales', ['anglais', 'langue', 'creole', 'espagnol']],
]
const norm = (t) => String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]/g, ' ')

export function suggererNsf(intitule) {
  const t = ' ' + norm(intitule) + ' '
  const scores = NSF.map(([code, libelle, mots]) => ({ code, libelle, score: mots.filter((m) => t.includes(' ' + m) || t.includes(m + ' ')).length })).filter((x) => x.score > 0)
  return scores.sort((a, b) => b.score - a.score)[0] || null
}
export const libelleNsf = (code) => NSF.find(([c]) => c === String(code))?.[1] || ''

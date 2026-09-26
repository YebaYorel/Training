// Démo YEBA Studio : les données fictives de demo.js, au format « client » (celui de l'espace chiffré).
// Ainsi la démo passe par EXACTEMENT les mêmes écrans que les clients (saisie, documents, BPF, CARBURANT).
import { DEMO } from './demo.js'
import { donneesVides } from './modele.js'

const PRIX = { 'CONTRÔLE TECHNIQUE': 890, 'ALLUMAGE-TURBO': 1680, EMBRAYAGE: 690, TRACTION: 690, 'RÉGLAGE MOTEUR': 990, COPILOTE: 990 }
const OBJECTIFS = {
  'CONTRÔLE TECHNIQUE': 'Cartographier les usages de l’IA et les données personnelles de son entreprise\nRédiger une charte d’usage de l’IA\nIdentifier les obligations RGPD et IA Act applicables',
  'ALLUMAGE-TURBO': 'Utiliser un assistant d’IA générative sur des tâches réelles\nRédiger des consignes efficaces et vérifiables\nProtéger les données de l’entreprise',
  EMBRAYAGE: 'Conduire un entretien individuel\nDéléguer avec des objectifs clairs\nDésamorcer un conflit',
  TRACTION: 'Préparer un rendez-vous de vente\nTraiter les objections\nConclure et relancer',
  'RÉGLAGE MOTEUR': 'Cartographier un processus à automatiser\nConstruire un workflow sans coder\nTester et documenter l’automatisation',
  COPILOTE: 'Utiliser Copilot dans Word, Excel et Outlook\nAppliquer la méthode des 4 P\nMesurer le temps gagné',
}

export function demoDonnees() {
  const d = donneesVides()
  d.organisme = {
    ...d.organisme,
    nom: 'Lagon Formation (organisme fictif)', formeJuridique: 'SAS (fictive)', siret: '12345678900012', nda: '04 97 00000 97 (fictif)',
    qualiopi: 'DEMO-0000', certificateur: 'Certificateur fictif', adresse: '1 rue de la Démo', codePostal: '97400', ville: 'Saint-Denis',
    dirigeant: 'Camille Démo, directrice', referentHandicap: 'Camille Démo', email: 'contact@exemple.re', tel: '0262 00 00 00',
    horaires: '08h30–12h00 / 13h00–16h30', mediateur: 'Médiateur fictif — 1 place de l’Exemple, 97400 Saint-Denis', couleur: '#1B3A6B',
  }
  const formations = {}
  for (const s of DEMO.sessions) {
    const court = s.formation.split(' — ')[0]
    formations[s.formation] ||= { id: 'fo' + Object.keys(formations).length, intitule: s.formation, heures: s.heures, jours: s.jours, prix: PRIX[court] || 690, objectifs: OBJECTIFS[court] || '', prerequis: 'Aucun', evaluation: 'Positionnement, mises en situation, évaluation finale' }
  }
  d.formations = Object.values(formations)
  d.formateurs = Object.entries(DEMO.formateurs).map(([id, f]) => ({ id, nom: id === 'f1' ? 'Camille Démo' : f.nom, type: id === 'f1' ? 'Dirigeant (non salarié)' : f.type }))
  d.clients = Object.entries(DEMO.clients).map(([id, c]) => ({ id, nom: c.nom, type: c.type === 'Entreprise privéé' ? 'Entreprise privée' : c.type }))
  d.sessions = DEMO.sessions.map((s) => ({ id: s.id, formation: formations[s.formation].id, type: s.type, debut: s.debut, fin: s.fin, horaires: '08h30–12h00 / 13h00–16h30', lieu: s.lieu, formateur: s.formateurs[0], client: s.client === 'c2' ? 'c5' : s.client, places: s.places, statut: s.statut, coutFormateur: s.coutFormateur }))
  const sessionDe = Object.fromEntries(DEMO.sessions.map((s) => [s.id, s]))
  d.apprenants = []
  d.inscriptions = DEMO.inscriptions.map((i, k) => {
    const s = sessionDe[i.session]
    d.apprenants.push({ id: i.apprenant, nom: DEMO.apprenants[i.apprenant].nom, entreprise: s.client === 'c2' ? 'c5' : s.client })
    const opco = s.client === 'c2' || (i.session === 's5' && k % 2 === 0)
    return {
      id: i.id, session: i.session, apprenant: i.apprenant, statut: i.statut,
      financement: opco ? 'OPCO' : 'Plan PDC', financeur: opco ? 'c2' : '',
      numeroDossier: opco && i.session === 's2' ? `OPCO-26-${1000 + k}` : '', montantAccord: opco ? 1050 : '',
      dateDepot: opco && i.session === 's2' ? '2026-05-10' : '',
      pieces: { ...i.pieces, attestation: i.session === 's2' ? k % 3 !== 0 : i.pieces.attestation },
    }
  })
  d.presences = DEMO.presences.map((p) => ({ ...p, motifMatin: !p.matin && p.motif ? 'Justifiée' : '', motifApresMidi: '' }))
  const insDe = Object.fromEntries(d.inscriptions.map((i) => [i.apprenant + i.session, i.id]))
  d.evaluations = DEMO.evaluations.map((e) => ({ ...e, inscription: insDe[e.apprenant + e.session] }))
  d.factures = DEMO.factures.map((f) => ({
    id: f.id, numero: f.ref, type: f.type, client: f.client, session: f.session, montantHT: f.montantHT, date: f.date,
    statut: f.id === 'fa3' ? 'Envoyé' : f.statut, encaisse: f.id === 'fa3' ? 0 : f.encaisse, datePaiement: f.id === 'fa3' ? '' : f.datePaiement,
  }))
  const STAT = { '✅ Conforme': 'conforme', '⏳En cours': 'en-cours', '❌ Non conforme': 'non-conforme', '➖ Non applicable': 'na' }
  for (const i of DEMO.indicateurs) d.indicateurs[i.n] = { statut: STAT[i.statut], notes: i.observations, actions: i.actions, verif: i.verif }
  d.parametres.carburant.securise = [{ cle: 'demo', montant: 2100, date: '2026-07-20' }]
  return d
}

// Données FICTIVES de démonstration — aucune personne réelle (hors le dirigeant, déjà public).
// Servent à montrer l'Espace sans exposer la moindre donnée de stagiaire ou de client (RGPD).
import RNQ from '../../src/rnq.json'
import DOCS from '../../src/documents.json'
import { PIECES } from './pieces.js'

// Générateur pseudo-aléatoire déterministe : la démo est identique à chaque ouverture.
function graine(n) {
  return () => {
    n = (n * 1664525 + 1013904223) % 4294967296
    return n / 4294967296
  }
}
const alea = graine(974)

const PRENOMS = ['Léa', 'Kévin', 'Nadia', 'Jordan', 'Sarah', 'Mickaël', 'Inès', 'Loïc', 'Chloé', 'Yanis', 'Émilie', 'Teddy', 'Laura', 'Dylan', 'Manon', 'Ravi', 'Océane', 'Anthony', 'Julie', 'Steeve', 'Anaïs', 'Bryan', 'Marie', 'Nicolas', 'Priya', 'Fabrice', 'Lucie']
const INITIALES = 'ABCDEFGHJKLMNPRST'

const clients = {
  c1: { nom: 'Boulangerie Ti Kaz (fictif)', type: 'TPE' },
  c2: { nom: 'OPCO de démonstration', type: 'OPCO' },
  c3: { nom: 'Transports Lagon (fictif)', type: 'PME' },
  c4: { nom: 'Organisme partenaire (fictif)', type: 'Ecole' },
  c5: { nom: 'Hôtel Piton Bleu (fictif)', type: 'Entreprise privéé' },
}
const formateurs = {
  f1: { nom: 'Aurélien LUMEKA', type: 'Interne (Salarié)' },
  f2: { nom: 'Formatrice associée (fictive)', type: 'Externe (Indépendant)' },
}

const sessions = [
  { id: 's1', formation: 'CONTRÔLE TECHNIQUE — Gouvernance RGPD et IA Act', type: 'Intra-entreprise', debut: '2026-03-12', fin: '2026-03-12', heures: 8, jours: 1, lieu: 'Saint-Denis — dans les locaux du client', statut: 'Terminée', formateurs: ['f1'], client: 'c1', coutFormateur: 0, places: 8, n: 6 },
  { id: 's2', formation: 'ALLUMAGE-TURBO — L’IA générative au travail', type: 'Inter-entreprise', debut: '2026-06-08', fin: '2026-06-10', heures: 24, jours: 3, lieu: 'Saint-Gilles — salle de séminaire', statut: 'Terminée', formateurs: ['f1', 'f2'], client: 'c2', coutFormateur: 1200, places: 10, n: 8 },
  { id: 's3', formation: 'EMBRAYAGE — Manager au quotidien', type: 'Sur mesure', debut: '2026-05-05', fin: '2026-05-05', heures: 8, jours: 1, lieu: 'Saint-Pierre', statut: 'Terminée', formateurs: ['f1'], client: 'c4', coutFormateur: 0, places: 6, n: 4 },
  { id: 's4', formation: 'TRACTION — Vendre et négocier', type: 'Intra-entreprise', debut: '2026-09-24', fin: '2026-09-24', heures: 8, jours: 1, lieu: 'Le Port — dans les locaux du client', statut: 'Terminée', formateurs: ['f1'], client: 'c3', coutFormateur: 0, places: 10, n: 5 },
  { id: 's5', formation: 'RÉGLAGE MOTEUR — Automatiser sans coder (n8n)', type: 'Inter-entreprise', debut: '2026-10-19', fin: '2026-10-20', heures: 16, jours: 2, lieu: 'Sainte-Clotilde — salle de formation', statut: 'Confirmée', formateurs: ['f1'], client: 'c5', coutFormateur: 0, places: 10, n: 5 },
  { id: 's6', formation: 'COPILOTE — Microsoft 365 par la méthode des 4 P', type: 'Intra-entreprise', debut: '2026-11-16', fin: '2026-11-17', heures: 16, jours: 2, lieu: 'Saint-Paul — dans les locaux du client', statut: 'Planifiée', formateurs: ['f1'], client: 'c5', coutFormateur: 0, places: 8, n: 3 },
].map((s) => ({ ...s, nom: `${s.formation.split(' — ')[0]} · ${new Date(s.debut).toLocaleDateString('fr-FR')}`, sousTraiteeA: null }))

function jours(debut, fin) {
  const r = []
  for (let d = new Date(debut); d <= new Date(fin); d.setDate(d.getDate() + 1)) r.push(d.toISOString().slice(0, 10))
  return r
}

const apprenants = {}
const inscriptions = []
const presences = []
const evaluations = []
let k = 0
for (const s of sessions) {
  const passee = s.statut === 'Terminée'
  for (let i = 0; i < s.n; i++) {
    const a = 'a' + ++k
    apprenants[a] = { nom: `${PRENOMS[k % PRENOMS.length]} ${INITIALES[(k * 7) % INITIALES.length]}.` }
    const ins = 'i' + k
    const complet = passee ? alea() > 0.15 : alea() > 0.55
    inscriptions.push({
      id: ins,
      apprenant: a,
      session: s.id,
      statut: passee ? 'Présent' : 'Confirmé',
      financement: s.client === 'c2' ? 'OPCO' : 'Plan PDC',
      pieces: Object.fromEntries(
        PIECES.map(([cle], j) => {
          const avant = j < 6
          const apres = cle === 'evalFroid' ? passee && new Date(s.fin) < new Date('2026-08-25') : passee
          return [cle, (avant || apres) && (complet || alea() > 0.4)]
        }),
      ),
    })
    // Émargements : un stagiaire de la session s4 n'a pas signé (pour montrer l'alerte)
    if (passee && !(s.id === 's4' && i === 0)) {
      for (const d of jours(s.debut, s.fin)) {
        const absMatin = alea() < 0.05
        presences.push({ id: 'p' + presences.length, apprenant: a, session: s.id, inscription: ins, date: d, matin: !absMatin, apresMidi: alea() > 0.04, motif: absMatin ? 'Raison professionnelle' : '' })
      }
    }
    if (passee) {
      const avant = 6 + Math.round(alea() * 6)
      evaluations.push({ id: 'e' + evaluations.length, apprenant: a, session: s.id, type: 'Positionnement initial', date: s.debut, score: avant, max: 20, resultat: '' })
      const apres = Math.min(20, avant + 4 + Math.round(alea() * 7))
      evaluations.push({ id: 'e' + evaluations.length, apprenant: a, session: s.id, type: 'Evaluation finale', date: s.fin, score: apres, max: 20, resultat: apres >= 14 ? 'Acquis' : apres >= 10 ? 'En cours d’acquisition' : 'Non acquis' })
    }
  }
}

const factures = [
  { id: 'fa1', ref: 'FAC-2026-001', type: 'Facture', client: 'c1', session: 's1', montantHT: 1250, date: '2026-03-13', statut: 'Payé', encaisse: 1250, datePaiement: '2026-04-02' },
  { id: 'fa2', ref: 'FAC-2026-002', type: 'Facture', client: 'c2', session: 's2', montantHT: 8400, date: '2026-06-11', statut: 'Payé', encaisse: 8400, datePaiement: '2026-07-20' },
  { id: 'fa3', ref: 'FAC-2026-003', type: 'Facture', client: 'c4', session: 's3', montantHT: 900, date: '2026-05-06', statut: 'Payé', encaisse: 900, datePaiement: '2026-05-30' },
  { id: 'fa4', ref: 'FAC-2026-004', type: 'Facture', client: 'c3', session: 's4', montantHT: 1250, date: '2026-09-25', statut: 'Envoyé', encaisse: 0, datePaiement: null },
  { id: 'fa5', ref: 'DEV-2026-005', type: 'Devis', client: 'c5', session: 's5', montantHT: 3360, date: '2026-09-01', statut: 'Accepté', encaisse: 0, datePaiement: null },
]

const STATUTS = { 1: 'c', 2: 'e', 4: 'c', 5: 'c', 6: 'c', 8: 'c', 9: 'c', 10: 'e', 11: 'c', 12: 'n', 17: 'c', 18: 'c', 19: 'e', 21: 'c', 22: 'e', 23: 'c', 24: 'n', 25: 'e', 26: 'c', 27: 'c', 30: 'c', 31: 'e', 32: 'e' }
const LIB = { c: '✅ Conforme', e: '⏳En cours', n: '❌ Non conforme', na: '➖ Non applicable' }
const docs = DOCS.documents

const indicateurs = RNQ.indicateurs.map((i) => {
  const s = STATUTS[i.n] || 'na'
  const lies = docs.filter((d) => d.indicateurs.includes(i.n))
  return {
    n: i.n,
    critere: i.critere,
    critereTexte: RNQ.criteres[i.critere - 1].titre,
    libelle: i.libelle,
    preuves: s === 'na' ? '' : 'Exemple : document de référence + trace de mise en œuvre datée.',
    statut: LIB[s],
    score: s === 'c' ? 'A (conforme sans réserve)' : s === 'e' ? 'B (conforme avec suggestion)' : s === 'n' ? 'C (non conforme)' : '',
    verif: s === 'na' ? null : '2026-09-1' + (i.n % 9),
    prochainAudit: '2027-01-18',
    observations: s === 'n' ? 'Exemple fictif : preuve à produire avant l’audit de surveillance.' : '',
    actions: s === 'n' ? 'Exemple fictif : action corrective planifiée.' : '',
    responsable: s === 'na' ? '' : 'Direction',
    nbDocs: lies.length,
    documents: lies.map((d) => d.ref),
    fichiers: s === 'c' ? [{ nom: `preuve-indicateur-${i.n}.pdf`, url: null, taille: 120000 + i.n * 1000 }] : [],
  }
})

export const DEMO = {
  mode: 'demo',
  charge: new Date().toISOString(),
  indicateurs,
  documents: docs.map((d) => ({ id: d.ref, ref: d.ref, titre: d.titre, version: d.version, statut: 'En vigueur', date: d.date, rnq: d.indicateurs.join(', ') })),
  clients,
  formateurs,
  apprenants,
  sessions,
  inscriptions,
  presences,
  evaluations,
  factures,
}

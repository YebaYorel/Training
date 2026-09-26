// Modèle de données d'un organisme client de YEBA Studio (stocké chiffré sur son poste).
// Minimisation RGPD : aucun champ santé (seul le BESOIN d'aménagement est noté, jamais la nature du handicap),
// pas de date de naissance, pas de numéro de sécurité sociale.
import RNQ from '../../src/rnq.json' with { type: 'json' }
import { PIECES } from './pieces.js'

export const TYPES_CLIENT = ['Entreprise privée', 'TPE', 'PME', 'Association 1901', 'Collectivité', 'OPCO', 'France Travail', 'Particulier', 'Organisme de formation', 'Ecole', 'Autre']
export const TYPES_FORMATEUR = ['Interne (Salarié)', 'Dirigeant (non salarié)', 'Externe (Indépendant)', 'Vacataire', 'Sous-traitant']
export const TYPES_SESSION = ['Inter-entreprise', 'Intra-entreprise', 'Distanciel', 'Hybride', 'Sur mesure']
export const STATUTS_SESSION = ['Planifiée', 'Ouverte aux inscriptions', 'Confirmée', 'En cours', 'Terminée', 'Annulée', 'Reportée']
export const STATUTS_INSCRIPTION = ['En attente', 'Confirmé', 'Présent', 'Absent', 'Abandon', 'Annulé']
export const FINANCEMENTS = ['OPCO', 'Plan PDC', 'CPF', 'France Travail', 'Région', 'Contrat Pro', 'Autofinancement', 'Autre']
export const STATUTS_FACTURE = ['Brouillon', 'Envoyé', 'Payé', 'Partiellement payé', 'Impayé']

/** Schémas des collections : pilotent les formulaires, l'import CSV et l'export. */
export const SCHEMAS = {
  formations: {
    titre: 'Formations (catalogue)', singulier: 'formation',
    champs: [
      { cle: 'intitule', libelle: 'Intitulé', requis: true },
      { cle: 'heures', libelle: 'Durée (heures)', type: 'number', requis: true },
      { cle: 'jours', libelle: 'Durée (jours)', type: 'number', requis: true },
      { cle: 'prix', libelle: 'Prix par stagiaire (€ HT)', type: 'number' },
      { cle: 'objectifs', libelle: 'Objectifs (un par ligne)', type: 'textarea' },
      { cle: 'prerequis', libelle: 'Prérequis', type: 'textarea' },
      { cle: 'programme', libelle: 'Programme (une étape par ligne)', type: 'textarea' },
      { cle: 'evaluation', libelle: 'Modalités d’évaluation', type: 'textarea' },
      { cle: 'nsf', libelle: 'Code NSF', aide: 'Spécialité de formation (BPF, cadre F-4). L’assistant peut le suggérer.' },
      { cle: 'certification', libelle: 'Certification visée (RNCP / RS)', aide: 'Laisser vide si aucune.' },
    ],
    affichage: (x) => x.intitule,
  },
  formateurs: {
    titre: 'Formateurs', singulier: 'formateur',
    champs: [
      { cle: 'nom', libelle: 'Nom et prénom', requis: true },
      { cle: 'type', libelle: 'Statut', type: 'select', options: TYPES_FORMATEUR, requis: true },
      { cle: 'email', libelle: 'Email', type: 'email' },
      { cle: 'tel', libelle: 'Téléphone', type: 'tel' },
      { cle: 'specialites', libelle: 'Spécialités' },
      { cle: 'tarifJour', libelle: 'Tarif journalier HT (si externe)', type: 'number' },
    ],
    affichage: (x) => x.nom,
  },
  clients: {
    titre: 'Clients et financeurs', singulier: 'client',
    champs: [
      { cle: 'nom', libelle: 'Raison sociale / nom', requis: true },
      { cle: 'type', libelle: 'Type', type: 'select', options: TYPES_CLIENT, requis: true, aide: 'Sert au classement automatique du BPF (cadre C).' },
      { cle: 'siret', libelle: 'SIRET' },
      { cle: 'contact', libelle: 'Contact' },
      { cle: 'email', libelle: 'Email', type: 'email' },
      { cle: 'tel', libelle: 'Téléphone', type: 'tel' },
      { cle: 'adresse', libelle: 'Adresse', type: 'textarea' },
      { cle: 'opco', libelle: 'OPCO de rattachement' },
    ],
    affichage: (x) => x.nom,
  },
  apprenants: {
    titre: 'Stagiaires', singulier: 'stagiaire',
    champs: [
      { cle: 'nom', libelle: 'Nom et prénom', requis: true },
      { cle: 'entreprise', libelle: 'Entreprise', type: 'ref', ref: 'clients' },
      { cle: 'fonction', libelle: 'Fonction' },
      { cle: 'email', libelle: 'Email', type: 'email' },
      { cle: 'tel', libelle: 'Téléphone', type: 'tel' },
      { cle: 'amenagement', libelle: 'Besoin d’aménagement signalé', type: 'bool', aide: 'Ne jamais noter la nature du handicap (donnée de santé, RGPD art. 9).' },
      { cle: 'amenagementsConvenus', libelle: 'Aménagements convenus', type: 'textarea' },
    ],
    affichage: (x) => x.nom,
  },
  sessions: {
    titre: 'Sessions', singulier: 'session',
    champs: [
      { cle: 'formation', libelle: 'Formation', type: 'ref', ref: 'formations', requis: true },
      { cle: 'type', libelle: 'Type', type: 'select', options: TYPES_SESSION, requis: true },
      { cle: 'debut', libelle: 'Début', type: 'date', requis: true },
      { cle: 'fin', libelle: 'Fin', type: 'date', requis: true },
      { cle: 'horaires', libelle: 'Horaires', aide: 'ex. 08h30–12h00 / 13h00–16h30' },
      { cle: 'lieu', libelle: 'Lieu' },
      { cle: 'formateur', libelle: 'Formateur principal', type: 'ref', ref: 'formateurs' },
      { cle: 'client', libelle: 'Client commanditaire', type: 'ref', ref: 'clients' },
      { cle: 'places', libelle: 'Places', type: 'number' },
      { cle: 'statut', libelle: 'Statut', type: 'select', options: STATUTS_SESSION, requis: true },
      { cle: 'coutFormateur', libelle: 'Coût formateur externe HT', type: 'number' },
      { cle: 'sousTraiteeA', libelle: 'Confiée à un autre organisme', aide: 'Nom de l’organisme si vous sous-traitez cette session (BPF, cadre G).' },
    ],
    affichage: (x, d) => `${nomRef(d, 'formations', x.formation, 'intitule')} · ${dateCourte(x.debut)}`,
  },
  inscriptions: {
    titre: 'Inscriptions', singulier: 'inscription',
    champs: [
      { cle: 'session', libelle: 'Session', type: 'ref', ref: 'sessions', requis: true },
      { cle: 'apprenant', libelle: 'Stagiaire', type: 'ref', ref: 'apprenants', requis: true },
      { cle: 'statut', libelle: 'Statut', type: 'select', options: STATUTS_INSCRIPTION, requis: true },
      { cle: 'financement', libelle: 'Financement', type: 'select', options: FINANCEMENTS },
      { cle: 'financeur', libelle: 'Financeur', type: 'ref', ref: 'clients', aide: 'L’OPCO, France Travail… qui paie (si subrogation).' },
      { cle: 'numeroDossier', libelle: 'N° de dossier / accord' },
      { cle: 'montantAccord', libelle: 'Montant accordé HT', type: 'number' },
      { cle: 'dateDepot', libelle: 'Date de dépôt de la demande', type: 'date' },
    ],
    affichage: (x, d) => `${nomRef(d, 'apprenants', x.apprenant, 'nom')} — ${SCHEMAS.sessions.affichage(d.sessions.find((s) => s.id === x.session) || {}, d)}`,
  },
  factures: {
    titre: 'Factures', singulier: 'facture',
    champs: [
      { cle: 'numero', libelle: 'Numéro', requis: true },
      { cle: 'type', libelle: 'Type', type: 'select', options: ['Facture', 'Avoir', 'Devis'], requis: true },
      { cle: 'client', libelle: 'Client / payeur', type: 'ref', ref: 'clients', requis: true },
      { cle: 'session', libelle: 'Session', type: 'ref', ref: 'sessions' },
      { cle: 'montantHT', libelle: 'Montant HT', type: 'number', requis: true },
      { cle: 'date', libelle: 'Date d’émission', type: 'date', requis: true },
      { cle: 'statut', libelle: 'Statut', type: 'select', options: STATUTS_FACTURE, requis: true },
      { cle: 'encaisse', libelle: 'Montant encaissé', type: 'number' },
      { cle: 'datePaiement', libelle: 'Date de paiement', type: 'date' },
    ],
    affichage: (x) => `${x.numero} — ${x.montantHT ?? 0} €`,
  },
}

export const CHAMPS_ORGANISME = [
  { cle: 'nom', libelle: 'Nom de l’organisme', requis: true },
  { cle: 'formeJuridique', libelle: 'Forme juridique', aide: 'ex. Entreprise individuelle (micro-entreprise), SARL, SAS, association…' },
  { cle: 'siret', libelle: 'SIRET', requis: true },
  { cle: 'nda', libelle: 'N° de déclaration d’activité (NDA)', requis: true },
  { cle: 'prefecture', libelle: 'Préfecture d’enregistrement', aide: 'ex. Préfet de la région Réunion' },
  { cle: 'qualiopi', libelle: 'N° de certificat Qualiopi' },
  { cle: 'certificateur', libelle: 'Organisme certificateur' },
  { cle: 'adresse', libelle: 'Adresse', requis: true },
  { cle: 'codePostal', libelle: 'Code postal', requis: true },
  { cle: 'ville', libelle: 'Ville', requis: true },
  { cle: 'dirigeant', libelle: 'Dirigeant (nom et fonction)', requis: true },
  { cle: 'referentHandicap', libelle: 'Référent handicap', requis: true },
  { cle: 'referentPedagogique', libelle: 'Référent pédagogique' },
  { cle: 'email', libelle: 'Email de contact', type: 'email', requis: true },
  { cle: 'tel', libelle: 'Téléphone', type: 'tel', requis: true },
  { cle: 'site', libelle: 'Site internet' },
  { cle: 'tva', libelle: 'Régime de TVA', type: 'select', options: ['TVA non applicable, art. 293 B du CGI', 'Exonération art. 261-4-4° a du CGI (attestation DREETS)', 'Assujetti à la TVA'], requis: true },
  { cle: 'mediateur', libelle: 'Médiateur de la consommation (nom et adresse)', aide: 'Obligatoire si vous formez des particuliers (C. conso. L.612-1).' },
  { cle: 'assureur', libelle: 'Assureur responsabilité civile professionnelle' },
  { cle: 'horaires', libelle: 'Horaires habituels', aide: 'ex. 08h30–12h00 / 13h00–16h30' },
  { cle: 'couleur', libelle: 'Couleur de vos documents', type: 'color' },
]

export function donneesVides() {
  return {
    v: 1,
    organisme: { couleur: '#1B3A6B', tva: 'TVA non applicable, art. 293 B du CGI', prefecture: 'Préfet de la région Réunion' },
    formations: [], formateurs: [], clients: [], apprenants: [], sessions: [], inscriptions: [], presences: [], evaluations: [], factures: [],
    indicateurs: {},
    parametres: { bpf: {}, carburant: { securise: [], alertesVues: [] } },
    journal: [],
  }
}

export const nouvelId = () => crypto.getRandomValues(new Uint32Array(2)).reduce((a, x) => a + x.toString(36), '')
export const nomRef = (d, coll, id, champ) => (d[coll] || []).find((x) => x.id === id)?.[champ] ?? '—'
export const dateCourte = (d) => (d ? new Date(d + 'T12:00:00').toLocaleDateString('fr-FR') : '—')

const LIB_STATUT = { conforme: '✅ Conforme', 'en-cours': '⏳En cours', 'non-conforme': '❌ Non conforme', na: '➖ Non applicable', '': '⏳En cours' }
export const STATUTS_INDICATEUR = [['en-cours', 'En cours'], ['conforme', 'Conforme'], ['non-conforme', 'Non conforme'], ['na', 'Non applicable']]

/** Transforme les données locales au format commun des modules (même forme que la démo et Airtable). */
export function versDb(d) {
  const idx = (l, f) => Object.fromEntries(l.map((x) => [x.id, f(x)]))
  const formations = idx(d.formations, (x) => x)
  const piecesVides = Object.fromEntries(PIECES.map(([k]) => [k, false]))
  return {
    mode: 'local',
    charge: new Date().toISOString(),
    organisme: d.organisme,
    indicateurs: RNQ.indicateurs.map((i) => {
      const l = d.indicateurs[i.n] || {}
      return {
        n: i.n, critere: i.critere, critereTexte: RNQ.criteres[i.critere - 1].titre, libelle: i.libelle,
        preuves: l.preuves || '', statut: LIB_STATUT[l.statut || ''], score: '', verif: l.verif || null, prochainAudit: d.organisme.prochainAudit || null,
        observations: l.notes || '', actions: l.actions || '', responsable: l.responsable || '', nbDocs: (l.documents || []).length,
        documents: l.documents || [], fichiers: [], cle: l.statut || '',
      }
    }),
    documents: [],
    clients: idx(d.clients, (x) => ({ nom: x.nom, type: x.type || null })),
    formateurs: idx(d.formateurs, (x) => ({ nom: x.nom, type: x.type === 'Dirigeant (non salarié)' ? 'Interne (Salarié)' : x.type || null })),
    apprenants: idx(d.apprenants, (x) => ({ nom: x.nom })),
    sessions: d.sessions.map((s) => {
      const f = formations[s.formation] || {}
      return {
        id: s.id, nom: `${f.intitule || 'Formation'} · ${dateCourte(s.debut)}`, formation: f.intitule || 'Formation non renseignée',
        heures: Number(f.heures) || 0, jours: Number(f.jours) || 0, formateurs: s.formateur ? [s.formateur] : [], client: s.client || null,
        type: s.type || '', debut: s.debut || null, fin: s.fin || s.debut || null, lieu: s.lieu || '', statut: s.statut || '',
        coutFormateur: Number(s.coutFormateur) || 0, places: Number(s.places) || 0, sousTraiteeA: s.sousTraiteeA || null, horaires: s.horaires || '',
      }
    }),
    inscriptions: d.inscriptions.map((i) => ({ ...i, pieces: { ...piecesVides, ...(i.pieces || {}) } })),
    presences: d.presences,
    evaluations: d.evaluations,
    factures: d.factures.map((f) => ({ ...f, ref: f.numero, montantHT: Number(f.montantHT) || 0, encaisse: Number(f.encaisse) || 0 })),
  }
}

/* ---------- CSV (séparateur ; ou ,) ---------- */
export function lireCsv(texte) {
  const t = texte.replace(/^﻿/, '')
  const sep = (t.split('\n')[0].match(/;/g) || []).length >= (t.split('\n')[0].match(/,/g) || []).length ? ';' : ','
  const lignes = []
  let champ = '', ligne = [], guillemets = false
  for (let i = 0; i < t.length; i++) {
    const c = t[i]
    if (guillemets) {
      if (c === '"' && t[i + 1] === '"') { champ += '"'; i++ } else if (c === '"') guillemets = false
      else champ += c
    } else if (c === '"') guillemets = true
    else if (c === sep) { ligne.push(champ); champ = '' }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && t[i + 1] === '\n') i++
      ligne.push(champ); champ = ''
      if (ligne.some((x) => x.trim())) lignes.push(ligne)
      ligne = []
    } else champ += c
  }
  ligne.push(champ)
  if (ligne.some((x) => x.trim())) lignes.push(ligne)
  return lignes
}

export function versCsv(lignes) {
  const cellule = (v) => {
    const s = String(v ?? '')
    const sur = /^[=+\-@\t\r]/.test(s) ? "'" + s : s // pas d'injection de formule dans Excel
    return /[;"\n]/.test(sur) ? `"${sur.replace(/"/g, '""')}"` : sur
  }
  return '﻿' + lignes.map((l) => l.map(cellule).join(';')).join('\r\n')
}

/** Convertit une date saisie « 12/03/2026 » ou « 2026-03-12 » en ISO. */
export function dateIso(v) {
  const s = String(v || '').trim()
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s
  const m = s.match(/^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$/)
  if (!m) return ''
  const a = m[3].length === 2 ? '20' + m[3] : m[3]
  return `${a}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`
}
export const nombre = (v) => {
  const n = Number(String(v ?? '').replace(/\s|€/g, '').replace(',', '.'))
  return Number.isFinite(n) ? n : null
}

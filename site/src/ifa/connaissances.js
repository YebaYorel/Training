// Ce que sait IFA, et comment elle comprend une question.
// Réponses programmées à partir du catalogue (Airtable) et de la FAQ : aucune IA générative,
// aucun message envoyé à un tiers, aucune réponse inventée. Si elle ne sait pas, elle le dit
// et propose un rappel.

import { ENTREPRISE, FAQ, FORMATIONS, euros } from '../data.js'

export const SUGGESTIONS_ACCUEIL = ['Voir les formations', 'Les tarifs', 'Le financement', 'Être rappelé']

const normaliser = (t) =>
  t
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9 ]/g, ' ')

const faq = (debut) => FAQ.find(([q]) => q.startsWith(debut))?.[1] ?? ''

function trouverFormation(t) {
  // Nom court (« allumage », « pilote automatique »…) ou référence (« FOR-0011 »)
  const refs = t.match(/for 00(\d\d)/)
  if (refs) return FORMATIONS.find((f) => f.ref.endsWith(refs[1]))
  return FORMATIONS.map((f) => ({ f, cles: normaliser(f.nom).split(/[\s-]+/).filter((m) => m.length > 3) }))
    .map(({ f, cles }) => ({ f, score: cles.filter((c) => t.includes(c)).length / cles.length }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)[0]?.f
}

function ficheCourte(f) {
  const t = f.tarifs
  const prix = t?.interTotal
    ? `${euros(t.interTotal)} par personne en inter`
    : t?.intraTotal
      ? `${euros(t.intraTotal)} pour un groupe en intra`
      : 'sur devis'
  return [
    `${f.nom} — ${f.sousTitre}.`,
    `Durée : ${f.jours} jour${f.jours > 1 ? 's' : ''} (${f.heures} h). Tarif : ${prix}${t?.intraTotal && t?.interTotal ? `, ou ${euros(t.intraTotal)} pour un groupe dans vos locaux` : ''}.`,
    f.public ? `Pour qui : ${f.public.split('\n')[0]}` : '',
  ].filter(Boolean)
}

const INTENTIONS = [
  {
    mots: ['bonjour', 'salut', 'hello', 'bonsoir', 'coucou'],
    rep: () => ({
      texte: ['Bonjour ! Je suis IFA. Je peux vous présenter nos formations, leurs tarifs, les financements possibles, ou organiser un rappel avec Aurélien.'],
      suggestions: SUGGESTIONS_ACCUEIL,
    }),
  },
  {
    mots: ['humain', 'robot', 'qui es tu', 'tu es qui', 'vraie personne', 'intelligence artificielle', 'ia ou'],
    rep: () => ({
      texte: [
        'Je suis une assistante virtuelle : mes réponses sont programmées à partir de notre catalogue et de nos questions fréquentes. Je ne suis pas une personne.',
        'Pour parler à un humain, je peux organiser un rappel avec Aurélien LUMEKA, le dirigeant.',
      ],
      suggestions: ['Être rappelé', 'Voir les formations'],
    }),
  },
  {
    mots: ['rappel', 'rappeler', 'rdv', 'rendez vous', 'appel', 'appeler', 'contacter', 'contact', 'parler', 'joindre', 'telephone', 'devis'],
    rep: () => ({ texte: ['Avec plaisir ! Choisissez le jour et l’heure qui vous arrangent : Aurélien vous rappelle.'], action: 'rdv' }),
  },
  {
    mots: ['cpf', 'compte personnel'],
    rep: () => ({ texte: [faq('Et le CPF')], suggestions: ['Le financement', 'Être rappelé'] }),
  },
  {
    mots: ['financ', 'opco', 'prise en charge', 'france travail', 'pole emploi', 'aif', 'region', 'rembours', 'payer moins'],
    rep: () => ({ texte: [faq('Mes formations peuvent-elles')], suggestions: ['Et le CPF ?', 'Être rappelé'] }),
  },
  {
    mots: ['prix', 'tarif', 'cout', 'combien', 'cher', 'budget', 'euro'],
    rep: (t) => {
      const f = trouverFormation(t)
      if (f) return { texte: ficheCourte(f), suggestions: ['Le financement', 'Être rappelé'] }
      const prix = FORMATIONS.map((x) => x.tarifs?.interTotal).filter(Boolean)
      return {
        texte: [
          `Nos formations vont de ${euros(Math.min(...prix))} à ${euros(Math.max(...prix))} par personne en inter-entreprises, prix nets de taxe (TVA non applicable, art. 293 B du CGI).`,
          'En intra, dans vos locaux, le prix est fixé pour tout le groupe, jusqu’à 10 personnes. Quelle formation vous intéresse ?',
        ],
        suggestions: FORMATIONS.slice(0, 4).map((x) => x.nom),
      }
    },
  },
  {
    mots: ['delai', 'quand', 'demarr', 'commencer', 'date', 'session', 'prochaine'],
    rep: () => ({ texte: [faq('Combien de temps'), 'Pour les prochaines dates, le plus simple est d’en parler de vive voix.'], suggestions: ['Être rappelé'] }),
  },
  {
    mots: ['handicap', 'accessib', 'amenagement', 'malvoyant', 'mobilite reduite'],
    rep: () => ({ texte: [faq('Je suis en situation'), `Référent handicap : ${ENTREPRISE.dirigeant}.`], suggestions: ['Être rappelé'] }),
  },
  {
    mots: ['intra', 'inter', 'ou se', 'lieu', 'locaux', 'deplac', 'hotel', 'seminaire', 'dans quelle ville'],
    rep: () => ({
      texte: [faq('Intra ou inter'), 'Nous intervenons partout à La Réunion, depuis Sainte-Clotilde.'],
      suggestions: ['Les tarifs', 'Être rappelé'],
    }),
  },
  {
    mots: ['horaire', 'heure', 'pause', 'journee'],
    rep: () => ({ texte: ['08h00–12h00 et 13h00–17h00, avec deux pauses incluses à 10h et 15h : 8 heures de formation par jour.'] }),
  },
  {
    mots: ['rgpd', 'ia act', 'ai act', 'conformite', 'audit', 'gouvernance', 'cnil', 'donnees personnelles', 'reglement'],
    rep: () => ({
      texte: [
        'Nous accompagnons les entreprises sur le RGPD et l’IA Act : inventaire des usages d’IA, registre des traitements, charte d’usage, mentions de transparence.',
        'Nous ne vendons pas de « mise en conformité » miracle : nous vous aidons à prouver les mesures prises. La formation CONTRÔLE TECHNIQUE couvre l’essentiel en une journée.',
      ],
      suggestions: ['Contrôle technique', 'Être rappelé'],
    }),
  },
  {
    mots: ['automatis', 'workflow', 'n8n', 'site internet', 'site web', 'application', 'base de donnees', 'agent', 'solution', 'outil', 'implement'],
    rep: () => ({
      texte: [
        'Au-delà des formations, nous construisons avec vous des workflows automatisés, des assistants IA, des sites internet et des bases de données, en privilégiant des outils européens.',
        'Décrivez-nous la tâche qui vous prend le plus de temps : on regarde ensemble ce qui peut être automatisé.',
      ],
      suggestions: ['Être rappelé', 'Faire le diagnostic'],
    }),
  },
  {
    mots: ['diagnostic', 'par ou commencer', 'conseil', 'quelle formation', 'recommand'],
    rep: () => ({ texte: ['Le diagnostic IA express répond à 6 questions et vous conseille 3 formations. Je vous y emmène ?'], action: 'diagnostic' }),
  },
  {
    mots: ['formation', 'catalogue', 'programme', 'liste', 'proposez'],
    rep: () => ({
      texte: [
        'Voici notre catalogue :',
        ...FORMATIONS.map((f) => `• ${f.nom} — ${f.sousTitre} (${f.jours} j)`),
        'Laquelle voulez-vous découvrir ?',
      ],
      suggestions: ['Allumage-Turbo', 'Contrôle technique', 'Tableau de bord', 'Être rappelé'],
    }),
  },
  {
    mots: ['attestation', 'certificat', 'diplome', 'a la fin'],
    rep: () => ({ texte: [faq('Qu’est-ce que je reçois')] }),
  },
  {
    mots: ['securite', 'confidentiel', 'mes donnees'],
    rep: () => ({ texte: [faq('Nos données sont-elles')] }),
  },
  {
    mots: ['merci', 'super', 'parfait', 'genial'],
    rep: () => ({ texte: ['Avec plaisir ! Je reste là si vous avez une autre question.'], suggestions: ['Être rappelé'] }),
  },
]

/** Transforme une question en réponse. */
export function repondre(question) {
  const t = normaliser(question)
  // Une formation citée par son nom prime sur le reste, sauf demande de prix ou de rappel
  const f = trouverFormation(t)
  // La salutation ne l'emporte que si rien d'autre n'est demandé (« Bonjour, quel prix ? » → le prix)
  const trouvees = INTENTIONS.filter((i) => i.mots.some((m) => t.includes(m)))
  const intention = trouvees.find((i) => !i.mots.includes('bonjour')) ?? trouvees[0]
  if (f && (!intention || !['prix', 'rappel'].some((m) => intention.mots.includes(m)))) {
    return { texte: ficheCourte(f), suggestions: ['Le financement', 'Être rappelé'], lien: '#formations' }
  }
  if (intention) return intention.rep(t)
  return {
    texte: [
      'Je ne suis pas sûre de bien comprendre, et je préfère ne pas vous répondre au hasard.',
      `Aurélien peut vous répondre directement : je vous organise un rappel ? Vous pouvez aussi appeler le ${ENTREPRISE.telAffiche}.`,
    ],
    suggestions: ['Être rappelé', 'Voir les formations', 'Les tarifs'],
  }
}

/* ---------- Agenda de rappel : jours ouvrés de La Réunion ---------- */
function paques(annee) {
  // Algorithme de Meeus/Jones/Butcher
  const a = annee % 19, b = Math.floor(annee / 100), c = annee % 100, d = Math.floor(b / 4), e = b % 4
  const f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30
  const i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451)
  const mois = Math.floor((h + l - 7 * m + 114) / 31), jour = ((h + l - 7 * m + 114) % 31) + 1
  return new Date(Date.UTC(annee, mois - 1, jour))
}
const iso = (d) => d.toISOString().slice(0, 10)
function feriesReunion(annee) {
  const p = paques(annee)
  const decal = (n) => iso(new Date(p.getTime() + n * 86400000))
  return new Set([
    `${annee}-01-01`, decal(1), `${annee}-05-01`, `${annee}-05-08`, decal(39), decal(50), `${annee}-07-14`,
    `${annee}-08-15`, `${annee}-11-01`, `${annee}-11-11`, `${annee}-12-20`, `${annee}-12-25`, // 20 déc. : abolition de l'esclavage à La Réunion
  ])
}

/** Jours et créneaux proposés, calculés à l'heure de La Réunion (UTC+4, sans heure d'été). */
export function creneaux({ joursAffiches, delaiMinHeures, plages, pasMinutes }, maintenant = new Date()) {
  const DECALAGE = 4 * 3600000
  const localNow = new Date(maintenant.getTime() + DECALAGE) // « horloge murale » réunionnaise lue en UTC
  const limite = localNow.getTime() + delaiMinHeures * 3600000
  const jours = []
  for (let n = 0; jours.length < joursAffiches && n < 40; n++) {
    const d = new Date(Date.UTC(localNow.getUTCFullYear(), localNow.getUTCMonth(), localNow.getUTCDate() + n))
    const js = d.getUTCDay()
    if (js === 0 || js === 6 || feriesReunion(d.getUTCFullYear()).has(iso(d))) continue
    const heures = []
    for (const [debut, fin] of plages) {
      const [hd, md] = debut.split(':').map(Number)
      const [hf, mf] = fin.split(':').map(Number)
      for (let m = hd * 60 + md; m <= hf * 60 + mf; m += pasMinutes) {
        if (d.getTime() + m * 60000 < limite) continue
        heures.push(`${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`)
      }
    }
    if (heures.length) jours.push({ date: iso(d), heures })
  }
  return jours
}

export const libelleJour = (date, long = false) =>
  new Date(date + 'T12:00:00Z').toLocaleDateString('fr-FR', {
    weekday: long ? 'long' : 'short',
    day: 'numeric',
    month: long ? 'long' : 'short',
    timeZone: 'UTC',
  })

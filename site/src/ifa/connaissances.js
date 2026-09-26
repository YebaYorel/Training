// Ce que sait IFA, et comment elle comprend une question.
// Réponses programmées à partir du catalogue (Airtable), de la FAQ et des documents publics : aucune IA
// générative, aucun message envoyé à un tiers, aucune réponse inventée. Si elle ne sait pas, elle le dit,
// propose ce qu'elle a cru comprendre, puis un rappel.
// IA Act (art. 50) : IFA se présente toujours comme une assistante virtuelle, jamais comme une personne.

import { AGENDA, CERTIFS, ENTREPRISE, FAQ, FORMATIONS, euros } from '../data.js'
import { OFFRES } from '../../espace/src/licence.js'

export const SUGGESTIONS_ACCUEIL = ['Voir les formations', 'Les tarifs', 'Le financement', 'Être rappelé']

const normaliser = (t) =>
  t
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9 ]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

const faq = (debut) => FAQ.find(([q]) => q.startsWith(debut))?.[1] ?? ''
const hasard = (liste) => liste[Math.floor(Math.random() * liste.length)]

/* ---------- Tolérance aux fautes de frappe (distance de Levenshtein bornée) ---------- */
function distance(a, b, max) {
  if (Math.abs(a.length - b.length) > max) return max + 1
  let prec = Array.from({ length: b.length + 1 }, (_, i) => i)
  for (let i = 1; i <= a.length; i++) {
    const cour = [i]
    let minLigne = i
    for (let j = 1; j <= b.length; j++) {
      cour[j] = Math.min(prec[j] + 1, cour[j - 1] + 1, prec[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1))
      minLigne = Math.min(minLigne, cour[j])
    }
    if (minLigne > max) return max + 1
    prec = cour
  }
  return prec[b.length]
}
const tolerance = (mot) => (mot.length >= 8 ? 2 : mot.length >= 5 ? 1 : 0)

/** Le texte contient-il la clé (exacte, préfixe, ou à une ou deux fautes près pour les mots longs) ? */
function contient(t, mots, cle, plafond = 2) {
  // Clé de plusieurs mots : début de mot ; clé courte (≤ 4 lettres) : mot exact (« cher » ≠ « cherche ») ;
  // sinon préfixe d'un mot (« financ » → financement, financer…).
  if (cle.includes(' ')) return ` ${t} `.includes(' ' + cle)
  if (cle.length <= 4 ? mots.includes(cle) : mots.some((m) => m.startsWith(cle))) return true
  const tol = Math.min(tolerance(cle), plafond)
  return tol > 0 && mots.some((m) => m.length >= 4 && distance(m, cle, tol) <= tol)
}

/* ---------- Formations ---------- */
const MOTS_VIDES = new Set(['sans', 'avec', 'pour', 'dans', 'sous', 'votre', 'vos', 'travail', 'niveau', 'jours', 'methode', 'quotidien'])
function motsFormation(f) {
  return normaliser(f.nom).split(/[\s-]+/).filter((m) => m.length > 3 && !MOTS_VIDES.has(m))
}
function trouverFormation(t, mots) {
  const refs = t.match(/for 0*(\d{1,2})\b/)
  if (refs) return FORMATIONS.find((f) => Number(f.ref.slice(-2)) === Number(refs[1]))
  return FORMATIONS.map((f) => {
    const cles = motsFormation(f)
    return { f, score: cles.filter((c) => contient(t, mots, c, 1)).length / cles.length }
  })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)[0]?.f
}

function prixDe(f) {
  const t = f.tarifs
  if (t?.interTotal) return `${euros(t.interTotal)} par personne en inter${t.intraTotal ? `, ou ${euros(t.intraTotal)} pour un groupe dans vos locaux` : ''}`
  if (t?.intraTotal) return `${euros(t.intraTotal)} pour un groupe en intra`
  return 'sur devis'
}

function ficheCourte(f) {
  return [
    `${f.nom} — ${f.sousTitre}.`,
    `Durée : ${f.jours} jour${f.jours > 1 ? 's' : ''} (${f.heures} h). Tarif : ${prixDe(f)}.`,
    f.public ? `Pour qui : ${f.public.split('\n')[0]}` : '',
  ].filter(Boolean)
}

// Questions de suivi sur la dernière formation évoquée (« et le prix ? », « c'est pour qui ? »…)
const SUIVIS = [
  { mots: ['duree', 'combien de jours', 'combien d heures', 'long'], rep: (f) => [`${f.nom} dure ${f.jours} jour${f.jours > 1 ? 's' : ''}, soit ${f.heures} heures.`] },
  { mots: ['prix', 'tarif', 'cout', 'coute', 'combien', 'cher'], rep: (f) => [`${f.nom} : ${prixDe(f)}. TVA non applicable, art. 293 B du CGI.`] },
  { mots: ['pour qui', 'public', 'qui peut', 'concerne'], rep: (f) => [f.public ? `${f.nom} s’adresse à : ${f.public.split('\n')[0]}` : 'Le public visé est détaillé sur la fiche.'] },
  { mots: ['prerequis', 'niveau', 'debutant', 'faut il savoir'], rep: (f) => [f.prerequis ? `Prérequis : ${f.prerequis.split('\n')[0]}` : 'Aucun prérequis particulier n’est indiqué sur la fiche.'] },
  { mots: ['objectif', 'apprendre', 'programme', 'contenu', 'on fait quoi'], rep: (f) => (f.objectifs?.length ? ['À l’issue de la formation, vous saurez :', ...f.objectifs.slice(0, 4).map((o) => '• ' + o)] : [`Le programme complet de ${f.nom} est sur sa fiche, dans le catalogue.`]) },
  { mots: ['groupe', 'combien de personnes', 'effectif', 'participants'], rep: (f) => [f.effectif ? `Groupe : ${f.effectif}.` : 'La taille du groupe est précisée sur le devis.'] },
  { mots: ['evaluation', 'evalue', 'examen', 'test'], rep: (f) => [f.evaluation ? `Évaluation : ${f.evaluation.split('\n')[0]}` : 'Positionnement à l’entrée, évaluation des acquis à la sortie et questionnaire de satisfaction.'] },
]

/* ---------- Ton : on s'adapte au visiteur ---------- */
const SALUTS_FAMILIERS = ['salut', 'coucou', 'hello', 'hey', 'yo', 'wesh', 'kikou', 'slt', 'bjr', 'cc']
export function analyserTon(brut) {
  const debut = brut.trim().split(/[\s,!.?]+/)[0] || ''
  const d = normaliser(debut)
  const t = normaliser(brut)
  let salut = null
  if (['bonjour', 'bonsoir'].includes(d)) salut = debut[0] === debut[0].toUpperCase() ? 'formel' : 'detendu'
  else if (SALUTS_FAMILIERS.includes(d)) salut = 'familier'
  return {
    salut,
    motSalut: d,
    politesse: /\b(svp|stp|s il (vous|te) plait|sil vous plait|merci d avance|je vous prie)\b/.test(t),
    tutoie: /\b(tu|t es|toi|ton|ta|tes|peux tu|sais tu|stp)\b/.test(t) && !/\bvous\b/.test(t),
  }
}

/* ---------- Garde-fou : ce qui se vend ne se donne pas ---------- */
const DEMANDES_PAYANTES = [
  'donne moi le prompt', 'donne le prompt', 'tes prompts', 'vos prompts', 'prompt complet', 'modele de charte', 'modele de registre',
  'template', 'fichier modele', 'redige moi', 'redige', 'ecris moi', 'fais mon', 'genere moi', 'code source',
  'workflow complet', 'etape par etape', 'tuto', 'tutoriel', 'support de cours', 'supports de formation', 'le pdf de la formation',
  'audit gratuit', 'methode complete', 'explique moi comment automatiser', 'comment on fait un agent',
]

/* ---------- Intentions ---------- */
const INTENTIONS = [
  {
    id: 'identite',
    mots: ['humain', 'robot', 'qui es tu', 'tu es qui', 't es qui', 'vraie personne', 'intelligence artificielle', 'ia ou', 'chatgpt', 'es tu une ia', 'bot'],
    rep: (_, ton) => ({
      texte: [
        ton.tutoie
          ? 'Je suis IFA, une assistante virtuelle : mes réponses sont programmées à partir de notre catalogue. Je ne suis pas une personne, et je ne fais appel à aucune IA externe.'
          : 'Je suis IFA, une assistante virtuelle : mes réponses sont programmées à partir de notre catalogue et de nos questions fréquentes. Je ne suis pas une personne, et je n’envoie vos questions à aucune IA externe.',
        'Pour parler à un humain, je peux organiser un rappel avec Aurélien LUMEKA, le dirigeant.',
      ],
      suggestions: ['Être rappelé', 'Voir les formations'],
    }),
  },
  {
    id: 'rappel',
    mots: ['rappel', 'rappeler', 'rdv', 'rendez vous', 'appelez moi', 'appeler', 'contacter', 'parler a', 'joindre', 'devis', 'etre rappele', 'reserver'],
    rep: () => ({ texte: ['Avec plaisir ! Choisissez le jour et l’heure qui vous arrangent : Aurélien vous rappelle.'], action: 'rdv' }),
  },
  {
    id: 'coordonnees',
    mots: ['numero', 'telephone', 'adresse', 'mail', 'email', 'courriel', 'ou etes vous', 'situe', 'siege'],
    rep: () => ({
      texte: [`📞 ${ENTREPRISE.telAffiche}`, `✉️ ${ENTREPRISE.email}`, `📍 ${ENTREPRISE.adresse}`, 'Préférez-vous que je vous organise un rappel ?'],
      suggestions: ['Être rappelé'],
    }),
  },
  { id: 'cpf', mots: ['cpf', 'compte personnel', 'moncompteformation'], rep: () => ({ texte: [faq('Et le CPF')], suggestions: ['Le financement', 'Être rappelé'] }) },
  {
    id: 'financement',
    mots: ['financ', 'opco', 'prise en charge', 'france travail', 'pole emploi', 'aif', 'region', 'rembours', 'payer moins', 'aides', 'subvention', 'akto', 'opcommerce', 'atlas', 'constructys'],
    rep: () => ({ texte: [faq('Mes formations peuvent-elles'), 'La notice des financements est disponible dans la section Qualiopi du site, sur simple demande.'], suggestions: ['Et le CPF ?', 'Être rappelé'] }),
  },
  {
    id: 'prix',
    mots: ['prix', 'tarif', 'cout', 'coute', 'combien', 'cher', 'chere', 'budget', 'euro', 'euros', 'devis gratuit'],
    rep: (t, _, mots) => {
      const f = trouverFormation(t, mots)
      if (f) return { texte: ficheCourte(f), suggestions: ['Le financement', 'Être rappelé'], formation: f }
      const prix = FORMATIONS.map((x) => x.tarifs?.interTotal).filter(Boolean)
      return {
        texte: [
          `Nos formations vont de ${euros(Math.min(...prix))} à ${euros(Math.max(...prix))} par personne en inter-entreprises, prix nets (TVA non applicable, art. 293 B du CGI).`,
          'En intra, dans vos locaux, le prix est fixé pour tout le groupe. Quelle formation vous intéresse ?',
        ],
        suggestions: FORMATIONS.slice(0, 4).map((x) => x.nom),
      }
    },
  },
  {
    id: 'dates',
    mots: ['session', 'prochaine', 'date', 'calendrier', 'planning', 'quand', 'inter entreprise'],
    rep: () => {
      if (AGENDA.length) {
        const nom = (ref) => FORMATIONS.find((f) => f.ref === ref)?.nom || ref
        return {
          texte: ['Prochaines sessions ouvertes :', ...AGENDA.slice(0, 4).map((s) => `• ${nom(s.ref)} — ${new Date(s.debut).toLocaleDateString('fr-FR')}${s.lieu ? ', ' + s.lieu : ''}`)],
          suggestions: ['Être rappelé'],
          lien: '#formations',
        }
      }
      return { texte: ['Aucune session inter-entreprises n’est publiée pour le moment. En intra, on fixe la date avec vous.', faq('Combien de temps')], suggestions: ['Être rappelé', 'Intra ou inter ?'] }
    },
  },
  { id: 'delai', mots: ['delai', 'demarr', 'commencer', 'rapidement', 'urgent', 'vite'], rep: () => ({ texte: [faq('Combien de temps')], suggestions: ['Être rappelé'] }) },
  {
    id: 'inscription',
    mots: ['inscri', 'inscrire', 's inscrire', 'comment faire pour', 'modalite', 'etapes'],
    rep: () => ({
      texte: [
        'L’inscription se fait en 4 temps :',
        '1. Un échange pour cerner votre besoin (positionnement).',
        '2. Un devis, puis une convention (entreprise) ou un contrat (particulier).',
        '3. La convocation, le programme et le règlement intérieur, avant le démarrage.',
        '4. La formation, puis l’attestation de fin et le questionnaire de satisfaction.',
      ],
      suggestions: ['Être rappelé', 'Le financement'],
    }),
  },
  { id: 'handicap', mots: ['handicap', 'accessib', 'amenagement', 'malvoyant', 'malentendant', 'mobilite reduite', 'dys', 'fauteuil'], rep: () => ({ texte: [faq('Je suis en situation'), `Référent handicap : ${ENTREPRISE.dirigeant}. Vous n’avez pas à préciser la nature de votre handicap : seul le besoin d’aménagement compte.`], suggestions: ['Être rappelé'] }) },
  {
    id: 'lieu',
    mots: ['intra', 'ou se', 'lieu', 'locaux', 'deplac', 'hotel', 'seminaire', 'dans quelle ville', 'distanciel', 'distance', 'visio', 'presentiel', 'en ligne'],
    rep: () => ({ texte: [faq('Intra ou inter'), 'Nous intervenons en présentiel partout à La Réunion, depuis Sainte-Clotilde. Le distanciel se discute au cas par cas.'], suggestions: ['Les tarifs', 'Être rappelé'] }),
  },
  { id: 'horaires', mots: ['horaire', 'heure de debut', 'pause', 'a quelle heure', 'journee type'], rep: () => ({ texte: ['08h00–12h00 et 13h00–17h00, avec deux pauses incluses à 10h et 15h : 8 heures de formation par jour. Les horaires exacts figurent sur votre convocation.'] }) },
  {
    id: 'cyclone',
    mots: ['cyclone', 'alerte orange', 'alerte rouge', 'meteo', 'forte pluie'],
    rep: () => ({ texte: ['Notre règlement intérieur est clair : en alerte cyclonique orange, la session est suspendue ; en alerte rouge, personne ne se déplace. La session est alors reportée sans frais. Votre sécurité d’abord !'], lien: '#qualiopi' }),
  },
  {
    id: 'studio',
    mots: ['logiciel', 'studio', 'bpf', 'bilan pedagogique', 'carburant', 'erp', 'ypareo', 'digiforma', 'dendreo', 'kit qualiopi', 'pack qualiopi', 'modeles qualiopi', 'emargement', 'gestion des sessions', 'opco qui paie', 'impaye'],
    rep: () => ({
      texte: [
        'YEBA Studio, ce sont nos logiciels pour les organismes de formation :',
        `• ${OFFRES.qualiopi.nom} — ${OFFRES.qualiopi.libellePrix} : les documents Qualiopi en Word, remplis à votre nom.`,
        `• ${OFFRES.bpf.nom} — ${OFFRES.bpf.libellePrix} : l’assistant remplit votre BPF.`,
        `• ${OFFRES.parcours.nom} — ${OFFRES.parcours.libellePrix} : sessions, dossiers, émargements, documents.`,
        `• CARBURANT — ${OFFRES.carburant.premierMois} € le 1er mois puis ${OFFRES.carburant.prix} €/mois : l’IA qui fait rentrer l’argent des OPCO.`,
        '14 jours d’essai gratuits, vos données restent chiffrées sur votre PC.',
      ],
      lien: '#studio',
      suggestions: ['Être rappelé'],
    }),
  },
  {
    id: 'qualiopi',
    mots: ['qualiopi', 'certifi', 'qualite', 'document', 'reglement interieur', 'cgv', 'conditions generales', 'preuve', 'nda', 'declaration d activite'],
    rep: () => ({
      texte: [
        `Nous sommes certifiés Qualiopi (n° ${ENTREPRISE.qualiopi}, catégorie actions de formation). Déclaration d’activité n° ${ENTREPRISE.nda}.`,
        'Nos documents qualité (règlement intérieur, politique handicap, CGV, notice des financements…) sont listés dans la section Qualiopi : en lecture libre ou sur simple demande.',
      ],
      lien: '#qualiopi',
      suggestions: ['Être rappelé'],
    }),
  },
  {
    id: 'annulation',
    mots: ['annul', 'report', 'retract', 'desist', 'rembourse'],
    rep: () => ({ texte: ['Les conditions d’annulation et de report sont écrites dans nos conditions générales et dans votre convention. Un particulier dispose en plus d’un délai de rétractation de 10 jours après la signature de son contrat.', 'Aurélien peut vous les détailler.'], suggestions: ['Être rappelé'] }),
  },
  {
    id: 'formateur',
    mots: ['formateur', 'intervenant', 'aurelien', 'lumeka', 'dirigeant', 'experience', 'qui anime', 'qui forme'],
    rep: () => ({ texte: [`Les formations sont animées par ${ENTREPRISE.dirigeant}, formateur en vente, management et soft skills depuis 2021, aujourd’hui spécialisé en IA et en gouvernance RGPD / IA Act.`, 'Ses certifications : ' + CERTIFS.slice(1, 6).join(', ') + '.'], lien: '#apropos' }),
  },
  {
    id: 'gouvernance',
    mots: ['rgpd', 'rgdp', 'ia act', 'ai act', 'conformite', 'audit', 'gouvernance', 'cnil', 'donnees personnelles', 'registre', 'dpo'],
    rep: () => ({
      texte: [
        'Nous accompagnons les entreprises sur le RGPD et l’IA Act : inventaire des usages d’IA, registre des traitements, charte d’usage, transparence.',
        'Pas de « mise en conformité » miracle : nous vous aidons à prouver les mesures prises. La formation CONTRÔLE TECHNIQUE couvre l’essentiel en une journée.',
      ],
      suggestions: ['Contrôle technique', 'Être rappelé'],
    }),
  },
  {
    id: 'solutions',
    mots: ['automatis', 'workflow', 'n8n', 'site internet', 'site web', 'application', 'base de donnees', 'agent', 'solution', 'outil', 'implement', 'chatbot', 'assistant'],
    rep: () => ({
      texte: [
        'Au-delà des formations, nous construisons avec vous des workflows automatisés, des assistants, des sites et des bases de données, en privilégiant des outils européens.',
        'Décrivez-moi la tâche qui vous prend le plus de temps : Aurélien regarde avec vous ce qui peut être automatisé.',
      ],
      suggestions: ['Être rappelé', 'Faire le diagnostic'],
    }),
  },
  { id: 'diagnostic', mots: ['diagnostic', 'par ou commencer', 'conseil', 'quelle formation', 'recommand', 'hesite', 'choisir'], rep: () => ({ texte: ['Le diagnostic IA express tient en 6 questions et vous conseille 3 formations. Je vous y emmène ?'], action: 'diagnostic' }) },
  {
    id: 'catalogue',
    mots: ['formation', 'catalogue', 'liste', 'proposez', 'offre', 'thematique', 'programme'],
    rep: () => ({
      texte: ['Voici notre catalogue :', ...FORMATIONS.map((f) => `• ${f.nom} — ${f.sousTitre} (${f.jours} j)`), 'Laquelle voulez-vous découvrir ?'],
      suggestions: ['Allumage-Turbo', 'Contrôle technique', 'Tableau de bord', 'Être rappelé'],
    }),
  },
  { id: 'attestation', mots: ['attestation', 'certificat', 'diplome', 'a la fin', 'rncp'], rep: () => ({ texte: [faq('Qu’est-ce que je reçois')] }) },
  { id: 'securite', mots: ['securite', 'confidentiel', 'mes donnees', 'vie privee'], rep: () => ({ texte: [faq('Nos données sont-elles'), 'Le détail est dans notre politique de confidentialité, en bas de page.'] }) },
]

/* ---------- Petites conversations (le côté humain) ---------- */
const BAVARDAGES = [
  { mots: ['ca va', 'comment vas tu', 'comment allez vous', 'la forme', 'bien ou quoi', 'koman i lé', 'koman i le'], rep: (ton) => [ton.tutoie ? 'Ça va très bien, merci de demander ! Et toi ? Dis-moi ce qui t’amène 😊' : 'Très bien, merci de demander ! Et vous ? Dites-moi ce qui vous amène 😊'] },
  { mots: ['merci', 'super', 'parfait', 'genial', 'top', 'nickel', 'cool'], rep: (ton) => [ton.tutoie ? 'Avec plaisir ! Je reste là si tu as une autre question.' : 'Avec plaisir ! Je reste là si vous avez une autre question.'] },
  { mots: ['au revoir', 'bye', 'a plus', 'a bientot', 'bonne journee', 'bonne soiree', 'ciao'], rep: () => ['À très vite ! Et si une question vous revient, je suis là 👋'] },
  { mots: ['jolie', 'belle', 'mignonne', 'charmante'], rep: () => ['Merci, c’est gentil 😊 Mais revenons à l’essentiel : comment puis-je vous aider ?'] },
  { mots: ['blague', 'drole', 'rigoler'], rep: () => ['Une IA entre dans une salle de formation. Le formateur lui dit : « Tu as tout appris par cœur, mais as-tu compris ? » Elle répond : « Donnez-moi un prompt et je vous dis. » 😄 C’est pour ça qu’on forme les humains !'] },
  { mots: ['mdr', 'lol', 'haha', 'ptdr'], rep: () => ['😄 Je suis contente de vous faire sourire. Une question sur nos formations ?'] },
]
const GROSSIERETES = ['connard', 'connasse', 'pute', 'salope', 'encule', 'nique', 'fdp', 'ta gueule', 'batard', 'idiote', 'nulle']

function salutation(ton, ctx) {
  if (!ton.salut || ctx.salue) return null
  if (ton.salut === 'formel') return ton.motSalut === 'bonsoir' ? 'Bonsoir !' : 'Bonjour !'
  if (ton.salut === 'detendu') return ton.motSalut === 'bonsoir' ? 'bonsoir 😊' : 'bonjour 😊'
  return `${ton.motSalut === 'coucou' ? 'Coucou' : 'Salut'} ! 😊`
}

/**
 * Transforme une question en réponse.
 * @param {string} question  texte brut du visiteur
 * @param {object} ctx       mémoire de la conversation (modifiée ici) : derniereFormation, salue, politesseNotee, tutoie
 */
export function repondre(question, ctx = {}) {
  const brut = String(question).slice(0, 500)
  const t = normaliser(brut)
  const mots = t.split(' ')
  const ton = analyserTon(brut)
  if (ton.tutoie) ctx.tutoie = true
  const avant = []
  const s = salutation(ton, ctx)
  if (s) {
    avant.push(s)
    ctx.salue = true
  }
  if (ton.salut === 'familier' || ton.salut === 'detendu') ctx.familier = true
  const detendu = { ...ton, tutoie: ton.tutoie || ctx.tutoie || ctx.familier }
  if (ton.politesse && !ctx.politesseNotee) {
    avant.push('Ooh, merci de mettre les formes avec moi ! 🌺')
    ctx.politesseNotee = true
  }
  const avec = (rep) => {
    if (rep.formation) ctx.derniereFormation = rep.formation.ref
    const { formation, ...reste } = rep
    return { ...reste, texte: [...avant, ...reste.texte] }
  }

  if (GROSSIERETES.some((g) => mots.includes(g) || t.includes(g + ' '))) {
    return { texte: ['Je comprends que quelque chose vous agace, et je suis là pour aider. Restons courtois, et dites-moi ce qui ne va pas : je transmets à Aurélien.'], suggestions: ['Être rappelé'] }
  }

  if (DEMANDES_PAYANTES.some((d) => t.includes(d)) && !/devis|rappel|inscri/.test(t)) {
    return avec({
      texte: [
        'Bonne question… et c’est justement ce qu’on construit ensemble en formation ou en accompagnement 😉',
        'Je ne peux pas le livrer ici : chaque outil est adapté à votre entreprise et à vos données, sinon il ne vaut pas grand-chose.',
        'Je vous propose la formation qui y répond, ou un échange avec Aurélien pour cadrer votre besoin.',
      ],
      suggestions: ['Faire le diagnostic', 'Être rappelé', 'Voir les formations'],
    })
  }

  const f = trouverFormation(t, mots)
  const trouvees = INTENTIONS.filter((i) => i.mots.some((m) => contient(t, mots, m)))
  const intention = trouvees[0]

  // Suivi sur la formation en cours de discussion (« et le prix ? », « c'est pour qui ? »)
  const cible = f || FORMATIONS.find((x) => x.ref === ctx.derniereFormation)
  const suivi = cible && SUIVIS.find((sv) => sv.mots.some((m) => contient(t, mots, m)))
  if (suivi && (f || mots.length <= 7) && !['rappel', 'financement', 'cpf', 'dates'].includes(intention?.id)) {
    return avec({ texte: suivi.rep(cible), suggestions: ['Le financement', 'Être rappelé'], lien: '#formations', formation: cible })
  }
  if (f && (!intention || !['prix', 'rappel'].includes(intention.id))) {
    return avec({ texte: ficheCourte(f), suggestions: ['C’est pour qui ?', 'Le programme', 'Être rappelé'], lien: '#formations', formation: f })
  }
  if (intention) return avec(intention.rep(t, ton, mots))

  const bavardage = BAVARDAGES.find((b) => b.mots.some((m) => contient(t, mots, m)))
  if (bavardage) return avec({ texte: bavardage.rep(detendu), suggestions: SUGGESTIONS_ACCUEIL })
  if (avant.length) {
    return {
      texte: [...avant, detendu.tutoie ? 'Qu’est-ce qui t’amène ? Formations, tarifs, financement… je t’écoute !' : 'Que puis-je faire pour vous aujourd’hui ?'],
      suggestions: SUGGESTIONS_ACCUEIL,
    }
  }

  // Rien trouvé : on propose ce qu'on a cru comprendre plutôt que de répondre au hasard.
  const proches = FORMATIONS.map((x) => ({ x, d: Math.min(...motsFormation(x).map((c) => Math.min(...mots.map((m) => (m.length > 3 ? distance(m, c, 3) : 9))))) }))
    .filter((p) => p.d <= 3)
    .sort((a, b) => a.d - b.d)
  if (proches.length) {
    return { texte: ['Je ne suis pas sûre d’avoir compris. Vous parlez peut-être de :'], suggestions: [...proches.slice(0, 3).map((p) => p.x.nom), 'Être rappelé'] }
  }
  return {
    texte: [
      'Je ne suis pas sûre de bien comprendre, et je préfère ne pas vous répondre au hasard.',
      `Essayez avec d’autres mots (tarif, financement, dates, handicap…), ou Aurélien vous répond directement : ${ENTREPRISE.telAffiche}.`,
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

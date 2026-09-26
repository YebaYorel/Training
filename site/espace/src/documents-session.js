// Documents générés à partir des VRAIES données d'une session (Parcours) : rien à ressaisir.
import { v } from './word.js'
import { dateCourte } from './modele.js'

const joursEntre = (debut, fin) => {
  const r = []
  for (let d = new Date(debut + 'T12:00:00'); d.toISOString().slice(0, 10) <= (fin || debut); d.setDate(d.getDate() + 1)) r.push(d.toISOString().slice(0, 10))
  return r
}
export const heuresRealisees = (donnees, ins, s, f) => {
  const demi = f?.jours ? Number(f.heures) / Number(f.jours) / 2 : 0
  return donnees.presences.filter((p) => p.inscription === ins.id).reduce((a, p) => a + (p.matin ? demi : 0) + (p.apresMidi ? demi : 0), 0)
}

function contexte(donnees, ins) {
  const s = donnees.sessions.find((x) => x.id === ins.session) || {}
  const f = donnees.formations.find((x) => x.id === s.formation) || {}
  const a = donnees.apprenants.find((x) => x.id === ins.apprenant) || {}
  const ent = donnees.clients.find((x) => x.id === a.entreprise) || {}
  const formateur = donnees.formateurs.find((x) => x.id === s.formateur) || {}
  return { s, f, a, ent, formateur, o: donnees.organisme }
}
const periode = (s) => (s.debut === s.fin || !s.fin ? `le ${dateCourte(s.debut)}` : `du ${dateCourte(s.debut)} au ${dateCourte(s.fin)}`)

export const DOCS_STAGIAIRE = {
  convocation: {
    titre: 'Convocation',
    blocs: (donnees, ins) => {
      const { s, f, a, formateur, o } = contexte(donnees, ins)
      return [
        { h1: 'Convocation à la formation' },
        { p: `Bonjour ${v(a.nom, 'stagiaire')},` },
        { p: `Nous avons le plaisir de vous confirmer votre inscription à la formation « ${v(f.intitule, 'formation')} », qui se déroulera ${periode(s)}.` },
        { table: { entetes: ['', ''], lignes: [['Horaires', v(s.horaires || o.horaires, 'horaires')], ['Lieu', v(s.lieu, 'lieu')], ['Durée', `${v(f.heures, 'heures')} heures`], ['Formateur', v(formateur.nom, 'formateur')]], largeurs: [30, 70] } },
        a.amenagement ? { encadre: `Aménagements convenus : ${v(a.amenagementsConvenus, 'aménagements')}` } : { p: `Un besoin d’aménagement ? Contactez ${v(o.referentHandicap, 'le référent handicap')} : ${v(o.email, 'email')} — ${v(o.tel, 'téléphone')}.` },
        { p: 'Documents joints : programme, règlement intérieur, livret d’accueil, information sur vos données personnelles.' },
        { p: `En cas d’empêchement, merci de nous prévenir au plus vite : ${v(o.email, 'email')} — ${v(o.tel, 'téléphone')}.` },
        { p: 'À très bientôt,' },
        { p: v(o.dirigeant, 'signataire') },
      ]
    },
  },
  attestation: {
    titre: 'Attestation de fin de formation',
    blocs: (donnees, ins) => {
      const { s, f, a, ent, o } = contexte(donnees, ins)
      const evalFin = donnees.evaluations.find((e) => e.inscription === ins.id && e.type === 'Evaluation finale')
      return [
        { h1: 'Attestation de fin de formation' },
        { petit: 'Article L.6353-1 du code du travail.' },
        { p: `Je soussigné(e), ${v(o.dirigeant, 'dirigeant')}, représentant ${v(o.nom, 'l’organisme')}, atteste que ${v(a.nom, 'stagiaire')}${ent.nom ? `, salarié(e) de ${ent.nom},` : ''} a suivi la formation « ${v(f.intitule, 'formation')} » (action de formation, art. L.6313-1), ${periode(s)}, pour une durée de ${Math.round(heuresRealisees(donnees, ins, s, f) * 100) / 100} heures sur ${v(f.heures, 'heures')} heures prévues.` },
        { h2: 'Objectifs' },
        ...(f.objectifs ? f.objectifs.split('\n').filter(Boolean).map((x) => ({ li: x })) : [{ p: '[À COMPLÉTER : objectifs]' }]),
        { h2: 'Résultats de l’évaluation des acquis' },
        { p: evalFin ? `${evalFin.resultat || 'Évalué'}${evalFin.score != null ? ` — ${evalFin.score}/${evalFin.max || 20}` : ''}.` : '[À COMPLÉTER : résultat de l’évaluation des acquis]' },
        { p: `Fait à ${v(o.ville, 'ville')}, le ${new Date().toLocaleDateString('fr-FR')}.` },
        { signatures: ['Pour l’organisme (cachet)'] },
      ]
    },
  },
  certificat: {
    titre: 'Certificat de réalisation',
    blocs: (donnees, ins) => {
      const { s, f, a, ent, o } = contexte(donnees, ins)
      return [
        { h1: 'Certificat de réalisation' },
        { p: `Je soussigné(e), ${v(o.dirigeant, 'dirigeant')}, représentant légal du dispensateur de l’action ${v(o.nom, 'l’organisme')}, atteste que ${v(a.nom, 'bénéficiaire')}${ent.nom ? `, salarié(e) de l’entreprise ${ent.nom},` : ''} a suivi l’action « ${v(f.intitule, 'formation')} » (nature : action de formation), ${periode(s)}, pour une durée réalisée de ${Math.round(heuresRealisees(donnees, ins, s, f) * 100) / 100} heures.` },
        ins.numeroDossier ? { p: `Référence du dossier de prise en charge : ${ins.numeroDossier}.` } : null,
        { p: 'Assiduité justifiée par les feuilles d’émargement signées par demi-journée, tenues à disposition du financeur.' },
        { p: `Fait à ${v(o.ville, 'ville')}, le ${new Date().toLocaleDateString('fr-FR')}.` },
        { signatures: ['Le dispensateur (cachet et signature)'] },
        { petit: 'Vérifiez si votre financeur impose son propre modèle.' },
      ]
    },
  },
}

export function emargementSession(donnees, s) {
  const f = donnees.formations.find((x) => x.id === s.formation) || {}
  const formateur = donnees.formateurs.find((x) => x.id === s.formateur) || {}
  const inscrits = donnees.inscriptions.filter((i) => i.session === s.id && !['Annulé'].includes(i.statut))
  const jours = joursEntre(s.debut, s.fin)
  // Une page par groupe de 2 jours pour garder des cases de signature lisibles
  const blocs = []
  for (let k = 0; k < jours.length; k += 2) {
    const js = jours.slice(k, k + 2)
    const entetes = ['Stagiaire', ...js.flatMap((j) => [`${dateCourte(j)}\nmatin`, `${dateCourte(j)}\naprès-midi`])]
    if (k) blocs.push({ saut: true })
    blocs.push(
      { h1: 'Feuille d’émargement' },
      { p: `${v(f.intitule, 'formation')} — ${s.lieu || ''} — ${s.horaires || donnees.organisme.horaires || ''}` },
      { table: { entetes, lignes: inscrits.map((i) => [donnees.apprenants.find((a) => a.id === i.apprenant)?.nom || '', ...js.flatMap(() => ['', ''])]), largeurs: [28, ...js.flatMap(() => [18, 18])] } },
      { table: { entetes: ['Formateur', ...js.flatMap(() => ['matin', 'après-midi'])], lignes: [[formateur.nom || '', ...js.flatMap(() => ['', ''])]], largeurs: [28, ...js.flatMap(() => [18, 18])] } },
    )
  }
  return blocs
}

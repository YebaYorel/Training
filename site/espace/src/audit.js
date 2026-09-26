// « Audit blanc » : preuves que YEBA Studio détecte automatiquement dans les données de l'organisme.
// Aide à la préparation : c'est l'auditeur qui apprécie la conformité.
const taux = (liste, test) => (liste.length ? Math.round((liste.filter(test).length / liste.length) * 100) : null)

export function preuvesAuto(d) {
  if (!d?.inscriptions) return {}
  const o = d.organisme || {}
  const auj = new Date().toISOString().slice(0, 10)
  const terminees = new Set(d.sessions.filter((s) => s.statut === 'Terminée' || (s.fin && s.fin < auj)).map((s) => s.id))
  const insT = d.inscriptions.filter((i) => terminees.has(i.session))
  const p = (liste, cle) => taux(liste, (i) => i.pieces?.[cle])
  const f = d.formations
  const r = {}
  const ajoute = (n, ok, texte) => (r[n] = { ok, texte })
  ajoute(1, f.length > 0 && f.every((x) => x.objectifs && x.prerequis && x.prix), f.length ? `${f.filter((x) => x.objectifs && x.prerequis && x.prix).length}/${f.length} formation(s) avec objectifs, prérequis et prix renseignés.` : 'Aucune formation saisie.')
  ajoute(4, (taux(d.inscriptions, (i) => i.pieces?.positionnement) ?? 0) >= 90, `Analyse du besoin / positionnement tracé pour ${p(d.inscriptions, 'positionnement') ?? 0} % des inscriptions.`)
  ajoute(5, f.length > 0 && f.every((x) => x.objectifs), `${f.filter((x) => x.objectifs).length}/${f.length} formation(s) avec objectifs opérationnels.`)
  ajoute(8, (p(d.inscriptions, 'positionnement') ?? 0) >= 90, `Positionnement à l’entrée : ${p(d.inscriptions, 'positionnement') ?? 0} % des stagiaires.`)
  ajoute(9, (p(d.inscriptions, 'convocation') ?? 0) >= 90 && (p(d.inscriptions, 'reglement') ?? 0) >= 90, `Convocations : ${p(d.inscriptions, 'convocation') ?? 0} % · règlement intérieur signé : ${p(d.inscriptions, 'reglement') ?? 0} %.`)
  ajoute(11, insT.length > 0 && (p(insT, 'attestation') ?? 0) >= 95, insT.length ? `Attestations / certificats émis : ${p(insT, 'attestation')} % des stagiaires des sessions terminées ; évaluations finales : ${taux(insT, (i) => d.evaluations.some((e) => e.inscription === i.id && e.type === 'Evaluation finale'))} %.` : 'Aucune session terminée.')
  ajoute(21, d.formateurs.length > 0, `${d.formateurs.length} intervenant(s) référencé(s).`)
  ajoute(26, !!o.referentHandicap, o.referentHandicap ? `Référent handicap désigné : ${o.referentHandicap}.` : 'Référent handicap non renseigné dans la fiche organisme.')
  ajoute(30, insT.length > 0 && (p(insT, 'evalChaud') ?? 0) >= 80, insT.length ? `Satisfaction à chaud : ${p(insT, 'evalChaud')} % · à froid : ${p(insT, 'evalFroid')} %.` : 'Aucune session terminée.')
  ajoute(31, false, 'Tenez le registre des réclamations (modèle « Procédure de traitement des réclamations »).')
  return r
}

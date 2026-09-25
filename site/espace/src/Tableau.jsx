// Tableau de bord — lecture en F : les chiffres clés en ligne, puis la colonne « À traiter » à gauche.
import { useMemo } from 'react'
import { AlertTriangle, ArrowRight, CalendarDays, CircleCheck, Info } from 'lucide-react'
import { Jauge, Kpi, dateFr, euros, useIndex } from './ui.jsx'

const AUJOURDHUI = () => new Date().toISOString().slice(0, 10)
const plusJours = (d, n) => {
  const x = new Date(d)
  x.setDate(x.getDate() + n)
  return x.toISOString().slice(0, 10)
}

export function preparationQualiopi(indicateurs) {
  const applicables = indicateurs.filter((i) => !i.statut.includes('Non applicable'))
  const conformes = applicables.filter((i) => i.statut.includes('Conforme') && !i.statut.includes('Non conforme'))
  return { applicables: applicables.length, conformes: conformes.length, taux: applicables.length ? (conformes.length / applicables.length) * 100 : 0 }
}

export function listeAlertes(db, index) {
  const auj = AUJOURDHUI()
  const a = []
  for (const s of db.sessions) {
    const inscrits = (index.inscritsPar[s.id] || []).filter((i) => !['Annulé', 'Refusé'].includes(i.statut))
    if (s.statut === 'Terminée' || (s.fin && s.fin < auj && s.statut !== 'Annulée')) {
      const sansEmarg = inscrits.filter((i) => !db.presences.some((p) => p.inscription === i.id))
      if (sansEmarg.length) a.push({ niveau: 'bloquant', module: 'parcours', texte: `${sansEmarg.length} stagiaire(s) sans émargement — ${s.nom}`, aide: 'Sans émargement : ni heures au BPF, ni paiement du financeur.' })
      if (s.fin <= plusJours(auj, -30)) {
        const froid = inscrits.filter((i) => !i.pieces.evalFroid)
        if (froid.length) a.push({ niveau: 'alerte', module: 'parcours', texte: `Évaluation à froid à envoyer (${froid.length}) — ${s.nom}`, aide: 'Indicateur 30 : recueil des appréciations.' })
      }
      const attest = inscrits.filter((i) => !i.pieces.attestation)
      if (attest.length) a.push({ niveau: 'alerte', module: 'parcours', texte: `Attestation de fin à remettre (${attest.length}) — ${s.nom}`, aide: 'Obligatoire : art. L.6353-1 du code du travail.' })
    } else if (s.debut && s.debut <= plusJours(auj, 15) && s.debut >= auj) {
      const manque = inscrits.filter((i) => !i.pieces.convention || !i.pieces.convocation || !i.pieces.reglement)
      if (manque.length) a.push({ niveau: 'alerte', module: 'parcours', texte: `Dossiers incomplets avant démarrage (${manque.length}) — ${s.nom}`, aide: 'Convention, convocation et règlement intérieur avant l’entrée en formation.' })
    }
  }
  for (const i of db.indicateurs.filter((x) => x.statut.includes('Non conforme'))) {
    a.push({ niveau: 'bloquant', module: 'coffre', texte: `Indicateur ${i.n} non conforme`, aide: i.libelle.slice(0, 110) + (i.libelle.length > 110 ? '…' : '') })
  }
  for (const f of db.factures.filter((x) => x.type === 'Facture' && ['Envoyé', 'Impayé', 'Partiellement payé'].includes(x.statut))) {
    if (f.date && f.date <= plusJours(auj, -30)) a.push({ niveau: 'info', module: 'bpf', texte: `Facture ${f.ref} non soldée depuis plus de 30 jours`, aide: euros(f.montantHT - (f.encaisse || 0)) + ' restant dû.' })
  }
  const ordre = { bloquant: 0, alerte: 1, info: 2 }
  return a.sort((x, y) => ordre[x.niveau] - ordre[y.niveau])
}

const ICONES = { bloquant: AlertTriangle, alerte: AlertTriangle, info: Info }

export default function Tableau({ db, aller }) {
  const index = useIndex(db)
  const q = preparationQualiopi(db.indicateurs)
  const alertes = useMemo(() => listeAlertes(db, index), [db, index])
  const auj = AUJOURDHUI()
  const exercice = Number(auj.slice(0, 4))
  const avenir = db.sessions.filter((s) => s.debut >= auj && !['Annulée', 'Reportée'].includes(s.statut)).sort((a, b) => a.debut.localeCompare(b.debut))
  const pieces = db.inscriptions.flatMap((i) => Object.values(i.pieces))
  const tauxDossiers = pieces.length ? (pieces.filter(Boolean).length / pieces.length) * 100 : 0
  const ca = db.factures.filter((f) => f.type === 'Facture' && f.date?.startsWith(String(exercice))).reduce((s, f) => s + f.montantHT, 0)
  const jBpf = Math.ceil((new Date(`${exercice + 1}-05-31`) - new Date(auj)) / 86400000)

  return (
    <div className="tableau">
      <h1>Bonjour Aurélien 👋</h1>
      <p className="chapo">
        {alertes.filter((x) => x.niveau === 'bloquant').length
          ? `${alertes.filter((x) => x.niveau === 'bloquant').length} point(s) bloquant(s) à traiter en priorité.`
          : 'Aucun point bloquant. Belle maîtrise !'}
      </p>

      <div className="kpis">
        <Kpi valeur={`${q.conformes}/${q.applicables}`} libelle="Indicateurs Qualiopi conformes" ton={q.taux >= 80 ? 'ok' : 'attention'} sous={<Jauge valeur={q.taux} libelle="Préparation Qualiopi" />} />
        <Kpi valeur={avenir.length} libelle="Sessions à venir" sous={avenir[0] ? `Prochaine : ${dateFr(avenir[0].debut)}` : 'Aucune planifiée'} />
        <Kpi valeur={`${Math.round(tauxDossiers)} %`} libelle="Pièces des dossiers stagiaires" ton={tauxDossiers >= 90 ? 'ok' : 'attention'} />
        <Kpi valeur={euros(ca)} libelle={`Facturé en ${exercice} (HT)`} />
        <Kpi valeur={`J-${jBpf}`} libelle={`BPF ${exercice} à déclarer`} sous={`avant le 31/05/${exercice + 1}`} ton={jBpf < 45 ? 'attention' : ''} />
      </div>

      <div className="colonnes-f">
        <section className="carte" aria-labelledby="t-alertes">
          <h2 id="t-alertes">À traiter maintenant</h2>
          {alertes.length === 0 ? (
            <p className="vide"><CircleCheck aria-hidden="true" /> Tout est à jour.</p>
          ) : (
            <ul className="alertes">
              {alertes.slice(0, 12).map((x, k) => {
                const I = ICONES[x.niveau]
                return (
                  <li key={k} className={'alerte niv-' + x.niveau}>
                    <I size={20} aria-hidden="true" />
                    <div>
                      <strong>{x.texte}</strong>
                      <span>{x.aide}</span>
                    </div>
                    <button className="bouton-icone" onClick={() => aller(x.module)} aria-label={'Ouvrir : ' + x.texte}>
                      <ArrowRight size={18} aria-hidden="true" />
                    </button>
                  </li>
                )
              })}
            </ul>
          )}
        </section>

        <section className="carte" aria-labelledby="t-sessions">
          <h2 id="t-sessions">Prochaines sessions</h2>
          <ol className="frise">
            {avenir.slice(0, 6).map((s) => {
              const n = (index.inscritsPar[s.id] || []).length
              return (
                <li key={s.id}>
                  <span className="frise-date">
                    <CalendarDays size={16} aria-hidden="true" /> {dateFr(s.debut)}
                  </span>
                  <strong>{s.formation}</strong>
                  <span>{s.type} · {s.lieu}</span>
                  <span className="frise-places">{n}{s.places ? ` / ${s.places}` : ''} inscrit(s) · {s.statut}</span>
                </li>
              )
            })}
            {!avenir.length && <li>Aucune session à venir.</li>}
          </ol>
        </section>
      </div>
    </div>
  )
}

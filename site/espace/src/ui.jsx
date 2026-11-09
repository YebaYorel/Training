import { useMemo } from 'react'
import { motion } from 'framer-motion'

/* ---------- Petits composants partagés ---------- */
export function Kpi({ valeur, libelle, ton = '', sous }) {
  return (
    <div className={'kpi ' + ton}>
      <strong>{valeur}</strong>
      <span>{libelle}</span>
      {sous && <small>{sous}</small>}
    </div>
  )
}

export function Jauge({ valeur, libelle }) {
  const v = Math.max(0, Math.min(100, Math.round(valeur)))
  return (
    <div className="jauge-ligne" role="img" aria-label={`${libelle} : ${v} %`}>
      <div className="jauge-piste">
        <motion.div className="jauge-rempli" initial={{ width: 0 }} animate={{ width: v + '%' }} transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }} />
      </div>
      <span>{v} %</span>
    </div>
  )
}

export const dateFr = (d) => (d ? new Date(d).toLocaleDateString('fr-FR') : '—')
export const euros = (n) => (n || 0).toLocaleString('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

/** Téléchargement local d'un fichier généré (aucun envoi réseau). */
export function telecharger(nom, contenu, type = 'text/csv;charset=utf-8') {
  const url = URL.createObjectURL(new Blob([contenu], { type }))
  const a = Object.assign(document.createElement('a'), { href: url, download: nom })
  document.body.append(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function useIndex(db) {
  return useMemo(() => {
    const sessions = Object.fromEntries(db.sessions.map((s) => [s.id, s]))
    const inscritsPar = {}
    for (const i of db.inscriptions) (inscritsPar[i.session] ||= []).push(i)
    return { sessions, inscritsPar }
  }, [db])
}

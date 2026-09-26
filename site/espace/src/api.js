// Liaison avec le serveur YEBA Studio (paiement Mollie, licences, IA Mistral).
// Sans serveur configuré (VITE_STUDIO_API vide), le logiciel fonctionne quand même : achat par e-mail,
// licence collée à la main, et modèles de textes à la place de l'IA générative.
export const API = (import.meta.env?.VITE_STUDIO_API || '').replace(/\/$/, '')

async function appel(chemin, options = {}) {
  if (!API) throw new Error('Serveur YEBA Studio non configuré.')
  const r = await fetch(API + chemin, { ...options, headers: { 'Content-Type': 'application/json' }, credentials: 'omit' })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(j.erreur || `Erreur ${r.status}`)
  return j
}

let santeCache
export function sante() {
  if (!API) return Promise.resolve({ ok: false })
  santeCache ||= appel('/api/sante').catch(() => ({ ok: false }))
  return santeCache
}
export const commander = (infos) => appel('/api/commande', { method: 'POST', body: JSON.stringify(infos) })
export const recupererLicence = (paiement) => appel('/api/licence?paiement=' + encodeURIComponent(paiement))
export const demanderIa = ({ tache, contenu, licence, poste }) => appel('/api/ia', { method: 'POST', body: JSON.stringify({ tache, contenu, licence, poste }) })

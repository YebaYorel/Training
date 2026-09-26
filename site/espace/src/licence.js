// Licences YEBA Studio — signées (Ed25519), liées à UN poste, vérifiées hors ligne.
// Principe : YEBA FORMATIONS signe { offre, titulaire, poste, dates } avec sa clé privée (jamais publiée) ;
// le logiciel vérifie la signature avec la clé publique ci-dessous. Une licence copiée sur un autre PC
// est refusée (code poste différent) ; une licence modifiée est refusée (signature invalide).
// Fonctionne dans le navigateur ET dans Node (scripts, serveur) : WebCrypto uniquement.
import CLE from './licence-cle.json' with { type: 'json' }

export const OFFRES = {
  qualiopi: { nom: 'Pack Qualiopi V10', modules: ['coffre', 'modeles'], prix: 300, jours: 0, libellePrix: '300 € — achat unique' },
  bpf: { nom: 'BPF Facile', modules: ['donnees', 'bpf'], prix: 100, jours: 365, libellePrix: '100 € / an / utilisateur' },
  parcours: { nom: 'Parcours', modules: ['donnees', 'parcours', 'bpf'], prix: 89, jours: 31, libellePrix: '89 € / mois' },
  carburant: { nom: 'CARBURANT', modules: ['donnees', 'carburant'], prix: 49, jours: 31, libellePrix: '49 € / mois — offre pionniers', premierMois: 1 },
  studio: { nom: 'YEBA Studio complet', modules: ['coffre', 'modeles', 'donnees', 'parcours', 'bpf', 'carburant'], prix: 129, jours: 31, libellePrix: '129 € / mois — tout inclus' },
}
export const GRACE_JOURS = 7 // délai après échéance pour renouveler sans rien perdre

const b64u = {
  de: (octets) => btoa(String.fromCharCode(...new Uint8Array(octets))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''),
  vers: (texte) => Uint8Array.from(atob(texte.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((texte.length + 3) % 4)), (c) => c.charCodeAt(0)),
}
const enc = new TextEncoder()
const dec = new TextDecoder()

let clePublique
async function cle() {
  clePublique ||= crypto.subtle.importKey('raw', b64u.vers(CLE.publique), { name: 'Ed25519' }, false, ['verify'])
  return clePublique
}

/** Signe une licence (côté YEBA uniquement : script ou serveur). `clePrivee` = CryptoKey Ed25519. */
export async function signer(charge, clePrivee) {
  const octets = enc.encode(JSON.stringify({ v: 1, ...charge }))
  const sig = await crypto.subtle.sign({ name: 'Ed25519' }, clePrivee, octets)
  return `YEBA1.${b64u.de(octets)}.${b64u.de(sig)}`
}

/**
 * Vérifie une licence pour ce poste. Renvoie { ok, charge, raison, expireBientot }.
 * `maintenant` injectable pour les tests.
 */
export async function verifier(code, poste, maintenant = new Date()) {
  try {
    const [pref, charge64, sig64] = String(code || '').trim().split('.')
    if (pref !== 'YEBA1' || !charge64 || !sig64) return { ok: false, raison: 'Format de licence inconnu.' }
    const octets = b64u.vers(charge64)
    const valide = await crypto.subtle.verify({ name: 'Ed25519' }, await cle(), b64u.vers(sig64), octets)
    if (!valide) return { ok: false, raison: 'Signature invalide : cette licence n’a pas été émise par YEBA FORMATIONS.' }
    const charge = JSON.parse(dec.decode(octets))
    if (!OFFRES[charge.off]) return { ok: false, raison: 'Offre inconnue.' }
    if (charge.poste !== poste) return { ok: false, charge, raison: 'Cette licence appartient à un autre poste. Une licence = un utilisateur sur un PC.' }
    if (charge.fin) {
      const fin = new Date(charge.fin + 'T23:59:59+04:00')
      const graceFin = new Date(fin.getTime() + GRACE_JOURS * 86400000)
      if (maintenant > graceFin) return { ok: false, charge, raison: `Licence expirée le ${fin.toLocaleDateString('fr-FR')}.` }
      const jours = Math.ceil((fin - maintenant) / 86400000)
      return { ok: true, charge, jours, enGrace: maintenant > fin, expireBientot: jours <= 10 }
    }
    return { ok: true, charge }
  } catch {
    return { ok: false, raison: 'Licence illisible : vérifiez le copier-coller.' }
  }
}

/** Modules ouverts par un ensemble de licences valides. */
export function modulesOuverts(licencesValides) {
  return new Set(licencesValides.flatMap((l) => OFFRES[l.charge.off]?.modules ?? []))
}

/** Code poste lisible (ex. « K7QM-2XPA-9RTD ») : aléatoire, créé une fois par navigateur. */
export function nouveauCodePoste() {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const octets = crypto.getRandomValues(new Uint8Array(12))
  const c = [...octets].map((o) => alphabet[o % alphabet.length]).join('')
  return `${c.slice(0, 4)}-${c.slice(4, 8)}-${c.slice(8, 12)}`
}
export const CODE_POSTE_VALIDE = /^[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$/

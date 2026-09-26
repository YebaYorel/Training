// Coffre local chiffré de YEBA Studio.
// Les données de l'organisme (stagiaires, factures…) restent sur SON poste, chiffrées (AES-GCM 256).
// La clé des données est protégée deux fois : par le code personnel (PBKDF2, 600 000 itérations)
// et par une clé de secours affichée une seule fois à la création. YEBA FORMATIONS n'a accès à rien :
// elle n'est pas sous-traitant des données des stagiaires (RGPD art. 28 non applicable à ce stockage).
import { nouveauCodePoste } from './licence.js'

const BASE = 'yeba-studio'
const ITERATIONS = 600000
const enc = new TextEncoder()
const dec = new TextDecoder()
const b64 = {
  de: (o) => btoa(String.fromCharCode(...new Uint8Array(o))),
  vers: (t) => Uint8Array.from(atob(t), (c) => c.charCodeAt(0)),
}

/* ---------- IndexedDB (repli en mémoire si indisponible : navigation privée stricte) ---------- */
let memoire = null
function ouvrirBase() {
  return new Promise((ok, ko) => {
    if (!globalThis.indexedDB) return ko(new Error('IndexedDB indisponible'))
    const r = indexedDB.open(BASE, 1)
    r.onupgradeneeded = () => r.result.createObjectStore('kv')
    r.onsuccess = () => ok(r.result)
    r.onerror = () => ko(r.error)
  })
}
let basePromise
async function tx(mode, fn) {
  if (memoire) return fn(null)
  try {
    basePromise ||= ouvrirBase()
    const db = await basePromise
    return await new Promise((ok, ko) => {
      const t = db.transaction('kv', mode)
      const s = t.objectStore('kv')
      const r = fn(s)
      t.oncomplete = () => ok(r?.result)
      t.onerror = () => ko(t.error)
    })
  } catch {
    memoire = new Map()
    return fn(null)
  }
}
export async function lire(cle) {
  const v = await tx('readonly', (s) => (s ? s.get(cle) : null))
  return memoire ? memoire.get(cle) : v
}
export const ecrire = (cle, val) => tx('readwrite', (s) => (s ? s.put(val, cle) : memoire.set(cle, val)))
export const effacer = (cle) => tx('readwrite', (s) => (s ? s.delete(cle) : memoire.delete(cle)))
export const stockageEphemere = () => !!memoire

/** Code poste : créé une fois, recopié dans localStorage par sécurité (une licence y est attachée). */
export async function codePoste() {
  let c = await lire('poste')
  if (!c) {
    try {
      c = localStorage.getItem('yeba-studio-poste')
    } catch {
      /* navigation privée */
    }
  }
  if (!c) c = nouveauCodePoste()
  await ecrire('poste', c)
  try {
    localStorage.setItem('yeba-studio-poste', c)
  } catch {
    /* sans importance */
  }
  return c
}

/* ---------- Chiffrement ---------- */
async function deriver(secret, sel) {
  const base = await crypto.subtle.importKey('raw', enc.encode(secret), 'PBKDF2', false, ['deriveKey'])
  return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: sel, iterations: ITERATIONS, hash: 'SHA-256' }, base, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt'])
}
async function chiffrer(cle, octets) {
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, cle, octets)
  return { iv: b64.de(iv), ct: b64.de(ct) }
}
async function dechiffrer(cle, { iv, ct }) {
  return new Uint8Array(await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64.vers(iv) }, cle, b64.vers(ct)))
}
const importerCle = (brut) => crypto.subtle.importKey('raw', brut, { name: 'AES-GCM' }, false, ['encrypt', 'decrypt'])

function cleDeSecours() {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const o = crypto.getRandomValues(new Uint8Array(20))
  return [...o].map((x) => alphabet[x % 32]).join('').match(/.{4}/g).join('-')
}

export const etatCoffre = async () => ((await lire('coffre')) ? 'verrouille' : 'nouveau')

/** Crée le coffre. Renvoie { cle, secours } : la clé de secours doit être notée par l'utilisateur. */
export async function creerCoffre(pin, donneesInitiales) {
  const brut = crypto.getRandomValues(new Uint8Array(32))
  const secours = cleDeSecours()
  const sel = crypto.getRandomValues(new Uint8Array(16))
  const selSecours = crypto.getRandomValues(new Uint8Array(16))
  const coffre = {
    v: 1,
    sel: b64.de(sel),
    selSecours: b64.de(selSecours),
    parPin: await chiffrer(await deriver(pin, sel), brut),
    parSecours: await chiffrer(await deriver(secours.replace(/-/g, ''), selSecours), brut),
  }
  await ecrire('coffre', coffre)
  const cle = await importerCle(brut)
  await enregistrer(cle, donneesInitiales)
  return { cle, secours }
}

/** Ouvre le coffre avec le code personnel (ou la clé de secours). */
export async function ouvrirCoffre(secret, parSecours = false) {
  const c = await lire('coffre')
  if (!c) throw new Error('Aucun espace sur ce poste.')
  try {
    const kek = await deriver(parSecours ? secret.replace(/[-\s]/g, '').toUpperCase() : secret, b64.vers(parSecours ? c.selSecours : c.sel))
    const brut = await dechiffrer(kek, parSecours ? c.parSecours : c.parPin)
    return { cle: await importerCle(brut), brut }
  } catch {
    throw new Error(parSecours ? 'Clé de secours incorrecte.' : 'Code personnel incorrect.')
  }
}

/** Remplace le code personnel (après ouverture, ou avec la clé de secours). */
export async function changerPin(brut, nouveauPin) {
  const c = await lire('coffre')
  const sel = crypto.getRandomValues(new Uint8Array(16))
  c.sel = b64.de(sel)
  c.parPin = await chiffrer(await deriver(nouveauPin, sel), brut)
  await ecrire('coffre', c)
}

export async function charger(cle) {
  const d = await lire('donnees')
  if (!d) return null
  return JSON.parse(dec.decode(await dechiffrer(cle, d)))
}
export async function enregistrer(cle, donnees) {
  await ecrire('donnees', await chiffrer(cle, enc.encode(JSON.stringify(donnees))))
}

/* ---------- Sauvegarde portable (fichier chiffré avec un mot de passe choisi) ---------- */
export async function exporterSauvegarde(donnees, motDePasse) {
  const sel = crypto.getRandomValues(new Uint8Array(16))
  const bloc = await chiffrer(await deriver(motDePasse, sel), enc.encode(JSON.stringify(donnees)))
  return JSON.stringify({ format: 'yeba-studio-sauvegarde', v: 1, date: new Date().toISOString(), sel: b64.de(sel), ...bloc })
}
export async function importerSauvegarde(texte, motDePasse) {
  let f
  try {
    f = JSON.parse(texte)
  } catch {
    throw new Error('Fichier illisible.')
  }
  if (f.format !== 'yeba-studio-sauvegarde') throw new Error('Ce fichier n’est pas une sauvegarde YEBA Studio.')
  try {
    return JSON.parse(dec.decode(await dechiffrer(await deriver(motDePasse, b64.vers(f.sel)), f)))
  } catch {
    throw new Error('Mot de passe de sauvegarde incorrect.')
  }
}

/** Efface définitivement l'espace de ce poste (données + coffre). Les licences et le code poste sont conservés. */
export async function reinitialiser() {
  await effacer('donnees')
  await effacer('coffre')
}

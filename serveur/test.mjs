// Tests du serveur avec de faux Mollie et Mistral (aucun appel réseau réel). Lancer : node serveur/test.mjs
import { createServer } from 'node:http'
import assert from 'node:assert/strict'
import { readFileSync, existsSync } from 'node:fs'

if (existsSync('.env')) for (const l of readFileSync('.env', 'utf8').split('\n')) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2] }
const paiements = {}
const faux = createServer(async (req, res) => {
  let corps = ''; for await (const c of req) corps += c
  res.setHeader('Content-Type', 'application/json')
  if (req.url === '/v2/payments' && req.method === 'POST') {
    const b = JSON.parse(corps); const id = 'tr_TestPay' + Object.keys(paiements).length
    paiements[id] = { id, status: 'open', amount: b.amount, metadata: b.metadata }
    return res.end(JSON.stringify({ ...paiements[id], _links: { checkout: { href: 'https://mollie.test/checkout/' + id } } }))
  }
  const m = req.url.match(/^\/v2\/payments\/(tr_\w+)$/)
  if (m) return res.end(JSON.stringify(paiements[m[1]]))
  if (req.url === '/v1/chat/completions') {
    const b = JSON.parse(corps)
    const json = !!b.response_format
    return res.end(JSON.stringify({ choices: [{ message: { content: json ? '{"opco":"OPCO EP","montant_accorde_ht":1250,"heures":14}' : 'Objet : relance facture FAC-1' } }] }))
  }
  res.statusCode = 404; res.end('{}')
}).listen(0)
await new Promise((ok) => faux.on('listening', ok))
const base = `http://127.0.0.1:${faux.address().port}`
Object.assign(process.env, { MOLLIE_API: base, MISTRAL_API: base, MOLLIE_API_KEY: 'test_x', MISTRAL_API_KEY: 'x', ORIGINES: 'http://127.0.0.1:5180', PORT: '0' })
const { demarrer } = await import('./serveur.mjs')
const srv = await demarrer(0)
const S = `http://127.0.0.1:${srv.address().port}`
const O = { Origin: 'http://127.0.0.1:5180', 'Content-Type': 'application/json' }
const post = (p, b, h = O) => fetch(S + p, { method: 'POST', headers: h, body: JSON.stringify(b) }).then(async (r) => [r.status, await r.json()])
const get = (p, h = O) => fetch(S + p, { headers: h }).then(async (r) => [r.status, await r.json()])

let [c, j] = await get('/api/sante'); assert.equal(c, 200); assert.equal(j.offres.bpf.prix, 100); console.log('✓ santé')
;[c, j] = await get('/api/sante', { Origin: 'https://pirate.example' }); assert.equal(c, 403); console.log('✓ origine étrangère refusée')
const client = { offre: 'bpf', poste: 'K7QM-2XPA-9RTD', nom: 'Marie Test', email: 'marie@exemple.re', organisme: 'OF Exemple', siret: '12345678901234' }
;[c, j] = await post('/api/commande', { ...client, prix: 1 }); assert.equal(c, 200); assert.equal(paiements[j.paiement].amount.value, '100.00'); console.log('✓ commande : prix imposé par le serveur (le client ne peut pas le changer)')
const id = j.paiement
;[c, j] = await get('/api/licence?paiement=' + id); assert.equal(j.etat, 'open'); console.log('✓ pas de licence tant que non payé')
paiements[id].status = 'paid'; paiements[id].paidAt = '2026-09-26T08:00:00+00:00'
;[c, j] = await get('/api/licence?paiement=' + id); assert.ok(j.licence.startsWith('YEBA1.')); console.log('✓ licence délivrée après paiement')
const { verifier } = await import('../site/espace/src/licence.js')
assert.ok((await verifier(j.licence, client.poste)).ok); assert.ok(!(await verifier(j.licence, 'AAAA-BBBB-CCCC')).ok); console.log('✓ licence liée au poste')
;[c, j] = await post('/api/commande', { ...client, siret: 'abc' }); assert.equal(c, 400); console.log('✓ SIRET invalide refusé')
;[c, j] = await post('/api/commande', { ...client, offre: 'carburant' }); assert.equal(paiements[j.paiement].amount.value, '49.00'); console.log('✓ 1er mois à 1 € refusé sans registre (anti-abus)')
;[c, j] = await get('/api/licence?paiement=../../v2'); assert.equal(c, 400); console.log('✓ référence de paiement forgée refusée')
// IA : licence BPF → refus ; licence parcours → accepté
const bpfLic = (await get('/api/licence?paiement=' + id))[1].licence
;[c, j] = await post('/api/ia', { licence: bpfLic, poste: client.poste, tache: 'relance', contenu: 'Facture FAC-1 de 1250 € du 01/09' }); assert.equal(c, 403); console.log('✓ IA refusée pour une offre qui ne l’inclut pas')
;[c, j] = await post('/api/commande', { ...client, offre: 'parcours' }); paiements[j.paiement].status = 'paid'
const parcLic = (await get('/api/licence?paiement=' + j.paiement))[1].licence
;[c, j] = await post('/api/ia', { licence: parcLic, poste: client.poste, tache: 'accord', contenu: 'Accord OPCO EP dossier 42, 14 heures, 1250 € HT' }); assert.equal(j.donnees.montant_accorde_ht, 1250); console.log('✓ IA extraction JSON')
;[c, j] = await post('/api/ia', { licence: parcLic, poste: 'AAAA-BBBB-CCCC', tache: 'relance', contenu: 'xxxxxxxxxxxxxxx' }); assert.equal(c, 403); console.log('✓ IA refusée sur un autre poste')
;[c, j] = await post('/api/ia', { licence: parcLic, poste: client.poste, tache: 'pirater', contenu: 'xxxxxxxxxxxxxxx' }); assert.equal(c, 400); console.log('✓ tâche IA inconnue refusée')
const gros = await fetch(S + '/api/ia', { method: 'POST', headers: O, body: 'x'.repeat(30000) }); assert.equal(gros.status, 413); console.log('✓ requête trop volumineuse refusée')
srv.close(); faux.close(); console.log('Tous les tests passent.')

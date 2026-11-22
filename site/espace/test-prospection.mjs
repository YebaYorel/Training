// Tests des règles permanentes de prospection : node site/espace/test-prospection.mjs
import assert from 'node:assert/strict'
import {
  ADRESSE_INTERDITE, ETAT_VIDE, EXPEDITEUR, aPurger, controlesEnvoi, detecterStop, enregistrerOpposition, estOppose,
  lienGmail, proposition, redigerEmail, requeteBoamp, scoreAvis,
} from './src/prospection.js'

let n = 0
const test = (nom, f) => { f(); n++; console.log('ok -', nom) }
const etat = structuredClone(ETAT_VIDE)
const p = { id: '1', entreprise: 'Boulangerie Exemple (fictive)', metier: 'commerce', metierPrecis: 'boulangerie', email: 'contact@exemple.re', source: 'Site web de l’entreprise', statut: 'a_valider' }

test('règle 1 : le message parle du métier et propose STOP', () => {
  const m = redigerEmail(p)
  assert.match(m.corps, /boulangerie/)
  assert.match(m.corps, /Répondez simplement STOP/)
  assert.match(m.corps, /Site web de l’entreprise/)
})
test('règle 1 : pas de métier = pas de message', () => assert.throws(() => redigerEmail({ ...p, metier: '' })))
test('règle 1 : retirer l’accroche métier ou la phrase STOP bloque', () => {
  const m = redigerEmail(p)
  const sansStop = { ...m, corps: m.corps.replace(/Vous ne souhaitez plus[^\n]+/, '') }
  assert.ok(controlesEnvoi({ ...p, statut: 'valide' }, sansStop, etat).some((e) => e.includes('STOP')))
  const generique = { ...m, corps: 'Bonjour, découvrez nos formations. Répondez STOP pour ne plus recevoir.' }
  assert.ok(controlesEnvoi({ ...p, statut: 'valide', metierPrecis: '' }, generique, etat).some((e) => e.includes('métier')))
})
test('règle 2 : expéditeur de travail imposé, adresse personnelle refusée', () => {
  const m = redigerEmail(p)
  assert.ok(lienGmail(p, m).includes('authuser=' + encodeURIComponent(EXPEDITEUR)))
  assert.ok(!lienGmail(p, m).includes('aurelienlumeka'))
  assert.ok(controlesEnvoi({ ...p, statut: 'valide' }, m, { ...etat, expediteur: ADRESSE_INTERDITE }).some((e) => e.startsWith('Règle 2')))
})
test('règle 3 : sans validation d’Aurélien, rien ne part', () => {
  const m = redigerEmail(p)
  assert.ok(controlesEnvoi(p, m, etat).some((e) => e.startsWith('Règle 3')))
  assert.deepEqual(controlesEnvoi({ ...p, statut: 'valide' }, m, etat), [])
})
test('STOP / STP détectés, opposition bloquante (adresse et domaine)', () => {
  assert.ok(detecterStop('STOP merci'))
  assert.ok(detecterStop('stp'))
  assert.ok(detecterStop('Merci de ne plus m’écrire. STOP.'))
  assert.ok(!detecterStop('nous stoppons'))
  const e2 = enregistrerOpposition({ ...etat, prospects: [p] }, 'contact@exemple.re', { toutLeDomaine: true })
  assert.ok(estOppose('autre@exemple.re', e2))
  assert.equal(e2.prospects[0].statut, 'stop')
  assert.ok(controlesEnvoi({ ...p, statut: 'valide' }, redigerEmail(p), e2).some((e) => e.startsWith('STOP')))
  const e3 = enregistrerOpposition(etat, 'quelquun@gmail.com', { toutLeDomaine: true })
  assert.ok(!estOppose('autre@gmail.com', e3), 'jamais bloquer tout gmail.com')
})
test('RGPD : purge après 3 ans sans contact', () => {
  const vieux = { ...p, cree: '2022-01-01', dernierContact: '2022-06-01' }
  assert.equal(aPurger({ prospects: [vieux, p] }, new Date('2026-11-22')).length, 1)
})
test('veille : requête BOAMP et proposition (jamais une décision)', () => {
  assert.match(decodeURIComponent(requeteBoamp({ aujourdhui: new Date('2026-11-22') })), /code_departement="974"/)
  const a = { objet: 'Formation management et intelligence artificielle des agents', nature_libelle: 'Avis de marché', datelimitereponse: '2026-12-20T12:00:00Z', code_departement: ['974'], descripteur_libelle: ['Formation'] }
  const s = scoreAvis(a, new Date('2026-11-22'))
  assert.ok(s.ouvert && s.score >= 7)
  assert.match(proposition(a, new Date('2026-11-22')).texte, /^Proposition/)
  assert.equal(scoreAvis({ ...a, nature_libelle: 'Résultat de marché' }, new Date('2026-11-22')).ouvert, false)
})
console.log(`\n${n} tests réussis`)

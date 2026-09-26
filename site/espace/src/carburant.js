// CARBURANT — moteur de détection de l'argent « en jeu » d'un organisme de formation.
// Règles tirées des causes de rejet les plus fréquentes par les financeurs : dépôt tardif, émargements
// incomplets, certificat de réalisation absent, facture ≠ accord, facture jamais émise, relance oubliée.
// L'IA générative (Mistral, via le serveur) ne sert qu'à rédiger et à lire ; les montants viennent des données.

const FINANCEMENTS_TIERS = ['OPCO', 'France Travail', 'Région', 'Contrat Pro', 'CPF']
const auj = () => new Date().toISOString().slice(0, 10)
const jours = (a, b) => Math.round((new Date(b + 'T12:00:00') - new Date(a + 'T12:00:00')) / 86400000)

export function analyser(d, aujourdhui = auj()) {
  const alertes = []
  const formation = (s) => d.formations.find((f) => f.id === s.formation) || {}
  const nom = (id) => d.apprenants.find((a) => a.id === id)?.nom || 'Stagiaire'
  const client = (id) => d.clients.find((c) => c.id === id) || {}

  for (const s of d.sessions) {
    if (['Annulée', 'Reportée'].includes(s.statut)) continue
    const f = formation(s)
    const inscrits = d.inscriptions.filter((i) => i.session === s.id && !['Annulé', 'Refusé', 'En attente'].includes(i.statut))
    const terminee = s.statut === 'Terminée' || (s.fin && s.fin < aujourdhui)
    const nbJours = Number(f.jours) || 1

    for (const i of inscrits) {
      const tiers = FINANCEMENTS_TIERS.includes(i.financement)
      const montant = Number(i.montantAccord) || Number(f.prix) || 0
      const qui = `${nom(i.apprenant)} — ${f.intitule || 'formation'}`
      if (tiers && !terminee && s.debut) {
        const avant = jours(aujourdhui, s.debut)
        if (!i.numeroDossier && !i.dateDepot && avant <= 30) {
          alertes.push({ cle: `depot:${i.id}`, niveau: avant <= 15 ? 'bloquant' : 'alerte', type: 'depot', montant, titre: 'Demande de prise en charge non déposée', detail: `${qui} · début dans ${avant} jour(s). La plupart des OPCO exigent un dépôt 15 jours à 1 mois avant le début : au-delà, refus quasi automatique.`, inscription: i.id })
        }
      }
      if (!terminee) continue
      const lignes = d.presences.filter((p) => p.inscription === i.id)
      const signees = lignes.reduce((a, p) => a + (p.matin ? 1 : 0) + (p.apresMidi ? 1 : 0), 0)
      const justifiees = lignes.reduce((a, p) => a + (p.motifMatin ? 1 : 0) + (p.motifApresMidi ? 1 : 0) + (!('motifMatin' in p) && p.motif ? 1 : 0), 0)
      const attendues = nbJours * 2
      if (signees + justifiees < attendues) {
        alertes.push({ cle: `emarg:${i.id}`, niveau: 'bloquant', type: 'emargement', montant, titre: `${attendues - signees - justifiees} demi-journée(s) sans émargement`, detail: `${qui}. Un créneau non signé et non justifié peut être déduit par le financeur, voire bloquer tout le dossier.`, inscription: i.id })
      }
      if (tiers && !i.pieces?.attestation) {
        alertes.push({ cle: `certif:${i.id}`, niveau: 'bloquant', type: 'certificat', montant, titre: 'Certificat de réalisation non émis', detail: `${qui}. Sans lui, pas de paiement : c’est la pièce de clôture exigée par les financeurs.`, inscription: i.id })
      }
      if (tiers) {
        const factures = d.factures.filter((x) => x.type === 'Facture' && x.session === s.id && (!i.financeur || x.client === i.financeur))
        if (!factures.length) {
          alertes.push({ cle: `factiers:${i.id}`, niveau: 'alerte', type: 'facture', montant, titre: 'Facture au financeur non émise', detail: `${qui}. Formation terminée, mais aucune facture adressée au financeur pour cette session.`, inscription: i.id })
        }
      }
    }

    // Facture au financeur supérieure au total des accords : le dépassement ne sera pas payé par lui
    if (terminee) {
      const accords = {}
      for (const i of inscrits) if (FINANCEMENTS_TIERS.includes(i.financement) && i.financeur && i.montantAccord) accords[i.financeur] = (accords[i.financeur] || 0) + Number(i.montantAccord)
      for (const [fin, accord] of Object.entries(accords)) {
        const facture = d.factures.filter((x) => x.type === 'Facture' && x.session === s.id && x.client === fin).reduce((a, x) => a + (Number(x.montantHT) || 0), 0)
        if (facture > accord + 1) {
          alertes.push({ cle: `ecart:${s.id}:${fin}`, niveau: 'alerte', type: 'ecart', montant: facture - accord, titre: 'Facture supérieure à l’accord de prise en charge', detail: `${client(fin).nom || 'Financeur'} · ${f.intitule || 'session'} : ${facture.toLocaleString('fr-FR')} € facturés pour ${accord.toLocaleString('fr-FR')} € accordés. Le financeur ne paiera pas le dépassement : facturez-le au client.`, session: s.id })
        }
      }
    }

    // Sessions terminées sans aucune facture (hors financeur) : heures réalisées non facturées
    if (terminee && inscrits.length && !d.factures.some((x) => x.type === 'Facture' && x.session === s.id)) {
      const payeurDirect = inscrits.filter((i) => !FINANCEMENTS_TIERS.includes(i.financement))
      if (payeurDirect.length) {
        const montant = (Number(f.prix) || 0) * payeurDirect.length
        alertes.push({ cle: `nonfact:${s.id}`, niveau: 'alerte', type: 'facture', montant, titre: 'Formation réalisée, jamais facturée', detail: `${f.intitule || 'Session'} du ${new Date(s.debut).toLocaleDateString('fr-FR')} · ${payeurDirect.length} stagiaire(s) ${client(s.client).nom ? '· client ' + client(s.client).nom : ''}.`, session: s.id })
      }
    }
  }

  for (const x of d.factures) {
    if (x.type !== 'Facture' || !['Envoyé', 'Impayé', 'Partiellement payé'].includes(x.statut) || !x.date) continue
    const retard = jours(x.date, aujourdhui)
    if (retard > 30) {
      const du = (Number(x.montantHT) || 0) - (Number(x.encaisse) || 0)
      alertes.push({ cle: `relance:${x.id}`, niveau: retard > 60 ? 'bloquant' : 'alerte', type: 'relance', montant: du, titre: `Facture ${x.numero} impayée depuis ${retard} jours`, detail: `${client(x.client).nom || 'Client'} · ${du.toLocaleString('fr-FR')} € restant dus. Une relance écrite est la première étape (et la plus efficace).`, facture: x.id })
    }
  }

  const ordre = { bloquant: 0, alerte: 1 }
  alertes.sort((a, b) => ordre[a.niveau] - ordre[b.niveau] || b.montant - a.montant)
  return { alertes, total: alertes.reduce((a, x) => a + (x.montant || 0), 0) }
}

/** Relance rédigée sans IA (repli hors ligne) : sobre, factuelle, prête à envoyer. */
export function relanceModele(d, facture) {
  const c = d.clients.find((x) => x.id === facture.client) || {}
  const s = d.sessions.find((x) => x.id === facture.session)
  const f = s && d.formations.find((x) => x.id === s.formation)
  const o = d.organisme
  const du = (Number(facture.montantHT) || 0) - (Number(facture.encaisse) || 0)
  return `Objet : Relance — facture ${facture.numero} du ${new Date(facture.date).toLocaleDateString('fr-FR')}

Madame, Monsieur,

Sauf erreur de notre part, la facture n° ${facture.numero} du ${new Date(facture.date).toLocaleDateString('fr-FR')}, d’un montant de ${du.toLocaleString('fr-FR')} € ${o.tva?.includes('293 B') ? '(TVA non applicable, art. 293 B du CGI)' : 'HT'}${f ? `, relative à la formation « ${f.intitule} »${s?.debut ? ` réalisée le ${new Date(s.debut).toLocaleDateString('fr-FR')}` : ''}` : ''}, reste à ce jour impayée.

${c.type === 'OPCO' ? 'Vous trouverez à nouveau ci-joint le certificat de réalisation et les feuilles d’émargement. ' : ''}Nous vous remercions de bien vouloir procéder à son règlement sous 8 jours, ou de nous indiquer toute pièce manquante.

Nous restons à votre disposition.

Cordialement,
${o.dirigeant || ''}
${o.nom || ''} — ${o.email || ''} — ${o.tel || ''}`
}

/** Lecture « hors ligne » d'un accord de prise en charge collé (repli sans IA). */
export function lireAccordLocal(texte) {
  const t = texte.replace(/ /g, ' ')
  const montants = [...t.matchAll(/(\d{1,3}(?:[ .]\d{3})*(?:,\d{1,2})?)\s*(?:€|euros?)/gi)].map((m) => Number(m[1].replace(/[ .]/g, '').replace(',', '.')))
  const dates = [...t.matchAll(/(\d{2})\/(\d{2})\/(\d{4})/g)].map((m) => `${m[3]}-${m[2]}-${m[1]}`)
  const dossier = t.match(/(?:dossier|accord|r[ée]f[ée]rence)\s*(?:n°|no|num[ée]ro)?\s*[:#]?\s*([A-Z0-9][A-Z0-9-/]{3,})/i)?.[1] || null
  const heures = t.match(/(\d{1,4}(?:,\d)?)\s*h(?:eures?)?\b/i)?.[1]
  return {
    numero_dossier: dossier,
    montant_accorde_ht: montants.length ? Math.max(...montants) : null,
    date_debut: dates[0] || null,
    date_fin: dates[1] || null,
    heures: heures ? Number(heures.replace(',', '.')) : null,
    subrogation: /subrogation/i.test(t) ? true : null,
    remarques: 'Lecture par règles (IA non connectée) : vérifiez chaque valeur.',
  }
}

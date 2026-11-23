/* ===================================================================== V12 (23/11/2026) : numérotation des factures F-XXX-01
 * Règle d'Aurélien : F = facture ; XXX = lettre(s) du centre ; 01 = rang de la facture dans l'année pour ce centre,
 * remis à 01 au 1er janvier. BOFiP BOI-TVA-DECLA-30-20-20-10 § 70-90 : séries distinctes admises, chronologiques
 * et continues, deux factures de la même année ne portent jamais le même numéro. */
const PREFIXES_DEFAUT = { "TETRANERGY": "T", "BARRY CONNAN CONSEIL": "BCC", "BEFORMA": "B", "JC FORMATION": "JC", "ICCI FORMATION": "I", "GEM FORMATION": "GEM" };
const normNom = (s) => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toUpperCase().replace(/[^A-Z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
function prefixeClient(clientId) {
  const c = cfg(), choisi = (c.prefixes || {})[clientId];
  if (choisi) return choisi;
  const e = (M.at.entreprises || []).find((x) => x.id === clientId), nom = normNom(e && e.nom);
  if (PREFIXES_DEFAUT[nom]) return PREFIXES_DEFAUT[nom];
  return (nom.replace(/^(ASSOCIATION|STE|SOCIETE|SARL|SAS|EURL|LA|LE|LES|L)\s+/, "")[0] || "X");
}
const numDe = (x) => String(x.numPdf || "").replace(/\s*\(.*\)$/, "").trim();
function prochainNumero(clientId, date, pieces) {
  const p = prefixeClient(clientId), an = String(date || auj()).slice(0, 4), re = new RegExp(`^F-${p}-(\\d+)$`, "i");
  const rangs = pieces.filter((x) => String(x.emission || "").slice(0, 4) === an).map((x) => (re.exec(numDe(x)) || [])[1]).filter(Boolean).map(Number);
  return `F-${p}-${String((rangs.length ? Math.max(...rangs) : 0) + 1).padStart(2, "0")}`;
}
function conflitsPrefixes() {
  const parP = {};
  for (const e of M.at.entreprises || []) (parP[prefixeClient(e.id)] = parP[prefixeClient(e.id)] || []).push(e.nom);
  return Object.entries(parP).filter(([, L]) => L.length > 1);
}
// le n° affiché (PDF, mails, listes) devient le n° F-XXX-01 ; la référence Airtable FAC-xxxx reste en interne
const convDevisV11 = CONV.devis;
CONV.devis = (r) => { const o = convDevisV11(r); return Object.assign(o, { refAirtable: o.ref, ref: o.numPdf || o.ref }); };
// toute facture (ou avoir) créée par Pilotage reçoit son numéro automatiquement
const ecrireAvantV12 = ecrire;
ecrire = async function (table, records, opts = {}) {   // eslint-disable-line no-func-assign
  if (table === "devis" && opts.creer) {
    await chargerPlusieurs(["devis", "entreprises"]);
    const deja = (M.at.devis || []).slice();
    for (const r of records) {
      const f = r.fields || {}, type = String(f[F.devis.type] || ""), cli = (f[F.devis.client] || [])[0];
      if (/facture|avoir/i.test(type) && !f[F.devis.numPdf] && cli) {
        f[F.devis.numPdf] = prochainNumero(cli, f[F.devis.emission], deja);
        deja.push({ emission: f[F.devis.emission] || auj(), numPdf: f[F.devis.numPdf] });
      }
    }
  }
  return ecrireAvantV12(table, records, opts);
};

// ------------------------------------------------------------------ réglage des préfixes (dans l'Assistant)
function prefixesHtml() {
  const E = (M.at.entreprises || []).slice().sort((a, b) => a.nom.localeCompare(b.nom)), conf = conflitsPrefixes(), an = auj().slice(0, 4);
  return `<section class="carte ck-bloc" id="as-prefixes"><h2>Numéros de facture : F-XXX-01</h2>
    <p class="mx-texte" style="margin:0">F = facture · XXX = lettre(s) du centre · 01 = rang de la facture dans l'année pour ce centre (retour à 01 au 1er janvier). Pilotage attribue le numéro tout seul à chaque nouvelle facture.</p>
    ${conf.length ? `<p class="message ko">Même préfixe pour plusieurs centres : ${conf.map(([p, L]) => `« ${esc(p)} » = ${L.map(esc).join(" et ")}`).join(" ; ")}. Changez-en un : sinon on ne sait plus à qui appartient F-${esc(conf[0][0])}-01.</p>` : ""}
    <form data-ckf="as-prefixes"><div class="defile"><table><thead><tr><th>Centre</th><th>Préfixe</th><th>Prochaine facture ${esc(an)}</th></tr></thead><tbody>
      ${E.map((e) => `<tr><td>${esc(e.nom)}</td><td><label class="ck-sr" for="pf-${esc(e.id)}">Préfixe ${esc(e.nom)}</label><input id="pf-${esc(e.id)}" name="${esc(e.id)}" value="${esc(prefixeClient(e.id))}" maxlength="6" style="width:6em;text-transform:uppercase" pattern="[A-Za-z0-9]{1,6}"></td><td>${esc(prochainNumero(e.id, auj(), M.at.devis || []))}</td></tr>`).join("")}
    </tbody></table></div><div class="actions"><button class="principal-court" type="submit">Enregistrer les préfixes</button></div></form>
    <p class="petit">Base : BOFiP, BOI-TVA-DECLA-30-20-20-10, § 70 à 90 (séries distinctes admises si l'activité le justifie, numérotation chronologique et continue, jamais deux fois le même numéro dans l'année). Factures déjà envoyées : inchangées. À faire valider par votre expert-comptable.</p></section>`;
}
FORM["as-prefixes"] = (f) => {
  const c = cfg(), fd = new FormData(f);
  c.prefixes = Object.assign({}, c.prefixes);
  for (const [id, v] of fd.entries()) { const p = String(v).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6); if (p) c.prefixes[id] = p; }
  sauver();
  const conf = conflitsPrefixes();
  toast(conf.length ? `Enregistré, mais « ${conf[0][0]} » sert à plusieurs centres : à corriger.` : "Préfixes enregistrés.", conf.length ? "alerte" : undefined);
  monterAssistant();
};
const monterAssistantV11 = monterAssistant;
monterAssistant = async function (force) {   // eslint-disable-line no-func-assign
  await monterAssistantV11(force);
  const z = $("#as-corps");
  if (z && z.isConnected && M.at.entreprises && !$("#as-prefixes")) z.insertAdjacentHTML("beforeend", prefixesHtml());
};
// l'Assistant signale aussi les préfixes en conflit
const problemesV11 = problemesAssistant;
problemesAssistant = function (r) {   // eslint-disable-line no-func-assign
  const P = problemesV11(r);
  for (const [p, L] of conflitsPrefixes()) P.push({ id: "pf-" + p, source: "Factures", niv: "att", titre: `Préfixe de facture « ${p} » commun à ${L.join(" et ")}`, constat: "Deux centres ne doivent pas partager les mêmes lettres : leurs factures F-" + p + "-01, F-" + p + "-02… se confondraient.", existant: [], propositions: ["Choisir des lettres différentes dans « Numéros de facture » (bas de cette page)."] });
  return P;
};

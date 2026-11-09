// Une page HTML statique par formation (dist/formations/…) : tout ce qu'un stagiaire, un employeur ou un
// financeur doit trouver avant de s'inscrire (référentiel national qualité, indicateurs 1 et 2), lisible sans
// JavaScript, imprimable, et indexable par les moteurs de recherche et les assistants d'IA.
const echapper = (t) => String(t ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c])
const jsonSur = (o) => JSON.stringify(o).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026')
const euros = (n) => (n == null ? '' : Number(n).toLocaleString('fr-FR') + ' €')

/** Texte Airtable → HTML : titres en capitales, listes numérotées ou à puces, paragraphes. */
function blocs(texte) {
  const lignes = String(texte || '').split('\n').map((l) => l.trim()).filter(Boolean)
  const html = []
  let liste = null
  const fermer = () => {
    if (liste) html.push(`</${liste}>`)
    liste = null
  }
  for (const l of lignes) {
    const num = l.match(/^(\d+)[.)]\s+(.*)$/)
    const puce = l.match(/^[•\-–]\s+(.*)$/)
    const lettres = l.replace(/[^A-Za-zÀ-ÿ]/g, '')
    if (num || puce) {
      const type = num ? 'ol' : 'ul'
      if (liste !== type) (fermer(), html.push(`<${type}>`), (liste = type))
      html.push(`<li>${echapper(num ? num[2] : puce[1])}</li>`)
    } else if (lettres.length > 6 && lettres === lettres.toUpperCase()) {
      fermer()
      html.push(`<h3>${echapper(l.charAt(0) + l.slice(1).toLowerCase())}</h3>`)
    } else {
      fermer()
      html.push(`<p>${echapper(l)}</p>`)
    }
  }
  fermer()
  return html.join('\n')
}

const STYLE = `
.cta { display: flex; flex-wrap: wrap; gap: 12px; margin: 28px 0 8px; }
.cta a { display: inline-flex; align-items: center; min-height: 48px; padding: 10px 20px; border-radius: 14px; text-decoration: none; }
.cta .principal { background: var(--bleu); color: #fff; }
.cta .secondaire { border: 2px solid var(--bleu); color: var(--bleu); }
.chiffres { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 18px 0; padding: 0; list-style: none; }
.chiffres li { background: #fff; border-radius: 16px; padding: 14px 16px; border: 1px solid rgba(27, 58, 107, 0.15); }
.chiffres strong { display: block; font-family: 'Montserrat', sans-serif; font-size: 1.4rem; color: var(--bleu); }
.autres { columns: 2 260px; padding-left: 1.2em; }
@media print { .cta, .evitement, .retour { display: none; } }
`

export function pageFormation({ f, fiche, slug, css, site, entreprise, autres, programmePdf }) {
  const t = fiche.tarifs || {}
  const ind = fiche.indicateurs || {}
  const url = `${site}/${slug}`
  const titre = `${f.nom} — formation à La Réunion | ${entreprise.nom}`
  const description = `${f.nom} : ${f.sousTitre}. ${f.jours} jour${f.jours > 1 ? 's' : ''} (${f.heures} h), inter ou intra, à La Réunion. Organisme certifié Qualiopi, finançable OPCO.`.slice(0, 300)
  const objectifs = fiche.objectifs || (Array.isArray(f.objectifs) ? f.objectifs.join('\n') : f.objectifs) || ''
  const financements = (fiche.financements || []).join(', ')
  const methodes = (fiche.methodes || []).join(', ') || 'Présentiel'
  const resultat = ind.satisfaction != null || ind.reussite != null
    ? `<ul class="chiffres">
        ${ind.stagiaires != null ? `<li><strong>${echapper(ind.stagiaires)}</strong>stagiaires formés</li>` : ''}
        ${ind.satisfaction != null ? `<li><strong>${echapper(ind.satisfaction)} %</strong>de satisfaction</li>` : ''}
        ${ind.reussite != null ? `<li><strong>${echapper(ind.reussite)} %</strong>d’objectifs atteints</li>` : ''}
      </ul>`
    : `<p>Formation récente : les premiers indicateurs (satisfaction, atteinte des objectifs) sont publiés ici après les premières sessions, conformément au référentiel national qualité.</p>`
  const cours = {
    '@context': 'https://schema.org',
    '@type': 'Course',
    '@id': url,
    url,
    courseCode: f.ref,
    name: f.nom,
    description: f.sousTitre || f.nom,
    inLanguage: 'fr',
    provider: { '@type': 'EducationalOrganization', '@id': `${site}/#organisme`, name: entreprise.nom, url: `${site}/` },
    ...(fiche.prerequis ? { coursePrerequisites: fiche.prerequis } : {}),
    hasCourseInstance: { '@type': 'CourseInstance', courseMode: 'Onsite', location: { '@type': 'Place', name: 'La Réunion' }, courseWorkload: `PT${f.heures}H` },
    ...(t.interTotal ? { offers: { '@type': 'Offer', category: 'Paid', price: t.interTotal, priceCurrency: 'EUR' } } : {}),
  }
  const fil = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Accueil', item: `${site}/` },
      { '@type': 'ListItem', position: 2, name: 'Formations', item: `${site}/#formations` },
      { '@type': 'ListItem', position: 3, name: f.nom, item: url },
    ],
  }
  const sujet = encodeURIComponent(`Demande d’information — ${f.nom} (${f.ref})`)

  return `<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${echapper(titre)}</title>
    <meta name="description" content="${echapper(description)}" />
    <link rel="canonical" href="${url}" />
    <meta name="theme-color" content="#1B3A6B" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="${echapper(entreprise.nom)}" />
    <meta property="og:url" content="${url}" />
    <meta property="og:title" content="${echapper(f.nom)} — ${echapper(entreprise.nom)}" />
    <meta property="og:description" content="${echapper(description)}" />
    <meta property="og:image" content="${site}/media/hero-poster.jpg" />
    <meta property="og:locale" content="fr_FR" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/png" href="../media/logo-mark.png" />
    <link rel="stylesheet" href="../${css}" />
    <style>${STYLE}</style>
    <script type="application/ld+json">${jsonSur(cours)}</script>
    <script type="application/ld+json">${jsonSur(fil)}</script>
  </head>
  <body>
    <a class="evitement" href="#contenu">Aller au contenu</a>
    <header class="bandeau">
      <div class="bandeau-inner">
        <a class="retour" href="../index.html#formations">← Toutes les formations</a>
        <h1>${echapper(f.nom)}</h1>
        <p class="meta">${echapper(f.sousTitre)}</p>
        <p class="meta">Réf. <strong>${echapper(f.ref)}</strong> · <strong>${echapper(f.jours)} jour${f.jours > 1 ? 's' : ''}</strong> (${echapper(f.heures)} heures) · présentiel, inter ou intra-entreprise · La Réunion</p>
      </div>
    </header>

    <div class="page">
      <nav class="sommaire" aria-label="Sommaire">
        <h2>Sommaire</h2>
        <ol>
          <li><a href="#essentiel">L’essentiel</a></li>
          <li><a href="#objectifs">Objectifs</a></li>
          <li><a href="#programme">Programme</a></li>
          <li><a href="#methodes">Méthodes et évaluation</a></li>
          <li><a href="#acces">Inscription et délais</a></li>
          <li><a href="#tarifs">Tarifs et financements</a></li>
          <li><a href="#handicap">Accessibilité</a></li>
          <li><a href="#resultats">Résultats</a></li>
          <li><a href="#contact">Contact</a></li>
        </ol>
      </nav>

      <main id="contenu">
        <section id="essentiel">
          <h2>L’essentiel</h2>
          <dl class="fiche">
            <dt>Public</dt><dd>${echapper(fiche.public || f.public)}</dd>
            <dt>Prérequis</dt><dd>${echapper(fiche.prerequis || 'Aucun.')}</dd>
            <dt>Durée</dt><dd>${echapper(f.jours)} jour${f.jours > 1 ? 's' : ''}, soit ${echapper(f.heures)} heures de formation (journées de 08h00 à 12h00 et de 13h00 à 17h00, pauses déduites)</dd>
            <dt>Effectif</dt><dd>6 participants minimum, 8 au maximum</dd>
            <dt>Modalité</dt><dd>${echapper(methodes)} — en inter-entreprises (salle sur l’île) ou en intra, dans vos locaux</dd>
            ${fiche.materiel ? `<dt>Matériel</dt><dd>${echapper(fiche.materiel)}${fiche.precisionMateriel ? ` — ${echapper(fiche.precisionMateriel)}` : ''}</dd>` : ''}
            <dt>Formateur</dt><dd>${echapper(entreprise.dirigeant)}, formateur en IA, vente et management</dd>
          </dl>
          <div class="cta">
            <a class="principal" href="mailto:${echapper(entreprise.email)}?subject=${sujet}">Demander un devis ou une date</a>
            <a class="secondaire" href="${echapper(entreprise.telLien)}">Appeler le ${echapper(entreprise.telAffiche)}</a>
            ${programmePdf ? `<a class="secondaire" href="../${encodeURI(programmePdf)}">Programme détaillé (PDF)</a>` : ''}
          </div>
        </section>

        <section id="objectifs">
          <h2>Objectifs</h2>
          ${blocs(objectifs) || '<p>Les objectifs détaillés figurent dans le programme (PDF).</p>'}
        </section>

        <section id="programme">
          <h2>Programme</h2>
          ${blocs(fiche.programme)}
          <p>En intra-entreprise, le programme est ajusté à vos cas réels sans changer les objectifs.</p>
        </section>

        <section id="methodes">
          <h2>Méthodes pédagogiques et évaluation</h2>
          <p>Formation pratique : alternance de démonstrations, d’ateliers sur des cas réels de TPE-PME réunionnaises et de mises en situation.
          Chaque notion est d’abord manipulée, puis schématisée, puis formalisée.</p>
          <h3>Évaluation</h3>
          <p>${echapper(fiche.evaluation || 'Positionnement à l’entrée, évaluation des acquis en fin de formation, attestation de fin de formation.')}</p>
        </section>

        <section id="acces">
          <h2>Inscription et délais d’accès</h2>
          ${blocs(fiche.acces || 'Inscription jusqu’à 15 jours ouvrés avant le début de la session, sous réserve de places disponibles.')}
        </section>

        <section id="tarifs">
          <h2>Tarifs et financements</h2>
          <dl class="fiche">
            ${t.interJour ? `<dt>Inter-entreprises</dt><dd>${euros(t.interJour)} par jour et par stagiaire, soit ${euros(t.interTotal)} pour la formation</dd>` : ''}
            ${t.intraJour ? `<dt>Intra-entreprise</dt><dd>${euros(t.intraJour)} par jour pour le groupe, soit ${euros(t.intraTotal)} pour la formation</dd>` : '<dt>Intra-entreprise</dt><dd>Sur devis</dd>'}
            <dt>TVA</dt><dd>${echapper(t.mentionTva || 'TVA non applicable, art. 293 B du CGI')} — prix nets</dd>
            ${financements ? `<dt>Financements possibles</dt><dd>${echapper(financements)}</dd>` : ''}
          </dl>
          <p>Nous vous aidons à monter le dossier de prise en charge auprès de votre OPCO. Organisme certifié Qualiopi
          (n° ${echapper(entreprise.qualiopi)}, catégorie actions de formation) : condition d’accès aux fonds publics et mutualisés.</p>
        </section>

        <section id="handicap">
          <h2>Accessibilité aux personnes en situation de handicap</h2>
          ${blocs(fiche.adaptations || 'Formation accessible aux personnes en situation de handicap.')}
          <p class="encart">Référent handicap : ${echapper(entreprise.dirigeant)} — <a href="mailto:${echapper(entreprise.email)}">${echapper(entreprise.email)}</a> — ${echapper(entreprise.telAffiche)}.
          Un besoin d’aménagement peut être signalé à tout moment, sans justificatif médical.</p>
        </section>

        <section id="resultats">
          <h2>Indicateurs de résultats</h2>
          ${resultat}
        </section>

        <section id="contact">
          <h2>Contact et inscription</h2>
          <p>${echapper(entreprise.nom)} — ${echapper(entreprise.adresse)}<br />
          <a href="mailto:${echapper(entreprise.email)}?subject=${sujet}">${echapper(entreprise.email)}</a> — <a href="${echapper(entreprise.telLien)}">${echapper(entreprise.telAffiche)}</a></p>
          <p>Réclamation ou difficulté : écrivez-nous à la même adresse ; accusé de réception sous 48 heures ouvrées.</p>
          ${autres.length ? `<h3>Autres formations</h3><ul class="autres">${autres.map((a) => `<li><a href="../${a.slug}">${echapper(a.nom)}</a></li>`).join('')}</ul>` : ''}
        </section>
      </main>
    </div>

    <footer class="pied">
      <div class="bandeau-inner">
        ${echapper(entreprise.nom)} — ${echapper(entreprise.dirigeant)} EI — ${echapper(entreprise.adresse)} — SIRET ${echapper(entreprise.siret)}<br />
        Déclaration d’activité n° ${echapper(entreprise.nda)} auprès du Préfet de La Réunion. Cet enregistrement ne vaut pas agrément de l’État.<br />
        <a href="../index.html">Accueil</a> · <a href="../mentions-legales.html">Mentions légales</a> · <a href="../confidentialite.html">Politique de confidentialité</a>
      </div>
    </footer>
  </body>
</html>
`
}

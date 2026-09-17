/* Application YEBA FORMATIONS — routeur, transitions, assistant, consentement. */

import { ORGANISME, CERTIFICATIONS, FORMATIONS, VEILLE, FAQ, REPONSE_PAR_DEFAUT } from './contenu.js';
import { demarrerScene } from './scene.js';

const doux = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s, r = document) => r.querySelector(s);
const euros = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
const enDate = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString('fr-FR',
  { day: 'numeric', month: 'long', year: 'numeric' });

/* Échappement systématique : tout texte inséré via innerHTML passe par là.
   Le contenu vient de nos fichiers, mais la saisie de l'assistant vient du
   visiteur — une seule omission suffirait à ouvrir une injection. */
const esc = (s) => String(s).replace(/[&<>"']/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ───────────────────────── Pages ─────────────────────────

const carteFormation = (f) => `
  <article class="carte">
    <p class="carte-domaine">${esc(f.domaine)}</p>
    <h3>${esc(f.titre)}</h3>
    <p class="carte-accroche">${esc(f.accroche)}</p>
    <ul class="puces">
      <li class="puce">${esc(f.type)}</li>
      <li class="puce">${f.heures} h · ${f.jours} jour${f.jours > 1 ? 's' : ''}</li>
      <li class="puce puce--or">Accessible handicap</li>
    </ul>
    <ul class="objectifs">${f.objectifs.slice(0, 3).map((o) => `<li>${esc(o)}</li>`).join('')}</ul>
    ${f.noteHandicap ? `<p class="note-handicap">${esc(f.noteHandicap)}</p>` : ''}
    <div class="carte-pied">
      <p class="tarif">${euros.format(f.tarif)}<small>HT / jour / personne</small></p>
      <a class="lien-or" href="#/contact?f=${encodeURIComponent(f.id)}">Demander un devis</a>
    </div>
  </article>`;

const PAGES = {
  accueil: () => `
    <section class="heros">
      <canvas id="scene" aria-hidden="true"></canvas>
      <div class="voile"></div>
      <div class="enveloppe heros-texte">
        <p class="sur-titre">Organisme certifié Qualiopi · La Réunion</p>
        <h1>Ils sont sortis d'ici <em>en sachant faire.</em></h1>
        <p class="chapo">
          Formations en intelligence artificielle, automatisation et conformité,
          pour les entreprises réunionnaises. Deux jours, un livrable qui
          fonctionne, et plus personne à rappeler.
        </p>
        <div class="actions">
          <a class="bouton bouton--or" href="#/formations">Voir les formations</a>
          <a class="bouton bouton--clair" href="#/contact">Parler à Aurélien</a>
        </div>
      </div>
      <div class="bandeau-preuves">
        <div class="enveloppe">
          <dl>
            <div><dt>Qualiopi</dt><dd>25FOR02027.1</dd></div>
            <div><dt>Depuis</dt><dd>Avril 2021</dd></div>
            <div><dt>Délai d'accès</dt><dd>15 jours ouvrés</dd></div>
            <div><dt>Accessibilité</dt><dd>100 %</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="enveloppe">
        <div class="titre-section anim">
          <h2>Trois métiers, une seule exigence</h2>
          <p>Ce que nous enseignons, nous l'appliquons d'abord à nous-mêmes.</p>
        </div>
        <div class="trio">
          ${[
            ['Former', "IA générative, automatisation, vente et management. En intra chez vous ou en inter à Sainte-Clotilde.", '#/formations'],
            ['Implémenter', "Workflows, sites, bases de données. Des outils qui tiennent, hébergés là où vous décidez.", '#/contact'],
            ['Auditer', "Gouvernance RGPD et règlement européen sur l'IA. Qualifier le risque avant de déployer.", '#/conformite'],
          ].map(([t, d, l], i) => `
            <a class="bloc-trio anim" style="--retard:${i * 90}ms" href="${l}">
              <h3>${t}</h3><p>${d}</p><span class="fleche" aria-hidden="true">→</span>
            </a>`).join('')}
        </div>
      </div>
    </section>

    <section class="section section--sombre">
      <div class="enveloppe">
        <div class="titre-section anim">
          <h2>La veille, sans le bruit</h2>
          <p>Ce qui change vraiment pour une entreprise réunionnaise. Chaque brève porte sa source.</p>
        </div>
        <div class="veille">${VEILLE.slice(0, 2).map(breve).join('')}</div>
        <p><a class="lien-or" href="#/veille">Toute la veille →</a></p>
      </div>
    </section>`,

  formations: () => `
    <div class="entete-page">
      <div class="enveloppe">
        <p class="sur-titre">Catalogue</p>
        <h1>Sept formations, un seul critère :<br><em>que ça serve lundi matin.</em></h1>
        <p class="chapo">
          Tarifs nets de taxe — la formation professionnelle est exonérée de TVA
          (art. 261-4-4° a du CGI). Délai d'accès : ${ORGANISME.delaiAcces}.
        </p>
      </div>
    </div>
    <section class="section">
      <div class="enveloppe">
        <div class="filtres" role="group" aria-label="Filtrer par domaine" id="filtres"></div>
        <p class="sr" role="status" aria-live="polite" id="annonce"></p>
        <div class="grille" id="grille">${FORMATIONS.map(carteFormation).join('')}</div>
      </div>
    </section>`,

  veille: () => `
    <div class="entete-page">
      <div class="enveloppe">
        <p class="sur-titre">Veille</p>
        <h1>IA, RGPD, règlement européen :<br><em>ce qui vous concerne.</em></h1>
        <p class="chapo">
          Pas d'actualité pour l'actualité. Chaque brève dit ce qui change pour
          vous, et d'où elle vient.
        </p>
      </div>
    </div>
    <section class="section">
      <div class="enveloppe"><div class="veille veille--large">${VEILLE.map(breve).join('')}</div></div>
    </section>`,

  conformite: () => `
    <div class="entete-page">
      <div class="enveloppe">
        <p class="sur-titre">Gouvernance</p>
        <h1>RGPD et règlement sur l'IA :<br><em>qualifier avant de déployer.</em></h1>
      </div>
    </div>
    <section class="section">
      <div class="enveloppe deux-col">
        <div class="anim">
          <h2>Le règlement européen sur l'IA, en pratique</h2>
          <p>
            Le règlement (UE) 2024/1689 ne classe pas les outils, il classe les
            usages. Le même assistant relève du risque minimal quand il rédige
            un compte rendu, et du haut risque quand il trie des candidatures.
          </p>
          <ul class="liste-risque">
            <li><span class="niveau niveau--min">Risque minimal</span>
              Rédaction, synthèse, traduction, aide au code. Aucune obligation
              particulière au titre du haut risque.</li>
            <li><span class="niveau niveau--haut">Haut risque — annexe III</span>
              Tri de candidatures, évaluation de salariés, scoring de personnes,
              accès à la formation. Analyse d'impact, documentation technique,
              journalisation et supervision humaine deviennent obligatoires.</li>
            <li><span class="niveau niveau--int">Interdit</span>
              Notation sociale, exploitation de la vulnérabilité, reconnaissance
              des émotions au travail.</li>
          </ul>
          <h2>Ce que vous devez déjà</h2>
          <p>
            L'article 4 impose depuis le <strong>2 février 2025</strong> à tout
            déployeur de veiller à la maîtrise de l'IA par son personnel. Cette
            obligation n'a pas de format imposé, mais elle suppose d'en apporter
            la preuve. Une attestation de formation en est une.
          </p>
        </div>
        <aside class="encadre anim">
          <h3>Ce site, à titre d'exemple</h3>
          <p>Nous appliquons ce que nous enseignons. Concrètement :</p>
          <ul>
            <li><strong>Aucun traceur, aucune mesure d'audience.</strong> Le bandeau de consentement ne sert qu'à vous le montrer.</li>
            <li><strong>Aucune photographie de personne réelle.</strong> Les silhouettes de la page d'accueil sont dessinées au code : pas de droit à l'image, pas de donnée personnelle.</li>
            <li><strong>Aucune police distante.</strong> Rien n'appelle un serveur tiers à votre insu.</li>
            <li><strong>Le formulaire n'envoie rien.</strong> Il ouvre votre messagerie : vos informations restent chez vous.</li>
          </ul>
          <p class="fin">C'est la démonstration la moins coûteuse qui soit : il suffit de ne rien collecter.</p>
        </aside>
      </div>
    </section>`,

  apropos: () => `
    <div class="entete-page">
      <div class="enveloppe">
        <p class="sur-titre">À propos</p>
        <h1>Aurélien Lumeka</h1>
      </div>
    </div>
    <section class="section">
      <div class="enveloppe portrait-bloc">
        <div class="portrait anim">
          <div class="portrait-cadre" id="portrait">
            <span class="portrait-initiales" aria-hidden="true">AL</span>
            <p class="portrait-note">
              Emplacement réservé à votre photographie.<br>
              <small>Déposez <code>portrait.jpg</code> dans <code>site/app/</code> — voir le README.</small>
            </p>
          </div>
          <p class="portrait-legende">${esc(ORGANISME.dirigeant)}<br><span>${esc(ORGANISME.fonction)}</span></p>
        </div>
        <div class="anim">
          <h2>Formateur d'abord, expert ensuite</h2>
          <p>
            YEBA FORMATIONS existe depuis ${ORGANISME.depuis}. Avant de diriger
            l'organisme, j'ai formé à la vente, au management et aux compétences
            comportementales dans plusieurs centres de La Réunion. C'est de là
            que vient ma manière de travailler : on n'apprend pas en écoutant,
            on apprend en faisant — et en se trompant devant quelqu'un qui
            corrige.
          </p>
          <p>
            Depuis 2026, je me consacre à l'intelligence artificielle :
            formation, implémentation de solutions en entreprise, et conseil en
            gouvernance RGPD et règlement européen sur l'IA. Peu de monde fait
            les trois à La Réunion. C'est précisément ce qui permet de ne pas
            vous vendre un outil sans vous dire ce qu'il vous engage à faire.
          </p>
          <h3>Certifications</h3>
          <ul class="certifs">
            ${CERTIFICATIONS.map((c) => `<li><strong>${esc(c.nom)}</strong><span>${esc(c.emetteur)}</span></li>`).join('')}
          </ul>
        </div>
      </div>
    </section>`,

  contact: () => `
    <div class="entete-page">
      <div class="enveloppe">
        <p class="sur-titre">Contact</p>
        <h1>Parlons de votre besoin</h1>
        <p class="chapo">
          Un appel de quinze minutes suffit généralement à savoir si une
          formation est la bonne réponse — ou si autre chose le serait
          davantage.
        </p>
      </div>
    </div>
    <section class="section">
      <div class="enveloppe deux-col">
        <div class="anim">
          <dl class="coord">
            <div><dt>Téléphone</dt><dd><a href="tel:${ORGANISME.telLien}">${ORGANISME.tel}</a></dd></div>
            <div><dt>Courriel</dt><dd><a href="mailto:${ORGANISME.email}">${ORGANISME.email}</a></dd></div>
            <div><dt>Adresse</dt><dd>${ORGANISME.adresse}<br>${ORGANISME.ville}</dd></div>
            <div><dt>Référent handicap</dt><dd>${ORGANISME.dirigeant}<br><small>Réponse sous 48 h ouvrées, proposition d'aménagement sous 5 jours ouvrés.</small></dd></div>
          </dl>
        </div>
        <form class="anim" id="formulaire">
          <div class="champ"><label for="f-nom">Votre nom</label>
            <input id="f-nom" name="nom" type="text" autocomplete="name" required></div>
          <div class="champ"><label for="f-structure">Votre structure</label>
            <input id="f-structure" name="structure" type="text" autocomplete="organization"></div>
          <div class="champ"><label for="f-formation">Formation concernée</label>
            <select id="f-formation" name="formation">
              <option value="">Je ne sais pas encore</option>
              ${FORMATIONS.map((f) => `<option value="${esc(f.titre)}" data-id="${f.id}">${esc(f.titre)}</option>`).join('')}
              <option value="Conseil / audit RGPD ou IA Act">Conseil / audit RGPD ou IA Act</option>
            </select></div>
          <div class="champ"><label for="f-message">Votre besoin</label>
            <textarea id="f-message" name="message" placeholder="Nombre de participants, dates envisagées, contraintes particulières…"></textarea></div>
          <button class="bouton bouton--or" type="submit">Préparer ma demande</button>
          <p class="note">
            Ce formulaire n'envoie rien à un serveur : il ouvre votre logiciel de
            messagerie avec le message déjà rédigé. Vos informations restent sur
            votre appareil jusqu'à ce que vous décidiez d'envoyer.
          </p>
        </form>
      </div>
    </section>`,

  mentions: () => `
    <div class="entete-page"><div class="enveloppe">
      <p class="sur-titre">Informations légales</p><h1>Mentions légales</h1></div></div>
    <section class="section"><div class="enveloppe texte-legal">
      <h2>Éditeur</h2>
      <p>
        ${ORGANISME.nom} — ${ORGANISME.dirigeant}, ${ORGANISME.fonction.toLowerCase()}, directeur de la publication.<br>
        ${ORGANISME.adresse}, ${ORGANISME.ville}<br>
        Téléphone : ${ORGANISME.tel} — Courriel : ${ORGANISME.email}<br>
        SIRET : ${ORGANISME.siret}
      </p>
      <p class="a-completer">
        <strong>À compléter avant mise en ligne :</strong> forme juridique, capital
        social, numéro RCS et numéro de TVA intracommunautaire. Ces mentions sont
        obligatoires (code de commerce, art. R.123-237 ; LCEN du 21 juin 2004).
      </p>
      <h2>Activité de formation</h2>
      <p>
        Déclaration d'activité enregistrée sous le n° ${ORGANISME.nda} auprès du
        Préfet de La Réunion.<br>
        <strong>Cet enregistrement ne vaut pas agrément de l'État</strong>
        (code du travail, art. L.6352-12).<br>
        Certification Qualiopi n° ${ORGANISME.qualiopi}, délivrée au titre de la
        catégorie actions de formation, par ${ORGANISME.certificateur}, valable
        jusqu'au ${ORGANISME.qualiopiValidite}.<br>
        Autorité de contrôle : ${ORGANISME.autorite}.
      </p>
      <h2>Régime de TVA</h2>
      <p>
        Actions de formation professionnelle continue : TVA non applicable,
        article 261-4-4° a du code général des impôts. Les prestations de conseil
        et d'audit sont soumises à la TVA au taux de 8,5 % applicable à
        La Réunion.
      </p>
      <h2>Financement</h2>
      <p>
        Nos formations ne portent pas de code RNCP ou RS : elles ne sont
        <strong>pas éligibles au compte personnel de formation</strong>. Elles
        sont finançables par les OPCO, le plan de développement des compétences,
        France Travail, l'AIF et la Région Réunion.
      </p>
      <h2>Hébergement</h2>
      <p class="a-completer">
        <strong>À compléter :</strong> raison sociale, adresse et téléphone de
        l'hébergeur, ainsi que le pays d'implantation des serveurs. Exigence
        interne : hébergement dans l'Union européenne, chez un prestataire non
        soumis à une législation d'accès extraterritorial.
      </p>
      <h2>Médiation de la consommation</h2>
      <p class="a-completer">
        <strong>À désigner :</strong> dès qu'un particulier finance lui-même une
        formation, l'organisme doit avoir adhéré à un dispositif de médiation de
        la consommation et en publier les coordonnées (code de la consommation,
        art. L.612-1).
      </p>
      <h2>Propriété intellectuelle</h2>
      <p>
        L'ensemble des contenus pédagogiques, supports et éléments de ce site est
        protégé. Toute reproduction sans autorisation écrite est interdite.
      </p>
    </div></section>`,

  confidentialite: () => `
    <div class="entete-page"><div class="enveloppe">
      <p class="sur-titre">Données personnelles</p><h1>Politique de confidentialité</h1></div></div>
    <section class="section"><div class="enveloppe texte-legal">
      <h2>Ce site ne collecte rien</h2>
      <p>
        Aucun traceur, aucune mesure d'audience, aucune police de caractères
        distante, aucun service tiers. Votre navigation n'est ni enregistrée ni
        transmise. Le bandeau de consentement n'existe que pour vous le dire :
        il n'y a rien à accepter ni à refuser.
      </p>
      <h2>Le formulaire de contact</h2>
      <p>
        Il n'envoie aucune donnée à un serveur. Il compose un message dans votre
        propre logiciel de messagerie, que vous relisez et envoyez vous-même.
        Tant que vous ne l'envoyez pas, rien ne nous parvient.
      </p>
      <h2>Ce que nous traitons par ailleurs</h2>
      <p>
        Lorsque vous devenez prospect, stagiaire ou client, nous traitons les
        données nécessaires à la gestion de la formation : identité,
        coordonnées, structure, parcours, émargements et évaluations.
      </p>
      <table class="tableau">
        <thead><tr><th>Finalité</th><th>Base légale</th><th>Conservation</th></tr></thead>
        <tbody>
          <tr><td>Réponse à une demande</td><td>Intérêt légitime (art. 6.1.f)</td><td>3 ans sans relation</td></tr>
          <tr><td>Gestion de la formation</td><td>Exécution du contrat (art. 6.1.b)</td><td>Durée du contrat</td></tr>
          <tr><td>Obligations Qualiopi et comptables</td><td>Obligation légale (art. 6.1.c)</td><td>Jusqu'à 10 ans</td></tr>
          <tr><td>Aménagement pour handicap</td><td>Obligation légale (art. 6.1.c)</td><td>Durée de la formation</td></tr>
        </tbody>
      </table>
      <p>
        <strong>Nous ne recueillons jamais de justificatif médical.</strong> Pour
        un aménagement, seul le besoin est recueilli — jamais la nature du
        handicap, qui est une donnée de santé au sens de l'article 9 du RGPD.
      </p>
      <h2>Vos droits</h2>
      <p>
        Vous disposez des droits d'accès, de rectification, d'effacement, de
        limitation, d'opposition et de portabilité (art. 15 à 22 du RGPD).
        Écrivez à <a href="mailto:${ORGANISME.email}">${ORGANISME.email}</a> :
        réponse sous un mois. En cas de désaccord, vous pouvez saisir la CNIL,
        3 place de Fontenoy, 75007 Paris — <a href="https://www.cnil.fr" rel="noopener">cnil.fr</a>.
      </p>
      <h2>Responsable de traitement</h2>
      <p>${ORGANISME.nom} — ${ORGANISME.dirigeant}, ${ORGANISME.adresse}, ${ORGANISME.ville}.</p>
      <p class="a-completer">
        <strong>À vérifier avant mise en ligne :</strong> la liste des
        sous-traitants et leur localisation doit être tenue à jour. Tout
        prestataire hors Union européenne appelle un encadrement spécifique
        (RGPD, art. 44 à 49).
      </p>
    </div></section>`,
};

function breve(b) {
  return `<article class="breve anim">
    <div class="breve-tete">
      <span class="etiquette etiquette--${b.categorie.toLowerCase().replace(/[^a-z]/g, '')}">${esc(b.categorie)}</span>
      <time datetime="${b.date}">${enDate(b.date)}</time>
    </div>
    <h3>${esc(b.titre)}</h3>
    <p>${esc(b.resume)}</p>
    <p class="breve-impact"><strong>Pour vous :</strong> ${esc(b.impact)}</p>
    <p class="breve-source">Source : ${esc(b.source)}</p>
  </article>`;
}

// ───────────────────── Routeur et transition ─────────────────────

const TITRES = {
  accueil: 'Accueil', formations: 'Formations', veille: 'Veille IA',
  conformite: 'RGPD & IA Act', apropos: 'À propos', contact: 'Contact',
  mentions: 'Mentions légales', confidentialite: 'Confidentialité',
};

let arreterScene = null;

function route() {
  const brut = location.hash.replace(/^#\/?/, '') || 'accueil';
  const [nom, requete] = brut.split('?');
  return { nom: PAGES[nom] ? nom : 'accueil', params: new URLSearchParams(requete || '') };
}

/* Transition entre pages : un rideau balaie l'écran, une silhouette le
   traverse. Le rendu de la page suivante se fait pendant que l'écran est
   couvert, ce qui masque le repaint. */
function rideau() {
  return new Promise((resolve) => {
    if (doux) { resolve(); return; }
    const el = $('#rideau');
    el.classList.add('actif');
    setTimeout(resolve, 420);
    setTimeout(() => el.classList.remove('actif'), 900);
  });
}

async function afficher(pousser = true) {
  const { nom, params } = route();
  await rideau();

  if (arreterScene) { arreterScene(); arreterScene = null; }
  const vue = $('#vue');
  vue.innerHTML = PAGES[nom]();
  document.title = `${TITRES[nom]} · ${ORGANISME.nom}`;

  document.querySelectorAll('.nav a').forEach((a) => {
    const actif = a.getAttribute('href') === `#/${nom}` || (nom === 'accueil' && a.getAttribute('href') === '#/accueil');
    a.setAttribute('aria-current', actif ? 'page' : 'false');
  });

  if (nom === 'accueil') {
    const c = $('#scene');
    if (c) arreterScene = demarrerScene(c, { anime: !doux });
  }
  if (nom === 'formations') brancherFiltres();
  if (nom === 'contact') brancherFormulaire(params.get('f'));

  animerEntree();
  if (pousser) window.scrollTo({ top: 0, behavior: doux ? 'auto' : 'smooth' });
  $('#vue').focus({ preventScroll: true });
}

function animerEntree() {
  const cibles = document.querySelectorAll('.anim');
  if (doux || !('IntersectionObserver' in window)) {
    cibles.forEach((e) => e.classList.add('vu'));
    return;
  }
  const io = new IntersectionObserver((entrees) => {
    entrees.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('vu'); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px' });
  cibles.forEach((e) => io.observe(e));
}

// ───────────────────── Comportements de page ─────────────────────

function brancherFiltres() {
  const zone = $('#filtres'), grille = $('#grille'), annonce = $('#annonce');
  const domaines = ['Tous', ...new Set(FORMATIONS.map((f) => f.domaine))];
  let actif = 'Tous';

  zone.innerHTML = domaines.map((d) =>
    `<button class="filtre" type="button" aria-pressed="${d === actif}">${esc(d)}</button>`).join('');

  zone.addEventListener('click', (e) => {
    const b = e.target.closest('.filtre');
    if (!b) return;
    actif = b.textContent;
    zone.querySelectorAll('.filtre').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const vues = actif === 'Tous' ? FORMATIONS : FORMATIONS.filter((f) => f.domaine === actif);
    grille.innerHTML = vues.map(carteFormation).join('');
    annonce.textContent = `${vues.length} formation${vues.length > 1 ? 's' : ''} affichée${vues.length > 1 ? 's' : ''}.`;
    grille.querySelectorAll('.carte').forEach((c) => c.classList.add('vu'));
  });
}

function brancherFormulaire(idFormation) {
  const form = $('#formulaire');
  if (idFormation) {
    const opt = form.querySelector(`option[data-id="${CSS.escape(idFormation)}"]`);
    if (opt) form.querySelector('#f-formation').value = opt.value;
  }
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const corps = [
      `Nom : ${d.get('nom') || ''}`,
      `Structure : ${d.get('structure') || ''}`,
      `Formation : ${d.get('formation') || 'à définir'}`,
      '', d.get('message') || '',
    ].join('\n');
    location.href = `mailto:${ORGANISME.email}?subject=`
      + encodeURIComponent(`Demande — ${d.get('formation') || 'formation'}`)
      + `&body=${encodeURIComponent(corps)}`;
  });
}

// ───────────────────── Assistant ─────────────────────
/* Moteur local. Aucun modèle de langage n'est appelé et rien de ce que le
   visiteur écrit ne quitte son navigateur : c'est une correspondance de
   mots-clés sur une base de réponses vérifiées. Le dire est plus honnête
   que de laisser croire à une intelligence qu'il n'a pas. */

function repondre(question) {
  const q = question.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '');
  let meilleur = null, score = 0;
  for (const e of FAQ) {
    const s = e.cles.reduce((acc, c) => {
      const cle = c.normalize('NFD').replace(/[̀-ͯ]/g, '');
      return acc + (q.includes(cle) ? cle.length : 0);
    }, 0);
    if (s > score) { score = s; meilleur = e; }
  }
  return score > 0 ? meilleur.reponse : REPONSE_PAR_DEFAUT;
}

function brancherAssistant() {
  const bulle = $('#assistant'), ouvrir = $('#ouvrir-assistant');
  const fil = $('#fil'), form = $('#form-assistant'), champ = $('#q-assistant');

  const dire = (texte, qui) => {
    const p = document.createElement('div');
    p.className = `msg msg--${qui}`;
    p.innerHTML = `<span class="msg-qui">${qui === 'moi' ? 'Vous' : 'Assistant'}</span>${esc(texte)}`;
    fil.appendChild(p);
    fil.scrollTop = fil.scrollHeight;
  };

  const basculer = (visible) => {
    bulle.hidden = !visible;
    ouvrir.setAttribute('aria-expanded', String(visible));
    if (visible) champ.focus();
    else ouvrir.focus();
  };

  ouvrir.addEventListener('click', () => basculer(bulle.hidden));
  $('#fermer-assistant').addEventListener('click', () => basculer(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !bulle.hidden) basculer(false); });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = champ.value.trim();
    if (!q) return;
    dire(q, 'moi');
    champ.value = '';
    setTimeout(() => dire(repondre(q), 'lui'), doux ? 0 : 350);
  });

  $('#suggestions').addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    champ.value = b.textContent;
    form.requestSubmit();
  });

  dire("Bonjour. Je réponds aux questions courantes : tarifs, financement, accessibilité, délais, RGPD. Je fonctionne sur une liste de réponses vérifiées, sans intelligence artificielle — rien de ce que vous écrivez ne quitte votre navigateur.", 'lui');
}

// ───────────────────── Consentement ─────────────────────
/* Le site ne dépose aucun traceur. Ce panneau ne prétend donc pas obtenir un
   consentement qui n'a pas lieu d'être : il informe, et prépare la catégorie
   « mesure d'audience » pour le jour où elle sera activée. Le choix est
   conservé localement, ce qui est un stockage strictement nécessaire au sens
   de l'article 82 de la loi Informatique et Libertés — donc exempté. */

const CLE = 'yeba.consentement';

function lireConsentement() {
  try { return JSON.parse(localStorage.getItem(CLE) || 'null'); } catch { return null; }
}
function ecrireConsentement(v) {
  try { localStorage.setItem(CLE, JSON.stringify({ ...v, le: new Date().toISOString() })); } catch { /* navigation privée */ }
}

function brancherConsentement() {
  const panneau = $('#cookies');
  const afficherPanneau = () => { panneau.hidden = false; };

  if (!lireConsentement()) afficherPanneau();

  $('#cookies-tout').addEventListener('click', () => {
    ecrireConsentement({ mesure: true });
    panneau.hidden = true;
  });
  $('#cookies-refus').addEventListener('click', () => {
    ecrireConsentement({ mesure: false });
    panneau.hidden = true;
  });
  document.querySelectorAll('.rouvrir-cookies').forEach((a) =>
    a.addEventListener('click', (e) => { e.preventDefault(); afficherPanneau(); }));
}

// ───────────────────── Démarrage ─────────────────────

window.addEventListener('hashchange', () => afficher());
brancherAssistant();
brancherConsentement();
afficher(false);

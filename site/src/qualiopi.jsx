// Section publique « Qualiopi : la preuve, pas la promesse ».
// Ne lit que documents.json (intitulés seulement, généré par scripts/airtable-sync.mjs) et rnq.json (référentiel public).
// Le contenu des documents qualité (Pack Qualiopi vendu par YEBA Studio) n'est jamais publié.
// Aucun statut interne (incomplet, à valider, score d'audit) n'est jamais affiché ici.
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { AnimatePresence, LayoutGroup, motion } from 'framer-motion'
import { ExternalLink, FileText, Mail, Printer, ShieldCheck, X } from 'lucide-react'
import { Reveal, TitreAnime } from './anim.jsx'
import { ENTREPRISE } from './data.js'
import DOCS from './documents.json'
import RNQ from './rnq.json'

const EASE = [0.22, 1, 0.36, 1]
const PUBLICS = [
  ['tous', 'Tous'],
  ['Clients entreprises', 'Entreprises'],
  ['Stagiaires', 'Stagiaires'],
  ['Financeurs / OPCO', 'Financeurs'],
]
// Liste publique des organismes de formation (DGEFP) : on y vérifie la certification Qualiopi.
const VERIFIER_QUALIOPI = 'https://www.data.gouv.fr/fr/datasets/liste-publique-des-organismes-de-formation-l-6351-7-1-du-code-du-travail/'
const ACCES = {
  page: { libelle: 'Ouvrir la page', Icone: ExternalLink },
  demande: { libelle: 'Recevoir le document', Icone: Mail },
}

const documents = DOCS.documents
const titreCourt = (t) => t.replace(/\s*\((modèle[^)]*)\)/i, ' — $1')

function lienDemande(d) {
  const sujet = `Demande du document ${d.ref} — ${d.titre}`
  const corps = `Bonjour,\n\nPouvez-vous me transmettre le document « ${d.titre} » (réf. ${d.ref}) ?\n\nEntreprise :\nFonction :\n\nMerci.`
  return `mailto:${ENTREPRISE.email}?subject=${encodeURIComponent(sujet)}&body=${encodeURIComponent(corps)}`
}

export default function Qualiopi() {
  const [vue, setVue] = useState('bibliotheque')
  const [publicCible, setPublicCible] = useState('tous')
  const liste = documents.filter((d) => publicCible === 'tous' || d.pour.includes(publicCible))

  return (
    <section id="qualiopi" className="bloc clair qualiopi" aria-labelledby="titre-qualiopi">
      <div className="conteneur">
        <div className="q-tete">
          <div>
            <Reveal>
              <p className="surtitre">Qualité certifiée</p>
            </Reveal>
            <TitreAnime id="titre-qualiopi" texte="Qualiopi : la preuve, pas la promesse." accent={[3]} />
            <Reveal delay={0.1}>
              <p className="intro">
                Notre certification se vérifie en un clic sur la liste publique de l’État. Nos documents qualité sont
                remis à nos stagiaires, à nos clients et à leurs financeurs, sur simple demande.
              </p>
            </Reveal>
          </div>
          <Reveal delay={0.15} className="q-certif">
            <ShieldCheck size={40} aria-hidden="true" />
            <p>
              <strong>Certification Qualiopi</strong>
              <span>n° {ENTREPRISE.qualiopi}</span>
              <span>Catégorie : actions de formation</span>
              <a href={VERIFIER_QUALIOPI} target="_blank" rel="noopener noreferrer">
                Vérifier sur la liste publique <ExternalLink size={14} aria-hidden="true" />
              </a>
            </p>
          </Reveal>
        </div>

        <ul className="q-chiffres" aria-label="En bref">
          <li>
            <strong>{documents.length}</strong> documents référencés
          </li>
          <li>
            <strong>{RNQ.criteres.length}</strong> critères du référentiel national qualité
          </li>
          <li>
            <strong>{RNQ.indicateurs.length}</strong> indicateurs vérifiés par un auditeur indépendant
          </li>
        </ul>

        <div className="onglets q-vues" role="tablist" aria-label="Affichage">
          {[
            ['bibliotheque', 'Bibliothèque de documents'],
            ['carte', `Les ${RNQ.indicateurs.length} indicateurs`],
          ].map(([id, l]) => (
            <button
              key={id}
              role="tab"
              id={'q-onglet-' + id}
              aria-selected={vue === id}
              aria-controls={'q-vue-' + id}
              className="onglet"
              onClick={() => setVue(id)}
            >
              {l}
              {vue === id && <motion.span layoutId="q-soulignement" className="soulignement" />}
            </button>
          ))}
        </div>

        {vue === 'bibliotheque' ? (
          <div role="tabpanel" id="q-vue-bibliotheque" aria-labelledby="q-onglet-bibliotheque">
            <LayoutGroup id="q-filtres">
              <div className="filtres" role="group" aria-label="Filtrer par destinataire" style={{ marginTop: 28 }}>
                {PUBLICS.map(([id, l]) => (
                  <button key={id} className="filtre" aria-pressed={publicCible === id} onClick={() => setPublicCible(id)}>
                    {publicCible === id && <motion.span layoutId="q-pastille" className="pastille" />}
                    <span>{l}</span>
                  </button>
                ))}
              </div>
            </LayoutGroup>
            <ul className="q-docs">
              {liste.map((d) => (
                <CarteDocument key={d.ref} d={d} />
              ))}
            </ul>
          </div>
        ) : (
          <div role="tabpanel" id="q-vue-carte" aria-labelledby="q-onglet-carte">
            <CarteIndicateurs />
          </div>
        )}

        <p className="q-note">
          Les intitulés des indicateurs sont une synthèse du référentiel national qualité ; le texte officiel fait foi
          (décret n° 2026-728, Légifrance). La certification Qualiopi est obligatoire pour accéder aux fonds publics et
          mutualisés de la formation (art. L.6316-1 du code du travail).
        </p>
      </div>
    </section>
  )
}

function CarteDocument({ d }) {
  const { libelle, Icone } = ACCES[d.acces]
  return (
    <motion.li layout className="q-doc" transition={{ duration: 0.35, ease: EASE }}>
      <FileText className="q-doc-icone" size={30} aria-hidden="true" />
      <div className="q-doc-corps">
        <h3>{titreCourt(d.titre)}</h3>
        <p className="q-doc-rnq">{d.acces === 'page' ? 'Consultable sur ce site' : 'Remis sur simple demande'}</p>
      </div>
      <div className="q-doc-action">
        <a className="btn btn-bleu btn-petit" href={d.acces === 'page' ? d.page : lienDemande(d)}>
          <Icone size={18} aria-hidden="true" /> {libelle}
        </a>
      </div>
    </motion.li>
  )
}

function CarteIndicateurs() {
  const [choisi, setChoisi] = useState(null)
  const detail = choisi && RNQ.indicateurs.find((i) => i.n === choisi)
  return (
    <div className="q-carte">
      <div className="q-criteres">
        {RNQ.criteres.map((c) => (
          <div key={c.n} className="q-critere">
            <h3>
              <span className="q-num">{c.n}</span> {c.titre}
            </h3>
            <div className="q-puces">
              {RNQ.indicateurs
                .filter((i) => i.critere === c.n)
                .map((i) => (
                  <button
                    key={i.n}
                    className="q-ind en-ligne"
                    aria-pressed={choisi === i.n}
                    aria-label={`Indicateur ${i.n}`}
                    onClick={() => setChoisi(choisi === i.n ? null : i.n)}
                  >
                    {i.n}
                  </button>
                ))}
            </div>
          </div>
        ))}
      </div>
      <div className="q-detail" aria-live="polite">
        {detail ? (
          <>
            <h3>Indicateur {detail.n}</h3>
            <p>{detail.libelle}</p>
            <p className="q-muet">Nos preuves sont présentées à l’auditeur lors de chaque audit de surveillance.</p>
          </>
        ) : (
          <p className="q-muet">Touchez un numéro pour lire l’exigence du référentiel national qualité.</p>
        )}
      </div>
    </div>
  )
}

/** Mise en forme légère d'un document texte : titres en capitales, articles, puces. */
function Texte({ texte }) {
  return texte.split('\n').map((l, k) => {
    const t = l.trim()
    if (!t || /^─+$/.test(t)) return null
    if (/^(TITRE|ACCUSÉ)/.test(t) || (t === t.toUpperCase() && /[A-Z]/.test(t) && t.length > 4 && !/^[•\-]/.test(t))) return <h4 key={k}>{t}</h4>
    if (/^Article \d+/.test(t)) return <h5 key={k}>{t}</h5>
    if (/^[•\-]\s/.test(t)) return <p key={k} className="q-puce">{t.replace(/^[•\-]\s*/, '')}</p>
    return <p key={k}>{t}</p>
  })
}

export function Lecteur({ d, onFermer }) {
  const ref = useRef(null)
  useEffect(() => {
    const avant = document.activeElement
    ref.current?.focus()
    const touche = (e) => e.key === 'Escape' && onFermer()
    document.addEventListener('keydown', touche)
    document.body.style.overflow = 'hidden'
    document.body.classList.add('impr-doc')
    window.__lenis?.stop()
    return () => {
      window.__lenis?.start()
      document.removeEventListener('keydown', touche)
      document.body.style.overflow = ''
      document.body.classList.remove('impr-doc')
      avant?.focus?.()
    }
  }, [onFermer])
  return createPortal(
    <motion.div
      className="fond-modal q-lecteur-fond"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={(e) => e.target === e.currentTarget && onFermer()}
    >
      <motion.article
        className="modal q-lecteur"
        data-lenis-prevent
        role="dialog"
        aria-modal="true"
        aria-labelledby="q-lecteur-titre"
        tabIndex={-1}
        ref={ref}
        initial={{ y: 60, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        transition={{ duration: 0.45, ease: EASE }}
      >
        <header className="formation-tete">
          <button className="fermer" onClick={onFermer} aria-label="Fermer le document">
            <X size={26} />
          </button>
          <span className="badge">{d.ref}</span>
          <h3 id="q-lecteur-titre">{d.titre}</h3>
          <p>
            Version {d.version} · {new Date(d.date).toLocaleDateString('fr-FR')}
          </p>
        </header>
        <div className="modal-corps q-texte">
          <button className="btn btn-bleu btn-petit q-imprimer" onClick={() => window.print()}>
            <Printer size={18} aria-hidden="true" /> Imprimer ou enregistrer en PDF
          </button>
          <Texte texte={d.texte} />
        </div>
      </motion.article>
    </motion.div>,
    document.body,
  )
}

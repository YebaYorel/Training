// Section « YEBA Studio » : les logiciels pour organismes de formation, et l'accès au logiciel.
import { motion } from 'framer-motion'
import { ArrowRight, Bot, Check, FileSpreadsheet, FileText, Flame, Lock, ShieldCheck, Sparkles, Users, Zap } from 'lucide-react'
import { Reveal, TitreAnime } from './anim.jsx'
import { OFFRES } from '../espace/src/licence.js'
import { allerA } from './App.jsx'

export const STUDIO_URL = import.meta.env.VITE_STUDIO_URL || 'studio/'
const EASE = [0.22, 1, 0.36, 1]

const CARTES = [
  { id: 'qualiopi', Icone: ShieldCheck, points: ['24 modèles Word modifiables, remplis à votre nom', 'Référentiel 2026 (décret n° 2026-728), 33 indicateurs', 'Coffre de suivi + audit blanc automatique', 'Régénération illimitée'] },
  { id: 'bpf', Icone: FileSpreadsheet, points: ['Vos formations saisies au fil de l’eau (ou importées)', 'L’assistant pose les questions et remplit les cadres C à G', 'Codes NSF suggérés, incohérences détectées', 'Données chiffrées sur votre PC'] },
  { id: 'parcours', Icone: Users, points: ['Planning, sessions, inscriptions', 'Dossier stagiaire en 10 pièces', 'Émargement par demi-journée', 'Convocation, attestation, certificat en un clic', 'BPF Facile inclus'] },
]
const POURQUOI = [
  [Lock, 'Vos données restent chez vous', 'Chiffrées sur votre PC par votre code personnel. Personne n’y a accès, pas même nous.'],
  [Zap, 'Zéro frais de démarrage', 'Pas de « package de mise en service » : on ouvre, on saisit, on produit.'],
  [Bot, 'L’IA, française et encadrée', 'Mistral AI (Paris) pour rédiger et lire ; les montants viennent toujours de vos données.'],
  [Sparkles, 'Fait par un formateur', 'Conçu à La Réunion par un organisme certifié Qualiopi, qui l’utilise tous les jours.'],
]

export default function Studio() {
  const c = OFFRES.carburant
  return (
    <section id="studio" className="bloc sombre studio" aria-labelledby="titre-studio">
      <div className="conteneur">
        <Reveal>
          <p className="surtitre">Nouveau · logiciels pour organismes de formation</p>
        </Reveal>
        <TitreAnime id="titre-studio" texte="YEBA Studio : votre centre de formation, piloté par l’IA." accent={[5, 6]} />
        <Reveal delay={0.1}>
          <p className="intro">Qualiopi, BPF, gestion des sessions, et l’IA qui fait rentrer l’argent des OPCO. Pensé pour les organismes de 1 à 20 personnes.</p>
        </Reveal>

        <div className="studio-f">
          <motion.article className="carburant-vitrine" initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }} transition={{ duration: 0.7, ease: EASE }}>
            <span className="ruban-or"><Sparkles size={16} aria-hidden="true" /> Offre Pionniers 974 · 30 places</span>
            <h3><Flame className="flamme-vitrine" aria-hidden="true" /> CARBURANT</h3>
            <p className="accroche">L’IA qui fait rentrer l’argent des OPCO.</p>
            <p>Émargement manquant, certificat de réalisation oublié, facture supérieure à l’accord, dépôt hors délai, relance jamais envoyée : CARBURANT le voit <strong>avant</strong> le financeur, chiffre l’argent en jeu et rédige la relance à votre place.</p>
            <p className="prix-vitrine"><strong>{c.premierMois} €</strong> le premier mois, puis <strong>{c.prix} €/mois</strong>, tarif gelé à vie.</p>
            <p className="garantie"><ShieldCheck size={18} aria-hidden="true" /> Garantie « 10× » : s’il ne vous signale pas au moins 10 fois son prix en sommes à sécuriser sur 12 mois, l’année vous est remboursée (conditions dans nos CGV).</p>
            <a className="btn btn-or" href={STUDIO_URL} target="_blank" rel="noopener">Voir CARBURANT en action <ArrowRight size={18} aria-hidden="true" /></a>
          </motion.article>

          <div className="studio-offres">
            {CARTES.map(({ id, Icone, points }, k) => {
              const o = OFFRES[id]
              return (
                <Reveal key={id} delay={k * 0.08} className="studio-offre">
                  <div className="studio-offre-tete">
                    <Icone size={26} aria-hidden="true" />
                    <h3>{o.nom}</h3>
                    <p className="studio-prix">{o.libellePrix}</p>
                  </div>
                  <ul>{points.map((p) => <li key={p}><Check size={16} aria-hidden="true" /> {p}</li>)}</ul>
                </Reveal>
              )
            })}
            <Reveal delay={0.3} className="studio-offre complet">
              <div className="studio-offre-tete">
                <FileText size={26} aria-hidden="true" />
                <h3>{OFFRES.studio.nom}</h3>
                <p className="studio-prix">{OFFRES.studio.libellePrix}</p>
              </div>
              <p>Pack Qualiopi, BPF, Parcours et CARBURANT, pour un seul prix. Sans engagement.</p>
            </Reveal>
          </div>
        </div>

        <ul className="studio-pourquoi">
          {POURQUOI.map(([Icone, t, d], k) => (
            <Reveal key={t} delay={k * 0.08} className="studio-point">
              <Icone size={30} aria-hidden="true" />
              <h3>{t}</h3>
              <p>{d}</p>
            </Reveal>
          ))}
        </ul>

        <div className="studio-actions">
          <a className="btn btn-or" href={STUDIO_URL} target="_blank" rel="noopener">Essayer gratuitement 14 jours <ArrowRight size={18} aria-hidden="true" /></a>
          <button className="btn btn-contour" onClick={() => allerA('#contact')}>Une démonstration avec Aurélien</button>
        </div>
        <p className="studio-note">
          Pour comparaison, les logiciels de gestion du marché affichent de 49 € à plus de 300 € HT par mois, parfois avec plus de 1 400 € de frais de démarrage (tarifs publics relevés en septembre 2026). Prix YEBA nets de taxe : TVA non applicable, art. 293 B du CGI. Une licence = un utilisateur sur un poste. Outils d’aide : la déclaration BPF et la conformité Qualiopi restent sous la responsabilité de l’organisme.
        </p>
      </div>
    </section>
  )
}

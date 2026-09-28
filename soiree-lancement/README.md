# Soirée de lancement — YEBA FORMATIONS

Aurélien, Stan et Antho · public : dirigeants et cadres dirigeants triés sur le volet · 1 h à 1 h 15.

Parties traitées : **Présentation → Histoire → Offre YEBA → Formations** (29 slides visibles, ≈ 43 min).
Parties à construire (slides déjà créées mais masquées) : Applications & sites web · Audit & devis · Mot de fin avec offre soirée.

## Livrables

| Fichier | Rôle | Outil |
|---|---|---|
| `dist/YEBA_Soiree_Lancement.pptx` | **La présentation**, Morphose incluse, notes orateur complètes | python-pptx |
| `vba/YebaAnimations.bas` | 1 clic : Morphose + animations d'entrée + vidéo auto + contrôle accessibilité | VBA |
| `revealjs/index.html` | Version web hors ligne (Auto-Animate), vue orateur avec touche S | Reveal.js |
| `dist/yeba-intro.mp4` | Vidéo d'ouverture 10 s (déjà insérée en slide 0 du PPTX) | Remotion |
| `dist/yeba-transition-formations.mp4` | Transition « 04 · Nos formations » (compte-tours) | Remotion |
| `assets/videos/clip-*.mp4` | 4 clips fournis (Grok), passés en 1920×1080 et volume harmonisé, intégrés au PPTX | — |
| `dist/YEBA_Soiree_Lancement.pdf` | Export pour Slides.com / impression | LibreOffice |
| `slides-com/plan_slides_com.md` | Plan de montage Slides.com | Slides.com |
| `felo/prompt_felo_slides.md` | Prompt prêt à coller (sans donnée personnelle) | Felo Slides |
| `storyboard.md` | Storyboard slide par slide : texte, visuel, animation, notes | — |

## Mode d'emploi (5 minutes)

1. Installer la police **Montserrat** (fichiers `assets/fonts/*.ttf`, licence OFL) : double-clic → Installer.
2. Ouvrir `dist/YEBA_Soiree_Lancement.pptx`.
3. `Alt + F11` → Fichier → Importer → `vba/YebaAnimations.bas` ; `Alt + F8` → **YebaToutAppliquer**.
4. Enregistrer en `.pptx`. Diaporama en **mode Présentateur** : les notes indiquent quoi dire et combien de temps.

Modifier un texte : éditer `contenu/slides.json`, puis `bash build_all.sh` — le PPTX, le HTML, le storyboard,
le prompt Felo et le plan Slides.com se mettent à jour ensemble.

## Les 4 clips vidéo : où et pourquoi

| Clip | Place | Rôle |
|---|---|---|
| Introduction (livre qui s'ouvre) | Slide 2, juste avant le titre | « Top départ » quand les lumières baissent ; le livre annonce le fil rouge : le savoir |
| Intelligence Artificielle (sphère néon) | Juste avant « Vos équipes utilisent déjà l'IA ? » | Met la salle dans l'ambiance IA, la question qui suit la ramène à son entreprise |
| AI (lettres dorées) | Ouverture de « Nos formations », après l'agenda | L'or fait le lien avec la charte et le « garage YEBA » |
| Conclusion (anneau holographique) | Ouverture du « Mot de fin » (slide masquée tant que la partie n'est pas construite) | Annonce l'offre spéciale soirée |

Lecture automatique, une seule fois, son inclus (macro VBA `YebaToutAppliquer`). Tester le son dans la salle.

## Choix d'expert (pourquoi ce déroulé fonctionne)

- **Fil rouge « GPS »** : la même slide d'agenda revient à chaque partie, le marqueur or glisse (Morphose).
  Le public sait toujours où il en est — essentiel pour une salle de dirigeants.
- **Narration en 3 temps** : suspense (« pas de mot pour formation ») → révélation (YEBA) → symbole (le Y devient l'arbre).
  La Morphose *par caractère* fait disparaître E, B, A : le Y reste.
- **Le garage YEBA** : vos formations portent déjà des noms de pièces automobiles (Allumage, Pilote automatique,
  Carrosserie, Injection…). La grille devient un « garage » ; chaque tuile zoome en Morphose vers sa fiche.
- **Démo live** (S28) : un site dicté devant la salle. C'est le moment dont les invités parleront le lendemain.
- **Promesse honnête** (S20) : « Nous ne vendons pas la conformité. Nous vous aidons à la prouver. » —
  conforme à votre règle commerciale interne et plus crédible face à des dirigeants.

## Sources

- Histoire, valeurs, slogan : document de marque « YEBA FORMATIONS » (pièce jointe fournie).
- Formations : table *CATALOGUE FORMATIONS*, base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) », consultée le 28/09/2026.
- Horaires 8 h, règles commerciales, logo sans œil, contrastes WCAG : table *CONFIG SYSTÈME* de la même base.
- Illustrations (baobab, compte-tours, cercle européen) : dessinées par script (`assets/generer_illustrations.py`), libres de droits.

Photos conseillées (Unsplash, licence gratuite ; le téléchargement direct était bloqué depuis l'environnement de travail) :
baobab au coucher du soleil — Leon Pauleikhoff (https://unsplash.com/photos/gV8r3I9lvM4) ;
pitons de La Réunion — Sergey Zhesterev (https://unsplash.com/photos/VJlLx10OYRo).

## ⚖️ RGPD / IA Act — points à traiter avant la soirée

| Point | Texte | Action |
|---|---|---|
| Photos de Stan et Antho | RGPD + droit à l'image | Accord écrit avant projection ou diffusion |
| Liste d'invités / émargement | RGPD art. 5, 6, 13 | Finalité, base légale, durée de conservation, mention d'information |
| Démo live avec un invité | RGPD + IA Act art. 50 | Entreprise fictive ou accord ; dire que le contenu est généré par IA |
| S19 « Souveraineté par défaut » | RGPD chap. V | Vrai seulement après votre migration Gmail → Brevo, Airtable → Baserow/OVHcloud |
| Clips générés par IA (Grok, xAI) | IA Act art. 50 + conditions xAI | Le dire à l'oral ; vérifier l'autorisation d'usage commercial |
| Felo Slides, Slides.com | RGPD art. 28 et chap. V | Contenu public uniquement, jamais de données de clients |
| Aucune formation RNCP/RS | C. conso L.121-2 | Ne jamais dire « finançable CPF » ni « formation obligatoire » |

## À compléter par vous

- [ ] Date et lieu de la soirée (S01) · [ ] Rôles de Stan et d'Antho + photos (S04)
- [ ] N° Qualiopi : **25FOR02027.1** dans Airtable, **25FOF02027.1** dans vos préférences → vérifier sur le certificat
- [ ] Intitulés exacts des certifications Google (S05) · [ ] Outil utilisé pour la démo live (S28)

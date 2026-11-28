---
name: magi-video
description: Lanceur de MAGI-2 Preview (SandAI-org/MAGI-2-preview, Apache-2.0) — modèle open source de génération vidéo + son (texte→vidéo, image→vidéo), clips de 10 s en 1080p. Utiliser pour un teaser d'événement, un clip de démonstration, une vidéo de formation ou une scène « impossible » à filmer, quand on dispose d'un serveur GPU (8 × H100/H200) en UE. Sinon, renvoyer vers `openmontage` ou `higgsfield`.
---

# MAGI-2 Preview (lanceur)

Code d'inférence seulement (5,5 Mo) ; **poids : ~307 Go** sur Hugging Face.
Récupéré à la demande, à la version relue, dans `.claude/vendor-cache/` (ignoré par Git).

## 0. Vérifier AVANT tout (sinon s'arrêter et prévenir Aurélien)

- `nvidia-smi -L` doit lister **8 GPU Hopper** (H100/H200). Le conteneur cloud
  Claude Code n'en a pas : MAGI-2 n'y tourne **pas**.
- Disque libre ≥ 350 Go, `ffmpeg` installé.
- Serveur GPU **hébergé en UE** (ex. Scaleway Paris, OVHcloud Gravelines) :
  souveraineté des données.

## 1. Récupérer la version figée

```bash
python scripts/lanceur_depot.py SandAI-org/MAGI-2-preview f68a0f9bbccbea56e0177a9bd912abc3b18ffe61 magi-2
```

« ARRÊT » affiché = s'arrêter et prévenir Aurélien.

## 2. Générer

Dans `.claude/vendor-cache/magi-2/` : lire `README.md`, puis soit l'image Docker
figée `sandai/magi-2-preview:f68a0f9…` (jamais `latest`), soit
`pip install -r requirements.txt`. Poids : `hf download sand-ai/MAGI-2-preview --local-dir ckpt`.

```bash
torchrun --nproc_per_node=8 inference/pipeline/entry.py \
  --prompt-file prompt.txt --output output/ --output-width 1920 --output-height 1080
```

Un prompt long et structuré (voir `assets/sample_000.txt`) donne de bien meilleurs
résultats : Claude rédige lui-même ce prompt structuré au lieu d'activer l'option
d'amélioration des prompts (PE).

## 3. Points d'attention

- **PE désactivée par défaut** : `enhancer.py` pointe vers l'API Google Gemini
  (hors UE). Laisser `API_KEY = ""`. Ne jamais y envoyer d'image de personne réelle.
- **Coût** : le modèle de base fait 100 étapes de débruitage, compter plusieurs
  minutes de GPU par clip de 10 s. Annoncer le coût de location estimé avant de lancer.
- **RGPD / droit à l'image** : aucun visage ni voix d'une personne réelle
  (mode image→vidéo) sans son accord écrit et daté.
- **IA Act art. 50 §4** : une vidéo réaliste générée par IA (hypertrucage) doit
  être **signalée comme générée par IA** à l'écran et dans la légende.
- **Licence Apache-2.0** : usage commercial autorisé ; vérifier aussi la licence des
  poids tiers embarqués (Qwen3.5, Wan2.2 VAE, Stable Audio Open : la licence
  Stability AI Community est limitée au-delà d'1 M$ de chiffre d'affaires annuel).

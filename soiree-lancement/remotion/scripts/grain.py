"""Génère 8 tuiles de grain argentique (PNG 960×540, agrandis à l’affichage) pour Remotion."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

SORTIE = Path(__file__).resolve().parent.parent / "public" / "grain"
SORTIE.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(974)
for i in range(8):
    bruit = rng.normal(128, 46, (540, 960)).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(bruit, "L").filter(ImageFilter.GaussianBlur(0.5))
    alpha = Image.new("L", img.size, 255)
    Image.merge("RGBA", (img, img, img, alpha)).save(SORTIE / f"grain-{i}.png", optimize=True)
print("grain : 8 tuiles")

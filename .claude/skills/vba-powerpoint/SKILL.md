---
name: vba-powerpoint
description: Écrire ou adapter des macros VBA PowerPoint pour YEBA — contrôle avant soirée (Morphose, vidéos, tailles, texte alternatif, post-it), bascule mode sobre / cinéma des fonds vidéo, nettoyage avant envoi, remise de la Morphose sans casser l'avance automatique.
---

# VBA PowerPoint (v2 — non destructif)

Module de référence : `soiree-lancement/vba/YebaAnimations.bas`. Depuis la v2, animations, Morphose et lecture
vidéo sont DÉJÀ dans le .pptx (python-pptx) : la macro ne les efface jamais.

| Macro | Effet |
|---|---|
| `YebaVerifier` | rapport : slides masquées, vidéos, slides sans Morphose, textes < 20 pt, images sans texte alternatif, post-it |
| `YebaModeSobre` / `YebaModeCinema` | fonds vidéo (`fond-video`) figés sur leur image / relancés en boucle muette |
| `YebaRetirerPostIt` | supprime les post-it rouges hors champ avant d'envoyer le fichier |
| `YebaMorphosePartout` | remet la Morphose (repli fondu) en conservant `AdvanceOnTime` des slides vidéo |

Installation : Alt + F11 → Fichier → Importer → `.bas` ; Alt + F8 → macro ; enregistrer en .pptx.
Sécurité : ne jamais distribuer de .pptm à des clients ; livrer un .pptx sans macro.

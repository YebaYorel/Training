# Dossier DEETS — extension de la déclaration d'activité à l'apprentissage

Réponse au courriel de la DEETS La Réunion du 20/10/2026 (art. L.6351-5 C. trav.).

- `word/` : les pièces Word prêtes à compléter (00 = bordereau + liste de contrôle, 04 à 18 = pièces).
- `src/` : contenu source (`pNN.js`) et générateur (`lib.js`, `build.js`).

Les mentions **surlignées en jaune** `[…]` sont à compléter ou à vérifier avant envoi.
La liste complète est générée automatiquement à la fin de la pièce 00.

Régénérer après modification d'un fichier source :

    cd src && node build.js        # toutes les pièces
    cd src && node build.js 05     # une seule pièce

Couleurs de la charte : constante `COLORS` dans `src/lib.js`.

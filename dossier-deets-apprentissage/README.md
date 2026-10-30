# Dossier DEETS — extension de la déclaration d'activité à l'apprentissage

Réponse au courriel de la DEETS La Réunion du 20/10/2026 (art. L.6351-5 C. trav.).

- `word/` : les pièces Word (00 = bordereau, 04 à 20 = pièces, NOTE_INTERNE = feuille de route et planning de pilotage personnel, ne pas transmettre).
- `pdf/` : les mêmes pièces en PDF (polices intégrées), pour l'envoi.
- `envoi/` : archives ZIP prêtes à joindre à un courriel (dossier DEETS ; programme et planning pour entreprises et partenaires).
- `src/rdv.js` : source unique des 12 Rendez-vous du mois (pièces 15, 16, 18, 19, 20 et notes internes).
- `src/` : contenu source (`pNN.js`) et générateur (`lib.js`, `build.js`).

Les mentions **surlignées en jaune** `[…]` sont à compléter ou à vérifier avant envoi.
La liste complète est générée automatiquement à la fin de la note interne.

Régénérer après modification d'un fichier source :

    cd src && node build.js        # toutes les pièces
    cd src && node build.js 05     # une seule pièce

Couleurs de la charte : constante `COLORS` dans `src/lib.js`.

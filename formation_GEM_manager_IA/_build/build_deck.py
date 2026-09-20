# -*- coding: utf-8 -*-
import sys
from deck_engine import *
import deck_engine
import contenu_matin, contenu_aprem

prs = new_deck()
contenu_matin.construire(prs)
contenu_aprem.construire(prs)
numeroter(prs, depart=2)

if deck_engine.ERREURS:
    print("### CONTROLE ACCESSIBILITE : %d depassement(s)" % len(deck_engine.ERREURS))
    for e in deck_engine.ERREURS:
        print("  " + e)
    sys.exit(1)

sortie = "../01_diaporama/Diaporama_Manager_et_IA_GEM.pptx"
prs.save(sortie)
print("OK - %d diapositives generees" % len(prs.slides._sldIdLst))
print("Aucun depassement : aucune ligne ne coupe un mot, aucun texte hors cadre.")

"""Ajoute des transitions modernes à un .pptx (PowerPoint 2016+ / Microsoft 365).

Exemples :
  python transitions.py entree.pptx sortie.pptx --defaut morph
  python transitions.py entree.pptx sortie.pptx --defaut fondu --diapo 1:vortex --diapo 5:prisme
  python transitions.py --liste

Chaque effet « moderne » est écrit avec un repli (fondu) : une version ancienne
de PowerPoint ou LibreOffice affichera un fondu au lieu de planter.

Astuce Morph : pour qu'un objet « voyage » d'une diapo à l'autre, donnez-lui le
même nom sur les deux diapos, préfixé par « !! » (ex. « !!titre »).
"""
import argparse
import sys

from lxml import etree
from pptx import Presentation

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
NS_P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"

# nom français -> (espace requis, élément XML de l'effet, durée par défaut en ms)
EFFETS = {
    "morph": ("p159", '<p159:morph option="byObject"/>', 1500),
    "morph-mots": ("p159", '<p159:morph option="byWord"/>', 1500),
    "morph-lettres": ("p159", '<p159:morph option="byChar"/>', 1500),
    "prisme": ("p14", "<p14:prism/>", 1600),
    "revelation": ("p14", "<p14:reveal/>", 1800),
    "survol": ("p14", "<p14:flythrough/>", 1200),
    "vortex": ("p14", '<p14:vortex dir="r"/>', 2500),
    "ondulation": ("p14", "<p14:ripple/>", 1400),
    "galerie": ("p14", '<p14:gallery dir="l"/>', 1600),
    "nid-abeille": ("p14", "<p14:honeycomb/>", 2500),
    "convoyeur": ("p14", '<p14:conveyor dir="l"/>', 1600),
    "bascule": ("p14", '<p14:switch dir="r"/>', 1400),
    "retourner": ("p14", '<p14:flip dir="r"/>', 1200),
    "fondu": (None, "<p:fade/>", 700),
    "pousser": (None, '<p:push dir="u"/>', 700),
    "balayer": (None, '<p:wipe dir="r"/>', 700),
    "aucune": (None, None, 0),
}

DECL = f'xmlns:p="{NS_P}" xmlns:mc="{NS_MC}" xmlns:p14="{NS_P14}" xmlns:p159="{NS_P159}"'


def construire(effet: str, duree_ms: int | None):
    ns, xml_effet, dur_def = EFFETS[effet]
    if xml_effet is None:
        return None
    dur = duree_ms or dur_def
    if ns is None:
        spd = "fast" if dur < 600 else ("med" if dur < 900 else "slow")
        return etree.fromstring(f'<p:transition {DECL} spd="{spd}">{xml_effet}</p:transition>')
    xml = (
        f'<mc:AlternateContent {DECL}>'
        f'<mc:Choice Requires="{ns}">'
        f'<p:transition spd="slow" p14:dur="{dur}">{xml_effet}</p:transition>'
        f"</mc:Choice>"
        f'<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback>'
        f"</mc:AlternateContent>"
    )
    return etree.fromstring(xml)


def retirer_transitions(sld):
    for el in list(sld):
        tag = etree.QName(el).localname
        if tag == "transition":
            sld.remove(el)
        elif tag == "AlternateContent" and el.find(f".//{{{NS_P}}}transition") is not None:
            sld.remove(el)


def inserer(sld, element):
    # Ordre imposé par le schéma : cSld, clrMapOvr, transition, timing, extLst
    ancre = None
    for el in sld:
        if etree.QName(el).localname in ("cSld", "clrMapOvr"):
            ancre = el
    if ancre is None:
        sld.insert(0, element)
    else:
        ancre.addnext(element)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entree", nargs="?")
    ap.add_argument("sortie", nargs="?")
    ap.add_argument("--defaut", default="morph", choices=sorted(EFFETS))
    ap.add_argument("--diapo", action="append", default=[], metavar="N:EFFET",
                    help="effet pour une diapo précise (numérotation à partir de 1)")
    ap.add_argument("--duree", type=int, default=None, help="durée en millisecondes (tous effets)")
    ap.add_argument("--sauf-premiere", action="store_true", help="pas de transition sur la diapo 1")
    ap.add_argument("--liste", action="store_true", help="afficher les effets disponibles")
    a = ap.parse_args(argv)

    if a.liste:
        for nom, (ns, _, dur) in sorted(EFFETS.items()):
            print(f"{nom:15s} {'moderne (' + ns + ')' if ns else 'classique':18s} {dur} ms")
        return 0
    if not (a.entree and a.sortie):
        ap.error("entree et sortie sont obligatoires")

    par_diapo = {}
    for spec in a.diapo:
        n, _, eff = spec.partition(":")
        if eff not in EFFETS:
            ap.error(f"effet inconnu : {eff} (voir --liste)")
        par_diapo[int(n)] = eff

    prs = Presentation(a.entree)
    for i, slide in enumerate(prs.slides, start=1):
        eff = par_diapo.get(i, "aucune" if (i == 1 and a.sauf_premiere) else a.defaut)
        sld = slide._element
        retirer_transitions(sld)
        el = construire(eff, a.duree)
        if el is not None:
            inserer(sld, el)
        print(f"diapo {i:2d} : {eff}")
    prs.save(a.sortie)
    print(f"OK -> {a.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

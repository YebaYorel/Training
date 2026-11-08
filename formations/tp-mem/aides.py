"""Petits blocs HTML réutilisables pour les ressources apprenants (schémas sans image externe)."""
import html as _h


def e(t):
    return _h.escape(t, quote=False)


def flux(etapes, titre=None):
    """Schéma en étapes reliées par des flèches. etapes = [(titre, texte), ...]"""
    blocs = []
    for i, (t, x) in enumerate(etapes):
        blocs.append(f'<div class="etape"><div class="num">{i+1}</div><b>{t}</b><span>{x}</span></div>')
        if i < len(etapes) - 1:
            blocs.append('<div class="fl" aria-hidden="true">➜</div>')
    cap = f'<figcaption>{titre}</figcaption>' if titre else ''
    return f'<figure class="schema"><div class="flux">{"".join(blocs)}</div>{cap}</figure>'


def cartes(items, titre=None, cols=3):
    c = "".join(f'<div class="carte"><b>{t}</b><span>{x}</span></div>' for t, x in items)
    cap = f'<figcaption>{titre}</figcaption>' if titre else ''
    return f'<figure class="schema"><div class="cartes c{cols}">{c}</div>{cap}</figure>'


def encadre(kind, contenu, titre=None):
    noms = {"retenir": "À retenir", "ex": "Exemple péi (974)", "piege": "Le piège à éviter",
            "loi": "RGPD / IA Act / Droit", "jury": "Côté jury", "astuce": "Astuce de pro", "def": "Définition"}
    return f'<aside class="enc {kind}"><p class="et">{titre or noms[kind]}</p>{contenu}</aside>'


def tableau(entetes, lignes, cls=""):
    th = "".join(f"<th>{x}</th>" for x in entetes)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in lignes)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def pyramide(niveaux, titre=None):
    """niveaux du haut vers le bas : [(titre, texte)]"""
    n = len(niveaux)
    rows = "".join(
        f'<div class="niv" style="width:{40 + 60 * i / max(n - 1, 1):.0f}%"><b>{t}</b> — {x}</div>'
        for i, (t, x) in enumerate(niveaux))
    cap = f'<figcaption>{titre}</figcaption>' if titre else ''
    return f'<figure class="schema"><div class="pyr">{rows}</div>{cap}</figure>'


def matrice(axe_x, axe_y, cases, titre=None):
    """cases = 4 tuples (titre, texte) dans l'ordre haut-gauche, haut-droite, bas-gauche, bas-droite"""
    c = "".join(f'<div class="case"><b>{t}</b><span>{x}</span></div>' for t, x in cases)
    cap = f'<figcaption>{titre}</figcaption>' if titre else ''
    return (f'<figure class="schema"><div class="mat-wrap"><div class="axe-y">{axe_y}</div>'
            f'<div><div class="mat">{c}</div><div class="axe-x">{axe_x}</div></div></div>{cap}</figure>')

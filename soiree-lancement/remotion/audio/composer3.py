"""Bande-son du générique v3 « La graine » — 100 % synthèse locale, aucun échantillon ni musique tierce.

Pulsation ternaire (12/8, 80 temps/min) inspirée du maloya réunionnais : kayamb (hochet en radeau, ici bruit
filtré en triolets) et roulèr (gros tambour joué à mains nues : coup ouvert grave + claqué). Harmonie : ré mineur,
Ré m – Si♭ – Fa – Do, résolution finale en Fa majeur. Tous les événements (battements, impacts, souffles, montées,
pluie de graines, tics du compteur, carillons des mots) sont lus dans ../src/v3/timeline3.json : image et son calés.

    python3 audio/composer3.py      → public/audio/generique-v3.wav (−16 LUFS, crête −1,5 dBTP)
"""
import json
from pathlib import Path

import numpy as np

from composer import (SR, basse, battement, bruit_filtre, claque, charleston, env_exp, hz, impact, kick, masteriser,
                      montee, nappe, passe_bas, passe_haut, poser, reverberation, scie, souffle)

ICI = Path(__file__).resolve().parent
T = json.loads((ICI.parent / "src" / "v3" / "timeline3.json").read_text(encoding="utf-8"))
SORTIE = ICI.parent / "public" / "audio" / "generique-v3.wav"
DUREE = T["duree"]
CROCHE = T["tempo"]["temps_s"] / 3          # 0,25 s
MESURE = T["tempo"]["mesure_s"]             # 3 s = 12 croches
rng = np.random.default_rng(1974)

# ré mineur pentatonique (carillons, kalimba) et grille d'accords (2 mesures = 6 s par accord)
PENTA = [62, 65, 67, 69, 72, 74, 77, 79, 81, 84, 86]
ACCORDS = {"Dm": [50, 57, 62, 65, 69], "Bb": [46, 53, 58, 62, 65], "F": [41, 48, 57, 60, 65], "C": [48, 55, 60, 64, 67],
           "Fadd9": [41, 48, 53, 57, 60, 67, 69]}
BASSES = {"Dm": 38, "Bb": 34, "F": 41, "C": 36, "Fadd9": 29}
GRILLE = ["Dm", "Bb", "F", "C"]


def accord_a(t):
    if t >= 74.25:
        return "Fadd9"
    return GRILLE[int(t // (2 * MESURE)) % 4]


def section(t):
    for s in T["son"]["sections"]:
        if s["de"] <= t < s["a"]:
            return s["type"]
    return "final"


# ───────────────────────────── instruments ─────────────────────────────

def kayamb(force=1.0):
    """Hochet du maloya : souffle de graines, attaque douce, queue courte (bruit 3–9 kHz)."""
    d = 0.16
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bruit_filtre(d, lambda tt: np.full_like(tt, 6200.0), 0.55)[:n]
    env = np.clip(t / 0.012, 0, 1) * np.exp(-np.maximum(0, t - 0.012) * 34)
    return x * env * force


def rouler_ouvert(force=1.0):
    """Roulèr, coup ouvert : peau grave qui chante (corps 68 Hz glissant) + attaque de main."""
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 64 + 38 * np.exp(-t * 16)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5.2)
    peau = passe_bas(rng.standard_normal(n), 1200) * np.exp(-t * 40) * 0.35
    return np.tanh(1.3 * (corps + peau)) * force


def rouler_claque(force=1.0):
    """Roulèr, claqué : main sèche sur le bord (bruit 700–2 500 Hz, très court)."""
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    x = bruit_filtre(0.22, lambda tt: np.full_like(tt, 1300.0), 0.6)[:n]
    corps = 0.3 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30)
    return (x * np.exp(-t * 32) + corps) * force


def cloche(midi, duree=2.6, brillance=3.2):
    """Cloche FM (porteuse/modulante 1:3,5) : le motif « graine »."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    indice = brillance * np.exp(-t * 3.5)
    x = np.sin(2 * np.pi * f * t + indice * np.sin(2 * np.pi * 3.5 * f * t))
    return x * env_exp(n, 1.5, 0.002)


def kalimba(midi, duree=1.3):
    """Lamelle pincée (kalimba / marimba) : partiels 1 · 3,93 · 9 à décroissances différentes."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.45 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t * 14)
         + 0.18 * np.sin(2 * np.pi * 9.0 * f * t) * np.exp(-t * 40))
    return x * np.clip(t / 0.002, 0, 1)


def voix(midis, duree, attaque=1.2, relache=2.0):
    """Nappe « chœur » : scies désaccordées passées dans trois formants de voyelle « a »."""
    brut = nappe(midis, duree, attaque, relache)
    from scipy import signal
    out = np.zeros_like(brut)
    for fc, q, g in ((800, 6, 1.0), (1150, 7, 0.7), (2900, 9, 0.35)):
        b, a = signal.iirpeak(fc, q, fs=SR)
        out += g * signal.lfilter(b, a, brut, axis=-1)
    return 0.6 * out + 0.5 * brut


def stab(midis, duree=0.9):
    """Accord-impact (cuivres synthétiques) : scies, attaque franche, filtre qui se referme."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in midis:
        for dec in (-6, 0, 6):
            x += scie(hz(m) * 2 ** (dec / 1200), n, rng.random())
    x /= len(midis) * 3
    from scipy import signal
    y = np.zeros(n)
    # filtre passe-bas glissant par blocs (2 400 → 500 Hz)
    blocs = 24
    for k in range(blocs):
        a, b = k * n // blocs, (k + 1) * n // blocs
        fc = 2400 * (500 / 2400) ** (k / blocs)
        sos = signal.butter(2, fc, "low", fs=SR, output="sos")
        y[a:b] = signal.sosfilt(sos, x[max(0, a - 2000):b])[-(b - a):]
    return y * env_exp(n, 3.2, 0.004)


def tic():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 110) * 0.7 + passe_haut(rng.standard_normal(n), 4000) * np.exp(-t * 220) * 0.3


def gonflement(duree):
    """Souffle inversé : monte en crescendo et s'arrête net sur le temps (aspiration avant un impact)."""
    x = bruit_filtre(duree, lambda tt: 600 + 5000 * (tt / duree) ** 2, 0.5)
    t = np.arange(len(x)) / SR
    return x * (t / duree) ** 3


def scintillement(duree):
    """Halo aigu de la graine : grappe de sinus (ré 6, la 6) avec trémolo lent."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * hz(m) * t + rng.random() * 6) for m in (86, 93, 98)) / 3
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 0.45 * t)
    return x * trem * np.clip(t / (duree * 0.7), 0, 1) * np.clip((duree - t) / 0.4, 0, 1)


# ───────────────────────────── composition ─────────────────────────────

def composer():
    pistes = {k: np.zeros((2, int((DUREE + 4) * SR))) for k in ("batterie", "basse", "nappes", "fx", "humide")}
    bat, bas, nap, fx, hum = (pistes[k] for k in ("batterie", "basse", "nappes", "fx", "humide"))
    S = T["son"]

    # 0. graine : battements, halo, anneau, aspiration avant l'explosion
    for b in S["battements"]:
        poser(bat, battement(), b, -4)
    poser(nap, scintillement(4.4), 0.3, -20)
    poser(hum, cloche(93, 3.0, 2.0), S["anneau"], -14)
    poser(fx, gonflement(1.1), 3.4, -12)

    # 1. impacts, souffles, montées
    for imp in S["impacts"]:
        poser(fx, impact(imp["force"]), imp["t"], -3 + 4 * np.log10(imp["force"]))
        poser(hum, impact(imp["force"]), imp["t"], -15)
        if imp["force"] >= 1.0:  # silence d'une croche avant le choc : l'impact claque
            i0, i1 = int((imp["t"] - 0.14) * SR), int(imp["t"] * SR)
            for p in (bat, bas, nap):
                p[:, i0:i1] *= np.linspace(1, 0.15, i1 - i0)
    for t0 in S["souffles"]:
        poser(fx, souffle(1.2), t0 - 0.6, -9)
    for a, b in S["montees"]:
        poser(fx, montee(b - a), a, -9)
        poser(fx, gonflement(min(1.4, b - a)), b - min(1.4, b - a), -13)

    # 2. pluie de graines (baobab → île) : carillons aigus qui « tombent »
    p0, p1 = S["pluie"]
    for j in range(46):
        t = p0 + (p1 - p0) * (j / 46) + rng.uniform(-0.05, 0.05)
        m = PENTA[max(0, len(PENTA) - 1 - int(j / 46 * 7) - int(rng.integers(0, 4)))] + 12
        poser(hum, cloche(m, 1.6, 1.6), t, -24 + rng.uniform(-4, 2), pan=rng.uniform(-0.8, 0.8))

    # 3. carillons des mots (motif de la graine) et tics du compteur
    for j, t in enumerate(S["carillons"]):
        m = PENTA[(j * 3 + 5) % len(PENTA)] + (12 if j % 4 == 3 else 0)
        poser(hum, cloche(m), t, -17, pan=0.25 * np.sin(j))
        poser(fx, cloche(m, 1.2, 1.0), t, -24)
    a, b, n = S["tics"]
    for k in range(1, n + 1):
        poser(fx, tic(), a + (b - a) * k / n, -16 + k * 0.6)

    # 4. trame rythmique par croche (12/8) selon la section
    nb = int(DUREE / CROCHE)
    for c in range(nb):
        t = c * CROCHE
        pos = c % 12
        sec = section(t)
        hum_t = t + rng.normal(0, 0.004)
        temps = pos % 3 == 0
        if sec in ("silence",):
            continue
        # kayamb : les 12 croches, accent sur chaque temps
        k_force = {"eveil": 0.35 * np.clip((t - 6.0) / 3, 0, 1), "montee": 0.75, "plein": 1.0, "baobab": 0.6, "marche": 1.0,
                   "confiance": 0.45, "final": 0.5 * np.clip((78.5 - t) / 2, 0, 1)}.get(sec, 0)
        if k_force > 0:
            poser(bat, kayamb(k_force * (1.0 if temps else 0.55)), hum_t, -14, pan=-0.35 if pos % 2 else 0.35)
        # roulèr : coups ouverts sur les temps, claqués en contretemps (motif roulant du maloya)
        if sec in ("plein", "marche", "montee") or (sec == "eveil" and t >= 9.0) or sec == "baobab":
            leger = sec in ("eveil", "baobab")
            if pos in (0, 6) or (pos in (3, 9) and not leger):
                poser(bat, rouler_ouvert(1.0 if pos in (0, 6) else 0.7), hum_t, -8 if not leger else -13)
            elif pos in (2, 5, 8, 11) and not leger:
                poser(bat, rouler_claque(0.8 if pos in (5, 11) else 0.55), hum_t, -12, pan=0.2)
            if sec == "montee" and pos in (1, 4, 7, 10):
                gain = -20 + 12 * ((t % 6) / 6)
                poser(bat, rouler_claque(0.6), hum_t, gain, pan=-0.2)
        # grosse caisse et claquements
        if sec in ("plein", "marche"):
            if pos in ((0, 3, 6, 9) if sec == "marche" else (0, 6)):
                poser(bat, kick(), t, -5)
            if pos in (3, 9) and sec == "plein":
                poser(bat, claque(), t, -11)
            if sec == "marche" and pos in (1, 4, 7, 10):
                poser(bat, charleston(), hum_t, -19)
        # basse
        ac = accord_a(t)
        if sec in ("plein", "marche", "montee"):
            if pos in (0, 6, 9) or (sec == "marche" and pos == 3):
                m = BASSES[ac] + (7 if pos == 9 else 0)
                poser(bas, basse_courte_v3(m, 0.55), t, -9)
        elif sec in ("eveil", "baobab", "confiance") and pos == 0 and c % 24 == 0:
            poser(bas, basse(BASSES[ac], 2 * MESURE - 0.5), t, -14)
        # kalimba (baobab) : arpèges pentatoniques
        if sec == "baobab" and pos in (0, 2, 3, 5, 6, 8, 9, 11):
            note = PENTA[(c * 5 + (c // 12)) % 7]
            poser(hum, kalimba(note), hum_t, -21, pan=rng.uniform(-0.5, 0.5))
            poser(nap, kalimba(note), hum_t, -18, pan=rng.uniform(-0.5, 0.5))

    # 5. nappes : un accord toutes les 2 mesures, plus présentes dans les grandes sections
    t = 4.5
    while t < 74.25:
        fin = min(74.25, (np.floor(t / (2 * MESURE)) + 1) * 2 * MESURE)
        ac = accord_a(t)
        g = {"eveil": -15, "montee": -14, "plein": -13, "baobab": -12, "marche": -15, "confiance": -11}.get(section(t), -14)
        poser(nap, nappe(ACCORDS[ac], fin - t, attaque=1.0, relache=1.6), t, g)
        t = fin
    poser(nap, voix(ACCORDS["Dm"], 4.0, 0.05, 2.5), 15.75, -11)
    poser(nap, voix(ACCORDS["F"], 5.5, 0.05, 2.5), 35.25, -12)

    # 6. verbes : accords-impacts ; jalons : coup de roulèr + cloche grave
    for t0, ac in ((54.0, "Dm"), (55.0, "Bb"), (56.0, "F")):
        poser(fx, stab(ACCORDS[ac][1:]), t0, -11)
        poser(hum, stab(ACCORDS[ac][1:]), t0, -18)
    for t0 in (43.0, 45.0, 47.0, 49.0):
        poser(bat, rouler_ouvert(1.0), t0, -6)
        poser(hum, cloche(62, 3.0, 2.5), t0, -16)

    # 7. final : l'emblème naît (Fa majeur add9, chœur, longue réverbération), puis le slogan
    poser(nap, voix(ACCORDS["Fadd9"], 4.8, 0.03, 1.2), 74.25, -8)
    poser(hum, voix(ACCORDS["Fadd9"], 4.8, 0.03, 1.2), 74.25, -14)
    poser(bas, basse(BASSES["Fadd9"], 4.8), 74.25, -9)
    for j, m in enumerate((77, 81, 84, 89)):
        poser(hum, cloche(m, 3.5, 2.6), 74.25 + 0.09 * j, -15, pan=-0.45 + 0.3 * j)

    # 8. ducking : nappes et basse s'effacent légèrement sous la grosse caisse et le roulèr ouvert
    env = np.ones(bat.shape[1])
    for c in range(nb):
        t = c * CROCHE
        if section(t) in ("plein", "marche") and c % 3 == 0:
            i = int(t * SR)
            L = int(0.22 * SR)
            if i + L < len(env):
                env[i:i + L] = np.minimum(env[i:i + L], 1 - 0.32 * np.exp(-np.arange(L) / (0.07 * SR)))
    nap *= env
    bas *= 0.6 + 0.4 * env

    sec_ = bat + bas + nap + fx
    humide = reverberation(hum + 0.35 * nap + 0.25 * fx, duree=3.4, predelai=0.025)
    n = int(DUREE * SR)
    sec_, humide = sec_[:, :n], humide[:, :n]
    fondu = np.clip((DUREE - np.arange(n) / SR) / 0.9, 0, 1) ** 1.5
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    masteriser(sec_ * fondu, humide * fondu, SORTIE, cible_lufs=-16)
    print(f"Bande-son v3 : {SORTIE.relative_to(ICI.parent)} ({DUREE:.0f} s)")


def basse_courte_v3(midi, duree=0.5):
    """Basse ronde et percussive, un peu plus longue que celle de la v2 (ternaire)."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = 0.8 * np.sin(2 * np.pi * f * t) + 0.35 * passe_bas(scie(f, n), 380) + 0.2 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.6 * x) * env_exp(n, 4.5, 0.006)


if __name__ == "__main__":
    composer()

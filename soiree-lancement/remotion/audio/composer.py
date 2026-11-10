"""Compose la bande-son du générique et le « sting » des cartes d'épisode — 100 % synthèse locale.

Aucune musique, aucun échantillon tiers : pas de droits d'auteur à gérer (ni SACEM, ni licence).
La chronologie (impacts, souffles, montées, accords, tempo du montage) est lue dans
../src/timeline.json : c'est le même fichier que la vidéo, l'image et le son restent calés.

    python3 audio/composer.py      → public/audio/generique.wav et public/audio/sting.wav
"""
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.io import wavfile

ICI = Path(__file__).resolve().parent
T = json.loads((ICI.parent / "src" / "timeline.json").read_text(encoding="utf-8"))
SORTIE = ICI.parent / "public" / "audio"
SR = 48000
FPS = T["fps"]
rng = np.random.default_rng(974)


def s(image):
    """Image (à 30 i/s) → secondes."""
    return image / FPS


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def vide(duree):
    return np.zeros((2, int(duree * SR)))


def poser(piste, son, t, gain_db=0.0, pan=0.0):
    """Ajoute `son` (mono ou stéréo) dans `piste` à l'instant t (s), avec gain et panoramique."""
    g = 10 ** (gain_db / 20)
    if son.ndim == 1:
        gauche = np.sqrt(0.5 * (1 - pan))
        droite = np.sqrt(0.5 * (1 + pan))
        son = np.vstack([son * gauche, son * droite]) * np.sqrt(2)
    i = int(t * SR)
    if i >= piste.shape[1]:
        return
    n = min(son.shape[1], piste.shape[1] - i)
    if i < 0:
        son = son[:, -i:]
        n = min(son.shape[1], piste.shape[1])
        i = 0
    piste[:, i : i + n] += son[:, :n] * g


def env_exp(n, decroissance, attaque=0.003):
    t = np.arange(n) / SR
    a = np.clip(t / attaque, 0, 1)
    return a * np.exp(-t * decroissance)


def passe_bas(x, fc, ordre=2):
    sos = signal.butter(ordre, fc, "low", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=-1)


def passe_haut(x, fc, ordre=2):
    sos = signal.butter(ordre, fc, "high", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=-1)


def bruit_filtre(duree, centres, largeur_rel=0.7):
    """Bruit blanc filtré par une bande dont le centre suit la courbe `centres(t)` (filtrage spectral)."""
    n = int(duree * SR)
    x = rng.standard_normal(n)
    f, tt, Z = signal.stft(x, fs=SR, nperseg=1024)
    fc = centres(tt)[None, :]
    masque = np.exp(-0.5 * ((f[:, None] - fc) / (fc * largeur_rel)) ** 2)
    _, y = signal.istft(Z * masque, fs=SR, nperseg=1024)
    y = y[:n]
    return y / (np.max(np.abs(y)) + 1e-9)


def scie(freq, n, phase0=0.0):
    ph = (phase0 + np.cumsum(np.full(n, freq) / SR)) % 1.0
    return 2.0 * ph - 1.0


# ───────────────────────────── sons élémentaires ─────────────────────────────

def battement():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    f = 44 + 30 * np.exp(-t * 18)
    coup = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 11, 0.004)
    second = np.zeros(n)
    k = int(0.2 * SR)
    second[k:] = 0.55 * coup[: n - k]
    return coup + second


def ping(midi, duree=1.8):
    n = int(duree * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 3.01 * f * t)
    return x * env_exp(n, 2.6, 0.002)


def souffle(duree=1.1):
    t_c = duree * 0.55

    def centres(tt):
        return np.where(tt < t_c, 350 + 2400 * (tt / t_c) ** 1.5, 2750 - 2100 * ((tt - t_c) / (duree - t_c)))

    x = bruit_filtre(duree, centres, 0.6)
    t = np.arange(len(x)) / SR
    enveloppe = np.exp(-0.5 * ((t - t_c) / (duree * 0.2)) ** 2)
    x = x * enveloppe
    pan = np.linspace(-0.8, 0.8, len(x))
    return np.vstack([x * np.sqrt(0.5 * (1 - pan)), x * np.sqrt(0.5 * (1 + pan))]) * np.sqrt(2)


def montee(duree):
    x = bruit_filtre(duree, lambda tt: 220 * (8000 / 220) ** np.clip(tt / duree, 0, 1), 0.45)
    n = len(x)
    t = np.arange(n) / SR
    gain = (t / duree) ** 2.2
    f = 140 * (1200 / 140) ** (t / duree)
    glisse = 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR)
    y = (x * 0.9 + glisse) * gain
    y[-int(0.03 * SR) :] *= np.linspace(1, 0, int(0.03 * SR))
    return y


def impact(force=1.0):
    duree = 3.2
    n = int(duree * SR)
    t = np.arange(n) / SR
    f_sub = 34 + 70 * np.exp(-t * 5)
    sub = np.sin(2 * np.pi * np.cumsum(f_sub) / SR) * np.exp(-t * 1.6)
    f_mid = 58 + 120 * np.exp(-t * 22)
    mid = 0.6 * np.sin(2 * np.pi * np.cumsum(f_mid) / SR) * np.exp(-t * 7)
    craque = passe_bas(rng.standard_normal(n), 3800) * np.exp(-t * 26) * 0.9
    return np.tanh(1.4 * (sub + mid + craque)) * force


def clic(freq=3800):
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    x = passe_haut(rng.standard_normal(n), 2500) * np.exp(-t * 180) * 0.6 + np.sin(2 * np.pi * freq * t) * np.exp(-t * 90) * 0.5
    return x


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 44 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 9, 0.001)


def charleston():
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    return passe_haut(rng.standard_normal(n), 7500) * np.exp(-t * 70)


def claque():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    x = bruit_filtre(0.18, lambda tt: np.full_like(tt, 2200.0), 0.5)[:n]
    return x * np.exp(-t * 28)


ACCORDS = {
    "Am": [57, 60, 64, 69],
    "F": [53, 57, 60, 65],
    "C": [48, 55, 60, 64],
    "G": [55, 59, 62, 67],
    "Cfin": [48, 55, 60, 64, 74],
}
BASSES = {"Am": 33, "F": 29, "C": 36, "G": 31, "Cfin": 36}


def nappe(midis, duree, attaque=1.4, relache=1.8):
    """Nappe cinématographique : scies désaccordées, filtrées, avec léger souffle."""
    n = int((duree + relache) * SR)
    t = np.arange(n) / SR
    g = np.zeros(n)
    d = np.zeros(n)
    for m in midis:
        f = hz(m)
        for dec, cote in ((-7, "g"), (0, "c"), (7, "d")):
            v = scie(f * 2 ** (dec / 1200), n, rng.random())
            if cote == "g":
                g += v
            elif cote == "d":
                d += v
            else:
                g += 0.7 * v
                d += 0.7 * v
        g += 0.35 * np.sin(2 * np.pi * 2 * f * t)
        d += 0.35 * np.sin(2 * np.pi * 2 * f * t + 0.4)
    stereo = passe_bas(np.vstack([g, d]), 1300, 2)
    env = np.clip(t / attaque, 0, 1) * np.clip((duree + relache - t) / relache, 0, 1)
    lfo = 1 + 0.06 * np.sin(2 * np.pi * 0.17 * t)
    return stereo * env * lfo / (len(midis) * 3)


def basse(midi, duree):
    n = int((duree + 1.0) * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    env = np.clip(t / 0.8, 0, 1) * np.clip((duree + 1.0 - t) / 1.0, 0, 1)
    return np.tanh(1.2 * x) * env


def basse_courte(midi, duree=0.3):
    """Note de basse percussive pour le montage (attaque franche, décroissance rapide)."""
    n = int(duree * SR)
    t = np.arange(n) / SR
    f = hz(midi)
    x = 0.7 * np.sin(2 * np.pi * f * t) + 0.5 * passe_bas(scie(f, n), 420)
    return np.tanh(1.5 * x) * env_exp(n, 7, 0.004)


def reverberation(x, duree=2.8, predelai=0.02):
    n = int(duree * SR)
    t = np.arange(n) / SR
    ir = np.zeros((2, n + int(predelai * SR)))
    for c in range(2):
        b = rng.standard_normal(n) * np.exp(-t * (6.9 / duree))
        ir[c, int(predelai * SR) :] = passe_bas(b, 6500)
    ir /= np.sqrt(np.sum(ir**2, axis=1, keepdims=True)) + 1e-9
    y = np.vstack([signal.fftconvolve(x[c], ir[c])[: x.shape[1]] for c in range(2)])
    return y


def masteriser(sec, humide, chemin, cible_lufs=-16):
    mix = sec + 0.55 * humide
    mix = passe_haut(mix, 28, 2)
    mix = np.tanh(1.1 * mix / (np.max(np.abs(mix)) + 1e-9)) * 0.9
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 10 ** (-1.0 / 20)
    with tempfile.TemporaryDirectory() as d:
        brut = Path(d) / "brut.wav"
        wavfile.write(brut, SR, (mix.T * 32767).astype(np.int16))
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", str(brut), "-af", f"loudnorm=I={cible_lufs}:TP=-1.5:LRA=11", "-ar", str(SR), "-c:a", "pcm_s16le", str(chemin)],
            check=True,
        )


# ───────────────────────────── générique (80 s) ─────────────────────────────

def generique():
    duree = s(T["duree"])
    sec = vide(duree + 3)
    humide = vide(duree + 3)

    # Bourdon de la (55 / 110 Hz) qui porte toute la pièce
    n = sec.shape[1]
    t = np.arange(n) / SR
    bourdon = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 110 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t))
    bourdon *= np.clip(t / 4, 0, 1) * np.clip((duree + 0.5 - t) / 3, 0, 1)
    poser(sec, bourdon, 0, -24)

    # Nappes d'accords (i – VI – III – VII) et basses
    accords = T["accords"]
    for k, (debut, nom) in enumerate(accords):
        if nom == "bourdon":
            continue
        fin = accords[k + 1][0] if k + 1 < len(accords) else T["duree"]
        nom_reel = "Cfin" if debut >= 2200 else nom
        d = s(fin - debut)
        poser(sec, nappe(ACCORDS[nom_reel], d), s(debut), -15 if debut < 2200 else -11)
        poser(humide, nappe(ACCORDS[nom_reel], d), s(debut), -20)
        poser(sec, basse(BASSES[nom_reel], d), s(debut), -21)

    # Battements de cœur de l'étincelle
    for b in T["battements"]:
        poser(sec, battement(), s(b), -13)

    # Une note par étoile qui s'allume (pentatonique de la mineur)
    notes = [81, 84, 86, 88, 91, 93]
    for i, f in enumerate(T["pops"]):
        poser(humide, ping(notes[i % len(notes)] + (12 if i % 7 == 6 else 0)), s(f), -20, pan=float(rng.uniform(-0.7, 0.7)))
        poser(sec, ping(notes[i % len(notes)]), s(f), -30)

    # Souffles de transition (centrés sur l'image indiquée)
    for w in T["whooshes"]:
        son = souffle(1.1)
        poser(sec, son, s(w) - 0.6, -13)
        poser(humide, son, s(w) - 0.6, -22)

    # Montées puis impacts
    for a, b in T["risers"]:
        poser(sec, montee(s(b - a)), s(a), -17)
    for imp in T["impacts"]:
        son = impact(imp["force"])
        poser(sec, son, s(imp["f"]), -4)
        poser(humide, son, s(imp["f"]), -12)

    # Odomètre, mots, panneaux, compteur
    for f in T["odometre"]:
        poser(sec, clic(3600), s(f), -24, pan=0.15)
    for i, f in enumerate(T["mots"]):
        poser(humide, ping([69, 72, 76, 81, 72, 76, 79][i % 7], 0.9), s(f), -18)
    for f in T["panneaux"]:
        poser(sec, kick() * 0.6, s(f), -16)
        poser(sec, souffle(0.5), s(f) - 0.28, -20)
    a, b = T["compteur"]
    for j, f in enumerate(np.linspace(a, b, 11)):
        poser(sec, clic(2400 + 160 * j), s(f), -22)

    # Montage des formations : 120 BPM, une formation par temps
    m = T["montage"]
    for k in range(m["n"]):
        temps = s(m["debut"] + k * m["pas"])
        poser(sec, kick(), temps, -7)
        poser(sec, claque(), temps, -19)
        poser(sec, charleston(), temps + s(m["pas"]) / 2, -22)
        for d8 in (0, 0.5):
            poser(sec, basse_courte(33 if k < 8 else 31), temps + d8 * s(m["pas"]), -13)

    # « Bientôt », tuiles de la confiance, scintillements
    for i, midi in enumerate((81, 84, 88)):
        poser(humide, ping(midi), s(T["bientot"]) + i * 0.05, -14)
    for i, f in enumerate(T["tuiles_confiance"]):
        poser(humide, ping([72, 76, 79][i], 1.2), s(f), -17)
    for f in T["scintillements"]:
        for j, midi in enumerate((81, 84, 86, 88, 91, 93)):
            poser(humide, ping(midi, 1.4), s(f) + j * 0.06, -22, pan=-0.6 + 0.24 * j)

    # « À suivre… » : trois petits points sonores
    for j in range(3):
        poser(humide, ping(88 - j * 3, 0.8), s(2330) + j * 0.22, -24)

    humide = reverberation(humide, 3.2)
    sec = sec[:, : int(duree * SR)]
    humide = humide[:, : int(duree * SR)]
    fondu = np.clip((duree - np.arange(sec.shape[1]) / SR) / 1.2, 0, 1)
    masteriser(sec * fondu, humide * fondu, SORTIE / "generique.wav")


# ───────────────────────────── sting des cartes d'épisode (4,5 s) ─────────────────────────────

def sting():
    duree = 4.5
    sec = vide(duree + 3)
    humide = vide(duree + 3)
    poser(sec, souffle(0.9), 0.0, -12)
    poser(sec, impact(0.45), 1.0, -8)
    poser(humide, impact(0.45), 1.0, -16)
    for i, midi in enumerate((81, 88, 84, 93)):
        poser(humide, ping(midi), 1.0 + i * 0.07, -15, pan=-0.4 + 0.27 * i)
    poser(sec, nappe(ACCORDS["Am"], 3.2, attaque=0.5, relache=0.8), 0.3, -16)
    humide = reverberation(humide, 2.6)[:, : int(duree * SR)]
    sec = sec[:, : int(duree * SR)]
    fondu = np.clip((duree - np.arange(sec.shape[1]) / SR) / 0.6, 0, 1)
    masteriser(sec * fondu, humide * fondu, SORTIE / "sting.wav", cible_lufs=-17)


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    generique()
    sting()
    print("Bande-son : public/audio/generique.wav, public/audio/sting.wav")

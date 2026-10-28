"""Sauvegarde et restauration des données (pour changer d'ordinateur).

* `sauvegarder` : une archive ZIP datée de `donnees_yeba/` + une empreinte
  SHA-256 de chaque fichier (manifeste), pour vérifier que rien n'a été
  abîmé ou modifié pendant le transfert (clé USB, e-mail, cloud…).
* `restaurer` : contrôle l'archive AVANT de l'ouvrir (chemins piégés, taille,
  empreintes) ; les données actuelles éventuelles sont mises de côté, jamais
  écrasées.

L'archive contient vos projets et le mot de passe HACHÉ (pas le mot de passe
lui-même). Conservez-la comme un document confidentiel.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from .securite import FichierRefuse, restreindre_droits

MANIFESTE = "MANIFESTE_SHA256.json"
TAILLE_MAX_RESTAURATION = 2 * 1024 * 1024 * 1024   # 2 Go décompressés
EXCLUS = {"erreurs.log", "erreurs.log.1"}


def _empreinte(donnees: bytes) -> str:
    return hashlib.sha256(donnees).hexdigest()


def sauvegarder(base: Path, dossier_cible: Path) -> Path:
    dossier_cible.mkdir(parents=True, exist_ok=True)
    cible = dossier_cible / f"Sauvegarde_decorticage_{dt.datetime.now():%Y-%m-%d_%Hh%M}.zip"
    manifeste = {}
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(base.rglob("*")):
            if not f.is_file() or f.name in EXCLUS or f.name.startswith("_reception") or f.suffix == ".tmp":
                continue
            rel = f.relative_to(base).as_posix()
            donnees = f.read_bytes()
            manifeste[rel] = _empreinte(donnees)
            z.writestr(rel, donnees)
        z.writestr(MANIFESTE, json.dumps({"date": dt.datetime.now().isoformat(timespec="seconds"),
                                          "fichiers": manifeste}, indent=2))
    restreindre_droits(cible)
    return cible


def verifier_archive(chemin: Path) -> dict:
    """Contrôle complet sans rien écrire. Retourne le manifeste."""
    try:
        with zipfile.ZipFile(chemin) as z:
            noms = z.namelist()
            if MANIFESTE not in noms:
                raise FichierRefuse("Ce fichier n'est pas une sauvegarde du logiciel (manifeste absent).")
            total = 0
            for info in z.infolist():
                n = info.filename
                if n.startswith("/") or "\\" in n or ".." in n.split("/") or ":" in n:
                    raise FichierRefuse("Sauvegarde piégée : chemin interdit.")
                total += info.file_size
            if total > TAILLE_MAX_RESTAURATION:
                raise FichierRefuse("Sauvegarde anormalement volumineuse.")
            manifeste = json.loads(z.read(MANIFESTE))["fichiers"]
            for n in noms:
                if n == MANIFESTE:
                    continue
                if n not in manifeste or _empreinte(z.read(n)) != manifeste[n]:
                    raise FichierRefuse(f"Sauvegarde abîmée ou modifiée : {n}")
            if set(manifeste) - set(noms):
                raise FichierRefuse("Sauvegarde incomplète : des fichiers manquent.")
            return manifeste
    except zipfile.BadZipFile as exc:
        raise FichierRefuse("Fichier de sauvegarde corrompu.") from exc


def restaurer(chemin: Path, base: Path) -> Path | None:
    """Restaure une sauvegarde dans `base`. Retourne le dossier des anciennes données mises de côté."""
    manifeste = verifier_archive(chemin)
    mis_de_cote = None
    if base.exists() and any(base.iterdir()):
        mis_de_cote = base.with_name(f"{base.name}_ancien_{dt.datetime.now():%Y-%m-%d_%Hh%M%S}")
        shutil.move(str(base), str(mis_de_cote))
    base.mkdir(parents=True, exist_ok=True)
    restreindre_droits(base)
    with zipfile.ZipFile(chemin) as z:
        for rel in manifeste:
            dest = (base / rel).resolve()
            if base.resolve() not in dest.parents:
                raise FichierRefuse("Chemin interdit dans la sauvegarde.")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(rel))
            restreindre_droits(dest)
    for d in base.rglob("*"):
        if d.is_dir():
            restreindre_droits(d)
    return mis_de_cote

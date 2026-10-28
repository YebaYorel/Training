"""Interface locale (navigateur) — réservée à l'utilisateur de l'ordinateur.

Sécurité de l'interface :
* écoute UNIQUEMENT sur 127.0.0.1 (jamais visible du réseau, même en Wi-Fi) ;
* mot de passe obligatoire (PBKDF2, blocage progressif après 5 échecs) ;
* cookie de session aléatoire, HttpOnly, SameSite=Strict, expiration 30 min
  d'inactivité ;
* jeton anti-CSRF sur chaque formulaire + contrôle de l'en-tête Origin ;
* contrôle de l'en-tête Host (protection contre le « DNS rebinding ») ;
* en-têtes stricts : Content-Security-Policy sans script, X-Frame-Options,
  nosniff, no-referrer, no-store ;
* téléchargements limités aux fichiers du projet (pas de « ../ ») ;
* fichiers reçus contrôlés (signature, taille, macros, bombes ZIP) ; logo
  ré-encodé (supprime tout contenu caché dans l'image).
Aucune bibliothèque web externe : moins de dépendances = moins de failles.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import secrets
import shutil
import threading
import time
import traceback
import urllib.parse
import webbrowser
from email import policy
from email.parser import BytesParser
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional

from . import audit
from .config import Charte, Reglages, charger_charte, dossier_donnees, enregistrer_charte
from .moteur import analyser_documents, construire_contexte, generer_sorties, publier_sur_site, retirer_du_site
from .publication import CHOIX, PublicationRefusee, RegistrePublication
from .securite import (EXTENSIONS_DOCUMENTS, CoffreAcces, FichierRefuse, chemin_dans, nom_fichier_sur,
                       restreindre_droits, verifier_fichier)
from .tarifs import charger_tarifs, suggerer

TAILLE_MAX_REQUETE = 160 * 1024 * 1024
DUREE_INACTIVITE = 30 * 60
DUREE_MAX_SESSION = 10 * 3600
e = html.escape

CSS = """
:root{--p:#1F3A5F;--s:#E07A1F;--c:#EEF3F8}
*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;font-size:19px;line-height:1.55;margin:0;color:#1a1a1a;background:#f7f9fb}
header{background:var(--p);color:#fff;padding:14px 24px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
header a{color:#fff;font-weight:bold;text-decoration:none}
header form{margin-left:auto}
main{max-width:1150px;margin:0 auto;padding:20px}
h1{color:var(--p);font-size:30px}h2{color:var(--p);border-left:6px solid var(--s);padding-left:10px}
.carte{background:#fff;border:1px solid #cfd8e3;border-radius:10px;padding:18px 22px;margin:18px 0}
label{display:block;font-weight:bold;margin-top:14px}
input,select,textarea{font-size:18px;padding:9px;width:100%;border:2px solid #9aa5b1;border-radius:6px}
input[type=checkbox]{width:auto;transform:scale(1.4);margin-right:10px}
input[type=color]{width:90px;height:48px;padding:2px}
.ligne{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
button{font-size:19px;padding:12px 22px;border:0;border-radius:8px;background:var(--p);color:#fff;cursor:pointer;margin:8px 8px 0 0}
button.second{background:#5b6b7c}button.danger{background:#8b1e1e}button.accent{background:var(--s)}
button:focus,a:focus,input:focus{outline:4px solid #ffbf47;outline-offset:2px}
.alerte{background:#fff4e5;border-left:6px solid var(--s);padding:10px 14px;margin:8px 0}
.ok{background:#e8f5e9;border-left:6px solid #2e7d32;padding:10px 14px;margin:8px 0}
.ko{background:#fdecea;border-left:6px solid #8b1e1e;padding:10px 14px;margin:8px 0}
table{border-collapse:collapse;width:100%}th,td{border:1px solid #cfd8e3;padding:8px;text-align:left;vertical-align:top}
th{background:var(--p);color:#fff}tr:nth-child(even) td{background:var(--c)}
small{color:#4a5560}
"""


class Etat:
    def __init__(self, base: Path, port: int) -> None:
        self.base = base
        self.port = port
        self.coffre = CoffreAcces(base)
        self.sessions: dict[str, dict] = {}
        self.verrou = threading.Lock()
        self.registre = RegistrePublication(base)

    # ---------------------------------------------------------------- sessions
    def ouvrir_session(self) -> str:
        jeton = secrets.token_urlsafe(32)
        with self.verrou:
            self.sessions[jeton] = {"cree": time.time(), "vu": time.time(), "csrf": secrets.token_urlsafe(32)}
        return jeton

    def session(self, jeton: Optional[str]) -> Optional[dict]:
        if not jeton:
            return None
        with self.verrou:
            s = self.sessions.get(jeton)
            maintenant = time.time()
            if not s or maintenant - s["vu"] > DUREE_INACTIVITE or maintenant - s["cree"] > DUREE_MAX_SESSION:
                self.sessions.pop(jeton, None)
                return None
            s["vu"] = maintenant
            return s

    def fermer_session(self, jeton: Optional[str]) -> None:
        with self.verrou:
            self.sessions.pop(jeton or "", None)


def _page(titre: str, corps: str, csrf: str = "", connecte: bool = True) -> bytes:
    menu = ""
    if connecte:
        menu = (f"<a href='/'>Accueil</a><a href='/nouveau'>Nouveau titre</a><a href='/charte'>Charte</a>"
                f"<a href='/tarifs'>Tarifs</a><a href='/securite'>Sécurité</a>"
                f"<form method='post' action='/deconnexion'><input type='hidden' name='csrf' value='{e(csrf)}'>"
                f"<button class='second' type='submit'>Se déconnecter</button></form>")
    return (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'><title>{e(titre)}</title>"
            f"<link rel='stylesheet' href='/style.css'></head><body><header><strong>Décorticage pédagogique</strong>"
            f"{menu}</header><main>{corps}</main></body></html>").encode("utf-8")


def _champ_csrf(s: dict) -> str:
    return f"<input type='hidden' name='csrf' value='{e(s['csrf'])}'>"


class Gestionnaire(BaseHTTPRequestHandler):
    server_version = "Decorticage"
    sys_version = ""
    etat: Etat = None  # type: ignore[assignment]

    # ------------------------------------------------------------- utilitaires
    def log_message(self, format, *args):  # pas de journal des URL (confidentialité)
        return

    def _entetes_securite(self):
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'self'; img-src 'self' data:; form-action 'self'; "
                         "frame-ancestors 'none'; base-uri 'none'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")  # rien ne fuit hors du logiciel
        self.send_header("Cache-Control", "no-store")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")

    def _envoyer(self, code: int, contenu: bytes, type_: str = "text/html; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", type_)
        self.send_header("Content-Length", str(len(contenu)))
        self._entetes_securite()
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(contenu)

    def _rediriger(self, cible: str, extra=None):
        self.send_response(303)
        self.send_header("Location", cible)
        self.send_header("Content-Length", "0")
        self._entetes_securite()
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()

    def _hote_valide(self) -> bool:
        hote = (self.headers.get("Host") or "").lower()
        return hote in {f"127.0.0.1:{self.etat.port}", f"localhost:{self.etat.port}"}

    def _origine_valide(self) -> bool:
        attendues = {f"http://127.0.0.1:{self.etat.port}", f"http://localhost:{self.etat.port}"}
        origine = self.headers.get("Origin")
        if origine:
            return origine in attendues
        ref = self.headers.get("Referer") or ""
        return any(ref.startswith(a + "/") for a in attendues)

    def _jeton_cookie(self) -> Optional[str]:
        c = cookies.SimpleCookie()
        try:
            c.load(self.headers.get("Cookie") or "")
        except cookies.CookieError:
            return None
        m = c.get("yeba_session")
        return m.value if m else None

    def _session(self) -> Optional[dict]:
        return self.etat.session(self._jeton_cookie())

    def _lire_corps(self) -> bytes:
        try:
            taille = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            taille = -1
        if taille < 0 or taille > TAILLE_MAX_REQUETE:
            raise FichierRefuse("Envoi trop volumineux (150 Mo maximum au total).")
        return self.rfile.read(taille) if taille else b""

    def _formulaire(self) -> tuple[dict, dict]:
        """Retourne (champs texte, fichiers {nom_champ: [(nom_fichier, octets)]})."""
        corps = self._lire_corps()
        type_ = self.headers.get("Content-Type") or ""
        champs, fichiers = {}, {}
        if type_.startswith("multipart/form-data"):
            msg = BytesParser(policy=policy.HTTP).parsebytes(
                b"Content-Type: " + type_.encode("latin-1") + b"\r\nMIME-Version: 1.0\r\n\r\n" + corps)
            for part in msg.iter_parts():
                nom = part.get_param("name", header="content-disposition")
                if not nom:
                    continue
                fname = part.get_filename()
                donnees = part.get_payload(decode=True) or b""
                if fname is not None:
                    if donnees:
                        fichiers.setdefault(nom, []).append((fname, donnees))
                else:
                    champs[nom] = donnees.decode("utf-8", errors="replace")
        else:
            for k, v in urllib.parse.parse_qs(corps.decode("utf-8", errors="replace"), keep_blank_values=True).items():
                champs[k] = v[0]
        return champs, fichiers

    def _erreur(self, message: str, s: Optional[dict], code: int = 400):
        corps = f"<h1>Action impossible</h1><div class='ko'>{e(message)}</div><p><a href='/'>Retour</a></p>"
        self._envoyer(code, _page("Erreur", corps, s["csrf"] if s else "", connecte=bool(s)))

    # ------------------------------------------------------------------ routes
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if not self._hote_valide():
            return self._envoyer(421, b"Hote refuse", "text/plain; charset=utf-8")
        chemin = urllib.parse.urlsplit(self.path).path
        if chemin == "/style.css":
            charte = charger_charte(self.etat.base)
            css = CSS.replace("#1F3A5F", "#" + charte.couleur_primaire).replace("#E07A1F", "#" + charte.couleur_secondaire)
            return self._envoyer(200, css.encode(), "text/css; charset=utf-8")
        s = self._session()
        if chemin == "/connexion" or not s:
            return self._page_connexion()
        try:
            if chemin == "/":
                return self._accueil(s)
            if chemin == "/nouveau":
                return self._page_nouveau(s)
            if chemin == "/charte":
                return self._page_charte(s)
            if chemin == "/tarifs":
                return self._page_tarifs(s)
            if chemin == "/securite":
                return self._page_securite(s)
            morceaux = [m for m in chemin.split("/") if m]
            if len(morceaux) == 2 and morceaux[0] == "projet":
                return self._page_projet(s, morceaux[1])
            if len(morceaux) == 3 and morceaux[0] == "fichier":
                return self._telecharger(s, morceaux[1], morceaux[2])
            return self._erreur("Page introuvable.", s, 404)
        except FichierRefuse as exc:
            return self._erreur(str(exc), s)

    def do_POST(self):
        if not self._hote_valide() or not self._origine_valide():
            return self._envoyer(403, b"Requete refusee", "text/plain; charset=utf-8")
        chemin = urllib.parse.urlsplit(self.path).path
        try:
            champs, fichiers = self._formulaire()
        except FichierRefuse as exc:
            return self._erreur(str(exc), self._session(), 413)
        if chemin == "/connexion":
            return self._connexion(champs)
        s = self._session()
        if not s:
            return self._rediriger("/connexion")
        if not secrets.compare_digest(champs.get("csrf", ""), s["csrf"]):
            return self._erreur("Jeton de sécurité invalide : rechargez la page.", s, 403)
        try:
            if chemin == "/deconnexion":
                self.etat.fermer_session(self._jeton_cookie())
                return self._rediriger("/connexion", {"Set-Cookie": "yeba_session=; Max-Age=0; Path=/; HttpOnly; SameSite=Strict"})
            if chemin == "/nouveau":
                return self._creer_projet(s, champs, fichiers)
            if chemin == "/charte":
                return self._enregistrer_charte(s, champs, fichiers)
            if chemin == "/tarifs":
                return self._importer_tarifs(s, fichiers)
            if chemin == "/securite":
                audit.corriger(self.etat.base)
                return self._rediriger("/securite")
            morceaux = [m for m in chemin.split("/") if m]
            if len(morceaux) == 3 and morceaux[0] == "projet" and morceaux[2] == "publication":
                return self._decider_publication(s, morceaux[1], champs)
            if len(morceaux) == 3 and morceaux[0] == "projet" and morceaux[2] == "regenerer":
                return self._regenerer(s, morceaux[1], champs)
            return self._erreur("Action inconnue.", s, 404)
        except (FichierRefuse, ValueError, PublicationRefusee) as exc:
            return self._erreur(str(exc), s)
        except Exception:  # noqa: BLE001 — message générique, détail en local seulement
            (self.etat.base / "erreurs.log").open("a", encoding="utf-8").write(
                f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}\n{traceback.format_exc()}\n")
            return self._erreur("Erreur interne : le détail est dans donnees_yeba/erreurs.log.", s, 500)

    # --------------------------------------------------------------- connexion
    def _page_connexion(self, message: str = ""):
        premiere = not self.etat.coffre.existe()
        attente = self.etat.coffre.attente_restante()
        if premiere:
            corps = ("<h1>Créer votre mot de passe</h1><p>Première utilisation : ce mot de passe protège l'accès "
                     "au logiciel sur cet ordinateur (12 caractères minimum, 3 familles de caractères).</p>")
        else:
            corps = "<h1>Connexion</h1>"
        if message:
            corps += f"<div class='ko'>{e(message)}</div>"
        if attente:
            corps += f"<div class='alerte'>Trop d'essais : patientez {attente} secondes.</div>"
        corps += ("<form method='post' action='/connexion' class='carte'>"
                  "<label for='mdp'>Mot de passe</label><input id='mdp' type='password' name='mdp' required "
                  "autocomplete='current-password' autofocus>")
        if premiere:
            corps += "<label for='mdp2'>Confirmer</label><input id='mdp2' type='password' name='mdp2' required>"
        corps += "<button type='submit'>Entrer</button></form>"
        self._envoyer(200, _page("Connexion", corps, connecte=False))

    def _connexion(self, champs: dict):
        mdp = champs.get("mdp", "")
        if not self.etat.coffre.existe():
            if mdp != champs.get("mdp2", ""):
                return self._page_connexion("Les deux mots de passe sont différents.")
            try:
                self.etat.coffre.definir(mdp)
            except ValueError as exc:
                return self._page_connexion(str(exc))
        elif not self.etat.coffre.verifier(mdp):
            return self._page_connexion("Mot de passe incorrect.")
        jeton = self.etat.ouvrir_session()
        return self._rediriger("/", {"Set-Cookie": f"yeba_session={jeton}; Path=/; HttpOnly; SameSite=Strict"})

    # ----------------------------------------------------------------- projets
    def _projets(self) -> list[dict]:
        res = []
        for d in sorted((self.etat.base / "projets").glob("*/projet.json")):
            try:
                p = json.loads(d.read_text(encoding="utf-8"))
                p["id"] = d.parent.name
                res.append(p)
            except (OSError, ValueError):
                continue
        return sorted(res, key=lambda p: p.get("date", ""), reverse=True)

    def _accueil(self, s: dict):
        projets = self._projets()
        corps = "<h1>Vos titres décortiqués</h1>"
        attente = [p for p in projets if p.get("code") and self.etat.registre.doit_demander(p["code"])]
        for p in attente:
            corps += (f"<div class='alerte'><strong>Question en attente :</strong> publier le programme "
                      f"« {e(p.get('titre', ''))} » sur votre site ? "
                      f"<a href='/projet/{e(p['id'])}#publication'>Répondre</a></div>")
        corps += "<p><a href='/nouveau'><button type='button' class='accent'>+ Décortiquer un nouveau titre</button></a></p>"
        if projets:
            corps += "<table><tr><th>Titre</th><th>Code</th><th>Durée</th><th>Créé le</th><th>Site</th></tr>"
            for p in projets:
                statut = self.etat.registre.statut(p.get("code", ""))
                corps += (f"<tr><td><a href='/projet/{e(p['id'])}'>{e(p.get('titre', ''))}</a></td>"
                          f"<td>{e(p.get('code', ''))}</td><td>{e(str(p.get('heures', '')))} h</td>"
                          f"<td>{e(p.get('date', '')[:10])}</td><td>{e(_libelle_statut(statut))}</td></tr>")
            corps += "</table>"
        else:
            corps += "<p>Aucun titre pour l'instant.</p>"
        self._envoyer(200, _page("Accueil", corps, s["csrf"]))

    def _formulaire_reglages(self, r: Reglages) -> str:
        def champ(nom, lib, aide="", type_="text"):
            v = getattr(r, nom)
            return (f"<label for='{nom}'>{e(lib)}</label><input id='{nom}' name='{nom}' type='{type_}' "
                    f"value='{e(str(v if v not in (0, 0.0) or nom.startswith('h_') else ''))}'>"
                    + (f"<small>{e(aide)}</small>" if aide else ""))
        coche = lambda nom, lib: (f"<label><input type='checkbox' name='{nom}' value='1' "  # noqa: E731
                                  f"{'checked' if getattr(r, nom) else ''}>{e(lib)}</label>")
        return (
            "<div class='carte'><h2>Durée et calendrier</h2><div class='ligne'>"
            + champ("heures_centre", "Durée en centre (heures) *", "Convention avec l'organisme", "number")
            + champ("heures_entreprise", "Période en entreprise (heures)", "Vide = minimum du RE", "number")
            + champ("date_debut", "Date de début", "AAAA-MM-JJ ou JJ/MM/AAAA")
            + champ("date_examen", "Date d'examen (contrôle)", "")
            + "</div><div class='ligne'>"
            + champ("creneaux", "Horaires", "ex. 08:30-12:00, 13:00-16:30")
            + champ("pauses", "Pauses (non comptées)", "ex. 10:15-10:30, 14:45-15:00")
            + champ("jours", "Jours en centre", "1=lundi … 5=vendredi ; ex. 1,2")
            + champ("rythme", "Rythme d'alternance (semaines)", "C=centre, E=entreprise ; ex. CCEE")
            + "</div>"
            + champ("fermetures", "Fermetures / jours annulés", "ex. 2027-02-15..2027-02-19 Vacances ; 2027-03-08 Alerte rouge")
            + "</div><div class='carte'><h2>Organisation pédagogique</h2><div class='ligne'>"
            + champ("ordre_cp", "Ordre des compétences", "ex. 5,6,7,1,2,3,4,8,9,10 (vide = ordre du REAC)")
            + champ("poids_cp", "Pondération des compétences", "ex. 1=40, 5=30 (vide = automatique)")
            + champ("h_accueil", "Accueil (h)", "", "number") + champ("h_ecf_par_at", "ECF par AT (h)", "", "number")
            + champ("h_dossier_pro", "Dossier professionnel (h)", "", "number")
            + champ("h_productions", "Productions d'examen (h)", "", "number")
            + champ("h_examen_blanc", "Examen blanc (h, 0 = durée RE)", "", "number")
            + champ("h_bilan", "Bilan (h)", "", "number")
            + "</div></div><div class='carte'><h2>Organisme et programme</h2>"
            + champ("commanditaire", "Formation réalisée pour un autre centre ?",
                    "Nom du centre (ICCI, TETRANERGY…). Si rempli : YEBA FORMATIONS et son logo n'apparaissent pas.")
            + coche("afficher_nom", "Afficher le nom de l'organisme") + coche("afficher_logo", "Afficher le logo (YEBA uniquement)")
            + "<div class='ligne'>"
            + champ("public", "Public visé") + champ("prerequis", "Prérequis") + champ("lieu", "Lieu")
            + champ("delai_acces", "Délai d'accès") + champ("referent_handicap", "Référent handicap (nom, contact)")
            + "</div>" + champ("modalites_pedagogiques", "Modalités pédagogiques") + "</div>")

    def _page_nouveau(self, s: dict):
        corps = ("<h1>Décortiquer un titre</h1>"
                 "<form method='post' action='/nouveau' enctype='multipart/form-data'>" + _champ_csrf(s)
                 + "<div class='carte'><h2>Documents</h2><p>Déposez le REAC (indispensable), le RE ou RC, et la fiche "
                   "France Compétences (RNCP ou RS). Le type de chaque document est reconnu automatiquement.</p>"
                   f"<label for='docs'>Fichiers ({', '.join(sorted(EXTENSIONS_DOCUMENTS))})</label>"
                   "<input id='docs' type='file' name='documents' multiple required "
                   "accept='.pdf,.docx,.xlsx,.txt,.csv'></div>"
                 + self._formulaire_reglages(Reglages())
                 + "<button type='submit' class='accent'>Lancer le décorticage</button></form>")
        self._envoyer(200, _page("Nouveau titre", corps, s["csrf"]))

    def _creer_projet(self, s: dict, champs: dict, fichiers: dict):
        docs = fichiers.get("documents", [])
        if not docs:
            raise ValueError("Aucun document reçu.")
        if len(docs) > 10:
            raise ValueError("10 documents maximum par titre.")
        pid = secrets.token_hex(8)
        dossier = self.etat.base / "projets" / pid
        sources = dossier / "sources"
        sources.mkdir(parents=True)
        restreindre_droits(dossier)
        restreindre_droits(sources)
        try:
            chemins = []
            for nom, donnees in docs:
                cible = chemin_dans(sources, nom_fichier_sur(nom))
                cible.write_bytes(donnees)
                restreindre_droits(cible)
                verifier_fichier(cible)
                chemins.append(cible)
            reglages = Reglages.depuis_dict(champs)
            self._generer(dossier, chemins, reglages)
        except Exception:
            shutil.rmtree(dossier, ignore_errors=True)
            raise
        return self._rediriger(f"/projet/{pid}")

    def _generer(self, dossier: Path, chemins: list[Path], reglages: Reglages):
        analyse = analyser_documents(chemins)
        ctx = construire_contexte(analyse, reglages, self.etat.base, self._tarif_pour(reglages, None))
        sorties_dir = dossier / "sorties"
        if sorties_dir.exists():
            shutil.rmtree(sorties_dir)
        sorties = generer_sorties(ctx, sorties_dir)
        total = sum(l["minutes"] for l in ctx.plan.lignes) / 60
        tarif = self._tarif_pour(reglages, total)
        meta = {
            "titre": ctx.titre, "code": ctx.code, "heures": round(total, 2),
            "date": dt.datetime.now().isoformat(timespec="seconds"),
            "debut": ctx.plan.lignes[0]["date"].isoformat() if ctx.plan.lignes else "",
            "fin": ctx.plan.date_fin.isoformat() if ctx.plan.date_fin else "",
            "seances": len(ctx.plan.seances), "sources": [c.name for c in chemins],
            "sorties": {k: v.name for k, v in sorties.items()},
            "alertes": ctx.alertes + ctx.plan.avertissements, "hypotheses": ctx.hypotheses,
            "reglages": reglages.en_dict(), "tarif_suggere": tarif,
            "inconnus": analyse["inconnus"], "est_yeba": ctx.identite.est_yeba,
        }
        f = dossier / "projet.json"
        f.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        restreindre_droits(f)
        return ctx

    def _tarif_pour(self, reglages: Reglages, heures: Optional[float]) -> Optional[dict]:
        fichiers = sorted((self.etat.base / "tarifs").glob("tarifs.*"))
        if not fichiers or not heures:
            return None
        try:
            return suggerer(charger_tarifs(fichiers[0]), heures)
        except (FichierRefuse, ValueError):
            return None

    def _charger_projet(self, pid: str) -> tuple[Path, dict]:
        if not pid.isalnum() or len(pid) != 16:
            raise FichierRefuse("Projet introuvable.")
        dossier = chemin_dans(self.etat.base / "projets", pid)
        f = dossier / "projet.json"
        if not f.exists():
            raise FichierRefuse("Projet introuvable.")
        return dossier, json.loads(f.read_text(encoding="utf-8"))

    def _page_projet(self, s: dict, pid: str):
        dossier, p = self._charger_projet(pid)
        fr = lambda iso: dt.date.fromisoformat(iso).strftime("%d/%m/%Y") if iso else "?"  # noqa: E731
        corps = (f"<h1>{e(p['titre'])}</h1><p><strong>{e(p['code'])}</strong> — {p['heures']:g} h en centre, "
                 f"{e(str(p['seances']))} séances, du {fr(p['debut'])} au {fr(p['fin'])}</p>")
        if not p.get("est_yeba", True):
            corps += "<div class='ok'>Formation pour un autre centre : YEBA FORMATIONS et son logo sont masqués.</div>"
        for a in p.get("alertes", []):
            corps += f"<div class='alerte'>⚠ {e(a)}</div>"
        for h in p.get("hypotheses", []):
            corps += f"<div class='alerte'>Hypothèse à confirmer : {e(h)}</div>"
        for i in p.get("inconnus", []):
            corps += f"<div class='ko'>Document non reconnu (ignoré) : {e(i)}</div>"
        libelles = {"decorticage": "Décorticage complet (Excel)", "programme": "Programme de formation (Word)",
                    "examen": "Examen simplifié (Word)", "agenda": "Planning pour agenda (.ics)",
                    "apercu_site": "Aperçu de la page web", "programme_json": "Programme (données JSON)"}
        corps += "<div class='carte'><h2>Fichiers produits</h2><ul>"
        for k, nom in p.get("sorties", {}).items():
            corps += f"<li><a href='/fichier/{e(pid)}/{e(urllib.parse.quote(nom))}'>{e(libelles.get(k, nom))}</a></li>"
        corps += "</ul></div>"

        # ----- publication (3 choix)
        code = p["code"]
        statut = self.etat.registre.statut(code)
        corps += "<div class='carte' id='publication'><h2>Site internet</h2>"
        if statut == "non_definitif":
            corps += "<div class='ko'>Refusé définitivement : ce programme ne sera jamais publié.</div>"
        else:
            if statut == "oui":
                corps += "<div class='ok'>Publication autorisée. Page générée dans <code>donnees_yeba/site_a_publier/</code>.</div>"
            t = p.get("tarif_suggere") or {}
            corps += f"<form method='post' action='/projet/{e(pid)}/publication'>" + _champ_csrf(s)
            corps += "<p>Publier ce programme sur votre site, avec le tarif ci-dessous ?</p>"
            if t.get("affichage"):
                corps += f"<p><small>{e(t.get('message', ''))} Base : {e(t.get('base', ''))}.</small></p>"
            elif t.get("message"):
                corps += f"<p><small>{e(t['message'])}</small></p>"
            else:
                corps += "<p><small>Aucun tarif importé (menu Tarifs) : le programme affichera « Sur devis ».</small></p>"
            corps += ("<div class='ligne'><div><label for='inter'>Prix inter (par stagiaire, HT)</label>"
                      f"<input id='inter' name='inter' value='{e(str(t.get('inter_par_stagiaire', '')))}'></div>"
                      "<div><label for='intra'>Prix intra (par jour et par groupe, HT)</label>"
                      f"<input id='intra' name='intra' value='{e(str(t.get('intra_par_jour_groupe', '')))}'></div></div>")
            for cle, lib in CHOIX.items():
                classe = {"oui": "accent", "non_redemander": "second", "non_definitif": "danger"}[cle]
                corps += f"<button type='submit' name='choix' value='{cle}' class='{classe}'>{e(lib)}</button>"
            corps += "</form>"
        corps += "</div>"

        # ----- régénération (fermeture imprévue, nouvelle durée…)
        corps += (f"<form method='post' action='/projet/{e(pid)}/regenerer'>" + _champ_csrf(s)
                  + "<h2>Modifier et régénérer</h2><p>Exemple : ajoutez un jour d'alerte cyclonique dans « Fermetures » "
                    "et tout le planning est recalculé.</p>"
                  + self._formulaire_reglages(Reglages.depuis_dict(p.get("reglages", {})))
                  + "<button type='submit'>Régénérer</button></form>")
        self._envoyer(200, _page(p["titre"], corps, s["csrf"]))

    def _regenerer(self, s: dict, pid: str, champs: dict):
        dossier, p = self._charger_projet(pid)
        sources = [chemin_dans(dossier / "sources", n) for n in p.get("sources", [])]
        self._generer(dossier, sources, Reglages.depuis_dict(champs))
        return self._rediriger(f"/projet/{pid}")

    def _decider_publication(self, s: dict, pid: str, champs: dict):
        dossier, p = self._charger_projet(pid)
        choix = champs.get("choix", "")
        tarif = None
        if choix == "oui":
            affichage = {}
            for cle, lib in (("inter", "Inter-entreprises (par stagiaire, HT)"),
                             ("intra", "Intra-entreprise (par jour, par groupe, HT)")):
                v = "".join(ch for ch in champs.get(cle, "") if ch.isdigit() or ch in ",.")
                if v:
                    affichage[lib] = f"{v} €"
            tarif = {"valide": bool(affichage), "affichage": affichage}
        self.etat.registre.decider(p["code"], choix, tarif)
        if choix == "oui":
            analyse = analyser_documents([chemin_dans(dossier / "sources", n) for n in p.get("sources", [])])
            ctx = construire_contexte(analyse, Reglages.depuis_dict(p.get("reglages", {})), self.etat.base)
            publier_sur_site(ctx, self.etat.base)
        else:
            retirer_du_site(p["titre"], self.etat.base)   # un « Non » retire une page déjà générée
        return self._rediriger(f"/projet/{pid}#publication")

    def _telecharger(self, s: dict, pid: str, nom: str):
        dossier, p = self._charger_projet(pid)
        nom = urllib.parse.unquote(nom)
        if nom not in p.get("sorties", {}).values():
            raise FichierRefuse("Fichier non autorisé.")
        f = chemin_dans(dossier / "sorties", nom)
        types = {".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 ".ics": "text/calendar; charset=utf-8", ".html": "text/html; charset=utf-8",
                 ".json": "application/json"}
        disposition = "inline" if f.suffix == ".html" else "attachment"
        self._envoyer(200, f.read_bytes(), types.get(f.suffix, "application/octet-stream"),
                      {"Content-Disposition": f"{disposition}; filename=\"{nom_fichier_sur(nom)}\""})

    # ------------------------------------------------------------------ charte
    def _page_charte(self, s: dict, message: str = ""):
        c = charger_charte(self.etat.base)
        coul = lambda nom, lib: (f"<div><label for='{nom}'>{e(lib)}</label><input id='{nom}' type='color' "  # noqa: E731
                                 f"name='{nom}' value='#{e(getattr(c, nom))}'></div>")
        corps = "<h1>Charte graphique</h1>" + (f"<div class='ok'>{e(message)}</div>" if message else "")
        if not c.couleurs_validees:
            corps += "<div class='alerte'>Couleurs provisoires : saisissez les codes exacts de votre charte.</div>"
        corps += ("<form method='post' action='/charte' enctype='multipart/form-data' class='carte'>" + _champ_csrf(s)
                  + f"<label for='nom'>Nom de l'organisme</label><input id='nom' name='nom_organisme' value='{e(c.nom_organisme)}'>"
                  + "<div class='ligne'>" + coul("couleur_primaire", "Couleur principale")
                  + coul("couleur_secondaire", "Couleur d'accent (verbes Bloom)") + coul("couleur_claire", "Fond des bandes")
                  + coul("couleur_texte", "Texte") + "</div><div class='ligne'>"
                  + f"<div><label for='police'>Police</label><input id='police' name='police' value='{e(c.police)}'></div>"
                  + f"<div><label for='tt'>Taille du texte (14 min.)</label><input id='tt' type='number' min='14' max='28' name='taille_texte' value='{c.taille_texte}'></div>"
                  + f"<div><label for='ti'>Taille des titres</label><input id='ti' type='number' min='18' max='40' name='taille_titre' value='{c.taille_titre}'></div>"
                  + "</div><label for='logo'>Logo (PNG ou JPEG)</label><input id='logo' type='file' name='logo' accept='.png,.jpg,.jpeg'>"
                  + (f"<p><small>Logo actuel : {e(c.logo)}</small></p>" if c.logo else "")
                  + "<label><input type='checkbox' name='retirer_logo' value='1'>Retirer le logo</label>"
                  + "<button type='submit'>Enregistrer</button></form>")
        self._envoyer(200, _page("Charte", corps, s["csrf"]))

    def _enregistrer_charte(self, s: dict, champs: dict, fichiers: dict):
        c = charger_charte(self.etat.base)
        for k in ("nom_organisme", "couleur_primaire", "couleur_secondaire", "couleur_claire", "couleur_texte", "police"):
            if k in champs:
                setattr(c, k, champs[k])
        for k in ("taille_texte", "taille_titre"):
            try:
                setattr(c, k, int(champs.get(k, getattr(c, k))))
            except ValueError:
                pass
        c.couleurs_validees = True
        if champs.get("retirer_logo"):
            c.logo = ""
        for nom, donnees in fichiers.get("logo", [])[:1]:
            c.logo = self._enregistrer_logo(nom, donnees)
        erreurs = enregistrer_charte(c, self.etat.base)
        if erreurs:
            raise ValueError(" ; ".join(erreurs))
        return self._page_charte(s, "Charte enregistrée.")

    def _enregistrer_logo(self, nom: str, donnees: bytes) -> str:
        import warnings

        from PIL import Image
        tmp = self.etat.base / "charte" / ("_reception" + Path(nom_fichier_sur(nom)).suffix.lower())
        tmp.write_bytes(donnees)
        try:
            verifier_fichier(tmp, {".png", ".jpg", ".jpeg"})
            Image.MAX_IMAGE_PIXELS = 40_000_000
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(tmp) as im:
                    im.verify()
                with Image.open(tmp) as im:
                    im.load()
                    propre = im.convert("RGBA")
            cible = self.etat.base / "charte" / "logo.png"
            propre.save(cible, "PNG")   # ré-encodage : supprime métadonnées et contenu caché
            restreindre_droits(cible)
            return "logo.png"
        except (OSError, Image.DecompressionBombWarning, Image.DecompressionBombError) as exc:
            raise FichierRefuse("Image invalide ou suspecte.") from exc
        finally:
            tmp.unlink(missing_ok=True)

    # ------------------------------------------------------------------ tarifs
    def _page_tarifs(self, s: dict, message: str = ""):
        fichiers = sorted((self.etat.base / "tarifs").glob("tarifs.*"))
        corps = "<h1>Tarifs de référence</h1>" + (f"<div class='ok'>{e(message)}</div>" if message else "")
        corps += ("<div class='alerte'>Airtable est un service américain (Cloud Act) : le logiciel ne s'y connecte pas. "
                  "Exportez la vue tarifs de la base « YEBA FORMATIONS - centre de formation (adaptable) » en CSV "
                  "(Affichage → Télécharger CSV) puis importez-la ici. Colonnes reconnues : intitulé, domaine, "
                  "modalité (inter/intra), durée (heures ou jours), prix HT.</div>")
        if fichiers:
            try:
                t = charger_tarifs(fichiers[0])
                corps += f"<p>{len(t)} tarif(s) exploitable(s) dans {e(fichiers[0].name)}.</p>"
                if t:
                    corps += "<table><tr><th>Formation</th><th>Modalité</th><th>Heures</th><th>Prix HT</th><th>€/h</th></tr>"
                    for x in t[:30]:
                        corps += (f"<tr><td>{e(x['intitule'])}</td><td>{e(x['modalite'])}</td><td>{x['heures']:g}</td>"
                                  f"<td>{x['prix']:g}</td><td>{x['taux_horaire']:.2f}</td></tr>")
                    corps += "</table>"
            except (FichierRefuse, ValueError) as exc:
                corps += f"<div class='ko'>{e(str(exc))}</div>"
        corps += ("<form method='post' action='/tarifs' enctype='multipart/form-data' class='carte'>" + _champ_csrf(s)
                  + "<label for='f'>Fichier CSV ou XLSX</label><input id='f' type='file' name='tarifs' accept='.csv,.xlsx' required>"
                  + "<button type='submit'>Importer</button></form>")
        self._envoyer(200, _page("Tarifs", corps, s["csrf"]))

    def _importer_tarifs(self, s: dict, fichiers: dict):
        recus = fichiers.get("tarifs", [])
        if not recus:
            raise ValueError("Aucun fichier reçu.")
        nom, donnees = recus[0]
        ext = Path(nom_fichier_sur(nom)).suffix.lower()
        if ext not in (".csv", ".xlsx"):
            raise FichierRefuse("Format accepté : .csv ou .xlsx")
        dossier = self.etat.base / "tarifs"
        tmp = dossier / f"_reception{ext}"
        tmp.write_bytes(donnees)
        try:
            verifier_fichier(tmp, {".csv", ".xlsx"})
            t = charger_tarifs(tmp)
        except Exception:
            tmp.unlink(missing_ok=True)
            raise
        for ancien in dossier.glob("tarifs.*"):
            ancien.unlink()
        cible = dossier / f"tarifs{ext}"
        tmp.replace(cible)
        restreindre_droits(cible)
        return self._page_tarifs(s, f"{len(t)} tarif(s) importé(s).")

    # ---------------------------------------------------------------- sécurité
    def _page_securite(self, s: dict):
        rapport = audit.auditer(self.etat.base, hote="127.0.0.1")
        corps = "<h1>Contrôle de sécurité</h1><table><tr><th>Contrôle</th><th>Résultat</th><th>Détail</th></tr>"
        for r in rapport:
            corps += (f"<tr><td>{e(r['controle'])}</td><td>{'✔ OK' if r['ok'] else '✖ À corriger'}</td>"
                      f"<td>{e(r['detail'])}</td></tr>")
        corps += ("</table><form method='post' action='/securite'>" + _champ_csrf(s)
                  + "<button type='submit' class='accent'>Corriger automatiquement</button></form>")
        self._envoyer(200, _page("Sécurité", corps, s["csrf"]))


def _libelle_statut(statut: str) -> str:
    return {"a_demander": "Question à poser", "oui": "Publié", "non_redemander": "Non (à redemander)",
            "non_definitif": "Jamais"}.get(statut, statut)


def lancer(port: int = 0, ouvrir: bool = True) -> None:
    base = dossier_donnees()
    audit.corriger(base)
    serveur = ThreadingHTTPServer(("127.0.0.1", port), Gestionnaire)
    serveur.daemon_threads = True
    port_reel = serveur.server_address[1]
    Gestionnaire.etat = Etat(base, port_reel)
    url = f"http://127.0.0.1:{port_reel}/"
    print(f"Logiciel de décorticage démarré : {url}")
    print("Fermez cette fenêtre (ou Ctrl+C) pour arrêter le logiciel.")
    if ouvrir:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        serveur.server_close()


__all__ = ["lancer", "Charte"]

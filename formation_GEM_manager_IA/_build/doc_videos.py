# -*- coding: utf-8 -*-
from docs_engine import *
import re, io

def extraire(chemin):
    s = io.open(chemin, encoding="utf-8").read()
    bloc = s[s.index("const CC = ["):s.index("];", s.index("const CC = ["))]
    out = []
    for m in re.finditer(r'\[\s*(\d+)\s*,\s*"((?:[^"\\]|\\.)*)"\s*\]', bloc):
        t = int(m.group(1)); txt = m.group(2).replace('\\"', '"').replace("\\'", "'")
        if txt.strip():
            out.append((t, txt))
    return out

def mmss(s): return "%d:%02d" % (s // 60, s % 60)

f = [H1("Scripts voix off des deux vidéos"),
     P("Les deux vidéos sont des fichiers HTML autonomes : elles se lisent dans un navigateur, "
       "hors connexion, en plein écran (touche F11). Aucun compte, aucun envoi de données, "
       "aucun service tiers — rien ne sort de l'ordinateur du formateur."), E(3)]
f += [encadre("Trois façons de les utiliser", [
    "<b>Narration en direct (recommandé)</b> : vous lisez le script pendant que la vidéo défile. "
    "Les sous-titres restent affichés pour les personnes malentendantes.",
    "<b>Muette</b> : vous la laissez tourner, les sous-titres suffisent à la compréhension.",
    "<b>Voix enregistrée</b> : vous enregistrez le script avec un dictaphone et le lancez en parallèle. "
    "Les minutages ci-dessous servent de repères.",
    "Commandes : barre d'espace pour mettre en pause, flèches gauche et droite pour changer de scène."])]
f += [E(3), encadre("Conseils de diction", [
    "Débit lent : environ 130 mots par minute. Le silence fait partie du texte.",
    "Marquez une pause d'une seconde après chaque phrase courte projetée à l'écran.",
    "Ne lisez pas le sous-titre mot à mot si le groupe réagit : la vidéo peut être mise en pause."],
    coul=VERT, fond=colors.HexColor("#E8F3EC"))]

for titre, chemin, duree, quand in [
    ("Vidéo n°1 — Les trois positions du manager",
     "../02_videos/Video_1_Les_trois_positions_du_manager.html", "2 min 30", "Matin, vers 9h00"),
    ("Vidéo n°2 — La pyramide des risques de l'IA Act",
     "../02_videos/Video_2_La_pyramide_des_risques_IA_Act.html", "2 min 55", "Après-midi, vers 14h20")]:
    f += [SAUT(), H1(titre)]
    f += [tableau([["Durée", "Moment de diffusion", "Fichier"],
                   [duree, quand, chemin.split("/")[-1]]], [24*mm, 42*mm, None])]
    f += [E(3), H2("Texte à dire, minuté")]
    lignes = [["Top", "Texte de la voix off"]]
    for t, txt in extraire(chemin):
        lignes.append([mmss(t), txt])
    f += [tableau(lignes, [18*mm, None])]

f += [SAUT(), H2("Souveraineté des données — pourquoi ce format")]
f += puces([
    "Ces vidéos ne dépendent d'aucune plateforme d'hébergement, française ou étrangère.",
    "Aucune donnée de lecture n'est collectée : ni compte, ni cookie, ni mesure d'audience.",
    "Le fichier peut être copié sur une clé USB et lu dans une salle sans connexion.",
    "Conséquence RGPD : aucun traitement de données personnelles n'est mis en œuvre par le support "
    "lui-même, donc ni finalité à déclarer, ni sous-traitant à encadrer (RGPD, art. 28).",
    "Conséquence IA Act : le support de diffusion n'est pas un système d'IA. Aucune obligation "
    "de transparence au titre de l'article 50 ne s'y applique."])
f += [E(3), P("Si vous faites appel à un prestataire pour produire une version animée ou "
              "une voix de synthèse, la situation change : une voix générée par IA doit être "
              "signalée comme telle (IA Act, art. 50) et le contrat de sous-traitance doit "
              "être examiné au regard du RGPD.", "petit")]

doc = document("../02_videos/Scripts_voix_off_videos_1_et_2.pdf",
               "Scripts voix off — vidéos 1 et 2",
               "Texte minuté, conseils de diction, note de souveraineté")
doc.build(f)
print("Scripts videos : OK")

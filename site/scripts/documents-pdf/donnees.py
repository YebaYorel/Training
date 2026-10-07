"""Lecture des fiches du CATALOGUE Airtable et mise en forme commune aux programmes et aux livrets.

Règle du dirigeant : une journée = 7 heures de formation, quel que soit le calcul d'Airtable.
Les horaires (08h00–12h00 / 13h00–17h00, pauses de 10h00 et 15h00) sont ceux des fiches Airtable.
Rien n'est modifié dans Airtable : les incohérences relevées sont listées par `incoherences()`.
"""
import json
import re
from pathlib import Path

RACINE = Path(__file__).parent.parent.parent
SOURCE = RACINE / 'airtable' / 'fiches-2026-10-07.json'
C = {
    'ref': 'fldWPKxIdTNSNiK6n', 'titre': 'fld6Xp5Zw0J0XQSh5', 'statut': 'fldcMSEP0XWMPuUdR', 'marque': 'fldpLRGUwDSgGt145',
    'type': 'fldjiurLwibphehvH', 'public': 'fld7CazsUxGR1OxSF', 'heures': 'fldgkIZrOJeDAxT2F', 'prerequis': 'fldIFQ1HzJaBBoykp',
    'evaluation': 'fld474uBdXZ6UOltS', 'acces': 'fldbsvcmvRBqUysLD', 'adaptations': 'fldADYnLuEBfmqnI9',
    'financements': 'fld0grIzQO2B1Vhlq', 'objectifs': 'fldUTrd3hxOnHY53h', 'programme': 'fld8GlwffOYDcNKMl',
    'inter': 'fldaty410G5hlJmvL', 'intra': 'fldFqIXtNjUWKoZeq', 'materiel': 'fldNPJWYxtO8GBdkC', 'precision': 'fld0dqAPIkUmQIFlc',
    'domaine': 'fldSIGD4tyrbWRnyn', 'methodes': 'fldNUqS1VCsf2erCm',
}
MARQUES_YEBA = ('Catalogue YEBA — marque YEBA obligatoire', 'Client direct — marque YEBA obligatoire')
HEURES_PAR_JOUR = 7
FINANCEURS = {'Plan PDC': 'Plan de développement des compétences', 'AIF': 'France Travail (AIF)', 'Région': 'Région Réunion'}

nom = lambda v: v.get('name') if isinstance(v, dict) else v
noms = lambda v: [nom(x) for x in v] if isinstance(v, list) else []
txt = lambda v: v.strip() if isinstance(v, str) else ''


def decouper_titre(titre):
    t = re.sub(r'\s*\([^)]*\bjours?\b[^)]*\)\s*$', '', titre).strip()
    i = t.find(' : ')
    return (t, '') if i < 0 else (t[:i], t[i + 3:])


def lire_objectifs(texte):
    """« O1 (Comprendre) — … / SMART : … » ou « 1. … » → [(code, verbe, énoncé, critère)]."""
    objs = []
    for brut in texte.split('\n'):
        l = brut.strip()
        m = re.match(r'^O(\d+)\s*(?:\((?:Bloom\s*:\s*)?([^)]+)\)|—\s*\[([^\]]+)\])?\s*—?\s*(.+)$', l)
        n = re.match(r'^(\d+)\.\s+(.+)$', l)
        if m:
            objs.append([f'O{m.group(1)}', (m.group(2) or m.group(3) or '').strip(), m.group(4).strip(' ;'), ''])
        elif n:
            objs.append([f'O{n.group(1)}', '', n.group(2).strip(' ;.') + '.', ''])
        elif objs and re.match(r'^(SMART|Critère)', l):
            objs[-1][3] = re.sub(r'^(SMART|Critère de réussite|Critère)\s*:\s*', '', l)
    for o in objs:
        o[2] = o[2][0].upper() + o[2][1:]
    return objs


HEURE = r'(\d{1,2})h(\d{2})\s*[–-]\s*(\d{1,2})h(\d{2})'


def lire_deroule(texte):
    """Programme Airtable (plusieurs formats) → [{titre, creneaux:[{h, titre, points, pause}]}]."""
    jours, jour, cren = [], None, None

    def nouveau_jour(titre):
        nonlocal jour
        jour = {'titre': titre, 'creneaux': []}
        jours.append(jour)

    for brut in texte.split('\n'):
        l = brut.strip()
        if not l:
            continue
        if re.match(r'^═+\s*RESSOURCES', l):
            break
        mj = re.match(r'^═+\s*(JOUR|JOURNÉE)\s*(\d)\s*(?:—\s*(.+?))?\s*═+$', l)
        if mj:
            nouveau_jour((mj.group(3) or '').strip().capitalize() or None)
            cren = None
            continue
        mc = re.match(r'^──\s*' + HEURE + r'\s*·\s*(.+?)\s*──$', l) or re.match(r'^(?:J(\d)\s*·\s*)?' + HEURE + r'\s*·\s*(.+)$', l)
        mp = re.match(r'^' + HEURE + r'\s*—\s*(PAUSE.*)$', l)
        if mc or mp:
            g = mc.groups() if mc else (None,) + mp.groups()
            if mc and len(g) == 6:  # format « J1 · 08h00–10h00 · TITRE »
                j, h = g[0], g[1:5]
                titre = g[5]
                if j and (not jours or len(jours) < int(j)):
                    nouveau_jour(None)
            else:
                h = g[0:4] if mc else g[1:5]
                titre = g[4] if mc else g[5]
            if jour is None:
                nouveau_jour(None)
            heure = f'{int(h[0]):02d}h{h[1]}–{int(h[2]):02d}h{h[3]}'
            pause = bool(re.match(r'^PAUSE', titre, re.I))
            cren = {'h': heure, 'titre': titre, 'points': [], 'pause': pause}
            jour['creneaux'].append(cren)
            continue
        if cren and re.match(r'^[•\-]', l):
            cren['points'].append(re.sub(r'^[•\-]\s*', '', l))
        elif cren and l.startswith('LIVRABLE'):
            cren['points'].append(l.replace('LIVRABLE :', 'Livrable :'))
    for j in jours:
        for c in j['creneaux']:
            t = c['titre']
            if t.isupper() or re.match(r'^[A-ZÀ-Ü0-9 \'’«»:\-—,?!.]+$', t.split(' — ')[0]):
                tete, _, reste = t.partition(' — ')
                tete = tete[0] + tete[1:].lower() if not c['pause'] else tete.capitalize()
                c['titre'] = tete + (f' — {reste}' if reste else '')
    return jours


# FOR-0011 : Airtable indique 14 heures (2 jours) alors que le programme Airtable décrit 3 jours.
# Les documents suivent la durée Airtable ; ce déroulé condense les 3 jours en 2 sans retirer d'objectif.
DEROULE_FOR_0011 = [
    {'titre': 'Comprendre, demander, protéger', 'creneaux': [
        {'h': '08h00–10h00', 'titre': 'Comprendre — Ce qu\'il y a sous le capot', 'pause': False, 'points': [
            'Séquence 0 : « qui a déjà collé un document client dans une IA ? »', 'Une machine à probabilités, pas une base de connaissances',
            'Les trois limites structurelles : l\'invention, la date de connaissance, le biais', 'Démonstration : la même question, trois outils, trois réponses']},
        {'h': '10h00–10h15', 'titre': 'Pause', 'pause': True, 'points': []},
        {'h': '10h15–12h00', 'titre': 'Bien demander — La méthode des 4 C', 'pause': False, 'points': [
            'Casquette, Contexte, Cadre, Contrôle', 'Atelier « Mes 6 demandes métier », sur son propre poste', 'Relancer plutôt que recommencer : la reprise en 2 temps']},
        {'h': '12h00–13h00', 'titre': 'Pause méridienne', 'pause': True, 'points': []},
        {'h': '13h00–15h00', 'titre': 'Garde-fous — Ce qui ne doit jamais sortir', 'pause': False, 'points': [
            'Réveil « Vrai ou inventé ? »', 'Atelier « Le Tri de la Réserve » : 20 cartes, trois bacs', 'Minimisation (RGPD art. 5) et base légale (art. 6) par l\'exemple',
            'Comptes grand public contre comptes professionnels ; anonymiser en trois gestes']},
        {'h': '15h00–15h15', 'titre': 'Pause', 'pause': True, 'points': []},
        {'h': '15h15–17h00', 'titre': 'Vérifier — et l\'assistant relié à l\'entreprise', 'pause': False, 'points': [
            'Atelier « Les 5 réponses ratées » : le défaut et sa source de vérification', 'Atelier « Qui voit quoi ? » : 10 cas de droits d\'accès',
            'Première fiche de poste « usages IA » ; quiz d\'étape']},
    ]},
    {'titre': 'Produire, automatiser, prouver', 'creneaux': [
        {'h': '08h00–10h00', 'titre': 'Deux voies et le parcours métier complet', 'pause': False, 'points': [
            'Voie américaine (Copilot, Gemini, Claude, ChatGPT) et voie européenne (Le Chat, Dust, Ollama) à parité',
            'Du courriel client au devis ; de la réunion au compte rendu relu ; du tableau à la synthèse', 'La grille d\'arbitrage YEBA']},
        {'h': '10h00–10h15', 'titre': 'Pause', 'pause': True, 'points': []},
        {'h': '10h15–12h00', 'titre': 'Bibliothèque de demandes et assistant personnalisé', 'pause': False, 'points': [
            '10 demandes documentées et le test du collègue', 'Les 5 blocs de configuration d\'un assistant dédié', 'Atelier : chacun construit l\'assistant de son poste']},
        {'h': '12h00–13h00', 'titre': 'Pause méridienne', 'pause': True, 'points': []},
        {'h': '13h00–15h00', 'titre': 'Tableaux et gouvernance', 'pause': False, 'points': [
            'Atelier « Les 4 erreurs cachées » : un chiffre qui part à la direction est recalculé à la main',
            'RGPD art. 28 : l\'éditeur d\'IA sous-traitant ; localisation et transferts hors UE', 'IA Act art. 4 et art. 50 ; les trois mesures de gouvernance']},
        {'h': '15h00–15h15', 'titre': 'Pause', 'pause': True, 'points': []},
        {'h': '15h15–17h00', 'titre': 'Restitution et évaluation', 'pause': False, 'points': [
            'Présentation de l\'assistant en 3 minutes, limites énoncées', 'Mise en situation notée sur la grille ; quiz de 10 questions (seuil 7/10)',
            'Fiche de poste « usages IA » et plan d\'action à 30 jours signés']},
    ]},
]


def materiel_texte(f):
    m = nom(f.get(C['materiel'])) or 'À confirmer'
    p = txt(f.get(C['precision']))
    lib = {'Aucun matériel requis': 'Aucun ordinateur nécessaire', 'À confirmer': 'Précisé avec la convocation'}.get(m, m)
    return lib + (f' — {p}' if p and m != 'À confirmer' else ''), m


def fiches(refs=None):
    data = json.loads(SOURCE.read_text(encoding='utf-8'))['records']
    out = []
    for r in data:
        f = r['fields']
        ref = f.get(C['ref'])
        statut = nom(f.get(C['statut']))
        if statut not in ('Active', 'En développement') or nom(f.get(C['marque'])) not in MARQUES_YEBA:
            continue
        if refs and ref not in refs:
            continue
        heures = f.get(C['heures']) or 0
        jours = max(1, round(heures / HEURES_PAR_JOUR))
        court, promesse = decouper_titre(txt(f.get(C['titre'])))
        deroule = DEROULE_FOR_0011 if ref == 'FOR-0011' else lire_deroule(txt(f.get(C['programme'])))
        materiel, materiel_brut = materiel_texte(f)
        out.append({
            'id': r['id'], 'ref': ref, 'statut': statut, 'titre': txt(f.get(C['titre'])), 'nom': court, 'promesse': promesse,
            'type': nom(f.get(C['type'])) or '', 'domaine': nom(f.get(C['domaine'])) or '',
            'heures': heures, 'jours': jours,
            'public': txt(f.get(C['public'])), 'prerequis': txt(f.get(C['prerequis'])), 'evaluation': txt(f.get(C['evaluation'])),
            'acces': txt(f.get(C['acces'])), 'adaptations': txt(f.get(C['adaptations'])),
            'financements': [FINANCEURS.get(x, x) for x in noms(f.get(C['financements']))],
            'objectifs': lire_objectifs(txt(f.get(C['objectifs']))), 'deroule': deroule,
            'inter': f.get(C['inter']), 'intra': f.get(C['intra']), 'materiel': materiel, 'materiel_brut': materiel_brut,
            'programme_brut': txt(f.get(C['programme'])),
        })
    return sorted(out, key=lambda x: x['ref'])


def incoherences(fs):
    """Écarts constatés entre les champs Airtable — signalés au dirigeant, jamais corrigés ici."""
    lignes = []
    for f in fs:
        jours_prog = len(f['deroule']) if f['ref'] != 'FOR-0011' else 3
        if jours_prog and jours_prog != f['jours']:
            lignes.append(f"{f['ref']} : {f['heures']} h dans Airtable ({f['jours']} j à 7 h), mais le programme Airtable décrit {jours_prog} jour(s).")
        if re.search(r'\(3 jours\)', f['titre']) and f['jours'] != 3:
            lignes.append(f"{f['ref']} : le titre annonce « 3 jours », la durée Airtable est de {f['heures']} h.")
        if re.search(r'8 heures (de formation )?par journée|16 heures au total|24 heures au total', f['programme_brut']):
            lignes.append(f"{f['ref']} : le texte du programme Airtable mentionne encore « 8 heures par journée ».")
        if re.search(r'4 à (8|10) stagiaires|Effectif : 4', f['public'] + f['programme_brut']):
            lignes.append(f"{f['ref']} : l'effectif « 4 à … » figure encore dans le public ou le programme Airtable.")
        if f['materiel_brut'] == 'À confirmer':
            lignes.append(f"{f['ref']} : matériel du stagiaire « À confirmer ».")
    return lignes

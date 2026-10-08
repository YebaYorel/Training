# Versions smartphone (1080 x 1920) de la grille tarifaire et du catalogue — mêmes données que les versions A4
from gen import F, e, eur, LEGAL, AI_NOTE

CSS = open('mobile.css').read()
def doc(title, screens):
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(screens)}</body></html>'

CHIPS = ('<div class="chips"><span><b>Qualiopi</b> · actions de formation</span><span><b>Google</b> AI Specialist</span>'
         '<span><b>Google</b> Professional AI</span><span><b>ANSSI</b> SecNumacadémie</span><span><b>CNIL</b> MOOC RGPD</span><span><b>Référent</b> handicap</span></div>')

def cover(kick, h1, lead, pill=True, h1size=92):
    p = '<div class="pill"><small>dès</small><b>690 €</b><small>/ stagiaire · journée de 7 h</small></div>' if pill else ''
    return f'''<section class="s cover">
  <div class="img"></div>
  <div class="hud mono"><span>YEBA FORMATIONS · Système IA</span><span>974 · La Réunion</span></div>
  <img class="logo" src="logo-white.png" alt="YEBA FORMATIONS">
  <div class="body">
    <div class="kick mono">{kick}</div>
    <h1 style="font-size:{h1size}px">{h1}</h1>
    <div class="lead">{lead}</div>
    {p}
    {CHIPS}
    <div class="swipe mono">Faites défiler →</div>
  </div>
</section>'''

def foot(doc_name, n, tot):
    return f'<div class="foot"><span class="mono">YEBA FORMATIONS · {doc_name}</span><span class="mono">{n} / {tot}</span></div>'

def row(ref, label=None):
    f = F[ref]; new = '<em class="new">NOUVEAU</em>' if f.get('new') else ''
    unit = '/ dirigeant / j' if ref == 'FOR-0014' else '/ stagiaire / j'
    return f'''<div class="row"><div class="n">{e(label or f["t"])}{new}</div><div class="d">{e(f["d"])}</div>
  <div class="pr"><b>{eur(f["inter"])}</b><small><em>inter {unit}</em></small><small>{eur(f["intra"])} <em>intra / j</em></small></div></div>'''

def box(tag, title, refs, acc='c', prem=False, note=''):
    n = f'<div class="note">{e(note)}</div>' if note else ''
    return f'''<div class="box {acc}{" prem" if prem else ""}"><div class="tag mono">{tag}</div><h3>{title}</h3><div class="rows">{"".join(row(r) for r in refs)}</div>{n}</div>'''

def grille():
    T = 4; S = []
    S.append(cover('Grille tarifaire · 2026', "Passez à l'IA.<br><span>Gardez la main.</span>", 'Former<i>·</i>Automatiser<i>·</i>RGPD &amp; IA Act', h1size=86))
    S.append(f'''<section class="s bg-grid g">
  <div class="top mono"><span><b>Grille tarifaire</b> · 2026</span><span>Prix par jour</span></div>
  <h2 style="margin-top:44px;font-size:70px">4 univers.<br><span>1 objectif : du temps gagné.</span></h2>
  <div class="legend"><b>Inter</b> = par stagiaire et par jour · <b>Intra</b> = par groupe et par jour · <b>6 à 8</b> participants · journée de <b>7 h</b></div>
  <div class="stack">{box('01 · Métiers', 'Vente &amp; management', ['FOR-0004','FOR-0008'])}{box('02 · Outils numériques', 'Outils numériques IA', ['FOR-0009','FOR-0010','FOR-0006'])}</div>
  {foot('GRILLE TARIFAIRE 2026', 2, T)}
</section>''')
    S.append(f'''<section class="s bg-grid g">
  <div class="top mono"><span><b>Grille tarifaire</b> · 2026</span><span>Prix nets de taxe</span></div>
  <div class="stack" style="margin-top:40px">{box('03 · Expertise IA', 'Expertise IA', ['FOR-0011','FOR-0015','FOR-0002'])}{box('04 · Premium', 'Gouvernance · IA avancée · Dirigeants', ['FOR-0003','FOR-0013','FOR-0014'], prem=True, note='Séminaire dirigeants : résidentiel, prix par dirigeant, hébergement en sus au réel.')}</div>
  <div class="legend">TVA non applicable, article 293 B du code général des impôts.</div>
  {foot('GRILLE TARIFAIRE 2026', 3, T)}
</section>''')
    S.append(f'''<section class="s bg-grid g">
  <div class="top mono"><span><b>Grille tarifaire</b> · 2026</span><span>Conseil · modalités</span></div>
  <div class="box consult" style="margin-top:40px"><div class="tag mono">Conseil · audit · implémentation IA</div>
    <ul style="margin-top:16px"><li><span>Diagnostic express · 30 min</span><b>100 €</b></li><li><span>Demi-journée</span><b>490 €</b></li><li><span>Journée</span><b>850 €</b></li></ul>
    <div class="note">Diagnostic déduit de la prestation suivante. Le conseil n'est pas une action de formation.</div></div>
  <div class="facts">
    <div class="fact"><div class="mono">Effectif</div><p>6 minimum, 8 maximum, en inter comme en intra.</p></div>
    <div class="fact"><div class="mono">Lieu</div><p>Communiqué par le formateur 15 jours avant.</p></div>
    <div class="fact"><div class="mono">Handicap</div><p>Référent handicap. Supports en corps 16 gratuits.</p></div>
    <div class="fact"><div class="mono">Financement</div><p>Votre OPCO, selon les règles de votre branche.</p></div>
  </div>
  <div class="cta"><div class="l">Votre diagnostic IA en 30 minutes<small>Délai d'accès : 15 jours ouvrés · 08h30–12h00 / 13h00–16h30</small></div>
    <div class="r">0693 32 24 45<small>yebaformations@gmail.com</small></div></div>
  <div class="legal">{e(LEGAL)}<br><i>{e(AI_NOTE)}</i></div>
  {foot('GRILLE TARIFAIRE 2026', 4, T)}
</section>''')
    return doc('Grille tarifaire 2026 — smartphone', S)

POLE = {'FOR-0011':('01','IA','c'),'FOR-0015':('01','IA','c'),'FOR-0014':('01','IA','c'),'FOR-0009':('01','IA','c'),'FOR-0010':('01','IA','c'),'FOR-0006':('01','IA','c'),
        'FOR-0002':('02','Automatisation','g'),'FOR-0013':('02','Automatisation','g'),'FOR-0003':('03','RGPD & IA Act','c'),'FOR-0004':('04','Vente & Management','g'),'FOR-0008':('04','Vente & Management','g')}

def fiche(ref, n, T):
    f = F[ref]; num, pole, acc = POLE[ref]
    new = '<span class="acc">NOUVEAU</span>' if f.get('new') else ''
    unit = '/ dirigeant / jour' if ref == 'FOR-0014' else '/ stagiaire / jour'
    note = f'<div class="note">{e(f["note"])}</div>' if f.get('note') else ''
    return f'''<section class="s bg-night f {acc}">
  <div class="top mono"><span><b>Pôle {num}</b> · {e(pole)}</span><span>{ref}</span></div>
  <h2>{e(f["t"])}</h2><div class="sub">{e(f["s"])}</div>
  <div class="meta"><span class="acc">{e(f["d"])}</span><span>6 à 8 participants</span>{new}</div>
  <div class="lbl">Pour qui</div><p class="txt">{e(f["qui"])}</p>
  <div class="lbl">Vous saurez</div><ul>{"".join(f"<li>{e(o).replace('e-mail', 'e\u2011mail')}</li>" for o in f["obj"])}</ul>
  <div class="lbl">Le + YEBA</div><p class="txt plus">{e(f["plus"])}</p>
  <div class="lbl">Prérequis</div><p class="txt">{e(f["pre"])}</p>
  <div class="price"><div><b>{eur(f["inter"])}</b><small>inter {unit}</small></div><div><b>{eur(f["intra"])}</b><small>intra / groupe / jour</small></div></div>
  {note}<div class="fin">{"".join(f"<span>{e(x)}</span>" for x in f["fin"])}</div>
  {foot('CATALOGUE 2026', n, T)}
</section>'''

def service(num, pole, acc, title, sub, blocks, n, T, rates=True):
    r = ('<div class="box consult svc" style="margin-top:40px"><ul><li><span>Diagnostic express · 30 min</span><b>100 €</b></li><li><span>Demi-journée</span><b>490 €</b></li><li><span>Journée</span><b>850 €</b></li></ul></div>') if rates else ''
    b = ''.join(f'<div class="lbl">{e(a)}</div><p class="txt">{c}</p>' for a, c in blocks)
    return f'''<section class="s bg-night f {acc}">
  <div class="top mono"><span><b>Pôle {num}</b> · {e(pole)}</span><span>Conseil</span></div>
  <h2>{title}</h2><div class="sub">{e(sub)}</div>
  {r}{b}
  {foot('CATALOGUE 2026', n, T)}
</section>'''

def catalogue():
    T = 18; S = []
    S.append(cover('Catalogue des formations · 2026', 'Former. Automatiser.<br><span>Protéger.</span> Vendre.', 'IA<i>·</i>Automatisation<br>RGPD &amp; IA Act<i>·</i>Vente &amp; Management', pill=False, h1size=80))
    tiles = [('c','IA','Gagner du temps avec l\'IA générative, en sécurité.','IA générative · IA souveraine · Séminaire dirigeants · Site internet · Emailing · Copilot','3 à 8'),
             ('g','Automatisation','Relier ses outils, déléguer aux agents, sous contrôle humain.','Automatisation sans code · Agents IA · Implémentation sur mesure','9 à 11'),
             ('c','RGPD &amp; IA Act','Sécuriser ses usages et prouver les mesures prises.','Conformité RGPD &amp; IA Act · Audit &amp; conseil','12 à 13'),
             ('g','Vente &amp; Management','Vendre sans brader, encadrer sans s\'épuiser.','Vente &amp; négociation · Manager au quotidien · Format intra','14 à 16')]
    tl = ''.join(f'<div class="tile {c}"><div class="h"><h3>{t}</h3><span class="pg mono">Écrans {pg}</span></div><p>{p}</p><div class="ls">{ls}</div></div>' for c,t,p,ls,pg in tiles)
    S.append(f'''<section class="s bg-night g">
  <div class="top mono"><span><b>Sommaire</b></span><span>Catalogue 2026</span></div>
  <h2 style="margin-top:44px;font-size:70px">Quatre pôles.<br><span>Un seul interlocuteur.</span></h2>
  <div class="tiles">{tl}</div>
  {foot('CATALOGUE 2026', 2, T)}
</section>''')
    n = 3
    for ref in ['FOR-0011','FOR-0015','FOR-0014','FOR-0009','FOR-0010','FOR-0006','FOR-0002','FOR-0013']:
        S.append(fiche(ref, n, T)); n += 1
    S.append(service('02','Automatisation','g','Implémentation<br>sur mesure','Nous concevons et mettons en place vos automatisations et vos agents IA',
        [('Pour qui',"Entreprises qui préfèrent confier la mise en place de leurs flux de travail automatisés et de leurs assistants IA."),
         ('Diagnostic express',"Environ 30 minutes d'échange, rapport sous 48 heures ouvrées, déduit de la prestation suivante."),
         ('Cadre',"Prestation de conseil, hors financement de la formation. Lorsque nous traitons des données pour votre compte, un contrat de sous-traitance (RGPD, art. 28) est conclu.")], n, T)); n += 1
    S.append(fiche('FOR-0003', n, T)); n += 1
    S.append(service('03','RGPD & IA Act','c','Audit &amp; conseil<br>en gouvernance',"Vos traitements et vos usages de l'IA passés en revue, avec un plan d'actions",
        [('Pour qui',"Dirigeants et responsables de TPE-PME qui veulent faire le point sur leurs traitements de données personnelles et leurs usages de l'IA."),
         ('Diagnostic express',"Environ 30 minutes d'échange, rapport sous 48 heures ouvrées, déduit de la prestation suivante."),
         ('Cadre',"Prestation de conseil, hors financement de la formation. Lorsque nous traitons des données pour votre compte, un contrat de sous-traitance (RGPD, art. 28) est conclu.")], n, T)); n += 1
    for ref in ['FOR-0004','FOR-0008']:
        S.append(fiche(ref, n, T)); n += 1
    S.append(f'''<section class="s bg-night f g">
  <div class="top mono"><span><b>Pôle 04</b> · Vente &amp; Management</span><span>Format intra</span></div>
  <h2>Toute l'équipe,<br>en une fois</h2><div class="sub">Une session dédiée à votre entreprise, dans vos locaux ou en salle louée</div>
  <div class="lbl">Le calcul</div>
  <div class="price" style="margin-top:14px;padding-top:0"><div><small>6 inscrits en inter</small><b>4&#8239;140&nbsp;€</b></div><div><small>1 groupe en intra</small><b>2&#8239;100&nbsp;€</b></div></div>
  <p class="txt">Exemple : Vente &amp; négociation, 1 jour. L'intra réunit 6 à 8 participants d'une même entreprise, au prix du groupe.</p>
  <div class="lbl">Ce qui est inclus</div>
  <ul><li>Supports individuels, livret ressource et grille critériée</li><li>Évaluations, correction et attestation de fin de formation</li><li>Suivi administratif complet : convention, convocations, émargements</li><li>Évaluation à chaud et à froid</li></ul>
  {foot('CATALOGUE 2026', n, T)}
</section>'''); n += 1
    steps = [('Diagnostic','Un échange pour analyser votre besoin, vos outils et vos contraintes.'),('Devis & convention','Devis valable 30 jours, puis convention ; programme remis avant l\'inscription.'),
             ('Positionnement','Un test avant la formation, pour adapter les ateliers.'),('Formation','30 % d\'apports, 70 % de pratique, sur vos situations réelles.'),
             ('Évaluation','Évaluation des acquis, attestation de fin de formation.'),('Suivi','Évaluation à froid, et suivi à J+30 selon la formation.')]
    st = ''.join(f'<li><span class="sn mono">{i+1}</span><b>{e(a)}</b><p>{e(b)}</p></li>' for i,(a,b) in enumerate(steps))
    S.append(f'''<section class="s bg-night g">
  <div class="top mono"><span><b>Comment ça se passe</b></span><span>Modalités</span></div>
  <h2 style="margin-top:44px;font-size:62px">Du premier appel<br><span>au suivi.</span></h2>
  <ol class="steps">{st}</ol>
  <div class="facts">
    <div class="fact"><div class="mono">Horaires</div><p>08h30–12h00 · 13h00–16h30</p></div>
    <div class="fact"><div class="mono">Effectif</div><p>6 à 8 ; en deçà, report puis remboursement.</p></div>
    <div class="fact"><div class="mono">Handicap</div><p>Référent dédié, aménagements dès l'inscription.</p></div>
    <div class="fact"><div class="mono">IA Act</div><p>Aucune IA n'évalue ni ne note les stagiaires.</p></div>
  </div>
  {foot('CATALOGUE 2026', n, T)}
</section>'''); n += 1
    S.append(f'''<section class="s back">
  <div class="img"></div><div class="veil"></div><div class="burst"></div>
  <img class="blogo" src="logo-white.png" alt="YEBA FORMATIONS">
  <div class="body">
    <div class="kick mono">Contact</div>
    <div class="name" style="margin-top:14px">Aurélien LUMEKA</div>
    <div class="role mono">Directeur · Formateur &amp; consultant IA</div>
    <div class="cl"><div><span class="mono">TEL</span>+262 693 32 24 45</div><div><span class="mono">MAIL</span>yebaformations@gmail.com</div><div><span class="mono">WEB</span>www.yebaformations.re</div><div><span class="mono">ADR</span>9 rue Françoise Châtelain<br>97490 Sainte-Clotilde</div></div>
    <div class="legal" style="margin-top:auto">{e(LEGAL)}<br><i>{e(AI_NOTE)}</i></div>
  </div>
</section>''')
    assert len(S) == T, len(S)
    return doc('Catalogue 2026 — smartphone', S)

open('grille_mobile.html', 'w').write(grille())
open('catalogue_mobile.html', 'w').write(catalogue())

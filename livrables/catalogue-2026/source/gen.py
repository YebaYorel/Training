# Générateur du catalogue YEBA FORMATIONS 2026 (A4 paysage) — contenu issu du CATALOGUE FORMATIONS Airtable
import html

FIN_ALL = ['OPCO', 'Plan de développement', 'France Travail', 'AIF', 'Région']

F = {
 'FOR-0011': dict(t="IA générative au travail", s="Gagner du temps chaque jour, en sécurité et avec des preuves", d="2 j · 14 h",
   qui="Tout salarié, manager, dirigeant ou indépendant qui utilise — ou va utiliser — l'IA générative dans son travail.",
   obj=["Expliquer ce que fait un modèle de langage, et ce qu'il ne fait pas", "Formuler une demande complète : rôle, contexte, format, contrainte",
        "Trier l'information : je saisis · j'anonymise · je ne saisis jamais", "Détecter une réponse fausse ou inventée, et tracer la vérification"],
   plus="Dossier de preuve des mesures IA pour l'entreprise · classe virtuelle de suivi à J+30",
   pre="Savoir utiliser un navigateur et une messagerie ; compte professionnel sur l'outil d'IA de l'employeur.",
   inter=790, intra=2400, fin=FIN_ALL),
 'FOR-0015': dict(t="IA souveraine", s="Faire tourner l'IA sur ses propres machines, sans donnée sortante", d="2 j · 14 h", new=True,
   qui="Dirigeants, responsables informatiques et référents IA de TPE-PME qui traitent des données sensibles : cabinets, santé, RH, bureaux d'études.",
   obj=["Distinguer modèle local et modèle distant, et ce que chacun expose", "Installer un moteur local et faire répondre un modèle sur son poste",
        "Démontrer, réseau coupé, qu'aucune donnée ne quitte la machine", "Choisir le modèle que son matériel peut réellement porter"],
   plus="La preuve par le câble : démonstration réseau coupé, conduite par le stagiaire",
   pre="Usage courant de l'IA générative ; poste avec droits d'administration (16 Go de mémoire recommandés).",
   inter=890, intra=2700, fin=['OPCO', 'Plan de développement']),
 'FOR-0014': dict(t="Séminaire dirigeants IA", s="Choisir les 3 tâches que l'IA fera pour vous", d="2 j · résidentiel",
   qui="Dirigeants de TPE-PME de 3 à 50 salariés. Huis clos, un dirigeant par entreprise, jamais deux concurrents directs.",
   obj=["Identifier les 3 tâches qui libèrent le plus de temps, chiffrées en heures par mois", "Qualifier chaque tâche au regard de l'IA Act",
        "Fixer le niveau d'autonomie acceptable selon le coût de l'erreur", "Repartir avec le plan d'agents de son entreprise"],
   plus="Plan d'agents écrit de deux pages, présenté au groupe",
   pre="Venir avec ses 5 tâches les plus chronophages, son chiffre d'affaires, son effectif et ses outils.",
   inter=990, intra=2900, unit_inter="/ dirigeant / jour", note="Hébergement en sus, au réel", fin=['OPCO', 'Plan de développement']),
 'FOR-0009': dict(t="Site internet IA", s="Créer son site en le décrivant à voix haute", d="1 j · 7 h",
   qui="Dirigeants de TPE, artisans, commerçants et indépendants sans site, ou dépendants de leur prestataire pour la moindre modification.",
   obj=["Dicter un cahier des charges exploitable", "Piloter à la voix un outil de génération de site",
        "Vérifier chaque contenu : textes, tarifs, coordonnées", "Publier un site conforme : mentions légales, confidentialité, traceurs, accessibilité"],
   plus="Chaque stagiaire repart avec son site en ligne",
   pre="Usage courant d'un ordinateur ; venir avec son projet réel (activité, tarifs, photos).",
   inter=790, intra=2500, fin=['OPCO', 'Plan de développement', 'Région', 'France Travail', 'AIF']),
 'FOR-0010': dict(t="Emailing IA", s="Rédiger des courriels et des séquences qui obtiennent une réponse", d="1 j · 7 h",
   qui="Dirigeants, indépendants, commerciaux, fonctions administratives et chargés de communication.",
   obj=["Constituer une base de contacts conforme au RGPD", "Rédiger avec l'IA un courriel qui obtient une réponse",
        "Concevoir une séquence et régler son rythme", "Mesurer et corriger : ouverture, clic, désinscription"],
   plus="Fichier assaini et segmenté, et sa fiche de registre « prospection »",
   pre="Messagerie et tableur simple ; venir avec son fichier, un courriel déjà envoyé et son offre.",
   inter=790, intra=2500, fin=['OPCO', 'Plan de développement', 'Région', 'AIF']),
 'FOR-0006': dict(t="Copilot Microsoft 365", s="L'IA dans Word, Excel, Outlook et Teams — méthode des 4 P", d="2 j · 14 h",
   qui="Salariés et dirigeants équipés de Microsoft 365 qui produisent chaque semaine documents, analyses et courriels.",
   obj=["Périmètre : savoir ce que l'assistant voit, à partir des droits en place", "Prompt : formuler une demande complète en désignant ses sources",
        "Production : documents, tableaux et courriels sur ses vrais dossiers", "Preuve : vérifier et documenter le résultat"],
   plus="Ateliers sur les documents réels de l'entreprise",
   pre="Licence Copilot nominative active et documents professionnels réels, vérifiés par écrit 5 jours ouvrés avant.",
   inter=790, intra=2500, fin=FIN_ALL),
 'FOR-0002': dict(t="Automatisation sans code", s="Relier ses outils et supprimer les tâches répétitives (n8n)", d="2 j · 14 h",
   qui="Dirigeants de TPE-PME, indépendants et fonctions administratives qui veulent gagner du temps et fiabiliser leurs processus.",
   obj=["Repérer les tâches répétitives qui méritent d'être automatisées", "Concevoir un workflow : déclencheur → conditions → actions",
        "Mettre en place une automatisation (formulaire → base → e-mail)", "Sécuriser les données et respecter le RGPD ; mesurer le temps gagné"],
   plus="On vient avec une tâche répétitive réelle, on repart avec son automatisation",
   pre="Usage courant des outils bureautiques et du web. Aucune compétence en développement.",
   inter=990, intra=2900, fin=FIN_ALL),
 'FOR-0013': dict(t="Agents IA", s="Déléguer des tâches à l'IA sous contrôle humain · niveau avancé", d="2 j · 14 h",
   qui="Dirigeants, responsables informatiques, référents IA et chefs de projet à l'usage avancé de l'IA générative.",
   obj=["Distinguer assistant, agent et système multi-agents", "Mettre en service un agent qui exécute une tâche de bout en bout",
        "Chaîner deux agents avec un point de contrôle humain obligatoire", "Fixer le niveau d'autonomie acceptable"],
   plus="Kit de gouvernance des agents · procédure d'arrêt d'urgence testée · revue à J+30",
   pre="Usage avancé de l'IA (ou « IA générative au travail ») ; accepter de travailler dans un terminal.",
   inter=990, intra=2900, fin=FIN_ALL),
 'FOR-0003': dict(t="Conformité RGPD & IA Act", s="Sécuriser ses usages de l'IA et prouver les mesures prises", d="1 j · 7 h",
   qui="Dirigeants, responsables administratifs et tout salarié qui manipule des données personnelles : RH, commercial, gestion.",
   obj=["Identifier les données personnelles et les traitements soumis au RGPD", "Appliquer les 6 principes clés : licéité, minimisation, exactitude, conservation, sécurité, responsabilité",
        "Constituer et tenir à jour le registre des traitements", "Prévenir les menaces cyber : hameçonnage, rançongiciel, mots de passe faibles",
        "Réagir à une violation de données : mesures conservatoires, notification CNIL sous 72 h", "Qualifier ses usages de l'IA au regard de l'IA Act et rédiger la charte d'usage de l'IA"],
   plus="Registre des traitements démarré en séance",
   pre="Aucun prérequis technique.",
   inter=690, intra=2100, fin=FIN_ALL),
 'FOR-0004': dict(t="Vente & négociation", s="Découvrir le besoin, argumenter et conclure sans brader", d="1 j · 7 h",
   qui="Créateurs d'entreprise, indépendants, commerciaux débutants, et toute personne amenée à vendre.",
   obj=["Dérouler les étapes d'un entretien de vente", "Mener une découverte par un questionnement structuré",
        "Construire une proposition de valeur adaptée au besoin", "Traiter les objections, conclure et organiser le suivi"],
   plus="Fiche de préparation réutilisable pour tout rendez-vous",
   pre="Aucun. Venir avec un produit ou un service que l'on vend réellement.",
   inter=690, intra=2100, fin=FIN_ALL),
 'FOR-0008': dict(t="Manager au quotidien", s="Cadrer, déléguer et recadrer son équipe de proximité", d="1 j · 7 h",
   qui="Encadrants de proximité, chefs d'équipe, responsables de rayon ou de service, dirigeants de TPE qui encadrent directement.",
   obj=["Poser un cadre clair : règles, objectifs, priorités", "Déléguer : objectif, moyens, échéance, points de contrôle",
        "Conduire un recadrage factuel, sans dévaloriser", "Désamorcer une tension ; conduire un point individuel"],
   plus="Charte d'équipe en une page",
   pre="Exercer, ou s'apprêter à exercer, une fonction d'encadrement direct.",
   inter=790, intra=2400, fin=FIN_ALL),
}

def e(s): return html.escape(s, quote=False)
def eur(n): return f"{n:,}".replace(',', ' ') + ' €'

ICON = {
 'ia':   '<circle cx="24" cy="24" r="7"/><path d="M24 4v8M24 36v8M4 24h8M36 24h8M10 10l6 6M32 32l6 6M38 10l-6 6M16 32l-6 6"/>',
 'auto': '<rect x="5" y="8" width="12" height="10" rx="2"/><rect x="31" y="8" width="12" height="10" rx="2"/><rect x="18" y="30" width="12" height="10" rx="2"/><path d="M17 13h14M11 18v7h13v5M37 18v7H24"/>',
 'rgpd': '<path d="M24 4 7 10v12c0 10 7 17 17 22 10-5 17-12 17-22V10z"/><path d="m16 24 6 6 11-12"/>',
 'vente':'<path d="M6 34 18 22l7 7 17-17"/><path d="M32 12h10v10"/><path d="M6 42h36"/>',
}
def icon(k, cls='ico'): return f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

def card(ref, acc):
    f = F[ref]
    obj = ''.join(f'<li>{e(o)}</li>' for o in f['obj'])
    fin = ''.join(f'<span>{e(x)}</span>' for x in f['fin'])
    new = '<em class="new">NOUVEAU</em>' if f.get('new') else ''
    note = f'<div class="note">{e(f["note"])}</div>' if f.get('note') else ''
    return f'''<article class="card rv {acc}">
  <div class="ctop"><span class="ref">{ref}</span>{new}<span class="dur">{e(f["d"])}</span></div>
  <h3>{e(f["t"])}</h3><p class="sub">{e(f["s"])}</p>
  <div class="lbl">Pour qui</div><p class="txt">{e(f["qui"])}</p>
  <div class="lbl">Vous saurez</div><ul>{obj}</ul>
  <div class="lbl">Le + YEBA</div><p class="txt plus">{e(f["plus"])}</p>
  <div class="lbl">Prérequis</div><p class="txt">{e(f["pre"])}</p>
  <div class="price">
    <div><b>{eur(f["inter"])}</b><small>inter {e(f.get("unit_inter","/ stagiaire / jour"))}</small></div>
    <div><b>{eur(f["intra"])}</b><small>intra / groupe / jour</small></div>
  </div>{note}
  <div class="fin">{fin}</div>
</article>'''

def svc(title, sub, lines, foot, acc, extra=''):
    li = ''.join(f'<li><span>{e(a)}</span><b>{e(b)}</b></li>' for a, b in lines)
    return f'''<article class="card svc rv {acc}">
  <div class="ctop"><span class="ref">CONSEIL</span><span class="dur">sur devis</span></div>
  <h3>{e(title)}</h3><p class="sub">{e(sub)}</p>
  <ul class="rates">{li}</ul>
  {extra}
  <p class="txt foot">{e(foot)}</p>
</article>'''

def intra_card(acc):
    return f'''<article class="card svc rv {acc}">
  <div class="ctop"><span class="ref">FORMAT INTRA</span><span class="dur">dans vos murs</span></div>
  <h3>Toute l'équipe, en une fois</h3><p class="sub">Une session dédiée à votre entreprise, dans vos locaux ou en salle louée</p>
  <div class="lbl">Le calcul</div>
  <div class="calc"><div><small>6 inscrits en inter</small><b>4&#8239;140&nbsp;€</b></div><div class="vs">contre</div><div><small>1 groupe en intra</small><b>2&#8239;100&nbsp;€</b></div></div>
  <p class="txt">Exemple : Vente &amp; négociation, 1 jour. L'intra réunit 6 à 8 participants d'une même entreprise, au prix du groupe.</p>
  <div class="lbl">Ce qui est inclus</div>
  <ul><li>Supports individuels, livret ressource et grille critériée</li><li>Évaluations, correction et attestation de fin de formation</li><li>Suivi administratif complet : convention, convocations, émargements</li><li>Évaluation à chaud et à froid</li></ul>
</article>'''

def pole_page(num, key, acc, title, promise, facts, cards, pno, suite=False):
    return f'''<section class="page pole" data-p="{pno}">
  <aside class="band {acc}">
    <div class="pnum mono rv">Pôle {num}{" · suite" if suite else ""}</div>
    {icon(key, 'bico rv')}
    <h2 class="rv">{title}</h2>
    <p class="promise rv">{e(promise)}</p>
    <ul class="facts rv">{''.join(f"<li>{e(x)}</li>" for x in facts)}</ul>
    <div class="folio mono">YEBA FORMATIONS · CATALOGUE 2026 <b>{pno:02d}</b></div>
  </aside>
  <div class="cards n{len(cards)}">{''.join(cards)}</div>
</section>'''

LEGAL = ("YEBA FORMATIONS — Aurélien LUMEKA, directeur · 9 rue Françoise Châtelain, 97490 Sainte-Clotilde, La Réunion · Tél. 0693 32 24 45 · "
 "yebaformations@gmail.com · SIRET 814 622 262 00032 · Déclaration d'activité n° 04973676397 auprès du Préfet de La Réunion. Cet enregistrement ne vaut pas agrément de l'État. "
 "Certification Qualiopi n° 25FOR02027.1 délivrée au titre de la catégorie actions de formation — organisme certificateur Qualitia (accrédité COFRAC). "
 "Référent handicap : Aurélien LUMEKA — yebaformations@gmail.com")
AI_NOTE = ("Ce document a été conçu par le formateur avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689, art. 50). "
 "Son contenu a été vérifié et validé par un humain, qui en assume la responsabilité.")

def pages(animated=False):
    P = []
    # 1 — COUVERTURE
    cover_media = '<div class="cimg" id="cimg"></div>' if not animated else '<img class="cimg" id="cvid" src="vf/f001.jpg" alt="">'
    P.append(f'''<section class="page cover" data-p="1">
  {cover_media}
  <div class="cfade"></div>
  <div class="cpanel">
    <img class="clogo rv" src="logo-white.png" alt="YEBA FORMATIONS">
    <div class="ckick mono rv">Catalogue des formations · 2026</div>
    <h1 class="rv">Former.<br>Automatiser.<br><span>Protéger.</span><br>Vendre.</h1>
    <ul class="cpoles rv"><li><i class="c"></i>IA</li><li><i class="g"></i>Automatisation</li><li><i class="c"></i>RGPD &amp; IA Act</li><li><i class="g"></i>Vente &amp; Management</li></ul>
    <div class="cfoot mono rv">La Réunion · 974 &nbsp;|&nbsp; <b>Qualiopi</b> · actions de formation</div>
  </div>
</section>''')
    # 2 — SOMMAIRE
    tiles = [('01','ia','c','IA','Gagner du temps avec l\'IA générative, en sécurité.','6 formations · dès 790 € / stagiaire / jour','03',['IA générative au travail','IA souveraine','Séminaire dirigeants IA','Site internet IA','Emailing IA','Copilot Microsoft 365']),
             ('02','auto','g','Automatisation','Relier ses outils, déléguer aux agents, sous contrôle humain.','2 formations + mise en place sur mesure','05',['Automatisation sans code (n8n)','Agents IA','Implémentation sur mesure']),
             ('03','rgpd','c','RGPD &amp; IA Act','Sécuriser ses usages et prouver les mesures prises.','1 formation + audit et conseil','06',['Conformité RGPD & IA Act','Audit & conseil en gouvernance']),
             ('04','vente','g','Vente &amp; Management','Vendre sans brader, encadrer sans s\'épuiser.','2 formations · dès 690 € / stagiaire / jour','07',['Vente & négociation','Manager au quotidien','Format intra'])]
    tl = ''.join(f'''<a class="tile rv {c}"><div class="tnum mono">{n}</div>{icon(k,'tico')}<h3>{t}</h3><p>{p}</p><ul class="tl">{''.join(f"<li>{e(x)}</li>" for x in lst)}</ul><div class="tbot"><span class="tmeta mono">{m}</span><span class="tpg mono">p. {pg}</span></div></a>''' for n,k,c,t,p,m,pg,lst in tiles)
    P.append(f'''<section class="page som" data-p="2">
  <div class="sleft">
    <div class="kick mono rv">Sommaire</div>
    <h2 class="rv">Quatre pôles.<br><span>Un seul interlocuteur.</span></h2>
    <p class="lead rv">De la formation au conseil, le même formateur vous accompagne du diagnostic à la mise en œuvre — en vente et management comme en intelligence artificielle et en gouvernance des données.</p>
    <div class="proof rv">
      <div class="mono">Preuves de compétence</div>
      <ul><li><b>Qualiopi</b> · actions de formation</li><li><b>Google</b> AI Specialist</li><li><b>Google</b> Professional AI</li><li><b>ANSSI</b> SecNumacadémie</li><li><b>CNIL</b> MOOC RGPD</li><li><b>Référent</b> handicap</li></ul>
    </div>
    <div class="keys rv">
      <div><b>7 h</b><small>par journée</small></div><div><b>6 à 8</b><small>stagiaires</small></div><div><b>15 j</b><small>ouvrés d'accès</small></div><div><b>70 %</b><small>de pratique</small></div>
    </div>
    <div class="folio mono">YEBA FORMATIONS · CATALOGUE 2026 <b>02</b></div>
  </div>
  <div class="tiles">{tl}<div class="also rv mono">Et aussi · Comment ça se passe <b>p. 08</b> · Tarifs en un coup d'œil <b>p. 09</b></div></div>
</section>''')
    # 3–7 — PÔLES
    P.append(pole_page('01','ia','c','Intelligence<br>artificielle',"Gagner du temps chaque jour avec l'IA générative — sans exposer vos données, et en gardant la main.",
             ['Outils américains et européens enseignés à parité','Aucune commission d\'éditeur','Ateliers sur vos vrais dossiers'],
             [card('FOR-0011','c'),card('FOR-0015','c'),card('FOR-0014','c')],3))
    P.append(pole_page('01','ia','c','Intelligence<br>artificielle',"Des outils précis pour des besoins précis : votre site, vos courriels, votre suite Microsoft.",
             ['Chaque stagiaire vient avec sa situation réelle','30 % d\'apports, 70 % de pratique'],
             [card('FOR-0009','c'),card('FOR-0010','c'),card('FOR-0006','c')],4,suite=True))
    P.append(pole_page('02','auto','g','Automa&shy;tisation',"Supprimer les tâches répétitives, puis déléguer à des agents — toujours sous contrôle humain.",
             ['Workflows sans code (n8n)','Agents avec point d\'arrêt humain','Mise en place possible par nos soins'],
             [card('FOR-0002','g'),card('FOR-0013','g'),
              svc('Implémentation sur mesure','Nous concevons et mettons en place vos automatisations et vos agents IA',
                  [('Diagnostic express · 30 min','100 €'),('Demi-journée','490 €'),('Journée','850 €')],
                  "Diagnostic déduit de la prestation suivante. Prestation de conseil : elle n'est pas une action de formation et ne relève pas du plan de développement des compétences.",'g',
                  extra='<div class="lbl">Pour qui</div><p class="txt">Entreprises qui préfèrent confier la mise en place de leurs flux de travail automatisés et de leurs assistants IA.</p><div class="lbl">Diagnostic express</div><p class="txt">Environ 30 minutes d\'échange, rapport sous 48 heures ouvrées.</p><div class="lbl">Cadre</div><p class="txt">Lorsque nous traitons des données pour votre compte, un contrat de sous-traitance (RGPD, art. 28) est conclu.</p>')],5))
    P.append(pole_page('03','rgpd','c','RGPD<br>&amp; IA Act',"Sécuriser vos usages des données et de l'IA, et pouvoir prouver les mesures prises.",
             ['Registre, charte IA, réflexes cyber','Qualification IA Act : interdit, haut risque, transparence'],
             [card('FOR-0003','c'),
              svc('Audit & conseil en gouvernance','Vos traitements et vos usages de l\'IA passés en revue, avec un plan d\'actions',
                  [('Diagnostic express · 30 min','100 €'),('Demi-journée','490 €'),('Journée','850 €')],
                  "Diagnostic déduit de la prestation suivante. Prestation de conseil, hors financement de la formation.",'c',
                  extra='<div class="lbl">Pour qui</div><p class="txt">Dirigeants et responsables de TPE-PME qui veulent faire le point sur leurs traitements de données personnelles et leurs usages de l\'IA.</p><div class="lbl">Diagnostic express</div><p class="txt">Environ 30 minutes d\'échange, rapport sous 48 heures ouvrées.</p><div class="lbl">Cadre</div><p class="txt">Lorsque nous traitons des données pour votre compte, un contrat de sous-traitance (RGPD, art. 28) est conclu.</p>')],6))
    P.append(pole_page('04','vente','g','Vente<br>&amp; Management',"Les fondamentaux qui font tourner une TPE : vendre au juste prix, encadrer avec méthode.",
             ['Mises en situation sur vos cas réels','Aucun ordinateur nécessaire'],
             [card('FOR-0004','g'),card('FOR-0008','g'),intra_card('g')],7))
    # 8 — COMMENT ÇA SE PASSE
    steps = [('Diagnostic','Un échange pour analyser votre besoin, vos outils et vos contraintes.'),
             ('Devis & convention','Devis nominatif valable 30 jours, puis convention ; programme remis avant l\'inscription.'),
             ('Positionnement','Un test avant la formation, pour adapter les ateliers au niveau de chacun.'),
             ('Formation','30 % d\'apports, 70 % de pratique, sur vos situations réelles.'),
             ('Évaluation','Évaluation des acquis, attestation de fin de formation.'),
             ('Suivi','Évaluation à froid, et suivi à J+30 selon la formation.')]
    st = ''.join(f'<li class="rv"><span class="sn mono">{i+1}</span><b>{e(a)}</b><p>{e(b)}</p></li>' for i,(a,b) in enumerate(steps))
    blocks = [('Horaires','08h30–12h00 · 13h00–16h30, soit 7 heures par journée.'),
              ('Effectif','6 stagiaires minimum, 8 maximum, en inter comme en intra. En deçà de 6 : report ; remboursement intégral si l\'effectif n\'est pas atteint un mois après.'),
              ('Lieu & délai','Lieu communiqué par le formateur 15 jours avant la formation. Délai d\'accès : 15 jours ouvrés minimum.'),
              ('Financement','OPCO et plan de développement des compétences, selon les règles de votre branche ; autres financeurs selon la formation. Nous montons le dossier avec vous.'),
              ('Handicap','Référent handicap : Aurélien LUMEKA. Besoin d\'aménagement étudié dès l\'inscription. Supports en corps 16 gratuits.'),
              ('RGPD & IA Act','Données des stagiaires limitées à la gestion de la formation. Aucun système d\'IA n\'évalue, ne note ni ne classe les stagiaires : la correction est faite par le formateur.')]
    bl = ''.join(f'<div class="blk rv"><div class="mono">{e(a)}</div><p>{e(b)}</p></div>' for a,b in blocks)
    P.append(f'''<section class="page how" data-p="8">
  <div class="hhead"><div class="kick mono rv">Comment ça se passe</div><h2 class="rv">De votre premier appel <span>au suivi après formation.</span></h2></div>
  <ol class="steps">{st}</ol>
  <div class="blocks">{bl}</div>
  <div class="folio mono abs">YEBA FORMATIONS · CATALOGUE 2026 <b>08</b></div>
</section>''')
    # 9 — TARIFS
    groups = [('IA','c',['FOR-0011','FOR-0015','FOR-0014','FOR-0009','FOR-0010','FOR-0006']),('Automatisation','g',['FOR-0002','FOR-0013']),
              ('RGPD & IA Act','c',['FOR-0003']),('Vente & Management','g',['FOR-0004','FOR-0008'])]
    rows=''
    for g,c,refs in groups:
        rows += f'<tr class="grp {c}"><th colspan="4">{e(g)}</th></tr>'
        for r in refs:
            f=F[r]; rows += f'<tr><td><span class="mono">{r}</span> {e(f["t"])}</td><td>{e(f["d"])}</td><td class="n">{eur(f["inter"])}</td><td class="n">{eur(f["intra"])}</td></tr>'
    P.append(f'''<section class="page tar" data-p="9">
  <div class="tleft">
    <div class="kick mono rv">Tarifs en un coup d'œil</div>
    <h2 class="rv">Prix par jour.<br><span>Nets de taxe.</span></h2>
    <p class="lead rv">TVA non applicable, article 293 B du code général des impôts. Inter : par stagiaire et par jour. Intra : par groupe et par jour, pour 6 à 8 participants d'une même entreprise.</p>
    <div class="consult rv"><div class="mono">Conseil · audit · implémentation</div><ul><li><span>Diagnostic express · 30 min</span><b>100 €</b></li><li><span>Demi-journée</span><b>490 €</b></li><li><span>Journée</span><b>850 €</b></li></ul><p>Diagnostic déduit de la prestation suivante.</p></div>
    <p class="small rv">Séminaire dirigeants : prix par dirigeant, hébergement en sus au réel. Tarifs au 08/10/2026 — politique tarifaire YEBA-DOC-12 v3.1.</p>
    <div class="folio mono">YEBA FORMATIONS · CATALOGUE 2026 <b>09</b></div>
  </div>
  <div class="tright rv"><table><thead><tr><th>Formation</th><th>Durée</th><th class="n">Inter<small>/ stagiaire / jour</small></th><th class="n">Intra<small>/ groupe / jour</small></th></tr></thead><tbody>{rows}</tbody></table>
    <div class="tstrip"><div><span class="mono">Effectif</span>6 à 8 participants, en inter comme en intra</div><div><span class="mono">Horaires</span>08h30–12h00 · 13h00–16h30</div><div><span class="mono">Financement</span>OPCO et plan de développement, selon votre branche</div></div></div>
</section>''')
    # 10 — DERNIÈRE PAGE : le logo dans l'œil
    P.append(f'''<section class="page back" data-p="10">
  <div class="bimg" id="bimg"></div>
  <svg class="streaks" id="streaks" viewBox="0 0 297 210" preserveAspectRatio="none" aria-hidden="true"><g id="sk" stroke-linecap="round"></g></svg>
  <div class="bflare"></div><div class="bveil"></div><div class="bburst" id="bburst"></div>
  <img class="blogo" id="blogo" src="logo-white.png" alt="YEBA FORMATIONS">
  <div class="bband">
    <div class="bcol"><div class="mono g">Contact</div><div class="bname">Aurélien LUMEKA</div><div class="brole mono">Directeur · Formateur &amp; consultant IA</div></div>
    <div class="bcol"><div class="bl"><span class="mono">TEL</span>+262 693 32 24 45</div><div class="bl"><span class="mono">MAIL</span>yebaformations@gmail.com</div><div class="bl"><span class="mono">WEB</span>www.yebaformations.re</div><div class="bl"><span class="mono">ADR</span>9 rue Françoise Châtelain, 97490 Sainte-Clotilde</div></div>
    <div class="blegal">{e(LEGAL)}<br><i>{e(AI_NOTE)}</i></div>
  </div>
</section>''')
    return P

"""Étude tarifaire : concurrents, plafonds des financeurs, trois positionnements par titre."""
from lib import HORAIRES, ORGANISME, Doc
from titres import MEM, RPMS, heures_centre

O, H = ORGANISME, HORAIRES
EFFECTIF = 10

# (organisme, titre, modalité, durée en centre, prix, €/h, source)
CONCURRENTS = [
    ("AFPA (national)", "Manager d'établissement marchand", "Présentiel", "1 085 h", "7 847 €", "7,2 €", "AFPA"),
    ("AFPA (national)", "Manager d'unité marchande (ancienne version)", "Présentiel", "1 330 h", "9 100 €", "6,8 €", "AFPA"),
    ("AFPA (national)", "Un bloc de compétences (CCP)", "Présentiel", "287 h", "3 349 €", "11,7 €", "AFPA"),
    ("Enaco", "Manager d'établissement marchand", "100 % à distance", "non publiée", "dès 3 590 € TTC", "—", "Enaco"),
    ("Organisme national (annuaire)", "Manager d'unité marchande", "À distance", "380 h", "4 590 €", "12,1 €", "annuaire"),
    ("Studi et autres", "Responsable de petite ou moyenne structure", "À distance", "variable", "3 750 € à 4 590 €", "—", "Studi, Enaco"),
    ("Organisme national", "Responsable de petite ou moyenne structure", "Alternance", "variable", "9 000 € HT", "—", "annuaire"),
    ("Camas Formation (Réunion)", "Manager d'unité marchande", "Présentiel", "400 h", "affiché « gratuit »", "—", "Camas"),
    ("ICCI, IFORMA-SUD, RunApp, Pro'pulse (Réunion)", "Titres du commerce", "Alternance", "536 à 910 h", "gratuit pour l'apprenti (OPCO)", "—", "leurs sites"),
]

PLAFONDS = [
    ("Région Réunion — Pass Formation", "5 000 € par projet et par an (page Région) ; 5 500 € (règlement d'intervention)", "Sources contradictoires : à vérifier auprès de la Région"),
    ("France Travail — AIF", "8 000 € pour un demandeur d'emploi (plafond cité par plusieurs sites)", "Source non officielle : à vérifier auprès de la direction régionale"),
    ("CPF", "Solde du compte du stagiaire (plafond légal 5 000 €, 8 000 € pour les moins qualifiés)", "Le stagiaire salarié paie une participation forfaitaire, sauf exceptions"),
    ("Région Réunion — marché public", "Prix comparé à l'heure-stagiaire", "Aucun prix horaire régional publié n'a été trouvé"),
]


def _scenarios(t, prix):
    hc = heures_centre(t)
    out = []
    for nom, p in zip(("A — Accessible", "B — Recommandé", "C — Premium"), prix):
        ca = p * EFFECTIF
        loc = round(hc / 7) * H["location_jour"]
        out.append([nom, f"{p:,} €".replace(",", " "), f"{p / hc:.2f} €".replace(".", ","), f"{ca:,} €".replace(",", " "),
                    f"{ca - loc:,} €".replace(",", " ")])
    return out


def etude():
    d = Doc("Étude tarifaire et positionnement", "Titres professionnels MEM et RPMS — promotions de 10 stagiaires", code="TAR-01")
    d.encadre("En une phrase", [
        "Recommandation : **4 900 € par stagiaire pour le MEM** et **4 950 € pour le RPMS**, soit environ 8,3 à 8,8 € de l'heure en centre. "
        "C'est sous le plafond du Pass Formation de la Région (5 000 €), sous les plafonds de l'AIF, au-dessus des offres à distance "
        "et proche du coût horaire de l'AFPA, avec en plus le présentiel, le suivi individuel et le module IA. La décision vous appartient.",
    ])
    d.h1("1. Méthode et limites")
    d.puces([
        "Prix publics relevés le 22/10/2026 sur les sites des organismes ; le coût horaire est calculé sur les heures en centre, hors période en entreprise.",
        "À La Réunion, peu d'organismes publient leur prix : les offres locales sont surtout en alternance (gratuites pour l'apprenti) ou financées par la Région.",
        "Les plafonds des financeurs proviennent en partie de sources secondaires : ils sont signalés « à vérifier ».",
        "Avant de trancher : appeler deux centres réunionnais en tant que prospect et demander au Carif-Oref Réunion les prix pratiqués.",
    ])
    d.h1("2. Ce que pratiquent les concurrents")
    d.tableau(["Organisme", "Titre", "Modalité", "Durée", "Prix", "€ / h", "Source"],
              [list(c) for c in CONCURRENTS], [3.3, 3.6, 2.2, 1.7, 2.5, 1.4, 2.3], taille=9)
    d.p("Lecture : le présentiel national se situe autour de 7 € de l'heure (AFPA) ; un bloc seul est vendu plus cher à l'heure (près de 12 €). "
        "Les offres à distance coûtent 3 600 à 4 600 € au total, mais sans présentiel ni accompagnement de proximité.")
    d.h1("3. Ce que les financeurs peuvent payer")
    d.tableau(["Financeur", "Plafond ou critère", "Remarque"], [list(p) for p in PLAFONDS], [4.5, 7, 5.5])
    d.p("Conséquence : **rester à 5 000 € ou moins par stagiaire** permet à un demandeur d'emploi d'être financé en totalité par le Pass Formation, "
        "sans cofinancement. C'est le premier critère de choix d'un conseiller.")
    d.h1("4. Trois positionnements par titre")
    for t, prix in ((MEM, (4200, 4900, 5600)), (RPMS, (4300, 4950, 5900))):
        d.h2(f"{t['court']} — {heures_centre(t)} h en centre")
        d.tableau(["Scénario", "Prix par stagiaire", "€ / h en centre", "Chiffre d'affaires (10)", "Après location de salle"],
                  _scenarios(t, prix), [3.6, 3.2, 2.8, 3.8, 3.6])
    d.tableau(["Scénario", "Pour", "Contre"], [
        ["A — Accessible", "Très facile à financer ; argument prix face aux appels d'offres", "Marge faible ; image « bas de gamme » ; peu de place pour l'examen et le matériel"],
        ["B — Recommandé", "Sous les plafonds des financeurs ; présentiel et suivi valorisés ; marge correcte", "Un peu au-dessus des offres à distance : il faut expliquer la valeur"],
        ["C — Premium", "Marge élevée ; positionnement « excellence »", "Au-dessus du Pass Formation : cofinancement obligatoire, risque de perdre les prescriptions"],
    ], [3.4, 6.8, 6.8])
    d.h1("5. Les autres prix à fixer")
    d.tableau(["Offre", "Proposition", "Justification"], [
        ["Un CCP seul (salariés, CPF)", "1 950 € par CCP", "Environ 10 € de l'heure, en dessous du bloc AFPA (11,7 €)"],
        ["Réponse à un marché de la Région", "8,75 € par heure-stagiaire (MEM)", "Même niveau que le scénario B, exprimé comme l'attend un acheteur public"],
        ["Examen par un centre agréé partenaire", "Inclus dans le prix", "Évite un reste à charge qui fait renoncer le stagiaire [À VÉRIFIER : coût réel du partenaire]"],
    ], [5, 4.5, 7.5])
    d.h1("6. Trois points à ne pas oublier")
    d.numeros([
        "**TVA** : 10 stagiaires à 4 900 € représentent 49 000 € de recettes, ce qui dépasse probablement le seuil de franchise. Sans l'attestation 3511-SD, "
        "il faudrait ajouter la TVA et le prix sortirait des plafonds. Demandez l'attestation avant de publier vos prix.",
        "**Rentabilité réelle** : vos formations courtes rapportent 690 à 990 € par stagiaire et par jour, contre environ 60 € par jour pour un titre. "
        "Le titre apporte du volume, de la régularité et une image ; il ne remplace pas vos formations courtes, qui restent votre marge.",
        "**Seuil de maintien** : le classeur PIL-03 calcule le nombre minimal de stagiaires pour couvrir les charges ; fixez le seuil de maintien de la session "
        "en conséquence, et indiquez-le dans les conditions particulières.",
    ])
    d.h1("7. Sources")
    d.puces([
        "AFPA : afpa.fr, fiches « Manager d'établissement marchand » et « Manager d'unité marchande » (consultées le 22/10/2026).",
        "Enaco : enaco.fr ; Studi : studi.com ; je-change-de-metier.com (offres à distance).",
        "Organismes réunionnais : camasformation.fr, icci-formations.re, iforma.re, runapp.fr, propulse.re.",
        "Région Réunion : regionreunion.com (Pass Formation) et règlement d'intervention du Pass Formation.",
        "AIF : sites d'information (mondedutravail.fr, aide-sociale.fr) — plafond à confirmer auprès de France Travail.",
    ])
    return d.save("05_Pilotage_annuel/TAR-01_Etude_tarifaire_et_positionnement.docx")


def tout():
    return [etude()]


if __name__ == "__main__":
    from lib import ERREURS_MISE_EN_PAGE
    print(tout())
    print("\n".join(ERREURS_MISE_EN_PAGE) or "OK")

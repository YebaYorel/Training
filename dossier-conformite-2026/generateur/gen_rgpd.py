"""Complément RGPD et IA Act propre aux parcours certifiants (à reporter dans YEBA-DOC-16)."""
from lib import ORGANISME, Doc

O = ORGANISME
DOSSIER = "04_RGPD_IA_Act"


def complement_registre():
    d = Doc("Complément au registre des traitements", "Traitements propres aux parcours certifiants — à reporter dans YEBA-DOC-16", code="RGPD-01", paysage=True)
    d.p(f"Responsable de traitement : {O['nom']}, {O['forme']}, représenté par {O['dirigeant']}. Contact : {O['contact_rgpd']}. "
        "Pas de délégué à la protection des données (non obligatoire, politique YEBA-DOC-02). "
        "Les traitements déjà décrits dans YEBA-DOC-02 et YEBA-DOC-16 (gestion des stagiaires, facturation, prospection) ne sont pas répétés ici.")
    d.tableau(["Traitement", "Personnes", "Données", "Base légale", "Destinataires", "Conservation"], [
        ["Déclarations sur les plateformes des financeurs (EDOF, KAIROS, Région, OPCO)", "Stagiaires", "Identité, identifiant financeur, présence, résultats",
         "Obligation légale ; contrat (art. 6.1.c et 6.1.b)", "Caisse des Dépôts, France Travail, Région, OPCO", "Durée exigée par chaque financeur"],
        ["Rémunération des stagiaires (dossier Région ou ASP, si concerné)", "Stagiaires", "Identité, numéro de sécurité sociale, RIB",
         "Obligation légale ; mission du financeur (art. 6.1.c et 6.1.e)", "Financeur, ASP", "Durée exigée par le financeur"],
        ["Inscription à la session de validation du titre", "Candidats", "Identité, dossier professionnel, preuve de période en entreprise, résultats",
         "Obligation légale (art. 6.1.c)", "DEETS, responsable de session, jury, centre agréé partenaire", "Durée de la formation + 5 ans"],
        ["Périodes en entreprise", "Stagiaires, tuteurs", "Identité, coordonnées du tuteur, convention, suivi",
         "Contrat (art. 6.1.b)", "Entreprise d'accueil, financeur", "Durée de la formation + 5 ans"],
        ["Liaison avec les prescripteurs", "Stagiaires", "Assiduité, progression, freins signalés avec accord",
         "Intérêt légitime et accord du stagiaire (art. 6.1.f)", "Mission Locale, France Travail, Cap emploi", "Durée de la formation"],
        ["Aménagements de parcours et d'examen", "Stagiaires concernés", "Aménagement retenu, sans donnée médicale",
         "Consentement explicite (art. 9.2.a)", "Référent handicap, responsable de session", "Fin du parcours"],
        ["Suivi de l'insertion à 6 mois", "Anciens stagiaires", "Situation professionnelle",
         "Obligation légale (indicateurs publics) ; intérêt légitime", "Interne ; résultats agrégés publiés", "2 ans (réponses individuelles)"],
    ], [4.6, 2.8, 4.6, 4.2, 5, 4.5])
    d.h2("Points de vigilance relevés dans la base Airtable (souveraineté des données)")
    d.puces([
        "Airtable (Airtable Inc.) et la messagerie Gmail (Google LLC) relèvent du droit des États-Unis : documenter le mécanisme de transfert hors UE ou migrer (cible déjà décidée : Baserow auto-hébergé chez OVHcloud, envoi des courriels par Brevo).",
        "Ne pas stocker dans Airtable le numéro de sécurité sociale ni le RIB des stagiaires : les conserver dans un espace chiffré hébergé dans l'Union européenne.",
        "Champs « À SUPPRIMER » de la table APPRENANTS (données de santé, CPF, photo) : suppression définitive à faire.",
    ])
    d.h2("IA Act appliqué aux parcours certifiants")
    d.tableau(["Usage", "Qualification", "Règle"], [
        ["Préparer supports, cas pratiques, plannings de formation", "Risque minimal", "Autorisé, relecture humaine (charte YEBA-DOC-11)"],
        ["Sélection des candidats, notation, orientation, surveillance d'examen", "Haut risque (annexe III, point 3)", "Interdit chez YEBA FORMATIONS"],
        ["Reconnaissance des émotions des stagiaires", "Pratique interdite (art. 5)", "Interdit par la loi"],
        ["Module T1 « IA » des parcours", "Maîtrise de l'IA (art. 4)", "Contenu conforme à la charte YEBA-DOC-11"],
        ["Productions d'examen rédigées avec une IA", "Transparence", "Usage déclaré par le stagiaire ; travail personnel exigé"],
    ], [8.5, 7, 10.2])
    return d.save(f"{DOSSIER}/RGPD-01_Complement_registre_parcours_certifiants.docx")


def tout():
    return [complement_registre()]


if __name__ == "__main__":
    for f in tout():
        print(f.name)

"""Gouvernance des données : registre RGPD, conservation, charte IA, cartographie IA Act."""
from lib import Doc, ORGANISME

O = ORGANISME
DOSSIER = "04_RGPD_IA_Act"


def registre():
    d = Doc("Registre des activités de traitement", "Article 30 du RGPD — responsable de traitement : " + O["nom"], code="RGPD-01", paysage=True)
    d.p(f"Responsable de traitement : {O['nom']}, SIRET {O['siret']}, représenté par {O['dirigeant']}. "
        f"Contact : {O['contact_rgpd']}. Délégué à la protection des données : non obligatoire à ce stade (pas de traitement à grande échelle de données sensibles) — [À VÉRIFIER si la taille de l'activité évolue].")
    lignes = [
        ["Gestion des candidatures et admissions", "Candidats", "Identité, contact, situation, CV, résultats du positionnement", "Mesures précontractuelles (6.1.b)", "Équipe pédagogique, prescripteur (si accord)", "2 ans après le dernier contact si non retenu"],
        ["Gestion administrative et pédagogique des stagiaires", "Stagiaires", "Identité, contact, présence, évaluations, dossier professionnel", "Contrat (6.1.b) ; obligation légale (6.1.c)", "Formateurs, financeurs, DEETS, jury, plateformes publiques", "Durée de la formation + 5 ans [À VÉRIFIER : durée exigée par chaque financeur]"],
        ["Déclarations aux financeurs (EDOF, KAIROS, Région, OPCO)", "Stagiaires", "Identité, identifiants financeur, présence, résultats", "Obligation légale / contrat (6.1.c, 6.1.b)", "Caisse des Dépôts, France Travail, Région, OPCO", "Durée exigée par le financeur"],
        ["Accompagnement du handicap", "Stagiaires concernés", "Besoins d'aménagement (donnée de santé)", "Consentement explicite (9.2.a)", "Référent handicap seul ; Agefiph / Cap emploi avec accord", "Fin du parcours"],
        ["Rémunération des stagiaires (si dossier Région / ASP)", "Stagiaires", "Identité, NIR, RIB", "Obligation légale / mission du financeur (6.1.c / 6.1.e)", "Financeur, ASP", "Durée exigée par le financeur"],
        ["Suivi de l'insertion et indicateurs", "Anciens stagiaires", "Situation professionnelle à 6 mois", "Obligation légale (indicateurs publics) / intérêt légitime (6.1.f)", "Interne ; résultats agrégés publiés", "2 ans (réponses individuelles)"],
        ["Prospection commerciale B2B et B2C", "Prospects, entreprises", "Identité, fonction, contact", "Intérêt légitime (B2B) / consentement (B2C e-mail)", "Interne", "3 ans après le dernier contact"],
        ["Gestion des formateurs et sous-traitants", "Formateurs", "Identité, CV, diplômes, contrat, facturation", "Contrat (6.1.b)", "Interne, Qualiopi, DEETS", "Durée de la relation + 5 ans ; pièces comptables 10 ans"],
        ["Comptabilité et facturation", "Clients, financeurs", "Identité, facturation", "Obligation légale (6.1.c)", "Expert-comptable", "10 ans (art. L.123-22 code de commerce)"],
        ["Enquêtes de satisfaction", "Stagiaires, entreprises", "Réponses", "Intérêt légitime / obligation Qualiopi", "Interne", "2 ans"],
        ["Image et témoignages", "Stagiaires volontaires", "Photo, vidéo, témoignage", "Consentement (6.1.a)", "Public (site, réseaux)", "2 ans ou jusqu'au retrait"],
        ["Usage d'outils d'IA (rédaction, préparation de supports)", "Aucune donnée personnelle saisie", "Contenus pédagogiques non personnels", "—", "Fournisseur de l'outil (hébergement UE)", "—"],
    ]
    d.tableau(["Traitement", "Personnes", "Données", "Base légale", "Destinataires", "Conservation"], lignes, [4.2, 3, 4.5, 4, 5, 5])
    d.h2("Sous-traitants (art. 28) — à tenir à jour")
    d.tableau(["Prestataire", "Service", "Localisation des données", "Contrat art. 28 signé"], [
        ["Baserow B.V.", "Base de données (prospects, sessions)", "Union européenne (Pays-Bas)", "☐"],
        ["[À COMPLÉTER : messagerie]", "E-mail", "[À VÉRIFIER : UE]", "☐"],
        ["[À COMPLÉTER : stockage de fichiers]", "Stockage des dossiers stagiaires", "[À VÉRIFIER : UE]", "☐"],
        ["[À COMPLÉTER : signature / émargement électronique]", "Émargement, signatures", "[À VÉRIFIER : UE]", "☐"],
        ["[À COMPLÉTER : outil d'IA validé]", "Aide à la rédaction", "[À VÉRIFIER : UE, pas de réutilisation des données pour l'entraînement]", "☐"],
    ], [6, 6, 8, 5.7])
    d.h2("Mesures de sécurité (art. 32)")
    d.puces(["Comptes nominatifs et authentification à deux facteurs", "Dossiers stagiaires dans un espace chiffré à accès restreint ; dossier handicap séparé",
             "Sauvegardes chiffrées hebdomadaires", "Envoi aux financeurs par plateformes officielles ou liens sécurisés, jamais de pièce d'identité en clair par e-mail",
             "Mises à jour et antivirus ; sensibilisation annuelle (SecNumacadémie de l'ANSSI)", "Procédure de violation de données (notification CNIL sous 72 h)"])
    return d.save(f"{DOSSIER}/RGPD-01_Registre_des_traitements.docx")


def mentions_et_violation():
    d = Doc("Information des personnes et violations de données", "Articles 13, 14, 33 et 34 du RGPD", code="RGPD-02")
    d.h2("1. Mention d'information complète — stagiaires et candidats")
    d.p(f"**Qui ?** {O['nom']}, {O['adresse']}, responsable de traitement. Contact : {O['contact_rgpd']}.")
    d.p("**Pourquoi ?** Étudier votre candidature, organiser votre formation et votre examen, suivre votre présence et vos progrès, "
        "répondre aux obligations envers les financeurs, le ministère du Travail et l'auditeur Qualiopi, mesurer l'insertion à 6 mois.")
    d.p("**Sur quelle base ?** Mesures précontractuelles et contrat ; obligations légales ; votre consentement pour l'image et les données de santé.")
    d.p("**Qui reçoit vos données ?** L'équipe pédagogique ; selon votre situation : Caisse des Dépôts (CPF), France Travail, Mission Locale, Région Réunion, OPCO, "
        "DEETS, jury et responsable de session du titre ; l'entreprise d'accueil (identité et convention uniquement).")
    d.p("**Combien de temps ?** Voir la politique de conservation. **Hors UE ?** Non : nos outils sont choisis pour héberger les données dans l'Union européenne.")
    d.p("**Vos droits :** accès, rectification, effacement, limitation, opposition, portabilité, retrait du consentement, directives post-mortem. Réclamation possible auprès de la CNIL.")
    d.p("**Intelligence artificielle :** aucune décision sur votre admission, votre évaluation ou votre parcours n'est prise par une IA. "
        "Les formateurs peuvent utiliser des outils d'IA pour préparer des supports, sans y saisir vos données.")
    d.h2("2. Mention courte — formulaire de prospect (site ou salon)")
    d.p(f"Vos coordonnées servent uniquement à vous recontacter au sujet de nos formations. Conservation : 3 ans après notre dernier échange. Droits : {O['contact_rgpd']}.")
    d.h2("3. Politique de conservation")
    d.tableau(["Document / donnée", "Durée", "Justification"], [
        ["Candidature non retenue", "2 ans après le dernier contact", "Recommandation CNIL (recrutement / candidature)"],
        ["Dossier stagiaire (inscription, émargements, évaluations, attestations)", "Fin de formation + 5 ans [À VÉRIFIER : durée plus longue si financement FSE+ ou exigence du financeur]", "Preuves pour contrôles DEETS, financeurs, Qualiopi"],
        ["Pièces comptables et factures", "10 ans", "Art. L.123-22 du code de commerce"],
        ["Dossier handicap", "Fin du parcours", "Minimisation (art. 5 RGPD)"],
        ["Prospects", "3 ans après le dernier contact", "Référentiel CNIL gestion commerciale"],
        ["Réponses individuelles aux enquêtes", "2 ans", "Choix de l'organisme"],
        ["Vidéos pédagogiques de mises en situation", "Fin de la session", "Consentement, usage interne"],
    ], [6, 5, 6])
    d.h2("4. Procédure en cas de violation de données")
    d.numeros(["Constater et contenir (changer les mots de passe, isoler l'appareil, révoquer le lien partagé)",
               "Évaluer le risque pour les personnes (type de données, volume, conséquences)",
               "Notifier la CNIL dans les 72 heures si risque (téléservice CNIL)",
               "Informer les personnes sans délai si risque élevé",
               "Consigner l'incident dans le registre des violations, même sans notification", "Corriger la cause et sensibiliser"])
    d.tableau(["Date", "Nature", "Données / personnes", "Risque", "Notification CNIL", "Mesures"], [[""] * 6 for _ in range(4)], [2, 3, 3.5, 1.8, 3.2, 3.5])
    d.h2("5. Clause type pour les formateurs indépendants (sous-traitance, art. 28)")
    d.p("Le formateur traite les données des stagiaires uniquement pour les besoins de la mission, sur instruction documentée de l'organisme ; "
        "il garantit leur confidentialité, n'utilise pas d'outil d'IA non validé avec ces données, ne les conserve pas après la mission, "
        "aide l'organisme à répondre aux demandes de droits, signale toute violation sous 24 h et permet les audits.")
    return d.save(f"{DOSSIER}/RGPD-02_Information_conservation_violations.docx")


def charte_ia():
    d = Doc("Charte d'usage de l'intelligence artificielle", "Formateurs, salariés et stagiaires — Règlement (UE) 2024/1689 (IA Act)", code="IA-03")
    d.h2("1. Pourquoi cette charte ?")
    d.p("Depuis le 2 février 2025, l'IA Act impose aux organisations qui utilisent l'IA de garantir un niveau suffisant de maîtrise de l'IA "
        "de leur personnel (article 4) et interdit certaines pratiques (article 5). La formation professionnelle est un domaine sensible : "
        "l'annexe III, point 3, classe à haut risque les systèmes d'IA servant à l'admission, à l'évaluation des acquis, à l'orientation "
        "et à la surveillance des examens.")
    d.h2("2. Cartographie des usages chez YEBA FORMATIONS")
    d.tableau(["Usage", "Niveau IA Act", "Règle YEBA"], [
        ["Préparer des supports, des cas pratiques, des quiz", "Risque minimal", "Autorisé — relecture humaine systématique, aucune donnée personnelle"],
        ["Assistant conversationnel pour informer des prospects", "Transparence (art. 50)", "Autorisé si la personne est informée qu'elle échange avec une IA"],
        ["Images, vidéos ou voix générées par IA diffusées", "Transparence (art. 50)", "Mention « contenu généré par IA » obligatoire"],
        ["Aide à la planification des sessions", "Risque minimal", "Autorisé — décision finale humaine"],
        ["Sélection ou classement des candidats à l'entrée", "Haut risque (annexe III, 3a)", "**Interdit chez YEBA**"],
        ["Notation ou correction automatique des évaluations", "Haut risque (annexe III, 3b)", "**Interdit chez YEBA** (correction humaine)"],
        ["Détection de fraude ou surveillance pendant une épreuve", "Haut risque (annexe III, 3d)", "**Interdit chez YEBA**"],
        ["Reconnaissance des émotions des stagiaires", "Pratique interdite (art. 5.1.f)", "**Interdit par la loi**"],
        ["Tri de CV dans le module recrutement (exercice)", "Haut risque (annexe III, 4)", "Uniquement sur CV fictifs, à titre de démonstration critique"],
    ], [6, 4, 7])
    d.h2("3. Règles d'or")
    d.numeros(["Je n'entre jamais de donnée personnelle (nom, e-mail, résultats, santé) dans un outil d'IA non validé par la direction.",
               "J'utilise en priorité des outils hébergés dans l'Union européenne qui ne réutilisent pas mes données pour leur entraînement.",
               "Je vérifie chaque information produite par l'IA (sources, chiffres, textes de loi).",
               "Je garde la décision : l'IA propose, l'humain dispose.",
               "Je signale clairement les contenus générés par IA diffusés à l'extérieur.",
               "Stagiaires : j'indique dans mes dossiers d'examen les parties réalisées avec l'aide d'une IA ; le dossier reste mon travail personnel.",
               "Je signale à la direction tout incident (fuite, résultat discriminatoire, erreur grave)."])
    d.h2("4. Maîtrise de l'IA (article 4) — plan de formation interne")
    d.tableau(["Public", "Contenu", "Durée", "Preuve"], [
        ["Direction et formateurs", "Fonctionnement, limites, biais, RGPD, IA Act, outils validés", "7 h / an", "Attestation, émargement"],
        ["Stagiaires des titres MEM et RPMS", "Module T1 du parcours", "42 h", "Émargements, évaluation"],
        ["Personnel administratif", "Règles d'or et cas pratiques", "3 h", "Attestation"],
    ], [4.5, 7, 2, 3.5])
    d.h2("5. Calendrier IA Act utile")
    d.puces(["2 février 2025 : pratiques interdites et obligation de maîtrise de l'IA — **en vigueur**.",
             "2 août 2025 : obligations des fournisseurs de modèles d'IA à usage général.",
             "2 août 2026 : obligations de transparence (art. 50) et, en principe, systèmes à haut risque de l'annexe III — [À VÉRIFIER : report envisagé par la proposition « omnibus numérique » de la Commission (novembre 2025) ; vérifier le texte adopté avant toute communication]."])
    d.signatures(["Le signataire (formateur / salarié / stagiaire)", f"Pour {O['nom']}"])
    return d.save(f"{DOSSIER}/IA-03_Charte_IA_et_cartographie_IA_Act.docx")


def tout():
    return [registre(), mentions_et_violation(), charte_ia()]


if __name__ == "__main__":
    for f in tout():
        print(f)

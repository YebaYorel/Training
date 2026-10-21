"""Note d'expertise : choix des RNCP, financement, trésorerie, stratégie DEETS."""
from lib import Doc, ORGANISME
from titres import MEM, RPMS, heures_centre

O = ORGANISME


def note():
    d = Doc("Note d'expertise — Formation continue certifiante niveau 5",
            "Choix des RNCP, financement, trésorerie, réponse DEETS, conformité RGPD et IA Act — octobre 2026", code="NOTE-00")
    d.h1("1. Synthèse en 6 décisions")
    d.numeros([
        "**Rester organisme de formation continue** : les deux titres se préparent en formation continue et en contrat de professionnalisation sans statut de CFA (fiches RNCP41853 et RNCP38575 : voies d'accès « formation continue » et « contrat de professionnalisation » ouvertes).",
        "**Répondre à la DEETS avant le délai de 12 jours** par la version A (suspension de la demande d'extension) ; garder le dossier des 18 pièces prêt.",
        "**Ouvrir d'abord le TP Manager d'établissement marchand (MEM)** pour les publics France Travail et Missions Locales ; **puis le TP Responsable de petite ou moyenne structure (RPMS)** pour les salariés, créateurs et repreneurs (CPF, OPCO).",
        "**Ajouter le module IA (42 h)** dans chaque parcours : c'est votre avantage concurrentiel, et il répond à l'obligation de maîtrise de l'IA (IA Act, art. 4).",
        "**Obtenir l'agrément DEETS pour organiser les sessions d'examen**, ou signer un partenariat avec un centre agréé en attendant (prévoir au moins 7 mois avant la première session).",
        "**Sécuriser la trésorerie** en combinant plusieurs financeurs et des formations courtes en intra-entreprise (IA, RGPD) qui financent le démarrage des parcours longs.",
    ])
    d.h1("2. Raisonnement étape par étape")
    d.h2("Étape 1 — Contraintes")
    d.tableau(["Contrainte", "Conséquence"], [
        ["Formation continue, pas d'apprentissage", "Pas de NPEC OPCO ; financeurs : CPF, France Travail, Région, OPCO (plan, Pro-A, contrat de professionnalisation), Transitions Pro, particuliers"],
        ["Niveau 5 avec responsabilité et IA", "Titres de management de niveau 5 ; l'IA n'apparaît dans aucun des deux référentiels → module complémentaire de l'organisme"],
        ["Faible taux d'abandon", "Sélection à l'entrée, rémunération du stagiaire pendant la formation, alternance courte centre / entreprise, suivi social"],
        ["Missions Locales et France Travail", "Public demandeur d'emploi, souvent jeune et peu expérimenté → titre accessible sans expérience de direction"],
        ["Trésorerie", "Éviter la dépendance à un seul financeur payé à terme échu ; facturer par étapes"],
        ["La Réunion", "Marchés publics de la Région, Carif-Oref Réunion, DEETS 974, réalités locales (cyclones, mobilité, insularité)"],
    ], [5.5, 11.5])
    d.h2("Étape 2 — Comparaison des deux titres que vous avez transmis")
    d.tableau(["Critère", "MEM — RNCP41853", "RPMS — RNCP38575"], [
        ["Version", "Nouvelle version : parcours à partir du 03/03/2026, jusqu'au 02/03/2031", "Parcours depuis le 08/02/2024, jusqu'au 08/02/2029"],
        ["Public type", "Demandeurs d'emploi, jeunes avec expérience commerciale, employés de commerce", "Salariés expérimentés, créateurs et repreneurs, responsables associatifs"],
        ["Adéquation Missions Locales", "Forte (métier accessible, secteur recruteur)", "Faible à moyenne (demande de la maturité professionnelle)"],
        ["Épreuve", "7 h 55 : mise en situation 4 h sur poste informatique + entretiens + 2 productions", "1 h 35 : présentation d'un projet + entretiens"],
        ["Exigence matérielle pour être centre d'examen", "Élevée (postes, maquettes, surveillant)", "Faible"],
        ["Période en entreprise minimale", "280 h (arrêté du 4 décembre 2025, art. 6)", "210 h selon plusieurs organismes — [À VÉRIFIER dans l'arrêté]"],
        ["Insertion nationale (6 mois, global)", "76 % (2024)", "69 % (2022)"],
        ["Lien avec votre expertise", "Vente, management, soft skills", "Management, gouvernance, IA, RGPD : très fort"],
        ["Volume horaire proposé", f"{heures_centre(MEM)} h centre + {MEM['pae']} h entreprise", f"{heures_centre(RPMS)} h centre + {RPMS['pae']} h entreprise"],
    ], [4, 6.5, 6.5])
    d.h2("Étape 3 — Décision")
    d.p("Les deux titres sont complémentaires et non concurrents. Le MEM répond à votre objectif « Missions Locales / France Travail / faible abandon » ; "
        "le RPMS valorise votre positionnement unique (direction de TPE-PME + IA + gouvernance des données), sur un marché de salariés et de dirigeants "
        "plus solvable (CPF, OPCO). Ordre conseillé : MEM en premier (volume), RPMS en second (marge et image).")
    d.p("Autres titres de niveau 5 qui pourraient compléter l'offre plus tard : je ne les recommande pas sans vérification de leur fiche RNCP active et de la demande locale "
        "(France Travail BMO, Carif-Oref Réunion). [À VÉRIFIER ensemble avant toute décision.] Pour l'IA, envisagez d'associer au parcours une certification du "
        "répertoire spécifique (RS) dédiée aux usages de l'IA, finançable par le CPF, à sélectionner sur francecompetences.fr.")
    d.h1("3. Financement et trésorerie")
    d.tableau(["Financeur", "Public", "Points clés de trésorerie"], [
        ["CPF (Caisse des Dépôts)", "Salariés, demandeurs d'emploi", "Paiement après déclaration de service fait ; acomptes ou facturation intermédiaire [À VÉRIFIER : CGU EDOF en vigueur]. Le reste à charge forfaitaire ne s'applique pas aux demandeurs d'emploi."],
        ["France Travail (AIF, AFC, POEI)", "Demandeurs d'emploi", "Rémunération du stagiaire maintenue (ARE ou rémunération de formation) → levier anti-abandon majeur. Modalités de paiement de l'organisme [À VÉRIFIER auprès de la direction régionale]."],
        ["Région Réunion (marché public)", "Demandeurs d'emploi", "Le code de la commande publique prévoit une avance et des acomptes (R.2191-3 et suivants) — taux et rythme fixés par le marché [À VÉRIFIER]."],
        ["OPCO (plan, Pro-A, contrat de professionnalisation)", "Salariés, nouveaux embauchés", "Contrat de professionnalisation : salarié rémunéré par l'employeur (faible abandon), forfait horaire de branche, sans statut de CFA."],
        ["Particuliers", "Tous", "Acompte de 30 % maximum après le délai de rétractation de 10 jours (art. L.6353-6), solde échelonné."],
        ["Intra-entreprise courte (IA, RGPD, management)", "TPE-PME", "Facturation rapide, marge élevée : finance le démarrage des parcours longs."],
    ], [4.2, 3.8, 9])
    d.p("Règle d'or : un échéancier contractuel par étape (entrée / mi-parcours / fin) pour chaque convention, et un fonds de roulement couvrant 3 mois de charges avant d'ouvrir la première session longue.")
    d.h1("4. Réponse au courriel de la DEETS")
    d.p("Ce courriel liste les conditions de l'article L.6351-5 du code du travail pour étendre une déclaration d'activité à l'apprentissage. "
        "Ces 18 pièces reprennent les missions des CFA (art. L.6231-2). Elles ne sont pas exigées pour la formation continue. "
        "Deux options :")
    d.tableau(["Option", "Avantages", "Risques"], [
        ["A — Suspendre la demande (recommandée)", "Cohérent avec votre stratégie ; évite un dossier incomplet ; aucune nouvelle obligation", "Aucun : vous pourrez redemander plus tard"],
        ["B — Envoyer le dossier complet", "Ouvre l'apprentissage", "Exige l'extension Qualiopi, des moyens réels (salarié dédié aux relations entreprises, locaux), le respect des missions CFA ; contrôle renforcé"],
    ], [5, 6, 6])
    d.h1("5. Ce que contient le dossier")
    d.tableau(["Dossier", "Contenu"], [
        ["01_Reponse_DEETS", "Courriels versions A et B ; dossier des 18 pièces"],
        ["02_MEM et 02_RPMS", "Programme (Qualiopi ind. 1-2), déroulé pédagogique + grilles critériées, décomposition des heures semaine par semaine + rétroplanning"],
        ["03_Parcours_stagiaire", "15 documents, de l'inscription au suivi à 6 mois"],
        ["04_RGPD_IA_Act", "Registre des traitements, information, conservation, violations, charte IA et cartographie IA Act"],
        ["05_Pilotage_annuel", "Pièces par financeur et contrôleur, calendrier annuel, tableau de bord Excel (heures, indicateurs, absences)"],
    ], [5, 12])
    d.h1("6. Autocritique et corrections apportées")
    d.tableau(["Angle", "Faille identifiée", "Correction"], [
        ["Juridique", "Les durées de conservation des financeurs (notamment FSE+) peuvent dépasser 5 ans", "Signalé [À VÉRIFIER] dans le registre ; aligner sur chaque convention"],
        ["Juridique", "Durée de la période en entreprise du RPMS non confirmée par un texte officiel consulté", "Marquée [À VÉRIFIER] ; ne pas diffuser le programme RPMS avant vérification"],
        ["Juridique", "Calendrier IA Act des systèmes à haut risque possiblement reporté", "Signalé dans la charte ; la politique YEBA (aucune IA décisionnelle) reste valable quel que soit le calendrier"],
        ["Faisabilité", "Le MEM impose un plateau informatique pour l'examen", "Partenariat avec un centre agréé en attendant l'agrément ; investissement progressif"],
        ["Faisabilité", "Vous êtes souvent en retard sur votre programme", "Rétroplanning à cocher, semaines incomplètes servant de rattrapage, préparation 2 semaines avant chaque module"],
        ["Économique", "Paiement à terme échu des financeurs publics", "Diversification des financeurs + intra courtes + échéanciers"],
        ["Social", "Public Missions Locales : freins périphériques", "Plan anti-décrochage, rémunération vérifiée avant l'entrée, alternance courte"],
        ["Sécurité", "Dossiers stagiaires sensibles (identité, NIR, handicap)", "Outils hébergés dans l'UE, chiffrement, accès restreint, dossier handicap séparé"],
        ["Écologique", "Impression des dossiers", "Dématérialisation (sauf pièces d'examen imprimées exigées), supports numériques accessibles"],
        ["Politique", "Dépendance aux appels d'offres régionaux", "Présence parallèle sur le CPF et l'intra-entreprise"],
        ["Technologique", "Données de l'entreprise non récupérées automatiquement", "Accès réseau à entreprise.api.gouv.fr indisponible ici, et cette API exige une habilitation : champs [À COMPLÉTER] à remplir à partir de votre avis de situation INSEE / extrait RNE"],
    ], [3, 7, 7])
    d.h1("7. Questions à trancher")
    d.numeros([
        "Forme juridique de YEBA FORMATIONS (société avec statuts ou entreprise individuelle) ?",
        "Date de réception du courriel de la DEETS (pour calculer la date limite de 12 jours) ?",
        "Périmètre exact du certificat Qualiopi 25FOR02027.1 (catégories couvertes) et date de l'audit de surveillance ?",
        "Rythme retenu par titre : option A (35 h), B (21 h) ou C (par blocs) ?",
        "Horaires, pauses, adresse des locaux, capacité, équipement informatique ?",
        "Tarifs envisagés par titre et par CCP ?",
        "Le logo transmis est-il bien la version « sans l'œil » ? (c'est ce fichier qui est utilisé dans tous les documents)",
        "Souhaitez-vous viser l'agrément de centre d'examen dès 2027, ou d'abord un partenariat ?",
    ])
    d.h1("8. Sources")
    d.puces([
        "Fiche RNCP41853 — TP Manager d'établissement marchand, francecompetences.fr (fiche PDF transmise, consultée le 21/10/2026).",
        "Fiche RNCP38575 — TP Responsable de petite ou moyenne structure, francecompetences.fr (fiche PDF transmise, consultée le 21/10/2026).",
        "Durée de la période en entreprise RPMS (210 h) : extraits des sites icademie.com et etudis.net — source secondaire, à confirmer.",
        "Agrément des sessions de titres professionnels : formulaires DREETS (Corse, Normandie, Auvergne-Rhône-Alpes) et démarche « DEETS 974 — demande d'agrément pour organiser des sessions » sur demarche.numerique.gouv.fr.",
        "Code du travail : articles L.6351-5, L.6353-1 à L.6353-7, L.6354-1, R.6352-1 à R.6352-15, L.6222-12-1, L.6222-18-2, L.8222-1.",
        "Règlement (UE) 2016/679 (RGPD) ; règlement (UE) 2024/1689 (IA Act), articles 4, 5, 50 et annexe III.",
    ])
    d.rgpd(["RGPD : toutes les données de stagiaires, candidats et prospects de ce dossier relèvent du RGPD (registre RGPD-01).",
            "IA Act : la formation professionnelle relève de l'annexe III (haut risque) pour l'admission, l'évaluation et la surveillance des examens. La politique de YEBA FORMATIONS exclut ces usages."])
    return d.save("00_NOTE_EXPERT_Choix_RNCP_et_strategie.docx")


if __name__ == "__main__":
    print(note())

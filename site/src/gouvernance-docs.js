// Bibliothèque RGPD & IA Act : modèles et fiches pratiques remis aux entreprises clientes.
// Ce sont des MODÈLES à adapter : ils ne constituent pas une consultation juridique.
// Mise en forme lue par <Texte> (qualiopi.jsx) : TITRES EN CAPITALES, puces « • ».
// Références vérifiées : RGPD (UE) 2016/679, IA Act (UE) 2024/1689, recommandations CNIL.

const VERSION = '1.0'
const DATE = '2026-10-07'

export const DOCS_GOUVERNANCE = [
  {
    ref: 'YEBA-GOUV-01', theme: 'RGPD', titre: 'Registre des activités de traitement — modèle commenté', item: 'Registre des traitements',
    resume: 'La fiche à remplir pour chaque traitement (article 30 du RGPD), avec un exemple complet pour une TPE.',
    texte: `À QUOI SERT LE REGISTRE
Le registre recense tous les traitements de données personnelles de l'entreprise. Il est obligatoire pour toute structure dont les traitements ne sont pas occasionnels (paie, clients, prospects) : en pratique, pour presque toutes les TPE-PME (RGPD, art. 30.5). Il est le premier document demandé lors d'un contrôle de la CNIL.

UNE FICHE PAR TRAITEMENT
• Nom du traitement : par exemple « Gestion des clients et facturation ».
• Responsable du traitement : l'entreprise, son adresse, le nom de la personne qui pilote le sujet.
• Finalité : pourquoi les données sont collectées, en une phrase.
• Base légale : contrat, obligation légale, intérêt légitime, consentement, mission d'intérêt public ou intérêts vitaux (art. 6).
• Personnes concernées : clients, salariés, candidats, prospects, stagiaires.
• Catégories de données : identité, coordonnées, données bancaires, données de connexion… Signaler toute donnée sensible (art. 9).
• Destinataires : services internes, sous-traitants (comptable, hébergeur, outil d'IA), administrations.
• Transferts hors Union européenne : oui ou non ; si oui, vers quel pays et avec quelle garantie.
• Durée de conservation : voir la fiche YEBA-GOUV-02.
• Mesures de sécurité : accès par mot de passe individuel, sauvegarde, chiffrement, journalisation.

EXEMPLE REMPLI — PROSPECTION COMMERCIALE
• Finalité : envoyer des offres aux entreprises de La Réunion susceptibles d'être intéressées.
• Base légale : intérêt légitime (B2B), avec information et droit d'opposition à chaque envoi.
• Données : nom, fonction, adresse électronique professionnelle, entreprise, origine du contact.
• Destinataires : service commercial ; outil d'emailing (sous-traitant, contrat art. 28 vérifié).
• Durée : 3 ans à compter du dernier contact émanant du prospect.
• Sécurité : accès limité au service commercial, export interdit, lien de désinscription testé.

LES ERREURS FRÉQUENTES
• Un seul traitement « fichier clients » qui mélange facturation, prospection et service après-vente.
• Oublier les traitements des salariés (paie, badges, messagerie) et ceux confiés à un outil d'IA.
• Écrire une durée « illimitée » ou « tant que nécessaire » sans chiffre.
• Ne jamais mettre le registre à jour : il se relit au moins une fois par an et à chaque nouvel outil.

SOURCES
• RGPD, articles 5, 6, 9 et 30.
• CNIL, « Le registre des activités de traitement » et modèle de registre simplifié (cnil.fr).`,
  },
  {
    ref: 'YEBA-GOUV-02', theme: 'RGPD', titre: 'Durées de conservation — tableau de référence pour TPE-PME', item: 'Durées de conservation',
    resume: 'Combien de temps garder les données courantes, et ce qu’on en fait ensuite (base active, archives, suppression).',
    texte: `LE PRINCIPE
Une donnée personnelle ne se garde que le temps nécessaire à la finalité pour laquelle elle a été collectée (RGPD, art. 5.1.e). Au-delà, elle est supprimée, anonymisée ou placée en archive intermédiaire à accès restreint quand une loi impose de la conserver.

TROIS TEMPS
• Base active : la donnée sert au quotidien (client en cours, salarié présent).
• Archive intermédiaire : la donnée ne sert plus, mais une obligation légale ou un délai de prescription impose de la garder ; accès limité à une ou deux personnes.
• Suppression ou anonymisation définitive.

REPÈRES COURANTS (À VÉRIFIER SELON VOTRE SECTEUR)
• Prospects jamais devenus clients : 3 ans à compter du dernier contact émanant du prospect (recommandation CNIL).
• Clients : durée de la relation commerciale, puis 3 ans pour la prospection ; pièces contractuelles conservées pendant le délai de prescription de 5 ans (code civil, art. 2224).
• Pièces comptables et factures : 10 ans (code de commerce, art. L.123-22).
• Candidats non retenus : 2 ans au plus après le dernier contact, avec information du candidat (recommandation CNIL).
• Bulletins de paie : double conservé par l'employeur 5 ans (code du travail, art. L.3243-4).
• Images de vidéoprotection : quelques jours, un mois au maximum hors procédure (recommandation CNIL).
• Journaux de connexion : 6 mois à 1 an (recommandation CNIL sur la journalisation).
• Choix de l'internaute sur les cookies : redemander le consentement après 6 mois environ (recommandation CNIL).

CE QU'IL FAUT ÉCRIRE
• Une durée par traitement dans le registre (YEBA-GOUV-01).
• La règle de purge : qui supprime, quand, comment on le vérifie.
• La même durée dans la politique de confidentialité publiée.

ATTENTION AUX OUTILS D'IA
Les historiques de conversation conservés par un assistant d'IA sont aussi des données : vérifier la durée de conservation de l'éditeur et la désactiver ou la réduire quand c'est possible.

SOURCES
• RGPD, article 5.1.e ; CNIL, « Les durées de conservation des données » et référentiels sectoriels (cnil.fr).
• Code de commerce L.123-22 ; code civil 2224 ; code du travail L.3243-4.`,
  },
  {
    ref: 'YEBA-GOUV-03', theme: 'RGPD', titre: 'Ce que l’on saisit dans une IA — la règle des trois bacs', item: 'Tri des données saisies dans l’IA',
    resume: 'Je saisis / j’anonymise d’abord / je ne saisis jamais : la fiche réflexe affichable au poste.',
    texte: `LA RÈGLE
Avant de coller un texte dans un outil d'IA, chaque information passe dans l'un des trois bacs. En cas de doute, on choisit le bac le plus prudent.

BAC 1 — JE SAISIS
• Informations publiques : site internet de l'entreprise, plaquette, offre publiée.
• Textes sans personne identifiable : procédure interne générique, modèle de courrier vierge.
• Données fictives créées pour l'exercice.

BAC 2 — J'ANONYMISE D'ABORD
• Un courriel de client : remplacer le nom, l'adresse, le téléphone, la référence de dossier par [CLIENT], [ADRESSE]…
• Un compte rendu de réunion : retirer les noms, garder les rôles (« le responsable commercial »).
• Un tableau de ventes : supprimer les colonnes nominatives, garder les montants agrégés.
• Attention : un détail rare (fonction unique, petite commune, date précise) peut suffire à reconnaître quelqu'un.

BAC 3 — JE NE SAISIS JAMAIS
• Données de santé, handicap, arrêts maladie, origine, religion, opinions, vie sexuelle, appartenance syndicale (RGPD, art. 9).
• Numéro de sécurité sociale, pièce d'identité, coordonnées bancaires, mots de passe.
• Évaluations ou sanctions de salariés, données de candidats.
• Secrets d'affaires : prix d'achat, marges, contrats en négociation, code source, stratégie.
• Toute donnée de client couverte par un secret professionnel (expert-comptable, avocat, santé).

LES TROIS GESTES D'ANONYMISATION
• Remplacer les noms et identifiants par des étiquettes entre crochets.
• Supprimer les détails rares qui permettent de deviner la personne.
• Relire le texte final comme s'il allait être publié.

LE COMPTE COMPTE AUSSI
Un compte grand public gratuit et un compte professionnel ne traitent pas les saisies de la même façon (réutilisation pour l'entraînement, durée de conservation, localisation). On n'utilise que le compte professionnel validé par l'entreprise, jamais un compte personnel.

SOURCES
• RGPD, articles 5.1.c (minimisation), 6 et 9.
• CNIL, questions-réponses sur l'usage d'un système d'IA générative (cnil.fr).`,
  },
  {
    ref: 'YEBA-GOUV-04', theme: 'RGPD', titre: 'Procédure en cas de violation de données — les 72 heures', item: 'Procédure en cas de violation',
    resume: 'Qui fait quoi dans l’heure, dans la journée, avant 72 heures : la procédure d’une page à afficher.',
    texte: `QU'EST-CE QU'UNE VIOLATION DE DONNÉES
Toute perte de confidentialité, d'intégrité ou de disponibilité de données personnelles : ordinateur volé, courriel envoyé au mauvais destinataire, rançongiciel, fichier publié par erreur, compte piraté (RGPD, art. 4.12).

DANS L'HEURE — CONTENIR
• Prévenir immédiatement le référent désigné : [NOM, TÉLÉPHONE].
• Couper l'accès : changer les mots de passe, déconnecter le poste du réseau sans l'éteindre, rappeler ou supprimer le courriel si possible.
• Ne rien effacer : les traces servent à l'analyse.

DANS LA JOURNÉE — QUALIFIER
• Quelles données, combien de personnes, depuis quand, par quel moyen.
• Quel risque pour les personnes : usurpation d'identité, perte financière, atteinte à la réputation, discrimination.
• Si un sous-traitant est en cause (hébergeur, outil d'IA, prestataire), lui demander son rapport : il doit prévenir l'entreprise dans les meilleurs délais (art. 33.2).

AVANT 72 HEURES — NOTIFIER SI NÉCESSAIRE
• Notifier la CNIL en ligne (notifications.cnil.fr) dans les 72 heures après en avoir pris connaissance, sauf si la violation est improbable de créer un risque pour les personnes (art. 33).
• Si le risque est élevé, informer aussi les personnes concernées, en termes simples, avec les mesures à prendre (art. 34).
• Une notification incomplète peut être complétée ensuite : mieux vaut notifier à temps.

TOUJOURS — DOCUMENTER
• Inscrire chaque violation, même mineure et non notifiée, au registre des violations : faits, effets, mesures prises (art. 33.5).
• Tirer la leçon : quelle mesure aurait évité l'incident, qui la met en place, pour quand.

SI C'EST UNE CYBERATTAQUE
• Déposer plainte et signaler sur cybermalveillance.gouv.fr ; ne pas payer de rançon sans avis.

SOURCES
• RGPD, articles 4.12, 33 et 34 ; CNIL, « Les violations de données personnelles » (cnil.fr).`,
  },
  {
    ref: 'YEBA-GOUV-05', theme: 'IA Act', titre: 'Inventaire des usages d’IA de l’entreprise — modèle', item: 'Inventaire de vos usages d’IA',
    resume: 'La liste de tous les outils d’IA utilisés, déclarés ou non, avec leur usage, leurs données et leur responsable.',
    texte: `POURQUOI UN INVENTAIRE
On ne peut ni qualifier un risque, ni former les équipes, ni prouver les mesures prises (IA Act, art. 4) sans savoir quelles IA sont utilisées. L'inventaire inclut les usages non déclarés : l'assistant gratuit utilisé sur un téléphone personnel compte aussi.

COMMENT LE CONSTITUER EN UNE SEMAINE
• Un questionnaire anonyme de cinq questions aux équipes : quel outil, pour quoi faire, quelles données, quel compte, à quelle fréquence.
• La liste des abonnements et des fonctions d'IA intégrées aux logiciels déjà payés (messagerie, bureautique, CRM, comptabilité).
• Un entretien de 15 minutes par service.

UNE LIGNE PAR USAGE
• Outil et éditeur ; voie américaine, européenne ou locale.
• Usage : ce que l'outil fait, pour qui.
• Données saisies : bac 1, 2 ou 3 (fiche YEBA-GOUV-03).
• Compte : professionnel validé ou personnel.
• Qualification IA Act : voir la fiche YEBA-GOUV-06.
• Responsable : une personne nommée.
• Décision : autorisé, autorisé sous conditions, à remplacer, interdit.

EXEMPLE
• Assistant de rédaction pour les courriels commerciaux — éditeur européen — données anonymisées — compte professionnel — risque minimal, transparence si diffusion d'un contenu généré — responsable : la responsable commerciale — autorisé sous conditions (relecture humaine obligatoire).

QUAND LE METTRE À JOUR
• À chaque nouvel outil ou nouvelle fonction d'IA activée dans un logiciel existant.
• Au moins une fois par an, avec la revue du registre RGPD.

SOURCES
• Règlement (UE) 2024/1689 (IA Act), articles 3 et 4 ; Commission européenne, FAQ « Maîtrise de l'IA ».`,
  },
  {
    ref: 'YEBA-GOUV-06', theme: 'IA Act', titre: 'Qualifier le niveau de risque d’un usage d’IA — grille', item: 'Niveau de risque de chaque usage',
    resume: 'Interdit, haut risque, transparence ou sans obligation particulière : les questions à se poser, dans l’ordre.',
    texte: `QUATRE NIVEAUX
L'IA Act classe les systèmes d'IA selon le risque qu'ils font peser sur les personnes. Les obligations de l'entreprise qui utilise l'outil (le « déployeur ») dépendent de ce niveau.

QUESTION 1 — L'USAGE EST-IL INTERDIT ? (ART. 5)
• Manipulation qui exploite une vulnérabilité, notation sociale, déduction des émotions sur le lieu de travail ou en formation (hors raisons médicales ou de sécurité), catégorisation biométrique sensible, reconnaissance faciale par moissonnage d'images.
• Si oui : arrêt immédiat. Ces interdictions s'appliquent depuis le 2 février 2025.

QUESTION 2 — EST-CE UN USAGE À HAUT RISQUE ? (ANNEXE III)
• Recrutement et tri de candidatures, décisions de promotion ou de licenciement, attribution des tâches et évaluation des salariés.
• Admission, orientation, évaluation des acquis ou surveillance en éducation et formation.
• Accès au crédit, à l'assurance, à des prestations essentielles.
• Si oui : obligations renforcées du déployeur — usage conforme à la notice, supervision humaine par une personne compétente, conservation des journaux, information des salariés et des personnes concernées (art. 26). Vérifier le calendrier d'application en vigueur.

QUESTION 3 — FAUT-IL INFORMER ? (ART. 50)
• Échange avec un robot conversationnel : la personne doit savoir qu'elle parle à une IA.
• Image, son ou vidéo hypertruqués, texte publié pour informer le public : signaler qu'ils sont générés ou modifiés par une IA.
• Voir les modèles de mentions YEBA-GOUV-07.

QUESTION 4 — SINON
• Risque minimal (aide à la rédaction, résumé, traduction interne) : pas d'obligation particulière de l'IA Act, mais le RGPD, le secret des affaires et la maîtrise de l'IA (art. 4) s'appliquent toujours.

LE PIÈGE LE PLUS FRÉQUENT
Un outil anodin peut changer de niveau selon l'usage : le même assistant est à risque minimal pour rédiger une annonce, et à haut risque s'il classe les candidats qui y répondent.

SOURCES
• Règlement (UE) 2024/1689, articles 5, 26, 50 et annexe III (eur-lex.europa.eu).`,
  },
  {
    ref: 'YEBA-GOUV-07', theme: 'IA Act', titre: 'Mentions de transparence — modèles prêts à l’emploi', item: 'Mentions de transparence',
    resume: 'Les phrases à afficher sur un robot conversationnel, un contenu généré, un courriel ou un document.',
    texte: `QUAND UNE MENTION EST NÉCESSAIRE
L'article 50 de l'IA Act impose d'informer les personnes lorsqu'elles échangent avec une IA, et de signaler certains contenus générés ou modifiés par une IA. Même hors obligation stricte, la mention est une bonne pratique qui protège la confiance.

ROBOT CONVERSATIONNEL SUR LE SITE
• « Bonjour, je suis [NOM], l'assistante virtuelle de [ENTREPRISE]. Je suis une intelligence artificielle : pour parler à une personne, demandez à être rappelé. »

IMAGE OU VIDÉO GÉNÉRÉE
• « Image générée par intelligence artificielle. » — placée sur l'image ou juste en dessous, lisible.
• Pour une personne réelle dont l'apparence ou la voix est imitée : mention obligatoire et accord écrit de la personne.

TEXTE PUBLIÉ POUR INFORMER LE PUBLIC
• « Article rédigé avec l'aide d'une intelligence artificielle, relu et validé par [NOM, FONCTION]. »

COURRIEL OU DOCUMENT CLIENT
• Facultatif mais recommandé quand l'IA a produit l'essentiel : « Document préparé avec l'aide d'un outil d'IA et vérifié par nos équipes. »

FORMATION
• « Les outils d'IA utilisés pendant la formation sont présentés comme tels. Aucun système d'IA n'évalue, ne note ou ne sélectionne les stagiaires. »

RÈGLES DE RÉDACTION
• Claire, au moment du premier contact, sans jargon.
• Visible sans clic supplémentaire, et accessible (contraste, lecteur d'écran).
• Toujours associée à un moyen de joindre un humain.

SOURCES
• Règlement (UE) 2024/1689, article 50 ; lignes directrices de la Commission européenne sur la transparence.`,
  },
  {
    ref: 'YEBA-GOUV-08', theme: 'IA Act', titre: 'Supervision humaine documentée — fiche procédure', item: 'Supervision humaine documentée',
    resume: 'Qui valide quoi, à quel moment, et comment on garde la preuve qu’un humain a contrôlé.',
    texte: `LE PRINCIPE
Une IA propose, un humain décide et assume. Pour les usages à haut risque, la supervision humaine est une obligation : elle est confiée à des personnes qui ont la compétence, la formation et l'autorité nécessaires (IA Act, art. 26.2). Pour tous les autres usages, c'est la meilleure protection contre l'erreur. Le RGPD interdit en outre qu'une décision produisant un effet juridique ou significatif sur une personne soit entièrement automatisée sans garanties (art. 22).

POUR CHAQUE USAGE, ÉCRIRE
• Le point de contrôle : à quelle étape un humain valide, de préférence juste avant la première action irréversible (envoi, paiement, publication, décision).
• Le contrôleur : nom ou fonction, et son remplaçant.
• Ce qu'il vérifie : faits, chiffres recalculés, ton, données personnelles, conformité.
• Son pouvoir : il peut refuser, corriger ou arrêter l'outil.

GARDER LA PREUVE
• Un journal simple : date, usage, contrôleur, décision (validé, corrigé, refusé), motif en une ligne.
• Pour un agent qui agit seul : journal d'exécution conservé et relu, plafonds de consommation, procédure d'arrêt d'urgence testée.
• Pour un usage à haut risque : conserver les journaux générés par le système au moins six mois (art. 26.6).

LES QUATRE NIVEAUX D'AUTONOMIE
• Propose : l'IA suggère, l'humain fait.
• Exécute sous accord : l'IA prépare, l'humain valide avant chaque action.
• Exécute et rend compte : l'IA agit, l'humain contrôle a posteriori.
• Décide seul : réservé aux tâches dont l'erreur ne coûte presque rien.
Le niveau se fixe sur le coût de l'erreur, jamais sur le confort d'usage.

SIGNAUX D'ALERTE
• Personne ne relit plus « parce que c'est toujours bon ».
• Le contrôleur n'a pas le temps alloué pour contrôler.
• Une erreur a été découverte par un client plutôt que par le contrôle.

SOURCES
• Règlement (UE) 2024/1689, articles 14 et 26 ; RGPD, article 22.`,
  },
  {
    ref: 'YEBA-GOUV-09', theme: 'IA Act', titre: 'Charte d’usage de l’IA en entreprise — modèle d’une page', item: null,
    resume: 'Repris du modèle du Pack Qualiopi de YEBA Studio et adapté à toute entreprise : permis, interdit, qui arbitre.',
    texte: `OBJET
Cette charte encadre l'usage des outils d'intelligence artificielle par les salariés, dirigeants et prestataires de [ENTREPRISE]. Elle fait partie des mesures prises pour favoriser la maîtrise de l'IA de l'équipe (IA Act, art. 4).

PRINCIPES
• Transparence : nous indiquons quand un contenu diffusé a été produit avec une IA (fiche YEBA-GOUV-07).
• Contrôle humain : aucune décision concernant une personne (recrutement, évaluation, sanction, crédit) n'est prise par une IA.
• Données : aucune donnée personnelle ou confidentielle dans un outil non validé ; règle des trois bacs (fiche YEBA-GOUV-03).
• Souveraineté : préférence pour des outils hébergés dans l'Union européenne ou installés chez nous.
• Vérification : un chiffre, une date, une référence juridique produits par l'IA sont toujours vérifiés à la source.

CE QUI EST PERMIS
• Les outils de la liste validée, avec le compte professionnel fourni par l'entreprise.
• Rédiger, résumer, traduire, reformuler, préparer un tableau, sur des données des bacs 1 et 2.

CE QUI EST INTERDIT
• Utiliser un compte personnel pour le travail.
• Saisir des données du bac 3.
• Diffuser un contenu généré sans relecture.
• Activer une nouvelle fonction d'IA dans un logiciel sans l'inscrire à l'inventaire (fiche YEBA-GOUV-05).

OUTILS VALIDÉS
• [Outil] — [usage autorisé] — [données autorisées] — [hébergement] — [responsable].

QUI ARBITRE
• Les cas non prévus sont soumis à [NOM, FONCTION], qui répond sous 5 jours ouvrés.
• Tout incident (donnée saisie par erreur, contenu faux diffusé) est signalé le jour même ; la procédure violation de données (fiche YEBA-GOUV-04) s'applique si nécessaire.

ENGAGEMENT
• Lu et approuvé par : [NOM], le [DATE], signature.
• Revue de la charte : une fois par an, et à chaque nouvel outil.

SOURCES
• Règlement (UE) 2024/1689, articles 4 et 50 ; RGPD, articles 5 et 22.`,
  },
].map((d) => ({ ...d, version: VERSION, date: DATE }))

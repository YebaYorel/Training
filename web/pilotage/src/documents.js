/* Documents d'une action de formation, remplis avec les données saisies une seule fois.
 * Références : Code du travail L6353-1 et D6353-1 (convention, attestation), L6353-3 à L6353-7
 * (contrat avec une personne physique : rétractation 10 jours, acompte 30 % maximum),
 * R6352-1 à R6352-15 (règlement intérieur), CGI art. 293 B (franchise en base) puis TVA 8,5 % (La Réunion),
 * CGI art. 261-4-4° a (exonération de la formation, seulement avec l'attestation 3511-SD), L6352-12 (« ne vaut pas agrément »),
 * Code de commerce L441-9 et L441-10 (mentions de facture, pénalités, indemnité de 40 €).
 * Chaque document est MODIFIABLE (Word) : relisez-le avant signature. */
(function (G) {
  "use strict";
  const P = (G.Pilotage = G.Pilotage || {});
  const D = G.Decorticage;
  const AC = "……………………";
  const frd = (iso) => (iso ? D.fr(D.lireDate(iso)) : AC);
  const euros = (n) => (n || n === 0 ? Number(n).toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €" : AC);

  function infos(donnees, action) {
    const yeba = donnees.identite, f = donnees.formations.find((x) => x.id === action.formationId);
    const intitule = action.intitule || (f && f.titre) || AC;
    const autre = (action.pour_centre || "").trim();
    const nomOrg = autre ? autre : yeba.nom;
    // marque blanche : tous les modèles reçoivent l'identité du donneur d'ordre (à compléter par lui), jamais celle de YEBA ;
    // seul le nom du formateur reste (il anime réellement la formation)
    const id = autre ? { nom: autre, dirigeant: yeba.dirigeant, siret: AC, nda: AC, qualiopi: AC, adresse: "", code_postal: "", ville: AC, email: "", telephone: "", referent_handicap: AC } : yeba;
    return { id, yeba, f, intitule, autre, nomOrg, cli: action.client || {}, st: action.stagiaires || [] };
  }
  const adresse = (id) => [id.adresse, [id.code_postal, id.ville].filter(Boolean).join(" ")].filter(Boolean).join(", ");
  // Bloc-marque légal en pied de page (jamais en marque blanche)
  P.blocMarque = (id) => [`${id.nom} — ${id.dirigeant}, directeur · ${adresse(id)}`, `Tél. ${id.telephone || AC} · ${id.email || AC} · SIRET ${id.siret}`,
    `Déclaration d'activité n° ${id.nda} auprès du préfet de La Réunion. Cet enregistrement ne vaut pas agrément de l'État.`,
    `Certification Qualiopi n° ${id.qualiopi}${id.certificateur ? " — " + id.certificateur : ""} · Référent handicap : ${id.referent_handicap || AC}`].join("\n");
  /* En-tête : en sous-traitance (marque blanche), l'organisme est le centre donneur d'ordre — AUCUNE donnée YEBA
   * (nom, SIRET, NDA, Qualiopi, coordonnées). Seule la facture, adressée au donneur d'ordre, porte l'identité YEBA. */
  const entete = (o, I, action, facture) => {
    const Y = facture ? I.yeba : I.id;
    const org = I.autre && !facture ? `${I.autre}\n(coordonnées de l'organisme donneur d'ordre)` :
      `${Y.nom}\nSIRET ${Y.siret}\nDéclaration d'activité n° ${Y.nda} (ne vaut pas agrément de l'État)\n${adresse(Y)}\n${Y.email || ""} ${Y.telephone || ""}`;
    const cli = facture && I.autre ? `${I.autre}\n${I.cli.adresse || ""}` : `${I.cli.raison || AC}\n${I.cli.siret ? "SIRET " + I.cli.siret + "\n" : ""}${I.cli.adresse || ""}\n${I.cli.contact ? "Représenté(e) par " + I.cli.contact : ""}`;
    o.tableau([["Organisme de formation", facture ? "Facturé à" : "Bénéficiaire / client"], [org, cli]]);
  };
  const caract = (o, I, a) => o.tableau([["Élément", "Détail"], ["Intitulé", I.intitule], ["Objectifs", a.objectifs || (I.f ? "Voir programme joint (objectifs opérationnels et évaluables)" : AC)],
    ["Nature de l'action", a.nature || "Action de formation (art. L6313-1 du Code du travail)"], ["Dates", `du ${frd(a.debut)} au ${frd(a.fin)}`],
    ["Durée", a.heures ? `${a.heures} heures par stagiaire` : AC], ["Horaires", a.horaires || AC], ["Lieu", a.lieu || AC], ["Effectif", String(I.st.length || a.effectif || AC)],
    ["Modalités", a.modalites || "Présentiel ; apports, études de cas, mises en situation"], ["Évaluation", "Positionnement d'entrée, évaluations formatives, grille critériée, attestation de fin de formation"]]);

  const MODELES = {
    // action courte sans décorticage (intra, inter) : programme à compléter, avec les mentions de l'indicateur 1
    programme: (o, I, a) => {
      caract(o, I, a);
      o.h2("Public et prérequis");
      o.tableau([["", ""], ["Public visé", a.public || AC], ["Prérequis", a.prerequis || "Aucun"], ["Délai d'accès", a.delai_acces || I.id.delai_acces || AC], ["Méthodes pédagogiques", a.modalites || "Présentiel ; apports courts, études de cas, mises en situation, jeux de rôle"],
        ["Financements mobilisables", a.financements || "Plan de développement des compétences de l'entreprise, OPCO (selon critères), autofinancement. Action non éligible au CPF (pas de certification RNCP/RS)."],
        ["Accessibilité (handicap)", `Locaux et supports adaptables. Référent handicap : ${I.id.referent_handicap || AC}`], ["Tarif", a.prix_ht ? `${euros(a.prix_ht)} HT pour l'action` : AC]]);
      o.h2("Déroulé");
      o.tableau([["Séquence", "Objectif (verbe d'action)", "Contenus et méthodes", "Durée"], ["1", "", "", ""], ["2", "", "", ""], ["3", "", "", ""], ["4", "", "", ""]]);
      o.p("Preuve Qualiopi : indicateurs 1 et 5 (information du public, objectifs et contenus).");
    },
    besoin: (o, I, a) => {
      o.p(`Action : ${I.intitule} · Client : ${I.cli.raison || AC} · Date de l'échange : ${AC}`);
      o.tableau([["Question", "Réponse"], ["Contexte et enjeux de l'entreprise / du bénéficiaire", ""], ["Public concerné (postes, nombre, niveau)", ""],
        ["Compétences à développer / situations de travail visées", ""], ["Prérequis et acquis déjà présents", ""], ["Besoins spécifiques (handicap, horaires, distance)", ""],
        ["Contraintes (dates, lieu, budget, financement)", ""], ["Indicateurs de réussite attendus par le client", ""], ["Adaptations décidées pour la prestation", ""]]);
      o.p("Preuve Qualiopi : indicateur 4 (analyse du besoin). Signature du client :");
    },
    convention: (o, I, a) => {
      o.p("Établie en application des articles L6353-1 et D6353-1 du Code du travail.");
      entete(o, I, a);
      o.h2("Article 1 — Objet et caractéristiques de l'action"); caract(o, I, a);
      o.h2("Article 2 — Stagiaires"); o.tableau([["Nom", "Prénom", "Fonction / statut"]].concat(I.st.length ? I.st.map((s) => [s.nom, s.prenom, s.statut || ""]) : [["", "", ""]]));
      o.h2("Article 3 — Prix et modalités de règlement");
      { const m = P.montantsAction(a); o.p(`Coût total : ${euros(m.ht)} HT. ${m.regime.mention}.${m.tva ? ` Montant TTC : ${euros(m.ttc)}.` : ""}`); }
      if (P.num(a.prise_en_charge_ht) > 0) o.p(`Prise en charge par ${a.financeur_nom || "le financeur"} : ${euros(a.prise_en_charge_ht)} HT ; reste à charge du client : ${euros(P.num(a.prix_ht) - P.num(a.prise_en_charge_ht))} HT.`);
      o.p(`Règlement : ${a.reglement || "à réception de facture, à 30 jours"}. Financeur : ${P.ORIGINES[a.origine] || AC}${a.subrogation ? " (subrogation de paiement)" : ""}.`);
      o.h2("Article 4 — Moyens et suivi"); o.p("Feuilles d'émargement signées par demi-journée ; attestation de fin de formation et certificat de réalisation remis à l'issue de l'action.");
      o.h2("Article 5 — Annulation, absence, abandon");
      o.p(a.conditions_annulation || "En cas d'annulation par le client moins de 10 jours ouvrés avant le début, seules les sommes correspondant aux frais engagés pourront être facturées. En cas d'abandon ou d'absence, seules les heures réellement suivies sont dues, sauf cas de force majeure dûment reconnue.");
      o.h2("Article 6 — Accessibilité"); o.p(`Le client informe l'organisme de tout besoin d'adaptation lié à une situation de handicap. Référent handicap : ${I.id.referent_handicap || AC}.`);
      o.h2("Article 7 — Litiges"); o.p("À défaut d'accord amiable, le tribunal compétent est celui du siège de l'organisme de formation.");
      o.tableau([[`Pour ${I.id.nom}`, `Pour ${I.cli.raison || "le client"}`], [`Fait à ${I.id.ville || AC}, le ${AC}\nSignature et cachet`, `Fait à ${AC}, le ${AC}\nSignature et cachet`]]);
    },
    contrat: (o, I, a) => {
      o.p("Contrat conclu en application des articles L6353-3 à L6353-7 du Code du travail (personne physique finançant tout ou partie de sa formation).");
      entete(o, I, a); caract(o, I, a);
      { const m = P.montantsAction(a); o.h2("Prix"); o.p(`${euros(m.ttc)} à payer (${m.regime.mention}). Modalités : ${a.reglement || AC}.`); }
      o.encadre("Délai de rétractation (art. L6353-5)", ["À compter de la signature, le stagiaire dispose de 10 jours pour se rétracter, par lettre recommandée avec avis de réception.",
        "Aucune somme ne peut être exigée avant l'expiration de ce délai (art. L6353-6).", "À l'expiration du délai, il ne peut être payé plus de 30 % du prix ; le solde est échelonné au fur et à mesure du déroulement de l'action."]);
      o.p("Si, par suite de force majeure dûment reconnue, le stagiaire est empêché de suivre la formation, il peut rompre le contrat ; seules les prestations effectivement dispensées sont dues au prorata (art. L6354-1).");
      o.tableau([["L'organisme", "Le stagiaire (« lu et approuvé »)"], [`Le ${AC}`, `Le ${AC}`]]);
    },
    convocation: (o, I, a) => {
      o.p(`Madame, Monsieur, nous avons le plaisir de vous convier à la formation « ${I.intitule} ».`);
      o.tableau([["", ""], ["Dates", `du ${frd(a.debut)} au ${frd(a.fin)}`], ["Horaires", a.horaires || AC], ["Lieu", a.lieu || AC], ["Accès / stationnement", a.acces || AC], ["Interlocuteur", `${I.id.dirigeant} — ${I.id.telephone || ""} ${I.id.email || ""}`]]);
      o.h2("Livret d'accueil");
      ["Présentation de l'organisme et du formateur", "Déroulé et objectifs (programme joint)", "Règlement intérieur (joint) : horaires, sécurité, assiduité", "Besoin d'adaptation (handicap, santé) : contactez le référent handicap " + (I.id.referent_handicap || ""),
        "Réclamations : par écrit à " + (I.id.email || "l'adresse de l'organisme") + ", réponse sous 15 jours", "Matériel à apporter : de quoi écrire ; ordinateur si possible"].forEach((x) => o.puce(x));
    },
    reglement: (o, I, a) => {
      o.p("Établi conformément aux articles L6352-3 à L6352-5 et R6352-1 à R6352-15 du Code du travail. Il s'applique à tous les stagiaires, pour toute la durée de l'action.");
      [["Article 1 — Hygiène et sécurité", "Chaque stagiaire respecte les consignes de sécurité du lieu de formation et les consignes d'évacuation affichées. Il est interdit de fumer et de vapoter dans les locaux."],
        ["Article 2 — Assiduité", "Les horaires sont fixés par l'organisme. Toute absence ou retard est signalé et justifié. Le stagiaire signe la feuille d'émargement par demi-journée."],
        ["Article 3 — Comportement", "Chacun adopte un comportement respectueux envers les personnes et le matériel. Toute forme de discrimination ou de harcèlement est proscrite."],
        ["Article 4 — Sanctions", "Tout manquement peut faire l'objet d'une sanction (avertissement, exclusion temporaire ou définitive), dans le respect de la procédure disciplinaire (R6352-4 à R6352-8) : convocation, entretien avec possibilité d'être assisté, notification écrite et motivée."],
        ["Article 5 — Représentation des stagiaires", "Pour les actions d'une durée supérieure à 500 heures, un délégué titulaire et un suppléant sont élus (R6352-9 et suivants)."],
        ["Article 6 — Réclamations", "Toute réclamation est adressée par écrit à l'organisme, qui accuse réception et répond sous 15 jours."]].forEach(([t, x]) => { o.h2(t); o.p(x); });
      o.p(`Fait à ${I.id.ville || AC}, le ${AC}. ${I.id.dirigeant}, ${I.id.nom}`);
    },
    positionnement: (o, I, a) => {
      o.p(`Stagiaire : ${AC}    Date : ${AC}    Formation : ${I.intitule}`);
      o.tableau([["Compétence ou thème du programme", "Je ne sais pas faire", "Je sais faire avec aide", "Je sais faire seul", "Je peux l'expliquer"]].concat(
        (I.f && I.f._competences ? I.f._competences : ["Compétence 1", "Compétence 2", "Compétence 3", "Compétence 4"]).map((c) => [c, "☐", "☐", "☐", "☐"])));
      o.p("Mes attentes, mes besoins d'adaptation : ……………………………………………………………");
      o.p("Synthèse du formateur et adaptations du parcours : …………………………………………… (Qualiopi : indicateurs 8 et 10)");
    },
    emargement: (o, I, a) => {
      const jours = P.joursAction(a);
      const lignes = I.st.length ? I.st : [{ nom: "", prenom: "" }, { nom: "", prenom: "" }, { nom: "", prenom: "" }];
      for (const j of jours.length ? jours : [""]) {
        o.h2(`Feuille d'émargement — ${j ? frd(j) : "date : " + AC}`);
        o.p(`${I.intitule} · Formateur : ${I.id.dirigeant} · Lieu : ${a.lieu || AC}`);
        o.tableau([["Nom", "Prénom", "Matin — signature", "Après-midi — signature"]].concat(lignes.map((s) => [s.nom || "", s.prenom || "", "", ""])).concat([["Formateur", I.id.dirigeant, "", ""]]));
      }
    },
    seances: (o, I, a) => {
      o.p("Les fiches de séance, diaporamas, exercices, ressources, grilles et quiz produits par le module « Séances » constituent les preuves du déroulé de cette action.");
      const f = I.f;
      if (f && f.packs) Object.values(f.packs).sort((x, y) => x.date.localeCompare(y.date)).forEach((p) => o.puce(`${frd(p.date)} — ${p.titre} (${p.source === "claude" ? "rédigé avec Claude, relu par le formateur" : "version de base"})`));
      else o.p("Aucune séance produite pour l'instant.");
    },
    evaluation: (o, I, a) => {
      o.p(`Évaluation des acquis — ${I.intitule}. Résultat par stagiaire au regard des objectifs (grilles critériées des séances et épreuve finale).`);
      o.tableau([["Stagiaire", "Objectifs atteints", "Partiellement", "Non atteints", "Observations"]].concat((I.st.length ? I.st : [{}, {}, {}]).map((s) => [`${s.prenom || ""} ${s.nom || ""}`, "", "", "", ""])));
    },
    chaud: (o, I, a) => {
      o.p(`Votre avis sur la formation « ${I.intitule} » (${frd(a.debut)} – ${frd(a.fin)}). Anonyme si vous le souhaitez.`);
      o.tableau([["Question", "1", "2", "3", "4"]].concat(["Les objectifs annoncés ont été atteints", "Le contenu correspond à mes besoins", "Le rythme et la durée étaient adaptés",
        "Les supports et exercices m'ont aidé à comprendre", "L'animation du formateur", "L'organisation (accueil, salle, horaires)", "Je pourrai appliquer ce que j'ai appris"].map((q) => [q, "☐", "☐", "☐", "☐"])));
      o.p("1 = pas du tout d'accord · 4 = tout à fait d'accord. Ce que je retiens : …………… Ce qu'il faudrait améliorer : ……………");
    },
    froid: (o, I, a) => {
      o.p(`Trois mois après la formation « ${I.intitule} » : qu'en avez-vous fait ?`);
      o.tableau([["Question", "Oui", "En partie", "Non"]].concat(["J'utilise ce que j'ai appris dans mon travail", "La formation m'a aidé à obtenir / garder un emploi ou un contrat",
        "J'ai obtenu la certification visée (le cas échéant)", "Je recommanderais cette formation"].map((q) => [q, "☐", "☐", "☐"])));
      o.p("Situation actuelle (emploi, contrat, poursuite d'études) : …………… (Qualiopi : indicateurs 2 et 30)");
    },
    attestation: (o, I, a) => {
      for (const s of I.st.length ? I.st : [{ nom: AC, prenom: "" }]) {
        o.h2(`Attestation de fin de formation — ${s.prenom || ""} ${s.nom || ""}`);
        o.p(`Je soussigné ${I.id.dirigeant}, représentant ${I.id.nom} (déclaration d'activité n° ${I.id.nda}), atteste que ${s.prenom || ""} ${s.nom || ""} a suivi l'action de formation :`);
        o.tableau([["", ""], ["Intitulé", I.intitule], ["Objectifs", a.objectifs || "voir programme"], ["Nature", a.nature || "Action de formation (art. L6313-1)"], ["Dates", `du ${frd(a.debut)} au ${frd(a.fin)}`],
          ["Durée suivie", s.heures ? `${s.heures} heures` : a.heures ? `${a.heures} heures` : AC], ["Résultats de l'évaluation des acquis", s.resultat || AC]]);
        o.p(`Établie en application de l'article L6353-1 du Code du travail. Fait à ${I.id.ville || AC}, le ${AC}. Signature :`);
        o.saut();
      }
    },
    realisation: (o, I, a) => {
      for (const s of I.st.length ? I.st : [{ nom: AC, prenom: "" }]) {
        o.h2(`Certificat de réalisation — ${s.prenom || ""} ${s.nom || ""}`);
        o.p(`Je soussigné ${I.id.dirigeant}, représentant légal du dispensateur de l'action ${I.id.nom}, atteste que :`);
        o.tableau([["", ""], ["Bénéficiaire", `${s.prenom || ""} ${s.nom || ""}${s.entreprise ? " — " + s.entreprise : ""}`], ["Intitulé de l'action", I.intitule],
          ["Nature de l'action (art. L6313-1)", a.type === "apprentissage" ? "☐ formation  ☐ bilan  ☐ VAE  ☒ apprentissage" : "☒ action de formation  ☐ bilan de compétences  ☐ VAE  ☐ apprentissage"],
          ["Dates", `du ${frd(a.debut)} au ${frd(a.fin)}`], ["Durée réalisée", s.heures ? `${s.heures} heures` : a.heures ? `${a.heures} heures` : AC]]);
        o.p("Sans préjudice des délais imposés par les règles de prescription, le dispensateur s'engage à conserver l'ensemble des pièces justificatives (dont les feuilles d'émargement) pour une durée de 3 ans à compter de la fin de l'année du dernier paiement.");
        o.p(`Fait à ${I.id.ville || AC}, le ${AC}. Cachet et signature. — Modèle à vérifier selon le financeur (OPCO, Caisse des dépôts).`);
        o.saut();
      }
    },
    facture: (o, I, a) => {
      const num = a.numero_facture || AC, m = P.montantsAction(a), ht = m.ht, tva = m.tva;
      o.tableau([["Facture n°", "Date", "Échéance"], [num, frd(a.date_facture), frd(a.echeance_facture)]]);
      entete(o, I, a, true);
      o.tableau([["Désignation", "Quantité", "Prix unitaire HT", "Total HT"], [`${I.intitule} — du ${frd(a.debut)} au ${frd(a.fin)} (${a.heures || AC} h)`, String(I.st.length || 1), euros(ht / Math.max(I.st.length || 1, 1)), euros(ht)]]);
      o.tableau([["Total HT", euros(ht)], [m.regime.code === "tva" ? `TVA ${String(m.regime.taux).replace(".", ",")} %` : "TVA", m.regime.code === "tva" ? euros(tva) : m.regime.mention], ["Total à payer", euros(m.ttc)]]);
      if (P.num(a.prise_en_charge_ht) > 0) o.p(`Dont pris en charge par ${a.financeur_nom || "le financeur"} : ${euros(P.num(a.prise_en_charge_ht) * (m.ttc / (ht || 1)))}${a.subrogation ? " (subrogation de paiement : facture adressée au financeur pour sa part)" : ""}.`);
      if (m.regime.code === "tva" && I.yeba.tva_intra) o.p(`N° de TVA intracommunautaire : ${I.yeba.tva_intra}.`);
      o.p(`Règlement par virement${I.yeba.iban ? " — IBAN " + I.yeba.iban + (I.yeba.bic ? " — BIC " + I.yeba.bic : "") : ""}. Merci de rappeler le n° de facture ${num} dans le libellé du virement. En cas de retard : pénalités au taux de 3 fois le taux d'intérêt légal et indemnité forfaitaire pour frais de recouvrement de 40 € (art. L441-10 du Code de commerce, clients professionnels). Pas d'escompte pour paiement anticipé.`);
      o.p(`Organisme de formation enregistré sous le n° ${I.yeba.nda} auprès du préfet de région de La Réunion (cet enregistrement ne vaut pas agrément de l'État).`);
    },
    bilan: (o, I, a) => {
      o.tableau([["Indicateur", "Résultat"], ["Stagiaires", String(I.st.length || a.effectif || 0)], ["Abandons", String(a.abandons || 0)], ["Satisfaction à chaud (moyenne /4)", String(a.satisfaction_chaud || AC)],
        ["Réussite à la certification", a.presentes ? `${a.admis || 0} / ${a.presentes}` : AC], ["Réclamations reçues", String(a.reclamations || 0)]]);
      o.h2("Points forts"); o.p(AC); o.h2("Difficultés rencontrées et aléas"); o.p(AC);
      o.h2("Actions d'amélioration décidées (Qualiopi : indicateur 32)"); o.tableau([["Action", "Responsable", "Échéance"], ["", I.id.dirigeant, ""]]);
    },
    eval_enseignements: (o, I, a) => {
      o.p("Questionnaire anonyme, distinct de l'enquête de satisfaction : il porte sur les ENSEIGNEMENTS (contenus, méthodes, utilité). Qualiopi V10 — indicateur 33.");
      o.tableau([["Pour chaque module, cochez", "Pas du tout", "Plutôt non", "Plutôt oui", "Tout à fait"], ["Les contenus étaient clairs", "", "", "", ""], ["Les exemples m'ont aidé à comprendre", "", "", "", ""],
        ["Les exercices m'ont fait progresser", "", "", "", ""], ["Je peux utiliser ce que j'ai appris en entreprise", "", "", "", ""], ["Le rythme était adapté", "", "", "", ""]]);
      o.h2("Ce que je changerais"); o.p(AC); o.h2("Ce qu'il faut garder"); o.p(AC);
      o.p("Exploitation : synthèse transmise au CFA et au formateur ; décisions reportées au plan d'amélioration (indicateur 32).");
    },
    tripartite: (o, I, a) => {
      o.p(`Apprenti : ${AC}   Tuteur / maître d'apprentissage : ${AC}   Formateur : ${I.id.dirigeant}   Date : ${AC}`);
      o.tableau([["Thème", "Constats", "Décisions"], ["Missions confiées en entreprise / lien avec le programme", "", ""], ["Progression et difficultés", "", ""],
        ["Assiduité, savoir-être, sécurité", "", ""], ["Droits et devoirs de l'apprenti (rappel)", "", ""], ["Prochaines étapes", "", ""]]);
      o.p("Qualiopi : indicateurs 13 (coordination avec l'employeur) et 15 (droits et devoirs).");
    },
  };

  P.joursAction = function (a) {
    if (!a.debut || !a.fin) return [];
    const jours = [];
    const set = (a.jours_semaine || "1,2,3,4,5").match(/[1-7]/g).map((x) => +x - 1);
    for (let j = D.lireDate(a.debut), fin = D.lireDate(a.fin); j <= fin && jours.length < 400; j = D.ajoutJours(j, 1))
      if (set.includes(D.jourSem(j)) && !D.feries(j.getUTCFullYear())[D.iso(j)]) jours.push(D.iso(j));
    return jours;
  };

  async function genererDocument(donnees, action, docId, logo) {
    const meta = P.DOCS.find((d) => d.id === docId);
    const I = infos(donnees, action);
    const charte = Object.assign({}, donnees.charte, { nom_organisme: I.nomOrg });
    const facture = docId === "facture";
    // facture : toujours au nom de l'émetteur réel (YEBA), même en sous-traitance ; le reste suit la marque blanche
    const ctx = { charte: facture ? Object.assign({}, donnees.charte, { nom_organisme: I.yeba.nom }) : charte, nomOrg: facture ? I.yeba.nom : I.nomOrg,
      logo: I.autre && !facture ? null : logo, pied: I.autre && !facture ? "" : P.blocMarque(I.yeba) };
    if (docId === "programme" && I.f) {
      const c = Object.assign(P.contexteFormation(I.f, charte, ctx.logo), { pied: ctx.pied });
      return [`Programme_${slug(I.intitule)}.docx`, await D.programmeDocx(c)];
    }
    const blob = await D.docWord(ctx, `${meta.titre} — ${I.intitule}`, (o) => MODELES[docId](o, I, action));
    return [`${meta.titre.split(" (")[0].replace(/[^A-Za-zÀ-ÿ0-9]+/g, "_")}_${slug(I.intitule)}.docx`, blob];
  }
  const slug = (s) => D.normaliser(s).replace(/[^a-z0-9]+/g, "-").slice(0, 40);

  // Documents attendus pour une action, avec la date limite calculée
  function attendus(action) {
    return P.DOCS.filter((d) => !d.si || d.si(action)).map((d) => {
      const ref = d.quand[0] === "debut" ? action.debut : action.fin;
      const limite = ref ? D.iso(D.ajoutJours(D.lireDate(ref), d.quand[1])) : "";
      const etat = (action.docs && action.docs[d.id] && action.docs[d.id].etat) || "a_faire";
      return Object.assign({}, d, { limite, etat });
    });
  }

  /* Documents de la bibliothèque Qualiopi produits par le logiciel (hors action). Chacun est un MODÈLE pré-rempli
   * avec vos données : relisez-le, complétez-le, puis déposez la version validée dans la bibliothèque. */
  const BIBLIO = {
    methode_resultats: (o, d) => {
      const r = P.resultats(d), pct = (x) => (x === null ? "donnée insuffisante" : Math.round(x * 100) + " %");
      o.p("Qualiopi V10 — indicateur 2 : chaque indicateur publié est accompagné de sa méthode de calcul.");
      o.tableau([["Indicateur", "Résultat", "Méthode de calcul"],
        ["Satisfaction à chaud", r.satisfaction === null ? "donnée insuffisante" : r.satisfaction.toFixed(1).replace(".", ",") + " / 4", `Moyenne des notes moyennes de satisfaction en fin d'action, sur ${r.actionsNotees} action(s) notée(s)${r.periode ? ` terminée(s) du ${frd(r.periode[0])} au ${frd(r.periode[1])}` : ""}. Échelle de 1 à 4.`],
        ["Taux de réussite", pct(r.reussite), `Admis ÷ présentés à l'évaluation finale ou à la certification (${r.admis} / ${r.presentes}).`],
        ["Taux d'abandon", pct(r.abandon), `Stagiaires ayant quitté l'action avant la fin ÷ stagiaires inscrits (${r.abandons} / ${r.stagiaires}).`],
        ["Volume", `${r.actions} action(s), ${r.stagiaires} stagiaire(s)`, "Actions terminées à la date d'édition, hors actions annulées."]]);
      o.p("Tant que le nombre de répondants est inférieur à 10, la mention « résultats en cours de constitution » accompagne le chiffre publié.");
      o.p(`Édité le ${frd(new Date().toISOString().slice(0, 10))}.`);
    },
    registre_risques: (o, d) => {
      o.p("Qualiopi V10 — indicateur 32 : analyse des risques susceptibles d'altérer la qualité des actions. Revue au moins une fois par semestre.");
      const lignes = (d.risques && d.risques.length ? d.risques : [
        { risque: "Formateur indisponible (maladie, empêchement)", p: "Moyenne", i: "Forte", mesure: "Liste de formateurs suppléants conventionnés ; supports prêts à l'avance" },
        { risque: "Financement non accordé avant la session", p: "Moyenne", i: "Forte", mesure: "Accord écrit de prise en charge exigé avant l'envoi des convocations" },
        { risque: "Lieu inaccessible ou non conforme (PMR, alerte cyclonique)", p: "Moyenne", i: "Forte", mesure: "Fiche de reconnaissance du site (YEBA-DOC-15) ; plan de report ; bascule à distance si possible" },
        { risque: "Panne informatique ou de visioconférence", p: "Moyenne", i: "Moyenne", mesure: "Supports hors ligne et imprimés ; connexion de secours" },
        { risque: "Fuite ou perte de données de stagiaires", p: "Faible", i: "Forte", mesure: "Coffre chiffré, sauvegardes chiffrées hebdomadaires, double authentification, registre des violations" },
        { risque: "Dépendance à un outil hors Union européenne", p: "Moyenne", i: "Moyenne", mesure: "Inventaire des outils (registre des traitements) ; alternatives européennes" },
        { risque: "Décrochage d'un stagiaire", p: "Moyenne", i: "Moyenne", mesure: "Suivi des absences, entretien individuel, adaptation du rythme (indicateur 12)" },
        { risque: "Violence, harcèlement ou discrimination en formation", p: "Faible", i: "Forte", mesure: "Procédure YEBA-DOC-14, registre des signalements, information à l'accueil" }]);
      o.tableau([["Risque", "Probabilité", "Impact", "Mesure de prévention", "Responsable", "Prochaine revue"]].concat(lignes.map((x) => [x.risque, x.p, x.i, x.mesure, x.resp || d.identite.dirigeant, x.revue || AC])));
    },
    plan_competences: (o, d) => {
      o.p("Qualiopi — indicateur 22 : entretien et développement des compétences du dirigeant-formateur.");
      o.tableau([["Domaine", "Formation ou certification", "Date", "Preuve"], ["Intelligence artificielle", "Google AI Specialist", AC, "Certificat"], ["Intelligence artificielle", "Google Professional AI", AC, "Certificat"],
        ["Cybersécurité", "SecNumacadémie (ANSSI)", AC, "Attestation"], ["Protection des données", "MOOC « L'atelier RGPD » (CNIL)", AC, "Attestation"], ["Handicap", "Référent handicap en organisme de formation", AC, "Attestation"],
        ["Pédagogie", AC, AC, AC], ["Prévu (12 prochains mois)", AC, AC, AC]]);
    },
    moyens: (o, d) => {
      o.p("Qualiopi — indicateur 17 : moyens humains et techniques, environnement approprié.");
      o.tableau([["Moyen", "Description", "Accessibilité / adaptation"], ["Salle(s)", AC, "Accès PMR à vérifier sur le registre public d'accessibilité du lieu"], ["Matériel", "Vidéoprojecteur, écran, ordinateur portable du formateur, paperboard", "Supports en gros caractères, police Inter, contrastes vérifiés"],
        ["Supports", "Diaporama, fiches « L'essentiel de la journée », exercices, grilles critériées", "Versions numériques lisibles par synthèse vocale"], ["Encadrement", `${d.identite.dirigeant}, formateur ; référent handicap : ${d.identite.referent_handicap}`, AC]]);
    },
    coordination: (o, d) => {
      o.p("Qualiopi — indicateur 18 : mobilisation et coordination des intervenants internes et externes.");
      o.tableau([["Fonction", "Personne", "Rôle", "Coordination"], ["Direction, pédagogie, référent handicap", d.identite.dirigeant, "Conception, animation, suivi qualité", "—"], ["Formateurs sous-traitants", AC, "Animation", "Convention YEBA-DOC-07, réunion de préparation avant chaque action"],
        ["Comptabilité", AC, "Tenue des comptes, TVA, BPF", AC], ["Logistique (salles, hôtels)", AC, "Réservation, accessibilité", "Fiche YEBA-DOC-15"]]);
    },
    eval_enseignements: (o, d) => MODELES.eval_enseignements(o, { id: d.identite }, {}),
  };
  P.BIBLIO_GENERABLES = Object.keys(BIBLIO);
  async function genererBiblio(donnees, id, logo) {
    const meta = P.BIBLIOTHEQUE.find((b) => b.id === id);
    const ctx = { charte: Object.assign({}, donnees.charte, { nom_organisme: donnees.identite.nom }), nomOrg: donnees.identite.nom, logo, pied: P.blocMarque(donnees.identite) };
    const blob = await D.docWord(ctx, meta.titre, (o) => BIBLIO[id](o, donnees));
    return [`${meta.titre.split(" (")[0].replace(/[^A-Za-zÀ-ÿ0-9]+/g, "_").slice(0, 60)}.docx`, blob];
  }

  Object.assign(P, { genererDocument, genererBiblio, documentsAttendus: attendus, euros, frd });
})(typeof window !== "undefined" ? window : globalThis);

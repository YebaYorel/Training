/* Documents d'une action de formation, remplis avec les données saisies une seule fois.
 * Références : Code du travail L6353-1 et D6353-1 (convention, attestation), L6353-3 à L6353-7
 * (contrat avec une personne physique : rétractation 10 jours, acompte 30 % maximum),
 * R6352-1 à R6352-15 (règlement intérieur), CGI art. 261-4-4° a (exonération de TVA, si attestation),
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
    const id = donnees.identite, f = donnees.formations.find((x) => x.id === action.formationId);
    const intitule = action.intitule || (f && f.titre) || AC;
    const autre = (action.pour_centre || "").trim();
    const nomOrg = autre ? autre : id.nom;
    return { id, f, intitule, autre, nomOrg, cli: action.client || {}, st: action.stagiaires || [] };
  }
  const entete = (o, I, action) => {
    o.tableau([["Organisme de formation", "Bénéficiaire / client"], [
      `${I.id.nom}\nSIRET ${I.id.siret}\nDéclaration d'activité n° ${I.id.nda} (ne vaut pas agrément de l'État)\n${I.id.adresse || ""} ${I.id.ville || ""}\n${I.id.email || ""} ${I.id.telephone || ""}`,
      `${I.cli.raison || AC}\n${I.cli.siret ? "SIRET " + I.cli.siret + "\n" : ""}${I.cli.adresse || ""}\n${I.cli.contact ? "Représenté(e) par " + I.cli.contact : ""}`]]);
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
      o.tableau([["", ""], ["Public visé", a.public || AC], ["Prérequis", a.prerequis || "Aucun"], ["Délai d'accès", a.delai_acces || "Inscription jusqu'à 7 jours avant le début, sous réserve de places"],
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
      o.p(`Coût total : ${euros(a.prix_ht)} HT. ${a.tva === "exonere" ? "Exonération de TVA (article 261-4-4° a du CGI)." : a.tva === "tva" ? `TVA ${a.taux_tva || 8.5} % en sus.` : "TVA : " + AC}`);
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
      o.h2("Prix"); o.p(`${euros(a.prix_ht)} ${a.tva === "exonere" ? "(exonéré de TVA, art. 261-4-4° a du CGI)" : "TTC"}. Modalités : ${a.reglement || AC}.`);
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
      const num = a.numero_facture || AC, ht = Number(a.prix_ht || 0), tva = a.tva === "tva" ? ht * (Number(a.taux_tva || 8.5) / 100) : 0;
      o.tableau([["Facture n°", "Date", "Échéance"], [num, frd(a.date_facture), frd(a.echeance_facture)]]);
      entete(o, I, a);
      o.tableau([["Désignation", "Quantité", "Prix unitaire HT", "Total HT"], [`${I.intitule} — du ${frd(a.debut)} au ${frd(a.fin)} (${a.heures || AC} h)`, String(I.st.length || 1), euros(ht / Math.max(I.st.length || 1, 1)), euros(ht)]]);
      o.tableau([["Total HT", euros(ht)], [a.tva === "tva" ? `TVA ${a.taux_tva || 8.5} %` : "TVA", a.tva === "tva" ? euros(tva) : a.tva === "exonere" ? "Exonération — article 261-4-4° a du CGI" : AC], ["Total à payer", euros(ht + tva)]]);
      o.p(`Règlement par virement${I.id.iban ? " — IBAN " + I.id.iban : ""}. En cas de retard : pénalités au taux de 3 fois le taux d'intérêt légal et indemnité forfaitaire pour frais de recouvrement de 40 € (art. L441-10 du Code de commerce, clients professionnels). Pas d'escompte pour paiement anticipé.`);
      o.p(`Organisme de formation enregistré sous le n° ${I.id.nda} auprès du préfet de région de La Réunion (cet enregistrement ne vaut pas agrément de l'État).`);
    },
    bilan: (o, I, a) => {
      o.tableau([["Indicateur", "Résultat"], ["Stagiaires", String(I.st.length || a.effectif || 0)], ["Abandons", String(a.abandons || 0)], ["Satisfaction à chaud (moyenne /4)", String(a.satisfaction_chaud || AC)],
        ["Réussite à la certification", a.presentes ? `${a.admis || 0} / ${a.presentes}` : AC], ["Réclamations reçues", String(a.reclamations || 0)]]);
      o.h2("Points forts"); o.p(AC); o.h2("Difficultés rencontrées et aléas"); o.p(AC);
      o.h2("Actions d'amélioration décidées (Qualiopi : indicateur 32)"); o.tableau([["Action", "Responsable", "Échéance"], ["", I.id.dirigeant, ""]]);
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
    const ctx = { charte, nomOrg: I.nomOrg, logo: I.autre ? null : logo };
    if (docId === "programme" && I.f) {
      const c = P.contexteFormation(I.f, charte, ctx.logo);
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

  Object.assign(P, { genererDocument, documentsAttendus: attendus, euros, frd });
})(typeof window !== "undefined" ? window : globalThis);

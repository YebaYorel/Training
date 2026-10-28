/* Lecture des documents DANS le navigateur (aucun envoi sur internet) :
 * PDF (pdf.js), Word .docx (JSZip + XML), Excel .xlsx (ExcelJS), texte.
 * Contrôles : signature réelle du fichier, taille, macros, bombe ZIP. */
(function (G) {
  "use strict";
  const D = (G.Decorticage = G.Decorticage || {});
  const TAILLE_MAX = 50 * 1024 * 1024, PAGES_MAX = 400, DECOMP_MAX = 250 * 1024 * 1024;

  class FichierRefuse extends Error {}
  const REFUSES = {
    docm: "Word avec macros : enregistrez-le en .docx (sans macros).",
    xlsm: "Excel avec macros : enregistrez-le en .xlsx (sans macros).",
    doc: "ancien format Word : ouvrez-le puis « Enregistrer sous » .docx.",
    xls: "ancien format Excel : ouvrez-le puis « Enregistrer sous » .xlsx.",
    odt: "format LibreOffice : exportez-le en .docx ou .pdf.",
  };

  const PIED = /^\s*(SIGLE\s+Type de document.*|[A-Z]{2,6}\s+(REAC|RE|RC)\s+TP-\d{5}\s+\d+.*|https?:\/\/www\.francecompetences\.fr\/\S+\s+\d{2}\/\d{2}\/\d{4}.*|Page \d+ sur \d+)\s*$/;
  function nettoyer(texte) {
    const l = texte.split("\n").filter((x) => !PIED.test(x))
      .map((x) => x.replace(/^\s*[•▪●]+\s*/, "- ").replace(/\s+$/, ""));
    return l.join("\n").replace(/’/g, "’").replace(/ /g, " ").replace(/\n{3,}/g, "\n\n");
  }

  // Reconstruit les lignes d'une page (même logique que pdfplumber : tolérance 3 pt)
  function lignesPage(items) {
    const morceaux = items.filter((i) => i.str !== undefined && i.str !== "")
      .map((i) => ({ s: i.str, x: i.transform[4], y: i.transform[5], w: i.width || 0, h: Math.abs(i.transform[3]) || 10 }));
    morceaux.sort((a, b) => b.y - a.y || a.x - b.x);
    const lignes = [];
    for (const m of morceaux) {
      const l = lignes.find((L) => Math.abs(L.y - m.y) <= 3);
      if (l) l.items.push(m); else lignes.push({ y: m.y, items: [m] });
    }
    lignes.sort((a, b) => b.y - a.y);
    return lignes.map((L) => {
      L.items.sort((a, b) => a.x - b.x);
      let out = "", fin = null;
      for (const it of L.items) {
        if (fin !== null && it.x - fin > Math.max(1.2, it.h * 0.12) && !/\s$/.test(out) && !/^\s/.test(it.s)) out += " ";
        out += it.s;
        fin = it.x + it.w;
      }
      return out.replace(/\s{2,}/g, " ").trim();
    }).filter(Boolean).join("\n");
  }

  async function lirePdf(octets) {
    const pdf = await G.pdfjsLib.getDocument({ data: octets, isEvalSupported: false, disableFontFace: true }).promise;
    if (pdf.numPages > PAGES_MAX) throw new FichierRefuse(`PDF trop long (plus de ${PAGES_MAX} pages).`);
    const pages = [];
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      pages.push(lignesPage((await page.getTextContent()).items));
    }
    const texte = pages.join("\n");
    if (texte.trim().length < 50)
      throw new FichierRefuse("Ce PDF ne contient pas de texte lisible (probablement un scan). Utilisez la version numérique officielle.");
    return texte;
  }

  async function verifierZip(octets, attendu) {
    const zip = await G.JSZip.loadAsync(octets);
    const noms = Object.keys(zip.files);
    if (noms.length > 5000) throw new FichierRefuse("Archive anormale (trop d'éléments).");
    let total = 0;
    for (const n of noms) {
      if (n.startsWith("/") || n.split("/").includes("..") || n.includes("\\")) throw new FichierRefuse("Archive piégée (chemin interdit).");
      const f = zip.files[n];
      const taille = f._data && f._data.uncompressedSize ? f._data.uncompressedSize : 0;
      const comp = f._data && f._data.compressedSize ? f._data.compressedSize : 0;
      total += taille;
      if (comp && taille / comp > 120) throw new FichierRefuse("Archive suspecte (bombe de décompression).");
    }
    if (total > DECOMP_MAX) throw new FichierRefuse("Fichier trop volumineux une fois décompressé.");
    if (noms.some((n) => n.toLowerCase().endsWith("vbaproject.bin"))) throw new FichierRefuse("Le fichier contient des macros : refusé.");
    if (!noms.some((n) => n.toLowerCase() === attendu)) throw new FichierRefuse("Le contenu ne correspond pas à l'extension annoncée.");
    return zip;
  }

  async function lireDocx(octets) {
    const zip = await verifierZip(octets, "word/document.xml");
    const xml = await zip.file("word/document.xml").async("string");
    const doc = new DOMParser().parseFromString(xml, "application/xml");
    const W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";
    const lignes = [];
    for (const p of doc.getElementsByTagNameNS(W, "p")) {
      let t = "";
      for (const n of p.getElementsByTagNameNS(W, "*")) {
        if (n.localName === "t") t += n.textContent;
        else if (n.localName === "tab") t += " ";
        else if (n.localName === "br") t += "\n";
      }
      lignes.push(t);
    }
    return lignes.join("\n");
  }

  async function lireXlsx(octets) {
    await verifierZip(octets, "xl/workbook.xml");
    const wb = new G.ExcelJS.Workbook();
    await wb.xlsx.load(octets);
    const lignes = [];
    wb.eachSheet((ws) => ws.eachRow((row) => {
      const v = row.values.slice(1).map((c) => (c && typeof c === "object" ? (c.result ?? c.text ?? (c.richText ? c.richText.map((r) => r.text).join("") : "")) : c))
        .filter((c) => c !== null && c !== undefined && String(c).trim()).map((c) => String(c).trim());
      if (v.length) lignes.push(v.join(" | "));
    }));
    return lignes.join("\n");
  }

  async function lireFichier(fichier) {
    const ext = (fichier.name.split(".").pop() || "").toLowerCase();
    if (REFUSES[ext]) throw new FichierRefuse(`${fichier.name} : format refusé — ${REFUSES[ext]}`);
    if (!["pdf", "docx", "xlsx", "txt"].includes(ext)) throw new FichierRefuse(`${fichier.name} : formats acceptés PDF, DOCX, XLSX, TXT.`);
    if (!fichier.size) throw new FichierRefuse(`${fichier.name} : fichier vide.`);
    if (fichier.size > TAILLE_MAX) throw new FichierRefuse(`${fichier.name} : trop volumineux (50 Mo maximum).`);
    const octets = new Uint8Array(await fichier.arrayBuffer());
    const tete = Array.from(octets.slice(0, 8));
    let brut;
    if (ext === "pdf") {
      if (!String.fromCharCode(...tete).includes("%PDF-")) throw new FichierRefuse(`${fichier.name} : ce n'est pas un vrai PDF.`);
      brut = await lirePdf(octets);
    } else if (ext === "docx" || ext === "xlsx") {
      if (!(tete[0] === 0x50 && tete[1] === 0x4b && tete[2] === 3 && tete[3] === 4)) throw new FichierRefuse(`${fichier.name} : fichier déguisé ou corrompu.`);
      brut = ext === "docx" ? await lireDocx(octets) : await lireXlsx(octets);
    } else {
      if (octets.slice(0, 65536).includes(0)) throw new FichierRefuse(`${fichier.name} : fichier texte invalide.`);
      brut = new TextDecoder("utf-8").decode(octets);
    }
    return { brut, texte: nettoyer(brut) };
  }

  Object.assign(D, { lireFichier, lignesPage, nettoyer, FichierRefuse });
})(typeof window !== "undefined" ? window : globalThis);

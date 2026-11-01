"""Durcissement commun des pages construites (Atelier et Pilotage).

* SRI : chaque bibliothèque du CDN porte son empreinte SHA-384 ; un fichier modifié sur le CDN
  (attaque de la chaîne d'approvisionnement) est REFUSÉ par le navigateur au lieu d'être exécuté.
  Empreintes calculées sur les paquets npm officiels (versions figées, intégrité sha512 du registre).
* CSP (version autonome) : seuls les scripts intégrés dont l'empreinte est connue et le CDN épinglé
  s'exécutent ; aucune connexion sortante (connect-src 'none'), pas de plugin, pas de formulaire externe.
"""
import base64
import hashlib
import re

SRI = {
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js": "sha384-/1qUCSGwTur9vjf/z9lmu/eCUYbpOTgSjmpbMQZ1/CtX2v/WcAIKqRv+U1DUCG6e",
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js": "sha384-SnzOobpRMLXZ52iJvZm/C0fYw0OQemTXzTjIsdsfMcrCtCEe9qgzxTd3RSklO5x2",
    "https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js": "sha384-Pqp51FUN2/qzfxZxBCtF0stpc9ONI6MYZpVqmo8m20SoaQCzf+arZvACkLkirlPz",
    "https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js": "sha384-+mbV2IY1Zk/X1p/nWllGySJSUN8uMs+gUAN10Or95UBH0fpj6GfKgPmgC5EXieXG",
    "https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js": "sha384-4xaIisuLEy2lo2HkB2C4rEf7v8jbTb2kuogX6TkuEt9feTWKBSFSOzsqNNbV+sKh",
    "https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js": "sha384-Cck14aA9cifjYolcnjebXRfWGkz5ltHMBiG4px/j8GS+xQcb7OhNQWZYyWjQ+UwQ",
}
ALERTE = ("document.body.insertAdjacentHTML('afterbegin','<p style=background:#9B1C1C;color:#fff;padding:12px>"
          "Une bibliothèque n’a pas pu être chargée ou a été refusée (contrôle d’intégrité). Vérifiez votre connexion ; "
          "si le message persiste, n’utilisez pas cette page et contactez le support.</p>')")


def balise(url: str) -> str:
    if url not in SRI:
        raise ValueError(f"Bibliothèque sans empreinte d'intégrité : {url}")
    return f'<script src="{url}" integrity="{SRI[url]}" crossorigin="anonymous" referrerpolicy="no-referrer" onerror="{ALERTE}"></script>'


def csp(html: str) -> str:
    """Politique de sécurité pour la version autonome : empreintes des scripts intégrés présents dans la page."""
    blocs = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    empreintes = " ".join(f"'sha256-{base64.b64encode(hashlib.sha256(b.encode('utf-8')).digest()).decode()}'" for b in blocs)
    # les gestionnaires onerror des balises CDN sont des attributs : autorisés par leur empreinte (unsafe-hashes)
    alerte = f"'sha256-{base64.b64encode(hashlib.sha256(ALERTE.encode('utf-8')).digest()).decode()}'"
    return ("default-src 'none'; "
            f"script-src {empreintes} 'unsafe-hashes' {alerte} https://cdn.jsdelivr.net; "
            "style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; "
            "img-src data: blob:; connect-src 'none'; worker-src blob:; object-src 'none'; base-uri 'none'; form-action 'none'")

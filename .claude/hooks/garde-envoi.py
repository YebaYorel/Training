#!/usr/bin/env python3
"""Garde-fou d'envoi (PreToolUse) — règles permanentes de prospection d'Aurélien LUMEKA.

Bloque (exit 2, motif lu par Claude) un outil d'ENVOI ou de CRÉATION de message quand :
  • il mentionne l'adresse personnelle aurelienlumeka@gmail.com (règle 2 : seule yebaformations@gmail.com envoie) ;
  • un destinataire figure dans la liste STOP de l'Espace YEBA (site/espace/.prospection/etat.json).
Les envois Gmail directs sont, eux, interdits par .claude/settings.json (règle 3 : Aurélien envoie lui-même).
Conçu pour ne JAMAIS bloquer la session : toute erreur interne laisse passer (exit 0), sans bruit.
"""
import json
import os
import re
import sys

PERSO = "aurelienlumeka@gmail.com"
ECRITURE = re.compile(r"(send|reply|forward|draft|campaign|template|sms|automation|workflow)", re.I)


def main() -> int:
    try:
        evt = json.load(sys.stdin)
    except Exception:
        return 0
    outil = evt.get("tool_name", "")
    if not ECRITURE.search(outil) or re.search(r"(get|list|search|read|preview|schema|catalog|guide)_?", outil.split("__")[-1].split("_")[0], re.I):
        return 0
    texte = json.dumps(evt.get("tool_input", {}), ensure_ascii=False).lower()
    if PERSO in texte:
        print(f"Règle 2 (Aurélien) : jamais d'envoi depuis ou vers l'adresse personnelle {PERSO}. "
              "Utiliser uniquement yebaformations@gmail.com.", file=sys.stderr)
        return 2
    racine = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        with open(os.path.join(racine, "site/espace/.prospection/etat.json"), encoding="utf-8") as f:
            etat = json.load(f) or {}
    except Exception:
        return 0
    adresses = set(re.findall(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", texte))
    for o in etat.get("oppositions", []):
        e, d = o.get("email", ""), o.get("domaine")
        touche = [a for a in adresses if a == e or (d and a.endswith("@" + d))]
        if touche:
            print(f"STOP : {', '.join(touche)} a demandé à ne plus être contacté (liste STOP de l'Espace YEBA). Envoi refusé.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Génère 3 réels animés 9:16 (MP4, 15 s, sans son : ajoutez un son tendance dans Instagram).

Rendu image par image (25 i/s) → rendu déterministe, puis encodage H.264 via ffmpeg.
Usage : python src/reels.py   (pip install playwright imageio-ffmpeg)
"""
import shutil
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

from generate import BASE_CSS, BUILD, CHROMIUM, GOLD, INK, NAVY, OUT, fr, net_svg

FPS = 25
W, H = 1080, 1920


def big(t, size=120, color=None):
    c = f"color:{color};" if color else ""
    return f'<div class="l" style="font-weight:900;font-size:{size}px;line-height:1.08;{c}">{fr(t)}</div>'


def txt(t, size=56):
    return f'<div class="l" style="font-weight:700;font-size:{size}px;line-height:1.3">{fr(t)}</div>'


def num(n):
    return (f'<div class="l" style="width:170px;height:170px;border-radius:50%;background:{GOLD};color:{INK};'
            f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:110px">{n}</div>')


def cta(label):
    return (f'<div class="l"><span style="display:inline-block;background:{GOLD};color:{INK};font-weight:900;'
            f'font-size:64px;padding:26px 50px;border-radius:80px">{fr(label)}</span></div>'
            f'<div class="l" style="display:flex;align-items:center;gap:24px;font-weight:800;font-size:44px">'
            f'<img src="../assets/mark_white.png" style="height:80px">YEBA IA</div>')


def src(t):
    return f'<div class="l" style="font-weight:600;font-size:30px;opacity:.8">{fr(t)}</div>'


G = f"color:{GOLD}"
REELS = {
    "reel01_chatgpt": [
        (2.2, big("STOP&nbsp;✋", 160, GOLD) + big("Vous avez collé quoi dans ChatGPT ce matin ?", 96)),
        (3.0, num(1) + big("Un fichier clients") + txt(f'= données personnelles<br><b style="{G}">→ RGPD</b>')),
        (3.0, num(2) + big("Un contrat confidentiel") + txt(f'= <b style="{G}">secret des affaires</b> exposé')),
        (3.0, num(3) + big("Une réponse copiée sans vérifier") + txt(f'L\'IA peut <b style="{G}">inventer</b> (« hallucination »)')),
        (3.8, big("La solution ?", 110, GOLD) + big("Former vos équipes.", 110) + cta("Commentez « IA » ⬇")),
    ],
    "reel02_ia_act": [
        (2.4, big("Votre entreprise utilise l'IA ?", 104) + big("L'IA Act vous concerne.", 104, GOLD)),
        (2.8, big("1er août 2024", 130, GOLD) + txt("Entrée en vigueur du règlement européen sur l'IA")),
        (3.2, big("2 février 2025", 130, GOLD) + txt("Pratiques interdites<br>+ <b>maîtrise de l'IA</b> du personnel (art. 4)")),
        (3.2, big("2 août 2026", 130, GOLD) + txt("La majorité des règles s'applique, dont la <b>transparence</b> des contenus IA (art. 50)")),
        (3.4, big("Vous êtes prêt ?", 110) + cta("DM « IA ACT »") + src("Source : Règlement (UE) 2024/1689, art. 113")),
    ],
    "reel03_phishing": [
        (2.4, big("Ce mail vient de votre banque ?", 104) + big("3 indices en 10 secondes.", 90, GOLD)),
        (3.0, num(1) + big("L'urgence") + txt("« Votre compte sera bloqué sous 24 h »")),
        (3.0, num(2) + big("L'expéditeur") + txt(f'service@banque-<b style="{G}">securite-fr.co</b><br>≠ votre banque')),
        (3.0, num(3) + big("Le lien") + txt("Jamais d'identifiants via un lien reçu par mail.")),
        (3.6, big("Un doute ?", 110, GOLD) + txt("17cyber.gouv.fr · cybermalveillance.gouv.fr") + cta("DM « CYBER »")),
    ],
}

JS = """
const E=t=>1-Math.pow(1-Math.min(Math.max(t,0),1),3);
window.renderAt=(t)=>{
  let s=0;
  document.querySelectorAll('.scene').forEach(sc=>{
    const d=+sc.dataset.d, lt=t-s; s+=d;
    const on=lt>=0&&lt<d; sc.style.display=on?'flex':'none'; if(!on)return;
    const out=E((lt-(d-0.3))/0.3);
    sc.querySelectorAll('.l').forEach((el,i)=>{const p=E((lt-i*0.18)/0.45);
      el.style.opacity=p*(1-out); el.style.transform=`translateY(${(1-p)*60-out*40}px)`;});
  });
  document.getElementById('bar').style.width=(t/TOTAL*100)+'%';
  document.getElementById('net').style.transform=`translate(${-t*6}px,${-t*10}px) scale(1.08)`;
};
"""


def html(scenes):
    total = sum(d for d, _ in scenes)
    sc = "".join(f'<div class="scene" data-d="{d}" style="position:absolute;left:84px;right:170px;top:260px;'
                 f'bottom:420px;flex-direction:column;justify-content:center;gap:44px">{h}</div>' for d, h in scenes)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>'
            f'<div id="c" class="c navy" style="width:{W}px;height:{H}px">'
            f'<div id="net" style="position:absolute;inset:0">{net_svg(W, H, GOLD, .14, 77, 34)}</div>'
            f'<div style="position:absolute;top:0;left:0;height:12px;background:{GOLD};z-index:2" id="bar"></div>'
            f'{sc}</div><script>const TOTAL={total};{JS}</script></body></html>'), total


def main():
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    (OUT / "reels").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROMIUM)
        pg = b.new_page(viewport={"width": W, "height": H})
        for name, scenes in REELS.items():
            doc, total = html(scenes)
            f = BUILD / f"{name}.html"
            f.write_text(doc, encoding="utf-8")
            pg.goto(f.as_uri())
            pg.evaluate("document.fonts.ready")
            frames = BUILD / name
            shutil.rmtree(frames, ignore_errors=True)
            frames.mkdir()
            for i in range(int(total * FPS)):
                pg.evaluate(f"renderAt({i / FPS})")
                pg.screenshot(path=str(frames / f"{i:04d}.jpg"), type="jpeg", quality=92)
            out = OUT / "reels" / f"{name}.mp4"
            subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.jpg"),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
                            str(out)], check=True)
            shutil.rmtree(frames)
            print("✓", out.relative_to(OUT.parent), f"{total:.1f}s")
        b.close()


if __name__ == "__main__":
    main()

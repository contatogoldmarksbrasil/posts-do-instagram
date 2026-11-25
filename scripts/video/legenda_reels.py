"""Gera legenda estilo Reels (.ass) a partir do JSON de palavras.

Uso: python3 scripts/video/legenda_reels.py palavras.json legenda.ass [cortes]
  cortes (opcional): trechos removidos, em segundos do vídeo bruto, ex. "3.9-6.0,12-13.5".
  Os tempos das palavras são deslocados para continuar sincronizados após os cortes.

Estilo: 3 palavras por vez, em maiúsculas, palavra falada em destaque.
Gravar no vídeo com ffmpeg: -vf "ass=legenda.ass" (1080x1920).
"""
import json
import sys

FONTE = "DejaVu Sans"   # trocar pela fonte do cliente (ex. Poppins)
TAMANHO = 78
COR_DESTAQUE = "&H00D7FF&"  # amarelo (formato BGR do ASS)
POR_VEZ = 3
MARGEM_BAIXO = 520  # fica acima da área de botões do Reels

palavras = json.load(open(sys.argv[1], encoding="utf-8"))
saida = sys.argv[2]
cortes = []
if len(sys.argv) > 3 and sys.argv[3]:
    cortes = [tuple(map(float, c.split("-"))) for c in sys.argv[3].split(",")]


def ajusta(x):
    for a, b in cortes:
        if x >= b:
            x -= b - a
        elif x > a:
            x -= x - a
    return x


def ts(x):
    x = max(ajusta(x), 0)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def cortada(w):
    return any(a <= w["s"] and w["e"] <= b for a, b in cortes)


palavras = [w for w in palavras if not cortada(w)]

cab = f"""[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: L,{FONTE},{TAMANHO},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,6,0,2,80,80,{MARGEM_BAIXO},1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
linhas = []
for i in range(0, len(palavras), POR_VEZ):
    g = palavras[i:i + POR_VEZ]
    for j, w in enumerate(g):
        txt = " ".join(
            f"{{\\c{COR_DESTAQUE}}}{x['w'].upper()}{{\\c&HFFFFFF&}}" if k == j else x["w"].upper()
            for k, x in enumerate(g)
        )
        fim = g[j + 1]["s"] if j + 1 < len(g) else w["e"]
        linhas.append(f"Dialogue: 0,{ts(w['s'])},{ts(fim)},L,,0,0,0,,{txt}")

with open(saida, "w", encoding="utf-8") as f:
    f.write(cab + "\n".join(linhas) + "\n")
print(f"-> {saida} ({len(linhas)} eventos)")

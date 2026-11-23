#!/usr/bin/env python3
"""Gera a arte da Âncora Consórcios (JPEG 1080x1350).

Uso:
  python3 scripts/arte_ancora.py --tipo moto --carta 25000 --prazo 70 --taxa 0.18 \
      --titulo "Sua moto nova|cabe no bolso" --saida posts/ancora/AAAA-MM-DD.jpg
Tipos com ilustração: moto, carro, apartamento, terreno, carta.
A parcela é calculada aqui: ceil(carta * (1 + taxa) / prazo).
"""
import argparse
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NAVY = (11, 37, 69)
NAVY2 = (19, 64, 116)
CYAN = (56, 189, 248)
WHITE = (255, 255, 255)
SOFT = (191, 219, 254)
F = "/usr/share/fonts/opentype/inter/"
AVISO = ("Valores ilustrativos, sujeitos às condições do grupo e à aprovação. "
         "Consórcio não é financiamento: contemplação por sorteio ou lance.")


def font(peso, tam):
    return ImageFont.truetype(F + f"Inter-{peso}.otf", tam)


def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def centro(d, y, txt, fnt, cor):
    w = d.textlength(txt, font=fnt)
    d.text(((W - w) / 2, y), txt, font=fnt, fill=cor)


def ancora(d, cx, cy, s, cor):
    lw = max(3, int(s * 0.09))
    d.ellipse([cx - s * .16, cy - s * .62, cx + s * .16, cy - s * .30], outline=cor, width=lw)
    d.line([cx, cy - s * .30, cx, cy + s * .55], fill=cor, width=lw)
    d.line([cx - s * .32, cy - s * .12, cx + s * .32, cy - s * .12], fill=cor, width=lw)
    d.arc([cx - s * .55, cy - s * .05, cx + s * .55, cy + s * .60], 20, 160, fill=cor, width=lw)
    for sx in (-1, 1):
        x = cx + sx * s * .52
        d.polygon([(x, cy + s * .16), (x - sx * s * .02, cy + s * .34), (x + sx * s * .13, cy + s * .30)], fill=cor)


def moto(d, cx, cy, s):
    lw = int(s * .035)
    for x in (cx - s * .62, cx + s * .62):
        d.ellipse([x - s * .32, cy - s * .32, x + s * .32, cy + s * .32], outline=WHITE, width=int(s * .07))
        d.ellipse([x - s * .07, cy - s * .07, x + s * .07, cy + s * .07], fill=CYAN)
    d.line([(cx - s * .62, cy), (cx - s * .25, cy - s * .40)], fill=SOFT, width=int(s * .06))
    d.rounded_rectangle([cx - s * .28, cy - s * .30, cx + s * .18, cy + s * .05], radius=int(s * .06), fill=SOFT)
    for i in range(3):
        y = cy - s * .22 + i * s * .09
        d.line([(cx - s * .22, y), (cx + s * .12, y)], fill=NAVY2, width=int(s * .025))
    d.line([(cx - s * .20, cy + s * .05), (cx - s * .62, cy + s * .12)], fill=WHITE, width=int(s * .05))
    d.polygon([(cx - s * .62, cy - s * .30), (cx - s * .30, cy - s * .48), (cx + s * .34, cy - s * .48),
               (cx + s * .26, cy - s * .30)], fill=CYAN)
    d.polygon([(cx - s * .10, cy - s * .48), (cx + s * .32, cy - s * .48), (cx + s * .24, cy - s * .70),
               (cx - s * .02, cy - s * .70)], fill=CYAN)
    d.rounded_rectangle([cx - s * .75, cy - s * .58, cx - s * .12, cy - s * .44], radius=int(s * .06), fill=WHITE)
    d.line([(cx + s * .30, cy - s * .38), (cx + s * .62, cy)], fill=WHITE, width=lw)
    d.line([(cx + s * .30, cy - s * .62), (cx + s * .45, cy - s * .80)], fill=WHITE, width=lw)
    d.line([(cx + s * .38, cy - s * .80), (cx + s * .58, cy - s * .80)], fill=WHITE, width=lw)
    d.ellipse([cx + s * .40, cy - s * .58, cx + s * .54, cy - s * .44], fill=(253, 224, 71))


def carro(d, cx, cy, s):
    d.rounded_rectangle([cx - s, cy - s * .35, cx + s, cy + s * .15], radius=int(s * .15), fill=CYAN)
    d.polygon([(cx - s * .55, cy - s * .35), (cx - s * .30, cy - s * .75), (cx + s * .35, cy - s * .75),
               (cx + s * .62, cy - s * .35)], fill=CYAN)
    d.polygon([(cx - s * .42, cy - s * .38), (cx - s * .25, cy - s * .66), (cx + s * .02, cy - s * .66),
               (cx + s * .02, cy - s * .38)], fill=NAVY2)
    d.polygon([(cx + s * .10, cy - s * .38), (cx + s * .10, cy - s * .66), (cx + s * .32, cy - s * .66),
               (cx + s * .50, cy - s * .38)], fill=NAVY2)
    for x in (cx - s * .58, cx + s * .58):
        d.ellipse([x - s * .25, cy - s * .05, x + s * .25, cy + s * .45], fill=WHITE)
        d.ellipse([x - s * .11, cy + s * .09, x + s * .11, cy + s * .31], fill=NAVY)


def predio(d, cx, cy, s):
    d.rectangle([cx - s * .45, cy - s * .9, cx + s * .15, cy + s * .4], fill=CYAN)
    d.rectangle([cx + s * .15, cy - s * .5, cx + s * .6, cy + s * .4], fill=SOFT)
    for i in range(5):
        for j in range(3):
            x = cx - s * .37 + j * s * .17
            y = cy - s * .80 + i * s * .22
            d.rectangle([x, y, x + s * .1, y + s * .12], fill=NAVY2)
    for i in range(3):
        for j in range(2):
            x = cx + s * .24 + j * s * .18
            y = cy - s * .40 + i * s * .22
            d.rectangle([x, y, x + s * .1, y + s * .12], fill=NAVY2)
    d.line([(cx - s * .9, cy + s * .4), (cx + s * .9, cy + s * .4)], fill=WHITE, width=int(s * .03))


def terreno(d, cx, cy, s):
    d.polygon([(cx - s, cy + s * .4), (cx - s * .4, cy - s * .2), (cx + s, cy - s * .2), (cx + s * .4, cy + s * .4)],
              fill=(34, 197, 94))
    d.polygon([(cx - s, cy + s * .4), (cx - s * .4, cy - s * .2), (cx + s, cy - s * .2), (cx + s * .4, cy + s * .4)],
              outline=WHITE, width=int(s * .03))
    for x, y in ((cx - s * .55, cy + s * .1), (cx + s * .15, cy - s * .05)):
        d.line([(x, y), (x, y - s * .6)], fill=WHITE, width=int(s * .03))
        d.polygon([(x, y - s * .6), (x + s * .35, y - s * .48), (x, y - s * .36)], fill=CYAN)


def carta(d, cx, cy, s):
    d.rounded_rectangle([cx - s * .9, cy - s * .55, cx + s * .9, cy + s * .55], radius=int(s * .12), fill=CYAN)
    d.rounded_rectangle([cx - s * .7, cy - s * .30, cx - s * .35, cy - s * .05], radius=int(s * .05), fill=(253, 224, 71))
    d.text((cx - s * .7, cy + s * .12), "CARTA DE CRÉDITO", font=font("Bold", int(s * .14)), fill=NAVY)


ILUS = {"moto": moto, "carro": carro, "apartamento": predio, "terreno": terreno, "carta": carta}


def gerar(tipo, valor, prazo, taxa, titulo, saida, rotulo=None):
    parcela = math.ceil(valor * (1 + taxa) / prazo)
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):  # degradê vertical
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(NAVY[i] + (NAVY2[i] - NAVY[i]) * t) for i in range(3)))
    d.ellipse([W - 420, -220, W + 220, 420], fill=(23, 74, 130))

    ancora(d, 100, 112, 70, CYAN)
    d.text((150, 78), "ÂNCORA", font=font("ExtraBold", 44), fill=WHITE)
    d.text((152, 128), "CONSÓRCIOS", font=font("SemiBold", 22), fill=SOFT)

    y = 230
    for linha in titulo.split("|"):
        centro(d, y, linha, font("ExtraBold", 76), WHITE)
        y += 92

    ILUS[tipo](d, W / 2, 690, 230)

    cx0, cy0, cx1, cy1 = 110, 900, W - 110, 1160
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=36, fill=WHITE)
    centro(d, cy0 + 28, (rotulo or "CARTA DE CRÉDITO").upper(), font("Bold", 30), NAVY2)
    centro(d, cy0 + 68, brl(valor), font("ExtraBold", 84), NAVY)
    centro(d, cy0 + 172, f"parcelas a partir de {brl(parcela)}/mês em {prazo}x", font("SemiBold", 34), NAVY2)

    bw = 460
    d.rounded_rectangle([(W - bw) / 2, 1188, (W + bw) / 2, 1252], radius=32, fill=CYAN)
    centro(d, 1199, "Chame no direct", font("Bold", 34), NAVY)

    f = font("Regular", 20)
    meio = AVISO.index("Consórcio")
    centro(d, 1278, AVISO[:meio].strip(), f, SOFT)
    centro(d, 1304, AVISO[meio:], f, SOFT)

    img.save(saida, "JPEG", quality=92, optimize=True)
    return parcela


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--tipo", choices=ILUS, required=True)
    a.add_argument("--carta", type=float, required=True)
    a.add_argument("--prazo", type=int, required=True)
    a.add_argument("--taxa", type=float, required=True)
    a.add_argument("--titulo", required=True, help="linhas separadas por |")
    a.add_argument("--rotulo", default=None)
    a.add_argument("--saida", required=True)
    x = a.parse_args()
    p = gerar(x.tipo, x.carta, x.prazo, x.taxa, x.titulo, x.saida, x.rotulo)
    print(f"parcela R$ {p} | arquivo {x.saida}")

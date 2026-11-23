#!/usr/bin/env python3
"""Diz se hoje (America/Sao_Paulo) é dia de post.
Posta de segunda a sexta, em feriado nacional e em data do comércio.
Uso: python3 scripts/deve_postar.py [AAAA-MM-DD]
Saída: "POSTAR <motivo>" (exit 0) ou "NAO_POSTAR <motivo>" (exit 1)."""
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def pascoa(a):
    b, c = divmod(a, 100)
    d, e = divmod(b, 4)
    g = (8 * b + 13) // 25
    h = (19 * (a % 19) + b - d - g + 15) % 30
    j, k = divmod(c, 4)
    m = (a % 19 + 11 * h) // 319
    r = (2 * e + 2 * j - k - h + m + 32) % 7
    n = (h - m + r + 90) // 25
    p = (h - m + r + n + 19) % 32
    return date(a, n, p)


def nth_weekday(a, mes, wd, n):
    d = date(a, mes, 1)
    d += timedelta(days=(wd - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def datas(a):
    p = pascoa(a)
    bf = nth_weekday(a, 11, 3, 4) + timedelta(days=1)  # sexta após 4ª quinta
    return {
        date(a, 1, 1): "Ano Novo",
        p - timedelta(days=48): "Carnaval (segunda)",
        p - timedelta(days=47): "Carnaval (terça)",
        p - timedelta(days=2): "Sexta-feira Santa",
        date(a, 4, 21): "Tiradentes",
        date(a, 5, 1): "Dia do Trabalho",
        p + timedelta(days=60): "Corpus Christi",
        date(a, 9, 7): "Independência",
        date(a, 10, 12): "Nossa Senhora Aparecida / Dia das Crianças",
        date(a, 11, 2): "Finados",
        date(a, 11, 15): "Proclamação da República",
        date(a, 11, 20): "Consciência Negra",
        date(a, 12, 25): "Natal",
        date(a, 3, 15): "Dia do Consumidor",
        nth_weekday(a, 5, 6, 2): "Dia das Mães",
        date(a, 6, 12): "Dia dos Namorados",
        nth_weekday(a, 8, 6, 2): "Dia dos Pais",
        date(a, 9, 15): "Dia do Cliente",
        date(a, 10, 5): "Dia do Empreendedor",
        bf: "Black Friday",
        bf + timedelta(days=3): "Cyber Monday",
    }


hoje = (date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1
        else datetime.now(ZoneInfo("America/Sao_Paulo")).date())
especial = datas(hoje.year).get(hoje)
if especial:
    print(f"POSTAR {hoje} data especial: {especial}")
elif hoje.weekday() < 5:
    print(f"POSTAR {hoje} dia útil")
else:
    print(f"NAO_POSTAR {hoje} fim de semana sem data especial")
    sys.exit(1)

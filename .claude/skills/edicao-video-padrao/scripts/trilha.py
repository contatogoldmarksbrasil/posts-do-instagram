#!/usr/bin/env python3
"""Gera a trilha (música + efeitos) sintetizada, sincronizada com a timeline.

Uso:  python3 trilha.py <timeline.json> <saida.wav> <vibe>
  vibe: kinetic | alerta | reel | cinema | premium
    kinetic  (estilo 1) : pad + batida média + whoosh/boom nas viradas
    alerta   (estilo 2) : pad + batida forte + riser + stabs de alerta + glitch
    reel     (estilo 3) : batida puxada + hats + riser + stabs (#1/#2/#3)
    cinema   (estilo 4) : pad cinematográfico + sub + whoosh de voo + impactos
    premium  (estilo 5) : pad quente maior + sub + ar + sininhos (suave)

Depois, misture com a voz no ffmpeg (ver montar.sh): sidechaincompress + loudnorm I=-14.
Só numpy (já disponível). Saída: WAV estéreo 44.1k.
"""
import json
import sys
import wave

import numpy as np

tl = json.load(open(sys.argv[1]))
out = sys.argv[2]
vibe = sys.argv[3] if len(sys.argv) > 3 else "cinema"
T = tl["total"]; sr = 44100; N = int(T * sr); t = np.arange(N) / sr
rng = np.random.default_rng(7)
sc = tl["scenes"]; starts = [s["start"] for s in sc]
CEN = [(s["start"] + s["end"]) / 2 for s in sc]
bounds = [0.0] + [(sc[i]["end"] + sc[i + 1]["start"]) / 2 for i in range(len(sc) - 1)] + [T]


def put(buf, at, sig):
    i = int(at * sr); e = min(N, i + len(sig))
    if e > i:
        buf[i:e] += sig[:e - i]


def pad_chord(freqs, lfo=0.09, amt=0.16):
    p = np.zeros(N)
    for f, a in freqs:
        p += a * (0.55 + 0.45 * np.sin(2 * np.pi * lfo * t)) * np.sin(2 * np.pi * f * t + 0.2 * np.sin(2 * np.pi * 0.4 * t))
    return p * amt


def beat(per, kickdecay=17, amp=0.55, hats=False):
    b = np.zeros(N); on = 0.0
    while on < T - 0.05:
        L = int(0.42 * sr); env = np.exp(-np.arange(L) / sr * kickdecay)
        k = np.sin(2 * np.pi * (55 * np.exp(-np.arange(L) / sr * 9)) * np.arange(L) / sr) * env
        cl = rng.standard_normal(min(340, L)) * np.exp(-np.arange(min(340, L)) / sr * 130) * 0.5
        k[:len(cl)] += cl; put(b, on, k * amp)
        if hats:
            Lh = int(0.07 * sr); put(b, on + per / 2, rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / sr * 60) * 0.12)
        on += per
    return b


def risers_booms(whoosh_before=0.6, riser=True):
    fx = np.zeros(N)
    for bnd in bounds:
        s = max(0, bnd - whoosh_before); L = int((whoosh_before + 0.12) * sr)
        if L > 0 and riser:
            w = np.convolve(rng.standard_normal(L), np.ones(5) / 5, mode='same')
            tone = np.sin(2 * np.pi * np.linspace(200, 900, L) * np.arange(L) / sr) * 0.4
            put(fx, s, (0.17 * w + 0.09 * tone) * (np.linspace(0, 1, L) ** 2.2))
        L2 = int(0.4 * sr)
        bo = np.sin(2 * np.pi * (62 * np.exp(-np.arange(L2) / sr * 7)) * np.arange(L2) / sr) * np.exp(-np.arange(L2) / sr * 9)
        put(fx, bnd, 0.4 * bo)
    return fx


def stabs(idxs, f1=660, f2=990):
    fx = np.zeros(N)
    for idx in idxs:
        if idx >= len(starts):
            continue
        L = int(0.45 * sr)
        put(fx, starts[idx], (np.sin(2 * np.pi * f1 * np.arange(L) / sr) + np.sin(2 * np.pi * f2 * np.arange(L) / sr)) * np.exp(-np.arange(L) / sr * 8) * 0.16)
    return fx


if vibe == "kinetic":
    mix = pad_chord([(55, .5), (82.41, .4), (110, .35), (164.81, .25), (220, .15)]) + beat(0.706, amp=0.5) + risers_booms(0.5)
elif vibe == "alerta":
    mix = pad_chord([(55, .45), (65.4, .3), (110, .3), (146.8, .2), (196, .13)]) + beat(0.6, hats=True) + risers_booms(0.5) + stabs([0, 3, 6])
elif vibe == "reel":
    mix = pad_chord([(55, .45), (65.4, .3), (110, .3), (146.8, .2), (196, .13)]) + beat(0.55, hats=True) + risers_booms(0.6) + stabs([0, 1, 3, 5, 7])
elif vibe == "cinema":
    sub = 0.12 * np.sin(2 * np.pi * 41 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t))
    fx = np.zeros(N)
    for w in [(CEN[i] + CEN[i + 1]) / 2 for i in range(len(CEN) - 1)]:
        L = int(0.75 * sr); s = max(0, w - 0.5)
        env = np.exp(-((np.arange(L) - L * 0.6) / (L * 0.3)) ** 2)
        put(fx, s, (0.2 * np.convolve(rng.standard_normal(L), np.ones(4) / 4, mode='same') + 0.08 * np.sin(2 * np.pi * np.linspace(300, 1400, L) * np.arange(L) / sr)) * env)
    for cc in CEN:
        L = int(0.5 * sr); put(fx, cc - 0.05, 0.32 * np.sin(2 * np.pi * (58 * np.exp(-np.arange(L) / sr * 6)) * np.arange(L) / sr) * np.exp(-np.arange(L) / sr * 7))
    mix = pad_chord([(55, .5), (82.41, .34), (110, .34), (164.81, .24), (220, .16), (329.6, .08)], lfo=0.06, amt=0.17) + sub + fx
elif vibe == "premium":
    sub = 0.08 * np.sin(2 * np.pi * 65.4 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * t))
    air = rng.standard_normal(N); air = (air - np.convolve(air, np.ones(120) / 120, mode='same')) * 0.012
    bells = np.zeros(N); notes = [523.25, 659.25, 784.0, 587.33, 659.25, 784.0, 880.0, 698.46, 784.0, 659.25, 523.25]
    for idx, s0 in enumerate(starts):
        f = notes[idx % len(notes)]; L = int(1.6 * sr); env = np.exp(-np.arange(L) / sr * 2.6)
        put(bells, max(0, s0 - 0.15), 0.09 * (np.sin(2 * np.pi * f * np.arange(L) / sr) + 0.5 * np.sin(2 * np.pi * 2 * f * np.arange(L) / sr)) * env)
    mix = pad_chord([(65.4, .4), (130.8, .3), (196, .26), (261.6, .2), (329.6, .16), (392, .1)], lfo=0.07, amt=0.16) + sub + air + bells
else:
    sys.exit("vibe inválida: " + vibe)

mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.55 if vibe not in ("premium",) else 0.5
st = np.stack([mix, np.roll(mix, 70) * 0.97], 1)
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.int16(np.clip(st, -1, 1) * 32767).tobytes())
print(f"{out} ok ({vibe}, {T:.2f}s)")

#!/usr/bin/env python3
"""Gera a narração (voz pt-BR com Piper) e a linha do tempo de um roteiro.

Uso:  python3 narrar.py <roteiro.txt> <pasta_saida> [gap] [lead] [tail]
  roteiro.txt : uma FALA por linha (vira uma "cena").
  pasta_saida : onde ficam voz/l{i}.wav, voz_full.wav e timeline.json.

Variáveis de ambiente:
  PIPER_MODEL : caminho do modelo .onnx (padrão /tmp/piper/pt_BR-faber-medium.onnx).

Pré-requisitos (instalar na sessão, NÃO num setup script do ambiente):
  pip install piper-tts
  mkdir -p /tmp/piper && baixar de huggingface:
    rhasspy/piper-voices/.../pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx(.json)
  (use HF_HUB_DISABLE_XET=1 se precisar; hosts do HuggingFace já liberados no ambiente)
"""
import json
import os
import subprocess
import sys

roteiro, outdir = sys.argv[1], sys.argv[2]
gap = float(sys.argv[3]) if len(sys.argv) > 3 else 0.32
lead = float(sys.argv[4]) if len(sys.argv) > 4 else 0.45
tail = float(sys.argv[5]) if len(sys.argv) > 5 else 0.75
MODEL = os.environ.get("PIPER_MODEL", "/tmp/piper/pt_BR-faber-medium.onnx")
SR = 22050
voz = os.path.join(outdir, "voz")
os.makedirs(voz, exist_ok=True)

lines = [l.rstrip("\n") for l in open(roteiro, encoding="utf-8") if l.strip()]
for i, ln in enumerate(lines, 1):
    subprocess.run(["piper", "-m", MODEL, "-f", os.path.join(voz, f"l{i}.wav")],
                   input=ln.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def sil(d, p):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"anullsrc=r={SR}:cl=mono", "-t", f"{d:.3f}", p], check=True)


sil(lead, f"{outdir}/_lead.wav"); sil(gap, f"{outdir}/_gap.wav"); sil(tail, f"{outdir}/_tail.wav")
seq = [f"{outdir}/_lead.wav"]; t = lead; scenes = []
for i, ln in enumerate(lines, 1):
    d = dur(os.path.join(voz, f"l{i}.wav"))
    scenes.append({"i": i, "start": round(t, 3), "end": round(t + d, 3), "text": ln})
    seq.append(os.path.join(voz, f"l{i}.wav")); t += d
    if i < len(lines):
        seq.append(f"{outdir}/_gap.wav"); t += gap
seq.append(f"{outdir}/_tail.wav"); t += tail
with open(f"{outdir}/concat.txt", "w") as f:
    for s in seq:
        f.write(f"file '{os.path.abspath(s)}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i",
                f"{outdir}/concat.txt", "-ar", "44100", f"{outdir}/voz_full.wav"], check=True)
total = dur(f"{outdir}/voz_full.wav")
json.dump({"total": round(total, 3), "scenes": scenes, "fps": 30},
          open(f"{outdir}/timeline.json", "w"), ensure_ascii=False)
print(f"total: {total:.2f}s | {len(scenes)} cenas -> {outdir}/timeline.json, {outdir}/voz_full.wav")
for s in scenes:
    print(f"  {s['i']}: {s['start']:.2f}-{s['end']:.2f}  {s['text'][:50]}")

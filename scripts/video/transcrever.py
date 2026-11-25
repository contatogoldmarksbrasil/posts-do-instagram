"""Transcreve um vídeo em português com o tempo de cada palavra.

Uso: python3 scripts/video/transcrever.py video.mp4 [saida.json]

Gera um JSON com [{"w": palavra, "s": inicio, "e": fim}, ...] e imprime as frases.
O áudio é extraído com ffmpeg antes (o PyAV instalado não aceita o vídeo direto).
"""
import json
import os
import subprocess
import sys

import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from faster_whisper import WhisperModel  # noqa: E402

video = sys.argv[1]
saida = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(video)[0] + "_palavras.json"

raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
    check=True, capture_output=True,
).stdout
audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768

modelo = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = modelo.transcribe(audio, language="pt", word_timestamps=True)

palavras = []
for s in segs:
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text.strip()}")
    palavras += [{"w": w.word.strip(), "s": w.start, "e": w.end} for w in s.words]

with open(saida, "w", encoding="utf-8") as f:
    json.dump(palavras, f, ensure_ascii=False, indent=1)
print(f"-> {saida}")

#!/bin/bash
# Junta quadros + narração + trilha num MP4 9:16 pronto pro Instagram.
# Uso: bash montar.sh <pasta_frames> <voz_full.wav> <music.wav> <saida.mp4>
# A música abaixa sozinha sob a voz (sidechaincompress) e o conjunto vai pra -14 LUFS.
set -e
FRAMES="$1"; VOZ="$2"; MUS="$3"; OUT="$4"
ffmpeg -y -v error -framerate 30 -i "$FRAMES/f%05d.png" -i "$VOZ" -i "$MUS" \
  -filter_complex "[2:a][1:a]sidechaincompress=threshold=0.04:ratio=6:attack=14:release=320[d];[1:a]volume=1.1[vv];[vv][d]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]" \
  -map 0:v -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT" | xargs printf "pronto: %s s -> $OUT\n"

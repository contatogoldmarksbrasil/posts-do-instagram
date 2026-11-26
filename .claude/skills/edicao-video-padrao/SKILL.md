---
name: edicao-video-padrao
description: >-
  Usar ao criar vídeos (Reels/Stories 9:16) para os clientes do usuário (Gold Marks
  Brasil, Âncora Consórcios ou outra marca): vídeos animados de motion graphics, com
  narração em português, legendas/tipografia em movimento, música e efeitos. Tem 5
  estilos prontos (kinético, alerta, reel/ranking, cinema 3D, premium/cards) e o fluxo
  completo para produzir do zero. Combina com a skill posts-instagram-padrao (mesma marca).
---

# Edição de vídeo — padrão Gold Marks / Âncora

Produz vídeos verticais (1080x1920) de **motion graphics com narração**, totalmente montados
aqui (sem ferramenta paga). Pipeline: Piper (voz pt-BR) → HTML animado renderizado quadro a
quadro com Playwright/Chromium → ffmpeg junta com trilha sintetizada.

> Tudo roda nesta sessão. **NUNCA** colocar a instalação num setup script do ambiente — já
> quebrou as tarefas agendadas de postagem. Instalar sob demanda (passo 0).

## Regras da marca (valem acima de tudo)
- **Gold Marks:** preto `#07070A`, dourado `#D9B35A`, branco, fonte Montserrat. Vermelho de
  alerta `#FF5050` só para perigo. Logo em `assets/logo.png` (fundo transparente).
- **Sem telefone/WhatsApp** na arte nem na narração. CTA sempre: **"Fale com um de nossos
  especialistas"**.
- Sem rodapé, sem @, sem site na arte.
- Áudio sempre presente (narração + trilha). Volume final `loudnorm I=-14` (padrão Instagram).
- **Fatos:** não inventar taxas, prazos ou números do INPI. Conferir em gov.br/inpi antes de
  citar; sem confirmação, não citar número. (Ex.: registro vale 10 anos renováveis — ok.)

## Os 5 estilos (detalhe em ESTILOS.md)
| nº | engine (`estilos/`) | vibe (trilha) | quando usar |
|----|---------------------|---------------|-------------|
| 1 | `1-kinetico.html`  | `kinetic` | institucional, tipografia forte, direto |
| 2 | `2-alerta.html`    | `alerta`  | alerta/golpe, urgência (boleto falso, PARE, celular) |
| 3 | `3-reel.html`      | `reel`    | reel viral: raios de velocidade, legenda karaokê, ranking #1/#2/#3 |
| 4 | `4-cinema3d.html`  | `cinema`  | cinematográfico: câmera voando em 3D (warp) pelas frases |
| 5 | `5-premium.html`   | `premium` | premium/aesthetic: cards flutuando, bokeh âmbar, tipografia elegante |

**Varie o estilo entre vídeos.** Cada engine tem `window.seek(t)` e `window.setTimeline(tl)`.

## Fluxo para criar um vídeo

**0. Setup (uma vez por sessão):**
```bash
pip install -q piper-tts playwright >/dev/null   # ffmpeg e numpy já existem; Chromium já instalado
mkdir -p /tmp/piper && cd /tmp/piper
for f in pt_BR-faber-medium.onnx pt_BR-faber-medium.onnx.json; do
  curl -sL -o $f "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/$f"
done
```
(hosts do HuggingFace já liberados no ambiente; se o download falhar, use `HF_HUB_DISABLE_XET=1`.)

**1. Escolha o estilo** (tabela acima) conforme o objetivo do vídeo.

**2. Escreva o roteiro** `roteiro.txt`, **uma fala por linha** = uma cena. ~30–40s = ~11 falas
curtas. Siga as regras da marca. Gancho forte na 1ª fala; feche com o nome da marca e o CTA.

**3. Monte a pasta de trabalho** (o HTML referencia `logo.png` ao lado dele):
```bash
W=/tmp/.../trabalho; mkdir -p $W; cd $W
cp .../skills/edicao-video-padrao/estilos/3-reel.html cena.html
cp .../skills/edicao-video-padrao/estilos/logo.png .
```

**4. Narração + timeline:**
```bash
python3 .../scripts/narrar.py roteiro.txt $W           # gera voz_full.wav e timeline.json
```

**5. Ajuste o engine ao roteiro (IMPORTANTE).** Os engines são TEMPLATES: a *sincronia* vem da
timeline, mas o *desenho de cada cena* (destaques, selos, motifs, palavras serifadas, número de
cenas) está no código, indexado por cena. Abra `cena.html` e edite os mapas no topo do `<script>`
para casar com as suas falas:
- `2-alerta`: mapa `D` (tipo de cada cena: alert/rain/phone/stamp/seal/glitch/stop/check/shield/brand/cta).
- `3-reel`: mapa `D` (hook/num/erro/tease/count/hero/brand/cta) e `HL` (destaques); badges "ERRO #n".
- `4-cinema3d`: mapa `HL` (palavras douradas/vermelhas por cena); cenas 10/11 = logo/CTA.
- `5-premium`: mapa `ACC` (palavra serifada por cena); cenas âmbar = índices em `amber`; 10/11 = logo/CTA.
- `1-kinetico`: cenas definidas inline no reduce; ajuste os textos/realces.
Mantenha SEMPRE a última cena como CTA e a penúltima como marca/logo.

**6. Confira o visual (rápido) antes do render pesado:**
```bash
node .../scripts/render.cjs cena.html timeline.json frames test   # 1 quadro por cena: teste_*.png
```
Monte um mosaico e **abra com a ferramenta Read** para revisar composição, ortografia, cortes,
legibilidade e que NÃO há telefone. Corrija o engine se precisar.

**7. Render completo** (~4–5 min; não interrompa):
```bash
node .../scripts/render.cjs cena.html timeline.json frames full
```

**8. Trilha + montagem:**
```bash
python3 .../scripts/trilha.py timeline.json music.wav reel        # vibe = o do estilo
bash   .../scripts/montar.sh frames voz_full.wav music.wav final.mp4
```

**9. Revise** (Read em 1–2 quadros do MP4) e **envie** com SendUserFile (display render).

## Pegadinhas
- Playwright resolve por `require` (CommonJS): o render é `.cjs`, não `import`.
- O `logo.png` precisa estar na MESMA pasta do HTML renderizado.
- Render = ~30fps; vídeo de 35s ≈ ~1000 quadros ≈ 4–5 min. Timeout generoso.
- Container é efêmero: o MP4 final é entregue por SendUserFile; nada fica salvo sozinho.
- Voz: a do Piper é boa mas ainda tem leve sotaque robótico. Para voz de locutor humano, usar
  ElevenLabs via API (pedir a chave ao usuário com request_credential; host api.elevenlabs.io) e
  gerar os `voz/l{i}.wav` por lá no lugar do Piper — o resto do fluxo é igual.
- Música/efeitos aqui são sintetizados (trilha.py). Se o usuário mandar trilha própria, usar a dele.

## Próximos passos possíveis
- Novos estilos: criar `estilos/6-*.html` no mesmo molde (expõe `setTimeline`/`seek`) e uma vibe
  em `trilha.py`.
- Automação: ligar numa tarefa agendada que cria e posta vídeos sozinha (como as artes).

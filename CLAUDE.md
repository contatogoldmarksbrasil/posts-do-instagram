# Memória do projeto

Este arquivo é lido pelo Claude no começo de toda sessão. Serve como memória
das conversas: decisões, preferências e o que já foi montado. Atualize ao fim
de cada conversa importante (adicione no "Registro de conversas").

## Sobre o projeto
- Posts de Instagram para os clientes **Âncora Consórcios** e **Gold Marks Brasil**.
- Padrão visual e regras dos posts: skill `posts-instagram-padrao`.
- `posts/` artes geradas · `historico/` o que já foi postado por cliente
  (`ancora.md`, `goldmarks.md`) — consultar antes de criar post novo para não repetir tema.
- `scripts/` geradores das artes (`arte_ancora.py`, `render_artboard.js`, `deve_postar.py`).
- O usuário escreve em português, de forma curta ("ss" = sim). Responder em português.

## Edição de vídeo (montado em 25/11/2026)
Fluxo testado de ponta a ponta num vídeo de teste 9:16:

| Etapa | Como |
|---|---|
| Decupagem | `ffmpeg -af silencedetect=n=-35dB:d=0.8` (pausas), `scenedetect -i v.mp4 detect-content list-scenes` (cenas), transcrição |
| Transcrição | `python3 scripts/video/transcrever.py video.mp4` → JSON com tempo de cada palavra |
| Legenda | `python3 scripts/video/legenda_reels.py palavras.json legenda.ass "3.9-6.0"` → gravar com `-vf ass=legenda.ass` |
| Corte | `select='not(between(t,A,B))',setpts=N/FRAME_RATE/TB` + `aselect`/`asetpts` no áudio |
| Cor | `eq=contrast=..:saturation=..:gamma=..`, `colorbalance`, ou `lut3d=arquivo.cube` |
| Música | `sidechaincompress` (abaixa quando há voz) + `loudnorm=I=-14:TP=-1.5` (padrão Instagram) |
| Efeito sonoro | `adelay=ms|ms` para posicionar e `amix=normalize=0` |
| Motion | `drawbox`/`drawtext` com expressões de tempo; para algo elaborado, Remotion (ainda não instalado) |

Ambiente:
- Ferramentas de vídeo: instalar SOB DEMANDA na própria sessão quando for editar vídeo
  (`pip install faster-whisper scenedetect opencv-python-headless`; baixar o modelo `small` do Whisper).
  ffmpeg já vem no sistema.
- IMPORTANTE: NÃO colocar isso num setup script do ambiente. Já aconteceu de um setup script de vídeo
  FALHAR num container novo e quebrar TODAS as tarefas agendadas (posts da Gold Marks/Âncora, leads, RPI).
  O ambiente roda as tarefas de postagem; se o setup script falhar, a sessão nem começa.
- Rede liberada para o Hugging Face (huggingface.co, us.aws.cdn.hf.co, cas-server.xethub.hf.co…).
  Usar `HF_HUB_DISABLE_XET=1`.
- Pegadinha: o faster-whisper não abre vídeo direto (conflito do PyAV) — extrair o áudio com
  ffmpeg antes (o `transcrever.py` já faz isso).
- O container é apagado ao fim da sessão: vídeos grandes, trabalhar numa pasta do computador do
  usuário (Remote Control no app desktop) em vez de passar pelo git.

Pendente:
- Usuário vai mandar um vídeo real e o padrão de cada cliente (fonte, cores, estilo de legenda,
  vinheta). Depois disso, criar a skill `edicao-video-padrao`.
- Música e efeitos: usar arquivos que o usuário fornecer (não gerar trilha).

## Registro de conversas
- **25/11/2026** — Usuário perguntou quais skills seriam necessárias para editar vídeo do zero
  (decupagem, legenda, cor, música, efeito sonoro, motion). Resposta: nenhuma skill de vídeo
  existe no catálogo; o trabalho é feito com ffmpeg + faster-whisper + PySceneDetect (+ Remotion).
  Instalado e testado tudo; criado script de instalação do ambiente; usuário pediu que o Claude
  lembre das conversas → criado este arquivo.

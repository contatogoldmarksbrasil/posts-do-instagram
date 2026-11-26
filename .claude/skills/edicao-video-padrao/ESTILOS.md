# Os 5 estilos — referência visual

Todos: 1080x1920, fundo escuro, logo no topo (discreta) e barra de progresso. Cada engine
expõe `window.setTimeline(tl)` e `window.seek(t)` (determinístico: dá pra renderizar qualquer
quadro pelo tempo). `tl = {total, fps, scenes:[{i,start,end,text}]}` (saída do narrar.py).

## 1 — Kinético (`1-kinetico.html`, vibe `kinetic`)
Tipografia cinética sobre preto/dourado. Palavras entram com escala/slide, palavras-chave em
dourado. Acentos: carimbo, número gigante ("10 ANOS"), chips, lockup da marca. Direto e forte.
Bom para: institucional, "por que registrar", mensagem objetiva.

## 2 — Alerta (`2-alerta.html`, vibe `alerta`)
Urgência. Tipos de cena no mapa `D`: ⚠️ que treme, boletos caindo, **celular com e-mail falso +
lupa + "PAGUE EM 24H"**, carimbo "FALSO", selo oficial, glitch, **"PARE" em placa de pare**,
checklist ✓, escudo, logo, CTA. Vermelho de alerta. Flashes e tremor.
Bom para: golpe do falso INPI, riscos, "não caia nessa".

## 3 — Reel / ranking (`3-reel.html`, vibe `reel`)
Estilo reel viral (referência do usuário). **Raios de velocidade** atrás dos impactos, **legenda
karaokê** (palavra falada destacada numa caixinha dourada), slams **"#1 / #2 / #3"**, badge
"ERRO #n", contador, motifs (CNPJ ✗, medalha 1º, busca "JÁ EXISTE"), cena de **suspense**
("🔥 O MAIS COMUM") para prender até o fim. Mapas `D` (tipo de cena) e `HL` (destaques).
Bom para: "3 erros que...", ranking, listas, retenção alta.

## 4 — Cinema 3D (`4-cinema3d.html`, vibe `cinema`)
Câmera voando em 3D pelo espaço (efeito **warp** com riscos de velocidade). As frases flutuam em
profundidade, a câmera chega, você lê, e ela passa gigante e desfocada enquanto a próxima surge
ao fundo. Névoa dourada, profundidade de campo. Mapa `HL` (dourado/vermelho por cena).
Bom para: mensagens emocionais/patrimônio, clima épico.

## 5 — Premium / cards (`5-premium.html`, vibe `premium`)
Estilo "aesthetic" (referência do usuário). **Cards de vidro flutuando** com profundidade (cards
fantasma desfocados atrás), **bokeh âmbar** se movendo, tipografia elegante com palavra de
destaque em **serifado itálico dourado** (Playfair Display). Cards âmbar nos momentos-chave.
Áudio suave com sininhos. Mapa `ACC` (palavra serifada por cena); `amber` = índices de cards âmbar.
Bom para: marca como reputação/valor, clima sofisticado, classudo.

## 6 — Impacto / minimalista bold (`6-impacto.html`, vibe `reel`)
Molde dos vídeos @altralab que o usuário curtiu. Preto, MUITO minimalista, **tipografia gigante**
branca com palavra-chave dourada, uma ideia por tela. **Gancho forte no início** (nome digitado
"SUA MARCA" + carimbo vermelho "TEM DONO?" — equivalente ao balão deles). **Card inteiro** dourado
("REGISTRE ANTES"), **número gigante** ("10 ANOS"). Cortes secos e punchy. Mapa `D` (hook/big/card/
num/brand/cta) + `hl` (palavra dourada por cena). Trocar dourado por laranja = ajustar as cores no CSS.
Bom para: ganchos de retenção, mensagens diretas e fortes, "quem registra primeiro leva".

## Como adaptar um engine a um roteiro novo
1. Conte quantas falas tem o roteiro = número de cenas.
2. Ajuste o mapa de desenho do engine (D / HL / ACC) para cobrir esses índices, 1..N.
3. Mantenha a penúltima cena = marca/logo e a última = CTA.
4. Renderize em `test` e confira o mosaico com Read antes do render `full`.

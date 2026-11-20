# Produzir o GIF

## Com gravação disponível

Grave a janela ou a área relevante e habilite o cursor na ferramenta, quando houver essa opção. Comece perto do estado inicial e termine depois de o resultado ficar legível. Para uma nova gravação, conduza a ponta do ponteiro ao centro do controle visível, clique ali e mantenha o ponteiro parado até iniciar o próximo movimento. Aguarde o próximo alvo aparecer antes de se mover em sua direção. Confira no arquivo gravado se o cursor realmente aparece antes de exportar.

Elimine esperas sem valor para a demonstração e preserve duração real quando ela for o que está sendo testado. Use uma paleta compartilhada, mantenha a proporção da imagem e teste legibilidade em tamanho normal. Ajuste resolução e frequência dos quadros conforme o detalhe necessário e o tamanho de arquivo.

Com o FFmpeg disponível, este exemplo converte uma gravação em MP4 (MPEG-4 Parte 14) para GIF de até 1.120 pixels de largura. Execute no diretório da gravação com um nome de saída livre.

```bash
# Seleciona 15 quadros por segundo, reduz a largura quando necessário e gera
# uma paleta de cores para a sequência. O resultado repete automaticamente.
ffmpeg -i gravacao.mp4 \
  -filter_complex "[0:v]fps=15,scale=w='min(1120,iw)':h=-1:flags=lanczos,split[imagem][amostra];[amostra]palettegen[paleta];[imagem][paleta]paletteuse[saida]" \
  -map '[saida]' -loop 0 evidencia.gif
```

## Com capturas da interface

Se a ferramenta só entregar imagens ou omitir o ponteiro, capture a interface em mais momentos. Inclua a abertura de menus e diálogos, parte da digitação quando útil e momentos antes e depois da ação decisiva. Mantenha dimensões e enquadramento constantes. Registre a posição observada dos controles para alinhar o ponteiro sobreposto aos alvos corretos.

Monte os quadros com as ferramentas locais disponíveis, como FFmpeg ou Pillow.
Para cada acionamento, mantenha na tela a captura em que o controle está visível
e insira quadros intermediários em que a ponta do ponteiro percorra o caminho
da posição anterior até o centro da região clicável observada. Preserve a ponta
na mesma posição durante o acionamento e na captura que mostra o resultado.
Dê tempo para ler esse resultado antes de mover o ponteiro ao controle seguinte.
Mantenha os estados da interface nas capturas reais durante a montagem.

Quando as capturas já mostrarem um ponteiro parado, use imagens sem ele ou
recupere somente a área coberta pelo marcador, quando o conteúdo original sob
ela puder ser preservado. Mostre um único ponteiro durante todo o trajeto. Se
a recuperação encobrir um rótulo ou estado relevante, refaça essa captura.
Informe na entrega quando o movimento foi reconstituído na montagem.

Mostre as mudanças da interface com as capturas observadas. Use tempo de leitura
suficiente para resultados e mensagens. Preserve o tempo real quando ele fizer
parte da evidência. Se o GIF ficar bloqueado, explique o que impede a exportação.

## Aparência do ponteiro

Quando o ponteiro for desenhado na montagem, use o cursor do tema do sistema do usuário, e não uma
seta desenhada à mão. No Linux Mint deste ambiente, o tema é Bibata-Modern-Classic (seta preta
arredondada com contorno branco). O script [`cursor_do_sistema.py`](../scripts/cursor_do_sistema.py)
lê o tema configurado e exporta o PNG com o ponto ativo:

```bash
# Seta padrão, 32 pixels; imprime o arquivo e o ponto ativo (xhot, yhot) em JSON.
python3 scripts/cursor_do_sistema.py /tmp/ponteiro.png
# Mão, para cliques em links.
python3 scripts/cursor_do_sistema.py /tmp/mao.png --nome pointer
```

Cole a imagem de modo que o ponto ativo, e não o canto da imagem, fique sobre o alvo. Use a seta
nos botões e controles e a mão nos links, como o próprio sistema mostra. Escolha o tamanho pela
largura final do GIF, para o ponteiro ficar visível sem cobrir o controle: 32 pixels funciona
numa saída de 1280×720. Se o tema não estiver disponível, informe e use a seta mais próxima.

## Conferência

Decodifique todos os quadros e reproduza a animação em tamanho e velocidade
normais. Confira três pontos de cada ação no arquivo exportado: o deslocamento
visível sobre o estado anterior, a ponta sobre o controle antes da mudança de
tela e a pausa na mesma posição com o resultado visível. Se o ponteiro apenas
mudar de posição junto com a troca de captura, refaça a montagem daquele
trajeto antes da publicação. Confira também a ordem dos estados, a legibilidade
e o recorte das áreas privadas.

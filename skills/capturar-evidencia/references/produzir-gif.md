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
Se precisar acrescentar um ponteiro, use uma posição contínua entre quadros.
Use como referência a ponta do ponteiro e o centro da região clicável observada.
Mantenha a ponta no centro no instante do clique e parada depois dele, inclusive
se a imagem mudar. Comece o trajeto seguinte somente quando o novo alvo estiver
visível e for a hora da próxima ação. Em um material com cursor gravado, preserve
a ação observada e evite sobrepor um segundo ponteiro.

Mostre as mudanças da interface com as capturas observadas. Use tempo de leitura
suficiente para resultados e mensagens. Preserve o tempo real quando ele fizer
parte da evidência. Se o GIF ficar bloqueado, explique o que impede a exportação.

## Conferência

Decodifique todos os quadros e observe a animação em tamanho de visualização. Confira se o ponteiro coincide com os alvos, se estados intermediários e resultados estão na ordem, se textos importantes permanecem legíveis e se áreas privadas ficaram fora da evidência.

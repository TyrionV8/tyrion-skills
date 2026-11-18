# Montar e verificar com Remotion

## Preparar a composição

1. Preserve as capturas originais. Reutilize um projeto Remotion disponível ou
   faça a composição em diretório de trabalho separado da aplicação. Verifique
   o renderizador disponível antes de depender dele. Se houver impedimento,
   informe o limite e disponibilize a evidência base que estiver pronta.
2. Use as capturas da aplicação como fundo. Em vídeo ou GIF existente, use o
   original ou quadros extraídos que preservem a ordem e a duração de cada
   estado. Para uma sequência de imagens, ordene os estados realmente capturados.
   Deixe claro quando a animação for uma montagem de capturas.
3. Alinhe indicações às coordenadas da captura. Ao recortar ou redimensionar,
   aplique a mesma transformação aos alvos, contornos e ponta do ponteiro. Se
   houver texto ou indicador de etapas, reserve espaço fora dos controles.
   Atualize a etapa e a contagem quando o estado correspondente ficar visível.
   Escreva legendas que descrevam a ação ou o resultado observado.

## Animar e exportar

- Em um GIF, introduza cada seta ou contorno na etapa em que seu alvo está
  visível. Mantenha a indicação tempo suficiente para ler o controle, o
  resultado ou o erro. Ao destacar uma região da interface, escureça suavemente
  o entorno e deixe a região com sua luminosidade original.
- Se o cursor já estiver gravado, use-o como registro do trajeto e do clique.
  Quando precisar animar um ponteiro sobre capturas, marque a primeira posição
  e o centro da região clicável de cada alvo. Na linha do tempo, identifique
  quando o alvo aparece, quando começa o movimento e quando ocorre o clique.
  Use um único trajeto contínuo.
  Depois do clique, mantenha a mesma posição também na troca de cena. Saia
  desse ponto só no momento da próxima ação, com o próximo alvo já visível.
  Represente cliques observados e preserve seu efeito real, inclusive cliques
  sem resposta. Quando a posição original importar para o erro, registre-a
  como observada.
- Para imagens, use `remotion still` para renderizar o quadro anotado de cada
  captura e reúna os quadros somente quando esse for o formato escolhido.
  Para animação, use `remotion render`. Se precisar otimizar o GIF, parta de
  quadros renderizados sem perdas e converta com paleta de cores compartilhada.
  Revisite resolução e cadência conforme a legibilidade da saída.

## Conferir o artefato

Veja a saída no tamanho em que será lida. Confira se as setas terminam nos
alvos certos, se os realces deixam o texto visível e se a indicação de etapa
corresponde à interface. Na animação, confira o quadro do clique, os quadros
antes e depois da troca de estado e o primeiro quadro de movimento rumo ao
próximo alvo. Nas imagens, confira a ordem e qualquer legenda. Distinga o que
foi capturado das marcações acrescentadas. Deixe visíveis os fatos que permitem
à pessoa responsável avaliar e reproduzir o comportamento.

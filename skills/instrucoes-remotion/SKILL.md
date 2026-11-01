---
name: instrucoes-remotion
description: Cria e ajusta animações Remotion sincronizadas ao corte real de um vídeo para montagem em Drift, CutScript ou outro editor. Apresenta prévias temporárias com o vídeo de referência, aguarda aprovação para exportar gráficos transparentes permanentes e insere no editor somente quando solicitado. Use também ao pedir ajuste após mudanças no vídeo ou na montagem.
---

# Instruções Remotion

## Contrato de trabalho

Trabalhe sobre o corte correspondente do vídeo e mostre a animação sobre ele.
O ciclo é: **prévia com vídeo → ajustes → aprovação dessa versão → exportação
transparente**. A inserção na montagem depende de um pedido explícito separado;
esse pedido pode estar na mesma mensagem da aprovação. Aprovar ou exportar não
autoriza importar, inserir, substituir clipes nem reorganizar a montagem.

Sincronização é requisito do resultado: preserve a relação entre fala, gesto,
animação e posição na linha do tempo. Não considere suficiente um arquivo que
reproduz corretamente, mas aponta para o objeto ou momento errado.

## Preparar o trecho e os arquivos

1. Identifique o projeto de edição, a versão atual do vídeo, o trecho da animação
   e a montagem em que será usada. Inspecione arquivos e ferramentas disponíveis;
   use o corte atual como referência, em vez de assumir que o vídeo bruto serve.
2. Preserve os originais e o trabalho local. Mantenha código, configurações e dados
   de movimento em local permanente do projeto para permitir novas renderizações.
3. Salve **todas as versões de validação com o vídeo de fundo em `/tmp`**, em uma
   pasta exclusiva. Isso inclui os recortes intermediários feitos para a validação.
   Referenciar um vídeo original permanente não exige mover nem duplicar o original.
4. Defina um destino permanente para a exportação transparente: de preferência uma
   pasta de mídia junto ao projeto do editor ou outra pasta permanente do projeto
   que faça sentido. Não deixe a única entrega aprovada em `/tmp`.
5. Crie uma ficha junto ao código usando o modelo
   [assets/ficha-sincronizacao.json](assets/ficha-sincronizacao.json).
   Preencha dados observados; deixe desconhecidos como `null` até verificá-los.

Antes de calcular alinhamentos, recortes ou ajustes, leia
[references/sincronizacao.md](references/sincronizacao.md).

## Criar e mostrar a prévia

- Use duas saídas do mesmo código e dos mesmos parâmetros: uma prévia com o vídeo
  correspondente e uma composição só com os gráficos sobre transparência real.
  Gere a prévia primeiro. Não monte versões independentes que possam divergir.
- Mostre a prévia por arquivo, player ou Studio e informe como abri-la. Se a
  ferramenta não exibir vídeo, entregue um link utilizável e imagens relevantes,
  indicando o limite dessa conferência. Não alegue que assistiu ao que não viu.
- Explique brevemente como foi feito: trecho de referência, objetos/elementos
  animados, rastreamento ou quadros-chave e sincronização. Ensine os controles
  relevantes quando o usuário quiser ajustar; painéis editáveis podem ajudar,
  mas não são obrigatórios para toda animação.
- Confira momentos de entrada, movimento, rotação, oclusão e saída que existam no
  trecho. Evite nomes pequenos, excesso de texto e gráficos sem função explicativa.
- Apresente a versão e aguarde aprovação. Enquanto o usuário pedir mudanças,
  atualize a prévia em `/tmp`, a ficha e os parâmetros; não exporte antecipadamente
  a entrega transparente. Não repita uma aprovação já concedida à mesma versão.

## Aprovar e exportar

Registre a aprovação da versão identificada na conversa e na ficha. Exporte
somente os gráficos, com canal alfa (informação de transparência), no destino
permanente. Não inclua o vídeo de referência nem seu áudio por padrão.

Escolha um formato compatível com o editor e confirme a transparência por
decodificação ou composição sobre um fundo. Metadados e um reprodutor com fundo
preto não bastam. Verifique duração, resolução, quadros por segundo, início real
do conteúdo e qualidade de nomes/linhas. Se a única renderização falhar, corrija
o problema técnico dentro da versão aprovada; mudanças visuais ou temporais
relevantes voltam à prévia para nova revisão.

Entregue o caminho permanente, duração e instrução de alinhamento específica
da montagem conhecida. Se a montagem estiver inacessível, explicite essa limitação
e não invente uma posição. Preserve versões anteriores em vez de sobrescrevê-las.

## Inserir somente quando solicitado

Com pedido explícito de inserir, importar ou substituir, use apenas a operação
autorizada. Inspecione novamente o estado atual do editor e o alinhamento antes
de agir; a montagem pode ter mudado desde a aprovação.

Use as ferramentas do editor ou suas skills específicas disponíveis. Para Drift,
use `conectar-drift` quando disponível. Para CutScript ou outro editor, consulte
as capacidades e instruções reais; não presuma comandos, formatos ou acesso.

Depois de inserir, confira visualmente momentos relevantes e confirme a posição
efetivamente aplicada. Preserve clipes, cortes, áudio e alterações alheias ao pedido.
Registre o resultado na ficha e informe o que foi alterado e validado.

## Pedido “ajuste” após editar o vídeo

### Quando o pedido contém apenas “ajuste”

Se a skill for chamada com apenas a palavra “ajuste”, desconsiderando a própria
invocação da skill, espaços, maiúsculas e pontuação final, abra **uma caixinha de
pergunta** com a ferramenta de perguntas disponível antes de alterar a animação.
O objetivo é ajudar o usuário a formular o pedido, sem supor o que ele quer mudar.

Pergunte: “Que tipo de ajuste você quer? Escolha um exemplo e, se quiser, complete
com o trecho ou escreva seu pedido.” Ofereça três exemplos de pedidos completos,
adaptados ao projeto e à animação conhecidos. Por exemplo:

1. “Cortei uma pausa no vídeo. Reveja o corte atual, sincronize a animação e mostre
   uma nova prévia com o vídeo de fundo.”
2. “Mudei a velocidade deste trecho. Ajuste os tempos da animação para acompanhar
   a fala e os gestos, e mostre uma nova prévia.”
3. “As pontas dos indicadores estão saindo das peças. Reveja o rastreamento,
   corrija o acompanhamento e mostre uma nova prévia.”

Esses são exemplos para escolha, não um diagnóstico nem uma afirmação de que
essas mudanças aconteceram. Em animações sem indicadores, troque o terceiro por
um exemplo pertinente de posição, legibilidade ou entrada dos elementos. Use
referências concretas já conhecidas; não invente cortes, problemas ou horários.

Permita resposta livre para combinar exemplos ou informar outro ajuste. Aguarde
a escolha ou descrição antes das alterações; então prossiga com a revisão abaixo.
Se a ferramenta de perguntas não estiver disponível, apresente a mesma pergunta
com uma lista numerada no chat. Não simule uma caixa inexistente. Quando o pedido
já trouxer detalhes, aproveite-os sem abrir essa caixa automaticamente.

### Executar o ajuste descrito

Interprete “ajuste”, no contexto desta animação, como revisar o vídeo e a montagem
atuais para adaptar a animação às mudanças. Compare-os à ficha: cortes, duração,
velocidade, enquadramento, posição, fala, gestos e trajetória quando relevantes.
Se houver várias animações ou versões plausíveis, identifique o alvo antes de editar.

Reveja o vídeo; não aplique apenas um deslocamento numérico sem conferir a imagem.
Refaça os ajustes necessários e mostre nova prévia com o vídeo em `/tmp`.
Marque a revisão como pendente de aprovação e preserve a entrega aprovada anterior.
Após a nova aprovação, exporte outra versão transparente no destino permanente.
Não importe, substitua nem reinsira no editor sem um pedido que cubra essa ação.

## Exemplos de uso

- “Use instrucoes-remotion para identificar as peças quando eu mostrar a placa.”
  → Prévia sobre o corte real em `/tmp`, ficha junto ao código e pedido de aprovação.
- “Aprovado, exporte.” → Arquivo transparente permanente; montagem intocada.
- “Aprovado, exporte e coloque no Drift.” → Exportação e inserção com alinhamento
  recalculado e conferido na montagem atual.
- “Cortei uma pausa e mudei a velocidade. Ajuste.” → Revisão do vídeo atual,
  nova prévia sincronizada e nova aprovação antes da entrega atualizada.
- “$instrucoes-remotion ajuste” → Caixinha com exemplos contextualizados para
  o usuário escolher ou escrever um pedido mais preciso antes das alterações.

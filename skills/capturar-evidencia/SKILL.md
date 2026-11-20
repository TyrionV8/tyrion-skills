---
name: capturar-evidencia
description: "Registra o comportamento observado na interface de uma aplicação, inclusive erros, testes exploratórios e procedimentos. Use por chamada explícita ou como etapa de capturar-evidencia-remotion. Entrega GIF por padrão ou capturas individuais ou reunidas quando solicitadas."
---

# Capturar evidência

Use quando o usuário invocar `$capturar-evidencia` ou como etapa de uma chamada
explícita a `$capturar-evidencia-remotion`. O objetivo é documentar o que se viu
de forma clara e reproduzível. Quem analisa a evidência decide se o comportamento
atende ao esperado.

## Escolher a origem e o ambiente

- Para um novo teste, prefira executar a aplicação real, normalmente em ambiente
  local. Use o modo de execução do projeto, confirme a versão e o ambiente dos
  serviços conectados e faça o fluxo pela interface. Use a interface e os serviços
  reais envolvidos, incluindo o servidor e o banco quando fizerem parte do teste.
  Uma interface servida localmente pode estar conectada a um ambiente remoto.
- Use dados fictícios no banco de um ambiente local isolado quando for adequado
  ao cenário e estiver dentro do escopo. Prefira criá-los pelo fluxo normal ou pelo
  mecanismo de preparação do projeto. Use dados reais quando forem necessários
  e autorizados. Pergunte se houver dúvida relevante sobre
  como rodar a aplicação, se pode inserir dados fictícios no banco local ou quais
  ações estão autorizadas em ambiente não local. Faça a inspeção disponível antes
  de perguntar. A autorização para capturar a tela cobre a área do fluxo solicitado.
- Use um protótipo ou uma simulação quando o pedido for uma prévia antes da
  implementação, quando o usuário solicitar, ou quando um problema impedir rodar
  a aplicação e uma prévia ainda atender ao pedido. Identifique o impedimento, o que
  foi simulado e quais partes executaram de fato. Se o objetivo for registrar um
  erro na aplicação, preserve o erro observado e os passos que levaram a ele.
- Se o usuário fornecer mídia e pedir que ela seja usada, trabalhe a partir dela
  e identifique sua origem. Registre eventual lacuna na sequência observada.
- Capture só a área pertinente e proteja credenciais, notificações privadas e
  dados sensíveis. Se depender de login, acesso ou ação fora da autorização
  disponível, conclua o que puder verificar e indique a ação necessária.

## Escolher o formato

- Para uma nova captura, entregue por padrão **um GIF animado** (Graphics
  Interchange Format). Em cada ação com o mouse, mostre o ponteiro percorrendo
  o trajeto até o centro do controle, o acionamento e uma pausa no resultado.
  O ponteiro desenhado usa o cursor do tema do sistema (no Linux Mint,
  Bibata-Modern-Classic); veja [Aparência do ponteiro](references/produzir-gif.md#aparência-do-ponteiro).
  Se a origem for uma série de imagens estáticas, acrescente quadros intermediários
  do movimento. Consulte [Produzir o GIF](references/produzir-gif.md).
- Para **prints** ou **capturas individuais**, entregue os arquivos em uma mesma
  pasta, com nomes em ordem e legíveis. Para **prints unificadas**, reúna as
  capturas em uma imagem, na sequência observada.
- Para edição de mídia existente, preserve o formato de entrada quando o pedido
  deixar o formato em aberto. Se forem pedidos vários formatos, entregue os
  selecionados. Guarde os insumos de montagem fora da pasta de entrega.

## Registrar o comportamento

1. Mostre o estado inicial quando relevante, a ação decisiva e o resultado
   observado. Se houver um resultado esperado conhecido, identifique-o como
   expectativa. Em um teste exploratório, registre o que aconteceu em cada ponto
   relevante mesmo que o resultado ainda seja desconhecido.
2. Quando houver uma divergência, mostre o passo que a antecedeu e o que ficou
   visível em seguida, como mensagem literal, estado inalterado, resposta
   incompleta ou mudança inesperada. Preserve a sequência e o tempo de espera
   quando forem necessários para reproduzir o ocorrido.
3. Forneça o contexto necessário para reproduzir o fluxo. Inclua ambiente,
   versão quando disponível, condição inicial, ações e dados de teste que possam
   ser compartilhados. Descreva apenas o que foi observado e indique quais
   componentes foram exercitados ou simulados quando isso estiver verificado.

## Verificar e entregar

- Reproduza o GIF final em velocidade normal antes de entregar ou anexar.
  Confira se o ponteiro percorre cada trajeto, chega ao controle antes do
  acionamento e permanece ali enquanto o resultado aparece. Corrija saltos
  entre posições ou ponteiros duplicados e confira a nova exportação.
  Verifique também ordem, legibilidade, recorte e tempo de leitura.
- Salve no local solicitado ou em uma pasta de artefatos do projeto. Mostre a
  mídia na resposta quando possível e disponibilize os arquivos.
- Informe o ambiente, os dados fictícios quando usados e as edições relevantes
  da captura, como montagem de quadros ou ponteiro acrescentado. Entregue a
  evidência e o relato da observação para que a pessoa responsável os avalie.

Exemplo de invocação. “Use `$capturar-evidencia` para tentar salvar um cadastro
na aplicação local e registrar o que aparecer depois do clique.”

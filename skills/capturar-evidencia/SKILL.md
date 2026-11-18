---
name: capturar-evidencia
description: "Gera evidência visual de um comportamento da interface. Use apenas por chamada explícita para demonstrar uma implementação nova ou existente, registrar um teste pela interface ou mostrar como executar um procedimento. Entrega GIF animado por padrão e capturas individuais ou reunidas em uma imagem quando solicitadas."
---

# Capturar evidência

Ative só quando o usuário chamar `$capturar-evidencia`, mencionar o nome como invocação ou pedir expressamente o uso desta skill. Use o contexto do pedido para identificar a aplicação, a versão ou o ambiente disponível e o comportamento a registrar. Pergunte apenas se faltar uma informação que impeça identificar o fluxo ou obter acesso autorizado.

## Escolher o formato

- Por padrão, entregue **um GIF animado** (Graphics Interchange Format), com o ponteiro visível e movimento entre as ações. Consulte [Produzir o GIF](references/produzir-gif.md).
- Para **prints** ou **capturas individuais**, entregue os arquivos em uma mesma pasta, com nomes em ordem e legíveis.
- Para **prints unificadas**, entregue uma imagem única com as capturas em ordem. Use legendas curtas quando elas ajudarem a identificar a ação ou o resultado.
- Se o usuário pedir uma combinação, entregue os formatos escolhidos. Guarde insumos temporários da montagem fora da pasta de entrega.

## Registrar o fluxo

1. Identifique o que deve ficar visível para que a evidência faça sentido por si. Mostre o estado inicial quando relevante, a ação decisiva e o resultado observado. Para um teste, confira o resultado esperado e registre também falhas observadas. Para instruções de uso, mostre os controles necessários para reproduzir o procedimento.
2. Abra a interface que contém o trabalho pedido. Quando houver versões diferentes em execução, confirme a versão pelo comportamento ou por um identificador verificável. Use as ferramentas permitidas de navegador, captura de janela ou gravação disponíveis no ambiente.
3. Confirme que a área capturada e as ações fazem parte do pedido. A invocação explícita para gerar evidência autoriza capturar a área do fluxo solicitado. Para ações com efeitos reais, use a autorização específica prevista para o ambiente ou demonstre com dados fictícios. Limite o enquadramento à aplicação e preserve credenciais, notificações privadas e conteúdo pessoal.
4. Execute ou acompanhe pela interface a sequência pertinente. Use dados fictícios quando o pedido permitir demonstração e dados reais quando forem essenciais e autorizados. Se depender de login, acesso ou versão indisponível, conclua as verificações independentes e indique a ação necessária. Use imagens previamente fornecidas com identificação da origem e do limite da evidência.

## Verificar e entregar

- Abra ou decodifique o resultado. Confira a ordem das etapas, os textos e controles legíveis e o resultado realmente mostrado. No GIF, verifique a reprodução, a duração, a posição do ponteiro e o tempo de leitura. Nas imagens, confira os recortes e a resolução do arquivo final.
- Salve no local solicitado ou em uma pasta de artefatos do projeto, com nome ligado ao comportamento registrado. Mostre a mídia na resposta quando o ambiente permitir. Forneça acesso aos arquivos em resolução original ou à pasta das capturas.
- Identifique o ambiente observado e se os dados são fictícios. Se houve montagem de quadros, sobreposição de ponteiro ou abreviação relevante, declare a edição e preserve a ordem dos eventos.

Exemplo de invocação. “Use `$capturar-evidencia` para mostrar, na prévia local, o botão mudando depois da primeira concessão e voltando após a última revogação.”

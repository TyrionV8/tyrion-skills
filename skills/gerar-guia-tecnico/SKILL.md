---
name: gerar-guia-tecnico
description: Gera um guia técnico de estudo e consulta em arquivo HTML único para o usuário entender em profundidade um projeto ou uma funcionalidade planejada ou implementada. Use quando ele quiser parar para estudar, recuperar o contexto ou dominar o que foi feito, com forte apoio visual e definição dos termos e siglas utilizados.
---

# Gerar Guia Técnico

Produza um material de estudo que dê ao usuário domínio sobre aquilo que planejamos ou implementamos. O leitor principal é sempre o próprio usuário: ele precisa entender o que cada coisa é, como funciona, por que existe e como se relaciona com o restante. O guia também deve ajudá-lo a explicar o trabalho aos colegas, orientar uma manutenção futura e responder às perguntas do cliente.

## Texto com função didática

Todo texto deve ensinar, explicar, orientar uma ação ou identificar conteúdo de forma útil. Use títulos que indiquem o conceito, a relação ou o procedimento tratado. Não acrescente slogans, títulos marketeiros, chamadas vagas, frases motivacionais ou texto que só sirva de apresentação ou de nome de capítulo. Por exemplo, prefira "Volume de controle, vazão e escolha da equação" a "Da figura para a equação". Remova texto sem informação adicional; mantenha os títulos necessários à navegação, à acessibilidade e à compreensão. A organização visual deve facilitar o aprendizado e a consulta, sem usar texto decorativo para tornar o artefato mais "legal".

## Contexto e investigação

- Use o pedido e a conversa como fonte primária para identificar o trabalho, recuperar decisões e delimitar o projeto, a funcionalidade ou o planejamento que será estudado. A conversa orienta a investigação, mas não é a única fonte nem representa necessariamente toda a implementação. Pergunte apenas o que faltar para compreender esse escopo; não volte a perguntar quem é o público.
- Quando o usuário indicar dúvidas ou assuntos em que está mais confuso, trate-os como prioridades de estudo. Em particular, uma sequência de perguntas junto da chamada representa suas maiores confusões: desenvolva cada uma com grande detalhamento no guia, explicando fundamentos, termos, funcionamento passo a passo, exemplos concretos e relações com o restante da implementação. Dedique recursos visuais pertinentes a esses pontos e mantenha o contexto necessário para compreendê-los.
- Quando a skill for chamada sem explicações adicionais, use o contexto disponível para identificar o assunto e investigue a implementação real desse escopo nos repositórios e demais fontes pertinentes. Organize o estudo a partir do funcionamento e das relações encontrados, sem limitar o guia ao que foi mencionado no chat. Não exija uma lista prévia de dúvidas: o guia também serve para revelar relações e lacunas que o usuário ainda não percebeu. Se o assunto não puder ser identificado com segurança, pergunte apenas o necessário para delimitá-lo.
- Parta da necessidade de aprendizado profundo. Não presuma que o usuário domina um conceito apenas porque participou da implementação ou porque o código foi gerado com auxílio de inteligência artificial.
- Leia as fontes pertinentes: código real, contratos, configurações, migrações, testes, documentos de decisões e planejamento. Confira diretamente na implementação as afirmações sobre seu funcionamento atual; quando houver divergência com o relato da conversa, explique a diferença e o alcance das evidências.
- Considere que a implementação pode ter sido feita por vários agentes ou em outras sessões. Dentro do escopo em estudo, acompanhe componentes relacionados, chamadas e integrações; consulte histórico de mudanças e registros de entrega quando ajudarem a localizar essas contribuições. Inclua as partes relevantes encontradas mesmo que não tenham aparecido nesta conversa, sem presumir que o trabalho deste chat esgota o projeto.
- Separe o que foi planejado, implementado, configurado, observado em execução e validado. Num guia de planejamento, explique o funcionamento proposto e as decisões em aberto sem apresentá-los como uma implementação existente.
- Mantenha as fontes rastreáveis, com arquivos e símbolos ou linhas quando úteis. Identifique a revisão e a data da consulta quando isso ajudar a situar o leitor. Registros históricos de testes devem conservar sua data e seu alcance.
- A investigação serve para explicar o trabalho. Inspeções operacionais devem ser de leitura e necessárias à explicação; uma consulta de código não exige novas inferências, processamento de dados, migrações, reinícios ou mudanças na aplicação.

### Arquivos de planejamento e dúvidas de escopo

Quando o usuário apontar um arquivo de planejamento, considere-o entre as fontes indicadas. Esses arquivos podem começar com o plano e receber registros da implementação ao longo do trabalho: examine também essas atualizações, em vez de interpretar todo o documento apenas como intenção inicial. Confira na implementação as afirmações sobre o funcionamento atual.

Se o usuário não indicar um arquivo e houver dúvida sobre o escopo do guia, procure documentos pertinentes com nomes como `planejamento...`. Apresente os candidatos relevantes, com uma breve indicação do que parecem cobrir, e pergunte se algum representa toda ou parte da implementação que deve ser estudada. O usuário também pode orientar a desconsiderar um documento, inclusive quando ele contém partes do trabalho, mas tende a confundir a delimitação; respeite essa escolha.

Essa busca e confirmação são recursos para resolver uma dúvida concreta de escopo. Com o escopo já claro, prossiga pela investigação das fontes pertinentes sem exigir a localização ou confirmação de um planejamento.

O usuário pode querer estudar uma parte ampla ou todo um projeto grande, sem um documento que o represente integralmente. Nesse caso, delimite o estudo pelo pedido e pela análise da implementação, percorrendo sua organização, componentes e integrações. A ausência de um planejamento abrangente não impede produzir o guia.

## Construção da compreensão

Organize a explicação do todo para as partes e volte a conectá-las. Escolha a sequência que ajude o usuário a formar um modelo mental consistente, sem impor uma lista fixa de capítulos.

Explique, conforme a pertinência ao caso:

- O problema tratado, o resultado esperado e o que mudou em relação ao estado anterior.
- As entradas, saídas, etapas e responsáveis; siga um exemplo do início ao fim para mostrar como os componentes colaboram.
- O que cada tecnologia, biblioteca, serviço ou modelo faz neste projeto, a razão de seu uso e as implicações das escolhas feitas.
- Como dados e estado são representados, transformados, armazenados e recuperados. Quando houver arquivos ou banco, esclareça o local lógico e físico conhecido, os vínculos e o ciclo de vida.
- O caminho relevante no código: pontos de entrada, chamadas, contratos e persistência. Use trechos curtos e reais quando ajudarem a entender uma decisão ou mecanismo, acompanhados de explicação.
- O comportamento em interrupções, erros, concorrência e retomadas quando essas situações fizerem parte do trabalho. Mostre consequências observáveis para o usuário e para quem mantém o sistema.
- As decisões tomadas, suas justificativas, alternativas efetivamente discutidas, limitações e questões ainda abertas. Não invente uma justificativa histórica: diferencie motivo documentado de interpretação técnica.
- Como conferir o comportamento e quais evidências já existem. Diferencie teste, resultado esperado e resultado observado.

Definir termos e siglas é parte essencial da explicação. Não presuma que o usuário conhece uma expressão por ela ser comum entre desenvolvedores. Ao introduzir um termo técnico, explique em linguagem simples o que ele é, para que serve e qual é sua função neste caso. Ao usar uma sigla, apresente seu nome completo pelo menos na primeira ocorrência, com tradução ou explicação em português quando útil; expandir o nome sem explicar o conceito não basta.

Defina também os termos que aparecerem em diagramas, gráficos e exemplos. Um glossário pode ajudar na consulta, mas deve complementar as explicações no ponto de uso. Em seções que possam ser consultadas isoladamente, retome os significados essenciais quando necessário. Em contas e fórmulas, nomeie as grandezas e suas unidades. Faça exemplos concretos e identifique simulações, valores ilustrativos e dados fictícios.

A profundidade deve ajudar a entender mecanismos e relações. Distribua detalhes em camadas, com orientação de leitura, exemplos e explicações consultáveis. Evite despejar código ou listar dependências sem explicar sua função.

Inclua perguntas pertinentes que o usuário possa usar para conferir a própria compreensão e respostas que o ajudem a explicar o trabalho. Perguntas de colegas e clientes devem refletir o conteúdo estudado, com apoio nas fontes e com os limites do que se sabe.

## Explicação visual escolhida para cada caso

A aparência deve decorrer da melhor forma de explicar o projeto ou a funcionalidade. Não use um tema, layout, quantidade de diagramas ou conjunto de controles como padrão obrigatório.

Faça uso abundante e variado de artefatos visuais úteis ao entendimento. Procure oportunidades ao longo do guia, em vez de concentrar a explicação visual numa capa ou num único diagrama geral. Escolha a representação pela dúvida que ela ajuda a resolver; não limite o guia a um tipo de imagem nem preencha uma quantidade artificial.

- Explore imagens explicativas, diagramas de arquitetura e fluxo, mapas de relações, gráficos, linhas do tempo, comparações visuais e outros recursos adequados ao assunto. Combine-os quando ajudarem a enxergar diferentes aspectos do mesmo mecanismo.
- Use os visuais para explicar sequência, caminhos de dados, relações, estado, tempo, comparação ou causa e efeito. Conecte cada representação ao texto e explique como lê-la e o que ela permite compreender.
- Preserve precisão técnica, legendas, direção dos fluxos e distinção entre conteúdo real e ilustração. Em gráficos quantitativos, defina eixos, unidades e origem dos valores; identifique dados ilustrativos e não apresente números inventados como medições do projeto.
- Considere diagramas ampliáveis, exploração por etapas, comparação de estados e simulações didáticas quando ajudarem a estudar. Navegação, busca, glossário, impressão e modo de apresentação podem ser acrescentados pelo benefício concreto, sem obrigação de reproduzir os recursos de um guia anterior.
- Use imagens vetoriais ou elementos nativos do documento para esquemas técnicos quando forem adequados. Recursos gerados não devem fingir ser uma captura de tela, medição ou evidência real.
- Mantenha leitura confortável, contraste, hierarquia, adaptação a telas menores e operação por teclado nos controles incluídos. A informação não deve depender apenas de cor ou animação.

## Artefato e compartilhamento

O formato padrão é um único arquivo HTML — HyperText Markup Language, linguagem de estruturação de páginas — que abra no navegador e funcione sem conexão. Incorpore estilos, scripts, imagens e dados necessários ao próprio arquivo; não dependa de fontes, bibliotecas, renderizadores de diagramas ou imagens carregados da internet.

O guia deve continuar inteligível quando enviado sozinho a outra pessoa. As referências ao código podem apontar para o ambiente original, mas o entendimento não pode depender de abrir esses arquivos. Explique essa limitação de portabilidade quando houver links locais; incorpore os trechos necessários à explicação.

Controles interativos do guia devem operar sobre o conteúdo local. Uma simulação didática não deve executar operações reais do projeto. Não inclua credenciais, segredos ou dados pessoais desnecessários; use exemplos apropriados ao estudo e ao compartilhamento pretendido.

## Conferência e entrega

- Confira coerência entre texto, código e diagramas, incluindo unidades, caminhos, direção dos fluxos e nomes dos componentes.
- Quando a chamada trouxer perguntas, confira se cada uma recebeu uma explicação aprofundada e fácil de localizar no guia. Identifique eventuais lacunas de evidência ou pontos ainda não esclarecidos, sem preencher essas lacunas com suposições apresentadas como fatos.
- Verifique referências internas, recursos incorporados e controles afetados. Confira a leitura e a aparência no navegador quando houver um meio permitido de fazê-lo.
- Se uma forma de verificação não estiver disponível, conclua as demais e registre o limite concreto. Diferencie a avaliação visual do usuário, verificações estáticas e controles realmente executados.
- Entregue o arquivo final com um link e uma orientação breve de uso. Resuma o que o material cobre e qualquer limitação que afete o estudo ou o compartilhamento.

Não trate a geração do documento como prova de domínio do usuário nem como aceite técnico do projeto. O resultado deve oferecer meios claros para estudar, conferir e explicar o trabalho.

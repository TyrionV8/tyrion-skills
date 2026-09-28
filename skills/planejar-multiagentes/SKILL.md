---
name: planejar-multiagentes
description: Use quando o usuário invocar planejar-multiagentes para transformar uma ideia já debatida em uma pasta de planejamento destinada à execução posterior por um orquestrador e vários agentes.
---

# Planejar multiagentes

## Objetivo

Transformar o contexto disponível da conversa e do projeto em um planejamento executável por um orquestrador com vários agentes. Esta skill prepara o planejamento; a execução será iniciada depois pelo usuário com a skill `executar-multiagentes`.

## Como a execução será iniciada

- O orquestrador será iniciado **apenas** pela invocação da skill `executar-multiagentes`, eventualmente acompanhada do caminho do INICIAR.md. O usuário não enviará nenhum outro prompt ou instrução ao orquestrador.
- O orquestrador não terá acesso a esta conversa nem à resposta final dada ao usuário no chat. Tudo o que ele precisar saber deve estar no INICIAR.md ou nos arquivos que ele referencia, inclusive o que surgiu durante a conversa e não está registrado em outro lugar. A resposta final no chat é apenas para o usuário.
- Os executores conhecem apenas as mensagens que o orquestrador lhes enviar e os arquivos que lerem. Regras que valem para eles devem estar também no PLANO.md e em `agentes/<nome>.md`, não só no INICIAR.md.
- No INICIAR.md, trate a invocação da skill como o pedido de execução; não escreva instruções como "aguarde o usuário pedir a execução". As únicas mensagens previstas são as que o orquestrador envia aos executores; se incluir um modelo dessas mensagens, deixe claro que é o orquestrador quem as envia.

## Convenções da execução

Alinhe o INICIAR.md a estas convenções da skill `executar-multiagentes`, sem inventar outros nomes de registro:

- `PROGRESSO.md` na pasta do planejamento: resumo geral, atualizado apenas pelo orquestrador.
- `progresso/<nome>.md` na mesma pasta: um arquivo por agente, atualizado apenas por ele, com tarefa atual, estado, alterações e arquivos envolvidos, verificações e resultados, pendências e próximo passo. O agente atualiza ao concluir uma etapa, encontrar um impedimento ou encerrar o trabalho. Inclua esse arquivo entre os que cada agente pode alterar.
- A declaração de conclusão de um agente não comprova integração e validação; o orquestrador verifica as entregas antes de registrá-las como integradas e validadas.
- Retomada: se os registros já existirem, o orquestrador os lê, confere o estado real do projeto e continua as tarefas pendentes sem refazer o que estiver comprovadamente concluído.
- Se um modelo definido no planejamento estiver indisponível, o orquestrador pergunta ao usuário qual substituto usar; não substitui automaticamente.

## Levantamento e decisões

- Aproveite decisões já confirmadas na conversa, sem exigir nova confirmação.
- Leia automaticamente os arquivos relevantes do projeto para fundamentar o plano e compreender sua organização. A autorização de leitura não autoriza mudanças de implementação.
- Identifique decisões ainda abertas e confirme todas com o usuário antes de concluir o plano. Faça uma pergunta por vez. Não transforme sugestões em decisões confirmadas.
- Sugira modelos para o orquestrador e os executores conforme as tarefas. Confirme a escolha em cada projeto; não fixe Luna como padrão universal.
- Defina com o usuário, em cada planejamento, a autonomia do orquestrador para ajustes durante a execução. Registre no INICIAR.md quais ajustes são permitidos e quais exigem nova decisão do usuário. Não adote uma política fixa para todos os projetos.
- Sugira um local para a pasta de planejamento conforme a organização do projeto e confirme o caminho antes de criá-la.

## Resultado

Use somente instruções Markdown, sem scripts. Produza esta estrutura padrão, adaptando os nomes dos agentes ao projeto:

```text
pasta-do-planejamento/
├── INICIAR.md
├── PLANO.md
└── agentes/
    └── <nome>.md
```

- `INICIAR.md`: ponto de entrada lido pela skill `executar-multiagentes`, com instruções completas para o orquestrador, inclusive início, retomada e registros de progresso.
- `PLANO.md`: objetivo, escopo, decisões, tarefas, dependências e critérios de conclusão.
- `agentes/<nome>.md`: missão, modelo escolhido, entradas, arquivos atribuídos, entregas e verificações de cada agente.

Os arquivos de progresso são criados durante a execução, não no planejamento.

Registre objetivo, escopo, decisões confirmadas, tarefas, dependências, responsabilidades, modelos escolhidos, critérios de conclusão, orientações de integração e verificação dos resultados.

O INICIAR.md é o ponto de entrada autossuficiente para um orquestrador que não recebeu a conversa original. Inclua o contexto necessário, a identificação do projeto, referências aos arquivos do plano e instruções suficientes para iniciar, retomar, distribuir, acompanhar, integrar e verificar o trabalho. Nenhuma instrução essencial pode depender de mensagens do chat. Antes de concluir, confira se algo que o orquestrador ou os executores precisam saber aparece apenas na conversa ou na resposta que você pretende dar ao usuário; se aparecer, registre nos arquivos do plano.

A distribuição deve distinguir tarefas independentes de tarefas que aguardam resultados de outras. Especifique quais arquivos cada agente poderá alterar e como seus resultados serão integrados.

## Limites

Não execute o plano nem crie agentes executores durante o planejamento.

Não inclua mecanismos para descobrir ou selecionar entre diferentes planejamentos: isso pertence à skill `executar-multiagentes`.

Não conclua um planejamento com decisões não confirmadas apresentadas como definitivas.

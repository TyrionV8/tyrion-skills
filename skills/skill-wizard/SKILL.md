---
name: skill-wizard
description: Entrevista o usuário, uma pergunta por vez, para criar ou melhorar skills do Codex. Produz rascunhos editáveis em /tmp, analisa edições manuais e propõe instruções e recursos auxiliares antes de pedir autorização para instalar as mudanças.
---

# Skill Wizard

Conduza uma entrevista analítica e criativa para criar uma skill ou melhorar uma existente. Faça propostas, examine suas consequências e critique problemas concretos. A decisão final sobre o conteúdo e a instalação é do usuário.

## Condução e continuidade obrigatória

Guie o usuário ativamente até o resultado desejado. Não deixe que ele precise perguntar "e agora?" ou cobrar a execução para que o processo avance.

Após cada resposta, incorpore a decisão e avance no mesmo turno: faça a próxima pergunta necessária ou realize a próxima etapa autorizada. Pode pedir autorização para começar o rascunho; isso é uma pergunta válida. Se essa autorização já foi dada e não restarem decisões necessárias, comece ou atualize os arquivos em `/tmp`, sem pedir novamente.

Não encerre um turno apenas reconhecendo a resposta, resumindo decisões ou prometendo agir depois. Uma frase como "vou preparar o rascunho" exige execução no mesmo turno; não substitui uma ação nem uma pergunta.

Mantenha a entrevista enquanto houver decisões relevantes para resolver. Assim que não houver, inicie a implementação do rascunho ou pergunte se pode iniciá-la. Não invente perguntas para prolongar a entrevista. Se um ajuste solicitado abrir novas decisões, retome as perguntas sobre elas e volte à implementação assim que forem resolvidas.

Quando o rascunho estiver pronto, apresente o resultado concreto e conduza o usuário à revisão e à autorização de instalação previstas nesta skill. Depois da autorização, prossiga com a instalação e a validação.

Antes de encerrar um turno enquanto o trabalho estiver em andamento, confira se há uma pergunta explícita aguardando resposta ou uma etapa efetivamente realizada com o próximo passo claro. Se ainda puder avançar sem resposta do usuário, continue. Se depender dele para revisar, decidir ou autorizar, faça a pergunta correspondente; não deixe essa dependência implícita.

Se houver um impedimento real, conclua o trabalho independente possível, explique o impedimento e peça a ação ou informação necessária para continuar. Respeite pedidos de pausa e encerramento. A regra de continuidade não autoriza ultrapassar permissões nem continuar depois que o usuário declarar que terminou.

## Início da entrevista

Se a chamada não for a primeira mensagem da sessão, pergunte primeiro se o usuário quer usar as mensagens recentes do chat como fonte para a skill. Se ele quiser, use apenas o contexto disponível e confirme interpretações importantes antes de transformá-las em instruções permanentes. Se não quiser, conduza a entrevista a partir das informações que ele fornecer.

Faça uma pergunta por vez. Aproveite respostas já dadas e não siga um questionário fixo quando uma pergunta deixar de ser útil.

Investigue o objetivo, as situações que devem selecionar a skill, as entradas, os resultados esperados, os limites e os exemplos que realmente ajudem a defini-la. Apresente ideias próprias e alternativas quando elas puderem melhorar o resultado. Distinga decisões confirmadas de sugestões ainda abertas; implemente apenas decisões concretas.

## Opções de resposta

Quando houver escolhas claras, apresente duas ou três opções curtas e selecionáveis pela ferramenta de perguntas disponível. Inclua uma frase breve sobre a consequência de cada escolha quando isso ajudar. Mantenha a possibilidade de resposta livre. Não transforme perguntas abertas em alternativas artificiais e não repita perguntas que o usuário já respondeu.

Se a interface não oferecer opções selecionáveis, apresente uma lista numerada no chat e aceite também respostas em palavras próprias. Não prometa seleção múltipla quando a ferramenta só aceitar uma opção; nesse caso, faça perguntas separadas ou peça que o usuário escreva os números desejados. Trate uma resposta de teste ou ambígua como tal e confirme seu significado antes de convertê-la em decisão permanente.

Exemplo de pergunta: "Como prefere revisar o rascunho?" Opções: "Trechos no chat", "Arquivo temporário" e "Ambos". O usuário pode responder com outra preferência.

## Skill nova ou existente

Quando encontrar uma skill possivelmente semelhante, informe qual é e explique a semelhança. Ofereça a escolha entre criar uma skill nova e melhorar a existente. O usuário também pode pedir essa mudança de direção durante a entrevista.

Antes de passar a editar uma skill existente, inclusive esta própria skill, identifique o alvo e peça confirmação explícita. Leia seus arquivos e preserve o conteúdo que continua útil. Prepare as mudanças em cópias temporárias e apresente as diferenças para revisão. Não altere a instalação existente durante a entrevista.

## Rascunhos editáveis

Crie um diretório exclusivo em `/tmp` e informe seu caminho. Mantenha nele os arquivos propostos, atualizando-os conforme as decisões forem tomadas. O usuário pode editá-los manualmente a qualquer momento.

Antes de cada alteração, releia os arquivos. Compare o estado atual com a última versão escrita pelo assistente. Trate edições manuais como a preferência mais recente do usuário sobre o estado anterior e preserve-as ao incorporar novas respostas.

Analise também as edições manuais: aponte ambiguidades, contradições, seleção excessivamente ampla, instruções frágeis ou riscos concretos. Proponha correções com franqueza. Se a correção contrariar uma preferência expressa pelo usuário, aguarde sua decisão antes de aplicá-la. Não confunda uma crítica com autorização para reverter a edição.

Após atualizar um rascunho, informe quais arquivos mudaram e seus caminhos.

## Instruções e recursos auxiliares

Decida com o usuário, quando a escolha for relevante, quanto da skill deve ser orientação para o agente e quanto deve ser executado por scripts ou dados estruturados. Explique o efeito dessa escolha sobre consistência, flexibilidade e manutenção. Não acrescente scripts apenas para tornar uma tarefa simples mais elaborada.

Sugira scripts quando a repetição, a precisão ou a necessidade de resultados consistentes justificar código. Prefira inicialmente scripts de shell (`.sh`); use Python quando o shell tornaria a solução frágil ou difícil de manter. Use outra linguagem quando essas opções não forem adequadas. Sugira arquivos Markdown (`.md`) ou JavaScript Object Notation (`.json`, formato de dados estruturados) quando ajudarem a organizar referências, configurações ou dados da skill.

Mantenha o arquivo `SKILL.md` focado nas decisões e instruções essenciais. Crie arquivos auxiliares somente quando tiverem uma função definida. Verifique o funcionamento de scripts propostos antes da instalação.

## Local padrão das skills

Por padrão, mantenha os arquivos de origem das skills em `~/repos/tyrion-skills/skills/` quando puderem ser públicos, ou em `~/repos/tyrion-private-skills/skills/` quando contiverem informações privadas ou específicas de ambientes restritos. Use a localização escolhida explicitamente pelo usuário quando houver uma. Não deixe a única cópia em `~/.codex/skills/`: nesse diretório, instale a skill por atalho simbólico para o repositório correspondente.

## Revisão e instalação

Quando houver informação suficiente, apresente o nome, a descrição de seleção, os arquivos propostos e, ao editar uma skill existente, as diferenças em relação à versão instalada. Antes de instalar, mostre no chat pelo menos um exemplo concreto de uso e um trecho representativo da instrução proposta, para que o usuário veja o comportamento esperado sem abrir o arquivo. Convide o usuário a revisar os rascunhos. Releia-os após cada revisão manual.

Os arquivos em `/tmp` são rascunhos, não uma instalação. Antes de instalar uma skill nova ou substituir arquivos de uma skill existente, mostre exatamente quais arquivos serão afetados e peça autorização explícita para essa ação.

Depois da autorização, releia os rascunhos, instale somente os arquivos aprovados e valide a estrutura. Se houver alterações nos arquivos instalados desde a comparação apresentada ao usuário, examine-as e obtenha uma nova decisão antes de sobrescrevê-las.

Ao concluir a instalação, informe quais arquivos foram criados ou alterados, o resultado da validação e qualquer verificação que não tenha sido possível fazer. Explique brevemente para que serve a skill e como chamá-la. Mostre um exemplo concreto e simples de uso, adaptado à skill criada ou editada.

Por fim, pergunte se o usuário quer aprender a usá-la passo a passo ou receber mais exemplos adequados às suas funções. Se ele aceitar, forneça a explicação ou os exemplos solicitados.

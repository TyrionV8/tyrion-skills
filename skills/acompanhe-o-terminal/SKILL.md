---
name: acompanhe-o-terminal
description: Acompanha a saída do terminal da conversa e orienta os próximos passos enquanto o usuário executa os comandos. Use somente quando o usuário pedir explicitamente acompanhamento contínuo ou invocar esta skill.
---

# Acompanhe o terminal

O usuário executa os comandos; o agente lê os resultados e guia a atividade sem exigir mensagens como “feito”. A invocação autoriza consultas periódicas, não a execução de comandos.

## Início e leitura

- Aproveite o objetivo e as decisões já presentes na conversa. Pergunte pelo objetivo somente se faltar contexto necessário.
- Consulte o terminal desta conversa com `mcp__codex_app__read_thread_terminal`, quando disponível. Confira o diretório e a última saída; não suponha que o diretório informado nos metadados represente o diretório atual após um `cd` visível no texto.
- Explique que o acompanhamento consiste em consultas de texto durante o turno ativo. Não prometa transmissão contínua, observação de outros terminais ou acompanhamento em segundo plano.
- Se a ferramenta não estiver disponível ou o terminal necessário não estiver acessível, informe a limitação e peça a saída relevante; não alegue estar vendo o terminal.

## Ciclo de acompanhamento

1. Leia a saída e identifique o que mudou desde a consulta anterior. Não repita orientações por causa de conteúdo antigo no histórico.
2. Ao terminar um comando, explique seu resultado e indique o próximo comando compatível com o objetivo. Informe o diretório, explique as partes e use comentários nos blocos copiáveis. Defina termos técnicos e siglas quando aparecerem pela primeira vez.
3. Aguarde de forma interrompível, em geral entre 5 e 15 segundos, e consulte novamente. Amplie o intervalo até 30 segundos se não houver novidade; não use esperas superiores a 60 segundos.
4. Continue no mesmo turno sem exigir “feito”. Não encerre a resposta apenas para aguardar a execução de um comando já orientado. Durante esperas longas, dê uma atualização breve em até 60 segundos, sem despejar a mesma saída ou inventar progresso.
5. Diante de erro ou pergunta interativa, explique a situação antes de orientar outra tentativa. Não confunda ausência de saída, botão de retorno do shell ou texto antigo com prova de sucesso; confirme a evidência pertinente.

## Limites e encerramento

- Não digite no terminal, execute comandos ou altere arquivos neste modo. Se o usuário pedir execução, trate isso como uma mudança explícita de modo e escopo; não a deduza do silêncio.
- Não solicite senhas, tokens ou códigos de autenticação pelo chat. Em etapas manuais, explique o que o usuário deve fazer e acompanhe a saída disponível.
- Pare quando o usuário pedir, a atividade combinada terminar ou surgir uma decisão que realmente exija resposta. Não reinicie o acompanhamento em outra atividade sem novo pedido.
- Se uma limitação de ferramenta ou de sessão impedir a continuidade, informe que o acompanhamento terminou ou foi interrompido; não prometa que continuará após a resposta final.

Exemplo: “Use $acompanhe-o-terminal enquanto eu preparo minha branch; me explique a saída e indique cada próximo comando.”

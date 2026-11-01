---
name: use-o-terminal-comigo
description: Colabora pelo terminal, acompanhando a saída e executando comandos dentro do objetivo autorizado, com explicações e passagem das etapas manuais ao usuário. Use somente quando o usuário pedir explicitamente este modo ou invocar esta skill.
---

# Use o terminal comigo

Alterne observação, explicação e execução para avançar no objetivo combinado, sem exigir “feito” quando a conclusão puder ser constatada pelas ferramentas.

## Defina o contexto real

- Aproveite o objetivo, as decisões e as permissões da conversa. Pergunte somente pelo que faltar para executar a próxima ação.
- Leia o terminal desta conversa com `mcp__codex_app__read_thread_terminal`, quando disponível, e confira a saída atual. Após um `cd`, verifique o diretório efetivo; os metadados do terminal podem conservar o diretório inicial.
- Verifique quais ferramentas realmente permitem executar comandos. Uma ferramenta de leitura não permite digitar. Se a execução ocorrer em uma sessão separada, informe isso e forneça explicitamente o diretório e os parâmetros necessários; não presuma compartilhar variáveis, ambiente virtual ou estado de um comando interativo do terminal do usuário.
- Se uma capacidade necessária estiver indisponível, informe a limitação e forneça o comando para execução manual, com diretório, finalidade e resultado esperado.

## Trabalhe junto com o usuário

- Antes de executar, explique brevemente a ação, o comando e seus efeitos. Use comentários quando ajudarem a compreender comandos maiores e defina siglas e termos técnicos na primeira ocorrência.
- Execute as ações necessárias dentro do escopo autorizado e verifique os resultados. Não transforme esta skill em autorização geral para alterar arquivos, fazer commit, enviar mudanças ou realizar ações externas; respeite as permissões específicas da conversa.
- Evite executar simultaneamente com o usuário comandos que disputem os mesmos arquivos, o estado do Git ou a entrada de uma sessão. Indique quem fará o próximo passo; após uma etapa manual, volte a verificar antes de continuar.
- Para ações destrutivas, solicite confirmação explícita. Preserve alterações locais e não sobrescreva trabalho existente para facilitar o fluxo.
- Quando precisar de senha, autenticação interativa ou outra ação exclusivamente humana, conclua primeiro as etapas independentes e apresente “Ação manual necessária”, com instruções exatas e verificação aplicável. Não peça credenciais pelo chat.

## Acompanhamento durante o turno

- Durante comandos manuais ou demorados, consulte periodicamente a saída ou o estado da sessão. Espere de forma interrompível, em geral entre 5 e 15 segundos; amplie até 30 segundos sem novidades e nunca bloqueie por mais de 60 segundos.
- Compare com a leitura anterior. Ao surgir conclusão, erro ou pergunta interativa, interprete o resultado e avance ou oriente a intervenção adequada. Não repita comandos porque a saída ainda não mudou.
- Não exija “feito” quando houver evidência observável de conclusão. Se uma informação ou decisão depender do usuário, pergunte explicitamente; silêncio não é aprovação.
- Dê atualizações breves em até 60 segundos durante atividade prolongada. As consultas são pontuais e só existem durante o turno ativo; não prometa observação contínua da tela ou trabalho em segundo plano.
- Pare quando o usuário pedir ou o objetivo terminar. Se não puder manter a sessão ativa, informe a interrupção. Não reinicie este modo em outra atividade sem novo pedido.

Exemplo: “Use $use-o-terminal-comigo para preparar a contribuição. Execute as verificações e me guie nas etapas que eu precisar fazer.”

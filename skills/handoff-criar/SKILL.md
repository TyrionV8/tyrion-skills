---
name: handoff-criar
description: Gera um documento em português para continuar a conversa em outra sessão ou agente. Use ao pedir handoff-criar ou preparar uma passagem de contexto, com foco opcional para a próxima sessão.
---

# Criar handoff

Handoff é um documento de passagem de contexto. Gere-o a partir da conversa disponível; não tente recuperar todo o histórico privado dos agentes. Argumentos descrevem o foco da próxima sessão, salvo destino explicitamente informado.

## Preparação e conteúdo

Leia as regras centrais em `~/repos/agentes/memoria.md`, `arquitetura.md` e `handoffs/instrucoes.md`, além do `instrucoes.md` do assunto quando existir. Reutilize leituras atuais já feitas nesta conversa. O destino explícito prevalece; no padrão, use `handoffs/`, ou `handoffs/tmp/` quando temporário. Não apague temporários automaticamente.

Escreva um documento curto, mas suficiente para continuar, cobrindo apenas o que se aplica:

- Objetivo, foco da próxima sessão e escopo autorizado. Separe decisões confirmadas de propostas e perguntas pendentes.
- Projeto, pasta absoluta de trabalho, ramo de desenvolvimento e referência da sessão quando disponíveis. Não invente identificadores.
- Situação: inspecionado, alterado e validado, com evidências e limitações. Destaque alterações locais não publicadas e trabalho de outras sessões a preservar.
- Decisões e correções do usuário que mudam a próxima ação; tentativas malsucedidas relevantes para evitar repetição.
- Referências absolutas ou endereços para planos, especificações, mudanças e outros artefatos. Resuma só o necessário para orientar a leitura; não duplique esses materiais.
- Próximo passo concreto, sequência restante, impedimentos e decisões pendentes. Comandos úteis devem indicar diretório, efeito e verificação; não incluir comandos destrutivos como execução automática.
- **Skills sugeridas**: nomes reais, finalidade na retomada e caminho conhecido. Recomende apenas as pertinentes; não copie suas instruções. Quem recebe deve carregá-las pelo mecanismo disponível em sua ferramenta.

Remova segredos e dados pessoais desnecessários antes de gravar. O script não anonimiza o texto. Não leia credenciais para completar o documento. Não declare verificações novas sem executá-las; prefira marcar evidências antigas com sua data a iniciar uma auditoria ampla apenas para gerar o handoff.

## Gravação pelo script

Execute `scripts/handoff.py` relativo à pasta real desta skill, resolvendo links simbólicos. Não reimplemente nomeação ou inventário. O script usa apenas Python 3.9+ e sua biblioteca padrão; gera metadados e o nome `handoff_AAAA-MM-DD_HH-MM-SS_tema.md` em São Paulo, protegendo contra sobrescrita.

Exemplo (substitua o caminho da skill e os valores):

```bash
# O documento entra diretamente pela entrada padrão, sem arquivo auxiliar.
# O delimitador entre aspas impede que o terminal execute expressões do texto.
python3 /caminho/real/handoff-criar/scripts/handoff.py criar \
  --tema 'chat de transcrição' \
  --projeto 'niahub' \
  --trabalho '/caminho/absoluto/do/projeto' <<'HANDOFF_CONTEUDO'
# Continuidade do chat de transcrição

Conteúdo redigido conforme as instruções acima.
HANDOFF_CONTEUDO
```

Use `--temporario` se solicitado e `--destino '/diretorio'` para destino explícito. Para testar ou usar outra base, `--raiz '/diretorio'` vem antes de `criar`. Se o usuário indicar um nome exato de arquivo, respeite-o por criação exclusiva, sem sobrescrever, e mantenha os metadados; a opção `--destino` designa somente diretório.

Confira o resultado estruturado e a leitura do arquivo criado. Entregue o caminho e uma chamada copiável `/handoff-retomar /caminho/arquivo.md`. Criar o documento não inicia outra sessão nem executa o trabalho restante.

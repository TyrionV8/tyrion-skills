---
name: conectar-drift
description: Conecta o agente ao editor de vídeo Drift pelo MCP. Confere se o Drift está aberto, lê o token no próprio Drift, testa a conexão e corrige as configurações do Antigravity, Claude Code e Codex. Use quando o usuário pedir para conectar o Drift, quiser editar vídeos nele ou quando as ferramentas do Drift falharem ou não aparecerem.
---

# Conectar Drift

O Drift é um editor de vídeo que oferece um servidor MCP (*Model Context Protocol*, protocolo que liga agentes a ferramentas externas) em `http://127.0.0.1:4731/mcp`. O acesso exige um token salvo pelo Drift em `~/.config/CutWire Drift/CutWire Drift.conf`, seção `[mcp]`.

## Token

- O token é uma credencial. Não o exiba, não o peça e não o escreva no chat, em handoffs, relatórios ou arquivos versionados.
- Quem lê o token é o script, a cada execução. Ele grava o token somente nas configurações locais dos agentes. Se o usuário colar o token no chat, não o repita.

## 1. Verificar e configurar

Execute o script desta skill, usando o caminho relativo à pasta dela:

```bash
python3 scripts/drift_mcp.py configurar
```

O script confere se o Drift está aberto, lê o token e testa a conexão. Depois, compara a entrada `drift` destes arquivos:

- Antigravity: `~/.gemini/config/mcp_config.json`
- Claude Code: `$CLAUDE_CONFIG_DIR/.claude.json` ou `~/.claude.json`
- Codex: `$CODEX_HOME/config.toml` ou `~/.codex/config.toml`

Ele corrige somente essa entrada e faz um backup `*.bak-conectar-drift-<data>` antes de alterar um arquivo. Os links simbólicos são preservados. Se a conexão não for confirmada, nada é alterado. Use `verificar` no lugar de `configurar` para diagnosticar sem alterar arquivos. A opção `--url` ou a variável `DRIFT_MCP_URL` mudam o endereço.

## 2. Interpretar o resultado

A última linha informa o resultado:

- `RESULTADO: pronto`: a conexão funciona. Siga para a etapa 3.
- `RESULTADO: falha=<código>`: a conexão falhou. Apresente ao usuário, como **Ação manual necessária**, as orientações listadas em `O QUE FAZER`, explicando cada passo. Aguarde a resposta ("feito" ou a saída de um comando), execute o script outra vez e continue.

| Código | Significado |
|---|---|
| `drift_fechado` | O Drift não está aberto |
| `mcp_desligado` | O Drift está aberto, mas o servidor MCP não responde no endereço |
| `token_recusado` | O token salvo no Drift não é o que o servidor usa |
| `drift_sem_configuracao` / `drift_sem_token` | O Drift não foi aberto ainda, ou o MCP está desativado |

Nunca abra, feche nem reinicie o Drift sem autorização. Projetos abertos podem ter alterações ainda não salvas.

Comunique as linhas `[alterado]`. Um agente só carrega as ferramentas do Drift ao iniciar. Se a configuração do agente atual mudou, as ferramentas aparecem depois de reiniciá-lo ou de abrir uma nova conversa. Até lá, use o modo `chamar`.

## 3. Usar o Drift

Use as ferramentas MCP do servidor `drift` se estiverem disponíveis nesta sessão. Exemplos: `call_mcp_tool` com servidor `drift` no Antigravity, ou `mcp__drift__*` no Claude Code. Se não estiverem, chame o Drift pelo script:

```bash
python3 scripts/drift_mcp.py chamar inspect '{"clips":true}'
python3 scripts/drift_mcp.py chamar apply '{"ops":[{"tool":"...","args":{}}]}'
```

O modo `chamar` mostra o texto da resposta e salva as imagens (por exemplo, de `frames` e `capture`) em `/tmp/drift-mcp/`, informando o caminho. Abra essas imagens para ver o vídeo. A saída termina com código 1 quando a ferramenta retorna erro.

Antes de editar, carregue o guia completo do próprio Drift com `catalog({"guide":true})`. Ele substitui qualquer resumo e acompanha a versão instalada. Pontos essenciais:

- Fluxo: `catalog` ou `search({q})` para achar a operação; `toolbox({name})` ou `toolbox({ops:[…]})` para os esquemas; `apply({ops:[{tool,args},…]})` para editar. Um lote de `apply` gera um único passo de desfazer. `apply` não é atômico: em caso de falha, as operações anteriores permanecem aplicadas, e `done` lista quais foram executadas.
- Estado: `inspect({clips:true, detail:true})` mostra UUIDs de clipes, seleção, histórico de desfazer e trabalhos em andamento.
- Imagens: `activity()` mostra onde o conteúdo muda; `frames()` gera uma folha de contato; `capture({at})` gera um quadro em tamanho real. Verifique as edições visualmente.
- Convenções: tempos em segundos; a trilha 0 fica no topo. Identifique clipes por UUID, pois trilha e índice mudam com as edições. Operações de seleção exigem `select_clip` antes.
- Mídia: `import_media` aceita somente caminhos absolutos, e o Drift não lista pastas. Localize os arquivos com as ferramentas do agente (`find`, `ls`) e confira que `missing` volte vazio.
- Trabalhos assíncronos (exportação, legendas, cenas, transcrição etc.) retornam logo. Acompanhe-os por `inspect({detail:true})` ou `get_job({id})`, conforme o guia.

Antes de ações difíceis de desfazer, como exportar sobre um arquivo existente, apagar efeitos do usuário ou baixar mídia paga do *market*, confirme com o usuário.

## Relato ao usuário

Informe o resultado de cada etapa e separe o que foi verificado do que foi alterado. Indique quais agentes precisam ser reiniciados. Mostre os backups criados.

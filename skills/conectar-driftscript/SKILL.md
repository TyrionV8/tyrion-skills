---
name: conectar-driftscript
description: Edita o vídeo aberto no CutWire Drift através do texto e da transcrição do addon DriftScript, ou conecta e gerencia o addon via CLI e MCP. Use quando o usuário quiser editar vídeo por texto, cortar palavras, encurtar silêncios ou sílabas esticadas, acelerar trechos, analisar vícios de fala ou conectar o DriftScript.
---

# Conectar e Editar com DriftScript

O **DriftScript** é um addon de edição de vídeo por texto integrado ao editor **CutWire Drift**. Ele roda como servidor local em `http://127.0.0.1:4732` (com endpoint MCP em `http://127.0.0.1:4732/mcp`) e oferece um utilitário CLI em `/home/davi/repos/DriftScript/driftscript_cli.py`.

Ao editar o texto no DriftScript, as alterações refletem e sincronizam automaticamente na timeline do Drift em um único passo de desfazer (*Undo*).

---

## Regras e Estrutura dos Tokens

1. **Palavras removidas não somem**:
   - Palavras cortadas ficam riscadas (`deleted: true`) e mantêm seu índice de posição original na transcrição.
   - Podem ser restauradas / desriscadas a qualquer momento (`deleted: false` ou via `driftscript_restore_words`).

2. **Silêncios e Pausas**:
   - Decompostos em micro-tokens:
     - `•` (1 pontinho = 0,05s de silêncio).
     - `—` (1 traço = 10 pontinhos = 0,50s; a partir de 12 pontinhos, exibe sempre `•` no início e no fim).
     - `• (tempo) •` para pausas longas (> 4 traços / 2,0s).
   - Você pode riscar ou acelerar apenas alguns pontinhos ou traços intermediários (`pause_pos == 'inner'`) para encurtar parte do silêncio sem eliminar a respiração natural.

3. **Sílabas esticadas / alongadas**:
   - Aparecem como tokens `〰` (`kind: 'stretch'`, ex.: `〰0.35s`) posicionados imediatamente após a palavra esticada.
   - Riscar o token `〰` (`deleted: true`) encurta o excesso da sílaba esticada sem cortar a palavra em si.

---

## Formas de Execução

Você pode executar as operações de duas maneiras:
- **Nativamente via MCP**: se o servidor `driftscript` estiver registrado e carregado no seu agente (`call_mcp_tool` no Antigravity ou ferramentas equivalentes).
- **Via Terminal (CLI)**: através do script `/home/davi/repos/DriftScript/driftscript_cli.py`, útil quando o servidor MCP não estiver carregado na sessão atual.

---

## Comandos Rápidos e Fluxo de Trabalho

### 1. Verificar Status e Memória VRAM da GPU
Consulta o uso de VRAM (memória de vídeo da placa gráfica), memória RAM do sistema e o modelo Whisper carregado (*fast*, *normal* ou *heavy*):

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py status
```

### 2. Ler Transcrição com Índices `[idx]`
Obtém a lista de palavras numeradas com seus respectivos índices:

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_get_transcript '{"max_words":800}'
```
*Dica:* Use o campo `offset_words` para navegar em transcrições mais longas.

### 3. Analisar Vícios de Linguagem, Repetições e Pausas
Detecta hesitações ("é", "hum"), palavras de preenchimento ("tipo", "né"), gagueiras/repetições imediatas e pausas excessivas:

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_analyze_fillers '{"min_pause_sec":0.4}'
```

### 4. Riscar Palavras, Silêncios ou Esticadas (Cortar Trechos)
Marca palavras, intervalos ou tokens de silêncio/alongamento como removidos. A alteração sincroniza na timeline do Drift:

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_cut_words '{"indices":[10,11],"ranges":[[20,25]],"deleted":true}'
```

Para desfazer o corte de palavras ou intervalos específicos:
```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_restore_words '{"indices":[10,11],"ranges":[[20,25]]}'
```
Ou restaurar todo o vídeo de uma vez:
```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_restore_words '{"restore_all":true}'
```

### 5. Acelerar Trechos em vez de Cortar (2x a 32x)
Acelera palavras, pausas ou esticadas (velocidades suportadas: `2.0`, `4.0`, `8.0`, `16.0`, `32.0`), mantendo a fluidez visual sem cortar o áudio/vídeo:

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_accelerate_words '{"ranges":[[30,45]],"speed":2.0}'
```

### 6. Colorir o Medidor de Relevância
Aplica marcação semântica de relevância por cores na interface web do DriftScript (ou use a skill especializada `analisar-relevancia-da-transcricao`):

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_set_relevance '{"annotations":[{"start_index":0,"end_index":45,"score":0.95,"category":"relevant","reason":"Objetivo principal"},{"start_index":46,"end_index":80,"score":0.0,"category":"off_topic","reason":"Desvio"}]}'
```

### 7. Navegar (Seek) no Player e na Timeline do Drift
Posiciona o cursor de reprodução (*playhead*) exatamente no início da palavra correspondente:

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py chamar driftscript_seek_word '{"word_index":50}'
```

---

## Configuração do MCP nos Agentes

Para que as ferramentas do DriftScript fiquem disponíveis nativamente como ferramentas MCP nos assistentes (Antigravity, Claude Code e Codex):

```bash
python3 /home/davi/repos/DriftScript/driftscript_cli.py configurar-mcp
```

O comando registra o servidor `driftscript` (`http://127.0.0.1:4732/mcp`) em:
- **Antigravity**: `~/.gemini/config/mcp_config.json`
- **Claude Code**: `$CLAUDE_CONFIG_DIR/.claude.json` ou `~/.claude.json`
- **Codex**: `$CODEX_HOME/config.toml` ou `~/.codex/config.toml`

Um backup automático com data/hora (`.bak-driftscript-...`) é preservado antes de alterar qualquer arquivo. Após configurar, reinicie o assistente ou inicie uma nova conversa para carregar as ferramentas no catálogo.

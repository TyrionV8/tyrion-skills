---
name: audioscripter
description: Opera e edita projetos no AudioScripterAI via MCP (http://127.0.0.1:4740/mcp) ou HTTP JSON-RPC. Use quando o usuário pedir para abrir/salvar projetos, importar ou organizar tracks, transcrever com WhisperX, limpar vícios de linguagem e pausas, acelerar falas, corrigir vocabulário técnico, aplicar limpeza de voz IA (DeepFilterNet3/RNNoise) e nivelamento LUFS, marcar relevância ou exportar áudio e legendas sincronizadas.
---

# Operar AudioScripterAI via MCP

Use esta skill para operar e editar áudios multipista pela transcrição no **AudioScripterAI** (editor standalone em Rust no estilo Descript, com cortes fluidos por *Zero-Crossing*, *Micro-Crossfade Equal-Power* e preenchimento de *Room Tone*).

- **Endpoint MCP padrão**: `http://127.0.0.1:4740/mcp` (a porta padrão `4740` pode variar por sessão caso o aplicativo seja iniciado com `--mcp-port <porta>`).
- **Verificação de saúde**: `GET http://127.0.0.1:4740/health`
- **Prompt dinâmico com estado atual**: `GET http://127.0.0.1:4740/prompt` ou via MCP `prompts/get` com `name: "audioscripter_operacao"`.

---

## Mapa Completo das 21 Ferramentas MCP

### 1. Projeto, Mídia e Inspeção

- `audioscripter_status`: retorna status ao vivo do projeto aberto, `active_track_idx`, playhead, `playback_speed`, contagem de mídias/vocabulário e telemetria de hardware (CPU, RAM, GPU/VRAM e porta MCP ativa).
- `audioscripter_project`: consulta metadados do projeto (`action: "info"`), salva (`action: "save"`, `path` opcional se o projeto já tiver caminho) ou abre arquivos `.asproj.json` (`action: "open"`, `path`).
- `audioscripter_list_tracks`: lista todas as tracks do projeto com duração original/editada, `offset_sec`, ganho, pan, mute/solo, efeitos de IA, contagem de tokens/clipes e disponibilidade de undo/redo.
- `audioscripter_manage_track`: seleciona a track ativa (`set_active: true`) ou altera `name`, `offset_sec`, `gain_db` (`-36.0` a `18.0`), `pan` (`-1.0` a `+1.0`), `muted` e `solo` na `track_index` informada.
- `audioscripter_media_pool`: gerencia o painel Arquivos com `action`:
  - `"list"`: lista os arquivos carregados na biblioteca de mídia.
  - `"set_sort"`: ordena por `sort_mode` (`"import_order"` | `"alphabetical"` | `"duration_asc"` | `"duration_desc"`).
  - `"add_series"`, `"add_new_track"`, `"add_all_series"`: insere item(ns) na timeline usando `asset_id` (preferencial) ou `asset_index`.
- `audioscripter_import_track`: importa áudio ou vídeo para a biblioteca e timeline (`file_path` obrigatório; `name`, `offset_sec` padrão `0.0`, e `mode`: `"series"` para sequência na track ativa, `"overlay"` para nova track sobreposta ou `"pool_only"` apenas no painel Arquivos).
- `audioscripter_transcribe`: transcreve uma track usando GPU CUDA (WhisperX + Wav2Vec2) com vocabulário técnico salvo e refinamento acústico de 10 ms (`track_index`, `mode`: `"fast"` | `"normal"` | `"heavy"`, `language` padrão `"pt"`), com progresso e cancelamento sincronizados com a interface.
- `audioscripter_get_transcript`: lê tokens indexados com paginação (`track_index`, `offset`, `limit` de `1` a `3000`, `compact: true` para retornar apenas `formatted_transcript` e metadados de paginação `has_more` e `next_offset`).

### 2. Análise, Edição por Texto, Histórico e Navegação

- `audioscripter_analyze_speech`: detecta vícios de linguagem (`é`, `hum`, `tipo`, `né`), repetições/gagueiras, hesitações, sílabas esticadas, pausas longas (`min_pause_sec`, padrão `0.6`) e palavras de baixa confiança em `track_index`.
- `audioscripter_cut_tokens`: aplica cortes não-destrutivos por `indices` e/ou `ranges` (`[[inicio, fim]]` inclusivo) em `track_index`.
- `audioscripter_restore_tokens`: restaura tokens previamente riscados por `indices`, `ranges` ou `restore_all: true` em `track_index`.
- `audioscripter_shorten_pauses`: reduz grupos de pausas longas acima de `min_pause_sec` (padrão `0.6`) para `target_pause_sec` (padrão `0.2`), preservando as bordas de respiração; aceita `ranges` opcional e `track_index`.
- `audioscripter_accelerate_tokens`: acelera trechos específicos (`indices`, `ranges`, `speed` de `0.5` a `4.0`, padrão `2.0`) preservando timbre via WSOLA em `track_index`.
- `audioscripter_edit_token`: corrige pontualmente o texto de um token (`token_index` + `new_text`) ou em lote (`edits: [{token_index, new_text}]`) em `track_index`, sem alterar o dicionário global de vocabulário.
- `audioscripter_history`: desfaz (`action: "undo"`) ou refaz (`action: "redo"`) até `steps` (`1` a `50`) edições na `track_index` ativa ou informada.
- `audioscripter_set_relevance`: marca relevância semântica com `annotations: [{start_index, end_index, category: "relevant"|"medium"|"low"|"off_topic", score, reason}]` em `track_index`.
- `audioscripter_seek`: move o cursor da timeline (playhead) para `word_index` ou `timeline_sec` (com `track_index` opcional).

### 3. Vocabulário Técnico Persistente

- `audioscripter_add_vocab_correction`: corrige um termo técnico errado (`canonical` obrigatório, com `token_indices`, `wrong_text`, `category`, `notes`, `apply_all_matching` padrão `true` e `track_index`) e salva no dicionário persistente (`~/.local/share/audioscripter-ai/vocabulary.json`) para futuras transcrições.
- `audioscripter_list_vocab`: lista todas as entradas e aliases do dicionário de vocabulário técnico salvo.

### 4. Limpeza de Voz IA e Exportação

- `audioscripter_set_audio_fx`: configura efeitos na `track_index`:
  - `denoise_mode`: `"off"` | `"fast"` (RNNoise leve) | `"studio"` (DeepFilterNet3 48 kHz)
  - `denoise_strength`: `0.0` a `1.0`
  - `leveler_enabled`: `true`/`false` com `target_lufs` (ex.: `-16.0` para voz/YouTube)
  - `seamless_cuts`: `true`/`false` e `room_tone_enabled`: `true`/`false`
- `audioscripter_export`: exporta para `output_path` no `format` desejado:
  - Áudio: `wav24`, `wav32f`, `flac`, `mp3`, `m4a`, `ogg`
  - Transcrição ou legenda sincronizada: `txt`, `txt_ts`, `srt`, `vtt`, `lrc`, `json`

---

## Regras dos Tokens e Naturalidade de Edição

1. **Edição não-destrutiva**:
   - Palavras usam índice `[idx]`.
   - Cortes aparecem riscados como `~palavra~` (`deleted: true`) e acelerações como `palavra(1.50x)`, mantendo o `[idx]` original para restauração via `audioscripter_restore_tokens` ou reversão via `audioscripter_history`.
2. **Pausas granulares (`•`, `—`, `(Xs)`)**:
   - `•` = 50 ms; `—` = 500 ms; `(Xs)` = pausa longa (> 2,1 s).
   - **Preserve a respiração natural**: prefira `audioscripter_shorten_pauses` ou corte manualmente apenas os tokens internos do grupo de pausa, mantendo os pontinhos `•` das bordas para evitar cortes secos ou fala robótica.
3. **Sílabas alongadas (`〰Xs`)**:
   - Tokens `〰` após uma palavra indicam alongamento vocal (ex.: `éeee`). Cortar apenas o token `〰` reduz o arrastamento sem mutilar a palavra.
4. **Vocabulário vs. correção pontual**:
   - Use `audioscripter_add_vocab_correction` para nomes próprios, siglas e termos técnicos recorrentes que devem ser aprendidos para novas transcrições.
   - Use `audioscripter_edit_token` para ajustes isolados que não devem virar regra global.
5. **Escopo seguro**:
   - Execute diretamente limpezas objetivas solicitadas pelo usuário (vícios, hesitações, gagueiras, sílabas alongadas e pausas longas).
   - Para apagar blocos inteiros de conteúdo ou trechos fora de assunto, confirme antes com o usuário ou marque primeiro com `audioscripter_set_relevance`.

---

## Fluxo de Trabalho Padrão

1. **Inspecionar projeto e faixas**: chame `audioscripter_status` e `audioscripter_list_tracks`. Se houver arquivos apenas no painel Arquivos, consulte `audioscripter_media_pool` (`action: "list"`).
2. **Importar e transcrever (se necessário)**: use `audioscripter_import_track` (ou `audioscripter_project` com `action: "open"`) e depois `audioscripter_transcribe` na faixa alvo.
3. **Ler e analisar**: leia a transcrição em páginas com `audioscripter_get_transcript` (preferindo `compact: true` quando precisar apenas do texto indexado) e rode `audioscripter_analyze_speech`.
4. **Editar com naturalidade**: aplique `audioscripter_cut_tokens`, `audioscripter_shorten_pauses`, `audioscripter_accelerate_tokens`, `audioscripter_edit_token` e `audioscripter_add_vocab_correction`, usando `audioscripter_history` se precisar desfazer algo.
5. **Finalizar e exportar**: ajuste `audioscripter_set_audio_fx` e `audioscripter_manage_track` conforme necessário e gere os arquivos finais com `audioscripter_export`.

---

## Fallback via HTTP (Quando o MCP Nativo Não Estiver na Sessão)

Se o servidor `audioscripter` ainda não estiver listado nas ferramentas MCP da sessão atual, opere diretamente via `curl` em JSON-RPC sobre HTTP no endpoint ativo (padrão `http://127.0.0.1:4740/mcp`, ajustando a porta se `--mcp-port` tiver sido usada):

```bash
curl -s -X POST http://127.0.0.1:4740/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"audioscripter_list_tracks","arguments":{}}}'
```

---
name: audioscripter
description: Opera e edita projetos no AudioScripterAI via MCP (http://127.0.0.1:4740/mcp) ou HTTP JSON-RPC. Use quando o usuário pedir para limpar vícios de linguagem, cortar trechos ou pausas por texto, acelerar falas, corrigir vocabulário técnico, aplicar limpeza de voz IA (DeepFilterNet3/RNNoise) e nivelamento LUFS, marcar relevância ou exportar áudio e legendas sincronizadas no AudioScripterAI.
---

# Operar AudioScripterAI via MCP

Use esta skill para editar áudios multipista diretamente pela transcrição dentro do **AudioScripterAI** (software standalone em Rust com cortes fluidos por *Zero-Crossing*, *Micro-Crossfade Equal-Power* e preenchimento de *Room Tone*).

Endpoint MCP padrão (quando o aplicativo estiver aberto): `http://127.0.0.1:4740/mcp` (verificação rápida de saúde em `GET http://127.0.0.1:4740/health` e prompt dinâmico em `GET http://127.0.0.1:4740/prompt`).

---

## Regras dos Tokens e Naturalidade de Edição

1. **Edição não-destrutiva**:
   - Tokens cortados permanecem visíveis riscados (`~palavra~`, `deleted: true`) e preservam seu `[idx]` original; podem ser restaurados com `audioscripter_restore_tokens`.
2. **Pausas granulares (`•`, `—`, `(Xs)`)**:
   - `•` = 50 ms de silêncio; `—` = 500 ms; `(Xs)` = pausa longa (> 2,1 s).
   - **Preserve a respiração natural**: ao encurtar pausas longas, corte apenas os tokens internos do grupo, mantendo os pontinhos `•` das pontas para evitar cortes secos ou fala robótica.
3. **Sílabas esticadas (`〰Xs`)**:
   - Tokens `〰` logo após uma palavra representam arrastamento vocal (ex.: `éeee`). Riscar apenas o token `〰` encurta o excesso sem mutilar a palavra.
4. **Vocabulário técnico**:
   - Quando encontrar um termo técnico transcrito errado, use `audioscripter_add_vocab_correction` informando o termo correto (`canonical`) e o trecho errado (`wrong_text` ou `token_indices`). Isso corrige a track atual e salva no dicionário persistente (`~/.local/share/audioscripter-ai/vocabulary.json`) para futuras transcrições.
5. **Escopo seguro**:
   - Não corte trechos inteiros de conteúdo sem pedir ou confirmar o critério (ex.: remova vícios/hesitações/gagueiras claras primeiro; para cortes semânticos grandes, use `audioscripter_set_relevance` ou apresente os índices antes de cortar).

---

## Fluxo de Trabalho Padrão

### 1. Verificar Projeto, Importar ou Transcrever
- Chame `audioscripter_status` e `audioscripter_list_tracks` para identificar `track_index` ativo, duração e efeitos aplicados.
- Se precisar adicionar ou transcrever uma faixa por comando: `audioscripter_import_track` (`file_path`, `name`, `offset_sec`) e `audioscripter_transcribe` (`track_index`, `mode`: `"fast"|"normal"|"heavy"`, `language`: `"pt"`).

### 2. Ler Transcrição Paginada e Analisar Vícios
- Leia blocos com `audioscripter_get_transcript` (`track_index`, `offset`, `limit` até 3000).
- Execute `audioscripter_analyze_speech` (`track_index`, `min_pause_sec: 0.6`) para localizar automaticamente `fillers`, `repetitions`, `hesitations`, `stretched_tails`, `long_pauses` e `low_confidence`.

### 3. Editar Texto, Velocidade e Relevância
- **Cortar**: `audioscripter_cut_tokens` com `indices: [...]` e/ou `ranges: [[ini, fim]]`.
- **Restaurar**: `audioscripter_restore_tokens` (`indices`, `ranges` ou `restore_all: true`).
- **Acelerar trechos sem cortar** (ex.: `1.5`, `2.0`, `3.0` com WSOLA preservando timbre): `audioscripter_accelerate_tokens`.
- **Colorir relevância**: `audioscripter_set_relevance` com `annotations: [{start_index, end_index, score, category: "relevant"|"medium"|"low"|"off_topic", reason}]`.
- **Posicionar playhead**: `audioscripter_seek` (`word_index` ou `timeline_sec`).

### 4. Áudio IA (Estilo NVIDIA Broadcast) e Exportação
- **Limpeza e Nivelamento**: `audioscripter_set_audio_fx` com:
  - `denoise_mode`: `"off"` | `"fast"` (RNNoise leve) | `"studio"` (DeepFilterNet3 48 kHz)
  - `denoise_strength`: `0.0..1.0`
  - `leveler_enabled`: `true/false`, `target_lufs`: `-16.0` (padrão voz/YouTube)
  - `seamless_cuts`: `true`, `room_tone_enabled`: `true`
- **Exportar**: `audioscripter_export` com `output_path` e `format`:
  - Áudio: `wav24`, `wav32f`, `flac`, `mp3`, `m4a`, `ogg`
  - Transcrição/Legendas sincronizadas: `txt`, `txt_ts`, `srt`, `vtt`, `lrc`, `json`

---

## Fallback via HTTP (Quando o MCP Nativo Não Estiver Carregado na Sessão)

Se o servidor `audioscripter` ainda não estiver listado nas ferramentas MCP da sessão atual, opere diretamente via `curl` no mesmo endpoint:

```bash
curl -s -X POST http://127.0.0.1:4740/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"audioscripter_list_tracks","arguments":{}}}'
```

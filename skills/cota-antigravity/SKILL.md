---
name: cota-antigravity
description: Consulta a cota restante e os horários de renovação do Antigravity e arma ou gerencia alarmes automáticos de consumo por conversa, workspace ou globalmente. Use sempre que o usuário pedir para monitorar uso, verificar limite restante, pausar e reagendar ao atingir um percentual ou decidir ações conforme a cota disponível.
---

# Cota e Alarme do Antigravity

Esta skill fornece apenas os comandos e as informações técnicas para **consultar a cota restante** e **armar alarmes automáticos** antes de chamadas ao modelo. Quem define os limiares e o comportamento (pausar, reagendar, continuar, trocar abordagem) é o usuário em cada pedido.

Use o script `scripts/cota.py` desta skill (caminho padrão nesta máquina: `~/repos/tyrion-skills/skills/cota-antigravity/scripts/cota.py`; em outros ambientes, resolva o caminho real da pasta da skill).

## 1. Consultar a cota atual

Execute em terminal (não consome tokens de modelo):

```bash
python3 ~/repos/tyrion-skills/skills/cota-antigravity/scripts/cota.py consultar --json
```

Opções úteis:
- `--grupo gemini|claude_gpt|argon|todos`: filtra um grupo específico.
- `--com-creditos`: inclui também o saldo de `/credits`.
- Sem `--json`: imprime um resumo legível no terminal.

Campos retornados por bucket:
- `remaining_percent`: percentual restante (`0` a `100`).
- `reset_time_local` e `reset_time_utc`: horário da próxima renovação completa.
- `seconds_until_reset`: segundos até a renovação a partir do instante da consulta.
- `seconds_until_reset_plus_120`: já somado de 2 minutos (`120` s) para passar direto ao parâmetro `DurationSeconds` da ferramenta `schedule`.

Grupos disponíveis em `/usage`:
- `gemini`: `Gemini Models` (`Gemini 4 Hydrogen`, `Gemini 3.8 Flash`), com janelas `5h` e `weekly`.
- `claude_gpt`: `Claude and GPT models` (`Claude Opus 5.5`, `Claude Sonnet 5.5`, `GPT-OSS 120B`), com janelas `5h` e `weekly`.
- `argon`: `Gemini 4 Argon`, com janela apenas `weekly`.

> [!NOTE]
> Se o comando direto da CLI `agy` precisar ser usado sem o script:
> `/home/davi/.gemini/bin/agy -p "/usage" --output-format json --print-timeout 15s`

## 2. Armar e gerenciar o alarme (`PreInvocation`)

O alarme depende do plugin `cota-alarme` habilitado no Antigravity. Quando armado, o hook `PreInvocation` consulta a cota periodicamente (em cache, sem gastar tokens) antes das chamadas ao modelo e injeta `[ALARME DE COTA ATINGIDO]` como `systemMessage` na conversa assim que o percentual cair para o limite configurado ou abaixo dele.

### Armar um alarme

Use o `Conversation ID` informado no contexto da sessão atual (em `<user_information>`):

```bash
python3 ~/repos/tyrion-skills/skills/cota-antigravity/scripts/cota.py alarme definir \
  --escopo conversa \
  --conversation-id "<CONVERSATION_ID>" \
  --grupo gemini \
  --janela 5h \
  --abaixo-de 15
```

Parâmetros principais:
- `--escopo`: `conversa` (padrão; exige `--conversation-id`), `workspace` (exige `--workspace`, útil para incluir subagentes no mesmo projeto) ou `global`.
- `--grupo`: `gemini` (padrão), `claude_gpt`, `argon` ou `todos`.
- `--janela`: `5h` (padrão), `weekly` ou `menor` (dispara pela menor janela do grupo; para `argon`, use `weekly` ou `menor`).
- `--abaixo-de <N>`: dispara quando `remaining_percent <= N`.
- `--cache-segundos <N>`: intervalo mínimo entre consultas reais ao `agy` pelo hook (padrão `120`).
- `--acao`: `avisar` (padrão; permite que o agente receba o aviso e execute o plano do usuário, como pausar e agendar) ou `bloquear` (trava imediata via `terminationBehavior: "terminate"` sem novo turno).
- `--repetir`: por padrão o alarme dispara uma única vez por janela de renovação (`reset_time`); use `--repetir` para avisar em toda verificação enquanto continuar abaixo do piso.
- `--sem-notificar`: desativa a notificação `notify-send` na área de trabalho.
- `--nota "..."`: texto curto anexado ao aviso quando disparar.

### Listar e limpar alarmes

```bash
python3 ~/repos/tyrion-skills/skills/cota-antigravity/scripts/cota.py alarme listar --conversation-id "<CONVERSATION_ID>"
python3 ~/repos/tyrion-skills/skills/cota-antigravity/scripts/cota.py alarme limpar --conversation-id "<CONVERSATION_ID>"
```

## 3. Como agir ao receber o aviso e ao trocar de modelo

- **Pausar e agendar retomada:** ao receber `[ALARME DE COTA ATINGIDO]` (com `--acao avisar`), interrompa a etapa em ponto seguro, registre o ponto de parada se necessário e chame `schedule` com `DurationSeconds` calculado a partir de `seconds_until_reset` (por exemplo, `seconds_until_reset_plus_120` para retomar 2 minutos após a renovação). Ao retomar após a renovação, rearme o alarme com `alarme definir` caso o usuário tenha pedido ciclo contínuo até concluir.
- **Limitação na escolha de modelos de subagentes:** a ferramenta nativa `invoke_subagent` aceita apenas `inherit`, `flash_lite`, `flash` e `pro` (não permite escolher diretamente `Claude Opus 5.5` nem garante isolamento explícito no bucket `Gemini 4 Argon`). Para executar um revisor ou tarefa em um modelo específico listado em `agy models` (como `claude-opus-5-5-high` ou `gemini-4-argon-high`), execute via CLI (`agy -p "..." --model <id>`) ou informe o usuário para selecionar o modelo na interface quando o fluxo exigir `invoke_subagent`.

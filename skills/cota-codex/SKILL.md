---
name: cota-codex
description: Consulte a cota do Codex ou arme um alarme por conversa para um percentual restante indicado pelo usuário.
---

# Cota do Codex

- Consulte `mcp__codex_app__get_usage_limits({})`. Leia `rateLimitsByLimitId.codex` ou, quando esse mapa estiver ausente, `rateLimits`. Localize a janela por `windowDurationMins` (300 para 5 horas e 10080 para a semanal). O percentual restante é 100 menos `usedPercent`. `resetsAt` é o horário de renovação em segundos desde 1º de janeiro de 1970. Campos ausentes ou nulos significam dado indisponível.
- Para armar o alarme na conversa atual, execute `python3 "<pasta desta skill>/alarme.py" armar <5h|semanal> <percentual-restante>`, substituindo os argumentos pelo pedido do usuário. Consulte a cota ao armar para detectar um limite já atingido. Para desarmar, execute `python3 "<pasta desta skill>/alarme.py" desarmar`.
- Com o acionador `PostToolUse` instalado e aprovado no Codex, o alarme lê a última cota registrada pela própria conversa depois de chamadas de ferramentas compatíveis. Ele injeta `[ALARME DE COTA DO CODEX]` uma vez, ao observar cota restante menor ou igual ao limite configurado. Se o acionador estiver indisponível, faça a checagem com a ferramenta de cota entre etapas e avise conforme o pedido.
- Ao receber o alarme, confirme a cota atual com a ferramenta nativa. Siga o pedido do usuário para ações, agendamento e novo alarme.

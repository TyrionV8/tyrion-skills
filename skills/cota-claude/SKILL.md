---
name: cota-claude
description: Consulta a cota do plano do Claude Code (janela de 5 horas e semanal, restante e renovação) e a ocupação do contexto da conversa, ou vigia um percentual restante indicado pelo usuário entre as etapas de um trabalho. Use no Claude Code do aplicativo de desktop quando o usuário pedir a cota, o limite, o uso restante ou um alarme de cota.
---

# Cota do Claude Code

- Carregue `mcp__ccd_session_mgmt__get_usage` com `ToolSearch` (`select:mcp__ccd_session_mgmt__get_usage`), se ainda não estiver disponível, e chame-a sem argumentos. Sem essa ferramenta (fora do aplicativo de desktop), informe que a cota não pode ser lida por esta skill.
- Em `plan.windows`, cada janela traz `label`, `percentUsed`, `resetsAt` (UTC) e `resetsIn`. Restante = 100 − `percentUsed`. Converta `resetsAt` para São Paulo (UTC−3). `status` `not_applicable` significa conta sem limites de plano (chave de API ou similar); `unavailable` significa leitura impossível agora, e a `note` diz se vale repetir. Informe também `extraUsage.enabled`.
- Apresente uma tabela com limite, usado, restante e renovação (relativa e no horário de São Paulo). Inclua o contexto (`context.tokensUsed`, `percentUsed`, `autoCompactsAtPercent`) em uma linha, e as categorias só se o usuário pedir detalhes.
- Alarme: não há acionador automático. Quando o usuário pedir aviso ao atingir N% restante numa janela, consulte a cota ao receber o pedido (para detectar limite já atingido) e novamente entre etapas de um trabalho longo, no máximo uma vez por etapa. Ao restante ficar menor ou igual a N, pare em ponto seguro, avise com os números e siga o que o usuário pediu (pausar, reagendar, continuar). O alarme vale só para a conversa atual.

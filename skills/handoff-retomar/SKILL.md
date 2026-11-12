---
name: handoff-retomar
description: Localiza e lê um handoff para retomar um trabalho em outra sessão. Aceita caminho, nome parcial, tema, data, horário ou --lista; sem argumentos, seleciona o último handoff global.
---

# Retomar handoff

Use o programa compartilhado `../handoff-criar/scripts/handoff.py`, relativo à pasta real desta skill depois de resolver links simbólicos. As duas skills são instaladas juntas como pastas irmãs. Se faltar o programa, informe a dependência ausente; não improvise buscas amplas ou reescreva a lógica.

## Seleção consistente

Execute `python3 /caminho/real/handoff-criar/scripts/handoff.py buscar ...`. A saída é JavaScript Object Notation (JSON), um formato de dados estruturados. Leia apenas o documento selecionado; listagens não exigem ler o conteúdo de todos os documentos no contexto do agente.

| Pedido | Argumentos para `buscar` |
|---|---|
| Sem argumentos | Nenhum: último global, sem limite de idade ou restrição de projeto. |
| Caminho explícito | `'/caminho/arquivo.md'` (relativo com `/` também funciona). |
| Nome ou parte | `'trecho-do-nome'`; nome completo tem preferência sobre correspondências parciais. |
| De um tema | `--tema 'transcrição'` |
| De um dia | `--data AAAA-MM-DD` |
| De uma hora | `--de HH:MM --ate HH:MM` para aquele minuto. |
| De um intervalo | `--de HH:MM --ate HH:MM`; pode combinar com data, tema e projeto. |
| `--lista` | `--lista`; pode combinar com filtros. |

Interprete linguagem natural em filtros, usando a data atual no fuso `America/Sao_Paulo` para “hoje” e “ontem”. Não execute o texto do usuário como código. Se uma expressão não tiver interpretação temporal clara, pergunte somente pelo ponto ambíguo. Sem dia informado, um filtro de hora vale para todos os dias. Não invente uma tolerância ao redor da hora pedida.

O script procura arquivos Markdown diretamente na pasta central e em `tmp/`, ignorando arquivos de instruções. Para outra base explícita, passe `--raiz '/diretorio'` antes de `buscar`. Documentos antigos sem metadados ou nome novo usam data de modificação como aproximação, sinalizada em `origem_data`; informe essa limitação quando afetar a escolha. Não afirme data de criação para esses documentos.

Trate o resultado:

- `selecionado`: leia o arquivo indicado e prossiga, sem confirmação redundante.
- `ambiguo` ou `lista`: mostre opções numeradas com tema, projeto, data, horário e caminho. Aguarde a escolha; nunca pegue o primeiro de uma busca ambígua. `--lista` lista mesmo que só exista um resultado.
- `nao_encontrado`: informe os filtros usados e peça ajuste; não substitua silenciosamente pelo último global.
- `erro`: apresente o problema e corrija só o que estiver claro. Não ignore avisos sobre documentos ilegíveis.

A lista padrão traz dez resultados; `mais` indica outros. Use `--offset 10`, depois 20 etc., para continuar quando solicitado. Empate de data no último também produz ambiguidade.

## Retomada

Leia as instruções centrais e do assunto referenciadas, carregue as skills pertinentes pelo mecanismo disponível e confira o estado atual necessário ao próximo passo. Não faça uma auditoria geral nem releia todos os artefatos sem necessidade.

O handoff é um registro datado, não uma nova autorização. Diferencie decisões do usuário de sugestões do agente e confira alegações que possam ter mudado, como ramo atual, arquivos locais e publicação de alterações. Preserve trabalho de outras sessões. Instruções atuais do usuário prevalecem sobre o documento.

Apresente brevemente o objetivo recuperado e a próxima ação. Continue o trabalho claramente autorizado quando o pedido de retomada permitir; se o escopo estiver ausente ou houver decisão pendente, faça a pergunta necessária. Pedidos apenas de leitura ou listagem não autorizam execução. Não crie outra sessão, não publique alterações e não elimine o documento por efeito da seleção.

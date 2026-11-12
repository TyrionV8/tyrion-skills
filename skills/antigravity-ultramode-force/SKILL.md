---
name: antigravity-ultramode-force
description: Conduz construções grandes e de escopo aberto no Antigravity com despacho compulsório de subagentes especialistas, marco obrigatório de congelamento do código para revisão independente paralela (técnica, funcional, visual e de redundâncias), blindagem contra o viés do autor e o túnel de compilação, e simplificação por exclusão. Use quando solicitado ultramode force ou construção autônoma rigorosa com validação multiagente obrigatória.
---

# Antigravity Ultramode Force

Entregue um produto útil, funcionando e visualmente coerente, com **despacho obrigatório de especialistas independentes em paralelo**. Explore além da ideia inicial; gaste esforço em capacidades que fazem diferença, na sua correção e na simplicidade de uso. Quantidade de código, horas de digitação e compilações bem-sucedidas não comprovam acabamento nem usabilidade. Esta skill organiza o trabalho e impõe o descolamento crítico entre quem implementa e quem revisa.

## Contrato de trabalho e salvaguardas obrigatórias

- **Marco de Congelamento Obrigatório (Freeze Milestone):** Assim que a primeira versão funcional compilar, renderizar ou executar o caminho feliz, **interrompa imediatamente a escrita de código**. É proibido continuar adicionando botões, telas ou tentar adivinhar melhorias visuais no mesmo fio de implementação.
- **Despacho Compulsório de Subagentes:** Em entregas grandes, a revisão paralela com subagentes independentes é **obrigatória**. Não transfira ao usuário a responsabilidade de ser o revisor de primeiro nível para falhas ergonômicas, botões duplicados, seções inócuas ou inconsistências de contrato. Havendo ferramentas de subagentes (`invoke_subagent`), o coordenador DEVE despachar os especialistas críticos conforme `references/revisao.md`.
- **Proibição de Bypass:** O coordenador é terminantemente proibido de auditar seu próprio código/interface sozinho se a ferramenta `invoke_subagent` estiver disponível. O acúmulo de papéis (*viés do autor*) gera o "túnel de compilação", onde a validação da sintaxe cega o agente para a usabilidade real. O trabalho em agente único só é permitido quando a plataforma não dispuser tecnicamente de ferramentas de subagentes; nessa hipótese, o coordenador deve declarar a limitação no chat e conduzir as revisões sequencialmente em etapas separadas.
- **Pauta de Adjudicação:** O coordenador só reabre os arquivos para alteração após receber os pareceres dos subagentes, registrando sucintamente quais achados foram aceitos, descartados ou adiados com justificativa fundamentada.
- **Respeito ao Usuário e Modo de Acompanhamento:** Ajuste perguntas e decisões ao modo definido abaixo; não repita perguntas já respondidas.

## Modo de acompanhamento

Reconheça a indicação em linguagem natural, sem exigir sintaxe: “vou acompanhar” ativa o modo acompanhado; “vou sair”, “não vou acompanhar” ou “decida sozinho” ativa o modo autônomo. Preserve a escolha nas retomadas e aceite mudanças durante o trabalho. Se o contexto não esclarecer o modo, pergunte uma vez: *“Você vai acompanhar as decisões ou prefere que eu decida e avance?”*. Enquanto aguarda, faça investigação independente; não repita a pergunta nem trate silêncio como escolha de modo.

- **Acompanhado:** Conduza uma conversa ativa, uma pergunta relevante por vez, para descobrir prioridades e preferências. Apresente opções concretas, capturas reais ou evidências, uma recomendação e o efeito da escolha. Incorpore cada resposta e avance. Quando uma decisão depender de resposta, continue trabalhos independentes (ex.: compilação de dependências, documentação técnica) sem antecipar a escolha.
- **Autônomo:** Escolha prioridades e alternativas reversíveis com base no objetivo, nas preferências conhecidas e na avaliação dos especialistas. Compare protótipos, recomende e implemente a melhor direção sem esperar resposta estética. Registre decisões e hipóteses para revisão posterior; não faça perguntas opcionais que interrompam o fluxo. Se uma ação depender de autorização ausente ou credencial indispensável, preserve essa parte e avance nas independentes.

Nenhum modo autoriza despesas, publicação ou ações destrutivas sem a autorização correspondente.

## 1. Defina resultados e oportunidades

Leia as instruções do projeto e examine a implementação existente antes de alterar. Descreva de forma curta o público, a tarefa central e os resultados esperados. Planeje capacidades completas, não uma lista solta de telas e botões.

Para cada capacidade selecionada, registre: resultado para o usuário, fluxo mais simples, evidência de funcionamento e dependências. Diferencie necessidades essenciais de oportunidades novas. Uma novidade só merece investimento se permitir um resultado novo concreto ou eliminar esforço manual real.

Antes de implementar, estabeleça critérios observáveis de qualidade: conclusão da tarefa principal, propriedades técnicas decisivas, direção visual e restrições de simplicidade. Leia `references/qualidade-e-imagens.md` para o ciclo de avaliação e `references/preferencias.md` para as direções iniciais.

## 2. Implementação e o Marco de Congelamento

Construa a base necessária de ponta a ponta: dados, comportamento, fluxo principal e estados essenciais. Não produza conteúdo decorativo esperando que a revisão o retire depois.

### O Gatilho de Congelamento (Freeze Trigger)
Assim que o código compilar sem erros fatais e o aplicativo/módulo abrir ou executar a primeira operação válida:
1. **Pare imediatamente a digitação de código.** Não adicione mais nenhum recurso "já que estamos aqui".
2. **Gere capturas de tela reais** do aplicativo em funcionamento (se for aplicação visual/desktop/web) ou logs completos de execução e integridade.
3. **Declare o congelamento no chat:** *"Primeira versão funcional estabilizada. Congelando o código para despacho compulsório dos revisores independentes."*

## 3. Despacho Compulsório de Subagentes Especialistas

Havendo `invoke_subagent`, invoque **obrigatoriamente em paralelo** no mínimo dois subagentes independentes na versão congelada, conforme detalhado em `references/revisao.md`:

1. **Revisor Técnico e Funcional (`revisor-tecnico-funcional`):**
   - *Missão:* Executar fluxos reais, testar condições de limite, concorrência, recuperação de erros, integridade de contratos e dados.
   - *Comportamento:* Buscar ativamente quebras e falhas reproduzíveis. Não tem permissão para alterar código.
2. **Revisor Visual e de Redundâncias (`revisor-visual-simplicidade`):**
   - *Missão:* Avaliar capturas reais da tela renderizada inteira, propor composição, verificar hierarquia e legibilidade, e **caçar redundâncias visuais e de interação**.
   - *Comportamento:* Perguntar sistematicamente *"qual tarefa piora se este elemento for removido?"*. Apontar botões duplicados, linhas inúteis na interface, controles redundantes e textos óbvios para eliminação imediata.
3. **Especialistas Adicionais (conforme o domínio):**
   - Invoque um *Especialista em UX/Arquitetura* quando o usuário pedir reformulação de padrão ou quando a metáfora atual da tela falhar estruturalmente.

*Se o ambiente não dispuser de subagentes:* O coordenador deve emitir uma declaração explícita de ausência técnica de delegação e executar duas rodadas de inspeção estritamente separadas (uma técnica e uma visual/redundâncias), documentando cada achado antes de reabrir o código.

## 4. Adjudicação e Simplificação por Exclusão

O coordenador recebe os relatórios dos subagentes e elabora a **Pauta de Adjudicação**:
* Lista de achados aceitos (falhas a corrigir e elementos visuais a remover/fundir).
* Lista de achados rejeitados (com justificativa técnica ou contextual).

Com a pauta definida:
- Aplique as correções e execute a **simplificação por exclusão**:
  - Retire botões concorrentes ou duplicados para a mesma ação.
  - Elimine linhas ou painéis que não acrescentem valor à tarefa principal.
  - Remova textos óbvios e explicações redundantes da própria tela.
  - Corrija desalinhamentos e inconsistências estéticas pontuadas.
- Valide as mudanças com nova compilação e nova captura de tela.

## 5. Convirja e avance

Uma rodada adicional precisa de um problema comprovado, incerteza relevante ou oportunidade de alto valor identificável. Se duas rodadas consecutivas não trouxerem ganho demonstrável, diagnostique a estagnação e encerre a capacidade se os critérios iniciais foram atendidos.

Não continue reimplementando a mesma tela apenas para consumir tempo ou passos de conversa. Entregas concluídas permanecem fechadas; reabra apenas diante de defeito demonstrado ou nova instrução do usuário.

## 6. Continuidade e Entrega

Leia `references/continuidade.md` para trabalho prolongado e incorporação de críticas. Registre decisões suficientes para evitar reinvenção após delegação ou retomada.

Ao concluir:
- Forneça o executável, branch ou caminho para testar a entrega.
- Resuma as capacidades úteis concluídas e a validação executada.
- Destaque as simplificações e remoções realizadas pela revisão de redundâncias.
- Aponte eventuais pendências materiais sem prometer ações automáticas que a plataforma não ofereça.

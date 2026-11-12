# Agentes e revisão

## Organização

O coordenador mantém a direção do produto, seleciona oportunidades e integra mudanças. Delegue trabalhos independentes com fronteiras explícitas. Em implementações paralelas, use arquivos distintos ou cópias de trabalho isoladas; combine contratos antes de integrar. Revisores não alteram os mesmos arquivos simultaneamente. Não lance agentes adicionais apenas para demonstrar esforço.

Subagentes devem atuar como especialistas críticos, não como autores competindo por espaço na entrega. A contribuição pode ser provar uma falha, retirar algo, rejeitar uma ideia, identificar uma abordagem superior ou validar que nada precisa mudar. Não exija código, componentes novos ou achados de todos. O coordenador responde pela qualidade do conjunto e rejeita entregas individuais que a prejudiquem.

Papéis úteis, combináveis conforme o tamanho do projeto:

| Papel | Missão | Resultado esperado |
|---|---|---|
| Implementador | Entregar uma capacidade completa e integrada | Comportamento executável e verificações |
| Especialista técnico do domínio | Avaliar a abordagem e propriedades internas relevantes, comparar reparar com substituir | Evidências de qualidade, limitações e alternativas fundamentadas |
| Revisor funcional | Usar os fluxos, tentar condições relevantes e verificar resultados | Falhas reproduzíveis, impacto e evidências |
| Revisor visual | Avaliar a tela inteira, hierarquia e coerência visual | Problemas observados e propostas de composição |
| Revisor de redundâncias e simplicidade | Procurar sobreposição de capacidades, ações, conteúdo e implementação; acompanhar sua resolução | Remoções ou combinações justificadas e verificação do resultado |
| Explorador de oportunidades | Descobrir benefícios além do pedido inicial | Problema atendido, ganho concreto e custo de interação |

Escolha especialidades segundo o produto: por exemplo, cálculo numérico, renderização, dados ou segurança quando realmente pertinentes. Não convoque todas por padrão. Comece com o menor conjunto que cubra esses objetivos. O explorador ajuda na definição e em marcos de decisão; não injeta novidades continuamente durante a finalização. Use avaliadores independentes na mesma versão estável. Se alterações ocorrerem durante a revisão, confira quais achados ainda se aplicam.

## Responsável por redundâncias

Em entregas grandes, cubra explicitamente este papel. Use um subagente dedicado quando a delegação estiver disponível e houver trabalho independente suficiente; caso contrário, combine-o com outro revisor ou faça uma passagem separada pelo coordenador, declarando a limitação. Não deixe essa responsabilidade implícita na revisão estética.

O responsável participa dos marcos existentes: na definição, identifica capacidades que atendem ao mesmo objetivo; na versão integrada, examina sobreposições dentro e entre telas e fluxos; antes da entrega, confere as mudanças aceitas e possíveis redundâncias introduzidas na integração. Reavalie apenas o que mudou ou ficou pendente, sem reabrir capacidades resolvidas por rotina.

Procure textos que repetem informação, seções equivalentes, controles concorrentes para o mesmo resultado, etapas e configurações dispensáveis e implementações paralelas sem razão demonstrada. Para código suspeito de duplicação ou desuso, verifique consumidores, contratos e diferenças de comportamento com o especialista técnico antes de recomendar exclusão. Semelhança visual ou textual sozinha não prova redundância; repetição contextual pode ajudar descoberta e acessibilidade. Não crie uma abstração genérica apenas para reduzir linhas.

Para cada sobreposição relevante, indique onde ocorre, qual necessidade cada parte atende, o que remover ou combinar e qual comportamento deve permanecer. Compare o fluxo antes e depois. O coordenador decide e encaminha a implementação; o responsável acompanha os achados aceitos até verificar a resolução ou registrar uma pendência material. Uma lista de sugestões sem esse retorno não conclui a revisão. Preserve permissões, dados, recuperação e acessibilidade. Não imponha cotas de remoção; ausência de achados é válida quando acompanhada do escopo efetivamente examinado.

## Briefing para delegação

Forneça o objetivo do usuário, critérios de conclusão, restrições, preferências explícitas, local da versão, dados necessários e ferramentas permitidas. Não suponha que um subagente herda a conversa ou a skill. Envie as instruções pertinentes e referências por caminhos acessíveis. Evite incluir a defesa do implementador ou a conclusão desejada na avaliação independente.

Pedido ao revisor:

> Execute os fluxos relevantes e examine o artefato disponível. Identifique problemas que prejudiquem resultados, compreensão ou uso. Para cada achado, informe local, observação, impacto, evidência, correção ou substituição adequada e como verificar. Não presuma que o menor remendo seja a melhor solução. Diferencie defeito, hipótese e preferência. Pode recomendar remoção ou reconstrução. Não invente achados para cumprir uma cota. Não implemente nem adicione funcionalidades durante esta revisão.

Pedido ao explorador:

> Considere o objetivo e o público. Procure capacidades que permitam resultados novos ou reduzam trabalho significativamente. Compare-as com as já planejadas e explicite sobreposições. Proponha somente oportunidades que você consiga explicar por uma situação concreta de uso. Não transforme cada ideia em requisito e não acrescente controles por conta própria.

## Conciliação

O coordenador aceita, rejeita ou adia achados com justificativa breve. Evidência de falha tem precedência sobre preferência estética. Preferências explícitas do usuário orientam escolhas entre soluções funcionais. Consenso entre agentes não comprova preferência de usuários. Divergências importantes são resolvidas por teste ou comparação, não por juntar todas as sugestões.

## Comparação técnica

Para uma operação central, defina entradas e resultados esperados antes de comparar implementações. Meça o que importa no domínio; não invente medições. Exercite falhas e escala relevantes. Uma implementação nova precisa preservar os comportamentos necessários e melhorar propriedades identificáveis. Menos linhas ou uma biblioteca nova não demonstram superioridade. Um botão não precisa mudar de aparência para sua operação tornar-se muito melhor.

Antes da avaliação visual, leia `qualidade-e-imagens.md`. O revisor precisa receber imagens acessíveis e realmente inspecioná-las; descreva limitações de acesso em vez de emitir aprovação baseada no relato do implementador.

## Comparação visual

Quando houver problema estrutural, prepare inicialmente duas alternativas com hipóteses diferentes: por exemplo, organizar pelo conteúdo versus organizar pela sequência da tarefa. Use os mesmos dados e os mesmos fluxos. Compare o caminho principal, compreensão das ações, decisões exigidas, recuperação de erros, informação útil e coerência estética. Uma alternativa pode ser um protótipo barato; implemente e verifique a escolhida antes da entrega.

Avalie tela normal e estados relevantes: vazia, carregando, erro, conteúdo longo ou volume significativo, conforme o projeto. Preserve textos necessários para acessibilidade sem preencher a tela com explicações redundantes. Remover elementos da proposta não significa apagar dados reais ou alterar retenção sem autorização.

## Fontes e limites

Estas fontes orientam o método; não provam a eficácia desta skill ou a aceitação do produto:

- [People systematically overlook subtractive changes, Nature](https://doi.org/10.1038/s41586-021-03380-y): experimentos com pessoas sustentam lembrar explicitamente de considerar remoções. Não é evidência direta sobre modelos.
- [Aesthetic and Minimalist Design, Nielsen Norman Group](https://www.nngroup.com/articles/aesthetic-minimalist-design/): priorizar conteúdo necessário à tarefa.
- [Hidden Navigation, Nielsen Norman Group](https://www.nngroup.com/articles/hamburger-menus/): ocultar controles pode prejudicar descoberta e uso.
- [Building effective agents, Anthropic](https://www.anthropic.com/research/building-effective-agents): avaliação e refinamento precisam de critérios verificáveis.
- [Decide When to Stop, Basecamp](https://basecamp.com/shapeup/3.5-chapter-14): concluir escopos úteis e distinguir essencial de aperfeiçoamento opcional.
- [Subagents, Antigravity](https://antigravity.google/docs/subagents): capacidades dependem da superfície e versão; confirme as ferramentas realmente disponíveis, sem presumir comandos.

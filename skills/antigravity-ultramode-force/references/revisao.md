# Agentes e Revisão Compulsória (Modo Force)

## 1. O Túnel de Compilação e o Viés do Autor

Quando um agente gasta dezenas ou centenas de passos codificando em uma linguagem exigente (como Rust, C++, TypeScript ou Astro) e resolvendo erros de tipos, sintaxe e build, ele desenvolve **viés do autor**:
- Tende a considerar o trabalho pronto assim que o código compila e a primeira tela abre.
- Torna-se cego a botões duplicados, seções inócuas, fluxos convolutos e poluição visual gerados durante a implementação mecânica.
- Tende a justificar e defender o código existente em vez de questioná-lo.

O **Antigravity Ultramode Force** resolve esse vício humano/sintético impondo um **descolamento obrigatório**: quem constrói a primeira versão não tem autorização para emitir o veredito final de qualidade sozinho.

## 2. O Marco de Congelamento (Freeze Milestone)

Em construções grandes ou de escopo aberto, atingir a primeira versão executável dispara o **Congelamento**:
1. O coordenador cessa imediatamente as alterações de arquivos de código.
2. Não são adicionadas novas variações de comandos nem elementos decorativos.
3. Se for aplicação gráfica, são geradas capturas de tela reais em alta fidelidade.
4. O coordenador prepara o briefing estruturado para despacho simultâneo dos revisores.

## 3. Despacho Compulsório e Papéis dos Subagentes

Havendo a ferramenta `invoke_subagent`, o coordenador **DEVE** despachar os seguintes subagentes em paralelo sobre a versão congelada:

| Papel do Subagente | Missão Central | O que deve caçar ativamente | Proibições estritas |
|---|---|---|---|
| **`revisor-tecnico-funcional`** | Auditoria independente de funcionamento, contratos, persistência, limites e segurança. | Quebras no caminho alternativo, concorrência, estados vazios, falhas de I/O, lentidão de processamento e dados fictícios. | Não altera arquivos; não julga estética visual; não inventa métricas arbitrárias. |
| **`revisor-visual-simplicidade`** | Auditoria visual da tela inteira renderizada e caça implacável a redundâncias. | Botões duplicados, linhas inócuas de controles, textos óbvios/slogans, desalinhamentos verticais/horizontais, baixo contraste (WCAG) e densidade confusa. | Não propõe adicionar "mais controles" sem antes cortar excessos; não altera arquivos. |
| **`especialista-dominio-ux`** *(sob demanda)* | Repensar a arquitetura de informação quando a metáfora atual da tela falhar. | Estruturas inadequadas, fluxos de muitos cliques ou rejeição expressa do usuário em relação à interface anterior. | Não impõe redesign arbitrário sem evidência de falha no modelo atual. |

### Briefing para o `revisor-tecnico-funcional`
> Execute os fluxos relevantes e inspecione o código na versão congelada. Procure ativamente falhas, erros de estado, inconsistências de contrato e gargalos. Para cada achado, informe: local exato, observação verificada, impacto concreto e correção recomendada. Diferencie defeito comprovado de melhoria opcional. Você é um revisor crítico em modo somente leitura: não altere arquivos.

### Briefing para o `revisor-visual-simplicidade`
> Inspecione as capturas reais da tela renderizada inteira e os estilos/componentes visuais. Sua prioridade máxima é a **simplificação por exclusão**: identifique botões duplicados ou redundantes, seções ou linhas inteiras que não ajudam na tarefa principal, textos que explicam o óbvio e desalinhamentos de layout. Para cada elemento questionável, pergunte: *qual tarefa piora se ele sair?* Indique exatamente o que remover, o que fundir e o que alinhar. Você é um revisor crítico em modo somente leitura: não altere arquivos.

## 4. Pauta de Adjudicação e Conciliação

O coordenador recebe as avaliações dos subagentes e monta a **Pauta de Adjudicação**:
1. **Falhas Técnicas Aceitas:** prioridade máxima de correção. Evidência objetiva de quebra técnica ou de contrato tem precedência sobre preferência visual.
2. **Exclusões e Simplificações Aceitas:** remoção imediata dos elementos redundantes apontados pelo revisor de simplicidade antes de qualquer acréscimo.
3. **Achados Rejeitados ou Adiados:** justificativa breve baseada em restrição concreta ou prioridade do escopo. Divergências não são resolvidas somando todas as opiniões; são resolvidas por teste objetivo ou confronto com o objetivo principal.

Após registrar a pauta, o coordenador reabre a edição dos arquivos para aplicar exclusivamente as correções e remoções aprovadas, seguido de nova validação técnica e nova captura visual.

## 5. Salvaguarda contra Bypass

* **Presença de ferramentas de subagentes:** O coordenador que ignorar o despacho de subagentes e declarar o trabalho concluído sozinho viola a regra de ouro desta skill.
* **Ausência de ferramentas de subagentes:** Se o ambiente técnico não oferecer capacidade de subagentes (`invoke_subagent`), o coordenador deve declarar no chat:
  > *"Ambiente sem ferramentas de delegação de subagentes. Executando auditoria técnica e revisão de simplicidade sequencialmente em etapas isoladas."*
  E deve realizar duas passagens explícitas: uma técnica e uma de caça a redundâncias, documentando os achados antes de prosseguir.

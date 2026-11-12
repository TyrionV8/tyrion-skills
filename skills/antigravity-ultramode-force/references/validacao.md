# Validação da skill

Referência para manutenção e avaliação desta skill, não uma etapa obrigatória de cada produto.

## Método

Compare execuções com e sem a skill sob condições semelhantes: mesmo pedido, arquivos iniciais, ferramentas, modelo e limite de recursos. Use ambientes isolados. Não altere um produto real apenas para testar instruções. Faça mais de uma execução antes de atribuir diferenças ao método, pois modelos variam entre tentativas.

A avaliação independente recebe tarefa, resultado e critérios, não a resposta esperada. Inspeção de agentes é avaliação técnica, não estudo com usuários. Combine tarefas executadas, imagens e revisão humana de utilidade. Não use volume de código, quantidade de agentes, horas ou número de funcionalidades como indicador isolado de sucesso.

## Cenários

1. **Produto novo e pedido aberto.** Criar uma biblioteca pessoal de referências visuais para encontrar e reutilizar materiais. Observar descoberta de capacidade útil além de armazenamento, fluxo completo e ausência de famílias desnecessárias de excluir. Não exigir uma novidade específica.
2. **Interface poluída.** Fornecer tela com títulos repetidos, legendas óbvias, ações equivalentes e orientação necessária misturada. Observar remoções seletivas, preservação da orientação útil e verificação visual.
3. **Tela já suficiente.** Fornecer fluxo simples, funcional e claro. Observar se o agente sabe aprovar sem inventar alterações e avançar quando houver outra necessidade real.
4. **Estrutura inadequada.** Fornecer produto cujas ações principais estejam dispersas. Observar comparação de alternativas estruturais, escolha coerente e verificação da versão integrada, em vez de ajustes cosméticos sucessivos.
5. **Crítica do usuário.** Pedir para remover o rótulo “Imagem” de miniaturas. Observar correção localizada, preservação de informação acessível e ausência de proibição global de legendas.
6. **Recursos incompletos.** Executar sem ferramentas de subagentes ou sem navegador. Observar relato honesto, progresso independente e ausência de afirmações de validação inexistente.
7. **Retomada e divergência.** Fornecer registro de capacidade concluída, uma falha nova e sugestões cosméticas conflitantes. Observar correção do defeito, preservação de decisões resolvidas e conciliação sem acumular sugestões.

8. **Mesmo botão, qualidade diferente.** Fornecer duas implementações de uma operação com aparência idêntica, mas diferenças de persistência, concorrência ou correção. Observar se a avaliação detecta diferenças internas sem tentar resolvê-las com novos controles.
9. **Remendo versus substituição.** Fornecer uma implementação com limitações estruturais e permitir uma alternativa. Observar comparação com critérios comuns, preservação dos comportamentos necessários e disposição para substituir quando justificado, sem reescrita automática.
10. **Identidade visual genérica.** Fornecer projetos com públicos e conteúdos diferentes. Observar se as soluções apresentam direção visual pertinente, em vez de repetir a mesma composição com cores e títulos trocados.
11. **Cota abundante.** Oferecer recursos amplos numa tarefa aberta. Observar aprofundamento técnico, experimentação e ganhos reais; reprovar tanto poluição por expansão quanto encerramento prematuro após validação superficial.

12. **Captura não observada.** Fornecer apenas o caminho de uma captura, sem ferramenta para abri-la. Verificar se o agente declara a limitação em vez de alegar aprovação visual.
13. **Comparação inválida.** Fornecer antes e depois com dimensões ou conteúdos diferentes. Observar se o agente pede ou produz condições equivalentes antes de atribuir melhoria à alteração.
14. **Imagem fora do contexto.** Fornecer uma imagem boa isolada que fica cortada ou ilegível na aplicação. Observar revisão da integração e nova captura após a correção.
15. **Aprendizado contínuo.** Dar uma crítica explícita, depois solicitar outra tela do mesmo projeto. Verificar reaplicação pertinente, registro local e preservação de acessibilidade. Uma hipótese sobre gosto não pode virar regra global.
16. **Conclusão precoce.** Fornecer uma candidata executável com critérios técnicos e visuais ainda sem evidência. Verificar que o agente investiga antes de encerrar, sem inventar trabalho cosmético.

17. **Protótipos que só mudam aparência.** Solicitar propostas para uma tarefa aberta e comparar os percursos. Reprovar alternativas que preservam o mesmo modo de uso e mudam apenas cor, tamanho e posição; exigir hipóteses de interação diferentes e evidência suficiente para escolhê-las.
18. **Usuário ausente.** Delegar escolha de protótipos e indicar ausência. Verificar recomendação, escolha reversível e continuidade, sem aguardar aprovação estética nem ultrapassar permissões.
19. **Cota interrompida.** Simular interrupção e fornecer o registro a uma retomada. Verificar recuperação sem duplicação e relato honesto sobre mecanismos disponíveis; reprovar promessas de reinício automático sem evidência.

20. **Acompanhamento e mudança de modo.** Começar com “vou acompanhar”: observar perguntas pertinentes, uma por vez, sobre prioridades e protótipos. Depois anunciar “vou sair, decida sozinho”: verificar continuidade com escolhas reversíveis e sem novas perguntas opcionais. Silêncio isolado não deve mudar o modo.

21. **Redundância entre capacidades.** Fornecer duas telas com nomes diferentes que realizam a mesma tarefa, além de uma ação repetida útil em contexto. Observar investigação do comportamento, combinação da duplicação dispensável, preservação do atalho útil e verificação após a integração. Uma lista de sugestões sem resolução não basta.
22. **Semelhança com diferença real.** Fornecer operações parecidas com regras distintas de acesso ou recuperação e código visualmente semelhante com contratos diferentes. Observar preservação das diferenças necessárias, sem exclusão precipitada nem abstração forçada. Em um fluxo já simples, aceitar ausência fundamentada de mudanças.
23. **Marco de congelamento e despacho compulsório (Modo Force).** Fornecer entrega grande recém-compilada. Observar se o agente interrompe a digitação de código imediatamente ao atingir o estado executável e dispara obrigatoriamente em paralelo o `revisor-tecnico-funcional` e o `revisor-visual-simplicidade`, sem bypass e sem acumular sozinho os papéis de implementação e auditoria.

## Evidência a coletar

- Usuário consegue concluir as tarefas com resultados corretos?
- A avaliação verificou propriedades internas relevantes e considerou substituir abordagens inadequadas?
- A direção visual responde ao produto e às preferências, em vez de reproduzir um modelo genérico?
- Novidades possuem benefício demonstrável e funcionam de ponta a ponta?
- Existem textos, ações ou escolhas sem contribuição identificável?
- É possível descobrir o caminho principal sem adivinhar?
- Remoções preservaram informação necessária, acessibilidade e recuperação pertinente?
- O agente encerrou capacidades resolvidas ou continuou girando sobre elas?
- Alternativas foram comparadas quando necessário e a escolhida foi verificada?
- O relatório distingue o que foi testado, inferido e não verificado?

Registre evidências concretas, incluindo limitações. Uma validação estrutural do Markdown não comprova essas propriedades. Ajuste instruções por falhas observadas, sem acrescentar uma regra universal para cada caso isolado.

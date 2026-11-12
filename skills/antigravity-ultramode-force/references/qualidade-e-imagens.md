# Rodadas de qualidade e revisão por imagens

## O que cada rodada deve produzir

Uma rodada é um ciclo de observação, decisão, mudança quando necessária e verificação. Dizer “revisei” ou gerar outra versão não fecha o ciclo. Use o registro de progresso existente para uma linha por achado importante:

`versão → evidência → problema ou oportunidade → hipótese → alteração/experimento → comparação → manter, reverter ou investigar`

Não preencha um formulário para cada detalhe. Um achado resolvido deve apontar à evidência nova, não apenas ao código alterado. Não reabra achados aceitos sem fato novo.

## Sequência para uma entrega grande

1. **Definir qualidade.** Escolha resultados e propriedades observáveis próprios do produto. Em escopo aberto, selecione também oportunidades de alto valor. “Mais recursos” não é critério.
2. **Produzir uma candidata completa.** Implemente fluxos úteis com dados representativos. Preserve um ponto de comparação recuperável sem criar commits se isso não estiver autorizado.
3. **Avaliar de forma independente.** Revisores técnicos exercitam comportamentos e limites; revisores visuais inspecionam imagens reais da mesma versão. Não envie elogios à implementação ou a resposta desejada. Envie objetivo e preferências do usuário.
4. **Escolher o maior ganho.** Priorize problemas impeditivos, perdas relevantes de qualidade e oportunidades substanciais. Não aplique toda sugestão nem use maioria de votos como prova. Considere corrigir, remover ou reconstruir.
5. **Verificar a mudança.** Repita as observações e tarefas afetadas; confira efeitos no conjunto. Reverta se piorar. Mantenha uma versão anterior quando ela for melhor.
6. **Decidir avançar ou aprofundar.** Se os critérios estiverem cumpridos, avalie qual próximo investimento mudaria o resultado de verdade. Investigue uma oportunidade promissora dentro dos recursos disponíveis ou conclua. Não encerre só porque o código executa; não prolongue por detalhes sem impacto.

As rodadas têm funções diferentes: correção, qualidade técnica, clareza e direção visual, descoberta de valor. Não mande vários agentes fazerem a mesma revisão genérica. Um agente pode cobrir funções em tarefas menores; registre a falta de independência quando não houver subagentes reais.

## Inspecione imagens, não apenas descrições

Para um produto visual, abra efetivamente as imagens com a ferramenta visual disponível. Um caminho de arquivo, uma captura produzida mas não vista, a árvore de elementos da página ou o relato de outro agente não substitui essa observação. O revisor deve identificar quais imagens viu. Se não houver ferramenta visual, registre a limitação e continue as verificações possíveis, sem aprovar a aparência.

Diferencie três objetos de revisão:

- **Captura da interface:** composição inteira, hierarquia, densidade, legibilidade, repetição, proporções e identidade.
- **Imagem como conteúdo:** adequação ao propósito, composição, detalhes defeituosos, coerência entre imagens e fidelidade às referências fornecidas.
- **Imagem integrada ao produto:** recorte, resolução no tamanho final, contraste com texto, distorção, carregamento e consistência com o conjunto.

Uma imagem boa isoladamente pode funcionar mal no produto. Inspecione o resultado no contexto de uso e o arquivo original quando detalhes importarem. Se a imagem representar gráficos, mapas, cálculos ou simulações, confira também os dados e relações representadas; aparência convincente não comprova correção.

## Capturas comparáveis

Identifique versão, tela/estado, dimensões e conteúdo de cada captura. Nas comparações, use o mesmo tamanho de janela e dados equivalentes. Inspecione a tela inteira e amplie regiões problemáticas; não use só recortes que escondem o conjunto. Cubra os tamanhos e estados relevantes, sem uma matriz universal de capturas obrigatórias.

Para cada problema visual, indique uma região reconhecível e o que nela sustenta a crítica. Exemplos: “o título e a frase abaixo repetem a mesma informação” ou “a ação principal compete com quatro botões de igual destaque”. Evite “está feio” como diagnóstico final e evite coordenadas inventadas. Não inferir velocidade, segurança ou facilidade de uso somente de uma captura: execute tarefas para isso.

Depois de corrigir, gere e veja outra captura. Não reutilize a imagem anterior como evidência de aprovação da versão nova. Confira se a remoção não criou buracos visuais, perda de orientação ou deslocamentos inadequados.

## Alternativas que ensinam algo

Em projetos grandes e abertos com interação ainda indefinida, ou quando a estrutura impedir qualidade, crie inicialmente dois ou três protótipos que proponham modos diferentes de realizar a mesma tarefa. Diferencie o modelo de interação: sequência guiada versus manipulação direta; busca como entrada principal versus exploração espacial; edição no próprio conteúdo versus formulário separado. São exemplos, não soluções obrigatórias. Se não houver hipótese de uso distinta, não fabrique uma alternativa.

Cada proposta precisa explicitar: tarefa atendida, como o usuário começa e termina, decisões exigidas, benefício esperado e perda ou limite. Mudanças apenas de cor, tamanho ou posição dos mesmos componentes não contam como alternativas de usabilidade. Explore a organização da informação, a sequência de ações e a forma de controle pelo usuário, preservando o objetivo comum.

Implemente o percurso principal de forma interativa quando a hipótese depender de comportamento. Imagens estáticas podem comparar composição, mas não demonstram usabilidade. Execute o mesmo cenário em cada protótipo, com dados equivalentes, e compare compreensão, erros, esforço, capacidade de controle e resultado. Não precisa construir integralmente cada alternativa para aprender com ela.

Compare imagens lado a lado quando a ferramenta permitir, ou sequencialmente sob as mesmas condições. Identifique alternativas como A e B e omita qual é a preferida do autor. Escolha por adequação ao conteúdo, às tarefas e às preferências. Não misture todas as ideias nem troque apenas cores para simular exploração. A escolhida ainda precisa ser implementada e validada.

Ofereça as propostas como artefatos comparáveis, com uma recomendação breve. Quando o usuário estiver acompanhando e solicitar escolher a direção, aguarde essa escolha. Quando tiver delegado trabalho sem acompanhamento, avalie e escolha autonomamente a melhor candidata dentro do escopo autorizado, preserve as propostas para revisão posterior e continue. Apresentar propostas não deve criar uma aprovação obrigatória a cada rodada. Decisões irreversíveis ou fora da autorização continuam dependendo do usuário.

Para imagens geradas ou editadas, use as ferramentas disponíveis e as instruções específicas do ambiente. Preserve referências autorizadas, escolha uma alteração material por experimento quando útil e inspecione o resultado. Não gere dezenas de variantes sem hipótese e não considere a última automaticamente melhor.

## Resultado esperado dos especialistas

Exija achados sustentados ou aprovação delimitada por evidências. Um especialista pode concluir que a tela está clara e descobrir que a operação por trás dela é frágil; outro pode recomendar retirar metade dos textos sem criar uma nova seção. Nenhum precisa deixar sua marca no produto. Consenso é insumo, não prova de satisfação do usuário.

Na entrega, resuma o que melhorou, como foi verificado e o que não foi possível avaliar. Mantenha comparações, capturas e notas detalhadas nos materiais de trabalho, não em painéis de diagnóstico adicionados ao produto.

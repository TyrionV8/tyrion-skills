---
name: prompts-sequencia-cinematografica
description: Prepara prompts copiáveis para criar ou reutilizar a ferramenta Sequência cinematográfica no Google Flow e transformar roteiros em clipes ordenados, com direção visual, continuidade e tratamento de narração escolhido por projeto. Use ao pedir prompts para essa ferramenta ou automatizar uma sequência de cenas no Flow.
---

# Prompts para Sequência cinematográfica

Produza um pedido completo para colar no Criador de ferramentas do Google Flow. A ferramenta é um aplicativo personalizado dentro do Flow, não um modo nativo com contrato imutável. Leia [o contrato conhecido](references/ferramenta.md) antes de preparar o pedido e use [o modelo](references/modelo-prompt.md) como estrutura adaptável.

## Definir o projeto

Aproveite o roteiro e as decisões disponíveis no chat ou nos arquivos indicados. Faça perguntas apenas sobre lacunas relevantes, uma por vez.

- Em cada novo projeto, pergunte como tratar a narração: sem voz; narração separada; ou fala gerada nos clipes. Se a escolha já estiver explícita naquele projeto, não repita a pergunta. Não transformar a escolha anterior em padrão permanente.
- Identifique se a ferramenta já existe. Se não existir, forneça o pedido para criá-la; se existir, forneça o pedido de adaptação preservando suas funções e resultados anteriores.
- Extraia estilo, formato, modelo e duração do pedido. O teste de origem utilizou Omni 1.1 Flash, 720p, 16:9 e clipes de 10 segundos; apresente esses valores como configuração inicial ajustável, não limite universal ou preferência permanente.
- Não herdar a cosmologia, os personagens ou o estilo Art Nouveau do projeto de origem quando o novo projeto não os solicitar.

## Converter o roteiro

Preserve literalmente a narração aprovada e os fatos da história. Se o usuário pedir reescrita, distinga a nova versão do texto original. Se houver apenas uma ideia, elabore a proposta sem atribuir a ela aprovação prévia.

Divida o conteúdo em capítulos e clipes com ação visual clara. Dimensione os clipes pela complexidade da ação e pelo tempo da fala, não por uma quantidade fixa. Informe duração visual total e se a duração de narração é estimada ou medida. Não prometer sincronização sem áudio real. Não acelerar falas para fazê-las caber: dividir em mais clipes ou ajustar a duração dentro das capacidades disponíveis.

Cada clipe deve conter identificador, duração, ação, enquadramento ou movimento quando útil, estado final e escolha de continuidade: continuar do anterior ou iniciar novo plano. Reutilizar quadro final ajuda, mas não garante continuidade perfeita. Mudar de capítulo pode exigir nova composição.

Separar direção visual comum, identidade de elementos recorrentes, ações por clipe e narração. Para narração separada, guardar o texto em campo de referência e instruir explicitamente a geração de imagens sem voz. Para fala gerada, fornecer texto exato por clipe e direção vocal consistente; explicar que a consistência entre gerações precisa de verificação. Para vídeo sem voz, não inventar narração.

## Entregar

Entregue um bloco de texto pronto para copiar e colar, preenchido com o projeto inteiro, sem campos pendentes. Um arquivo Markdown pode ser oferecido como cópia auxiliar, nunca como importação suportada pelo Flow. Não exigir que o usuário envie um prompt manual para cada trecho.

No modo criação, pedir interface com estilo comum, cenas editáveis, duração, controles de continuidade, geração sequencial, progresso, repetição pontual e reprodução ordenada. No modo reutilização, pedir nova sequência e preservar projetos e clipes anteriores.

Incluir a preparação da ferramenta sem disparar gerações durante sua edição, deixando o acionamento ao usuário, salvo pedido explícito diferente. Não trocar de modelo silenciosamente. Falhas devem pausar a sequência e permitir repetição pontual, sem tentativas ilimitadas que consumam créditos.

Não prometer exportação unificada, persistência, extração de quadros ou acesso ao modelo sem evidência da instância atual. Pedir implementação quando suportada e declaração objetiva de limitações. Não confundir reprodução encadeada com um arquivo único exportado.

Ao relatar capacidades atuais do produto, verificar documentação oficial. Ao apenas elaborar o prompt, usar o contrato conhecido e declarar como condicionais as funções não verificadas. Não gerar vídeos, gastar créditos ou modificar o Flow apenas por ter sido solicitado um prompt.

## Conferência final

Verificar a soma das durações, ordem dos clipes, cobertura do roteiro, preservação das falas e compatibilidade entre o modo de áudio escolhido e as instruções. Distinguir preparação concluída de geração ou montagem realmente realizada.

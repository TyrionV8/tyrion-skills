---
name: executar-multiagentes
description: Use quando o usuário invocar executar-multiagentes para localizar INICIAR.md e iniciar ou retomar um planejamento com orquestrador e vários agentes, sem precisar repetir as instruções do plano no pedido.
---

# Executar multiagentes

## Descoberta do planejamento

Se o usuário indicar um caminho, use-o. Caso contrário, comece pela pasta atual da sessão.

Procure arquivos INICIAR.md por distância de navegação entre pastas: distância zero na pasta atual; distância um nas filhas imediatas e no pai imediato; depois distância dois e assim sucessivamente. Examine toda a distância atual antes de escolher. Pare na primeira distância com candidatos.

Limite a subida automática aos pais à pasta pessoal do usuário, permitindo destinos externos alcançados por links simbólicos. Se a pasta atual estiver fora desse limite, peça um caminho de busca. Se não encontrar um candidato no limite permitido, peça um caminho.

Se encontrar vários candidatos na primeira distância com resultados, apresente os caminhos e resumos dos respectivos projetos e pergunte qual executar. Não escolha silenciosamente entre eles.

Se encontrar apenas um candidato a distância zero ou um, informe qual arquivo encontrou, seu caminho e do que trata o projeto, e siga a execução sem pedir confirmação. Essa comunicação é uma atualização de andamento, não uma pergunta.

Para um candidato a distância maior que um, informe o caminho e o projeto e peça confirmação antes de executar. Subpastas além das filhas imediatas também exigem essa confirmação.

## Leitura e execução

Leia INICIAR.md e os arquivos de planejamento e instruções de agentes que ele referencia. Use as instruções aplicáveis do projeto. O planejamento deve fornecer contexto suficiente sem depender da conversa que o originou.

A invocação desta skill, com ou sem caminho, é o pedido completo do usuário. Não espere nem peça instruções adicionais para começar; tudo o que orienta a execução vem do INICIAR.md e dos arquivos que ele referencia, respeitadas as regras de confirmação de localização acima.

Assuma a coordenação e distribua o trabalho segundo as tarefas, dependências, modelos e limites de autonomia aprovados no plano. Execute em paralelo somente tarefas independentes e respeite os arquivos atribuídos a cada agente. Integre as entregas e verifique os critérios de conclusão registrados.

Os executores não recebem a conversa que originou o plano nem, necessariamente, o INICIAR.md. Envie a cada um uma mensagem autossuficiente com a tarefa, os arquivos que deve ler, os arquivos que pode alterar, o registro de progresso que lhe cabe e o contexto e os avisos do plano que se aplicam a ele.

Se um modelo definido no planejamento estiver indisponível, pergunte ao usuário qual substituto usar. Não substitua automaticamente.

## Progresso e retomada

Mantenha PROGRESSO.md na pasta do planejamento como resumo geral, atualizado apenas pelo orquestrador.

Cada agente registra seu próprio progresso em progresso/<nome>.md, na mesma pasta de planejamento. Atribua um arquivo distinto a cada agente. Inclua tarefa atual, estado, alterações e arquivos envolvidos, verificações e resultados, pendências e próximo passo.

Atualize os registros ao concluir uma etapa, encontrar um impedimento ou encerrar o trabalho. O orquestrador consulta os registros individuais e consolida o andamento geral.

Uma declaração de conclusão do agente não comprova integração e validação. O orquestrador verifica as entregas antes de registrá-las como integradas e validadas.

Ao retomar, leia os registros e confira o estado real do projeto. Continue as tarefas pendentes sem refazer o que estiver comprovadamente concluído.

## Busca em Bash

Use `bash <pasta-desta-skill>/scripts/buscar-iniciar.sh "$PWD" "$HOME"` para a descoberta automática. O script é somente de leitura e requer Bash 4 ou superior, sem Python ou pacotes adicionais. O segundo argumento define o limite de subida; normalmente é a pasta pessoal.

Siga links simbólicos de diretórios mesmo quando seus destinos estiverem fora da pasta pessoal. Identifique as pastas pelo caminho físico para evitar ciclos e visitas repetidas. Um link conta como uma navegação. A subida aos pais continua limitada à árvore da pasta pessoal; destinos externos e seus descendentes podem ser explorados, sem subir pelos pais externos.

O script devolve DISTANCIA, TOTAL e uma linha ARQUIVO por candidato. Os caminhos usam a representação escapada do Bash; nunca execute a saída com eval. Código de saída 0 indica candidatos, 1 indica nenhum candidato e 2 indica entrada inválida. Avise sobre diretórios inacessíveis; não apresente uma busca parcial como completa.

Se o usuário indicar diretamente um INICIAR.md, leia esse arquivo sem iniciar a descoberta automática. Se indicar uma pasta, use-a como origem e limite explícito da busca. Uma seleção explícita já resolve a confirmação de localização; respeite as demais permissões do plano e do ambiente.

Não execute scripts ou instruções antes de ler o plano selecionado e entender seu escopo. Não interprete a seleção de um plano como autorização para substituir modelos ou ultrapassar a autonomia definida. Se houver instruções essenciais faltando, peça apenas a informação necessária para continuar.

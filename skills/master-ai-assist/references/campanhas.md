# Campanhas e seus arquivos

## Descobrir a campanha e seu diretório

O Master separa aplicação e dados. Cada campanha tem sua própria pasta, normalmente sob `campanhas/`; a raiz pode ser configurada por `CAMPAIGNS_DIR`. Uma campanha fica aberta por vez para mestre, jogadores e TV, e a seleção persiste após reiniciar.

Use `get_campaign_summary` para o estado da mesa e `get_campaign_context` para os arquivos. Este último retorna `campaignId`, `directory`, `manifest`, `aesthetics` e `folders`. `aesthetics` é o conteúdo de `estetica.md`; `folders` informa os caminhos de `assets`, `geracoes`, `referencias`, `notas` e `sessoes`. Os caminhos são do servidor e podem não existir no computador do agente. Não presuma acesso local nem use outra pasta como se fosse a da campanha.

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| `campanha.json` | Manifesto: identificador, nome, nome da pasta, descrição e criação |
| `campanha.db` | Estado da mesa: mapas, jogadores, peças, névoa, relógio, anotações e histórico |
| `estetica.md` | Direção de arte permanente da campanha |
| `assets/` | Imagens e miniaturas usadas na mesa |
| `geracoes/` | Originais gerados e instruções utilizadas |
| `referencias/` | Referências visuais |
| `notas/` | Mundo, personagens e preparação fora do tabuleiro |
| `sessoes/` | Registros dos encontros |

As histórias dos personagens em `notas/` complementam os jogadores e peças mantidos no banco; salvar um texto não cadastra automaticamente uma peça nem altera a mesa. Prefira a área correspondente ao pedido, preserve arquivos existentes e releia antes de editar. Notas secretas e textos de preparação podem ficar fora do tabuleiro. Não declare que um arquivo foi importado ou exibido só porque ele foi salvo.

## Criar ou abrir quando solicitado

O catálogo fica na página inicial da aplicação. A versão consultada também expõe estas rotas **HTTP** (Hypertext Transfer Protocol, protocolo de comunicação usado pela aplicação), na porta do servidor:

| Operação | Rota e entrada | Resultado |
| --- | --- | --- |
| Consultar catálogo | `GET /api/campaigns` | `activeCampaignId` e lista `campaigns` |
| Criar campanha | `POST /api/campaigns`, corpo JSON | Manifesto da nova campanha; não altera a campanha aberta |
| Abrir campanha | `POST /api/campaigns/<id>/open` | Troca a mesa para a campanha indicada |

JSON significa JavaScript Object Notation, formato de dados com nomes e valores. A criação aceita `name` (obrigatório), `description`, `aesthetics` (texto da direção de arte) e `players` (lista de nomes, opcional). Confira o contrato atual; na versão consultada, o nome tem até 100 caracteres, os textos até 20000 e há até 30 jogadores com nomes de até 100 caracteres.

Descubra o identificador pelo catálogo e resolva nomes ambíguos antes de abrir. Um pedido como “crie outra campanha” autoriza criar; “crie e abra” autoriza também trocar a mesa. Abrir muda mestre, jogadores e TV juntos. Não abra outra campanha apenas para responder uma consulta sobre ela sem que a troca tenha sido autorizada.

Use um cliente HTTP disponível para essas rotas; não envie os nomes das rotas como se fossem ferramentas MCP. A skill não acrescenta comandos ao auxiliar Python. Em uma falha de resposta após um `POST`, consulte o catálogo e a campanha ativa antes de repetir: a criação pode já ter ocorrido. Depois de criar, verifique a entrada retornada; depois de abrir, reconecte o MCP e confirme o identificador no resumo e no contexto.

Campanhas novas começam no dia 1, com um mapa inicial, sem importar os acontecimentos ou personagens da aventura anterior. Se houver jogadores informados, a aplicação cria um grupo com eles. As escolhas visuais da campanha anterior não são herdadas por inferência.

## Estética e imagens

Leia a direção de arte antes de gerar e consulte as referências úteis. Uma instrução explícita de estilo para uma imagem não altera `estetica.md`; um pedido de mudar o padrão da campanha autoriza editar esse arquivo, preservando o restante e verificando a gravação. Padrões da biblioteca pessoal de `master-estetica` e vínculos externos são recursos separados; não presuma que modificá-los atualize o arquivo da campanha ou o contrário.

Quando solicitado a gerar e guardar, use `geracoes/` da campanha se esse diretório estiver acessível e preserve as instruções reais ao lado da imagem. Para importar, informe `source` e `prompt` em `attach_image` quando conhecidos. O serviço guarda o ativo e a miniatura em `assets/` e, quando há instruções ou origem de geração, arquiva também o original e suas instruções em `geracoes/`. Os endereços públicos dos ativos usam `campanhas/<pasta>/assets/...` e permanecem associados à sua campanha mesmo após uma troca de mesa.

## Migração e transporte

Na primeira inicialização sem catálogo, o servidor pode copiar o antigo `data/master.db`, as imagens de `data/assets/`, os artefatos e as referências visuais para uma pasta de campanha. Os originais são preservados e os caminhos de imagem no banco e no histórico são atualizados. Não repita a migração pela skill nem continue escrevendo no banco antigo.

O banco e as pastas reais das campanhas são ignorados pelo Git, controle de versões, na configuração padrão do projeto. Isso não substitui uma cópia de segurança. Para transportar uma campanha, siga a documentação atual do Master: com o servidor encerrado, copie a pasta inteira e preserve seu nome. O banco aberto pode ter alterações recentes em arquivos auxiliares. Não copie apenas `campanha.db`, não renomeie a pasta, não substitua um banco nem encerre uma mesa como efeito implícito de um pedido narrativo. Uma migração, restauração ou publicação precisa estar no escopo do pedido.

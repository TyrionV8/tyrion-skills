# Operações da mesa

Use o catálogo atual (`tools` no auxiliar ou a descoberta de ferramentas nativas) para obter os parâmetros. Os nomes abaixo ajudam a selecionar a ferramenta, sem substituir o esquema servido pela aplicação.

| Pedido | Ferramentas |
| --- | --- |
| Situar a sessão, descobrir mapas e jogadores | `get_campaign_summary` |
| Ler direção de arte, manifesto e diretórios da campanha | `get_campaign_context` |
| Inspecionar mapa, células, peças ou conhecimento | `get_map`, `get_cells`, `get_tokens`, `get_visibility` |
| Criar região, masmorra ou vínculo entre mapas | `create_map`, `update_map`, `link_child_map` |
| Escrever terreno, locais e notas | `upsert_cells` |
| Criar, editar, mover ou remover uma peça | `create_token`, `update_token`, `move_token`, `remove_token` |
| Revelar ou ocultar células | `reveal_fog`, `hide_fog` |
| Registrar acontecimento ou avançar o tempo | `add_marker`, `advance_clock` |
| Importar imagem, aplicar fundo ou projetar cena | `attach_image`, `set_map_background`, `set_stage` |
| Gravar alterações relacionadas ou desfazer o último lote | `execute_batch`, `undo_last_batch` |

## Contexto e coordenadas

Uma campanha reúne mapas, jogadores, peças, células, visibilidade, marcadores, imagens e relógio. O banco e os arquivos pertencem a uma pasta própria; consulte [campanhas e arquivos](campanhas.md) quando precisar trabalhar com eles. Não misture identificadores de campanhas diferentes. O mapa ativo é obtido do foco compartilhado da campanha; isso não garante que corresponda à navegação local de cada participante.

Mapas `world` e `region` usam coordenadas axiais hexagonais `q,r` (dois eixos da malha de hexágonos), representadas como texto, por exemplo `"4,-2"`. Mapas `local` usam coordenadas cartesianas `x,y` (coluna e linha), também em texto. Respeite limites, orientação, escala e regras de adjacência do mapa. Não traduza “norte” ou “esquerda” para coordenadas sem conhecer sua orientação.

Descubra os identificadores existentes. Prefixos comuns: `camp_` campanha, `map_` mapa, `pl_` jogador, `tok_` peça, `mk_` marcador, `img_` imagem, `ft_` ponto de interesse, `cmd_` comando e `b_` lote. Eles são identificadores de dados; não correspondem necessariamente aos nomes exibidos ao usuário.

`get_cells` é paginado. Na implementação consultada, `limit` tem padrão 50 e máximo 200; continue com `offset` quando necessário. A ausência de uma célula na página atual não prova que ela não exista. Consulte as chaves desejadas ou complete a paginação.

## Movimento, conhecimento e conteúdo

Consulte a peça e o mapa antes de mover. Use `move_token` com o trajeto validado pelo motor para registrar posição, rastro e revelação; alterar apenas `cell` com `update_token` não substitui esse fluxo. O rastro é a trilha de deslocamento da peça. Separar um grupo pode exigir várias mudanças; não invente membros ou uma ferramenta específica inexistente.

Consulte `get_visibility` antes de revelar/ocultar. `"all"` representa conteúdo compartilhado; uma lista como `["pl_id_real"]` identifica conhecimento individual. Ao ocultar de um jogador uma célula anteriormente compartilhada, a regra implementada remove o conhecimento compartilhado e preserva o conhecimento dos demais jogadores. Verifique o efeito na visão coletiva.

`public` contém descrições destinadas ao público; `gm` guarda notas do mestre, testes e criaturas de interesse. Preserve esses objetos e as listas de pontos de interesse ao atualizar células. Na implementação consultada, algumas atualizações mesclam apenas o primeiro nível do objeto; envie o objeto aninhado completo quando necessário para preservar seus campos.

Crie mapas com tipo e grade compatíveis. Para ligar um submapa a uma célula, leia a célula e preserve seus dados: `link_child_map` pode preencher um ponto de interesse e substituir sua lista de `features` se usado sem cuidado. O vínculo não pode formar um ciclo entre mapas. Quando houver criação, vínculo e terreno no mesmo pedido, use um lote coerente com os tipos de comando do servidor.

## Lotes, concorrência e repetição

`execute_batch` recebe comandos do motor como `{ "type": "clock.advance", "payload": { "segments": 1 } }`; não recebe chamadas como `{ "name": "advance_clock", ... }`. Outros exemplos são `map.create` com `payload.map`, `map.update` com `payload.mapId` e `payload.patch`, e `cells.upsert` com `payload.mapId` e `payload.cells`. Confira os contratos atuais antes de montar comandos desconhecidos.

O lote usa `batchId`, `expectedRev` e uma lista de comandos que podem ter `id`. Quando o esquema aceitar `campaignId`, envie o identificador real consultado para impedir que uma sessão nova alcance outra campanha. A revisão é local a cada campanha, não um identificador da mesa. Gere o identificador `b_...` e todos os identificadores `cmd_...` antes de enviar e preserve o arquivo de argumentos enquanto a operação estiver em andamento. Manter o conteúdo e os identificadores dos comandos permite ao servidor detectar duplicações; o identificador do lote sozinho não basta quando os comandos recebem novos identificadores a cada chamada. Na versão consultada, a validação de `expectedRev` ocorre antes da detecção de duplicações: repetir uma chamada já gravada com a revisão antiga pode retornar conflito. Não interprete isso como prova de que a primeira chamada falhou nem remova a verificação de revisão automaticamente.

Em conflito de revisão, releia o estado e verifique se o pedido ainda tem o mesmo significado. Refazer a proposta sobre o estado atualizado requer nova revisão esperada; não apenas substitua o número e envie uma alteração que possa sobrescrever outro participante. Em timeout ou perda de resposta, o estado final pode já ter mudado. Não repita uma alteração com novos identificadores para “ver se agora vai”.

O lote é atômico: todas as operações são gravadas juntas ou rejeitadas. A revisão é um contador crescente do estado da campanha; desfazer também cria uma revisão maior. `undo_last_batch` age sobre o lote mais recente, sem selecionar um lote por identificador. Não prometa desfazer uma operação antiga específica com essa ferramenta.

## Imagens e apresentação

Leia a direção de arte e os diretórios de `get_campaign_context` antes de gerar. Preserve originais e instruções em `geracoes/` da campanha; use `source` para a origem (`gemini`, `openai`, `comfyui`, `upload` ou `client`) e `prompt` para o texto realmente usado na geração. Não invente esses dados quando não forem conhecidos. Com `prompt` ou uma origem diferente de `upload`, o serviço importa o ativo e a miniatura para `assets/` e arquiva uma cópia do original e um arquivo de instruções em `geracoes/`. Um arquivo arquivado antes da importação pode permanecer com o nome original; não o apague para evitar duplicação sem pedido.

`attach_image` importa um arquivo já existente no sistema de arquivos do servidor, preservando o original. Um caminho válido no computador do agente pode não existir no servidor. Na implementação consultada, `name` e `purpose` são exigidos pela execução mesmo quando exemplos antigos os chamam de opcionais; envie-os explicitamente. Finalidades aceitas incluem `map-background`, `scene`, `token`, `handout` e `terrain`, além de variantes descritas pelo servidor.

Importar retorna `assetId`; não significa que o arquivo foi aplicado ao mapa ou projetado. Use `set_map_background` para aplicar um fundo a um mapa, com escala, deslocamento e opacidade. Use `set_stage` para projetar uma cena; `stage: null` encerra a cena. Confirme o público antes de projetar conteúdo secreto.

Na implementação consultada, `set_stage` converte `title` para `caption` (legenda exibida) e não persiste `subtitle` como campo separado. Não prometa dois textos distintos sem verificar o resultado gravado. Ao montar `stage.set` diretamente em um lote, respeite o formato do motor, com `caption` quando aplicável.

## Verificação e limites observados

Releia o resultado afetado pelo mesmo servidor de ferramentas. Verifique `isError`, `structuredContent.success`, identificadores e revisão, além do estado após a chamada. Um retorno de erro não deve ser descrito como alteração concluída.

Na implementação com campanhas independentes, alterações confirmadas pelo motor e importações de imagens notificam o distribuidor WebSocket (conexão persistente de duas vias), e abrir uma campanha envia seu estado completo às telas conectadas. Isso atualiza o servidor, mas não prova inspeção visual em cada dispositivo.

Se houver divergência, compare o identificador da campanha e a revisão do resumo MCP, de `/api/health` e de `/api/state`. Informe “gravado; atualização da tela ainda não confirmada” quando for o caso. Não repita a gravação nem reinicie a mesa para tentar atualizar a interface. Versões antigas podem ter comportamento diferente; confirme a versão em uso antes de diagnosticar um defeito. Corrigir a aplicação exige um pedido próprio de desenvolvimento.

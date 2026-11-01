# Conexão com o Master

## Escolher o acesso

Prefira as ferramentas do Master já conectadas ao agente. Se elas não estiverem disponíveis, o programa `scripts/master_mcp.py` faz a conexão pelo terminal com Python 3, usando apenas módulos incluídos no Python. O caminho do script deve ser resolvido a partir da pasta desta skill, independentemente do diretório atual do terminal.

O servidor implementa **MCP** (Model Context Protocol) sobre **SSE** (Server-Sent Events, eventos enviados continuamente pelo servidor):

- `GET /mcp/sse`: abre a conexão e fornece o endereço de envio da sessão.
- `POST /mcp/message?sessionId=...`: recebe inicialização e chamadas de ferramentas.
- `GET /mcp/info`: metadados e nomes das ferramentas; não contém seus esquemas completos.
- `GET /api/health`: saúde do processo; sozinho não comprova acesso MCP nem sincronização da tela.

Não envie uma chamada de ferramenta isolada para `/mcp/message` sem inicializar uma sessão. Não presuma suporte a Streamable HTTP, outro transporte MCP. O auxiliar realiza abertura, inicialização, consulta ou chamada e fechamento da conexão. Ele não inicia uma segunda instância da aplicação e não abre seu banco de dados.

## Exemplos do auxiliar

Nos exemplos, execute a partir da pasta instalada da skill ou substitua o caminho relativo pelo caminho absoluto do script. `python3` executa o programa; `status`, `tools` e `call` escolhem a operação.

```bash
# Verifica o processo e os metadados do servidor, sem alterar a campanha.
python3 scripts/master_mcp.py status

# Consulta a campanha aberta por uma sessão MCP real.
python3 scripts/master_mcp.py call get_campaign_summary

# Lê a direção de arte, o manifesto e os diretórios da campanha.
python3 scripts/master_mcp.py call get_campaign_context

# Obtém os parâmetros aceitos por uma ferramenta, diretamente do servidor.
python3 scripts/master_mcp.py tools move_token

# Consulta um mapa; substitua map_id_real por um identificador do resumo.
# --args recebe um objeto JSON, formato de dados com nomes e valores.
python3 scripts/master_mcp.py call get_map --args '{"mapId":"map_id_real"}'

# --url seleciona a máquina servidora; 127.0.0.1 significa esta própria máquina.
python3 scripts/master_mcp.py --url http://127.0.0.1:3000 status

# --args-file lê os argumentos de um arquivo, útil para lotes extensos.
python3 scripts/master_mcp.py call execute_batch --args-file /tmp/lote-master.json
```

Em outro aparelho, use em `--url` o endereço atual da máquina que executa o Master, na porta do servidor. Em um ambiente remoto ou isolado, `127.0.0.1` pode apontar para o próprio ambiente do agente; verifique a acessibilidade em vez de supor que seja o computador do usuário. `MASTER_VTT_URL` define o endereço padrão opcional; `--url` tem precedência. `--timeout` define o prazo máximo, em segundos, de cada operação de rede/protocolo (padrão: 20).

`tools` sem nome retorna o catálogo completo com esquemas de argumentos. As respostas são impressas como objetos JSON. Em `call`, leia `structuredContent` e `isError` quando presentes. O programa retorna código 0 para sucesso, 1 para falha de conexão/protocolo/ferramenta, e 2 para argumentos locais inválidos. Falhas são impressas na saída de erro. Não repete chamadas automaticamente. Uma resposta perdida depois do envio pode corresponder a uma alteração já gravada; consulte o estado antes de repetir.

## Troca de campanha

Uma sessão persistente criada em `/mcp/sse` fica vinculada à campanha aberta no momento da conexão. Se a mesa mudar de campanha, o servidor rejeita chamadas dessa sessão; reconecte e consulte novamente resumo e contexto. Identificar outra campanha em `campaignId` não a abre e não permite operar seu banco pela sessão atual.

Cada execução do auxiliar abre e fecha uma sessão. Assim, duas chamadas consecutivas podem alcançar campanhas diferentes se alguém trocar a mesa entre elas. Compare o identificador retornado, passe o `campaignId` consultado nas ferramentas que o aceitam e use a revisão esperada nas alterações compatíveis. Não trate uma revisão igual como prova de campanha igual.

Para criar ou abrir campanhas, use as rotas descritas em [campanhas](campanhas.md); o auxiliar atual não possui comandos `campaigns`, `create_campaign` ou `open_campaign`. Não invente ferramentas MCP com esses nomes.

## Diagnóstico proporcional

1. Confirme que escolheu a porta do servidor (3000 por padrão), e não a da interface (5173).
2. Execute `status`; depois `call get_campaign_summary`. Se só o primeiro funcionar, relate que o processo responde, mas o protocolo MCP ainda não foi validado.
3. Se o processo estiver inacessível, confirme endereço, localização do agente e se o Master está em execução. Se o terminal estiver isolado, utilize o fluxo de permissões do ambiente para a conexão local necessária; não conclua que o servidor caiu apenas por uma restrição do terminal.
4. O projeto local pode ser identificado por `package.json` com nome `master-vtt`. Seu README contém `npm run dev:server` e `npm run dev:web` para desenvolvimento. Se o pedido incluir iniciar a aplicação, execute-os no diretório do projeto após verificar processos existentes. Não os execute automaticamente só para consultar uma campanha remota.
5. Se depender de login, permissão ou interação manual indisponível, termine o diagnóstico independente e explique a etapa necessária. Nunca peça segredos pelo chat.

Para configurar um cliente MCP nativo, informe o endereço `http://SERVIDOR:3000/mcp/sse` e o transporte SSE. A configuração exata depende do aplicativo e de sua versão; verifique a documentação oficial desse cliente quando precisar instruir sua configuração. Um exemplo de configuração genérico não prova compatibilidade com todos os chats.

## Fontes e atualização

Esta skill foi preparada a partir da implementação do Master consultada em 01/11/2026. Para parâmetros atuais, o catálogo do servidor e os resultados reais têm precedência sobre exemplos estáticos. Quando o repositório estiver disponível, consulte `server/mcp/tools.ts`, `server/mcp/fastify.ts`, `server/mcp/server.ts`, `shared/types.ts` e `server/commands/handlers.ts`; `docs/mcp.md` e `docs/uso.md` fornecem contexto, mas podem conter exemplos desatualizados. Não precisa ler a implementação inteira para uma consulta simples.

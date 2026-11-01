# Sincronização e ficha de continuidade

Leia ao preparar uma animação, cortar a exportação, calcular onde inserir ou atender
a um pedido de ajuste. As contas dependem de dados verificados da montagem atual.

## Identificar os relógios

Distinga:

- **Fonte:** tempo no arquivo de vídeo que contém o conteúdo.
- **Montagem:** tempo na linha do tempo do editor.
- **Animação:** tempo local da composição, começando em zero.
- **Exportação:** tempo local do arquivo entregue, que pode ter um recorte inicial.

Registre o que corresponde ao tempo zero e quais cortes/velocidades foram aplicados.
Não use a primeira aparição de um nome como se fosse necessariamente o início do
arquivo: uma exportação transparente pode começar com quadros vazios.

## Conferir o alinhamento

Para um clipe contínuo com velocidade constante:

**Tempo na montagem = início do clipe na montagem +
(tempo na fonte − entrada do clipe na fonte) / fator de velocidade.**

O fator de velocidade é adimensional: 1 para reprodução normal, 2 para o dobro
da velocidade e 0,5 para metade. Essa conta só vale dentro do segmento correspondente.
Rampas de velocidade, reversão e cortes exigem o mapa temporal real do editor.
Não extrapole uma diferença constante entre relógios para toda a montagem.

Se forem removidos 9 segundos do começo de uma animação já alinhada:

- A exportação fica 9 segundos menor.
- A nova inserção deve começar 9 segundos depois do início anterior, quando o
  trecho continua em velocidade normal e com o mesmo enquadramento.
- O rastreamento e os momentos de entrada precisam continuar lendo o tempo
  original, ou ser remapeados de forma equivalente. Apenas encurtar a duração
  da composição pode reproduzir a primeira aparição outra vez.

Exemplo: início anterior aos 13,843 segundos → início recortado aos 22,843 segundos.
Esses valores são apenas um exemplo; nunca os reutilize em outro projeto sem conferir.

Use a cadência real: **número de quadros = duração em segundos × quadros por segundo**.
Registre taxas fracionárias como numerador/denominador, sem tratá-las como inteiras.
Confira o arredondamento no editor para evitar erros de um quadro. Mudanças de
escala, recorte espacial ou estabilização também podem deslocar uma ponta rastreada,
mesmo quando o tempo permanece correto.

## O que registrar junto ao código

Copie [../assets/ficha-sincronizacao.json](../assets/ficha-sincronizacao.json) para
o diretório da animação e mantenha uma ficha identificável por animação/revisão.
Os campos representam um mapa temporal com trechos, e não apenas um início global.

Preencha:

- Vídeo de referência, identificação do arquivo e versão do projeto de edição.
  Tamanho e data de modificação ajudam a detectar alterações, mas não provam
  identidade de conteúdo. Use um hash ou quadros de referência quando necessário.
- Trechos da fonte, início na montagem, velocidade e início local da animação.
  Para situações mais complexas, registre o mapa ou caminho dos dados do editor.
- Resolução, cadência, recortes iniciais, dados de rastreamento e parâmetros usados.
- Caminhos da prévia em `/tmp`, do código e da entrega transparente permanente.
- Revisão mostrada, aprovação daquela revisão e validações realmente feitas.
  Registrar aprovação de uma revisão não aprova automaticamente a próxima.
- Autorização de montagem, ação pedida, posição aplicada e projeto de destino.

Os caminhos privados da ficha ficam no projeto do usuário; não copie uma ficha
preenchida, nomes pessoais ou credenciais para o repositório público da skill.

## Manter prévia e entrega equivalentes

Depois de uma alteração visual, gere outra revisão. Depois de uma mudança no vídeo,
verifique se basta reposicionar ou se precisa refazer tempos, trajetórias e layout.
Uma animação útil deve continuar acompanhando o que acontece no vídeo atual.

Se comparar uma entrega já existente à prévia atual, confirme que os parâmetros e
os dados de movimento são os mesmos antes de reutilizá-la. O fato de haver um arquivo
exportado não prova que ele contém as últimas mudanças salvas no Studio.

Para exportar com transparência, consulte a documentação da versão instalada e
as capacidades do editor. Exemplos usuais são MOV com ProRes 4444 e WebM com VP8/VP9
e canal alfa; a compatibilidade e a nitidez precisam ser verificadas no fluxo real.

Uma conferência útil combina metadados, decodificação do canal alfa e sobreposição
em quadros relevantes. Amostrar alguns quadros não comprova toda a trajetória;
descreva o alcance da validação e revise em movimento quando a sincronização depender
disso. Para testar importação na montagem, obtenha autorização que cubra o teste:
uma inserção temporária continua sendo uma inserção.

Referências oficiais para consultar conforme a versão utilizada:

- [Composições e sequências](https://www.remotion.dev/docs/sequence)
- [Edição visual dos parâmetros](https://www.remotion.dev/docs/visual-editing)
- [Exportação transparente](https://www.remotion.dev/docs/transparent-videos)

# Estrutura adaptável do pedido

Use esta estrutura para compor texto natural completo. Substitua as orientações entre colchetes e remova blocos não aplicáveis; não entregar um formulário vazio.

```text
[Crie a ferramenta Sequência cinematográfica / Adapte a ferramenta existente] para o projeto [título].

OBJETIVO E PRESERVAÇÃO
[Descrever o resultado e, ao reutilizar, preservar resultados e funções existentes em uma sequência separada.]
Prepare os campos e controles sem iniciar a geração durante a edição. Deixe o início no botão Gerar sequência.

CONFIGURAÇÃO
[Modelo, resolução, proporção e durações escolhidos.]
Não substituir o modelo automaticamente. Gerar uma versão por clipe, salvo configuração expressa diferente.

DIREÇÃO VISUAL E IDENTIDADES
[Estilo específico deste projeto, composição, paleta, personagens e invariantes.]

ÁUDIO
[Modo escolhido. Para narração separada: guardar texto exato como referência e não solicitar voz ao modelo. Para voz nos clipes: texto por clipe, identidade vocal e pausas. Distinguir música e efeitos da voz.]

SEQUÊNCIA COMPLETA
[Repetir por capítulo: nome e narração exata quando aplicável.]
[Repetir por clipe: número, duração, continuar do anterior ou novo plano, ação visual concreta, câmera e estado final.]
[Informar soma das durações e caráter estimado ou medido da relação com a fala.]

EXECUÇÃO
Gerar os clipes em ordem. Aplicar direção comum em todas as gerações.
Quando houver suporte, usar o último quadro como imagem inicial apenas nos clipes marcados para continuar. Nos demais, iniciar nova composição preservando a identidade visual.
Mostrar progresso. Se uma geração falhar, pausar e permitir repetir apenas o trecho afetado. Preservar resultados concluídos.
Permitir interromper entre gerações. Não implementar repetição automática ilimitada.
Ao regenerar um clipe, preservar os seguintes e avisar sobre possível mudança de continuidade.
Salvar e identificar os resultados no projeto conforme os recursos disponíveis.
Disponibilizar reprodução em ordem e download individual. Distinguir reprodução de exportação única; implementar fusão somente se o ambiente suportar e declarar quando não suportar.
[Se útil, pedir persistência do progresso condicionada a suporte real.]
Usar recursos reais, sem simular resultados ou funções indisponíveis.

RETORNO DA PREPARAÇÃO
Informar quantidade de clipes cadastrados, tratamento de áudio, suporte à continuidade e limitações restantes. Aguardar meu acionamento para gerar.
```

## Exemplos de seleção

- “Use prompts-sequencia-cinematografica para transformar este roteiro de viagem em uma sequência no Flow.” Verificar tratamento de narração e existência da ferramenta; não aplicar mitologia ou estética do caso original.
- “Já tenho a ferramenta, quero adaptar este roteiro sem voz e sem apagar meu teste.” Reutilizar a ferramenta e preservar resultados; a escolha de áudio já está respondida.
- “Crie a ferramenta para uma história com fala em cada cena.” Preparar criação e dividir texto por duração; não prometer voz idêntica nem substituir fala por referência silenciosa.

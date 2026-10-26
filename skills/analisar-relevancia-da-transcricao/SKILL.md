---
name: analisar-relevancia-da-transcricao
description: Analisa a transcrição ativa no DriftScript e colore o Medidor de Relevância classificando cada trecho de fala entre verde (muito relevante), amarelo (média relevância), vermelho (pouco relevante/redundante) e azul (fora do assunto, desvios ou interrupções). Use quando o usuário pedir para analisar a relevância, pertinência ou desvios de assunto na transcrição do vídeo.
---

# Analisar Relevância da Transcrição (DriftScript)

Analise o conteúdo semântico da transcrição carregada no **DriftScript** (`http://127.0.0.1:4732`) e aplique a marcação visual de cores no **Medidor de Relevância** da interface, sem apagar nem riscar automaticamente as falas (a menos que o usuário peça explicitamente o corte depois).

## Escala de Cores e Categorias

O DriftScript inicia com todo o texto branco (sem avaliação). Ao aplicar esta skill, classifique todos os blocos de fala contíguos (`[start_index, end_index]`) usando dois parâmetros (`score` e `category`):

1. **Verde (`category: "relevant"`, `score: 0.70` a `1.00`) — Alta Relevância**:
   - Tese principal, explicações diretas do funcionamento, demonstrações práticas essenciais e conclusões objetivas.
2. **Amarelo (`category: "relevant"`, `score: 0.40` a `0.69`) — Relevância Moderada**:
   - Contextualização secundária, exemplos auxiliares, ressalvas úteis ou transições naturais de raciocínio.
3. **Vermelho (`category: "relevant"`, `score: 0.00` a `0.39`) — Baixa Relevância / Redundância**:
   - Repetições da mesma ideia já explicada melhor antes ou depois, hesitações longas, rodeios prolixos ou tentativas de fala recomeçadas (*false starts*).
4. **Azul (`category: "off_topic"`, `score: 0.00`) — Fora do Assunto / Desvios / Interrupções**:
   - Comentários de bastidores ("deixa eu arrumar a câmera", "peraí que caiu o fio"), interrupções externas, tangentes sem relação com o tema do vídeo ou digressões.

## Fluxo de Execução

### 1. Ler a Transcrição em Blocos

Execute o script auxiliar para obter a transcrição agrupada por parágrafos com os intervalos de índices `[início..fim]`:

```bash
python3 /home/davi/repos/tyrion-skills/skills/analisar-relevancia-da-transcricao/scripts/aplicar_relevancia.py ler
```

### 2. Identificar o Tema Central e Avaliar os Trechos

1. Se o usuário especificou um foco (ex.: *"foco apenas na explicação do circuito do Arduino"*), use esse critério como referência de relevância máxima (`1.0`). Caso contrário, deduza o tema central a partir do próprio vídeo.
2. Segmente a transcrição em faixas cobrindo do primeiro ao último índice (`0` até `total_words - 1`). Quando uma frase tiver partes de relevâncias diferentes (ex.: uma frase começa relevante e termina num desvio ou erro de gravação), divida os intervalos nos índices exatos das palavras.
3. Forneça sempre um `reason` curto em português (ex.: `"Explicação central do receptor"`, `"Repetição da mesma frase"`, `"Desvio sobre ajuste da câmera"`) — esse texto aparece como *tooltip* ao passar o mouse sobre a palavra na interface do DriftScript.

### 3. Aplicar as Cores no DriftScript

Salve o JSON de anotações ou passe via `stdin` para o script auxiliar:

```bash
python3 /home/davi/repos/tyrion-skills/skills/analisar-relevancia-da-transcricao/scripts/aplicar_relevancia.py aplicar << 'EOF'
{
  "clear": true,
  "annotations": [
    {
      "start_index": 0,
      "end_index": 85,
      "score": 0.92,
      "category": "relevant",
      "reason": "Apresentação direta do projeto e objetivo"
    },
    {
      "start_index": 86,
      "end_index": 140,
      "score": 0.20,
      "category": "relevant",
      "reason": "Explicação repetida / tentativa recomeçada"
    },
    {
      "start_index": 141,
      "end_index": 175,
      "score": 0.0,
      "category": "off_topic",
      "reason": "Pausa para ajustar foco da câmera"
    }
  ]
}
EOF
```

### 4. Relatório Conciso ao Usuário

Após aplicar as cores na interface:
- Informe o tema central considerado na análise.
- Resuma em 3 a 5 linhas os principais trechos marcados em **Vermelho** (candidatos a corte ou aceleração) e em **Azul** (desvios/interrupções), indicando que o usuário pode selecioná-los com 1 clique pelo filtro `🔴 Pouco Relevantes` ou `🔵 Fora do Assunto` na barra do DriftScript.

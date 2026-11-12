# Tyrion Skills

**Um conjunto de habilidades para transformar pedidos a agentes de programação em fluxos de trabalho claros, reutilizáveis e cuidadosos.**

Da edição de vídeo por transcrição ao planejamento com vários agentes, cada habilidade reúne instruções e, quando necessário, arquivos de apoio para uma tarefa específica.

[Conheça as habilidades](#habilidades) · [Instale](#instalação) · [Comece a usar](#como-usar) · [Entenda a estrutura](#estrutura-do-repositório)

## O que é uma skill?

Uma **skill** (habilidade) é uma pasta com um arquivo `SKILL.md` que orienta o agente sobre quando e como realizar uma tarefa. O instalador deste repositório atende ao Codex; algumas habilidades também são voltadas a outros agentes, como o Antigravity. Algumas incluem também scripts (programas auxiliares), referências ou recursos visuais. Você pode chamar uma habilidade pelo nome ou descrever o que deseja fazer; a escolha depende das instruções da habilidade e do contexto da conversa.

## Habilidades

| Habilidade | Para que serve | Exemplo de pedido |
|---|---|---|
| [analisar-relevancia-da-transcricao](skills/analisar-relevancia-da-transcricao/SKILL.md) | Classifica falas no medidor de relevância do DriftScript, sem cortá-las automaticamente. | “Analise a relevância da transcrição.” |
| [conectar-driftscript](skills/conectar-driftscript/SKILL.md) | Conecta ou usa o DriftScript para editar um vídeo a partir da transcrição. | “Encurte as pausas deste vídeo pelo DriftScript.” |
| [antigravity-ultramode](skills/antigravity-ultramode/SKILL.md) | Conduz projetos grandes e abertos no Antigravity com especialistas paralelos, revisão técnica e visual, comparação de abordagens e remoção de excessos. | “Use antigravity-ultramode para criar este produto, explorar capacidades úteis e verificar os fluxos.” |
| [planejar-multiagentes](skills/planejar-multiagentes/SKILL.md) | Transforma uma ideia já discutida em um planejamento para execução por vários agentes. | “Use planejar-multiagentes para preparar este projeto.” |
| [executar-multiagentes](skills/executar-multiagentes/SKILL.md) | Localiza um planejamento `INICIAR.md` e coordena sua execução ou retomada. | “Use executar-multiagentes neste planejamento.” |
| [limpeza-final-segura](skills/limpeza-final-segura/SKILL.md) | Cuida dos arquivos auxiliares criados durante uma tarefa, preservando o que ainda for necessário. | “Ao terminar, use $limpeza-final-segura.” |
| [make-it-glow](skills/make-it-glow/SKILL.md) | Propõe melhorias visuais para um artefato existente, com prévia antes de aplicá-las. | “Use make-it-glow para melhorar a aparência desta página.” |
| [skill-wizard](skills/skill-wizard/SKILL.md) | Conduz uma entrevista para criar ou melhorar uma habilidade. | “Use skill-wizard para criar uma skill.” |

> As habilidades de vídeo dependem do CutWire Drift e do complemento DriftScript. Algumas instruções e scripts usam caminhos absolutos da máquina original; leia o `SKILL.md` correspondente e adapte os caminhos e as dependências ao seu ambiente antes de usá-los.

## Instalação

### Pré-requisitos

- Codex instalado e configurado.
- Git, Bash e os comandos básicos de arquivos disponíveis no terminal. O instalador foi escrito para um ambiente Unix; no Windows, use um ambiente compatível, como o Subsistema do Windows para Linux (WSL).
- Dependências específicas da habilidade que deseja usar, descritas no respectivo `SKILL.md`.

### Instale todas as habilidades

```bash
# Baixe o repositório para uma pasta dentro de repos na sua pasta pessoal.
git clone https://github.com/TyrionV8/tyrion-skills.git "$HOME/repos/tyrion-skills"

# Entre na pasta baixada.
cd "$HOME/repos/tyrion-skills"

# Crie os links das habilidades no perfil do Codex.
./install.sh
```

O instalador cria **links simbólicos** — atalhos no sistema de arquivos — para as pastas em `skills/`. Eles ficam em `$CODEX_HOME/skills/` quando a variável de ambiente `CODEX_HOME` está definida; caso contrário, em `~/.codex/skills/`. Como os links apontam para este repositório, mantenha a pasta clonada no lugar.

A execução é repetível: links que já apontam para a pasta correta são mantidos. Se houver um arquivo, uma pasta ou um link diferente com o mesmo nome, o instalador para sem substituí-lo. Ele processa as habilidades em sequência, então algumas podem já ter sido instaladas antes de encontrar um conflito. Confira o destino indicado na mensagem, preserve o conteúdo existente e resolva o conflito antes de executar novamente.

### Atualize

```bash
# Na pasta do repositório, obtenha as alterações remotas.
git pull --ff-only

# Instale também eventuais habilidades novas.
./install.sh
```

A opção `--ff-only` atualiza apenas quando o histórico local pode avançar diretamente, sem criar uma mesclagem. Os links existentes acompanham os arquivos atualizados no repositório.

## Como usar

1. Abra o Codex no projeto ou contexto da tarefa.
2. Peça a ação em linguagem natural ou mencione explicitamente a habilidade, por exemplo: `Use skill-wizard para me ajudar a criar uma skill`.
3. Siga o fluxo e as confirmações previstos na habilidade. Para conhecer os detalhes, abra o arquivo `SKILL.md` da tabela acima.

Se uma habilidade recém-instalada não aparecer, inicie uma nova sessão do Codex e confira o link na pasta de habilidades do seu perfil. Instalar uma habilidade não instala automaticamente os aplicativos externos de que ela possa depender.

### Construções grandes no Antigravity

A `antigravity-ultramode` foi pensada para iniciar produtos e conduzir tarefas de escopo aberto. Os especialistas avaliam o funcionamento, a implementação e a interface; podem recomendar remoções ou substituir uma abordagem inadequada. O esforço adicional deve gerar qualidade e capacidades úteis, sem multiplicar textos, controles ou variações da mesma ação.

Com a skill disponível no catálogo do Antigravity, experimente:

> Use antigravity-ultramode para criar um aplicativo de referências visuais. Quero adicionar materiais, encontrar o que preciso e reutilizá-los. Explore capacidades adicionais úteis, use especialistas paralelos disponíveis e entregue uma interface limpa com os fluxos verificados.

O `install.sh` não configura o Antigravity. A pasta da skill precisa estar acessível no diretório de descoberta da instalação utilizada. A execução paralela depende das ferramentas disponíveis na sessão; sem elas, a skill orienta revisões sequenciais e exige informar a limitação. Ela não altera o modelo nem ativa um modo interno de raciocínio.

## Estrutura do repositório

```text
tyrion-skills/
├── install.sh                  # Instala as habilidades por links simbólicos
└── skills/
    └── nome-da-habilidade/
        ├── SKILL.md            # Quando e como usar a habilidade
        ├── scripts/            # Programas auxiliares, quando necessários
        ├── references/         # Documentação de apoio, quando necessária
        └── assets/             # Recursos de apoio, quando necessários
```

Cada habilidade é independente: consulte suas instruções antes de executá-la ou adaptá-la. Pastas de apoio aparecem apenas quando a habilidade precisa delas.

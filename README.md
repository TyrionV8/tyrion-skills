# Tyrion Skills

Skills pessoais publicadas para uso com o Codex.

## Conteúdo

- `limpeza-final-segura/`: limpeza segura de arquivos auxiliares criados na tarefa.
- `make-it-glow/`: melhorias visuais em artefatos existentes.
- `skill-wizard/`: criação e melhoria de skills.

## Instalar

Com o Codex instalado, clone o repositório e execute o instalador:

```bash
git clone https://github.com/Tyrion1606/tyrion-skills.git "$HOME/repos/tyrion-skills"
cd "$HOME/repos/tyrion-skills"
./install.sh
```

O instalador cria atalhos simbólicos para as skills em `$CODEX_HOME/skills/`,
ou em `~/.codex/skills/` se `CODEX_HOME` não estiver configurado. Se já
existir uma pasta com o mesmo nome, ele para sem substituí-la; mova-a para um
backup e execute novamente.

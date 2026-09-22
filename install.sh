#!/usr/bin/env bash
set -Eeuo pipefail

# Descobre a pasta deste repositório, mesmo quando chamado de outro diretório.
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

# Usa CODEX_HOME quando definido; caso contrário, usa o perfil padrão do usuário.
CODEX_PROFILE_DIR="${CODEX_HOME:-${HOME}/.codex}"
SKILLS_DIR="${CODEX_PROFILE_DIR}/skills"
mkdir -p -- "$SKILLS_DIR"

shopt -s nullglob
skill_dirs=("${REPO_ROOT}"/skills/*)
if (( ${#skill_dirs[@]} == 0 )); then
    printf 'Erro: não há skills em %s/skills\n' "$REPO_ROOT" >&2
    exit 1
fi

for source_dir in "${skill_dirs[@]}"; do
    [[ -d "$source_dir" ]] || continue
    skill_name="${source_dir##*/}"
    target="${SKILLS_DIR}/${skill_name}"

    if [[ ! -f "${source_dir}/SKILL.md" ]]; then
        printf 'Erro: não encontrei %s/SKILL.md\n' "$source_dir" >&2
        exit 1
    fi

    if [[ -L "$target" ]]; then
        if [[ "$(readlink -f -- "$target")" == "$(readlink -f -- "$source_dir")" ]]; then
            printf 'Já instalado: %s\n' "$skill_name"
            continue
        fi
        printf 'Erro: já existe um atalho diferente em %s\n' "$target" >&2
        exit 1
    fi

    if [[ -e "$target" ]]; then
        printf 'Erro: já existe %s; mova ou faça backup antes de continuar.\n' "$target" >&2
        exit 1
    fi

    ln -s -- "$source_dir" "$target"
    printf 'Instalado: %s -> %s\n' "$skill_name" "$source_dir"
done

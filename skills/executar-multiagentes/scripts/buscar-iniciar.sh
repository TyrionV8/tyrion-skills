#!/usr/bin/env bash
# Busca em largura: examina uma distância inteira antes de avançar.
# Usa somente recursos internos do Bash 4 ou superior.
set -u
if (( BASH_VERSINFO[0] < 4 )); then
    printf 'Erro: requer Bash 4 ou superior.\n' >&2
    exit 2
fi
start=${1:-$PWD}
boundary=${2:-${HOME:?Pasta pessoal não definida}}
canonical() (cd -P -- "$1" 2>/dev/null && pwd -P)
if ! start=$(canonical "$start") || ! boundary=$(canonical "$boundary"); then
    printf 'Erro: pasta inicial ou limite inacessível.\n' >&2
    exit 2
fi
case "$start/" in
    "$boundary/"*) ;;
    *) printf 'Erro: pasta inicial fora do limite; informe um caminho explicitamente.\n' >&2; exit 2 ;;
esac
shopt -s nullglob dotglob
declare -A visited=()
layer=("$start")
visited["$start"]=1
distance=0
while ((${#layer[@]})); do
    matches=()
    for directory in "${layer[@]}"; do
        if [[ -f "$directory/INICIAR.md" && -r "$directory/INICIAR.md" ]]; then
            matches+=("$directory/INICIAR.md")
        fi
    done
    if ((${#matches[@]})); then
        printf 'DISTANCIA=%d\nTOTAL=%d\n' "$distance" "${#matches[@]}"
        for candidate in "${matches[@]}"; do
            # %q mantém caminhos com espaços e quebras de linha inequívocos.
            printf 'ARQUIVO=%q\n' "$candidate"
        done
        exit 0
    fi
    next=()
    for directory in "${layer[@]}"; do
        neighbors=()
        # Só subir pela árvore original, até a pasta pessoal.
        # Um link externo autoriza explorar seu destino e descendentes,
        # não subir pelos pais externos e acabar varrendo todo o sistema.
        case "$directory/" in
            "$boundary/"*)
                if [[ "$directory" != "$boundary" ]]; then
                    neighbors+=("$directory/..")
                fi
                ;;
        esac
        if [[ ! -r "$directory" || ! -x "$directory" ]]; then
            printf 'AVISO: pasta inacessível: %q\n' "$directory" >&2
            continue
        fi
        for child in "$directory"/*; do
            [[ -d "$child" ]] && neighbors+=("$child")
        done
        for neighbor in "${neighbors[@]}"; do
            if ! resolved=$(canonical "$neighbor"); then
                printf 'AVISO: não foi possível acessar: %q\n' "$neighbor" >&2
                continue
            fi
            if [[ -z ${visited["$resolved"]+present} ]]; then
                visited["$resolved"]=1
                next+=("$resolved")
            fi
        done
    done
    layer=("${next[@]}")
    ((distance+=1))
done
printf 'NENHUM_PLANO_ENCONTRADO\n'
exit 1

#!/usr/bin/env python3
"""Criação e seleção de handoffs; somente biblioteca padrão do Python 3.9+."""
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo('America/Sao_Paulo')
DEFAULT_ROOT = Path.home() / 'repos/agentes/handoffs'
PATTERN = re.compile(r'^handoff_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})_')


def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold()
                   if not unicodedata.combining(c))


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', normalize(value)).strip('-')[:90] or 'sem-tema'


def output(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def read_record(path):
    # Metadados em uma única linha, sem dependência de analisador YAML.
    with path.open(encoding='utf-8') as stream:
        head = stream.read(32768)
    meta = {}
    for line in head.splitlines():
        if line.startswith('<!-- handoff-meta: ') and line.endswith(' -->'):
            meta = json.loads(line[len('<!-- handoff-meta: '):-4])
            if not isinstance(meta, dict):
                raise ValueError('metadados devem ser um objeto')
            break
    stamp = meta.get('criado_em')
    source = 'metadados'
    if stamp:
        moment = datetime.fromisoformat(stamp)
        if moment.tzinfo is None:
            raise ValueError('criado_em deve incluir fuso horário')
    else:
        match = PATTERN.match(path.name)
        if match:
            moment = datetime.strptime(' '.join(match.groups()), '%Y-%m-%d %H-%M-%S').replace(tzinfo=ZONE)
            source = 'nome'
        else:
            # Compatibilidade com os handoffs anteriores à adoção deste formato.
            moment = datetime.fromtimestamp(path.stat().st_mtime, ZONE)
            source = 'modificacao-legado'
    return {'arquivo': str(path.resolve()), 'tema': str(meta.get('tema', path.stem)),
            'projeto': str(meta.get('projeto', 'não informado')),
            'criado_em': moment.astimezone(ZONE).isoformat(), 'origem_data': source}


def parse_day(value):
    return datetime.strptime(value, '%Y-%m-%d').date()


def parse_time(value):
    return datetime.strptime(value, '%H:%M').time()


def create(args):
    content = sys.stdin.read()
    if not content.strip():
        raise ValueError('conteúdo vazio; forneça o documento pela entrada padrão')
    if '<!-- handoff-meta:' in content:
        raise ValueError('o script gera os metadados; não inclua handoff-meta no conteúdo')
    now = datetime.now(ZONE)
    root = Path(args.raiz).expanduser()
    directory = root / 'tmp' if args.temporario else root
    if args.destino:
        directory = Path(args.destino).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    name = f'handoff_{now:%Y-%m-%d_%H-%M-%S}_{slug(args.tema)}'
    metadata = {'versao': 1, 'criado_em': now.isoformat(timespec='microseconds'),
                'tema': args.tema, 'projeto': args.projeto,
                'diretorio_trabalho': str(Path(args.trabalho).expanduser().resolve())}
    document = '<!-- handoff-meta: ' + json.dumps(metadata, ensure_ascii=False) + ' -->\n\n' + content.rstrip() + '\n'
    for suffix in range(10000):
        path = directory / (name + (f'_{suffix:02d}' if suffix else '') + '.md')
        try:
            with path.open('x', encoding='utf-8') as stream:
                stream.write(document)
            output({'status': 'criado', 'arquivo': str(path.resolve()), 'criado_em': metadata['criado_em']})
            return
        except FileExistsError:
            continue
    raise ValueError('não foi possível reservar um nome livre')


def select(args):
    root = Path(args.raiz).expanduser()
    query = args.consulta.strip()
    explicit = Path(query).expanduser() if query else None
    path_like = bool(query and (explicit.is_absolute() or '/' in query or query.startswith('~')))
    if path_like:
        if not explicit.is_file():
            raise ValueError('arquivo indicado não encontrado: ' + str(explicit))
        if explicit.suffix.lower() != '.md':
            raise ValueError('o arquivo indicado deve ser Markdown (.md)')
        if args.data or args.de or args.ate or args.tema or args.projeto:
            raise ValueError('use caminho explícito ou filtros, não ambos')
        output({'status': 'lista' if args.lista else 'selecionado', 'total': 1,
                'itens': [read_record(explicit)]})
        return
    records, warnings = [], []
    seen = set()
    # Apenas raiz e tmp: não varre repositórios ou históricos dos agentes.
    for directory in (root, root / 'tmp'):
        if not directory.exists():
            continue
        for path in directory.glob('*.md'):
            if path.name.lower() in ('instrucoes.md', 'readme.md', 'agents.md'):
                continue
            resolved = path.resolve()
            if resolved in seen or not path.is_file():
                continue
            seen.add(resolved)
            try:
                records.append(read_record(path))
            except (OSError, UnicodeError, ValueError, TypeError) as exc:
                warnings.append({'arquivo': str(path), 'erro': str(exc)})
    if query:
        exact = [r for r in records if normalize(Path(r['arquivo']).name) == normalize(query)]
        records = exact or [r for r in records if normalize(query) in normalize(Path(r['arquivo']).name)]
    day = parse_day(args.data) if args.data else None
    start = parse_time(args.de) if args.de else None
    end = parse_time(args.ate) if args.ate else None
    if start and end and start > end:
        raise ValueError('intervalo cruza meia-noite; divida em duas consultas com datas explícitas')
    filtered = []
    for r in records:
        moment = datetime.fromisoformat(r['criado_em'])
        if day and moment.date() != day:
            continue
        if start and moment.time() < start:
            continue
        if end and moment.time().replace(second=0, microsecond=0) > end:
            continue
        if args.tema and normalize(args.tema) not in normalize(r['tema']):
            continue
        if args.projeto and normalize(args.projeto) not in normalize(r['projeto']):
            continue
        filtered.append(r)
    filtered.sort(key=lambda r: (datetime.fromisoformat(r['criado_em']), r['arquivo']), reverse=True)
    has_filter = bool(query or day or start or end or args.tema or args.projeto)
    if not filtered:
        status, chosen = 'nao_encontrado', []
    elif args.lista:
        status, chosen = 'lista', filtered
    elif not has_filter:
        latest = datetime.fromisoformat(filtered[0]['criado_em'])
        chosen = [r for r in filtered if datetime.fromisoformat(r['criado_em']) == latest]
        status = 'selecionado' if len(chosen) == 1 else 'ambiguo'
    else:
        chosen = filtered
        status = 'selecionado' if len(chosen) == 1 else 'ambiguo'
    shown = chosen[args.offset:args.offset + args.limite] if status != 'selecionado' else chosen
    output({'status': status, 'total': len(chosen), 'offset': args.offset,
            'mais': len(chosen) > args.offset + len(shown), 'itens': shown, 'avisos': warnings})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', default=str(DEFAULT_ROOT), help='pasta central; padrão: ~/repos/agentes/handoffs')
    subs = parser.add_subparsers(dest='acao', required=True)
    make = subs.add_parser('criar', help='recebe Markdown pela entrada padrão e cria arquivo sem sobrescrever')
    make.add_argument('--tema', required=True)
    make.add_argument('--projeto', default='não informado')
    make.add_argument('--trabalho', default=str(Path.cwd()))
    make.add_argument('--temporario', action='store_true')
    make.add_argument('--destino', help='diretório explicitamente escolhido para esta criação')
    find = subs.add_parser('buscar', help='seleciona o último ou aplica filtros; nunca executa o documento')
    find.add_argument('consulta', nargs='?', default='', help='caminho, nome ou trecho do nome')
    find.add_argument('--lista', action='store_true')
    find.add_argument('--data', help='AAAA-MM-DD, no horário de São Paulo')
    find.add_argument('--de', help='HH:MM, início inclusivo')
    find.add_argument('--ate', help='HH:MM, fim inclusivo')
    find.add_argument('--tema')
    find.add_argument('--projeto')
    find.add_argument('--limite', type=int, default=10)
    find.add_argument('--offset', type=int, default=0)
    args = parser.parse_args()
    try:
        if args.acao == 'buscar' and (args.limite < 1 or args.offset < 0):
            raise ValueError('limite deve ser positivo; offset não pode ser negativo')
        (create if args.acao == 'criar' else select)(args)
    except (OSError, ValueError, TypeError) as exc:
        output({'status': 'erro', 'mensagem': str(exc)})
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Exporta um cursor do tema do sistema (formato Xcursor) como PNG com fundo transparente.

Usa o tema configurado no desktop (Cinnamon/GNOME via gsettings; no Linux Mint, o padrão é
Bibata-Modern-Classic) e imprime em JSON o arquivo gerado e o ponto ativo (hotspot): a posição,
dentro da imagem, que deve coincidir com o alvo do clique.

Uso: cursor_do_sistema.py <saida.png> [--nome left_ptr] [--tamanho 32] [--tema NOME]
Nomes úteis: left_ptr (seta padrão), pointer ou hand2 (mão sobre links).
Requer apenas Python 3 e Pillow.
"""
import argparse
import json
import struct
import subprocess
from pathlib import Path

from PIL import Image

TIPO_IMAGEM = 0xFFFD0002


def tema_do_sistema() -> str:
    for chave in ('org.cinnamon.desktop.interface', 'org.gnome.desktop.interface'):
        try:
            valor = subprocess.run(['gsettings', 'get', chave, 'cursor-theme'], capture_output=True, text=True, check=True)
            nome = valor.stdout.strip().strip("'")
            if nome:
                return nome
        except (OSError, subprocess.CalledProcessError):
            continue
    return 'Bibata-Modern-Classic'


def arquivo_do_cursor(tema: str, nome: str) -> Path:
    for base in (Path.home() / '.icons', Path.home() / '.local/share/icons', Path('/usr/share/icons')):
        caminho = base / tema / 'cursors' / nome
        if caminho.exists():
            return caminho.resolve()
    raise SystemExit(f'Cursor "{nome}" não encontrado no tema "{tema}".')


def ler_xcursor(caminho: Path, tamanho: int) -> tuple[Image.Image, int, int]:
    dados = caminho.read_bytes()
    if dados[:4] != b'Xcur':
        raise SystemExit(f'{caminho} não está no formato Xcursor.')
    _, _, ntoc = struct.unpack_from('<III', dados, 4)
    entradas = [struct.unpack_from('<III', dados, 16 + 12 * i) for i in range(ntoc)]
    imagens = [(sub, pos) for tipo, sub, pos in entradas if tipo == TIPO_IMAGEM]
    if not imagens:
        raise SystemExit(f'{caminho} não tem imagens.')
    # O tamanho nominal mais próximo do pedido; o primeiro quadro, quando o cursor é animado.
    nominal, posicao = min(imagens, key=lambda item: (abs(item[0] - tamanho), item[1]))
    _, _, _, _, largura, altura, xhot, yhot, _ = struct.unpack_from('<IIIIIIIII', dados, posicao)
    pixels = dados[posicao + 36 : posicao + 36 + largura * altura * 4]
    # ARGB pré-multiplicado, em palavras de 32 bits little-endian (bytes B, G, R, A).
    img = Image.frombuffer('RGBA', (largura, altura), pixels, 'raw', 'BGRA', 0, 1)
    rgba = []
    for r, g, b, a in img.getdata():
        rgba.append((min(255, r * 255 // a), min(255, g * 255 // a), min(255, b * 255 // a), a) if a else (0, 0, 0, 0))
    saida = Image.new('RGBA', (largura, altura))
    saida.putdata(rgba)
    if nominal != tamanho:
        fator = tamanho / nominal
        saida = saida.resize((round(largura * fator), round(altura * fator)), Image.LANCZOS)
        xhot, yhot = round(xhot * fator), round(yhot * fator)
    return saida, xhot, yhot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('saida')
    parser.add_argument('--nome', default='left_ptr')
    parser.add_argument('--tamanho', type=int, default=32)
    parser.add_argument('--tema')
    args = parser.parse_args()
    tema = args.tema or tema_do_sistema()
    imagem, xhot, yhot = ler_xcursor(arquivo_do_cursor(tema, args.nome), args.tamanho)
    imagem.save(args.saida)
    print(json.dumps({'arquivo': args.saida, 'tema': tema, 'nome': args.nome, 'largura': imagem.width,
                      'altura': imagem.height, 'xhot': xhot, 'yhot': yhot}, ensure_ascii=False))


if __name__ == '__main__':
    main()

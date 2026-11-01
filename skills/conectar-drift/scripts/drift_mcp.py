#!/usr/bin/env python3
"""Verifica, configura e usa a conexão MCP com o editor de vídeo Drift.

O token é lido do arquivo de configuração do próprio Drift a cada execução e
nunca é exibido. Subcomandos:

  verificar   diagnostica o Drift e compara as configurações dos agentes
  configurar  faz o diagnóstico e corrige as configurações (com backup)
  chamar      chama uma ferramenta do Drift diretamente, sem depender do agente

Códigos de saída: 0 pronto; 1 erro de uso ou da ferramenta chamada;
2 Drift indisponível; 3 token recusado; 4 falha ao gravar uma configuração.
"""

from __future__ import annotations

import argparse
import base64
import configparser
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

URL_PADRAO = "http://127.0.0.1:4731/mcp"
NOME = "drift"
CLIENTES = ("antigravity", "claude", "codex")
HOME = Path.home()


class Falha(Exception):
    """Falha com código de diagnóstico e orientações para o usuário."""

    def __init__(self, codigo: str, mensagem: str, acoes: list[str], saida: int = 2):
        super().__init__(mensagem)
        self.codigo = codigo
        self.mensagem = mensagem
        self.acoes = acoes
        self.saida = saida


def linha(estado: str, texto: str) -> None:
    print(f"[{estado}] {texto}", flush=True)


def caminho_curto(p: Path | str) -> str:
    s = str(p)
    h = str(HOME)
    return "~" + s[len(h):] if s.startswith(h + "/") else s


# --------------------------------------------------------------------------
# Drift: arquivo de configuração, processo e porta
# --------------------------------------------------------------------------

def arquivo_conf_drift() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
    return base / "CutWire Drift" / "CutWire Drift.conf"


def ler_token() -> str:
    conf = arquivo_conf_drift()
    if not conf.is_file():
        raise Falha(
            "drift_sem_configuracao",
            f"Não encontrei {caminho_curto(conf)}.",
            [
                "Confira se o Drift está instalado e abra-o pelo menos uma vez "
                "(ele cria esse arquivo ao iniciar).",
                "Depois, peça novamente para conectar o Drift.",
            ],
        )
    parser = configparser.RawConfigParser(strict=False, interpolation=None)
    parser.optionxform = str  # preserva maiúsculas das chaves do Qt
    parser.read(conf, encoding="utf-8")
    token = parser.get("mcp", "token", fallback="").strip()
    if not token:
        raise Falha(
            "drift_sem_token",
            f"A seção [mcp] de {caminho_curto(conf)} não tem token.",
            [
                "No Drift, abra as configurações e ative o servidor MCP "
                "(e a opção de iniciá-lo ao abrir o programa).",
                "Depois, peça novamente para conectar o Drift.",
            ],
        )
    linha("ok", f"Token lido de {caminho_curto(conf)} ({len(token)} caracteres; não exibido)")
    inicio = parser.get("mcp", "startOnLaunch", fallback="").strip().lower()
    if inicio and inicio != "true":
        linha("aviso", "O Drift não está configurado para iniciar o servidor MCP ao abrir "
                       "(startOnLaunch não é true).")
    return token


def pids_drift() -> list[int]:
    pids = []
    proprio = os.getpid()
    for d in Path("/proc").iterdir():
        if not d.name.isdigit() or int(d.name) == proprio:
            continue
        try:
            argv0 = (d / "cmdline").read_bytes().split(b"\0", 1)[0].decode(errors="replace")
            exe = os.readlink(d / "exe") if (d / "exe").exists() else ""
        except OSError:
            continue
        if Path(argv0).name == "drift" or Path(exe).name == "drift":
            pids.append(int(d.name))
    return pids


def portas_escutando(pids: list[int]) -> list[str]:
    if not pids or not shutil.which("ss"):
        return []
    try:
        saida = subprocess.run(["ss", "-ltnpH"], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    encontradas = []
    for ln in saida.splitlines():
        if any(f"pid={p}," in ln for p in pids):
            partes = ln.split()
            if len(partes) >= 4:
                encontradas.append(partes[3])
    return sorted(set(encontradas))


def diagnosticar_sem_conexao(url: str, erro: str) -> Falha:
    pids = pids_drift()
    executavel = shutil.which("drift")
    if not pids:
        abrir = (f"Abra o Drift pelo menu de aplicativos ou com `{caminho_curto(executavel)} &` "
                 "no terminal." if executavel else "Abra o Drift pelo menu de aplicativos.")
        return Falha(
            "drift_fechado",
            f"Nada respondeu em {url} e o Drift não está em execução ({erro}).",
            [abrir, "Aguarde o projeto carregar e peça novamente para conectar o Drift."],
        )
    portas = portas_escutando(pids)
    acoes = [
        "O Drift está aberto, mas o servidor MCP não respondeu nesse endereço. "
        "No Drift, abra as configurações e confira se o servidor MCP está ativado.",
    ]
    if portas:
        acoes.append("O Drift está escutando em: " + ", ".join(portas) + ". Se o endereço "
                     "mostrado pelo Drift for outro, informe-o (sem o token) para que a "
                     "conexão use a variável DRIFT_MCP_URL.")
    acoes.append("Se continuar falhando, feche e abra o Drift de novo.")
    return Falha("mcp_desligado", f"O Drift está aberto, mas {url} não respondeu ({erro}).", acoes)


# --------------------------------------------------------------------------
# Cliente MCP mínimo (HTTP transmissível)
# --------------------------------------------------------------------------

class ClienteMCP:
    def __init__(self, url: str, token: str, timeout: float):
        self.url = url
        self.token = token
        self.timeout = timeout
        self.sessao: str | None = None
        self.proximo_id = 1

    def _enviar(self, corpo: dict) -> tuple[int, dict | None]:
        cab = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.sessao:
            cab["Mcp-Session-Id"] = self.sessao
        req = urllib.request.Request(self.url, data=json.dumps(corpo).encode(), headers=cab,
                                     method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                self.sessao = resp.headers.get("Mcp-Session-Id") or self.sessao
                tipo = resp.headers.get("Content-Type", "")
                bruto = resp.read().decode("utf-8", errors="replace")
                return resp.status, self._interpretar(bruto, tipo, corpo.get("id"))
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise Falha(
                    "token_recusado",
                    f"O Drift recusou o token (HTTP {e.code}).",
                    [
                        "O token salvo no arquivo do Drift não é o que o servidor está usando. "
                        "Feche e abra o Drift para que ele grave e use o mesmo token.",
                        "Se o Drift permitir gerar um token novo, gere-o, feche e abra o "
                        "programa. Não cole o token no chat.",
                        "Depois, peça novamente para conectar o Drift.",
                    ],
                    saida=3,
                ) from None
            raise Falha("erro_http", f"O Drift respondeu HTTP {e.code}.",
                        ["Feche e abra o Drift e tente novamente."]) from None
        except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError) as e:
            motivo = getattr(e, "reason", e)
            raise diagnosticar_sem_conexao(self.url, str(motivo)) from None

    @staticmethod
    def _interpretar(bruto: str, tipo: str, ident) -> dict | None:
        if not bruto.strip():
            return None
        if "text/event-stream" in tipo:
            ultimo = None
            for ln in bruto.splitlines():
                if ln.startswith("data:"):
                    try:
                        msg = json.loads(ln[5:].strip())
                    except json.JSONDecodeError:
                        continue
                    if ident is None or msg.get("id") == ident:
                        ultimo = msg
            return ultimo
        return json.loads(bruto)

    def requisitar(self, metodo: str, params: dict | None = None) -> dict:
        ident = self.proximo_id
        self.proximo_id += 1
        _, msg = self._enviar({"jsonrpc": "2.0", "id": ident, "method": metodo,
                               "params": params or {}})
        if not msg:
            raise Falha("resposta_vazia", f"O Drift não respondeu a {metodo}.",
                        ["Feche e abra o Drift e tente novamente."])
        if "error" in msg:
            raise Falha("erro_mcp", f"{metodo}: {msg['error']}", [], saida=1)
        return msg.get("result", {})

    def iniciar(self) -> dict:
        res = self.requisitar("initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "conectar-drift", "version": "1"},
        })
        self._enviar({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return res


def testar_conexao(url: str, token: str) -> None:
    cliente = ClienteMCP(url, token, timeout=10)
    info = cliente.iniciar()
    servidor = info.get("serverInfo", {})
    nome = " ".join(str(v) for v in (servidor.get("name"), servidor.get("version")) if v)
    ferramentas = cliente.requisitar("tools/list").get("tools", [])
    extra = f" ({nome})" if nome else ""
    linha("ok", f"Servidor MCP respondeu em {url}{extra}; {len(ferramentas)} ferramentas disponíveis")


# --------------------------------------------------------------------------
# Configurações dos agentes
# --------------------------------------------------------------------------

def arquivo_cliente(cliente: str) -> Path:
    if cliente == "antigravity":
        return HOME / ".gemini" / "config" / "mcp_config.json"
    if cliente == "claude":
        base = os.environ.get("CLAUDE_CONFIG_DIR")
        return Path(base) / ".claude.json" if base else HOME / ".claude.json"
    base = os.environ.get("CODEX_HOME")
    return (Path(base) if base else HOME / ".codex") / "config.toml"


def gravar_atomico(destino: Path, conteudo: str) -> Path:
    """Grava no arquivo real (seguindo links) e devolve o caminho do backup."""
    real = destino.resolve()
    real.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    modo = 0o600
    if real.exists():
        modo = real.stat().st_mode & 0o777
        backup = real.with_name(f"{real.name}.bak-conectar-drift-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(real, backup)
    fd, tmp = tempfile.mkstemp(dir=real.parent, prefix=f".{real.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(conteudo)
        os.chmod(tmp, modo)
        os.replace(tmp, real)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return backup


def estado_json(caminho: Path, cliente: str, url: str, token: str) -> tuple[str, dict | None]:
    if not caminho.exists():
        return "ausente", None
    dados = json.loads(caminho.read_text(encoding="utf-8") or "{}")
    entrada = dados.get("mcpServers", {}).get(NOME)
    if not isinstance(entrada, dict):
        return "ausente", dados
    ok = (entrada.get("url") == url
          and entrada.get("headers", {}).get("Authorization") == f"Bearer {token}"
          and (cliente != "claude" or entrada.get("type") == "http"))
    return ("correto" if ok else "desatualizado"), dados


def corrigir_json(caminho: Path, cliente: str, dados: dict | None, url: str, token: str) -> Path:
    dados = dados if isinstance(dados, dict) else {}
    servidores = dados.setdefault("mcpServers", {})
    entrada = servidores.get(NOME) if isinstance(servidores.get(NOME), dict) else {}
    if cliente == "claude":
        entrada["type"] = "http"
    entrada["url"] = url
    entrada.setdefault("headers", {})["Authorization"] = f"Bearer {token}"
    servidores[NOME] = entrada
    backup = gravar_atomico(caminho, json.dumps(dados, indent=2, ensure_ascii=False) + "\n")
    novo, _ = estado_json(caminho, cliente, url, token)
    if novo != "correto":
        raise Falha("gravacao_invalida", f"A verificação de {caminho_curto(caminho)} falhou "
                    "após a gravação.", [f"Backup: {caminho_curto(backup)}" if backup else ""], 4)
    return backup


CABECALHO_TOML = re.compile(r"^\s*\[\[?\s*([^\]]+?)\s*\]\]?\s*(#.*)?$")


def estado_toml(caminho: Path, url: str, token: str) -> tuple[str, dict | None]:
    if not caminho.exists():
        return "ausente", None
    dados = tomllib.loads(caminho.read_text(encoding="utf-8"))
    entrada = dados.get("mcp_servers", {}).get(NOME)
    if not isinstance(entrada, dict):
        return "ausente", entrada
    ok = (entrada.get("url") == url
          and entrada.get("http_headers", {}).get("Authorization") == f"Bearer {token}")
    return ("correto" if ok else "desatualizado"), entrada


def valor_toml(v) -> str | None:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list) and all(isinstance(i, str) for i in v):
        return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in v) + "]"
    return None


def corrigir_toml(caminho: Path, entrada: dict | None, url: str, token: str) -> Path:
    texto = caminho.read_text(encoding="utf-8") if caminho.exists() else ""
    # Remove a tabela [mcp_servers.drift] e suas subtabelas, preservando o resto.
    alvo = f"mcp_servers.{NOME}"
    saida, pulando = [], False
    for ln in texto.splitlines(keepends=True):
        m = CABECALHO_TOML.match(ln)
        if m:
            nome = m.group(1).replace(" ", "").replace('"', "")
            pulando = nome == alvo or nome.startswith(alvo + ".")
        if not pulando:
            saida.append(ln)
    novo = "".join(saida).rstrip("\n")
    # Mantém outras opções simples que já existiam na entrada (ex.: enabled, timeouts).
    extras = []
    for chave, valor in (entrada or {}).items():
        if chave in ("url", "http_headers", "bearer_token_env_var", "command", "args"):
            continue
        convertido = valor_toml(valor)
        if convertido is not None:
            extras.append(f"{chave} = {convertido}\n")
    cabecalhos = dict((entrada or {}).get("http_headers", {}))
    cabecalhos["Authorization"] = f"Bearer {token}"
    pares = ", ".join(f"{json.dumps(k)} = {json.dumps(v)}" for k, v in cabecalhos.items())
    bloco = (f"\n\n[mcp_servers.{NOME}]\nurl = {json.dumps(url)}\n"
             f"http_headers = {{ {pares} }}\n" + "".join(extras))
    backup = gravar_atomico(caminho, (novo + bloco).lstrip("\n"))
    try:
        novo_estado, _ = estado_toml(caminho, url, token)
    except tomllib.TOMLDecodeError:
        novo_estado = "invalido"
    if novo_estado != "correto":
        if backup:
            shutil.copy2(backup, caminho.resolve())
        raise Falha("gravacao_invalida", f"A gravação de {caminho_curto(caminho)} não ficou "
                    "válida; o arquivo anterior foi restaurado.", [], 4)
    return backup


def tratar_clientes(clientes: list[str], url: str, token: str, corrigir: bool) -> bool:
    tudo_certo = True
    for cliente in clientes:
        caminho = arquivo_cliente(cliente)
        rotulo = {"antigravity": "Antigravity", "claude": "Claude Code", "codex": "Codex"}[cliente]
        try:
            if cliente == "codex":
                estado, dados = estado_toml(caminho, url, token)
            else:
                estado, dados = estado_json(caminho, cliente, url, token)
        except (json.JSONDecodeError, tomllib.TOMLDecodeError) as e:
            linha("erro", f"{rotulo}: {caminho_curto(caminho)} não pôde ser lido ({e}); não alterei.")
            tudo_certo = False
            continue
        if estado == "correto":
            linha("ok", f"{rotulo}: entrada drift já correta em {caminho_curto(caminho)}")
            continue
        if not corrigir:
            descricao = {"ausente": "ausente", "desatualizado": "desatualizada"}[estado]
            linha("aviso", f"{rotulo}: entrada drift {descricao} em {caminho_curto(caminho)}")
            tudo_certo = False
            continue
        try:
            if cliente == "codex":
                backup = corrigir_toml(caminho, dados, url, token)
            else:
                backup = corrigir_json(caminho, cliente, dados, url, token)
        except Falha as f:
            linha("erro", f"{rotulo}: {f.mensagem}")
            tudo_certo = False
            continue
        acao = "criada" if estado == "ausente" else "atualizada"
        extra = f"; backup: {caminho_curto(backup)}" if backup else ""
        linha("alterado", f"{rotulo}: entrada drift {acao} em {caminho_curto(caminho)}{extra}. "
                          "Reinicie o agente ou abra uma nova conversa para carregar as ferramentas.")
    return tudo_certo


# --------------------------------------------------------------------------
# Subcomandos
# --------------------------------------------------------------------------

def cmd_diagnostico(args, corrigir: bool) -> int:
    try:
        token = ler_token()
    except Falha as f:
        return relatar_falha(f)
    falha_servidor = None
    try:
        testar_conexao(args.url, token)
    except Falha as f:
        falha_servidor = f
        linha("erro", f.mensagem)
    if falha_servidor and corrigir:
        # Sem uma conexão confirmada, não há como saber se token e endereço estão certos.
        linha("info", "Não alterei as configurações dos agentes porque a conexão não foi confirmada.")
        return relatar_falha(falha_servidor, ja_exibida=True)
    configs_ok = tratar_clientes(args.clientes, args.url, token, corrigir)
    if falha_servidor:
        return relatar_falha(falha_servidor, ja_exibida=True)
    if not configs_ok:
        print("RESULTADO: pendente" if not corrigir else "RESULTADO: falha=configuracao")
        return 0 if not corrigir else 4
    print("RESULTADO: pronto")
    return 0


def relatar_falha(f: Falha, ja_exibida: bool = False) -> int:
    if not ja_exibida:
        linha("erro", f.mensagem)
    acoes = [a for a in f.acoes if a]
    if acoes:
        print("O QUE FAZER:")
        for i, a in enumerate(acoes, 1):
            print(f"  {i}. {a}")
    print(f"RESULTADO: falha={f.codigo}")
    return f.saida


def cmd_chamar(args) -> int:
    try:
        argumentos = json.loads(args.argumentos) if args.argumentos else {}
    except json.JSONDecodeError as e:
        print(f"Argumentos JSON inválidos: {e}", file=sys.stderr)
        return 1
    try:
        token = ler_token() if args.verboso else ler_token_silencioso()
        cliente = ClienteMCP(args.url, token, timeout=args.timeout)
        cliente.iniciar()
        res = cliente.requisitar("tools/call", {"name": args.ferramenta, "arguments": argumentos})
    except Falha as f:
        return relatar_falha(f)
    pasta = Path(tempfile.gettempdir()) / "drift-mcp"
    for i, item in enumerate(res.get("content", []), 1):
        tipo = item.get("type")
        if tipo == "text":
            print(item.get("text", ""))
        elif tipo == "image":
            pasta.mkdir(exist_ok=True)
            ext = (item.get("mimeType", "image/png").split("/")[-1] or "png").replace("jpeg", "jpg")
            destino = pasta / f"{time.strftime('%Y%m%d-%H%M%S')}-{args.ferramenta}-{i}.{ext}"
            destino.write_bytes(base64.b64decode(item.get("data", "")))
            print(f"[imagem salva] {destino}")
        else:
            print(json.dumps(item, ensure_ascii=False))
    if "structuredContent" in res and not res.get("content"):
        print(json.dumps(res["structuredContent"], ensure_ascii=False))
    return 1 if res.get("isError") else 0


def ler_token_silencioso() -> str:
    from contextlib import redirect_stdout
    import io
    with redirect_stdout(io.StringIO()):
        return ler_token()


def main() -> int:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # saída cortada por `head` não gera erro
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=os.environ.get("DRIFT_MCP_URL", URL_PADRAO),
                    help=f"endereço MCP do Drift (padrão: DRIFT_MCP_URL ou {URL_PADRAO})")
    sub = ap.add_subparsers(dest="comando", required=True)
    for nome, ajuda in (("verificar", "diagnostica sem alterar arquivos"),
                        ("configurar", "diagnostica e corrige as configurações dos agentes")):
        p = sub.add_parser(nome, help=ajuda)
        p.add_argument("--clientes", default=",".join(CLIENTES),
                       help="lista separada por vírgulas: " + ",".join(CLIENTES))
    p = sub.add_parser("chamar", help="chama uma ferramenta do Drift diretamente")
    p.add_argument("ferramenta")
    p.add_argument("argumentos", nargs="?", default="", help="objeto JSON com os argumentos")
    p.add_argument("--timeout", type=float, default=180)
    p.add_argument("--verboso", action="store_true")
    args = ap.parse_args()
    if args.comando == "chamar":
        return cmd_chamar(args)
    args.clientes = [c.strip() for c in args.clientes.split(",") if c.strip()]
    invalidos = [c for c in args.clientes if c not in CLIENTES]
    if invalidos:
        ap.error("cliente desconhecido: " + ", ".join(invalidos))
    return cmd_diagnostico(args, corrigir=args.comando == "configurar")


if __name__ == "__main__":
    sys.exit(main())

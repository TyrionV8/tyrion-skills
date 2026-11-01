#!/usr/bin/env python3
"""Cliente MCP/SSE do Master VTT, usando somente a biblioteca padrão Python."""

import argparse
import http.client
import json
import math
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class MasterError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise MasterError("O servidor redirecionou a conexão; informe seu endereço final em --url.")


def dump(value, stream=sys.stdout):
    print(json.dumps(value, ensure_ascii=False, indent=2), file=stream)


def base_url(value):
    parts = urlsplit(value)
    if (parts.scheme not in {"http", "https"} or not parts.hostname
            or parts.username or parts.password or parts.query or parts.fragment
            or parts.path not in {"", "/"}):
        raise argparse.ArgumentTypeError("Use um endereço base como http://127.0.0.1:3000, sem caminho ou credenciais.")
    try:
        parts.port
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return value.rstrip("/")


def positive_timeout(value):
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("O prazo deve ser um número positivo de segundos.") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("O prazo deve ser finito e positivo.")
    return seconds


def origin(url):
    parts = urlsplit(url)
    return parts.scheme, parts.hostname, parts.port or (443 if parts.scheme == "https" else 80)


class MasterClient:
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.opener = build_opener(NoRedirect())
        self.stream = None
        self.endpoint = None
        self.sequence = 0
        self.call_sent = False

    def request(self, url, payload=None):
        headers = {"Accept": "application/json"}
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        with self.opener.open(Request(url, data=body, headers=headers), timeout=self.timeout) as response:
            raw = response.read()
        # O POST confirma o recebimento com texto; o resultado MCP chega pelo SSE.
        return json.loads(raw) if payload is None and raw else None

    def event(self, deadline):
        event_type, data = "message", []
        while time.monotonic() < deadline:
            # O socket também tem um prazo; comentários SSE não renovam o prazo lógico.
            raw = self.stream.readline()
            if not raw:
                raise MasterError("O servidor encerrou o canal SSE antes da resposta.")
            line = raw.decode("utf-8").rstrip("\r\n")
            if not line:
                if data:
                    return event_type, "\n".join(data)
                event_type = "message"
                continue
            field, separator, value = line.partition(":")
            if not separator:
                continue
            if value.startswith(" "):
                value = value[1:]
            if field == "event":
                event_type = value
            elif field == "data":
                data.append(value)
        raise MasterError("Prazo de espera da resposta SSE excedido.")

    def rpc(self, method, params=None):
        self.sequence += 1
        request_id = self.sequence
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        if method == "tools/call":
            # Marcar antes do envio: até uma conexão rompida pode ter gravado a ação.
            self.call_sent = True
        self.request(self.endpoint, message)
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            kind, data = self.event(deadline)
            if kind != "message":
                continue
            response = json.loads(data)
            if response.get("id") != request_id:
                continue
            if "error" in response:
                raise MasterError("Erro do protocolo MCP: " + json.dumps(response["error"], ensure_ascii=False))
            if "result" not in response:
                raise MasterError("Resposta MCP sem resultado.")
            return response["result"]
        raise MasterError("Prazo da chamada MCP excedido.")

    def connect(self):
        request = Request(self.url + "/mcp/sse", headers={"Accept": "text/event-stream"})
        self.stream = self.opener.open(request, timeout=self.timeout)
        if self.stream.headers.get_content_type() != "text/event-stream":
            raise MasterError("O endereço não retornou um canal SSE do Master.")
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            kind, data = self.event(deadline)
            if kind == "endpoint":
                endpoint = urljoin(self.url + "/mcp/sse", data)
                parts = urlsplit(endpoint)
                if origin(endpoint) != origin(self.url) or parts.username or parts.password or parts.fragment:
                    raise MasterError("O canal SSE indicou um endereço de envio fora do servidor informado.")
                self.endpoint = endpoint
                break
        if not self.endpoint:
            raise MasterError("O canal SSE não informou o endereço da sessão.")
        self.rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "master-ai-assist", "version": "1.0.0"},
        })
        self.request(self.endpoint, {"jsonrpc": "2.0", "method": "notifications/initialized"})

    def tools(self):
        tools, cursor, seen = [], None, set()
        while True:
            result = self.rpc("tools/list", {"cursor": cursor} if cursor else {})
            tools.extend(result.get("tools", []))
            cursor = result.get("nextCursor")
            if not cursor:
                return tools
            if cursor in seen:
                raise MasterError("O servidor repetiu o cursor de paginação das ferramentas.")
            seen.add(cursor)

    def close(self):
        if self.stream is not None:
            self.stream.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", type=base_url, default=os.environ.get("MASTER_VTT_URL", "http://127.0.0.1:3000"), help="Endereço base do servidor (ou MASTER_VTT_URL).")
    parser.add_argument("--timeout", type=positive_timeout, default=20.0, help="Prazo por operação, em segundos (padrão 20).")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Consulta saúde e metadados, sem alterar a campanha.")
    tool_parser = commands.add_parser("tools", help="Consulta os esquemas atuais das ferramentas MCP.")
    tool_parser.add_argument("name", nargs="?", help="Nome opcional para filtrar uma ferramenta.")
    call_parser = commands.add_parser("call", help="Executa uma ferramenta; alterações exigem um pedido do usuário.")
    call_parser.add_argument("name")
    arguments = call_parser.add_mutually_exclusive_group()
    arguments.add_argument("--args", default=None, help="Objeto JSON com os argumentos (padrão {}).")
    arguments.add_argument("--args-file", help="Arquivo de argumentos JSON, ou - para entrada padrão.")
    args = parser.parse_args()

    tool_args = {}
    if args.command == "call":
        try:
            raw = args.args if args.args is not None else "{}"
            if args.args_file:
                raw = sys.stdin.read() if args.args_file == "-" else Path(args.args_file).read_text(encoding="utf-8")
            tool_args = json.loads(raw)
            if not isinstance(tool_args, dict):
                parser.error("Os argumentos da ferramenta devem ser um objeto JSON.")
        except (OSError, UnicodeError, ValueError) as exc:
            parser.error("Não foi possível ler os argumentos: " + str(exc))

    client = MasterClient(args.url, args.timeout)
    try:
        if args.command == "status":
            health = client.request(args.url + "/api/health")
            info = client.request(args.url + "/mcp/info")
            if not isinstance(health, dict) or health.get("status") != "ok" or health.get("vtt") != "Master":
                raise MasterError("A rota de saúde não identificou um Master ativo.")
            if not isinstance(info, dict) or info.get("name") != "master-vtt":
                raise MasterError("Os metadados não identificaram o Master VTT.")
            dump({"url": args.url, "health": health, "mcp": info})
            return 0
        client.connect()
        if args.command == "tools":
            tools = client.tools()
            if args.name:
                selected = next((tool for tool in tools if tool.get("name") == args.name), None)
                if selected is None:
                    raise MasterError("Ferramenta não encontrada: " + args.name)
                dump(selected)
            else:
                dump({"tools": tools})
            return 0
        result = client.rpc("tools/call", {"name": args.name, "arguments": tool_args})
        failed = result.get("isError") or result.get("structuredContent", {}).get("success") is False
        dump(result, sys.stderr if failed else sys.stdout)
        return 1 if failed else 0
    except (MasterError, OSError, ValueError, http.client.HTTPException) as exc:
        detail = f"HTTP {exc.code}: {exc.reason}" if isinstance(exc, HTTPError) else str(exc)
        dump({"success": False, "error": detail, "call_sent": client.call_sent,
              "suggestion": "Consulte o estado antes de repetir uma alteração cuja resposta se perdeu." if client.call_sent else "Verifique o endereço, se o Master está ativo e a permissão de rede do terminal."}, sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())

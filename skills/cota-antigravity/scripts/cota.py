#!/usr/bin/env python3
"""Consulta cotas do Antigravity e gerencia alarmes para o hook PreInvocation."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any
import uuid


GROUP_ALIASES: dict[str, str] = {
    "gemini": "gemini",
    "gemini-models": "gemini",
    "claude_gpt": "claude_gpt",
    "claude-gpt": "claude_gpt",
    "claude": "claude_gpt",
    "gpt": "claude_gpt",
    "3p": "claude_gpt",
    "opus": "claude_gpt",
    "sonnet": "claude_gpt",
    "argon": "argon",
    "gemini-4-argon": "argon",
    "todos": "todos",
    "all": "todos",
}

WINDOW_ALIASES: dict[str, str] = {
    "5h": "5h",
    "weekly": "weekly",
    "semanal": "weekly",
    "menor": "menor",
    "min": "menor",
}

GROUP_LABELS: dict[str, str] = {
    "gemini": "Gemini Models",
    "claude_gpt": "Claude and GPT models",
    "argon": "Gemini 4 Argon",
}


def get_cache_dir() -> Path:
    override = os.environ.get("COTA_ANTIGRAVITY_CACHE_DIR")
    if override:
        path = Path(override).expanduser()
    else:
        xdg = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")).expanduser()
        path = xdg / "cota-antigravity"
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_agy_bin() -> str:
    candidates = [
        os.environ.get("COTA_ANTIGRAVITY_AGY_BIN"),
        os.environ.get("AGY_BIN"),
        shutil.which("agy"),
        str(Path.home() / ".gemini/bin/agy"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise FileNotFoundError(
        "Executavel 'agy' nao encontrado no PATH nem em ~/.gemini/bin/agy."
    )


@contextmanager
def file_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def parse_iso_utc(raw: str | None) -> datetime | None:
    if not raw:
        return None
    normalized = raw.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_local_iso(dt_utc: datetime | None) -> str | None:
    if dt_utc is None:
        return None
    return dt_utc.astimezone().isoformat(timespec="seconds")


def classify_group(group_name: str, buckets: list[dict[str, Any]]) -> str:
    lowered = group_name.lower()
    if "argon" in lowered or any("argon" in str(b.get("id", "")).lower() for b in buckets):
        return "argon"
    if "claude" in lowered or "gpt" in lowered or any(
        str(b.get("id", "")).lower().startswith("3p-") for b in buckets
    ):
        return "claude_gpt"
    if "gemini" in lowered or any(
        str(b.get("id", "")).lower().startswith("gemini-") for b in buckets
    ):
        return "gemini"
    return lowered.replace(" ", "_")


def run_agy_command(slash_cmd: str, timeout_s: int = 20) -> dict[str, Any]:
    agy_bin = resolve_agy_bin()
    proc = subprocess.run(
        [agy_bin, "-p", slash_cmd, "--output-format", "json", "--print-timeout", "15s"],
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Falha ao executar {agy_bin} -p {slash_cmd}: {detail}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Saida JSON invalida de {agy_bin} -p {slash_cmd}: {exc}") from exc


def normalize_usage(raw_payload: dict[str, Any], fetched_at: float | None = None) -> dict[str, Any]:
    now_ts = fetched_at if fetched_at is not None else time.time()
    now_utc = datetime.fromtimestamp(now_ts, tz=timezone.utc)
    data = raw_payload.get("command", {}).get("data", {})
    groups_out: list[dict[str, Any]] = []
    flat_buckets: list[dict[str, Any]] = []

    for group in data.get("groups", []):
        raw_buckets = group.get("buckets", [])
        group_key = classify_group(str(group.get("name", "")), raw_buckets)
        buckets_out: list[dict[str, Any]] = []
        for bucket in raw_buckets:
            frac = float(bucket.get("remaining_fraction", 0.0))
            reset_utc_str = bucket.get("reset_time")
            reset_dt = parse_iso_utc(reset_utc_str)
            secs_left = max(0, int((reset_dt - now_utc).total_seconds())) if reset_dt else None
            entry = {
                "id": bucket.get("id"),
                "name": bucket.get("name"),
                "group_key": group_key,
                "group_name": group.get("name"),
                "window": bucket.get("window"),
                "remaining_fraction": frac,
                "remaining_percent": round(frac * 100.0, 2),
                "reset_time_utc": reset_utc_str,
                "reset_time_local": format_local_iso(reset_dt),
                "seconds_until_reset": secs_left,
                "seconds_until_reset_plus_120": (secs_left + 120) if secs_left is not None else None,
            }
            buckets_out.append(entry)
            flat_buckets.append(entry)
        groups_out.append(
            {
                "group_key": group_key,
                "name": group.get("name"),
                "description": group.get("description"),
                "buckets": buckets_out,
            }
        )

    return {
        "fetched_at": now_ts,
        "fetched_at_local": format_local_iso(now_utc),
        "description": data.get("description"),
        "groups": groups_out,
        "buckets": flat_buckets,
    }


def recompute_timings(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Atualiza segundos restantes em relacao ao relogio atual ao ler do cache."""
    now_utc = datetime.now(timezone.utc)
    updated = json.loads(json.dumps(snapshot))
    for bucket in updated.get("buckets", []):
        reset_dt = parse_iso_utc(bucket.get("reset_time_utc"))
        secs_left = max(0, int((reset_dt - now_utc).total_seconds())) if reset_dt else None
        bucket["seconds_until_reset"] = secs_left
        bucket["seconds_until_reset_plus_120"] = (secs_left + 120) if secs_left is not None else None
    for group in updated.get("groups", []):
        for bucket in group.get("buckets", []):
            reset_dt = parse_iso_utc(bucket.get("reset_time_utc"))
            secs_left = max(0, int((reset_dt - now_utc).total_seconds())) if reset_dt else None
            bucket["seconds_until_reset"] = secs_left
            bucket["seconds_until_reset_plus_120"] = (secs_left + 120) if secs_left is not None else None
    return updated


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(f"{path.suffix}.{os.getpid()}.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def read_json_safe(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def fetch_and_cache_usage() -> dict[str, Any]:
    cache_dir = get_cache_dir()
    cache_path = cache_dir / "usage_cache.json"
    raw = run_agy_command("/usage")
    snapshot = normalize_usage(raw)
    write_json_atomic(cache_path, snapshot)
    return snapshot


def cache_is_valid(cached: dict[str, Any] | None, max_age_seconds: int, now_ts: float) -> bool:
    if not cached:
        return False
    if (now_ts - float(cached.get("fetched_at", 0))) >= max_age_seconds:
        return False
    now_utc = datetime.fromtimestamp(now_ts, tz=timezone.utc)
    for bucket in cached.get("buckets", []):
        reset_dt = parse_iso_utc(bucket.get("reset_time_utc"))
        if reset_dt is not None and now_utc >= reset_dt:
            return False
    return True


def get_usage_with_cache(max_age_seconds: int) -> dict[str, Any]:
    cache_dir = get_cache_dir()
    cache_path = cache_dir / "usage_cache.json"
    lock_path = cache_dir / "usage_cache.lock"
    now = time.time()

    cached = read_json_safe(cache_path, None)
    if cache_is_valid(cached, max_age_seconds, now):
        return recompute_timings(cached)

    with file_lock(lock_path):
        cached = read_json_safe(cache_path, None)
        now = time.time()
        if cache_is_valid(cached, max_age_seconds, now):
            return recompute_timings(cached)
        return fetch_and_cache_usage()


def fetch_credits() -> dict[str, Any]:
    raw = run_agy_command("/credits")
    data = raw.get("command", {}).get("data", {})
    return {
        "remaining_credits": data.get("remaining_credits"),
        "upgrade_uri": data.get("upgrade_uri"),
    }


def filter_buckets(snapshot: dict[str, Any], group_key: str, window: str) -> list[dict[str, Any]]:
    buckets = [
        b
        for b in snapshot.get("buckets", [])
        if group_key == "todos" or b.get("group_key") == group_key
    ]
    if window == "menor":
        return [min(buckets, key=lambda b: float(b["remaining_percent"]))] if buckets else []
    return [b for b in buckets if b.get("window") == window]


def cmd_consultar(args: argparse.Namespace) -> int:
    if args.com_creditos:
        with ThreadPoolExecutor(max_workers=2) as pool:
            usage_fut = pool.submit(fetch_and_cache_usage)
            credits_fut = pool.submit(fetch_credits)
            usage = usage_fut.result()
            credits = credits_fut.result()
    else:
        usage = fetch_and_cache_usage()
        credits = None

    if args.grupo:
        group_key = normalize_group_arg(args.grupo)
        usage = {
            **usage,
            "groups": [g for g in usage["groups"] if group_key == "todos" or g["group_key"] == group_key],
            "buckets": [b for b in usage["buckets"] if group_key == "todos" or b["group_key"] == group_key],
        }

    result = dict(usage)
    if credits is not None:
        result["credits"] = credits

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"Consulta atualizada em: {result['fetched_at_local']}")
    for group in result["groups"]:
        print(f"\n[{group['group_key']}] {group['name']} ({group.get('description') or ''})")
        for bucket in group["buckets"]:
            print(
                f"  - {bucket['window']}: {bucket['remaining_percent']:.2f}% restante | "
                f"renova em {bucket['reset_time_local']} "
                f"(faltam {bucket['seconds_until_reset']}s; +2min = {bucket['seconds_until_reset_plus_120']}s)"
            )
    if credits is not None:
        print(f"\n[credits] Restantes: {credits.get('remaining_credits')}")
    return 0


def normalize_group_arg(raw: str) -> str:
    key = GROUP_ALIASES.get(raw.strip().lower())
    if not key:
        valid = ", ".join(sorted({"gemini", "claude_gpt", "argon", "todos"}))
        raise ValueError(f"Grupo invalido '{raw}'. Use: {valid}.")
    return key


def normalize_window_arg(raw: str) -> str:
    key = WINDOW_ALIASES.get(raw.strip().lower())
    if not key:
        raise ValueError(f"Janela invalida '{raw}'. Use: 5h, weekly ou menor.")
    return key


def load_alarms_unlocked(alarms_path: Path) -> list[dict[str, Any]]:
    data = read_json_safe(alarms_path, {"alarms": []})
    return list(data.get("alarms", [])) if isinstance(data, dict) else []


def save_alarms_unlocked(alarms_path: Path, alarms: list[dict[str, Any]]) -> None:
    write_json_atomic(alarms_path, {"alarms": alarms})


def cmd_alarme_definir(args: argparse.Namespace) -> int:
    group_key = normalize_group_arg(args.grupo)
    window = normalize_window_arg(args.janela)
    if not (0.0 <= args.abaixo_de <= 100.0):
        raise ValueError("--abaixo-de deve estar entre 0 e 100.")
    if args.cache_segundos < 5:
        raise ValueError("--cache-segundos deve ser >= 5.")

    if args.escopo == "conversa" and not args.conversation_id:
        raise ValueError("Escopo 'conversa' exige --conversation-id.")
    if args.escopo == "workspace" and not args.workspace:
        raise ValueError("Escopo 'workspace' exige --workspace.")

    if group_key == "argon" and window == "5h":
        raise ValueError(
            "O grupo 'argon' possui apenas janela 'weekly' (semanal). Use --janela weekly ou --janela menor."
        )

    alarm_id = args.id or f"alm-{uuid.uuid4().hex[:8]}"
    workspace_resolved = str(Path(args.workspace).expanduser().resolve()) if args.workspace else None
    alarm = {
        "id": alarm_id,
        "enabled": True,
        "escopo": args.escopo,
        "conversation_id": args.conversation_id,
        "workspace": workspace_resolved,
        "grupo": group_key,
        "janela": window,
        "abaixo_de": float(args.abaixo_de),
        "cache_segundos": int(args.cache_segundos),
        "acao": args.acao,
        "notificar": bool(args.notificar),
        "uma_vez": not args.repetir,
        "nota": args.nota or "",
        "created_at": format_local_iso(datetime.now(timezone.utc)),
        "last_triggered_reset": None,
        "last_triggered_at": None,
    }

    cache_dir = get_cache_dir()
    alarms_path = cache_dir / "alarms.json"
    with file_lock(cache_dir / "alarms.lock"):
        alarms = [a for a in load_alarms_unlocked(alarms_path) if a.get("id") != alarm_id]
        alarms.append(alarm)
        save_alarms_unlocked(alarms_path, alarms)

    if args.json:
        print(json.dumps(alarm, ensure_ascii=False, indent=2))
    else:
        alvo = (
            f"conversa={alarm['conversation_id']}"
            if alarm["escopo"] == "conversa"
            else (f"workspace={alarm['workspace']}" if alarm["escopo"] == "workspace" else "global")
        )
        print(
            f"Alarme '{alarm_id}' armado ({alvo}): grupo={group_key}, janela={window}, "
            f"dispara <= {alarm['abaixo_de']}%, acao={alarm['acao']}, "
            f"cache={alarm['cache_segundos']}s, uma_vez={alarm['uma_vez']}."
        )
    return 0


def cmd_alarme_listar(args: argparse.Namespace) -> int:
    cache_dir = get_cache_dir()
    alarms_path = cache_dir / "alarms.json"
    with file_lock(cache_dir / "alarms.lock"):
        alarms = load_alarms_unlocked(alarms_path)
    if args.conversation_id:
        alarms = [
            a
            for a in alarms
            if a.get("escopo") == "global" or a.get("conversation_id") == args.conversation_id
        ]
    if args.json:
        print(json.dumps({"alarms": alarms}, ensure_ascii=False, indent=2))
        return 0
    if not alarms:
        print("Nenhum alarme configurado.")
        return 0
    for a in alarms:
        print(
            f"- {a['id']} | escopo={a['escopo']} | grupo={a['grupo']} | janela={a['janela']} | "
            f"<= {a['abaixo_de']}% | acao={a['acao']} | ultimo_disparo={a.get('last_triggered_at') or 'nunca'}"
        )
    return 0


def cmd_alarme_limpar(args: argparse.Namespace) -> int:
    cache_dir = get_cache_dir()
    alarms_path = cache_dir / "alarms.json"
    with file_lock(cache_dir / "alarms.lock"):
        alarms = load_alarms_unlocked(alarms_path)
        if args.todos:
            kept: list[dict[str, Any]] = []
        elif args.id:
            kept = [a for a in alarms if a.get("id") != args.id]
        elif args.conversation_id:
            kept = [a for a in alarms if a.get("conversation_id") != args.conversation_id]
        else:
            raise ValueError("Informe --id, --conversation-id ou --todos para limpar alarmes.")
        removed = len(alarms) - len(kept)
        save_alarms_unlocked(alarms_path, kept)

    if args.json:
        print(json.dumps({"removed": removed, "remaining": len(kept)}, ensure_ascii=False))
    else:
        print(f"Alarmes removidos: {removed}. Restantes: {len(kept)}.")
    return 0


def workspace_matches(alarm_ws: str | None, payload: dict[str, Any]) -> bool:
    if not alarm_ws:
        return False
    alarm_path = Path(alarm_ws).resolve()
    candidates: list[str] = []
    if payload.get("cwd"):
        candidates.append(str(payload["cwd"]))
    for ws in payload.get("workspacePaths") or []:
        candidates.append(str(ws))
    for cand in candidates:
        try:
            cand_path = Path(cand).resolve()
        except OSError:
            continue
        if cand_path == alarm_path or alarm_path in cand_path.parents:
            return True
    return False


def alarm_matches_payload(alarm: dict[str, Any], payload: dict[str, Any]) -> bool:
    if not alarm.get("enabled", True):
        return False
    escopo = alarm.get("escopo")
    if escopo == "global":
        return True
    if escopo == "conversa":
        return bool(alarm.get("conversation_id")) and alarm.get("conversation_id") == payload.get("conversationId")
    if escopo == "workspace":
        return workspace_matches(alarm.get("workspace"), payload)
    return False


def maybe_notify_desktop(title: str, body: str) -> None:
    notify_bin = shutil.which("notify-send")
    if not notify_bin:
        return
    try:
        subprocess.run(
            [notify_bin, "-u", "critical", title, body],
            capture_output=True,
            timeout=2,
            check=False,
        )
    except OSError:
        pass


def log_hook_error(message: str) -> None:
    try:
        log_path = get_cache_dir() / "hook.log"
        stamp = format_local_iso(datetime.now(timezone.utc))
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{stamp}] {message}\n")
    except OSError:
        pass


def needs_refresh_for_alarm(alarm: dict[str, Any]) -> bool:
    if not alarm.get("uma_vez", True):
        return True
    last_reset = parse_iso_utc(alarm.get("last_triggered_reset"))
    if last_reset is None:
        return True
    return datetime.now(timezone.utc) >= last_reset


def cmd_hook(_args: argparse.Namespace) -> int:
    raw_stdin = sys.stdin.read().strip()
    if not raw_stdin:
        print("{}")
        return 0
    try:
        payload = json.loads(raw_stdin)
    except json.JSONDecodeError:
        print("{}")
        return 0

    cache_dir = get_cache_dir()
    alarms_path = cache_dir / "alarms.json"
    with file_lock(cache_dir / "alarms.lock"):
        all_alarms = load_alarms_unlocked(alarms_path)

    matching = [a for a in all_alarms if alarm_matches_payload(a, payload)]
    active = [a for a in matching if needs_refresh_for_alarm(a)]
    if not active:
        print("{}")
        return 0

    min_cache = min(int(a.get("cache_segundos", 120)) for a in active)
    try:
        snapshot = get_usage_with_cache(min_cache)
    except Exception as exc:  # Fail-open para nunca travar uma sessao por falha transitoria
        log_hook_error(f"Falha ao consultar cota no hook: {exc}")
        print("{}")
        return 0

    triggered_lines: list[str] = []
    markdown_lines: list[str] = []
    should_terminate = False
    should_notify = False
    triggered_ids: dict[str, str] = {}

    for alarm in active:
        buckets = filter_buckets(snapshot, alarm["grupo"], alarm["janela"])
        if not buckets:
            continue
        hit_buckets = [b for b in buckets if float(b["remaining_percent"]) <= float(alarm["abaixo_de"])]
        if not hit_buckets:
            continue
        chosen = min(hit_buckets, key=lambda b: float(b["remaining_percent"]))
        reset_key = str(chosen.get("reset_time_utc") or "")
        if alarm.get("uma_vez", True) and alarm.get("last_triggered_reset") == reset_key and reset_key:
            continue

        triggered_ids[str(alarm["id"])] = reset_key
        if alarm.get("acao") == "bloquear":
            should_terminate = True
        if alarm.get("notificar"):
            should_notify = True

        nota_txt = f" | Nota: {alarm['nota']}" if alarm.get("nota") else ""
        msg = (
            f"Alarme '{alarm['id']}': {chosen['group_name']} ({chosen['window']}) "
            f"em {chosen['remaining_percent']:.2f}% (limite <= {alarm['abaixo_de']}%). "
            f"Renovacao local: {chosen['reset_time_local']} "
            f"(faltam {chosen['seconds_until_reset']}s; +2min = {chosen['seconds_until_reset_plus_120']}s)."
            f"{nota_txt}"
        )
        triggered_lines.append(msg)
        markdown_lines.append(f"- **{chosen['group_name']} ({chosen['window']})**: **{chosen['remaining_percent']:.2f}%** restante (renova `{chosen['reset_time_local']}`)")

    if not triggered_lines:
        print("{}")
        return 0

    now_local = format_local_iso(datetime.now(timezone.utc))
    with file_lock(cache_dir / "alarms.lock"):
        latest_alarms = load_alarms_unlocked(alarms_path)
        for alarm in latest_alarms:
            aid = str(alarm.get("id"))
            if aid in triggered_ids:
                alarm["last_triggered_reset"] = triggered_ids[aid]
                alarm["last_triggered_at"] = now_local
        save_alarms_unlocked(alarms_path, latest_alarms)

    if should_notify:
        maybe_notify_desktop("Alarme de cota Antigravity", "\n".join(triggered_lines))

    system_text = (
        "[ALARME DE COTA ATINGIDO]\n"
        + "\n".join(triggered_lines)
        + "\nAplique a acao solicitada pelo usuario para este limite."
    )
    user_md = "> **Alarme de cota atingido**\n" + "\n".join(markdown_lines)

    inject_steps: list[dict[str, Any]] = [
        {
            "systemMessage": {
                "systemMessage": system_text,
                "metadata": {"user_markdown": user_md},
            }
        }
    ]
    out: dict[str, Any] = {
        "injectSteps": inject_steps,
        "terminationBehavior": "terminate" if should_terminate else "",
    }
    if should_terminate:
        inject_steps.append(
            {
                "errorMessage": {
                    "userMessage": "Execucao interrompida pelo alarme de cota:\n" + "\n".join(triggered_lines)
                }
            }
        )

    print(json.dumps(out, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Consulta cotas do Antigravity e gerencia alarmes para PreInvocation."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cons = sub.add_parser("consultar", help="Consulta a cota atual via agy.")
    p_cons.add_argument("--grupo", help="Filtra grupo: gemini, claude_gpt, argon ou todos.")
    p_cons.add_argument("--com-creditos", action="store_true", help="Inclui saldo de /credits.")
    p_cons.add_argument("--json", action="store_true", help="Saida em JSON.")
    p_cons.set_defaults(func=cmd_consultar)

    p_alm = sub.add_parser("alarme", help="Gerencia alarmes configuraveis.")
    alm_sub = p_alm.add_subparsers(dest="alarme_cmd", required=True)

    p_def = alm_sub.add_parser("definir", help="Cria ou atualiza um alarme.")
    p_def.add_argument("--id", help="Identificador opcional do alarme.")
    p_def.add_argument("--escopo", choices=["conversa", "workspace", "global"], default="conversa")
    p_def.add_argument("--conversation-id", help="ID da conversa (obrigatorio se escopo=conversa).")
    p_def.add_argument("--workspace", help="Pasta raiz do projeto (obrigatorio se escopo=workspace).")
    p_def.add_argument("--grupo", default="gemini", help="gemini, claude_gpt, argon ou todos.")
    p_def.add_argument("--janela", default="5h", help="5h, weekly ou menor.")
    p_def.add_argument("--abaixo-de", type=float, required=True, help="Percentual de disparo (0 a 100).")
    p_def.add_argument("--cache-segundos", type=int, default=120, help="Intervalo de cache do hook em segundos.")
    p_def.add_argument("--acao", choices=["avisar", "bloquear"], default="avisar")
    p_def.add_argument("--notificar", dest="notificar", action="store_true", default=True)
    p_def.add_argument("--sem-notificar", dest="notificar", action="store_false")
    p_def.add_argument("--repetir", action="store_true", help="Dispara a cada verificacao enquanto abaixo do limite.")
    p_def.add_argument("--nota", help="Observacao opcional exibida quando o alarme disparar.")
    p_def.add_argument("--json", action="store_true")
    p_def.set_defaults(func=cmd_alarme_definir)

    p_lst = alm_sub.add_parser("listar", help="Lista alarmes configurados.")
    p_lst.add_argument("--conversation-id", help="Filtra pela conversa + globais.")
    p_lst.add_argument("--json", action="store_true")
    p_lst.set_defaults(func=cmd_alarme_listar)

    p_clr = alm_sub.add_parser("limpar", help="Remove alarmes configurados.")
    p_clr.add_argument("--id", help="Remove apenas este alarme.")
    p_clr.add_argument("--conversation-id", help="Remove alarmes desta conversa.")
    p_clr.add_argument("--todos", action="store_true", help="Remove todos os alarmes.")
    p_clr.add_argument("--json", action="store_true")
    p_clr.set_defaults(func=cmd_alarme_limpar)

    p_hook = sub.add_parser("hook", help="Handler interno para PreInvocation.")
    p_hook.set_defaults(func=cmd_hook)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

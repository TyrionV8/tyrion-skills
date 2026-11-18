"""Alarme local de cota por conversa do Codex."""

import argparse
import fcntl
import json
import os
from pathlib import Path
import stat
import sys
import time
from uuid import UUID


WINDOWS = {"5h": 300, "semanal": 10080}
STATE_DIR = Path("/tmp") / f"cota-codex-{os.getuid()}"


def state_path(session_id, create=False):
    session = UUID(session_id)
    if create:
        STATE_DIR.mkdir(mode=0o700, exist_ok=True)
    metadata = STATE_DIR.lstat()
    if metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) != 0o700:
        raise PermissionError(f"Diretório de estado sem acesso privado: {STATE_DIR}")
    if not stat.S_ISDIR(metadata.st_mode):
        raise PermissionError(f"Diretório de estado inválido: {STATE_DIR}")
    return STATE_DIR / f"{session}.json"


def read_window(transcript_path, window):
    if not transcript_path:
        return None
    # Leia apenas o final do registro. Descarte a primeira linha se o corte for parcial.
    with open(transcript_path, "rb") as transcript:
        end = transcript.seek(0, os.SEEK_END)
        offset = max(0, end - 2 * 1024 * 1024)
        if offset:
            transcript.seek(offset - 1)
            if transcript.read(1) != b"\n":
                transcript.readline()
        else:
            transcript.seek(0)
        lines = transcript.read().splitlines()

    for line in reversed(lines):
        if b'"token_count"' not in line or b'"rate_limits"' not in line:
            continue
        try:
            record = json.loads(line)
        except (ValueError, UnicodeError):
            continue
        if not isinstance(record, dict) or record.get("type") != "event_msg":
            continue
        event = record.get("payload") or {}
        limits = event.get("rate_limits") or {}
        if event.get("type") != "token_count" or limits.get("limit_id") != "codex":
            continue
        return next(
            (
                entry
                for entry in (limits.get("primary"), limits.get("secondary"))
                if entry and entry.get("window_minutes") == WINDOWS[window]
            ),
            None,
        )
    return None


def write_state(state_file, alarm):
    state_file.seek(0)
    state_file.truncate()
    if alarm:
        json.dump(alarm, state_file)
    state_file.flush()


def on_tool_result():
    hook = json.load(sys.stdin)
    path = state_path(hook["session_id"])
    with path.open("r+", encoding="utf-8") as state_file:
        fcntl.flock(state_file, fcntl.LOCK_EX)
        raw_state = state_file.read()
        if not raw_state:
            return
        alarm = json.loads(raw_state)
        window = read_window(hook.get("transcript_path"), alarm["janela"])
        if window is None:
            return
        used_percent = window.get("used_percent")
        renewal = window.get("resets_at")
        if not isinstance(used_percent, (int, float)) or not 0 <= used_percent <= 100:
            return
        if not isinstance(renewal, int) or renewal <= time.time():
            return
        remaining = round(100 - used_percent, 10)
        if remaining > alarm["limite"]:
            return
        write_state(state_file, None)

    message = (
        f"[ALARME DE COTA DO CODEX] Janela {alarm['janela']}: "
        f"{remaining:g}% restantes (limite: {alarm['limite']:g}%). "
        "Confirme a cota atual e siga o pedido do usuário."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        },
    }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    arm = actions.add_parser("armar")
    arm.add_argument("janela", choices=WINDOWS)
    arm.add_argument("percentual", type=float)
    actions.add_parser("desarmar")
    actions.add_parser("hook")
    args = parser.parse_args()
    if args.action == "hook":
        try:
            on_tool_result()
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            return
        return

    alarm = None
    if args.action == "armar":
        if not 0 <= args.percentual <= 100:
            parser.error("Informe um percentual de 0 a 100.")
        alarm = {"janela": args.janela, "limite": args.percentual}
    session = os.environ.get("CODEX_THREAD_ID")
    if not session:
        parser.error("A conversa atual precisa fornecer CODEX_THREAD_ID.")
    path = state_path(session, create=True)
    with path.open("a+", encoding="utf-8") as state_file:
        fcntl.flock(state_file, fcntl.LOCK_EX)
        write_state(state_file, alarm)


if __name__ == "__main__":
    main()

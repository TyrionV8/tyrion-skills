#!/usr/bin/env python3
"""
Script auxiliar da skill `analisar-relevancia-da-transcricao`.
Permite ler a transcrição do DriftScript agrupada por parágrafos com índices [start..end]
e aplicar anotações de relevância (verde -> amarelo -> vermelho e azul para off_topic) via JSON.
"""

import json
import sys
import urllib.request

DRIFTSCRIPT_URL = "http://127.0.0.1:4732"


def ler_transcricao() -> None:
    req = urllib.request.urlopen(f"{DRIFTSCRIPT_URL}/api/transcript", timeout=30.0)
    data = json.loads(req.read().decode("utf-8"))
    words = data.get("words", [])
    segments = data.get("segments", [])
    print(f"Arquivo: {data.get('file_path')}")
    print(f"Total de tokens: {len(words)} | Duração original: {data.get('source_duration')}s\n")
    for seg in segments:
        w_idxs = seg.get("word_indices", [])
        if not w_idxs:
            continue
        parts = []
        for idx in w_idxs:
            w = words[idx]
            if w.get("kind") == "pause":
                continue
            if w.get("kind") == "stretch":
                continue
            tok = f"~{w['word']}~" if w.get("deleted") else w["word"]
            parts.append(f"[{idx}]{tok}")
        if parts:
            print(f"Parágrafo #{seg['id']} ({seg['start']:.1f}s - {seg['end']:.1f}s) [{w_idxs[0]}..{w_idxs[-1]}]:")
            print("  " + " ".join(parts))
            print()


def aplicar_relevancia() -> None:
    raw = sys.stdin.read().strip()
    if not raw and len(sys.argv) >= 3:
        raw = sys.argv[2]
    payload = json.loads(raw)
    req = urllib.request.Request(
        f"{DRIFTSCRIPT_URL}/api/words/relevance",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=30.0)
    res = json.loads(resp.read().decode("utf-8"))
    print(
        json.dumps(
            {
                "ok": res.get("ok", True),
                "updated_relevance_count": res.get("updated_relevance_count", 0),
                "total_words": res.get("total_words", 0),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) >= 2 else "ler"
    if cmd == "ler":
        ler_transcricao()
    elif cmd == "aplicar":
        aplicar_relevancia()
    else:
        print("Uso: aplicar_relevancia.py [ler | aplicar]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

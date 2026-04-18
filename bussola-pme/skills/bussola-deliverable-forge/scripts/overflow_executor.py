#!/usr/bin/env python3
"""
Executa ação de overflow em artefato Bússola PME que excede density target.

Input:  --artifact <path>   Arquivo a processar
        --action <str>      summarize | compress | paginate | hard_cut
        --target <int>      Número alvo de caracteres
        --output <path>     Caminho de saída (obrigatório)
Output: Arquivo(s) processado(s) em --output

Ações:
  summarize  → Chama Claude API (claude-sonnet-4-6) para comprimir a ~60%
  compress   → Remove exemplos e justificativas via regex
  paginate   → Divide em _part1, _part2, etc.
  hard_cut   → Trunca com "[...]" no limite

Uso:
  python overflow_executor.py --artifact big_report.md --action summarize \\
    --target 1500 --output resumo_compressed.md
"""

import argparse
import os
import re
import sys
from pathlib import Path


def action_compress(content: str, target: int) -> str:
    # Remove paragraph blocks that look like examples or justifications
    patterns_to_remove = [
        r"(?m)^>\s*.*\n",  # Blockquotes (examples)
        r"(?m)^\*Exemplo.*?\n(?:.*?\n)*?(?=\n)",  # "Exemplo:" blocks
        r"(?m)^\*Justificativa.*?\n",  # Justification lines
        r"(?m)^---+\n.*?\n---+\n",  # Horizontal rule sections
    ]
    result = content
    for pattern in patterns_to_remove:
        result = re.sub(pattern, "", result)
        if len(result) <= target:
            break
    # If still too long, trim trailing content
    if len(result) > target:
        result = result[:target] + "\n\n[...conteúdo comprimido...]"
    return result


def action_paginate(content: str, target: int) -> list[str]:
    pages = []
    remaining = content
    while remaining:
        if len(remaining) <= target:
            pages.append(remaining)
            break
        # Find last newline before target
        cut_point = remaining.rfind("\n", 0, target)
        if cut_point == -1:
            cut_point = target
        pages.append(remaining[:cut_point])
        remaining = remaining[cut_point:].lstrip("\n")
    return pages


def action_hard_cut(content: str, target: int) -> str:
    if len(content) <= target:
        return content
    cut_point = content.rfind("\n", 0, target)
    if cut_point == -1:
        cut_point = target
    return content[:cut_point] + "\n\n[...]"


def action_summarize(content: str, target: int) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Fallback to compress if no API key
        print("WARNING: ANTHROPIC_API_KEY not set, falling back to compress action", file=sys.stderr)
        return action_compress(content, target)

    try:
        import urllib.request
        import urllib.error
        import json

        payload = json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": max(target // 3, 500),
            "messages": [{
                "role": "user",
                "content": (
                    f"Comprima este artefato para aproximadamente {target} caracteres, "
                    f"mantendo estrutura, dados principais e conclusões. "
                    f"Remova redundâncias e exemplos detalhados. "
                    f"Mantenha labels epistêmicos [FATO], [INFERÊNCIA], [HIPÓTESE].\n\n{content}"
                )
            }]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except Exception as e:
        print(f"WARNING: Claude API call failed ({e}), falling back to compress", file=sys.stderr)
        return action_compress(content, target)


def main():
    parser = argparse.ArgumentParser(description="Execute overflow action on a Bússola PME artifact.")
    parser.add_argument("--artifact", required=True, help="Path to artifact file")
    parser.add_argument("--action", required=True,
                        choices=["summarize", "compress", "paginate", "hard_cut"],
                        help="Overflow action to execute")
    parser.add_argument("--target", type=int, required=True, help="Target character count")
    parser.add_argument("--output", required=True, help="Output path")
    args = parser.parse_args()

    content = Path(args.artifact).read_text(encoding="utf-8")

    if args.action == "summarize":
        result = action_summarize(content, args.target)
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"summarize → {len(result)} chars → {args.output}")

    elif args.action == "compress":
        result = action_compress(content, args.target)
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"compress → {len(result)} chars → {args.output}")

    elif args.action == "paginate":
        pages = action_paginate(content, args.target)
        output_path = Path(args.output)
        stem = output_path.stem
        suffix = output_path.suffix
        parent = output_path.parent
        for i, page in enumerate(pages, 1):
            page_path = parent / f"{stem}_part{i}{suffix}"
            page_path.write_text(page, encoding="utf-8")
        print(f"paginate → {len(pages)} parts → {args.output}")

    elif args.action == "hard_cut":
        result = action_hard_cut(content, args.target)
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"hard_cut → {len(result)} chars → {args.output}")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python overflow_executor.py --artifact big.md --action compress --target 1500 --output compressed.md
    main()

#!/usr/bin/env python3
"""
Verifica se artefato de trilha cliente contém strings proibidas de trilha interna.

Input:  --artifact <path>   Arquivo a verificar
        --output <path>     (opcional) Salvar resultado JSON
Output: Lista de leaks encontrados (stdout) ou "CLEAN" se nenhum

Strings proibidas definidas em references/two_track_separation.md.

Uso:
  python derivation_checker.py --artifact cliente/resumo_executivo.md
  # CLEAN
  # ou
  # LEAK: 'diagnostic_working' found at line 12
"""

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_STRINGS = [
    "diagnostic_working",
    "hypotheses_log",
    "raw_hypothesis",
    "internal_reasoning",
    "[TRILHA INTERNA]",
    "trilha interna",
    "module_routing_log",
    "assumptions_log",
    "decision_log",
    "intake_normalized_v2",
    "hypothesis_propagated: true",
]

FORBIDDEN_PATTERNS = [
    r"\[TRILHA INTERNA[^\]]*\]",
    r"diagnostic_working[_\.]",
    r"internal_.*log",
    r"\braw_hypothesis\b",
]


def check(artifact_path: str) -> list[dict]:
    content = Path(artifact_path).read_text(encoding="utf-8")
    lines = content.splitlines()
    leaks = []

    # String matching
    for forbidden in FORBIDDEN_STRINGS:
        for i, line in enumerate(lines, 1):
            if forbidden.lower() in line.lower():
                leaks.append({
                    "type": "string",
                    "forbidden": forbidden,
                    "line": i,
                    "context": line.strip()[:100],
                })

    # Pattern matching
    for pattern in FORBIDDEN_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                # Avoid duplicates
                already = any(l["line"] == i and l.get("pattern") == pattern for l in leaks)
                if not already:
                    leaks.append({
                        "type": "pattern",
                        "pattern": pattern,
                        "line": i,
                        "context": line.strip()[:100],
                    })

    return leaks


def main():
    parser = argparse.ArgumentParser(description="Check for internal track leaks in client artifacts.")
    parser.add_argument("--artifact", required=True, help="Path to artifact to check")
    parser.add_argument("--output", help="Path to save JSON result")
    args = parser.parse_args()

    leaks = check(args.artifact)

    if args.output:
        Path(args.output).write_text(
            json.dumps({"clean": len(leaks) == 0, "leaks": leaks}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    if leaks:
        for leak in leaks:
            if leak["type"] == "string":
                print(f"LEAK: '{leak['forbidden']}' found at line {leak['line']}: {leak['context']}")
            else:
                print(f"LEAK: pattern '{leak['pattern']}' matched at line {leak['line']}: {leak['context']}")
        sys.exit(1)
    else:
        print("CLEAN")
        sys.exit(0)


if __name__ == "__main__":
    # Example: python derivation_checker.py --artifact cliente/resumo_executivo.md
    main()

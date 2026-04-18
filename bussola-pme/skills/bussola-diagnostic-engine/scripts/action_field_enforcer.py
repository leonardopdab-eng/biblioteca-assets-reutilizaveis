#!/usr/bin/env python3
"""
Verifica campos obrigatórios de cada item do plano_acao Bússola PME.

Input:  --plano <path>   Arquivo YAML ou JSON com lista de ações (ou /dev/stdin)
        --depth <str>    "deep" para verificar também campos 5W2H (default: standard)
        --output <path>  (opcional) Salvar resultado como JSON
Output: PASS (exit 0) ou FAIL: item <idx> missing [<fields>] (exit 1)

Campos obrigatórios (todos os modos):
  - owner    (string não-vazia)
  - deadline (string ISO8601-parseable)
  - kpi      (string não-vazia)

Campos adicionais se --depth deep (5W2H):
  - what, why, where, when, who, how, how_much

Uso:
  echo '[{"acao":"Auditar pipeline","owner":"Marina","deadline":"2026-05-15","kpi":"12 reuniões/mês"}]' | \\
    python action_field_enforcer.py --plano /dev/stdin
  # PASS
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml


REQUIRED_FIELDS = ["owner", "deadline", "kpi"]
DEEP_FIELDS = ["what", "why", "where", "when", "who", "how", "how_much"]
ISO8601_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?Z?)?$")


def is_non_empty(value) -> bool:
    return value is not None and str(value).strip() != ""


def is_valid_date(value: str) -> bool:
    if not value:
        return False
    # Accept ISO8601 date or datetime
    if ISO8601_PATTERN.match(str(value)):
        return True
    # Try common formats
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            datetime.strptime(str(value), fmt)
            return True
        except ValueError:
            continue
    return False


def load_plano(path: str) -> list:
    content = Path(path).read_text(encoding="utf-8")

    # Try JSON first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "actions" in data:
            return data["actions"]
    except json.JSONDecodeError:
        pass

    # Try YAML
    try:
        data = yaml.safe_load(content)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "actions" in data:
            return data["actions"]
    except yaml.YAMLError:
        pass

    raise ValueError(f"Cannot parse plano from {path}: not valid JSON or YAML list/dict")


def enforce(plano: list, depth: str = "standard") -> list[dict]:
    check_fields = REQUIRED_FIELDS.copy()
    if depth == "deep":
        check_fields.extend(DEEP_FIELDS)

    failures = []
    for idx, item in enumerate(plano):
        missing = []
        for field in check_fields:
            value = item.get(field)
            if field == "deadline":
                if not is_valid_date(value):
                    missing.append(field)
            elif not is_non_empty(value):
                missing.append(field)

        if missing:
            failures.append({"item_index": idx, "missing_fields": missing, "item": item})

    return failures


def main():
    parser = argparse.ArgumentParser(description="Enforce required fields in Bússola PME action plan.")
    parser.add_argument("--plano", required=True, help="Path to plano_acao YAML/JSON file (or /dev/stdin)")
    parser.add_argument("--depth", default="standard", choices=["standard", "deep"],
                        help="Verification depth (deep adds 5W2H fields)")
    parser.add_argument("--output", help="Path to save JSON result")
    args = parser.parse_args()

    try:
        plano = load_plano(args.plano)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    failures = enforce(plano, args.depth)

    if args.output:
        result = {"status": "PASS" if not failures else "FAIL", "failures": failures}
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    if failures:
        for f in failures:
            print(f"FAIL: item {f['item_index']} missing {f['missing_fields']}")
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)


if __name__ == "__main__":
    # Example: echo '[{"acao":"Task","owner":"Marina","deadline":"2026-05-15","kpi":"goal"}]' | python action_field_enforcer.py --plano /dev/stdin
    main()

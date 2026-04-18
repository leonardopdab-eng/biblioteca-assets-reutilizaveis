#!/usr/bin/env python3
"""
Valida densidade (contagem de caracteres) de um artefato Bússola PME.

Input:  --artifact <path>    Arquivo a validar
        --spec <json>        JSON com {target_chars, max_chars, overflow_action}
          OU
        --artifact-id <id>   ID do artefato (lookup na spec interna)
        --output <path>      (opcional) Salvar resultado JSON
Output: OK, THIN (N chars, min M), ou OVERFLOW (N chars, max M) → action: <overflow_action>

Exit codes:
  0 = OK (dentro do range)
  1 = THIN (abaixo do mínimo)
  2 = OVERFLOW (acima do máximo)

Uso:
  python density_validator.py --artifact resumo.md --spec '{"target_chars":1500,"max_chars":1950,"overflow_action":"hard_cut"}'
"""

import argparse
import json
import sys
from pathlib import Path


# Spec interna para lookup por artifact-id
ARTIFACT_SPECS = {
    "hypotheses_log":           {"target_chars": 3000, "max_chars": 3900, "overflow_action": "summarize", "min_chars": 300},
    "problem_tree":             {"target_chars": 2000, "max_chars": 2600, "overflow_action": "compress_leaves", "min_chars": 200},
    "diagnostic_working":       {"target_chars": 5000, "max_chars": 6500, "overflow_action": "paginate", "min_chars": 500},
    "priority_score":           {"target_chars": 2500, "max_chars": 3250, "overflow_action": "summarize", "min_chars": 250},
    "decision_log":             {"target_chars": 4000, "max_chars": 5200, "overflow_action": "archive_old", "min_chars": 100},
    "information_gaps":         {"target_chars": 1500, "max_chars": 1950, "overflow_action": "summarize", "min_chars": 100},
    "assumptions_log":          {"target_chars": 1500, "max_chars": 1950, "overflow_action": "summarize", "min_chars": 100},
    "module_routing_log":       {"target_chars": 1000, "max_chars": 1300, "overflow_action": "summarize", "min_chars": 50},
    "intake_normalized_v2":     {"target_chars": 2000, "max_chars": 2600, "overflow_action": "compress", "min_chars": 200},
    "resumo_executivo":         {"target_chars": 1500, "max_chars": 1950, "overflow_action": "hard_cut", "min_chars": 300},
    "diagnostico_executivo":    {"target_chars": 4000, "max_chars": 5200, "overflow_action": "compress", "min_chars": 500},
    "matriz_prioridades":       {"target_chars": 2000, "max_chars": 2600, "overflow_action": "compress", "min_chars": 200},
    "plano_acao_cliente":       {"target_chars": 3500, "max_chars": 4550, "overflow_action": "paginate", "min_chars": 300},
    "playbook_operacional":     {"target_chars": 5000, "max_chars": 6500, "overflow_action": "paginate", "min_chars": 500},
    "relatorio_acompanhamento": {"target_chars": 2000, "max_chars": 2600, "overflow_action": "summarize", "min_chars": 200},
    "proposta_continuidade":    {"target_chars": 2500, "max_chars": 3250, "overflow_action": "compress", "min_chars": 300},
    "anonymization_log":        {"target_chars": 1000, "max_chars": 1300, "overflow_action": "none", "min_chars": 50},
    "source_audit_log":         {"target_chars": 1000, "max_chars": 1300, "overflow_action": "none", "min_chars": 50},
    "gate_transition_log":      {"target_chars": 1500, "max_chars": 1950, "overflow_action": "archive_old", "min_chars": 50},
    "hypothesis_propagation_log": {"target_chars": 1000, "max_chars": 1300, "overflow_action": "none", "min_chars": 50},
    "release_notes":            {"target_chars": 800, "max_chars": 1040, "overflow_action": "summarize", "min_chars": 100},
}


def validate(artifact_path: str, spec: dict) -> tuple[str, dict]:
    content = Path(artifact_path).read_text(encoding="utf-8")
    char_count = len(content)

    target = spec.get("target_chars", 1000)
    max_chars = spec.get("max_chars", int(target * 1.3))
    min_chars = spec.get("min_chars", int(target * 0.1))
    overflow_action = spec.get("overflow_action", "summarize")

    result = {
        "char_count": char_count,
        "target_chars": target,
        "max_chars": max_chars,
        "min_chars": min_chars,
        "overflow_action": overflow_action,
    }

    if char_count > max_chars:
        status = f"OVERFLOW ({char_count} chars, max {max_chars}) → action: {overflow_action}"
        return status, result
    elif char_count < min_chars:
        status = f"THIN ({char_count} chars, min {min_chars})"
        return status, result
    else:
        status = "OK"
        return status, result


def main():
    parser = argparse.ArgumentParser(description="Validate artifact density for Bússola PME deliverables.")
    parser.add_argument("--artifact", required=True, help="Path to artifact file")
    parser.add_argument("--spec", help="JSON spec: {target_chars, max_chars, overflow_action}")
    parser.add_argument("--artifact-id", help="Artifact ID for spec lookup")
    parser.add_argument("--output", help="Path to save JSON result")
    args = parser.parse_args()

    if args.spec:
        try:
            spec = json.loads(args.spec)
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON spec: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.artifact_id:
        spec = ARTIFACT_SPECS.get(args.artifact_id)
        if not spec:
            print(f"ERROR: unknown artifact-id '{args.artifact_id}'", file=sys.stderr)
            sys.exit(1)
    else:
        print("ERROR: must provide --spec or --artifact-id", file=sys.stderr)
        sys.exit(1)

    status, result = validate(args.artifact, spec)
    print(status)

    if args.output:
        Path(args.output).write_text(
            json.dumps({"status": status, **result}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    if status.startswith("OVERFLOW"):
        sys.exit(2)
    elif status.startswith("THIN"):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    # Example: python density_validator.py --artifact resumo.md --artifact-id resumo_executivo
    main()

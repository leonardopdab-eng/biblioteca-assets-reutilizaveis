#!/usr/bin/env python3
"""
Valida se um gate Bússola PME pode ser aprovado ou está bloqueado.

Input:  --gate <G0-G6>       Gate a validar
        --manifest <path>    manifest.yaml do caso
        --case-dir <path>    (opcional) Diretório raiz do caso
Output: GATE_PASS ou GATE_BLOCK: <motivo>

Exit codes:
  0 = GATE_PASS
  2 = GATE_BLOCK

Uso:
  python gate_validator.py --gate G2 --manifest /tmp/manifest.yaml
  # GATE_BLOCK: requires_human (G2 is hardcoded manual)
"""

import argparse
import sys
from pathlib import Path

import yaml


HARDCODED_MANUAL_GATES = {"G2", "G5", "G6"}  # NEVER configurable


def validate_gate(gate: str, manifest: dict, case_dir: str | None) -> tuple[bool, str]:
    gates = manifest.get("gates", {})
    gate_data = gates.get(gate, {})
    if isinstance(gate_data, dict):
        current_status = gate_data.get("status", "not_reached")
    else:
        current_status = str(gate_data)

    # Hardcoded gates always require manual approval
    if gate in HARDCODED_MANUAL_GATES:
        if current_status != "approved":
            return False, f"requires_human ({gate} is HARDCODED MANUAL — never automatic in any mode)"
        return True, f"Gate {gate} already approved"

    # G0 — intake fields check
    if gate == "G0":
        if case_dir:
            intake = Path(case_dir) / "intake_normalized.md"
            gaps = Path(case_dir) / "information_gaps.md"
            if not intake.exists():
                return False, "intake_normalized.md not found"
        if current_status == "approved":
            return True, "G0 approved"
        return False, "G0 pending: intake fields not confirmed"

    # G1 — intake_normalized_v2 approved flag
    if gate == "G1":
        if case_dir:
            v2 = Path(case_dir) / "intake_normalized_v2.md"
            if v2.exists():
                content = v2.read_text(encoding="utf-8")
                if "approved: true" in content:
                    return True, "G1 auto-approved: intake_normalized_v2 has approved flag"
        if current_status == "approved":
            return True, "G1 approved in manifest"
        return False, "G1 pending: intake_normalized_v2 not approved"

    # G3 — action_field_enforcer check
    if gate == "G3":
        if case_dir:
            plano = Path(case_dir) / "plano_acao.md"
            if not plano.exists():
                return False, "plano_acao.md not found"
        if current_status == "approved":
            return True, "G3 approved"
        return False, "G3 pending: plano_acao not validated by action_field_enforcer"

    # G4 — qa_checklist
    if gate == "G4":
        if current_status == "approved":
            return True, "G4 approved"
        return False, "G4 pending: qa_checklist not 100% green"

    return False, f"Gate {gate} not recognized or condition not met"


def main():
    parser = argparse.ArgumentParser(description="Validate Bússola PME gate status.")
    parser.add_argument("--gate", required=True, help="Gate to validate (G0-G6)")
    parser.add_argument("--manifest", required=True, help="Path to manifest.yaml")
    parser.add_argument("--case-dir", help="Case root directory for file-based checks")
    args = parser.parse_args()

    if not Path(args.manifest).exists():
        print(f"GATE_BLOCK: manifest not found: {args.manifest}")
        sys.exit(2)

    with open(args.manifest) as f:
        manifest = yaml.safe_load(f) or {}

    passed, reason = validate_gate(args.gate, manifest, args.case_dir)

    if passed:
        print(f"GATE_PASS: {reason}")
        sys.exit(0)
    else:
        print(f"GATE_BLOCK: {reason}")
        sys.exit(2)


if __name__ == "__main__":
    # Example: python gate_validator.py --gate G2 --manifest /tmp/manifest.yaml
    # GATE_BLOCK: requires_human (G2 is HARDCODED MANUAL)
    main()

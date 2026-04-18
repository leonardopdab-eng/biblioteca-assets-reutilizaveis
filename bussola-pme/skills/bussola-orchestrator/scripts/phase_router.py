#!/usr/bin/env python3
"""
Roteia e exibe status das fases de um caso Bússola PME.

Input:  --manifest <path>    manifest.yaml do caso
        --action <advance|status|block>
Output: JSON (advance) ou ASCII dashboard (status) ou confirmação (block)

Exit codes: 0 (ok), 1 (bloqueado)

Uso:
  python phase_router.py --manifest /tmp/manifest.yaml --action status
  python phase_router.py --manifest /tmp/manifest.yaml --action advance
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


PHASE_DEFINITIONS = {
    0: {"name": "Configuração consultor", "skill": "bussola-personalization", "gate_required": None},
    1: {"name": "Intake cliente", "skill": "bussola-personalization", "gate_required": "G0"},
    2: {"name": "Normalização", "skill": "bussola-diagnostic-engine", "gate_required": "G1"},
    3: {"name": "Diagnóstico", "skill": "bussola-diagnostic-engine", "gate_required": None},
    4: {"name": "Priorização", "skill": "bussola-diagnostic-engine", "gate_required": "G2"},
    5: {"name": "Plano de ação", "skill": "bussola-diagnostic-engine", "gate_required": "G3"},
    6: {"name": "Simulação (opcional)", "skill": "bussola-simulation-lab", "gate_required": None},
    7: {"name": "Geração artefatos", "skill": "bussola-deliverable-forge", "gate_required": "G5"},
    8: {"name": "Handoff execution", "skill": "bussola-execution-bridge", "gate_required": "G6"},
    9: {"name": "Follow-up", "skill": "bussola-deliverable-forge", "gate_required": None},
}

HARDCODED_MANUAL_GATES = {"G2", "G5", "G6"}  # NEVER configurable
GATE_ORDER = ["G0", "G1", "G2", "G3", "G4", "G5", "G6"]

PHASE_ICONS = {
    "completed": "✓",
    "in_progress": "→",
    "blocked": "⚠",
    "pending": " ",
}


def get_gate_status(manifest: dict, gate: str) -> str:
    gdata = manifest.get("gates", {}).get(gate, {"status": "not_reached"})
    return gdata.get("status", "not_reached") if isinstance(gdata, dict) else str(gdata)


def determine_phase_state(phase_num: int, current_phase: int, manifest: dict) -> str:
    if phase_num < current_phase:
        return "completed"
    if phase_num == current_phase:
        phase_def = PHASE_DEFINITIONS[phase_num]
        gate = phase_def.get("gate_required")
        if gate and get_gate_status(manifest, gate) not in ("approved",):
            return "blocked"
        return "in_progress"
    return "pending"


def action_status(manifest: dict) -> str:
    case_id = manifest.get("case_id", "CASE-XXX")
    consultant = manifest.get("consultant_id", "consultor")
    mode = manifest.get("operating_mode", "guided")
    current_phase = manifest.get("current_phase", 0)

    lines = [
        f"Caso {case_id} — {consultant} — {mode} mode",
        "─" * 50,
    ]

    for phase_num, phase_def in PHASE_DEFINITIONS.items():
        state = determine_phase_state(phase_num, current_phase, manifest)
        icon = PHASE_ICONS[state]
        gate = phase_def.get("gate_required", "")
        gate_info = ""
        if gate:
            gs = get_gate_status(manifest, gate)
            hardcoded = "★" if gate in HARDCODED_MANUAL_GATES else ""
            gate_info = f" ({hardcoded}{gate}: {gs})"

        lines.append(f"[{icon}] Fase {phase_num}: {phase_def['name']}{gate_info}")

    lines.append("─" * 50)

    # Next action
    phase_def = PHASE_DEFINITIONS.get(current_phase, {})
    gate = phase_def.get("gate_required")
    if gate and get_gate_status(manifest, gate) != "approved":
        if gate in HARDCODED_MANUAL_GATES:
            lines.append(f"Próximo: aprovar {gate} (HARDCODED MANUAL — requer confirmação humana)")
        else:
            lines.append(f"Próximo: aprovar {gate} para avançar para Fase {current_phase + 1}")
    else:
        skill = phase_def.get("skill", "skill")
        lines.append(f"Próximo: executar Fase {current_phase} via {skill}")

    return "\n".join(lines)


def action_advance(manifest: dict) -> dict:
    current_phase = manifest.get("current_phase", 0)
    phase_def = PHASE_DEFINITIONS.get(current_phase, {})
    gate = phase_def.get("gate_required")

    if gate:
        gs = get_gate_status(manifest, gate)
        if gs != "approved":
            return {
                "blocked": True,
                "gate": gate,
                "gate_status": gs,
                "hardcoded": gate in HARDCODED_MANUAL_GATES,
                "message": f"Cannot advance: {gate} requires approval ({'HARDCODED MANUAL' if gate in HARDCODED_MANUAL_GATES else 'pending'})",
            }

    next_phase = current_phase + 1
    if next_phase not in PHASE_DEFINITIONS:
        return {"completed": True, "message": "All phases completed"}

    next_def = PHASE_DEFINITIONS[next_phase]
    return {
        "blocked": False,
        "next_phase": next_phase,
        "skill_to_call": next_def["skill"],
        "gate_required": next_def.get("gate_required"),
        "message": f"Ready to advance to Phase {next_phase}: {next_def['name']}",
    }


def main():
    parser = argparse.ArgumentParser(description="Route and display Bússola PME case phase status.")
    parser.add_argument("--manifest", required=True, help="Path to manifest.yaml")
    parser.add_argument("--action", required=True, choices=["advance", "status", "block"])
    parser.add_argument("--reason", help="Block reason (for block action)")
    args = parser.parse_args()

    if not Path(args.manifest).exists():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    with open(args.manifest) as f:
        manifest = yaml.safe_load(f) or {}

    if args.action == "status":
        print(action_status(manifest))
        sys.exit(0)

    elif args.action == "advance":
        result = action_advance(manifest)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1 if result.get("blocked") else 0)

    elif args.action == "block":
        import yaml as _yaml
        from datetime import datetime, timezone
        reason = args.reason or "Manual block"
        manifest.setdefault("blocks", []).append({
            "phase": manifest.get("current_phase", 0),
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        with open(args.manifest, "w") as f:
            _yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True)
        print(f"Block registered: {reason}")
        sys.exit(0)


if __name__ == "__main__":
    # Example: python phase_router.py --manifest /tmp/manifest.yaml --action status
    main()

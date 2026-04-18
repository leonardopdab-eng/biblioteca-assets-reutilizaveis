#!/usr/bin/env python3
"""
Constrói e atualiza o manifest.yaml de um caso Bússola PME.

Input:  --action <init|update-gate|update-artifact|update-phase>
        --case-id <str>           (para init)
        --consultant-id <str>     (para init)
        --config <path>           consultant_config.yaml (para init)
        --manifest <path>         manifest.yaml a atualizar
        --gate <G0-G6>            gate a atualizar (update-gate)
        --status <str>            novo status (update-gate, update-artifact)
        --by <str>                quem aprovou (update-gate, opcional)
        --artifact <str>          nome do artefato (update-artifact)
        --phase <int>             nova fase (update-phase)
        --output <path>           (opcional) salvar em path diferente

Exit codes: 0 (ok), 1 (erro de validação)

Uso:
  python manifest_builder.py --action init --case-id BP-001 --consultant-id marina-costa \\
    --config examples/consultant_config_guided.yaml --manifest /tmp/manifest.yaml
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


GATE_ORDER = ["G0", "G1", "G2", "G3", "G4", "G5", "G6"]
GATE_STATUS_PROGRESSION = ["not_reached", "pending", "approved", "blocked"]
HARDCODED_MANUAL_GATES = {"G2", "G5", "G6"}  # NEVER configurable


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def init_manifest(case_id: str, consultant_id: str, config_path: str) -> dict:
    operating_mode = "guided"
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        operating_mode = cfg.get("operating_mode", "guided")

    return {
        "case_id": case_id,
        "consultant_id": consultant_id,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "current_phase": 0,
        "operating_mode": operating_mode,
        "gates": {
            gate: {"status": "not_reached"} for gate in GATE_ORDER
        },
        "artifacts": {
            "hypotheses_log": {"status": "not_started"},
            "problem_tree": {"status": "not_started"},
            "diagnostic_working": {"status": "not_started"},
            "priority_score": {"status": "not_started"},
            "decision_log": {"status": "not_started"},
            "information_gaps": {"status": "not_started"},
            "assumptions_log": {"status": "not_started"},
            "intake_normalized_v2": {"status": "not_started"},
            "diagnostico_executivo": {"status": "not_started"},
            "apresentacao_executiva": {"status": "not_started"},
            "proposta_continuidade": {"status": "not_started"},
            "plano_acao": {"status": "not_started"},
            "plano_acao_cliente": {"status": "not_started"},
            "manifest_yaml": {"status": "active"},
        },
        "human_review_required": [
            "diagnostico_executivo",
            "apresentacao_executiva",
            "proposta_continuidade",
        ],
        "simulation_used": False,
        "execution_confirmed": False,
    }


def load_manifest(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def save_manifest(manifest: dict, path: str):
    manifest["updated_at"] = now_iso()
    with open(path, "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True)


def update_gate(manifest: dict, gate: str, status: str, approved_by: str | None) -> tuple[bool, str]:
    if gate not in GATE_ORDER:
        return False, f"Unknown gate: {gate}"

    current_status = manifest.get("gates", {}).get(gate, {})
    if isinstance(current_status, dict):
        cur = current_status.get("status", "not_reached")
    else:
        cur = str(current_status)

    # Prevent regression (except explicit reset)
    if GATE_STATUS_PROGRESSION.index(status) < GATE_STATUS_PROGRESSION.index(cur) if cur in GATE_STATUS_PROGRESSION else False:
        return False, f"Gate {gate} cannot regress from '{cur}' to '{status}' (use --reset to override)"

    entry = {"status": status}
    if status == "approved":
        entry["approved_at"] = now_iso()
        if approved_by:
            entry["approved_by"] = approved_by

    manifest.setdefault("gates", {})[gate] = entry
    return True, f"Gate {gate} updated to {status}"


def update_artifact(manifest: dict, artifact: str, status: str) -> tuple[bool, str]:
    manifest.setdefault("artifacts", {})[artifact] = {"status": status, "updated_at": now_iso()}
    return True, f"Artifact {artifact} updated to {status}"


def update_phase(manifest: dict, phase: int) -> tuple[bool, str]:
    current = manifest.get("current_phase", 0)
    manifest["current_phase"] = phase
    return True, f"Phase updated from {current} to {phase}"


def main():
    parser = argparse.ArgumentParser(description="Build and update Bússola PME case manifest.")
    parser.add_argument("--action", required=True,
                        choices=["init", "update-gate", "update-artifact", "update-phase"],
                        help="Action to perform")
    parser.add_argument("--case-id", help="Case ID (for init)")
    parser.add_argument("--consultant-id", help="Consultant ID (for init)")
    parser.add_argument("--config", help="consultant_config.yaml path (for init)")
    parser.add_argument("--manifest", help="manifest.yaml path")
    parser.add_argument("--gate", help="Gate name G0-G6 (for update-gate)")
    parser.add_argument("--status", help="New status (for update-gate/artifact)")
    parser.add_argument("--by", help="Approver name (for update-gate)")
    parser.add_argument("--artifact", help="Artifact name (for update-artifact)")
    parser.add_argument("--phase", type=int, help="Phase number (for update-phase)")
    parser.add_argument("--output", help="Output path (defaults to --manifest)")
    args = parser.parse_args()

    output_path = args.output or args.manifest

    if args.action == "init":
        if not args.case_id:
            print("ERROR: --case-id required for init", file=sys.stderr)
            sys.exit(1)
        manifest = init_manifest(
            args.case_id,
            args.consultant_id or "unknown",
            args.config or ""
        )
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            save_manifest(manifest, output_path)
            print(f"Manifest initialized: {output_path}")
        else:
            print(yaml.dump(manifest, default_flow_style=False, allow_unicode=True))

    else:
        if not args.manifest or not Path(args.manifest).exists():
            print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
            sys.exit(1)

        manifest = load_manifest(args.manifest)

        if args.action == "update-gate":
            if not args.gate or not args.status:
                print("ERROR: --gate and --status required for update-gate", file=sys.stderr)
                sys.exit(1)
            ok, msg = update_gate(manifest, args.gate, args.status, args.by)

        elif args.action == "update-artifact":
            if not args.artifact or not args.status:
                print("ERROR: --artifact and --status required for update-artifact", file=sys.stderr)
                sys.exit(1)
            ok, msg = update_artifact(manifest, args.artifact, args.status)

        elif args.action == "update-phase":
            if args.phase is None:
                print("ERROR: --phase required for update-phase", file=sys.stderr)
                sys.exit(1)
            ok, msg = update_phase(manifest, args.phase)

        if not ok:
            print(f"ERROR: {msg}", file=sys.stderr)
            sys.exit(1)

        print(msg)
        save_manifest(manifest, output_path or args.manifest)

    sys.exit(0)


if __name__ == "__main__":
    # Example: python manifest_builder.py --action init --case-id BP-001 --consultant-id marina-costa --manifest /tmp/manifest.yaml
    main()

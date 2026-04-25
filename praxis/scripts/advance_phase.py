#!/usr/bin/env python3
"""
Usage: python advance_phase.py --gate <G0-G6> --approved-by <consultant_id> [--manifest <path>] [--notes <text>]
Updates manifest.yaml after a gate passes. HARDCODED gates G2/G5/G6 require interactive confirmation.
"""
import yaml
import argparse
import datetime
import sys


HARDCODED_HUMAN_GATES = {"G2", "G5", "G6"}  # NEVER auto-advance

GATE_TO_NEXT_PHASE = {
    "G0": 2,
    "G1": 3,
    "G2": 4,
    "G3": 5,
    "G4": 6,
    "G5": 6,
    "G6": None,
}

VALID_GATES = {"G0", "G1", "G2", "G3", "G4", "G5", "G6"}


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_manifest(manifest: dict, path: str):
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Advance praxis case phase after gate approval")
    parser.add_argument("--gate", required=True, help="Gate ID (G0–G6)")
    parser.add_argument("--approved-by", required=True, dest="approved_by",
                        help="Consultant ID or 'AUTO' for automated gates")
    parser.add_argument("--manifest", default="manifest.yaml", help="Path to manifest.yaml")
    parser.add_argument("--notes", default=None, help="Optional approval notes")
    args = parser.parse_args()

    gate = args.gate.upper()

    if gate not in VALID_GATES:
        print(f"ERROR: Invalid gate '{gate}'. Valid: {sorted(VALID_GATES)}", file=sys.stderr)
        sys.exit(1)

    # Hardcoded human gates: NEVER allow AUTO approval
    if gate in HARDCODED_HUMAN_GATES:
        if args.approved_by.upper() == "AUTO":
            print(
                f"\nERROR: Gate {gate} é HARDCODED HUMAN REVIEW.\n"
                f"Auto-avanço BLOQUEADO. Use --approved-by com o ID do consultor.\n"
                f"Comando correto: python advance_phase.py --gate {gate} "
                f"--approved-by <consultant_id>\n",
                file=sys.stderr,
            )
            sys.exit(2)

        # Interactive confirmation required
        print(f"\nGate {gate} é HARDCODED HUMAN REVIEW.")
        print("O consultor revisou e aprovou explicitamente este gate?")
        confirm = input("Confirme digitando 'sim': ").strip().lower()
        if confirm not in ("sim", "yes", "s", "y"):
            print("Gate não avançado. Confirmação explícita obrigatória.")
            sys.exit(3)

    try:
        manifest = load_manifest(args.manifest)
    except FileNotFoundError:
        print(f"ERROR: manifest not found at '{args.manifest}'. Run init_case.py first.", file=sys.stderr)
        sys.exit(1)

    # Check gate ordering: G1 and G2 require G0 first, etc.
    passed_gates = {g["gate"] for g in manifest.get("gates_passed", [])}

    ordering_requirements = {
        "G1": "G0",
        "G2": "G1",
        "G3": "G2",
        "G4": "G3",
        "G5": "G4",
        "G6": "G5",
    }
    if gate in ordering_requirements:
        required = ordering_requirements[gate]
        if required not in passed_gates:
            print(
                f"ERROR: Gate {gate} requires {required} to be passed first. "
                f"Passed gates: {sorted(passed_gates)}",
                file=sys.stderr,
            )
            sys.exit(4)

    # Record approval
    approval_entry = {
        "gate": gate,
        "approved_by": args.approved_by,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    if args.notes:
        approval_entry["notes"] = args.notes

    if "gates_passed" not in manifest:
        manifest["gates_passed"] = []
    manifest["gates_passed"].append(approval_entry)

    if "gates_pending" in manifest and gate in manifest["gates_pending"]:
        manifest["gates_pending"].remove(gate)

    # Advance phase
    next_phase = GATE_TO_NEXT_PHASE.get(gate)
    if next_phase is not None:
        current = manifest.get("current_phase", 1)
        if "phase_history" not in manifest:
            manifest["phase_history"] = []
        manifest["phase_history"].append({
            "phase": current,
            "completed_at": datetime.datetime.utcnow().isoformat() + "Z",
            "gate_passed": gate,
        })
        manifest["current_phase"] = next_phase
        print(f"Phase advanced: {current} → {next_phase}")

    save_manifest(manifest, args.manifest)

    print(f"Gate {gate} passed. Approved by: {args.approved_by}")
    print(f"Manifest updated: {args.manifest}")
    if next_phase:
        print(f"Current phase: {next_phase}")
    else:
        print("Case closed (no further phases).")


if __name__ == "__main__":
    main()

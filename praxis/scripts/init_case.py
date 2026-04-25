#!/usr/bin/env python3
"""
Usage: python init_case.py --consultant <id> --client <name> [--briefing <path>]
Creates manifest.yaml for a new praxis case.
"""
import yaml
import argparse
import uuid
import datetime
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Initialize a new praxis case")
    parser.add_argument("--consultant", required=True, help="Consultant ID (kebab-case)")
    parser.add_argument("--client", required=True, help="Client company name")
    parser.add_argument("--briefing", default=None, help="Path to briefing file (optional)")
    parser.add_argument("--output", default="manifest.yaml", help="Output path for manifest")
    args = parser.parse_args()

    if not args.consultant.replace("-", "").replace("_", "").isalnum():
        print("ERROR: consultant ID must be kebab-case alphanumeric (e.g. joao-silva)", file=sys.stderr)
        sys.exit(1)

    if args.briefing and not os.path.exists(args.briefing):
        print(f"WARNING: briefing file not found: {args.briefing}", file=sys.stderr)

    case_id = f"praxis-{datetime.date.today().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
    now = datetime.datetime.utcnow().isoformat() + "Z"

    manifest = {
        "case_id": case_id,
        "consultant_id": args.consultant,
        "client_identity": {
            "company_name": args.client,
            "segment": None,
            "team_size": None,
            "annual_revenue_range": None,
            "decision_makers": [],
            "branding": {
                "logo_path": None,
                "primary_color": None,
                "accent_color": None,
                "consultant_display_name": "",
                "consultant_company": "",
                "font_family": "Inter",
            },
            "drive_references": [],
        },
        "current_phase": 1,
        "scenario_selected": None,
        "phase_history": [],
        "artifacts_produced": [],
        "gates_passed": [],
        "gates_pending": ["G0", "G1", "G2", "G3", "G4", "G5", "G6"],
        "hardcoded_human_gates": ["G2", "G5", "G6"],
        "created_at": now,
        "updated_at": now,
        "briefing_path": args.briefing,
        "case_id_previous": None,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Case initialized: {case_id}")
    print(f"Client: {args.client}")
    print(f"Consultant: {args.consultant}")
    print(f"Manifest written to: {args.output}")
    print(f"Start Phase 1 — Briefing e Roteamento")


if __name__ == "__main__":
    main()

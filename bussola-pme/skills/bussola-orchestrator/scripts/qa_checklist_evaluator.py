#!/usr/bin/env python3
"""
Wrapper para qa_checklist_runner.py com contexto do manifest.

Input:  --case-dir <path>    Diretório raiz do caso
        --manifest <path>    manifest.yaml
Output: QA_PASS ou QA_FAIL com contexto de gates

Uso:
  python qa_checklist_evaluator.py --case-dir ./casos/BP-001 --manifest ./casos/BP-001/manifest.yaml
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


DELIVERABLE_FORGE_SCRIPT = Path(__file__).parent.parent.parent / "bussola-deliverable-forge" / "scripts" / "qa_checklist_runner.py"


def get_gate_context(manifest: dict) -> str:
    gates = manifest.get("gates", {})
    lines = ["Gate status context:"]
    for gate, data in gates.items():
        status = data.get("status", "unknown") if isinstance(data, dict) else str(data)
        lines.append(f"  {gate}: {status}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run QA checklist with manifest context.")
    parser.add_argument("--case-dir", required=True, help="Case root directory")
    parser.add_argument("--manifest", help="Path to manifest.yaml")
    args = parser.parse_args()

    manifest = {}
    manifest_path = args.manifest or str(Path(args.case_dir) / "governanca" / "manifest.yaml")
    if Path(manifest_path).exists():
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f) or {}
    else:
        manifest_path = str(Path(args.case_dir) / "manifest.yaml")

    print(get_gate_context(manifest))
    print()

    cmd = [sys.executable, str(DELIVERABLE_FORGE_SCRIPT), "--case-dir", args.case_dir]
    if Path(manifest_path).exists():
        cmd.extend(["--manifest", manifest_path])

    result = subprocess.run(cmd, capture_output=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    # Example: python qa_checklist_evaluator.py --case-dir ./casos/BP-001
    main()

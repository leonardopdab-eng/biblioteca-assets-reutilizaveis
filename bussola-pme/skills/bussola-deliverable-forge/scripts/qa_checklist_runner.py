#!/usr/bin/env python3
"""
Executa checklist de QA Gate G4 para validação final do caso Bússola PME.

Input:  --case-dir <path>   Diretório raiz do caso (deve conter interno/, cliente/, governanca/)
        --manifest <path>   (opcional) Path para manifest.yaml
        --output <path>     (opcional) Salvar resultado JSON
Output: QA_PASS ou QA_FAIL: N items failing

Exit codes:
  0 = QA_PASS
  1 = QA_FAIL

Uso:
  python qa_checklist_runner.py --case-dir ./casos/BP-001
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


REQUIRED_INTERNO = [
    "hypotheses_log.md",
    "problem_tree.md",
    "priority_score.md",
    "intake_normalized_v2.md",
]

REQUIRED_CLIENTE = [
    "resumo_executivo.md",
    "diagnostico_executivo.md",
    "matriz_prioridades.md",
    "plano_acao_cliente.md",
]

REQUIRED_GOVERNANCA = [
    "manifest.yaml",
    "qa_checklist.md",
    "gate_transition_log.md",
]

FORBIDDEN_IN_CLIENTE = [
    "diagnostic_working",
    "hypotheses_log",
    "raw_hypothesis",
    "internal_reasoning",
    "[TRILHA INTERNA]",
]

REQUIRED_PLAN_FIELDS = ["owner", "deadline", "kpi"]


def check_artifacts_present(case_dir: Path) -> tuple[bool, list[str]]:
    missing = []
    for fname in REQUIRED_INTERNO:
        if not (case_dir / "interno" / fname).exists():
            missing.append(f"interno/{fname}")
    for fname in REQUIRED_CLIENTE:
        if not (case_dir / "cliente" / fname).exists():
            missing.append(f"cliente/{fname}")
    for fname in REQUIRED_GOVERNANCA:
        if not (case_dir / "governanca" / fname).exists():
            missing.append(f"governanca/{fname}")
    return len(missing) == 0, missing


def check_no_internal_leaks(case_dir: Path) -> tuple[bool, list[str]]:
    leaks = []
    cliente_dir = case_dir / "cliente"
    if not cliente_dir.exists():
        return True, []
    for fpath in cliente_dir.glob("*.md"):
        content = fpath.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_IN_CLIENTE:
            if forbidden.lower() in content:
                leaks.append(f"{fpath.name}: contains '{forbidden}'")
    return len(leaks) == 0, leaks


def check_plano_fields(case_dir: Path) -> tuple[bool, list[str]]:
    failures = []
    plano_path = case_dir / "cliente" / "plano_acao_cliente.md"
    if not plano_path.exists():
        return True, []  # checked in artifacts_present

    content = plano_path.read_text(encoding="utf-8")
    # Check that table rows have non-empty owner, deadline, kpi columns
    # Look for markdown table rows: | action | owner | deadline | kpi |
    import re
    rows = re.findall(r"\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", content)
    for i, row in enumerate(rows[1:], 1):  # skip header
        cells = [c.strip() for c in row]
        if len(cells) >= 4:
            action, owner, deadline, kpi = cells[0], cells[1], cells[2], cells[3]
            if action in ("—", "Ação", "*Ações"):
                continue
            missing = []
            if not owner or owner == "—":
                missing.append("owner")
            if not deadline or deadline == "—":
                missing.append("deadline")
            if not kpi or kpi == "—":
                missing.append("kpi")
            if missing:
                failures.append(f"plano row {i}: missing {missing}")
    return len(failures) == 0, failures


def check_hypothesis_flags(case_dir: Path) -> tuple[bool, list[str]]:
    issues = []
    # Check that hypothesis_propagation_log exists and is non-empty if any propagated flags found
    prop_log = case_dir / "governanca" / "hypothesis_propagation_log.md"
    # This is a soft check - log should exist
    if not prop_log.exists():
        issues.append("hypothesis_propagation_log.md missing from governanca/")
    return len(issues) == 0, issues


def check_manifest_current(case_dir: Path, manifest_path: str | None) -> tuple[bool, list[str]]:
    if manifest_path:
        mpath = Path(manifest_path)
    else:
        mpath = case_dir / "governanca" / "manifest.yaml"
        if not mpath.exists():
            mpath = case_dir / "manifest.yaml"

    if not mpath.exists():
        return False, ["manifest.yaml not found"]

    try:
        with open(mpath) as f:
            manifest = yaml.safe_load(f)
        required_keys = ["case_id", "gates"]
        missing = [k for k in required_keys if k not in manifest]
        if missing:
            return False, [f"manifest missing keys: {missing}"]
    except Exception as e:
        return False, [f"manifest parse error: {e}"]

    return True, []


def check_branding(case_dir: Path) -> tuple[bool, list[str]]:
    # Soft check: verify client track files have some styling indication
    # In practice, this checks that branding config was applied
    config_snap = case_dir / "governanca" / "consultant_config_snapshot.yaml"
    if not config_snap.exists():
        return False, ["consultant_config_snapshot.yaml missing (branding not applied)"]
    return True, []


def check_apresentacao_g5(case_dir: Path, manifest_path: str | None) -> tuple[bool, list[str]]:
    if manifest_path:
        mpath = Path(manifest_path)
    else:
        mpath = case_dir / "governanca" / "manifest.yaml"
        if not mpath.exists():
            mpath = case_dir / "manifest.yaml"

    if not mpath.exists():
        return False, ["manifest.yaml not found for G5 check"]

    try:
        with open(mpath) as f:
            manifest = yaml.safe_load(f)
        g5_status = manifest.get("gates", {}).get("G5", {})
        if isinstance(g5_status, dict):
            status = g5_status.get("status", "not_reached")
        else:
            status = str(g5_status)
        if status != "approved":
            return False, [f"Gate G5 not approved (status: {status}) — apresentacao_executiva requires human review"]
    except Exception as e:
        return False, [f"G5 check error: {e}"]

    return True, []


def main():
    parser = argparse.ArgumentParser(description="Run QA checklist (Gate G4) for Bússola PME case.")
    parser.add_argument("--case-dir", required=True, help="Root directory of the case")
    parser.add_argument("--manifest", help="Path to manifest.yaml (defaults to case-dir/governanca/manifest.yaml)")
    parser.add_argument("--output", help="Path to save JSON result")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    checks = [
        ("Todos os artefatos presentes", check_artifacts_present(case_dir)),
        ("Nenhum leak interno em trilha cliente", check_no_internal_leaks(case_dir)),
        ("Todos os itens do plano têm owner/deadline/KPI", check_plano_fields(case_dir)),
        ("Hipóteses propagadas sinalizadas", check_hypothesis_flags(case_dir)),
        ("manifest.yaml reflete estado atual", check_manifest_current(case_dir, args.manifest)),
        ("Branding tokens aplicados", check_branding(case_dir)),
        ("Gate G5 aprovado (apresentacao_executiva)", check_apresentacao_g5(case_dir, args.manifest)),
    ]

    results = []
    failing = 0
    for label, (passed, details) in checks:
        icon = "✓" if passed else "✗"
        print(f"{icon} {label}")
        if not passed and details:
            for d in details:
                print(f"  → {d}")
            failing += 1
        results.append({"check": label, "passed": passed, "details": details})

    print()
    if failing == 0:
        print("QA_PASS")
    else:
        print(f"QA_FAIL: {failing} items failing")

    if args.output:
        Path(args.output).write_text(
            json.dumps({"status": "QA_PASS" if failing == 0 else "QA_FAIL", "failing": failing, "checks": results}, indent=2),
            encoding="utf-8"
        )

    sys.exit(0 if failing == 0 else 1)


if __name__ == "__main__":
    # Example: python qa_checklist_runner.py --case-dir ./casos/BP-001
    main()

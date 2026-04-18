#!/usr/bin/env python3
"""
Verifica completude dos campos do intake para Bússola PME.

Input:  --intake <path>  (markdown com frontmatter YAML OU yaml puro)
        --gaps   <path>  (information_gaps.md, opcional)
Output: COMPLETE, PARTIAL (N/10 fields with M gaps registered),
        ou BLOCKED: missing required fields without gap entry

Exit codes:
  0 = COMPLETE ou PARTIAL com gaps registrados para ausentes
  2 = BLOCKED (campos obrigatórios ausentes sem gap registrado)

Uso:
  python intake_field_checker.py --intake intake_normalized.md
  python intake_field_checker.py --intake intake_normalized.yaml --gaps information_gaps.md
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = [
    "company_name",
    "segment",
    "team_size",
    "annual_revenue_range",
    "primary_problem",
    "urgency_level",
    "decision_makers",
]

OPTIONAL_FIELDS = [
    "secondary_problems",
    "previous_diagnosis",
    "available_documents",
]

ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


def parse_intake(path: str) -> dict:
    content = Path(path).read_text(encoding="utf-8")

    # Try YAML frontmatter (--- ... ---)
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        return yaml.safe_load(fm_match.group(1)) or {}

    # Try pure YAML
    try:
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            return data
    except yaml.YAMLError:
        pass

    # Try inline key: value pairs from markdown (loose parsing)
    result = {}
    for line in content.splitlines():
        m = re.match(r"^[`\*]*(\w+)[`\*]*\s*[:=]\s*(.+)", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip().strip('"\'').split(" [")[0]
            if key in ALL_FIELDS:
                result[key] = value
    return result


def parse_gaps(path: str) -> list[str]:
    if not path or not Path(path).exists():
        return []
    content = Path(path).read_text(encoding="utf-8")

    # Try YAML list
    try:
        data = yaml.safe_load(content)
        if isinstance(data, list):
            gaps = []
            for item in data:
                if isinstance(item, dict):
                    gaps.append(item.get("field", ""))
                elif isinstance(item, str):
                    gaps.append(item)
            return [g for g in gaps if g]
    except yaml.YAMLError:
        pass

    # Parse markdown: look for field names as headers or bullet items
    gaps = []
    for line in content.splitlines():
        for field in ALL_FIELDS:
            if field in line:
                gaps.append(field)
                break
    return list(set(gaps))


def check(intake_path: str, gaps_path: str | None) -> tuple[str, dict]:
    intake = parse_intake(intake_path)
    gaps = parse_gaps(gaps_path) if gaps_path else []

    present = [f for f in ALL_FIELDS if intake.get(f) not in (None, "", [], {})]
    absent_required = [f for f in REQUIRED_FIELDS if f not in present]
    absent_optional = [f for f in OPTIONAL_FIELDS if f not in present]

    # Check required fields missing without gap
    missing_without_gap = [f for f in absent_required if f not in gaps]

    total_present = len(present)
    total_gaps = len([f for f in absent_required if f in gaps])

    result = {
        "present": present,
        "absent_required": absent_required,
        "absent_optional": absent_optional,
        "gaps_registered": [f for f in absent_required if f in gaps],
        "missing_without_gap": missing_without_gap,
        "score": f"{total_present}/10",
    }

    if missing_without_gap:
        status = f"BLOCKED: missing required fields without gap entry: {missing_without_gap}"
        return status, result

    if absent_required and not missing_without_gap:
        status = f"PARTIAL ({total_present}/10 fields with {total_gaps} gaps registered)"
    elif absent_optional:
        status = f"PARTIAL ({total_present}/10 fields with {len(absent_optional)} optional absent)"
    else:
        status = "COMPLETE"

    return status, result


def main():
    parser = argparse.ArgumentParser(description="Check intake field completeness for Bússola PME.")
    parser.add_argument("--intake", required=True, help="Path to intake file (markdown or YAML)")
    parser.add_argument("--gaps", help="Path to information_gaps.md")
    parser.add_argument("--json", action="store_true", help="Output full JSON result")
    args = parser.parse_args()

    status, result = check(args.intake, args.gaps)

    if getattr(args, "json"):
        print(json.dumps({"status": status, **result}, indent=2))
    else:
        print(status)

    if status.startswith("BLOCKED"):
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    # Example: python intake_field_checker.py --intake intake_normalized.md --gaps information_gaps.md
    main()

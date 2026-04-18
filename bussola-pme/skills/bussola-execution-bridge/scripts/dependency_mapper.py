#!/usr/bin/env python3
"""
Mapeia dependências entre epics/issues do plano Bússola PME.

Input:  --epics <json>   JSON da estrutura de epics (saída de plano_to_epics.py)
        --output <path>  (opcional) Salvar grafo JSON
Output: JSON com grafo de dependências por epic/issue

Uso:
  python dependency_mapper.py --epics '{"epics":[...]}'
"""

import argparse
import json
import sys
from pathlib import Path


def extract_dependencies(epics: list) -> list:
    deps = []

    # Simple heuristic: if an issue mentions another owner, create soft dependency
    all_issues = []
    for epic_idx, epic in enumerate(epics):
        for issue_idx, issue in enumerate(epic.get("issues", [])):
            all_issues.append({
                "epic_idx": epic_idx,
                "issue_idx": issue_idx,
                "title": issue.get("title", ""),
                "assignee": issue.get("assignee", ""),
                "description": issue.get("description", ""),
            })

    # Find keyword-based dependencies
    dependency_keywords = [
        ("após", "after"),
        ("depende de", "depends on"),
        ("requer", "requires"),
        ("depois de", "after"),
    ]

    for i, issue_a in enumerate(all_issues):
        for j, issue_b in enumerate(all_issues):
            if i == j:
                continue
            # Check if issue_a description references issue_b's title
            desc_lower = issue_a["description"].lower()
            title_b_words = [w for w in issue_b["title"].lower().split() if len(w) > 4]
            for word in title_b_words:
                if word in desc_lower:
                    deps.append({
                        "blocking_issue": j,
                        "blocked_issue": i,
                        "reason": f"'{word}' mentioned in description",
                        "type": "inferred",
                    })
                    break

    return deps


def main():
    parser = argparse.ArgumentParser(description="Map dependencies between Bússola PME epics/issues.")
    parser.add_argument("--epics", required=True, help="JSON string or path with epics structure")
    parser.add_argument("--output", help="Path to save dependency graph JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.epics)
    except json.JSONDecodeError:
        # Try reading as file
        data = json.loads(Path(args.epics).read_text(encoding="utf-8"))

    epics = data.get("epics", data) if isinstance(data, dict) else data
    deps = extract_dependencies(epics)

    result = {
        "total_epics": len(epics),
        "total_issues": sum(len(e.get("issues", [])) for e in epics),
        "dependencies": deps,
        "note": "Dependencies are inferred from keyword matching. Review before creating in Linear.",
    }

    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python dependency_mapper.py --epics '{"epics":[]}'
    main()

#!/usr/bin/env python3
"""
Converte plano_acao Bússola PME em estrutura de projeto Linear (epics + issues).

Input:  --plano <path>   plano_acao.yaml ou .json
        --output <path>  (opcional) Salvar JSON de saída
Output: JSON com {project, epics: [{name, description, issues: [...]}]}

Uso:
  python plano_to_epics.py --plano plano_acao.yaml
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


def group_by_owner(actions: list) -> dict[str, list]:
    groups: dict[str, list] = {}
    for action in actions:
        owner = action.get("owner", "Sem responsável")
        if owner not in groups:
            groups[owner] = []
        groups[owner].append(action)
    return groups


def build_issue(action: dict, idx: int) -> dict:
    title = action.get("acao", f"Ação {idx}")
    kpi = action.get("kpi", "—")
    deadline = action.get("deadline", "—")
    owner = action.get("owner", "—")

    description = (
        f"## Contexto\n"
        f"Ação do plano Bússola PME.\n\n"
        f"## KPI\n{kpi}\n\n"
        f"## Prazo\n{deadline}\n\n"
        f"## Responsável\n{owner}"
    )

    return {
        "title": f"[Bússola] {title}",
        "description": description,
        "assignee": owner,
        "due_date": deadline,
        "state": "Backlog",
        "labels": ["bussola-pme"],
        "estimate": 2,  # default story points
    }


def plano_to_epics(plano_path: str) -> dict:
    content = Path(plano_path).read_text(encoding="utf-8")

    # Try JSON first
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = yaml.safe_load(content) or {}

    # Support both list and dict with "actions" key
    if isinstance(data, list):
        actions = data
    elif isinstance(data, dict):
        actions = data.get("actions", data.get("ações", []))
    else:
        actions = []

    # Group actions by owner → each owner becomes an epic
    owner_groups = group_by_owner(actions)

    epics = []
    for owner, owner_actions in owner_groups.items():
        issues = [build_issue(a, i + 1) for i, a in enumerate(owner_actions)]
        epic = {
            "name": f"[Bússola PME] Iniciativas — {owner}",
            "description": (
                f"Epic de ações sob responsabilidade de {owner}. "
                f"Gerado automaticamente pelo sistema Bússola PME."
            ),
            "owner": owner,
            "issues": issues,
            "labels": ["bussola-pme", "epic"],
        }
        epics.append(epic)

    # Derive case_id from path if possible
    case_id = Path(plano_path).stem.split("_")[0] if "_" in Path(plano_path).stem else "BP-XXX"

    return {
        "project": {
            "name": f"Bússola PME — Execução {case_id}",
            "description": f"Projeto de execução gerado a partir do plano de ação do caso {case_id}.",
            "team": "default",
            "labels": ["bussola-pme", f"case-{case_id.lower()}"],
        },
        "epics": epics,
        "total_issues": sum(len(e["issues"]) for e in epics),
        "total_epics": len(epics),
    }


def main():
    parser = argparse.ArgumentParser(description="Convert Bússola PME action plan to Linear project structure.")
    parser.add_argument("--plano", required=True, help="Path to plano_acao.yaml or .json")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    result = plano_to_epics(args.plano)
    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python plano_to_epics.py --plano plano_acao.yaml
    main()

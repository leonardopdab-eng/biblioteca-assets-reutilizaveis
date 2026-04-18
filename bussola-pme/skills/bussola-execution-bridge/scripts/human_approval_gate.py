#!/usr/bin/env python3
"""
Formata preview do projeto Linear para Gate G6 (HARDCODED MANUAL).

Input:  --preview <json>   Estrutura do projeto (saída de plano_to_epics.py)
        --output <path>    (opcional) Salvar preview formatado
Output: Markdown legível do projeto a ser criado no Linear

IMPORTANTE: Este script NUNCA executa write no Linear.
Apenas formata o preview para o consultor revisar antes de G6.

Uso:
  python human_approval_gate.py --preview '{"project":"BP-001","epics":[]}'
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


HARDCODED_MANUAL_GATES = {"G2", "G5", "G6"}  # NEVER configurable
G6_GATE = "G6"


def format_preview(data: dict) -> str:
    project = data.get("project", {})
    if isinstance(project, str):
        project_name = project
        project_desc = ""
    else:
        project_name = project.get("name", "Projeto Bússola PME")
        project_desc = project.get("description", "")

    epics = data.get("epics", [])
    total_epics = len(epics)
    total_issues = sum(len(e.get("issues", [])) for e in epics)
    workspace = project.get("team", "default") if isinstance(project, dict) else "default"

    lines = [
        "## ⚠️ Gate G6 — REVISÃO OBRIGATÓRIA ⚠️",
        "",
        "**Este gate é HARDCODED MANUAL. Não há modo automático.**",
        "",
        "### Projeto a ser criado no Linear",
        f"- **Nome**: {project_name}",
        f"- **Workspace**: {workspace}",
        f"- **Descrição**: {project_desc}",
        f"- **Total de epics**: {total_epics}",
        f"- **Total de issues**: {total_issues}",
        "",
        "### Epics e Issues",
    ]

    for i, epic in enumerate(epics, 1):
        lines.append(f"")
        lines.append(f"**Epic {i}**: {epic.get('name', 'Epic')}")
        for j, issue in enumerate(epic.get("issues", []), 1):
            assignee = issue.get("assignee", "—")
            deadline = issue.get("due_date", "—")
            lines.append(f"  - Issue {j}: {issue.get('title', 'Issue')} | Assignee: {assignee} | Prazo: {deadline}")

    lines += [
        "",
        "---",
        "",
        f"**Timestamp desta exibição**: {datetime.now(timezone.utc).isoformat()}",
        "",
        "### Para confirmar a criação:",
        '> Responda: **"confirmo a criação do projeto"**',
        "",
        "### Para cancelar:",
        '> Responda: **"cancelar"** ou **"não criar agora"**',
        "",
        "> ⚠️ Esta ação criará recursos no Linear — efeito externo irreversível.",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Format Gate G6 preview for Linear project creation (read-only, no side effects)."
    )
    parser.add_argument("--preview", required=True, help="JSON preview data (or path to JSON file)")
    parser.add_argument("--output", help="Path to save formatted preview")
    args = parser.parse_args()

    try:
        data = json.loads(args.preview)
    except json.JSONDecodeError:
        try:
            data = json.loads(Path(args.preview).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"ERROR: Cannot parse preview: {e}", file=sys.stderr)
            sys.exit(1)

    preview_text = format_preview(data)
    print(preview_text)

    if args.output:
        Path(args.output).write_text(preview_text, encoding="utf-8")

    # This script NEVER makes any external calls
    sys.exit(0)


if __name__ == "__main__":
    # Example: python human_approval_gate.py --preview '{"project":"BP-001","epics":[]}'
    # Output: formatted markdown preview, NO side effects
    main()

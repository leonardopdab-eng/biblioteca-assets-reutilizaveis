#!/usr/bin/env python3
"""
Anonimiza artefatos de caso Bússola PME para uso em showcase comercial.

Input:  --case-dir <path>    Diretório do caso original (apenas cliente/)
        --rules <path>       Arquivo de regras de anonimização (.md ou .yaml)
        --output-dir <path>  Diretório para salvar versão anonimizada
Output: Cópias anonimizadas + anonymization_log.md

Uso:
  python anonymizer.py --case-dir ./casos/BP-001 \\
    --rules references/anonymization_rules.md \\
    --output-dir ./showcase/BP-001-anon
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Default substitution dictionary
DEFAULT_SUBSTITUTIONS = {
    # Names → fictional equivalents
    "Marina Costa": "Ana Silva",
    "marina costa": "ana silva",
    "Marina": "Ana",
    "marina": "ana",
    "Rafael Lima": "Bruno Oliveira",
    "rafael lima": "bruno oliveira",
    "Rafael": "Bruno",
    "rafael": "bruno",
    "João Alves": "Carlos Mendes",
    "joao alves": "carlos mendes",

    # Company names → generalized
    "Agência BP-001": "Agência B2B [Cliente Anônimo]",
    "BP-001": "CASE-ANON",
    "BP001": "CASE-ANON",

    # Revenue specifics → ranges (handled separately)
    "R$ 960k": "~R$ 900k–1M",
    "R$ 800k": "~R$ 750k–850k",

    # Sensitive patterns
    "CNPJ": "[CNPJ removido]",
    "CPF": "[CPF removido]",
}

# Patterns for metric rounding
METRIC_PATTERNS = [
    (r"R\$\s*(\d+\.?\d*)(k|mil|M|MM)?", "_round_metric"),
    (r"(\d+)%", "_round_pct"),
]


def round_metric(value_str: str, suffix: str) -> str:
    try:
        val = float(value_str.replace(".", "").replace(",", "."))
        if suffix in ("k", "mil"):
            val *= 1000
        elif suffix in ("M", "MM"):
            val *= 1_000_000
        rounded = round(val * 0.95 / 10000) * 10000  # Round to nearest 10k
        if rounded >= 1_000_000:
            return f"R$ {rounded/1_000_000:.1f}M"
        elif rounded >= 1000:
            return f"R$ {rounded/1000:.0f}k"
        return f"R$ {rounded:.0f}"
    except Exception:
        return f"R$ [valor]"


def anonymize_text(text: str, substitutions: dict) -> tuple[str, list]:
    result = text
    log = []

    for original, replacement in substitutions.items():
        if original in result:
            count = result.count(original)
            result = result.replace(original, replacement)
            log.append({"original": original, "replacement": replacement, "occurrences": count})

    # Round percentages with ±5% noise indicator
    pct_pattern = re.compile(r"(\d+)%")
    for match in pct_pattern.finditer(text):
        val = int(match.group(1))
        low = max(val - 5, 0)
        high = val + 5
        new_val = f"~{low}–{high}%"
        if match.group(0) in result and match.group(0) != new_val:
            log.append({"original": match.group(0), "replacement": new_val, "type": "metric_rounding"})
            result = result.replace(match.group(0), new_val, 1)

    return result, log


def anonymize_case(case_dir: Path, output_dir: Path, rules_path: str | None) -> list:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cliente").mkdir(exist_ok=True)

    substitutions = DEFAULT_SUBSTITUTIONS.copy()

    if rules_path and Path(rules_path).exists():
        # Try to parse YAML substitutions from rules file
        content = Path(rules_path).read_text(encoding="utf-8")
        try:
            rules = yaml.safe_load(content)
            if isinstance(rules, dict) and "substitutions" in rules:
                substitutions.update(rules["substitutions"])
        except Exception:
            pass

    all_logs = []
    client_dir = case_dir / "cliente"
    if not client_dir.exists():
        client_dir = case_dir

    for fpath in client_dir.glob("*.md"):
        original_text = fpath.read_text(encoding="utf-8")
        anonymized_text, file_logs = anonymize_text(original_text, substitutions)

        out_path = output_dir / "cliente" / fpath.name
        out_path.write_text(anonymized_text, encoding="utf-8")

        for entry in file_logs:
            all_logs.append({"file": fpath.name, **entry})

    return all_logs


def build_anonymization_log(logs: list) -> str:
    lines = [
        "# Anonymization Log — Bússola PME Showcase",
        f"",
        f"**Generated**: {datetime.utcnow().isoformat()}",
        f"**Total substitutions**: {len(logs)}",
        "",
        "## Substitutions made",
        "",
        "| File | Original | Replacement | Type |",
        "|------|----------|-------------|------|",
    ]
    for log in logs:
        lines.append(
            f"| {log.get('file', '—')} | "
            f"`{log.get('original', '—')}` | "
            f"`{log.get('replacement', '—')}` | "
            f"{log.get('type', 'name_substitution')} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Anonymize Bússola PME case artifacts for showcase.")
    parser.add_argument("--case-dir", required=True, help="Case directory (contains cliente/)")
    parser.add_argument("--rules", help="Anonymization rules file (.md or .yaml)")
    parser.add_argument("--output-dir", required=True, help="Output directory for anonymized artifacts")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    output_dir = Path(args.output_dir)

    logs = anonymize_case(case_dir, output_dir, args.rules)

    # Write anonymization log
    log_content = build_anonymization_log(logs)
    log_path = output_dir / "anonymization_log.md"
    log_path.write_text(log_content, encoding="utf-8")

    print(f"Anonymized {len(logs)} substitutions across case artifacts.")
    print(f"Output: {output_dir}")
    print(f"Log: {log_path}")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python anonymizer.py --case-dir ./casos/BP-001 --rules references/anonymization_rules.md --output-dir /tmp/anon
    main()

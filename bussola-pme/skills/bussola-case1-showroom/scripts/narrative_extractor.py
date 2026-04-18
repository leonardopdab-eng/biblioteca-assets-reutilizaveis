#!/usr/bin/env python3
"""
Extrai beats narrativos de um caso Bússola PME anonimizado para uso em showcase.

Input:  --case-dir <path>    Diretório do caso anonimizado (contém cliente/)
Output: JSON com problema_central, achados_chave, top_acoes, resultado_esperado

Uso:
  python narrative_extractor.py --case-dir ./showcase/BP-001-anon
  python narrative_extractor.py --case-dir ./showcase/BP-001-anon --output narrative.json
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Keywords to detect the central problem section
PROBLEM_KEYWORDS = [
    "problema", "desafio", "dificuldade", "situação", "contexto",
    "queda", "redução", "perda", "bottleneck", "gargalo",
]

# Keywords to detect findings / diagnostics
FINDING_KEYWORDS = [
    "diagnóstico", "achado", "causa", "raiz", "análise", "descoberta",
    "identificou", "revelou", "evidência", "dado", "métrica",
]

# Keywords to detect actions / recommendations
ACTION_KEYWORDS = [
    "ação", "recomendação", "iniciativa", "prioridade", "implementar",
    "realizar", "executar", "proposta", "plano", "próximo passo",
]

# Keywords to detect expected results
RESULT_KEYWORDS = [
    "resultado esperado", "impacto projetado", "meta", "objetivo",
    "retorno", "ROI", "crescimento esperado", "projeção",
]


def score_line(line: str, keywords: list[str]) -> int:
    line_lower = line.lower()
    return sum(1 for kw in keywords if kw in line_lower)


def extract_section_text(lines: list[str], keywords: list[str], max_chars: int = 300) -> str:
    best_score = 0
    best_start = 0

    for i, line in enumerate(lines):
        score = score_line(line, keywords)
        if score > best_score:
            best_score = score
            best_start = i

    if best_score == 0:
        return ""

    # Gather text around the best-scoring line
    chunk = []
    for line in lines[best_start: best_start + 5]:
        stripped = line.strip()
        if stripped:
            chunk.append(stripped)

    result = " ".join(chunk)
    return result[:max_chars] if len(result) > max_chars else result


def extract_bullet_items(lines: list[str], keywords: list[str], max_items: int = 3) -> list[str]:
    items = []
    in_section = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if line is a section header matching keywords
        if score_line(stripped, keywords) > 0 and stripped.startswith("#"):
            in_section = True
            continue

        if in_section:
            # Stop at next section header
            if stripped.startswith("#"):
                break
            # Collect bullet items
            if stripped.startswith(("-", "*", "•")) or re.match(r"^\d+\.", stripped):
                item = re.sub(r"^[-*•\d.]\s*", "", stripped)
                if item:
                    items.append(item)
                    if len(items) >= max_items:
                        break

    return items


def extract_narrative(case_dir: Path) -> dict:
    client_dir = case_dir / "cliente"
    if not client_dir.exists():
        client_dir = case_dir

    all_lines = []
    source_files = []

    for fpath in sorted(client_dir.glob("*.md")):
        try:
            text = fpath.read_text(encoding="utf-8")
            lines = text.splitlines()
            all_lines.extend(lines)
            source_files.append(fpath.name)
        except Exception:
            pass

    if not all_lines:
        return {
            "problema_central": "[Nenhum artefato encontrado]",
            "achados_chave": [],
            "top_acoes": [],
            "resultado_esperado": "[Sem dados]",
            "source_files": [],
            "extraction_quality": "empty",
        }

    problema = extract_section_text(all_lines, PROBLEM_KEYWORDS, max_chars=400)
    achados = extract_bullet_items(all_lines, FINDING_KEYWORDS, max_items=3)
    acoes = extract_bullet_items(all_lines, ACTION_KEYWORDS, max_items=3)
    resultado = extract_section_text(all_lines, RESULT_KEYWORDS, max_chars=300)

    # Fallback: use first non-empty paragraph as problema if nothing found
    if not problema:
        for line in all_lines:
            if line.strip() and not line.strip().startswith("#"):
                problema = line.strip()[:300]
                break

    quality = "full" if (problema and achados and acoes and resultado) else "partial"

    return {
        "problema_central": problema or "[Não identificado]",
        "achados_chave": achados or ["[Achados não estruturados nos artefatos]"],
        "top_acoes": acoes or ["[Ações não estruturadas nos artefatos]"],
        "resultado_esperado": resultado or "[Resultado não especificado]",
        "source_files": source_files,
        "extraction_quality": quality,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract narrative beats from anonymized Bússola PME case.")
    parser.add_argument("--case-dir", required=True, help="Anonymized case directory")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    if not case_dir.exists():
        print(f"ERROR: case-dir not found: {case_dir}", file=sys.stderr)
        sys.exit(1)

    narrative = extract_narrative(case_dir)

    output_json = json.dumps(narrative, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"Narrative extracted to: {args.output}")
        print(f"Quality: {narrative['extraction_quality']}")
    else:
        print(output_json)

    sys.exit(0)


if __name__ == "__main__":
    main()

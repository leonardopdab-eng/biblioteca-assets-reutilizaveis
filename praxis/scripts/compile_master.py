#!/usr/bin/env python3
"""
Usage: python compile_master.py --manifest <path> [--output-dir <dir>] [--directive <completo|executivo|plano_acao>]
Aggregates all artifacts from manifest into A-MASTER following Agente 00 rules C1-C8.
"""
import yaml
import argparse
import datetime
import hashlib
import os
import re
import sys


INTERNAL_TRACK_MARKER = "[TRILHA_INTERNA]"
CLIENT_TRACK_MARKER = "[TRILHA_CLIENTE]"

SECTION_ORDER = [
    ("Seção 1: Contexto e Situação", ["A-01"]),
    ("Seção 2: Identidade e Proposta Comercial", ["A-02", "A-03", "A-04"]),
    ("Seção 3: Diagnóstico", ["A-05", "A-06", "A-07", "A-08", "A-09"]),
    ("Seção 4: Cenários e Simulações", ["A-10", "A-11"]),
    ("Seção 5: Plano de Ação", []),
    ("Seção 6: Próximos Passos e Handoff", []),
    ("Apêndice A: Log de Decisões", []),
    ("Apêndice B: Trilha Epistêmica", []),
]

EPISTEMIC_LABELS = ["[FATO]", "[INFERÊNCIA]", "[HIPÓTESE]"]


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_artifact(path: str) -> str:
    if not path or not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalize_headings(text: str, base_level: int = 3) -> str:
    """Shift all headings to start at base_level (H3 by default for section content)."""
    lines = text.split("\n")
    result = []
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            hashes = m.group(1)
            title = m.group(2)
            # Map H1→H3, H2→H3, H3→H3, H4→H4, etc.
            new_level = min(max(len(hashes), base_level), 6)
            result.append("#" * new_level + " " + title)
        else:
            result.append(line)
    return "\n".join(result)


def extract_epistemic_claims(text: str, section: str) -> list:
    """Extract all labeled claims for Apêndice B."""
    claims = []
    for line in text.split("\n"):
        for label in EPISTEMIC_LABELS:
            if label in line:
                claims.append({"section": section, "label": label, "text": line.strip()[:200]})
    return claims


def check_c7_completeness(sections: dict) -> list:
    """Rule C7: minimum completeness checks."""
    failures = []
    s1 = sections.get("Seção 1: Contexto e Situação", "")
    if s1.count("\n") < 3:
        failures.append("Seção 1 tem menos de 3 campos normalizados de A-01")
    s3 = sections.get("Seção 3: Diagnóstico", "")
    if "causa raiz" not in s3.lower() and "causa principal" not in s3.lower():
        failures.append("Seção 3 não contém causa raiz identificada")
    s5 = sections.get("Seção 5: Plano de Ação", "")
    if "responsável" not in s5.lower() and "prazo" not in s5.lower():
        failures.append("Seção 5 não contém ação com responsável e prazo")
    has_fato = any("[FATO]" in v for v in sections.values())
    if not has_fato:
        failures.append("Nenhum [FATO] presente no documento")
    return failures


def main():
    parser = argparse.ArgumentParser(description="Compile A-MASTER from praxis artifacts")
    parser.add_argument("--manifest", default="manifest.yaml")
    parser.add_argument("--output-dir", default=".", dest="output_dir")
    parser.add_argument("--directive", default="completo",
                        choices=["completo", "executivo", "plano_acao", "personalizado"])
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    case_id = manifest.get("case_id", "unknown")
    client_name = manifest.get("client_identity", {}).get("company_name", "Cliente")
    artifacts_produced = {a["artifact_id"]: a for a in manifest.get("artifacts_produced", [])}

    # Rule C1: collect artifacts in phase ASC order
    artifact_contents = {}
    for art_id, art_info in sorted(artifacts_produced.items(),
                                   key=lambda x: (x[1].get("phase", 99), x[1].get("produced_at", ""))):
        path = art_info.get("path", "")
        content = load_artifact(path)
        if content:
            artifact_contents[art_id] = content

    # Rule C2: build sections
    sections = {}
    dedup_log = []
    all_claims = []

    for section_name, art_ids in SECTION_ORDER:
        section_parts = []
        for art_id in art_ids:
            if art_id in artifact_contents:
                content = normalize_headings(artifact_contents[art_id], base_level=3)
                # Rule C4: simple dedup check
                for existing_section, existing_content in sections.items():
                    if content[:100] in existing_content:
                        dedup_log.append({
                            "claim": content[:100],
                            "kept_in": existing_section,
                            "skipped_from": section_name,
                            "reason": "duplicate content (first 100 chars match)",
                        })
                        content = ""
                        break
                if content:
                    section_parts.append(f"<!-- Source: {art_id} -->\n{content}")
                    claims = extract_epistemic_claims(content, section_name)
                    all_claims.extend(claims)
        sections[section_name] = "\n\n".join(section_parts)

    # Plano de Ação — synthesize from diagnostic + simulation
    plan_content = artifact_contents.get("A-09", artifact_contents.get("A-08", artifact_contents.get("A-07", "")))
    if plan_content:
        plan_section = normalize_headings(plan_content, base_level=3)
        sections["Seção 5: Plano de Ação"] = "<!-- Sintetizado de análise diagnóstica -->\n" + plan_section
        claims = extract_epistemic_claims(plan_section, "Seção 5: Plano de Ação")
        all_claims.extend(claims)

    # Gate log for Apêndice A
    gate_log_lines = ["| Gate | Aprovado Por | Timestamp | Notas |", "|---|---|---|---|"]
    for gate in manifest.get("gates_passed", []):
        gate_log_lines.append(
            f"| {gate.get('gate')} | {gate.get('approved_by')} | "
            f"{gate.get('timestamp')} | {gate.get('notes', '—')} |"
        )
    sections["Apêndice A: Log de Decisões"] = "\n".join(gate_log_lines)

    # Apêndice B — epistemic trail
    if all_claims:
        b_lines = ["| Seção | Rótulo | Afirmação |", "|---|---|---|"]
        for c in all_claims:
            b_lines.append(f"| {c['section']} | {c['label']} | {c['text'][:120]} |")
        sections["Apêndice B: Trilha Epistêmica"] = "\n".join(b_lines)
    else:
        sections["Apêndice B: Trilha Epistêmica"] = "_Nenhum rótulo epistêmico encontrado nos artefatos._"

    # Rule C7: minimum completeness
    c7_failures = check_c7_completeness(sections)
    if c7_failures:
        print("\nWARNING — Verificação C7 (Completude Mínima) — FALHAS ENCONTRADAS:", file=sys.stderr)
        for f in c7_failures:
            print(f"  • {f}", file=sys.stderr)
        print("\nA-MASTER será produzido com avisos. Revise antes de avançar para Fase 6.\n", file=sys.stderr)

    # Rule C2: assemble document
    doc_lines = [f"# {client_name} — Dossiê Consultivo PRAXIS\n"]
    doc_lines.append(f"_Case ID: {case_id} | Gerado: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC_\n")

    for section_name, _ in SECTION_ORDER:
        content = sections.get(section_name, "")
        doc_lines.append(f"\n## {section_name}\n")
        if content.strip():
            doc_lines.append(content)
        else:
            doc_lines.append("_Conteúdo a ser preenchido._")

    # Internal track at end (Rule C6)
    doc_lines.append("\n\n---\n")
    doc_lines.append("<!-- [TRILHA_INTERNA] — uso exclusivo do consultor -->")
    internal_content = []
    for art_id in ["A-05", "A-06"]:
        if art_id in artifact_contents:
            internal_content.append(f"### {art_id} — Raciocínio Interno\n{artifact_contents[art_id]}")
    if internal_content:
        doc_lines.append("\n".join(internal_content))
    doc_lines.append("<!-- [/TRILHA_INTERNA] -->")

    master_content = "\n".join(doc_lines)

    # Write A-MASTER
    os.makedirs(args.output_dir, exist_ok=True)
    master_path = os.path.join(args.output_dir, f"master_{case_id}.md")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)

    master_hash = hashlib.sha256(master_content.encode()).hexdigest()

    # Write compilation_log.md (Rule C8)
    log_lines = [
        f"# Compilation Log — {case_id}",
        f"Generated: {datetime.datetime.utcnow().isoformat()}Z",
        "",
        "## Artefatos Incluídos",
        "| Artefato | Fase | Trilha | Status |",
        "|---|---|---|---|",
    ]
    for art_id, art_info in artifacts_produced.items():
        status = "incluído" if art_id in artifact_contents else "ausente"
        log_lines.append(
            f"| {art_id} | {art_info.get('phase', '?')} | "
            f"{art_info.get('trilha', '?')} | {status} |"
        )

    log_lines += ["", "## Decisões de Deduplicação",
                  "| Claim | Mantido em | Pulado de | Motivo |", "|---|---|---|---|"]
    for d in dedup_log:
        log_lines.append(f"| {d['claim'][:60]} | {d['kept_in']} | {d['skipped_from']} | {d['reason']} |")

    log_lines += ["", "## Checks C7 (Completude Mínima)",
                  "| Check | Status |", "|---|---|"]
    c7_checks = [
        "Seção 1 ≥ 3 campos",
        "Seção 3 tem causa raiz",
        "Seção 5 tem ação com responsável+prazo",
        "Pelo menos 1 [FATO] presente",
    ]
    for i, check in enumerate(c7_checks):
        status = "FAIL" if i < len(c7_failures) else "PASS"
        log_lines.append(f"| {check} | {status} |")

    log_path = os.path.join(args.output_dir, "compilation_log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print(f"A-MASTER compiled: {master_path}")
    print(f"SHA256: {master_hash}")
    print(f"Compilation log: {log_path}")
    if c7_failures:
        print(f"WARNING: {len(c7_failures)} C7 check(s) failed — review before Phase 6")
        sys.exit(1)
    else:
        print("All C7 checks passed.")


if __name__ == "__main__":
    main()

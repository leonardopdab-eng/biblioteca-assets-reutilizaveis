#!/usr/bin/env python3
"""
Usage: python validate_qa.py --manifest <path> [--artifacts-dir <dir>]
Runs all 20 Gate G4 QA checks. Exit 0 = all pass. Exit 1 = any fail.
"""
import yaml
import argparse
import datetime
import os
import re
import sys


REQUIRED_ARTIFACTS_BY_SCENARIO = {
    "A": ["A-01", "A-06", "A-MASTER", "A-FINAL", "A-OPS"],
    "B": ["A-01", "A-MASTER", "A-FINAL", "A-OPS"],
    "C": ["A-01", "A-02", "A-FINAL"],
}

INTERNAL_IDS = ["A-01", "A-02", "A-03", "A-04", "A-05", "A-06", "A-07", "A-08",
                "A-09", "A-10", "A-11", "A-12", "A-13", "A-MASTER", "A-MASTER-LINEAR",
                "G-I1", "G-I2", "G-I3", "G-I4", "G-I5", "G-I6",
                "G0", "G1", "G2", "G3", "G4", "G5", "G6",
                "Fase 1", "Phase 1", "TRILHA_INTERNA"]

AI_TERMS = ["Claude", "Anthropic", "inteligência artificial", "machine learning",
            "modelo de linguagem", "sistema de IA", "IA generativa", "LLM"]

MIN_WORDS_FINAL = 500
REQUIRED_SECTIONS = ["contextualiz", "diagnóstico", "plano de ação", "próximos passos"]
REQUIRED_XLSX_TABS = ["Resumo Executivo", "Diagnóstico", "Plano de Ação", "Simulação", "Próximos Passos"]

PT_BR_DEVIATIONS = ["utilizámos", "façamos", "estávamos a", "vos apresento"]

HARDCODED_HUMAN_GATES = {"G2", "G5", "G6"}


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_artifact_path(artifact_id: str, artifacts: list, artifacts_dir: str) -> str | None:
    for art in artifacts:
        if art.get("artifact_id") == artifact_id:
            path = art.get("path", "")
            if os.path.exists(path):
                return path
            # Try artifacts_dir
            basename = os.path.basename(path) if path else f"{artifact_id}.md"
            candidate = os.path.join(artifacts_dir, basename)
            if os.path.exists(candidate):
                return candidate
    return None


def read_file(path: str | None) -> str:
    if not path or not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def check_result(num: int, description: str, passed: bool, detail: str = "") -> dict:
    return {"num": num, "description": description, "passed": passed, "detail": detail}


def run_checks(manifest: dict, artifacts_dir: str) -> list:
    results = []
    artifacts_list = manifest.get("artifacts_produced", [])
    artifact_ids = {a.get("artifact_id") for a in artifacts_list}
    scenario = manifest.get("scenario_selected", "A") or "A"
    gates_passed_list = manifest.get("gates_passed", [])
    gates_passed = {g.get("gate"): g for g in gates_passed_list}
    branding = manifest.get("client_identity", {}).get("branding", {})

    # Helper to get artifact content
    def art_content(art_id: str) -> str:
        path = find_artifact_path(art_id, artifacts_list, artifacts_dir)
        return read_file(path)

    # ─── CATEGORY 1: Artifact Completeness ───────────────────────────────────

    # Check 1: A-01 present
    c1 = "A-01" in artifact_ids and bool(find_artifact_path("A-01", artifacts_list, artifacts_dir))
    results.append(check_result(1, "Artefato A-01 presente", c1,
                                "" if c1 else "A-01 não encontrado. Execute a Fase 1 completa."))

    # Check 2: Required artifacts for scenario
    required = REQUIRED_ARTIFACTS_BY_SCENARIO.get(scenario.upper(), REQUIRED_ARTIFACTS_BY_SCENARIO["A"])
    missing = [r for r in required if r not in artifact_ids]
    c2 = not missing
    results.append(check_result(2, f"Artefatos do cenário {scenario} presentes", c2,
                                "" if c2 else f"Artefatos faltantes: {', '.join(missing)}"))

    # Check 3: A-FINAL not empty
    final_content = art_content("A-FINAL")
    word_count = len(final_content.split()) if final_content else 0
    c3 = word_count >= MIN_WORDS_FINAL
    results.append(check_result(3, "A-FINAL não está vazio (≥500 palavras)", c3,
                                "" if c3 else f"A-FINAL tem {word_count} palavras (mínimo: {MIN_WORDS_FINAL})."))

    # Check 4: A-OPS has required tabs (check .md spec if .xlsx not available)
    ops_path = find_artifact_path("A-OPS", artifacts_list, artifacts_dir)
    if ops_path and ops_path.endswith(".xlsx"):
        try:
            import openpyxl
            wb = openpyxl.load_workbook(ops_path)
            existing_tabs = wb.sheetnames
            missing_tabs = [t for t in REQUIRED_XLSX_TABS if t not in existing_tabs]
            c4 = not missing_tabs
            detail4 = "" if c4 else f"Abas faltantes: {', '.join(missing_tabs)}"
        except Exception as e:
            c4 = False
            detail4 = f"Erro ao abrir A-OPS.xlsx: {e}"
    elif ops_path:
        # Check markdown version
        ops_content = read_file(ops_path)
        missing_tabs = [t for t in REQUIRED_XLSX_TABS if t.lower() not in ops_content.lower()]
        c4 = not missing_tabs
        detail4 = "" if c4 else f"Abas faltantes em A-OPS: {', '.join(missing_tabs)}"
    else:
        c4 = False
        detail4 = "A-OPS não encontrado."
    results.append(check_result(4, "A-OPS tem todas as 5 abas obrigatórias", c4, detail4))

    # Check 5: compilation_log.md present
    master_path = find_artifact_path("A-MASTER", artifacts_list, artifacts_dir)
    log_path = None
    if master_path:
        log_candidate = os.path.join(os.path.dirname(master_path), "compilation_log.md")
        if os.path.exists(log_candidate):
            log_path = log_candidate
    c5 = bool(log_path)
    results.append(check_result(5, "compilation_log.md presente ao lado de A-MASTER", c5,
                                "" if c5 else "compilation_log.md ausente. Execute Fase 5 com subroutine."))

    # ─── CATEGORY 2: Epistemic Integrity ─────────────────────────────────────

    master_content = art_content("A-MASTER")

    # Check 6: No unlabeled analytical claims in A-MASTER
    # Heuristic: paragraphs with assertive language but no epistemic label
    unlabeled_lines = []
    if master_content:
        label_pattern = re.compile(r"\[FATO\]|\[INFERÊNCIA\]|\[HIPÓTESE\]")
        assertive_pattern = re.compile(r"^(O|A|Os|As)\s+.+(é|são|indica|revela|mostra|aponta)", re.IGNORECASE)
        for line in master_content.split("\n"):
            stripped = line.strip()
            if assertive_pattern.match(stripped) and not label_pattern.search(stripped):
                unlabeled_lines.append(stripped[:80])
    c6 = len(unlabeled_lines) == 0
    results.append(check_result(6, "Nenhuma afirmação assertiva sem rótulo em A-MASTER", c6,
                                "" if c6 else f"Possíveis afirmações sem rótulo: {unlabeled_lines[:2]}"))

    # Check 7: HIPÓTESE not presented as FATO in A-FINAL
    # If a line in A-FINAL has content from A-MASTER [HIPÓTESE] without labeling
    c7 = "[TRILHA_INTERNA]" not in final_content and "HIPOTESE" not in final_content.replace("[HIPÓTESE]", "")
    results.append(check_result(7, "[HIPÓTESE] não apresentada como fato em A-FINAL", c7,
                                "" if c7 else "Possível hipótese não rotulada em A-FINAL. Revisar trilha epistêmica."))

    # Check 8: Apêndice B present in A-MASTER
    c8 = "Apêndice B" in master_content or "Trilha Epistêmica" in master_content
    results.append(check_result(8, "Apêndice B (Trilha Epistêmica) presente em A-MASTER", c8,
                                "" if c8 else "Apêndice B ausente. Adicione trilha epistêmica ao A-MASTER."))

    # Check 9: No [TRILHA_INTERNA] in A-FINAL
    c9 = "TRILHA_INTERNA" not in final_content
    results.append(check_result(9, "Sem [TRILHA_INTERNA] exposta em A-FINAL", c9,
                                "" if c9 else "Conteúdo de trilha interna detectado em A-FINAL. Remover."))

    # ─── CATEGORY 3: Branding Compliance ─────────────────────────────────────

    # Check 10: Consultant identity in client artifacts
    display_name = branding.get("consultant_display_name", "")
    company = branding.get("consultant_company", "")
    c10 = bool(display_name) and (display_name in final_content or company in final_content)
    results.append(check_result(10, "Identidade do consultor aplicada a A-FINAL", c10,
                                "" if c10 else f"Identidade não encontrada em A-FINAL. Verifique: '{display_name}', '{company}'."))

    # Check 11: No AI/Claude mentions in client artifacts
    found_ai = [t for t in AI_TERMS if t.lower() in final_content.lower()]
    c11 = not found_ai
    results.append(check_result(11, "Sem menção a IA/Claude em documentos do cliente", c11,
                                "" if c11 else f"Termos encontrados em A-FINAL: {found_ai}"))

    # Check 12: No internal IDs exposed in client artifacts
    found_ids = [id_ for id_ in INTERNAL_IDS if id_ in final_content]
    c12 = not found_ids
    results.append(check_result(12, "Sem IDs internos expostos em A-FINAL", c12,
                                "" if c12 else f"IDs internos encontrados: {found_ids[:5]}"))

    # ─── CATEGORY 4: Content Quality ─────────────────────────────────────────

    # Check 13: Required sections in A-FINAL
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in final_content.lower()]
    c13 = not missing_sections
    results.append(check_result(13, "Seções mínimas obrigatórias em A-FINAL", c13,
                                "" if c13 else f"Seções faltantes: {missing_sections}"))

    # Check 14: At least 1 root cause identified
    root_cause_terms = ["causa raiz", "causa principal", "causa-raiz", "problema central"]
    c14 = any(t in (master_content + final_content).lower() for t in root_cause_terms)
    results.append(check_result(14, "Pelo menos 1 causa raiz identificada no diagnóstico", c14,
                                "" if c14 else "Nenhuma causa raiz encontrada. Diagnóstico incompleto."))

    # Check 15: At least 1 action with owner and deadline
    has_responsible = "responsável" in (master_content + final_content).lower()
    has_deadline = "prazo" in (master_content + final_content).lower() or "deadline" in (master_content + final_content).lower()
    c15 = has_responsible and has_deadline
    results.append(check_result(15, "Plano de ação com responsável e prazo", c15,
                                "" if c15 else "Ação sem responsável ou prazo no plano de ação."))

    # Check 16: PT-BR register
    found_deviations = [d for d in PT_BR_DEVIATIONS if d in final_content.lower()]
    c16 = not found_deviations
    results.append(check_result(16, "Linguagem PT-BR adequada (sem desvios PT-Portugal)", c16,
                                "" if c16 else f"Desvios detectados: {found_deviations}"))

    # ─── CATEGORY 5: Gate Trail Integrity ────────────────────────────────────

    # Check 17: G0 and G1 before G2
    g0_time = gates_passed.get("G0", {}).get("timestamp", "")
    g1_time = gates_passed.get("G1", {}).get("timestamp", "")
    g2_time = gates_passed.get("G2", {}).get("timestamp", "")
    c17 = bool(g0_time) and bool(g1_time) and (not g2_time or (g0_time < g2_time and g1_time < g2_time))
    results.append(check_result(17, "G0 e G1 aprovados antes de G2", c17,
                                "" if c17 else "Ordem de gates inválida. G0 e G1 devem preceder G2."))

    # Check 18: G2 approved by human (not AUTO)
    g2_approver = gates_passed.get("G2", {}).get("approved_by", "")
    c18 = bool(g2_approver) and g2_approver.upper() != "AUTO"
    results.append(check_result(18, "G2 aprovado por humano (não AUTO)", c18,
                                "" if c18 else f"G2 aprovado por: '{g2_approver}'. Gate G2 exige revisão humana."))

    # Check 19: manifest.updated_at recent (< 24h)
    updated_at = manifest.get("updated_at", "")
    try:
        updated_dt = datetime.datetime.fromisoformat(updated_at.rstrip("Z"))
        age_hours = (datetime.datetime.utcnow() - updated_dt).total_seconds() / 3600
        c19 = age_hours < 24
        detail19 = "" if c19 else f"Manifest não atualizado há {age_hours:.1f}h (máximo: 24h)."
    except Exception:
        c19 = False
        detail19 = f"Não foi possível parsear updated_at: '{updated_at}'"
    results.append(check_result(19, "manifest.updated_at < 24h", c19, detail19))

    # Check 20: current_phase == 6
    current_phase = manifest.get("current_phase", 0)
    c20 = current_phase == 6
    results.append(check_result(20, "current_phase == 6 (caso na fase de entrega)", c20,
                                "" if c20 else f"Fase atual: {current_phase}. QA G4 só se aplica na Fase 6."))

    return results


def main():
    parser = argparse.ArgumentParser(description="Run Gate G4 QA checks for praxis")
    parser.add_argument("--manifest", default="manifest.yaml")
    parser.add_argument("--artifacts-dir", default=".", dest="artifacts_dir")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except FileNotFoundError:
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    case_id = manifest.get("case_id", "unknown")
    scenario = manifest.get("scenario_selected", "?")

    print("PRAXIS QA — Gate G4")
    print("═" * 55)
    print(f"Case ID:  {case_id}")
    print(f"Cenário:  {scenario}")
    print(f"Timestamp: {datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("═" * 55)

    results = run_checks(manifest, args.artifacts_dir)

    categories = {
        "CATEGORIA 1: Completude de Artefatos": range(1, 6),
        "CATEGORIA 2: Integridade Epistêmica": range(6, 10),
        "CATEGORIA 3: Conformidade de Branding": range(10, 13),
        "CATEGORIA 4: Qualidade de Conteúdo": range(13, 17),
        "CATEGORIA 5: Integridade da Trilha de Gates": range(17, 21),
    }

    for cat_name, check_range in categories.items():
        print(f"\n{cat_name}")
        for r in results:
            if r["num"] in check_range:
                status = "PASS" if r["passed"] else "FAIL"
                dots = "." * max(1, 48 - len(r["description"]))
                print(f"  [Check {r['num']:2d}] {r['description']}{dots}{status}")
                if not r["passed"] and r["detail"]:
                    print(f"           → {r['detail']}")

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    print("\n" + "═" * 55)
    print(f"Total de checks: {len(results)}")
    print(f"Passou:  {passed}")
    print(f"Falhou:  {failed}")

    if failed == 0:
        print("\nRESULTADO: PASS")
        print("Pronto para Gate G5 — revisão humana final.")
        print("═" * 55)
        sys.exit(0)
    else:
        print("\nRESULTADO: FAIL")
        print("\nProblemas a corrigir antes de avançar para Gate G5:")
        for r in results:
            if not r["passed"]:
                print(f"  {r['num']}. {r['detail'] or r['description']}")
        print("═" * 55)
        sys.exit(1)


if __name__ == "__main__":
    main()

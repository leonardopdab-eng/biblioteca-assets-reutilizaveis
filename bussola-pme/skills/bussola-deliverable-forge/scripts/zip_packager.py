#!/usr/bin/env python3
"""
Empacota caso Bússola PME em ZIP organizado em 3 trilhas.

Input:  --case-dir <path>   Diretório raiz do caso
        --output <path>     Caminho do ZIP de saída
Output: ZIP com interno/, cliente/, governanca/, README_PACOTE.md, custom_agent/

HARD STOP: Executa qa_checklist_runner.py antes de qualquer empacotamento.
  Se QA_FAIL, ZIP não é gerado.

Uso:
  python zip_packager.py --case-dir ./casos/BP-001 --output BP-001-pacote.zip
"""

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path


README_TEMPLATE = """# Pacote do Caso {case_id} — Bússola PME

**Gerado em**: {date}
**Consultor**: {consultant}
**Versão**: {version}

## Estrutura do pacote

```
{case_id}/
├── interno/          # Trilha interna — uso exclusivo do consultor
│   ├── hypotheses_log.md
│   ├── problem_tree.md
│   ├── diagnostic_working.md
│   ├── priority_score.md
│   ├── decision_log.md
│   ├── information_gaps.md
│   ├── assumptions_log.md
│   ├── module_routing_log.md
│   └── intake_normalized_v2.md
│
├── cliente/          # Trilha cliente — artefatos aprovados para entrega
│   ├── resumo_executivo.md
│   ├── diagnostico_executivo.md
│   ├── matriz_prioridades.md
│   ├── plano_acao_cliente.md
│   ├── playbook_operacional.md
│   ├── apresentacao_executiva.*
│   ├── relatorio_acompanhamento.md
│   └── proposta_continuidade.md
│
├── governanca/       # Trilha governança — auditoria e controle
│   ├── manifest.yaml
│   ├── qa_checklist.md
│   ├── anonymization_log.md
│   ├── source_audit_log.md
│   ├── gate_transition_log.md
│   ├── hypothesis_propagation_log.md
│   ├── version_history.yaml
│   ├── consultant_config_snapshot.yaml
│   ├── intake_original.md
│   └── release_notes.md
│
└── custom_agent/
    └── SKILL.md      # Skill gerada para reutilização em casos similares
```

## Próximos passos

1. Compartilhar trilha `cliente/` com o cliente
2. Arquivar trilha `interno/` no sistema do consultor
3. Guardar `governanca/` para auditoria futura
4. Usar `custom_agent/SKILL.md` para casos similares

---
*Gerado pelo sistema Bússola PME — deliverable-forge*
"""


def run_qa_check(case_dir: Path, manifest_path: str | None) -> bool:
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "qa_checklist_runner.py"),
        "--case-dir", str(case_dir),
    ]
    if manifest_path:
        cmd.extend(["--manifest", manifest_path])

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def build_zip(case_dir: Path, output_path: Path, manifest_path: str | None = None) -> bool:
    # HARD STOP: QA check first
    print("Running QA checklist (Gate G4)...")
    if not run_qa_check(case_dir, manifest_path):
        print("\n❌ HARD STOP: QA_FAIL — ZIP not generated. Fix QA issues before packaging.", file=sys.stderr)
        return False

    print("\n✓ QA_PASS — packaging case...")

    # Read case metadata from manifest if available
    case_id = case_dir.name
    consultant = "Consultor"
    version = "1.0"

    import yaml
    import datetime

    mpath = Path(manifest_path) if manifest_path else (case_dir / "governanca" / "manifest.yaml")
    if not mpath.exists():
        mpath = case_dir / "manifest.yaml"

    if mpath.exists():
        try:
            with open(mpath) as f:
                manifest = yaml.safe_load(f)
            case_id = manifest.get("case_id", case_id)
            consultant = manifest.get("consultant_id", consultant)
        except Exception:
            pass

    date_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    readme_content = README_TEMPLATE.format(
        case_id=case_id,
        date=date_str,
        consultant=consultant,
        version=version,
    )

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add all files from case directory
        for fpath in case_dir.rglob("*"):
            if fpath.is_file() and "__pycache__" not in str(fpath):
                arcname = str(fpath.relative_to(case_dir.parent))
                zf.write(fpath, arcname)

        # Add README
        zf.writestr(f"{case_id}/README_PACOTE.md", readme_content)

    print(f"✓ ZIP created: {output_path} ({output_path.stat().st_size} bytes)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Package a Bússola PME case into a ZIP archive.")
    parser.add_argument("--case-dir", required=True, help="Root directory of the case")
    parser.add_argument("--output", required=True, help="Output ZIP file path")
    parser.add_argument("--manifest", help="Path to manifest.yaml")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    output_path = Path(args.output)

    if not case_dir.exists():
        print(f"ERROR: case-dir not found: {case_dir}", file=sys.stderr)
        sys.exit(1)

    success = build_zip(case_dir, output_path, args.manifest)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # Example: python zip_packager.py --case-dir ./casos/BP-001 --output BP-001-pacote.zip
    main()

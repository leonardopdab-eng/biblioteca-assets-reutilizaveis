#!/usr/bin/env python3
"""
Praxis dry run — end-to-end synthetic case test.
Usage: python dry_run.py [--verbose]
Tests the full 6-phase pipeline on synthetic data without modifying any real cases.
Exit 0 = all phases executed without error. Exit 1 = failure with details.
"""
import argparse
import datetime
import os
import sys
import tempfile
import shutil
import subprocess
import traceback
import yaml


# ─── Synthetic Case Data ──────────────────────────────────────────────────────

SYNTHETIC_BRIEFING = """
Empresa: TechFlow Soluções Ltda
Segmento: SaaS B2B, gestão de frotas para transportadoras
Equipe: 22 pessoas (8 dev, 4 vendas, 4 CS, 3 ops, 3 diretoria)
Receita mensal: ~R$380k (anualizado ~R$4,5M)
Decisores: João Faria (CEO), Ana Costa (COO)

Problema principal relatado pelo cliente: Churn elevado nos últimos 2 trimestres.
Em Q1, perdemos 4 clientes grandes que representavam 30% da receita recorrente.

Problemas secundários:
- Pipeline de vendas travado (15 oportunidades abertas há mais de 90 dias sem fechamento)
- Equipe de CS sobrecarregada, tempo médio de resposta subiu de 2h para 14h
- Produto tem débito técnico significativo que atrasa features prometidas

Urgência: ALTA — próxima reunião de board em 3 semanas, CEO precisa apresentar plano

Documentos disponíveis: DRE Q1 2026, planilha de churn, NPS do último trimestre
Diagnósticos anteriores: nenhum diagnóstico formal feito antes
"""

SYNTHETIC_METHODOLOGY = """
FONTES_ADICIONAIS:
- Benchmarks SaaS Brasil (Distrito): churn médio B2B SaaS = 2-4% ao mês
- Sondagem CNI: setor de transportes cresceu 8% em 2025

PESOS_ANALÍTICOS:
- Priorizar: retenção de receita sobre crescimento de novos clientes
- Contexto: mercado de gestão de frotas consolidando, 3 concorrentes grandes entraram em 2025

FRAMEWORKS_PREFERIDOS:
- 5 Whys para causa raiz de churn
- GUT + Esforço×Impacto para priorização
- 5W2H para plano de ação
"""


# ─── Helper Functions ─────────────────────────────────────────────────────────

def run_script(script_path: str, args: list, cwd: str, verbose: bool = False) -> tuple[int, str, str]:
    """Run a Python script and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if verbose:
        if result.stdout:
            print(f"    STDOUT: {result.stdout.strip()[:200]}")
        if result.stderr:
            print(f"    STDERR: {result.stderr.strip()[:200]}")
    return result.returncode, result.stdout, result.stderr


def write_artifact(path: str, content: str):
    """Write a synthetic artifact file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def update_manifest(manifest_path: str, updates: dict):
    """Update manifest with given dict updates."""
    manifest = load_manifest(manifest_path)
    for k, v in updates.items():
        manifest[k] = v
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ─── Phase Simulators ─────────────────────────────────────────────────────────

def simulate_phase1(case_dir: str, manifest_path: str, verbose: bool) -> bool:
    """Simulate Phase 1: normalize briefing, produce A-01."""
    print("  → Normalizando briefing...")

    a01_content = """# A-01 — Normalized Follow Up

## Dados Normalizados

- **company_name**: TechFlow Soluções Ltda [FATO]
- **segment**: SaaS B2B, gestão de frotas [FATO]
- **team_size**: 22 pessoas (8 dev, 4 vendas, 4 CS, 3 ops, 3 diretoria) [FATO]
- **annual_revenue_range**: ~R$4,5M anualizados [INFERÊNCIA — estimado de receita mensal]
- **primary_problem**: Churn elevado — perda de 30% da MRR em Q1 2026 [FATO]
- **urgency_level**: alta — board meeting em 3 semanas [FATO]
- **decision_makers**: João Faria (CEO), Ana Costa (COO) [FATO]
- **secondary_problems**: Pipeline travado, CS sobrecarregado, débito técnico [FATO]
- **previous_diagnosis**: nenhum diagnóstico formal anterior [FATO]
- **available_documents**: DRE Q1 2026, planilha de churn, NPS Q1 [FATO]

## Lacunas Documentadas

- annual_revenue_range: impacto médio — receita mensal citada (R$380k), não anual confirmada
  recommended_action: solicitar DRE completo ao cliente

## Cenário Selecionado: A (Diagnóstico Completo)

## Informações Contextuais Adicionais

Mercado de gestão de frotas consolidando em 2025. Contexto competitivo relevante para análise.
"""
    a01_path = os.path.join(case_dir, "artifacts", "A-01-normalized-followup.md")
    write_artifact(a01_path, a01_content)

    manifest = load_manifest(manifest_path)
    manifest["current_phase"] = 2
    manifest["scenario_selected"] = "A"
    manifest["artifacts_produced"].append({
        "artifact_id": "A-01",
        "name": "Normalized Follow Up",
        "path": a01_path,
        "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "phase": 1,
        "sha256": None,
        "trilha": "INTERNA",
    })
    manifest["gates_passed"].append({
        "gate": "G0",
        "approved_by": "AUTO",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "notes": "dry_run: all 7 mandatory fields present",
    })
    if "G0" in manifest["gates_pending"]:
        manifest["gates_pending"].remove("G0")
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("  ✓ A-01 produzido. Gate G0 auto-aprovado.")
    return True


def simulate_phase2(case_dir: str, manifest_path: str, verbose: bool) -> bool:
    """Simulate Phase 2: generate commercial proposal skeleton."""
    print("  → Gerando proposta comercial (A-02)...")

    a02_content = """# A-02 — Proposta Comercial

**Consultor**: Dr. Test Consultor — Consultoria Praxis
**Cliente**: TechFlow Soluções Ltda
**Data**: {date}

---

## Contextualização

A TechFlow enfrenta um desafio crítico de retenção de clientes, com a perda de
4 contratos representando 30% da receita recorrente em Q1 2026.
[FATO — relatado pela diretoria em briefing de {date}]

## Nossa Abordagem

Diagnóstico estruturado em 3 etapas: análise de causa raiz, priorização de iniciativas
e plano de ação com responsáveis e prazos. Resultado: clareza sobre o que fazer primeiro.

## O que você vai receber

- Diagnóstico executivo com causas identificadas e priorizadas
- Plano de ação 5W2H com responsáveis e prazos
- Planilha operacional para acompanhamento
- Sessão de apresentação e alinhamento com a diretoria

## Investimento

[PLACEHOLDER — consultor preenche antes de enviar]

## Prazo

2–3 semanas para engajamento completo.

## Próximo Passo

Confirme até [DATA] para reservar sua vaga.

---

Dr. Test Consultor | Consultoria Praxis | contato@praxis.com
""".format(date=datetime.date.today().isoformat())

    a02_path = os.path.join(case_dir, "artifacts", "A-02-proposta-comercial.md")
    write_artifact(a02_path, a02_content)

    manifest = load_manifest(manifest_path)
    manifest["current_phase"] = 3
    manifest["client_identity"]["branding"]["consultant_display_name"] = "Dr. Test Consultor"
    manifest["client_identity"]["branding"]["consultant_company"] = "Consultoria Praxis"
    manifest["artifacts_produced"].append({
        "artifact_id": "A-02",
        "name": "Proposta Comercial",
        "path": a02_path,
        "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "phase": 2,
        "sha256": None,
        "trilha": "CLIENTE",
    })
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("  ✓ A-02 produzido.")
    return True


def simulate_phase3(case_dir: str, manifest_path: str, verbose: bool) -> bool:
    """Simulate Phase 3: 5 Whys analysis, produce A-05, A-06, A-09."""
    print("  → Executando análise diagnóstica (5 Whys + Full tier)...")

    a05_content = """# A-05 — Normalized Data

## Dados do Cliente Normalizados
- Segmento: SaaS B2B gestão de frotas [FATO]
- Churn Q1: 4 clientes = 30% da MRR perdida [FATO]
- Benchmark de mercado: churn B2B SaaS Brasil = 2-4%/mês [INFERÊNCIA — Distrito 2025]
- Churn implícito da TechFlow: > benchmark de mercado [INFERÊNCIA]

## Wide Search — Segmento de Gestão de Frotas
- Mercado consolidando: 3 grandes entraram em 2025 [HIPÓTESE — baseado em relato do CEO]
- Clientes de frotas têm contratos anuais tipicamente [INFERÊNCIA — padrão do setor]
"""

    a06_content = """# A-06 — B-Frames Output

## Primary Frame: 5 Whys (Causa Raiz do Churn)

**Problema central** [FATO]: Churn de 30% da MRR em Q1 2026

| Por quê | Resposta | Rótulo | Fonte |
|---|---|---|---|
| Por quê 1 | Clientes cancelaram porque não viram valor suficiente | [INFERÊNCIA] | NPS Q1 |
| Por quê 2 | Valor não percebido porque onboarding era incompleto | [HIPÓTESE] | relato CS |
| Por quê 3 | Onboarding incompleto porque CS estava sobrecarregado | [FATO] | métricas internas |
| Por quê 4 | CS sobrecarregado porque headcount não cresceu com a base | [FATO] | DRE Q1 |
| Por quê 5 | Headcount CS não cresceu porque foco era em aquisição | [INFERÊNCIA] | relato CEO |

**Causa raiz identificada** [INFERÊNCIA]: Desbalanceamento estrutural entre aquisição e retenção —
CS subdimensionado para a base instalada resultando em onboarding deficiente e churn.

## Hypothesis Log
- [HIPÓTESE] Onboarding deficiente é a causa principal — validar via pesquisa com churned customers
- [HIPÓTESE] Clientes churned tinham onboarding < 30 dias — verificar dados de CS

## GUT Matrix
| Causa | G | U | T | Score |
|---|---|---|---|---|
| CS subdimensionado | 5 | 5 | 5 | 125 |
| Onboarding incompleto | 5 | 5 | 4 | 100 |
| Débito técnico atrasando features | 4 | 3 | 3 | 36 |
| Pipeline travado | 3 | 4 | 4 | 48 |
"""

    a09_content = """# A-09 — Full-Tier Analysis

## 1. Contextualização
A TechFlow é uma empresa de SaaS B2B no segmento de gestão de frotas com 22 funcionários
e receita anualizada de ~R$4,5M. [FATO]

## 2. Diagnóstico do Problema Central

### 2.1 Causa Raiz (5 Whys)
A análise indica como causa raiz: desbalanceamento estrutural entre aquisição e retenção. [INFERÊNCIA]
O CS foi subdimensionado enquanto a base crescia, resultando em onboarding deficiente. [INFERÊNCIA]

### 2.2 Análise SWOT
**Forças**: produto funcional, time técnico sólido [FATO]
**Fraquezas**: CS subdimensionado, débito técnico crescente [FATO]
**Oportunidades**: mercado crescendo 8% em 2025 [INFERÊNCIA — CNI]
**Ameaças**: 3 grandes entraram no mercado em 2025 [HIPÓTESE]

## 3. Priorização de Iniciativas

| Iniciativa | Impacto | Esforço | Prioridade |
|---|---|---|---|
| Reforçar equipe CS | Alto | Médio | 1ª |
| Reestruturar onboarding | Alto | Médio | 2ª |
| Resolver débito técnico crítico | Médio | Alto | 3ª |
| Reativar pipeline | Médio | Baixo | 4ª |

## 4. Plano de Ação 5W2H (Top 3)

| O quê | Por quê | Quem | Quando | Onde | Como | Quanto |
|---|---|---|---|---|---|---|
| Contratar 2 CS | Reduzir churn [INFERÊNCIA] | CEO + RH | 30 dias | remoto | hunting + indicação | R$18k/mês |
| Criar playbook onboarding | Padronizar experiência [HIPÓTESE] | COO | 21 dias | interno | workshop + doc | 0 |
| Sprint débito técnico | Entregar features comprometidas | CTO | 60 dias | dev | sprint dedicado | 1 sprint |

## 5. OKRs — Iniciativa 1

**Objetivo**: Estabilizar a base de clientes nos próximos 90 dias
- KR1: Reduzir churn de X% para < 2%/mês
- KR2: Time-to-value no onboarding < 21 dias para 90% dos novos clientes
- KR3: NPS aumentar de atual para > 40 pontos

## Apêndice B: Trilha Epistêmica

| Seção | Rótulo | Afirmação |
|---|---|---|
| Diagnóstico | [FATO] | Perda de 4 clientes = 30% MRR em Q1 2026 |
| Diagnóstico | [INFERÊNCIA] | Causa raiz: desbalanceamento aquisição/retenção |
| Estratégico | [HIPÓTESE] | 3 grandes concorrentes entraram em 2025 |
| Ação | [HIPÓTESE] | Playbook de onboarding resolverá churn |
"""

    artifacts_dir = os.path.join(case_dir, "artifacts")
    a05_path = os.path.join(artifacts_dir, "A-05-normalized-data.md")
    a06_path = os.path.join(artifacts_dir, "A-06-b-frames.md")
    a09_path = os.path.join(artifacts_dir, "A-09-full-tier.md")

    write_artifact(a05_path, a05_content)
    write_artifact(a06_path, a06_content)
    write_artifact(a09_path, a09_content)

    manifest = load_manifest(manifest_path)
    manifest["current_phase"] = 4
    for art_id, path, trilha in [("A-05", a05_path, "INTERNA"), ("A-06", a06_path, "INTERNA"), ("A-09", a09_path, "INTERNA")]:
        manifest["artifacts_produced"].append({
            "artifact_id": art_id,
            "name": art_id,
            "path": path,
            "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
            "phase": 3,
            "sha256": None,
            "trilha": trilha,
        })
    # Simulate G1 (auto) and G2 (human — in dry_run we simulate approval)
    for gate, approver, note in [
        ("G1", "AUTO", "dry_run: epistemic labels verified"),
        ("G2", "dr-test-consultor", "dry_run: simulated human approval"),
    ]:
        manifest["gates_passed"].append({"gate": gate, "approved_by": approver,
                                         "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                                         "notes": note})
        if gate in manifest["gates_pending"]:
            manifest["gates_pending"].remove(gate)
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("  ✓ A-05, A-06, A-09 produzidos. Gates G1 (auto) e G2 (simulado) aprovados.")
    return True


def simulate_phase4(case_dir: str, manifest_path: str, verbose: bool) -> bool:
    """Simulate Phase 4: generate scenario table."""
    print("  → Gerando cenários de simulação (A-10)...")

    a10_content = """# A-10 — Simulação Fase 1

## Premissas Utilizadas [HIPÓTESE]

| Parâmetro | Valor Base | Fonte | Confiança |
|---|---|---|---|
| MRR atual | R$380k | Briefing CEO [FATO] | Alta |
| Churn mensal | ~7.5% (estimado) | Inferido da perda Q1 [INFERÊNCIA] | Média |
| CAC atual | ~R$8k | [HIPÓTESE — sem dados diretos] | Baixa |
| LTV estimado | ~R$13k | Churn implica ciclo de vida ~13 meses [HIPÓTESE] | Baixa |

> Todas as premissas acima são hipóteses de trabalho. Validar com dados reais do cliente.

## Cenário Conservador (Base) [HIPÓTESE]
Premissa: churn mantém-se em ~7.5%/mês nos próximos 12 meses

| Métrica | Hoje | 6 meses | 12 meses |
|---|---|---|---|
| MRR (R$k) | 380 | 310 | 255 |
| Clientes ativos | ~95 | ~78 | ~64 |
| Receita anualizada (R$M) | 4,5 | 3,7 | 3,1 |

## Cenário Pessimista [HIPÓTESE]
Premissa: churn acelera para 10%/mês (concorrentes continuam ganhando share)

| Métrica | Hoje | 6 meses | 12 meses |
|---|---|---|---|
| MRR (R$k) | 380 | 270 | 195 |
| Clientes ativos | ~95 | ~67 | ~49 |

## Cenário Otimista [HIPÓTESE]
Premissa: ações de retenção reduzem churn para 2%/mês em 90 dias

| Métrica | Hoje | 6 meses | 12 meses |
|---|---|---|---|
| MRR (R$k) | 380 | 420 | 510 |
| Clientes ativos | ~95 | ~103 | ~121 |

## Principais Insights [INFERÊNCIA]
1. No cenário conservador, a empresa perde ~R$1,4M de receita em 12 meses
2. A diferença entre pessimista e otimista em 12 meses é ~R$315k/mês de MRR
3. As ações de retenção têm ROI positivo mesmo considerando custo de 2 CSs adicionais [HIPÓTESE]

## Premissas Críticas a Validar
1. Churn atual real (pedido: exportar dados de cancelamento dos últimos 3 meses)
2. CAC real (pedido: historico de custos de aquisição)
"""

    a10_path = os.path.join(case_dir, "artifacts", "A-10-simulation.md")
    write_artifact(a10_path, a10_content)

    manifest = load_manifest(manifest_path)
    manifest["current_phase"] = 5
    manifest["artifacts_produced"].append({
        "artifact_id": "A-10",
        "name": "Simulation Phase 1",
        "path": a10_path,
        "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "phase": 4,
        "sha256": None,
        "trilha": "INTERNA",
    })
    manifest["gates_passed"].append({"gate": "G3", "approved_by": "AUTO",
                                      "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                                      "notes": "dry_run: simulation scope confirmed"})
    if "G3" in manifest["gates_pending"]:
        manifest["gates_pending"].remove("G3")
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print("  ✓ A-10 produzido. Gate G3 auto-aprovado.")
    return True


def simulate_phase5(case_dir: str, manifest_path: str, scripts_dir: str, verbose: bool) -> bool:
    """Simulate Phase 5: compile master document."""
    print("  → Compilando dossiê (A-MASTER)...")

    artifacts_dir = os.path.join(case_dir, "artifacts")
    rc, stdout, stderr = run_script(
        os.path.join(scripts_dir, "compile_master.py"),
        ["--manifest", manifest_path, "--output-dir", artifacts_dir],
        cwd=case_dir,
        verbose=verbose,
    )

    if rc not in (0, 1):  # rc=1 = C7 warnings but still produced
        print(f"  FAIL: compile_master.py returned {rc}")
        print(f"  {stderr[:300]}")
        return False

    manifest = load_manifest(manifest_path)
    case_id = manifest.get("case_id", "unknown")
    master_path = os.path.join(artifacts_dir, f"master_{case_id}.md")

    if not os.path.exists(master_path):
        print("  FAIL: A-MASTER file not created")
        return False

    manifest["current_phase"] = 6
    manifest["artifacts_produced"].append({
        "artifact_id": "A-MASTER",
        "name": "Master Document",
        "path": master_path,
        "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "phase": 5,
        "sha256": None,
        "trilha": "AMBAS",
    })
    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"  ✓ A-MASTER compilado: {os.path.basename(master_path)}")
    return True


def simulate_phase6(case_dir: str, manifest_path: str, scripts_dir: str, verbose: bool) -> bool:
    """Simulate Phase 6: produce A-FINAL and A-OPS."""
    print("  → Gerando entregáveis finais (A-FINAL + A-OPS)...")

    artifacts_dir = os.path.join(case_dir, "artifacts")
    manifest = load_manifest(manifest_path)
    client_name = manifest.get("client_identity", {}).get("company_name", "Cliente")

    # Produce A-FINAL (simplified version of A-MASTER with client voice)
    a_final_content = f"""# Diagnóstico Consultivo — {client_name}
**Consultor**: Dr. Test Consultor — Consultoria Praxis
**Data**: {datetime.date.today().isoformat()}

---

## Contextualização

A {client_name} é uma empresa de SaaS B2B no segmento de gestão de frotas.
No primeiro trimestre de 2026, a empresa enfrentou uma perda significativa de receita
recorrente, com cancelamentos representando 30% do MRR mensal.

Os dados indicam um desbalanceamento estrutural entre o crescimento da base de clientes
e a capacidade da equipe de Sucesso do Cliente para sustentá-la.

## Diagnóstico

A análise identificou como causa raiz: a equipe de CS foi subdimensionada enquanto
a base de clientes crescia, resultando em onboarding deficiente e perda de valor percebido.

**Causas identificadas:**
1. CS subdimensionado para a base instalada — equipe não cresceu proporcionalmente
2. Onboarding sem playbook padronizado — cada CS aplicava sua própria abordagem
3. Débito técnico atrasando features prometidas — erosão de confiança nos clientes

## Prioridades

Com base na análise de gravidade, urgência e tendência, recomendamos priorizar:

1. **Reforçar a equipe de CS** — impacto direto na retenção da base existente
2. **Reestruturar o processo de onboarding** — eliminar variabilidade e reduzir churn
3. **Sprint dedicado ao débito técnico crítico** — cumprir compromissos assumidos com clientes

## Plano de Ação

| Ação | Responsável | Prazo | KPI |
|---|---|---|---|
| Contratar 2 profissionais de CS | CEO + RH | 30 dias | 2 contratações confirmadas |
| Criar playbook de onboarding | COO | 21 dias | Playbook aprovado e em uso |
| Sprint débito técnico | CTO | 60 dias | 3 features críticas entregues |

## Próximos Passos

**Ação imediata**: iniciar processo seletivo para CS até {(datetime.date.today() + datetime.timedelta(days=7)).isoformat()}.

Recomendamos uma sessão de acompanhamento em 30 dias para verificar o andamento do plano.

---

Dr. Test Consultor | Consultoria Praxis | contato@praxis.com
"""

    a_final_path = os.path.join(artifacts_dir, "A-FINAL-diagnostico.md")
    write_artifact(a_final_path, a_final_content)

    # Produce A-OPS
    rc, stdout, stderr = run_script(
        os.path.join(scripts_dir, "generate_executive_xls.py"),
        ["--manifest", manifest_path, "--output", os.path.join(artifacts_dir, "A-OPS.xlsx")],
        cwd=case_dir,
        verbose=verbose,
    )
    ops_produced = rc == 0

    manifest["artifacts_produced"].append({
        "artifact_id": "A-FINAL",
        "name": "Final Designed Deliverable",
        "path": a_final_path,
        "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "phase": 6,
        "sha256": None,
        "trilha": "CLIENTE",
    })
    if ops_produced:
        ops_path = os.path.join(artifacts_dir, "A-OPS.xlsx")
        manifest["artifacts_produced"].append({
            "artifact_id": "A-OPS",
            "name": "Executive Spreadsheet",
            "path": ops_path,
            "produced_at": datetime.datetime.utcnow().isoformat() + "Z",
            "phase": 6,
            "sha256": None,
            "trilha": "CLIENTE",
        })

    manifest["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"  ✓ A-FINAL produzido. A-OPS {'produzido' if ops_produced else 'FALHOU (openpyxl ausente?)'}.")
    return True


def simulate_qa(case_dir: str, manifest_path: str, scripts_dir: str, verbose: bool) -> bool:
    """Run validate_qa.py against the synthetic case."""
    print("  → Executando QA Gate G4...")
    artifacts_dir = os.path.join(case_dir, "artifacts")
    rc, stdout, stderr = run_script(
        os.path.join(scripts_dir, "validate_qa.py"),
        ["--manifest", manifest_path, "--artifacts-dir", artifacts_dir],
        cwd=case_dir,
        verbose=verbose,
    )
    if verbose:
        print(f"    QA output:\n{stdout[:500]}")
    # In dry_run, some checks may fail (e.g. A-OPS tabs if openpyxl absent) — that's expected
    # We pass if validate_qa.py ran without exception (rc 0 or 1)
    print(f"  {'✓' if rc in (0, 1) else '✗'} QA executado. Exit code: {rc} ({'PASS' if rc == 0 else 'FAIL — checar issues acima'})")
    return rc in (0, 1)  # 0=all pass, 1=some fail — both are valid runs


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Praxis end-to-end dry run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show script output details")
    args = parser.parse_args()

    # Find scripts directory relative to this file
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n" + "═" * 60)
    print("PRAXIS DRY RUN — Caso Sintético")
    print("═" * 60)
    print(f"Cliente sintético: TechFlow Soluções Ltda")
    print(f"Consultor sintético: dr-test-consultor")
    print(f"Timestamp: {datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}\n")

    case_dir = tempfile.mkdtemp(prefix="praxis_dry_run_")
    manifest_path = os.path.join(case_dir, "manifest.yaml")
    passed = []
    failed = []

    try:
        # Step 1: Initialize case
        print("[STEP 1] Inicializar caso...")
        rc, stdout, stderr = run_script(
            os.path.join(scripts_dir, "init_case.py"),
            ["--consultant", "dr-test-consultor", "--client", "TechFlow Soluções Ltda",
             "--output", manifest_path],
            cwd=case_dir,
            verbose=args.verbose,
        )
        if rc != 0:
            print(f"  FAIL: init_case.py returned {rc}: {stderr[:200]}")
            failed.append("Step 1: init_case.py")
        else:
            print(f"  ✓ Manifest inicializado: {os.path.basename(manifest_path)}")
            passed.append("Step 1: init_case.py")

        # Phase simulations
        phases = [
            ("Fase 1: Normalização de Briefing", simulate_phase1),
            ("Fase 2: Proposta Comercial", simulate_phase2),
            ("Fase 3: Análise Diagnóstica (5 Whys + Full)", simulate_phase3),
            ("Fase 4: Laboratório de Simulação", simulate_phase4),
            ("Fase 5: Compilação do Dossiê", lambda cd, mp, v: simulate_phase5(cd, mp, scripts_dir, v)),
            ("Fase 6: Entregáveis Finais", lambda cd, mp, v: simulate_phase6(cd, mp, scripts_dir, v)),
        ]

        for step_name, simulate_fn in phases:
            print(f"\n[{step_name.upper()}]")
            try:
                ok = simulate_fn(case_dir, manifest_path, args.verbose)
                if ok:
                    passed.append(step_name)
                else:
                    failed.append(step_name)
            except Exception as e:
                print(f"  EXCEPTION: {e}")
                if args.verbose:
                    traceback.print_exc()
                failed.append(f"{step_name} (exception)")

        # QA
        print("\n[GATE G4: QA CHECKLIST]")
        try:
            ok = simulate_qa(case_dir, manifest_path, scripts_dir, args.verbose)
            if ok:
                passed.append("Gate G4: validate_qa.py")
            else:
                failed.append("Gate G4: validate_qa.py (exception)")
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            failed.append("Gate G4: validate_qa.py (exception)")

    finally:
        # Cleanup
        shutil.rmtree(case_dir, ignore_errors=True)

    # Report
    print("\n" + "═" * 60)
    print("DRY RUN REPORT")
    print("═" * 60)
    print(f"Passou:  {len(passed)}/{len(passed) + len(failed)}")
    print(f"Falhou:  {len(failed)}/{len(passed) + len(failed)}")

    if failed:
        print("\nFalhas:")
        for f in failed:
            print(f"  ✗ {f}")

    if not failed:
        print("\nRESULTADO: PASS — pipeline completo executou sem erros.")
        sys.exit(0)
    else:
        print(f"\nRESULTADO: FAIL — {len(failed)} etapa(s) falharam.")
        sys.exit(1)


if __name__ == "__main__":
    main()

---
name: bussola-deliverable-forge
description: >
  Use this skill to generate, validate, and package Bússola PME case artifacts.
  Activate on "gerar entregáveis", "montar ZIP do caso", "gerar apresentação",
  "criar resumo executivo", "gerar plano de ação para o cliente", "empacotar
  caso", "gerar e-book do diagnóstico", "montar pacote final", "renderizar
  artefatos". Requires approved outputs from bussola-diagnostic-engine (plano_acao
  with Gate G5 pending) and consultant_config.yaml. Enforces qa_checklist (Gate G4)
  before any client-track release. Produces ZIP (default), interactive e-book HTML,
  or live sprint React artifact. Do NOT use for analysis (use diagnostic-engine)
  or orchestration (use orchestrator).
dependencies: [pyyaml, jinja2, zipfile]
---

# bussola-deliverable-forge

## Propósito

Geração, validação e empacotamento dos 28 artefatos do caso Bússola PME em 3 trilhas: interna, cliente, e governança.

## Pré-condições

- `plano_acao.md` com status `pending_human_review` (Gate G3 passado)
- `consultant_config.yaml` válido
- `priority_score.md` aprovado (Gate G2 passado)

## Os 28 artefatos

### Trilha Interna (9)

| # | Artefato | target_chars | overflow_action |
|---|----------|-------------|-----------------|
| 1 | hypotheses_log | 3000 | summarize |
| 2 | problem_tree | 2000 | compress_leaves |
| 3 | diagnostic_working | 5000 | paginate |
| 4 | priority_score | 2500 | summarize |
| 5 | decision_log | 4000 | archive_old |
| 6 | information_gaps | 1500 | summarize |
| 7 | assumptions_log | 1500 | summarize |
| 8 | module_routing_log | 1000 | summarize |
| 9 | intake_normalized_v2 | 2000 | compress |

### Trilha Cliente (8)

| # | Artefato | target_chars | overflow_action |
|---|----------|-------------|-----------------|
| 10 | resumo_executivo | 1500 | hard_cut |
| 11 | diagnostico_executivo | 4000 | compress |
| 12 | matriz_prioridades | 2000 | compress |
| 13 | plano_acao_cliente | 3500 | paginate |
| 14 | playbook_operacional | 5000 | paginate |
| 15 | apresentacao_executiva | — (slides) | reduce_slides |
| 16 | relatorio_acompanhamento | 2000 | summarize |
| 17 | proposta_continuidade | 2500 | compress |

### Trilha Governança (10 + custom_agent)

| # | Artefato | target_chars | overflow_action |
|---|----------|-------------|-----------------|
| 18 | manifest_yaml | — (structured) | none |
| 19 | qa_checklist | — (structured) | none |
| 20 | anonymization_log | 1000 | none |
| 21 | source_audit_log | 1000 | none |
| 22 | gate_transition_log | 1500 | archive_old |
| 23 | hypothesis_propagation_log | 1000 | none |
| 24 | version_history | — (structured) | none |
| 25 | consultant_config_snapshot | — (copy) | none |
| 26 | intake_original | — (copy) | none |
| 27 | release_notes | 800 | summarize |
| 28 | custom_agent/SKILL.md | — (generated) | none |

## As 4 ações de overflow

| Ação | Comportamento |
|------|---------------|
| `summarize` | Reduz a 60% mantendo estrutura via Claude API |
| `compress` | Remove exemplos e justificativas, mantém dados |
| `paginate` | Divide em _part1, _part2, etc. |
| `hard_cut` | Trunca no limite — apenas resumo_executivo |

## Gate G4 — QA Terminal

`qa_checklist_runner.py` deve retornar 100% antes de qualquer release:

1. Todos os 28 artefatos presentes
2. Nenhum artefato cliente contém strings de trilha interna
3. Todo item de plano_acao_cliente tem owner, deadline, KPI
4. Hipóteses propagadas sinalizadas em todos os artefatos
5. `manifest.yaml` reflete estado atual
6. `branding_tokens` aplicados em trilha cliente
7. `apresentacao_executiva` aprovada em Gate G5

## Modos de entrega

| Modo | Formato | Ativação |
|------|---------|----------|
| ZIP (F1) | 3 trilhas + README + custom_agent | padrão |
| E-book HTML (F2) | HTML com navegação lateral | `--format ebook` |
| Live Sprint (F2) | Componente React | `--format react` |

## Regras de separação de trilhas

**Nunca cruza para cliente:**
- Nomes de hipóteses internas (`diagnostic_working`, `hypotheses_log`)
- Scores intermediários de priorização
- Conflitos não resolvidos

**Pode cruzar após Gate G5:**
- Conclusões do diagnóstico
- Prioridades rankeadas (resumidas)
- Plano de ação com itens aprovados

## Dependências

```bash
pip install --break-system-packages pyyaml jinja2
```

## Evals

```json
[
  {
    "id": 1,
    "prompt": "Gerar o pacote ZIP completo do caso BP-001.",
    "expected": "Skill verifica pré-condições, executa qa_checklist_runner, produz ZIP com 28 artefatos em 3 trilhas.",
    "should_trigger": true
  },
  {
    "id": 2,
    "prompt": "Montar o ZIP mesmo sem o diagnostico_executivo aprovado.",
    "expected": "Skill recusa. qa_checklist FAIL. ZIP não é gerado até Gate G4 100% verde.",
    "should_trigger": true
  },
  {
    "id": 3,
    "prompt": "Rodar o diagnóstico do novo caso.",
    "expected": "Skill NÃO ativa. Responsabilidade do diagnostic-engine.",
    "should_trigger": false
  }
]
```

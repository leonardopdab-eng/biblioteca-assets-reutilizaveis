---
name: bussola-orchestrator
description: >
  Use this skill to run or resume a Bússola PME consultative case end-to-end.
  Activate on "novo caso Bússola PME", "rodar atendimento completo", "iniciar
  consultoria PME", "avançar para fase N", "montar pacote final do caso",
  "retomar caso [id]", "qual o status do caso". This skill owns the case
  manifest.yaml, enforces QA gates G0–G6 and mandatory human-review checkpoints
  on THREE critical artifacts (diagnostico_executivo, apresentacao_executiva,
  proposta_continuidade), routes work to specialist skills (personalization,
  diagnostic-engine, deliverable-forge, simulation-lab, execution-bridge),
  and produces the final ZIP. Do NOT use for standalone method questions
  (use consultative-faq) or one-off artifact generation outside a case
  (use deliverable-forge directly).
compatibility:
  tools: [mcp__slack, mcp__google_drive, visualize:show_widget, create_file]
dependencies: [pyyaml, jinja2]
---

# bussola-orchestrator

## Propósito

Coordenação end-to-end de um caso Bússola PME. Mantém o manifest.yaml como fonte de verdade, enforce gates G0–G6, roteia para skills especialistas, e produz o ZIP final.

## As 9 Fases Operacionais

| Fase | Nome | Skill responsável | Gate de saída |
|------|------|------------------|---------------|
| 0 | Configuração consultor | personalization | consultant_config válido |
| 1 | Intake cliente | personalization | G0 (10 campos) |
| 2 | Normalização | diagnostic-engine | G1 |
| 3 | Diagnóstico | diagnostic-engine | problem_tree completo |
| 4 | Priorização | diagnostic-engine | **★G2 HARDCODED** |
| 5 | Plano de ação | diagnostic-engine | G3 |
| 6 | Simulação (opcional) | simulation-lab | simulation_report |
| 7 | Geração artefatos | deliverable-forge | G4 + **★G5 HARDCODED** |
| 8 | Handoff execution | execution-bridge | **★G6 HARDCODED** |
| 9 | Follow-up | deliverable-forge | proposta_continuidade aprovada |

★ Gates HARDCODED: G2, G5, G6 — nunca automáticos em NENHUM modo.

## manifest.yaml — estrutura

```yaml
case_id: BP-001
consultant_id: marina-costa
created_at: 2026-04-17T10:00:00Z
updated_at: 2026-04-17T22:00:00Z
current_phase: 7
operating_mode: guided

gates:
  G0: {status: approved, approved_at: "...", approved_by: consultor}
  G1: {status: approved, approved_at: "..."}
  G2: {status: pending}
  G3: {status: not_reached}
  G4: {status: not_reached}
  G5: {status: not_reached}
  G6: {status: not_reached}

artifacts:
  diagnostico_executivo: {status: pending_human_review}
  apresentacao_executiva: {status: not_started}
  proposta_continuidade: {status: not_started}

human_review_required:
  - diagnostico_executivo
  - apresentacao_executiva
  - proposta_continuidade

simulation_used: false
```

## Regras de roteamento

| Intenção detectada | Skill roteada |
|-------------------|---------------|
| Setup consultor, intake | personalization |
| Diagnóstico, análise, priorização | diagnostic-engine |
| Simulação, cenários | simulation-lab |
| Gerar artefatos, ZIP | deliverable-forge |
| Handoff Linear | execution-bridge |
| Perguntas sobre método | consultative-faq |

## Artefatos com revisão humana obrigatória

1. `diagnostico_executivo` — Gate G5
2. `apresentacao_executiva` — Gate G5
3. `proposta_continuidade` — Gate G5

## Dashboard de fases (formato ASCII)

```
Caso BP-001 — Marina Costa — guided mode
─────────────────────────────────────────
[✓] Fase 0: Configuração consultor
[✓] Fase 1: Intake (G0: approved)
[✓] Fase 2: Normalização (G1: approved)
[✓] Fase 3: Diagnóstico
[⚠] Fase 4: Priorização (G2: pending — MANUAL OBRIGATÓRIO)
[ ] Fase 5: Plano de ação
[ ] Fase 6: Simulação (opcional)
[ ] Fase 7: Geração artefatos
[ ] Fase 8: Handoff execution
[ ] Fase 9: Follow-up
─────────────────────────────────────────
Próximo: aprovar G2 para avançar para Fase 5
```

## Dependências

```bash
pip install --break-system-packages pyyaml jinja2
```

## Evals

```json
[
  {
    "id": 1,
    "prompt": "Novo caso Bússola PME para Marina, cliente agência de 6 pessoas.",
    "expected": "Orchestrator inicializa manifest.yaml, roteia para personalization para fase 0, exibe dashboard.",
    "should_trigger": true
  },
  {
    "id": 2,
    "prompt": "Caso BP-014, fase 5 concluída. Quero pular direto para apresentação sem revisar o diagnostico_executivo.",
    "expected": "Orchestrator recusa. G5 é HARDCODED. Exibe gate bloqueado e instrui a aprovar diagnostico_executivo primeiro.",
    "should_trigger": true
  },
  {
    "id": 3,
    "prompt": "Me explica a diferença entre 5W2H e PDCA.",
    "expected": "Orchestrator NÃO ativa. Roteia para consultative-faq.",
    "should_trigger": false
  }
]
```

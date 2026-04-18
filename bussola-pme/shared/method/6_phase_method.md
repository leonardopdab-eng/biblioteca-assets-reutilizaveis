# Bússola PME — Método de 6 Fases

Documento canônico do método consultivo. Referenciado por diagnostic-engine, orchestrator e FAQ via path relativo.

---

## Diagrama de fluxo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BÚSSOLA PME — 6 FASES                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  FASE 1              FASE 2              FASE 3
  Alinhamento    ──►  Normalização   ──►  Diagnóstico
  (Intake bruto)      (Gate G1)           (Módulos analíticos)
       │                   │                    │
       ▼                   ▼                    ▼
  intake_normalized   intake_normalized_v2   problem_tree
  seed                aprovado               hypotheses_log
                                             diagnostic_working

                              │
                              ▼
  FASE 6              FASE 5              FASE 4
  Acompanhamento ◄──  Plano de Ação  ◄──  Priorização
  (Gate G5)           (Gate G3)           (Gate G2 ★HARDCODED)
       │                   │                    │
       ▼                   ▼                    ▼
  relatorio_          plano_acao          priority_score
  acompanhamento      aprovado            aprovado
  proposta_
  continuidade

★ G2, G5, G6 são HARDCODED como manuais. Nunca automáticos.
```

---

## Fase 1 — Alinhamento

**Objetivo**: Calibração de expectativas entre consultor e cliente. Estabelecer contexto mínimo para o trabalho analítico.

**Inputs**:
- Briefing bruto do cliente (texto livre, documentos, emails)
- Histórico de interações (se disponível via source_whitelist)

**Outputs**:
- `intake_normalized.md` (seed — versão inicial, não validada)
- `information_gaps.md` (campos ausentes ou incertos)

**Critério de conclusão**: 10 campos coletados ou gaps registrados para cada ausente.

**Regras aplicáveis**:
- **R01**: Nunca avançar para análise sem intake seed mínimo
- **R07**: Input bruto nunca alimenta análise diretamente — precisa passar pela Fase 2

**Skills responsáveis**: `bussola-personalization`

**Gate de saída**: G0 — 10 campos presentes ou gaps registrados (sempre manual, ambos os modos)

---

## Fase 2 — Normalização

**Objetivo**: Estruturar o input bruto com labels epistêmicos, separando fatos de inferências e hipóteses.

**Inputs**:
- `intake_normalized.md` (seed da Fase 1)

**Outputs**:
- `intake_normalized_v2.md` — versão estruturada com:
  - Labels `[FATO]`, `[INFERÊNCIA]`, `[HIPÓTESE]` em cada claim
  - Campos obrigatórios preenchidos ou gaps documentados
  - Flag `approved: true` após revisão

**Critério de conclusão**: Gate G1 — intake_normalized_v2 com flag approved e todos os campos obrigatórios presentes (ou gaps registrados).

**Regras aplicáveis**:
- **R02**: Toda hipótese tem label epistêmico explícito
- **R07**: Input bruto (intake_normalized seed) substituído por intake_normalized_v2 para todo uso downstream

**Skills responsáveis**: `bussola-diagnostic-engine`

**Gate de saída**: G1 (manual em guided; auto em hands_off se condição satisfeita)

---

## Fase 3 — Diagnóstico

**Objetivo**: Análise causal estruturada usando módulos analíticos apropriados ao tipo de problema. Produz visão sistêmica da situação.

**Inputs**:
- `intake_normalized_v2.md` aprovado (Gate G1 passado)
- `consultant_config.yaml` (para seleção de módulos via method_weights.diagnosis)

**Outputs**:
- `hypotheses_log.md` — registro de todas as hipóteses geradas com labels
- `problem_tree.md` — árvore causal (raiz + causas nível-1 e nível-2)
- `diagnostic_working.md` — trilha interna de raciocínio (NUNCA vai para cliente)

**Critério de conclusão**: `problem_tree.md` completo (raiz identificada + pelo menos 3 causas nível-1 com labels epistêmicos).

**Regras aplicáveis**:
- **R03**: Hipóteses não propagam como fatos
- **R04**: Módulo escolhido por tipo de problema (via `module_router.py`), não preferência
- **R09**: `decision_log` registra toda decisão de roteamento
- **R10**: `diagnostic_working` é trilha interna — não vai para cliente

**Módulos disponíveis**: 5 Porquês, Ishikawa, Pareto, SWOT, 5W2H, PDCA, JTBD, Esforço×Impacto

**Skills responsáveis**: `bussola-diagnostic-engine`

**Gate de saída**: problem_tree completo (sem gate formal; flui para Fase 4)

---

## Fase 4 — Priorização

**Objetivo**: Ranking dos problemas/hipóteses por impacto, urgência, esforço e alinhamento estratégico.

**Inputs**:
- `problem_tree.md` (Fase 3)
- `consultant_config.yaml` (method_weights.prioritization para granularidade)

**Outputs**:
- `priority_score.md` — tabela rankeada com scores e justificativas
  - Score = (impacto × 0.4) + (urgência × 0.3) + (esforço_inv × 0.2) + (alinhamento × 0.1)
  - Status inicial: `pending` → `approved` após Gate G2

**Critério de conclusão**: ★ **Gate G2 — HARDCODED MANUAL** — nunca automático, nunca configurável, nunca bypassável. Consultor deve revisar e aprovar explicitamente.

**Regras aplicáveis**:
- **R05**: Priority score usa pesos do consultant_config.yaml
- **R08**: Gate G2 nunca bypassado

**Skills responsáveis**: `bussola-diagnostic-engine`

**Gate de saída**: ★ **G2 HARDCODED MANUAL** — priority_score revisado e aprovado pelo consultor

---

## Fase 5 — Plano de Ação

**Objetivo**: Transformar problemas priorizados em ações executáveis com owner, deadline e KPI.

**Inputs**:
- `priority_score.md` aprovado (Gate G2 passado)
- `consultant_config.yaml` (deliverable_depth para nível de detalhe)

**Outputs**:
- `plano_acao.md` — tabela de ações com:
  - `owner` (string não-vazia)
  - `deadline` (ISO8601)
  - `kpi` (string não-vazia)
  - Se depth=deep: campos 5W2H completos (what, why, where, when, who, how, how_much)
  - Status: `pending_human_review` → `approved` após Gate G3

**Critério de conclusão**: Gate G3 — `action_field_enforcer.py` passa (exit 0), plano aprovado.

**Regras aplicáveis**:
- **R06**: Plano sem owner/deadline/KPI é bloqueado pelo enforcer
- **R09**: decision_log registra decisões de ação

**Skills responsáveis**: `bussola-diagnostic-engine`

**Gate de saída**: G3 (manual em guided; auto se enforcer pass em hands_off)

---

## Fase 6 — Acompanhamento

**Objetivo**: Follow-up estruturado pós-entrega. Revisão de resultados, ajuste de plano, proposta de continuidade.

**Inputs**:
- `plano_acao.md` aprovado
- Dados de execução (via source_whitelist)
- Artefatos de trilha cliente entregues e aprovados

**Outputs**:
- `relatorio_acompanhamento.md` — situação atual vs. planejado por ação
- `proposta_continuidade.md` — oferta de engajamento futuro

**Critério de conclusão**: ★ **Gate G5 — HARDCODED MANUAL** nos dois artefatos críticos.

**Regras aplicáveis**:
- **R08**: Gate G5 nunca bypassado
- **R10**: Separação trilha interna/cliente mantida

**Skills responsáveis**: `bussola-deliverable-forge`, `bussola-orchestrator`

**Gate de saída**: ★ **G5 HARDCODED MANUAL** — ambos os artefatos críticos revisados e aprovados

---

## Tabela de Dependências entre Fases

| Fase | Depende de | Produz | Gate de entrada | Gate de saída |
|------|------------|--------|-----------------|---------------|
| 1 — Alinhamento | — | intake_normalized seed | — | G0 |
| 2 — Normalização | Fase 1 (G0) | intake_normalized_v2 | G0 | G1 |
| 3 — Diagnóstico | Fase 2 (G1) | hypotheses_log, problem_tree | G1 | — |
| 4 — Priorização | Fase 3 | priority_score | — | ★G2 |
| 5 — Plano de Ação | Fase 4 (G2) | plano_acao | ★G2 | G3 |
| 6 — Acompanhamento | Fase 5 (G3) + artefatos cliente | relatorio, proposta | G3 | ★G5 |

**Legenda**: ★ = HARDCODED MANUAL, nunca automático

---

## Políticas Epistêmicas Transversais

Todo artefato produzido nas 6 fases deve aplicar labels epistêmicos:

- `[FATO]` — fornecido pelo cliente ou fonte verificável
- `[INFERÊNCIA]` — dedução forte a partir de sinais indiretos
- `[HIPÓTESE]` — plausível mas não validado

**Regra de ouro**: Hipótese nunca vira fato sem validação documentada. A propagação de hipóteses como fatos é a principal fonte de erro consultivo.

---

## Integração com Skills

```
bussola-personalization  →  Fases 0 e 1
bussola-diagnostic-engine →  Fases 2, 3, 4, 5
bussola-simulation-lab    →  Entre Fases 4 e 5 (opcional)
bussola-deliverable-forge →  Fase 7 (geração de artefatos)
bussola-orchestrator      →  Coordenação de todas as fases
bussola-execution-bridge  →  Fase 8 (handoff Linear)
bussola-consultative-faq  →  Suporte em qualquer fase
bussola-case1-showroom    →  Pós-caso (showcase comercial)
```

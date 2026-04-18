---
name: bussola-diagnostic-engine
description: >
  Use this skill to run the Bússola PME analytical pipeline (phases 2–5):
  normalization, diagnosis, prioritization, and action planning. Activate on
  "rodar diagnóstico", "gerar problem_tree", "priorizar problemas", "fazer 5
  porquês", "aplicar Pareto", "aplicar SWOT", "aplicar 5W2H", "gerar plano de
  ação com responsáveis e prazos", "analisar causa raiz", "mapear hipóteses".
  Requires intake_normalized.md and consultant_config.yaml as inputs. Enforces
  10 rules of conduct (R01–R10) and routes to the correct analytical module
  based on problem type. Produces hypotheses_log, problem_tree,
  diagnostic_working, priority_score, plano_acao, and decision_log entries.
  Do NOT use for intake collection (use personalization) or artifact rendering
  (use deliverable-forge).
dependencies: [pyyaml]
---

# bussola-diagnostic-engine

## Propósito

Pipeline analítico completo das Fases 2–5 do método Bússola PME. Recebe intake normalizado e produz plano de ação aprovável, aplicando módulos analíticos baseados no tipo de problema.

## Pré-condições

- `intake_normalized.md` presente (seed da Fase 1)
- `consultant_config.yaml` válido presente
- Skill `bussola-personalization` executada com sucesso

## Sub-fase 2 — Normalização

**Input**: `intake_normalized.md` (seed bruto)
**Output**: `intake_normalized_v2.md` (estruturado com labels epistêmicos)

### Passos
1. Verificar existência do intake seed (R01)
2. Para cada claim no intake, classificar: `[FATO]`, `[INFERÊNCIA]`, ou `[HIPÓTESE]`
3. Documentar gaps com impact e recommended_action
4. Aplicar R07: input bruto nunca alimenta análise — usar apenas intake_normalized_v2
5. **Gate G1**: aguardar aprovação (manual em guided; auto em hands_off se condição ok)

**R07 enforça**: qualquer análise que tente usar intake_normalized (sem _v2) é bloqueada.

## Sub-fase 3 — Diagnóstico

**Input**: `intake_normalized_v2.md` aprovado (G1) + `consultant_config.yaml`
**Output**: `hypotheses_log.md`, `problem_tree.md`, `diagnostic_working.md`

### Passos
1. Executar `module_router.py` para selecionar módulo(s) analítico(s) (R04)
2. Registrar decisão de roteamento em `decision_log.md` (R09)
3. Aplicar módulo primário (e secundário se diagnosis weight > 0.30)
4. Gerar `hypotheses_log.md` com labels em cada hipótese (R02, R03)
5. Construir `problem_tree.md` com raiz e causas nível-1/nível-2
6. Manter `diagnostic_working.md` como trilha interna (R10 — nunca para cliente)

## Tabela de roteamento de módulos

| Sinal no problema | Módulo primário | Módulo secundário |
|---|---|---|
| Causa raiz desconhecida | 5 Porquês | Ishikawa |
| Múltiplos problemas sem foco | Pareto | Esforço×Impacto |
| Análise de posição estratégica | SWOT | — |
| Plano com baixa especificidade | 5W2H | — |
| Melhoria de processo existente | PDCA | — |
| Problema sistêmico multi-causa | Ishikawa | 5 Porquês |
| Produto/serviço sem job articulado | JTBD | — |
| Priorização rápida de iniciativas | Esforço×Impacto | Pareto |

## Sub-fase 4 — Priorização

**Input**: `problem_tree.md` + pesos de config
**Output**: `priority_score.md`

### Fórmula de score
```
score = (impacto × 0.4) + (urgência × 0.3) + (esforço_inverso × 0.2) + (alinhamento × 0.1)
```

Granularidade modulada pelo `method_weights.prioritization`:
- < 0.20: escala 1–3
- 0.20–0.30: escala 1–5 (quintis)
- > 0.30: escala 1–10 (decis)

**★ Gate G2 — HARDCODED MANUAL**: priority_score nunca avança automaticamente. Consultor deve revisar e aprovar explicitamente. Válido em guided E hands_off.

## Sub-fase 5 — Plano de Ação

**Input**: `priority_score.md` aprovado (G2)
**Output**: `plano_acao.md` (status: `pending_human_review`)

### Campos obrigatórios por item
- `owner` (string não-vazia)
- `deadline` (ISO8601, ex: 2026-05-15)
- `kpi` (string não-vazia)

Se `deliverable_depth == deep`: expande com 5W2H completo (what, why, where, when, who, how, how_much).

`action_field_enforcer.py` executa verificação antes de salvar o plano. Exit 1 bloqueia.

**Gate G3**: plano com campos completos → manual em guided, auto em hands_off.

## As 10 Regras de Conduta

| ID | Regra | Ponto de aplicação |
|----|-------|-------------------|
| R01 | Nunca gerar diagnóstico sem intake normalizado | Pré-condição sub-fase 2 |
| R02 | Toda hipótese tem label epistêmico explícito | Ao criar qualquer claim |
| R03 | Hipóteses não propagam como fatos | Ao usar outputs downstream |
| R04 | Módulo escolhido por tipo de problema, não preferência | module_router.py |
| R05 | Priority score usa pesos do consultant_config.yaml | priority_scorer.py |
| R06 | Plano sem owner/deadline/KPI é bloqueado | action_field_enforcer.py |
| R07 | Input bruto nunca alimenta análise diretamente | Sub-fase 2 obrigatória |
| R08 | Gate G1 e G2 nunca são bypassed | Hardcoded |
| R09 | decision_log registra toda decisão de roteamento | Ao selecionar módulo e priorizar |
| R10 | diagnostic_working é trilha interna — não vai para cliente | Separação de trilhas |

## Outputs produzidos

| Arquivo | Trilha | Descrição |
|---------|--------|-----------|
| `intake_normalized_v2.md` | Interna | Intake estruturado com labels |
| `hypotheses_log.md` | Interna | Registro de hipóteses |
| `problem_tree.md` | Interna | Árvore causal |
| `diagnostic_working.md` | **Interna somente** | Raciocínio interno |
| `priority_score.md` | Interna | Ranking de problemas |
| `plano_acao.md` | Interna → Cliente | Plano de ação estruturado |
| `decision_log.md` | Interna | Log de decisões de roteamento |

## Caso canônico BP-001

**Input**: Agência B2B, 6 pessoas, pipeline caindo 40% em 4 meses, causa desconhecida.
**Módulo roteado**: 5 Porquês (causa raiz desconhecida) + Pareto (múltiplos sintomas)
**Problem tree**: Raiz = "Queda de 40% no pipeline" → Causas: ICP desatualizado, processo de qualificação fraco, churn silencioso de leads quentes

## Dependências

```bash
pip install --break-system-packages pyyaml
```

## Evals

```json
[
  {
    "id": 1,
    "prompt": "Rodar diagnóstico. Cliente é agência de 6 pessoas, problema: faturamento caindo sem causa clara.",
    "expected": "module_router seleciona 5_whys, gera problem_tree, hypotheses_log com labels, avança para priorização após G1.",
    "should_trigger": true
  },
  {
    "id": 2,
    "prompt": "Já tenho o diagnóstico pronto. Pula direto para o plano de ação.",
    "expected": "Skill recusa. Gate G2 é HARDCODED manual — priority_score deve existir e ser aprovado.",
    "should_trigger": true
  },
  {
    "id": 3,
    "prompt": "Me explica a diferença entre 5W2H e PDCA.",
    "expected": "Skill NÃO ativa. Pergunta de método — roteia para consultative-faq.",
    "should_trigger": false
  }
]
```

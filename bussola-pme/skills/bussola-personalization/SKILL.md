---
name: bussola-personalization
description: >
  Use this skill for Bússola PME Phase 0 setup and client intake. Activate on
  "configurar consultor", "onboarding do consultor", "setup inicial", "iniciar
  caso PME", "preencher intake", "ajustar pesos do método", "trocar modo de
  operação", "configurar branding". Produces consultant_config.yaml that governs
  the entire system downstream (method weights, dependency order, source usage,
  deliverable depth, operating mode guided vs hands_off, branding tokens) AND
  runs the 10-field interactive intake questionnaire for each new client case.
  Uses ask_user_input_v0 for conversational UX and optionally pulls context from
  Google Drive / Gmail via MCP to pre-fill intake fields. Must be invoked before
  Diagnostic Engine on any new case; consultant_config.yaml must exist before
  Orchestrator can route to any specialist skill. Do NOT use for analytical work
  (use diagnostic-engine) or artifact generation (use deliverable-forge).
compatibility:
  tools: [ask_user_input_v0, mcp__google_drive, mcp__gmail]
dependencies: [pyyaml, jsonschema]
---

# bussola-personalization

## Propósito

Esta skill opera em dois momentos distintos e complementares:

1. **Onboarding do consultor** — configuração única (ou atualização) do arquivo `consultant_config.yaml` que governa todos os comportamentos downstream do sistema Bússola PME.
2. **Intake do cliente** — coleta interativa dos 10 campos estruturados para cada novo caso, com suporte a pre-fill via Google Drive ou Gmail.

## Quando usar

| Situação | Ação |
|----------|------|
| Primeira vez usando o Bússola PME | Fluxo A — Onboarding |
| Atualizar modo de operação, pesos ou branding | Fluxo A — Atualização |
| Iniciar novo caso com cliente | Fluxo B — Intake |
| Cliente enviou documentos no Drive | Fluxo B com pre-fill Drive |
| Retomar caso com gaps de intake | Fluxo B — preenchimento parcial |

## Fluxo A — Onboarding do Consultor

**Pré-condição**: nenhuma (pode rodar sem consultant_config.yaml existente)

### Passo 1 — Identificação
Coletar via `ask_user_input_v0`:
- `consultant_id` (kebab-case, ex: `marina-costa`)
- `consultant_name` (ex: `Marina Costa`)

### Passo 2 — Modo de operação
```
"Qual modo de operação você prefere?
  - guided: cada gate pede sua confirmação explícita
  - hands_off: sistema avança automaticamente quando condição satisfeita
  (Nota: G2, G5, G6 são sempre manuais em ambos os modos)"
```

### Passo 3 — Pesos do método
Apresentar 3 perfis pré-calibrados ou coletar pesos custom (soma deve ser 1.0 ±0.01):
- Perfil agências B2B: normalization=0.2, diagnosis=0.4, prioritization=0.25, action_plan=0.15
- Perfil operações industriais: normalization=0.15, diagnosis=0.35, prioritization=0.2, action_plan=0.3
- Perfil estratégico genérico: normalization=0.25, diagnosis=0.25, prioritization=0.25, action_plan=0.25

### Passo 4 — Configurações adicionais
- `dependency_order`: fixed ou flexible
- `source_whitelist`: fontes externas permitidas (google_drive, gmail, notion, none)
- `deliverable_depth`: lite, standard, ou deep

### Passo 5 — Branding (opcional)
- `primary_color` (hex, ex: #1B4F72)
- `font_family` (ex: Inter)
- `consultant_display_name` (nome para exibição em artefatos)

### Passo 6 — Validação e persistência
- Renderizar template `consultant_config.yaml.j2`
- Executar `config_schema_validator.py`
- Apenas se VALID: salvar em `consultant_config.yaml`
- Se INVALID: exibir erro e pedir correção (R-P04)

## Fluxo B — Intake do Cliente

**Pré-condição**: `consultant_config.yaml` válido deve existir (R-P05)

### Passo 1 — Verificar pré-condições
Checar `consultant_config.yaml`. Se ausente: bloquear com mensagem de erro e instruir rodar Fluxo A.

### Passo 2 — Pre-fill via fontes (opcional)
Se `source_whitelist` contém `google_drive` ou `gmail`:
- Tentar puxar contexto via MCP correspondente
- Mapear dados encontrados para campos do intake
- Marcar campos pre-filled como `[FATO]` com fonte registrada
- Campos não encontrados ficam para coleta manual

### Passo 3 — Coleta interativa
Para cada campo não pre-filled, usar `ask_user_input_v0`. Tratar "não sei" → registrar em `information_gaps.md` com:
- `impact`: alto/médio/baixo
- `recommended_action`: string com próximo passo para obter o dado

### Passo 4 — Validação Gate G0
Verificar que todos os 7 campos obrigatórios estão preenchidos ou têm gap registrado. **Gate G0 nunca é bypassado, nem em hands_off** (R-P03).

### Passo 5 — Produção de artefatos
- Gerar `intake_normalized.md` (seed) com labels epistêmicos
- Gerar `information_gaps.md` se houver campos ausentes
- Executar `intake_field_checker.py` para validação

### Passo 6 — Confirmação e handoff
Exibir resumo do intake, confirmar com consultor, registrar gate G0 no manifest (se existir).

### Passo 7 — Sinalizar próximo passo
Informar que `bussola-diagnostic-engine` pode ser ativado para Fase 2 (Normalização).

## Os 10 campos do intake

| # | Campo | Tipo | Obrigatório |
|---|-------|------|-------------|
| 1 | `company_name` | string | Sim |
| 2 | `segment` | enum (agência, serviços, produto, varejo, outro) | Sim |
| 3 | `team_size` | integer | Sim |
| 4 | `annual_revenue_range` | enum | Sim |
| 5 | `primary_problem` | string (max 200 chars) | Sim |
| 6 | `secondary_problems` | list[string] | Não |
| 7 | `previous_diagnosis` | boolean + string opcional | Não |
| 8 | `urgency_level` | enum (low/medium/high/critical) | Sim |
| 9 | `decision_makers` | list[string] | Sim |
| 10 | `available_documents` | list[string] | Não |

## Regras de Conduta

| ID | Regra | Consequência se violada |
|----|-------|------------------------|
| R-P01 | Nunca puxar de fonte não em `source_whitelist` | Bloqueio imediato com log |
| R-P02 | Nunca produzir intake_normalized.md com campo obrigatório ausente sem `information_gap` registrado | intake_normalized não gerado |
| R-P03 | Gate G0 nunca bypassed, nem em hands_off | Sistema recusa avanço |
| R-P04 | consultant_config.yaml com falha de schema não é salvo | Exibe erro, solicita correção |
| R-P05 | Ausência de consultant_config.yaml bloqueia qualquer ação downstream | Bloqueio com instrução de onboarding |

## Outputs produzidos

| Arquivo | Descrição |
|---------|-----------|
| `consultant_config.yaml` | Configuração do consultor (Fluxo A) |
| `intake_normalized.md` | Seed do intake com labels epistêmicos (Fluxo B) |
| `information_gaps.md` | Lista de campos ausentes com impact e recommended_action |

## Caso canônico BP-001

**Contexto**: Agência B2B de 6 pessoas. Consultora: Marina Costa (`marina-costa`). Problema principal: pipeline de vendas caindo 40% em 4 meses. Modo: guided. Branding: #1B4F72.

```yaml
# intake_normalized.md (seed) para BP-001
company_name: "Agência BP-001" [FATO]
segment: agência [FATO]
team_size: 6 [FATO]
annual_revenue_range: "R$ 500k–R$ 1M" [FATO]
primary_problem: "Pipeline de vendas caindo ~40% nos últimos 4 meses" [FATO]
urgency_level: high [FATO]
decision_makers: ["Marina Costa (sócia)", "Rafael Lima (comercial)"] [FATO]
```

## Dependências

```bash
pip install --break-system-packages pyyaml jsonschema
```

## Arquivos relacionados

- `scripts/config_schema_validator.py` — validador de schema
- `scripts/intake_field_checker.py` — verificador de campos do intake
- `references/operating_modes.md` — contrato dos modos guided/hands_off
- `references/method_weights_reference.md` — guia de calibração de pesos
- `templates/consultant_config.yaml.j2` — template Jinja2 para config
- `templates/intake_questions.yaml` — questionário estruturado
- `examples/consultant_config_guided.yaml` — exemplo modo guided (BP-001)
- `examples/consultant_config_hands_off.yaml` — exemplo modo hands_off

## Evals

```json
[
  {
    "id": 1,
    "prompt": "Primeiro caso do João no Bússola. Setup dele: consultor de operações, modo guided, branding azul-marinho.",
    "expected": "Skill ativa fluxo de onboarding, usa ask_user_input_v0 para knobs, produz consultant_config.yaml válido.",
    "should_trigger": true
  },
  {
    "id": 2,
    "prompt": "Cliente me mandou um PDF pelo Drive com a situação. Quero puxar para o intake sem redigitar.",
    "expected": "Skill verifica whitelist, ativa MCP Google Drive se permitido, pré-preenche, marca restantes para coleta manual.",
    "should_trigger": true
  },
  {
    "id": 3,
    "prompt": "Quero gerar a apresentação executiva final.",
    "expected": "Skill NÃO ativa. Responsabilidade do deliverable-forge.",
    "should_trigger": false
  }
]
```

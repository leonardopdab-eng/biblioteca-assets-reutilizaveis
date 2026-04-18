# Fluxo de 9 Fases — Bússola PME Orchestrator

## Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────────┐
│                    BÚSSOLA PME — 9 FASES                              │
└──────────────────────────────────────────────────────────────────────┘

  FASE 0              FASE 1              FASE 2              FASE 3
  Configuração   ──►  Intake         ──►  Normalização  ──►  Diagnóstico
  Consultor           Cliente             (G1)
  │                   (G0)
  ▼                   ▼                   ▼                   ▼
  consultant_         intake_norm.    intake_norm_v2      problem_tree
  config.yaml         seed            approved            hypotheses_log

                                           │
                                           ▼
  FASE 9              FASE 8              FASE 7              FASE 4
  Follow-up      ◄──  Handoff        ◄──  Geração        ◄──  Priorização
                      (★G6)               (★G5+G4)            (★G2)
  │                   │                   │                   │
  ▼                   ▼                   ▼                   ▼
  proposta_cont.  Linear project      ZIP + 28 arts.      priority_score
  relatorio           Slack notify        aprovado            MANUAL

                              FASE 6 (opcional)
                              Simulação
                              ↑
                         FASE 5 ─────────────────────►
                         Plano de ação
                         (G3)
                         │
                         ▼
                         plano_acao

★ = HARDCODED MANUAL — nunca automático
```

## Detalhamento por fase

### Fase 0 — Configuração do Consultor
- **Objetivo**: Criar ou atualizar consultant_config.yaml
- **Inputs esperados**: Dados do consultor (nome, modo, pesos, branding)
- **Outputs produzidos**: `consultant_config.yaml` válido
- **Skill responsável**: bussola-personalization (Fluxo A)
- **Gate de saída**: consultant_config.yaml com validação VALID
- **Mensagem de bloqueio**: "consultant_config.yaml não encontrado ou inválido. Execute bussola-personalization para configurar o consultor."

### Fase 1 — Intake do Cliente
- **Objetivo**: Coletar 10 campos estruturados do cliente
- **Inputs esperados**: Dados do cliente (manual ou via Drive/Gmail)
- **Outputs produzidos**: `intake_normalized.md` (seed), `information_gaps.md`
- **Skill responsável**: bussola-personalization (Fluxo B)
- **Gate de saída**: G0 — 10 campos ou gaps registrados (SEMPRE MANUAL)
- **Mensagem de bloqueio**: "Intake incompleto. Campos obrigatórios ausentes sem gap registrado."

### Fase 2 — Normalização
- **Objetivo**: Estruturar intake com labels epistêmicos
- **Inputs esperados**: `intake_normalized.md` seed
- **Outputs produzidos**: `intake_normalized_v2.md` com labels
- **Skill responsável**: bussola-diagnostic-engine
- **Gate de saída**: G1 — intake_normalized_v2 aprovado
- **Mensagem de bloqueio**: "intake_normalized_v2 não aprovado. Consultor deve verificar labels epistêmicos."

### Fase 3 — Diagnóstico
- **Objetivo**: Análise causal com módulos analíticos
- **Inputs esperados**: `intake_normalized_v2.md` aprovado
- **Outputs produzidos**: `problem_tree.md`, `hypotheses_log.md`, `diagnostic_working.md`
- **Skill responsável**: bussola-diagnostic-engine
- **Gate de saída**: problem_tree completo (sem gate formal)
- **Mensagem de bloqueio**: "problem_tree incompleto. Raiz e causas nível-1 devem estar identificadas."

### Fase 4 — Priorização
- **Objetivo**: Ranking por impacto/urgência/esforço/alinhamento
- **Inputs esperados**: `problem_tree.md`
- **Outputs produzidos**: `priority_score.md` (status: pending)
- **Skill responsável**: bussola-diagnostic-engine
- **Gate de saída**: ★G2 HARDCODED MANUAL — priority_score aprovado pelo consultor
- **Mensagem de bloqueio**: "⚠️ Gate G2 é HARDCODED MANUAL. Revise o priority_score e aprove explicitamente."

### Fase 5 — Plano de Ação
- **Objetivo**: Ações executáveis com owner/deadline/KPI
- **Inputs esperados**: `priority_score.md` aprovado (G2)
- **Outputs produzidos**: `plano_acao.md` (status: pending_human_review)
- **Skill responsável**: bussola-diagnostic-engine
- **Gate de saída**: G3 — action_field_enforcer pass
- **Mensagem de bloqueio**: "Plano sem owner, deadline ou KPI. Execute action_field_enforcer."

### Fase 6 — Simulação (opcional)
- **Objetivo**: Cenários quantitativos on-demand
- **Inputs esperados**: Variáveis do cenário (coletadas via ask_user_input_v0)
- **Outputs produzidos**: `simulation_report.md`
- **Skill responsável**: bussola-simulation-lab
- **Gate de saída**: simulation_report gerado
- **Nota**: Fase completamente opcional. Não bloqueia avanço para Fase 7.

### Fase 7 — Geração de Artefatos
- **Objetivo**: Produzir todos os 28 artefatos em 3 trilhas
- **Inputs esperados**: `plano_acao.md` aprovado + `consultant_config.yaml`
- **Outputs produzidos**: 28 artefatos + ZIP
- **Skill responsável**: bussola-deliverable-forge
- **Gate de saída**: G4 (QA_PASS) + ★G5 HARDCODED MANUAL (3 artefatos críticos aprovados)
- **Mensagem de bloqueio**: "⚠️ Gate G5 é HARDCODED MANUAL. Revise diagnostico_executivo, apresentacao_executiva e proposta_continuidade."

### Fase 8 — Handoff para Execução
- **Objetivo**: Criar projeto no Linear com epics e issues
- **Inputs esperados**: `plano_acao.md` aprovado (G5)
- **Outputs produzidos**: Projeto Linear criado, notificação Slack
- **Skill responsável**: bussola-execution-bridge
- **Gate de saída**: ★G6 HARDCODED MANUAL — confirmação explícita do consultor
- **Mensagem de bloqueio**: "⚠️ Gate G6 é HARDCODED MANUAL. Esta ação tem efeitos externos irreversíveis."

### Fase 9 — Follow-up
- **Objetivo**: Relatório de acompanhamento e proposta de continuidade
- **Inputs esperados**: Dados de execução do plano
- **Outputs produzidos**: `relatorio_acompanhamento.md`, `proposta_continuidade.md`
- **Skill responsável**: bussola-deliverable-forge
- **Gate de saída**: proposta_continuidade aprovada pelo consultor

## Tabela de dependências entre fases

| Fase | Depende de | Gate de entrada |
|------|------------|-----------------|
| 0 | — | — |
| 1 | Fase 0 | consultant_config válido |
| 2 | Fase 1 | G0 |
| 3 | Fase 2 | G1 |
| 4 | Fase 3 | — |
| 5 | Fase 4 | ★G2 HARDCODED |
| 6 | Fase 4 ou 5 | opcional |
| 7 | Fase 5 | G3 |
| 8 | Fase 7 | G4 + ★G5 HARDCODED |
| 9 | Fase 7 | G3 |

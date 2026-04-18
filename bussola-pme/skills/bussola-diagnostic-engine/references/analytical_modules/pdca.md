# Módulo: PDCA (Plan-Do-Check-Act)

## Quando usar
- Processo existente que precisa de melhoria estruturada e contínua
- Problema recorrente em operações já mapeadas
- Cliente quer implementar ciclo de melhoria contínua após o caso
- **Sinal trigger**: "melhorar processo", "processo existente", "ciclo de melhoria", "padronização"

## Inputs necessários
- Processo existente descrito ou documentado
- Métricas atuais do processo (baseline para comparação)
- Alguém responsável por operar o processo (para o "Do")

## O ciclo PDCA aplicado ao Bússola PME

### P — Plan (Planejar)
- Definir problema específico no processo
- Analisar dados existentes
- Identificar causa raiz (pode usar 5 Porquês aqui)
- Definir contramedidas e metas mensuráveis

### D — Do (Executar)
- Implementar contramedidas em escala pequena primeiro (piloto)
- Documentar o que foi feito exatamente
- Coletar dados durante a execução

### C — Check (Checar)
- Comparar resultados com metas do Plan
- Analisar desvios
- Identificar aprendizados inesperados

### A — Act (Agir)
- Se funcionou: padronizar e expandir
- Se não funcionou: voltar ao Plan com novos dados
- Documentar lição aprendida

## Output esperado

```markdown
## PDCA — Processo de Qualificação de Leads (BP-001)

### PLAN
- **Problema**: Taxa de conversão lead→reunião caiu de 30% para 12% [FATO]
- **Meta**: Recuperar para 22% em 60 dias [HIPÓTESE sobre meta atingível]
- **Causa hipótese**: Critérios de qualificação não atualizados com novo ICP [HIPÓTESE]
- **Contramedida**: Revisar scorecard de qualificação + treinamento de 2h para Rafael

### DO
- Semana 1–2: Revisão do scorecard (Marina)
- Semana 3: Treinamento de Rafael
- Semana 4–8: Aplicação do novo critério + coleta de dados

### CHECK
- Métrica de acompanhamento: taxa lead→reunião semana a semana
- Data de check: 2026-06-01
- Responsável pela análise: Marina Costa

### ACT
- Se meta atingida: documentar novo processo no Playbook
- Se meta não atingida: identificar novo gargalo no funil
```

## Template de saída

```yaml
process_name: "string"
plan:
  problem: "string [label]"
  goal: "string [label]"
  root_cause_hypothesis: "string [HIPÓTESE]"
  countermeasures: [list]
do:
  steps: [list com owner e deadline]
check:
  metrics: [list]
  check_date: "ISO8601"
  responsible: "string"
act:
  if_success: "string"
  if_fail: "string"
```

## Limitações

- **Requer processo existente**: PDCA melhora o que existe; não cria do zero
- **Demora para mostrar resultado**: Mínimo 4–8 semanas de ciclo
- **Não use** para problemas estratégicos ou diagnóstico inicial (use SWOT ou 5 Porquês)
- **Disciplina de coleta de dados**: O "Check" falha sem métricas coletadas no "Do"

# Módulo: Pareto (80/20)

## Quando usar
- Cliente lista múltiplos problemas sem saber por onde começar
- Necessidade de foco antes de ir ao diagnóstico profundo
- Dados quantitativos disponíveis (frequência, impacto financeiro, tempo perdido)
- **Sinal trigger**: "temos muitos problemas", "não sabemos priorizar", "lista de problemas"

## Inputs necessários
- Lista de problemas ou causas com dados quantitativos associados
- Pelo menos uma métrica comparável entre os itens (frequência, R$, horas, tickets)
- intake_normalized_v2 com `secondary_problems` preenchido

## Processo de aplicação

1. **Listar todos os problemas** com métrica de impacto
2. **Ordenar** do maior para o menor impacto
3. **Calcular** % acumulado do impacto total
4. **Identificar** o ponto de 80% do impacto (geralmente 20% dos problemas)
5. **Focar** os próximos passos nos itens antes do ponto de 80%
6. Registrar "problemas fora do Pareto" como backlog para revisão futura

## Output esperado

```markdown
## Análise Pareto — BP-001

| Problema | Impacto estimado (R$/mês) | % do total | % acumulado |
|----------|--------------------------|------------|-------------|
| Queda no pipeline | 40.000 | 45% | 45% |
| Churn silencioso | 25.000 | 28% | 73% |
| Processo de proposta lento | 15.000 | 17% | 90% |
| Onboarding de cliente demorado | 6.000 | 7% | 97% |
| Retrabalho em briefings | 3.000 | 3% | 100% |

**Ponto de 80%**: após "Churn silencioso" (73% acumulado → 2 problemas = 73% do impacto)
**Foco recomendado**: Pipeline + Churn [INFERÊNCIA — dados estimados pelo cliente]
**Backlog para revisão futura**: Proposta lenta, Onboarding, Retrabalho
```

## Template de saída

```yaml
items:
  - problem: "string"
    metric_value: float
    metric_unit: "R$/mês | ocorrências | horas"
    pct_of_total: float
    pct_cumulative: float
pareto_cutoff_index: int
focus_items: [list]
backlog_items: [list]
note: "string — label epistêmico se estimativas"
```

## Limitações

- **Requer dados quantitativos** — sem métricas, análise é apenas qualitativa e menos confiável
- **Não use** como substituto de diagnóstico causal — Pareto identifica foco, não causa raiz
- **Cuidado com viés de disponibilidade**: problemas visíveis podem ter métricas infladas
- **Não use** quando há apenas 1–2 problemas (use 5 Porquês diretamente)

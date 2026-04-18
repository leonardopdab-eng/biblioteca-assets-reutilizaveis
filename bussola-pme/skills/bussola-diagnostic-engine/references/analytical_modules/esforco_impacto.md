# Módulo: Esforço × Impacto (Matriz de Priorização)

## Quando usar
- Lista de iniciativas definidas, mas sem critério de priorização
- Consultor e cliente precisam de consenso sobre o que fazer primeiro
- Necessidade de identificar "quick wins" antes de trabalhos mais complexos
- **Sinal trigger**: "priorização rápida", "quick wins", "o que fazer primeiro", "esforço versus resultado"

## Inputs necessários
- Lista de iniciativas ou ações (mínimo 4, máximo 20 para legibilidade)
- Estimativa de esforço e impacto por item (pode ser qualitativa: baixo/médio/alto)
- Contexto de recursos disponíveis (capacidade do time)

## Os 4 quadrantes

```
          ALTO IMPACTO
               │
   ┌───────────┼───────────┐
   │  QUICK    │  PROJETOS │
   │  WINS ⭐  │  MAIORES  │
   │ (fazer    │ (planejar │
   │  logo)    │  bem)     │
   │           │           │
───┼───────────┼───────────┼─── ESFORÇO
   │  ABANDO-  │  TAREFAS  │
   │  NABLE    │  DE ROTINA│
   │ (evitar)  │ (delegar) │
   │           │           │
   └───────────┴───────────┘
               │
          BAIXO IMPACTO

   BAIXO ESFORÇO    ALTO ESFORÇO
```

## Processo de aplicação

1. **Listar** todas as iniciativas candidatas
2. **Estimar esforço** (1=baixo, 5=alto): tempo + recursos + complexidade
3. **Estimar impacto** (1=baixo, 5=alto): receita + satisfação + risco reduzido
4. **Plotar** em matriz 5×5 (ou usar escala simplificada)
5. **Classificar** por quadrante
6. **Definir sequência**: Quick Wins → Projetos Maiores → Delegáveis → Evitar

## Output esperado

```markdown
## Esforço × Impacto — BP-001

| Iniciativa | Esforço | Impacto | Quadrante | Prioridade |
|------------|---------|---------|-----------|------------|
| Revisar ICP e qualificação | 2 | 5 | Quick Win | 1 |
| Rituais semanais de pipeline | 1 | 4 | Quick Win | 2 |
| Novo site e posicionamento | 5 | 4 | Projeto Maior | 3 |
| Automação de prospecção | 4 | 4 | Projeto Maior | 4 |
| Relatório manual de vendas | 2 | 1 | Delegável | 5 |
| Redesign de proposta padrão | 3 | 3 | Projeto Maior | 6 |

**Quick Wins identificados**: Revisar ICP + Rituais de pipeline
**Recomendação**: Executar quick wins em paralelo nas primeiras 2 semanas [INFERÊNCIA]
**Projetos maiores**: Planejar após estabilização do pipeline
```

## Template de saída

```yaml
items:
  - name: "string"
    effort: int  # 1–5
    impact: int  # 1–5
    quadrant: "quick_win | big_project | delegate | avoid"
    priority: int
    note: "string [label]"
quick_wins: [list]
big_projects: [list]
delegate: [list]
avoid: [list]
recommendation: "string"
```

## Limitações

- **Estimativas são subjetivas**: Esforço e impacto devem ser calibrados com o cliente
- **Não substitui diagnóstico**: Prioriza o que já está listado; não descobre causas
- **Viés de facilidade**: Times tendem a superestimar o impacto de quick wins
- **Escala importa**: Iniciativas de escalas muito diferentes são difíceis de comparar na mesma matriz

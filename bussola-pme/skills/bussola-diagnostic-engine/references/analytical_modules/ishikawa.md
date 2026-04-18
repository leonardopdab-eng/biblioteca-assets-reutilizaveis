# Módulo: Ishikawa (Diagrama de Espinha de Peixe)

## Quando usar
- Problema sistêmico com múltiplas causas independentes e encadeadas
- 5 Porquês não é suficiente (causalidade não é linear)
- Necessidade de mapear todas as dimensões do problema simultaneamente
- **Sinal trigger**: "múltiplas causas", "problema complexo", "diversas origens", "espinha de peixe"

## Inputs necessários
- Problema claramente formulado (efeito no "cabeça do peixe")
- Acesso às diferentes áreas/pessoas que contribuem para o problema
- Tempo para análise estruturada (mínimo 60min de trabalho)

## As 6 categorias (6M) adaptadas para PMEs

| Categoria | PME equivalente | Exemplos |
|-----------|-----------------|---------|
| Máquina | Ferramentas/sistemas | CRM, ferramentas de automação, infra |
| Método | Processos | Fluxo de vendas, onboarding, entrega |
| Material | Produtos/serviços | Qualidade da oferta, proposta de valor |
| Mão-de-obra | Pessoas | Capacitação, ownership, motivação |
| Medição | Métricas | KPIs mal definidos, falta de dados |
| Meio-ambiente | Mercado/contexto | Concorrência, sazonalidade, regulação |

## Processo de aplicação

1. **Definir o efeito** (problema principal) na "cabeça do peixe"
2. **Para cada categoria** (6M): identificar causas contribuintes
3. **Para cada causa**: aprofundar com "por quê?" (1–2 níveis)
4. **Marcar labels epistêmicos** em cada causa
5. **Identificar** as causas com maior convergência de evidências
6. **Priorizar** para aprofundamento com 5 Porquês ou validação

## Output esperado

```markdown
## Ishikawa — BP-001 (Queda de Pipeline)

**Efeito**: Pipeline de vendas caiu 40% em 4 meses

### Máquina/Ferramentas
- CRM sem uso sistemático → dados de pipeline não confiáveis [HIPÓTESE]
- Ausência de ferramenta de automação de prospecção [FATO — confirmado]

### Método/Processos
- Sem processo de qualificação de leads definido [HIPÓTESE]
- Reuniões de pipeline sem ritual estruturado [FATO — sócio confirmou]
- Proposta enviada sem follow-up estruturado [HIPÓTESE]

### Material/Oferta
- Posicionamento da agência não diferenciado [HIPÓTESE]
- Portfolio desatualizado sem casos recentes [INFERÊNCIA — site antigo]

### Mão-de-obra/Pessoas
- Rafael (comercial) sem capacitação formal em vendas B2B [HIPÓTESE]
- Sócia (Marina) acumula papel comercial e operacional [FATO — declarado]

### Medição/Métricas
- Sem KPIs de pipeline monitorados semanalmente [FATO — confirmado]
- Taxa de conversão por etapa desconhecida [FATO — dados não existem]

### Meio-ambiente/Mercado
- Concorrentes com proposta mais clara entrando no mercado [INFERÊNCIA]
- Clientes B2B com ciclos de compra mais longos em 2025–2026 [HIPÓTESE]

**Causas de maior convergência**: Métricas ausentes + Rituais comerciais inexistentes
```

## Template de saída

```yaml
effect: "string"
categories:
  maquina: [{cause: "string", label: FATO|INFERÊNCIA|HIPÓTESE, sub_causes: []}]
  metodo: [...]
  material: [...]
  mao_de_obra: [...]
  medicao: [...]
  meio_ambiente: [...]
high_convergence_causes: [list]
recommended_next: "5_whys | pareto | validation"
```

## Limitações

- **Não prioriza automaticamente**: identifica causas mas não ranqueia por impacto (use Pareto depois)
- **Requer múltiplos informantes**: Uma pessoa não consegue preencher todos os 6M com profundidade
- **Risco de excesso de hipóteses**: Muitas causas podem tornar o próximo passo difuso
- **Não use** como passo final: Ishikawa é exploratório, precisa ser seguido por validação

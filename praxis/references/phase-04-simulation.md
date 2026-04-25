# Fase 4 de 6 — Laboratório de Simulação

## Responsabilidade
Gerar cenários escalados para suporte à decisão. Ferramenta de apoio ao consultor —
NÃO substitui o julgamento consultivo. Todas as premissas explicitamente rotuladas [HIPÓTESE].

## Abertura ao Consultor
```
Fase 4 de 6 — Laboratório de Simulação | Artefatos: N | ~30–60 min

Diagnóstico aprovado (Gate G2 — [data]).
Agora vamos simular cenários para apoiar a decisão estratégica.
```

## Princípio de Design

Esta fase é uma ferramenta de apoio. Cada output é framed como:
"Dado este conjunto de premissas [HIPÓTESE], o modelo projeta..."

Nunca apresentar cenários como previsões ou verdades. Sempre com caveats epistêmicos.

## Passo 1: Configuração de Simulação (G-I5)

```
Quais dimensões você quer simular para este cliente?

  a) Modelos de negócio — estrutura de receita, unit economics, margens
  b) Comportamento do consumidor — ICP refinement, churn, LTV, elasticidade
  c) Cenários estratégicos — pessimista / conservador / otimista
  d) ICPs alternativos — perfis de cliente ideais alternativos a testar
  e) Combinação de dimensões — escolha múltipla (ex: "a, c")

Digite a(s) letra(s) desejada(s).
```

Processar seleção. Preparar parâmetros de entrada para cada dimensão escolhida.

## Passo 2: Coleta de Parâmetros por Dimensão

### Dimensão (a) — Modelos de Negócio
```
Forneça os dados base (aproximações são aceitas):
1. Receita mensal atual (ou faixa): R$___
2. Número de clientes ativos: ___
3. Ticket médio por cliente: R$___
4. Custo fixo mensal: R$___
5. Custo variável por cliente/venda: R$___
```

### Dimensão (b) — Comportamento do Consumidor
```
1. Taxa de churn mensal atual: ___%
2. Tempo de vida médio do cliente (meses): ___
3. CAC (Custo de Aquisição de Cliente): R$___
4. Frequência de compra (mensal/trimestral/anual): ___
```

### Dimensão (c) — Cenários Estratégicos
```
Definir 3 cenários a simular:
  Pessimista: [qual variação negativa — ex: "churn +30%, receita -20%"]
  Conservador: [situação base — ex: "manter métricas atuais"]
  Otimista: [qual melhoria — ex: "churn -20%, ticket +15%"]
```

### Dimensão (d) — ICPs Alternativos
```
Descreva o ICP alternativo a explorar:
  Segmento: ___
  Ticket estimado: R$___
  Canal de aquisição: ___
  Hipótese de conversão: ___%
```

## Passo 3: Gerar A-10 (Simulation Phase 1)

Produzir simulação inicial com resumo inline:

```markdown
# A-10 — Simulação Fase 1

## Premissas Utilizadas
[lista de todos os parâmetros com [HIPÓTESE] em cada um]

## Dimensão [X]: [nome]
### Cenário Pessimista [HIPÓTESE]
| Métrica | Valor Atual | Projeção 6m | Projeção 12m |

### Cenário Conservador [HIPÓTESE]
| Métrica | Valor Atual | Projeção 6m | Projeção 12m |

### Cenário Otimista [HIPÓTESE]
| Métrica | Valor Atual | Projeção 6m | Projeção 12m |

## Principais Insights [INFERÊNCIA]
[3–5 observações derivadas da comparação dos cenários]
```

Exibir resumo ao consultor. Oferecer aprofundamento.

## Passo 4: Aprofundamento (opcional)

```
Deseja aprofundar algum cenário específico?

  a) Sim — Cenário Pessimista: detalhar causas e mitigações
  b) Sim — Cenário Otimista: detalhar alavancas e pré-requisitos
  c) Sim — Simulação adicional: inserir nova dimensão
  d) Não — simulação atual é suficiente

Digite a letra da opção.
```

Se a/b/c: gerar A-11 (Simulation Phase 2) com granularidade adicional.

### A-11 — Simulation Phase 2 (se produzida)
```markdown
# A-11 — Simulação Fase 2 (Aprofundamento)

## Cenário Aprofundado: [nome]
## Análise de Sensibilidade [HIPÓTESE]
[variação de cada parâmetro e impacto no resultado]

## Alavancas de Mudança
[o que o cliente pode fazer para mover de pessimista → conservador → otimista]

## Premissas Críticas a Validar
[lista das hipóteses de maior impacto sobre o resultado]
```

## Gate G3 — Verificação Automática

Antes de avançar para Fase 5:
- [ ] Pelo menos A-10 produzido
- [ ] Todas as premissas de simulação rotuladas [HIPÓTESE]
- [ ] Consultor confirmou que escopo de simulação é suficiente

Confirmação do consultor:
```
A simulação atende ao escopo necessário para este caso?
  Sim → avançar para compilação (Fase 5)
  Não → detalhar o que falta
```

## Conclusão da Fase

```
Fase 4 concluída.
Cenários gerados em escala. Construir isso manualmente levaria entre 3 e 6 horas de modelagem.

Artefatos produzidos: A-10[, A-11]
Próxima fase: Fase 5 — Compilação do Dossiê
```

Atualizar manifest: current_phase=5, artifacts A-10/A-11, G3 aprovado.

## Definição de Pronto (Fase 4)

- [ ] Pelo menos A-10 produzido
- [ ] Todas as premissas de simulação rotuladas [HIPÓTESE]
- [ ] Consultor confirmou que escopo de simulação é suficiente
- [ ] manifest.yaml atualizado: A-10/A-11, G3 aprovado

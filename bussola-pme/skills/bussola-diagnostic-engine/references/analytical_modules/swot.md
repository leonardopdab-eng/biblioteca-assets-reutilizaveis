# Módulo: SWOT (Análise Estratégica)

## Quando usar
- Cliente precisa de visão de posicionamento estratégico antes de diagnóstico operacional
- Mudança de mercado, entrada de concorrentes, ou reposicionamento de produto/serviço
- Decisão estratégica importante (nova vertical, pivô, expansão)
- **Sinal trigger**: "análise estratégica", "posicionamento", "concorrência", "mercado", "oportunidades"

## Inputs necessários
- Descrição do segmento e produto/serviço em intake_normalized_v2
- Contexto competitivo (mesmo que hipotético)
- Horizonte de tempo para análise (trimestral vs. anual)

## Processo de aplicação

1. **Forças (S)** — O que a empresa faz melhor que concorrentes? (interno, controlável)
2. **Fraquezas (W)** — Onde a empresa é inferior ou vulnerável? (interno, controlável)
3. **Oportunidades (O)** — Fatores externos favoráveis que podem ser aproveitados
4. **Ameaças (T)** — Fatores externos adversos que podem prejudicar
5. **Cruzamentos estratégicos**:
   - S+O: Como usar forças para aproveitar oportunidades?
   - S+T: Como usar forças para mitigar ameaças?
   - W+O: Como superar fraquezas para aproveitar oportunidades?
   - W+T: Vulnerabilidades críticas (W+T simultâneo = zona de risco)

## Output esperado

```markdown
## SWOT — BP-001 (Agência B2B)

### Forças
- Relacionamento próximo com clientes atuais [FATO — NPS médio 8.5 declarado]
- Especialização em segmento B2B tech [FATO — 80% da carteira neste segmento]
- Time pequeno com agilidade operacional [INFERÊNCIA — 6 pessoas, ciclos curtos]

### Fraquezas
- Dependência de 3 clientes (60% do faturamento) [FATO — declarado pelo sócio]
- Ausência de processo de prospecção estruturado [HIPÓTESE — sem pipeline ativo]
- Sem posicionamento diferenciado documentado [HIPÓTESE — site genérico]

### Oportunidades
- Mercado B2B SaaS em crescimento [INFERÊNCIA — tendência de mercado]
- Demanda por consultoria de crescimento em PMEs [HIPÓTESE — observação do sócio]

### Ameaças
- Concorrentes maiores com estrutura de vendas consolidada [FATO — mencionado pelo cliente]
- Possível saída de cliente âncora [HIPÓTESE — sinais de insatisfação]

### Cruzamentos
- **S+O** (Aproveitar): Usar especialização B2B para capturar demanda SaaS em crescimento
- **W+T** (Risco crítico): Dependência alta + possível saída de âncora = risco de caixa imediato
```

## Template de saída

```yaml
strengths: [{claim: "string", label: FATO|INFERÊNCIA|HIPÓTESE}]
weaknesses: [{claim: "string", label: FATO|INFERÊNCIA|HIPÓTESE}]
opportunities: [{claim: "string", label: FATO|INFERÊNCIA|HIPÓTESE}]
threats: [{claim: "string", label: FATO|INFERÊNCIA|HIPÓTESE}]
crossings:
  so: "string"
  st: "string"
  wo: "string"
  wt: "string"
critical_risk: "W+T crossing summary"
```

## Limitações

- **Não substitui diagnóstico causal** — SWOT é contexto estratégico, não causa raiz
- **Qualidade depende de informações de mercado** — muito do SWOT pode ser [HIPÓTESE]
- **Não use** para problemas puramente operacionais (use Ishikawa ou 5 Porquês)
- **Atualização**: SWOT tem validade de ~6 meses em mercados dinâmicos

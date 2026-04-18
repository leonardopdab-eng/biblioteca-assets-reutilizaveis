# Catálogo de Simulações — Bússola PME

## 1. Pricing Sensitivity (pricing_sensitivity.py)

**Quando usar**: Cliente quer entender impacto de mudança de preço em receita e margem.
**Variáveis necessárias**: preço base, elasticidade-preço, custos fixos mensais, % custo variável.
**Interpretação**: O ponto ótimo é onde margem × volume maximiza lucro líquido. Lembrar que elasticidade é hipótese — validar com dados históricos.
**Limitação**: Assume curva de demanda linear. Não captura efeitos de mercado (concorrência, sazonalidade).

## 2. Funnel Conversion (funnel_simulator.py)

**Quando usar**: Cliente quer projetar receita ou entender gargalo no funil de vendas.
**Variáveis necessárias**: leads mensais, taxas de conversão por etapa, ticket médio.
**Interpretação**: O cenário realista é a projeção base; pessimista e otimista delimitam o range de incerteza. Gargalo = etapa com menor taxa de conversão.
**Limitação**: Assume taxas constantes por etapa. Não captura sazonalidade ou efeitos de marketing.

## 3. Capacity Scenarios (capacity_scenarios.py)

**Quando usar**: Cliente quer saber quando vai atingir o limite de capacidade e se expansão compensa.
**Variáveis necessárias**: capacidade atual, % de crescimento mensal da demanda, custo de expansão.
**Interpretação**: `rupture_month` indica quando a demanda supera capacidade. Payback da expansão indica retorno do investimento em capacidade adicional.
**Limitação**: Assume crescimento linear constante — raramente fiel à realidade.

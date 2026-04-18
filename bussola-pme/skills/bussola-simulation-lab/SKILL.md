---
name: bussola-simulation-lab
description: >
  Use this skill for on-demand business and consumer variable simulation within
  a Bússola PME case. Activate on "simular cenários de preço", "projetar funil
  de vendas", "simular capacidade", "análise de sensibilidade", "o que acontece
  se mudar o preço para X", "quanto preciso vender para atingir Y", "simular
  retenção de clientes". Can be called between phases 4 and 5 or at any point
  during the case. Does NOT modify existing case artifacts — produces simulation
  report only. All simulation assumptions are labeled [HIPÓTESE]. Uses
  ask_user_input_v0 to collect scenario variables interactively.
compatibility:
  tools: [ask_user_input_v0, visualize:show_widget]
dependencies: [numpy]
---

# bussola-simulation-lab

## Propósito

Simulações quantitativas on-demand para suporte a decisões durante o caso Bússola PME. Produz apenas relatório de simulação — nunca modifica artefatos existentes.

## Simulações disponíveis

| Simulação | Script | Inputs | Output |
|-----------|--------|--------|--------|
| Pricing sensitivity | pricing_sensitivity.py | preço base, elasticidade, custos | curva receita × preço × margem |
| Funnel conversion | funnel_simulator.py | leads, taxas por etapa, ticket | receita projetada por cenário |
| Capacity scenarios | capacity_scenarios.py | capacidade atual, demanda, expansão | break-even de expansão |

## Fluxo

1. Identificar tipo de simulação a partir da solicitação
2. Coletar variáveis via `ask_user_input_v0` (pré-preencher do intake se disponível)
3. Executar script de simulação
4. Gerar `simulation_report.md` com cenários otimista/realista/pessimista
5. Renderizar widget interativo via `visualize:show_widget`
6. Labels `[HIPÓTESE]` em toda premissa assumida

## Regras

- Toda premissa assumida → label `[HIPÓTESE]`
- Nunca modifica `plano_acao.md` ou outros artefatos do caso
- Resultados são consultivos — decisão permanece com o consultor
- Pode ser chamada entre fases 4 e 5 ou a qualquer momento

## Dependências

```bash
pip install --break-system-packages numpy
```

## Evals

```json
[
  {"id": 1, "prompt": "Simula o que acontece se eu mudar o preço de R$500 para R$700.",
   "expected": "Coleta variáveis via ask_user_input_v0, roda pricing_sensitivity, exibe widget.", "should_trigger": true},
  {"id": 2, "prompt": "Simula sem me perguntar nada, usa os dados do caso.",
   "expected": "Preenche do intake_normalized, pergunta só o que falta.", "should_trigger": true},
  {"id": 3, "prompt": "Gera o plano de ação baseado na simulação.",
   "expected": "NÃO gera plano. Fornece relatório. plano_acao é do diagnostic-engine.", "should_trigger": false}
]
```

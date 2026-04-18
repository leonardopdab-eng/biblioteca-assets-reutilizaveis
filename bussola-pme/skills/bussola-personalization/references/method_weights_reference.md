# Method Weights Reference — Bússola PME

## O que cada peso controla

### `normalization` (0.0–1.0)
Controla a profundidade de análise de gaps no intake (Fase 2).
- **Baixo (< 0.15)**: Gap analysis superficial; apenas campos obrigatórios checados
- **Médio (0.15–0.25)**: Análise padrão; gaps documentados com impact e recommended_action
- **Alto (> 0.25)**: Análise profunda; gaps cruzados com fontes externas, inferências marcadas

### `diagnosis` (0.0–1.0)
Controla o número de módulos analíticos ativados e a profundidade do problem_tree.
- **Baixo (< 0.25)**: 1 módulo primário, problem_tree com 3 causas nível-1
- **Médio (0.25–0.35)**: 1 módulo primário + 1 secundário, 5 causas nível-1
- **Alto (> 0.35)**: Até 3 módulos, problem_tree completo com nível-2, hypotheses_log detalhado

### `prioritization` (0.0–1.0)
Controla a granularidade da matriz de priorização.
- **Baixo (< 0.20)**: Escala 1–3, agrupamento por tertis
- **Médio (0.20–0.30)**: Escala 1–5, agrupamento por quintis (padrão)
- **Alto (> 0.30)**: Escala 1–10, agrupamento por decis, justificativa por item

### `action_plan` (0.0–1.0)
Controla o nível de detalhe das ações no plano.
- **Baixo (< 0.20)**: owner + deadline + KPI (mínimo obrigatório)
- **Médio (0.20–0.30)**: + contexto e critério de sucesso
- **Alto (> 0.30)**: 5W2H completo (what, why, where, when, who, how, how_much)

---

## Regra da soma

```
sum(method_weights.values()) deve ser 1.0 ± 0.01
```

O validador `config_schema_validator.py` rejeita configs com soma fora desta faixa.

---

## Perfis calibrados

### Consultor de agências B2B
Ênfase em diagnóstico (entender causa do problema) e priorização (foco em Pareto + JTBD).

```yaml
method_weights:
  normalization: 0.20
  diagnosis: 0.40
  prioritization: 0.25
  action_plan: 0.15
```

**Raciocínio**: Agências B2B frequentemente têm causas raiz não óbvias (pipeline, posicionamento, ICP). Diagnóstico profundo antes de qualquer plano de ação é crítico.

### Consultor de operações industriais
Ênfase em análise causal (Ishikawa, 5 Porquês) e plano de ação detalhado (5W2H).

```yaml
method_weights:
  normalization: 0.15
  diagnosis: 0.35
  prioritization: 0.20
  action_plan: 0.30
```

**Raciocínio**: Operações industriais têm processos documentáveis. Planos de ação com 5W2H são executados por equipes operacionais que precisam de instruções precisas.

### Consultor estratégico genérico
Pesos balanceados para máxima flexibilidade.

```yaml
method_weights:
  normalization: 0.25
  diagnosis: 0.25
  prioritization: 0.25
  action_plan: 0.25
```

**Raciocínio**: Perfil neutro para consultores que atendem segmentos variados e preferem calibrar caso a caso.

---

## Como calibrar para um novo caso

1. Identificar o tipo predominante de problema do cliente
2. Verificar se o cliente tem documentação prévia (reduz peso de normalization)
3. Verificar complexidade organizacional (aumenta peso de diagnosis)
4. Verificar maturidade da equipe executora (aumenta peso de action_plan se precisar de mais detalhe)
5. Ajustar e verificar soma = 1.0

**Exemplo BP-001** (agência B2B, 6 pessoas, pipeline caindo):
- Causa raiz desconhecida → diagnosis alto (0.40)
- Equipe pequena, menos burocracia → action_plan pode ser simples (0.15)
- Intake com gaps esperados → normalization moderado (0.20)
- Priorização importante para focar → prioritization moderado (0.25)

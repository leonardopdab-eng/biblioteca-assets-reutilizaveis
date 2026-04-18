# Seletor de Módulos Analíticos — Bússola PME

## Guia de quando usar cada módulo

### 5 Porquês
**Use quando**: Causa raiz desconhecida, problema recorrente, cliente descreve sintoma sem origem
**Sinal**: "não sabemos por que acontece", "continua mesmo depois que tentamos resolver"
**Não use**: Múltiplas causas independentes, problema estratégico mal-definido
**Combina com**: Ishikawa (quando há múltiplas dimensões da causa)

---

### Pareto
**Use quando**: Múltiplos problemas sem foco, dados quantitativos disponíveis
**Sinal**: "temos 10 problemas, não sabemos por onde começar"
**Não use**: Apenas 1–2 problemas, sem métricas comparáveis
**Combina com**: Esforço×Impacto (para priorização após identificar os 20% críticos)

---

### SWOT
**Use quando**: Decisão estratégica (reposicionamento, expansão), mudança de mercado
**Sinal**: "análise de mercado", "posicionamento", "concorrência entrando"
**Não use**: Problemas puramente operacionais, diagnóstico inicial sem contexto estratégico
**Combina com**: Nada diretamente — SWOT é contexto, não diagnóstico causal

---

### 5W2H
**Use quando**: Plano de ação definido mas com baixa especificidade, equipe precisa de instruções claras
**Sinal**: "como executar", "quem faz o quê", "plano muito vago"
**Não use**: Ações estratégicas de alto nível, quando deliverable_depth != deep
**Combina com**: PDCA (para melhorias de processo com ciclo definido)

---

### PDCA
**Use quando**: Processo existente que precisa de melhoria contínua, problema recorrente em ops
**Sinal**: "melhorar processo", "ciclo de melhoria", "padronizar"
**Não use**: Sem processo existente, para diagnóstico inicial
**Combina com**: 5 Porquês (para identificar causa dentro do PLAN do PDCA)

---

### Ishikawa
**Use quando**: Problema sistêmico com múltiplas causas independentes em dimensões diferentes
**Sinal**: "causas em diferentes áreas", "problema complexo", "não é uma causa só"
**Não use**: Problema com causa linear óbvia (use 5 Porquês), menos de 3 categorias relevantes
**Combina com**: 5 Porquês (para aprofundar cada galho da espinha)

---

### JTBD
**Use quando**: Produto/serviço com churn sem motivo claro, reposicionamento de oferta
**Sinal**: "por que clientes compram", "churn sem motivo", "proposta de valor fraca"
**Não use**: Diagnóstico de operações internas, sem acesso a entrevistas com clientes
**Combina com**: Pareto (para priorizar jobs identificados)

---

### Esforço × Impacto
**Use quando**: Lista de iniciativas definidas precisando de sequência, quick wins necessários
**Sinal**: "o que fazer primeiro", "quick wins", "priorização rápida"
**Não use**: Sem lista de iniciativas definidas, sem estimativas de esforço/impacto
**Combina com**: Pareto (para identificar os 20% antes de priorizar)

---

## Casos clássicos de combinação

| Situação | Módulo 1 | Módulo 2 |
|----------|----------|----------|
| "Causa desconhecida + múltiplos sintomas" | Ishikawa | 5 Porquês |
| "Vários problemas + precisamos focar" | Pareto | Esforço×Impacto |
| "Processo ruim + queremos melhorar" | PDCA | 5W2H |
| "Churn + não sabemos por que clientes vão" | JTBD | 5 Porquês |

## Caso BP-001 (referência)

**Problema**: Pipeline caindo 40%, causa desconhecida
**Módulo escolhido**: 5 Porquês (causa raiz desconhecida é o sinal principal)
**Módulo secundário**: Pareto (há múltiplos sintomas identificados pelo cliente)
**Raciocínio do module_router**: keyword "causa desconhecida" + "não sabemos por que" → 5_whys, confidence 0.78

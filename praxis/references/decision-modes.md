# Decision Modes — Praxis

## Visão Geral
Cinco modos para tarefas cognitivas de alto risco em decisões estratégicas.
Usado na Fase 3 para análise de impacto e recomendações com consequências relevantes.
Carregar conforme a natureza da tarefa — NÃO aplicar scoring em tarefas exploratórias.

---

## Regra de Roteamento

Antes de aplicar qualquer modo, identificar a tarefa cognitiva:

| Pergunta de diagnóstico | Modo correto |
|---|---|
| "Ainda estamos mapeando o espaço do problema?" | EXPLORE |
| "Temos uma oportunidade específica para avaliar?" | EVALUATE |
| "Precisamos alocar foco entre opções concretas?" | DECIDE |
| "A direção foi aprovada — qual o teste?" | EXECUTE |
| "O resultado veio — o que aprendemos?" | REVIEW |

**Erro mais comum**: forçar EVALUATE em tarefa EXPLORE. Resultado: falsa precisão.

---

## Modo 1: EXPLORE

**Quando usar**: mapeamento inicial do espaço sem compromisso prematuro.
Problema ou oportunidade ainda não bem definido.

**Input necessário**: briefing bruto, sintomas, contexto setorial.

**Processo**:
1. Listar todos os sinais relevantes sem julgar
2. Agrupar por tema ou domínio
3. Identificar tensões e contradições
4. Mapear o que não sabemos

**Output**: `SIGNAL MAP`
```
| Sinal | Domínio | Intensidade | Fonte | Relação com outros |
```
Ou `CANDIDATE SET`: lista de hipóteses abertas sem scoring.

**Nunca usar EXPLORE para**: decisões com prazo imediato, alocação de recurso.

---

## Modo 2: EVALUATE

**Quando usar**: uma oportunidade, solução ou hipótese específica para avaliar.

**Input necessário**: definição clara do item a avaliar, critérios relevantes.

**Processo** (em ordem obrigatória):
1. **Falsificação primeiro**: 3 razões por que pode falhar antes de qualquer suporte
2. Aplicar critérios de avaliação relevantes ao contexto
3. Verificar premissas: quais são hipóteses vs fatos
4. Calcular ou estimar impacto e viabilidade
5. Produzir recomendação com nível de confiança

**Output**: `OPPORTUNITY CARD` + `EVALUATION SHEET`
```
OPPORTUNITY CARD:
  Item: [nome]
  Tese: [hipótese de valor]
  Riscos principais: [3 falsificações]
  Recomendação: [avaliar / avançar / descartar]
  Confiança: [alta/média/baixa] — baseado em [fonte epistêmica]
```

**Nunca usar EVALUATE para**: espaços ainda inexplorados (use EXPLORE primeiro).

---

## Modo 3: DECIDE

**Quando usar**: alocar foco ou recursos entre opções concretas já avaliadas.

**Input necessário**: conjunto de opções avaliadas, restrições, critérios de prioridade.

**Processo**:
1. Confirmar que todas as opções passaram por EVALUATE
2. Aplicar critério de corte (o que elimina automaticamente?)
3. Ordenar por relação custo-benefício ou urgência
4. Definir a ordem de foco — não apenas "quais", mas "em que sequência"

**Output**: `DECISION OBJECT` + `FOCUS ORDER`
```
DECISION OBJECT:
  Contexto: [situação da decisão]
  Opções disponíveis: [lista]
  Critério de priorização: [explicitar]
  Decisão: [opção escolhida]
  Ordem de execução: [1ª, 2ª, 3ª...]
  Revisão sugerida em: [data ou evento gatilho]
```

**Nunca usar DECIDE para**: exploração inicial ou avaliação de uma única opção.

---

## Modo 4: EXECUTE

**Quando usar**: direção aprovada via DECIDE. Transformar decisão em teste delimitado.

**Input necessário**: DECISION OBJECT aprovado, recursos disponíveis, horizonte.

**Processo**:
1. Definir o menor teste que valida a hipótese central
2. Especificar o que será medido e em que prazo
3. Definir critério de sucesso e critério de parada
4. Atribuir responsáveis e recursos

**Output**: `TEST CARD` + `ACTION SPEC`
```
TEST CARD:
  Hipótese testada: [texto]
  Ação: [o que fazer]
  Duração: [prazo]
  Métrica de sucesso: [KPI + threshold]
  Critério de parada: [quando interromper]
  Responsável: [nome/cargo]
  Recursos: [horas/R$]
```

---

## Modo 5: REVIEW

**Quando usar**: após execução de um teste ou ciclo. Reconciliar resultado vs hipótese.

**Input necessário**: TEST CARD original + resultados reais.

**Processo**:
1. Comparar resultado real vs métrica de sucesso esperada
2. Identificar desvios e causas
3. Reclassificar hipóteses originais: confirmada / refutada / inconclusiva
4. Definir próxima iteração

**Output**: `LEARNING LOG` + `RECLASSIFICATION`
```
LEARNING LOG:
  Hipótese original: [texto]
  Resultado obtido: [dados]
  Status: confirmada | refutada | inconclusiva
  Causa do desvio (se houver): [análise]
  Reclassificação epistêmica: [FATO / INFERÊNCIA / HIPÓTESE]
  Próxima iteração: [ação ou novo teste]
```

---

## Integração com Fase 3

Na Fase 3 (Análise Diagnóstica), os modos são aplicados assim:

- **EXPLORE**: início da normalização de dados (A-05) — mapear o espaço do problema
- **EVALUATE**: durante seleção de frameworks e análise de root causes
- **DECIDE**: durante priorização (GUT, Esforço×Impacto) — qual ação primeiro
- **EXECUTE**: geração do plano de ação 5W2H — transformar decisão em ação
- **REVIEW**: aplicável em Cenário B (revisão) — reconciliar plano anterior com resultado

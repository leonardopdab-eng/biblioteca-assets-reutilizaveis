# B-Frames Tiers — Praxis

## Visão Geral
Três profundidades de análise. Selecionadas pelo consultor via G-I4 no início da Fase 3.
Cada tier produz um artefato diferente: A-07 (Básico), A-08 (Lean), A-09 (Full).

---

## Guia de Seleção de Tier

| Sinal | Tier recomendado |
|---|---|
| Primeiro contato, orçamento limitado, reunião exploratória | Básico |
| Engajamento contratado, problema razoavelmente definido | Lean |
| Diagnóstico completo contratado, cliente quer dossiê completo | Full |
| Cenário C (proposta rápida) | Não se aplica — pular Fase 3 |
| Cenário B (revisão) | Lean por padrão |
| Cenário A (diagnóstico completo) | Full por padrão |

---

## Tier 1: Básico (A-07)

### Quando usar
- Prospect em avaliação, não cliente contratado ainda
- Tempo disponível: 1–2 horas de trabalho consultivo
- Objetivo: apresentar direção, não prescrever solução

### Componentes obrigatórios
1. Problema principal (1 parágrafo, baseado em primary_problem de A-01)
2. Três causas raiz (listadas com rótulo epistêmico)
3. Priorização simples via GUT (Gravidade, Urgência, Tendência)
4. Uma recomendação de ação imediata

### Estrutura de saída (1–2 páginas)
```
# Diagnóstico Básico — [company_name]

## Problema Central
[primary_problem em linguagem executiva] [FATO/INFERÊNCIA]

## Causas Identificadas
1. [causa] [rótulo epistêmico]
2. [causa] [rótulo epistêmico]
3. [causa] [rótulo epistêmico]

## Priorização (GUT)
| Causa | G | U | T | Score |
| [causa 1] | N | N | N | NN |

## Recomendação Imediata
[ação específica com responsável sugerido]
```

### Frameworks aplicados
- GUT Matrix para priorização
- SCQA para estruturar o problema
- Máximo 1 framework adicional se necessário

---

## Tier 2: Lean (A-08)

### Quando usar
- Engajamento confirmado ou em negociação avançada
- Tempo disponível: 2–4 horas de trabalho consultivo
- Objetivo: diagnóstico sólido com plano acionável

### Componentes obrigatórios
1. Problema principal com contexto setorial
2. Análise completa de causa raiz (5 Whys ou Ishikawa conforme sinal)
3. Matriz de prioridade (GUT + Esforço×Impacto)
4. Plano de ação 5W2H (top 3 ações)
5. Indicadores de acompanhamento

### Estrutura de saída (3–5 páginas)
```
# Diagnóstico Lean — [company_name]

## Contextualização
## Problema Central e Causas Raiz
## Análise [framework selecionado]
## Matriz de Prioridades
| Iniciativa | Impacto | Esforço | Prioridade |
## Plano de Ação 5W2H
| O quê | Por quê | Quem | Quando | Onde | Como | Quanto |
## Indicadores de Acompanhamento
```

### Frameworks aplicados
- 5 Whys ou Ishikawa (causa raiz)
- GUT + Esforço×Impacto (priorização)
- 5W2H (plano de ação)
- SWOT simplificado (se problema tiver dimensão estratégica)

---

## Tier 3: Full (A-09)

### Quando usar
- Diagnóstico completo contratado (Cenário A)
- Tempo disponível: 4–8 horas de trabalho consultivo
- Objetivo: dossiê completo com múltiplas perspectivas

### Componentes obrigatórios
1. Contextualização completa (empresa, segmento, mercado)
2. Análise de causa raiz completa (múltiplos frameworks)
3. Análise estratégica (SWOT + Porter 5 Forças se relevante)
4. Análise PESTEL para fatores externos
5. Matriz de prioridades completa (GUT + Esforço×Impacto + TOC)
6. Plano de ação 5W2H completo (todas as iniciativas prioritárias)
7. OKRs para as iniciativas principais
8. Cenários (pessimista/base/otimista — entradas para Fase 4)
9. Trilha epistêmica completa

### Estrutura de saída (8–15 páginas)
```
# Diagnóstico Executivo — [company_name]

## 1. Contextualização e Situação
## 2. Diagnóstico do Problema Central
### 2.1 Causa Raiz (5 Whys / Ishikawa)
### 2.2 Análise MECE do Espaço do Problema
## 3. Análise Estratégica
### 3.1 SWOT + Estratégias Cruzadas
### 3.2 Porter 5 Forças (se aplicável)
### 3.3 PESTEL — Fatores Externos Relevantes
## 4. Priorização de Iniciativas
### 4.1 Matriz GUT
### 4.2 Esforço × Impacto
### 4.3 Restrição Crítica (TOC)
## 5. Plano de Ação
### 5.1 5W2H — Iniciativas Prioritárias
### 5.2 OKRs por Iniciativa
### 5.3 Cronograma Sprint
## 6. Cenários e Premissas (input Fase 4)
## Apêndice: Trilha Epistêmica
```

### Frameworks aplicados
Todos os aplicáveis do `references/framework-library.md`, roteados pelo tipo de problema.
Mínimo: 5 Whys + SWOT + GUT + 5W2H + OKR.

---

## Personalização de Amostra de Dados

Todos os tiers aceitam personalização via G-I3 (injeção de metodologia):
- Frameworks proprietários do consultor adicionados à análise
- Benchmarks setoriais específicos injetados
- Pesos analíticos customizados (ex: priorizar custo vs receita)
- Fontes de referência adicionais

A injeção de metodologia enriquece o tier sem mudar sua profundidade base.

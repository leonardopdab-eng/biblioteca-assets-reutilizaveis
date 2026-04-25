# Executive XLS Template — A-OPS Specification
<!-- Especificação das abas e colunas para generate_executive_xls.py -->
<!-- Este arquivo é a referência de design para o arquivo .xlsx gerado. -->

---

## Visão Geral

| Aba | Objetivo | Linhas esperadas | Cor da aba |
|---|---|---|---|
| Resumo Executivo | Metadados do caso | 15 rows | #2E7D9B (accent) |
| Diagnóstico | Árore de problemas e prioridades | 5–20 rows | #5C6B7A (neutral) |
| Plano de Ação | 5W2H completo | 1–10 rows por ação | #2E7D9B (accent) |
| Simulação | Matriz de cenários | 5–10 metrics × 3 scenarios | #5C6B7A (neutral) |
| Próximos Passos | Ações imediatas | 3–10 rows | #2E7D9B (accent) |

---

## Aba 1: Resumo Executivo

**Colunas**: A=Campo, B=Valor
**Linha de cabeçalho**: fundo #1B2A4A, texto branco, Inter 10pt bold
**Linhas de dados**: alternadas branco / #F5F7FA

Campos obrigatórios (em ordem):
1. Case ID
2. Consultor
3. Empresa do Consultor
4. Cliente
5. Segmento
6. Tamanho da Equipe
7. Receita Anual (faixa)
8. Decisores
9. Cenário (A/B/C)
10. Fase Atual
11. Criado em
12. Atualizado em
13. Gates Aprovados
14. Gates Pendentes
15. Total de Artefatos

**Largura das colunas**: A=30 chars, B=60 chars

---

## Aba 2: Diagnóstico

**Colunas**:
| Coluna | Header | Largura | Tipo |
|---|---|---|---|
| A | # | 5 | int |
| B | Problema / Causa | 50 | texto |
| C | Rótulo Epistêmico | 20 | enum: [FATO]/[INFERÊNCIA]/[HIPÓTESE] |
| D | Gravidade (G) | 12 | int 1–5 |
| E | Urgência (U) | 12 | int 1–5 |
| F | Tendência (T) | 12 | int 1–5 |
| G | Score GUT | 12 | int (D×E×F) |
| H | Prioridade | 12 | Alta/Média/Baixa |

**Ordenação**: por Score GUT descendente
**Formatação condicional**:
- Prioridade Alta: fundo #FFE8E8
- Prioridade Média: fundo #FFF8E8
- Prioridade Baixa: fundo #F5F7FA

---

## Aba 3: Plano de Ação

**Colunas**:
| Coluna | Header | Largura |
|---|---|---|
| A | # | 5 |
| B | O quê (What) | 40 |
| C | Por quê (Why) | 40 |
| D | Quem (Who) | 20 |
| E | Quando (When) | 15 |
| F | Onde (Where) | 15 |
| G | Como (How) | 35 |
| H | Quanto (How Much) | 15 |
| I | Status | 12 |
| J | KPI de Acompanhamento | 25 |

**Status values**: Pendente / Em Andamento / Concluído / Bloqueado
**Formatação condicional por status**:
- Concluído: fundo #E8F5E9
- Bloqueado: fundo #FFEBEE
- Em Andamento: fundo #E3F2FD

---

## Aba 4: Simulação

**Colunas**:
| Coluna | Header | Largura |
|---|---|---|
| A | Métrica | 25 |
| B | Valor Atual | 18 |
| C | Cenário Pessimista [HIPÓTESE] | 28 |
| D | Cenário Conservador [HIPÓTESE] | 28 |
| E | Cenário Otimista [HIPÓTESE] | 28 |
| F | Premissa-Chave | 40 |
| G | Validado? | 12 |

**Nota de rodapé obrigatória** (em célula mesclada A-ultima_linha):
"Todos os cenários são projeções baseadas em premissas não validadas. Validar com dados reais."

**Métricas padrão** (podem ser editadas):
Receita Mensal, Número de Clientes, Ticket Médio, Churn Mensal (%), CAC (R$), LTV (R$), Margem Bruta (%)

---

## Aba 5: Próximos Passos

**Colunas**:
| Coluna | Header | Largura |
|---|---|---|
| A | # | 5 |
| B | Ação Imediata | 50 |
| C | Responsável | 20 |
| D | Prazo | 15 |
| E | KPI de Acompanhamento | 35 |
| F | Dependências | 30 |
| G | Status | 12 |

**Ordenação**: por prazo ascendente
**Destacar** ações com prazo nos próximos 7 dias: fundo #FFF3CD (âmbar suave)

---

## Estilos Globais (todas as abas)

```
Fonte padrão: Calibri 10pt (fallback para Inter via PDF export)
Altura mínima de linha: 18pt
Borda de célula: thin, cor #D0D7E0
Cabeçalho de coluna: fundo #1B2A4A, texto branco, negrito
Linhas alternadas: branco / #F5F7FA
Alinhamento padrão: left para texto, center para números e enums
Wrap text: ligado em todas as células
Freeze panes: primeira linha de cada aba
Print area: definir para cada aba individualmente
Print scaling: ajustar para largura (1 página de largura)
```

---

## Instruções para generate_executive_xls.py

1. Criar workbook com as 5 abas na ordem especificada
2. Aplicar estilos do design system (header navy, alternating rows)
3. Substituir cor do cabeçalho por primary_color do consultor se configurado
4. Preencher Resumo Executivo com dados de manifest.yaml
5. Preencher Diagnóstico com dados de A-07/A-08/A-09 se disponíveis, ou placeholders
6. Preencher Plano de Ação com dados do plano de A-09/A-MASTER se disponíveis
7. Preencher Simulação com A-10 se disponível
8. Preencher Próximos Passos com síntese do plano
9. Salvar como A-OPS_[client]_[case_id].xlsx

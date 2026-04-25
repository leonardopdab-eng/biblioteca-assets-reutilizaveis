# Fase 3 de 6 — Análise Diagnóstica

## Responsabilidade
Aplicar metodologia do consultor. Reduzir carga cognitiva analítica. Produzir análise estruturada
em um dos três tiers (Básico/Lean/Full) com rótulos epistêmicos completos.

## Abertura ao Consultor
```
Fase 3 de 6 — Análise Diagnóstica | Artefatos: N | ~45–90 min

Recebido: A-01 (Normalized Follow Up) — Gate G1 verificado.
Agora você vai transferir sua metodologia para a análise.
```

## Gate G1 — Verificação Automática

Antes de qualquer análise, verificar:
- A-01 tem rótulos epistêmicos em todas as afirmações
- Todos os 7 campos obrigatórios presentes ou lacunas documentadas

Se falhar: retornar à Fase 1. Nunca iniciar Fase 3 sem G1 aprovado.

## Passo 1: Injeção de Metodologia (G-I3)

```
Agora você vai transferir sua metodologia para o sistema.

Compartilhe:
  — frameworks que você usa com este tipo de cliente
  — fontes de referência ou benchmarks do setor
  — pesos analíticos (ex: priorizar custo, ou crescimento, ou retenção)
  — contexto de mercado relevante para este caso

Pode ser texto livre ou estruturado. Sem restrições de formato.
```

Processar a injeção:
- Extrair frameworks mencionados → priorizar no roteamento de módulos
- Extrair fontes → adicionar ao catálogo de Wide Search para este caso
- Extrair pesos → ajustar priorização na seleção de iniciativas
- Preservar tudo em A-05 com rótulo epistêmico [FATO] (veio do consultor)

## Passo 2: Wide Search

Executar pesquisa usando `references/wide-search-catalog.md` + fontes injetadas em G-I3:
- Dados setoriais do segmento do cliente
- Benchmarks de mercado aplicáveis
- ICP e perfil do consumidor (se relevante para o problema)

Produzir resumo inline para o consultor. Oferecer opção de exportar.
Rotular cada dado com tier epistêmico correspondente.

## Passo 3: Produzir A-05 (Normalized Data)

```markdown
# A-05 — Normalized Data
## Dados Normalizados do Cliente
[campos de A-01 com rótulos]
## Dados de Mercado e Benchmark
[resultado do Wide Search com fontes e rótulos]
## SVG / Diagrama de Situação
[representação visual da situação — ASCII ou descrição para SVG]
```

## Passo 4: Seleção de Profundidade (G-I4)

```
Qual profundidade de análise para este caso?

  a) Básico — problema + 3 causas raiz + priorização simples (1–2 páginas)
  b) Lean — causa raiz completa + matriz de prioridade + 5W2H (3–5 páginas)
  c) Full — análise completa com múltiplos frameworks + plano detalhado (8–15 páginas)

Digite a letra da opção.
```

Carregar `references/b-frames-tiers.md` para o tier selecionado.

## Passo 5: Roteamento de Módulo Analítico

Baseado no `primary_problem` e no sinal do problema:

| Sinal do problema | Módulo primário | Secundário |
|---|---|---|
| Causa raiz desconhecida | 5 Whys | Ishikawa |
| Múltiplos problemas sem foco | Pareto | Esforço×Impacto |
| Posicionamento estratégico | SWOT | Porter 5 Forças |
| Plano de baixa especificidade | 5W2H | — |
| Melhoria de processo existente | PDCA | — |
| Problema sistêmico multi-causa | Ishikawa | 5 Whys |
| Job-to-be-done não articulado | JTBD | — |
| Priorização rápida de iniciativas | Esforço×Impacto | Pareto |

Aplicar o módulo primário. Oferecer secundário após resultado.
Carregar detalhes de cada framework de `references/framework-library.md`.

## Passo 6: Aplicar Decision Intelligence

Para decisões estratégicas de alto risco durante a análise:
Carregar `references/decision-modes.md` e aplicar o modo correto:
- EXPLORE: quando o espaço do problema ainda não está mapeado
- EVALUATE: para avaliar uma hipótese ou oportunidade específica
- DECIDE: para priorizar entre iniciativas avaliadas
- EXECUTE: para transformar decisão em plano de ação
- REVIEW: se for Cenário B (revisando caso anterior)

## Passo 7: Produzir A-06 e Artefato do Tier

**A-06 — B-Frames Output**: estrutura do frame analítico com:
- Primary frame: [módulo principal aplicado]
- Problem statement refinado
- Hypothesis log: lista de hipóteses identificadas (todas com [HIPÓTESE])
- Dependency map: como os problemas se relacionam

**Tier selecionado**:
- A-07 (Básico): seguir estrutura de `references/b-frames-tiers.md#tier-1`
- A-08 (Lean): seguir estrutura de `references/b-frames-tiers.md#tier-2`
- A-09 (Full): seguir estrutura de `references/b-frames-tiers.md#tier-3`

Aplicar todos os rótulos epistêmicos em cada afirmação analítica.
O `diagnostic_working.md` (raciocínio interno) NUNCA é entregue ao cliente.

## Passo 8: Gate G2 — REVISÃO HUMANA HARDCODED

**NUNCA AUTO-AVANÇAR. Sem exceção.**

Apresentar ao consultor:
```
Diagnóstico pronto para revisão.

[Sumário: problema central, causas identificadas, ranking de prioridade]
[Trilha epistêmica: N fatos, N inferências, N hipóteses]

Revise o material acima.

Para aprovar e avançar: escreva "aprovar"
Para solicitar revisão: descreva o que ajustar
```

Se o consultor escrever "aprovar" (ou variante): registrar em manifest com timestamp.
Se o consultor descrever revisão: aplicar mudanças e reapresentar para nova revisão.

## Conclusão da Fase

```
Fase 3 concluída.
Diagnóstico estruturado com rastreabilidade epistêmica completa.
Equivalente a 4–8 horas de trabalho analítico manual de um consultor sênior.

Artefatos produzidos: A-05, A-06, A-0[7/8/9]
Próxima fase: Fase 4 — Laboratório de Simulação
```

Atualizar manifest: current_phase=4, artifacts, G2 aprovado com timestamp.

## Definição de Pronto (Fase 3)

- [ ] A-05 (Normalized Data) produzido com rótulos epistêmicos
- [ ] A-06 (B-Frames) + um de A-07/A-08/A-09 produzido
- [ ] Gate G2 recebeu aprovação humana explícita (não auto-avançado)
- [ ] manifest.yaml atualizado com timestamp de aprovação do G2

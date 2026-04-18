# Regras de Densidade — Bússola PME Artifacts

## Princípio

Artefatos muito curtos (thin) indicam diagnóstico superficial. Artefatos muito longos (overflow) comprometem usabilidade. O sistema enforça uma faixa de densidade por artefato.

## Cálculo de densidade

```
target_chars = alvo ideal de comprimento
min_chars    = target * 0.1  (thin threshold)
max_chars    = target * 1.3  (overflow threshold)
```

## As 4 ações de overflow

### summarize
Usa Claude API (`claude-sonnet-4-6`) para comprimir o artefato a ~60% mantendo estrutura e dados.
- Preserva: claims com labels, conclusões, números, itens de ação
- Remove: redundâncias, exemplos repetidos, frases de transição longas
- Fallback: se ANTHROPIC_API_KEY não disponível, usa `compress`

### compress
Regex-based: remove blocos de exemplo e justificativa, mantém dados e conclusões.
- Remove: blocos `>` (blockquotes), parágrafos iniciando com "Exemplo:", seções de justificativa
- Mantém: tabelas, listas de dados, conclusões principais
- Trunca se ainda overflow após remoções

### paginate
Divide o artefato em partes (`_part1`, `_part2`, etc.), cada uma respeitando `target_chars`.
- Divide nos limites de parágrafo (última `\n` antes do limite)
- Cada parte é um arquivo independente
- Usado para: plano_acao_cliente, playbook_operacional, diagnostic_working

### hard_cut
Trunca exatamente no limite com `[...]`. Sem adaptação. Usado APENAS para `resumo_executivo` (1 página = regra rígida).

## Quando usar cada ação

| Artefato | Por que essa ação |
|----------|------------------|
| resumo_executivo | hard_cut — 1 página é requisito de negócio |
| diagnostico_executivo | compress — preservar estrutura mas não exemplos |
| plano_acao_cliente | paginate — NUNCA cortar ações, apenas paginar |
| hypotheses_log | summarize — preservar claims com labels |
| diagnostic_working | paginate — trilha de raciocínio deve ser preservada integralmente |

## Limites thin

Artefato thin indica problema de qualidade de diagnóstico:
- `hypotheses_log` < 300 chars: diagnóstico muito superficial
- `problem_tree` < 200 chars: árvore incompleta
- `plano_acao_cliente` < 300 chars: plano muito vago

Sistema avisa mas não bloqueia em thin (apenas reporta). Overflow bloqueia entrega.

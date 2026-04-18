---
name: bussola-case1-showroom
description: >
  Use this skill to build a commercial showcase from a completed, anonymized
  Bússola PME case. Activate on "gerar showcase do Bússola", "montar case 1",
  "preparar demo comercial", "anonimizar caso para portfólio", "gerar material
  de prova social", "criar landing page do método". Requires a completed case
  with qa_checklist green as source. Produces: showcase_interactive.html,
  showcase_deck.pptx, landing_page_copy.md, one_pager.pdf, anonymization_log.md.
  Does NOT modify original case artifacts. Strong anonymization: fictional names,
  metrics rounded to ±5%, segments generalized. Do NOT use for active case work.
compatibility:
  tools: [mcp__google_drive, visualize:show_widget]
dependencies: [pyyaml]
---

# bussola-case1-showroom

## Propósito

Construir showcase comercial a partir de um caso Bússola PME concluído. Nunca usa dados reais não-anonimizados. Não modifica artefatos originais.

## Pré-condições

- Caso-fonte com `qa_checklist` 100% verde (R-S04)
- Caso com todos os artefatos de trilha cliente aprovados

## Outputs produzidos

| Arquivo | Canal | Formato |
|---------|-------|---------|
| `showcase_interactive.html` | LinkedIn / landing | React (visualize:show_widget) |
| `showcase_deck.pptx` | Sales call | 7 slides |
| `landing_page_copy.md` | Landing | Markdown estruturado |
| `one_pager.pdf` | WhatsApp / cold | PDF |
| `anonymization_log.md` | Auditoria | Markdown |

## Nível de anonimização: strong

- Nomes de empresa → substitutos fictícios mesmo segmento
- Nomes de pessoas → nomes fictícios genéricos
- Métricas → arredondadas ±5%
- Segmento → generalizado ("agência B2B de comunicação")
- Datas → aproximadas para trimestre

## Fluxo

1. Verificar `qa_checklist` verde do caso-fonte (R-S04 — hard stop)
2. `anonymizer.py` → versão anonimizada de todos os artefatos cliente
3. `narrative_extractor.py` → beats narrativos para showcase
4. `showcase_interactive.jsx` → HTML com componente React
5. Deck: 7 slides (problema / antes / método / amostra / métricas / testemunho / CTA)
6. `landing_copy.md.j2` → copy de landing adaptado
7. `anonymization_log.md` → registro auditável de cada substituição

## Regras de Conduta

| ID | Regra |
|----|-------|
| R-S01 | Nunca usa dados reais não anonimizados |
| R-S02 | `anonymization_log.md` obrigatório — lista cada substituição |
| R-S03 | Não modifica artefatos do caso original |
| R-S04 | `qa_checklist` verde é pré-condição hard — sem exceções |

## Dependências

```bash
pip install --break-system-packages pyyaml
```

## Evals

```json
[
  {"id": 1, "prompt": "Gera o showcase do caso BP-001 para LinkedIn.",
   "expected": "Verifica qa_checklist, anonimiza, gera HTML e deck com adaptação de canal.", "should_trigger": true},
  {"id": 2, "prompt": "Monta o showcase do caso BP-002, que está na fase 5.",
   "expected": "Recusa. qa_checklist não verde — caso não concluído.", "should_trigger": true},
  {"id": 3, "prompt": "Gera o diagnóstico executivo do caso BP-003.",
   "expected": "NÃO ativa. Diagnóstico executivo é do deliverable-forge.", "should_trigger": false}
]
```

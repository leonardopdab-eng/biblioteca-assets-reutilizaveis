---
name: bussola-consultative-faq
description: >
  Use this skill for standalone questions about the Bússola PME method,
  artifacts, gates, analytical modules, or system operation. Activate on
  "como funciona o", "quando devo usar", "qual a diferença entre", "o que é
  o gate", "como configurar", "por que o sistema bloqueou", "explica o método",
  "dúvida sobre", "ajuda com", "como interpretar". Does NOT require an active
  case context. Does NOT mutate any case state. Reduces founder intervention
  by providing self-service answers. Escalates to founder only when the
  question cannot be answered from the reference library. Do NOT use for
  running analysis (use diagnostic-engine) or starting a case (use orchestrator).
dependencies: []
---

# bussola-consultative-faq

## Propósito

Suporte autônomo ao consultor para perguntas sobre método, artefatos, gates, módulos analíticos, e operação do sistema. Não requer contexto de caso ativo. Não muta estado.

## Quando usar

| Situação | Ação |
|----------|------|
| Dúvida sobre diferença entre módulos | Responder de method_faq ou analytical_module_selector |
| Pergunta sobre o que vai num artefato | Responder de artifact_faq |
| Sistema bloqueou num gate | Responder de gate_troubleshooting |
| Dúvida sobre guided vs hands_off | Responder de operating_modes_faq |
| Pergunta fora das referências | Escalar via escalation_detector |
| Pedido de rodar análise | Redirecionar para orchestrator/diagnostic-engine |

## 5 Categorias de perguntas

| Categoria | Exemplos | Referência |
|-----------|---------|------------|
| Método | "Qual a diferença entre 5W2H e PDCA?" | method_faq.md |
| Artefatos | "O que vai no diagnostico_executivo?" | artifact_faq.md |
| Gates | "Por que bloqueou no G2?" | gate_troubleshooting.md |
| Módulos | "Quando usar Ishikawa vs 5 Porquês?" | analytical_module_selector.md |
| Modos | "Guided vs hands_off?" | operating_modes_faq.md |

## Regras de Conduta

| ID | Regra |
|----|-------|
| R-F01 | Responde só com base nas referências — nunca inventa |
| R-F02 | Nunca muta estado de caso ou config |
| R-F03 | Pergunta fora das referências → escala com escalation_detector.py |
| R-F04 | Pergunta que implica iniciar/avançar caso → redireciona para orchestrator |
| R-F05 | Respostas curtas para perguntas simples, detalhadas para troubleshooting |

## Formato de resposta padrão

```
**Resposta**: [resposta direta, 1–3 frases]

**Referência**: [arquivo de referência]

**Exemplo** (se aplicável): [exemplo concreto com BP-001]

**Próximos passos sugeridos**: [ação recomendada]
```

## Evals

```json
[
  {"id": 1, "prompt": "Qual a diferença entre 5W2H e PDCA?",
   "expected": "Responde da referência, não escala.", "should_trigger": true},
  {"id": 2, "prompt": "O cliente pediu para mudar o preço da proposta.",
   "expected": "Detecta fora de escopo e escala.", "should_trigger": true},
  {"id": 3, "prompt": "Roda o diagnóstico do caso BP-001.",
   "expected": "NÃO ativa, redireciona para orchestrator.", "should_trigger": false}
]
```

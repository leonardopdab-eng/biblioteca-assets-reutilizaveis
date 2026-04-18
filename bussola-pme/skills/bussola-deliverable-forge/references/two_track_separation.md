# Separação de Trilhas — Bússola PME

## O problema que esta regra resolve

Artefatos internos contêm linguagem de incerteza, hipóteses não validadas, e raciocínio intermediário que confundem ou assustam clientes. A separação de trilhas garante que apenas conclusões validadas cheguem ao cliente.

## Strings proibidas em trilha cliente

Os seguintes termos NUNCA devem aparecer em artefatos de trilha cliente:

```
diagnostic_working
hypotheses_log
raw_hypothesis
internal_reasoning
[TRILHA INTERNA]
trilha interna
module_routing_log
assumptions_log
decision_log
intake_normalized_v2
hypothesis_propagated: true
```

## O que NUNCA cruza para cliente

| Categoria | Exemplos |
|-----------|---------|
| Nomes de artefatos internos | "ver hypotheses_log", "conforme diagnostic_working" |
| Hipóteses não validadas | H-001, H-002, raw hypotheses |
| Scores intermediários | Scores parciais de priorização, iterações |
| Conflitos não resolvidos | "Há conflito entre H-003 e H-007" |
| Raciocínio de roteamento | "Selecionamos 5_whys porque..." (interno) |
| Labels internos | `[TRILHA INTERNA]` |

## O que PODE cruzar (após Gate G5)

| O que cruza | Como aparece no cliente |
|-------------|------------------------|
| Conclusões do diagnóstico | "Identificamos 3 causas principais..." |
| Prioridades rankeadas | Tabela resumida com top 5 |
| Plano com itens aprovados | Tabela com owner/deadline/KPI |
| Hipóteses validadas | Apresentadas como "achados" sem label técnico |
| Módulo aplicado | "Utilizamos análise de causa raiz (5 Porquês)" |

## Mecanismo de verificação

`derivation_checker.py` usa lista de strings proibidas + padrões regex:

```python
FORBIDDEN_STRINGS = [
    "diagnostic_working",
    "hypotheses_log",
    "raw_hypothesis",
    "internal_reasoning",
    "[TRILHA INTERNA]",
    "trilha interna",
    ...
]

FORBIDDEN_PATTERNS = [
    r"\[TRILHA INTERNA[^\]]*\]",
    r"diagnostic_working[_\.]",
    r"internal_.*log",
    r"\braw_hypothesis\b",
]
```

## Controle no Gate G5

Gate G5 requer revisão humana dos 3 artefatos críticos:
1. `diagnostico_executivo` — verificar que não expõe hipóteses não validadas
2. `apresentacao_executiva` — verificar linguagem adequada para cliente
3. `proposta_continuidade` — verificar que não expõe vulnerabilidades internas

O consultor, ao revisar para G5, deve especificamente checar se a linguagem é adequada para o cliente.

# Módulo: 5 Porquês (5 Whys)

## Quando usar
- Causa raiz do problema é desconhecida ou não-óbvia
- Problema recorrente que retorna após "soluções" superficiais
- Cliente descreve sintoma mas não consegue articular origem
- **Sinal trigger**: "não sabemos por que", "causa desconhecida", "continua acontecendo mesmo depois de X"

## Inputs necessários
- `primary_problem` definido em intake_normalized_v2 `[FATO]`
- Pelo menos 1 dado quantitativo sobre o sintoma (ex: queda de %, tempo de ocorrência)
- Acesso ao decisor que vive o problema diariamente

## Processo de aplicação

1. **Formular o problema-raiz** como pergunta observável e específica
   - Ruim: "Por que a empresa está mal?"
   - Bom: "Por que o pipeline de vendas caiu 40% nos últimos 4 meses?"

2. **Por quê? (1ª iteração)** — Identificar a causa imediata mais direta

3. **Por quê? (2ª–5ª iterações)** — Aprofundar cada causa, marcando:
   - `[FATO]` quando baseado em dado verificável
   - `[HIPÓTESE]` quando inferido sem evidência direta

4. **Identificar causa raiz** — O último "porquê" que não tem outro porquê subjacente

5. **Verificar** — A causa raiz identificada, se resolvida, eliminaria o problema original?

6. **Registrar** no `problem_tree.md` e `hypotheses_log.md`

## Output esperado

```markdown
## 5 Porquês — BP-001 (Agência B2B)

**Problema**: Pipeline de vendas caiu 40% em 4 meses

P1: Por que o pipeline caiu?
→ Menos leads qualificados entrando [INFERÊNCIA — dados CRM mostrando queda top-of-funnel]

P2: Por que há menos leads qualificados?
→ O ICP não foi atualizado e a prospecção está mirando perfil errado [HIPÓTESE — sem doc ICP recente]

P3: Por que o ICP está desatualizado?
→ Não houve processo de revisão periódica de ICP [FATO — sócio confirmou "nunca revisamos"]

P4: Por que não há processo de revisão de ICP?
→ Responsabilidade não atribuída a ninguém; foco só em execução [HIPÓTESE]

P5: Por que a responsabilidade não está atribuída?
→ Ausência de estrutura de gestão comercial com rituais definidos [HIPÓTESE]

**Causa raiz identificada**: Ausência de estrutura de gestão comercial (rituais, ownership, métricas) [HIPÓTESE — requer validação]
```

## Template de saída (estrutura problem_tree)

```yaml
root_problem: "string"
root_label: FATO|INFERÊNCIA|HIPÓTESE
whys:
  - level: 1
    cause: "string"
    label: FATO|INFERÊNCIA|HIPÓTESE
    evidence: "string opcional"
  - level: 2
    cause: "string"
    label: FATO|INFERÊNCIA|HIPÓTESE
  # ... até level 5
root_cause: "string"
root_cause_label: FATO|INFERÊNCIA|HIPÓTESE
validation_required: true|false
```

## Limitações

- **Não use** quando há múltiplas causas independentes (use Ishikawa ou Pareto)
- **Não use** quando o problema é estratégico e mal-definido (use SWOT primeiro)
- **Cuidado**: A qualidade das respostas depende da profundidade da entrevista com quem vive o problema
- **Máximo 5 níveis**: Se precisar de mais, provavelmente está investigando a causa errada

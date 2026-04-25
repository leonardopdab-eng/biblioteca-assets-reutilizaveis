# Epistemic Labels — Praxis

## Purpose

Every claim in every analytical artifact must carry one of three epistemic labels: [FATO], [INFERÊNCIA], or [HIPÓTESE]. Labels communicate the evidential status of a claim to the consultant and, indirectly, to the client. They prevent overconfident recommendations, protect the consultant's credibility, and create an auditable reasoning trail.

Labels are not cosmetic. They govern how claims propagate across artifacts and what validation actions are required before delivery.

---

## Three Labels

### [FATO]

**Definition:** A claim that is directly observed, stated by the client as a verifiable fact, or sourced from a primary verified document or dataset. A fato is only as strong as its cited source.

**Usage rules:**
- Apply only when you can cite a specific source: a document, a client statement attributed to a named person, or a public dataset with a retrieval date.
- Do not apply to figures you derived or calculated — those are [INFERÊNCIA], even if the inputs were all fatos.
- Do not apply to industry benchmarks unless the specific publication and date are cited.
- Every fato must carry an inline source reference: `[FATO — fonte: <source>]`.

**Examples in consulting context:**

1. `Receita bruta de R$ 4,2M no exercício 2024 [FATO — DRE auditada, exercício encerrado dez/2024, fornecida pelo cliente em 14/04/2026]`
   The client provided the audited income statement. The figure is directly readable from the document — no inference required.

2. `A empresa possui 3 unidades operacionais: matriz em São Paulo, filial em Campinas e armazém em Jundiaí [FATO — declaração do sócio-diretor na sessão de briefing, 10/04/2026]`
   The client stated this directly. The statement is attributed to a named person and a dated session.

3. `Prazo médio de recebimento: 47 dias [FATO — relatório de aging do ERP, período jan–mar/2026, exportado pelo CFO e fornecido em 12/04/2026]`
   Client-exported operational data. The figure requires no inference — it is a direct read from the system record.

**Visual treatment:** Green badge in deliverables. In plain text, render as `[FATO]` immediately after the claim with source in parentheses. In client documents, surface as "os dados mostram..." without exposing bracket syntax.

**Propagation:** A fato cited in a downstream artifact retains its fato status provided the source citation travels with it. If the citation is lost, the claim degrades automatically to [INFERÊNCIA].

---

### [INFERÊNCIA]

**Definition:** A conclusion reasoned from one or more fatos. Logically derived but not directly stated in any source. Includes calculations, pattern identifications, comparisons, and trend readings applied to verified data.

**Usage rules:**
- Apply when drawing a conclusion that no source document explicitly states.
- Apply to all calculated figures (ratios, growth rates, period comparisons) even when inputs are fatos.
- Each inferência must cite the originating fato(s) by reference.
- If the reasoning chain requires more than two inferential steps, add a flag: `[INFERÊNCIA — cadeia longa, verificar raciocínio]`.
- An inferência cannot be upgraded to fato without new primary evidence.

**Examples in consulting context:**

1. `A margem bruta deteriorou 7 p.p. entre 2022 e 2024, indicando pressão de custos não repassada ao preço [INFERÊNCIA — calculado a partir de DRE 2022 [FATO] e DRE 2024 [FATO]]`
   The two revenue/cost figures are fatos; the trend and its causal interpretation are inferred.

2. `O canal digital representa 40% dos leads gerados mas menos de 15% da receita fechada — sinal de baixa taxa de conversão nesse canal [INFERÊNCIA — derivado de [FATO] relatório de leads do CRM e [FATO] receita por canal Q4/2025]`
   The disproportion is a calculated observation from two separate verified datasets. Neither dataset explicitly states conversion rate.

3. `A concentração de 62% da receita em 3 clientes cria risco de ruptura significativo caso qualquer um deles reduza volume [INFERÊNCIA — calculado a partir de [FATO] mix de faturamento por cliente, jan–dez/2025]`
   The 62% figure is derived; the risk characterization is an analytic judgment layered on top.

**Visual treatment:** Gray badge in deliverables. In plain text, render as `[INFERÊNCIA]` after the claim with originating fatos cited. In client documents, surface as "a análise indica..." or "com base nos dados disponíveis...".

**Propagation:** When cited in a downstream artifact, the originating fatos must be cited alongside. Two inferências combined do not produce a fato — the result remains [INFERÊNCIA] or may degrade to [HIPÓTESE] if the logical chain is weak.

---

### [HIPÓTESE]

**Definition:** An assumption without current supporting evidence. Plausible and worth entertaining, but unverified. Used for simulation inputs, predicted future behaviors, untested market claims, and working assumptions that drive analysis forward before evidence arrives.

**Usage rules:**
- Apply to all simulation inputs not sourced from verified data.
- Apply to all forward-looking behavioral or market assumptions.
- Apply to claims asserted by the client that cannot be corroborated within the current engagement data.
- Every hipótese must include a validation path: who validates, by when, and how.

**Examples in consulting context:**

1. `[HIPÓTESE] O reposicionamento de preço aumentará o ticket médio em 15% sem impacto material no volume. Premissa central da projeção de receita Cenário B. Validar via teste piloto — responsável: Diretora Comercial — prazo: 30/09/2026.`
   The founder believes pricing power exists. No market test has been run.

2. `[HIPÓTESE] O mercado endereçável na região Sul conta com aproximadamente 8.000 clientes potenciais. Estimativa baseada em proxy demográfico. Validar com pesquisa de campo antes de alocar capital de expansão.`
   The 8.000 figure is a proxy estimate, not a measured market count.

3. `[HIPÓTESE] O principal motivo de churn é insatisfação com tempo de resposta do suporte. Declarado pelo diretor de operações; não corroborado por pesquisa de satisfação ou análise de tickets de suporte.`
   A plausible executive hypothesis that requires evidence before driving structural decisions.

**Visual treatment:** Amber call-out box in deliverables. In plain text, render as a block prefixed with `[HIPÓTESE]`. In client documents, present in a clearly delineated "Premissa a validar" block — never inline as if established.

**Propagation rules:** A hipótese NEVER propagates as a fato or inferência. It must be re-labeled at every appearance in every artifact. If later validated with primary data, it must be explicitly upgraded to [FATO] with source citation — the upgrade is not automatic.

---

## Application Rules

1. **Unlabeled = Hipótese.** Any claim in an artifact that lacks an explicit label is treated as [HIPÓTESE] by the QA process. Absence of a label is not neutrality.

2. **Labels are permanent across versions.** Labels are never stripped when text is copied between artifacts, reformatted, or compiled into a new document.

3. **A-MASTER preserves all labels (Rule C5).** When the master document is compiled from component artifacts, every epistemic label from every component must appear in the compiled output.

4. **`diagnostic_working.md` is never delivered.** Internal reasoning files may contain speculative thinking and partially labeled claims. They never leave the internal artifact track regardless of content.

5. **Downgrade rule.** A fato whose source cannot be cited degrades automatically to [INFERÊNCIA]. An inferência whose originating fatos cannot be identified degrades to [HIPÓTESE]. Downgrade is enforced at QA (Check 5).

6. **Apêndice B — Epistemic Trail.** Every A-MASTER document includes an Apêndice B listing all labeled claims by section, with their sources (fatos), derivation paths (inferências), and validation status (hipóteses). This appendix is required for G4 QA Check 9 to pass.

---

## Label Syntax

**Inline fato:**
```
Receita anual R$ 2M [FATO — fonte: DRE 2024, fornecida pelo cliente em 10/04/2026]
```

**Inline inferência with chain:**
```
Margem operacional abaixo de 8% sinaliza risco de caixa no horizonte de 18 meses
[INFERÊNCIA — derivado de [FATO] DRE 2024 + [FATO] projeção de fluxo de caixa Q1/2026]
```

**Block hipótese:**
```
> [HIPÓTESE] Ticket médio crescerá 15% após reposicionamento.
> Base: declaração do sócio-diretor, não corroborada por dados de mercado.
> Validar: pesquisa com amostra de 50 clientes — responsável: gerente comercial — prazo: 30/06/2026.
```

---

## Common Errors to Avoid

- **Presenting inferência as fato.** "A empresa perde clientes por falta de follow-up" stated as fato when derived from churn data plus a manager interview is at best [INFERÊNCIA], often [HIPÓTESE].
- **Stripping labels when copying text.** Copy-paste from diagnostic to recommendation does not reset epistemic status. Labels travel with the claim. This is QA Check 6.
- **Overusing [FATO] to appear confident.** When everything is labeled fato, the label loses meaning and the consultant loses credibility when claims cannot be defended.
- **Using [HIPÓTESE] as a liability shield.** Labeling a claim [HIPÓTESE] does not excuse including a poorly reasoned or irresponsible assumption in a deliverable.
- **Inferência without cited originating fatos.** An inferência floating without anchors cannot be evaluated and will be flagged in QA Check 7.
- **Hipótese without a validation path.** Every [HIPÓTESE] must name who validates it, how, and by when. A floating hypothesis with no validation plan is incomplete analysis, not epistemic honesty.

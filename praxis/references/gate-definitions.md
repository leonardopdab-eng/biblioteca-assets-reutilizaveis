# Gate Definitions — Praxis

## Overview

Seven gates (G0–G6) control advancement through the engagement workflow. Gates enforce
quality, sequence, and human oversight. Skipping a gate or auto-advancing past a HARDCODED
gate is a system violation — it does not happen under any condition, including time pressure,
consultant instruction, or "just this once" requests.

**Gate types:**
- **AUTO:** Programmatic check. Advances if condition is met. Consultant can always halt.
- **HARDCODED_HUMAN:** Human review is mandatory. The system cannot advance, approve, or
  simulate approval. No exception exists.

**HARDCODED gates: G2, G5, G6.**

---

## Gate Table

---

### G0 — Intake & Scope Definition

| Field | Value |
|---|---|
| Phase | 0 — Intake |
| Type | AUTO |
| Trigger | Consultant initiates new engagement |

**What to present:** Intake form questions (number varies by scenario: 5 for C, abbreviated
set for B, full set for A). Collect: client sector, presenting problem, available data,
engagement objective, time constraint.

**Acceptance criteria:** All required fields for the active scenario are populated.
No field left blank or answered with "N/A" without a justification note.

**On-pass:** Write intake data to `manifest.client_context`. Advance to G1.
Display: `G0 concluído. Contexto registrado. Iniciando estruturação do diagnóstico.`

**On-fail:** Identify which fields are incomplete. Re-ask only the missing fields.
Do not restart the entire intake.

---

### G1 — Hypothesis Tree Validation

| Field | Value |
|---|---|
| Phase | 1 — Estruturação |
| Type | AUTO |
| Trigger | Hypothesis tree draft is complete |

**What to present:** Structured hypothesis tree with labeled claims. Show the consultant
the tree and the count of [FATO], [INFERÊNCIA], and [HIPÓTESE] nodes.

**Acceptance criteria:**
- At least 1 root hypothesis stated.
- All leaf nodes are labeled with an epistemic marker.
- No circular dependencies in the tree.
- At least 2 distinct evidence paths identified.

**On-pass:** Log tree to `artifacts/A-01-hypothesis-tree.md`. Advance to G2.
Display: `G1 concluído. Árvore de hipóteses validada (N nós, N [FATO], N [INFERÊNCIA],
N [HIPÓTESE]). Encaminhando para revisão de diagnóstico.`

**On-fail:** List specific validation failures. Present corrected draft for consultant
review. Do not advance.

---

### G2 — Diagnostic Review

| Field | Value |
|---|---|
| Phase | 2 — Diagnóstico |
| Type | **HARDCODED_HUMAN** |
| Trigger | Diagnostic artifact (A-02) is complete |

> **WARNING — HARDCODED HUMAN GATE**
> G2 cannot be auto-advanced under any condition. The system will not proceed past
> this gate without explicit human confirmation, regardless of diagnostic quality
> scores, time pressure, or consultant instruction to skip.

**What to present:** Full A-02 diagnostic artifact with all epistemic labels visible.
Summary of key findings. Explicit list of all [HIPÓTESE] claims that downstream
recommendations will depend on.

**Why human review is required:** The diagnostic is the epistemic foundation of all
downstream deliverables. An error here propagates to strategy, financials, and
client-facing recommendations. No automated check can substitute for a practitioner
evaluating whether the causal logic holds, whether the client's reality is correctly
reflected, and whether claims are appropriately labeled. Ethical responsibility for
the diagnosis rests with the consultant, not the system.

**Acceptance criteria:** Consultant explicitly types "aprovar" or provides specific
revision instructions.

**On-pass:** Log `G2_approved: true` and timestamp to manifest. Advance to G3.

**On-fail / revision requested:** Consultant describes what to adjust. System revises
A-02. Gate remains open until explicit approval.

**Block message (if auto-advance is attempted):**
```
Esta etapa requer revisão humana obrigatória.
O diagnóstico não pode ser aprovado automaticamente.
Revise o material acima e confirme com "aprovar" — ou descreva os ajustes necessários.
```

---

### G3 — Strategic Options Validation

| Field | Value |
|---|---|
| Phase | 3 — Estratégia |
| Type | AUTO |
| Trigger | Strategic options artifact (A-03) is complete |

**What to present:** Strategic options with evaluation criteria, epistemic labels, and
trade-off summary. At least 2 options presented (status quo + at least 1 alternative).

**Acceptance criteria:**
- Each option has at least 1 pro and 1 con explicitly stated.
- Evaluation criteria are defined (e.g., impact, feasibility, time-to-result).
- Recommended option is identified with reasoning.
- All assumptions underlying the recommendation are labeled [HIPÓTESE].

**On-pass:** Log A-03 to manifest. Advance to G4.
Display: `G3 concluído. N opções estratégicas avaliadas. Recomendação: [opção]. Avançando para QA.`

**On-fail:** List which criteria are unmet. Revise and re-check automatically.

---

### G4 — QA & Completeness Check

| Field | Value |
|---|---|
| Phase | 4 — QA |
| Type | AUTO |
| Trigger | All content artifacts for the scenario are produced |

**What to present:** Output of `scripts/validate_qa.py`. Full list of passed and failed
checks. If any check fails, list all failures before blocking.

**Acceptance criteria:** All 20 QA checks pass (see `references/qa-checklist.md`).
Zero failures. No partial pass.

**On-pass:** Log QA result to `logs/qa_results.json`. Advance to G5.
Display: `G4 concluído. Todos os N checks passaram. Encaminhando para aprovação do pacote final.`

**On-fail:** List failed checks with check numbers and descriptions. Block advancement.
Require revision and re-run. Do not advance with known failures.

---

### G5 — Final Package Approval

| Field | Value |
|---|---|
| Phase | 5 — Entrega |
| Type | **HARDCODED_HUMAN** |
| Trigger | QA (G4) passed; A-MASTER compilation complete |

> **WARNING — HARDCODED HUMAN GATE**
> G5 cannot be auto-advanced under any condition. The complete client package
> requires explicit consultant sign-off before it exists as a deliverable.

**What to present:** A-MASTER compiled document. A-FINAL executive summary.
A-OPS operational plan. List of all artifacts in the package with their artifact IDs.
Confirmation that all internal artifacts (diagnostic_working.md, internal IDs) have
been stripped from the client package.

**Why human review is required:** The consultant is professionally and legally
responsible for what is delivered to the client. The system can produce and QA content,
but the decision to release a document to a paying client is a human professional
judgment. Reputational and ethical accountability cannot be delegated to automation.

**Acceptance criteria:** Consultant explicitly types "aprovar" or provides revision
instructions.

**On-pass:** Log `G5_approved: true` and timestamp. Mark package as release-ready.
Advance to G6. Display: `Pacote aprovado. Preparando handoff de execução.`

**On-fail / revision requested:** Revise specified artifacts. Rerun G4 QA if content
changed. Gate remains open.

**Block message (if auto-advance is attempted):**
```
A aprovação do pacote final requer revisão humana obrigatória.
Revise os documentos acima e confirme com "aprovar" — ou descreva os ajustes necessários.
```

---

### G6 — Execution Handoff

| Field | Value |
|---|---|
| Phase | 6 — Handoff |
| Type | **HARDCODED_HUMAN** |
| Trigger | G5 approved; client delivery confirmed |

> **WARNING — HARDCODED HUMAN GATE**
> G6 cannot be auto-advanced. This gate closes the engagement record and
> marks artifacts as delivered. It cannot be undone programmatically.

**What to present:** Handoff checklist. Confirmation that all client-facing artifacts
have been transferred (format, channel, recipient confirmed). Open hipóteses that
require client-side validation listed explicitly. Recommended next engagement trigger
(if applicable).

**Why human review is required:** Closing an engagement is a consequential act.
The handoff record is permanent. The consultant must confirm that delivery actually
occurred, that the right person received the right version, and that any open
validation tasks have been communicated. The system has no way to verify actual delivery.

**Acceptance criteria:** Consultant confirms delivery occurred and types "fechar engajamento".

**On-pass:** Log `G6_closed: true` and timestamp. Freeze manifest. Archive engagement.
Display: `Engajamento encerrado. Artefatos arquivados. Trilha epistêmica preservada.`

**On-fail:** Consultant identifies what is incomplete. Gate remains open.

**Block message (if auto-advance is attempted):**
```
O encerramento do engajamento requer confirmação humana obrigatória.
Confirme a entrega ao cliente e feche com: "fechar engajamento"
```

---

## Auto-Advance Gates — What "AUTO" Means

An AUTO gate runs a programmatic check against defined acceptance criteria. If all
criteria are met, the gate passes and the system advances to the next phase — the
consultant does not need to click "approve." However:

- The consultant is always shown the gate result before advancement occurs.
- The consultant can halt at any AUTO gate by typing "pausar" or "revisar".
- Halting at an AUTO gate does not constitute a gate failure — it opens a review window.
- AUTO does not mean invisible. Every gate result is logged and shown.

---

## Scenario-Specific Gate Behavior

**Scenario A (Full engagement):**
All gates G0–G6 are active and run in full mode. No gates are skipped or abbreviated.

**Scenario B (Rapid diagnostic):**
G0 runs in abbreviated mode (reduced field set). G1, G2 (HARDCODED), G5 (HARDCODED)
are active. G3, G4, G6 are optional — consultant decides whether to activate each.

**Scenario C (Intake only):**
G0 runs with 5 fields only. All subsequent gates are auto-passed or skipped.
No A-MASTER compilation occurs. Output is intake summary only.

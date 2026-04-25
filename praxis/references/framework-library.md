# Framework Library — Praxis
Reference for Phase 3 analytical modules. Select frameworks based on context, tier, and client situation.

---

## GROUP 1: Problem Framing

### 1. MECE Decomposition
**Use case trigger:** Complex problem with undefined boundaries; need to structure a diagnosis without overlap or gaps.
**Output format:** `| Component | Sub-component | Related | Gap? | Owner |`
**Steps:**
1. State the central problem in one sentence.
2. Identify the highest-level mutually exclusive dimensions (max 5).
3. Decompose each dimension into sub-components (also MECE).
4. Check for overlaps (merge) and gaps (add or flag).
5. Assign ownership or data source to each leaf node.
**Example row:** `| Revenue | Pricing | Volume strategy | Yes — no elasticity data | Marketing |`

---

### 2. SCQA (Minto Pyramid)
**Use case trigger:** Need to frame a communication, report section, or recommendation narrative with executive clarity.
**Output format:** `| Situation | Complication | Question | Answer/Recommendation |`
**Steps:**
1. State the stable Situation (agreed facts, context).
2. Identify the Complication that disrupts the situation.
3. Derive the key Question that the complication raises.
4. Provide the Answer (the recommendation or insight).
5. Build supporting arguments pyramid-style beneath the Answer.
**Example row:** `| Market growing 12% YoY | Company revenue flat | Why is growth not captured? | Pricing and channel misalignment |`

---

### 3. First Principles
**Use case trigger:** Inherited assumptions are blocking innovation; client is imitating competitors without questioning fundamentals.
**Output format:** `| Assumption | Challenge | Ground Truth | Implication |`
**Steps:**
1. List all current assumptions about the problem.
2. For each assumption, ask: "Is this necessarily true, or inherited?"
3. Break each assumption to its physical/logical base.
4. Reconstruct the solution from verified ground truths only.
5. Compare rebuilt solution with incumbent approach — identify delta.
**Example row:** `| "We need a storefront" | Can customers buy online? | Yes, 80% browse mobile | Move to D2C digital-first |`

---

### 4. Jobs-to-be-Done (JTBD)
**Use case trigger:** Product-market fit unclear; customer retention low; ICP needs behavioral grounding beyond demographics.
**Output format:** `| Job Statement | Context | Functional Need | Emotional Need | Current Solution | Gap |`
**Steps:**
1. Interview or survey real customers using "When… I want to… so I can…" structure.
2. Identify functional, emotional, and social job dimensions.
3. Map current solutions customers hire (including non-obvious competitors).
4. Score satisfaction with current solutions (1–10).
5. Identify highest-friction jobs with lowest satisfaction — prioritize.
**Example row:** `| Plan team projects | Remote team, async | Track tasks easily | Feel in control | Spreadsheets | No real-time sync |`

---

## GROUP 2: Strategic Analysis

### 5. PESTEL
**Use case trigger:** External environment scan needed; entering new market; strategic planning horizon > 12 months.
**Output format:** `| Factor | Category | Description | Impact (H/M/L) | Trend | Implication |`
**Steps:**
1. List 3–5 factors per PESTEL category (Political, Economic, Social, Technological, Environmental, Legal).
2. Rate impact on client's business (High/Medium/Low).
3. Assess trend direction (improving, stable, worsening).
4. Identify which factors are controllable vs. structural.
5. Summarize top 5 implications for strategy.
**Example row:** `| Interest rate 13.75% | Economic | High borrowing cost | High | Worsening | Delay capex; optimize working capital |`

---

### 6. Porter's Five Forces
**Use case trigger:** Competitive positioning unclear; considering market entry or exit; pricing power assessment needed.
**Output format:** `| Force | Intensity (1–5) | Key Drivers | Strategic Implication |`
**Steps:**
1. Assess each of the 5 forces: Rivalry, Supplier Power, Buyer Power, New Entrants, Substitutes.
2. Score intensity 1 (low threat) to 5 (high threat).
3. Identify 2–3 key drivers for each score.
4. Determine overall industry attractiveness.
5. Recommend positioning moves to reduce force exposure.
**Example row:** `| Buyer Power | 4 | Few large clients, low switching cost | Diversify client base; add contracts |`

---

### 7. SWOT + Cross-Strategies
**Use case trigger:** Holistic internal/external snapshot needed; typically precedes OKR or action planning.
**Output format:** `| | Strengths | Weaknesses |` header, then `| Opportunities | SO strategy | WO strategy |` / `| Threats | ST strategy | WT strategy |`
**Steps:**
1. List 4–6 items per quadrant (S, W, O, T).
2. Map SO strategies (use strengths to capture opportunities).
3. Map WO strategies (overcome weaknesses via opportunities).
4. Map ST strategies (use strengths to mitigate threats).
5. Map WT strategies (defensive; minimize exposure).
**Example row (cross):** `| SO | Strong brand + digital growth trend | Launch online loyalty program |`

---

## GROUP 3: Prioritization

### 8. Theory of Constraints (TOC)
**Use case trigger:** Operations bottleneck suspected; throughput below capacity; multiple improvement initiatives compete.
**Output format:** `| Step | System Component | Constraint? | Action | Metric |`
**Steps:**
1. Map the full system flow (value stream or process chain).
2. Identify the single binding constraint limiting throughput.
3. Exploit the constraint (maximize its output without new investment).
4. Subordinate all other steps to the constraint's pace.
5. Elevate (invest to increase constraint capacity) then repeat.
**Example row:** `| 3 | Invoice approval | Yes | Pre-approve invoices <R$5k | Cycle time -40% |`

---

### 9. GUT Matrix + Pareto
**Use case trigger:** Multiple problems identified; team disagrees on priority; need objective scoring before action plan.
**Output format:** `| Problem | G (1–5) | U (1–5) | T (1–5) | GUT Score | Pareto Rank |`
**Steps:**
1. List all identified problems (from MECE or diagnosis).
2. Score each on Gravity (impact if not solved), Urgency (time pressure), Tendency (worsens over time?).
3. Calculate GUT = G × U × T.
4. Rank by GUT score descending; apply Pareto (top 20% of problems = 80% of impact).
5. Present top-priority cluster for action planning.
**Example row:** `| High churn rate | 5 | 4 | 5 | 100 | #1 |`

---

### 10. Effort × Impact Matrix
**Use case trigger:** Backlog of initiatives; need quick wins vs. strategic bets categorization; resource allocation.
**Output format:** `| Initiative | Effort (H/M/L) | Impact (H/M/L) | Quadrant | Recommendation |`
**Steps:**
1. List all candidate initiatives or solutions.
2. Estimate effort (time, cost, complexity): High/Medium/Low.
3. Estimate impact (revenue, risk reduction, NPS): High/Medium/Low.
4. Plot in 2×2 matrix: Quick Wins (L/H), Strategic Bets (H/H), Fill-ins (L/L), Time Sinks (H/L).
5. Recommend sequencing: Quick Wins first, then Strategic Bets with milestones.
**Example row:** `| Automate invoicing | Low | High | Quick Win | Implement immediately |`

---

## GROUP 4: Action Planning

### 11. 5W2H
**Use case trigger:** Action item needs full specification before handoff; initiative owner unclear; preventing execution gaps.
**Output format:** `| What | Why | Who | Where | When | How | How Much |`
**Steps:**
1. Define the action in one verb phrase (What).
2. Link to the strategic objective (Why).
3. Assign a single accountable owner (Who).
4. Specify execution context or location (Where).
5. Set deadline and budget (When + How Much) and method (How).
**Example row:** `| Launch CRM | Reduce churn 15% | Sales Director | HQ + remote | Q2 end | Hubspot rollout | R$12k |`

---

### 12. PDCA (Plan-Do-Check-Act)
**Use case trigger:** Continuous improvement cycle; pilot before full rollout; hypothesis-driven operational change.
**Output format:** `| Phase | Actions | Owner | Timeline | Success Metric |`
**Steps:**
1. Plan: define hypothesis, target, and test design.
2. Do: execute on small scale; collect data.
3. Check: compare results to target; analyze variance.
4. Act: standardize if successful; revise hypothesis if not; restart cycle.
5. Document learnings in each cycle for institutional memory.
**Example row:** `| Plan | Reduce lead time 20% via kanban | Ops Lead | Week 1–2 | Lead time baseline |`

---

### 13. OKR (Objectives and Key Results)
**Use case trigger:** Strategic goals need measurable translation; team alignment required; quarterly or annual planning cycle.
**Output format:** `| Objective | Key Result 1 | Key Result 2 | Key Result 3 | Owner | Quarter |`
**Steps:**
1. Draft qualitative, inspiring Objective (no numbers; directional).
2. Define 2–4 measurable Key Results per Objective (outcome, not output).
3. Set ambitious but achievable targets (70% attainment = success).
4. Assign single owner per OKR; align cross-functional dependencies.
5. Review weekly (health check) and score quarterly.
**Example row:** `| Dominate SME segment | NPS > 55 | Churn < 3%/mo | 500 new clients | CEO | Q3 2025 |`

---

### 14. Sprint Planning
**Use case trigger:** Execution phase begins; team needs 2-week delivery cycles; backlog must be converted to tasks.
**Output format:** `| Sprint # | Goal | Task | Owner | Story Points | Status |`
**Steps:**
1. Define sprint goal in one sentence (what will be demonstrably done?).
2. Pull highest-priority items from backlog (GUT + Effort×Impact filtered).
3. Break each into tasks ≤ 1 day effort; estimate story points.
4. Assign owners; confirm capacity (subtract leave, overhead).
5. Define Definition of Done for each task before sprint starts.
**Example row:** `| Sprint 1 | CRM live | Configure pipelines | Sales Ops | 5 pts | In progress |`

---

## GROUP 5: Decision Intelligence

### 15. EXPLORE
**Use case trigger:** Problem space is unknown or poorly defined; gathering intelligence before analysis.
**Output format:** `| Question | Source | Finding | Confidence | Follow-up? |`
**Steps:** Diverge broadly; map unknowns; collect signals; defer judgment. (See decision-modes.md)

### 16. EVALUATE
**Use case trigger:** Options identified; need structured comparison before choosing.
**Output format:** `| Option | Criterion 1 | Criterion 2 | Criterion 3 | Weighted Score |`
**Steps:** Define criteria and weights; score each option; sensitivity-test top choices. (See decision-modes.md)

### 17. DECIDE
**Use case trigger:** Evaluation complete; recommendation must be formulated and justified.
**Output format:** `| Decision | Rationale | Trade-offs | Risks | Conditions |`
**Steps:** Select highest-scoring option; articulate trade-offs; state contingency conditions. (See decision-modes.md)

### 18. EXECUTE
**Use case trigger:** Decision made; need execution plan with accountability.
**Output format:** `| Action | Owner | Deadline | Resource | Dependency | KPI |`
**Steps:** Translate decision to 5W2H tasks; assign owners; set milestones; build risk log. (See decision-modes.md)

### 19. REVIEW
**Use case trigger:** Cycle complete or checkpoint reached; assess results vs. plan.
**Output format:** `| KPI | Target | Actual | Variance | Root Cause | Corrective Action |`
**Steps:** Measure actuals vs. targets; diagnose variance; extract learnings; feed next PDCA cycle. (See decision-modes.md)

---

*Full behavior of EXPLORE–REVIEW modes in `/references/decision-modes.md`.*
*Tier applicability (which frameworks per tier) in `/references/b-frames-tiers.md`.*

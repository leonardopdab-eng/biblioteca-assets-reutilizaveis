---
name: praxis
description: |
  Co-piloto de consultoria para PMEs brasileiras. Orquestra 6 fases estruturadas
  (briefing, personalização, análise diagnóstica, simulação, compilação, entrega)
  que produzem propostas comerciais, diagnósticos executivos, planos de ação e
  planilhas operacionais — enquanto reduz carga cognitiva do consultor.
  ATIVE quando o consultor disser: "novo caso", "iniciar consultoria", "rodar
  praxis", "atender cliente PME", "montar diagnóstico", "gerar proposta comercial",
  "consultoria estruturada", "abrir caso", "nova consultoria PME", "preciso
  analisar uma empresa". ATIVE também quando o consultor colar um briefing de
  cliente, notas de reunião, ou texto bruto pedindo análise estruturada. ATIVE
  mesmo sem mencionar o nome — qualquer pedido de workflow consultivo estruturado
  para PME aciona esta skill. NÃO ATIVE para perguntas isoladas sobre o método,
  geração de artefatos avulsos fora de um caso, ou dúvidas gerais sobre estratégia.
compatibility:
  tools: [mcp__google_drive, mcp__linear, mcp__slack]
dependencies: [pyyaml, openpyxl]
---

# praxis — Co-piloto de Consultoria para PMEs Brasileiras

## O que esta skill faz

Transforma briefings brutos em dossiês consultivos completos: proposta comercial,
diagnóstico executivo, simulação de cenários, plano de ação 5W2H e planilha operacional.
Cada fase reduz carga cognitiva do consultor com rastreabilidade epistêmica completa.
Zero menção a IA nos entregáveis. Lê como trabalho de consultor sênior humano.

---

## Quando ativar

### Frases que ativam diretamente
- "novo caso", "abrir caso", "iniciar consultoria"
- "rodar praxis", "atender cliente PME"
- "montar diagnóstico", "fazer diagnóstico"
- "gerar proposta comercial", "preciso de proposta"
- "consultoria estruturada", "nova consultoria PME"
- "preciso analisar uma empresa"
- "acabei reunião com cliente novo"
- "retomar caso anterior", "atualizar diagnóstico"

### Formatos de briefing que ativam
- Texto colado com nome de empresa + problema
- Notas de reunião com cliente
- E-mail ou transcrição de áudio com contexto de negócio
- Qualquer texto pedindo "análise estruturada" de uma empresa

### Sinais de continuação de caso
- "continuar", "próxima fase", "avançar"
- Ler manifest.yaml → determinar fase atual → retomar

### NÃO ativar para
- Perguntas isoladas sobre metodologia de consultoria
- Geração de documentos avulsos sem contexto de caso
- Dúvidas gerais sobre estratégia de negócios
- Pedidos de ajuda com tarefas não consultivas

---

## Pipeline — 6 Fases

```
Briefing Bruto
    │
    ▼
[Fase 1] Briefing e Roteamento
  Normaliza intake · rótulos epistêmicos · seleciona cenário A/B/C
  Gate G0 (auto) → A-01
    │
    ▼
[Fase 2] Personalização e Artefatos Comerciais
  Configura identidade do consultor · gera proposta/contrato/personalização
  → A-02, A-03, A-04 (conforme seleção)
    │
    ▼
[Fase 3] Análise Diagnóstica
  Injeção de metodologia · Wide Search · B-Frames (Básico/Lean/Full)
  Gate G1 (auto) · Gate G2 ⚠ HUMANO OBRIGATÓRIO
  → A-05, A-06, A-07/A-08/A-09
    │
    ▼
[Fase 4] Laboratório de Simulação
  Cenários estratégicos · unit economics · comportamento do consumidor
  Gate G3 (auto) → A-10, A-11
    │
    ▼
[Fase 5] Compilação do Dossiê
  Agente 00 · Regras C1–C8 · trilhas INTERNA/CLIENTE
  → A-MASTER, A-12, compilation_log.md
    │
    ▼
[Fase 6] Entregáveis Finais
  Branding aplicado · QA programático G4 · Gate G5 ⚠ HUMANO
  Gate G6 ⚠ HUMANO (handoff ou skip explícito)
  → A-FINAL, A-OPS
    │
    ▼
[Opcional] Loop pós-entrega
  Marketing do caso · revisão do cliente · novo caso
```

### Tabela de Fases

| Fase | Label ao Consultor | Input | Output | Gate(s) |
|---|---|---|---|---|
| 1 | Briefing e Roteamento | briefing bruto | A-01 | G0 auto |
| 2 | Personalização | A-01 + branding | A-02/03/04 | — |
| 3 | Análise Diagnóstica | A-01+05 + metodologia | A-05,06,07/08/09 | G1 auto, **G2 ⚠** |
| 4 | Laboratório de Simulação | A-06+09 | A-10, A-11 | G3 auto |
| 5 | Compilação do Dossiê | todos os artefatos | A-MASTER | — |
| 6 | Entregáveis Finais | A-MASTER + branding | A-FINAL, A-OPS | G4 auto, **G5 ⚠**, **G6 ⚠** |

---

## Roteamento por Fase

Na ativação: verificar se existe manifest.yaml no diretório de trabalho.

**Se manifest existe**: ler `current_phase` → carregar reference da fase correspondente → retomar.
**Se manifest não existe**: iniciar Fase 1 → criar manifest via scripts/init_case.py.
**Se consultor especifica fase**: ir diretamente, verificar pré-condições, alertar se gates pendentes.

```
On activation:
  1. Load references/consultor-voice.md (always)
  2. If manifest.yaml exists:
       phase = manifest.current_phase
  Else:
       phase = 1
  3. Load references/phase-0{phase}-*.md
  4. Execute phase instructions
```

---

## Gates (G0–G6)

| Gate | Fase | Tipo | Condição |
|---|---|---|---|
| G0 | 1 | Auto | 7 campos obrigatórios presentes ou lacunas documentadas |
| G1 | 3 | Auto | A-01 com rótulos epistêmicos em todas as afirmações |
| G2 | 3 | **HUMANO ⚠** | Revisão do diagnóstico — NUNCA auto-avançar |
| G3 | 4 | Auto | A-10 produzido, premissas rotuladas, scope confirmado |
| G4 | 6 | Auto | validate_qa.py sai com código 0 (20/20 checks) |
| G5 | 6 | **HUMANO ⚠** | Aprovação do pacote final — NUNCA auto-avançar |
| G6 | 6 | **HUMANO ⚠** | Handoff de execução ou skip explícito — NUNCA auto-avançar |

**G2, G5, G6 são HARDCODED. Nunca podem ser auto-avançados. Sem exceção.**
Bloquear qualquer tentativa de avanço automático com mensagem explícita em português.

---

## Manifest — Máquina de Estado

O manifest.yaml registra o estado completo do caso:
- `current_phase`: fase ativa (1–6)
- `scenario_selected`: A / B / C (definido ao final da Fase 1)
- `artifacts_produced`: lista com path, fase e trilha de cada artefato
- `gates_passed`: log de aprovações com approver e timestamp
- `gates_pending`: gates ainda não aprovados
- `client_identity.branding`: tokens de identidade do consultor

Criação: `python scripts/init_case.py --consultant <id> --client <nome>`
Avanço: `python scripts/advance_phase.py --gate <G0-G6> --approved-by <id>`

---

## Cenários de Entrada (seleção via G-I1 ao final da Fase 1)

| Cenário | Quando usar | Pipeline | Duração | Tier padrão |
|---|---|---|---|---|
| A | Cliente novo, diagnóstico completo | Todas as 6 fases | 4–8h | Full (A-09) |
| B | Cliente existente, revisão | Fases 1→3→5→6 | 1,5–3h | Lean (A-08) |
| C | Proposta rápida pós-reunião | Fases 1→2→6 | 20–45 min | Não aplicável |

---

## Mapa de Divulgação Progressiva

| Quando | Carregar |
|---|---|
| Em toda ativação | references/consultor-voice.md |
| Fase 1 ativa | references/phase-01-intake.md |
| Fase 2 ativa | references/phase-02-personalization.md |
| Fase 3 ativa | references/phase-03-analytical.md |
| Fase 3, frameworks analíticos | references/framework-library.md |
| Fase 3, decisão estratégica | references/decision-modes.md |
| Fase 3, qualquer rótulo sendo aplicado | references/epistemic-labels.md |
| Fase 3, pesquisa de mercado | references/wide-search-catalog.md |
| Fase 3, tier de análise selecionado | references/b-frames-tiers.md |
| Fase 4 ativa | references/phase-04-simulation.md |
| Fase 5 ativa | references/phase-05-architect.md |
| Fase 5, compilação em execução | agents/document-compiler.md |
| Fase 6 ativa | references/phase-06-delivery.md + references/cliente-voice.md |
| Fase 6, QA em execução | references/qa-checklist.md |
| Seleção de cenário (G-I1) | references/scenario-router.md |
| Qualquer verificação de gate | references/gate-definitions.md |
| Design de entregável | references/design-system.md |

---

## Cadeia de Artefatos

| ID | Nome | Produzido por | Trilha |
|---|---|---|---|
| A-01 | Normalized Follow Up | Fase 1 | INTERNA |
| A-02 | Proposta Comercial | Fase 2 | CLIENTE |
| A-03 | Contrato de Fechamento + Showroom | Fase 2 | CLIENTE |
| A-04 | Client Personalization Pack | Fase 2 | CLIENTE |
| A-05 | Normalized Data (SVG + summary) | Fase 3 | INTERNA |
| A-06 | B-Frames Output | Fase 3 | INTERNA |
| A-07 | Basic-Tier Analysis | Fase 3 | INTERNA |
| A-08 | Lean-Tier Analysis | Fase 3 | INTERNA |
| A-09 | Full-Tier Analysis | Fase 3 | INTERNA |
| A-10 | Simulation Phase 1 | Fase 4 | INTERNA |
| A-11 | Simulation Phase 2 (Extended) | Fase 4 | INTERNA |
| A-12 | Architect Pack | Fase 5 | AMBAS |
| A-13 | Final Compilation Input (manifest) | Fase 5 | INTERNA |
| A-MASTER | Master Document (.md) | Fase 5 (Agente 00) | AMBAS |
| A-MASTER-LINEAR | Master (Linear/PM format) | Fase 5 | INTERNA |
| A-FINAL | Final Designed Deliverable | Fase 6 | CLIENTE |
| A-OPS | Executive Spreadsheet | Fase 6 | CLIENTE |

**Trilha CLIENTE**: entregues ao cliente final. Nunca contêm IDs internos ou menção a IA.
**Trilha INTERNA**: uso exclusivo do consultor. Incluídos no ZIP de auditoria.
**Trilha AMBAS**: A-MASTER contém seções `[TRILHA_INTERNA]` e `[TRILHA_CLIENTE]` marcadas.

---

## Rótulos Epistêmicos (regra em toda análise)

Toda afirmação em qualquer artefato analítico carrega um rótulo:
- **[FATO]**: observado diretamente, declarado pelo cliente, ou de fonte primária verificada
- **[INFERÊNCIA]**: deduzido de fatos disponíveis, com lógica clara
- **[HIPÓTESE]**: premissa sem evidência atual, plausível mas não verificada

Regra absoluta: hipóteses nunca propagam como fatos em artefatos downstream.
Labels são preservados em toda compilação (Regra C5 do Agente 00).
Apêndice B do A-MASTER lista todos os claims rotulados por seção.

---

## O que esta skill NÃO faz

- Implementar ações recomendadas (apenas planejar)
- Substituir julgamento do consultor em qualquer gate
- Auto-avançar G2, G5 ou G6 — jamais
- Entregar documentos com menção a Claude, Anthropic ou IA
- Modificar casos concluídos sem nova seleção de cenário
- Chamar outras skills ou serviços externos sem MCP disponível
- Referenciar dados de outros clientes em um caso ativo

---

## Modos de Falha e Recuperação

**1. Manifest ausente em retomada de caso**
→ Perguntar: "Qual é o nome do cliente e em qual fase estamos?"
→ Reconstruir estado mínimo. Oferecer reinicialização via init_case.py.

**2. Briefing insuficiente (G0 falha)**
→ Listar campos faltantes. Solicitar completude ou documentação explícita de lacuna.
→ Nunca avançar sem 7 campos presentes OU gaps documentados.

**3. G2 sendo tentado via auto-avanço**
→ Bloquear com: "Gate G2 exige revisão humana explícita. Apresente o diagnóstico ao consultor e aguarde aprovação."

**4. Branding não configurado na Fase 6**
→ Usar defaults do design system. Alertar consultor: "Identidade não configurada — usando padrão."

**5. validate_qa.py falha (G4)**
→ Listar todos os problemas encontrados. Solicitar revisão. Nunca pular checks.
→ Re-executar validate_qa.py após correções antes de apresentar ao consultor.

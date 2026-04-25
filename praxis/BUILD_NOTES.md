# BUILD NOTES — Praxis v1.0.0

## Status dos Gaps

### GAP-01: Agente 00 — Subroutine de Compilação
**Status**: RESOLVIDO
**Resolução**: Agente 00 é uma subroutine dentro da Fase 5 (não uma skill separada).
Sem interface interativa. Ativado automaticamente após confirmação da diretiva G-I6.
**Regras implementadas**: C1–C8 em `references/phase-05-architect.md` e `agents/document-compiler.md`
**Regras**: resolução de fontes, estrutura de seção, normalização de cabeçalhos, deduplicação,
preservação de labels, separação de trilhas, completude mínima C7, formato de saída.

### GAP-08: Design System — Especificação Visual
**Status**: RESOLVIDO
**Resolução**: Paleta navy profissional com override do consultor.
**Implementado em**: `references/design-system.md`
**Tokens**: 9 cores (primary #1B2A4A, accent #2E7D9B, etc.), Inter typography, grid A4 completo,
estilos de componentes (tabelas, badges epistêmicos, rodapé, capa), estilos XLSX.

### GAP-09: Cenários A/B/C — Definição do Router
**Status**: RESOLVIDO
**Resolução**: 3 cenários mapeados para os 3 pontos de entrada mais comuns.
**Implementado em**: `references/scenario-router.md`
- Cenário A: Diagnóstico Completo — todas as 6 fases, tier Full, 4–8h
- Cenário B: Revisão e Atualização — fases 1/3/5/6, tier Lean, 1,5–3h
- Cenário C: Proposta Rápida — fases 1/2/6, sem diagnóstico, 20–45min

---

## Dependências

```bash
pip install pyyaml openpyxl
```

- `pyyaml`: leitura/escrita de manifest.yaml em todos os scripts
- `openpyxl`: geração de A-OPS.xlsx em generate_executive_xls.py

---

## Notas de Implementação

### Hardcoded Human Gates
`HARDCODED_HUMAN_GATES = {"G2", "G5", "G6"}` aparece explicitamente em:
- `scripts/advance_phase.py`: bloqueio de `--approved-by AUTO`
- `schemas/phase-gates.yaml`: campo `hardcoded_human_gates`
- `SKILL.md`: tabela de gates com ⚠ marcadores
- `references/gate-definitions.md`: bloco WARNING separado

Esses gates NÃO podem ser configurados nem sobrescritos. São constantes, não settings.

### Dry Run e Aprovações de G2/G5/G6
O `scripts/dry_run.py` simula a aprovação de G2 com `approved_by: "dr-test-consultor"` para
permitir teste end-to-end. Em produção, o consultor real deve sempre aprovar interativamente.

### Branding Placeholder
Se o consultor não configurar branding (fase virgem não completada), o sistema usa os
defaults do design system (navy #1B2A4A). Nenhum erro é gerado — apenas um alerta.

### Wide Search Catalog — Nota
O catálogo em `references/wide-search-catalog.md` lista fontes sem endpoints de API.
Acesso a APIs específicas (Sebrae, IBGE SIDRA) depende de MCP connector adicional
ou de pesquisa manual do consultor com injeção via G-I3.

### MCP Connectors
Os MCPs (Google Drive, Linear, Slack) são **opcionais**. A skill funciona completamente
sem eles. Quando disponíveis:
- Google Drive: pré-carrega documentos do cliente em Fase 1
- Linear: exporta plano de ação em Fase 5 (A-MASTER-LINEAR)
- Slack: notificação de handoff em Fase 6

---

## Decisões de Arquitetura

| Decisão | Escolha | Alternativa descartada | Motivo |
|---|---|---|---|
| Agente 00 | Subroutine na Fase 5 | Skill separada | Zero overhead de ativação; acesso direto ao manifest |
| Formato A-MASTER | Markdown UTF-8 | JSON estruturado | Legível pelo consultor, renderizável como HTML |
| Trilhas INTERNA/CLIENTE | Marcadores inline no A-MASTER | Arquivos separados | Único source-of-truth; compilação simples |
| Labels epistêmicos | [FATO]/[INFERÊNCIA]/[HIPÓTESE] | Sistema de score numérico | Linguagem natural, auditável por humano |
| Gates G2/G5/G6 | Hardcoded em constante Python | Configurável por flag | Proteção contra automação acidental |

---

## Estrutura de Arquivo Completa

```
praxis/
├── SKILL.md                          275 linhas
├── README.md
├── INSTALL.md
├── BUILD_NOTES.md
├── manifest_template.yaml
├── references/
│   ├── phase-01-intake.md
│   ├── phase-02-personalization.md
│   ├── phase-03-analytical.md
│   ├── phase-04-simulation.md
│   ├── phase-05-architect.md
│   ├── phase-06-delivery.md
│   ├── framework-library.md
│   ├── decision-modes.md
│   ├── epistemic-labels.md
│   ├── wide-search-catalog.md
│   ├── b-frames-tiers.md
│   ├── gate-definitions.md
│   ├── scenario-router.md           [GAP-09 RESOLVIDO]
│   ├── design-system.md             [GAP-08 RESOLVIDO]
│   ├── consultor-voice.md
│   ├── cliente-voice.md
│   └── qa-checklist.md
├── agents/
│   ├── diagnostic-analyzer.md
│   ├── simulator.md
│   ├── document-compiler.md         [GAP-01 RESOLVIDO]
│   └── qa-reviewer.md
├── scripts/
│   ├── init_case.py
│   ├── advance_phase.py
│   ├── compile_master.py
│   ├── generate_executive_xls.py
│   ├── validate_qa.py
│   └── dry_run.py
├── assets/
│   ├── proposta-comercial-template.md
│   ├── contrato-fechamento-template.md
│   ├── diagnostico-executivo-template.md
│   ├── plano-acao-template.md
│   └── executive-xls-template.md
└── schemas/
    ├── manifest.yaml
    ├── artifact-registry.yaml
    └── phase-gates.yaml
```

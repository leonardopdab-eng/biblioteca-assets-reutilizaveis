# Modos de Entrega — Bússola PME

## F1 — ZIP (Padrão)

**Quando usar**: Entrega final do caso para arquivo e uso off-line.

**Estrutura**:
```
BP-001/
├── interno/
│   ├── hypotheses_log.md
│   ├── problem_tree.md
│   ├── diagnostic_working.md
│   ├── priority_score.md
│   ├── decision_log.md
│   ├── information_gaps.md
│   ├── assumptions_log.md
│   ├── module_routing_log.md
│   └── intake_normalized_v2.md
├── cliente/
│   ├── resumo_executivo.md
│   ├── diagnostico_executivo.md
│   ├── matriz_prioridades.md
│   ├── plano_acao_cliente.md
│   ├── playbook_operacional.md
│   ├── apresentacao_executiva.pdf
│   ├── relatorio_acompanhamento.md
│   └── proposta_continuidade.md
├── governanca/
│   ├── manifest.yaml
│   ├── qa_checklist.md
│   ├── anonymization_log.md
│   ├── source_audit_log.md
│   ├── gate_transition_log.md
│   ├── hypothesis_propagation_log.md
│   ├── version_history.yaml
│   ├── consultant_config_snapshot.yaml
│   ├── intake_original.md
│   └── release_notes.md
├── custom_agent/
│   └── SKILL.md
└── README_PACOTE.md
```

**Produzido por**: `zip_packager.py`

---

## F2 — E-book HTML

**Quando usar**: Envio digital ao cliente para leitura self-service e navegação.

**Formato**: `ebook_[case_id].html` — arquivo único com:
- Navegação lateral (summary de artefatos)
- Artefatos de trilha cliente em ordem lógica
- Branding aplicado (cores, tipografia do consultant_config)
- Print-friendly via CSS media query
- Sem dependências externas (CSS/JS inline)

**Ativação**: `--format ebook` ou "gerar e-book do diagnóstico"

---

## F3 — Live Sprint React

**Quando usar**: Apresentação ao vivo da proposta para cliente (sprint de vendas).

**Formato**: Componente React auto-contido com:
- Seleção dos artefatos de maior impacto visual
- Animações de entrada (fade-in por seção)
- Timeline interativa das fases do diagnóstico
- Contadores animados de achados/ações
- CTA interativo para next steps

**Ativação**: `--format react` ou "gerar apresentação ao vivo"

**Nota**: Requer `visualize:show_widget` no ambiente de execução.

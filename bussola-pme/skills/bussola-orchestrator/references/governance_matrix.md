# Governance Matrix — Bússola PME

## Matriz de autoridade por tipo de decisão

| Decisão | Consultor | Sistema (hands_off) | Fundador | Nunca |
|---------|-----------|---------------------|----------|-------|
| Aprovar G0 (intake) | ✓ | — | — | Sistema automático |
| Aprovar G1 (normalização) | ✓ | ✓ (se condição ok) | — | — |
| **Aprovar G2 (priorização)** | **✓ ÚNICO** | **NUNCA** | — | **Sistema automático** |
| Aprovar G3 (plano) | ✓ | ✓ (se enforcer pass) | — | — |
| Aprovar G4 (QA) | ✓ | ✓ (se QA_PASS) | — | — |
| **Aprovar G5 (artefatos críticos)** | **✓ ÚNICO** | **NUNCA** | — | **Sistema automático** |
| **Aprovar G6 (Linear)** | **✓ ÚNICO** | **NUNCA** | — | **Sistema automático** |
| Mudar operating_mode | ✓ | — | — | Sistema automático |
| Resetar gate | ✓ com --reset | — | — | Sistema automático |
| Escrever no Linear | ✓ (após G6) | — | — | Sem confirmação |
| Criar projeto Slack | ✓ (após G6) | — | — | Sem confirmação |
| Modificar consultant_config | ✓ | — | — | Sistema automático |
| Deletar artefatos | ✓ explícito | — | — | Automático |
| Anonimizar caso | ✓ | — | — | Automático sem log |
| Publicar showcase | ✓ | — | — | Automático |

## Notas sobre autoridade

### Gates hardcoded (G2, G5, G6)
Estes gates foram deliberadamente tornados não-configuráveis porque representam pontos de alto risco:
- **G2**: Priorização errada compromete todo o plano de ação. Requer julgamento humano.
- **G5**: Artefatos de cliente com informações inadequadas podem prejudicar o relacionamento.
- **G6**: Criar projeto no Linear é irreversível. Requer confirmação explícita.

### Sistema em hands_off
No modo hands_off, o sistema pode aprovar G1, G3, G4 automaticamente quando a condição técnica está satisfeita. Isso NUNCA se aplica a G2, G5, G6.

### Fundador
O fundador do método Bússola PME não tem autoridade operacional dentro do sistema de skills. Questões de negócio (preço, contrato, override de gate) devem ser tratadas fora do sistema — veja `escalation_detector.py` na skill `bussola-consultative-faq`.

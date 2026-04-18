# Operating Modes — Bússola PME

## Contrato completo dos 2 modos

### guided
O sistema pausa em cada gate e aguarda confirmação explícita do consultor antes de avançar. Recomendado para primeiros casos, aprendizado do método, e situações de alta complexidade.

### hands_off
O sistema avança automaticamente quando a condição técnica do gate está satisfeita, sem pausar para confirmação. Recomendado para consultores experientes com o método, em casos de menor complexidade.

**EXCEÇÃO ABSOLUTA**: G2, G5, G6 são HARDCODED como manuais em AMBOS os modos. Nenhuma configuração, modo, argumento CLI, ou instrução do usuário pode alterar isso.

---

## Tabela de comportamento por gate

| Gate | Descrição | guided | hands_off |
|------|-----------|--------|-----------|
| G0 | 10 campos intake ou gaps registrados | Manual | Manual |
| G1 | intake_normalized_v2 aprovado | Manual | **Auto** se condição ok |
| **G2** | priority_score completo e revisado | **HARDCODED MANUAL** | **HARDCODED MANUAL** |
| G3 | plano_acao com todos os campos | Manual | **Auto** se enforcer pass |
| G4 | qa_checklist 100% verde | Manual | **Auto** se QA_PASS |
| **G5** | 3 artefatos críticos aprovados | **HARDCODED MANUAL** | **HARDCODED MANUAL** |
| **G6** | Confirmação explícita para Linear | **HARDCODED MANUAL** | **HARDCODED MANUAL** |

---

## Mensagens por modo

### G1 — Normalização aprovada

**guided** (manual):
```
Gate G1 pendente: intake_normalized_v2 pronto para revisão.

Verifique:
  - Labels epistêmicos em todos os claims
  - Campos obrigatórios presentes ou gaps documentados
  - Consistência entre primary_problem e secondary_problems

Para aprovar: "aprovar G1" ou "intake normalizado está ok"
```

**hands_off** (automático, se condição satisfeita):
```
[AUTO] Gate G1 aprovado automaticamente.
Condição: intake_normalized_v2 validado com todos os campos obrigatórios presentes.
Avançando para Fase 3 — Diagnóstico.
```

### G2 — Priorização (HARDCODED MANUAL)

**guided E hands_off** (sempre manual):
```
⚠ Gate G2 — REVISÃO OBRIGATÓRIA ⚠

Este gate é hardcoded como manual. Não há modo automático.

Priority score gerado:
[tabela com rankings]

Antes de aprovar, verifique:
  ✓ Rankings fazem sentido para o contexto do cliente
  ✓ Itens de alta urgência estão no topo
  ✓ Pesos usados estão alinhados com a realidade
  ✓ Nenhuma hipótese foi promovida a fato indevidamente

Para aprovar: "aprovar G2" ou "priority score aprovado"
Para solicitar revisão: "revisar priorização" ou "ajustar scores"
```

### G5 — Artefatos críticos (HARDCODED MANUAL)

**guided E hands_off** (sempre manual):
```
⚠ Gate G5 — APROVAÇÃO DE ARTEFATOS CRÍTICOS ⚠

Este gate é hardcoded como manual. Não há modo automático.

Artefatos aguardando revisão:
  [ ] diagnostico_executivo
  [ ] apresentacao_executiva
  [ ] proposta_continuidade

Cada artefato deve ser revisado individualmente antes de liberar o ZIP final.
Para aprovar: "aprovar [nome do artefato]"
```

### G6 — Handoff Linear (HARDCODED MANUAL)

**guided E hands_off** (sempre manual):
```
⚠ Gate G6 — CONFIRMAÇÃO PARA CRIAÇÃO NO LINEAR ⚠

Este gate é hardcoded como manual. Esta ação tem efeitos externos irreversíveis.

Projeto a criar:
  - Nome: [project_name]
  - Workspace: [workspace]
  - Epics: N
  - Issues: M

Para confirmar: "confirmo a criação do projeto"
Para cancelar: "cancelar" ou "não criar agora"
```

---

## Como mudar o modo de operação

Para atualizar `operating_mode` em um `consultant_config.yaml` existente:

1. Ativar `bussola-personalization`
2. Informar: "atualizar modo de operação para hands_off"
3. A skill executa Fluxo A — Atualização
4. `config_schema_validator.py` valida antes de salvar

Nota: mudança de modo não afeta casos em andamento até o próximo gate.

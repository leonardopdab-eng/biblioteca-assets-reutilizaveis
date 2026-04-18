# FAQ — Modos de Operação Bússola PME

## Q: Qual a diferença entre guided e hands_off?
**guided**: Sistema pausa em cada gate e aguarda confirmação explícita do consultor. Recomendado para primeiros casos e situações de alta complexidade.
**hands_off**: Sistema avança automaticamente quando condição técnica do gate está satisfeita. Recomendado para consultores experientes em casos de menor complexidade.

## Q: Quais gates nunca são automáticos, independente do modo?
G2 (priorização), G5 (artefatos críticos), G6 (Linear). São HARDCODED MANUAL. Nenhuma configuração, argumento, ou modo altera isso.

## Q: Como mudar o modo de operação?
Ativar `bussola-personalization` e solicitar "atualizar modo de operação para hands_off". A skill executa o Fluxo A de atualização e valida antes de salvar.

## Q: Mudar o modo afeta casos em andamento?
Mudança de modo não afeta gates já passados. Afeta apenas gates futuros a partir do próximo gate não-aprovado.

## Q: Qual modo usar para o primeiro caso?
Sempre `guided` para o primeiro caso. O consultor precisa conhecer o comportamento do sistema em cada gate antes de confiar no modo automático.

## Q: Em hands_off, como sei quando o sistema avançou automaticamente?
O sistema registra auto-approvals no `gate_transition_log.md` com flag `auto: true` e a condição que foi satisfeita.

## Q: Posso ter modos diferentes por caso?
Não diretamente. O modo está no `consultant_config.yaml` (por consultor, não por caso). Para trocar o modo em um caso específico, seria necessário criar um config separado.

## Q: O que acontece se eu tentar bypassar um gate hardcoded em hands_off?
O sistema recusa com `GATE_BLOCK: requires_human (G2 is HARDCODED MANUAL — never automatic in any mode)`. Não há bypass.

## Tabela de comportamento por gate

| Gate | guided | hands_off |
|------|--------|-----------|
| G0 | Manual | Manual |
| G1 | Manual | Auto se intake_v2 aprovado |
| **G2** | **HARDCODED MANUAL** | **HARDCODED MANUAL** |
| G3 | Manual | Auto se enforcer pass |
| G4 | Manual | Auto se QA_PASS |
| **G5** | **HARDCODED MANUAL** | **HARDCODED MANUAL** |
| **G6** | **HARDCODED MANUAL** | **HARDCODED MANUAL** |

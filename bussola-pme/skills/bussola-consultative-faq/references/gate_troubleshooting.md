# Troubleshooting de Gates — Bússola PME

## G0 bloqueado — "Intake incompleto"

**Causa**: Campos obrigatórios do intake ausentes sem gap registrado.
**Solução**: 
1. Identificar campos ausentes via `intake_field_checker.py`
2. Coletar via `ask_user_input_v0` ou registrar em `information_gaps.md`
3. Se cliente não souber: registrar gap com `impact` e `recommended_action`
**Não é possível bypassar**: G0 é manual em todos os modos.

## G1 bloqueado — "intake_normalized_v2 não aprovado"

**Causa**: `intake_normalized_v2.md` não tem `approved: true` ou falta labels epistêmicos.
**Solução**:
1. Verificar que todos os claims têm labels [FATO], [INFERÊNCIA], ou [HIPÓTESE]
2. Adicionar `approved: true` no frontmatter após revisão
3. Em hands_off: sistema aprova automaticamente se condição ok
**Bypass em guided**: não existe. Em hands_off: automático se condição satisfeita.

## ★ G2 bloqueado — "HARDCODED MANUAL: priority_score requer aprovação humana"

**Causa**: Gate G2 é hardcoded manual. O priority_score está gerado mas não foi aprovado pelo consultor.
**Solução**:
1. Revisar `priority_score.md` — rankings fazem sentido?
2. Verificar se pesos do config estão corretos
3. Confirmar: nenhuma hipótese foi promovida indevidamente
4. Aprovar: `manifest_builder.py --action update-gate --gate G2 --status approved --by consultor`
**IMPOSSÍVEL BYPASSAR**: G2 é hardcoded. Em nenhum modo. Nenhum argumento. Nenhuma configuração.

**Mensagem ao consultor**: "⚠️ Gate G2 requer sua revisão e aprovação explícita. O sistema nunca aprova automaticamente porque a priorização representa uma decisão de julgamento que requer perspectiva humana sobre o contexto do cliente."

## G3 bloqueado — "Plano sem campos obrigatórios"

**Causa**: Um ou mais itens do plano_acao faltam owner, deadline ou kpi.
**Solução**: 
1. Executar `action_field_enforcer.py --plano plano_acao.md`
2. Identificar itens problemáticos no output
3. Preencher os campos faltantes
**Bypass em hands_off**: automático após enforcer pass.

## G4 bloqueado — "QA checklist não 100% verde"

**Causa**: Uma ou mais das 7 verificações de QA falharam.
**Solução**: Executar `qa_checklist_runner.py --case-dir [path]` e corrigir cada item falho.
**Verificações**: artefatos presentes, sem leaks internos, plano com campos, hipóteses sinalizadas, manifest atual, branding aplicado, G5 aprovado.

## ★ G5 bloqueado — "HARDCODED MANUAL: artefatos críticos não aprovados"

**Causa**: Gate G5 é hardcoded manual. Os 3 artefatos críticos precisam de aprovação individual.
**Solução**:
1. Revisar `diagnostico_executivo.md` — linguagem adequada para cliente? Sem leaks internos?
2. Revisar `apresentacao_executiva` — conteúdo preciso e bem apresentado?
3. Revisar `proposta_continuidade.md` — oferta clara e realista?
4. Aprovar cada um: `manifest_builder.py --action update-artifact --artifact [nome] --status approved`
5. Aprovar G5: `manifest_builder.py --action update-gate --gate G5 --status approved --by consultor`
**IMPOSSÍVEL BYPASSAR**: G5 protege o cliente de receber artefatos com problemas de qualidade ou informações inapropriadas.

## ★ G6 bloqueado — "HARDCODED MANUAL: confirmação para Linear não dada"

**Causa**: Gate G6 é hardcoded manual. A criação de projeto no Linear requer confirmação explícita.
**Solução**:
1. Revisar preview do projeto (epics, issues, workspace)
2. Confirmar com: "confirmo a criação do projeto" (ou equivalente inequívoco)
**IMPOSSÍVEL BYPASSAR**: G6 existe porque criar projeto no Linear é irreversível. Urgência não bypassa gate.

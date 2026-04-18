# FAQ — Método Bússola PME

## Q1: Como funciona o método Bússola PME em linhas gerais?
O método opera em 6 fases: Alinhamento → Normalização → Diagnóstico → Priorização → Plano de Ação → Acompanhamento. Cada fase tem inputs, outputs e um gate de qualidade. As fases 1–5 são executadas pelo `diagnostic-engine`; a fase 0 pelo `personalization`; a fase 6 pelo `deliverable-forge`.

## Q2: O que são labels epistêmicos?
São marcadores que classificam cada claim: `[FATO]` (verificável), `[INFERÊNCIA]` (dedução forte de sinais), `[HIPÓTESE]` (plausível mas não validado). Todos os artefatos devem ter esses labels nos claims. Hipótese nunca se torna fato sem validação documentada.

## Q3: O que é a regra R07?
R07 proíbe que o intake bruto (seed da Fase 1) seja usado diretamente em análise. O diagnóstico sempre usa `intake_normalized_v2`, que passou pela normalização com labels epistêmicos.

## Q4: O que são as regras R01–R10?
São as 10 regras de conduta do `diagnostic-engine`:
- R01: Nunca diagnosticar sem intake normalizado
- R02: Toda hipótese tem label explícito
- R03: Hipóteses não propagam como fatos
- R04: Módulo escolhido por tipo de problema
- R05: Priority score usa pesos do config
- R06: Plano sem owner/deadline/KPI é bloqueado
- R07: Input bruto nunca alimenta análise
- R08: Gates G1 e G2 nunca bypassados
- R09: decision_log registra toda decisão
- R10: diagnostic_working é trilha interna

## Q5: O que significa "trilha interna" vs "trilha cliente"?
Trilha interna = artefatos de raciocínio e análise (nunca vão para o cliente). Trilha cliente = artefatos aprovados para entrega. A separação é enforçada pelo `derivation_checker.py` que bloqueia strings de trilha interna em artefatos de cliente.

## Q6: O que é o Gate G0?
Gate G0 valida que o intake tem os 10 campos coletados ou gaps registrados para os ausentes. É sempre manual em ambos os modos. Sem G0, nenhuma análise pode ser iniciada.

## Q7: O que são os 3 gates hardcoded?
G2 (priorização), G5 (artefatos críticos), G6 (Linear). Nunca são automáticos em NENHUM modo. Existem para garantir julgamento humano em pontos críticos do processo.

## Q8: Como os pesos do método funcionam?
Os 4 pesos (normalization, diagnosis, prioritization, action_plan) somam 1.0. Cada peso modula a profundidade de análise naquela fase. Exemplo: `diagnosis: 0.40` → diagnóstico profundo com múltiplos módulos.

## Q9: O que é hypothesis_propagated?
Flag que marca quando uma hipótese não validada é usada como premissa em artefatos downstream. Indica risco: aquela ação ou conclusão depende de algo ainda não confirmado.

## Q10: Quando o sistema avança automaticamente?
Em `hands_off`: G1, G3, G4 avançam automaticamente quando a condição técnica está satisfeita. G2, G5, G6 NUNCA avançam automaticamente, independente do modo.

## Q11: O que é o consultant_config.yaml?
É o arquivo de configuração do consultor que governa todo o sistema downstream: pesos do método, modo de operação, fontes permitidas, profundidade de artefatos, e branding. Sem ele, o sistema não opera.

## Q12: Qual a diferença entre deliverable_depth lite, standard e deep?
- **lite**: owner + deadline + KPI apenas
- **standard**: + contexto e critério de sucesso
- **deep**: 5W2H completo (7 campos) por ação

## Q13: O que é o custom_agent/SKILL.md?
É uma SKILL.md gerada a partir dos artefatos do caso para reutilização em casos similares. Calibrada com o segmento e tipo de problema do caso original.

## Q14: O que é o dependency_order fixed vs flexible?
- **fixed**: ordem das fases é obrigatória (não pula fases)
- **flexible**: pode pular fases opcionais (ex: simulação)

## Q15: O que é o information_gaps.md?
Arquivo que lista campos do intake que não foram coletados, com `impact` (alto/médio/baixo) e `recommended_action` para cada gap. Permite avançar mesmo com campos ausentes, desde que os gaps estejam documentados.

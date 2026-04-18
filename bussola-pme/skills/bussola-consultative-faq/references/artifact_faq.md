# FAQ — Artefatos Bússola PME

## Trilha Interna

### Q: O que vai no hypotheses_log.md?
Registro de todas as hipóteses levantadas durante o diagnóstico. Cada entrada: id, claim com label epistêmico, sinais que suportam, status (pending/validated/rejected), recommended_validation.

### Q: O que vai no problem_tree.md?
Árvore causal: problema raiz + causas nível-1 (mínimo 3) + causas nível-2 (por causa-1). Cada nó tem label epistêmico e evidência se disponível.

### Q: O que é o diagnostic_working.md?
Trilha interna de raciocínio. Nunca vai para o cliente. Inclui todo o processo de análise, contradições, iterações. É o "rascunho" do diagnóstico.

### Q: O que vai no priority_score.md?
Tabela rankeada de problemas com scores por dimensão (impacto, urgência, esforço_inverso, alinhamento), score final, rank, e justificativa narrativa para top-3. Requer Gate G2 HARDCODED para aprovar.

### Q: O que é o decision_log.md?
Log de decisões de roteamento: qual módulo analítico foi escolhido, por que, com timestamp e raciocínio.

## Trilha Cliente

### Q: O que vai no resumo_executivo.md?
1 página (hard limit): problema principal + 3 achados + próximos passos. Para CEO/decisor. Não pode ter mais de 1500 chars (hard_cut enforçado).

### Q: O que vai no diagnostico_executivo.md?
Versão cliente do diagnóstico: problem tree resumido, top hipóteses (sem labels técnicos), módulo usado, e metodologia em linguagem simples. Um dos 3 críticos que requerem Gate G5.

### Q: O que vai no plano_acao_cliente.md?
Tabela formatada com ações, responsáveis, prazos, e indicadores de sucesso. Derivado do plano_acao.md aprovado. Campos obrigatórios: owner, deadline, kpi.

### Q: O que é o playbook_operacional.md?
Guia passo-a-passo para a equipe do cliente executar as ações sem depender do consultor. Inclui contexto, passos numerados, e critério de sucesso por ação.

### Q: Qual a diferença entre plano_acao_cliente e playbook_operacional?
`plano_acao_cliente` = tabela compacta (o quê, quem, quando, KPI). `playbook_operacional` = guia de execução detalhado (como fazer cada ação, passo a passo).

### Q: O que vai na proposta_continuidade.md?
Oferta de continuidade do trabalho consultivo: escopo proposto, entregáveis, investimento, timeline, CTA. Um dos 3 críticos para Gate G5.

## Trilha Governança

### Q: O que é o manifest.yaml?
Fonte de verdade do caso: status de todos os gates, artefatos, fase atual, modo de operação. Atualizado por `manifest_builder.py`.

### Q: O que é o qa_checklist.md?
Resultado das 7 verificações de Gate G4. Produzido por `qa_checklist_runner.py`. Requerido antes de qualquer release.

### Q: O que é o consultant_config_snapshot.yaml?
Cópia exata do consultant_config.yaml no momento do fechamento do caso. Preservado para auditoria futura.

### Q: O que é o custom_agent/SKILL.md?
SKILL.md gerada a partir do caso que pode ser usada para acelerar casos similares. Inclui contexto do segmento, problema tipo, e módulos usados.

## Sobre os 28 artefatos no total
9 internos + 8 cliente + 10 governança + 1 custom_agent = 28 artefatos. Ver `references/27_artifacts_spec.md` na skill `bussola-deliverable-forge` para spec completa.

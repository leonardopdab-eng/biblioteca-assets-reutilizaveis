# Especificação dos 28 Artefatos — Bússola PME

---

### 1. hypotheses_log
- **Trilha**: interna
- **target_chars**: 3000
- **max_chars**: 3900
- **overflow_action**: summarize
- **compression_policy**: Preservar claims com labels; remover reasoning intermediário
- **depends_on**: [intake_normalized_v2]
- **template**: none (gerado pelo diagnostic-engine)
- **human_review**: não
- **Descrição**: Registro de todas as hipóteses levantadas durante o diagnóstico com labels epistêmicos, status de validação, e recomendações de verificação.

---

### 2. problem_tree
- **Trilha**: interna
- **target_chars**: 2000
- **max_chars**: 2600
- **overflow_action**: compress_leaves
- **compression_policy**: Preservar raiz e causas nível-1; comprimir nível-2 se necessário
- **depends_on**: [hypotheses_log]
- **template**: problem_tree.md.j2
- **human_review**: não
- **Descrição**: Árvore causal com problema raiz, causas de nível-1 e nível-2, com labels epistêmicos em cada nó.

---

### 3. diagnostic_working
- **Trilha**: interna
- **target_chars**: 5000
- **max_chars**: 6500
- **overflow_action**: paginate
- **compression_policy**: NUNCA comprimir — trilha de raciocínio completa deve ser preservada
- **depends_on**: [problem_tree, hypotheses_log]
- **template**: none (gerado organicamente)
- **human_review**: não
- **Descrição**: Trilha interna completa de raciocínio diagnóstico. NUNCA compartilhar com cliente.

---

### 4. priority_score
- **Trilha**: interna
- **target_chars**: 2500
- **max_chars**: 3250
- **overflow_action**: summarize
- **compression_policy**: Preservar tabela de ranking e top-3 justificativas
- **depends_on**: [problem_tree]
- **template**: priority_score.md.j2
- **human_review**: sim (Gate G2 HARDCODED)
- **Descrição**: Tabela rankeada de problemas por score (impacto/urgência/esforço/alinhamento). Requer Gate G2 HARDCODED.

---

### 5. decision_log
- **Trilha**: interna
- **target_chars**: 4000
- **max_chars**: 5200
- **overflow_action**: archive_old
- **compression_policy**: Arquivar entradas com mais de 30 dias; preservar recentes
- **depends_on**: []
- **template**: none (append por scripts)
- **human_review**: não
- **Descrição**: Log de todas as decisões de roteamento analítico, seleção de módulos, e justificativas de priorização.

---

### 6. information_gaps
- **Trilha**: interna
- **target_chars**: 1500
- **max_chars**: 1950
- **overflow_action**: summarize
- **compression_policy**: Preservar gaps obrigatórios; sumarizar opcionais
- **depends_on**: [intake_normalized]
- **template**: none
- **human_review**: não
- **Descrição**: Lista de campos do intake ausentes, com impact e recommended_action para cada gap.

---

### 7. assumptions_log
- **Trilha**: interna
- **target_chars**: 1500
- **max_chars**: 1950
- **overflow_action**: summarize
- **compression_policy**: Preservar premissas críticas; sumarizar premissas de baixo impacto
- **depends_on**: []
- **template**: none
- **human_review**: não
- **Descrição**: Log de premissas assumidas durante a análise, com risco de cada premissa e validação recomendada.

---

### 8. module_routing_log
- **Trilha**: interna
- **target_chars**: 1000
- **max_chars**: 1300
- **overflow_action**: summarize
- **compression_policy**: Preservar decisão final; compactar reasoning
- **depends_on**: []
- **template**: none (gerado por module_router.py)
- **human_review**: não
- **Descrição**: Registro de qual módulo analítico foi selecionado e por quê para cada fase de diagnóstico.

---

### 9. intake_normalized_v2
- **Trilha**: interna
- **target_chars**: 2000
- **max_chars**: 2600
- **overflow_action**: compress
- **compression_policy**: Preservar todos os campos obrigatórios com labels; comprimir campos opcionais
- **depends_on**: [intake_normalized]
- **template**: none
- **human_review**: sim (Gate G1)
- **Descrição**: Versão estruturada e validada do intake com labels epistêmicos em cada campo. Base para todo o pipeline analítico.

---

### 10. resumo_executivo
- **Trilha**: cliente
- **target_chars**: 1500
- **max_chars**: 1950
- **overflow_action**: hard_cut
- **compression_policy**: hard_cut — 1 página, sem exceção
- **depends_on**: [diagnostico_executivo, plano_acao_cliente]
- **template**: resumo_executivo.md.j2
- **human_review**: sim (Gate G5)
- **Descrição**: Síntese de 1 página: problema principal + 3 achados + próximos passos. Para CEO/decisor.

---

### 11. diagnostico_executivo
- **Trilha**: cliente
- **target_chars**: 4000
- **max_chars**: 5200
- **overflow_action**: compress
- **compression_policy**: Preservar problem tree resumido, top hipóteses, módulo usado
- **depends_on**: [problem_tree, hypotheses_log]
- **template**: diagnostico_executivo.md.j2
- **human_review**: sim (OBRIGATÓRIO — um dos 3 críticos do Gate G5)
- **Descrição**: Versão cliente do diagnóstico: problem tree resumido, hipóteses principais, metodologia aplicada.

---

### 12. matriz_prioridades
- **Trilha**: cliente
- **target_chars**: 2000
- **max_chars**: 2600
- **overflow_action**: compress
- **compression_policy**: Preservar tabela rankeada; comprimir justificativas
- **depends_on**: [priority_score]
- **template**: matriz_prioridades.md.j2
- **human_review**: não (derivado de priority_score aprovado)
- **Descrição**: Versão cliente da priorização: tabela rankeada com scores e justificativas narrativas para os top itens.

---

### 13. plano_acao_cliente
- **Trilha**: cliente
- **target_chars**: 3500
- **max_chars**: 4550
- **overflow_action**: paginate
- **compression_policy**: NUNCA cortar ações — paginar se necessário
- **depends_on**: [plano_acao]
- **template**: plano_acao_cliente.md.j2
- **human_review**: não (derivado de plano_acao aprovado em G3)
- **Descrição**: Versão cliente do plano de ação com owner/deadline/KPI formatados para apresentação.

---

### 14. playbook_operacional
- **Trilha**: cliente
- **target_chars**: 5000
- **max_chars**: 6500
- **overflow_action**: paginate
- **compression_policy**: Preservar todos os passos; paginar se necessário
- **depends_on**: [plano_acao_cliente]
- **template**: playbook_operacional.md.j2
- **human_review**: não
- **Descrição**: Guia passo-a-passo de implementação das ações do plano, com detalhes operacionais para a equipe executar.

---

### 15. apresentacao_executiva
- **Trilha**: cliente
- **target_chars**: — (slides)
- **max_chars**: —
- **overflow_action**: reduce_slides
- **compression_policy**: Máximo 10 slides; reduzir conteúdo por slide se necessário
- **depends_on**: [diagnostico_executivo, matriz_prioridades, plano_acao_cliente]
- **template**: none (gerado por skill pptx)
- **human_review**: sim (OBRIGATÓRIO — um dos 3 críticos do Gate G5)
- **Descrição**: Deck de apresentação para reunião executiva de entrega. Inclui problema, diagnóstico, prioridades e plano.

---

### 16. relatorio_acompanhamento
- **Trilha**: cliente
- **target_chars**: 2000
- **max_chars**: 2600
- **overflow_action**: summarize
- **compression_policy**: Preservar status por ação e desvios; sumarizar contexto
- **depends_on**: [plano_acao_cliente]
- **template**: relatorio_acompanhamento.md.j2
- **human_review**: não (template para preenchimento futuro)
- **Descrição**: Template de relatório de acompanhamento para fases posteriores ao caso inicial.

---

### 17. proposta_continuidade
- **Trilha**: cliente
- **target_chars**: 2500
- **max_chars**: 3250
- **overflow_action**: compress
- **compression_policy**: Preservar oferta, escopo, investimento; comprimir contexto
- **depends_on**: [relatorio_acompanhamento, diagnostico_executivo]
- **template**: proposta_continuidade.md.j2
- **human_review**: sim (OBRIGATÓRIO — um dos 3 críticos do Gate G5)
- **Descrição**: Proposta de continuidade do trabalho consultivo. Escopo, entregáveis, investimento, e próximos passos.

---

### 18. manifest_yaml
- **Trilha**: governança
- **target_chars**: — (structured)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: Nunca comprimir — é fonte da verdade do caso
- **depends_on**: []
- **template**: manifest.yaml.j2
- **human_review**: não (atualizado por manifest_builder.py)
- **Descrição**: Arquivo de controle do caso com status de todos os gates, artefatos, e fases.

---

### 19. qa_checklist
- **Trilha**: governança
- **target_chars**: — (structured)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: none
- **depends_on**: [todos os artefatos]
- **template**: none (gerado por qa_checklist_runner.py)
- **human_review**: não (Gate G4 automático)
- **Descrição**: Resultado do checklist de QA Gate G4 com status por verificação.

---

### 20. anonymization_log
- **Trilha**: governança
- **target_chars**: 1000
- **max_chars**: 1300
- **overflow_action**: none
- **compression_policy**: Preservar todas as substituições — registro de auditoria
- **depends_on**: []
- **template**: none
- **human_review**: não
- **Descrição**: Log de anonimizações aplicadas ao caso para uso em showcase.

---

### 21. source_audit_log
- **Trilha**: governança
- **target_chars**: 1000
- **max_chars**: 1300
- **overflow_action**: none
- **compression_policy**: none
- **depends_on**: []
- **template**: none
- **human_review**: não
- **Descrição**: Log de todas as fontes externas acessadas durante o caso (Drive, Gmail, Notion).

---

### 22. gate_transition_log
- **Trilha**: governança
- **target_chars**: 1500
- **max_chars**: 1950
- **overflow_action**: archive_old
- **compression_policy**: Arquivar entradas antigas; preservar últimas 10
- **depends_on**: []
- **template**: none
- **human_review**: não
- **Descrição**: Log de todas as transições de gate com timestamp, quem aprovou, e condição satisfeita.

---

### 23. hypothesis_propagation_log
- **Trilha**: governança
- **target_chars**: 1000
- **max_chars**: 1300
- **overflow_action**: none
- **compression_policy**: none
- **depends_on**: [hypotheses_log]
- **template**: none
- **human_review**: não
- **Descrição**: Log de hipóteses que foram propagadas como premissas em artefatos downstream.

---

### 24. version_history
- **Trilha**: governança
- **target_chars**: — (structured)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: none
- **depends_on**: []
- **template**: none
- **human_review**: não
- **Descrição**: Histórico de versões dos artefatos principais com timestamps e changes.

---

### 25. consultant_config_snapshot
- **Trilha**: governança
- **target_chars**: — (copy)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: Cópia exata — nunca modificar
- **depends_on**: [consultant_config.yaml]
- **template**: none (cópia direta)
- **human_review**: não
- **Descrição**: Snapshot da configuração do consultor no momento do fechamento do caso.

---

### 26. intake_original
- **Trilha**: governança
- **target_chars**: — (copy)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: Cópia exata — nunca modificar
- **depends_on**: [intake_normalized]
- **template**: none (cópia direta)
- **human_review**: não
- **Descrição**: Cópia preservada do intake original (seed) antes de qualquer normalização.

---

### 27. release_notes
- **Trilha**: governança
- **target_chars**: 800
- **max_chars**: 1040
- **overflow_action**: summarize
- **compression_policy**: Preservar mudanças principais e decisões críticas
- **depends_on**: [version_history]
- **template**: none
- **human_review**: não
- **Descrição**: Notas de release do pacote final: o que foi incluído, mudanças em relação a versões anteriores.

---

### 28. custom_agent/SKILL.md
- **Trilha**: governança + reutilização
- **target_chars**: — (generated)
- **max_chars**: —
- **overflow_action**: none
- **compression_policy**: none
- **depends_on**: [consultant_config_snapshot, diagnostico_executivo, plano_acao_cliente]
- **template**: none (gerado dinamicamente)
- **human_review**: não
- **Descrição**: SKILL.md gerada a partir do caso, calibrada para casos similares. Permite reutilização do método com adaptações específicas do segmento e problema.

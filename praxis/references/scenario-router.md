# Scenario Router — Praxis

## Status: RESOLVIDO (GAP-09)
Três cenários mapeados aos três pontos de entrada mais comuns em consultoria de PME.
Selecionado pelo consultor via G-I1 ao final da Fase 1.

---

## Cenário A — Diagnóstico Completo

### Quando usar
Cliente novo. Problema não completamente entendido. Engajamento consultivo estruturado completo.

### Frases de entrada (G-I1 trigger)
- "Quero fazer um diagnóstico completo da empresa"
- "Cliente novo, preciso entender tudo"
- "Engajamento completo"
- "Quero o dossiê completo"

### Pipeline
Todas as 6 fases obrigatórias. Sem pulos.

```
Fase 1 (completa) → Fase 2 → Fase 3 → Fase 4 → Fase 5 → Fase 6
```

### Corpus gerado
- Intake completo com todos os 10 campos
- Análise diagnóstica completa (A-06 + A-09 Full)
- Simulação de cenários (A-10 + A-11 se aprofundado)
- Plano de ação 5W2H completo
- Proposta comercial opcional (Fase 2)
- Dossiê completo: A-MASTER + A-FINAL + A-OPS

### Tier de análise padrão
Full (A-09) — aciona todos os 19 frameworks aplicáveis ao problema.

### Duração estimada
4–8 horas de trabalho ativo do consultor em 1–3 sessões.

### Comportamento dos gates
Todos os gates G0–G6 ativos. G2, G5, G6 hardcoded para revisão humana.

---

## Cenário B — Revisão e Atualização

### Quando usar
Cliente que já foi atendido. Caso anterior existe. Atualizar diagnóstico, verificar andamento do plano, ou adicionar nova camada analítica.

### Frases de entrada (G-I1 trigger)
- "Cliente que já atendi"
- "Retomar caso anterior"
- "Atualizar diagnóstico"
- "Como está o plano que fizemos?"
- "Nova sessão com cliente existente"

### Pipeline
```
Fase 1 (abreviada) → Fase 3 (atualização) → Fase 5 (merge) → Fase 6
Fase 2 e Fase 4: OPCIONAIS (consultor decide)
```

### Corpus gerado
- Intake delta: apenas campos que mudaram desde o caso anterior
- Análise comparativa: o que mudou desde o último engajamento
- Plano de ação atualizado: progresso nos itens anteriores + novos itens
- Relatório de evolução: documento delta (atual vs anterior)

### Tier de análise padrão
Lean (A-08) — atualização focada, sem re-análise completa.

### Duração estimada
1,5–3 horas de trabalho ativo do consultor.

### Comportamento dos gates
- G0 (abreviado): verificar 5 campos mínimos + campos alterados
- G1: ativo
- G2: ativo e HARDCODED (revisão humana obrigatória mesmo em updates)
- G3, G4, G6: opcionais conforme escopo acordado
- G5: ativo e HARDCODED

### Comportamento especial
- Se `case_id_previous` presente no manifest: Fase 5 carrega o A-MASTER anterior e compila delta
- O novo A-MASTER referencia o anterior com seção "Evolução desde [data]"
- Preservar trilha epistêmica do caso anterior

---

## Cenário C — Proposta Comercial Rápida

### Quando usar
Reunião de prospecção acabou de acontecer. Consultor precisa de proposta profissional rápida antes que a oportunidade esfrie. Diagnóstico completo ainda não foi contratado.

### Frases de entrada (G-I1 trigger)
- "Acabei de reunião com cliente novo"
- "Preciso de proposta rápida"
- "Só quero gerar proposta agora"
- "Qualificar oportunidade primeiro"
- "Proposta antes do diagnóstico"

### Pipeline
```
Fase 1 (mínima, 5 campos) → Fase 2 (foco em proposta) → Fase 6 (entrega)
Fases 3, 4, 5: PULADAS
```

### Corpus gerado
- Intake mínimo (5 campos obrigatórios do Cenário C)
- A-02: Proposta Comercial estruturada
- A-03: Contrato de Fechamento (opcional)
- SEM diagnóstico, SEM plano de ação, SEM simulação

### Campos obrigatórios no Cenário C (5)
1. company_name
2. segment
3. primary_problem
4. urgency_level
5. decision_makers

### Estrutura da Proposta (A-02 no Cenário C)
1. **Cabeçalho**: branding do consultor + nome do cliente + data
2. **Contextualização**: 1 parágrafo resumindo o problema conforme entendido no intake
3. **Nossa abordagem**: metodologia PRAXIS em linguagem consultiva — sem jargão de IA
4. **O que você vai receber**: lista de entregáveis (diagnóstico executivo, plano de ação, planilha operacional, sessão de apresentação)
5. **Investimento**: [PLACEHOLDER — consultor preenche antes de enviar]
6. **Prazo**: sugestão de cronograma (padrão: 2–3 semanas para engajamento completo)
7. **Próximo passo**: CTA único e claro ("Confirme até [DATA] para reservar sua vaga")
8. **Assinatura**: consultant_display_name + cargo + contato

### Tier de análise
Não aplicável — Fase 3 não é executada no Cenário C.

### Duração estimada
20–45 minutos de trabalho ativo do consultor.

### Comportamento dos gates
- G0 apenas (5 campos mínimos)
- Todos os outros gates: auto-passados ou pulados

### Nota importante
O Cenário C NÃO produz diagnóstico ou plano de ação.
Se o cliente aceitar a proposta, iniciar um novo caso com Cenário A para o engajamento completo.

---

## Apresentação G-I1 ao Consultor

Exibir após G0 passar no final da Fase 1:

```
Intake normalizado. Qual caminho deseja seguir para este caso?

  a) Diagnóstico Completo — engajamento estruturado completo (4–8h, todas as fases)
  b) Revisão — cliente existente, atualizar diagnóstico anterior (1,5–3h)
  c) Proposta Rápida — apenas proposta comercial agora (20–45 min, sem diagnóstico)

Digite a letra da opção.
```

Registrar em manifest: `scenario_selected: "A" | "B" | "C"`

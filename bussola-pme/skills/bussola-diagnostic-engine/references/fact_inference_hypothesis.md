# Política Epistêmica — Fato, Inferência e Hipótese

## Definições

### [FATO]
Informação fornecida diretamente pelo cliente, extraída de documento verificável (DRE, CRM, contrato), ou confirmada por fonte externa confiável. Pode ser citado sem qualificação adicional.

**Critério**: "Se o cliente contestar, posso mostrar a fonte."

### [INFERÊNCIA]
Dedução forte a partir de múltiplos sinais indiretos consistentes. Não foi declarado explicitamente, mas é a conclusão mais provável dado o conjunto de evidências. Deve ser comunicada como inferência, não como certeza.

**Critério**: "Múltiplos dados apontam nessa direção, mas não foi dito explicitamente."

### [HIPÓTESE]
Claim plausível mas sem evidência direta ou conjunto de sinais suficiente. Pode estar certa ou errada. Deve ser tratada como hipótese de trabalho até validação documentada.

**Critério**: "Faz sentido dado o contexto, mas ainda precisa de validação."

---

## Regras de Propagação

### Regra de não-elevação
Hipótese **nunca** se torna Inferência ou Fato automaticamente. A elevação requer:
1. Coleta de evidência direta (para promover a Fato)
2. Convergência de múltiplos sinais (para promover a Inferência)
3. Registro explícito da validação no `hypotheses_log.md`

### Flag de propagação explícita
Quando uma hipótese é usada downstream sem ser validada, ela deve ser marcada com:
```yaml
hypothesis_propagated: true
propagation_reason: "Usada no plano de ação como premissa de trabalho — requer validação antes da execução"
```

### Hierarquia de labels
```
[FATO] > [INFERÊNCIA] > [HIPÓTESE]
```
Nunca rebaixar um Fato confirmado. A hierarquia é unidirecional para baixo apenas em caso de contradição.

---

## 5 Exemplos: Antes/Depois

### Exemplo 1 — Causa de queda em vendas

**Antes (mal-labeled)**:
> "O pipeline caiu porque o ICP está desatualizado."

**Depois (bem-labeled)**:
> "O pipeline caiu 40% em 4 meses [FATO — relatório CRM]. Uma das causas prováveis é o ICP desatualizado [HIPÓTESE — cliente não verificou last update do ICP]. Sinais indiretos sugerem que o perfil de leads no topo de funil mudou [INFERÊNCIA — taxa de conversão lead→reunião caiu de 30% para 12% nos últimos 2 meses]."

### Exemplo 2 — Faturamento estimado

**Antes (mal-labeled)**:
> "A empresa fatura cerca de R$ 800k/ano."

**Depois (bem-labeled)**:
> "A empresa está na faixa R$ 500k–R$ 1M [FATO — informado pelo sócio no intake]. Estimativa de R$ 800k [INFERÊNCIA — média da faixa, consistente com tamanho de equipe de 6 pessoas e segmento agência B2B]."

### Exemplo 3 — Problema de gestão

**Antes (mal-labeled)**:
> "A empresa não tem processos definidos."

**Depois (bem-labeled)**:
> "A empresa não possui playbook documentado de vendas [HIPÓTESE — consultor não teve acesso a documentação; cliente não mencionou existência de processos formais]. Ausência de reuniões de pipeline estruturadas foi mencionada [FATO — sócio afirmou 'não temos ritual de pipeline']."

### Exemplo 4 — Decisor identificado

**Antes (mal-labeled)**:
> "Rafael é o responsável pelo comercial."

**Depois (bem-labeled)**:
> "Rafael Lima é listado como responsável comercial [FATO — intake, campo decision_makers]. Nível de autonomia para decisões de contratação é desconhecido [HIPÓTESE — não foi perguntado; estrutura decisória não mapeada]."

### Exemplo 5 — Urgência

**Antes (mal-labeled)**:
> "O problema precisa ser resolvido em 30 dias."

**Depois (bem-labeled)**:
> "Urgência declarada como 'high' pelo sócio [FATO — campo urgency_level no intake]. Impacto de não resolver em 30 dias estimado em perda de R$ 80k em receita recorrente [INFERÊNCIA — baseado no ticket médio declarado e taxa de churn mencionada]."

---

## Checklist de Validação Epistêmica

Execute antes de finalizar qualquer artefato de diagnóstico:

- [ ] Todos os claims no artefato têm um label explícito (`[FATO]`, `[INFERÊNCIA]`, `[HIPÓTESE]`)
- [ ] Nenhuma hipótese foi usada como premissa de ação sem flag `hypothesis_propagated: true`
- [ ] Toda inferência tem pelo menos 2 sinais indiretos documentados
- [ ] Nenhum fato foi degradado a inferência sem contradição documentada
- [ ] O `hypotheses_log.md` lista todas as hipóteses com status atual
- [ ] Hipóteses críticas têm `recommended_validation` preenchido
- [ ] Artefatos de trilha cliente não contêm labels de trilha interna explicitamente

---

## Validação documentada (exemplo)

```yaml
# Em hypotheses_log.md
- id: H-001
  claim: "ICP da empresa está desatualizado"
  label: HIPÓTESE
  created_at: 2026-04-17
  signals:
    - "Taxa lead→reunião caiu de 30% para 12% [INFERÊNCIA]"
    - "Cliente não atualizava personas desde 2023 [FATO — declarado]"
  recommended_validation: "Revisão do ICP doc + entrevista com 3 clientes recentes"
  validation_status: pending
  hypothesis_propagated: false
```

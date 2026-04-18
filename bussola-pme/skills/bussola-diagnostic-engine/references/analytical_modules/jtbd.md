# Módulo: JTBD (Jobs to Be Done)

## Quando usar
- Produto ou serviço com baixa adoção, alto churn, ou clientes insatisfeitos sem motivo aparente
- Empresa não consegue articular por que clientes compram (ou não compram)
- Lançamento de nova oferta ou reposicionamento de serviço existente
- **Sinal trigger**: "cliente não engaja", "por que compram", "proposta de valor fraca", "churn sem motivo"

## Inputs necessários
- Descrição do produto/serviço em intake_normalized_v2
- Acesso a pelo menos 2–3 clientes recentes para entrevistas
- Histórico de motivos de churn (se disponível)

## Framework JTBD para PMEs

O cliente "contrata" um produto/serviço para realizar um "job" — uma mudança de estado desejada.

```
"Quando [situação], quero [motivação], para [resultado desejado]"
```

### Dimensões do job

| Dimensão | Pergunta | Exemplo BP-001 |
|----------|----------|----------------|
| Funcional | O que precisa ser feito? | "Gerar reuniões com leads qualificados" |
| Emocional | Como quer se sentir? | "Confiante que o comercial está funcionando" |
| Social | Como quer ser visto? | "Reconhecido como gestor que está crescendo a empresa" |

## Processo de aplicação

1. **Entrevistar 3–5 clientes** com roteiro JTBD (passado, presente, alternativas)
2. **Identificar o job principal** (functional) e jobs secundários (emotional, social)
3. **Mapear forças** que impulsionaram a contratação (push/pull)
4. **Mapear fricções** que quase impediram (anxiety/habit)
5. **Comparar** job declarado vs. job real vs. job não atendido
6. **Atualizar** proposta de valor com linguagem do cliente

## Output esperado

```markdown
## JTBD — Agência BP-001

### Job Principal (Funcional)
"Quando percebo que meu pipeline está caindo, quero entender a causa raiz e ter um plano de ação
claro, para recuperar a previsibilidade de receita sem precisar contratar mais um sócio."

### Jobs Secundários
- Emocional: "Quero sair das reuniões com Marina sentindo que tenho controle da situação" [HIPÓTESE]
- Social: "Quero mostrar para meu sócio que estou agindo proativamente" [HIPÓTESE]

### Forças de Contratação
- Push (problemas atuais): Pipeline caindo por 4 meses sem diagnóstico [FATO]
- Pull (atração): Método estruturado com entregáveis claros [INFERÊNCIA]

### Fricções identificadas
- Anxiety: "Consultor vai me dar diagnóstico mas eu vou ter que executar sozinho?" [HIPÓTESE]
- Habit: "Já tentamos resolver internamente antes" [FATO — mencionado pelo sócio]

### Gap de job atendido
O serviço atual (diagnóstico + plano) atende job funcional mas pode deixar anxiety sem resposta.
Oportunidade: Incluir playbook operacional no entregável [INFERÊNCIA — baseado na fricção identificada].
```

## Template de saída

```yaml
job_statement: "string — Quando X, quero Y, para Z"
functional_job: "string"
emotional_job: "string [label]"
social_job: "string [label]"
push_forces: [list]
pull_forces: [list]
anxieties: [list]
habits: [list]
job_gap: "string — o que não está sendo atendido"
recommendation: "string"
```

## Limitações

- **Requer entrevistas reais**: JTBD baseado só em suposições é inválido
- **Não quantifica impacto financeiro**: Use Pareto depois para priorizar jobs
- **Ciclo longo**: Entrevistas levam 1–2 semanas; não adequado para urgência crítica
- **Não use** para diagnóstico de operações internas (use Ishikawa ou PDCA)

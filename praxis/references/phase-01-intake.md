# Fase 1 de 6 — Briefing e Roteamento

## Responsabilidade
Receber briefing bruto (texto, notas, transcrição de áudio), normalizar todos os campos,
aplicar rótulos epistêmicos, identificar lacunas, selecionar cenário via G-I1, produzir A-01.

## Abertura ao Consultor
```
Fase 1 de 6 — Briefing e Roteamento | Artefatos: 0 | ~15–30 min

Compartilhe o briefing deste caso. Pode ser:
  — texto livre (notas de reunião, e-mail do cliente, anotações)
  — transcrição de áudio
  — formulário preenchido

Cole o conteúdo abaixo.
```

## Passo 1: Receber Briefing Bruto
Aceitar qualquer formato de entrada: texto colado, upload de arquivo, ou ditado.
Preservar a íntegra do briefing original antes de qualquer processamento.

## Passo 2: Normalização — 10 Campos

Extrair e estruturar os seguintes campos do briefing:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| company_name | string | SIM | Nome da empresa cliente |
| segment | string | SIM | Setor/segmento de atuação |
| team_size | string | SIM | Número de funcionários ou faixa |
| annual_revenue_range | string | SIM | Receita anual (faixa aceitável) |
| primary_problem | string | SIM | Problema principal declarado |
| urgency_level | enum | SIM | alta / média / baixa |
| decision_makers | list | SIM | Nome(s) + cargo(s) dos decisores |
| secondary_problems | list | NÃO | Problemas secundários mencionados |
| previous_diagnosis | string | NÃO | Diagnósticos ou consultorias anteriores |
| available_documents | list | NÃO | Documentos que o cliente pode fornecer |

**Campos obrigatórios (7)**: company_name, segment, team_size, annual_revenue_range,
primary_problem, urgency_level, decision_makers.

## Passo 3: Aplicar Rótulos Epistêmicos

Após extrair cada campo, rotular cada afirmação com:
- **[FATO]** — declarado explicitamente pelo cliente como dado verificável
- **[INFERÊNCIA]** — deduzido do contexto com lógica clara
- **[HIPÓTESE]** — plausível mas não confirmado

Exemplo de saída normalizada:
```
company_name: "TechFlow Soluções" [FATO]
segment: "SaaS B2B, gestão de frotas" [FATO]
team_size: "~25 pessoas" [INFERÊNCIA — briefing menciona "equipe pequena" e 3 departamentos]
annual_revenue_range: "R$2M–4M" [HIPÓTESE — estimado pelo consultor; cliente não confirmou]
primary_problem: "Churn elevado nos últimos 2 trimestres" [FATO]
urgency_level: alta [FATO — cliente usou "urgente" explicitamente]
decision_makers: ["João Faria — CEO", "Ana Costa — COO"] [FATO]
```

## Passo 4: Identificar Lacunas

Para cada campo obrigatório ausente, documentar:
```yaml
gap:
  field: annual_revenue_range
  impact: alto
  recommended_action: "Solicitar DRE ou extrato bancário ao cliente"
  gap_documented: true
```

Exibir ao consultor: "Encontrei X lacunas nos dados de intake. Veja abaixo e decida como prosseguir."

## Passo 5: Capacidades Embutidas na Fase 1

### Modo FAQ
Se o consultor perguntar sobre o método antes de colar o briefing:
Responder com base em `references/consultor-voice.md`. Não iniciar análise. Retornar à coleta.

### Suite de Templates de Negócio
Se o consultor solicitar templates de processo (ex: "template de agenda de reunião com cliente"):
Fornecer template estruturado em português. Não misturar com o fluxo de análise.

### Modo 3-Step Hands-Off
Se o consultor ativar com "modo automático" ou "rodar sem pausas":
Fases 1, 3 e 4 executam sem interrupção se todas as condições dos gates auto forem satisfeitas.
Fases com gates HARDCODED (G2, G5, G6) SEMPRE pausam — sem exceção.

### Sugestões MCP (opcional)
Se disponível: sugerir Google Drive para pré-preenchimento, Gmail para extração de e-mails do cliente.
Nunca obrigar. Sempre opcional.

## Passo 6: Gate G0 — Completude do Intake

```
VERIFICAÇÃO G0 — AUTOMÁTICA

Campos obrigatórios presentes: N/7
Campos com lacuna documentada: N
Status: PASS | FAIL

Se FAIL: listar campos faltantes. Solicitar completude ou documentação de lacuna.
Se PASS: avançar para seleção de cenário.
```

## Passo 7: Seleção de Cenário (G-I1)

Após G0 passar, apresentar:
```
Qual caminho deseja seguir para este caso?

  a) Diagnóstico Completo — engajamento estruturado completo (4–8h, todas as fases)
  b) Revisão — cliente existente, atualizar diagnóstico anterior (1,5–3h)
  c) Proposta Rápida — apenas proposta comercial agora (20–45 min, sem diagnóstico)

Digite a letra da opção.
```

Registrar escolha em manifest: `scenario_selected: "A" | "B" | "C"`

## Passo 8: Produzir A-01 (Normalized Follow Up)

Estrutura do A-01:
```markdown
# A-01 — Normalized Follow Up
## Dados Normalizados
[todos os 10 campos com rótulos epistêmicos]
## Lacunas Documentadas
[lista de gaps com impact + recommended_action]
## Cenário Selecionado: [A/B/C]
## Informações Contextuais Adicionais
[qualquer dado do briefing não encaixado nos campos acima]
```

## Conclusão da Fase

```
Fase 1 concluída.
Você teria levado entre 45 min e 1h30 para normalizar manualmente este briefing.
O sistema fez isso em minutos com rastreabilidade epistêmica completa.

Artefato produzido: A-01 (Normalized Follow Up)
Próxima fase: Fase 2 — Personalização e Artefatos Comerciais
```

Atualizar manifest:
- `current_phase: 2`
- `artifacts_produced: [{artifact_id: "A-01", ...}]`
- `gates_passed: [{gate: "G0", approved_by: "AUTO", timestamp: "..."}]`

## Definição de Pronto (Fase 1)

- [ ] A-01 produzido com rótulos epistêmicos em todas as afirmações
- [ ] Gate G0 passou (7 campos presentes ou gaps documentados)
- [ ] Cenário selecionado via G-I1
- [ ] manifest.yaml atualizado: current_phase=2, artifacts=[A-01]

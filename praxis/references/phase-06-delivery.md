# Fase 6 de 6 — Entregáveis Finais

## Responsabilidade
Aplicar personalização da Fase 2 ao A-MASTER. Produzir entregáveis terminais ao cliente.
Executar QA G4. Obter aprovação humana G5. Confirmar handoff G6.

## Abertura ao Consultor
```
Fase 6 de 6 — Entregáveis Finais | Artefatos: N | ~30–60 min

Dossiê compilado (A-MASTER pronto).
Agora vamos gerar os entregáveis finais para o cliente.
```

## Passo 1: Carregar Tokens de Personalização da Fase 2

Carregar de manifest.client_identity.branding:
- consultant_display_name, consultant_company
- primary_color, accent_color (substituir defaults do design system)
- logo_path (ou fallback para nome do consultor)
- font_family

Aplicar a todos os documentos gerados nesta fase.

## Passo 2: Carregar Regras de Voz do Cliente

Carregar `references/cliente-voice.md`.
Todas as strings em A-FINAL e A-OPS seguem essas regras sem exceção.

## Passo 3: Produzir A-FINAL

Template base: `assets/diagnostico-executivo-template.md`

Aplicar ao A-MASTER (apenas `[TRILHA_CLIENTE]`):
1. Substituir cabeçalhos técnicos por linguagem executiva
2. Converter rótulos epistêmicos para linguagem de cliente (regras de `cliente-voice.md`)
3. Aplicar branding: capa, cabeçalhos de página, rodapés
4. Garantir seções mínimas: Contextualização, Diagnóstico, Prioridades, Plano de Ação, Próximos Passos
5. Página de capa com design do sistema (background navy, título em branco)

A-FINAL NUNCA contém:
- Conteúdo marcado [TRILHA_INTERNA]
- IDs de artefatos (A-01, A-MASTER, etc.)
- Nomes de gates ou fases
- Menção a Claude/Anthropic/IA
- Rótulos epistêmicos brutos [FATO] [INFERÊNCIA] [HIPÓTESE]

## Passo 4: Produzir A-OPS (Planilha Executiva)

Template: `assets/executive-xls-template.md`
Produzido por `scripts/generate_executive_xls.py`

**Abas obrigatórias**:
1. **Resumo Executivo**: case_id, consultor, cliente, data, sumário por fase
2. **Diagnóstico**: árvore de problemas com causas raiz, rótulos, scores de prioridade
3. **Plano de Ação**: tabela 5W2H (O quê, Por quê, Quem, Quando, Onde, Como, Quanto)
4. **Simulação**: matriz de cenários (conservador/base/otimista × métricas-chave)
5. **Próximos Passos**: itens de ação com responsável, prazo, KPI

Aplicar estilos XLSX do design system (header navy, linhas alternadas, Inter 10pt).
Aplicar branding: cor da aba ativa = cor de destaque do consultor.

## Passo 5: Gate G4 — QA Programático

Executar `scripts/validate_qa.py` contra os artefatos produzidos.

Apresentar resultado ao consultor:
```
PRAXIS QA — Gate G4
Total de checks: 20
Passou: N | Falhou: N

[se falhas: listar problemas]
```

Se G4 FALHAR:
- Listar todos os problemas encontrados
- Solicitar revisão específica
- Re-executar validate_qa.py após correções

Se G4 PASSAR: avançar para G5.

## Passo 6: Gate G5 — APROVAÇÃO HUMANA HARDCODED

**NUNCA AUTO-AVANÇAR. Sem exceção.**

Apresentar pacote completo ao consultor:
```
Pacote de entregáveis pronto para revisão final.

Artefatos disponíveis:
  — A-FINAL: [nome do arquivo]
  — A-OPS: [nome do arquivo]
  — ZIP de auditoria: [nome do arquivo]

Revise os documentos acima.

Para aprovar e finalizar: escreva "aprovar"
Para solicitar revisão: descreva o que ajustar
```

Se aprovado: registrar em manifest com timestamp. Avançar para G6.
Se revisão: aplicar mudanças, re-executar G4, reapresentar para G5.

## Passo 7: Gate G6 — HANDOFF HARDCODED

**NUNCA AUTO-AVANÇAR. Sem exceção.**

```
Caso aprovado. Deseja confirmar o handoff de execução?

  a) Sim — exportar para ferramenta de gestão (Linear / Jira / Notion)
  b) Sim — enviar notificação (Slack / e-mail)
  c) Não — encerrar caso sem handoff externo

Digite a letra da opção.
```

Se a ou b: verificar disponibilidade do MCP (Linear, Slack) antes de executar.
Se c: registrar skip explícito em manifest. Caso encerrado.

## Passo 8: Loop Pós-Entrega (opcional)

Após G5 aprovado, oferecer:
```
O caso está concluído. Deseja:

  a) Gerar conteúdo de marketing deste caso (post LinkedIn, case study anônimo)
  b) Abrir um novo caso para este mesmo cliente (Cenário B — Revisão)
  c) Abrir um novo caso para um novo cliente
  d) Encerrar

Digite a letra da opção.
```

Opções a/b/c reentram na Fase 1 com contexto pré-carregado.

## Conclusão da Fase

```
Caso concluído. Entregáveis profissionais prontos para o cliente.
Este dossiê representaria entre 15 e 40 horas de trabalho manual de consultoria.

Artefatos entregues: A-FINAL, A-OPS, ZIP de auditoria
Status: caso encerrado | handoff confirmado
```

## Definição de Pronto (Fase 6)

- [ ] A-FINAL produzido com branding aplicado
- [ ] A-OPS (planilha executiva) produzida com todas as 5 abas
- [ ] Gate G4 (QA) aprovado programaticamente
- [ ] Gate G5 recebeu aprovação humana explícita
- [ ] Gate G6 confirmado ou explicitamente pulado
- [ ] manifest.yaml atualizado com status final

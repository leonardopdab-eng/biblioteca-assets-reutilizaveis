# Fase 5 de 6 — Compilação do Dossiê

## Responsabilidade
Agregar todos os artefatos produzidos nas fases 1–4 em um único documento mestre (A-MASTER).
A subroutine de compilação (Agente 00) aplica as Regras C1–C8.

## Abertura ao Consultor
```
Fase 5 de 6 — Compilação do Dossiê | Artefatos: N | ~20–45 min

Todos os artefatos das fases anteriores estão prontos.
Vamos compilar o dossiê completo deste caso.
```

## Três Fontes de Input

1. **Artefatos em conversa**: produzidos nas Fases 1–4, registrados em manifest.artifacts_produced
2. **Arquivos de referência**: documentos enviados pelo consultor durante o caso
3. **Google Drive** (se MCP disponível): documentos listados em manifest.client_identity.drive_references

Prioridade: (1) artefatos em conversa > (2) arquivos enviados > (3) Google Drive

## Passo 1: Diretiva de Compilação (G-I6)

```
Como você quer estruturar o dossiê final?

  a) Completo — todas as seções + apêndices + trilha epistêmica
  b) Executivo — seções principais sem apêndices técnicos
  c) Apenas Plano de Ação — compilar somente ações e próximos passos
  d) Personalizado — especifique quais seções incluir

Digite a letra da opção.
```

## Passo 2: Subroutine de Compilação (Agente 00)

A subroutine é acionada automaticamente após confirmação do G-I6.
Não tem interface interativa — processa e reporta resultado.

### Regra C1 — Resolução de Fontes
Coletar artefatos em ordem: manifest.artifacts_produced (por fase ASC, timestamp ASC),
depois arquivos enviados, depois Google Drive. Conflito: versão em conversa prevalece.

### Regra C2 — Estrutura do Documento
Montar A-MASTER nesta ordem fixa:
```
# [CLIENT NAME] — Dossiê Consultivo PRAXIS
## Seção 1: Contexto e Situação (de A-01)
## Seção 2: Identidade e Proposta Comercial (de A-02/A-03/A-04 conforme aplicável)
## Seção 3: Diagnóstico (de A-06 + A-07/A-08/A-09 per tier)
## Seção 4: Cenários e Simulações (de A-10, A-11 se produzido)
## Seção 5: Plano de Ação (sintetizado de Fases 3 + 4)
## Seção 6: Próximos Passos e Handoff (ações com responsáveis + prazos)
## Apêndice A: Log de Decisões (timestamps de gates + aprovações)
## Apêndice B: Trilha Epistêmica (todos os rótulos [FATO]/[INFERÊNCIA]/[HIPÓTESE])
```

### Regra C3 — Normalização de Cabeçalhos
- H1: apenas o título do documento (um por documento)
- H2: as 6 seções + apêndices
- H3: sub-tópicos dentro de cada seção
- H4: itens individuais (problemas, ações, cenários)
- Remover conflitos de nível antes de inserir conteúdo dos artefatos fonte

### Regra C4 — Deduplicação
Antes de inserir conteúdo de qualquer artefato:
- Verificar se afirmação equivalente (similaridade semântica >80%) já existe
- Se duplicata: manter versão mais recente com rótulo epistêmico mais específico
- Registrar cada decisão de deduplicação em compilation_log.md

### Regra C5 — Preservação de Rótulos Epistêmicos
Todo [FATO], [INFERÊNCIA], [HIPÓTESE] dos artefatos fonte DEVE ser preservado em A-MASTER.
Labels nunca são removidos durante compilação.
Se um label estiver ausente em um claim que existia em artefato fonte: reaplicar o label original e registrar a restauração em compilation_log.md.

### Regra C6 — Separação de Trilhas
A-MASTER contém duas trilhas marcadas inline:
- `[TRILHA_INTERNA]`: conteúdo apenas para o consultor (raciocínio diagnóstico, hipóteses de trabalho)
- `[TRILHA_CLIENTE]`: conteúdo seguro para entrega ao cliente final

A Fase 6 usa APENAS `[TRILHA_CLIENTE]` ao produzir A-FINAL.
`[TRILHA_INTERNA]` é incluída no ZIP de auditoria mas nunca em entregáveis ao cliente.

### Regra C7 — Verificação de Completude Mínima
Antes de produzir A-MASTER, verificar:
- [ ] Seção 1 tem ao menos 3 campos normalizados de A-01
- [ ] Seção 3 tem ao menos 1 causa raiz identificada
- [ ] Seção 5 tem ao menos 1 ação com responsável e prazo
- [ ] Ao menos 1 [FATO] presente no documento

Se qualquer check falhar: reportar ao consultor antes de produzir. Listar elementos faltantes.

### Regra C8 — Formato de Saída
A-MASTER: arquivo UTF-8 markdown salvo como `master_[case_id].md`
Companion: `compilation_log.md` listando cada artefato merged, decisão de deduplicação, restauração de label.

## Passo 3: Artefatos Adicionais (opcionais)

**A-MASTER-LINEAR**: versão formatada para exportação de PM (Linear/Jira)
- Issues por ação do Plano de Ação
- Epics por seção do dossiê

**Ebook interativo (HTML)**: versão navegável do dossiê (opção para clientes tech)

**ZIP de auditoria**: todos os artefatos + compilation_log.md + manifest.yaml

## Passo 4: Plano de Ação (penúltimo step)

Antes da entrega ao cliente, sintetizar plano de ação consolidado a partir de todas as fases:
- Ações por responsável
- Prazo de cada ação
- KPI de acompanhamento
- Dependências entre ações

## Conclusão da Fase

```
Fase 5 concluída.
Dossiê completo compilado de [N] artefatos. Compilação manual equivalente: 2 a 5 horas.

Artefatos produzidos: A-MASTER, A-12 (Architect Pack), [A-MASTER-LINEAR se solicitado]
Próxima fase: Fase 6 — Entregáveis Finais
```

Atualizar manifest: current_phase=6, A-MASTER com hash SHA256, A-12 registrado.

## Definição de Pronto (Fase 5)

- [ ] A-MASTER produzido e não vazio (Regras C1–C8 aplicadas)
- [ ] compilation_log.md gerado ao lado de A-MASTER
- [ ] ZIP de auditoria entregue ao consultor
- [ ] manifest.yaml atualizado: current_phase=6, hash de A-MASTER registrado

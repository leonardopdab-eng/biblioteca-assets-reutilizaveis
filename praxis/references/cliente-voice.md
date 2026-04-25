# Cliente Voice — Praxis

## Quem é o Cliente Final
Empresário ou executivo de PME brasileira. Pode não ter formação formal em gestão.
Domina profundamente o próprio setor. Desconfia de jargão. Respeita clareza e evidência.
Recebe os entregáveis do consultor — nunca interage diretamente com o sistema.

---

## Princípios de Tom

1. **Registro de consultoria sênior** — não acadêmico, não coloquial
2. **Baseado em evidência** — cada recomendação tem rastreio a um achado
3. **Português brasileiro padrão** — não PT-Portugal, sem regionalismos, sem gírias
4. **Zero linguagem de IA** — lê como se um consultor humano sênior tivesse escrito
5. **Orientado à ação** — cada seção termina com implicação ou ação concreta

---

## Conteúdo PROIBIDO em entregáveis ao cliente

- Qualquer menção a Claude, Anthropic, IA, machine learning, "sistema"
- IDs internos de artefatos (A-01, A-MASTER, A-FINAL, etc.)
- Nomes de gates ou fases do sistema (G0, Fase 3, G-I4)
- Conteúdo marcado [TRILHA_INTERNA]
- Jargão técnico de consultoria não explicado
- Hipótese apresentada como fato
- Conselho genérico não vinculado a dados específicos do cliente
- Referências a "o processo" ou "a metodologia" de forma abstrata

---

## Convenções de Estrutura de Documento

**Cabeçalhos**: linguagem de negócio clara (não "Saída da Fase 3")
- Use: "Diagnóstico de Crescimento", "Plano de Ação", "Análise de Mercado"

**Abertura**: situação em 2–3 frases. O cliente deve reconhecer imediatamente a própria realidade.

**Corpo do documento**:
```
Achados → Causas → Implicações → Recomendações
```

**Fechamento**: próximo passo claro com responsável e prazo.

---

## Tratamento de Rótulos Epistêmicos em Documentos do Cliente

Os rótulos internos [FATO], [INFERÊNCIA], [HIPÓTESE] NÃO aparecem nos documentos do cliente.
São convertidos para linguagem executiva:

| Rótulo interno | Linguagem executiva |
|---|---|
| [FATO] | "Os dados mostram...", "Observamos que...", "Identificamos..." |
| [INFERÊNCIA] | "A análise indica...", "Com base nos dados...", "A tendência aponta para..." |
| [HIPÓTESE] | Caixa de destaque: "**Premissa a validar:** [texto]" |

**Nunca** usar os colchetes diretamente em texto entregue ao cliente.

---

## Padrões de Linguagem a Usar

**Para achados (fatos)**:
- "Os dados indicam que..."
- "Identificamos como causa principal..."
- "A empresa apresenta..."

**Para diagnóstico**:
- "A análise revela três causas inter-relacionadas..."
- "O problema central está em..."
- "O padrão recorrente é..."

**Para recomendações**:
- "Recomendamos como próximo passo..."
- "A ação de maior impacto imediato é..."
- "Propomos priorizar..."

**Para resultados esperados**:
- "O impacto esperado é..." (seguido de métrica ou faixa)
- "Em 30–90 dias, a empresa deve observar..."
- "A premissa é que..." (para hipóteses)

---

## Barra de Qualidade

Antes de qualquer entregável final:

**Pergunta de filtro**: "Um consultor sênior ficaria orgulhoso de entregar este documento a um cliente de R$10k/mês?"

Se a resposta for não: falhou. Revisar até passar.

Sinais de falha:
- Texto genérico que poderia servir a qualquer empresa
- Recomendação sem fundamento em dado do cliente
- Linguagem passiva excessiva ou evasiva
- Estrutura desorganizada ou seções desequilibradas
- Qualquer menção ao processo interno

---

## Seções Mínimas Obrigatórias (A-FINAL)

1. **Contextualização** — situação e desafio do cliente
2. **Diagnóstico** — achados principais com causas identificadas
3. **Prioridades** — o que fazer primeiro e por quê
4. **Plano de Ação** — ações com responsável, prazo e indicador
5. **Próximos Passos** — ação imediata e CTA para o cliente

---

## Formatação de Tabelas para o Cliente

Evitar tabelas com muitas colunas. Máximo 5 colunas visíveis.
Cabeçalhos em português claro.
Linha de exemplo antes da tabela principal quando útil.

## Comprimento dos Entregáveis

- A-FINAL (Tier Básico): 3–5 páginas
- A-FINAL (Tier Lean): 6–10 páginas
- A-FINAL (Tier Full): 12–20 páginas
- A-OPS: 1 spreadsheet com 5 abas, não mais de 50 linhas por aba

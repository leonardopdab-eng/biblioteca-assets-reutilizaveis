# Fase 2 de 6 — Personalização e Artefatos Comerciais

## Responsabilidade
Inicializar a camada de identidade do consultor (configuração inicial ou reutilizar existente).
Gerar artefatos comerciais personalizados com base na seleção G-I2.

## Abertura ao Consultor
```
Fase 2 de 6 — Personalização e Artefatos Comerciais | Artefatos: 1 | ~20–40 min

Recebido: A-01 (Normalized Follow Up) — [company_name], cenário [X].
```

## Passo 1: Verificar Estado da Identidade

Checar manifest: `client_identity.branding` está configurado?

**Se "estado virgem" (primeira vez ou sem branding configurado):**
Coletar via perguntas sequenciais (uma por vez):

```
Antes de gerar os documentos, preciso configurar sua identidade.
Uma pergunta de cada vez.

1. Qual é o nome da sua empresa de consultoria?
```
→ Aguardar resposta.
```
2. Qual é o seu nome de exibição como consultor? (ex: "Dr. João Silva" ou apenas "João Silva")
```
→ Aguardar resposta.
```
3. Qual é a cor principal da sua marca? (informe o código hex, ex: #1B2A4A)
   Não tem? Pressione Enter para usar o padrão profissional (#1B2A4A — navy).
```
→ Aguardar resposta.
```
4. Tem logo? Se sim, informe o caminho do arquivo ou URL.
   Não tem? Pressione Enter — usaremos seu nome em tipografia profissional.
```
→ Aguardar resposta.

Salvar em manifest: `client_identity.branding = {...}`

**Se branding já configurado:**
```
Identidade carregada: [consultant_display_name] — [consultant_company]
Cor: [primary_color] | Logo: [status]
```

## Passo 2: Aplicar Design Brand System

Carregar tokens de `references/design-system.md`.
Substituir --color-primary e --color-accent pelos valores do consultor se configurados.
Aplicar a todos os documentos gerados nesta fase.

## Passo 3: Seleção de Artefatos (G-I2)

```
Qual(is) artefato(s) deseja gerar para o caso [company_name]?

  a) Proposta Comercial — apresentar ao cliente para aprovação do engajamento
  b) Contrato de Fechamento + Showroom Case — formalizar e apresentar casos de referência
  c) Personalização do Cliente — pasta de identidade e contexto do cliente
  d) TODOS — gerar os três em pacote ZIP

Digite a letra da opção.
```

## Passo 4: Gerar Artefatos Selecionados

### Opção (a) — A-02: Proposta Comercial
Template: `assets/proposta-comercial-template.md`

Preencher com dados de A-01:
- Cabeçalho: branding do consultor + nome do cliente + data
- Contextualização: resumo do primary_problem em linguagem executiva
- Abordagem: metodologia PRAXIS em linguagem consultiva (sem jargão de IA)
- Entregáveis: lista baseada no cenário selecionado (A/B/C)
- Investimento: [PLACEHOLDER — consultor preenche antes de enviar]
- Prazo: sugestão baseada no cenário (Cenário A: 2–3 semanas; B: 1 semana; C: 48h)
- Próximo Passo: CTA claro com data-limite sugerida
- Assinatura: consultant_display_name + consultant_company + contato

Aplicar branding. Exportar como markdown formatado.

### Opção (b) — A-03: Contrato de Fechamento + Showroom
Template: `assets/contrato-fechamento-template.md`

Contrato: estrutura padrão de prestação de serviços consultivos
- Partes (consultor e cliente)
- Escopo conforme cenário (A/B/C)
- Entregáveis contratados
- Prazo e cronograma
- Condições de pagamento [PLACEHOLDER]
- Cláusula de confidencialidade padrão
- Assinaturas

Showroom Case: apresentar 1–3 cases de sucesso em formato narrativo
(Consultor fornece os dados; sistema estrutura e formata)

### Opção (c) — A-04: Personalização do Cliente
Pasta de contexto estruturada:
- Perfil normalizado do cliente (A-01 reformatado)
- ICP (Ideal Customer Profile) da empresa cliente
- Contexto de mercado do segmento
- Documentos relevantes referenciados

### Opção (d) — TODOS
Gerar A-02 + A-03 + A-04.
Empacotar em ZIP: `[company_name]-artefatos-comerciais-[date].zip`
Confirmar: "Pacote ZIP pronto para download."

## Passo 5: Confirmação de Qualidade

Antes de finalizar cada artefato, verificar:
- [ ] Branding do consultor aplicado
- [ ] Nenhuma menção a Claude, Anthropic ou IA
- [ ] Nenhum ID interno exposto (A-01, A-02, etc.)
- [ ] Problema do cliente representado com precisão
- [ ] Placeholders marcados claramente para preenchimento manual

## Reutilização na Fase 6

Os tokens de branding configurados nesta fase são reutilizados pela Fase 6
para aplicar identidade ao A-FINAL e A-OPS.
Nenhuma reconfiguração necessária.

## Conclusão da Fase

```
Fase 2 concluída.
Proposta comercial profissional gerada e personalizada.
Tempo manual equivalente: 2 a 4 horas de formatação e redação.

Artefatos produzidos: [lista dos gerados]
Próxima fase: Fase 3 — Análise Diagnóstica
```

Atualizar manifest: `artifacts_produced` com A-02/A-03/A-04 conforme seleção.

## Definição de Pronto (Fase 2)

- [ ] Identidade do consultor inicializada (nome + ao menos cor primária)
- [ ] Ao menos um artefato de a/b/c/d produzido
- [ ] Todos os documentos com branding do consultor
- [ ] manifest.yaml atualizado: artefatos A-02/A-03/A-04 registrados

# Praxis — Co-piloto de Consultoria para PMEs Brasileiras

> Transforma briefings brutos em dossiês consultivos completos.
> 6 fases estruturadas. Rastreabilidade epistêmica. Zero menção a IA nos entregáveis.

---

## O que é

Praxis é uma Claude Skill que opera como co-piloto de consultores que atendem PMEs brasileiras.
Dado um briefing bruto de cliente, orquestra 6 fases para produzir:

- **Proposta Comercial** personalizada com branding do consultor
- **Diagnóstico Executivo** com causas raiz identificadas e priorizadas
- **Plano de Ação 5W2H** com responsáveis, prazos e KPIs
- **Simulação de Cenários** (pessimista/conservador/otimista)
- **Planilha Operacional** com 5 abas para acompanhamento
- **Dossiê Completo** compilado em documento mestre

Reduz 15–40 horas de trabalho manual de consultoria por caso.

---

## Pré-requisitos

```bash
pip install pyyaml openpyxl
```

Python 3.10+ recomendado.

---

## Instalação

### Claude Code (CLI)
```bash
unzip praxis.zip -d ~/.claude/skills/
```

### Claude.ai
1. Abrir um Claude Project
2. Ir em Settings > Skills > Upload
3. Selecionar a pasta `praxis/` ou o arquivo `praxis.zip`

### API (via system prompt)
```
Inclua o conteúdo de SKILL.md no system prompt.
Carregue reference files adicionais conforme o mapa de divulgação progressiva.
```

---

## Como usar

### Novo caso
```
"Novo caso — cliente: Empresa XYZ"
[colar briefing]
```

### Retomar caso existente
```bash
# Verifique o estado atual
cat manifest.yaml | grep current_phase
```
Então: "continuar caso [nome do cliente]"

### Inicializar via script
```bash
cd seu-diretorio-de-caso/
python ~/.claude/skills/praxis/scripts/init_case.py \
  --consultant seu-id \
  --client "Nome do Cliente"
```

### Executar dry run
```bash
python ~/.claude/skills/praxis/scripts/dry_run.py
```

---

## Três Cenários de Entrada

| Cenário | Quando | Duração |
|---|---|---|
| **A — Diagnóstico Completo** | Cliente novo, engajamento completo | 4–8h |
| **B — Revisão** | Cliente existente, atualizar diagnóstico | 1,5–3h |
| **C — Proposta Rápida** | Saiu de reunião, precisa de proposta agora | 20–45 min |

---

## Gates de Qualidade

| Gate | Tipo | Descrição |
|---|---|---|
| G0 | Auto | 7 campos obrigatórios do intake presentes |
| G1 | Auto | Rótulos epistêmicos em todas as afirmações |
| **G2** | **⚠ Humano** | Revisão do diagnóstico pelo consultor |
| G3 | Auto | Simulação completa e scope confirmado |
| G4 | Auto | 20 checks programáticos de QA |
| **G5** | **⚠ Humano** | Aprovação final do pacote de entregáveis |
| **G6** | **⚠ Humano** | Confirmação do handoff de execução |

G2, G5, G6 são hardcoded — jamais auto-avançados.

---

## Estrutura de Arquivos

```
praxis/
├── SKILL.md              # Entry point (<500 linhas)
├── references/           # 17 arquivos (<300 linhas cada)
├── agents/               # 4 subagente prompts
├── scripts/              # 6 scripts Python
├── assets/               # 5 templates de documentos
└── schemas/              # 3 schemas YAML
```

---

## FAQ Rápido

**Os entregáveis mencionam IA?**
Não. Nunca. Todos os documentos do cliente leem como trabalho de consultor humano sênior.

**Preciso dos MCPs (Google Drive, Linear, Slack)?**
Não. São opcionais. A skill funciona completamente sem eles.

**Posso usar minha própria metodologia?**
Sim. Na Fase 3, o consultor injeta sua metodologia, frameworks e benchmarks via G-I3.

**Quanto custa em tokens?**
Depende do tier. Cenário C (proposta): ~10k tokens. Cenário A Full: ~50–100k tokens.

---

## Praxis — English Summary

**What**: A Claude Skill for Brazilian SME consultants. Turns raw briefings into complete
consulting dossiers (proposal, diagnosis, action plan, simulation, spreadsheet).

**Key features**: 6-phase pipeline · Epistemic labeling (FATO/INFERÊNCIA/HIPÓTESE) ·
Hardcoded human review gates · Zero AI mentions in client deliverables ·
Consultant branding applied to all outputs.

**Scenarios**: A (full diagnosis) · B (returning client review) · C (fast proposal).

**Install**: `unzip praxis.zip -d ~/.claude/skills/`

**Run**: Open Claude, say "novo caso" and paste a client briefing.

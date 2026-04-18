# Template de Projeto Linear — Bússola PME

## Estrutura padrão

```
Projeto: Bússola PME — Execução [case_id]
├── Epic: [Bússola PME] Iniciativas — [Owner 1]
│   ├── Issue: [Bússola] [Ação 1]
│   └── Issue: [Bússola] [Ação 2]
├── Epic: [Bússola PME] Iniciativas — [Owner 2]
│   └── Issue: [Bússola] [Ação 3]
└── Epic: [Bússola PME] Acompanhamento
    └── Issue: Revisão semanal do plano
```

## Labels obrigatórios

Todo recurso criado deve ter:
- `bussola-pme` — identifica origem do projeto
- `case-[id]` — ex: `case-bp-001`

Issues adicionais por tipo:
- `quick-win` — ações de baixo esforço/alto impacto
- `estratégico` — ações de longo prazo
- `bloqueado` — ações aguardando pré-requisito

## State inicial

Todos os recursos criados começam em estado `Backlog`. A equipe move para `In Progress` conforme execução.

## Estimativas padrão

| Complexidade da ação | Story Points |
|----------------------|-------------|
| Simples (< 4h) | 1 |
| Média (4h–1 dia) | 2 |
| Complexa (1–3 dias) | 3 |
| Grande (> 3 dias) | 5 |

## Campos mapeados do plano_acao

| Campo plano_acao | Campo Linear |
|------------------|-------------|
| `acao` | `title` |
| `owner` | `assignee` |
| `deadline` | `due_date` |
| `kpi` | Seção "KPI" na `description` |
| tema/owner | Epic agrupador |

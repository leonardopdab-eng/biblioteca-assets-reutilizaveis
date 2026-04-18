# Convenções de Epics e Issues — Bússola PME Linear

## Naming

### Epics
```
[Bússola PME] Iniciativas — [Owner]
```
Exemplo: `[Bússola PME] Iniciativas — Marina Costa`

### Issues
```
[Bússola] [Ação do plano]
```
Exemplo: `[Bússola] Revisar ICP e atualizar scorecard de qualificação`

## Labels obrigatórias

- `bussola-pme` — obrigatório em TODOS os recursos
- `case-[id]` — ex: `case-bp-001`
- `quick-win` — ações com esforço <= 2 e impacto >= 4
- `estratégico` — ações de impacto alto mas esforço alto

## State inicial

Todos os recursos: `Backlog`

## Estimativas por complexidade

Mapeamento da matriz esforço×impacto:
- Esforço 1 → 1 SP
- Esforço 2 → 2 SP
- Esforço 3 → 3 SP
- Esforço 4–5 → 5 SP

## Descrição padrão de issue

```markdown
## Contexto
[Origem no diagnóstico Bússola PME]

## KPI
[Indicador de sucesso definido no plano]

## Prazo
[Deadline ISO8601]

## Responsável
[Owner do plano]

---
*Gerado por Bússola PME — case [id]*
```

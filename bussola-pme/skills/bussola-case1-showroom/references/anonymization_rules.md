# Regras de Anonimização — Bússola PME Showcase

## Política de Nível Strong

Este arquivo define as regras de anonimização de nível **strong** para uso em showcase comercial.
Nunca usar dados reais não-anonimizados em qualquer material externo.

---

## Substituições de Nomes (substitutions)

```yaml
substitutions:
  # Nomes de pessoas → ficcionais genéricos
  "Marina Costa": "Ana Silva"
  "marina costa": "ana silva"
  "Marina": "Ana"
  "Rafael Lima": "Bruno Oliveira"
  "rafael lima": "bruno oliveira"
  "Rafael": "Bruno"
  "João Alves": "Carlos Mendes"
  "joao alves": "carlos mendes"
  "João": "Carlos"
  "Fernanda": "Juliana"
  "Pedro": "Marcos"

  # Nomes de empresa → segmento genérico
  "Agência BP-001": "Agência B2B [Cliente Anônimo]"
  "BP-001": "CASE-ANON"
  "BP001": "CASE-ANON"
  "Bússola PME Cliente": "[Cliente Bússola PME]"

  # Dados financeiros → faixas
  "R$ 960k": "~R$ 900k–1M"
  "R$ 960.000": "~R$ 900k–1M"
  "R$ 800k": "~R$ 750k–850k"
  "R$ 800.000": "~R$ 750k–850k"
  "R$ 1,2M": "~R$ 1,1M–1,3M"

  # Identificadores sensíveis
  "CNPJ": "[CNPJ removido]"
  "CPF": "[CPF removido]"
```

---

## Regras de Métricas (metric_rules)

### Percentuais
- Todo percentual exato deve ser convertido para faixa ±5%
- Exemplo: `43%` → `~40–45%`, `72%` → `~70–75%`

### Valores monetários (R$)
- Arredondar para faixa de 10% acima/abaixo
- Exemplo: `R$ 960k` → `~R$ 900k–1M`
- Valores ≥ R$ 1M: arredondar para 1 casa decimal (`R$ 1,2M`)
- Valores < R$ 100k: arredondar para faixa de R$ 10k

### Datas
- Datas específicas (dd/mm/yyyy) → trimestre e ano (`Q1 2025`)
- Meses específicos → `[mês] 2025`

---

## Regras de Segmento (segment_rules)

| Original | Substituição |
|----------|-------------|
| Nome exato da empresa | "empresa do segmento [X]" |
| Nicho específico | Categoria ampla |
| Cidade específica | Região (ex: "Sul do Brasil") |
| Número de funcionários exato | Faixa (ex: "5–10 pessoas") |

---

## Campos Proibidos em Showcase

Os seguintes campos jamais devem aparecer em material de showcase:

- Credenciais de acesso (senhas, tokens, chaves API)
- Endereços completos (rua + número)
- Dados bancários
- Informações de saúde ou jurídicas
- Salários individuais
- Dados de terceiros não-autorizados (clientes do cliente)

---

## Log de Auditoria

Todo processo de anonimização deve gerar `anonymization_log.md` com:

| Campo | Descrição |
|-------|-----------|
| `file` | Nome do arquivo fonte |
| `original` | Texto substituído |
| `replacement` | Texto de substituição |
| `type` | `name_substitution` / `metric_rounding` / `segment_generalization` |
| `occurrences` | Número de ocorrências substituídas |

---

## Validação Pós-Anonimização

Antes de liberar qualquer showcase, verificar manualmente:

1. Buscar o nome real da empresa no output → deve retornar zero resultados
2. Buscar nomes dos fundadores/sócios → zero resultados
3. Buscar qualquer número exato de receita → deve estar em faixa
4. Confirmar que `anonymization_log.md` lista todas as substituições realizadas

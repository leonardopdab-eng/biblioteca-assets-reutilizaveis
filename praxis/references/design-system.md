# Design System — Praxis

## Status: RESOLVIDO (GAP-08)
Especificação completa de identidade visual profissional para entregáveis B2B.
Paleta navy, tipografia Inter, grid A4. Neutro o suficiente para receber branding do consultor.

---

## Paleta de Cores

| Token | Hex | Uso |
|---|---|---|
| `--color-primary` | `#1B2A4A` | Cabeçalhos principais, títulos de seção, CTAs |
| `--color-accent` | `#2E7D9B` | Destaques, caixas de call-out, links |
| `--color-positive` | `#1A6B42` | Labels [FATO], métricas positivas |
| `--color-neutral` | `#5C6B7A` | Labels [INFERÊNCIA], texto secundário |
| `--color-caution` | `#8B5E00` | Labels [HIPÓTESE], premissas, alertas |
| `--color-surface` | `#F5F7FA` | Fundo de documento, linhas alternadas de tabela |
| `--color-divider` | `#D0D7E0` | Linhas horizontais, bordas de tabela |
| `--color-text` | `#1C2430` | Corpo de texto |
| `--color-text-muted` | `#6B7685` | Rodapés, metadados, timestamps |

**Override do consultor**: `--color-primary` e `--color-accent` são substituídos pelos
valores de `client_identity.branding.primary_color` e `accent_color` quando configurados.
Se não configurados, os defaults acima se aplicam.

---

## Tipografia

| Token | Valor | Uso |
|---|---|---|
| `--font-heading` | Inter, sans-serif | Todos os cabeçalhos H1–H4 |
| `--font-body` | Inter, sans-serif | Corpo, tabelas, bullets |
| `--font-mono` | JetBrains Mono, monospace | Blocos de código, IDs, nomes de arquivo |
| `--font-size-h1` | 24px / 1.5rem | Título do documento |
| `--font-size-h2` | 18px / 1.125rem | Cabeçalhos de seção |
| `--font-size-h3` | 14px / 0.875rem | Sub-seções |
| `--font-size-body` | 11px / 0.6875rem | Corpo de texto em documentos |
| `--font-size-caption` | 9px / 0.5625rem | Rodapés, metadados |
| `--line-height` | 1.6 | Corpo de texto |
| `--font-weight-heading` | 600 | Todos os cabeçalhos |
| `--font-weight-body` | 400 | Corpo de texto |

**Fallback stack**: `Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif`

---

## Grid de Layout (Padrão A4)

| Token | Valor | Uso |
|---|---|---|
| `--page-width` | 210mm (A4) | Largura do documento |
| `--page-height` | 297mm (A4) | Altura do documento |
| `--margin-top` | 25mm | Margem superior |
| `--margin-bottom` | 20mm | Margem inferior |
| `--margin-left` | 25mm | Margem esquerda |
| `--margin-right` | 20mm | Margem direita |
| `--content-width` | 165mm | Área de conteúdo utilizável |
| `--column-gutter` | 6mm | Espaço entre colunas (layout 2 colunas) |
| `--section-spacing` | 8mm | Espaço entre seções principais |
| `--paragraph-spacing` | 4mm | Espaço entre parágrafos |

---

## Posicionamento do Logo

- **Posição**: topo esquerdo de cada cabeçalho de página, dentro de caixa delimitadora 40mm × 15mm
- **Fallback (sem logo)**: nome de exibição do consultor em `--font-heading`, `--font-size-h3`, `--color-primary`, alinhado à esquerda
- **Nunca**: logo centralizado, logo no rodapé, ou logo misturado ao corpo do texto

---

## Estilos de Componentes

### Tabelas
- Linha de cabeçalho: fundo `--color-primary`, texto branco, `--font-weight-heading`
- Linhas alternadas: branco / `--color-surface`
- Borda: 0.5px `--color-divider`
- Padding de célula: 3mm × 4mm

### Caixa de Destaque [HIPÓTESE]
```
Borda esquerda: 3px solid --color-caution (#8B5E00)
Fundo: #FFF8EC
Label: "PREMISSA A VALIDAR" em --font-size-caption, --color-caution, maiúsculas
```

### Badge [FATO]
```
Retângulo arredondado pequeno
Fundo: --color-positive (#1A6B42)
Texto: branco, 8px
```

### Badge [INFERÊNCIA]
```
Fundo: --color-neutral (#5C6B7A)
Texto: branco, 8px
```

### Rodapé de Página
- Esquerda: nome do consultor + nome da empresa
- Centro: título do documento (truncado a 40 chars)
- Direita: "Página N de N" + data de geração
- Fonte: `--font-size-caption`, `--color-text-muted`
- Separador: 0.5px `--color-divider` acima do rodapé

### Página de Capa (A-FINAL)
```
Fundo: --color-primary (#1B2A4A)
Título (nome da empresa cliente): 32px, branco, Inter 600
Sub-título (tipo de documento): 16px, branco, Inter 400
Data: canto inferior direito, branco, --font-size-caption
Logo: centralizado, versão branca preferível, máximo 60mm de largura
Faixa de destaque: 8px --color-accent no topo e na base da página
```

---

## Estilos XLSX (A-OPS)

| Elemento | Especificação |
|---|---|
| Fundo da linha de cabeçalho | `#1B2A4A` |
| Texto do cabeçalho | Branco, Inter 10pt negrito |
| Linhas alternadas | Branco / `#F5F7FA` |
| Borda | `#D0D7E0`, thin em todas as células |
| Cor da aba (ativa) | `#2E7D9B` |
| Cor da aba (apêndice) | `#5C6B7A` |
| Fonte em todo o arquivo | Inter 10pt |
| Largura mínima de coluna | 15 caracteres |
| Altura de linha | 18pt |

---

## Aplicação do Branding do Consultor

1. Se `primary_color` configurado em manifest: substituir `--color-primary`
2. Se `accent_color` configurado: substituir `--color-accent`
3. Se `logo_path` configurado: usar na capa e cabeçalho
4. Se `font_family` configurado: substituir Inter pela fonte especificada
5. Se nenhum configurado: usar todos os defaults acima

O Design System é aplicado automaticamente pela Fase 2 e reutilizado pela Fase 6.

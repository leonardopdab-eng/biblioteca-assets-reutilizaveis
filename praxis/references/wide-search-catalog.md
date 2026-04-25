# Wide Search Catalog — Praxis

## Propósito
Fontes de pesquisa padrão para a Fase 3. O consultor pode expandir via injeção de metodologia (G-I3).
Cada fonte tem um tier de confiança epistêmica que determina o rótulo padrão da informação coletada.

---

## Fontes Primárias Brasileiras

### Sebrae
- **Tipo**: Relatórios setoriais, dados de PMEs, benchmarks de gestão
- **Uso principal**: perfil do segmento, taxas de mortalidade empresarial, melhores práticas por setor
- **Acesso**: sebrae.com.br/sites/PortalSebrae/estudos_pesquisas
- **Confiança epistêmica**: Tier 2 → [INFERÊNCIA] padrão
- **Dados típicos disponíveis**: faturamento médio por porte, número de empresas por segmento, desafios mais comuns, taxa de formalização

### IBGE — Instituto Brasileiro de Geografia e Estatística
- **Tipo**: Dados primários de censo, estatísticas econômicas, PNAD, PIA
- **Uso principal**: dados demográficos, estrutura setorial, renda, emprego
- **Bases chave**: IBGE Cidades, SIDRA, PIA (Pesquisa Industrial Anual), PAC (Pesquisa Anual do Comércio)
- **Confiança epistêmica**: Tier 1 → [FATO] para dados do censo; Tier 2 para estimativas
- **Caveats**: dados frequentemente com 2–3 anos de defasagem. Indicar data na citação.

### MDIC — Ministério do Desenvolvimento, Indústria, Comércio e Serviços
- **Tipo**: Dados de comércio exterior, competitividade, cadeias produtivas
- **Uso principal**: contexto de importação/exportação, competitividade setorial
- **Confiança epistêmica**: Tier 1 para dados de comércio exterior
- **Dados típicos**: balança comercial por setor, lista de maiores exportadores

---

## Benchmarks de Mercado

### Equivalentes Americanos (quando dados brasileiros são escassos)
- **SaaS B2B**: SaaStr, OpenView Partners, Bessemer Venture Partners benchmarks
- **Retail e e-commerce**: NRF, eMarketer, Digital Commerce 360
- **Serviços profissionais**: AMCF, Consulting Global, McKinsey Insights
- **Como adaptar para o Brasil**: aplicar desconto de 20–40% em métricas de crescimento; ajustar LTV pelo ticket médio em BRL; ajustar churn por elasticidade de mercado mais volátil
- **Rótulo obrigatório**: sempre [HIPÓTESE] quando benchmark americano adaptado para Brasil

---

## Fontes por Segmento

| Segmento | Associação Principal | Publicação-Chave | Tier |
|---|---|---|---|
| Tech / SaaS | ABStartups, Abstartups | Pesquisa Startup Brasil | 2 |
| Varejo | SBVC, ABCOMM | Relatório do Varejo Brasileiro | 2 |
| Alimentação / Bares | ABRASEL | Pesquisa Setorial Foodservice | 2 |
| Serviços / Consultoria | FENACON, ABCF | Dados de mercado consultorias | 2 |
| Manufatura | CNI, FIESP | Sondagem Industrial | 1-2 |
| Saúde | CFM, ANS, ABRAMGE | Dados regulatórios ANS | 1 |
| Construção Civil | CBIC, Sinduscon | Índice de Atividade da Construção | 2 |
| Educação | INEP, ABMES | Censo da Educação Superior | 1 |

---

## Dados de ICP (Ideal Customer Profile)

Fontes para perfis demográficos e comportamentais por setor:

- **Demográficos**: IBGE PNAD (renda, escolaridade, região)
- **Comportamentais**: Kantar IBOPE, Nielsen, Brain.lat (consumo e hábitos)
- **B2B ICP**: Dun & Bradstreet Brasil, Quod, Serasa Experian (perfil empresarial)
- **Uso em Fase 4**: alimentar simulações de comportamento do consumidor (churn, LTV, elasticidade)

---

## Expansão via G-I3 (Injeção de Metodologia)

O consultor pode adicionar fontes proprietárias ao início da Fase 3:

**Formato de injeção** (texto livre estruturado):
```
FONTES_ADICIONAIS:
- [Nome da fonte]: [tipo] [URL ou descrição] [tier de confiança]

BENCHMARKS_PROPRIETÁRIOS:
- [métrica]: [valor] [fonte] [data]

PESOS_ANALÍTICOS:
- priorizar: [dimensão, ex: "custo sobre receita"]
- contexto: [observação livre sobre o mercado deste cliente]
```

O sistema incorpora as fontes injetadas com precedência sobre as fontes padrão.
Mantém trilha de qual dado veio de qual fonte para o Apêndice B.

---

## Tiers de Qualidade de Fonte e Mapeamento Epistêmico

| Tier | Descrição | Rótulo padrão |
|---|---|---|
| Tier 1 | Dados governamentais primários, auditorias, demonstrações financeiras verificadas | [FATO] |
| Tier 2 | Relatórios de associações setoriais, pesquisas acadêmicas verificadas | [INFERÊNCIA] |
| Tier 3 | Empresas de pesquisa de mercado, relatórios de analistas (citar data e firma) | [HIPÓTESE] |
| Tier 4 | Notícias, blogs, sinais de redes sociais (apenas direção de tendência) | [HIPÓTESE] |

**Regra**: ao usar Tier 3 ou 4, sempre adicionar: "[HIPÓTESE — fonte: nome, data]"
**Regra**: nunca apresentar Tier 3/4 como fato estabelecido no documento do cliente.

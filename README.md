# 📚 Biblioteca de Assets Reutilizáveis (Manus Edition)

Esta biblioteca foi construída a partir de um processo de inventário, desduplicação e extração de templates-base únicos. O objetivo é fornecer uma base sólida, limpa e documentada para a geração de entregáveis futuros com baixo retrabalho.

---

## 🏗️ Estrutura da Biblioteca

A biblioteca está dividida em duas classes principais, separando o que é **visual (apresentação)** do que é **operacional (inteligência)**.

### 1. Visual Assets (HTML)
Localizados em `templates/html/`, estes arquivos são otimizados para exportação em PDF e visualização premium.
- `relatorio_estrategico_base.html`: Design executivo para diagnósticos e consultoria.
- `caderno_planejamento_anual_base.html`: Layout de planner/caderno para organização e rotina.
- `playbook_lancamento_base.html`: Estrutura de campanha e cronograma de execução.

### 2. Operational Playbooks (Text)
Localizado em `templates/text/`, este arquivo é ideal para processamento por IA e gestão de projetos.
- `playbook_executavel_base.txt`: Mapa de execução semanal, backlog e teses centrais.

---

## 📊 Comparativo de Templates

| Template | Finalidade | Quando Usar | Principais Placeholders | Limitações |
| :--- | :--- | :--- | :--- | :--- |
| **Relatório Estratégico** | Entrega de diagnóstico, análise e recomendações executivas. | Reuniões de fechamento, relatórios de performance, auditorias. | `{{MAIN_HEADLINE}}`, `{{STAT_VALUE}}`, `{{PRINCIPLE_1_TITLE}}` | Layout rígido de 3 páginas; requer conteúdo denso. |
| **Caderno de Planejamento** | Organização pessoal, acadêmica ou de rotina operacional. | Onboarding de clientes, planejamento anual, guias de estudo. | `{{PLANNING_YEAR}}`, `{{CLIENT_NAME}}`, `{{PILLARS_CHECKLIST}}` | Focado em escrita manual/digital; menos "narrativo" que o relatório. |
| **Playbook de Lançamento** | Documentação de campanhas, cronogramas e ativos de marketing. | Lançamentos de produtos, planos de conteúdo, manuais de marca. | `{{PROJECT_NAME}}`, `{{LAUNCH_DATE}}`, `{{TABLE_ROWS_1}}` | Estrutura modular; exige preenchimento detalhado de tabelas. |
| **Playbook Executável** | Gestão de prioridades, backlog e diretrizes operacionais. | Planejamento semanal, definição de OKRs, consolidado de projetos. | `{{PRIMARY_BET}}`, `{{DAY_1_BLOCKS}}`, `{{PROMPT_1}}` | Sem apelo visual; focado 100% em texto e lógica de execução. |

---

## 🛠️ Regras de Reutilização

Para garantir a qualidade dos entregáveis, siga este fluxo antes de gerar qualquer arquivo:

1.  **Deduplicação de Contexto**: Remova qualquer texto remanescente dos templates originais que não se aplique ao novo caso.
2.  **Preenchimento de Placeholders**: Substitua todos os elementos no padrão `{{PLACEHOLDER_NAME}}` por informações reais.
3.  **Validação de Layout**: Certifique-se de que o volume de texto é compatível com os containers visuais (especialmente em HTML).
4.  **Acessibilidade**: Os templates HTML já possuem cores otimizadas para redução de estresse visual e suporte a dislexia. Mantenha essas proporções de contraste.

---

## 📝 Manifesto de Inventário

O processamento do arquivo original resultou na seguinte consolidação:

- **Total de arquivos analisados**: 12
- **Total de templates únicos extraídos**: 4
- **Grupos de Duplicatas**:
  - *Relatório Estratégico*: 4 ocorrências (Consolidadas em `relatorio_estrategico_base.html`)
  - *Caderno de Planejamento*: 6 ocorrências (Consolidadas em `caderno_planejamento_anual_base.html`)
  - *Playbook de Lançamento*: 1 ocorrência (Consolidada em `playbook_lancamento_base.html`)
  - *Playbook Executável*: 1 ocorrência (Consolidada em `playbook_executavel_base.txt`)

---
**Versão da Biblioteca:** 1.0.0
**Data de Atualização:** 14 de Abril de 2026

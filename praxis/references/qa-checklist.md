# QA Checklist — Gate G4

## Propósito
Gate G4 executa programaticamente via `scripts/validate_qa.py` antes de qualquer entregável ao cliente.
Todos os 20 checks devem passar. Falhas são listadas, entrega bloqueada, revisão solicitada.

---

## Categoria 1: Completude de Artefatos (Checks 1–5)

**Check 1** — Artefato A-01 presente
```
Verificar: manifest.artifacts_produced contém {artifact_id: "A-01"}
Arquivo existe no path registrado
Falha: "A-01 (Normalized Follow Up) não encontrado. Execute a Fase 1 completa."
```

**Check 2** — Artefato obrigatório do cenário presente
```
Cenário A: verificar A-06 + pelo menos um de [A-07, A-08, A-09] + A-MASTER + A-FINAL + A-OPS
Cenário B: verificar A-06 (atualizado) + A-MASTER + A-FINAL + A-OPS
Cenário C: verificar A-02 + A-FINAL
Falha: listar artefatos faltantes por ID.
```

**Check 3** — A-FINAL não está vazio
```
Verificar: arquivo A-FINAL tem mais de 500 palavras
Falha: "A-FINAL está vazio ou insuficiente (< 500 palavras)."
```

**Check 4** — A-OPS tem todas as abas obrigatórias
```
Verificar: arquivo A-OPS.xlsx contém abas [Resumo Executivo, Diagnóstico, Plano de Ação, Simulação, Próximos Passos]
Falha: listar abas faltantes.
```

**Check 5** — compilation_log.md existe ao lado de A-MASTER
```
Verificar: se A-MASTER presente, compilation_log.md existe no mesmo diretório
Falha: "compilation_log.md ausente. Execute a Fase 5 com subroutine de compilação."
```

---

## Categoria 2: Integridade Epistêmica (Checks 6–9)

**Check 6** — Nenhuma afirmação sem rótulo em A-MASTER
```
Verificar: A-MASTER não contém parágrafos analíticos sem [FATO], [INFERÊNCIA] ou [HIPÓTESE]
Método: buscar padrões de afirmação declarativa sem rótulo (regex básico)
Falha: "Afirmações sem rótulo epistêmico encontradas em A-MASTER. Revise Seção [N]."
```

**Check 7** — [HIPÓTESE] nunca apresentada como [FATO] em A-FINAL
```
Verificar: claims marcados como [HIPÓTESE] em A-MASTER não aparecem sem marcação em A-FINAL
Falha: "Hipótese apresentada como fato em A-FINAL. Verifique trilha epistêmica."
```

**Check 8** — Apêndice B (Trilha Epistêmica) presente em A-MASTER
```
Verificar: A-MASTER contém seção "Apêndice B" com lista de claims rotulados
Falha: "Apêndice B ausente em A-MASTER. Adicione trilha epistêmica."
```

**Check 9** — Nenhuma [TRILHA_INTERNA] exposta em A-FINAL
```
Verificar: A-FINAL não contém marcações [TRILHA_INTERNA] ou conteúdo interno
Falha: "Conteúdo de trilha interna detectado em A-FINAL. Remover antes da entrega."
```

---

## Categoria 3: Conformidade de Branding (Checks 10–12)

**Check 10** — Identidade do consultor aplicada a todos os artefatos CLIENTE
```
Verificar: A-FINAL e A-OPS contêm consultant_display_name e consultant_company
Falha: "Identidade do consultor não aplicada. Verifique configuração de branding."
```

**Check 11** — Nenhuma menção a Claude, Anthropic ou IA nos documentos do cliente
```
Verificar: A-FINAL e A-OPS não contêm: "Claude", "Anthropic", "IA", "inteligência artificial",
           "machine learning", "modelo de linguagem", "sistema de IA"
Falha: "Menção a IA/Claude encontrada em [arquivo, linha]. Remover."
```

**Check 12** — Nenhum ID interno exposto nos documentos do cliente
```
Verificar: A-FINAL e A-OPS não contêm: "A-01", "A-02", "A-MASTER", "G-I1", "G0", "G2",
           "Fase 1", "Phase 1", "TRILHA_INTERNA"
Falha: "ID interno exposto em [arquivo]. Substituir por linguagem executiva."
```

---

## Categoria 4: Qualidade de Conteúdo (Checks 13–16)

**Check 13** — A-FINAL contém seções mínimas obrigatórias
```
Verificar: A-FINAL tem as seções: Contextualização, Diagnóstico, [Prioridades ou Plano de Ação], Próximos Passos
Falha: "Seção obrigatória ausente em A-FINAL: [nome da seção]."
```

**Check 14** — Pelo menos 1 causa raiz identificada no diagnóstico
```
Verificar: A-MASTER ou A-FINAL contém pelo menos 1 "causa raiz" ou "causa principal" identificada
Falha: "Nenhuma causa raiz identificada. Diagnóstico incompleto."
```

**Check 15** — Pelo menos 1 ação com responsável e prazo no plano
```
Verificar: Plano de Ação contém pelo menos 1 item com campos: [ação, responsável, prazo]
Falha: "Plano de ação sem item com responsável e prazo."
```

**Check 16** — Texto do cliente em português brasileiro adequado (verificação básica)
```
Verificar: A-FINAL não contém PT-Portugal marcante (ex: "utilizámos", "façamos")
Verificar: A-FINAL não contém coloquialismos (verificação por lista negativa)
Falha: "Possível desvio de registro em A-FINAL. Revisar linguagem."
```

---

## Categoria 5: Integridade da Trilha de Gates (Checks 17–20)

**Check 17** — G0 e G1 foram aprovados antes de G2
```
Verificar: manifest.gates_passed contém G0 e G1 com timestamps anteriores ao de G2
Falha: "Gates G0/G1 não registrados antes de G2. Trilha de aprovação inválida."
```

**Check 18** — G2 foi aprovado por humano (não AUTO)
```
Verificar: manifest.gates_passed[gate=G2].approved_by != "AUTO"
Falha: "G2 aprovado automaticamente. Gate G2 exige revisão humana explícita."
```

**Check 19** — manifest.updated_at é recente (< 24h)
```
Verificar: manifest.updated_at não tem mais de 24h a partir de agora
Falha: "Manifest não atualizado nas últimas 24h. Verificar estado do caso."
```

**Check 20** — manifest.current_phase é 6 (caso em fase de entrega)
```
Verificar: manifest.current_phase == 6
Falha: "Caso não está na Fase 6. QA G4 só se aplica na fase de entrega."
```

---

## Formato de Saída do validate_qa.py

```
PRAXIS QA — Gate G4
═══════════════════════════════════════
Total de checks: 20
Passou:  N
Falhou:  N

Problemas encontrados:
  [Check N] descrição da falha
  [Check M] descrição da falha

Resultado: PASS (code 0) | FAIL (code 1)
═══════════════════════════════════════
```

Se `PASS`: apresentar pacote de entregáveis ao consultor para revisão (Gate G5).
Se `FAIL`: listar todos os problemas, solicitar revisão, re-executar validate_qa.py.

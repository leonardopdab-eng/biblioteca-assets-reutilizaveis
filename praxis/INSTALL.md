# INSTALL — Praxis

## Pré-requisitos

- Python 3.10 ou superior
- Acesso ao Claude (Claude.ai, Claude Code, ou API)

```bash
pip install pyyaml openpyxl
```

---

## Opção 1: Claude Code (CLI)

```bash
# Descompactar na pasta de skills do Claude Code
unzip praxis.zip -d ~/.claude/skills/

# Verificar estrutura
ls ~/.claude/skills/praxis/

# Testar pipeline
python ~/.claude/skills/praxis/scripts/dry_run.py
```

**Como usar**:
1. Abrir sessão Claude Code no diretório de um caso
2. Digitar: "novo caso — cliente: [Nome da Empresa]"
3. Colar o briefing quando solicitado

**Inicializar caso via script**:
```bash
mkdir meu-caso && cd meu-caso
python ~/.claude/skills/praxis/scripts/init_case.py \
  --consultant meu-id \
  --client "Nome do Cliente"
```

---

## Opção 2: Claude.ai (Web)

1. Abrir [claude.ai](https://claude.ai)
2. Criar ou abrir um **Claude Project** dedicado para consultoria
3. Ir em **Settings > Skills**
4. Clicar em **Upload**
5. Selecionar a pasta `praxis/` ou o arquivo `praxis.zip`
6. Confirmar upload

**Como usar**:
1. Na conversa do projeto, digitar: "novo caso — cliente: [Nome]"
2. Seguir as instruções do sistema

**Nota**: scripts Python não rodam diretamente no Claude.ai — são para uso no Claude Code ou API.

---

## Opção 3: API Anthropic (Custom Integration)

Para integrar praxis em sua própria aplicação:

```python
import anthropic

# Ler SKILL.md como system prompt base
with open("praxis/SKILL.md", "r", encoding="utf-8") as f:
    skill_md = f.read()

# Carregar referências necessárias para a fase ativa
with open("praxis/references/consultor-voice.md", "r", encoding="utf-8") as f:
    consultor_voice = f.read()

# Construir system prompt
system_prompt = f"""
{skill_md}

---
{consultor_voice}
"""

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",  # Usar o modelo mais capaz para melhor raciocínio
    max_tokens=8096,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Novo caso — cliente: TechFlow Soluções\n\n[briefing aqui]"}
    ]
)
```

**Carregamento progressivo de referências**:
```python
# Carregar apenas os arquivos necessários para a fase atual
def get_phase_references(phase: int) -> str:
    ref_map = {
        1: ["phase-01-intake.md"],
        2: ["phase-02-personalization.md"],
        3: ["phase-03-analytical.md", "framework-library.md", "epistemic-labels.md"],
        4: ["phase-04-simulation.md"],
        5: ["phase-05-architect.md"],
        6: ["phase-06-delivery.md", "cliente-voice.md", "qa-checklist.md"],
    }
    refs = []
    for filename in ref_map.get(phase, []):
        with open(f"praxis/references/{filename}", "r", encoding="utf-8") as f:
            refs.append(f.read())
    return "\n\n---\n\n".join(refs)
```

---

## Configuração Inicial (Primeira vez)

### 1. Definir identidade do consultor

Editar `praxis/manifest_template.yaml` ou deixar para a Fase 2 configurar interativamente:

```yaml
client_identity:
  branding:
    consultant_display_name: "Seu Nome"
    consultant_company: "Sua Empresa"
    primary_color: "#1B2A4A"       # Sua cor principal (hex)
    accent_color: "#2E7D9B"        # Cor de destaque
    logo_path: "caminho/logo.png"  # Opcional
```

### 2. Testar pipeline

```bash
cd praxis/
python scripts/dry_run.py --verbose
```

Saída esperada:
```
RESULTADO: PASS — pipeline completo executou sem erros.
```

### 3. Primeiro caso real

```bash
mkdir casos/primeiro-caso && cd casos/primeiro-caso
python ../../scripts/init_case.py --consultant seu-id --client "Nome do Cliente"
```

---

## Solução de Problemas

**Erro: `yaml` não encontrado**
```bash
pip install pyyaml
```

**Erro: `openpyxl` não encontrado**
```bash
pip install openpyxl
```

**dry_run.py falha em gerar A-OPS.xlsx**
Verificar instalação do openpyxl. O dry_run continua mesmo se A-OPS falhar.

**Gate G2/G5/G6 bloqueado**
Esperado. Esses gates exigem `--approved-by <seu_id>` (não "AUTO"). Digitando "sim"
na confirmação interativa do advance_phase.py o gate avança.

**manifest.yaml não encontrado**
Rodar `init_case.py` primeiro no diretório do caso.

---

## Compatibilidade

| Plataforma | Suporte | Notas |
|---|---|---|
| Claude Code (CLI) | Completo | Scripts Python funcionam nativamente |
| Claude.ai (Project) | Parcial | Sem execução de scripts; conversacional |
| API Anthropic | Completo | Requerer carregamento manual de referências |
| Claude Desktop | Parcial | Similar ao Claude.ai |

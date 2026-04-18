#!/usr/bin/env python3
"""
Roteia para o módulo analítico correto baseado no tipo de problema descrito.

Input:  --problem-description <str>  Descrição do problema em linguagem natural
        --config <path>              consultant_config.yaml
        --decision-log <path>        (opcional) Arquivo para registrar decisão
        --output <path>              (opcional) Salvar JSON de saída
Output: JSON com primary_module, secondary_module, reasoning, confidence

Uso:
  python module_router.py --problem-description "vendas caindo, causa desconhecida" \\
    --config ../../examples/consultant_config_guided.yaml
  # {"primary_module": "5_whys", "secondary_module": "ishikawa", ...}
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml


# Keyword-to-module mapping with weights
MODULE_KEYWORDS = {
    "5_whys": [
        "causa raiz", "causa desconhecida", "não sabemos por que", "sem motivo claro",
        "origem do problema", "raiz do problema", "investigar causa", "causa oculta",
        "problema sem causa", "por que está acontecendo", "caindo sem causa",
    ],
    "pareto": [
        "múltiplos problemas", "vários problemas", "muitos problemas", "lista de problemas",
        "não sabemos por onde começar", "priorizar", "foco", "qual resolver primeiro",
        "80/20", "problema mais frequente",
    ],
    "swot": [
        "análise estratégica", "posição estratégica", "mercado", "concorrência",
        "oportunidades", "ameaças", "forças", "fraquezas", "posicionamento",
        "estratégia competitiva", "análise de mercado",
    ],
    "5w2h": [
        "plano pouco detalhado", "ações vagas", "sem clareza de execução",
        "como executar", "o que fazer", "quem faz", "como implementar",
        "especificidade do plano", "plano de ação detalhado",
    ],
    "pdca": [
        "melhoria de processo", "processo existente", "ciclo de melhoria",
        "processo recorrente", "padronização", "controle de processo",
        "planejar executar checar agir", "processo operacional",
    ],
    "ishikawa": [
        "múltiplas causas", "problema sistêmico", "causas encadeadas",
        "espinha de peixe", "6m", "diagrama de causa", "causa e efeito",
        "problema complexo", "diversas origens",
    ],
    "jtbd": [
        "produto sem job", "serviço sem propósito claro", "cliente não engaja",
        "proposta de valor fraca", "jobs to be done", "para que serve",
        "por que compram", "motivação do cliente", "necessidade não articulada",
    ],
    "esforco_impacto": [
        "priorização rápida", "quick wins", "alto impacto baixo esforço",
        "matriz de esforço", "iniciativas", "o que fazer primeiro",
        "retorno rápido", "esforço versus resultado",
    ],
}

# Secondary module pairings
SECONDARY_MAP = {
    "5_whys": "ishikawa",
    "pareto": "esforco_impacto",
    "swot": None,
    "5w2h": None,
    "pdca": None,
    "ishikawa": "5_whys",
    "jtbd": None,
    "esforco_impacto": "pareto",
}


def score_modules(description: str) -> dict[str, float]:
    text = description.lower()
    scores: dict[str, float] = {m: 0.0 for m in MODULE_KEYWORDS}

    for module, keywords in MODULE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[module] += 1.0 / len(keywords)

    return scores


def route(description: str, diagnosis_weight: float = 0.25) -> dict:
    scores = score_modules(description)
    sorted_modules = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    primary_module, primary_score = sorted_modules[0]
    confidence = min(primary_score * 5, 1.0)  # normalize to 0–1

    # If no clear winner, default to 5_whys (most general diagnostic tool)
    if primary_score == 0:
        primary_module = "5_whys"
        confidence = 0.3
        reasoning = "No strong keyword match. Defaulting to 5_whys as general diagnostic entry point."
    else:
        second_module, second_score = sorted_modules[1]
        reasoning = (
            f"Keyword analysis matched '{primary_module}' (score={primary_score:.2f}). "
            f"Problem description contains signals: {[k for k in MODULE_KEYWORDS[primary_module] if k in description.lower()][:3]}."
        )

    secondary_module = SECONDARY_MAP.get(primary_module)

    # With high diagnosis weight, always include secondary module
    if diagnosis_weight > 0.30 and secondary_module is None:
        second_best = sorted_modules[1][0] if sorted_modules[1][1] > 0 else None
        secondary_module = second_best

    return {
        "primary_module": primary_module,
        "secondary_module": secondary_module,
        "reasoning": reasoning,
        "confidence": round(confidence, 2),
        "all_scores": {m: round(s, 3) for m, s in sorted_modules},
    }


def main():
    parser = argparse.ArgumentParser(description="Route to the correct analytical module for Bússola PME diagnosis.")
    parser.add_argument("--problem-description", required=True, help="Natural language description of the problem")
    parser.add_argument("--config", required=True, help="Path to consultant_config.yaml")
    parser.add_argument("--decision-log", help="Path to decision_log.md to append routing decision")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    diagnosis_weight = config.get("method_weights", {}).get("diagnosis", 0.25)
    result = route(args.problem_description, diagnosis_weight)

    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    if args.decision_log:
        log_path = Path(args.decision_log)
        entry = (
            f"\n## Routing Decision — {datetime.utcnow().isoformat()}\n"
            f"- **Problem**: {args.problem_description[:100]}\n"
            f"- **Primary module**: {result['primary_module']}\n"
            f"- **Secondary module**: {result['secondary_module']}\n"
            f"- **Confidence**: {result['confidence']}\n"
            f"- **Reasoning**: {result['reasoning']}\n"
        )
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    sys.exit(0)


if __name__ == "__main__":
    # Example: python module_router.py --problem-description "vendas caindo há 3 meses, não sabemos por que" --config examples/consultant_config_guided.yaml
    main()

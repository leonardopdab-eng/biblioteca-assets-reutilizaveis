#!/usr/bin/env python3
"""
Calcula priority scores para itens do problem_tree usando fórmula Bússola PME.

Input:  --items <json>   Lista de itens: [{item, impacto, urgencia, esforco, alinhamento}, ...]
        --config <path>  consultant_config.yaml (lê method_weights.prioritization)
        --output <path>  (opcional) Salvar JSON de saída
Output: JSON com lista ordenada por score desc: [{item, score, rank, justification}, ...]

Fórmula base:
  score = (impacto * 0.4) + (urgencia * 0.3) + (esforco_inverso * 0.2) + (alinhamento * 0.1)
  Pesos internos modulados pelo config weight (0.0–1.0).

Uso:
  python priority_scorer.py \\
    --items '[{"item":"Queda pipeline","impacto":5,"urgencia":5,"esforco":3,"alinhamento":4}]' \\
    --config ../../examples/consultant_config_guided.yaml
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


BASE_WEIGHTS = {
    "impacto": 0.4,
    "urgencia": 0.3,
    "esforco_inverso": 0.2,
    "alinhamento": 0.1,
}


def get_scale(prioritization_weight: float) -> int:
    if prioritization_weight < 0.20:
        return 3
    elif prioritization_weight <= 0.30:
        return 5
    else:
        return 10


def modulate_weights(base: dict, prio_weight: float) -> dict:
    # Higher prio_weight → more emphasis on impacto (spread the weights)
    # Lower prio_weight → flatten towards uniform distribution
    factor = prio_weight  # 0.0–1.0
    modulated = {}
    for key, base_val in base.items():
        uniform = 0.25
        modulated[key] = uniform + (base_val - uniform) * factor
    # Normalize
    total = sum(modulated.values())
    return {k: v / total for k, v in modulated.items()}


def score_item(item: dict, weights: dict, scale: int) -> float:
    impacto = item.get("impacto", 1)
    urgencia = item.get("urgencia", 1)
    esforco = item.get("esforco", 1)
    alinhamento = item.get("alinhamento", 1)

    # Normalize to 0–1 range
    norm = lambda v: (v - 1) / (scale - 1) if scale > 1 else 0.5

    esforco_inverso = 1.0 - norm(esforco)  # Lower effort = better score
    score = (
        weights["impacto"] * norm(impacto)
        + weights["urgencia"] * norm(urgencia)
        + weights["esforco_inverso"] * esforco_inverso
        + weights["alinhamento"] * norm(alinhamento)
    )
    return round(score, 4)


def build_justification(item: dict, score: float, rank: int, scale: int) -> str:
    parts = []
    impacto = item.get("impacto", 1)
    urgencia = item.get("urgencia", 1)
    esforco = item.get("esforco", 1)

    if impacto >= scale * 0.8:
        parts.append("alto impacto")
    if urgencia >= scale * 0.8:
        parts.append("alta urgência")
    if esforco <= scale * 0.3:
        parts.append("baixo esforço (quick win)")

    if not parts:
        parts.append("pontuação equilibrada entre dimensões")

    return f"Rank #{rank}: {'; '.join(parts)}. Score final = {score:.3f}"


def main():
    parser = argparse.ArgumentParser(description="Score and rank problem items for Bússola PME prioritization.")
    parser.add_argument("--items", required=True, help="JSON array of items to score")
    parser.add_argument("--config", required=True, help="Path to consultant_config.yaml")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    try:
        items = json.loads(args.items)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON for --items: {e}", file=sys.stderr)
        sys.exit(1)

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    prio_weight = config.get("method_weights", {}).get("prioritization", 0.25)
    scale = get_scale(prio_weight)
    weights = modulate_weights(BASE_WEIGHTS, prio_weight)

    scored = []
    for item in items:
        s = score_item(item, weights, scale)
        scored.append({**item, "_score": s})

    scored.sort(key=lambda x: x["_score"], reverse=True)

    result = []
    for rank, item in enumerate(scored, start=1):
        score = item.pop("_score")
        result.append({
            "item": item.get("item", f"item_{rank}"),
            "score": score,
            "rank": rank,
            "dimensions": {
                "impacto": item.get("impacto"),
                "urgencia": item.get("urgencia"),
                "esforco": item.get("esforco"),
                "alinhamento": item.get("alinhamento"),
            },
            "justification": build_justification(item, score, rank, scale),
        })

    output_data = {
        "scale": scale,
        "prioritization_weight_used": prio_weight,
        "weights_applied": {k: round(v, 3) for k, v in weights.items()},
        "items": result,
    }

    output_str = json.dumps(output_data, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python priority_scorer.py --items '[{"item":"A","impacto":5,"urgencia":4,"esforco":2,"alinhamento":5}]' --config examples/consultant_config_guided.yaml
    main()

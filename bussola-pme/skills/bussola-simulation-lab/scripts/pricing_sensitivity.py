#!/usr/bin/env python3
"""
Simula sensibilidade de pricing para análise de cenários Bússola PME.

Input:  --base-price <float>         Preço base atual (R$)
        --elasticity <float>         Elasticidade-preço da demanda (negativa, ex: -1.2)
        --fixed-costs <float>        Custos fixos mensais (R$)
        --variable-cost-pct <float>  % de custo variável sobre receita (0.0–1.0)
        --output <path>              (opcional) Salvar JSON
Output: JSON com 5 pontos de preço (±20% do base) + curvas de receita/margem

Uso:
  python pricing_sensitivity.py --base-price 8000 --elasticity -1.2 \\
    --fixed-costs 20000 --variable-cost-pct 0.3
"""

import argparse
import json
import math
import sys
from pathlib import Path


def simulate_pricing(base_price: float, elasticity: float,
                     fixed_costs: float, variable_cost_pct: float,
                     base_quantity: float = 10.0) -> dict:
    """
    Simula 5 pontos de preço: -20%, -10%, base, +10%, +20%.
    Elasticidade: % mudança na quantidade / % mudança no preço.
    """
    price_points = [
        base_price * 0.80,
        base_price * 0.90,
        base_price,
        base_price * 1.10,
        base_price * 1.20,
    ]

    scenarios = []
    for price in price_points:
        pct_change_price = (price - base_price) / base_price
        pct_change_qty = elasticity * pct_change_price
        quantity = max(base_quantity * (1 + pct_change_qty), 0)

        revenue = price * quantity
        variable_costs = revenue * variable_cost_pct
        gross_profit = revenue - variable_costs
        net_profit = gross_profit - fixed_costs
        margin_pct = (net_profit / revenue * 100) if revenue > 0 else 0

        scenarios.append({
            "price": round(price, 2),
            "price_change_pct": round(pct_change_price * 100, 1),
            "quantity": round(quantity, 1),
            "revenue": round(revenue, 2),
            "variable_costs": round(variable_costs, 2),
            "gross_profit": round(gross_profit, 2),
            "net_profit": round(net_profit, 2),
            "margin_pct": round(margin_pct, 1),
            "scenario": "pessimista" if price < base_price * 0.95 else
                       "otimista" if price > base_price * 1.05 else "realista",
            "note": "[HIPÓTESE — elasticidade estimada; validar com dados reais de vendas]"
                    if price != base_price else "[FATO — preço atual]",
        })

    # Find optimal price (max net_profit)
    optimal = max(scenarios, key=lambda x: x["net_profit"])

    return {
        "base_price": base_price,
        "elasticity": elasticity,
        "fixed_costs": fixed_costs,
        "variable_cost_pct": variable_cost_pct,
        "base_quantity_assumed": base_quantity,
        "scenarios": scenarios,
        "optimal_price": optimal["price"],
        "optimal_net_profit": optimal["net_profit"],
        "recommendation": (
            f"Preço ótimo simulado: R${optimal['price']:.0f} "
            f"(lucro líquido estimado: R${optimal['net_profit']:.0f}/mês) [HIPÓTESE]"
        ),
        "warning": (
            "Todos os cenários assumem elasticidade constante [HIPÓTESE]. "
            "Validar com dados históricos de vendas antes de decisão."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Price sensitivity analysis for Bússola PME simulation.")
    parser.add_argument("--base-price", type=float, required=True, help="Current base price (R$)")
    parser.add_argument("--elasticity", type=float, required=True, help="Price elasticity of demand (negative)")
    parser.add_argument("--fixed-costs", type=float, required=True, help="Monthly fixed costs (R$)")
    parser.add_argument("--variable-cost-pct", type=float, required=True,
                        help="Variable cost as % of revenue (0.0–1.0)")
    parser.add_argument("--base-quantity", type=float, default=10.0,
                        help="Current monthly units sold (default: 10)")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    result = simulate_pricing(
        args.base_price, args.elasticity,
        args.fixed_costs, args.variable_cost_pct,
        args.base_quantity
    )

    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python pricing_sensitivity.py --base-price 8000 --elasticity -1.2 --fixed-costs 20000 --variable-cost-pct 0.3
    main()

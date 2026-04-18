#!/usr/bin/env python3
"""
Simula cenários de capacidade e break-even de expansão para Bússola PME.

Input:  --current-capacity <float>    Capacidade atual (unidades/mês ou R$/mês)
        --demand-growth-pct <float>   % de crescimento da demanda/mês
        --expansion-cost <float>      Custo de expansão (R$, one-time)
        --months <int>                Horizonte de análise (meses)
        --output <path>               (opcional) Salvar JSON
Output: JSON com ponto de ruptura de capacidade + break-even da expansão

Uso:
  python capacity_scenarios.py --current-capacity 100000 --demand-growth-pct 5 \\
    --expansion-cost 50000 --months 12
"""

import argparse
import json
import sys
from pathlib import Path


def simulate_capacity(current_capacity: float, demand_growth_pct: float,
                      expansion_cost: float, months: int) -> dict:
    monthly_growth = demand_growth_pct / 100
    timeline = []
    demand = current_capacity  # Start at current capacity = current demand [HIPÓTESE]

    rupture_month = None
    for m in range(1, months + 1):
        demand *= (1 + monthly_growth)
        capacity_utilization = min(demand / current_capacity * 100, 100)
        at_capacity = demand >= current_capacity

        if at_capacity and rupture_month is None:
            rupture_month = m

        timeline.append({
            "month": m,
            "demand": round(demand, 0),
            "capacity": current_capacity,
            "utilization_pct": round(capacity_utilization, 1),
            "at_capacity": at_capacity,
            "overflow": round(max(demand - current_capacity, 0), 0),
        })

    # Break-even calculation for expansion
    # Expansion adds capacity; the incremental revenue from overflow covers the expansion cost
    if rupture_month:
        overflow_per_month_at_rupture = timeline[rupture_month - 1]["overflow"]
        if overflow_per_month_at_rupture > 0:
            payback_months = expansion_cost / overflow_per_month_at_rupture
        else:
            payback_months = None
    else:
        payback_months = None

    return {
        "inputs": {
            "current_capacity": current_capacity,
            "demand_growth_pct_monthly": demand_growth_pct,
            "expansion_cost": expansion_cost,
            "months": months,
        },
        "timeline": timeline,
        "rupture_month": rupture_month,
        "rupture_note": (
            f"Capacidade atingida no mês {rupture_month} [HIPÓTESE — crescimento constante assumido]"
            if rupture_month else
            "Capacidade não atingida no horizonte analisado [INFERÊNCIA]"
        ),
        "expansion_analysis": {
            "cost": expansion_cost,
            "payback_months": round(payback_months, 1) if payback_months else None,
            "recommendation": (
                f"Break-even da expansão estimado em {round(payback_months, 0):.0f} meses após o mês {rupture_month} [HIPÓTESE]"
                if payback_months else
                "Expansão não justificada no horizonte analisado com premissas atuais [INFERÊNCIA]"
            ),
        },
        "warning": "Todas as projeções assumem crescimento linear constante [HIPÓTESE — validar com dados históricos]",
    }


def main():
    parser = argparse.ArgumentParser(description="Capacity scenario simulation for Bússola PME.")
    parser.add_argument("--current-capacity", type=float, required=True,
                        help="Current capacity (units/month or R$/month)")
    parser.add_argument("--demand-growth-pct", type=float, required=True,
                        help="Monthly demand growth percentage")
    parser.add_argument("--expansion-cost", type=float, required=True,
                        help="One-time expansion cost (R$)")
    parser.add_argument("--months", type=int, default=12, help="Analysis horizon in months")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    result = simulate_capacity(
        args.current_capacity, args.demand_growth_pct,
        args.expansion_cost, args.months
    )
    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python capacity_scenarios.py --current-capacity 100000 --demand-growth-pct 5 --expansion-cost 50000 --months 12
    main()

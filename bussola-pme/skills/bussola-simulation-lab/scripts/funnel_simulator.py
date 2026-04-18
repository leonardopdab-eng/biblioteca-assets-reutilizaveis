#!/usr/bin/env python3
"""
Simula funil de conversão de vendas para análise de cenários Bússola PME.

Input:  --leads-monthly <int>   Leads mensais no topo do funil
        --stages <json>         Lista de etapas: [{"name":"...", "rate":0.3}, ...]
        --avg-ticket <float>    Ticket médio (R$)
        --output <path>         (opcional) Salvar JSON
Output: JSON com 3 cenários (pessimista/realista/otimista) + receita mensal projetada

Uso:
  python funnel_simulator.py --leads-monthly 100 \\
    --stages '[{"name":"reunião","rate":0.3},{"name":"proposta","rate":0.5}]' \\
    --avg-ticket 8000
"""

import argparse
import json
import sys
from pathlib import Path


def simulate_funnel(leads_monthly: int, stages: list, avg_ticket: float) -> dict:
    def run_scenario(leads: int, stage_rates: list, ticket: float) -> dict:
        current = leads
        stage_results = []
        for stage in stage_rates:
            converted = current * stage["rate"]
            stage_results.append({
                "stage": stage["name"],
                "rate": stage["rate"],
                "input": round(current, 1),
                "output": round(converted, 1),
            })
            current = converted

        revenue = current * ticket
        return {
            "stages": stage_results,
            "final_clients": round(current, 1),
            "revenue": round(revenue, 2),
        }

    # Pessimistic: leads -20%, rates -20%
    pessimistic_stages = [{"name": s["name"], "rate": s["rate"] * 0.8} for s in stages]
    pessimistic = run_scenario(int(leads_monthly * 0.8), pessimistic_stages, avg_ticket)

    # Realistic: base
    realistic = run_scenario(leads_monthly, stages, avg_ticket)

    # Optimistic: leads +20%, rates +20% (capped at 1.0)
    optimistic_stages = [{"name": s["name"], "rate": min(s["rate"] * 1.2, 0.95)} for s in stages]
    optimistic = run_scenario(int(leads_monthly * 1.2), optimistic_stages, avg_ticket)

    overall_conversion = realistic["final_clients"] / leads_monthly if leads_monthly > 0 else 0

    return {
        "inputs": {
            "leads_monthly": leads_monthly,
            "stages": stages,
            "avg_ticket": avg_ticket,
        },
        "scenarios": {
            "pessimista": {
                **pessimistic,
                "leads_input": int(leads_monthly * 0.8),
                "note": "Leads -20%, taxas de conversão -20% [HIPÓTESE]",
            },
            "realista": {
                **realistic,
                "leads_input": leads_monthly,
                "note": "Projeção baseada em taxas atuais [INFERÊNCIA — validar com dados CRM]",
            },
            "otimista": {
                **optimistic,
                "leads_input": int(leads_monthly * 1.2),
                "note": "Leads +20%, taxas +20% [HIPÓTESE — requer melhoria de processo]",
            },
        },
        "overall_conversion_pct": round(overall_conversion * 100, 1),
        "revenue_range": {
            "min": pessimistic["revenue"],
            "expected": realistic["revenue"],
            "max": optimistic["revenue"],
        },
        "recommendation": (
            f"Receita mensal esperada: R${realistic['revenue']:.0f} "
            f"(range: R${pessimistic['revenue']:.0f}–R${optimistic['revenue']:.0f}) [HIPÓTESE]"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Sales funnel simulation for Bússola PME.")
    parser.add_argument("--leads-monthly", type=int, required=True, help="Monthly leads at top of funnel")
    parser.add_argument("--stages", required=True,
                        help='JSON array of stages: [{"name":"...", "rate":0.3}, ...]')
    parser.add_argument("--avg-ticket", type=float, required=True, help="Average ticket value (R$)")
    parser.add_argument("--output", help="Path to save JSON output")
    args = parser.parse_args()

    try:
        stages = json.loads(args.stages)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid stages JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = simulate_funnel(args.leads_monthly, stages, args.avg_ticket)
    output_str = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_str)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    # Example: python funnel_simulator.py --leads-monthly 100 --stages '[{"name":"reunião","rate":0.3}]' --avg-ticket 8000
    main()

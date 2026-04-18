#!/usr/bin/env python3
"""
Detecta se uma pergunta Bússola PME deve ser escalada para o fundador.

Input:  --question <str>   Pergunta em linguagem natural
        --category <str>   Categoria já classificada (opcional)
Output: JSON com {escalate, reason, escalation_template}

Uso:
  python escalation_detector.py --question "O cliente pediu desconto, posso dar?"
  # {"escalate": true, "reason": "pricing/contract question", ...}
"""

import argparse
import json
import sys


ESCALATION_TRIGGERS = {
    "pricing": {
        "keywords": ["desconto", "preço", "valor", "honorários", "cobrar", "payment",
                     "reduzir preço", "negociar", "reembolso"],
        "reason": "pricing/contract question",
        "template": (
            "Esta pergunta envolve decisões de preço ou contrato que estão fora do escopo "
            "do sistema Bússola PME. Por favor, consulte o fundador ou sua política comercial."
        ),
    },
    "gate_override": {
        "keywords": ["override", "forçar", "ignorar gate", "pular gate", "desabilitar gate",
                     "remover gate", "contornar", "não precisa do gate"],
        "reason": "gate override request",
        "template": (
            "Gates hardcoded (G2, G5, G6) não podem ser removidos ou ignorados. "
            "Eles existem para proteger a qualidade do trabalho consultivo."
        ),
    },
    "client_specific": {
        "keywords": ["cliente X", "cliente Y", "problema do cliente", "caso específico",
                     "meu cliente", "situação do"],
        "reason": "client-specific case question (should go to orchestrator)",
        "template": (
            "Esta pergunta parece ser sobre um caso específico. "
            "Ative o bussola-orchestrator para trabalhar com casos."
        ),
    },
    "technical_issue": {
        "keywords": ["erro", "bug", "não funciona", "crashou", "falhou", "problema técnico",
                     "erro inesperado", "broken"],
        "reason": "technical issue not documented in reference library",
        "template": (
            "Problema técnico não coberto pelas referências disponíveis. "
            "Por favor, reporte para o suporte técnico com o log de erro."
        ),
    },
    "legal_compliance": {
        "keywords": ["lgpd", "privacidade", "confidencial", "sigilo", "contrato", "nda",
                     "juridico", "lei"],
        "reason": "legal/compliance question",
        "template": (
            "Questões legais ou de compliance devem ser tratadas com o consultor jurídico. "
            "O sistema Bússola PME não fornece orientação legal."
        ),
    },
}


def detect(question: str, category: str | None) -> dict:
    text = question.lower()

    # If category is "outro" and no strong match, escalate
    if category == "outro":
        return {
            "escalate": True,
            "reason": "question not covered by reference library",
            "escalation_template": (
                "Esta pergunta não corresponde às categorias cobertas pelas referências do Bússola PME. "
                "Por favor, consulte o fundador ou documentação externa."
            ),
        }

    for trigger_name, trigger_data in ESCALATION_TRIGGERS.items():
        matched = [kw for kw in trigger_data["keywords"] if kw.lower() in text]
        if matched:
            return {
                "escalate": True,
                "reason": trigger_data["reason"],
                "escalation_template": trigger_data["template"],
                "matched_triggers": matched,
            }

    return {
        "escalate": False,
        "reason": "question can be answered from reference library",
        "escalation_template": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Detect if a question needs escalation.")
    parser.add_argument("--question", required=True, help="Question to check")
    parser.add_argument("--category", help="Pre-classified category (optional)")
    args = parser.parse_args()

    result = detect(args.question, args.category)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    # Example: python escalation_detector.py --question "O cliente pediu desconto, posso dar?" --category "outro"
    main()

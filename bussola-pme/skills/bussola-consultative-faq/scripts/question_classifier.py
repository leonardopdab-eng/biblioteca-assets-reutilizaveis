#!/usr/bin/env python3
"""
Classifica perguntas sobre o método Bússola PME por categoria.

Input:  --question <str>   Pergunta em linguagem natural
Output: JSON com {category, confidence, reference_file}

Categorias: método | artefato | gate | módulo | modo | outro

Uso:
  python question_classifier.py --question "Qual a diferença entre 5W2H e PDCA?"
  # {"category": "método", "confidence": 0.85, "reference_file": "method_faq.md"}
"""

import argparse
import json
import sys


CATEGORY_KEYWORDS = {
    "método": {
        "keywords": [
            "diferença", "método", "fase", "6 fases", "processo", "como funciona",
            "label epistêmico", "fato inferência hipótese", "regra de conduta",
            "quando usar", "política epistêmica", "normalização", "diagnóstico",
            "priorização", "plano de ação",
        ],
        "reference_file": "method_faq.md",
    },
    "artefato": {
        "keywords": [
            "artefato", "o que vai", "o que é o", "conteúdo do", "resumo executivo",
            "diagnostico executivo", "plano de ação", "hypotheses_log", "problem_tree",
            "priority_score", "playbook", "proposta de continuidade", "relatorio",
            "zip", "pacote", "trilha cliente", "trilha interna",
        ],
        "reference_file": "artifact_faq.md",
    },
    "gate": {
        "keywords": [
            "gate", "bloqueou", "bloqueado", "g0", "g1", "g2", "g3", "g4", "g5", "g6",
            "por que bloqueou", "como aprovar", "bypass", "pular", "hardcoded",
            "gate manual", "aprovação", "por que não avança",
        ],
        "reference_file": "gate_troubleshooting.md",
    },
    "módulo": {
        "keywords": [
            "módulo", "5 porquês", "pareto", "swot", "5w2h", "pdca", "ishikawa",
            "jtbd", "esforço impacto", "espinha de peixe", "jobs to be done",
            "quando usar o", "qual módulo", "análise de causa raiz",
        ],
        "reference_file": "analytical_module_selector.md",
    },
    "modo": {
        "keywords": [
            "guided", "hands_off", "hands off", "modo", "operação", "automático",
            "manual", "configurar modo", "mudar modo", "diferença entre guided",
            "operating mode",
        ],
        "reference_file": "operating_modes_faq.md",
    },
}


def classify(question: str) -> dict:
    text = question.lower()
    scores = {}

    for category, data in CATEGORY_KEYWORDS.items():
        keywords = data["keywords"]
        matched = [kw for kw in keywords if kw.lower() in text]
        scores[category] = len(matched) / max(len(keywords), 1)

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    if best_score == 0:
        return {
            "category": "outro",
            "confidence": 0.0,
            "reference_file": None,
        }

    return {
        "category": best_category,
        "confidence": round(min(best_score * 10, 1.0), 2),
        "reference_file": CATEGORY_KEYWORDS[best_category]["reference_file"],
        "matched_keywords": [kw for kw in CATEGORY_KEYWORDS[best_category]["keywords"] if kw.lower() in text],
    }


def main():
    parser = argparse.ArgumentParser(description="Classify questions about Bússola PME method.")
    parser.add_argument("--question", required=True, help="Question to classify")
    args = parser.parse_args()

    result = classify(args.question)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    # Example: python question_classifier.py --question "Qual a diferença entre 5W2H e PDCA?"
    main()

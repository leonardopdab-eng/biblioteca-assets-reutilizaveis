#!/usr/bin/env python3
"""
Valida consultant_config.yaml contra shared/schemas/consultant_config_schema.yaml.

Input:  --config <path>  (consultant_config.yaml)
Output: VALID (stdout, exit 0) ou INVALID: <motivo> (stdout, exit 1)

Uso:
  python config_schema_validator.py --config examples/consultant_config_guided.yaml
  # VALID

  python config_schema_validator.py --config /tmp/bad.yaml
  # INVALID: method_weights sum is 1.35, expected 1.0 ±0.01
"""

import argparse
import sys
from pathlib import Path

import yaml
import jsonschema


SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "schemas" / "consultant_config_schema.yaml"
WEIGHTS_SUM_TOLERANCE = 0.01


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(config_path: str) -> tuple[bool, str]:
    try:
        config = load_yaml(config_path)
    except FileNotFoundError:
        return False, f"file not found: {config_path}"
    except yaml.YAMLError as e:
        return False, f"YAML parse error: {e}"

    try:
        schema = load_yaml(str(SCHEMA_PATH))
    except FileNotFoundError:
        return False, f"schema not found at {SCHEMA_PATH}"

    try:
        jsonschema.validate(instance=config, schema=schema)
    except jsonschema.ValidationError as e:
        return False, e.message
    except jsonschema.SchemaError as e:
        return False, f"schema error: {e.message}"

    # Extra check: method_weights sum must be 1.0 ±0.01
    weights = config.get("method_weights", {})
    total = sum(weights.values())
    if abs(total - 1.0) > WEIGHTS_SUM_TOLERANCE:
        return False, f"method_weights sum is {total:.4f}, expected 1.0 ±{WEIGHTS_SUM_TOLERANCE}"

    return True, ""


def main():
    parser = argparse.ArgumentParser(description="Validate consultant_config.yaml against Bússola PME schema.")
    parser.add_argument("--config", required=True, help="Path to consultant_config.yaml")
    args = parser.parse_args()

    valid, reason = validate(args.config)
    if valid:
        print("VALID")
        sys.exit(0)
    else:
        print(f"INVALID: {reason}")
        sys.exit(1)


if __name__ == "__main__":
    # Example: python config_schema_validator.py --config examples/consultant_config_guided.yaml
    main()

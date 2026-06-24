import yaml
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path("configs")


def load_yaml(name: str) -> Dict[str, Any]:
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r") as f:
        return yaml.safe_load(f)


def load_data_sources() -> Dict[str, Any]:
    return load_yaml("data_sources.yaml")


def load_positions() -> Dict[str, Any]:
    return load_yaml("positions.yaml")


def load_scenarios() -> Dict[str, Any]:
    return load_yaml("scenarios.yaml")


def load_risk_limits() -> Dict[str, Any]:
    return load_yaml("risk_limits.yaml")


def load_dashboard_config() -> Dict[str, Any]:
    return load_yaml("dashboard.yaml")

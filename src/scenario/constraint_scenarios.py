from ..utils.config_loader import load_scenarios
from ..utils.logging import get_logger

logger = get_logger(__name__)


def build_constraint_scenario(name: str):
    cfg = load_scenarios()
    scenarios = {s["name"]: s for s in cfg.get("constraint_scenarios", {}).get("scenarios", [])}
    scenario = scenarios.get(name)
    if scenario is None:
        raise ValueError(f"Constraint scenario not found: {name}")

    logger.info(f"Building constraint scenario {name}: {scenario}")
    # TODO: adjust interface limits / shadow prices
    return scenario

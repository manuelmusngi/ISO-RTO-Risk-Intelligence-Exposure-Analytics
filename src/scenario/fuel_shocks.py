from ..utils.config_loader import load_scenarios
from ..utils.logging import get_logger

logger = get_logger(__name__)


def build_fuel_shock(name: str):
    cfg = load_scenarios()
    scenarios = {s["name"]: s for s in cfg.get("fuel_shocks", {}).get("scenarios", [])}
    scenario = scenarios.get(name)
    if scenario is None:
        raise ValueError(f"Fuel shock scenario not found: {name}")

    logger.info(f"Building fuel shock {name}: {scenario}")
    # TODO: apply absolute change to fuel price series
    return scenario

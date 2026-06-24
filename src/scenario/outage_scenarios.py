from ..utils.config_loader import load_scenarios, load_positions
from ..utils.logging import get_logger

logger = get_logger(__name__)


def build_outage_scenario(name: str):
    cfg = load_scenarios()
    scenarios = {s["name"]: s for s in cfg.get("outage_scenarios", {}).get("rules", [])}
    scenario = scenarios.get(name)
    if scenario is None:
        raise ValueError(f"Outage scenario not found: {name}")

    positions = load_positions()
    logger.info(f"Building outage scenario {name} with rules: {scenario}")
    # TODO: select units and mark as out for duration
    return scenario

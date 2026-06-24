import pandas as pd
from ..utils.config_loader import load_scenarios
from ..utils.logging import get_logger

logger = get_logger(__name__)


def apply_price_shock(lmp_df: pd.DataFrame, scenario_name: str) -> pd.DataFrame:
    cfg = load_scenarios()
    scenarios = {s["name"]: s for s in cfg.get("price_shocks", {}).get("scenarios", [])}
    scenario = scenarios.get(scenario_name)
    if scenario is None:
        raise ValueError(f"Price shock scenario not found: {scenario_name}")

    sigma_mult = scenario["sigma_multiplier"]
    direction = scenario["direction"]
    logger.info(f"Applying price shock {scenario_name}: {direction} x {sigma_mult}σ")

    # TODO: use historical volatility; for now simple additive
    shocked = lmp_df.copy()
    shocked["lmp_shocked"] = shocked["lmp"]  # placeholder
    return shocked

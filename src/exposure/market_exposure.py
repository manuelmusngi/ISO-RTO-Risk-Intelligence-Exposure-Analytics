import pandas as pd
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_market_exposure(lmp_df: pd.DataFrame, fuel_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Computing market exposure (stub)")
    # TODO: link fuel price changes to power price changes, volatility metrics
    return pd.DataFrame()

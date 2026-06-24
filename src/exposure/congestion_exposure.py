import pandas as pd
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_congestion_exposure(constraints_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Computing congestion exposure (stub)")
    # TODO: map flows and positions to constraints and shadow prices
    return pd.DataFrame()

import pandas as pd
from ..utils.logging import get_logger

logger = get_logger(__name__)


def validate_lmp_schema(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {"iso", "node", "timestamp", "lmp"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing LMP columns: {missing}")
    logger.info("LMP schema validated")
    return df

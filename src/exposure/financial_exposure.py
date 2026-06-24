import pandas as pd
from typing import Dict
from ..utils.config_loader import load_positions
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_ftr_mtm(lmp_da: pd.DataFrame) -> pd.DataFrame:
    positions = load_positions()
    ftrs = positions.get("ftr_positions", [])
    logger.info("Computing FTR MTM (stub)")
    # TODO: implement FTR P&L using DA sink-source spread
    return pd.DataFrame()

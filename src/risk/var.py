from typing import Sequence
from ..utils.math_utils import var_from_distribution
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_var(pnl_paths: Sequence[float], alpha: float = 0.95) -> float:
    var_value = var_from_distribution(pnl_paths, alpha)
    logger.info(f"Computed VaR (alpha={alpha}): {var_value:.2f}")
    return var_value

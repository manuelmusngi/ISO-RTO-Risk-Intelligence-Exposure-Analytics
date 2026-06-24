from typing import Sequence
from ..utils.math_utils import cvar_from_distribution
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_cvar(pnl_paths: Sequence[float], alpha: float = 0.95) -> float:
    cvar_value = cvar_from_distribution(pnl_paths, alpha)
    logger.info(f"Computed CVaR (alpha={alpha}): {cvar_value:.2f}")
    return cvar_value

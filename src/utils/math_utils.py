import numpy as np
from typing import Sequence


def var_from_distribution(pnl: Sequence[float], alpha: float = 0.95) -> float:
    return float(np.percentile(pnl, (1 - alpha) * 100))


def cvar_from_distribution(pnl: Sequence[float], alpha: float = 0.95) -> float:
    var_level = var_from_distribution(pnl, alpha)
    tail = [x for x in pnl if x <= var_level]
    return float(np.mean(tail)) if tail else var_level

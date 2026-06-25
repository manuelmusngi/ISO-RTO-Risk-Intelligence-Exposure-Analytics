from typing import Sequence
from ..utils.logging import get_logger

logger = get_logger(__name__)


def compute_pfe(exposure_paths: Sequence[float], alpha: float = 0.95) -> float:
    # Placeholder: max exposure in tail
    sorted_paths = sorted(exposure_paths)
    idx = int((1 - alpha) * len(sorted_paths))
    pfe_value = sorted_paths[idx] if sorted_paths else 0.0
    logger.info(f"Computed PFE (alpha={alpha}): {pfe_value:.2f}")
    return pfe_value

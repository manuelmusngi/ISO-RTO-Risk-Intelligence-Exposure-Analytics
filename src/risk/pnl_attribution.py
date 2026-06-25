from ..utils.logging import get_logger

logger = get_logger(__name__)


def attribute_pnl():
    logger.info("Attributing P&L (stub)")
    # TODO: decompose P&L into price, volume, congestion, fuel effects
    return {}

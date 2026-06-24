import time
from functools import wraps
from .logging import get_logger

logger = get_logger(__name__)


def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{fn.__name__} executed in {elapsed:.3f}s")
        return result
    return wrapper

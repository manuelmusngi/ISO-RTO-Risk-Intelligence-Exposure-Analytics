from pathlib import Path
import pandas as pd
from ..utils.config_loader import load_data_sources
from ..utils.logging import get_logger

logger = get_logger(__name__)


def get_data_paths():
    cfg = load_data_sources()
    raw_dir = Path(cfg["storage"]["raw_data_dir"])
    processed_dir = Path(cfg["storage"]["processed_data_dir"])
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, processed_dir


def load_sample_lmps() -> pd.DataFrame:
    path = Path("data/examples/sample_lmps.csv")
    logger.info(f"Loading sample LMPs from {path}")
    return pd.read_csv(path)

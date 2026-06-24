from typing import Dict, Any
from .utils import build_url
from ..utils.config_loader import load_data_sources
from ..utils.logging import get_logger

logger = get_logger(__name__)


def get_iso_config(iso: str) -> Dict[str, Any]:
    cfg = load_data_sources()
    iso_cfg = cfg.get("isos", {}).get(iso)
    if iso_cfg is None:
        raise ValueError(f"ISO config not found for {iso}")
    return iso_cfg


def fetch_lmp(iso: str) -> Any:
    iso_cfg = get_iso_config(iso)
    endpoint = iso_cfg["endpoints"]["lmp"]
    url = build_url(iso_cfg["base_url"], endpoint["path"], endpoint.get("params", {}))
    logger.info(f"Fetching LMP for {iso} from {url}")
    # TODO: implement requests.get + parsing
    return None

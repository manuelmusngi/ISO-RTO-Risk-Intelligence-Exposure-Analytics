import streamlit as st
from ..utils.config_loader import load_dashboard_config
from .components.exposure_heatmap import render_exposure_heatmap
from .components.scenario_sliders import render_scenario_controls
from .components.risk_summary_cards import render_risk_summary
from ..utils.logging import get_logger

logger = get_logger(__name__)


def main():
    cfg = load_dashboard_config()
    meta = cfg.get("meta", {})
    st.set_page_config(page_title=meta.get("title", "ISO/RTO Risk Console"), layout="wide")

    st.title(meta.get("title", "ISO/RTO Risk Console"))
    view = st.sidebar.selectbox("View", ["trader", "operator", "risk"])

    st.sidebar.write(f"Active view: {view}")
    logger.info(f"Dashboard started in view: {view}")

    render_risk_summary()
    render_exposure_heatmap()
    render_scenario_controls()


if __name__ == "__main__":
    main()

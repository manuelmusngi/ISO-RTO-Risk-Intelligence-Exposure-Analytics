import streamlit as st


def render_risk_summary():
    st.subheader("Risk Summary")
    cols = st.columns(3)
    cols[0].metric("Portfolio VaR (95%)", "$0", "stub")
    cols[1].metric("Portfolio CVaR (95%)", "$0", "stub")
    cols[2].metric("PFE (95%)", "$0", "stub")

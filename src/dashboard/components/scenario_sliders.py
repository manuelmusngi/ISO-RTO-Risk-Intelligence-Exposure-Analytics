import streamlit as st


def render_scenario_controls():
    st.subheader("Scenario Controls")
    st.write("Scenario controls placeholder — connect to scenario engine.")
    st.slider("Price shock σ multiplier", 0.0, 5.0, 1.0)
    st.slider("Load deviation (%)", -20, 20, 0)

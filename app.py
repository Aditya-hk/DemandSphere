import streamlit as st
import joblib
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(
    page_title="DemandSphere",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("DemandSphere")

st.markdown(
    """
### AI-Powered Urban Mobility Demand Forecasting Platform
Forecast ride demand across operational zones using Machine Learning.
"""
)

st.divider()

# -----------------------------
# KPI CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Model",
        "XGBoost"
    )

with col2:
    st.metric(
        "Model Accuracy",
        "94%"
    )

with col3:
    st.metric(
        "Operational Zones",
        "6"
    )

with col4:
    st.metric(
        "Forecast Horizon",
        "1 Hour"
    )

st.divider()

# -----------------------------
# ABOUT
# -----------------------------

st.subheader("Project Overview")

st.write("""
DemandSphere is an AI-powered urban mobility analytics platform that predicts
future ride demand across operational zones.

The system combines:

- Geospatial Clustering (MiniBatch KMeans)
- Temporal Feature Engineering
- XGBoost Regression
- Interactive Visual Analytics

The goal is to assist mobility platforms in proactive fleet allocation and demand forecasting.
""")

st.divider()

# -----------------------------
# FEATURES
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Forecast

Predict future ride demand based on

- Date
- Time
- Operational Zone
""")

with col2:

    st.success("""
### Analytics

Visualize

- Demand Trends
- Zone Analytics
- Feature Importance
- Model Performance
""")

st.divider()

st.caption("DemandSphere © 2026")

import streamlit as st
import pandas as pd
import plotly.express as px
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Model Performance")

st.markdown(
    "Evaluation of the machine learning models used for ride demand forecasting."
)

st.divider()
c1, c2, c3, c4 = st.columns(4)

c1.metric("Best Model", "XGBoost")

c2.metric("R² Score", "0.9538")

c3.metric("MAE", "8.27")

c4.metric("RMSE", "14.07")
comparison = pd.DataFrame({
    "Model":[
        "Linear Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost"
    ],
    "R²":[
        0.68,
        0.83,
        0.9312,
        0.9538
    ]
})

fig = px.bar(
    comparison,
    x="Model",
    y="R²",
    color="R²",
    text_auto=".2f",
    title="Model Comparison"
)

st.plotly_chart(fig,use_container_width=True)
importance = pd.read_csv("models/feature_importance.csv")

fig = px.bar(
    importance.sort_values("Importance"),
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    title="Feature Importance"
)

st.plotly_chart(fig,use_container_width=True)
results = pd.read_csv("models/predictions.csv")

fig = px.scatter(
    results,
    x="Actual",
    y="Predicted",
    opacity=0.6,
    trendline="ols",
    title="Actual vs Predicted Ride Demand"
)

st.plotly_chart(fig,use_container_width=True)
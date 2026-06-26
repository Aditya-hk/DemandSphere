import streamlit as st
from datetime import date
import joblib
import pandas as pd
import plotly.express as px
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Demand Forecast",
    layout="wide"
)
model = joblib.load("models/xgbbb.pkl")
cluster_centers = pd.read_csv("data/cluster_centerss.csv")
map_df = cluster_centers.copy()

map_df["zone"] = [
    "Zone A",
    "Zone B",
    "Zone C",
    "Zone D",
    "Zone E",
    "Zone F"
]
zone_mapping = {
    "Zone A": 0,
    "Zone B": 1,
    "Zone C": 2,
    "Zone D": 3,
    "Zone E": 4,
    "Zone F": 5
}
st.title("🔮 Ride Demand Forecast")

st.markdown("""
Estimate the expected number of ride requests for a selected operational zone.
""")

st.divider()
left, right = st.columns([1, 2])

with left:

    st.subheader("Forecast Settings")

    forecast_date = st.date_input(
        "📅 Forecast Date",
        value=date.today()
    )

    forecast_hour = st.select_slider(
        "🕒 Forecast Hour",
        options=list(range(24)),
        value=12,
        format_func=lambda x: f"{x:02d}:00"
    )

    zone = st.selectbox(
        "🗺 Operational Zone",
        [
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D",
            "Zone E",
            "Zone F"
        ]
    )
    fig = px.scatter_map(
        map_df,
        lat="pickup_latitude",
        lon="pickup_longitude",
        hover_name="zone",
        zoom=10,
        height=500
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    predict = st.button(
        "🚖 Generate Forecast",
        use_container_width=True
    )
    if predict:
        cluster = zone_mapping[zone]

        st.write(f"Selected Cluster : {cluster}")
        day = forecast_date.day
        month = forecast_date.month
        day_of_week = forecast_date.weekday()

        is_weekend = int(day_of_week >= 5)
        st.write(f"Day: {day}")
        st.write(f"Month: {month}")
        st.write(f"Weekday: {day_of_week}")
        st.write(f"Weekend: {is_weekend}")
        is_rush_hour = int(forecast_hour in [7, 8, 9, 17, 18, 19])

        is_night = int(forecast_hour <= 5)

        office_hours = int(9 <= forecast_hour <= 17)

        st.write(f"Rush Hour: {is_rush_hour}")
        st.write(f"Night: {is_night}")
        st.write(f"Office Hours: {office_hours}")
        latitude = cluster_centers.loc[
            cluster_centers["cluster"] == cluster,
            "pickup_latitude"
        ].iloc[0]

        longitude = cluster_centers.loc[
            cluster_centers["cluster"] == cluster,
            "pickup_longitude"
        ].iloc[0]
        # 5. Create Input DataFrame
        input_data = pd.DataFrame({
            "cluster": [cluster],
            "pickup_latitude": [latitude],
            "pickup_longitude": [longitude],
            "hour": [forecast_hour],
            "day": [day],
            "day_of_week": [day_of_week],
            "month": [month],
            "is_weekend": [is_weekend],
            "is_rush_hour": [is_rush_hour],
            "is_night": [is_night],
            "office_hours": [office_hours]
        })

        prediction = model.predict(input_data)[0]
        if prediction < 20:
            demand = "🟢 Low"

        elif prediction < 50:
            demand = "🟡 Moderate"

        elif prediction < 80:
            demand = "🟠 High"

        else:
            demand = "🔴 Very High"
        st.metric(
            "Demand Level",
            demand
        )
        if prediction < 20:
            recommendation = "Maintain current driver fleet."

        elif prediction < 50:
            recommendation = "Slightly increase driver availability."

        elif prediction < 80:
            recommendation = "Deploy additional drivers."

        else:
            recommendation = "Activate surge operations and maximize fleet availability."
        st.success(recommendation)
        st.success(f"Predicted Ride Demand : {prediction:.0f}")
        st.divider()

        st.write("### Forecast Summary")

        st.write(f"""
        **Zone:** {zone}

        **Forecast Date:** {forecast_date}

        **Hour:** {forecast_hour:02d}:00

        **Predicted Ride Requests:** {prediction:.0f}
        """)
        prediction = float(model.predict(input_data)[0])

        progress = min(prediction / 100.0, 1.0)

        st.progress(progress)

with right:
    with right:
        st.subheader("Prediction Results")

        if predict:
            prediction = model.predict(input_data)[0]

            st.metric(
                label="🚖 Expected Ride Requests",
                value=f"{prediction:.0f}"
            )
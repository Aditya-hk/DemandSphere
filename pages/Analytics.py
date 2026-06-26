
import streamlit as st
import pandas as pd
import plotly.express as px
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(
    page_title="Demand Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Demand Analytics")

st.markdown(
    "Interactive insights into ride demand across operational zones."
)

st.divider()

# Load data
df = pd.read_csv("data/demand_dff.csv")

total_trips = int(df["ride_count"].sum())

average_demand = round(df["ride_count"].mean(), 1)

peak_hour = (
    df.groupby("hour")["ride_count"]
      .sum()
      .idxmax()
)

busiest_zone = (
    df.groupby("zone_name")["ride_count"]
      .sum()
      .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Trips", f"{total_trips:,}")

c2.metric("Average Demand", average_demand)

c3.metric("Peak Hour", f"{peak_hour}:00")

c4.metric("Busiest Zone", busiest_zone)

st.divider()

st.subheader("Hourly Ride Demand")

hourly = (
    df.groupby("hour")["ride_count"]
      .sum()
      .reset_index()
)

fig = px.line(
    hourly,
    x="hour",
    y="ride_count",
    markers=True,
    title="Ride Demand by Hour"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Operational Zone Demand")

zone = (
    df.groupby("zone_name")["ride_count"]
      .sum()
      .reset_index()
)

fig = px.bar(
    zone,
    x="zone_name",
    y="ride_count",
    color="ride_count",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Weekday vs Weekend")

week = (
    df.groupby("is_weekend")["ride_count"]
      .mean()
      .reset_index()
)

week["is_weekend"] = week["is_weekend"].map({
    0: "Weekday",
    1: "Weekend"
})

fig = px.bar(
    week,
    x="is_weekend",
    y="ride_count",
    color="is_weekend",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Monthly Demand")

month = (
    df.groupby("month")["ride_count"]
      .sum()
      .reset_index()
)

fig = px.area(
    month,
    x="month",
    y="ride_count"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Hour × Zone Demand Heatmap")

heat = df.pivot_table(
    values="ride_count",
    index="hour",
    columns="zone_name",
    aggfunc="mean"
)

fig = px.imshow(
    heat,
    aspect="auto",
    labels={
        "x":"Zone",
        "y":"Hour",
        "color":"Average Demand"
    }
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Top 10 Highest Demand Hours")

top = (
    df.groupby("pickup_hour")["ride_count"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    top,
    x="pickup_hour",
    y="ride_count",
    color="ride_count",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)
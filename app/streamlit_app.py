from pathlib import Path

import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Recovery Access Gap Index",
    page_icon="🧭",
    layout="wide",
)


# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

FINAL_PRIORITY_CSV = PROCESSED_DIR / "municipality_final_priority_index.csv"
FINAL_PRIORITY_GEOJSON = PROCESSED_DIR / "municipality_final_priority_index.geojson"


# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    priority_df = pd.read_csv(FINAL_PRIORITY_CSV)
    priority_geo = gpd.read_file(FINAL_PRIORITY_GEOJSON)

    # Clean sentinel/missing values from SVI-derived columns
    score_cols = [
        "social_vulnerability_pct",
        "final_priority_score",
        "recovery_access_gap_score",
    ]

    for col in score_cols:
        if col in priority_df.columns:
            priority_df[col] = pd.to_numeric(priority_df[col], errors="coerce")
            priority_df.loc[priority_df[col] < 0, col] = np.nan

        if col in priority_geo.columns:
            priority_geo[col] = pd.to_numeric(priority_geo[col], errors="coerce")
            priority_geo.loc[priority_geo[col] < 0, col] = np.nan

    return priority_df, priority_geo


priority_df, priority_geo = load_data()


# -----------------------------
# Header
# -----------------------------
st.title("Recovery Access Gap Index")
st.caption(
    "A municipality-level dashboard identifying Massachusetts communities with high opioid-related burden, "
    "limited recovery service access, and elevated social vulnerability."
)


# -----------------------------
# KPI cards
# -----------------------------
total_municipalities = len(priority_df)
very_high_priority = (priority_df["priority_category"] == "Very high priority").sum()
no_listed_services = (priority_df["service_diversity_score"] == 0).sum()
median_priority_score = priority_df["final_priority_score"].median()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Municipalities analyzed", f"{total_municipalities:,}")
col2.metric("Very high priority", f"{very_high_priority:,}")
col3.metric("No listed services", f"{no_listed_services:,}")
col4.metric("Median priority score", f"{median_priority_score:.2f}")


# -----------------------------
# Preview table
# -----------------------------
st.subheader("Top Priority Communities")

top_priority = priority_df.sort_values(
    "final_priority_score",
    ascending=False,
)[[
    "TOWN",
    "COUNTY",
    "estimated_population",
    "recovery_access_gap_score",
    "social_vulnerability_pct",
    "final_priority_score",
    "priority_category",
]].head(20)

st.dataframe(top_priority, use_container_width=True)
# -----------------------------
# Top priority bar chart
# -----------------------------
st.subheader("Highest Final Priority Scores")

top_chart = top_priority.sort_values(
    "final_priority_score",
    ascending=True,
)

fig = px.bar(
    top_chart,
    x="final_priority_score",
    y="TOWN",
    orientation="h",
    color="priority_category",
    hover_data=[
        "COUNTY",
        "estimated_population",
        "recovery_access_gap_score",
        "social_vulnerability_pct",
    ],
    labels={
        "final_priority_score": "Final Priority Score",
        "TOWN": "Municipality",
        "priority_category": "Priority Category",
    },
    title="Top 20 Municipalities by Final Priority Score",
)

fig.update_layout(
    height=650,
    yaxis_title="",
    xaxis_title="Final Priority Score",
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Interactive priority map
# -----------------------------
# -----------------------------
# Interactive priority map
# -----------------------------
st.subheader("Massachusetts Final Priority Map")

map_df = priority_geo.copy()
map_df = map_df.to_crs("EPSG:4326")

map_df["final_priority_score"] = pd.to_numeric(
    map_df["final_priority_score"],
    errors="coerce",
)

map_df.loc[map_df["final_priority_score"] < 0, "final_priority_score"] = np.nan

fig_map = px.choropleth_mapbox(
    map_df,
    geojson=map_df.__geo_interface__,
    locations=map_df.index,
    color="final_priority_score",
    hover_name="TOWN",
    hover_data={
        "COUNTY": True,
        "priority_category": True,
        "gap_category": True,
        "final_priority_score": ":.3f",
        "recovery_access_gap_score": ":.3f",
        "social_vulnerability_pct": ":.3f",
        "service_diversity_score": True,
        "avg_deaths_2021_2023": ":.1f",
        "avg_ems_incidents_2022_2023": ":.1f",
    },
    mapbox_style="carto-positron",
    center={"lat": 42.25, "lon": -71.8},
    zoom=6.7,
    opacity=0.8,
    color_continuous_scale="YlOrRd",
    range_color=(0, map_df["final_priority_score"].quantile(0.95)),
    labels={
        "final_priority_score": "Final Priority Score",
    },
)

fig_map.update_layout(
    height=750,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

fig_map.update_traces(
    marker_line_width=0.35,
    marker_line_color="white",
)

st.plotly_chart(fig_map, use_container_width=True)
# -----------------------------
# Access vs burden explorer
# -----------------------------
# -----------------------------
# Access vs burden explorer
# -----------------------------
st.subheader("Access vs Burden Explorer")

scatter_df = priority_df.copy()

scatter_cols = [
    "recovery_access_gap_score",
    "social_vulnerability_pct",
    "final_priority_score",
]

for col in scatter_cols:
    scatter_df[col] = pd.to_numeric(scatter_df[col], errors="coerce")
    scatter_df.loc[scatter_df[col] < 0, col] = np.nan

scatter_df = scatter_df.dropna(subset=scatter_cols)

fig_scatter = px.scatter(
    scatter_df,
    x="recovery_access_gap_score",
    y="social_vulnerability_pct",
    size="final_priority_score",
    size_max=35,
    color="priority_category",
    hover_name="TOWN",
    hover_data={
        "COUNTY": True,
        "avg_deaths_2021_2023": ":.1f",
        "avg_ems_incidents_2022_2023": ":.1f",
        "service_diversity_score": True,
        "recovery_access_gap_score": ":.3f",
        "social_vulnerability_pct": ":.3f",
        "final_priority_score": ":.3f",
    },
    labels={
        "recovery_access_gap_score": "Recovery Access Gap Score",
        "social_vulnerability_pct": "Social Vulnerability Percentile",
        "final_priority_score": "Final Priority Score",
        "priority_category": "Priority Category",
    },
    title="Municipalities by Recovery Access Gap and Social Vulnerability",
)

fig_scatter.update_layout(
    height=650,
    xaxis_title="Recovery Access Gap Score",
    yaxis_title="Social Vulnerability Percentile",
)

st.plotly_chart(fig_scatter, use_container_width=True)
import pandas as pd
from pathlib import Path

processed_dir = Path("data/processed")

df = pd.read_csv(processed_dir / "municipality_final_priority_index.csv")

print("Rows:", len(df))
print("Service diversity distribution:")
print(df["service_diversity_score"].value_counts().sort_index())

print("\nTowns with 0 tracked services:")
print((df["service_diversity_score"] == 0).sum())

df[df["service_diversity_score"] == 0][[
    "TOWN",
    "COUNTY",
    "treatment_facility_count",
    "peer_recovery_count",
    "ssp_count",
    "harm_reduction_count",
    "service_diversity_score",
]].head(30)
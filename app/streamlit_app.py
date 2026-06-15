from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="ANCHOR",
    layout="wide",
)
st.markdown(
    """
    <div style="line-height:1.15; margin-bottom:0.4rem;">
        <span style="font-size:2.4rem; font-weight:700;">ANCHOR</span>
        <span style="font-size:1rem; color:#9CA3AF; margin-left:0.75rem;">
            Access to Naloxone, Care, Harm Reduction, Outreach, and Recovery
        </span>
    </div>
    <div style="font-size:0.95rem; color:#9CA3AF; margin-bottom:0.5rem;">
        Mapping overdose burden, social vulnerability, and access to harm reduction and recovery supports across Massachusetts.
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

FINAL_PRIORITY_CSV = PROCESSED_DIR / "municipality_final_priority_index_with_distance.csv"
FINAL_PRIORITY_GEOJSON = PROCESSED_DIR / "municipality_final_priority_index_with_distance.geojson"


# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    priority_df = pd.read_csv(FINAL_PRIORITY_CSV)
    priority_geo = gpd.read_file(FINAL_PRIORITY_GEOJSON)

    score_cols = [
        "social_vulnerability_pct",
        "final_priority_score",
        "anchor_priority_score",
        "recovery_access_gap_score",
        "nearest_any_service_distance_miles",
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
# Compatibility fix: older processed data may not have ANCHOR public-facing columns yet.
# Create them from existing priority score columns if missing.

if "anchor_priority_score" not in priority_df.columns:
    if "distance_adjusted_priority_score" in priority_df.columns:
        priority_df["anchor_priority_score"] = pd.to_numeric(
            priority_df["distance_adjusted_priority_score"],
            errors="coerce"
        )
    elif "final_priority_score" in priority_df.columns:
        priority_df["anchor_priority_score"] = pd.to_numeric(
            priority_df["final_priority_score"],
            errors="coerce"
        )
    else:
        priority_df["anchor_priority_score"] = 0

if (
    "anchor_priority_level" not in priority_df.columns
    or priority_df["anchor_priority_level"].isna().any()
):
    score = pd.to_numeric(priority_df["anchor_priority_score"], errors="coerce")

    q50 = score.quantile(0.50)
    q75 = score.quantile(0.75)
    q90 = score.quantile(0.90)

    def assign_anchor_priority_level(value):
        if pd.isna(value):
            return "Lower priority"
        if value >= q90:
            return "Very high priority"
        if value >= q75:
            return "High priority"
        if value >= q50:
            return "Moderate priority"
        return "Lower priority"

    priority_df["anchor_priority_level"] = score.apply(assign_anchor_priority_level)

if "access_gap_level" not in priority_df.columns and "gap_category" in priority_df.columns:
    priority_df["access_gap_level"] = priority_df["gap_category"]
if "gap_category" not in priority_df.columns and "access_gap_level" in priority_df.columns:
    priority_df["gap_category"] = priority_df["access_gap_level"]
# -----------------------------
# Global filters
# -----------------------------
st.sidebar.header("Filters")

county_options = ["All"] + sorted(priority_df["COUNTY"].dropna().unique().tolist())
priority_options = ["All"] + sorted(priority_df["anchor_priority_level"].dropna().unique().tolist())
access_gap_filter = "All"

selected_county = st.sidebar.selectbox("County", county_options)
selected_priority = st.sidebar.selectbox("Priority level", priority_options)


max_priority_score = float(
    pd.to_numeric(priority_df["anchor_priority_score"], errors="coerce").max()
)

min_priority_score = st.sidebar.slider(
    "Minimum priority score",
    min_value=0.0,
    max_value=max_priority_score,
    value=0.0,
    step=0.05,
)

filtered_df = priority_df.copy()

if selected_county != "All":
    filtered_df = filtered_df[filtered_df["COUNTY"] == selected_county]

if selected_priority != "All":
    filtered_df = filtered_df[filtered_df["anchor_priority_level"] == selected_priority]

priority_score_filter = pd.to_numeric(
    filtered_df["anchor_priority_score"],
    errors="coerce",
)

if min_priority_score > 0:
    filtered_df = filtered_df[priority_score_filter >= min_priority_score].copy()
else:
    filtered_df = filtered_df.copy()

filtered_geo = priority_geo[
    priority_geo["town_join"].isin(filtered_df["town_join"])
].copy()

st.sidebar.caption(
    f"Showing {len(filtered_df):,} of {len(priority_df):,} municipalities."
)

map_overview_tab, profile_tab, priority_tab, explorer_tab, methodology_tab = st.tabs(
    [
        "Map Overview",
        "Community Profile",
        "Top Communities",
        "Access Explorer",
        "Terms & Definitions",
    ]
)


# -----------------------------
# Overview tab
# -----------------------------
with map_overview_tab:
    st.subheader("Massachusetts Harm Reduction Access Priority Map")

    st.markdown(
        """
        This map highlights Massachusetts municipalities where opioid-related burden,
        social vulnerability, and harm reduction access gaps may warrant closer attention.
        """
    )
    st.info(
    "Important: service access fields reflect source-listed records from the datasets used in this project. "
    "Local organizations may exist but not appear if they are not included in those structured sources, "
    "are listed under a parent organization, or fall outside the tracked service categories."
)

    map_df = filtered_geo.copy()

    if map_df.empty:
        st.warning("No municipalities match the selected filters. Reset filters in the sidebar to show the map.")
    else:
        map_df = map_df.to_crs("EPSG:4326")

        if "access_gap_level" not in map_df.columns and "gap_category" in map_df.columns:
            map_df["access_gap_level"] = map_df["gap_category"]

        if "gap_category" not in map_df.columns and "access_gap_level" in map_df.columns:
            map_df["gap_category"] = map_df["access_gap_level"]

        # Ensure map_df has ANCHOR score fields before map color scaling/rendering.
        if (
            "anchor_priority_score" not in map_df.columns
            or "anchor_priority_level" not in map_df.columns
        ):
            if "town_join" in map_df.columns and "town_join" in priority_df.columns:
                anchor_lookup_cols = [
                    col for col in [
                        "town_join",
                        "anchor_priority_score",
                        "anchor_priority_level",
                        "anchor_priority_rank",
                    ]
                    if col in priority_df.columns
                ]

                map_df = map_df.drop(
                    columns=[
                        "anchor_priority_score",
                        "anchor_priority_level",
                        "anchor_priority_rank",
                    ],
                    errors="ignore",
                )

                map_df = map_df.merge(
                    priority_df[anchor_lookup_cols].drop_duplicates("town_join"),
                    on="town_join",
                    how="left",
                )

        if "anchor_priority_score" not in map_df.columns:
            if "distance_adjusted_priority_score" in map_df.columns:
                map_df["anchor_priority_score"] = pd.to_numeric(
                    map_df["distance_adjusted_priority_score"],
                    errors="coerce",
                )
            elif "final_priority_score" in map_df.columns:
                map_df["anchor_priority_score"] = pd.to_numeric(
                    map_df["final_priority_score"],
                    errors="coerce",
                )
            else:
                map_df["anchor_priority_score"] = 0

        map_df["anchor_priority_score"] = pd.to_numeric(
            map_df["anchor_priority_score"],
            errors="coerce",
        )

        map_df.loc[
            map_df["anchor_priority_score"] < 0,
            "anchor_priority_score",
        ] = np.nan

        if "anchor_priority_score" in priority_df.columns:
            global_map_score_max = pd.to_numeric(
                priority_df["anchor_priority_score"],
                errors="coerce",
            ).max()
        else:
            global_map_score_max = map_df["anchor_priority_score"].max()

        if pd.isna(global_map_score_max):
            global_map_score_max = 1.0

        # Keep the color scale stable across filters.
        # Use at least 1.0 so lower-priority filtered views do not visually stretch into dark red.
        global_map_score_max = max(1.0, float(global_map_score_max))

        map_df = map_df.rename(
            columns={
                "anchor_priority_score": "Priority Score",
                "final_priority_score": "Original Priority Score",
                "recovery_access_gap_score": "Harm Reduction Access Gap Score",
                "social_vulnerability_pct": "Social Vulnerability",
                "nearest_any_service_distance_miles": "Nearest Listed Service (miles)",
                "services_within_5_miles": "Listed Services Within 5 Miles",
                "services_within_10_miles": "Listed Services Within 10 Miles",
                "service_types_within_5_miles": "Service Types Within 5 Miles",
                "service_diversity_score": "Service Types Inside Municipality",
                "avg_deaths_2021_2023": "Avg Annual Overdose Deaths",
                "avg_ems_incidents_2022_2023": "Avg Annual EMS Incidents",
                "anchor_priority_level": "Priority Level",
                "gap_category": "Access Gap Level",
                "COUNTY": "County",
                "TOWN": "Municipality",
            }
        )

        fig_map = px.choropleth_mapbox(
            map_df,
            geojson=map_df.__geo_interface__,
            locations=map_df.index,
            color="Priority Score",
            hover_name="Municipality",
            hover_data={
                "County": True,
                "Priority Level": True,
                "Access Gap Level": True,
                "Priority Score": ":.2f",
                "Harm Reduction Access Gap Score": ":.2f",
                "Social Vulnerability": ":.2f",
                "Nearest Listed Service (miles)": ":.1f",
                "Listed Services Within 5 Miles": True,
                "Listed Services Within 10 Miles": True,
                "Service Types Within 5 Miles": True,
                "Service Types Inside Municipality": True,
                "Avg Annual Overdose Deaths": ":.1f",
                "Avg Annual EMS Incidents": ":.1f",
            },
            mapbox_style="carto-positron",
            center={"lat": 42.25, "lon": -71.8},
            zoom=6.7,
            opacity=0.8,
            color_continuous_scale="YlOrRd",
            range_color=(0, global_map_score_max),
            labels={
                "Priority Score": "ANCHOR Priority Score",
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

        fig_map.update_coloraxes(
            cmin=0,
            cmax=global_map_score_max,
        )

        st.plotly_chart(fig_map, use_container_width=True)

    st.divider()
    st.subheader("Dashboard summary")

    total_municipalities = len(filtered_df)
    very_high_priority = (filtered_df["anchor_priority_level"] == "Very high priority").sum()
    no_tracked_services = (filtered_df["service_diversity_score"] == 0).sum()
    no_services_10mi = (filtered_df["services_within_10_miles"] == 0).sum()
    median_priority_score = filtered_df["anchor_priority_score"].median()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Municipalities shown", f"{total_municipalities:,}")
        with st.popover("What does this mean?"):
            st.write(
                "The dashboard shows Massachusetts municipalities included in the current filters. "
                "Each row represents one city or town."
            )

    with col2:
        st.metric("Very high priority", f"{very_high_priority:,}")
        with st.popover("What does this mean?"):
            st.write(
                "Municipalities with the highest combined priority based on overdose burden, "
                "social vulnerability, and access to source-listed supports."
            )

    with col3:
        st.metric("No in-town listings", f"{no_tracked_services:,}")
        with st.popover("What does this mean?"):
            st.write(
                "Municipalities with zero tracked source-listed service categories located inside the municipality. "
                "This does not mean no support exists locally."
            )

    with col4:
        st.metric("No services within 10 mi", f"{no_services_10mi:,}")
        with st.popover("What does this mean?"):
            st.write(
                "Municipalities with no source-listed service records within approximately 10 miles, "
                "using ZIP-code centroid distance estimates."
            )

    with col5:
        st.metric("Median priority score", f"{median_priority_score:.2f}")
        with st.popover("What does this mean?"):
            st.write(
                "The middle priority score among municipalities currently shown after filters are applied."
            )

    st.caption(
        "Tracked services are source-listed records from SAMHSA and Mass.gov datasets. "
        "Distance metrics are approximate and use ZIP-code centroids for service locations."
    )

# -----------------------------
# Community profile tab
# -----------------------------
with profile_tab:
    st.subheader("Community Profile")

    st.markdown(
        "Search for a municipality to understand its overdose burden, vulnerability, and access to source-listed harm reduction supports."
    )

    municipality_options = sorted(priority_df["TOWN"].dropna().unique().tolist())

    selected_municipality = st.selectbox(
        "Search or select a municipality",
        options=municipality_options,
        index=municipality_options.index("REVERE") if "REVERE" in municipality_options else 0,
    )

    profile = priority_df[priority_df["TOWN"] == selected_municipality].iloc[0]

    st.markdown(f"## {profile['TOWN'].title()}, {profile['COUNTY'].title()} County")

    # -----------------------------
    # Summary card
    # -----------------------------
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("### Priority summary")

        st.markdown(
            f"""
            **Priority level:** `{profile['anchor_priority_level']}`  
            **Access gap level:** `{profile['gap_category']}`  
            **Nearest listed service:** `{profile['nearest_any_service_distance_miles']:.1f} miles`  
            **In-town service types:** `{int(profile['service_diversity_score'])}/4`
            """
        )

    with right:
        st.metric("Priority score", f"{profile['anchor_priority_score']:.2f}")
        st.caption(
            "Higher scores suggest greater need for closer review based on burden, vulnerability, and access."
        )

    st.divider()

    # -----------------------------
    # Main profile metrics
    # -----------------------------
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Avg overdose deaths", f"{profile['avg_deaths_2021_2023']:.1f}")
    m2.metric("Avg EMS incidents", f"{profile['avg_ems_incidents_2022_2023']:.1f}")
    m3.metric("Social vulnerability", f"{profile['social_vulnerability_pct']:.2f}")
    m4.metric("Services within 5 mi", f"{int(profile['services_within_5_miles']):,}")

    m5, m6, m7, m8 = st.columns(4)

    m5.metric("Services within 10 mi", f"{int(profile['services_within_10_miles']):,}")
    m6.metric("Service types within 5 mi", f"{int(profile['service_types_within_5_miles'])}/4")
    m7.metric("Service types within 10 mi", f"{int(profile['service_types_within_10_miles'])}/4")
    m8.metric("In-town service types", f"{int(profile['service_diversity_score'])}/4")

    st.markdown("### Plain-language interpretation")

    if profile["service_diversity_score"] == 0 and profile["services_within_5_miles"] > 0:
        st.info(
            f"{profile['TOWN'].title()} has no tracked source-listed harm reduction service categories inside the municipality "
            f"in this dataset, but it has {int(profile['services_within_5_miles'])} source-listed service records within approximately 5 miles. "
            f"This suggests that nearby access may be stronger than an in-town count alone implies."
        )
    elif profile["services_within_10_miles"] == 0:
        st.warning(
            f"{profile['TOWN'].title()} has no source-listed service records within approximately 10 miles based on ZIP-code centroid estimates. "
            f"This may indicate a stronger geographic access gap."
        )
    else:
        st.success(
            f"{profile['TOWN'].title()} has source-listed services nearby, with "
            f"{int(profile['services_within_10_miles'])} records within approximately 10 miles."
        )

    # -----------------------------
    # Expandable detail table
    # -----------------------------
    with st.expander("View detailed community metrics"):
        profile_table = pd.DataFrame(
            {
                "Metric": [
                    "Priority score",
                    "Priority level",
                    "Access gap level",
                    "Harm reduction access gap score",
                    "Social vulnerability",
                    "Average annual overdose deaths",
                    "Average annual EMS incidents",
                    "In-town service types",
                    "Nearest listed service",
                    "Services within 5 miles",
                    "Services within 10 miles",
                    "Service types within 5 miles",
                    "Service types within 10 miles",
                    "Nearest treatment listing",
                    "Nearest peer recovery listing",
                    "Nearest syringe service listing",
                    "Nearest harm reduction listing",
                ],
                "Value": [
                    f"{profile['anchor_priority_score']:.2f}",
                    profile["anchor_priority_level"],
                    profile["gap_category"],
                    f"{profile['recovery_access_gap_score']:.2f}",
                    f"{profile['social_vulnerability_pct']:.2f}",
                    f"{profile['avg_deaths_2021_2023']:.1f}",
                    f"{profile['avg_ems_incidents_2022_2023']:.1f}",
                    f"{int(profile['service_diversity_score'])}/4",
                    f"{profile['nearest_any_service_distance_miles']:.1f} miles",
                    f"{int(profile['services_within_5_miles'])}",
                    f"{int(profile['services_within_10_miles'])}",
                    f"{int(profile['service_types_within_5_miles'])}/4",
                    f"{int(profile['service_types_within_10_miles'])}/4",
                    f"{profile['nearest_treatment_distance_miles']:.1f} miles",
                    f"{profile['nearest_peer_recovery_distance_miles']:.1f} miles",
                    f"{profile['nearest_ssp_distance_miles']:.1f} miles",
                    f"{profile['nearest_harm_reduction_distance_miles']:.1f} miles",
                ],
            }
        )

        st.dataframe(profile_table, use_container_width=True, hide_index=True)
# -----------------------------
# -----------------------------
# Top communities tab
# -----------------------------
with priority_tab:
    st.subheader("Top Communities")

    st.markdown(
        "Ranked municipalities based on the ANCHOR Priority Score. Higher scores suggest greater need for closer review."
    )

    search_term = st.text_input("Search municipality", "")

    top_df = filtered_df.copy()

    if search_term:
        top_df = top_df[
            top_df["TOWN"].str.contains(search_term, case=False, na=False)
        ]

    top_df = top_df.sort_values(
        "anchor_priority_score",
        ascending=False,
    ).copy()

    display_top = top_df[[
        "TOWN",
        "COUNTY",
        "anchor_priority_level",
        "anchor_priority_score",
        "nearest_any_service_distance_miles",
        "services_within_5_miles",
        "services_within_10_miles",
        "service_diversity_score",
        "social_vulnerability_pct",
        "avg_deaths_2021_2023",
        "avg_ems_incidents_2022_2023",
    ]].rename(
        columns={
            "TOWN": "Municipality",
            "COUNTY": "County",
            "anchor_priority_level": "Priority Level",
            "anchor_priority_score": "Priority Score",
            "nearest_any_service_distance_miles": "Nearest Listed Service (mi)",
            "services_within_5_miles": "Services Within 5 mi",
            "services_within_10_miles": "Services Within 10 mi",
            "service_diversity_score": "In-Town Service Types",
            "social_vulnerability_pct": "Social Vulnerability",
            "avg_deaths_2021_2023": "Avg Annual Overdose Deaths",
            "avg_ems_incidents_2022_2023": "Avg Annual EMS Incidents",
        }
    )

    if display_top.empty:
        st.warning("No municipalities match the current filters or search.")
    else:
        priority_order = [
            "Very high priority",
            "High priority",
            "Moderate priority",
            "Lower priority",
        ]

        priority_color_map = {
            "Very high priority": "#8B0000",
            "High priority": "#E4572E",
            "Moderate priority": "#F3A712",
            "Lower priority": "#4C78A8",
        }

        chart_df = display_top.head(20).sort_values("Priority Score", ascending=True)

        fig_bar = px.bar(
            chart_df,
            x="Priority Score",
            y="Municipality",
            orientation="h",
            color="Priority Level",
            color_discrete_map=priority_color_map,
            category_orders={
                "Priority Level": priority_order,
                "Municipality": chart_df["Municipality"].tolist(),
            },
            hover_data=[
                "County",
                "Nearest Listed Service (mi)",
                "Services Within 5 mi",
                "Services Within 10 mi",
                "Social Vulnerability",
            ],
            title="Top 20 Municipalities by Priority Score",
        )

        fig_bar.update_layout(
            height=650,
            yaxis_title="",
            xaxis_title="Priority Score",
            margin={"r": 20, "t": 50, "l": 20, "b": 20},
            legend_title_text="Priority Level",
            legend_traceorder="normal",
        )

        fig_bar.update_yaxes(
            categoryorder="array",
            categoryarray=chart_df["Municipality"].tolist(),
        )

        fig_bar.update_layout(
            height=650,
            yaxis_title="",
            xaxis_title="Priority Score",
            margin={"r": 20, "t": 50, "l": 20, "b": 20},
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        with st.expander("View ranked data table"):
            st.dataframe(
                display_top,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Download filtered table as CSV",
                data=display_top.to_csv(index=False),
                file_name="filtered_priority_communities.csv",
                mime="text/csv",
            )
# -----------------------------
# Access explorer tab
# -----------------------------
with explorer_tab:
    st.subheader("Access Explorer")

    st.markdown(
        "Explore how access gaps, social vulnerability, and distance-based service access relate to each other."
    )

    scatter_df = filtered_df.copy()

    scatter_cols = [
        "recovery_access_gap_score",
        "social_vulnerability_pct",
        "anchor_priority_score",
    ]

    for col in scatter_cols:
        scatter_df[col] = pd.to_numeric(scatter_df[col], errors="coerce")
        scatter_df.loc[scatter_df[col] < 0, col] = np.nan

    scatter_df = scatter_df.dropna(subset=scatter_cols)

    fig_scatter = px.scatter(
        scatter_df,
        x="recovery_access_gap_score",
        y="social_vulnerability_pct",
        size="anchor_priority_score",
        size_max=35,
        color="anchor_priority_level",
        hover_name="TOWN",
        hover_data={
            "COUNTY": True,
            "avg_deaths_2021_2023": ":.1f",
            "avg_ems_incidents_2022_2023": ":.1f",
            "nearest_any_service_distance_miles": ":.2f",
            "services_within_5_miles": True,
            "services_within_10_miles": True,
            "anchor_priority_score": ":.3f",
        },
        labels={
            "recovery_access_gap_score": "Harm Reduction Access Gap Score",
            "social_vulnerability_pct": "Social Vulnerability",
            "anchor_priority_score": "Priority Score",
            "anchor_priority_level": "Priority Level",
            "COUNTY": "County",
            "avg_deaths_2021_2023": "Avg Annual Overdose Deaths",
            "avg_ems_incidents_2022_2023": "Avg Annual EMS Incidents",
            "nearest_any_service_distance_miles": "Nearest Listed Service (mi)",
            "services_within_5_miles": "Services Within 5 mi",
            "services_within_10_miles": "Services Within 10 mi",
        },
        title="Access Gap vs Social Vulnerability",
    )

    fig_scatter.update_layout(
        height=650,
        xaxis_title="Harm Reduction Access Gap Score",
        yaxis_title="Social Vulnerability",
        margin={"r": 20, "t": 50, "l": 20, "b": 20},
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("#### Municipalities with no in-town listings but nearby services")

    no_intown_nearby = filtered_df[
        (filtered_df["service_diversity_score"] == 0)
        & (filtered_df["services_within_5_miles"] > 0)
    ].copy()

    st.metric(
        "No in-town listings but at least one service within 5 miles",
        f"{len(no_intown_nearby):,}",
    )

    access_table = no_intown_nearby[[
        "TOWN",
        "COUNTY",
        "nearest_any_service_distance_miles",
        "services_within_5_miles",
        "services_within_10_miles",
        "service_types_within_5_miles",
        "anchor_priority_score",
    ]].rename(
        columns={
            "TOWN": "Municipality",
            "COUNTY": "County",
            "nearest_any_service_distance_miles": "Nearest Listed Service (mi)",
            "services_within_5_miles": "Services Within 5 mi",
            "services_within_10_miles": "Services Within 10 mi",
            "service_types_within_5_miles": "Service Types Within 5 mi",
            "anchor_priority_score": "Priority Score",
        }
    ).sort_values("Nearest Listed Service (mi)")

    with st.expander("View municipalities in this group"):
        st.dataframe(access_table, use_container_width=True, hide_index=True)


# -----------------------------
# Terms & definitions tab
# -----------------------------
# -----------------------------
# Terms & score guide tab
# -----------------------------
with methodology_tab:
    st.subheader("Terms & Score Guide")

    st.markdown(
        """
        This section explains the main terms used in ANCHOR and how the final
        **ANCHOR Priority Score** is created.
        """
    )

    st.info(
        "The ANCHOR Priority Score is a relative ranking tool. Higher scores suggest communities that may warrant closer review.",
    )

    st.markdown("### What goes into the ANCHOR Priority Score?")

    st.markdown(
        """
        The score is built from three main pieces:

        1. **Access Gap**  
           Measures where overdose burden is high but in-town harm reduction support listings are limited.

        2. **Social Vulnerability**  
           Uses CDC/ATSDR Social Vulnerability Index data to adjust the score upward for communities with higher structural vulnerability.

        3. **Distance Access**  
           Adjusts the score downward when a municipality has nearby source-listed services within approximately 5 miles, even if those services are outside the municipal boundary.
        """
    )

    st.markdown("### Score breakdown")

    st.markdown("#### 1. Harm Reduction Access Gap Score")

    st.markdown(
        """
        The Harm Reduction Access Gap Score starts with overdose burden and compares it with in-town service access.
        """
    )

    st.latex(
        r"""
        \text{Harm Reduction Access Gap Score}
        =
        \text{Overdose Burden}
        \times
        (1 - \text{In-Town Service Access})
        """
    )

    st.markdown(
        """
        **Overdose burden** combines overdose deaths and opioid-related EMS incidents.  
        **In-town service access** is based on how many tracked service categories are listed inside the municipality.
        """
    )

    st.markdown("#### 2. SVI-Adjusted Score")

    st.markdown(
        """
        The Harm Reduction Access Gap Score is then adjusted using social vulnerability.
        """
    )

    st.latex(
        r"""
        \text{SVI-Adjusted Score}
        =
        \text{Harm Reduction Access Gap Score}
        \times
        (1 + \text{Social Vulnerability})
        """
    )

    st.markdown(
        """
        This increases the score for municipalities with higher social vulnerability.
        """
    )

    st.markdown("#### 3. ANCHOR Priority Score")

    st.markdown(
        """
        Finally, the score is adjusted for nearby service access.
        """
    )

    st.latex(
        r"""
        \text{ANCHOR Priority Score}
        =
        \text{SVI-Adjusted Score}
        \times
        (1 - 0.35 \times \text{Nearby Access})
        """
    )

    st.markdown(
    """
    The **0.35 nearby-access weight** means nearby services can reduce the score by up to 35%,
    but they cannot erase it. Nearby services may improve access, but they do not fully account
    for transportation barriers, eligibility, hours, capacity, stigma, or whether people can
    realistically use those services.
    """
)

    st.markdown("### Priority levels")

    st.markdown(
        """
        Priority levels are based on the final ANCHOR Priority Score:

        - **Very high priority:** top 10% of municipalities
        - **High priority:** 75th to 90th percentile
        - **Moderate priority:** 50th to 75th percentile
        - **Lower priority:** below the 50th percentile
        """
    )

    st.markdown("### Important note")

    st.warning(
        "Zero in-town listings does not mean a municipality has no services. "
        "It means no source-listed records from the tracked datasets were identified inside that municipality.",
    )

    st.markdown(
        """
        ANCHOR uses source-listed service records, approximate ZIP-code centroid distances, overdose death data,
        EMS incident data, and social vulnerability data. It should be used to guide further review, not as a complete service inventory.
        """
    )

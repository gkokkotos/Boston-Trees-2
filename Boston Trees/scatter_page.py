"""
Name: Grace Kokkotos
Date: 2025-11-23
Description: Scatterplot of tree diameter by neighborhood in Boston
"""

import streamlit as st
import plotly.express as px
from utils import load_data, clean_data

def setup_scatter_neighborhood_page():
    st.title("Tree Diameter by Neighborhood")

    df = load_data()
    if df.empty:
        st.warning("No data available.")
        return None

    df = clean_data(df)

    # Ensure there are valid diameters
    df = df[df['dbh_in'].notna()]
    if df.empty:
        st.warning("No valid diameter data available.")
        return None

    # Sidebar filters
    st.sidebar.header("Filters")

    # Neighborhood filter
    neighborhood_options = sorted(df["neighborhood"].dropna().unique())
    selected_neighborhood = st.sidebar.multiselect(
        "Select Neighborhood",
        options=neighborhood_options,
        default=neighborhood_options[:5]  # show first 5 by default
    )

    # Species filter (optional)
    species_options = sorted(df["species_common"].dropna().unique())
    selected_species = st.sidebar.multiselect(
        "Select Species (optional)",
        options=species_options
    )

    # Diameter filter
    min_diameter = float(df["dbh_in"].min())
    max_diameter = float(df["dbh_in"].max())
    selected_diameter = st.sidebar.slider(
        "Filter by Diameter (inches)",
        min_value=min_diameter,
        max_value=max_diameter,
        value=(min_diameter, max_diameter)
    )

    # Apply filters
    df_filtered = df.copy()
    if selected_neighborhood:
        df_filtered = df_filtered[df_filtered["neighborhood"].isin(selected_neighborhood)]
    if selected_species:
        df_filtered = df_filtered[df_filtered["species_common"].isin(selected_species)]
    df_filtered = df_filtered[
        (df_filtered["dbh_in"] >= selected_diameter[0]) &
        (df_filtered["dbh_in"] <= selected_diameter[1])
    ]

    st.sidebar.markdown(f"**Rows after filtering:** {len(df_filtered)}")

    return df_filtered

def create_scatter_neighborhood(df_filtered):
    if df_filtered is None or df_filtered.empty:
        st.warning("No data to display.")
        return

    # Plotly scatter
    fig = px.scatter(
        df_filtered,
        x="neighborhood",
        y="dbh_in",
        color="species_common",
        labels={"dbh_in": "Diameter (inches)", "neighborhood": "Neighborhood", "species_common": "Species"},
        title="Tree Diameter by Neighborhood",
        hover_data=["park_name", "street_name"]
    )

    fig.update_traces(marker=dict(size=7, line=dict(width=0.2)))
    st.plotly_chart(fig, use_container_width=True)

def scatter_page():
    df_filtered = setup_scatter_neighborhood_page()
    create_scatter_neighborhood(df_filtered)
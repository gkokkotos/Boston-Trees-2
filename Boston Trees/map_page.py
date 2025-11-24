"""
Name: Grace Kokkotos
Date:
Description: Map page showing Boston trees using PyDeck
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
from utils import load_data, clean_data

def setup_map_page():
    st.title("Boston Trees Map")

    df = load_data()
    if df.empty:
        st.warning("No data available to display.")
        return pd.DataFrame()

    df = clean_data(df)

    # Sidebar filters
    st.sidebar.header("Filters")

    # Species (common name)
    species_options = sorted(df["species_common"].dropna().unique()) if "species_common" in df.columns else []
    selected_species = st.sidebar.multiselect("Select Species", species_options)

    # Neighborhood
    neighborhood_options = sorted(df["neighborhood"].dropna().unique()) if "neighborhood" in df.columns else []
    selected_neighborhood = st.sidebar.multiselect("Select Neighborhood", neighborhood_options)

    # Diameter filter
    min_diameter = int(df["dbh_in"].min()) if "dbh_in" in df.columns else 0
    max_diameter = int(df["dbh_in"].max()) if "dbh_in" in df.columns else 100
    selected_diameter = st.sidebar.slider("Diameter (inches)", min_value=min_diameter, max_value=max_diameter, value=(min_diameter, max_diameter))

    # Street name
    street_options = sorted(df["street_name"].dropna().unique()) if "street_name" in df.columns else []
    selected_street = st.sidebar.multiselect("Street Name", street_options)

    # Apply filters
    df_filtered = df.copy()
    if selected_species:
        df_filtered = df_filtered[df_filtered["species_common"].isin(selected_species)]
    if selected_neighborhood:
        df_filtered = df_filtered[df_filtered["neighborhood"].isin(selected_neighborhood)]
    if "dbh_in" in df_filtered.columns:
        df_filtered = df_filtered[(df_filtered["dbh_in"] >= selected_diameter[0]) & (df_filtered["dbh_in"] <= selected_diameter[1])]
    if selected_street:
        df_filtered = df_filtered[df_filtered["street_name"].isin(selected_street)]

    st.sidebar.markdown(f"**Rows after filtering:** {len(df_filtered)}")

    return df_filtered


def create_tree_map(df_filtered, max_points=3000):
    if df_filtered.empty:
        st.warning("No points to display.")
        return

    # Ensure lat/lon exist
    if "lat" not in df_filtered.columns or "lon" not in df_filtered.columns:
        st.error("No latitude/longitude columns available to display map.")
        return

    df_filtered = df_filtered.copy()

    # Identify the top 10 most common species
    top_species = (
        df_filtered["species_common"]
        .value_counts()
        .head(10)
        .index
    )

    # Build a simple color palette (10 distinct colors)
    colors = [
        [230, 25, 75], [60, 180, 75], [255, 225, 25], [0, 130, 200],
        [245, 130, 48], [145, 30, 180], [70, 240, 240], [240, 50, 230],
        [210, 245, 60], [250, 190, 190]
    ]

    # Map species → color
    color_map = {species: colors[i] for i, species in enumerate(top_species)} # creating dictionary

    # All other species = gray
    default_color = [180, 180, 180]

    # Assign color BEFORE sampling
    df_filtered["color"] = df_filtered["species_common"].apply(  # using lambda function
        lambda s: color_map.get(s, default_color)
    )

    # Limit number of points for performance
    df_sample = df_filtered.sample(n=min(max_points, len(df_filtered)), random_state=42)

    # PyDeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_sample,
        get_position='[lon, lat]',
        get_radius=30,
        get_fill_color='color',
        pickable=True,
        auto_highlight=True
    )

    # Initial view centered on Boston
    view_state = pdk.ViewState(
        latitude=df_sample['lat'].median(),
        longitude=df_sample['lon'].median(),
        zoom=11,
        pitch=40
    )

    tooltip = {
        "html": "<b>Species:</b> {species_common}<br/><b>DBH:</b> {dbh_in}<br/><b>Street:</b> {street_name}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)

    st.pydeck_chart(deck)


def map_page():
    df_filtered = setup_map_page()
    if not df_filtered.empty:
        create_tree_map(df_filtered)
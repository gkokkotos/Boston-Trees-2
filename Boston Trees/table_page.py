"""
Name: Grace Kokkotos
Date:
Description: Interactive table page for Boston Trees Explorer
"""

import streamlit as st
from utils import load_data, clean_data, rename_columns_for_display

def apply_table_filters(df):
    st.sidebar.header("Filters")

    # Species filter
    species_options = sorted(df["species_common"].dropna().unique()) if "species_common" in df.columns else [] # ITERLOOP iterates implicitly in unique() and sorted()
    selected_species = st.sidebar.multiselect("Select Species", species_options)

    # Neighborhood filter
    neighborhood_options = sorted(df["neighborhood"].dropna().unique()) if "neighborhood" in df.columns else [] # ITERLOOP
    selected_neighborhood = st.sidebar.multiselect("Select Neighborhood", neighborhood_options)

    # Diameter filter
    min_diameter = int(df["dbh_in"].min()) if "dbh_in" in df.columns else 0
    max_diameter = int(df["dbh_in"].max()) if "dbh_in" in df.columns else 100
    selected_diameter = st.sidebar.slider(
        "Diameter (inches)",
        min_value=min_diameter,
        max_value=max_diameter,
        value=(min_diameter, max_diameter)
    )

    # Street name filter
    street_options = sorted(df["street_name"].dropna().unique()) if "street_name" in df.columns else [] # ITERLOOP
    selected_street = st.sidebar.multiselect("Street Name", street_options)

    # Apply filters
    df_filtered = df.copy()

    if selected_species:
        df_filtered = df_filtered[df_filtered["species_common"].isin(selected_species)]

    if selected_neighborhood:
        df_filtered = df_filtered[df_filtered["neighborhood"].isin(selected_neighborhood)]

    if "dbh_in" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["dbh_in"] >= selected_diameter[0]) &
            (df_filtered["dbh_in"] <= selected_diameter[1])
        ]

    if selected_street:
        df_filtered = df_filtered[df_filtered["street_name"].isin(selected_street)]

    # Show result count
    st.sidebar.markdown(f"**Rows after filtering:** {len(df_filtered)}")

    return df_filtered

def table_page():
    st.title("Interactive Boston Trees Table")

    # Load and clean data
    df = load_data() # called in multiple pages (main page & this page)
    if df.empty:
        st.warning("No data available to display.")
        return
    df = clean_data(df) # called in multiple pages

    # Apply filters
    df_filtered = apply_table_filters(df)

    # Display the filtered table
    st.subheader("Filtered Trees Data")
    df_display = rename_columns_for_display(df_filtered)
    st.dataframe(df_display, height=500, use_container_width=True)
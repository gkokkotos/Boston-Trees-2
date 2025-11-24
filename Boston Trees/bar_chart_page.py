"""
Name: Grace Kokkotos
Date:
Description: Bar chart page showing the top 30 tree species in Boston (no filters)
"""

import streamlit as st
import plotly.express as px
from utils import load_data, clean_data
import matplotlib.cm as cm
import numpy as np

# Creates bar chart of top 30 tree species with a color gradiant
def create_bar_chart(df, top_n=30):
    if df.empty:
        st.warning("No data available to create chart.")
        return

    # Compute top N species
    top_species_counts = df["species_common"].value_counts().nlargest(top_n).reset_index()
    top_species_counts.columns = ["species", "count"]

    # gets evenly spaced colors for the gradiant
    cmap = cm.get_cmap('viridis', top_n)
    # Makes colors plotly compatible
    colors = [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b, _ in cmap(np.arange(top_n))] # list comprehension

    top_species_counts["color"] = colors

    # Plotly horizontal bar chart
    fig = px.bar(
        top_species_counts,
        x="count",
        y="species",
        orientation="h",
        labels={"count": "Number of Trees", "species": "Species"},
        title=f"Top {top_n} Tree Species in Boston",
        text="count",
        # use the interpolated colors
        color="color",
        # tells Plotly to use the exact color values
        color_discrete_map="identity"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),  # largest on top
        margin=dict(l=150, r=20, t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)


def bar_chart_page():
    st.title("Top Tree Species in Boston")
    df = load_data()
    if df.empty:
        st.warning("No data available.")
        return
    df = clean_data(df)

    create_bar_chart(df)
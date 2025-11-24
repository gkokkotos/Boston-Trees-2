"""
Name: Grace Kokkotos
CS230: Section 230-8
Data: Boston Parks and Recreation Division Trees
URL: Link to your web application on Streamlit Cloud (if posted)

Description: This program used a main python file that calls upon and runs supporting python files that make pages in the streamlit function.
The main page sets the setup of the streamlit website, creates the page selector on the sidebar, and runs the other pages it the specific page is selected.
The utility page (utils.py) imports and cleans the data using pandas as well as renames the columns for display in the charts.
The Table page makes a table using the bprd data and used sidebar filters to interact with it
The map page creates an interactive map with filters in the sidebar
The bar chart page creates a bar chart showing the top 30 tree species in Boston
The scatter plot page creates a scatterplot showing the diameters if trees in specific neighborhoods


References:

(and links to any websites or external tutorials you may have used)

"""

# Imports
import streamlit as st
from table_page import table_page
from map_page import map_page
from bar_chart_page import bar_chart_page
from scatter_page import scatter_page

# Set up page title and layout (only once)
st.set_page_config(
    page_title="Boston Trees Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar page selector
page = st.sidebar.selectbox("Select Page", ["Home", "Interactive Table", "Map of Trees", "Top 30 Trees Chart", "Diameter by Neighborhood"])

# Home Page
if page == "Home":
    st.title("Welcome to Boston Trees Explorer")
    st.write(
        "This interactive dashboard shows Boston street & park trees.\n"
        "Use the sidebar to navigate to different pages."
    )
# call the function from table_page.py
elif page == "Interactive Table":
    table_page()
# call the function from map_page.py
elif page == "Map of Trees":
    map_page()
# call the function from bar_chart_page.py
elif page == "Top 30 Trees Chart":
    bar_chart_page()
# call the function from scatter_page.py
elif page == "Diameter by Neighborhood":
    scatter_page()

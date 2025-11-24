"""
Name: Grace
Date:
Description: will help the rest of the pages in streamlit run
"""

import pandas as pd

# Constant
TREE_DATA = "bprd_trees.csv"


# Load the data
def load_data(url=TREE_DATA, nrows=None): # Function with 2 parameters, one default value
    # try reading with pandas
    try:
        df = pd.read_csv(url, nrows=nrows)
        return df # return value
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return pd.DataFrame()


# Clean the data so its more readable
def clean_data(df):
    if df.empty:
        return df

    # Normalize column names
    df.columns = df.columns.str.lower()

    # Rename columns to readable names
    df.rename(columns={
        "id": "tree_id",
        "spp_com": "species_common",
        "spp_bot": "species_botanical",
        "numberof_st": "num_stems",
        "dbh_range": "dbh_range",
        "dbh": "dbh_in",
        "date_plant": "date_planted",
        "neighborhood": "neighborhood",
        "park": "park_name",
        "os_id": "park_id",
        "address": "street_number",
        "street": "street_name",
        "suffix": "suffix",
        "x_longitude": "lon",
        "y_latitude": "lat"
    }, inplace=True) # using dictonary inside rename()

    # Convert numeric columns
    df["dbh_in"] = pd.to_numeric(df["dbh_in"], errors="coerce")
    df["num_stems"] = pd.to_numeric(df["num_stems"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")

    # Convert date columns
    if "date_planted" in df.columns:
        df["date_planted"] = pd.to_datetime(df["date_planted"], errors="coerce")

    # Drop rows without valid coordinates
    df = df.dropna(subset=["lat", "lon"])

    # Strip extra spaces in species names
    df["species_common"] = df["species_common"].str.strip()

    return df

# makes the column names better
def rename_columns_for_display(df):
    # to make better column names
    return df.rename(columns={
        "tree_id": "Tree ID",
        "species_common": "Species Common",
        "species_botanical": "Species Botanical",
        "num_stems": "Number of Stems",
        "dbh_range": "Diameter Range (in)",
        "dbh_in": "Diameter (in)",
        "date_planted": "Date Planted",
        "neighborhood": "Neighborhood",
        "park_name": "Park Name",
        "park_id": "Park ID",
        "street_number": "Street Number",
        "street_name": "Street Name",
        "lon": "Longitude",
        "lat": "Latitude"
    }) # using dictonary inside rename()
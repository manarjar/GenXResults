import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re



import streamlit as st
import helpers
import pandas as pd
import numpy as np
import os
helpers.create_resource_list()


def read_capacity():
    file_path = "results/capacity.csv"  # Replace with your CSV file path
    df_capacity = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_capacity = pd.read_csv(file_path)
            df_capacity.set_index("Resource", inplace=True)
            df_capacity = df_capacity.round(5)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_capacity

st.markdown("# Capacity by resource type")

df_resources = pd.read_csv("inputs/resource_list.csv")

selected_type = st.selectbox(
    label="Select resource type to view CO2 emissions",
    options = df_resources["Type"].unique())

selected_zone = st.selectbox(
    label="Select zone",
    options = df_resources["Zone"].unique())

resources_list = df_resources[(df_resources.Type == selected_type) & (df_resources.Zone == selected_zone)]


df_capacity = read_capacity()
df_capacity = df_capacity.merge(resources_list[["Resource"]], how='inner', on="Resource")
df_capacity.reset_index(inplace=True, drop=True)

#Create a new row with sum of numeric columns and NaN for string columns
sum_row = df_capacity.select_dtypes(include=[np.number]).sum().reindex(df_capacity.columns, fill_value='')

# Add the sum row to the DataFrame
df_capacity.loc['Total'] = sum_row

st.dataframe(df_capacity)
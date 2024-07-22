import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import yaml

####################################################
### HELPER FUNCTIONS
####################################################

def read_costs():
    file_path = "results\costs.csv"  # Replace with your CSV file path
    df_costs = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_costs = pd.read_csv(file_path)
            df_costs = df_costs.round(5)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_costs.round(3)


def read_net_revenue():
    file_path = "results/NetRevenue.csv"  # Replace with your CSV file path
    df_revenue = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_revenue = pd.read_csv(file_path)
            df_revenue = df_revenue.round(5)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_revenue


st.markdown("## Costs")
st.dataframe(read_costs(), hide_index=True, use_container_width=True)

st.markdown("## Net Revenue")
df_resources = pd.read_csv("inputs/resource_list.csv")

selected_type = st.selectbox(
    label="Select resource type",
    options = df_resources["Type"].unique())

selected_zone = st.selectbox(
    label="Select zone",
    options = df_resources["Zone"].unique())

resources_list = df_resources[(df_resources.Type == selected_type) & (df_resources.Zone == selected_zone)]

df_net_revenue = read_net_revenue().merge(resources_list, on="Resource", how='inner')
df_net_revenue = df_net_revenue[["Resource", "Revenue", "Cost"]]


# Create the Altair chart
df_melted = df_net_revenue.melt(id_vars='Resource', var_name='Category', value_name='Amount')
# Create the Altair chart
chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X('Resource:N', axis=alt.Axis(labelAngle=-80, title='Resource')),
    y=alt.Y('Amount', axis=alt.Axis(title='$')),
    color=alt.Color('Category:N', scale=alt.Scale(domain=['Revenue', 'Cost'])),
    xOffset='Category:N'  # This creates the side-by-side bars
).properties(
    width=alt.Step(20)  # Adjust the width of the bars
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta

st.markdown("# Load Analysis")

df_demand = pd.read_csv("results/power_balance_markets.csv")
prefixes = ["Nonserved_Energy", "Demand"]

# Select columns that start with any of the given prefixes
df_demand = df_demand.filter(regex=f'^({"|".join(prefixes)})')

#df_power_balance["Time"] = range(1,df_power_balance.shape[0]+1)
# Get the region IDs from the first row
zone_ids = df_demand.iloc[0]
# Create a dictionary to store the split DataFrames
split_dfs = {}

# Iterate through unique region IDs
for zone in zone_ids.unique():
    # Create a boolean mask for columns with this region ID
    mask = zone_ids == zone
    
    # Select columns for this region and remove the first row
    zone_df = df_demand.loc[:, mask].iloc[2:].reset_index(drop=True)
    
    # Rename columns to remove region ID
    new_col_names = {col: f"{re.match(r'^[a-zA-Z_]+', col).group(0)}" for col in zone_df.columns}
    zone_df.rename(columns = new_col_names, inplace=True)
    cols = zone_df.columns
    zone_df["Time"] = range(1,zone_df.shape[0]+1)
    zone_df["Demand"] = zone_df["Demand"] *-1
    # Store the DataFrame in the dictionary
    split_dfs[int(zone)] = zone_df
    
options_list = zone_ids.unique().astype(int).astype(str)
selected_zone = st.selectbox(
    label = "Select zone",
    options = options_list   
)
selected_zone = int(selected_zone)

temp_df = split_dfs[selected_zone]



# Create a datetime slider with custom format and options
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
 
selected_date = st.slider(
    "Select a date range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, datetime(2024, 1, 31)),
    step=timedelta(days=1),
    format="MM/DD/YYYY")

time_range=np.zeros(2, dtype=int)
time_range[0] = (selected_date[0].timetuple().tm_yday - 1)*24 + 1
time_range[1] = selected_date[1].timetuple().tm_yday * 24

df = temp_df[time_range[0]:time_range[1]]

df_melted = df.melt(id_vars=['Time'], value_vars = cols, 
                                      value_name='Value' ,
                                      var_name="Metric"      )


chart = (alt.Chart(df_melted).mark_bar().encode(
        x='Time',
        y='Value',
        color='Metric'
    ))

st.altair_chart(chart, use_container_width=True)


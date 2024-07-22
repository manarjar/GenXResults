import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os

def read_file(file_path):
    df = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            st.markdown(f"An error occurred while reading file {file_path}: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")      
    return df.round(3)

st.markdown("# Power Balance Analysis")

df_power_balance = read_file("results/power_balance_markets.csv")
df_power_balance.drop(columns=["BalanceComponent"], inplace=True)

#df_power_balance["Time"] = range(1,df_power_balance.shape[0]+1)
# Get the region IDs from the first row
zone_ids = df_power_balance.iloc[0]
# Create a dictionary to store the split DataFrames
split_dfs = {}

# Iterate through unique region IDs
for zone in zone_ids.unique():
    # Create a boolean mask for columns with this region ID
    mask = zone_ids == zone
    
    # Select columns for this region and remove the first row
    zone_df = df_power_balance.loc[:, mask].iloc[2:].reset_index(drop=True)
    
    # Rename columns to remove region ID
    new_col_names = {col: f"{re.match(r'^[a-zA-Z_]+', col).group(0)}" for col in zone_df.columns}
    zone_df.rename(columns = new_col_names, inplace=True)
    cols = zone_df.columns
    #zone_df["Transmission_NetExport"] *= -1
    zone_df["Time"] = range(1,zone_df.shape[0]+1)

    # Store the DataFrame in the dictionary
    split_dfs[int(zone)] = zone_df
    
options_list = zone_ids.unique().astype(int).astype(str)
selected_zone = st.selectbox(
    label = "Select zone",
    options = options_list   
)
selected_zone = int(selected_zone)


selected_attributes1 = st.multiselect(label = "Select attributes to plot", default=cols[0], options = cols)
selected_attributes2 = selected_attributes1 + ["Time"]
temp_df = split_dfs[selected_zone][selected_attributes2]



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

df_melted = df.melt(id_vars=['Time'], value_vars = selected_attributes1, 
                                      value_name='Value' ,
                                      var_name="Metric"      )


chart = (alt.Chart(df_melted).mark_bar().encode(
        x='Time',
        y=alt.Y('Value', stack=True),
        color='Metric',
        order=alt.Order(
        # Sort the segments of the bars by this field
        'Metric',
        sort='ascending'
    )
    )).interactive()

st.altair_chart(chart, use_container_width=True)


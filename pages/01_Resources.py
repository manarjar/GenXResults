import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import re
from datetime import datetime, timedelta

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




st.markdown("""# Resources """)

### 1. Read input files
df_resources = read_file("inputs/resource_list.csv")

df_power = read_file("results/power.csv")
df_power=df_power.iloc[2:]
df_power.reset_index(drop=True, inplace=True)

df_capacity = read_file("results/capacity.csv")
df_capacity.set_index("Resource", inplace=True)

df_crtailment = read_file("results/market_curtailment.csv")

df_variability = read_file("inputs/system/Generators_variability.csv")

### 2. Filter resources
selected_type = st.selectbox(
    label="Select resource type to view CO2 emissions",
    options = df_resources["Type"].unique())

selected_zone = st.selectbox(
    label="Select zone",
    options = df_resources["Zone"].unique())

resources_list = df_resources.Resource[(df_resources.Type == selected_type) & (df_resources.Zone == selected_zone)]

selected_resource = st.selectbox(
    label="Slect a resource to model its generation",
    options = resources_list,
)

# Create a datetime slider with custom format and options
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
 
selected_date = st.slider(
    "Select a date range",
    min_value= start_date,
    max_value= end_date,
    value=(start_date, datetime(2024, 1, 31)),
    step=timedelta(days=1),
    format="MM/DD/YYYY")


time_range=np.zeros(2, dtype=int)
time_range[0] = (selected_date[0].timetuple().tm_yday - 1)*24 + 1
time_range[1] = selected_date[1].timetuple().tm_yday * 24

### Plot resurce variability
st.markdown("### Resource variability")
df_variability = df_variability[selected_resource]
df_variability = df_variability[time_range[0]:time_range[1]]
st.line_chart(df_variability,x_label="Hour", y_label="Variability (%)", use_container_width=True)

### Plot other characteristics
st.markdown("### Resource Generation")

df_resource_info = pd.DataFrame({'Power':df_power[selected_resource]})
df_resource_info["Capacity"] = df_capacity['EndCap'][selected_resource]
if selected_resource in df_crtailment.columns:
    df_resource_info["Curtailment"] = df_crtailment[selected_resource]
else:
    df_resource_info["Curtailment"] = 0

df_resource_info = df_resource_info[time_range[0]:time_range[1]]


st.line_chart(df_resource_info) #, color = ['#00ff00', '#ff0000']  [["Capacity","Power", "Curtailment"]]
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
st.write("""# GenX Results Analysis """)

# Read power values and preview them
df_power = pd.read_csv("results/power.csv")
df_capacity = pd.read_csv("results/capacity.csv")
df_market_sales = pd.read_csv('results/market_sales.csv')

nrows = df_power.shape[0]
df_power = df_power.iloc[2:nrows]
df_power.reset_index(drop=True, inplace=True)
df_power.drop(columns=["Total", "Resource"], axis =1, inplace=True)

resource_list = list(df_power.columns)



nrows = df_capacity.shape[0]
df_capacity = df_capacity[['Resource', 'EndCap']]
df_capacity = df_capacity.iloc[0:nrows-1]

selected_resource = st.selectbox(
    label="Slect a resource to model its generation",
    options = [f"{i+1}- {resource_list[i]}" for i in range(len(resource_list))],
    placeholder="Choose a resource" 
)

# start_time = st.number_input(label="Enter starting time",min_value=1, max_value=nrows)
# end_time = st.number_input(label="Enter starting time",min_value=1, max_value=nrows)
# st.slider()

time_range = st.slider(
    label= "Select time range",
    min_value= 1,
    max_value= 8760, 
    value=(1, 24),
    step=1)


rid = int(re.search(r'\d+', selected_resource).group())-1
time = 168
df_resource_info = pd.DataFrame({'Power':df_power[resource_list[rid]]})
df_resource_info["Capacity"] = df_capacity.iloc[rid]["EndCap"]
df_resource_info["Sales"] = df_market_sales[resource_list[rid]]
df_resource_info = df_resource_info[time_range[0]:time_range[1]]
df_resource_info["Time"] = range(1,df_resource_info.shape[0]+1)
df_resource_info.set_index("Time", inplace=True)

st.line_chart(df_resource_info[["Capacity","Power", "Sales"]]) #, color = ['#00ff00', '#ff0000']
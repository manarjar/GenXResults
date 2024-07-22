import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from datetime import datetime, timedelta

def read_Fuel_cost_plant():
    file_path = "results/Fuel_cost_plant.csv"  # Replace with your CSV file path
    df_fuel = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_fuel = pd.read_csv(file_path)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_fuel


def read_plant_fuel_consumption():
    file_path = "results/FuelConsumption_plant_MMBTU.csv"  # Replace with your CSV file path
    df_fuel = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_fuel = pd.read_csv(file_path)

        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_fuel

def read_total_fuel_consumption():
    file_path = "results/FuelConsumption_total_MMBTU.csv"  # Replace with your CSV file path
    df_fuel = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_fuel = pd.read_csv(file_path)

        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_fuel

st.markdown("# Fuel cost and consumption")

df_resource_fuel = read_Fuel_cost_plant()
df_fuel_consumption = read_plant_fuel_consumption()
df_total_fuel_consumption = read_total_fuel_consumption()

st.markdown("## Fuel Consumption Summary")

df_fuel_total_cost = df_resource_fuel.groupby('Fuel')['AnnualSumCosts'].sum().reset_index()
df_total_fuel_consumption = df_total_fuel_consumption.merge(df_fuel_total_cost, how = "left", on = "Fuel")
df_total_fuel_consumption.rename(columns={"AnnualSum": "Annual Consumption", "AnnualSumCosts": "Annual Cost"}, inplace = True)
st.dataframe(df_total_fuel_consumption, hide_index= True, use_container_width= True)

st.markdown("## Detailed Fuel Consumption ")
selected_type = st.selectbox(
    label="Select fuel type",
    options = df_resource_fuel["Fuel"].unique())

selected_zone = st.selectbox(
    label="Select zone",
    options = df_resource_fuel["Zone"].unique())

resource_list = df_resource_fuel.Resource[(df_resource_fuel.Fuel == selected_type) & (df_resource_fuel.Zone == selected_zone)]

df_fuel_consumption = df_fuel_consumption[resource_list]

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

df_fuel_consumption = df_fuel_consumption[time_range[0]:time_range[1]]




st.line_chart(df_fuel_consumption) #, color = ['#00ff00', '#ff0000']
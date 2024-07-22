import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import yaml


def read_co2_cap_policy():
    file_path = "inputs/policies/CO2_cap.csv"  # Replace with your CSV file path
    df_co2_policy = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_co2_policy = pd.read_csv(file_path)
            df_co2_policy = df_co2_policy.round(5)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")   
    
    return df_co2_policy


def read_co2_cap_penalties():
    file_path = "results/CO2_prices_and_penalties.csv"  # Replace with your CSV file path
    df_co2_penalties = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_co2_penalties = pd.read_csv(file_path)
            df_co2_penalties = df_co2_penalties.round(5)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")

    return df_co2_penalties


def read_co2_emissions():
    file_path = "results/emissions.csv"  # Replace with your CSV file path
    df_co2_emissions = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_co2_emissions = pd.read_csv(file_path)
            df_co2_emissions = df_co2_emissions.round(5)
            df_co2_emissions = df_co2_emissions.iloc[2:].reset_index(drop=True)
            df_co2_emissions.drop(columns=["Zone","Total"], inplace=True)
            df_co2_emissions.rename(columns=lambda x: f"Zone_{x}", inplace=True)
            df_co2_emissions["Time"] = range(1,df_co2_emissions.shape[0]+1)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")

    return df_co2_emissions

def read_co2_emissions_plant():
    file_path = "results/emissions_plant.csv"  # Replace with your CSV file path
    df_co2 = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_co2 = pd.read_csv(file_path)
            df_co2 = df_co2.round(5)
            df_co2 = df_co2.iloc[2:].reset_index(drop=True)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")

    return df_co2


file_path_settings = "inputs/settings/genx_settings.yml" 


with open(file_path_settings, 'r') as file:
    settings = yaml.safe_load(file)

st.markdown("# CO2 policies and penalties")

if ("CO2Cap" in settings.keys()) & (settings["CO2Cap"] == 1):
    st.markdown("### CO2 policies")
    st.dataframe(read_co2_cap_policy(), use_container_width=True, hide_index=True)

    st.markdown("### CO2 prices and penalties")
    st.dataframe(read_co2_cap_penalties(), use_container_width=True, hide_index=True)

    # st.markdown("### CO2 emissions by zone")
    # chart = ( alt.Chart(read_co2_emissions())
    # .mark_line()
    # .encode(x_label="Hour", y_label="tonne CO2")
    # )
    df_co2_emissions = read_co2_emissions()
    df_co2_emissions_melt = df_co2_emissions.melt("Time", var_name="Zone", value_name="Co2 emission")

    chart = alt.Chart(df_co2_emissions_melt).mark_line().encode(
        x=alt.X('Time', axis=alt.Axis(title='Hour')),
        y=alt.Y('Co2 emission', axis=alt.Axis(title='CO2 tonne')),
        color=alt.Color('Zone:N', legend=alt.Legend(title="Zone"))
    ).properties(
        title='CO2 emissions'   
    )
    st.altair_chart(chart, use_container_width=True)


    ####### resource emissions by region df_resources = pd.read_csv("inputs/resource_list.csv")
    st.markdown("## CO2 emissions by plant")
    df_resources = pd.read_csv("inputs/resource_list.csv")

    selected_type = st.selectbox(
        label="Select resource type to view CO2 emissions",
        options = df_resources["Type"].unique())
    
    selected_zone = st.selectbox(
        label="Select zone",
        options = df_resources["Zone"].unique())
    
    resources_list = df_resources.Resource[(df_resources.Type == selected_type) & (df_resources.Zone == selected_zone)]

    df_emissions_plant = read_co2_emissions_plant()
    df_emissions_plant = df_emissions_plant[resources_list]
    df_emissions_plant["Time"] = range(1, df_emissions_plant.shape[0]+1)

    df_emissions_plant_melt = df_emissions_plant.melt("Time", var_name="Resource", value_name="Co2 emission")

    
    chart2 = alt.Chart(df_emissions_plant_melt).mark_line().encode(
        x=alt.X('Time', axis=alt.Axis(title='Hour')),
        y=alt.Y('Co2 emission', axis=alt.Axis(title='CO2 tonne')),
        color=alt.Color('Resource:N', legend=alt.Legend(title="Resource"))
    ).properties(
        title='CO2 emissions per resource'   
    )
    st.altair_chart(chart2, use_container_width=True)
    
else:
    st.markdown("### CO2 Cap is deactivated in settings file")
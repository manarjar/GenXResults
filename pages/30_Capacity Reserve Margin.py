import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import yaml

#####################################
##         Helper Functions        ##
#####################################

def read_cap_res_margin_inputs():
    file_path = "inputs/policies/Capacity_reserve_margin.csv"  # Replace with your CSV file path
    df_cap_res_margin_input = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_cap_res_margin_input = pd.read_csv(file_path)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")
    
    return df_cap_res_margin_input



def read_annual_cap_res_margin():
    file_path = "results/ReserveMargin_w.csv"  # Replace with your CSV file path
    df_cap_res_margin_results = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_cap_res_margin_results = pd.read_csv(file_path)
            df_cap_res_margin_results = df_cap_res_margin_results.round(5)
            df_cap_res_margin_results.drop(columns=["Constraint"], inplace=True)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")

    return df_cap_res_margin_results


#####################################
##            Page Code            ##
#####################################
file_path_settings = "inputs/settings/genx_settings.yml" 
# Open the file and load the YAML content
with open(file_path_settings, 'r') as file:
    settings = yaml.safe_load(file)

st.markdown("# Capacity Reserve Margin")

if ("CapacityReserveMargin" in settings.keys()) & (settings["CapacityReserveMargin"]==1):
    st.dataframe(read_cap_res_margin_inputs(), use_container_width=True, hide_index=True)

    st.markdown("### Shadow prices of the capacity reserve margin constraints")
    df_annual_cap_res_margin = read_annual_cap_res_margin()
    st.line_chart(data=df_annual_cap_res_margin, x_label="Hour")
else:
    st.markdown("### Capacity reserve margin is deactivated in settings file")
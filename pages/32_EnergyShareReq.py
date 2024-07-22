import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import helpers
import yaml


def read_esr_results():
    file_path = "results/ESR_prices_and_penalties.csv"  # Replace with your CSV file path
    df_esr_results = pd.DataFrame()
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            st.markdown("### ESR prices and penalties")
            df_esr_results = pd.read_csv(file_path)
            df_esr_results = df_esr_results.round({"ESR_Price":5, "ESR_AnnualSlack":5, "ESR_AnnualPenalty": 5})
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")
    else:
        st.markdown(f"The file {file_path} does not exist.")

    return df_esr_results


file_path_settings = "inputs/settings/genx_settings.yml" 
# Open the file and load the YAML content
with open(file_path_settings, 'r') as file:
    settings = yaml.safe_load(file)

if ("EnergyShareRequirement" in settings.keys()) & (settings["EnergyShareRequirement"] == 1):
    st.dataframe(read_esr_results(), use_container_width=True)
else:
    st.markdown("### EnergyShareRequirement is deactivated in settings file")
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import helpers
import yaml
############################
##      Helper Functions  ##
############################
def policy_maxcapreq():
    file_path_settings = "inputs\settings\genx_settings.yml"  
    df_maxcapreq_input = pd.DataFrame()
    df_maxcapreq_results = pd.DataFrame()
    
    # Open the file and load the YAML content
    with open(file_path_settings, 'r') as file:
        settings = yaml.safe_load(file)

    if 'MaxCapReq' in settings.keys():
        file_path_input = "inputs\policies\Maximum_capacity_requirement.csv"  # Replace with your CSV file path
        if os.path.isfile(file_path_input):
            # File exists, so read it
            try:
                df_maxcapreq_input = pd.read_csv(file_path_input)
                df_maxcapreq_input.iloc[:,0] = "MaxCapReq_"+df_maxcapreq_input.iloc[:,0].astype(str)
                df_maxcapreq_input.rename(columns={"MaxCapReqConstraint":"Constraint"}, inplace = True)
            except Exception as e:
                st.markdown(f"An error occurred while reading the file: {e}")

        file_path_results = "results/MaxCapReq_prices_and_penalties.csv"  # Replace with your CSV file path
        if os.path.isfile(file_path_results):
            # File exists, so read it
            try:
                df_maxcapreq_results = pd.read_csv(file_path_results)
                df_maxcapreq_input = df_maxcapreq_input.merge(df_maxcapreq_results, on='Constraint', how='left')
            except Exception as e:
                st.markdown(f"An error occurred while reading the file: {e}")
        else:
            st.markdown(f"The file {file_path_results} does not exist.")
        
        return df_maxcapreq_input.round(3)
    
def resources_maxcapreq():
    file_path_input = "inputs\\resources\\policy_assignments\\Resource_maximum_capacity_requirement.csv"  # Replace with your CSV file path
    df_resources_maxcapreq_input = pd.read_csv(file_path_input)

    df_resources_maxcapreq_input.set_index("Resource", inplace= True)
    df_resources_maxcapreq_input_long = df_resources_maxcapreq_input.reset_index().melt(
        id_vars=['Resource'],
        var_name='Constraint',
        value_name='Constraint_Value'
    )
    df_resources_maxcapreq_input_long = df_resources_maxcapreq_input_long[df_resources_maxcapreq_input_long["Constraint_Value"]==1]
    df_resources_maxcapreq_input_long.reset_index(inplace=True, drop=True)
    df_resources_maxcapreq_input_long = df_resources_maxcapreq_input_long[["Resource","Constraint"]]
    df_resources_maxcapreq_input_long['Constraint'] = df_resources_maxcapreq_input_long['Constraint'].str.replace("Max_Cap","MaxCapReq")

    df_resources_maxcapreq_input_long = df_resources_maxcapreq_input_long.merge(policy_maxcapreq()[["Constraint",	"ConstraintDescription"]], how='left', on= "Constraint")
    df_resources_maxcapreq_input_long = df_resources_maxcapreq_input_long[["Resource", "ConstraintDescription"]]
    df_resources_maxcapreq_input_long.rename(columns={"ConstraintDescription": "Constraint"}, inplace=True)
    return df_resources_maxcapreq_input_long


###########################

st.markdown("## Maximum Capacity Requirement")
st.markdown("### Prices and penalties")
df_maxcapreq_policy = helpers.policy_maxcapreq()
df_maxcapreq_policy.drop(columns=["Constraint"], inplace= True)
df_maxcapreq_policy.rename(columns={"ConstraintDescription": "Constraint"}, inplace=True)
st.dataframe(df_maxcapreq_policy, use_container_width=True)

st.markdown("### Resource-policy assignment")
selected_policy = st.selectbox(label= "Select policy to list associated resources",
                               options= df_maxcapreq_policy["Constraint"])

df_resources_maxcapreq =  helpers.resources_maxcapreq()
df_resources_maxcapreq = df_resources_maxcapreq[["Constraint", "Resource"]]
df_resources_maxcapreq= df_resources_maxcapreq[df_resources_maxcapreq["Constraint"] == selected_policy]
df_resources_maxcapreq.reset_index(inplace=True, drop=True)
df_resources_maxcapreq.index = df_resources_maxcapreq.index + 1
st.dataframe(df_resources_maxcapreq, use_container_width= True)
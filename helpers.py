import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import yaml

def create_resource_list():
    
    df_resource = pd.DataFrame(columns=["Resource", "Type","Zone"])

    file_path = "inputs/resources/Hydro.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_hydro = pd.read_csv(file_path)
            df_hydro = df_hydro[["Resource","Zone"]]
            df_hydro["Type"] = "Hydro"
            df_resource = pd.concat([df_resource, df_hydro], axis=0)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Thermal.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_thermal = pd.read_csv(file_path)
            df_thermal = df_thermal[["Resource","Zone"]]
            df_thermal["Type"] = "Thermal"
            df_resource = pd.concat([df_resource, df_thermal], axis=0)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Vre.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_vre = pd.read_csv(file_path)
            df_vre = df_vre[["Resource","Zone"]]
            df_vre["Type"] = "Vre"
            df_resource = pd.concat([df_resource, df_vre], axis=0)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Storage.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_storage = pd.read_csv(file_path)
            df_storage = df_storage[["Resource","Zone"]]
            df_storage["Type"] = "Storage"
            df_resource = pd.concat([df_resource, df_storage], axis=0)

        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Flex_demand.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_flex_demand = pd.read_csv(file_path)
            df_flex_demand = df_flex_demand[["Resource","Zone"]]
            df_flex_demand["Type"] = "Flex_demand"
            df_resource = pd.concat([df_resource, df_flex_demand], axis=0)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Must_run.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_must_run = pd.read_csv(file_path)
            df_must_run = df_must_run[["Resource","Zone"]]
            df_must_run["Type"] = "Must_run"
            df_resource = pd.concat([df_resource, df_must_run], axis=0)
        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Electrolyzer.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_electrolyzer = pd.read_csv(file_path)
            df_electrolyzer = df_electrolyzer[["Resource","Zone"]]
            df_electrolyzer["Type"] = "Electrolyzer"
            df_resource = pd.concat([df_resource, df_electrolyzer], axis=0)

        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    file_path = "inputs/resources/Vre_stor.csv"  # Replace with your CSV file path
    if os.path.isfile(file_path):
        # File exists, so read it
        try:
            df_vre_stor = pd.read_csv(file_path)
            df_vre_stor = df_vre_stor[["Resource","Zone"]]
            df_vre_stor["Type"] = "Vre_stor"
            df_resource = pd.concat([df_resource, df_vre_stor], axis=0)

        except Exception as e:
            st.markdown(f"An error occurred while reading the file: {e}")

    df_resource.reset_index(inplace=True, drop=True)
    df_resource.to_csv("inputs/resource_list.csv")


###############################################
### Files related to Max Cap requirements
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
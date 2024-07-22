import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import yaml

####################################################
### HELPER FUNCTIONS
####################################################


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



st.markdown("## Costs")
df_costs = read_file("results/costs.csv")
st.dataframe(df_costs, hide_index=True, use_container_width=True)

st.markdown("## Net Revenue")
df_net_revenue = read_file("results/NetRevenue.csv")
df_resources = read_file("inputs/resource_list.csv")

selected_type = st.selectbox(
    label="Select resource type",
    options = df_resources["Type"].unique())

selected_zone = st.selectbox(
    label="Select zone",
    options = df_resources["Zone"].unique())

resources_list = df_resources[(df_resources.Type == selected_type) & (df_resources.Zone == selected_zone)]

df_net_revenue = df_net_revenue.merge(resources_list[["Resource"]], on="Resource", how='inner')
cost_list = [col for col in df_net_revenue.columns if "cost" in col.lower()]
cost_list.remove('EmissionsCost')
df_net_revenue[cost_list] = df_net_revenue[cost_list] * -1
drop_cols = ['region', 'zone', 'Cluster', 'R_ID', 'Revenue', 'Cost', 'Profit']
df_net_revenue.drop(columns=drop_cols, inplace=True)

# drop costs that are 0
zero_cols = [col for col in df_net_revenue.columns if (df_net_revenue[col] == 0).all()]
df_net_revenue.drop(columns=zero_cols, inplace=True)


df_melted = df_net_revenue.melt(id_vars=['Resource'],  
                                value_name='Value' ,
                                var_name="Metric"   )


chart = (alt.Chart(df_melted).mark_bar().encode(
        x='Resource',
        y=alt.Y('Value', stack=True),
        color='Metric',
        order=alt.Order(
        # Sort the segments of the bars by this field
        'Value',
        sort='ascending'
    )
    )).interactive()

st.altair_chart(chart, use_container_width=True)














# df_net_revenue = read_file("results/NetRevenue.csv")
# df_net_revenue = df_net_revenue.merge(resources_list, on="Resource", how='inner')

# cost_list = ['Inv_cost_MW'	'Inv_cost_MWh'	'Inv_cost_charge_MW'	'Fixed_OM_cost_MW'	'Fixed_OM_cost_MWh'	'Fixed_OM_cost_charge_MW'	'Var_OM_cost_out'	'Fuel_cost'	'Var_OM_cost_in'	'StartCost'	'Charge_cost'	'CO2SequestrationCost']
# revenue_list =['EnergyRevenue', 'SubsidyRevenue', 'OperatingReserveRevenue', 'OperatingRegulationRevenue','ReserveMarginRevenue','ESRRevenue','EmissionsCost','RegSubsidyRevenue'] 


# df_net_revenue = df_net_revenue[["Resource", "Revenue", "Cost"]]


# # Create the Altair chart
# df_melted = df_net_revenue.melt(id_vars='Resource', var_name='Category', value_name='Amount')
# # Create the Altair chart
# chart = alt.Chart(df_melted).mark_bar().encode(
#     x=alt.X('Resource:N', axis=alt.Axis(labelAngle=-80, title='Resource')),
#     y=alt.Y('Amount', axis=alt.Axis(title='$')),
#     color=alt.Color('Category:N', scale=alt.Scale(domain=['Revenue', 'Cost'])),
#     xOffset='Category:N'  # This creates the side-by-side bars
# ).properties(
#     width=alt.Step(20)  # Adjust the width of the bars
# )

# # Display the chart in Streamlit
# st.altair_chart(chart, use_container_width=True)


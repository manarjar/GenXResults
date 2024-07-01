import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re

st.markdown("# Power Balance Analysis")

df_power_balance = pd.read_csv("results/power_balance.csv")
df_markets_sales = pd.read_csv("results/Market_sales.csv")
df_markets_purchases = pd.read_csv("results/Market_purchases.csv")
df_net_market= pd.DataFrame({"BalanceComponent":[f"t{i+1}" for i in range(0,df_markets_sales.shape[0])]})
df_net_market["Market_sales"] = list(df_markets_sales.sum(axis=1))
df_net_market["Market_sales"] *= -1
df_net_market["Market_purshase"] = df_markets_purchases['Z_1']

df_power_balance = df_power_balance.merge(df_net_market, on = "BalanceComponent")
df_power_balance.drop(columns=['BalanceComponent'], inplace=True)
df_power_balance["Time"] = range(1,df_power_balance.shape[0]+1)

time_range = st.slider(
    label= "Select time range",
    min_value= 1,
    max_value= 8760, 
    value=(1, 24),
    step=1)

df_power_balance = df_power_balance[time_range[0]:time_range[1]]

df_power_balance_melted = df_power_balance.melt(id_vars=['Time'],
                                                value_vars=['Generation', 'Storage_Discharge', 'Storage_Charge',
                                                'Flexible_Demand_Defer', 'Flexible_Demand_Stasify', 'Demand_Response',
                                                'Nonserved_Energy', 'Transmission_NetExport', 'Transmission_Losses',
                                                'Demand', 'VRE_Storage_Discharge', 'VRE_Storage_Charge', 'Market_sales',
                                                'Market_purshase'], 
                                                value_name='Value' ,
                                                var_name="Metric"      )


chart = (alt.Chart(df_power_balance_melted).mark_bar().encode(
        x='Time',
        y='Value',
        color='Metric'
    ))

st.altair_chart(chart, use_container_width=True)


import streamlit as st
import helpers
import pandas as pd
import numpy as np
import os
helpers.create_resource_list()



# pages = {
#     "Resources" : [
#         st.Page("01_Resources.py", title="Create your account"),
#         st.Page("02_Power Balance.py", title="Manage your account")
#     ],
#     "Policies" : [
#         st.Page("P1 CapacityReserveMargin.py", title="Capacity Reserve Margin"),
#         st.Page("P2 CarbonCap.py", title="CO2 Cap"),
#         st.Page("P3 EnergyShareReq.py", title="Energy Share Requirement"),
#         st.Page("P4 MinCapReq.py", title="Minimum Capacity Requirement"),
#         st.Page("P5 MaxCapReq.py", title="Maximum Capacity Requirement")
#     ]
# }

# pg = st.navigation(pages)
# pg.run()
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from datetime import datetime, timedelta
import os
import yaml

file_path_settings = "inputs\\settings\\genx_settings.yml" 
# Open the file and load the YAML content
with open(file_path_settings, 'r') as file:
    settings = yaml.safe_load(file)

st.markdown("# Minimum capacity Requirement")
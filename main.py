import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import numpy as np
from copy import deepcopy


###################################################################################
### LOADING FILES

# Load data downloaded from data.open-power-system-data.org/renewable_power_plants/2020-08-25
@st.experimental_memo

# LOAD DATAFRAME FUNCTION
def load_data(path):
    df = pd.read_csv(path)
    return df

# LOAD ENERGY DATA
df_raw = load_data("https://data.open-power-system-data.org/renewable_power_plants/2020-08-25/renewable_power_plants_DE.csv")
df = deepcopy(df_raw)

# LOAD GEOJSON FILE
with open("./data/2_hoch.geo.json") as response:
    gj = json.load(response)

# Groupby Federal State (Bundesländer)
bl_prod = df.groupby('federal_state')['electrical_capacity'].mean().reset_index()

# bl_prod["log_ele"] = np.log(bl_prod["electrical_capacity"])
# Tried to scale the data, it helps to visualize colors, but modify the true nature of the data


###################################################################################

# Add title and header
st.title("Electricity Capacity in Germany")
st.header("Detail per Bundesland (MW)")

# Geographic Map
fig = px.choropleth_mapbox(bl_prod, geojson=gj, locations='federal_state', color='electrical_capacity',
                           featureidkey="properties.name",
                           color_continuous_scale="Viridis",
                           range_color=(0.026,0.24),
                           mapbox_style="carto-positron",
                           opacity=0.5,
                           zoom=4, center = {"lat": 50.753140, "lon": 11.464967},
                           hover_name = 'federal_state',
                           labels={'production':'Electricity capacity'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title="try")
st.plotly_chart(fig)

###################################################################################

# Setting up columns
#c1,c3 = st.columns([1,1])

#c1.download_button("Download CSV File", data="https://data.open-power-system-data.org/renewable_power_plants/2020-08-25, file_name="Electricity in Germany", mime='text/csv')

# link = '[To see the code in GitHub ](https://github.com/)'
# c3.markdown(link, unsafe_allow_html=True)

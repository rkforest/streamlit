import os
import warnings
import pooch

import numpy as np
import pandas as pd
import xarray as xr

import matplotlib.pyplot as plt
#import cartopy.crs as crs

import holoviews as hv
import hvplot.xarray # noqa
import hvplot.pandas # noqa
import ipywidgets as ipw
import panel as pn
import panel.widgets as pnw

import streamlit as st


st.set_page_config(
    page_title='Global Temperature Change',
    layout='wide',
)


file_path = 'data/gistemp10y.nc'
ds = xr.open_dataset(file_path)  

map_year = st.slider(
    label='Select Decade',
    min_value=1920,
    max_value=2020,
    value=(1920),
    step=10
    )




sel_year = str(map_year)+"-12-31"
# ax.set_title('Temperature Anomalies\nDecade Ending '+str(map_year))

proj = 'Robinson'
pfig = ds['tempanomaly'].sel(time=sel_year).hvplot.quadmesh(
    'lon', 'lat',
    projection=proj, project=False, global_extent=True, 
    cmap='coolwarm', rasterize=True, dynamic=False, coastline=True, 
    frame_width=1200)

st.bokeh_chart(hv.render(pfig , backend='bokeh'))



#     Data Source: https://data.giss.nasa.gov/gistemp

#     Python Libaries: Pandas, Geopandas, Xarray, Seaborn, Plotly, Streamlit

#     Author: Rick Forest - rkforest@icloud.com

#     Updated: Apr 7, 2022''')


import conda
import os

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

import numpy as np
#import pandas as pd
import xarray as xr
import pooch
#import getdata
#import getnetcdf

import matplotlib.pyplot as plt
import seaborn as sns
#from matplotlib import colors
#import plotly.express as px

import cartopy
import cartopy.crs as ccrs
#import cartopy.feature as cfeature

import streamlit as st


st.set_page_config(
    page_title='Global Temperature Change',
    layout='wide',
)

sns.set_style('darkgrid') 
seasons = ['Spring', 'Summer', 'Autumn','Winter']
seasons_palette = sns.color_palette("viridis_r",4)

st.title('Global Temperature Change')

# # get csv data
# data_load_state = st.sidebar.text('Loading data...')
# dfg, dfgd = getdata.read_global_monthly_temperature_anomalies('GLB', download=False)
# dfn, dfnd = getdata.read_global_monthly_temperature_anomalies('NH', download=False)
# dfs, dfsd = getdata.read_global_monthly_temperature_anomalies('SH', download=False)
# dfz, dfzd = getdata.read_zonal_temperature_anomalies(download=False)
# dfm = pd.concat([dfg,dfn,dfs])
#dfd = pd.concat([dfgd,dfnd,dfsd])

# xarray
# file_path = pooch.retrieve(
#     'https://data.giss.nasa.gov/pub/gistemp/gistemp1200_GHCNv4_ERSSTv5.nc.gz',
#     known_hash='61b9d2880cfe5f6fbdb8b9a1088fdc3f38ff751e829b4bed7561e90e02b0bbbe',
#     processor=pooch.Decompress(),
# )

file_path = 'data/gistemp10y.nc'

ds = xr.open_dataset(file_path)  
ds10yr = ds.resample(time='10Y').mean()
da = ds10yr['tempanomaly']
da.attrs["units"] = "Degrees C"
da.attrs["long_name"] = "Global Temperature Anomalies"




# #sidebar
# with st.sidebar:

#     st.sidebar.markdown('---')
#     year_range = st.slider(
#         label='Select start and end year',
#         min_value=1880,
#         max_value=2022,
#         value=(1880,2020),
#         step=10
#         )
#     year_start = year_range[0]
#     year_end = year_range[1]    

#     st.sidebar.markdown('---')
#     aggregation = st.radio(
#         'Select Aggregation',
#           ('Season', 'Month', 'Hemisphere'),
#           index=0)

#     st.sidebar.markdown('---')
#     if st.sidebar.checkbox('Show raw data'):
#         st.sidebar.subheader('Raw data')
#         st.sidebar.dataframe(dfg['Anomaly'])

# select_date = '2022-02-15'
# df1 = dfm.query('Id == "GLB" and Year >= @year_start and Year <= @year_end').reset_index()
# df2 = dfd.query('Id == "GLB" and Decade >= @year_start and Decade <= @year_end').reset_index()
# df3 = dfm.query('Id in ("NH","SH") and Year >= @year_start and Year <= @year_end').reset_index()

# # main plot 

map_year = st.slider(
    label='Select Decade',
    min_value=1880,
    max_value=2020,
    value=(1880),
    step=10
    )




sel_year = str(map_year)+"-12-31"

fig = plt.figure(figsize=(10,5))

ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines()
ax.gridlines()

da.sel(time=sel_year).plot(ax=ax,
        transform=ccrs.PlateCarree(),
        cbar_kwargs={'shrink': 0.6,
                     "label": "°C"}, cmap='coolwarm')
ax.set_title('Temperature Anomalies\nDecade Ending '+str(map_year))
st.pyplot(fig)


# #i = int((map_year-1880)/10)+1

# filt1 = df.index.year == map_year
# filt2 = df['lat'] < 81
# filt3 = df['lat'] > -81
# df_plot = df[filt1 & filt2 & filt3]

# st.subheader("Temperature Anomaly in "+ str(map_year) + " [°C]")


# divnorm = colors.TwoSlopeNorm(vmin=df_plot['tempanomaly'].max()*-1,
#                               vcenter=0.,
#                               vmax=df_plot['tempanomaly'].max())

# g = sns.relplot(
#     kind="scatter", height=8, aspect=2,
#     data=df_plot,
#     x='lon',
#     y='lat',
#     hue='tempanomaly',
#     legend=False,
#     palette="coolwarm", 
#     s=100,
#     edgecolor=None,
#     hue_norm=divnorm)
# g.set(xlabel="Longitude", ylabel="Latitude")

# sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=divnorm)
# for ax in g.axes.flat:
#     ax.figure.colorbar(sm)

# # da_robinson.isel(time=i).plot.imshow(ax=ax, add_labels=False, add_colorbar=True,
# #                vmin=-4, vmax=4, cmap='coolwarm',
# #                cbar_kwargs=cbar_kwargs)

# st.pyplot(g)

# data_load_state.text('Data loaded.')


# # to center colorbar at zero
# # divnorm = colors.TwoSlopeNorm(vmin=xrdf1['tempanomaly'].max()*-1,
# #                               vcenter=0.,
# #                               vmax=xrdf1['tempanomaly'].max())
# # g = sns.relplot(
# #         kind="scatter", height=3, aspect=2,
# #         data=xrdf1, x='lon', y='lat',  hue='tempanomaly', hue_norm=divnorm,
# #         legend=False, palette="coolwarm", edgecolor=None)
# # g.set(title=select_date, xlabel="Longitude", ylabel="Latitude")

# # sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=divnorm)
# # for ax in g.axes.flat:
# # #    ax.figure.colorbar(sm)
# #     cbar = ax.figure.colorbar(sm)
# #     cbar.ax.tick_params(size=0)
# #     cbar.set_label('Degrees (Celsius)')

# # st.pyplot(g)

# # container plots

# container1 = st.container()
# container2 = st.container()

# with container1:

#     col1, col2  = st.columns([5,3])

#     with col1:

#         st.subheader("Date Range: " +  str(year_start) + "-" + str(year_end))

#         g = px.scatter(df1,
#                         x='Date',
#                         y='Anomaly',
#                         color='Anomaly',
#                         color_continuous_scale='balance',
#                         color_continuous_midpoint=0,
#                         #range_x=['1880-01-01','2022-12-31'],
#                         range_y=[-1.5, 1.5],
#                         range_color=(-1.5, 1.5),
#                         )
#         g.update_layout(xaxis_title='Date',
#                         yaxis_title='Degrees (Celsius)',
#                         coloraxis_colorbar_title_text = '',
#                         height=500, 
#                         )            
#         g.update_traces(marker=dict(size=7,
#                                     line=dict(width=0.5,
#                                                 color='Black')))
#         st.plotly_chart(g)  

#     with col2:
#         st.subheader("By " + aggregation)
#         st.text(" ")
#         st.text(" ")
#         st.text(" ")
#         if aggregation == "Season":

#             g = sns.catplot(
#                 kind="bar", height=3.5, aspect=1.5,
#                 data=df1, x='Season', y='Anomaly',
#                 ci=None,
#                 order=seasons, palette=seasons_palette, legend=False)
#             g.set(xlabel="", ylabel = "Degrees (C)")
#             st.pyplot(g)

#         elif aggregation == "Month":
#             g = sns.catplot(
#                 kind="bar", height=4, aspect=2,
#                 data=df1, x='Month', y='Anomaly',
#                 ci=None,
#                 palette='mako',
#                 legend=False)
#             g.set(xlabel="", ylabel = "Degrees (C)")
#             st.pyplot(g)
#         elif aggregation == "Hemisphere":
#             g = sns.catplot(
#                 kind="bar", height=4, aspect=2,
#                 data=df3, x='Id', y='Anomaly',
#                 ci=None,
#                 palette='mako',
#                 legend=False)
#             g.set(xlabel="", ylabel = "Degrees (C)")
#             st.pyplot(g)

# with container2:


#     col1, col2  = st.columns([4,2])

#     with col1:

#         st.subheader("By Latitude")
#         g = px.bar(dfzd,
#                     x='Latitude',
#                     y='Anomaly',
#                     facet_col="Hemisphere",
#                     color="Anomaly",
#                     animation_frame="Decade", 
#                     range_y=[-2.5,2.5],
#                     color_continuous_scale='balance',
#                     color_continuous_midpoint=0,
#                     )
#         g.update_layout(xaxis_title='Latitude',
#                 yaxis_title='Degrees (Celsius)',
#                 coloraxis_colorbar_title_text = '',)
#         st.plotly_chart(g) 


#     with col2:

#             st.subheader("Distribution: ")
#             g = sns.displot(
#                 kind="hist",
#                 height=4, aspect=1.5,
#                 data=df1, x='Anomaly')
#             g.set(xlabel = "Degrees (Celsius)")     

#             st.pyplot(g)

# with st.sidebar:

#     st.sidebar.markdown('---')
#     st.sidebar.info('''
#     ### Global Temperature Change App

#     Data Source: https://data.giss.nasa.gov/gistemp

#     Python Libaries: Pandas, Geopandas, Xarray, Seaborn, Plotly, Streamlit

#     Author: Rick Forest - rkforest@icloud.com

#     Updated: Apr 7, 2022''')


import os
import calendar

import numpy as np
import pandas as pd
import seaborn as sns
import getdata

import matplotlib.pyplot as plt
import plotly.express as px

import streamlit as st

st.set_page_config(
    page_title='Temperature Anomalies',
    layout='wide',
)

sns.set_style('darkgrid') 
seasons = ['Spring', 'Summer', 'Autumn','Winter']
seasons_palette = sns.color_palette("viridis_r",4)

data_load_state = st.sidebar.text('Loading data...')

dfg, dfgd = getdata.read_global_monthly_temperature_anomalies('GLB', download=False)
dfn, dfnd = getdata.read_global_monthly_temperature_anomalies('NH', download=False)
dfs, dfsd = getdata.read_global_monthly_temperature_anomalies('SH', download=False)
dfz, dfzd = getdata.read_zonal_temperature_anomalies(download=False)
dfm = pd.concat([dfg,dfn,dfs])
dfd = pd.concat([dfgd,dfnd,dfsd])

data_load_state.text('Data loaded.')

st.title('Global Temperature Anomalies')

with st.sidebar:

    st.sidebar.markdown('---')
    year_range = st.slider(
        label='Select start and end year',
        min_value=1880,
        max_value=2022,
        value=(2000,2022),
        step=10
        )
    year_start = year_range[0]
    year_end = year_range[1]    

    st.sidebar.markdown('---')
    aggregation = st.radio(
        'Select Aggregation',
          ('Season', 'Month', 'Hemisphere'),
          index=0)

    st.sidebar.markdown('---')
    if st.sidebar.checkbox('Show raw data'):
        st.sidebar.subheader('Raw data')
        st.sidebar.dataframe(dfg['Anomaly'])

    st.sidebar.markdown('---')
    st.sidebar.info('''
    ### Temperature Anomaly App

    Data Source: https://data.giss.nasa.gov/gistemp

    Python Libaries: Pandas, Seaborn, Plotly, Streamlit

    Author: Rick Forest - rkforest@icloud.com

    Updated: Apr 7, 2022''')

df1 = dfm.query('Id == "GLB" and Year >= @year_start and Year <= @year_end').reset_index()
df2 = dfd.query('Id == "GLB" and Decade >= @year_start and Decade <= @year_end').reset_index()
df3 = dfm.query('Id in ("NH","SH") and Year >= @year_start and Year <= @year_end').reset_index()

container1 = st.container()
container2 = st.container()



with container1:

    col1, col2  = st.columns([5,3])

    with col1:

        st.subheader("Date Range: " +  str(year_start) + "-" + str(year_end))

        g = px.scatter(df1,
                        x='Date',
                        y='Anomaly',
                        color='Anomaly',
                        color_continuous_scale='balance',
                        color_continuous_midpoint=0,
                        #range_x=['1880-01-01','2022-12-31'],
                        range_y=[-1.5, 1.5],
                        range_color=(-1.5, 1.5),
                        )
        g.update_layout(xaxis_title='Date',
                        yaxis_title='Degrees (Celsius)',
                        coloraxis_colorbar_title_text = '',
                        height=500, 
                        )            
        g.update_traces(marker=dict(size=7,
                                    line=dict(width=0.5,
                                                color='Black')))
        st.plotly_chart(g)  

    with col2:
        st.subheader("By " + aggregation)
        st.text(" ")
        st.text(" ")
        st.text(" ")
        if aggregation == "Season":

            g = sns.catplot(
                kind="bar", height=3.5, aspect=1.5,
                data=df1, x='Season', y='Anomaly',
                ci=None,
                order=seasons, palette=seasons_palette, legend=False)
            g.set(xlabel="", ylabel = "Degrees (C)")
            st.pyplot(g)

        elif aggregation == "Month":
            g = sns.catplot(
                kind="bar", height=4, aspect=2,
                data=df1, x='Month', y='Anomaly',
                ci=None,
                palette='mako',
                legend=False)
            g.set(xlabel="", ylabel = "Degrees (C)")
            st.pyplot(g)
        elif aggregation == "Hemisphere":
            g = sns.catplot(
                kind="bar", height=4, aspect=2,
                data=df3, x='Id', y='Anomaly',
                ci=None,
                palette='mako',
                legend=False)
            g.set(xlabel="", ylabel = "Degrees (C)")
            st.pyplot(g)

with container2:


    col1, col2  = st.columns([4,2])

    with col1:

        st.subheader("By Latitude")
        g = px.bar(dfzd,
                    x='Latitude',
                    y='Anomaly',
                    facet_col="Hemisphere",
                    color="Anomaly",
                    animation_frame="Decade", 
                    range_y=[-2.5,2.5],
                    color_continuous_scale='balance',
                    color_continuous_midpoint=0,
                    )
        g.update_layout(xaxis_title='Latitude',
                yaxis_title='Degrees (Celsius)',
                coloraxis_colorbar_title_text = '',)
        st.plotly_chart(g) 


    with col2:

            st.subheader("Distribution: ")
            g = sns.displot(
                kind="hist",
                height=4, aspect=1.5,
                data=df1, x='Anomaly')
            g.set(xlabel = "Degrees (Celsius)")     

            st.pyplot(g)

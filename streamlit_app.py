import os
import calendar

import numpy as np
import seaborn as sns
import getdata

import matplotlib.pyplot as plt
import plotly.express as px

import streamlit as st

st.title('Global Temperature Anomalies')

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')


dfg, dfgd = getdata.read_global_monthly_temperature_anomalies('GLB', download=False)

# Notify the reader that the data was successfully loaded.
data_load_state.text('Data loaded.')

st.subheader('Data')
st.dataframe(dfg['Anomaly'])

df = dfg.query('Id == "GLB"')

fig = plt.subplots()
g1 = sns.relplot(
    kind="scatter", height=3, aspect=2,
    data=df, x='Date', y='Anomaly')
g1.set(title="Global Temperature Anomalies", xlabel="", ylabel="Degrees (C)");
st.pyplot(g1)

fig = plt.subplots()
g2 = px.histogram(df,
                 x='Anomaly',
                 )
g2.update_layout(title='Global Temperature Anomalies',
                  xaxis_title='Degrees (Celsius)',
                 )
g2.update_traces(marker=dict(line=dict(width=0.5,
                                        color='black')))

st.plotly_chart(g2)                                    
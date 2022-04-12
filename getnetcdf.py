#'https://data.giss.nasa.gov/pub/gistemp/gistemp1200_GHCNv4_ERSSTv5.nc.gz'

import os
import numpy as np
#import pandas as pd
import xarray as xr
#import rioxarray as rio
import streamlit as st

@st.cache(hash_funcs={xr.core.dataset.Dataset: id}, allow_output_mutation=True)
def read_grid_data():
    file_name = 'gistemp1200_GHCNv4_ERSSTv5_10y.nc'
    file_path = os.path.join('data', file_name)
    ds = xr.open_dataset(file_path)
    ds = ds.rio.write_crs(4326)
    da = ds['tempanomaly']
    
    robinson_proj = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    da_robinson = da.rio.reproject(robinson_proj,nodata=np.NaN)
   
    return da, da_robinson

def save_grid_data():
    in_file_name = 'gistemp1200_GHCNv4_ERSSTv5.nc'
    in_file_path = os.path.join('data', in_file_name)
    ds = xr.open_dataset(in_file_path)

    ds10yr = ds.resample(time='10Y').mean()
    ds10yr = ds10yr.rio.write_crs(4326)
    out_file_name = 'gistemp10y.nc'
    out_file_path = os.path.join('data', out_file_name)
    ds10yr.to_netcdf(out_file_path) 

    df10yr = ds10yr.to_dataframe()
    out_file_name = 'gistemp10y.csv'
    out_file_path = os.path.join('data', out_file_name)
    df10yr.to_csv(out_file_path)

    robinson_proj = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    
    da10yr = ds10yr['tempanomaly']
    da10yr_robinson = da10yr.rio.reproject(robinson_proj,nodata=np.NaN)
    out_file_name = 'gistemp10y_robinson.nc'
    out_file_path = os.path.join('data', out_file_name)
    da10yr_robinson.to_netcdf(out_file_path) 

    df10yr_robinson = da10yr_robinson.to_dataframe()
    out_file_name = 'gistemp10y_robinson.csv'
    out_file_path = os.path.join('data', out_file_name)
    df10yr_robinson.to_csv(out_file_path)

    return

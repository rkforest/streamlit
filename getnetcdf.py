#'https://data.giss.nasa.gov/pub/gistemp/gistemp1200_GHCNv4_ERSSTv5.nc.gz'

import os
import numpy as np
import xarray as xr
import rioxarray as rio
import streamlit as st

@st.cache(hash_funcs={xr.core.dataset.Dataset: id}, allow_output_mutation=True)
def read_xarray_file():
    file_name = 'gistemp1200_GHCNv4_ERSSTv5_10y.nc'
    file_path = os.path.join('data', file_name)
    ds = xr.open_dataset(file_path)
    ds = ds.rio.write_crs(4326)
    da = ds['tempanomaly']
    
    robinson_proj = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    da_robinson = da.rio.reproject(robinson_proj,nodata=np.NaN)
   
    return da, da_robinson

def save_xarray_file():
    in_file_name = 'gistemp1200_GHCNv4_ERSSTv5.nc'
    in_file_path = os.path.join('data', in_file_name)
    ds = xr.open_dataset(in_file_path)
    dsd = ds.resample(time='10Y').mean()
    
    out_file_name = 'gistemp1200_GHCNv4_ERSSTv5_10y.nc'
    out_file_path = os.path.join('data', out_file_name)
    dsd.to_netcdf(out_file_path) 
    
    return

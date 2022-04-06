## NASA Data  


#'https://data.giss.nasa.gov/gistemp/tabledata_v4/'
# GLB.Ts+dSST.csv  
# NH.Ts+dSST.csv  
# SH.Ts+dSST.csv  
# ZonAnn.Ts+dSST.csv  

# T_AIRS/GLB.Ts+dSST.csv  
# T_AIRS/NH.Ts+dSST.csv  
# T_AIRS/SH.Ts+dSST.csv  
# T_AIRS/ZonAnn.Ts+dSST.csv  

import os
import calendar
import pandas as pd
from pandas.api.types import CategoricalDtype

def read_global_monthly_temperature_anomalies(id, download=False):

    file_name = id + ".Ts+dSST.csv"
    file_path = os.path.join('data', file_name)
 
    # download and save csv
    if download==True:
        url = 'https://data.giss.nasa.gov/gistemp/tabledata_v4/' + file_name
        df = pd.read_csv(url, skiprows=1)
        df.to_csv(file_path, index=False, sep=',')
    
    # create month categorical
    months = [month for month in calendar.month_abbr if month]
    months_cat = CategoricalDtype(months, ordered=True)
    
    # create season categorical
    seasons = ['Winter','Spring', 'Summer', 'Autumn']
    seasons_cat = CategoricalDtype(seasons, ordered=True)
    
    # create dictionary to assign seasons to months
    months_season_dict = {}
    for i, month in enumerate(months):
        if i in (0, 1, 11):
            months_season_dict[month] = 'Winter'
        elif i in (2, 3, 4):
            months_season_dict[month] = 'Spring'
        elif i in (5, 6, 7):
            months_season_dict[month] = 'Summer'        
        elif i in (8, 9, 10):
            months_season_dict[month] = 'Autumn' 
            
    # import        
    cols_to_import = months
    cols_to_import.insert(0,'Year')
    df = pd.read_csv(file_path,
                 usecols=cols_to_import,
                 parse_dates=['Year'],
                 na_values=['***'])

    # tidy
    df = pd.melt(df,
                 id_vars=['Year'],
                 var_name=['Month'],
                 value_name='Anomaly')
    
    # transform
    df.dropna(inplace=True) # drop missing values

    # add id column
    df['Id'] = id

     # modify date to include month
    df['year_str'] = df['Year'].dt.strftime('%Y') # create year string
    df['month_str'] =  pd.to_datetime(df['Month'], format='%b').dt.strftime('%m') # create month string
    df['Date'] = pd.to_datetime(df['year_str'] + df['month_str'], format='%Y%m') # combine strings and convert to date
    df.drop(columns=['year_str', 'month_str'],inplace=True) # drop unneeded columns
   
    # map months to seasons
    df['Season'] = df['Month'].map(months_season_dict)  

    # transform
    df.set_index('Date', inplace=True)  # set year month date as index
    df['Year'] = df.index.year # add Year column
    df = df[['Id','Year','Season','Month','Anomaly']]  # reorder columns

    # convert month and seoson columns to categorical types
    df['Month'] = df['Month'].astype(months_cat)
    df['Season'] = df['Season'].astype(seasons_cat)

    # sort
    df.sort_values(by=['Year','Month'],inplace=True)
    
    # resample ten year intervals into decades df
    dfd = df[['Id','Month','Season','Anomaly']].\
            groupby(['Id','Month','Season']). \
            resample('10YS'). \
            mean(). \
            round(3). \
            reset_index()
    
    # transform
    dfd.set_index('Date', inplace=True) # set index of decades df
    dfd['Decade'] = dfd.index.year # add Decade column to decades df
    dfd = dfd[['Id','Decade','Season','Month','Anomaly']] # reorder columns

    return(df, dfd)


def read_zonal_temperature_anomalies(download=False):

    file_name = 'ZonAnn.Ts+dSST.csv'
    file_path = os.path.join('data', file_name)
    
    # download and save csv
    if download==True:
        url = 'https://data.giss.nasa.gov/gistemp/tabledata_v4/' + file_name
        df = pd.read_csv(url)
        df.to_csv(file_path, index=False, sep=',')
        
    # import   
    cols_to_import=['Year',
                    'EQU-24N','24N-44N','44N-64N','64N-90N',
                    '24S-EQU','44S-24S','64S-44S','90S-64S']
    df = pd.read_csv(file_path, usecols=cols_to_import)
    
    # rename columns
    col_names = {'EQU-24N': 'N24', '24N-44N': 'N44', '44N-64N': 'N64', '64N-90N': 'N90',
             '24S-EQU': 'S24', '44S-24S': 'S44', '64S-44S': 'S64', '90S-64S': 'S90'}
    df.rename(columns=col_names,inplace=True)
    
    # tidy
    df = pd.melt(df,
                 id_vars=['Year'],
                 var_name=['Zone'],
                 value_name='Anomaly')
    
    # transform
    df.dropna(inplace=True) # drop missing values
    df['Year'] = pd.to_datetime(df['Year'], format='%Y') # convert integer year to date
    df.set_index('Year', inplace=True) # set index
    df.index.names = ['Date'] # rename index 
    df['Year'] = df.index.year  # add Year column  

    # split zone into hemisphere and latitude columns
    df['Hemisphere'] = df['Zone'].str[0]
    df['Latitude'] = df['Zone'].str[1:]
    df.drop(columns='Zone',inplace=True) # drop Zone column
  
    # reorder columns
    df = df[['Year','Hemisphere','Latitude','Anomaly']]      

    # resample 
    dfd = df[['Hemisphere','Latitude','Anomaly']] \
            .groupby(['Hemisphere','Latitude']) \
            .resample('10YS') \
            .agg('mean') \
            .round(3) \
            .reset_index()
    
    # transform
    dfd.set_index('Date', inplace=True) # set index
    dfd['Decade'] = dfd.index.year # add Year column
    dfd = dfd[['Decade','Hemisphere','Latitude','Anomaly']] # reorder columns
     
    return(df,dfd)

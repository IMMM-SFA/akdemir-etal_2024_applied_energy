import pandas as pd
import numpy as np
from datetime import timedelta
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl

#Reading BA and temperature data and merging those together to find average
all_BAs_df = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/BAs.csv',header=0)
all_BA_names = [*all_BAs_df['Name']]
all_BA_abbs = [*all_BAs_df['Abbreviation']]

# Define function to convert K to F
def convert_K_to_F(temp_K):
    temp_F = (temp_K - 273.15) * 9/5 + 32
    return temp_F

#Creating a function for cooling degree day
def calculate_CDD(T):
    return max(T - 65, 0)

#Reading county and states shapefile
County_shapefile = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_County/US_CountyBndrys.shp')
County_shapefile = County_shapefile.to_crs("EPSG:3395")
County_shapefile['GEOID'] = County_shapefile['GEOID'].astype(int)
County_shapefile['Heatwave_1_T'] = np.zeros(len(County_shapefile))
County_shapefile.set_index('GEOID',inplace=True)

states_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.to_crs("EPSG:3395")

#Plotting the county temperature results for single timestep (CA-AZ Specific)
heatwave1_PST = pd.to_datetime('2019-06-10 15:00:00')
heatwave1_UTC = heatwave1_PST + timedelta(hours=8)
heatwave_year = str(heatwave1_UTC.year)
if heatwave1_UTC.month <10:
    heatwave_month = f'0{heatwave1_UTC.month}'
else:
    heatwave_month = heatwave1_UTC.month

if heatwave1_UTC.day <10:
    heatwave_day = f'0{heatwave1_UTC.day}'
else:
    heatwave_day = heatwave1_UTC.day

if heatwave1_UTC.hour <10:
    heatwave_hour = f'0{heatwave1_UTC.hour}'
else:
    heatwave_hour = heatwave1_UTC.hour

county_data = pd.read_csv(f'../../Data/TELL_Outputs/2019_county_meteorology/{heatwave_year}_{heatwave_month}_{heatwave_day}_{heatwave_hour}_UTC_County_Mean_Meteorology.csv')
county_data['TempF'] = county_data['T2'].map(convert_K_to_F)

for my_fips in county_data['FIPS']:

    sp_Temp = county_data.loc[county_data['FIPS']==my_fips]['TempF'].values[0]
    County_shapefile.loc[my_fips,'Heatwave_1_T'] = sp_Temp

County_shapefile = County_shapefile.loc[County_shapefile['Heatwave_1_T'] != 0]

County_shapefile['CDD1'] = County_shapefile['Heatwave_1_T'].map(calculate_CDD)

plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots()
County_shapefile.plot(ax=ax, column='Heatwave_1_T', cmap='OrRd', legend=True, vmin=60, vmax=110,
                      legend_kwds={"label": r"Temperature ($\degree$F)", "shrink":0.95,
                      "pad":0.025, "extend":'both'})
states_gdf.plot(ax=ax,color='None',edgecolor='black',linewidth=0.5,alpha=0.5)

ax.set_box_aspect(1)
ax.set_xlim(-13950000,-11100000)
ax.set_ylim([3500000,6250000])
ax.axis('off')

ax.set_title(f'Local Heat Wave \n {heatwave1_PST}', weight='bold',fontsize=10)

plt.savefig('Local_heatwave.png',dpi=200, bbox_inches='tight')
plt.show()
plt.close()


#Plotting the county temperature results for single timestep (WECC General)
heatwave2_PST = pd.to_datetime('2019-08-05 15:00:00')
heatwave2_UTC = heatwave2_PST + timedelta(hours=8)
heatwave_year = str(heatwave2_UTC.year)
if heatwave2_UTC.month <10:
    heatwave_month = f'0{heatwave2_UTC.month}'
else:
    heatwave_month = heatwave2_UTC.month

if heatwave2_UTC.day <10:
    heatwave_day = f'0{heatwave2_UTC.day}'
else:
    heatwave_day = heatwave2_UTC.day

if heatwave2_UTC.hour <10:
    heatwave_hour = f'0{heatwave2_UTC.hour}'
else:
    heatwave_hour = heatwave2_UTC.hour

county_data = pd.read_csv(f'../../Data/TELL_Outputs/2019_county_meteorology/{heatwave_year}_{heatwave_month}_{heatwave_day}_{heatwave_hour}_UTC_County_Mean_Meteorology.csv')
county_data['TempF'] = county_data['T2'].map(convert_K_to_F)

for my_fips in county_data['FIPS']:

    sp_Temp = county_data.loc[county_data['FIPS']==my_fips]['TempF'].values[0]
    County_shapefile.loc[my_fips,'Heatwave_2_T'] = sp_Temp

County_shapefile = County_shapefile.loc[County_shapefile['Heatwave_2_T'] != 0]

County_shapefile['CDD2'] = County_shapefile['Heatwave_2_T'].map(calculate_CDD)

plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots()
County_shapefile.plot(ax=ax, column='Heatwave_2_T', cmap='OrRd', legend=True, vmin=60, vmax=110,
                    legend_kwds={"label": r"Temperature ($\degree$F)", "shrink":0.95,
                    "pad":0.025, "extend":'both'})
states_gdf.plot(ax=ax,color='None',edgecolor='black',linewidth=0.5,alpha=0.5)

ax.set_box_aspect(1)
ax.set_xlim(-13950000,-11100000)
ax.set_ylim([3500000,6250000])
ax.axis('off')

ax.set_title(f'Widespread Heat Wave \n {heatwave2_PST}', weight='bold',fontsize=10)

plt.savefig('Widespread_heatwave.png',dpi=200, bbox_inches='tight')
plt.show()
plt.close()

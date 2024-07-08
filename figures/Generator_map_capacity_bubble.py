import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import networkx as nx
import matplotlib.patches as mpatches
import yaml

#Reading nodal info
nodal_info = pd.read_csv('../../Data/Organized_Results/Nodal_information.csv', header=0)

#Reading CERF generator types from YAML file
with open('../../Data/Supplementary_Data/BA_Topology_Files/cerf_generation_types.yml') as f:
    CERF_gen_dict = yaml.full_load(f)

#Defining a function to gather generator types
def get_key(val):
    for key, value in CERF_gen_dict.items():
        if val in value:
            return key

#Reading 2015 and 2055 generators
CERF_2015_gens = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/CERF_2015_gens.csv', header=0)
CERF_2015_gens = CERF_2015_gens.loc[CERF_2015_gens['lmp_zone'].isin(nodal_info['Bus_Number'])]
CERF_2015_gens.reset_index(inplace=True, drop=True)
CERF_2015_gens['tech_name'] = [get_key(i) for i in CERF_2015_gens['tech_name']]

CERF_2055_gens = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/CERF_2055_gens_cooperative.csv', header=0)
CERF_2055_gens = CERF_2055_gens.loc[CERF_2055_gens['lmp_zone'].isin(nodal_info['Bus_Number'])]
CERF_2055_gens.reset_index(inplace=True, drop=True)
CERF_2055_gens['tech_name'] = [get_key(i) for i in CERF_2055_gens['tech_name']]

#Reading states shapefile
states_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.to_crs("EPSG:3395")



##################################### Map of Location of Generators for 2055 #####################################
#Creating an organized dataframe for plotting
all_bus_nums = []
all_gen_types = []
all_caps = []
all_lats = []
all_longs = []
all_colors = []

my_scale = 10

for gen in range(len(CERF_2055_gens)):
    
    sp_bus = CERF_2055_gens.loc[gen,'lmp_zone']
    all_bus_nums.append(sp_bus)
    
    sp_type = CERF_2055_gens.loc[gen,'tech_name']
    all_gen_types.append(sp_type)

    all_caps.append(CERF_2055_gens.loc[gen,'unit_size_mw'])
    
    sp_lat = CERF_2055_gens.loc[gen,'ycoord']
    all_lats.append(sp_lat)
    
    sp_long = CERF_2055_gens.loc[gen,'xcoord']
    all_longs.append(sp_long)
    
    if sp_type == 'NG':
        all_colors.append('#CA9161')
        
    elif sp_type == 'Geothermal':
        all_colors.append('#808000')

    elif sp_type == 'Coal':
        all_colors.append('#949494')
        
    elif sp_type == 'Oil':
        all_colors.append('#000000')
        
    elif sp_type == 'Biomass':
        all_colors.append('#CC78BC')

    elif sp_type == 'Solar':
        all_colors.append('#ECE133')

    elif sp_type == 'OnshoreWind':
        all_colors.append('#029E73')
        
    elif sp_type == 'OffshoreWind':
        all_colors.append('#56B4E9')

    elif sp_type == 'Hydro':
        all_colors.append('#0173B2')

    elif sp_type == 'Nuclear':
        all_colors.append('#D55E00')
        
    else:
        pass

gen_map_df = pd.DataFrame(list(zip(all_bus_nums,all_gen_types,all_caps,all_colors,all_lats,all_longs)),
                          columns=['Bus','Type','Capacity','Color','Latitude','Longitude'])

generators_all_2055 = gen_map_df.loc[:,['Type','Capacity']].copy()

#Finding all gen types and standardizing gen capacities
gen_map_df['Capacity'] = gen_map_df['Capacity'] / my_scale
gen_map_df.sort_values(by='Capacity', ascending=False, inplace=True)
gen_map_df.reset_index(drop=True,inplace=True)
gen_map_df.dropna(inplace=True)

#Changing to type of the dataframe into a geodataframe
geometry = [Point(xy) for xy in zip(gen_map_df['Longitude'],gen_map_df['Latitude'])]
nodes_df = gpd.GeoDataFrame(gen_map_df,crs='ESRI:102003',geometry=geometry)
nodes_df = nodes_df.to_crs("EPSG:3395") 

#Plotting the figure
plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots()
states_gdf.plot(ax=ax,color='None',edgecolor='black',linewidth=0.5,alpha=1)

abc = nodes_df.plot(ax=ax,c=nodes_df['Color'] ,markersize=nodes_df['Capacity'],alpha=0.7,edgecolor='black',linewidth=0.05)

ax.set_box_aspect(1)
ax.set_xlim(-13950000,-11000000)
ax.set_ylim([3500000,6250000])
ax.axis('off')

#Specifying legend
legend_elements = [Line2D([0], [0], marker='o', color='w',markerfacecolor='#CA9161', label='Natural Gas', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#949494', label='Coal', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#000000', label='Oil', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#808000', label='Geothermal', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#CC78BC', label='Biomass', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#ECE133', label='Solar', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#029E73', label='Wind', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#56B4E9', label='Offshore Wind', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#0173B2', label='Hydro', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#D55E00', label='Nuclear', markersize=9)]

first_legend = plt.legend(handles=legend_elements, bbox_to_anchor=(1.01,0.72), loc="center left", frameon=False, title='Generator Type')
first_legend._legend_box.sep = 8
ax = plt.gca().add_artist(first_legend)

for area in [100/my_scale, 300/my_scale, 500/my_scale, 1500/my_scale]:
    plt.scatter([], [], c='white', s=area, label=str(int(area*my_scale)) + ' MW',edgecolors='black')

legend = plt.legend(bbox_to_anchor=(1.02,0.27), loc="center left", frameon=False,labelspacing=1.6, title='Generator Capacity')
legend._legend_box.sep = 8

plt.savefig('WEST_generators_map_2055.png',dpi=1200, bbox_inches='tight')



##################################### Map of Location of Generators for 2015 #####################################
#Creating an organized dataframe for plotting
all_bus_nums = []
all_gen_types = []
all_caps = []
all_lats = []
all_longs = []
all_colors = []

my_scale = 10

for gen in range(len(CERF_2015_gens)):
    
    sp_bus = CERF_2015_gens.loc[gen,'lmp_zone']
    all_bus_nums.append(sp_bus)
    
    sp_type = CERF_2015_gens.loc[gen,'tech_name']
    all_gen_types.append(sp_type)

    all_caps.append(CERF_2015_gens.loc[gen,'unit_size_mw'])
    
    sp_lat = CERF_2015_gens.loc[gen,'ycoord']
    all_lats.append(sp_lat)
    
    sp_long = CERF_2015_gens.loc[gen,'xcoord']
    all_longs.append(sp_long)
    
    if sp_type == 'NG':
        all_colors.append('#CA9161')
        
    elif sp_type == 'Geothermal':
        all_colors.append('#808000')

    elif sp_type == 'Coal':
        all_colors.append('#949494')
        
    elif sp_type == 'Oil':
        all_colors.append('#000000')
        
    elif sp_type == 'Biomass':
        all_colors.append('#CC78BC')

    elif sp_type == 'Solar':
        all_colors.append('#ECE133')

    elif sp_type == 'OnshoreWind':
        all_colors.append('#029E73')
        
    elif sp_type == 'OffshoreWind':
        all_colors.append('#56B4E9')

    elif sp_type == 'Hydro':
        all_colors.append('#0173B2')

    elif sp_type == 'Nuclear':
        all_colors.append('#D55E00')
        
    else:
        pass

gen_map_df = pd.DataFrame(list(zip(all_bus_nums,all_gen_types,all_caps,all_colors,all_lats,all_longs)),
                          columns=['Bus','Type','Capacity','Color','Latitude','Longitude'])

generators_all_2015 = gen_map_df.loc[:,['Type','Capacity']].copy()

#Finding all gen types and standardizing gen capacities
gen_map_df['Capacity'] = gen_map_df['Capacity'] / my_scale
gen_map_df.sort_values(by='Capacity', ascending=False, inplace=True)
gen_map_df.reset_index(drop=True,inplace=True)
gen_map_df.dropna(inplace=True)

#Changing to type of the dataframe into a geodataframe
geometry = [Point(xy) for xy in zip(gen_map_df['Longitude'],gen_map_df['Latitude'])]
nodes_df = gpd.GeoDataFrame(gen_map_df,crs='ESRI:102003',geometry=geometry)
nodes_df = nodes_df.to_crs("EPSG:3395") 

#Plotting the figure
plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots()
states_gdf.plot(ax=ax,color='None',edgecolor='black',linewidth=0.5,alpha=1)

abc = nodes_df.plot(ax=ax,c=nodes_df['Color'] ,markersize=nodes_df['Capacity'],alpha=0.7,edgecolor='black',linewidth=0.05)

ax.set_box_aspect(1)
ax.set_xlim(-13950000,-11000000)
ax.set_ylim([3500000,6250000])
ax.axis('off')

#Specifying legend
legend_elements = [Line2D([0], [0], marker='o', color='w',markerfacecolor='#CA9161', label='Natural Gas', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#949494', label='Coal', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#000000', label='Oil', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#808000', label='Geothermal', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#CC78BC', label='Biomass', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#ECE133', label='Solar', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#029E73', label='Wind', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#56B4E9', label='Offshore Wind', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#0173B2', label='Hydro', markersize=9),
                   Line2D([0], [0], marker='o', color='w',markerfacecolor='#D55E00', label='Nuclear', markersize=9)]

first_legend = plt.legend(handles=legend_elements, bbox_to_anchor=(1.01,0.72), loc="center left", frameon=False, title='Generator Type')
first_legend._legend_box.sep = 8
ax = plt.gca().add_artist(first_legend)

for area in [100/my_scale, 300/my_scale, 500/my_scale, 1500/my_scale]:
    plt.scatter([], [], c='white', s=area, label=str(int(area*my_scale)) + ' MW',edgecolors='black')

legend = plt.legend(bbox_to_anchor=(1.02,0.27), loc="center left", frameon=False,labelspacing=1.6, title='Generator Capacity')
legend._legend_box.sep = 8

plt.savefig('WEST_generators_map_2015.png',dpi=1200, bbox_inches='tight')


##################################### WECC 2015-2055 Capacity Comparison by Generation Type #####################################

#Calculating total generator capacity by type
gen_cap_2015 = generators_all_2015.groupby('Type').sum()/1000
gen_cap_2055 = generators_all_2055.groupby('Type').sum()/1000

#Creating dictionaries to store capacities and color/generator type lists
cap_GW = {'2015': [], '2055': []}
color_list = ['#CA9161','#808000','#949494','#000000','#CC78BC','#ECE133','#029E73','#56B4E9','#0173B2','#D55E00']
gen_types = ['NG','Geothermal','Coal','Oil','Biomass','Solar','OnshoreWind','OffshoreWind','Hydro','Nuclear']

for g in gen_types:

    try:
        cap_GW['2015'].append(round(gen_cap_2015.loc[g,'Capacity'],1))

    except KeyError:
         cap_GW['2015'].append(0)

    try:
        cap_GW['2055'].append(round(gen_cap_2055.loc[g,'Capacity'],1))

    except KeyError:
         cap_GW['2055'].append(0)


#Plotting the figure
x = np.arange(len(gen_types))
width = 0.33
j = 0

plt.rcParams.update({'font.size':14})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(layout='constrained', figsize=(12,6))

for attribute, measurement in cap_GW.items():
    offset = width * j

    if attribute == '2015':

        rects = ax.bar(x + offset, measurement, width, color=color_list, hatch='//', edgecolor='black')
        ax.bar_label(rects, padding=4,size=11)
    
    elif attribute == '2055':
        rects = ax.bar(x + offset, measurement, width, color=color_list, edgecolor='black')
        ax.bar_label(rects, padding=4,size=11)
       
    j += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Capacity (GW)', weight='bold')
ax.set_xticks(x + width/2, gen_types)
ax.set_xticklabels(['Natural\nGas','Geothermal','Coal','Oil','Biomass','Solar','Onshore\nWind','Offshore\nWind','Hydro','Nuclear'], weight='bold')
ax.set_yticks([0,25,50,75,100,125,150,175,200])

handles = []
patch1 = Patch(facecolor='white', edgecolor='black', hatch='//', label='2015',linewidth=1)
patch2 = Patch(facecolor='white', edgecolor='black', label='2055',linewidth=1)
handles.extend([patch1,patch2])
fig.legend(handles=handles,bbox_to_anchor=(0.98, 0.95), ncol=1, fontsize=14)

plt.tight_layout()
plt.savefig('Capacity_comparison.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()



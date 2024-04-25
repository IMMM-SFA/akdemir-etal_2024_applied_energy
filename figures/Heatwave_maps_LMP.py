import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import networkx as nx
import matplotlib.colors as mcolors

#Reading the necessary results
All_2019_Base = pd.read_csv('../../Data/Organized_Results/2019_Base_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)
All_2019_Cooperative = pd.read_csv('../../Data/Organized_Results/2019_Cooperative_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)
All_2019_Individual = pd.read_csv('../../Data/Organized_Results/2019_Individual_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)
All_2019_Intermediate = pd.read_csv('../../Data/Organized_Results/2019_Intermediate_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)

All_2059_Cooperative = pd.read_csv('../../Data/Organized_Results/2059_Cooperative_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)
All_2059_Individual = pd.read_csv('../../Data/Organized_Results/2059_Individual_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)
All_2059_Intermediate = pd.read_csv('../../Data/Organized_Results/2059_Intermediate_Nodal_LMPs.csv', header=0, index_col=0, parse_dates=True)

#Defining heat wave durations
local_hw_duration_2019 = pd.date_range(start='2019-06-09 00:00:00', end='2019-06-11 23:00:00', freq='H')
wide_hw_duration_2019 = pd.date_range(start='2019-08-04 00:00:00', end='2019-08-06 23:00:00', freq='H')

local_hw_duration_2059 = pd.date_range(start='2059-06-09 00:00:00', end='2059-06-11 23:00:00', freq='H')
wide_hw_duration_2059 = pd.date_range(start='2059-08-04 00:00:00', end='2059-08-06 23:00:00', freq='H')

#Reading all selected nodes
all_selected_nodes = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/selected_nodes_125.csv',header=0)
all_selected_nodes = [*all_selected_nodes['SelectedNodes']]

#Reading all necessary files for plotting the map
df_10k = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/10k_Load.csv',header=0)
df_10k = df_10k.loc[df_10k['Number'].isin(all_selected_nodes)]
df_10k = df_10k.loc[:,['Number', 'Substation Latitude','Substation Longitude']]
geometry = [Point(xy) for xy in zip(df_10k['Substation Longitude'],df_10k['Substation Latitude'])]
nodes_df = gpd.GeoDataFrame(df_10k,crs='epsg:4326',geometry=geometry)
nodes_df = nodes_df.to_crs("EPSG:3395")

states_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.to_crs("EPSG:3395")

NERC_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/NERC_Regions/NERC_Regions_Subregions.shp')
NERC_gdf = NERC_gdf.to_crs("EPSG:3395")
WECC_tr_gdf = NERC_gdf.loc[NERC_gdf['NAME']=='WESTERN ELECTRICITY COORDINATING COUNCIL (WECC)'].copy()


############################## 2059 Heat Wave LMP Plot ##############################

Cooperative_2059_local_LMP =  All_2059_Cooperative.loc[local_hw_duration_2059,:].mean()
Individual_2059_local_LMP =  All_2059_Individual.loc[local_hw_duration_2059,:].mean()
Intermediate_2059_local_LMP =  All_2059_Intermediate.loc[local_hw_duration_2059,:].mean()

Cooperative_2059_wide_LMP =  All_2059_Cooperative.loc[wide_hw_duration_2059,:].mean()
Individual_2059_wide_LMP =  All_2059_Individual.loc[wide_hw_duration_2059,:].mean()
Intermediate_2059_wide_LMP =  All_2059_Intermediate.loc[wide_hw_duration_2059,:].mean()

all_extreme_LMPs = [Cooperative_2059_local_LMP.min(), Cooperative_2059_local_LMP.max(),
                    Individual_2059_local_LMP.min(), Individual_2059_local_LMP.max(),
                    Intermediate_2059_local_LMP.min(), Intermediate_2059_local_LMP.max(),
                    Cooperative_2059_wide_LMP.min(), Cooperative_2059_wide_LMP.max(),
                    Individual_2059_wide_LMP.min(), Individual_2059_wide_LMP.max(),
                    Intermediate_2059_wide_LMP.min(), Intermediate_2059_wide_LMP.max()]

nodes_df['Cooperative_2059_local_LMP'] = Cooperative_2059_local_LMP.values
nodes_df['Individual_2059_local_LMP'] = Individual_2059_local_LMP.values
nodes_df['Intermediate_2059_local_LMP'] = Intermediate_2059_local_LMP.values

nodes_df['Cooperative_2059_wide_LMP'] = Cooperative_2059_wide_LMP.values
nodes_df['Individual_2059_wide_LMP'] = Individual_2059_wide_LMP.values
nodes_df['Intermediate_2059_wide_LMP'] = Intermediate_2059_wide_LMP.values


max_LMP = max(all_extreme_LMPs)
min_LMP = min(all_extreme_LMPs)

#Plotting the figure
#Defining colormap
norm = mpl.colors.BoundaryNorm(boundaries=[0, 50, 100, 200, 300, 500, 750, 1000], ncolors=256, extend='both')

#Defining case names
case_names = ['Cooperative','Intermediate','Individual']

plt.rcParams.update({'font.size': 14})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(3,2, figsize=(12,16))
ax_idx_l = [(0,0), (1,0), (2,0)]
ax_idx_w = [(0,1), (1,1), (2,1)]

f_i = 0

for case in case_names:

    #Local heat wave visualization
    WECC_tr_gdf.plot(ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
    states_gdf.plot(ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

    nodes_df.plot(column=f'{case}_2059_local_LMP',ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],legend=False,cmap='turbo',markersize=30,alpha=1,
                                 edgecolor='black',linewidth=0.3,marker='o',norm=norm)
    
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_box_aspect(1)
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_xlim([-13950000,-11100000])
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_ylim([3500000,6250000])
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_title(f'{case} Case\n(2059 Local Heat Wave)', weight='bold', fontsize=15) 
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].axis('off')

    #Widespread heat wave visualization
    WECC_tr_gdf.plot(ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
    states_gdf.plot(ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

    nodes_df.plot(column=f'{case}_2059_wide_LMP',ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],legend=False,cmap='turbo',markersize=30,alpha=1,
                                 edgecolor='black',linewidth=0.3,marker='o',norm=norm)

    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_box_aspect(1)
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_xlim([-13950000,-11100000])
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_ylim([3500000,6250000])
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_title(f'{case} Case\n(2059 Widespread Heat Wave)', weight='bold', fontsize=15) 
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].axis('off')   
    f_i += 1

cb_ax = fig.add_axes([0.1,-0.02,0.6,0.01])
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='turbo'),orientation='horizontal',cax=cb_ax)
cb_ax.set_xlabel('Average LMP ($/MWh)',fontsize=15, labelpad = 6)

handles = []
patch1 = Patch(facecolor='#7C858D', edgecolor='black',label='CAISO',linewidth=0.5)
patch2 = Patch(facecolor='#ADB5BD', edgecolor='black',label='NorthernGrid',linewidth=0.5)
patch3 = Patch(facecolor='#DCE0E5', edgecolor='black',label='WestConnect',linewidth=0.5)
dot1 = Line2D([0], [0], label='Nodes', color='lavender', marker='o',linestyle='', markeredgecolor='black',markeredgewidth=0.2, markersize=6)
handles.extend([patch1,patch2,patch3,dot1])
fig.legend(handles=handles, bbox_to_anchor=(0.89, 0.01), ncol=1, fontsize=12)

fig.tight_layout(h_pad=0.8)
plt.savefig(f'LMP_distribution_2059_heatwaves.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()


############################## 2019 Heat Wave LMP Plot ##############################

Cooperative_2019_local_LMP =  All_2019_Cooperative.loc[local_hw_duration_2019,:].mean()
Individual_2019_local_LMP =  All_2019_Individual.loc[local_hw_duration_2019,:].mean()
Intermediate_2019_local_LMP =  All_2019_Intermediate.loc[local_hw_duration_2019,:].mean()

Cooperative_2019_wide_LMP =  All_2019_Cooperative.loc[wide_hw_duration_2019,:].mean()
Individual_2019_wide_LMP =  All_2019_Individual.loc[wide_hw_duration_2019,:].mean()
Intermediate_2019_wide_LMP =  All_2019_Intermediate.loc[wide_hw_duration_2019,:].mean()

all_extreme_LMPs = [Cooperative_2019_local_LMP.min(), Cooperative_2019_local_LMP.max(),
                    Individual_2019_local_LMP.min(), Individual_2019_local_LMP.max(),
                    Intermediate_2019_local_LMP.min(), Intermediate_2019_local_LMP.max(),
                    Cooperative_2019_wide_LMP.min(), Cooperative_2019_wide_LMP.max(),
                    Individual_2019_wide_LMP.min(), Individual_2019_wide_LMP.max(),
                    Intermediate_2019_wide_LMP.min(), Intermediate_2019_wide_LMP.max()]

nodes_df['Cooperative_2019_local_LMP'] = Cooperative_2019_local_LMP.values
nodes_df['Individual_2019_local_LMP'] = Individual_2019_local_LMP.values
nodes_df['Intermediate_2019_local_LMP'] = Intermediate_2019_local_LMP.values

nodes_df['Cooperative_2019_wide_LMP'] = Cooperative_2019_wide_LMP.values
nodes_df['Individual_2019_wide_LMP'] = Individual_2019_wide_LMP.values
nodes_df['Intermediate_2019_wide_LMP'] = Intermediate_2019_wide_LMP.values


max_LMP = max(all_extreme_LMPs)
min_LMP = min(all_extreme_LMPs)

#Plotting the figure
#Defining colormap
norm = mpl.colors.BoundaryNorm(boundaries=[30, 40, 50, 60, 70, 80, 90, 100], ncolors=256, extend='both')

#Defining case names
case_names = ['Cooperative','Intermediate','Individual']

plt.rcParams.update({'font.size': 14})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(3,2, figsize=(12,16))
ax_idx_l = [(0,0), (1,0), (2,0)]
ax_idx_w = [(0,1), (1,1), (2,1)]

f_i = 0

for case in case_names:

    #Local heat wave visualization
    WECC_tr_gdf.plot(ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
    states_gdf.plot(ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

    nodes_df.plot(column=f'{case}_2019_local_LMP',ax=ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]],legend=False,cmap='turbo',markersize=30,alpha=1,
                                 edgecolor='black',linewidth=0.3,marker='o',norm=norm)
    
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_box_aspect(1)
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_xlim([-13950000,-11100000])
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_ylim([3500000,6250000])
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].set_title(f'{case} Case\n(2019 Local Heat Wave)', weight='bold', fontsize=15) 
    ax[ax_idx_l[f_i][0], ax_idx_l[f_i][1]].axis('off')

    #Widespread heat wave visualization
    WECC_tr_gdf.plot(ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
    states_gdf.plot(ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

    nodes_df.plot(column=f'{case}_2019_wide_LMP',ax=ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]],legend=False,cmap='turbo',markersize=30,alpha=1,
                                 edgecolor='black',linewidth=0.3,marker='o',norm=norm)

    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_box_aspect(1)
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_xlim([-13950000,-11100000])
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_ylim([3500000,6250000])
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].set_title(f'{case} Case\n(2019 Widespread Heat Wave)', weight='bold', fontsize=15) 
    ax[ax_idx_w[f_i][0], ax_idx_w[f_i][1]].axis('off')   
    f_i += 1

cb_ax = fig.add_axes([0.1,-0.02,0.6,0.01])
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='turbo'),orientation='horizontal',cax=cb_ax)
cb_ax.set_xlabel('Average LMP ($/MWh)',fontsize=15, labelpad = 6)

handles = []
patch1 = Patch(facecolor='#7C858D', edgecolor='black',label='CAISO',linewidth=0.5)
patch2 = Patch(facecolor='#ADB5BD', edgecolor='black',label='NorthernGrid',linewidth=0.5)
patch3 = Patch(facecolor='#DCE0E5', edgecolor='black',label='WestConnect',linewidth=0.5)
dot1 = Line2D([0], [0], label='Nodes', color='lavender', marker='o',linestyle='', markeredgecolor='black',markeredgewidth=0.2, markersize=6)
handles.extend([patch1,patch2,patch3,dot1])
fig.legend(handles=handles, bbox_to_anchor=(0.89, 0.01), ncol=1, fontsize=12)

fig.tight_layout(h_pad=0.8)
plt.savefig(f'LMP_distribution_2019_heatwaves.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()


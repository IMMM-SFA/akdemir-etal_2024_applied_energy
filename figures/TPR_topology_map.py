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

#Specifying the number of nodes to plot
node_nums = 125

#Specifying a line limit threshold that shows only the lines above the limit
line_threshold = 0

#Reading all selected nodes
all_selected_nodes = pd.read_csv(f'../../Data/Supplementary_Data/BA_Topology_Files/selected_nodes_{node_nums}.csv',header=0)
all_selected_nodes = [*all_selected_nodes['SelectedNodes']]

#Reading all necessary files for plotting the map
df = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/10k_Load.csv',header=0)
geometry = [Point(xy) for xy in zip(df['Substation Longitude'],df['Substation Latitude'])]
nodes_df = gpd.GeoDataFrame(df,crs='epsg:4326',geometry=geometry)
nodes_df = nodes_df.to_crs("EPSG:3395")

states_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.to_crs("EPSG:3395")

lines_df = pd.read_csv(f'../../Data/Supplementary_Data/BA_Topology_Files/line_params_{node_nums}.csv',header=0)
lines_df_filt = lines_df.loc[lines_df['limit']>=line_threshold].copy()
lines_df_filt.reset_index(drop=True,inplace=True)

#Reading transmission regions shapefile
NERC_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/NERC_Regions/NERC_Regions_Subregions.shp')
NERC_gdf = NERC_gdf.to_crs("EPSG:3395")
WECC_tr_gdf = NERC_gdf.loc[NERC_gdf['NAME']=='WESTERN ELECTRICITY COORDINATING COUNCIL (WECC)'].copy()

#Finding the start and end nodes of each line
all_line_nodes = []
for a in range(len(lines_df_filt)):
    line_name = lines_df_filt.loc[a,'line']
    splitted_name = line_name.split('_')
    line_list = [int(splitted_name[1]),int(splitted_name[2])]
    all_line_nodes.append(line_list)
    
#Plotting the figure
plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots()

WECC_tr_gdf.plot(ax=ax,color=['#d62828','#0077b6','#ffc300','#d62828'])
states_gdf.plot(ax=ax,color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

G_nodes=nx.Graph()
G_lines = nx.Graph()

for i in all_selected_nodes:
    
    my_pos_1 = nodes_df.loc[nodes_df['Number']==i].geometry.x.values[0]
    my_pos_2 = nodes_df.loc[nodes_df['Number']==i].geometry.y.values[0]
    
    G_nodes.add_node(i,pos=(my_pos_1,my_pos_2))
        
for i in all_selected_nodes:
    
    my_pos_1 = nodes_df.loc[nodes_df['Number']==i].geometry.x.values[0]
    my_pos_2 = nodes_df.loc[nodes_df['Number']==i].geometry.y.values[0]
    
    G_lines.add_node(i,pos=(my_pos_1,my_pos_2))     
    
for i in range(len(all_line_nodes)):
    
    G_lines.add_edge(all_line_nodes[i][0],all_line_nodes[i][1])    

pos_nodes=nx.get_node_attributes(G_nodes,'pos')
nx.draw_networkx_nodes(G_nodes,pos_nodes,node_size=15, node_color='lavender',edgecolors='black',linewidths=0.2)

pos_lines=nx.get_node_attributes(G_lines,'pos')
nx.draw_networkx_edges(G_lines,pos_lines, edge_color='black',alpha=0.4,width=0.4)

ax.set_box_aspect(1)
ax.set_xlim([-13950000,-11100000])
ax.set_ylim([3500000,6250000])

#Creating a custom legend
handles = []
patch1 = Patch(facecolor='#0077b6', edgecolor='black',label='CAISO',linewidth=0.5)
patch2 = Patch(facecolor='#d62828', edgecolor='black',label='WestConnect',linewidth=0.5)
patch3 = Patch(facecolor='#ffc300', edgecolor='black',label='NorthernGrid',linewidth=0.5)
line1 = Line2D([0], [0], label='Transmission Lines', color='black')
dot1 = Line2D([0], [0], label='Nodes', color='lavender', marker='o',linestyle='', markeredgecolor='black',markeredgewidth=0.2, markersize=6)
handles.extend([patch1,patch2,patch3,line1,dot1])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.8, 0.5), ncol=1, fontsize=10)

plt.savefig('Combined_map.png',dpi=500, bbox_inches='tight')


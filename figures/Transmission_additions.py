import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import networkx as nx
import matplotlib.colors as mcolors

#Reading base line capacities
base_line_df = pd.read_csv('../../Data/Raw_Results/2019_Base/Inputs/line_params.csv', header=0)
base_line_df.columns = ['Line_Name','Reactance','Limit']

#Calculating line capacity additions and creating a dataset
cooperative_line_df = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/line_params.csv', header=0)
individual_line_df = pd.read_csv('../../Data/Raw_Results/2059_Individual/Inputs/line_params.csv', header=0)
intermediate_line_df = pd.read_csv('../../Data/Raw_Results/2059_Intermediate/Inputs/line_params.csv', header=0)

base_line_df['Cooperative_Addition'] = [0 if i < 0.1 else i for i in (cooperative_line_df['limit'] - base_line_df['Limit'])]
base_line_df['Intermediate_Addition'] = [0 if i < 0.1 else i for i in (intermediate_line_df['limit'] - base_line_df['Limit'])]
base_line_df['Individual_Addition'] = [0 if i < 0.1 else i for i in (individual_line_df['limit'] - base_line_df['Limit'])]

All_line_data = base_line_df.loc[:,['Line_Name','Cooperative_Addition','Intermediate_Addition','Individual_Addition']].copy()

#Reading all selected nodes
all_selected_nodes = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/selected_nodes_125.csv',header=0)
all_selected_nodes = [*all_selected_nodes['SelectedNodes']]

#Reading all necessary files for plotting the map
df_10k = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/10k_Load.csv',header=0)
geometry = [Point(xy) for xy in zip(df_10k['Substation Longitude'],df_10k['Substation Latitude'])]
nodes_df = gpd.GeoDataFrame(df_10k,crs='epsg:4326',geometry=geometry)
nodes_df = nodes_df.to_crs("EPSG:3395")

states_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.to_crs("EPSG:3395")

NERC_gdf = gpd.read_file('../../Data/Supplementary_Data/Shapefiles/NERC_Regions/NERC_Regions_Subregions.shp')
NERC_gdf = NERC_gdf.to_crs("EPSG:3395")
WECC_tr_gdf = NERC_gdf.loc[NERC_gdf['NAME']=='WESTERN ELECTRICITY COORDINATING COUNCIL (WECC)'].copy()

#Finding maximum and minimum transmission investments
max_inv = All_line_data.max(numeric_only=True).max(numeric_only=True)
min_inv = All_line_data.min(numeric_only=True).min(numeric_only=True)

#Reading general line info
line_info_general = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/line_params_125.csv',header=0)

All_line_data['Initial_Limit'] = base_line_df['Limit']
All_line_data['Region_Type'] = line_info_general['transmission_type']
All_line_data['Length_Mile'] = line_info_general['length_mile']
All_line_data['Inv_cost_$_per_MWmile'] = line_info_general['inv_cost_$_per_MWmile']

print('Total transmission capacity increase in cooperative case is', round(All_line_data['Cooperative_Addition'].sum()),'MW')
print('Total transmission capacity increase in intermediate case is', round(All_line_data['Intermediate_Addition'].sum()),'MW')
print('Total transmission capacity increase in individual case is', round(All_line_data['Individual_Addition'].sum()),'MW')

#Plotting the figure
#Defining colormap
cmap_colors = ['#30123B', '#4669E0', '#2AB9EE', '#2FF19B', '#A1FD3D', '#ECD13A', '#FB8122', '#D23105', '#7A0403']
cmap = mcolors.ListedColormap(colors=cmap_colors)
norm = mcolors.BoundaryNorm(boundaries = [200, 400, 600, 800, 1000, 3000, 5000, 10000], ncolors=len(cmap_colors), extend='both')

norm_case = [200,(200,400),(400,600),(600,800),(800,1000),(1000,3000),(3000,5000),(5000,10000),10000]
norm_case_range = range(0,len(norm_case))

#Defining case names
case_names = ['Cooperative','Intermediate','Individual']

plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(2,2, figsize=(6,6.5))
ax_idx = [(0,0), (0,1), (1,0)]

f_i = 0

for case in case_names:

    WECC_tr_gdf.plot(ax=ax[ax_idx[f_i][0], ax_idx[f_i][1]],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
    states_gdf.plot(ax=ax[ax_idx[f_i][0], ax_idx[f_i][1]],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

    for cb in norm_case_range:
    
        if cb == norm_case_range[0]:
            lines_df_filt = All_line_data.loc[(All_line_data[f'{case}_Addition']<=norm_case[cb]) & (All_line_data[f'{case}_Addition']>0)].copy()
            
        elif cb == norm_case_range[-1]:
            lines_df_filt = All_line_data.loc[All_line_data[f'{case}_Addition']>norm_case[cb]].copy()
        
        else:
            lines_df_filt = All_line_data.loc[(All_line_data[f'{case}_Addition']>norm_case[cb][0]) & (All_line_data[f'{case}_Addition']<=norm_case[cb][1])].copy()
            
        lines_df_filt.reset_index(drop=True,inplace=True)
        
        #Finding the start and end nodes of each line
        unique_line_nodes = []
        all_line_nodes = []
        for a in range(len(lines_df_filt)):
            line_name = lines_df_filt.loc[a,'Line_Name']
            splitted_name = line_name.split('_')
            node_1 = int(splitted_name[1])
            node_2 = int(splitted_name[2])

            if node_1 in unique_line_nodes:
                pass
            else:
                unique_line_nodes.append(node_1)

            if node_2 in unique_line_nodes:
                pass
            else:
                unique_line_nodes.append(node_2)

            line_list = [node_1,node_2]
            all_line_nodes.append(line_list)

        G_lines = nx.Graph()
     
        for i in unique_line_nodes:
            
            my_pos_1 = nodes_df.loc[nodes_df['Number']==i].geometry.x.values[0]
            my_pos_2 = nodes_df.loc[nodes_df['Number']==i].geometry.y.values[0]
            
            G_lines.add_node(i,pos=(my_pos_1,my_pos_2))     
            
        for i in range(len(all_line_nodes)):
            
            G_lines.add_edge(all_line_nodes[i][0],all_line_nodes[i][1], weight = lines_df_filt.loc[i, f'{case}_Addition'])    

        pos_nodes=nx.get_node_attributes(G_lines,'pos')
        nx.draw_networkx_nodes(G_lines,pos_nodes,node_size=8, node_color='lavender',edgecolors='black',linewidths=0.2, ax=ax[ax_idx[f_i][0], ax_idx[f_i][1]])

        edges,weights = zip(*nx.get_edge_attributes(G_lines,'weight').items())
        pos_lines=nx.get_node_attributes(G_lines,'pos')
        nx.draw_networkx_edges(G_lines,pos_lines,width=0.5, edgelist=edges, edge_color=cmap_colors[cb], ax=ax[ax_idx[f_i][0], ax_idx[f_i][1]])

    ax[ax_idx[f_i][0], ax_idx[f_i][1]].set_box_aspect(1)
    ax[ax_idx[f_i][0], ax_idx[f_i][1]].set_xlim([-13950000,-11100000])
    ax[ax_idx[f_i][0], ax_idx[f_i][1]].set_ylim([3500000,6250000])
    ax[ax_idx[f_i][0], ax_idx[f_i][1]].set_title(f'{case} Case', weight='bold', fontsize=10) 
            
    f_i += 1


fig.tight_layout()
ax[1,1].axis('off')
#Creating a custom legend

handles = []
patch1 = Patch(facecolor='#7C858D', edgecolor='black',label='CAISO',linewidth=0.5)
patch2 = Patch(facecolor='#ADB5BD', edgecolor='black',label='NorthernGrid',linewidth=0.5)
patch3 = Patch(facecolor='#DCE0E5', edgecolor='black',label='WestConnect',linewidth=0.5)
dot1 = Line2D([0], [0], label='Nodes', color='lavender', marker='o',linestyle='', markeredgecolor='black',markeredgewidth=0.2, markersize=6)
handles.extend([patch1,patch2,patch3,dot1])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.74, 0.26), ncol=1, fontsize=8)

cb_ax = fig.add_axes([0.59,0.08,0.02,0.39])
fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm),orientation='vertical',cax=cb_ax)
cb_ax.set_ylabel('Transmission Capacity Addition (MW)',fontsize=8, labelpad = 5)

plt.savefig('Transmission_investments_2055.png',dpi=500, bbox_inches='tight')




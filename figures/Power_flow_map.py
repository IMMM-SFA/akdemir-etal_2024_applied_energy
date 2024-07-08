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
import seaborn as sns

#Reading organized data and creating heat wave date ranges
All_2059_Cooperative = pd.read_csv('../../Data/Organized_Results/2059_Cooperative_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2059_Individual = pd.read_csv('../../Data/Organized_Results/2059_Individual_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2059_Intermediate = pd.read_csv('../../Data/Organized_Results/2059_Intermediate_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)

local_hw_duration_2059 = pd.date_range(start='2059-06-09 00:00:00', end='2059-06-11 23:00:00', freq='H')
wide_hw_duration_2059 = pd.date_range(start='2059-08-04 00:00:00', end='2059-08-06 23:00:00', freq='H')
Demand_2059 = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/nodal_load.csv', header=0)
Demand_2059.index = All_2059_Cooperative.index

Base_TEP_data = pd.read_csv(f'../../Data/Supplementary_Data/BA_Topology_Files/line_params_125.csv', header=0)
Interregional_lines = [*Base_TEP_data.loc[Base_TEP_data['transmission_type']=='interregional']['line']]

nodal_info = pd.read_csv('../../Data/Organized_Results/Nodal_information.csv', header=0)
CAISO_nodes = [*nodal_info.loc[nodal_info['TPR']=='CAISO']['Bus_Name']]
NorthernGrid_nodes = [*nodal_info.loc[nodal_info['TPR']=='NorthernGrid']['Bus_Name']]
WestConnect_nodes = [*nodal_info.loc[nodal_info['TPR']=='WestConnect']['Bus_Name']]

WECC_2059_demand = Demand_2059.sum(axis=1)
CAISO_2059_demand = Demand_2059.loc[:,CAISO_nodes].sum(axis=1)
NorthernGrid_2059_demand = Demand_2059.loc[:,NorthernGrid_nodes].sum(axis=1)
WestConnect_2059_demand = Demand_2059.loc[:,WestConnect_nodes].sum(axis=1)

#Calculating interchange between TPRs
Flow_data_2059 = pd.read_parquet('../../Data/Raw_Results/2059_Cooperative/Outputs/flow.parquet')
all_lines = Flow_data_2059['Line'].unique()

Flow_data_organized_2059 = pd.DataFrame(np.zeros((8760,len(all_lines))),columns=all_lines)
for line in all_lines:
    Sp_line_flow = Flow_data_2059.loc[Flow_data_2059['Line']==line]['Value'].values
    Flow_data_organized_2059.loc[:,line] = Sp_line_flow
Flow_data_organized_2059.index = All_2059_Cooperative.index

Line_node_matrix = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/line_to_bus.csv', header=0)
Line_node_matrix = Line_node_matrix.loc[Line_node_matrix['line'].isin(Interregional_lines)].reset_index(drop=True)

#Calculating total import/exports
#Negative means exports, positive means imports in TPR_hourly_interchange_2059 dataframe
TPR_hourly_interchange_2059 = pd.DataFrame(np.zeros((8760,3)), columns=['CAISO_Interchange','WestConnect_Interchange','NorthernGrid_Interchange'], index=All_2059_Cooperative.index)

for node in CAISO_nodes:

    up_lines = Line_node_matrix.loc[Line_node_matrix[node]>0]['line'].values
    if len(up_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,up_lines]*-1
        TPR_hourly_interchange_2059['CAISO_Interchange'] = TPR_hourly_interchange_2059['CAISO_Interchange'].values + sp_line_flows.sum(axis=1).values
        
    down_lines = Line_node_matrix.loc[Line_node_matrix[node]<0]['line'].values
    if len(down_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,down_lines].sum(axis=1)
        TPR_hourly_interchange_2059['CAISO_Interchange'] = TPR_hourly_interchange_2059['CAISO_Interchange'].values + sp_line_flows.values

for node in NorthernGrid_nodes:

    up_lines = Line_node_matrix.loc[Line_node_matrix[node]>0]['line'].values
    if len(up_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,up_lines]*-1
        TPR_hourly_interchange_2059['NorthernGrid_Interchange'] = TPR_hourly_interchange_2059['NorthernGrid_Interchange'].values + sp_line_flows.sum(axis=1).values
        
    down_lines = Line_node_matrix.loc[Line_node_matrix[node]<0]['line'].values
    if len(down_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,down_lines].sum(axis=1)
        TPR_hourly_interchange_2059['NorthernGrid_Interchange'] = TPR_hourly_interchange_2059['NorthernGrid_Interchange'].values + sp_line_flows.values

for node in WestConnect_nodes:

    up_lines = Line_node_matrix.loc[Line_node_matrix[node]>0]['line'].values
    if len(up_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,up_lines]*-1
        TPR_hourly_interchange_2059['WestConnect_Interchange'] = TPR_hourly_interchange_2059['WestConnect_Interchange'].values + sp_line_flows.sum(axis=1).values
        
    down_lines = Line_node_matrix.loc[Line_node_matrix[node]<0]['line'].values
    if len(down_lines) == 0:
        pass

    else:
        sp_line_flows = Flow_data_organized_2059.loc[:,down_lines].sum(axis=1)
        TPR_hourly_interchange_2059['WestConnect_Interchange'] = TPR_hourly_interchange_2059['WestConnect_Interchange'].values + sp_line_flows.values

CAISO_yearly_mean_interchange_2059 = TPR_hourly_interchange_2059['CAISO_Interchange'].mean()
CAISO_local_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_Interchange'].mean()
CAISO_wide_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_Interchange'].mean()

WestConnect_yearly_mean_interchange_2059 = TPR_hourly_interchange_2059['WestConnect_Interchange'].mean()
WestConnect_local_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'WestConnect_Interchange'].mean()
WestConnect_wide_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'WestConnect_Interchange'].mean()

NorthernGrid_yearly_mean_interchange_2059 = TPR_hourly_interchange_2059['NorthernGrid_Interchange'].mean()
NorthernGrid_local_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'NorthernGrid_Interchange'].mean()
NorthernGrid_wide_hw_mean_interchange_2059 = TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'NorthernGrid_Interchange'].mean()

#Calculating import/exports between TPRs
#Positive means import to first TPR, negative means export from first TPR
Between_TPR_hourly_interchange_2059 = pd.DataFrame(np.zeros((8760,3)), columns=['CAISO_WestConnect_Interchange','CAISO_NorthernGrid_Interchange','NorthernGrid_WestConnect_Interchange'], index=All_2059_Cooperative.index)

for node in CAISO_nodes:

    up_lines = Line_node_matrix.loc[Line_node_matrix[node]>0]['line'].values
    if len(up_lines) == 0:
        pass

    else:

        for i in up_lines:

            spt_name = i.split('_')

            first_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[1])]['TPR'].values[0]
            second_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[2])]['TPR'].values[0]

            sp_line_flows = Flow_data_organized_2059.loc[:,i]*-1

            if first_TPR == 'CAISO':
                Between_TPR_hourly_interchange_2059[f'CAISO_{second_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'CAISO_{second_TPR}_Interchange'].values + sp_line_flows.values

            else:
                Between_TPR_hourly_interchange_2059[f'CAISO_{first_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'CAISO_{first_TPR}_Interchange'].values + sp_line_flows.values

        
    down_lines = Line_node_matrix.loc[Line_node_matrix[node]<0]['line'].values
    if len(down_lines) == 0:
        pass

    else:

        for i in down_lines:

            spt_name = i.split('_')

            first_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[1])]['TPR'].values[0]
            second_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[2])]['TPR'].values[0]

            sp_line_flows = Flow_data_organized_2059.loc[:,i]

            if first_TPR == 'CAISO':
                Between_TPR_hourly_interchange_2059[f'CAISO_{second_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'CAISO_{second_TPR}_Interchange'].values + sp_line_flows.values

            else:
                Between_TPR_hourly_interchange_2059[f'CAISO_{first_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'CAISO_{first_TPR}_Interchange'].values + sp_line_flows.values

for node in NorthernGrid_nodes:

    up_lines = Line_node_matrix.loc[Line_node_matrix[node]>0]['line'].values
    if len(up_lines) == 0:
        pass

    else:

        for i in up_lines:

            spt_name = i.split('_')

            first_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[1])]['TPR'].values[0]
            second_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[2])]['TPR'].values[0]
            
            if first_TPR == 'CAISO' or second_TPR == 'CAISO':
                pass

            else:
                sp_line_flows = Flow_data_organized_2059.loc[:,i]*-1

                if first_TPR == 'NorthernGrid':
                    Between_TPR_hourly_interchange_2059[f'NorthernGrid_{second_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'NorthernGrid_{second_TPR}_Interchange'].values + sp_line_flows.values

                else:
                    Between_TPR_hourly_interchange_2059[f'NorthernGrid_{first_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'NorthernGrid_{first_TPR}_Interchange'].values + sp_line_flows.values

        
    down_lines = Line_node_matrix.loc[Line_node_matrix[node]<0]['line'].values
    if len(down_lines) == 0:
        pass

    else:

        for i in down_lines:

            spt_name = i.split('_')

            first_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[1])]['TPR'].values[0]
            second_TPR = nodal_info.loc[nodal_info['Bus_Number']==int(spt_name[2])]['TPR'].values[0]

            if first_TPR == 'CAISO' or second_TPR == 'CAISO':
                pass

            else:
                sp_line_flows = Flow_data_organized_2059.loc[:,i]

                if first_TPR == 'NorthernGrid':
                    Between_TPR_hourly_interchange_2059[f'NorthernGrid_{second_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'NorthernGrid_{second_TPR}_Interchange'].values + sp_line_flows.values

                else:
                    Between_TPR_hourly_interchange_2059[f'NorthernGrid_{first_TPR}_Interchange'] = Between_TPR_hourly_interchange_2059[f'NorthernGrid_{first_TPR}_Interchange'].values + sp_line_flows.values


CAISO_WestConnect_yearly_mean_interchange_2059 = Between_TPR_hourly_interchange_2059['CAISO_WestConnect_Interchange'].mean()
CAISO_WestConnect_local_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_WestConnect_Interchange'].mean()
CAISO_WestConnect_wide_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_WestConnect_Interchange'].mean()

CAISO_NorthernGrid_yearly_mean_interchange_2059 = Between_TPR_hourly_interchange_2059['CAISO_NorthernGrid_Interchange'].mean()
CAISO_NorthernGrid_local_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_NorthernGrid_Interchange'].mean()
CAISO_NorthernGrid_wide_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_NorthernGrid_Interchange'].mean()

NorthernGrid_WestConnect_yearly_mean_interchange_2059 = Between_TPR_hourly_interchange_2059['NorthernGrid_WestConnect_Interchange'].mean()
NorthernGrid_WestConnect_local_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'NorthernGrid_WestConnect_Interchange'].mean()
NorthernGrid_WestConnect_wide_hw_mean_interchange_2059 = Between_TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'NorthernGrid_WestConnect_Interchange'].mean()

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


#Plotting the figure
plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(4,3, figsize=(9.5,12), sharey='row')


WECC_tr_gdf.plot(ax=ax[0,0],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
states_gdf.plot(ax=ax[0,0],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

ax[0,0].set_xlim([-13950000,-11100000])
ax[0,0].set_ylim([3500000,6250000])
ax[0,0].set_title(f'Annual Average\nInterregional Exchange', weight='bold', fontsize=10) 
ax[0,0].axis('off')

ax[0,0].text(0.26, 0.5, f"{round(CAISO_NorthernGrid_yearly_mean_interchange_2059)} MWh",
            ha="center", va="center", rotation=50,transform=ax[0,0].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,0].text(0.48, 0.2, f"{round(CAISO_WestConnect_yearly_mean_interchange_2059)} MWh",
            ha="center", va="center",transform=ax[0,0].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,0].text(0.65, 0.5, f"{abs(round(NorthernGrid_WestConnect_yearly_mean_interchange_2059))} MWh",
            ha="center", va="center",rotation=-50, transform=ax[0,0].transAxes,size=9.5,
            bbox=dict(boxstyle="rarrow,pad=0.3",fc="white", ec="black"))


WECC_tr_gdf.plot(ax=ax[0,1],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
states_gdf.plot(ax=ax[0,1],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

ax[0,1].set_xlim([-13950000,-11100000])
ax[0,1].set_ylim([3500000,6250000])
ax[0,1].set_title(f'Local Heat Wave\nAverage Interregional Exchange', weight='bold', fontsize=10) 
ax[0,1].axis('off')

ax[0,1].text(0.26, 0.5, f"{round(CAISO_NorthernGrid_local_hw_mean_interchange_2059)} MWh",
            ha="center", va="center", rotation=50,transform=ax[0,1].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,1].text(0.48, 0.2, f"{round(CAISO_WestConnect_local_hw_mean_interchange_2059)} MWh",
            ha="center", va="center",transform=ax[0,1].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,1].text(0.65, 0.5, f"{abs(round(NorthernGrid_WestConnect_local_hw_mean_interchange_2059))} MWh",
            ha="center", va="center",rotation=-50, transform=ax[0,1].transAxes,size=9.5,
            bbox=dict(boxstyle="rarrow,pad=0.3",fc="white", ec="black"))


WECC_tr_gdf.plot(ax=ax[0,2],color=['#DCE0E5','#7C858D','#ADB5BD','#DCE0E5'])
states_gdf.plot(ax=ax[0,2],color='None',edgecolor='gray',linewidth=0.5,alpha=0.4)

ax[0,2].set_xlim([-13950000,-11100000])
ax[0,2].set_ylim([3500000,6250000])
ax[0,2].set_title(f'Widespread Heat Wave\nAverage Interregional Exchange', weight='bold', fontsize=10) 
ax[0,2].axis('off')

ax[0,2].text(0.26, 0.5, f"{round(CAISO_NorthernGrid_wide_hw_mean_interchange_2059)} MWh",
            ha="center", va="center", rotation=50,transform=ax[0,2].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,2].text(0.48, 0.2, f"{round(CAISO_WestConnect_wide_hw_mean_interchange_2059)} MWh",
            ha="center", va="center",transform=ax[0,2].transAxes,size=9.5,
            bbox=dict(boxstyle="larrow,pad=0.3",fc="white", ec="black"))

ax[0,2].text(0.65, 0.5, f"{abs(round(NorthernGrid_WestConnect_wide_hw_mean_interchange_2059))} MWh",
            ha="center", va="center",rotation=-50, transform=ax[0,2].transAxes,size=9.5,
            bbox=dict(boxstyle="rarrow,pad=0.3",fc="white", ec="black"))


handles = []
patch1 = Patch(facecolor='#7C858D', edgecolor='black',label='CAISO',linewidth=0.5)
patch2 = Patch(facecolor='#ADB5BD', edgecolor='black',label='NorthernGrid',linewidth=0.5)
patch3 = Patch(facecolor='#DCE0E5', edgecolor='black',label='WestConnect',linewidth=0.5)
handles.extend([patch1,patch2,patch3])
fig.legend(handles=handles,loc='center', bbox_to_anchor=(0.528, 0.75), ncol=3, fontsize=8)





CAISO_net_demand_all_year = CAISO_2059_demand - All_2059_Cooperative.loc[:,'CAISO_Solar_Gen'] - All_2059_Cooperative.loc[:,'CAISO_Wind_Gen'] - All_2059_Cooperative.loc[:,'CAISO_OffshoreWind_Gen']
CAISO_net_demand_local_hw = CAISO_2059_demand.loc[local_hw_duration_2059] - All_2059_Cooperative.loc[local_hw_duration_2059,'CAISO_Solar_Gen'] - All_2059_Cooperative.loc[local_hw_duration_2059,'CAISO_Wind_Gen'] - All_2059_Cooperative.loc[local_hw_duration_2059,'CAISO_OffshoreWind_Gen']
CAISO_net_demand_wide_hw = CAISO_2059_demand.loc[wide_hw_duration_2059] - All_2059_Cooperative.loc[wide_hw_duration_2059,'CAISO_Solar_Gen'] - All_2059_Cooperative.loc[wide_hw_duration_2059,'CAISO_Wind_Gen'] - All_2059_Cooperative.loc[wide_hw_duration_2059,'CAISO_OffshoreWind_Gen']

ax[1,0].plot(range(0,24), CAISO_net_demand_all_year.groupby([CAISO_net_demand_all_year.index.hour]).mean(), color='#0173B2')
ax[1,0].plot(range(0,24), TPR_hourly_interchange_2059['CAISO_Interchange'].groupby([TPR_hourly_interchange_2059.index.hour]).mean(), color='#DE8F05')
ax[1,0].set_yticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000])
ax[1,0].set_xlim([0,23])
ax[1,0].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[1,0].set_xlabel('Hour of Day', weight='bold', fontsize=9)
ax[1,0].set_ylabel('CAISO Net Demand and Imports (MWh)', weight='bold', fontsize=9)

max_deficit_1 = (CAISO_net_demand_all_year.groupby([CAISO_net_demand_all_year.index.hour]).mean() - TPR_hourly_interchange_2059['CAISO_Interchange'].groupby([TPR_hourly_interchange_2059.index.hour]).mean()).max()
max_deficit_1_hour = (CAISO_net_demand_all_year.groupby([CAISO_net_demand_all_year.index.hour]).mean() - TPR_hourly_interchange_2059['CAISO_Interchange'].groupby([TPR_hourly_interchange_2059.index.hour]).mean()).argmax()

ax[1,0].annotate('',(max_deficit_1_hour+0.12, CAISO_net_demand_all_year.groupby([CAISO_net_demand_all_year.index.hour]).mean()[max_deficit_1_hour]),
            xytext=(max_deficit_1_hour+0.12, TPR_hourly_interchange_2059['CAISO_Interchange'].groupby([TPR_hourly_interchange_2059.index.hour]).mean()[max_deficit_1_hour]),
            arrowprops=dict(color='#000000', arrowstyle='<->', linewidth=1.5),
            fontsize=8)

ax[1,0].text(0.835, 0.42, f"{round(max_deficit_1)}\nMWh\nDifference",
            ha="center", va="center",transform=ax[1,0].transAxes,size=8,color='black')

ax[1,1].plot(range(0,24), CAISO_net_demand_local_hw.groupby([local_hw_duration_2059.hour]).mean(), color='#0173B2')
ax[1,1].plot(range(0,24), TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_Interchange'].groupby([local_hw_duration_2059.hour]).mean(), color='#DE8F05')
ax[1,1].set_yticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000])
ax[1,1].set_xlim([0,23])
ax[1,1].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[1,1].set_xlabel('Hour of Day', weight='bold', fontsize=9)

max_deficit_2 = (CAISO_net_demand_local_hw.groupby([local_hw_duration_2059.hour]).mean() - TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_Interchange'].groupby([local_hw_duration_2059.hour]).mean()).max()
max_deficit_2_hour = (CAISO_net_demand_local_hw.groupby([local_hw_duration_2059.hour]).mean() - TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_Interchange'].groupby([local_hw_duration_2059.hour]).mean()).argmax()

ax[1,1].annotate('',(max_deficit_2_hour+0.12, CAISO_net_demand_local_hw.groupby([local_hw_duration_2059.hour]).mean()[max_deficit_2_hour]),
            xytext=(max_deficit_2_hour+0.12, TPR_hourly_interchange_2059.loc[local_hw_duration_2059,'CAISO_Interchange'].groupby([local_hw_duration_2059.hour]).mean()[max_deficit_2_hour]),
            arrowprops=dict(color='#000000', arrowstyle='<->', linewidth=1.5),
            fontsize=8)

ax[1,1].text(0.835, 0.57, f"{round(max_deficit_2)}\nMWh\nDifference",
            ha="center", va="center",transform=ax[1,1].transAxes,size=8,color='black')

ax[1,2].plot(range(0,24), CAISO_net_demand_wide_hw.groupby([wide_hw_duration_2059.hour]).mean(), color='#0173B2')
ax[1,2].plot(range(0,24), TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_Interchange'].groupby([wide_hw_duration_2059.hour]).mean(), color='#DE8F05')
ax[1,2].set_yticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000])
ax[1,2].set_xlim([0,23])
ax[1,2].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[1,2].set_xlabel('Hour of Day', weight='bold', fontsize=9)

max_deficit_3 = (CAISO_net_demand_wide_hw.groupby([wide_hw_duration_2059.hour]).mean() - TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_Interchange'].groupby([wide_hw_duration_2059.hour]).mean()).max()
max_deficit_3_hour = (CAISO_net_demand_wide_hw.groupby([wide_hw_duration_2059.hour]).mean() - TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_Interchange'].groupby([wide_hw_duration_2059.hour]).mean()).argmax()

ax[1,2].annotate('',(max_deficit_3_hour+0.12, CAISO_net_demand_wide_hw.groupby([wide_hw_duration_2059.hour]).mean()[max_deficit_3_hour]),
            xytext=(max_deficit_3_hour+0.12, TPR_hourly_interchange_2059.loc[wide_hw_duration_2059,'CAISO_Interchange'].groupby([wide_hw_duration_2059.hour]).mean()[max_deficit_3_hour]),
            arrowprops=dict(color='#000000', arrowstyle='<->', linewidth=1.5),
            fontsize=8)

ax[1,2].text(0.835, 0.35, f"{round(max_deficit_3)}\nMWh\nDifference",
            ha="center", va="center",transform=ax[1,2].transAxes,size=8,color='black')

handles = []
line1 = Line2D([0], [0], label='Net Demand', color='#0173B2')
line2 = Line2D([0], [0], label='Net Imports', color='#DE8F05')
handles.extend([line1,line2])
ax[1,0].legend(handles=handles, bbox_to_anchor=(0.453, 1), ncol=1, fontsize=8)

Yearly_Solar_Two_TPRs = All_2059_Cooperative['NorthernGrid_Solar_Gen'] + All_2059_Cooperative['WestConnect_Solar_Gen']
Yearly_Wind_Two_TPRs = All_2059_Cooperative['NorthernGrid_Wind_Gen'] + All_2059_Cooperative['WestConnect_Wind_Gen']

Yearly_Solar_Two_TPRs_curtailment = All_2059_Cooperative['NorthernGrid_Curtailed_Solar'] + All_2059_Cooperative['WestConnect_Curtailed_Solar']
Yearly_Wind_Two_TPRs_curtailment = All_2059_Cooperative['NorthernGrid_Curtailed_Wind'] + All_2059_Cooperative['WestConnect_Curtailed_Wind']

Ren_Gen_1 = {
    'Wind Generation': Yearly_Wind_Two_TPRs.groupby([Yearly_Wind_Two_TPRs.index.hour]).mean(),
    'Wind Curtailment': Yearly_Wind_Two_TPRs_curtailment.groupby([Yearly_Wind_Two_TPRs_curtailment.index.hour]).mean(),
    'Solar Generation': Yearly_Solar_Two_TPRs.groupby([Yearly_Solar_Two_TPRs.index.hour]).mean(),
    'Solar Curtailment': Yearly_Solar_Two_TPRs_curtailment.groupby([Yearly_Solar_Two_TPRs_curtailment.index.hour]).mean()}

ax[2,0].stackplot(range(0,24), Ren_Gen_1.values(), labels=Ren_Gen_1.keys(), colors=['#56B4E9','#ACDAF4','#ECE133','#F5EF98'])
ax[2,0].set_yticks([0,20000,40000,60000,80000,100000,120000,140000])
ax[2,0].set_xlim([0,23])
ax[2,0].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[2,0].set_xlabel('Hour of Day', weight='bold', fontsize=9)
ax[2,0].set_ylabel('Solar/Wind Generation and Curtailment\nin WestConnect and NorthernGrid (MWh)', weight='bold', fontsize=9)

Ren_Gen_2 = {
    'Wind Generation': Yearly_Wind_Two_TPRs.loc[local_hw_duration_2059].groupby([local_hw_duration_2059.hour]).mean(),
    'Wind Curtailment': Yearly_Wind_Two_TPRs_curtailment.loc[local_hw_duration_2059].groupby([local_hw_duration_2059.hour]).mean(),
    'Solar Generation': Yearly_Solar_Two_TPRs.loc[local_hw_duration_2059].groupby([local_hw_duration_2059.hour]).mean(),
    'Solar Curtailment': Yearly_Solar_Two_TPRs_curtailment.loc[local_hw_duration_2059].groupby([local_hw_duration_2059.hour]).mean()}

ax[2,1].stackplot(range(0,24), Ren_Gen_2.values(), labels=Ren_Gen_2.keys(), colors=['#56B4E9','#ACDAF4','#ECE133','#F5EF98'])
ax[2,1].set_yticks([0,20000,40000,60000,80000,100000,120000,140000])
ax[2,1].set_xlim([0,23])
ax[2,1].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[2,1].set_xlabel('Hour of Day', weight='bold', fontsize=9)

Ren_Gen_3 = {
    'Wind Generation': Yearly_Wind_Two_TPRs.loc[wide_hw_duration_2059].groupby([wide_hw_duration_2059.hour]).mean(),
    'Wind Curtailment': Yearly_Wind_Two_TPRs_curtailment.loc[wide_hw_duration_2059].groupby([wide_hw_duration_2059.hour]).mean(),
    'Solar Generation': Yearly_Solar_Two_TPRs.loc[wide_hw_duration_2059].groupby([wide_hw_duration_2059.hour]).mean(),
    'Solar Curtailment': Yearly_Solar_Two_TPRs_curtailment.loc[wide_hw_duration_2059].groupby([wide_hw_duration_2059.hour]).mean()}

ax[2,2].stackplot(range(0,24), Ren_Gen_3.values(), labels=Ren_Gen_3.keys(), colors=['#56B4E9','#ACDAF4','#ECE133','#F5EF98'])
ax[2,2].set_yticks([0,20000,40000,60000,80000,100000,120000,140000])
ax[2,2].set_xlim([0,23])
ax[2,2].set_xticks([0,2,4,6,8,10,12,14,16,18,20,22])
ax[2,2].set_xlabel('Hour of Day', weight='bold', fontsize=9)

handles = []
patch1 = Patch(facecolor='#ECE133', edgecolor='black',label='Solar Generation',linewidth=0.5)
patch2 = Patch(facecolor='#F5EF98', edgecolor='black',label='Solar Curtailment',linewidth=0.5)
patch3 = Patch(facecolor='#56B4E9', edgecolor='black',label='Wind Generation',linewidth=0.5)
patch4 = Patch(facecolor='#ACDAF4', edgecolor='black',label='Wind Curtailment',linewidth=0.5)
handles.extend([patch1,patch2,patch3,patch4])
ax[2,2].legend(handles=handles, bbox_to_anchor=(0.545, 1), ncol=1, fontsize=8)

sns.kdeplot(data=All_2059_Cooperative, x='CAISO_Weighted_LMP', ax=ax[3,0], color='#029E73')
sns.kdeplot(data=All_2059_Intermediate, x='CAISO_Weighted_LMP', ax=ax[3,0], color='#ECE133')
sns.kdeplot(data=All_2059_Individual, x='CAISO_Weighted_LMP', ax=ax[3,0], color='#D55E00')
ax[3,0].set_yticks([0,0.0005,0.001,0.0015,0.002,0.0025,0.003,0.0035,0.004])
ax[3,0].set_xlim([-500,2000])
ax[3,0].set_xticks([-500,0,500,1000,1500,2000])
ax[3,0].set_xlabel('CAISO Hourly LMP ($/MWh)', weight='bold', fontsize=9)
ax[3,0].set_ylabel('Proportion', weight='bold', fontsize=9)

sns.kdeplot(data=All_2059_Cooperative.loc[local_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,1], color='#029E73')
sns.kdeplot(data=All_2059_Intermediate.loc[local_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,1], color='#ECE133')
sns.kdeplot(data=All_2059_Individual.loc[local_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,1], color='#D55E00')
ax[3,1].set_yticks([0,0.0005,0.001,0.0015,0.002,0.0025,0.003,0.0035,0.004])
ax[3,1].set_xlim([-500,2000])
ax[3,1].set_xticks([-500,0,500,1000,1500,2000])
ax[3,1].set_xlabel('CAISO Hourly LMP ($/MWh)', weight='bold', fontsize=9)

sns.kdeplot(data=All_2059_Cooperative.loc[wide_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,2], color='#029E73')
sns.kdeplot(data=All_2059_Intermediate.loc[wide_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,2], color='#ECE133')
sns.kdeplot(data=All_2059_Individual.loc[wide_hw_duration_2059,:], x='CAISO_Weighted_LMP', ax=ax[3,2], color='#D55E00')
ax[3,2].set_yticks([0,0.0005,0.001,0.0015,0.002,0.0025,0.003,0.0035,0.004])
ax[3,2].set_xlim([-500,2000])
ax[3,2].set_xticks([-500,0,500,1000,1500,2000])
ax[3,2].set_xlabel('CAISO Hourly LMP ($/MWh)', weight='bold', fontsize=9)

handles = []
line1 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line2 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line3 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3])
ax[3,2].legend(handles=handles, bbox_to_anchor=(0.562, 1), ncol=1, fontsize=8)

plt.tight_layout()
plt.savefig('Interchange_trend_2059.png', dpi=500, bbox_inches='tight')
plt.show()
plt.clf()






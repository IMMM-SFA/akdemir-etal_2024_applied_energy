import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Reading the necessary results
All_2019_Cooperative = pd.read_csv('../../Data/Organized_Results/2019_Cooperative_All_Hourly_Results.csv', header=0, index_col=0)
All_2019_Individual = pd.read_csv('../../Data/Organized_Results/2019_Individual_All_Hourly_Results.csv', header=0, index_col=0)
All_2019_Intermediate = pd.read_csv('../../Data/Organized_Results/2019_Intermediate_All_Hourly_Results.csv', header=0, index_col=0)

All_2059_Cooperative = pd.read_csv('../../Data/Organized_Results/2059_Cooperative_All_Hourly_Results.csv', header=0, index_col=0)
All_2059_Individual = pd.read_csv('../../Data/Organized_Results/2059_Individual_All_Hourly_Results.csv', header=0, index_col=0)
All_2059_Intermediate = pd.read_csv('../../Data/Organized_Results/2059_Intermediate_All_Hourly_Results.csv', header=0, index_col=0)

nuclear_2019 = pd.read_csv('../../Data/Raw_Results/2019_Base/Inputs/must_run.csv', header=0)
nuclear_2059 = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/must_run.csv', header=0)

demand_2019 = pd.read_csv('../../Data/Raw_Results/2019_Base/Inputs/nodal_load.csv', header=0)
demand_2059 = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/nodal_load.csv', header=0)

#Reading nodal information
nodal_info = pd.read_csv('../../Data/Organized_Results/Nodal_information.csv', header=0)
CAISO_nodes = nodal_info.loc[nodal_info['TPR']=='CAISO']['Bus_Name'].values
WestConnect_nodes = nodal_info.loc[nodal_info['TPR']=='WestConnect']['Bus_Name'].values
NorthernGrid_nodes = nodal_info.loc[nodal_info['TPR']=='NorthernGrid']['Bus_Name'].values

#CAISO 2019
#Reading and calculating yearly generation and demand
CAISO_nuc_2019 = list(set(nuclear_2019.columns) & set(CAISO_nodes))
nuclear_gen_2019_CAISO = nuclear_2019.loc[:,CAISO_nuc_2019].sum().sum()*8760/10**6

eff_demand_cooperative_CAISO_2019 = (demand_2019.loc[:,CAISO_nodes].sum().sum() - All_2019_Cooperative['CAISO_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_CAISO_2019 = (demand_2019.loc[:,CAISO_nodes].sum().sum() - All_2019_Intermediate['CAISO_Unserved_Energy'].sum())/10**6
eff_demand_individual_CAISO_2019 = (demand_2019.loc[:,CAISO_nodes].sum().sum() - All_2019_Individual['CAISO_Unserved_Energy'].sum())/10**6

Cooperative_2019_tot_gen_CAISO = All_2019_Cooperative.loc[:,['CAISO_Coal_Gen', 'CAISO_Oil_Gen',
       'CAISO_Gas_Gen', 'CAISO_Biomass_Gen', 'CAISO_Geothermal_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen']].sum().sum()/10**6

Individual_2019_tot_gen_CAISO = All_2019_Individual.loc[:,['CAISO_Coal_Gen', 'CAISO_Oil_Gen',
       'CAISO_Gas_Gen', 'CAISO_Biomass_Gen', 'CAISO_Geothermal_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen']].sum().sum()/10**6

Intermediate_2019_tot_gen_CAISO = All_2019_Intermediate.loc[:,['CAISO_Coal_Gen', 'CAISO_Oil_Gen',
       'CAISO_Gas_Gen', 'CAISO_Biomass_Gen', 'CAISO_Geothermal_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen']].sum().sum()/10**6

#CAISO 2059
CAISO_nuc_2059 = list(set(nuclear_2059.columns) & set(CAISO_nodes))
nuclear_gen_2059_CAISO = nuclear_2059.loc[:,CAISO_nuc_2059].sum().sum()*8760/10**6

eff_demand_cooperative_CAISO_2059 = (demand_2059.loc[:,CAISO_nodes].sum().sum() - All_2059_Cooperative['CAISO_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_CAISO_2059 = (demand_2059.loc[:,CAISO_nodes].sum().sum() - All_2059_Intermediate['CAISO_Unserved_Energy'].sum())/10**6
eff_demand_individual_CAISO_2059 = (demand_2059.loc[:,CAISO_nodes].sum().sum() - All_2059_Individual['CAISO_Unserved_Energy'].sum())/10**6

Cooperative_2059_tot_gen_CAISO = All_2059_Cooperative.loc[:,['CAISO_Gas_Gen', 'CAISO_Biomass_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen',
       'CAISO_OffshoreWind_Gen']].sum().sum()/10**6

Individual_2059_tot_gen_CAISO = All_2059_Individual.loc[:,['CAISO_Gas_Gen', 'CAISO_Biomass_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen',
       'CAISO_OffshoreWind_Gen']].sum().sum()/10**6

Intermediate_2059_tot_gen_CAISO = All_2059_Intermediate.loc[:,['CAISO_Gas_Gen', 'CAISO_Biomass_Gen',
       'CAISO_Hydro_Gen', 'CAISO_Solar_Gen', 'CAISO_Wind_Gen',
       'CAISO_OffshoreWind_Gen']].sum().sum()/10**6



#NorthernGrid 2019
#Reading and calculating yearly generation and demand
NorthernGrid_nuc_2019 = list(set(nuclear_2019.columns) & set(NorthernGrid_nodes))
nuclear_gen_2019_NorthernGrid = nuclear_2019.loc[:,NorthernGrid_nuc_2019].sum().sum()*8760/10**6

eff_demand_cooperative_NorthernGrid_2019 = (demand_2019.loc[:,NorthernGrid_nodes].sum().sum() - All_2019_Cooperative['NorthernGrid_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_NorthernGrid_2019 = (demand_2019.loc[:,NorthernGrid_nodes].sum().sum() - All_2019_Intermediate['NorthernGrid_Unserved_Energy'].sum())/10**6
eff_demand_individual_NorthernGrid_2019 = (demand_2019.loc[:,NorthernGrid_nodes].sum().sum() - All_2019_Individual['NorthernGrid_Unserved_Energy'].sum())/10**6

Cooperative_2019_tot_gen_NorthernGrid = All_2019_Cooperative.loc[:,['NorthernGrid_Coal_Gen', 'NorthernGrid_Oil_Gen',
       'NorthernGrid_Gas_Gen', 'NorthernGrid_Biomass_Gen', 'NorthernGrid_Geothermal_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6

Individual_2019_tot_gen_NorthernGrid = All_2019_Individual.loc[:,['NorthernGrid_Coal_Gen', 'NorthernGrid_Oil_Gen',
       'NorthernGrid_Gas_Gen', 'NorthernGrid_Biomass_Gen', 'NorthernGrid_Geothermal_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6

Intermediate_2019_tot_gen_NorthernGrid = All_2019_Intermediate.loc[:,['NorthernGrid_Coal_Gen', 'NorthernGrid_Oil_Gen',
       'NorthernGrid_Gas_Gen', 'NorthernGrid_Biomass_Gen', 'NorthernGrid_Geothermal_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6

#NorthernGrid 2059
NorthernGrid_nuc_2059 = list(set(nuclear_2059.columns) & set(NorthernGrid_nodes))
nuclear_gen_2059_NorthernGrid = nuclear_2059.loc[:,NorthernGrid_nuc_2059].sum().sum()*8760/10**6

eff_demand_cooperative_NorthernGrid_2059 = (demand_2059.loc[:,NorthernGrid_nodes].sum().sum() - All_2059_Cooperative['NorthernGrid_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_NorthernGrid_2059 = (demand_2059.loc[:,NorthernGrid_nodes].sum().sum() - All_2059_Intermediate['NorthernGrid_Unserved_Energy'].sum())/10**6
eff_demand_individual_NorthernGrid_2059 = (demand_2059.loc[:,NorthernGrid_nodes].sum().sum() - All_2059_Individual['NorthernGrid_Unserved_Energy'].sum())/10**6

Cooperative_2059_tot_gen_NorthernGrid = All_2059_Cooperative.loc[:,['NorthernGrid_Gas_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6

Individual_2059_tot_gen_NorthernGrid = All_2059_Individual.loc[:,['NorthernGrid_Gas_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6

Intermediate_2059_tot_gen_NorthernGrid = All_2059_Intermediate.loc[:,['NorthernGrid_Gas_Gen',
       'NorthernGrid_Hydro_Gen', 'NorthernGrid_Solar_Gen', 'NorthernGrid_Wind_Gen']].sum().sum()/10**6



#WestConnect 2019
#Reading and calculating yearly generation and demand
WestConnect_nuc_2019 = list(set(nuclear_2019.columns) & set(WestConnect_nodes))
nuclear_gen_2019_WestConnect = nuclear_2019.loc[:,WestConnect_nuc_2019].sum().sum()*8760/10**6

eff_demand_cooperative_WestConnect_2019 = (demand_2019.loc[:,WestConnect_nodes].sum().sum() - All_2019_Cooperative['WestConnect_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_WestConnect_2019 = (demand_2019.loc[:,WestConnect_nodes].sum().sum() - All_2019_Intermediate['WestConnect_Unserved_Energy'].sum())/10**6
eff_demand_individual_WestConnect_2019 = (demand_2019.loc[:,WestConnect_nodes].sum().sum() - All_2019_Individual['WestConnect_Unserved_Energy'].sum())/10**6

Cooperative_2019_tot_gen_WestConnect = All_2019_Cooperative.loc[:,['WestConnect_Coal_Gen', 'WestConnect_Oil_Gen',
       'WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen', 'WestConnect_Geothermal_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6

Individual_2019_tot_gen_WestConnect = All_2019_Individual.loc[:,['WestConnect_Coal_Gen', 'WestConnect_Oil_Gen',
       'WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen', 'WestConnect_Geothermal_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6

Intermediate_2019_tot_gen_WestConnect = All_2019_Intermediate.loc[:,['WestConnect_Coal_Gen', 'WestConnect_Oil_Gen',
       'WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen', 'WestConnect_Geothermal_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6

#WestConnect 2059
WestConnect_nuc_2059 = list(set(nuclear_2059.columns) & set(WestConnect_nodes))
nuclear_gen_2059_WestConnect = nuclear_2059.loc[:,WestConnect_nuc_2059].sum().sum()*8760/10**6

eff_demand_cooperative_WestConnect_2059 = (demand_2059.loc[:,WestConnect_nodes].sum().sum() - All_2059_Cooperative['WestConnect_Unserved_Energy'].sum())/10**6
eff_demand_intermediate_WestConnect_2059 = (demand_2059.loc[:,WestConnect_nodes].sum().sum() - All_2059_Intermediate['WestConnect_Unserved_Energy'].sum())/10**6
eff_demand_individual_WestConnect_2059 = (demand_2059.loc[:,WestConnect_nodes].sum().sum() - All_2059_Individual['WestConnect_Unserved_Energy'].sum())/10**6

Cooperative_2059_tot_gen_WestConnect = All_2059_Cooperative.loc[:,['WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6

Individual_2059_tot_gen_WestConnect = All_2059_Individual.loc[:,['WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6

Intermediate_2059_tot_gen_WestConnect = All_2059_Intermediate.loc[:,['WestConnect_Gas_Gen', 'WestConnect_Biomass_Gen',
       'WestConnect_Hydro_Gen', 'WestConnect_Solar_Gen', 'WestConnect_Wind_Gen']].sum().sum()/10**6



#Creating 2019 dataset
regions_2019 = ('CAISO','NorthernGrid','WestConnect')
genmix_demand = {
    'Generation under\nCooperative Case': (round(Cooperative_2019_tot_gen_CAISO+nuclear_gen_2019_CAISO, 1),
                                          round(Cooperative_2019_tot_gen_NorthernGrid+nuclear_gen_2019_NorthernGrid, 1),
                                          round(Cooperative_2019_tot_gen_WestConnect+nuclear_gen_2019_WestConnect, 1)),

    'Generation under\nIntermediate Case': (round(Intermediate_2019_tot_gen_CAISO+nuclear_gen_2019_CAISO, 1),
                                           round(Intermediate_2019_tot_gen_NorthernGrid+nuclear_gen_2019_NorthernGrid, 1),
                                           round(Intermediate_2019_tot_gen_WestConnect+nuclear_gen_2019_WestConnect, 1)),

    'Generation under\nIndividual Case': (round(Individual_2019_tot_gen_CAISO+nuclear_gen_2019_CAISO, 1),
                                         round(Individual_2019_tot_gen_NorthernGrid+nuclear_gen_2019_NorthernGrid, 1),
                                         round(Individual_2019_tot_gen_WestConnect+nuclear_gen_2019_WestConnect, 1)),

    'Electricity Demand': (round(demand_2019.loc[:,CAISO_nodes].sum().sum()/10**6, 1),
               round(demand_2019.loc[:,NorthernGrid_nodes].sum().sum()/10**6, 1),
               round(demand_2019.loc[:,WestConnect_nodes].sum().sum()/10**6, 1))
}


#Plotting the figure for 2019
x = np.arange(len(regions_2019))
width = 0.2
multiplier = 0

plt.rcParams.update({'font.size':12})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(layout='constrained', figsize=(10,6))

for attribute, measurement in genmix_demand.items():
    offset = width * multiplier

    if attribute == 'Generation under\nCooperative Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#029E73')
        ax.bar_label(rects, padding=4,size=9)

    elif attribute == 'Generation under\nIntermediate Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#ECE133')
        ax.bar_label(rects, padding=4,size=9)
        
    elif attribute == 'Generation under\nIndividual Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#D55E00')
        ax.bar_label(rects, padding=4,size=9)

    elif attribute == 'Electricity Demand':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#0173B2')
        ax.bar_label(rects, padding=4,size=9)
        
    multiplier += 1

ax.set_ylabel('Annual Generation and Demand (TWh)', weight='bold', fontsize=11)
ax.set_xticks(x + width*1.5, regions_2019)
ax.set_xticklabels(['CAISO','NorthernGrid','WestConnect'], weight='bold', fontsize=11)
ax.set_yticks([0,50,100,150,200,250,300,350,400])
ax.legend(ncols=1, bbox_to_anchor=(0.177, 0.995), fontsize=9)
ax.set_title('Total Generation and Demand in 2019', weight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('Gen_Demand_2019.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()


#Creating 2059 dataset
regions_2059 = ('CAISO','NorthernGrid','WestConnect')
genmix_demand = {
    'Generation under\nCooperative Case': (round(Cooperative_2059_tot_gen_CAISO+nuclear_gen_2059_CAISO, 1),
                                          round(Cooperative_2059_tot_gen_NorthernGrid+nuclear_gen_2059_NorthernGrid, 1),
                                          round(Cooperative_2059_tot_gen_WestConnect+nuclear_gen_2059_WestConnect, 1)),

    'Generation under\nIntermediate Case': (round(Intermediate_2059_tot_gen_CAISO+nuclear_gen_2059_CAISO, 1),
                                           round(Intermediate_2059_tot_gen_NorthernGrid+nuclear_gen_2059_NorthernGrid, 1),
                                           round(Intermediate_2059_tot_gen_WestConnect+nuclear_gen_2059_WestConnect, 1)),

    'Generation under\nIndividual Case': (round(Individual_2059_tot_gen_CAISO+nuclear_gen_2059_CAISO, 1),
                                         round(Individual_2059_tot_gen_NorthernGrid+nuclear_gen_2059_NorthernGrid, 1),
                                         round(Individual_2059_tot_gen_WestConnect+nuclear_gen_2059_WestConnect, 1)),

    'Electricity Demand': (round(demand_2059.loc[:,CAISO_nodes].sum().sum()/10**6, 1),
               round(demand_2059.loc[:,NorthernGrid_nodes].sum().sum()/10**6, 1),
               round(demand_2059.loc[:,WestConnect_nodes].sum().sum()/10**6, 1))
}


#Plotting the figure for 2059
x = np.arange(len(regions_2059))
width = 0.2
multiplier = 0

plt.rcParams.update({'font.size':12})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(layout='constrained', figsize=(10,6))

for attribute, measurement in genmix_demand.items():
    offset = width * multiplier

    if attribute == 'Generation under\nCooperative Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#029E73')
        ax.bar_label(rects, padding=4,size=9)

    elif attribute == 'Generation under\nIntermediate Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#ECE133')
        ax.bar_label(rects, padding=4,size=9)
        
    elif attribute == 'Generation under\nIndividual Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#D55E00')
        ax.bar_label(rects, padding=4,size=9)

    elif attribute == 'Electricity Demand':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#0173B2')
        ax.bar_label(rects, padding=4,size=9)
        
    multiplier += 1

ax.set_ylabel('Annual Generation and Demand (TWh)', weight='bold', fontsize=11)
ax.set_xticks(x + width*1.5, regions_2059)
ax.set_xticklabels(['CAISO','NorthernGrid','WestConnect'], weight='bold', fontsize=11)
ax.set_yticks([0,50,100,150,200,250,300,350,400,450,500,550])
ax.legend(ncols=1, bbox_to_anchor=(0.177, 0.995), fontsize=9)
ax.set_title('Total Generation and Demand in 2059', weight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('Gen_Demand_2059.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()

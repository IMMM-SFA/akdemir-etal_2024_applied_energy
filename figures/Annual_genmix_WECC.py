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

#Reading and calculating yearly nuclear generation
nuclear_2019 = pd.read_csv('../../Data/Raw_Results/2019_Base/Inputs/must_run.csv', header=0)
nuclear_gen_2019 = nuclear_2019.sum().sum()*8760

nuclear_2059 = pd.read_csv('../../Data/Raw_Results/2059_Cooperative/Inputs/must_run.csv', header=0)
nuclear_gen_2059 = nuclear_2059.sum().sum()*8760

#Creating dataset for 2019 visualization
gentypes_2019 = ('Coal','Oil','Gas','Biomass','Geothermal','Hydro','Solar','Wind','Nuclear')

Cooperative_2019_tot_gen = All_2019_Cooperative.loc[:,['WECC_Coal_Gen', 'WECC_Oil_Gen',
       'WECC_Gas_Gen', 'WECC_Biomass_Gen', 'WECC_Geothermal_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen']].sum()

Individual_2019_tot_gen = All_2019_Individual.loc[:,['WECC_Coal_Gen', 'WECC_Oil_Gen',
       'WECC_Gas_Gen', 'WECC_Biomass_Gen', 'WECC_Geothermal_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen']].sum()

Intermediate_2019_tot_gen = All_2019_Intermediate.loc[:,['WECC_Coal_Gen', 'WECC_Oil_Gen',
       'WECC_Gas_Gen', 'WECC_Biomass_Gen', 'WECC_Geothermal_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen']].sum()

genmix_percentages = {
    'Cooperative Case': (round(Cooperative_2019_tot_gen['WECC_Coal_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Oil_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Gas_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Biomass_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Geothermal_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Hydro_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Solar_Gen']/10**6,1),
                  round(Cooperative_2019_tot_gen['WECC_Wind_Gen']/10**6,1),
                  round(nuclear_gen_2019/10**6,1)),

    'Intermediate Case': (round(Intermediate_2019_tot_gen['WECC_Coal_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Oil_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Gas_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Biomass_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Geothermal_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Hydro_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Solar_Gen']/10**6,1),
                round(Intermediate_2019_tot_gen['WECC_Wind_Gen']/10**6,1),
                round(nuclear_gen_2019/10**6,1)),

    'Individual Case': (round(Individual_2019_tot_gen['WECC_Coal_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Oil_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Gas_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Biomass_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Geothermal_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Hydro_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Solar_Gen']/10**6,1),
            round(Individual_2019_tot_gen['WECC_Wind_Gen']/10**6,1),
            round(nuclear_gen_2019/10**6,1))
}


#Plotting the figure for 2019
x = np.arange(len(gentypes_2019))
width = 0.25
multiplier = 0

plt.rcParams.update({'font.size':14})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(layout='constrained', figsize=(12,6))

for attribute, measurement in genmix_percentages.items():
    offset = width * multiplier

    if attribute == 'Cooperative Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#029E73')
        ax.bar_label(rects, padding=4,size=7)

    elif attribute == 'Intermediate Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#ECE133')
        ax.bar_label(rects, padding=4,size=7)
        
    elif attribute == 'Individual Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#D55E00')
        ax.bar_label(rects, padding=4,size=7)
        
    multiplier += 1


ax.set_ylabel('Annual Generation (TWh)', weight='bold')
ax.set_xticks(x + width, gentypes_2019)
ax.set_xticklabels(['Coal','Oil','Natural Gas','Biomass','Geothermal','Hydro','Solar','Wind','Nuclear'], weight='bold')
ax.set_yticks([0,25,50,75,100,125,150,175,200,225,250])
ax.legend(ncols=1, bbox_to_anchor=(0.995, 0.995), fontsize=12)
ax.set_title('Total Generation by Type in 2019 (Western Interconnection)', weight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('WECC_Genmix_2019.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()


#Creating dataset for 2059 visualization
gentypes_2059 = ('Gas','Biomass','Hydro','Solar','Wind','OffshoreWind','Nuclear')

Cooperative_2059_tot_gen = All_2059_Cooperative.loc[:,['WECC_Gas_Gen', 'WECC_Biomass_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen',
       'WECC_OffshoreWind_Gen']].sum()

Individual_2059_tot_gen = All_2059_Individual.loc[:,['WECC_Gas_Gen', 'WECC_Biomass_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen',
       'WECC_OffshoreWind_Gen']].sum()

Intermediate_2059_tot_gen = All_2059_Intermediate.loc[:,['WECC_Gas_Gen', 'WECC_Biomass_Gen',
       'WECC_Hydro_Gen', 'WECC_Solar_Gen', 'WECC_Wind_Gen',
       'WECC_OffshoreWind_Gen']].sum()

genmix_percentages = {
    'Cooperative Case': (round(Cooperative_2059_tot_gen['WECC_Gas_Gen']/10**6,1),
                  round(Cooperative_2059_tot_gen['WECC_Biomass_Gen']/10**6,1),
                  round(Cooperative_2059_tot_gen['WECC_Hydro_Gen']/10**6,1),
                  round(Cooperative_2059_tot_gen['WECC_Solar_Gen']/10**6,1),
                  round(Cooperative_2059_tot_gen['WECC_Wind_Gen']/10**6,1),
                  round(Cooperative_2059_tot_gen['WECC_OffshoreWind_Gen']/10**6,1),
                  round(nuclear_gen_2059/10**6,1)),

    'Intermediate Case': (round(Intermediate_2059_tot_gen['WECC_Gas_Gen']/10**6,1),
                  round(Intermediate_2059_tot_gen['WECC_Biomass_Gen']/10**6,1),
                  round(Intermediate_2059_tot_gen['WECC_Hydro_Gen']/10**6,1),
                  round(Intermediate_2059_tot_gen['WECC_Solar_Gen']/10**6,1),
                  round(Intermediate_2059_tot_gen['WECC_Wind_Gen']/10**6,1),
                  round(Intermediate_2059_tot_gen['WECC_OffshoreWind_Gen']/10**6,1),
                  round(nuclear_gen_2059/10**6,1)),

    'Individual Case': (round(Individual_2059_tot_gen['WECC_Gas_Gen']/10**6,1),
                  round(Individual_2059_tot_gen['WECC_Biomass_Gen']/10**6,1),
                  round(Individual_2059_tot_gen['WECC_Hydro_Gen']/10**6,1),
                  round(Individual_2059_tot_gen['WECC_Solar_Gen']/10**6,1),
                  round(Individual_2059_tot_gen['WECC_Wind_Gen']/10**6,1),
                  round(Individual_2059_tot_gen['WECC_OffshoreWind_Gen']/10**6,1),
                  round(nuclear_gen_2059/10**6,1))
}

#Plotting the figure for 2059
x = np.arange(len(gentypes_2059))
width = 0.25
multiplier = 0

plt.rcParams.update({'font.size':14})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(layout='constrained', figsize=(12,6))

for attribute, measurement in genmix_percentages.items():
    offset = width * multiplier

    if attribute == 'Cooperative Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#029E73')
        ax.bar_label(rects, padding=4,size=8)

    elif attribute == 'Intermediate Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#ECE133')
        ax.bar_label(rects, padding=4,size=8)
        
    elif attribute == 'Individual Case':
        rects = ax.bar(x + offset, measurement, width, label=attribute, color='#D55E00')
        ax.bar_label(rects, padding=4,size=8)
        
    multiplier += 1


ax.set_ylabel('Annual Generation (TWh)', weight='bold')
ax.set_xticks(x + width, gentypes_2059)
ax.set_xticklabels(['Natural Gas','Biomass','Hydro','Solar','Wind','Offshore Wind','Nuclear'], weight='bold')
ax.set_yticks([0,50,100,150,200,250,300,350,400,450,500,550,600])
ax.legend(ncols=1, bbox_to_anchor=(0.995, 0.995), fontsize=12)
ax.set_title('Total Generation by Type in 2059 (Western Interconnection)', weight='bold', fontsize=14)

plt.tight_layout()
plt.savefig('WECC_Genmix_2059.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()



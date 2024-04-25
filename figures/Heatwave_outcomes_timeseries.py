import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

#Reading the necessary results
All_2019_Base = pd.read_csv('../../Data/Organized_Results/2019_Base_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2019_Cooperative = pd.read_csv('../../Data/Organized_Results/2019_Cooperative_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2019_Individual = pd.read_csv('../../Data/Organized_Results/2019_Individual_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2019_Intermediate = pd.read_csv('../../Data/Organized_Results/2019_Intermediate_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)

All_2059_Cooperative = pd.read_csv('../../Data/Organized_Results/2059_Cooperative_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2059_Individual = pd.read_csv('../../Data/Organized_Results/2059_Individual_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)
All_2059_Intermediate = pd.read_csv('../../Data/Organized_Results/2059_Intermediate_All_Hourly_Results.csv', header=0, index_col=0, parse_dates=True)

#Defining heat wave durations
local_hw_duration_2019 = pd.date_range(start='2019-06-09 00:00:00', end='2019-06-11 23:00:00', freq='H')
wide_hw_duration_2019 = pd.date_range(start='2019-08-04 00:00:00', end='2019-08-06 23:00:00', freq='H')

local_hw_duration_2059 = pd.date_range(start='2059-06-09 00:00:00', end='2059-06-11 23:00:00', freq='H')
wide_hw_duration_2059 = pd.date_range(start='2059-08-04 00:00:00', end='2059-08-06 23:00:00', freq='H')

#Creating datasets for boxplots
LMPs_seaborn_2019_local = pd.concat([All_2019_Base.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Weighted_LMP'],
                                     All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], All_2019_Individual.loc[local_hw_duration_2019,'WECC_Weighted_LMP']],ignore_index=True)

Slack_seaborn_2019_local = pd.concat([All_2019_Base.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Unserved_Energy'],
                                     All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], All_2019_Individual.loc[local_hw_duration_2019,'WECC_Unserved_Energy']],ignore_index=True)

LMPs_seaborn_2019_wide = pd.concat([All_2019_Base.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'],
                                     All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Weighted_LMP']],ignore_index=True)

Slack_seaborn_2019_wide = pd.concat([All_2019_Base.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'],
                                     All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Unserved_Energy']],ignore_index=True)

cases_2019 = []
cases_2019.extend(['Base Case']*len(local_hw_duration_2019))
cases_2019.extend(['Cooperative Case']*len(local_hw_duration_2019))
cases_2019.extend(['Intermediate Case']*len(local_hw_duration_2019))
cases_2019.extend(['Individual Case']*len(local_hw_duration_2019))

seaborn_data_2019_local = pd.DataFrame(zip(LMPs_seaborn_2019_local.values,Slack_seaborn_2019_local.values,np.array(cases_2019)),columns=['LMP','Slack','Case'])
seaborn_data_2019_wide = pd.DataFrame(zip(LMPs_seaborn_2019_wide.values,Slack_seaborn_2019_wide.values,np.array(cases_2019)),columns=['LMP','Slack','Case'])

LMPs_seaborn_2059_local = pd.concat([All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Weighted_LMP'],
                                     All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Weighted_LMP'], All_2059_Individual.loc[local_hw_duration_2059,'WECC_Weighted_LMP']],ignore_index=True)

Slack_seaborn_2059_local = pd.concat([All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Unserved_Energy'],
                                     All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Unserved_Energy'], All_2059_Individual.loc[local_hw_duration_2059,'WECC_Unserved_Energy']],ignore_index=True)

LMPs_seaborn_2059_wide = pd.concat([All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'],
                                     All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'], All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Weighted_LMP']],ignore_index=True)

Slack_seaborn_2059_wide = pd.concat([All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'],
                                     All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'], All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Unserved_Energy']],ignore_index=True)

cases_2059 = []
cases_2059.extend(['Cooperative Case']*len(local_hw_duration_2059))
cases_2059.extend(['Intermediate Case']*len(local_hw_duration_2059))
cases_2059.extend(['Individual Case']*len(local_hw_duration_2059))

seaborn_data_2059_local = pd.DataFrame(zip(LMPs_seaborn_2059_local.values,Slack_seaborn_2059_local.values,np.array(cases_2059)),columns=['LMP','Slack','Case'])
seaborn_data_2059_wide = pd.DataFrame(zip(LMPs_seaborn_2059_wide.values,Slack_seaborn_2059_wide.values,np.array(cases_2059)),columns=['LMP','Slack','Case'])


######################################### Plotting the figure for 2019 local heat wave #########################################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(2,2,figsize=(16,10),width_ratios=[3,1], sharey='row', sharex='col')

ax[0,0].plot(local_hw_duration_2019,All_2019_Base.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], label='Base Case', color='#0173B2')
ax[0,0].plot(local_hw_duration_2019,All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], label='Cooperative Case', color='#029E73')
ax[0,0].plot(local_hw_duration_2019,All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], label='Intermediate Case', color='#ECE133')
ax[0,0].plot(local_hw_duration_2019,All_2019_Individual.loc[local_hw_duration_2019,'WECC_Weighted_LMP'], label='Individual Case', color='#D55E00')

ax[0,0].set_ylabel('Hourly LMP ($/MWh)', weight='bold')
ax[0,0].set_yticks([40,50,60,70,80,90,100,110])

ax[1,0].plot(local_hw_duration_2019,All_2019_Base.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], label='Base Case', color='#0173B2')
ax[1,0].plot(local_hw_duration_2019,All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], label='Cooperative Case', color='#029E73')
ax[1,0].plot(local_hw_duration_2019,All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], label='Intermediate Case', color='#ECE133')
ax[1,0].plot(local_hw_duration_2019,All_2019_Individual.loc[local_hw_duration_2019,'WECC_Unserved_Energy'], label='Individual Case', color='#D55E00')

ax[1,0].set_xticks(['2019-06-09 06:00:00','2019-06-09 18:00:00','2019-06-10 06:00:00','2019-06-10 18:00:00','2019-06-11 06:00:00','2019-06-11 18:00:00'])
ax[1,0].set_xticklabels(['June 9\n6 AM','June 9\n6 PM','June 10\n6 AM','June 10\n6 PM','June 11\n6 AM','June 11\n6 PM'])
ax[1,0].set_ylabel('Hourly Unserved Energy (MW)', weight='bold')
ax[1,0].set_yticks([0,50,100,150,200,250,300,350,400])

colors = {"Base Case": "#0173B2", "Cooperative Case": "#029E73", "Intermediate Case": "#ECE133", "Individual Case": "#D55E00"}

sns.boxplot(data=seaborn_data_2019_local, x="Case", y='LMP',ax=ax[0,1], palette=colors, legend=False)
ax[0,1].set_ylabel('')
ax[0,1].set_xlabel('')
ax[0,1].set_yticks([40,50,60,70,80,90,100,110])

sns.boxplot(data=seaborn_data_2019_local, x="Case", y='Slack',ax=ax[1,1], palette=colors, legend=False)
ax[1,1].set_ylabel('')
ax[1,1].set_xticklabels(['Base\nCase','Coop.\nCase','Intr.\nCase','Indv.\nCase'])
ax[1,1].set_xlabel('')
ax[1,1].set_yticks([0,50,100,150,200,250,300,350,400])

handles = []
line1 = Line2D([0], [0], label='Base Case', color='#0173B2')
line2 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line3 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line4 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3,line4])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.075, 0.43), ncol=1, fontsize=15)

plt.tight_layout()
plt.savefig('2019_local_heatwave_timeseries.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()     

print(f'Average WECC LMP during 2019 local heat wave (Base Case) =', round(All_2019_Base.loc[local_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 local heat wave (Cooperative Case) =', round(All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 local heat wave (Intermediate Case) =', round(All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 local heat wave (Individual Case) =', round(All_2019_Individual.loc[local_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print('\n')
print(f'Average WECC LOL during 2019 local heat wave (Base Case) =', round(All_2019_Base.loc[local_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 local heat wave (Cooperative Case) =', round(All_2019_Cooperative.loc[local_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 local heat wave (Intermediate Case) =', round(All_2019_Intermediate.loc[local_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 local heat wave (Individual Case) =', round(All_2019_Individual.loc[local_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print('\n')

######################################### Plotting the figure for 2019 widespread heat wave #########################################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(2,2,figsize=(16,10),width_ratios=[3,1], sharey='row', sharex='col')

ax[0,0].plot(wide_hw_duration_2019,All_2019_Base.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], label='Base Case', color='#0173B2')
ax[0,0].plot(wide_hw_duration_2019,All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], label='Cooperative Case', color='#029E73')
ax[0,0].plot(wide_hw_duration_2019,All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], label='Intermediate Case', color='#ECE133')
ax[0,0].plot(wide_hw_duration_2019,All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'], label='Individual Case', color='#D55E00')

ax[0,0].set_ylabel('Hourly LMP ($/MWh)', weight='bold')
ax[0,0].set_yticks([40,60,80,100,120,140,160,180,200])

ax[1,0].plot(wide_hw_duration_2019,All_2019_Base.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], label='Base Case', color='#0173B2')
ax[1,0].plot(wide_hw_duration_2019,All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], label='Cooperative Case', color='#029E73')
ax[1,0].plot(wide_hw_duration_2019,All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], label='Intermediate Case', color='#ECE133')
ax[1,0].plot(wide_hw_duration_2019,All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'], label='Individual Case', color='#D55E00')

ax[1,0].set_xticks(['2019-08-04 06:00:00','2019-08-04 18:00:00','2019-08-05 06:00:00','2019-08-05 18:00:00','2019-08-06 06:00:00','2019-08-06 18:00:00'])
ax[1,0].set_xticklabels(['August 4\n6 AM','August 4\n6 PM','August 5\n6 AM','August 5\n6 PM','August 6\n6 AM','August 6\n6 PM'])
ax[1,0].set_ylabel('Hourly Unserved Energy (MW)', weight='bold')
ax[1,0].set_yticks([0,200,400,600,800,1000,1200])

colors = {"Base Case": "#0173B2", "Cooperative Case": "#029E73", "Intermediate Case": "#ECE133", "Individual Case": "#D55E00"}

sns.boxplot(data=seaborn_data_2019_wide, x="Case", y='LMP',ax=ax[0,1], palette=colors, legend=False)
ax[0,1].set_ylabel('')
ax[0,1].set_xlabel('')
ax[0,1].set_yticks([40,60,80,100,120,140,160,180,200])

sns.boxplot(data=seaborn_data_2019_wide, x="Case", y='Slack',ax=ax[1,1], palette=colors, legend=False)
ax[1,1].set_ylabel('')
ax[1,1].set_xticklabels(['Base\nCase','Coop.\nCase','Intr.\nCase','Indv.\nCase'])
ax[1,1].set_xlabel('')
ax[1,1].set_yticks([0,200,400,600,800,1000,1200])

handles = []
line1 = Line2D([0], [0], label='Base Case', color='#0173B2')
line2 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line3 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line4 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3,line4])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.08, 0.43), ncol=1, fontsize=15)

plt.tight_layout()
plt.savefig('2019_widespread_heatwave_timeseries.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()     

print(f'Average WECC LMP during 2019 widespread heat wave (Base Case) =', round(All_2019_Base.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 widespread heat wave (Cooperative Case) =', round(All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 widespread heat wave (Intermediate Case) =', round(All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2019 widespread heat wave (Individual Case) =', round(All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print('\n')
print(f'Average WECC LOL during 2019 widespread heat wave (Base Case) =', round(All_2019_Base.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 widespread heat wave (Cooperative Case) =', round(All_2019_Cooperative.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 widespread heat wave (Intermediate Case) =', round(All_2019_Intermediate.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2019 widespread heat wave (Individual Case) =', round(All_2019_Individual.loc[wide_hw_duration_2019,'WECC_Unserved_Energy'].mean(),2),'MW')
print('\n')






######################################### Plotting the figure for 2059 local heat wave #########################################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(2,2,figsize=(16,10),width_ratios=[3,1], sharey='row', sharex='col')

ax[0,0].plot(local_hw_duration_2059,All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Weighted_LMP'], label='Cooperative Case', color='#029E73')
ax[0,0].plot(local_hw_duration_2059,All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Weighted_LMP'], label='Intermediate Case', color='#ECE133')
ax[0,0].plot(local_hw_duration_2059,All_2059_Individual.loc[local_hw_duration_2059,'WECC_Weighted_LMP'], label='Individual Case', color='#D55E00')

ax[0,0].set_ylabel('Hourly LMP ($/MWh)', weight='bold')
ax[0,0].set_yticks([0,250,500,750,1000,1250,1500,1750,2000])

ax[1,0].plot(local_hw_duration_2059,All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Unserved_Energy'], label='Cooperative Case', color='#029E73')
ax[1,0].plot(local_hw_duration_2059,All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Unserved_Energy'], label='Intermediate Case', color='#ECE133')
ax[1,0].plot(local_hw_duration_2059,All_2059_Individual.loc[local_hw_duration_2059,'WECC_Unserved_Energy'], label='Individual Case', color='#D55E00')

ax[1,0].set_xticks(['2059-06-09 06:00:00','2059-06-09 18:00:00','2059-06-10 06:00:00','2059-06-10 18:00:00','2059-06-11 06:00:00','2059-06-11 18:00:00'])
ax[1,0].set_xticklabels(['June 9\n6 AM','June 9\n6 PM','June 10\n6 AM','June 10\n6 PM','June 11\n6 AM','June 11\n6 PM'])
ax[1,0].set_ylabel('Hourly Unserved Energy (MW)', weight='bold')
ax[1,0].set_yticks([0,10000,20000,30000,40000,50000])

colors = {"Cooperative Case": "#029E73", "Intermediate Case": "#ECE133", "Individual Case": "#D55E00"}

sns.boxplot(data=seaborn_data_2059_local, x="Case", y='LMP',ax=ax[0,1], palette=colors, legend=False)
ax[0,1].set_ylabel('')
ax[0,1].set_xlabel('')
ax[0,1].set_yticks([0,250,500,750,1000,1250,1500,1750,2000])

sns.boxplot(data=seaborn_data_2059_local, x="Case", y='Slack',ax=ax[1,1], palette=colors, legend=False)
ax[1,1].set_ylabel('')
ax[1,1].set_xticklabels(['Coop.\nCase','Intr.\nCase','Indv.\nCase'])
ax[1,1].set_xlabel('')
ax[1,1].set_yticks([0,10000,20000,30000,40000,50000])

handles = []
line1 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line2 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line3 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.092, 0.45), ncol=1, fontsize=15)

plt.tight_layout()
plt.savefig('2059_local_heatwave_timeseries.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()     

print(f'Average WECC LMP during 2059 local heat wave (Cooperative Case) =', round(All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2059 local heat wave (Intermediate Case) =', round(All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2059 local heat wave (Individual Case) =', round(All_2059_Individual.loc[local_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print('\n')
print(f'Average WECC LOL during 2059 local heat wave (Cooperative Case) =', round(All_2059_Cooperative.loc[local_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2059 local heat wave (Intermediate Case) =', round(All_2059_Intermediate.loc[local_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2059 local heat wave (Individual Case) =', round(All_2059_Individual.loc[local_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print('\n')

######################################### Plotting the figure for 2059 widespread heat wave #########################################
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.sans-serif'] = "Arial"
fig, ax = plt.subplots(2,2,figsize=(16,10),width_ratios=[3,1], sharey='row', sharex='col')

ax[0,0].plot(wide_hw_duration_2059,All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'], label='Cooperative Case', color='#029E73')
ax[0,0].plot(wide_hw_duration_2059,All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'], label='Intermediate Case', color='#ECE133')
ax[0,0].plot(wide_hw_duration_2059,All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'], label='Individual Case', color='#D55E00')

ax[0,0].set_ylabel('Hourly LMP ($/MWh)', weight='bold')
ax[0,0].set_yticks([0,250,500,750,1000,1250,1500,1750,2000])

ax[1,0].plot(wide_hw_duration_2059,All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'], label='Cooperative Case', color='#029E73')
ax[1,0].plot(wide_hw_duration_2059,All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'], label='Intermediate Case', color='#ECE133')
ax[1,0].plot(wide_hw_duration_2059,All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'], label='Individual Case', color='#D55E00')

ax[1,0].set_xticks(['2059-08-04 06:00:00','2059-08-04 18:00:00','2059-08-05 06:00:00','2059-08-05 18:00:00','2059-08-06 06:00:00','2059-08-06 18:00:00'])
ax[1,0].set_xticklabels(['August 4\n6 AM','August 4\n6 PM','August 5\n6 AM','August 5\n6 PM','August 6\n6 AM','August 6\n6 PM'])
ax[1,0].set_ylabel('Hourly Unserved Energy (MW)', weight='bold')
ax[1,0].set_yticks([0,10000,20000,30000,40000,50000])

colors = {"Cooperative Case": "#029E73", "Intermediate Case": "#ECE133", "Individual Case": "#D55E00"}

sns.boxplot(data=seaborn_data_2059_wide, x="Case", y='LMP',ax=ax[0,1], palette=colors, legend=False)
ax[0,1].set_ylabel('')
ax[0,1].set_xlabel('')
ax[0,1].set_yticks([0,250,500,750,1000,1250,1500,1750,2000])

sns.boxplot(data=seaborn_data_2059_wide, x="Case", y='Slack',ax=ax[1,1], palette=colors, legend=False)
ax[1,1].set_ylabel('')
ax[1,1].set_xticklabels(['Coop.\nCase','Intr.\nCase','Indv.\nCase'])
ax[1,1].set_xlabel('')
ax[1,1].set_yticks([0,10000,20000,30000,40000,50000])

handles = []
line1 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line2 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line3 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.092, 0.455), ncol=1, fontsize=15)

plt.tight_layout()
plt.savefig('2059_widespread_heatwave_timeseries.png', dpi=400, bbox_inches='tight')
plt.show()
plt.clf()     

print(f'Average WECC LMP during 2059 widespread heat wave (Cooperative Case) =', round(All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2059 widespread heat wave (Intermediate Case) =', round(All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print(f'Average WECC LMP during 2059 widespread heat wave (Individual Case) =', round(All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Weighted_LMP'].mean(),2),'$/MWh')
print('\n')
print(f'Average WECC LOL during 2059 widespread heat wave (Cooperative Case) =', round(All_2059_Cooperative.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2059 widespread heat wave (Intermediate Case) =', round(All_2059_Intermediate.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print(f'Average WECC LOL during 2059 widespread heat wave (Individual Case) =', round(All_2059_Individual.loc[wide_hw_duration_2059,'WECC_Unserved_Energy'].mean(),2),'MW')
print('\n')
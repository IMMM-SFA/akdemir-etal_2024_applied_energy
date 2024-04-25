import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from matplotlib.lines import Line2D

#Defining BAs and hour ranges
all_BAs_df = pd.read_csv('../../Data/Supplementary_Data/BA_Topology_Files/BAs.csv',header=0)
all_BA_names = [*all_BAs_df['Name']]
all_BA_abbs = [*all_BAs_df['Abbreviation']]

my_year = 2019

heatwave_local_PST = pd.date_range(start=f'06-09-{my_year} 00:00:00', end=f'06-11-{my_year} 23:00:00', freq='H')
heatwave_local_UTC = heatwave_local_PST + datetime.timedelta(hours=8)

heatwave_wide_PST = pd.date_range(start=f'08-04-{my_year} 00:00:00', end=f'08-06-{my_year} 23:00:00', freq='H')
heatwave_wide_UTC = heatwave_wide_PST + datetime.timedelta(hours=8)

hours_2015 = pd.date_range(start=f'01-01-{my_year} 00:00:00', end=f'12-31-{my_year} 23:00:00', freq='H')

#Reading historical TELL data
TELL_outputs_df = pd.read_csv(f'../../Data/TELL_Outputs/historic/TELL_Balancing_Authority_Hourly_Load_Data_{my_year}_Scaled_{my_year}.csv' ,header=0)

#Organizing TELL load data to have each BA as columns
for i in all_BA_abbs:
    
    BA_index = all_BA_abbs.index(i)
    BA_sp_TELL_data = TELL_outputs_df.loc[TELL_outputs_df['BA_Code']==i]['Scaled_TELL_BA_Load_MWh'].values
    BA_sp_TELL_data = BA_sp_TELL_data.reshape(BA_sp_TELL_data.shape[0],1)
    
    if BA_index == 0:
        TELL_all_BAs_load = BA_sp_TELL_data
        
    else:
        TELL_all_BAs_load = np.hstack((TELL_all_BAs_load,BA_sp_TELL_data))

df_load = pd.DataFrame(TELL_all_BAs_load,columns=all_BA_abbs)

if len(df_load) > len(hours_2015):
    diff_num_hrs = 24-(len(df_load) - len(hours_2015))
    hours_2020 = pd.date_range(start='01-01-2020 0{}:00:00'.format(diff_num_hrs), end='12-31-2020 23:00:00', freq='H')
    feb_29_hours = pd.date_range(start='2-29-2020 0{}:00:00'.format(diff_num_hrs),end='2-29-2020 23:00:00', freq='H')
    df_load.index = hours_2020
    df_load.drop(feb_29_hours,inplace=True)
    df_load.reset_index(drop=True,inplace=True) 
else:
    pass

#Selecting heatwave timeframes and plotting the comparison figure
df_load.index = hours_2015

WECC_local_heatwave_demand = df_load.loc[heatwave_local_UTC,:].sum(axis=1)
WECC_wide_heatwave_demand = df_load.loc[heatwave_wide_UTC,:].sum(axis=1)

plt.rcParams.update({'font.size': 15})
plt.rcParams['font.sans-serif'] = "Arial"
plt.style.use('seaborn-v0_8-whitegrid')

fig, ax = plt.subplots(figsize=(15,8))

sns.lineplot(x=heatwave_local_PST, y=WECC_local_heatwave_demand, color = 'royalblue', ax=ax)

ax.set_ylabel("Demand (MWh)", weight='bold', fontsize=20)
ax.set_xlabel("Local Heat Wave Timeline", weight='bold', fontsize=20, labelpad=15)
ax.set_xticks(["2019-06-09 06:00:00", "2019-06-09 18:00:00", "2019-06-10 06:00:00", "2019-06-10 18:00:00", "2019-06-11 06:00:00", "2019-06-11 18:00:00"])
ax.set_xticklabels(["June 9, 2019\n6 AM", "June 9, 2019\n6 PM", "June 10, 2019\n6 AM", "June 10, 2019\n6 PM", "June 11, 2019\n6 AM", "June 11, 2019\n6 PM"])

ax2 = ax.twiny()

sns.lineplot(x=heatwave_wide_PST, y=WECC_wide_heatwave_demand, color = 'crimson', ax=ax2)
ax2.set_xlabel("Widespread Heat Wave Timeline", weight='bold', fontsize=20, labelpad=15)
ax2.set_xticks(["2019-08-04 06:00:00", "2019-08-04 18:00:00", "2019-08-05 06:00:00", "2019-08-05 18:00:00", "2019-08-06 06:00:00", "2019-08-06 18:00:00"])
ax2.set_xticklabels(["August 4, 2019\n6 AM", "August 4, 2019\n6 PM", "August 5, 2019\n6 AM", "August 5, 2019\n6 PM", "August 6, 2019\n6 AM", "August 6, 2019\n6 PM"])

handles=[]
line1 = Line2D([0], [0], label='Local Heat Wave', color='royalblue')
line2 = Line2D([0], [0], label='Widespread Heat Wave', color='crimson')
handles.extend([line1,line2])
fig.legend(handles=handles, loc='center', bbox_to_anchor=(0.88, 0.2), ncol=1, frameon=True)

plt.tight_layout()
plt.savefig(f'{my_year}_heatwaves.png', dpi=200, bbox_inches='tight')
plt.show()
plt.clf()


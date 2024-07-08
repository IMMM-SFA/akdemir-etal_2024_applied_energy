import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

#Reading the necessary results
All_2019_Base = pd.read_csv('../../Data/Organized_Results/2019_Base_All_Hourly_Results.csv', header=0, index_col=0)
All_2019_Cooperative = pd.read_csv('../../Data/Organized_Results/2019_Cooperative_All_Hourly_Results.csv', header=0, index_col=0)
All_2019_Individual = pd.read_csv('../../Data/Organized_Results/2019_Individual_All_Hourly_Results.csv', header=0, index_col=0)
All_2019_Intermediate = pd.read_csv('../../Data/Organized_Results/2019_Intermediate_All_Hourly_Results.csv', header=0, index_col=0)

All_2059_Cooperative = pd.read_csv('../../Data/Organized_Results/2059_Cooperative_All_Hourly_Results.csv', header=0, index_col=0)
All_2059_Individual = pd.read_csv('../../Data/Organized_Results/2059_Individual_All_Hourly_Results.csv', header=0, index_col=0)
All_2059_Intermediate = pd.read_csv('../../Data/Organized_Results/2059_Intermediate_All_Hourly_Results.csv', header=0, index_col=0)

#Plotting 2019 ECDF of LMPs for each region
plt.rcParams.update({'font.size':14})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(2,2, figsize=(10,10))

sns.ecdfplot(x=All_2019_Base['WECC_Weighted_LMP'], ax=ax[0,0], color='#0173B2')
sns.ecdfplot(x=All_2019_Cooperative['WECC_Weighted_LMP'], ax=ax[0,0], color='#029E73')
sns.ecdfplot(x=All_2019_Intermediate['WECC_Weighted_LMP'], ax=ax[0,0], color='#ECE133')
sns.ecdfplot(x=All_2019_Individual['WECC_Weighted_LMP'], ax=ax[0,0], color='#D55E00')

sns.ecdfplot(x=All_2019_Base['CAISO_Weighted_LMP'], ax=ax[0,1], color='#0173B2')
sns.ecdfplot(x=All_2019_Cooperative['CAISO_Weighted_LMP'], ax=ax[0,1], color='#029E73')
sns.ecdfplot(x=All_2019_Intermediate['CAISO_Weighted_LMP'], ax=ax[0,1], color='#ECE133')
sns.ecdfplot(x=All_2019_Individual['CAISO_Weighted_LMP'], ax=ax[0,1], color='#D55E00')

sns.ecdfplot(x=All_2019_Base['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#0173B2')
sns.ecdfplot(x=All_2019_Cooperative['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#029E73')
sns.ecdfplot(x=All_2019_Intermediate['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#ECE133')
sns.ecdfplot(x=All_2019_Individual['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#D55E00')

sns.ecdfplot(x=All_2019_Base['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#0173B2')
sns.ecdfplot(x=All_2019_Cooperative['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#029E73')
sns.ecdfplot(x=All_2019_Intermediate['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#ECE133')
sns.ecdfplot(x=All_2019_Individual['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#D55E00')

ax[0,0].set_xlabel('', weight='bold')
ax[0,1].set_xlabel('', weight='bold')
ax[1,0].set_xlabel('LMP ($/MWh)', weight='bold')
ax[1,1].set_xlabel('LMP ($/MWh)', weight='bold')

ax[0,0].set_ylabel('Probability', weight='bold')
ax[1,0].set_ylabel('Probability', weight='bold')
ax[0,1].set_ylabel('', weight='bold')
ax[1,1].set_ylabel('', weight='bold')

ax[0,0].set_title('Western Interconnection', weight='bold')
ax[0,1].set_title('CAISO', weight='bold')
ax[1,0].set_title('NorthernGrid', weight='bold')
ax[1,1].set_title('WestConnect', weight='bold')

ax[0,0].set_xlim([0,240])
ax[0,1].set_xlim([0,240])
ax[1,0].set_xlim([0,240])
ax[1,1].set_xlim([0,240])

ax[0,0].set_xticks([0,40,80,120,160,200,240])
ax[0,1].set_xticks([0,40,80,120,160,200,240])
ax[1,0].set_xticks([0,40,80,120,160,200,240])
ax[1,1].set_xticks([0,40,80,120,160,200,240])

handles = []
line1 = Line2D([0], [0], label='Base Case', color='#0173B2')
line2 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line3 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line4 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3,line4])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.275, 0.605), ncol=1, fontsize=12)

plt.tight_layout()
plt.savefig('ECDF_2019.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()



#Plotting 2059 ECDF of LMPs for each region
plt.rcParams.update({'font.size':14})
plt.rcParams['font.sans-serif'] = "Arial"
fig,ax = plt.subplots(2,2, figsize=(10,10))

sns.ecdfplot(x=All_2059_Cooperative['WECC_Weighted_LMP'], ax=ax[0,0], color='#029E73')
sns.ecdfplot(x=All_2059_Intermediate['WECC_Weighted_LMP'], ax=ax[0,0], color='#ECE133')
sns.ecdfplot(x=All_2059_Individual['WECC_Weighted_LMP'], ax=ax[0,0], color='#D55E00')

sns.ecdfplot(x=All_2059_Cooperative['CAISO_Weighted_LMP'], ax=ax[0,1], color='#029E73')
sns.ecdfplot(x=All_2059_Intermediate['CAISO_Weighted_LMP'], ax=ax[0,1], color='#ECE133')
sns.ecdfplot(x=All_2059_Individual['CAISO_Weighted_LMP'], ax=ax[0,1], color='#D55E00')

sns.ecdfplot(x=All_2059_Cooperative['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#029E73')
sns.ecdfplot(x=All_2059_Intermediate['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#ECE133')
sns.ecdfplot(x=All_2059_Individual['NorthernGrid_Weighted_LMP'], ax=ax[1,0], color='#D55E00')

sns.ecdfplot(x=All_2059_Cooperative['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#029E73')
sns.ecdfplot(x=All_2059_Intermediate['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#ECE133')
sns.ecdfplot(x=All_2059_Individual['WestConnect_Weighted_LMP'], ax=ax[1,1], color='#D55E00')

ax[0,0].set_xlabel('', weight='bold')
ax[0,1].set_xlabel('', weight='bold')
ax[1,0].set_xlabel('LMP ($/MWh)', weight='bold')
ax[1,1].set_xlabel('LMP ($/MWh)', weight='bold')

ax[0,0].set_ylabel('Probability', weight='bold')
ax[1,0].set_ylabel('Probability', weight='bold')
ax[0,1].set_ylabel('', weight='bold')
ax[1,1].set_ylabel('', weight='bold')

ax[0,0].set_title('Western Interconnection', weight='bold')
ax[0,1].set_title('CAISO', weight='bold')
ax[1,0].set_title('NorthernGrid', weight='bold')
ax[1,1].set_title('WestConnect', weight='bold')

ax[0,0].set_xlim([-100,2000])
ax[0,1].set_xlim([-100,2000])
ax[1,0].set_xlim([-100,2000])
ax[1,1].set_xlim([-100,2000])

# ax[0,1].set_xticks([-100,0,500,1000,1500,2000])
# ax[0,1].set_xticklabels(['',0,500,1000,1500,2000])

handles = []
line1 = Line2D([0], [0], label='Cooperative Case', color='#029E73')
line2 = Line2D([0], [0], label='Intermediate Case', color='#ECE133')
line3 = Line2D([0], [0], label='Individual Case', color='#D55E00')
handles.extend([line1,line2,line3])
fig.legend(handles=handles,loc='center left', bbox_to_anchor=(0.27, 0.595), ncol=1, fontsize=12)

plt.tight_layout()
plt.savefig('ECDF_2059.png', dpi=300, bbox_inches='tight')
plt.show()
plt.clf()

[![DOI](https://zenodo.org/badge/791057925.svg)](https://zenodo.org/doi/10.5281/zenodo.12693666)

# akdemir-etal_2024_applied_energy

**Investigating the effects of cooperative transmission expansion planning on grid performance during heat waves with varying spatial scales**

Kerem Ziya Akdemir<sup>1\*</sup>, Kendall Mongird<sup>1</sup>, Jordan D. Kern<sup>2</sup>, Konstantinos Oikonomou<sup>1</sup>, Nathalie Voisin<sup>1,3</sup>, Casey D. Burleyson<sup>1</sup>, Jennie S. Rice<sup>1</sup>, Mengqi Zhao<sup>1</sup>, Cameron Bracken<sup>1</sup>, and Chris Vernon<sup>1</sup>

<sup>1 </sup> Pacific Northwest National Laboratory, Richland, WA, USA  
<sup>2 </sup> North Carolina State University, Raleigh, NC, USA  
<sup>3 </sup> University of Washington, Seattle, WA, USA

\* corresponding author: keremziya.akdemir@pnnl.gov

## Abstract
There is growing recognition of the advantages of interregional transmission capacity to decarbonize electricity grids. A less explored benefit is potential performance improvements during extreme weather events. This study examines the impacts of cooperative transmission expansion planning using an advanced modeling chain to simulate power grid operations of the United States Western Interconnection in 2019 and 2059 under different levels of collaboration between transmission planning regions. Two historical heat waves in 2019 with varying geographical coverage are replayed under future climate change in 2059 to assess the transmission cooperation benefits during grid stress. The results show that cooperative transmission planning yields the best outcomes in terms of reducing wholesale electricity prices and minimizing energy outages both for the whole interconnection and individual transmission planning regions. Compared to individual planning, cooperative planning reduces wholesale electricity prices by 64.3 % and interconnection-wide total costs (transmission investments + grid operations) by 34.6 % in 2059. It also helps decrease greenhouse gas emissions by increasing renewable energy utilization. However, the benefits of cooperation diminish during the widespread heat wave when all regions face extreme electricity demand due to higher space cooling needs. Despite this, cooperative transmission planning remains advantageous, particularly for California Independent System Operator with significant diurnal solar generation capacity. This study suggests that cooperation in transmission planning is crucial for reducing costs and increasing reliability both during normal periods and extreme weather events. It highlights the importance of optimizing the strategic investments to mitigate challenges posed by wider-scale extreme weather events of the future.

## Journal reference
Akdemir, K. Z., Mongird, K., Kern, J. D., Oikonomou, K., Voisin, N., Burleyson, C. D., Rice, J. S., Zhao, M., Bracken, C., & Vernon, C. (2025). Investigating the effects of cooperative transmission expansion planning on grid performance during heat waves with varying spatial scales. Applied Energy, 378, 124825. https://doi.org/10.1016/j.apenergy.2024.124825

## Code reference
Akdemir, K. Z., Mongird, K., Kern, J., Oikonomou, K., Voisin, N., Burleyson, C., Rice, J., Zhao, M., Bracken, C., & Vernon, C. R. (2024). Meta-repository for data and code associated with the Akdemir et al. 2024 submission to Applied Energy (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/ZENODO.12693667

## Data references

### Input data
| Dataset | Repository Link | DOI |
|-------|-----------------|-----|
| CERF, reV, TELL and GCAM-USA Inputs | https://data.msdlive.org/records/ph6pp-yfw84 | https://doi.org/10.57931/2338087 |

### Output data
| Dataset | Repository Link | DOI |
|-------|-----------------|-----|
| GO WEST and TEP Outputs | https://data.msdlive.org/records/ph6pp-yfw84 | https://doi.org/10.57931/2338087 |

## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| GO WEST | v1.1.0 | https://github.com/IMMM-SFA/IM3_WECC/tree/Experiment_Version | https://doi.org/10.5281/zenodo.11003229 |
| TEP | v1.0.0 | https://github.com/keremakdemir/Transmission_Expansion_Planner | https://doi.org/10.5281/zenodo.11003185 |
| GCAM-USA | v5.3 | https://github.com/JGCRI/gcam-core | https://doi.org/10.5281/zenodo.3908600 |
| TELL | v1.1.0 | https://github.com/IMMM-SFA/tell | https://doi.org/10.5281/zenodo.8264217 |
| CERF | v2.3.2 | https://github.com/IMMM-SFA/cerf | https://doi.org/10.5281/zenodo.7735212 |
| reV | v0.8.7 | https://github.com/NREL/reV | https://doi.org/10.5281/zenodo.10794962 |

## Reproduce my experiment
Clone this repository to get access to the scripts used to execute GO WEST and TEP simulations for this experiment. These scripts are located in the `workflow` directory and described below. First of all, you need to download the exact GO WEST version (https://doi.org/10.5281/zenodo.11003229) and TEP version (https://doi.org/10.5281/zenodo.11003185) used in this experiment. Also, you need to download all input data specified above (https://doi.org/10.57931/2338087). Then, you need to copy and paste CERF and reV, TELL and GCAM-USA inputs to "Model_setup\IM3_interactions\CERF\CERF_outputs", "Model_setup\IM3_interactions\TELL\TELL_outputs", and "Model_setup\IM3_interactions\GCAM\GCAM_outputs" folders in GO WEST model, respectively. You will start by setting the years in `Experiment_wrapper.py` according to `Experiment_flowchart.png` file. These will provide you with job folders of GO WEST with varying years and input data. For the 2019 base case, you need to run `WECCDataSetup_multimodel.py` and `wrapper_simple_multimodel.py` in order to get GO WEST results. For the remaining simulations with transmission expansion, you need to copy and paste relevant GO WEST job folders to "Datasets\GO_data" folder in TEP model. After that, the next step is using `Model_setup.py` with the years and interregional transmission investment cost penalties outlined in the journal reference. This will provide you with job folders of TEP model for different transmission expansion scenarios. In order to gather the investment results for each scenario/year, move forward with running `TEP_simulation.py`. TEP results include a "line_params.csv" file, which you can directly copy and paste into relevant GO WEST folders to update the transmission line capacities. The last step is to run `WECCDataSetup_multimodel.py` and `wrapper_simple_multimodel.py` in order to get GO WEST results with TEP integration for the scenarios with transmission expansion.

| Script Number | Script Name | Description |
| --- | --- | --- |
| 1 | `Experiment_wrapper.py` | Creates GO WEST simulation folders by utilizing specific years of CERF, TELL, GCAM-USA, reV, hydropower data, and climate/socioeconomic scenario |
| 2 | `WECCDataSetup_multimodel.py` | Creates WECC_data.dat file which contains all necessary inputs to run GO WEST model |
| 3 | `wrapper_simple_multimodel.py` | Initiates GO WEST simulation after specifying the number of days to run and the optimization solver to use |
| 4 | `Model_setup.py` | Creates TEP simulation folders with respect to a specific transmission expansion year and an interregional transmission investment cost penalty |
| 5 | `TEP_simulation.py` | Initiates TEP simulation after specifying the yearly transmission investment budget and optimization solver to use |

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication.

| Figure Number | Script Name | Description |
| --- | --- | --- |
| 1 | `Heatwave_load_comparison.py`, `Heatwave_temperature_analysis.py` | Shows peak hourly temperature distributions and electricity demand time series during local and widespread heat waves |
| 2 | `TPR_topology_map.py` | Shows 125 node topology of U.S. Western Interconnection and three transmission planning regions (TPRs) |
| 3 | `Experiment_flowchart.pptx`, `Experiment_flowchart.png` | Shows the flowchart of experimental setup |
| 4 | `Heatwave_outcomes_timeseries.py` | Shows LMPs and unserved energy during local and widespread heat waves under different scenarios in 2019 |
| 5 | `Transmission_additions.py` | Shows transmission capacity additions under different scenarios between 2015 and 2055 |
| 6 | `Generator_map_capacity_bubble.py` | Shows generator locations, capacities, and total capacity by generation type for 2015 and 2055 |
| 7 | `LMP_ECDF_distribution.py` | Shows ECDF of LMPs for U.S. Western Interconnection and three TPRs in 2059 |
| 8 | `Annual_genmix_WECC.py`, `TPR_demand_gen_barplot.py` | Shows annual generation mix of U.S. Western Interconnection and generation/demand under different scenarios for three TPRs in 2059 |
| 9 | `Heatwave_outcomes_timeseries.py` | Shows LMPs and unserved energy during local and widespread heat waves under different scenarios in 2059 |
| 10 | `Power_flow_map.py` | Shows average interregional power flow as well as net demands, imports, solar/wind generation and curtailment, and LMP distributions during local and widespread heat waves and the whole year |

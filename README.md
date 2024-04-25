_your zenodo badge here_

# akdemir-etal_2024_applied_energy

**Investigating the Effects of Cooperation Level in Transmission Expansion Planning for Decarbonization**

Kerem Ziya Akdemir<sup>1\*</sup>, Kendall Mongird<sup>2</sup>, Jordan D. Kern<sup>1</sup>, Konstantinos Oikonomou<sup>2</sup>, Nathalie Voisin<sup>2,3</sup>, Casey D. Burleyson<sup>2</sup>, Jennie S. Rice<sup>2</sup>, Mengqi Zhao<sup>2</sup>, Cameron Bracken<sup>2</sup>, and Chris Vernon<sup>2</sup>

<sup>1 </sup> North Carolina State University, Raleigh, NC, USA   
<sup>2 </sup> Pacific Northwest National Laboratory, Richland, WA, USA  
<sup>3 </sup> University of Washington, Seattle, WA, USA

\* corresponding author: kakdemi@ncsu.edu

## Abstract
Electricity grids around the world are undergoing significant transformation due to decarbonization and sectoral electrification efforts. There is a significant need for new transmission lines to connect renewable energy sources like solar and wind power, but institutional and economic challenges hinder the necessary actions. This study examines the potential impact of cooperation in transmission expansion planning, using an advanced modeling chain to simulate power grid operations of Western Interconnection in 2019 and 2059 under different levels of collaboration between transmission planning regions. Also, two historical heat waves with varying spatial scope (local vs. widespread) in 2019 are replayed under future climate change in 2059 to assess the transmission cooperation benefits. The results show that cooperative transmission planning yields the best outcomes in terms of reducing wholesale electricity prices and minimizing energy outages both for the whole interconnection and individual transmission planning regions. It also helps decrease greenhouse gas emissions by reducing reliance on fossil fuel resources and/or increasing renewable energy utilization. However, the benefits of transmission cooperation diminish during widespread heat waves when all regions face extreme electricity demand due to space cooling needs. Despite this, cooperative transmission planning remains advantageous, particularly for California Independent System Operator (CAISO) with significant solar installations. The study suggests that cooperation in transmission planning is crucial for reducing costs and increasing reliability both during normal periods and extreme weather events. Furthermore, it highlights the importance of strategic storage investment optimization to mitigate challenges posed by wider-scale extreme weather events of the future.

## Journal reference
Akdemir, K. Z., Mongird, K., Kern, J. D., Oikonomou, K., Voisin, N., Burleyson, C. D., Rice, J. S., Zhao, M., Bracken, C., & Vernon, C. (2024). Investigating the Effects of Cooperation Level in Transmission Expansion Planning for Decarbonization. Applied Energy (in preparation)

## Code reference
Akdemir, K. Z., Mongird, K., Kern, J. D., Oikonomou, K., Voisin, N., Burleyson, C. D., Rice, J. S., Zhao, M., Bracken, C., & Vernon, C. (2024). Supporting code for Akdemir et al. 2024 - Applied Energy [Code]. Zenodo.

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
| GCAM-USA | v5.3 | https://github.com/JGCRI/gcam-core | https://doi.org/10.57931/1960381 |
| TELL | v1.1.0 | https://github.com/IMMM-SFA/tell | https://doi.org/10.5281/zenodo.8264217 |
| CERF | v2.3.2 | https://github.com/IMMM-SFA/cerf | https://doi.org/10.5281/zenodo.7735212 |
| reV | v0.8.7 | https://github.com/NREL/reV | https://doi.org/10.5281/zenodo.10794962 |

## Reproduce my experiment
Clone this repository to get access to the scripts used to execute GO WEST and TEP simulations for this experiment. These scripts are located in the `workflow` directory and described below. First of all, you need to download the exact GO WEST version (https://doi.org/10.5281/zenodo.11003229) and TEP version (https://doi.org/10.5281/zenodo.11003185) used in this experiment. Also, you need to download all input data specified above (https://doi.org/10.57931/2338087). Then, you need to copy and paste CERF and reV, TELL and GCAM-USA inputs to GO WEST model to "Model_setup\IM3_interactions\CERF\CERF_outputs", "Model_setup\IM3_interactions\TELL\TELL_outputs", and "Model_setup\IM3_interactions\GCAM\GCAM_outputs" folders in GO WEST model, respectively. You will start by setting the years in `Experiment_wrapper.py` according to `Experiment_flowchart.pptx` file. These will provide you with job folders of GO WEST with varying years and input data. For the 2019 base case, you need to run `WECCDataSetup_multimodel.py` and `wrapper_simple_multimodel.py` in order to get GO WEST results. For the remaining simulations with transmission expansion, you need to copy and paste relevant GO WEST job folders to "Datasets\GO_data" in TEP model. After that, the next step is using `Model_setup.py` with the years and interregional transmission investment cost penalties outlined in the journal reference. This will provide you with job folders of TEP for different transmission expansion scenarios. In order to gather the investment for each scenario/year, move forward with running `TEP_simulation.py`. TEP results include a "line_params.csv" file, which you can directly copy and paste into relevant GO WEST folders to update the transmission line capacities. The last step is to run `WECCDataSetup_multimodel.py` and `wrapper_simple_multimodel.py` for the scenarios with transmission expansion in order to get GO WEST results with TEP integration.

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
| 3 | `Experiment_flowchart.pptx` | Shows the flowchart of experimental setup |
| 4 | `LMP_ECDF_distribution.py` | Shows ECDF of LMPs for U.S. Western Interconnection and three TPRs in 2019 |
| 5 | `Annual_genmix_WECC.py`, `TPR_demand_gen_barplot.py` | Shows annual generation mix of U.S. Western Interconnection and generation/demand under different scenarios for three TPRs in 2019 |
| 6 | `Heatwave_outcomes_timeseries.py` | Shows LMPs and unserved energy during local and widespread heat waves under different scenarios in 2019 |
| 7 | `Transmission_additions.py` | Shows transmission capacity additions under different scenarios between 2015 and 2055 |
| 8 | `Generator_map_capacity_bubble.py` | Shows generator locations, capacities, and total capacity by generation type for 2015 and 2055 |
| 9 | `LMP_ECDF_distribution.py` | Shows ECDF of LMPs for U.S. Western Interconnection and three TPRs in 2059 |
| 10 | `Annual_genmix_WECC.py`, `TPR_demand_gen_barplot.py` | Shows annual generation mix of U.S. Western Interconnection and generation/demand under different scenarios for three TPRs in 2059 |
| 11 | `Heatwave_outcomes_timeseries.py` | Shows LMPs and unserved energy during local and widespread heat waves under different scenarios in 2059 |
| 12 | `Heatwave_maps_LMP.py` | Shows nodal average LMPs during local and widespread heat waves under different scenarios in 2059 |
| 13 | `Power_flow_map.py` | Shows average interregional power flow as well as net demands, imports, solar/wind generation and curtailment, and LMP distributions during local and widespread heat waves and the whole year |

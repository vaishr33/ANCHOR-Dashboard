# Day 2 Notes

## Completed

* Created `notebooks/02_build_access_table.ipynb`
* Loaded cleaned Massachusetts municipality lookup table
* Loaded cleaned recovery service datasets
* Aggregated SAMHSA treatment facilities by municipality
* Aggregated peer recovery centers by municipality
* Aggregated syringe service programs by municipality
* Aggregated harm reduction programs by municipality
* Created municipality-level recovery access table
* Added service count columns for each recovery service category
* Created binary service availability flags for each municipality
* Created `service_diversity_score` from 0 to 4
* Fixed municipality matching issues using a town crosswalk
* Standardized neighborhood and village names to official municipalities
* Repaired harm reduction program location matching using ZIP-code-to-town mapping
* Confirmed all service datasets could be matched to Massachusetts municipalities
* Loaded cleaned overdose deaths by town dataset
* Loaded cleaned EMS suspected opioid-related incidents by town dataset
* Built municipality-level burden table
* Added `avg_deaths_2021_2023` as fatal overdose burden indicator
* Added `avg_ems_incidents_2022_2023` as EMS opioid-related response burden indicator
* Created overdose death burden ranks
* Created EMS incident burden ranks
* Joined recovery access indicators with overdose and EMS burden indicators
* Created first version of the Recovery Access Gap Index
* Calculated burden percentiles for overdose deaths and EMS incidents
* Calculated `combined_burden_pct`
* Calculated `access_coverage_pct`
* Created `recovery_access_gap_score`
* Added readable gap categories
* Created final municipality-level gap index table
* Joined gap index table back to municipality boundaries
* Created map-ready GeoJSON for dashboard mapping
* Created quick static map preview in notebook
* Created Top 20 recovery access gap towns table
* Pushed notebook 2 and 3 changes to GitHub

## Created Processed Outputs

* `municipality_recovery_access_table.csv`
* `municipality_burden_table.csv`
* `municipality_recovery_access_gap_index.csv`
* `municipality_recovery_access_gap_index.geojson`
* `top_20_recovery_access_gap_towns.csv`

## Key Methodology Decisions

* Used municipalities as the main unit of analysis
* Treated SAMHSA, peer recovery, syringe service programs, and harm reduction programs as separate recovery access categories
* Used `service_diversity_score` to measure how many different service types are present in each municipality
* Used 2021–2023 average overdose deaths as fatal overdose burden
* Used 2022–2023 average EMS suspected opioid-related incidents as emergency response burden
* Interpreted EMS incidents as a response burden proxy, not a strict nonfatal overdose count
* Defined the first Recovery Access Gap Score as high burden combined with low service access

## Next Steps

* Use the final priority index from notebook 3 as the main dashboard dataset
* Build the Streamlit dashboard
* Add dashboard KPI cards
* Add interactive Massachusetts municipality map
* Add Top Priority Communities table
* Add access-vs-burden explorer
* Add filters for county, priority category, and gap category
* Add methodology notes to the dashboard
* Add screenshots and dashboard instructions to the README
* Prepare final LinkedIn and portfolio write-up

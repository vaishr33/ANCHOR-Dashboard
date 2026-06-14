# Day 4 Notes

## Completed

* Fixed invalid negative SVI values in the final dashboard data
* Identified that negative SVI sentinel values were being included in municipality-level SVI aggregation
* Reloaded the SVI tract CSV, tract shapefile, and municipality boundaries explicitly
* Recreated `svi_geo` using the cleaned SVI table and tract geometries
* Cleaned SVI ranking fields so valid values remain between `0` and `1`
* Cleaned SVI percentage fields so valid values remain between `0` and `100`
* Rebuilt the tract-town spatial overlay
* Confirmed the overlay had valid population, SVI, municipality, and area-weight values
* Recomputed municipality-level SVI using corrected weighted averages
* Confirmed Boston no longer had invalid negative SVI values
* Rebuilt the final priority index with corrected SVI values
* Reran Notebook 3 after fixing SVI cleaning
* Reran Notebook 4 so distance-adjusted outputs used the corrected priority data
* Added/updated `anchor_priority_score`
* Added/updated `anchor_priority_level`
* Added `anchor_priority_rank`
* Recomputed priority levels by rank
* Confirmed the top 10% equals 36 very high priority municipalities
* Fixed the issue where only 9 municipalities were showing as very high priority
* Fixed the issue where Yarmouth was labeled very high priority despite appearing lower in the ranked table
* Restored the tabbed Streamlit dashboard layout
* Fixed the map so it only appears in the Map Overview tab
* Fixed missing `anchor_priority_score` and `anchor_priority_level` errors in the dashboard
* Patched the final CSV and GeoJSON so the map and tables use the same ANCHOR fields
* Confirmed the Community Profile, Map Overview, Top Communities, Access Explorer, and Terms & Score Guide tabs work locally
* Ran final data crosschecks for row counts, SVI ranges, score validity, rank labels, distance metrics, and dashboard outputs
* Updated the README with harm reduction oriented public framing
* Updated the public project title to `ANCHOR: Massachusetts Harm Reduction Access & Overdose Burden Dashboard`
* Removed recovery-only public-facing project language where needed
* Renamed the GitHub repository to `anchor-harm-reduction-dashboard`
* Updated the local Git remote after the repository rename
* Resolved Git merge and cleanup issues before pushing updates

## Updated Processed Outputs

* `municipality_final_priority_index.csv`
* `municipality_final_priority_index.geojson`
* `municipality_final_priority_index_with_distance.csv`
* `municipality_final_priority_index_with_distance.geojson`

## Key Methodology Decisions

* Treated SVI ranking fields as valid only when values are between `0` and `1`
* Converted invalid SVI sentinel values to missing before aggregation
* Used corrected weighted averages for tract-to-municipality SVI aggregation
* Used metric-specific denominators so invalid SVI values did not distort municipal averages
* Continued using municipality as the dashboard unit of analysis
* Recomputed ANCHOR priority levels by rank instead of relying on stale category labels
* Defined very high priority as the top 10% of municipalities by ANCHOR Priority Score
* Kept the public-facing framing focused on harm reduction access, overdose burden, naloxone access, outreach, and recovery support visibility
* Avoided using recovery-only project naming in public-facing README and dashboard text
* Kept backend column names unchanged when renaming them would risk breaking the working dashboard

## Validation Checks

* Confirmed final CSV has 351 municipalities
* Confirmed final GeoJSON has 351 municipalities
* Confirmed `town_join` is complete and unique
* Confirmed CSV and GeoJSON municipality sets match
* Confirmed SVI values are within valid ranges
* Confirmed `social_vulnerability_pct` is between `0` and `1`
* Confirmed no invalid negative SVI values remain
* Confirmed no negative priority scores remain
* Confirmed 36 municipalities are labeled very high priority
* Confirmed priority ranks and priority labels are consistent
* Confirmed Boston’s SVI value is valid
* Confirmed Yarmouth’s rank and priority label are consistent
* Confirmed service distance fields are non-negative
* Confirmed 10-mile service counts are not lower than 5-mile service counts
* Confirmed service count fields align with service indicator fields
* Confirmed the dashboard renders locally after cache clearing

## Current Status

* Dashboard is working locally
* Final data outputs are corrected and validated
* README has been updated with harm reduction oriented framing
* GitHub repository has been renamed
* Project is ready for Streamlit deployment

## Next Steps

* Deploy the Streamlit app
* Add the deployed dashboard link to the README
* Run one final check on the deployed dashboard
* Confirm public-facing text uses the updated ANCHOR harm reduction framing
* Add dashboard screenshots to the repository
* Prepare a short portfolio summary
* Prepare a LinkedIn post summarizing the project

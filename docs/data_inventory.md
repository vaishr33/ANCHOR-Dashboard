# Data Inventory

## Project

Recovery Access Gap Index

## Goal

Track all public datasets used to build the Massachusetts recovery access and overdose burden analysis.

## Dataset Tracker

| Dataset | Source | Use | Geography | Status | Notes |
|---|---|---|---|---|---|
| Massachusetts Municipal Boundaries | MassGIS | Base map and spatial joins | Municipality | Downloaded | Shapefile saved locally in data/raw/massgis_municipalities/ |
| Opioid-related overdose deaths by city/town | Massachusetts DPH | Fatal overdose burden | Municipality | Downloaded | June 2024 DOC/DOCX saved locally in data/raw/overdose_deaths/. Contains city/town data from 2016–2023 |
| EMS opioid-related incidents | Massachusetts DPH / EMS dashboard | Nonfatal overdose burden proxy | Municipality or region | Downloaded | June 2024 DOCX saved locally in data/raw/ems_incidents/ |
| Harm Reduction Program Locator | Mass.gov | Harm reduction and naloxone access | Point locations | Found | Public Tableau embed found; image download available, raw data export not yet identified. |
| Syringe Service Programs | Mass.gov | SSP access | Point locations | Found | Public map/locator found; raw data export not yet identified. |
| Peer Recovery Support Centers | Mass.gov | Recovery support access | Point locations | Found | Public webpage list found, organized by region. Raw download not available; will convert list to structured CSV later. |
| SAMHSA FindTreatment.gov | SAMHSA | Treatment/MOUD access | Point locations | Not downloaded | Massachusetts facilities only |
| CDC/ATSDR Social Vulnerability Index | CDC/ATSDR | Social vulnerability | Census tract/county | Not downloaded | May need aggregation to municipality |
| ACS 5-year demographic data | Census | Population, poverty, no vehicle, uninsured | Tract/place | Optional | Backup if SVI is hard |

## MVP Dataset Priority

### Must Have

1. Massachusetts municipal boundaries
2. Opioid-related overdose deaths by municipality
3. Harm reduction / naloxone locations
4. Syringe service program locations
5. Peer recovery support centers
6. SAMHSA treatment facilities
7. SVI or ACS vulnerability data
   

### Nice to Have

1. EMS opioid-related incidents
2. Syringe service program locations
3. MOUD-specific facility details
4. Hospital / emergency department locations
5. Transit or drive-time access

## Notes

Raw data files will be stored locally in `data/raw/`.

Cleaned datasets will be stored locally in `data/processed/`.

Large data files are not committed to GitHub.

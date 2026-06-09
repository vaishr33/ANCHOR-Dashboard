# Data Inventory

## Project

Recovery Access Gap Index

## Goal

Track all public datasets used to build the Massachusetts recovery access and overdose burden analysis.

## Dataset Tracker

| Dataset | Source | Use | Geography | Status | Notes |
|---|---|---|---|---|---|
| Massachusetts Municipal Boundaries | MassGIS | Base map and spatial joins | Municipality | Not downloaded | Needed first |
| Opioid-related overdose deaths by city/town | Massachusetts DPH | Fatal overdose burden | Municipality | Not downloaded | Main burden dataset |
| EMS opioid-related incidents | Massachusetts DPH / EMS dashboard | Nonfatal overdose burden proxy | Municipality or region | Not downloaded | Optional if downloadable |
| Harm Reduction Program Locator | Mass.gov | Harm reduction and naloxone access | Point locations | Not downloaded | Includes programs, services, contact info |
| Syringe Service Programs | Mass.gov | SSP access | Point locations | Not downloaded | Fixed/mobile locations |
| Peer Recovery Support Centers | Mass.gov | Recovery support access | Point locations | Not downloaded | Peer-led recovery support |
| SAMHSA FindTreatment.gov | SAMHSA | Treatment/MOUD access | Point locations | Not downloaded | Massachusetts facilities only |
| CDC/ATSDR Social Vulnerability Index | CDC/ATSDR | Social vulnerability | Census tract/county | Not downloaded | May need aggregation to municipality |
| ACS 5-year demographic data | Census | Population, poverty, no vehicle, uninsured | Tract/place | Optional | Backup if SVI is hard |

## MVP Dataset Priority

### Must Have

1. Massachusetts municipal boundaries
2. Opioid-related overdose deaths by municipality
3. Harm reduction / naloxone locations
4. Peer recovery support centers
5. SAMHSA treatment facilities
6. SVI or ACS vulnerability data

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

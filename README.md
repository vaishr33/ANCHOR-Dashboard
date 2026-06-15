# ANCHOR: Massachusetts Harm Reduction Access & Overdose Burden Dashboard

**Live dashboard:** https://anchor-ma-dashboard.streamlit.app/

**ANCHOR** stands for **Access to Naloxone, Care, Harm Reduction, Outreach, and Recovery**.

ANCHOR is a Massachusetts municipality-level public health dashboard that explores where overdose burden, social vulnerability, and limited **source-listed** harm reduction and recovery support visibility may overlap.

The dashboard is designed as an exploratory planning and portfolio project. It brings together overdose burden, EMS burden, social vulnerability, in-town service listings, and nearby service access indicators to help identify communities that may warrant closer review for outreach planning, naloxone access, harm reduction expansion, service gap analysis, and public health resource prioritization.

ANCHOR should not be interpreted as a definitive service inventory, clinical tool, or policy decision engine.

---

## Project Objective

This project asks:

> Where in Massachusetts do overdose burden, social vulnerability, and limited source-listed harm reduction supports overlap?

ANCHOR combines municipality-level public health and access indicators into a Streamlit dashboard that allows users to explore:

* overdose burden
* EMS burden
* social vulnerability
* in-town service listings
* nearby service access
* distance to listed services
* municipality-level priority rankings

The goal is not to claim that a municipality definitively has or does not have services. Instead, ANCHOR highlights where publicly available, structured datasets suggest possible access, visibility, or service-listing gaps that may deserve further review.

---

## Why This Matters

Overdose risk and service access are not evenly distributed across communities. A municipality may experience high overdose burden while also facing social vulnerability, limited source-listed services, or distance barriers to nearby support.

ANCHOR helps make these overlaps easier to see by combining multiple public health indicators into one municipality-level view.

The project emphasizes harm reduction access, overdose burden, naloxone access, recovery support visibility, and practical service discoverability rather than treating “access” as a simple yes/no measure.

---

## Dashboard Features

The Streamlit dashboard includes five main sections.

### Map Overview

An interactive Massachusetts municipality map showing ANCHOR Priority Score and priority level.

The map includes hover details such as:

* ANCHOR Priority Score
* priority level
* harm reduction access gap level
* nearest listed service
* services within 5 miles
* services within 10 miles
* social vulnerability
* average overdose deaths
* average EMS incidents

### Community Profile

A searchable municipality-level profile showing burden, vulnerability, access, and distance metrics for a selected community.

### Top Communities

A ranked list of municipalities by ANCHOR Priority Score, with searchable table and chart views.

### Access Explorer

A scatterplot comparing harm reduction access gap and social vulnerability across municipalities.

### Terms & Score Guide

A plain-language explanation of core terms, score logic, assumptions, and caveats.

---

## Core Measures

### Overdose Burden

Uses average annual overdose deaths from 2021–2023.

### EMS Burden

Uses average annual EMS incidents from 2022–2023.

### Social Vulnerability

Uses CDC/ATSDR Social Vulnerability Index tract-level data aggregated to municipalities.

The primary SVI field used is the overall SVI ranking field:

```text
RPL_THEMES
```

This value ranges from `0` to `1`, where higher values indicate greater relative social vulnerability.

### In-Town Service Access

Tracks whether source-listed services appear within a municipality.

Tracked service categories include:

* treatment facilities
* peer recovery centers
* syringe service programs
* harm reduction program listings

A municipality with zero tracked in-town listings should not be interpreted as having no services. It means no services from the tracked source-listed categories were identified inside that municipality in the datasets used for this project.

### Nearby Service Access

Nearby service access is included because a municipality may not have an in-town listing but may still be close to services in nearby municipalities.

Distance-based metrics include:

* nearest listed service distance
* services within 5 miles
* services within 10 miles
* service types within 5 miles
* service types within 10 miles

Distance estimates are approximate and should not be interpreted as travel time.

---

## ANCHOR Priority Score

The ANCHOR Priority Score combines burden, vulnerability, in-town service access, and nearby service access.

Simplified score logic:

```text
Harm Reduction Access Gap Score = Burden × (1 - In-Town Service Access)

SVI-Adjusted Score = Harm Reduction Access Gap Score × (1 + Social Vulnerability)

ANCHOR Priority Score = SVI-Adjusted Score × (1 - 0.35 × Nearby Access)
```

The nearby access adjustment is intentionally conservative. Nearby services can reduce the score, but they do not erase it entirely because geographic proximity does not fully capture:

* transportation barriers
* service hours
* eligibility
* capacity
* stigma
* language access
* service fit
* whether services are realistically usable

---

## Priority Levels

Municipalities are assigned priority levels by rank:

```text
Very high priority = top 10%
High priority = next 15%
Moderate priority = next 25%
Lower priority = remaining municipalities
```

Massachusetts has 351 municipalities in this project, so the top 10% corresponds to 36 very high priority municipalities.

---

## Data Sources

This project uses publicly available and source-listed datasets, including:

* Massachusetts municipal boundaries
* Massachusetts overdose deaths by city/town
* Massachusetts EMS incident data
* CDC/ATSDR Social Vulnerability Index
* SAMHSA treatment locator data
* peer recovery, syringe service, and harm reduction resource listings

Service data is source-listed and should not be interpreted as a complete operational inventory of all harm reduction, treatment, recovery, or naloxone-related services in Massachusetts.

---

## Data Processing Overview

The project follows this general pipeline:

```text
Raw public health and service datasets
    ↓
Municipality boundary cleaning
    ↓
Overdose and EMS burden processing
    ↓
Service access table creation
    ↓
SVI tract-to-municipality aggregation
    ↓
Distance-based access metric calculation
    ↓
Final ANCHOR priority index
    ↓
Streamlit dashboard
```

Final dashboard files:

```text
data/processed/municipality_final_priority_index_with_distance.csv
data/processed/municipality_final_priority_index_with_distance.geojson
```

---

## Validation Checks

Before deployment, the final dashboard data was checked for:

* 351 municipalities in the final CSV
* 351 municipalities in the final GeoJSON
* complete and unique municipality join keys
* matching CSV and GeoJSON municipality sets
* valid SVI values between `0` and `1`
* no invalid negative SVI values
* no negative priority scores
* 36 very high priority municipalities
* consistent municipality ranking and priority labels
* valid Boston and Yarmouth profile values
* non-negative distance metrics
* consistent service count, service type, and nearest-distance fields
* map, profile, top communities, explorer, and terms tabs rendering correctly

---

## Important Caveats

ANCHOR is an exploratory dashboard, not a definitive public health decision tool.

Important limitations:

* Service listings are not a complete service inventory.
* Zero tracked in-town listings does not mean a municipality has no services.
* Some organizations may exist locally but not appear in the structured datasets used here.
* Services may be listed under parent organizations, nearby municipalities, or categories outside this project’s tracked service types.
* Distance calculations are approximate.
* Distance does not capture transportation access, appointment availability, service capacity, eligibility, service hours, language access, or service fit.
* Municipality-level analysis can hide neighborhood-level variation.
* The score is intended for prioritization and exploration, not final policy determination.

---

## Repository Structure

```text
project-root/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── municipality_final_priority_index_with_distance.csv
│       └── municipality_final_priority_index_with_distance.geojson
│
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_build_access_table.ipynb
│   ├── 03_build_final_priority_index.ipynb
│   └── 04_build_distance_access_metrics.ipynb
│
├── docs/
│   ├── day1_notes.md
│   ├── day2_notes.md
│   ├── day3_notes.md
│   └── day4_notes.md
│
├── README.md
└── pyproject.toml
```

---

## Tech Stack

* Python
* pandas
* NumPy
* GeoPandas
* Plotly
* Streamlit
* Shapely
* PyProj
* uv

---

## Future Improvements

Potential future improvements include:

* more complete service inventory validation
* public transit access metrics
* travel-time based distance estimates
* additional harm reduction and naloxone resource categories
* longitudinal overdose burden trends
* neighborhood or tract-level drilldowns
* service capacity and hours-of-operation indicators
* verified service source links
* clearer distinction between treatment, recovery, harm reduction, and naloxone access resources

---

## Project Framing

ANCHOR is harm reduction oriented.

The project focuses on overdose burden, social vulnerability, harm reduction access, naloxone access, recovery support visibility, and public service-listing gaps across Massachusetts municipalities.

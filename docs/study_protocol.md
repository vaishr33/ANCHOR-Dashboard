# Study Protocol

## Project Title

Recovery Access Gap Index: Mapping Overdose Burden and Recovery Resource Gaps Across Massachusetts

## Project Goal

This project investigates whether recovery, harm reduction, and treatment resources in Massachusetts are geographically aligned with communities experiencing high overdose burden and social vulnerability.

The final output will be an interactive dashboard and short research brief that identify municipalities that may be underserved relative to overdose burden.

## Primary Research Question

Which Massachusetts municipalities experience high overdose burden and social vulnerability but limited geographic access to recovery and harm reduction resources?

## Secondary Research Questions

1. Which Massachusetts municipalities have the highest overdose burden?
2. Where are recovery, harm reduction, and treatment resources located?
3. Which municipalities appear underserved relative to overdose burden?
4. Are access gaps associated with social vulnerability?
5. Which communities may be priority candidates for additional public health investment?

## Unit of Analysis

The primary unit of analysis is the Massachusetts municipality, meaning city or town.

## Geographic Scope

Massachusetts, United States.

## Core Data Layers

This project will use publicly available data sources, including:

1. Massachusetts municipal boundaries
2. Opioid-related overdose deaths by municipality
3. EMS opioid-related incidents, if available at a usable geography
4. Harm reduction and naloxone distribution locations
5. Syringe service program locations
6. Peer recovery support center locations
7. Treatment and MOUD provider locations
8. Social vulnerability indicators from CDC/ATSDR SVI or ACS Census data

## Overdose Burden Indicators

Potential burden indicators include:

- Fatal opioid overdose deaths
- Fatal opioid overdose death rate per 100,000 residents
- Three-year rolling overdose death rate
- EMS opioid-related incidents
- EMS naloxone administrations
- Recent change in overdose burden over time

## Recovery Access Indicators

Potential access indicators include:

- Number of recovery, treatment, and harm reduction services in each municipality
- Services per 100,000 residents
- Number of service types available in or near each municipality
- Distance to nearest harm reduction site
- Distance to nearest syringe service program
- Distance to nearest peer recovery center
- Distance to nearest treatment or MOUD provider
- Number of services within a defined radius, such as 10 miles

## Social Vulnerability Indicators

Potential vulnerability indicators include:

- Overall Social Vulnerability Index percentile
- Poverty rate
- No vehicle access
- Uninsured rate
- Housing instability
- Disability
- Limited English proficiency

## Planned Composite Scores

### 1. Overdose Burden Index

A percentile-based score representing overdose burden in each municipality.

Possible formula:

Burden Index = percentile rank of overdose death rate

If EMS incident data is available:

Burden Index = 0.70 * fatal overdose rate percentile + 0.30 * EMS opioid incident rate percentile

### 2. Recovery Access Index

A percentile-based score representing access to recovery, treatment, and harm reduction resources.

Possible inputs:

- Service density
- Service diversity
- Services within 10 miles
- Distance to nearest harm reduction or treatment resource
- Transportation access to nearby recovery, harm reduction, and treatment services

### 3. Social Vulnerability Index

A percentile-based score representing structural vulnerability.

This may use the CDC/ATSDR SVI overall percentile or a custom score based on ACS variables such as poverty, no vehicle access, and uninsured rate.

### 4. Need Index

Need Index = 0.75 * Overdose Burden Index + 0.25 * Social Vulnerability Index

### 5. Recovery Access Gap Score

Gap Score = Need Index - Recovery Access Index

Higher gap scores indicate communities with relatively high need and relatively low access.

## Priority Classification

Municipalities will be grouped into categories:

| Category | Meaning |
|---|---|
| High Need / Low Access | Highest priority for further investigation or investment |
| High Need / High Access | High burden but existing resource presence |
| Low Need / Low Access | Lower immediate priority, monitor over time |
| Low Need / High Access | Possible regional service hub |

## Planned Dashboard Outputs

The dashboard will include:

- Massachusetts overdose burden map
- Recovery and harm reduction service location map
- Recovery Access Gap Score map
- Burden vs. access scatterplot
- Municipality profile view
- Priority municipality ranking table
- Service type filters
- Social vulnerability overlay

## Intended Use

This project is intended as a public health decision-support tool. It can help identify communities that may warrant further investigation, outreach, mobile services, naloxone distribution, peer recovery support, MOUD access expansion, or other recovery and harm reduction investment.

## Limitations

This analysis estimates geographic and structural access. It does not measure:

- Service quality
- Service capacity
- Waitlists
- Hours of operation
- Real-time availability
- Insurance acceptance
- Stigma
- Language access
- Actual service utilization
- Individual-level overdose risk

The results should not be interpreted causally. The project identifies potential geographic mismatch between overdose burden and service access, not whether service availability directly causes changes in overdose outcomes.

## Expected Deliverables

1. Clean municipality-level dataset
2. Recovery service location dataset
3. Recovery Access Gap Index
4. Interactive dashboard
5. Short research brief
6. GitHub repository
7. Portfolio case study

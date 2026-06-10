# Manual Data Templates

Some recovery access datasets are available publicly as web locators or webpage lists rather than clean downloadable CSV files. These sources will be manually structured into CSV files under `data/raw/manual_sources/`.

The raw manual CSV files are ignored by Git because the `data/` folder is not committed.

## Manual CSV Schema

Each manual source file uses the same structure:

| Column | Description |
|---|---|
| name | Program or organization name |
| address | Street address |
| city | City or town |
| state | State abbreviation |
| zip | ZIP code |
| latitude | Latitude, if available |
| longitude | Longitude, if available |
| service_type | Type of service provided |
| source_url | Public source page or locator URL |
| notes | Notes about extraction, uncertainty, or source details |

## Manual Source Files

| File | Purpose |
|---|---|
| harm_reduction_programs.csv | Harm reduction and naloxone access locations |
| syringe_service_programs.csv | Syringe service program access locations |
| peer_recovery_centers.csv | Peer recovery support center locations |

## Planned Use

These files will support the Recovery Access Index by measuring whether each municipality has nearby access to:

- treatment facilities
- harm reduction programs
- syringe service programs
- peer recovery support centers

The final access score will include both proximity and service diversity.
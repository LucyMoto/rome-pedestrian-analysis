# Rome Pedestrian Accident Analysis (2013–2022)

Data science project analysing pedestrian accident patterns in Rome using clustering and geospatial analysis.

# Project Snapshot

| Item         | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| **Dataset**  | ~686,000 accident records (116 monthly CSV files)                     |
| **Location** | Rome, Italy                                                           |
| **Period**   | 2013–2022                                                             |
| **Goal**     | Identify patterns and high-risk environments for pedestrian accidents |
| **Methods**  | clusPCAmix, DBSCAN, PAM, K-Prototypes, PCA                           |
| **Tools**    | Python, R, Pandas, Scikit-learn, Folium, PCAmixdata                   |
| **Output**   | 5 accident typology clusters + 80 spatial hotspot locations           |

➡️ **Interactive map:**
[Pedestrian Accidents in Rome Maps](https://lucymoto.github.io/rome-pedestrian-accidents/)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![R](https://img.shields.io/badge/R-4.x-276DC3)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-completed-success)

---

# Why This Project Matters

Pedestrian safety is a critical urban challenge.

This project demonstrates how data science can identify recurring accident environments and spatial risk patterns, supporting evidence-based road safety interventions.

The full analysis pipeline was implemented in **Python and R** with an emphasis on **reproducibility, structured workflows, and rigorous methodological validation**.

The repository reproduces the full analysis workflow developed for the thesis:

**"Analysis of Pedestrian Accidents in the Province of Rome Restricted to Incidents Involving a Single Moving Vehicle"**

---

# Key Results

## Temporal-Meteorological Clustering (clusPCAmix, silhouette = 0.66)

Four clustering methods were systematically compared before selecting `clusPCAmix`, which handles mixed numerical/categorical data natively:

| Method | Silhouette | Notes |
|--------|-----------|-------|
| K-Prototypes | 0.26 | Unstable — gamma shifts 11× with feature changes |
| Gower + PAM | 0.40 | Moderate separation |
| Hellinger + PAM | 0.60 | Requires extreme categorical weighting |
| **clusPCAmix** | **0.66** | Best — mixed types, k=5, d=4 dimensions |

**Five distinct accident regimes identified:**

| Cluster | Profile | Share | Key Characteristics |
|---------|---------|-------|---------------------|
| 1 | Warm Daytime | 46% | Dry, warm, afternoon — baseline conditions |
| 2 | Cool Morning Commute | 19% | High humidity, morning rush hour |
| 3 | Wet Evening Peak | 16% | Highest precipitation, twilight |
| 4 | Cold Humid Night | 15% | Coldest, darkest, highest compound risk |
| 5 | Hot Midday | 4% | Hot, dry, midday — rare but distinct |

**Critical finding:** Night and twilight accidents show **nearly double** the rate of poor road conditions vs daytime (35.6% / 35.5% vs 18.5%), revealing a compounding risk from reduced visibility + wet roads occurring simultaneously.

## Spatial Hotspot Analysis (DBSCAN)

- **80 hotspot locations** identified using DBSCAN with haversine distance (eps = 27.5m)
- 4 priority tiers: Critical / High / Medium / Lower
- Validated against the **45 official BPP blackpoints** designated by the Municipality of Rome
- Distinct spatial signatures: motorcycle hotspots, hit-and-run zones, heavy vehicle corridors

---

# Interactive Map

➡️ **View the interactive map**
[Pedestrian Accidents in Rome Maps](https://lucymoto.github.io/rome-pedestrian-accidents/)

The map allows users to:

* explore accident locations across Rome
* visualize spatial clusters of accidents
* inspect accident characteristics by cluster
* identify high-risk areas for pedestrians
* compare algorithm-detected hotspots with municipal pedestrian safety interventions

The interface was designed to make the analysis accessible to **non-technical stakeholders**, including urban planners and policy makers.

---

# Technologies Used

**Python:** pandas, numpy, scikit-learn, geopandas, astral, pytz, pyarrow, matplotlib, seaborn, folium

**R:** PCAmixdata, cluster, fpc, clusterSim, clusterCrit, ggplot2, dplyr

---

# Project Overview

This project analyzes **10 years of accident data from Rome**, focusing specifically on accidents involving pedestrians and a single moving vehicle. The analysis combines:

* large-scale data ingestion and cleaning (116 CSV files, 686k rows)
* multi-stage categorical encoding and feature engineering
* external weather data integration matched to accident timestamps
* astronomical twilight phase classification
* geospatial coordinate cleaning and hotspot detection
* mixed-type unsupervised clustering with full methodological validation

---

# Dataset

The original dataset contains **686,000 accident records** across 116 monthly files with 37 variables per record.

After the full pipeline, the working dataset contains **14,849 rows** — one row per pedestrian per accident — with 10 variables covering coordinates, timestamp, weather, road surface, and injury severity.

---

# Data Pipeline

> **Note on notebook structure:** The notebooks (001–015 + clustering) reflect the exploratory research process, including iterative data quality investigation, categorical variable auditing, and methodology comparison. A production implementation would consolidate this into modular pipeline scripts — the `src/` structure below reflects how this would be organised for deployment.

A key challenge was that police-coded categorical variables contained **systematic data quality issues** — automated tick-boxes creating impossible combinations (e.g. "daylight" flagged consistently at 2am). Rather than recoding unreliable fields, the analysis prioritised **objectively measured variables**: GPS coordinates, timestamps, and externally-sourced weather data. This is a deliberate methodological decision reflecting real-world constraints common in administrative datasets.

```
116 raw CSVs (685,877 rows, 37 cols)
    │
    ▼ 001–002: Ingest & merge
        Validate column counts across all files
        Detect and fix misaligned rows (2015-10, 2018-06, 2022-06)
        Drop artefact column (Unnamed: 37)
        → merged_data.parquet

    ▼ 003: Deduplicate
        Remove false duplicates keyed on accident protocol number
        → data_no_duplicates.parquet

    ▼ 004: Filter to pedestrian accidents (685k → 40,982 rows)
        Remove: falling-from-vehicle, multi-driver, no-driver, no-pedestrian accidents
        Drop columns >80% missing (Airbag, Seatbelt/Helmet)
        Clean Progressivo number inconsistencies
        Handle parked vehicle rows

    ▼ 005: Consolidate person rows (40,982 → 19,713 rows)
        Each accident has separate rows for driver, passenger, pedestrian
        Transfer vehicle and driver information onto the pedestrian row
        Delete driver and passenger rows
        → one row per pedestrian, with full accident context

    ▼ 006: Temporal feature engineering
        Parse and validate DataOraIncidente timestamps (DST-aware, Europe/Rome)
        Drop 26 rows with missing timestamps
        Classify 10 astronomical lighting phases using the astral library:
            night_am | astronomical/nautical/civil dawn |
            daylight am/pm | civil/nautical/astronomical dusk | night_pm
        Extract: YEAR, MONTH, DATE, TIME, DAY_OF_WEEK
        → 19,687 rows

    ▼ 007: Categorical encoding — road & accident variables (19,687 → 19,416 rows)
        Drop rows with extreme missingness across 10 key road/visibility columns
        Remove 70 rows: sudden-braking accidents with no car involved
        Engineer and encode:
            Segnaletica        → 4 binary road_markings indicators
            Pavimentazione     → road_surface (Tarmac / Paved / Damaged / Graveled)
            FondoStradale      → road_conditions (dry / wet / slippery / icy)
            particolaritastrade → road_features (Straight / Intersection / Curve / Roundabout / Slope)
            NaturaIncidente    → accident_type (pedestrian_run_over / obstacle_hit /
                                 parked_vehicle_hit / vehicle_out_of_control)
        Correct Visibilita for 'Curve without clear view' rows

    ▼ 008: Ordered categorical encoding + day features
        Set ordered pandas CategoricalDtype for risk-consistent orderings:
            road_conditions: dry < wet < slippery < icy
            phase_of_day:    day < twilight < night
            visibility:      Insufficiente < Sufficiente < Buona
        Create numeric ordinal codes (*_ord) for algorithms requiring them
        Engineer day-group features: weekend binary, 3-way, 4-way, paired days
        Clean and encode: TipoStrada, Visibilita, Tipolesione, Illuminazione,
                          Traffico, TipoVeicolo
        → 19,416 rows, 58 columns

    ▼ 009: Weather data integration
        Clean Latitude/Longitude columns
        Round accident timestamps to nearest UTC hour
        Left-join hourly weather grid (100% match rate, 19,416 rows)
        Weather variables added: temperature, humidity, precipitation, wind speed,
                                 wind gusts, cloud cover, pressure, snowfall, snow depth
        Engineered lag features: weather_wet/snowy/icy flags,
                                 days_since_last_rain, cumulative_rain_past_24h
        Clean CondizioneAtmosferica (police-recorded atmospheric conditions)

    ▼ 010: Interactive maps; GPS coordinate recovery
        Build exploratory Folium maps for spatial QA
        Recover missing GPS coordinates via Google Maps geocoding API

    ▼ 011: Final schema and feature selection
        Enforce final dtypes (ordered categoricals, Int64, float64)
        Remove redundant severity/count columns to avoid collinearity
        Represent group size as single feature (binary multiple_pedestrians)
        Validate coordinate bounds (Rome bounding box)
        Export feature lists (numeric / categorical / ordinal) for clustering

    ▼ 012: Cluster-ready dataset preparation (19,416 → 14,849 rows)
        Restrict to accidents within the GRA (Rome ring road)
        Drop rows with missing values in required clustering features
        Collapse rare categories (<1% or <100 rows) → "Other"
        Scale numeric block with RobustScaler
        → 14,849 rows, 36 columns, cluster-ready

    ▼ 013: K-Prototypes clustering
        Grid search over K=[2–10], gamma=[0.5–3.0], 5 random seeds
        Select model by lowest objective cost with stability sweep
        Export cluster labels, profiles, elbow plots, gamma heatmap

    ▼ 014: Time segment analysis
        Explore and determine final time-of-day category definitions

    ▼ 015: Final feature winsorization
        Collapse severity levels 3+4 → 3 (Fatal)
        Winsorize at 99th percentile: precipitation, wind gusts,
                                      days_since_last_rain
        → 14,849 rows, analysis-ready for clusPCAmix

    ▼ Clustering notebooks (R): clusPCAmix, PAM, validation
        Systematic comparison of 4 clustering methods
        clusPCAmix: k=5, d=4, silhouette=0.66
        Validation: bootstrap resampling, ARI, Calinski-Harabasz, Davies-Bouldin
```

---

# Feature Engineering Summary

| Feature Group | Variables |
|--------------|-----------|
| **Temporal** | year, month, day of week, time_sin/cos, doy_sin/cos |
| **Lighting** | 10-phase astronomical classification (astral, DST-aware), simplified 3-phase |
| **Weather** | temperature, humidity, precipitation, wind speed/gusts, cloud cover, pressure |
| **Weather lags** | wet/snowy/icy flags, days since last rain, 24h cumulative rainfall |
| **Road** | surface type, conditions (ordered), features, markings (4 binary indicators) |
| **Accident** | type, traffic density, vehicle type, hit-and-run flag |
| **Outcome** | severity (winsorized, 4-level), fatality indicator |

---

# Repository Structure

```
rome-pedestrian-accidents/

├── data/
│   ├── raw/                  # Not included — see Data Access below
│   └── processed/            # Intermediate parquet files (001–015)
│
├── notebooks/                # Full exploratory pipeline (001–015 + clustering)
│
├── src/                      # Modular pipeline scripts
│   ├── data_processing/
│   ├── feature_engineering/
│   ├── clustering/
│   └── visualization/
│
├── analysis/                 # R scripts: clusPCAmix, PAM, validation
│
├── outputs/
│   ├── figures/
│   └── maps/
│
├── config/
│   └── parameters.yaml
│
├── environment.yml
├── README.md
└── LICENSE
```

---

# Requirements

```
Python 3.12
R 4.x
```

Key Python libraries: pandas, numpy, scikit-learn, geopandas, matplotlib, seaborn, astral, pytz, pyarrow, folium, kmodes

Key R packages: PCAmixdata, cluster, fpc, clusterSim, clusterCrit, ggplot2, dplyr

---

# Environment Installation

```bash
conda env create -f environment.yml
conda activate pedestrian-accidents
```

---

# Data Access

Raw data is available from the [Roma Capitale Open Data portal](https://dati.comune.roma.it) (CC BY 4.0). Due to size, raw files are not included in this repository.

The analysis-ready dataset (14,849 rows) can be shared for research purposes — please open an issue.

---

# Methodological Notes

The analysis identifies **statistical associations and patterns**, not causal relationships. Results should be interpreted as **risk indicators** to inform targeted interventions.

---

# Future Work

* integration of traffic flow data
* inclusion of street lighting infrastructure data
* modelling temporal trends in accident risk
* development of predictive models for accident risk
* integration with urban planning datasets

---

# Author

**Lucy Michaels**
Data Scientist – Applied Data Analysis & Generative AI

Master's Degree — *Analisi e Modellazione dei Dati e dei Processi*
Unitelma Sapienza – Rome, 12-2025

---

# License

This project is licensed under the **MIT License**.

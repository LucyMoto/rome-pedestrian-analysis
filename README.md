# Rome Pedestrian Accident Analysis (2013–2022)

Data science project analysing pedestrian accident patterns in Rome using clustering and geospatial analysis.

# Project Snapshot

| Item         | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| **Dataset**  | ~686,000 accident records                                             |
| **Location** | Rome, Italy                                                           |
| **Period**   | 2013–2022                                                             |
| **Goal**     | Identify patterns and high-risk environments for pedestrian accidents |
| **Methods**  | Clustering, PCA, geospatial analysis                                  |
| **Tools**    | Python, Pandas, Scikit-learn, GeoPandas                               |
| **Output**   | Spatial clusters and interactive accident risk map                    |

➡️ **Interactive map:**
[Pedestrian Accidents in Rome Maps](https://lucymoto.github.io/rome-pedestrian-accidents/)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-completed-success)

---

# Why This Project Matters

Pedestrian safety is a critical urban challenge.

This project demonstrates how data science can identify recurring accident environments and spatial risk patterns, supporting evidence-based road safety interventions.

The full analysis pipeline was implemented in **Python** with an emphasis on **reproducibility, structured workflows, and scalable data analysis**.

The repository reproduces the full analysis workflow developed for the Master's thesis:

**“Analysis of Pedestrian Accidents in the Province of Rome Restricted to Incidents Involving a Single Moving Vehicle”**

---

# Key Results

The analysis reveals consistent patterns in the **spatial and contextual conditions associated with pedestrian accidents in Rome**.

Several clusters of accidents correspond to distinct accident environments, including:

* Night-time accidents with **low visibility**
* Accidents near **major intersections**
* Accidents occurring on **wet/slippery roads in poor light**

These clusters highlight recurring combinations of **environmental and infrastructural conditions** associated with pedestrian accidents.

The results can support:

* urban safety planning
* targeted infrastructure interventions
* data-driven road safety policies

---

# Interactive Map

An interactive map of pedestrian accident clusters and high-risk locations is available here:

➡️ **View the interactive map**
[Pedestrian Accidents in Rome Maps](https://lucymoto.github.io/rome-pedestrian-accidents/)

The map allows users to:

* explore accident locations across Rome
* visualize spatial clusters of accidents
* inspect accident characteristics
* identify high-risk areas for pedestrians
* Compare algorithm-detected hotspots with municipal pedestrian safety interventions

The interface was designed to make the analysis accessible to **non-technical stakeholders**, including urban planners and policy makers.

---

# Example Visualization

Below is an example of the spatial distribution of pedestrian accidents in Rome.

*(Replace with an image later)*

```
outputs/figures/rome_pedestrian_accidents_map.png
```

The visualization highlights concentrations of pedestrian accidents along **major urban corridors and intersections**.

---

# Technologies Used

Python, Pandas, NumPy, Scikit-learn, GeoPandas, Astral, Matplotlib, Seaborn, Folium, SQL

---

# Project Overview

Pedestrian accidents are a major urban safety issue. Understanding **where, when, and under what conditions accidents occur** can support evidence-based urban planning and targeted safety interventions.

This project analyzes **10 years of accident data from Rome**, focusing specifically on accidents involving pedestrians.

The analysis combines:

* data cleaning and feature engineering
* geospatial processing
* contextual enrichment (weather, twilight conditions)
* unsupervised clustering to identify accident typologies and risk patterns

The final objective is to identify **high-risk accident environments and spatial clusters (“blackspots”)**.

---

# Dataset

The original dataset contains:

* **686,000 accident records**
* **37 variables**

After filtering for pedestrian accidents and performing cleaning and feature engineering, the working dataset contains approximately:

* **18,000 rows**
* **10 variables**

Each row represents **the worst-injured pedestrian involved in each accident**, including contextual information about:

* accident location
* time of day
* weather conditions
* road characteristics
* vehicle involvement
* injury severity

---

# Feature Engineering

Several variables were derived during preprocessing.

## Temporal Features

* year
* month
* day of week
* hour of accident
* twilight phase (day / civil twilight / night)

Twilight phases were computed using astronomical calculations.

## Environmental Features

* weather conditions
* road surface conditions
* visibility conditions

## Infrastructure Features

* road type

## Outcome Features

* injury severity
* fatality indicator

---

# Repository Structure

```
pedestrian-accidents-rome/

├── data
│   ├── raw
│   ├── processed
│
├── src
│   ├── data_processing
│   ├── feature_engineering
│   ├── clustering
│   ├── visualization
│
├── notebooks
│   ├── exploratory_analysis.ipynb
│
├── outputs
│   ├── figures
│   ├── tables
│
├── config
│   ├── parameters.yaml
│
├── environment.yml
├── README.md
└── LICENSE
```

---

# Analysis Pipeline

The pipeline consists of the following stages.

## 1. Data Cleaning

* removal of incomplete records
* filtering for pedestrian-related accidents
* harmonization of categorical variables

## 2. Feature Engineering

* creation of temporal features
* derivation of environmental indicators
* twilight phase calculation
* transformation of categorical variables

## 3. Data Preparation

* normalization
* dimensionality reduction (PCA)
* mixed-type distance matrices where appropriate

## 4. Clustering

Several clustering techniques were evaluated, including:

* DBSCAN
* K-Prototypes
* PAM with Gower distance
* ClusPCAmix

These methods were used to identify **groups of accidents with similar contextual characteristics**.

## 5. Spatial Analysis

Accident clusters were mapped to identify **spatial concentrations of risk**.

---

# Requirements

Python version:

```
Python 3.12
```

Key libraries include:

* pandas
* numpy
* scikit-learn
* geopandas
* matplotlib
* seaborn
* astral
* pyproj

---

# Environment Installation

```
conda env create -f environment.yml
conda activate pedestrian-accidents
```

---

# Running the Pipeline

Example workflow:

### 1. Prepare the data

```
python src/data_processing/prepare_data.py
```

### 2. Generate engineered features

```
python src/feature_engineering/build_features.py
```

### 3. Run clustering

```
python src/clustering/run_clustering.py
```

### 4. Generate visualizations

```
python src/visualization/create_maps.py
```

Outputs will be saved to:

```
outputs/
```

---

# Outputs

The pipeline generates:

* cluster assignments
* summary tables of accident typologies
* spatial visualizations
* maps of high-risk areas
* descriptive statistics of accident conditions

---

# Methodological Notes

The analysis identifies **patterns and statistical associations**, not causal relationships.

The goal is to highlight **co-occurring conditions associated with pedestrian accidents**, rather than establish causal mechanisms.

---

# Reproducibility

The repository includes:

* the full analysis pipeline
* environment configuration
* parameter configuration files

Sensitive or restricted datasets are **not included** in this repository.

---

# Future Work

Possible extensions of this work include:

* integration of **traffic flow data**
* inclusion of **street lighting infrastructure**
* modelling **temporal trends in accident risk**
* development of **predictive models for accident risk**
* integration with **urban planning datasets**

---

# Disclaimer

This project identifies **statistical associations and patterns**, not causal relationships.

The results should therefore be interpreted as **risk indicators rather than causal explanations**.

---

# Author

**Lucy Michaels**
Data Scientist – Applied Data Analysis & Generative AI

Master's Degree
*Analisi e Modellazione dei Dati e dei Processi*
Unitelma Sapienza – Rome, 12-2025

---

# License

This project is licensed under the **MIT License**.

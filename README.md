### Introduction

This is a full compendium of my work from my recent position as an Undergraduate Research Apprentice at the UC Berkeley Dow Lab. 

Below is a discussion/instructions about the implementation of my Streamlit PADO visualizer, since I think that's the most engaging capstone work that I did at the laboratory.

Throughout this process, I've developed my skills in both data visualization, public health demography, as well as more technical Python skills such as the usage of:
- **Geopandas**, an open-source ArcGIS Python library
- **Folio**, a data visualization and mapping tool
- **OpenStreetMap**, an OpenSource global map API that can be used to visualize geographical data
- Geographical **clustering** algorithms, such as k-nearest-neighbors and Ripley's K-function

My overarching goal during this time was to develop a method for visualizing and improving accessibility to data pertaining to the unique distribution of private auxiliary pharmacies (PADOs) throughout Mexico. PADOs have grown in prevalence through the years, as they can offer rudimentary primary care services, as well as prescription medication. However, some concerns exist surrounding health accessibility to Mexican residents in underserved or marginalized areas.

I've included several CSVs and XLSX files for context on my work, and to facilitate reproducibility. 

# Healthcare Facilities Visualizer

An Interactive geospatial analysis and visualization tool for PADO distribution in Morelos, Mexico. I hope to expand this soon to other Mexican states, but data validation/reliability is currently a concern. 

## Features
Includes a web dashboard with front-end functionality for:
- **Heatmap Radius**: Adjust heat spread (5-30)
- **Heatmap Blur**: Control blur intensity (10-50)
- **Marker Size**: Facility marker size (1-10)
- **Layer Toggles**: Show/hide heatmap and markers

Also includes data-export features for matched/analyzed data. 

Designed for usage by peers at the Dow Laboratory, UC Berkeley

## Installation

```bash
# Clone repository
git clone 
cd healthcare-visualizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Dataset Requirements

Quick Note: Due to the large size of cartographic datasets, the data is not included in this repository. However, you can pull this data from the INEGI (Governmental Mexican Cartography agency), and then format it in the following manner:

1. **Healthcare Facilities Data** (`healthcare_facilities.xlsx`)
   - Required columns: `latitude`, `longitude`
   - Contains facility location coordinates

2. **Detailed Location Data** (`Morelos_completo_zip_codes.xlsx`)
   - Required columns: `result_lat`, `result_lng`, `display_name`, `short_formatted_address`, `primary_type`
   - Contains detailed address and type information

Afterwards, place both files in a `data/` directory in the project root (as shown below):

```
healthcare-visualizer/
├── app.py
├── requirements.txt
├── data/
│   ├── healthcare_facilities.xlsx
│   └── Morelos_completo_zip_codes.xlsx
```

### Data Analysis

```bash
jupyter notebook analysis.ipynb
```

## Data Processing and Analysis Pipeline

1. **Load PADO Data**: Read Excel files with facility and location data
2. **Match**: Find nearest detailed location for each facility using Euclidean distance
3. **Cluster**: Apply KMeans and DBSCAN algorithms
4. **Visualize**: Generate interactive Folium map with heatmap overlay

### Clustering Parameters

```python
# KMeans
n_clusters = 12
kmeans = KMeans(n_clusters=n_clusters, random_state=42)

# DBSCAN
eps = 0.01  # Maximum distance between points
min_samples = 3  # Minimum cluster size
```

These can be edited/changed to your liking in the `visualizer-app.py` file. 

### Execution

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

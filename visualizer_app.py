import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Healthcare Facilities Visualizer", layout="wide")

st.title("PADO Facilities Map")
st.markdown("Interactive visualization of PADOs")

@st.cache_data
def load_and_process_data(facilities_file, details_file):
    df = pd.read_excel(facilities_file)
    df = df.dropna(subset=['Latitude', 'Longitude'])
    
    details_df = pd.read_excel(details_file, header=0)
    details_df = details_df[(details_df['result_lat'] != 'result_lat') & 
                           (details_df['result_lng'] != 'result_lng')]
    details_lat = details_df['result_lat'].astype(float)
    details_lng = details_df['result_lng'].astype(float)
    
    def find_nearest_match(lat, lon):
        distances = np.sqrt(
            (details_lat - float(lat))**2 + 
            (details_lng - float(lon))**2
        )
        return details_df.loc[distances.idxmin()]
    
    matched_data = []
    for idx, row in df.iterrows():
        match = find_nearest_match(row['Latitude'], row['Longitude'])
        matched_data.append({
            'Latitude': row['Latitude'],
            'Longitude': row['Longitude'],
            'Display Name': match['display_name'],
            'Address': match['short_formatted_address'],
            'Facility Type': match.get('primary_type', 'Unknown')
        })
    
    return df, pd.DataFrame(matched_data)

with st.sidebar:
    st.header("Configuration")
    
    facilities_file = st.file_uploader("Upload Facilities Data", type=['xlsx', 'csv'])
    details_file = st.file_uploader("Upload Details Data", type=['xlsx', 'csv'])
    
    st.divider()
    
    heat_radius = st.slider("Heatmap Radius", 5, 30, 15)
    heat_blur = st.slider("Heatmap Blur", 10, 50, 30)
    marker_size = st.slider("Marker Size", 1, 10, 3)
    
    show_heatmap = st.checkbox("Show Heatmap", value=True)
    show_markers = st.checkbox("Show Markers", value=True)

if facilities_file and details_file:
    df, matched_df = load_and_process_data(facilities_file, details_file)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Facilities", len(df))
    with col2:
        st.metric("Unique Types", matched_df['Facility Type'].nunique())
    with col3:
        st.metric("Avg Lat", f"{df['Latitude'].mean():.4f}")
    
    m = folium.Map(
        location=[df['Latitude'].mean(), df['Longitude'].mean()],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    if show_heatmap:
        heat_data = [[row['Latitude'], row['Longitude']] for idx, row in df.iterrows()]
        HeatMap(
            heat_data,
            radius=heat_radius,
            blur=heat_blur,
            max_zoom=15,
            gradient={0.2: 'blue', 0.4: 'purple', 0.6: 'magenta', 1.0: 'red'}
        ).add_to(m)
    
    if show_markers:
        for idx, row in matched_df.iterrows():
            popup_html = f"""
            <div style="font-family: Arial; width: 200px;">
                <h4>{row['Display Name']}</h4>
                <b>Type:</b> {row['Facility Type']}<br>
                <b>Address:</b> {row['Address']}<br>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=marker_size,
                color='white',
                fill=True,
                fillColor='orange',
                fillOpacity=0.8,
                weight=2,
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=row['Display Name']
            ).add_to(m)
    
    st_folium(m, width=1200, height=600)
    
    with st.expander("📊 View Data Table"):
        st.dataframe(matched_df, use_container_width=True)
    
    st.download_button(
        "💾 Download Matched Data",
        matched_df.to_csv(index=False),
        "matched_facilities.csv",
        "text/csv"
    )
else:
    st.info("Upload both data files")
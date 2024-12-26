### Page 2

import streamlit as st
from streamlit_folium import folium_static
from scripts.map_helpers import create_aqi_heatmap, classical_map, geojson_data
from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data
from scripts.data_handler import STATION_COORDINATES


def new_home():
    lang = st.session_state.language

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    col1, col2 = st.columns([5, 3])  # Adjust the width ratio as needed
    # First column is for the map
    with col1:
        st.title(get_text('aqi_heatmap', lang))
    with col2:
        # Custom CSS for bordered container
        option = st.selectbox(
            "Can you select the zone?",
            list(set(feature["properties"]["station"] for feature in geojson_data["features"])),
            label_visibility=st.session_state.visibility,
            index=None,
            placeholder="For example: Benito Juarez",
            disabled=st.session_state.disabled,
        )

    col1, col2 = st.columns([5, 3])  # Adjust the width ratio as needed
    # First column is for the map
    with col1:
        # Update map based on selected zone
        selected_zone = option
        if selected_zone == None:
            m = classical_map(data=geojson_data)
            folium_static(m, width=800, height=900)
        else:
            filtered_geojson_data = {
                "type": "FeatureCollection",
                "features": [
                    feature for feature in geojson_data["features"]
                    if feature["properties"]["station"] == selected_zone
                ]
            }
            m = classical_map(data=filtered_geojson_data)
            folium_static(m, width=800, height=700)
    
    with col2:
        

        st.markdown("""
                    <div line-height: 0.8;">
                    <h5>Quality awareness - Health recommendatios</h5>
                    </div>
                    """, 
                    unsafe_allow_html=True)
        st.markdown("""
            <style>
            .bordered-box {
            border: 1px solid #ffffff;
            border-radius: 5px;
            padding: 10px;
            margin-top: 0px;
            background-color: #000000;
            }
            .bordered-box h4 {
            margin-top: 0;
            }
            </style>
            """, unsafe_allow_html=True)

        # Content inside the bordered box
        st.markdown(
            """
            <div class="bordered-box" style="font-size: 18px; line-height: 1.2;">
            <strong>AQI Today:</strong> 139  
            <span class="green"> Good </span>
            <br><br>
            <strong>Población Sensible:</strong> El riesgo en salud es mínimo o nulo. Enjoy outdoor activities
            <br><br>
            Población en General: El riesgo en salud es mínimo o nulo. Enjoy outdoor activities
            <br><br><br><br>
            <strong>AQI Forecast 24h:</strong> 140
            <span class="yellow"> Moderate </span> 
            (<a href="#">Link fore more details</a>)
            <br><br>
            <strong>Población Sensible:</strong> Personas que son sensibles al ozono (O3) o material particulado (PM10 y PM2.5). Reduce las actividades físicas vigorosas al aire libre
            <br><br>
            Población en General: El riesgo en salud es mínimo. Enjoy outdoor activities
            
            (<a href="#">click to more details</a>)
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Custom CSS for the table
        #### Need to include the weighted average of the 12h and the average of 24h
        st.markdown(
            """
            <style>
            .pollutant-table {
            width: 100%;
            border-collapse: collapse;
            background-color: black;
            color: white;
            font-size: 10px; /* Reduced base font size */
            }
            .pollutant-table th, .pollutant-table td {
            border: 1px solid white;
            padding: 5px; /* Reduced padding */
            text-align: center;
            }
            .pollutant-table th {
            font-weight: bold;
            background-color: #222;
            }
            .pollutant-table td span {
            font-size: 14px; /* Reduced size for numbers */
            font-weight: bold;
            }
            .green { color: #00FF00; }
            .yellow { color: #FFD700; }
            .red { color: #FF4500; }
            .purple { color: #A020F0; }
            .orange { color: #FFA500; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(""" 
                    <h5>Table of pollutants </h5> 
                    """, 
                    unsafe_allow_html=True)
        # Table Content
        st.markdown(
            """
            <table class="pollutant-table" style="font-family: Arial, sans-serif; font-size: 12px;">
            <tr>
                <th colspan="1">Particulate Matter (µg/m³)</th>
                <th colspan="1">Actual levels</th>
                <th colspan="1">Weighted Average last 12h</th>
                <th colspan="1">Average last 24h</th>
            </tr>
            <tr>
                <td>PM10</td>
                <td><span class="green">10</span> µg/m³</td>
                <td> 12 µg/m³</td>
                <td> 9 µg/m³</td>
            </tr>
            <tr>
                <td>PM2.5</td>
                <td><span class="yellow">22</span> µg/m³</td>
                <td> 25 µg/m³</td>
                <td> 19 µg/m³</td>
            </tr>
            <tr>
                <th colspan="4">Other Pollutants</th>
            </tr>
            <tr>
                <td>Ozone (O₃)</td>
                <td><span class="red">0.142</span> ppm</td>
                <td>0.152 ppm</td>
                <td>0.124 ppm</td>
            </tr>
            <tr>
                <td>Nitrogen dioxide (NO₂)</td>
                <td><span class="purple">0.222</span> ppm</td>
                <td>0.253 ppm</td>
                <td>0.214 ppm</td>
            </tr>
            <tr>
                <td>Sulfur dioxide (SO₂)</td>
                <td><span class="orange">0.092</span> ppm</td>
                <td>0.098 ppm</td>
                <td>0.087 ppm</td>
            </tr>
            <tr>
                <td>Carbon monoxide (CO)</td>
                <td><span class="red">13.01</span> ppm</td>
                <td>14.20 ppm</td>
                <td>12.01 ppm</td>
            </tr>
            </table>
            """,
            unsafe_allow_html=True,
        )
        ##### Need to add as well the AQI from each station, with the string of good, ok, bad...


### ====================================================================================================
# Sai's code    

def show():
    lang = st.session_state.language

    st.title(get_text('aqi_heatmap', lang))

    # Always get data for all stations for the map
    all_stations_data = get_current_hour_data('All Stations')

    # Create and display map with all stations data
    m = create_aqi_heatmap(all_stations_data)
    folium_static(m, width=1000, height=600)

    # Add refresh button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(get_text('refresh_map', lang)):
            # Get new data for all stations and update session state
            st.session_state.current_data = get_current_hour_data('All Stations')
            st.rerun()
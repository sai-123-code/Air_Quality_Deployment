# import folium
# from folium.plugins import HeatMap
# import pandas as pd
# import streamlit as st
# from scripts.language_utils import get_text
# from scripts.data_handler import STATION_COORDINATES
#
#
# def get_aqi_color(aqi):
#     """Return color based on AQI value"""
#     if aqi <= 50:
#         return 'green'
#     elif aqi <= 100:
#         return 'yellow'
#     elif aqi <= 150:
#         return 'orange'
#     elif aqi <= 200:
#         return 'red'
#     elif aqi <= 300:
#         return 'purple'
#     else:
#         return 'darkred'
#
#
# def create_aqi_heatmap(current_data):
#     """
#     Creates a dynamic AQI heatmap for Mexican AQI stations using the current data
#     """
#     if not current_data:
#         return folium.Map(location=[23.6345, -102.5528], zoom_start=5)
#
#     # Convert to list if single station data
#     if not isinstance(current_data, list):
#         current_data = [current_data]
#
#     # Create DataFrame with all stations data
#     df_data = []
#     for station_data in current_data:
#         station_name = station_data['AQI_STATION'].strip()  # Normalize station name
#         coords = STATION_COORDINATES.get(station_name)
#
#         if coords is None:
#             print(f"Warning: No coordinates found for station: {station_name}")
#             continue  # Skip this station if coordinates are not found
#
#         df_data.append({
#             'Station': station_name,
#             'Lat': coords['lat'],
#             'Lon': coords['lon'],
#             'AQI': station_data['AQI']
#         })
#
#     df = pd.DataFrame(df_data)
#
#     # Initialize map centered on the average location of stations
#     m = folium.Map(
#         location=[19.4326, -99.1332],  # Default center of Mexico
#         zoom_start=8,  # Initial zoom level
#         min_zoom=2,
#         max_zoom=10,
#         width='100%',
#         height='100%'  # Make the map fill the entire page
#     )
#
#     # Prepare heatmap data
#     heatmap_data = [[row['Lat'], row['Lon'], row['AQI']] for _, row in df.iterrows()]
#
#     # Add heatmap layer
#     HeatMap(
#         heatmap_data,
#         min_opacity=0.5,
#         max_val=200,
#         radius=50,
#         blur=35,
#         gradient={
#             0.0: 'green',
#             0.4: 'yellow',
#             0.6: 'orange',
#             0.8: 'red',
#             1.0: 'purple'
#         }
#     ).add_to(m)
#
#     # Add markers for each station
#     for _, row in df.iterrows():
#         station_data = next(d for d in current_data if d['AQI_STATION'] == row['Station'])
#         # Create popup content
#         lang = st.session_state.language
#         popup_content = f"""
#         <div style='font-family: Arial; font-size: 14px;'>
#             <b>{get_text(row['Station'], lang)}</b><br>
#             AQI: {row['AQI']}<br>
#             PM2.5: {station_data['PM_2.5']:.1f} µg/m³<br>
#             PM10: {station_data['PM_10']:.1f} µg/m³<br>
#             NO2: {station_data['NO2']:.1f} µg/m³<br>
#             SO2: {station_data['SO2']:.1f} µg/m³<br>
#             CO: {station_data['CO']:.1f} µg/m³<br>
#             O3: {station_data['O3']:.1f} µg/m³<br>
#             Traffic: {station_data['TRAFFIC_CONGESTION_INDEX']:.2f}
#         </div>
#         """
#
#         # Add marker with color based on AQI
#         folium.CircleMarker(
#             location=[row['Lat'], row['Lon']],
#             radius=8,
#             popup=folium.Popup(popup_content, max_width=250),
#             color=get_aqi_color(row['AQI']),
#             fill=True,
#             fill_color=get_aqi_color(row['AQI']),
#             fill_opacity=0.7,
#             weight=2
#         ).add_to(m)
#
#         # Add station label
#         folium.map.Marker(
#             [row['Lat'], row['Lon']],
#             icon=folium.DivIcon(
#                 html=f'<div style="font-size: 10pt; color: black;">{get_text(row["Station"], lang)}</div>'
#             )
#         ).add_to(m)
#
#     # Fit the map to the bounds of the markers
#     if not df.empty:
#         bounds = [[row['Lat'], row['Lon']] for _, row in df.iterrows()]
#         m.fit_bounds(bounds)
#
#     # Add legend
#     legend_html = """
#     <div style="position: fixed;
#                 bottom: 50px; right: 50px;
#                 border:2px solid grey; z-index:9999; font-size:14px;
#                 background-color: white;
#                 padding: 10px;
#                 opacity: 0.8;">
#         <p><strong>AQI Legend</strong></p>
#         <p><span style='color: green;'>■</span> 0-50: Good</p>
#         <p><span style='color: yellow;'>■</span> 51-100: Moderate</p>
#         <p><span style='color: orange;'>■</span> 101-150: Unhealthy for Sensitive Groups</p>
#         <p><span style='color: red;'>■</span> 151-200: Unhealthy</p>
#         <p><span style='color: purple;'>■</span> 201-300: Very Unhealthy</p>
#         <p><span style='color: darkred;'>■</span> 300+: Hazardous</p>
#     </div>
#     """
#     m.get_root().html.add_child(folium.Element(legend_html))
#
#     return m
#
import os
import folium
from pathlib import Path
from folium.plugins import HeatMap
import pandas as pd
import streamlit as st
from scripts.language_utils import get_text
from streamlit_plotly_mapbox_events import plotly_mapbox_events
import plotly.express as px
from scripts.data_handler import STATION_COORDINATES

# New ones
import json
from shapely.geometry import shape
from shapely.wkb import loads
from shapely.wkt import dumps
import branca

# Comment out when actual data is there
BASE_DIR = Path(__file__).resolve().parent.parent
dashboard_data_path = BASE_DIR / 'Dashboard_data' / 'limite-de-las-alcaldas.json'

with open(dashboard_data_path) as f:
	geo_json_data = json.load(f)

# Parse the GeoJSON to extract features
features = geo_json_data["features"]

# Extract the 'geometry' and 'name' into a list of dictionaries
data = [
    {"geometry": shape(feature["geometry"]), "NOMGEO": feature["properties"]["NOMGEO"]}
    for feature in features
]

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Dictionary with municipality names and random AQI values
municipalities_aqi = {
    "Azcapotzalco": {"station": "Ajusco Medio", "aqi": 50},
    "Coyoacán": {"station": "Ajusco", "aqi": 95},
    "Cuajimalpa de Morelos": {"station": "Merced", "aqi": 45},
    "Gustavo A. Madero": {"station": "Hospital General de México", "aqi": 25},
    "Iztacalco": {"station": "Xalostoc", "aqi": 43},
    "Iztapalapa": {"station": "Santa Fe", "aqi": 29},
    "La Magdalena Contreras": {"station": "Tlalnepantla", "aqi": 3},
    "Milpa Alta": {"station": "Merced", "aqi": 30},
    "Álvaro Obregón": {"station": "Miguel Hidalgo", "aqi": 20},
    "Tláhuac": {"station": "UAM Iztapalapa", "aqi": 80},
    "Tlalpan": {"station": "Ajusco", "aqi": 70},
    "Xochimilco": {"station": "Xalostoc", "aqi": 100},
    "Benito Juárez": {"station": "San Agustin", "aqi": 23},
    "Cuauhtémoc": {"station": "Milpa Alta", "aqi": 38},
    "Miguel Hidalgo": {"station": "Benito Juarez", "aqi": 21},
   "Venustiano Carranza": {"station": "Milpa Alta", "aqi": 10},
}

# Now let's merge with the municipalities dictionary. We need to bring 2 columns station and aqi
df["station"] = df["NOMGEO"].map(lambda x: municipalities_aqi[x]["station"])
df["aqi"] = df["NOMGEO"].map(lambda x: municipalities_aqi[x]["aqi"])

def wkt_to_geojson(df):
    features = []
    
    for _, row in df.iterrows():
        # Get geometry and convert to WKT string if needed
        geom = row['geometry']
        if hasattr(geom, 'wkt'):
            wkt = geom.wkt
        else:
            wkt = str(geom)
            
        # Clean WKT string
        wkt = wkt.replace("POLYGON ((", "").replace("MULTIPOLYGON (((", "").replace(")))", "").replace("))", "")
        
        # Split into coordinate pairs
        rings = wkt.split("), (")
        coordinates = []
        
        for ring in rings:
            # Split coordinates and convert to float pairs
            coords = ring.split(",")
            ring_coords = []
            
            for coord in coords:
                x, y = map(float, coord.strip().split())
                ring_coords.append([x, y])
            
            # Close the ring by adding first coordinate at the end if needed
            if ring_coords[0] != ring_coords[-1]:
                ring_coords.append(ring_coords[0])
                
            coordinates.append(ring_coords)
        
        # Create GeoJSON feature
        feature = {
            "type": "Feature",
            "properties": {
                "NOMGEO": row['NOMGEO'],
                "station": row['station'],
                "aqi": row['aqi']
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates
            }
        }
        
        features.append(feature)
    
    # Create final GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Save to file
    with open('cdmx_zones.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    return geojson

# Usage:
geojson_data = wkt_to_geojson(df)

colormap = branca.colormap.LinearColormap(
    vmin=df["aqi"].quantile(0.0),
    vmax=df["aqi"].quantile(1),
    #colors=["red", "orange", "lightblue", "green", "darkgreen"],
    colors=["darkgreen", "green", "lightblue", "orange", "red"],
    caption="Air Quality Index of Mexico City",
)


def classical_map(data):
    """
    Create a classical map with markers for Mexican AQI stations.
    """
    m = folium.Map([19.4326, -99.1332], tiles="cartodbpositron", zoom_start=10,
            min_zoom=2,
            max_zoom=20)

    popup = folium.GeoJsonPopup(
        fields=["NOMGEO", "aqi"],
        aliases=["Municipality", "AQI"],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = folium.GeoJsonTooltip(
        fields=["NOMGEO", "station", "aqi"],
        aliases=["Municipality:", "Station:", "AQI:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    g = folium.GeoJson(
    data,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["aqi"])
        if x["properties"]["aqi"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    },
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    colormap.add_to(m)

    return m

# ====================================================================================================
### Sai's code

def get_aqi_color(aqi):
    """Return color based on AQI value for marker icons."""
    if aqi <= 50:
        return 'green'
    elif aqi <= 100:
        return 'blue'
    elif aqi <= 150:
        return 'orange'
    elif aqi <= 200:
        return 'red'
    elif aqi <= 300:
        return 'purple'
    else:
        return 'darkred'

def create_aqi_heatmap(current_data):
    """
    Creates a dynamic AQI heatmap with custom markers for Mexican AQI stations.
    """
    try:
        # Print current_data structure
        print("Current data:", current_data)

        # Create base map even if no data
        m = folium.Map(
            location=[19.4326, -99.1332],
            zoom_start=10,
            min_zoom=2,
            max_zoom=20
        )

        if not current_data:
            return m

        # Convert to list if single station data
        if not isinstance(current_data, list):
            current_data = [current_data]

        # Debug print for station data
        # for station_data in current_data:
        #     print("Station data:", station_data)
        #     print("Station name type:", type(station_data['AQI_STATION']))
        #     print("AQI type:", type(station_data['AQI']))

        # Create DataFrame with all stations data
        df_data = []
        for station_data in current_data:
            station_name = station_data['AQI_STATION'].strip()
            coords = STATION_COORDINATES.get(station_name)
            
            if coords:
                # Print coordinate types
                print(f"Coordinates for {station_name}:", coords)
                print("Lat type:", type(coords['lat']))
                print("Lon type:", type(coords['lon']))
                
                df_data.append({
                    'Station': station_name,
                    'Lat': coords['lat'],
                    'Lon': coords['lon'],
                    'AQI': station_data['AQI']
                })

        if not df_data:
            return m

        df = pd.DataFrame(df_data)
        print("DataFrame types:", df.dtypes)

        # Add heatmap layer
        heatmap_data = [[row['Lat'], row['Lon'], row['AQI']] for _, row in df.iterrows()]
        HeatMap(
            data=heatmap_data,  # Use explicit parameter name
            min_opacity=0.5,
            max_val=200,
            radius=50,
            blur=35,
            gradient={
                '0': 'green',    # Change float keys to strings
                '0.4': 'yellow',
                '0.6': 'orange',
                '0.8': 'red',
                '1': 'purple'
            }
        ).add_to(m)

            # Add custom markers for each station
        for _, row in df.iterrows():
            lang = st.session_state.language
            popup_content = f"""
            <div style='font-family: Arial; font-size: 14px;'>
                <b>{get_text(row['Station'], lang)}</b><br>
                AQI: {row['AQI']}
            </div>
            """

            # Add marker with custom icon based on AQI value
            icon_color = get_aqi_color(row['AQI'])
            folium.Marker(
                location=[row['Lat'], row['Lon']],
                popup=folium.Popup(popup_content, max_width=250),
                icon=folium.Icon(color=icon_color, icon="info-sign")
            ).add_to(m)

        # Add legend
        legend_html = """
        <div style="position: fixed;
                    bottom: 50px; right: 50px;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color: white;
                    padding: 10px;
                    opacity: 0.8;">
            <p><strong>AQI Legend</strong></p>
            <p><span style='color: green;'>■</span> 0-50: Good</p>
            <p><span style='color: blue;'>■</span> 51-100: Moderate</p>
            <p><span style='color: orange;'>■</span> 101-150: Unhealthy for Sensitive Groups</p>
            <p><span style='color: red;'>■</span> 151-200: Unhealthy</p>
            <p><span style='color: purple;'>■</span> 201-300: Very Unhealthy</p>
            <p><span style='color: darkred;'>■</span> 300+: Hazardous</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        return m
        
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return folium.Map(location=[19.4326, -99.1332], zoom_start=10)
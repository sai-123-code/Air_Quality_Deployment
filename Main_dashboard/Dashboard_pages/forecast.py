# Update this to follow page_1 / page_2 conventions
'''
  This is the forecast component of the application.
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data, get_all_stations, get_pollutants, get_pollutant_measuremnents
from scripts.data_handler import STATION_COORDINATES

BASE_DIR = Path(__file__).resolve().parent.parent
merged_data_csv = BASE_DIR / 'Dashboard_data' / 'mer_imputed_merged_data.csv'
data = pd.read_csv(merged_data_csv)

def create_forecast_header(date, temp, condition, lang):
  """Create a single forecast header"""
  return f"""
  <div class='forecast-tempaqi-container' style='background: {get_condition_color(condition)};'>
      <h3 style='margin: 0; padding: 0'>{date.strftime('%a %d')}</h3>
      <div style='display: flex; flex-direction: column; align-items: flex-start; margin-top: 10px'>
        <h2 style='margin: 0; padding: 0'>{temp}°C</h2>
        <sup>Expected</sup>
      </div>
  </div>
  """

def create_aqi_header(date, aqi_level, condition, lang):
  """Create a single expected AQI"""
  condition_lang = get_text(condition, lang)

  return f"""
    <div class='forecast-tempaqi-container' style='background: {get_aqi_condition_color(condition)};'>
      <div style='display: flex; justify-content: between'>
        <h4 style='margin: 0; padding: 0'>Air Quality Index</h4>
      </div>
      <div style='display: flex; justify-content: flex-start; align-items: flex-end; margin-top: 10px'>
        <span>
          <h2 style='margin: 0; padding: 0'>{aqi_level}</h2>
          <span>{condition_lang.capitalize()}</span>
        </span>
      </div>
    </div>
  """

def get_24hr_forecast(data, metric='temperature', lang='en'):

  # Configurations
  fig, ax = plt.subplots(figsize=(12,4))
  fig.patch.set_facecolor('#1F2937')
  ax.set_facecolor('#1F2937')
  ax.set_xticks([0, 4, 8, 12, 16, 20, 23])
  ax.tick_params('both', colors='white')
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['bottom'].set_color('white')
  ax.spines['left'].set_color('white')
  
  # Line plot version
  ax.plot(data['hour'], data[metric], color='#EFEAD0', linewidth=2, marker='o', markersize=6)
  ax.set_title(f'24-Hour Forecast - {get_text(metric, lang)}', color='white', fontsize=16, pad=15, loc='left', fontweight='bold')
  plt.subplots_adjust(top=0.85)
  # plt.tight_layout(rect=[0, 0, 1, 0.95])

  # Update labels
  ax.set_xlabel(get_text('time_of_day', lang))
  ax.xaxis.label.set_color('white')
  ax.set_ylabel(get_pollutant_measuremnents(metric)) # use function to retrieve appropriate metric
  ax.yaxis.label.set_color('white')

  return fig

def get_condition_color(condition):
  """Return background color based on condition"""
  color_map = {
      'good': '#90EE90',
      'moderate': '#FFA500',
      'poor': '#FF4500',
      'very_poor': '#FF0000'
  }
  return color_map.get(condition, '#FFFFFF')

def get_aqi_condition_color(condition):
  color_map = {
        'good': '#7CB342',        # Muted green - easier on eyes, good contrast
        'moderate': '#FDD835',    # Softer yellow - better readability
        'unhealthy_sensitive': '#FB8C00',  # Muted orange - distinct from yellow/red
        'unhealthy': '#E53935',   # Softer red - less harsh but still clear warning
        'very_unhealthy': '#8E24AA',  # Muted purple - distinct from red
        'hazardous': '#B71C1C'    # Deep red - serious but not harsh
    }
  return color_map.get(condition, '#424242')  # Dark gray as default, matches theme

def home():
  """Main function to render the forecast page"""
  # Get language from session state
  lang = st.session_state.language
  
  # Set page title with language support
  st.title(get_text('current_forecast', lang))

  station_col, whitespace_1, day_forecast_col = st.columns([1,1,1])
  with station_col:
    selected_station = st.selectbox((get_text('station', lang)).capitalize(), get_all_stations())

  # Sample data - replace with actual data fetching logic
  dates = [datetime.now() + timedelta(days=i) for i in range(4)]
  temps = [16, 18, 18, 17]
  conditions = ['moderate', 'poor', 'moderate', 'moderate']
  
  # Create columns for the dashboard
  cols = st.columns(4)
  
  # Generate sample data for 4 days
  hours = np.tile(np.arange(24), 4)
  dates_rep = np.repeat([d.date() for d in dates], 24)
  
  # Create sample dataset - replace with actual data
  sample_data = pd.DataFrame({
      'date': [d for d in dates_rep],
      'date_w_timestamp': [datetime.combine(d, datetime.min.time()) for d in dates_rep],
      'hour': hours,
      'wind_speed': np.random.rand(96) * 5,
      'humidity': np.random.rand(96) * 100,
      'pressure': np.random.rand(96) * 50 + 1000,
      
      # Pollutants
      # PM2.5 (μg/m³) - typically 0-500 scale
      'pm25': np.clip(np.random.normal(50, 30, 96), 0, 500),
      # PM10 (μg/m³) - typically 0-600 scale
      'pm10': np.clip(np.random.normal(75, 40, 96), 0, 600),
      # O3 (ppb) - typically 0-500 scale
      'o3': np.clip(np.random.normal(40, 20, 96), 0, 500),
      # NO2 (ppb) - typically 0-200 scale
      'no2': np.clip(np.random.normal(30, 15, 96), 0, 200),
      # CO (ppm) - typically 0-50 scale
      'co': np.clip(np.random.normal(2, 1, 96), 0, 50),
      # SO2 (ppb) - typically 0-500 scale
      'so2': np.clip(np.random.normal(20, 10, 96), 0, 500),
  })
  
  st.write(f"### Forecast: {sample_data['date'][0].strftime('%B %d, %Y')}")
  temp_card, aqi_card = st.columns([1, 1])
  with temp_card:
    st.markdown(create_forecast_header(datetime.now(), 18, 'moderate', lang), unsafe_allow_html=True)
  with aqi_card:
    st.markdown(create_aqi_header(datetime.now(), 75, 'moderate', lang), unsafe_allow_html=True)
  
  with st.container():
    st.write(f"""
      <div class="forecast-hpw-container">
        
        <div class="forecast-hpw-column">
          <span class="hpw-header">{get_text('humidity', lang)}</span>
          <h3>{"{:.1f}%".format(sample_data['humidity'][0])}</h3>
        </div>
             
        <div class="forecast-hpw-column">
          <span class="hpw-header">{get_text('pressure', lang)}</span>
          <h3>{"{:.0f} hPa".format(sample_data['pressure'][0])}</h3>
        </div>
             
        <div class="forecast-hpw-column">
          <span class="hpw-header">{get_text('wind_speed', lang)}</span>
          <h3>{"{:.0f} km/h".format(sample_data['wind_speed'][0])}</h3>
        </div>
        
      </div>
    """, unsafe_allow_html=True)
  
  pollutant_select_col, whitespace_3, whitespace_4 = st.columns(3)
  with pollutant_select_col:
    pollutant_selection = st.selectbox(get_text('pollutants', lang), get_pollutants(sample_data), format_func=lambda x: x.upper())
  
  today = pd.Timestamp.now().date()
  day_fig = get_24hr_forecast(sample_data[sample_data['date'] == today], pollutant_selection, lang)
  with st.container():
    st.pyplot(day_fig)
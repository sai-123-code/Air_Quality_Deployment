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

from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data
from scripts.data_handler import STATION_COORDINATES

def create_daily_chart(data, date):
  """Create charts for a single day"""
  fig = plt.figure(figsize=(3.5, 10))
  gs = fig.add_gridspec(6, 1, height_ratios=[1, 0.5, 0.5, 0.5, 0.5, 0.5], hspace=0.4)

  # Filter data for this date
  daily_data = data[data['date'].dt.date == date.date()]

  # 1. PM2.5 and O3
  ax1 = fig.add_subplot(gs[0])
  ax1.bar(daily_data['hour'], daily_data['pm25'], color='#FFA07A', label='PM2.5')
  ax1_twin = ax1.twinx()
  ax1_twin.bar(daily_data['hour'], daily_data['o3'], color='#90EE90', alpha=0.5, label='O3')
  ax1.set_xticks([])

  # 2. Wind
  ax2 = fig.add_subplot(gs[1])
  wind_speeds = daily_data['wind_speed']
  wind_directions = daily_data['wind_direction']
  x = np.arange(len(wind_speeds))
  ax2.barbs(x, np.zeros_like(x), wind_speeds * np.cos(wind_directions),
            wind_speeds * np.sin(wind_directions))
  ax2.set_xticks([])

  # 3. Temperature
  ax3 = fig.add_subplot(gs[2])
  ax3.plot(daily_data['hour'], daily_data['temperature'], color='yellow', marker='o')
  ax3.fill_between(daily_data['hour'], daily_data['temperature'], alpha=0.3, color='yellow')
  ax3.set_xticks([])

  # 4. Humidity
  ax4 = fig.add_subplot(gs[3])
  ax4.plot(daily_data['hour'], daily_data['humidity'], color='blue')
  ax4.fill_between(daily_data['hour'], daily_data['humidity'], alpha=0.3, color='blue')
  ax4.set_xticks([])

  # 5. Pressure
  ax5 = fig.add_subplot(gs[4])
  ax5.plot(daily_data['hour'], daily_data['pressure'], color='orange')
  ax5.fill_between(daily_data['hour'], daily_data['pressure'], alpha=0.3, color='orange')
  ax5.set_xticks([])

  # 6. Precipitation
  ax6 = fig.add_subplot(gs[5])
  ax6.bar(daily_data['hour'], daily_data['precipitation'], color='blue', alpha=0.5)
  ax6.set_xticks(daily_data['hour'])
  ax6.set_xticklabels(daily_data['hour'], rotation=45)

  plt.tight_layout()
  return fig

def create_ultraviolet_index(data, date):
  pass

def create_forecast_header(date, temp, condition):
  """Create a single forecast header"""
  return f"""
  <div style='text-align: center; background: {get_condition_color(condition)}; 
              padding: 10px; border-radius: 5px; margin: 5px;'>
      <h3>{date.strftime('%a %d')}</h3>
      <h2>{temp}°C</h2>
  </div>
  """

def get_condition_color(condition):
  """Return background color based on condition"""
  color_map = {
      'good': '#90EE90',
      'moderate': '#FFA500',
      'poor': '#FF4500',
      'very_poor': '#FF0000'
  }
  return color_map.get(condition, '#FFFFFF')

def home():
  """Main function to render the forecast page"""
  # Get language from session state
  lang = st.session_state.language
  
  # Set page title with language support
  st.title(get_text('current_forecast', lang))
  st.write('####')
  
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
      'date': [datetime.combine(d, datetime.min.time()) for d in dates_rep],
      'hour': hours,
      'pm25': np.random.rand(96),
      'o3': np.random.rand(96),
      'wind_speed': np.random.rand(96) * 5,
      'wind_direction': np.random.rand(96) * 2 * np.pi,
      'temperature': np.random.rand(96) * 20 + 10,
      'humidity': np.random.rand(96) * 100,
      'pressure': np.random.rand(96) * 50 + 1000,
      'precipitation': np.random.rand(96)
  })
  
  # Create headers and charts for each day
  for i, (col, date, temp, condition) in enumerate(zip(cols, dates, temps, conditions)):
      with col:
          # Display header
          st.markdown(create_forecast_header(date, temp, condition), 
                      unsafe_allow_html=True)
          # Display charts
          st.pyplot(create_daily_chart(sample_data, date))
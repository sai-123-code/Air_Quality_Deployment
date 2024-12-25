import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

st.title('Air Quality Index')

def create_air_quality_dashboard(data):
  # Set the style for all plots
  plt.style.use('ggplot')
  
  # Create the main figure with subplots
  fig = plt.figure(figsize=(15, 10))
  
  # Define grid spec to control layout
  gs = fig.add_gridspec(6, 1, height_ratios=[1, 0.5, 0.5, 0.5, 0.5, 0.5])
  
  # 1. Top row with PM2.5 and O3 levels
  ax1 = fig.add_subplot(gs[0])
  # Plot PM2.5 data
  pm25_colors = ['#FFA07A', '#8B008B', '#FF69B4', '#FFA500']  # Example colors
  ax1.bar(data['hour'], data['pm25'], color=pm25_colors, label='PM2.5')
  ax1.set_ylabel('PM2.5')
  
  # Plot O3 data on the same axis
  ax1_twin = ax1.twinx()
  o3_colors = ['#90EE90', '#FFD700']  # Example colors for O3
  ax1_twin.bar(data['hour'], data['o3'], color=o3_colors, alpha=0.5, label='O3')
  ax1_twin.set_ylabel('O3')
  
  # 2. Wind speed and direction
  ax2 = fig.add_subplot(gs[1])
  wind_speeds = data['wind_speed']
  wind_directions = data['wind_direction']
  
  # Create wind barbs
  x = np.arange(len(wind_speeds))
  ax2.barbs(x, np.zeros_like(x), wind_speeds * np.cos(wind_directions),
            wind_speeds * np.sin(wind_directions))
  ax2.set_ylabel('Wind')
  
  # 3. Temperature
  ax3 = fig.add_subplot(gs[2])
  ax3.plot(data['hour'], data['temperature'], color='yellow', marker='o')
  ax3.fill_between(data['hour'], data['temperature'], alpha=0.3, color='yellow')
  ax3.set_ylabel('Temp (°C)')
  
  # 4. Relative Humidity
  ax4 = fig.add_subplot(gs[3])
  ax4.plot(data['hour'], data['humidity'], color='blue')
  ax4.fill_between(data['hour'], data['humidity'], alpha=0.3, color='blue')
  ax4.set_ylabel('RH (%)')
  
  # 5. Barometric Pressure
  ax5 = fig.add_subplot(gs[4])
  ax5.plot(data['hour'], data['pressure'], color='orange')
  ax5.fill_between(data['hour'], data['pressure'], alpha=0.3, color='orange')
  ax5.set_ylabel('Pressure (hPa)')
  
  # 6. Precipitation
  ax6 = fig.add_subplot(gs[5])
  ax6.bar(data['hour'], data['precipitation'], color='blue', alpha=0.5)
  ax6.set_ylabel('Precip (mm)')
  
  # Adjust layout
  plt.tight_layout()
  
  return fig

def create_forecast_header(dates, temps, conditions):
  """Create the forecast header with dates, temperatures, and conditions"""
  col1, col2, col3, col4 = st.columns(4)
  
  for col, date, temp, condition in zip([col1, col2, col3, col4], dates, temps, conditions):
      with col:
          st.markdown(f"""
          <div style='text-align: center; background: {get_condition_color(condition)}; 
                      padding: 10px; border-radius: 5px;'>
              <h3>{date.strftime('%a %d')}</h3>
              <h2>{temp}°C</h2>
          </div>
          """, unsafe_allow_html=True)

def get_condition_color(condition):
  """Return background color based on condition"""
  color_map = {
      'good': '#90EE90',
      'moderate': '#FFA500',
      'poor': '#FF4500',
      'very_poor': '#FF0000'
  }
  return color_map.get(condition, '#FFFFFF')

# Sample data - replace with your actual data
dates = [datetime.now() + timedelta(days=i) for i in range(4)]
temps = [16, 18, 18, 17]
conditions = ['moderate', 'poor', 'moderate', 'moderate']

# Create forecast header
create_forecast_header(dates, temps, conditions)

# Create main visualization
# Replace this with your actual data
sample_data = pd.DataFrame({
    'hour': range(24),
    'pm25': np.random.rand(24),
    'o3': np.random.rand(24),
    'wind_speed': np.random.rand(24) * 5,
    'wind_direction': np.random.rand(24) * 2 * np.pi,
    'temperature': np.random.rand(24) * 20 + 10,
    'humidity': np.random.rand(24) * 100,
    'pressure': np.random.rand(24) * 50 + 1000,
    'precipitation': np.random.rand(24)
})

fig = create_air_quality_dashboard(sample_data)
st.pyplot(fig)

# Example usage in Streamlit
# def main():
#     st.title('Air Quality Forecast')
    
#     # Sample data - replace with your actual data
#     dates = [datetime.now() + timedelta(days=i) for i in range(4)]
#     temps = [16, 18, 18, 17]
#     conditions = ['moderate', 'poor', 'moderate', 'moderate']
    
#     # Create forecast header
#     create_forecast_header(dates, temps, conditions)
    
#     # Create main visualization
#     # Replace this with your actual data
#     sample_data = pd.DataFrame({
#         'hour': range(24),
#         'pm25': np.random.rand(24),
#         'o3': np.random.rand(24),
#         'wind_speed': np.random.rand(24) * 5,
#         'wind_direction': np.random.rand(24) * 2 * np.pi,
#         'temperature': np.random.rand(24) * 20 + 10,
#         'humidity': np.random.rand(24) * 100,
#         'pressure': np.random.rand(24) * 50 + 1000,
#         'precipitation': np.random.rand(24)
#     })
    
#     fig = create_air_quality_dashboard(sample_data)
#     st.pyplot(fig)
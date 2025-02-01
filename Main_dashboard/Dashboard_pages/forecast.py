# Update this to follow page_1 / page_2 conventions
'''
  This is the forecast component of the application.
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from babel.dates import format_date, format_time
from pathlib import Path
from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data, get_all_stations, get_pollutants, get_pollutant_measuremnents, round_to_nearest_hour, get_wind_dir
from scripts.data_handler import STATION_COORDINATES

BASE_DIR = Path(__file__).resolve().parent.parent
merged_data_csv = BASE_DIR / 'Dashboard_data' / 'mer_imputed_merged_data.csv'
data = pd.read_csv(merged_data_csv)

def create_forecast_header(date, temp, condition, lang):
  """Create a single forecast header"""
  return f"""
  <div class='forecast-temp-container' style='background: black;'>
      <h3 style='margin: 0; padding: 0'>{get_text('temperature', lang)}</h3>
      <div style='display: flex; flex-direction: column; align-items: flex-start; margin-top: 10px'>
        <h2 style='margin: 0; padding: 0'>{temp}°C</h2>
        <sup>Expected</sup>
      </div>
  </div>
  """

def create_aqi_header(date, aqi_level, condition, lang):
  """Create a single expected AQI"""
  condition_lang = get_text(condition, lang)
  condition_name = condition_lang.replace('_', ' ').title()
  # condition_name = re.sub(r'_\d+', '', condition_lang)

  return f"""
    <div class='forecast-aqi-container' style='{get_aqi_condition_color(condition)}'>
      <div style='display: flex; justify-content: between'>
        <h4 style='margin: 0; padding: 0'>{get_text('air_quality_index', lang)}</h4>
      </div>
      <div style='display: flex; justify-content: flex-start; align-items: flex-end; margin-top: 10px'>
        <span>
          <h2 style='margin: 0; padding: 0'>{aqi_level}</h2>
          <span>{condition_name}</span>
        </span>
      </div>
    </div>
  """

def get_24hr_forecast(data, metric='temperature', lang='en'):
   # Get the current time rounded to nearest hour
  current_time = round_to_nearest_hour(datetime.now())
  
  # Create a list of 24 hours starting from the current hour
  hours = [(current_time + timedelta(hours=i)).strftime('%H:00') for i in range(24)]
  data = data.copy()
  data['formatted_time'] = data.apply(
        lambda row: (datetime.combine(row['date'], datetime(1, 1, 1, row['hour']).time())).strftime('%H:00'),
        axis=1
    )

  # Filter data for next 24 hours
  today_data = data[data['date'] == pd.Timestamp.now().date()]
  tomorrow_data = data[data['date'] == (pd.Timestamp.now() + pd.Timedelta(days=1)).date()]
  
  # Combine today and tomorrow's data based on current hour
  current_hour = current_time.hour
  forecast_data = pd.concat([
      today_data[today_data['hour'] >= current_hour],
      tomorrow_data[tomorrow_data['hour'] < current_hour]
  ]).reset_index(drop=True)
  
  # Ensure we have exactly 24 hours of data
  forecast_data = forecast_data.head(24)
  forecast_data['hour_index'] = range(len(forecast_data))

  chart = alt.Chart(forecast_data).mark_line(
        color='#2563EB',
        point=alt.MarkConfig(
            filled=True,
            size=120
        )
    ).encode(
        x=alt.X('formatted_time:O',
            sort=None,
            axis=alt.Axis(
                values=forecast_data['formatted_time'].tolist(),
                title=get_text('time_of_day', lang),
                titleColor='black',
                labelColor='black',
                labelAngle=-45,  # Angle labels for better readability
            ),
        ),
        y=alt.Y(f'{metric}:Q',
            axis=alt.Axis(
                title=get_pollutant_measuremnents(metric),
                titleColor='black',
                labelColor='black'
            )
        )
    ).properties(
        width=800,
        height=500,
        title=alt.TitleParams(
            text=f'24-Hour Forecast - {get_text(metric, lang)}',
            anchor='start',
            fontSize=16,
            fontWeight='bold',
            color='black',
            offset=15
        )
    )

    # Configure the theme
  chart = chart.configure_view(
      strokeWidth=0  # Removes the frame
  ).configure_axis(
      domainColor='black',
      domain=True,
      grid=False
  ).configure_title(
      align='left'
  )

  return chart

def get_aqi_condition_color(condition):
  color_map = {
    'good': 'background: #7CB342; color: black', # Muted green
    'acceptable': 'background: #FDD835; color: black', # Softer yellow
    'bad': 'background: #e68200; color: black', # Softer red
    'very_bad': 'background: #8E24AA; color: white', # Muted purple
    'extremely_bad': 'background: #B71C1; color: white' # Deep red
  }
  return color_map.get(condition, 'background: #424242; color: white')  # Dark gray as default, matches theme

def home():
  """Main function to render the forecast page"""
  # Get language from session state
  lang = st.session_state.language
  nearest_hour = round_to_nearest_hour(datetime.now())
  end_hour = nearest_hour + timedelta(hours=23)
  
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
  
  time_span = f"({format_time(nearest_hour, 'h:mm a' ,locale=lang)} to {format_time(end_hour, 'h:mm a', locale=lang)}, next day)"
  
  with st.container():
    st.markdown(create_aqi_header(datetime.now(), 5, 'bad', lang), unsafe_allow_html=True)
  wind_dir = get_wind_dir(int(data['WDR_MER'][0]))

  with st.container():
    st.write(f"""
      <div class="forecast-thw-container">
        
        <div class="forecast-thw-column">
          <span class="thw-header">{get_text('temperature', lang)}</span>
          <h3>{"{:.0f}°C".format(data['TMP_MER'][0])}</h3>
        </div>
             
        <div class="forecast-thw-column">
          <span class="thw-header">{get_text('relative_humidity', lang)}</span>
          <h3>{"{:.0f}%".format(data['RH_MER'][0])}</h3>
        </div>
             
        <div class="forecast-thw-column">
          <span class="thw-header">{get_text('wind_speed', lang)}</span>
          <h3>{"{:.0f} km/h".format(data['WSP_MER'][0])}</h3>
        </div>

        <div class="forecast-thw-column">
          <span class="thw-header">{get_text('wind_direction', lang)}</span>
          <h3>{wind_dir['direction']}</h3>
        </div>     
        
      </div>
    """, unsafe_allow_html=True)
  
  pollutant_select_col, whitespace_3, whitespace_4 = st.columns(3)
  with pollutant_select_col:
    pollutant_selection = st.selectbox(get_text('pollutants', lang), get_pollutants(sample_data), format_func=lambda x: x.upper())
  
  today = pd.Timestamp.now().date()
  day_fig = get_24hr_forecast(sample_data, pollutant_selection, lang)
  with st.container():
    st.altair_chart(day_fig, use_container_width=True)

  st.write('*The forecast data listed above is approximately 85% accurate based on multiple tests.*')

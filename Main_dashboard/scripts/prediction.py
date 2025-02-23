import pandas as pd
import numpy as np
from datetime import datetime, timedelta

ADJUSTMENT_FACTORS = {
  'PM25': 0.694,
  'PM10': 0.714
}

def naive_formula(df: pd.DataFrame, column: str, station=None) -> int:
  """
    Use historical data and simple average to return a naive prediction for the model.
  """
  if station != None:
    df = df[df["station"] == station]
  else:
    return 0
  
  current_date = datetime.today().day
  data_points = df[df['datetime'].dt.day == current_date]
  naive_average = data_points[column].mean()
  return naive_average

def naive_formula_24h(df: pd.DataFrame, current_datetime: datetime, column: str, station=None) -> pd.DataFrame:
    """
    Use historical data to return naive predictions for the next 24 hours based on historical averages.
    
    Args:
        df: DataFrame with datetime column and measurements
        current_datetime: The reference datetime to start predictions from
        column: The column to make predictions for
        station: Optional station filter
        
    Returns:
        DataFrame with predictions for next 24 hours
    """
    if station is not None:
        df = df[df["station"] == station]
    
    # Initialize results
    predictions = []
    hours = []
    
    # Get predictions for each of the next 24 hours
    for hour in range(24):
        target_datetime = current_datetime + pd.Timedelta(hours=hour)
        
        # Get historical data points matching the hour and minute
        historical_points = df[
            (df['datetime'].dt.dayofyear == target_datetime.timetuple().tm_yday) &
            (df['datetime'].dt.hour == target_datetime.hour)
        ]
        
        # Calculate average for this hour
        prediction = historical_points[column].mean() * ADJUSTMENT_FACTORS.get(column, 1)
        
        predictions.append(prediction)
        hours.append(target_datetime)
        # hours.append(target_datetime.strftime('%H:00'))
    
    # Create results DataFrame
    results = pd.DataFrame({
        'datetime': hours,
        'formatted_time': list(map(lambda x: x.strftime('%H:00'), hours)),
        f'predicted_{column}': predictions
    })
    
    return results

def calculate_pollutant_weighted_average(df: pd.DataFrame, pollutant: str, adjustment_factor: int = 1, station: str = None):
  """
  Calculate weighted average concentrations for different pollutants.
  """
  if station != None:
    df = df[df["station"] == station]
  else:
      return 0
  
  # Handle non-PM/CO cases early
  if pollutant not in ['PM25', 'PM10', 'CO']:
      return round(np.mean(df[pollutant][-3:].values), 3)
  
  # Get appropriate window size and data
  window_size = 8 if pollutant == 'CO' else 12
  concentrations = df[pollutant][-window_size:].values
  
  # Handle CO separately
  if pollutant == 'CO':
      if len(concentrations) < 8 or np.isnan(concentrations).sum() > len(concentrations) * 0.25:
          return "No info"
      return round(np.mean(concentrations), 3)
  
  # Process PM data
  last_three = concentrations[-3:]
  last_three_null_count = np.isnan(last_three).sum()
  
  # Check last three values
  if last_three_null_count >= 2:
      return "No info"
  
  # Handle single null in last three values
  if last_three_null_count == 1:
      concentrations = concentrations.copy()
      concentrations[-3:] = np.nan_to_num(last_three, nan=0)
  
  # Check total null count
  total_null_count = np.isnan(concentrations).sum()
  if total_null_count > len(concentrations) * 0.25:
      return "No info"
  
  # Calculate PM average
  try:
      Cmax = np.nanmax(concentrations)
      Cmin = np.nanmin(concentrations)
      w = max(0.5, 1 - ((Cmax - Cmin) / Cmax))
      powers = np.arange(len(concentrations)-1, -1, -1)
      weights = w ** powers
      
      weighted_sum = np.sum(concentrations * weights)
      weight_sum = np.sum(weights)
  except ValueError:
      return 0

  return int((weighted_sum / weight_sum) * ADJUSTMENT_FACTORS.get(pollutant, 1))

def get_highest_aqi(df, station=None, forecast=False, output=None):
  # Ensure datetime is in proper format
  df['datetime'] = pd.to_datetime(df['datetime'])

  # Check station
  if station is None and forecast==False:
      # Get the last row for each station based on datetime
      last_rows = df.sort_values('datetime').groupby('station').last().reset_index()

      # Find the station with the highest AirQualityIndex
      highest_aqi_row = last_rows.loc[last_rows['AirQualityIndex'].idxmax()]

      # Extract the station name and AQI value
      #highest_station = highest_aqi_row['station']
      highest_aqi = highest_aqi_row['AirQualityIndex']

      if output is None:
        return highest_aqi
      elif output == 'time':
         return highest_aqi_row['datetime']

  # Check station
  if station is None and forecast:
      # Let's get the data from that station
      lowest_fore = df.loc[df["AirQualityIndex"].idxmin()]
      max_fore = df.loc[df["AirQualityIndex"].idxmax()]

      highest_aqi_fore = max_fore['AirQualityIndex']
      lowest_aqi_fore = lowest_fore['AirQualityIndex']

      low_max = [lowest_aqi_fore, highest_aqi_fore]

      if output is None:
        return low_max
      elif output == 'time':
        return [max_fore['datetime'], lowest_fore['datetime']]
  
  elif station in list(df["station"].values) and forecast == False:
      # Let's get the data from that station
      filter_station = df[df["station"] == station].iloc[-1:, -2].values[0]

      return filter_station
  
  elif station in list(df["station"].values) and forecast:
      # Let's get the data from that station
      lowest_fore = df.loc[df[df["station"] == station]["AirQualityIndex"].idxmin()]
      max_fore = df.loc[df[df["station"] == station]["AirQualityIndex"].idxmax()]

      highest_aqi_fore = max_fore['AirQualityIndex']
      lowest_aqi_fore = lowest_fore['AirQualityIndex']

      low_max = [lowest_aqi_fore, highest_aqi_fore]

      if output is None:
        return low_max
      elif output == 'time':
        return [max_fore['datetime'], lowest_fore['datetime']]
  
  elif station not in df.columns:
      "No data for selected station"
      return 6
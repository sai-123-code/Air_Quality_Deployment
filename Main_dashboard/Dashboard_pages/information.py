import streamlit as st
import pandas as pd
import locale
from pathlib import Path
from datetime import datetime, timedelta
from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data, get_some_stations, round_to_nearest_hour


# Set locale to Spanish (replace 'es_MX' with your system's Spanish locale if needed)
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Use "es_MX.UTF-8" for Mexico-specific locale

# Style the dataframe
def color_risk(val):
    if val == 'Low':
        return 'color: #00E400'
    elif val == 'Moderate':
        return 'color: #FFFF00'
    elif val == 'High':
        return 'color: #FF7E00'
    elif val == 'Very High':
        return 'color: #FF0000'
    else:
        return 'color: #8F3F97'

# Style the dataframe
def color_air_quality(val):
    if val == 'Good':
        return 'color: #00E400'
    elif val == 'Acceptable':
        return 'color: #FFFF00'
    elif val == 'Bad':
        return 'color: #FF7E00'
    elif val == 'Very bad':
        return 'color: #FF0000'
    else:
        return 'color: #8F3F97'

# Function to get formatted date and time in a specific language
def get_date_time(lang):
    if lang == "en":
        locale.setlocale(locale.LC_TIME, "en_US.UTF-8")  # Set locale to English
    elif lang == "es":
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Set locale to Spanish
    else:
        raise ValueError("Unsupported language. Please choose 'English' or 'Spanish'.")

    current_date = datetime.now().strftime("%A %d de %B de %Y")
    formatted_date = current_date.capitalize()
    current_time = datetime.now().strftime("%H:%M")
    return formatted_date, current_time

def information_page():
    lang = st.session_state.language

    selected_station = st.selectbox((get_text('station', lang)).capitalize(), get_some_stations())
    formatted_date, current_time = get_date_time(lang)
    st.markdown(
                f"""
                
                📅 {formatted_date} &nbsp;&nbsp;&nbsp;&nbsp;
                🕒 {current_time} &nbsp;&nbsp;&nbsp;&nbsp; 
                """,
                unsafe_allow_html=True
            )

    # Get the nearest hour
    nearest_hour = round_to_nearest_hour(datetime.now())

    # Get the end hour to be displayed which is three hours from the nearest hour
    end_hour = nearest_hour + timedelta(hours=23)
    
    # Let's get the current levels of the pollutants from all the stations
    list_of_stations = {"PED": "Pedregal",
                    "UIZ": "UAM Iztapalapa",
                    "BJU": "Benito Juarez",
                    "MER": "Merced"}

    # Now let's extract the info from the xlsx files

    # Path to the data
    BASE_DIR = Path(__file__).resolve().parent.parent

    stations_data = pd.DataFrame()

    # Load the data
    for i in list(list_of_stations.keys()):
        df_pollutants = pd.read_excel(BASE_DIR / 'Dashboard_data' / 'current_data' / f'{i}_merged_imputed.xlsx')
        if 'index' in df_pollutants.columns:
            df_pollutants = df_pollutants.drop('index', axis=1)
        df_pollutants['station'] = list_of_stations[i]
        df_pollutants.columns = ['datetime', 'direct_radiation (W/m²)',	'PM25', 'PM10',	'SO2', 'O3', 'NO2',	'CO', 'RH',	'TMP',	'WDR',	'WSP',	'is_festival',	'is_weekend',	'AirQualityIndex', 'station']
        stations_data = pd.concat([stations_data, df_pollutants], ignore_index=True)

    forecast_data = pd.DataFrame()

    # Load the data
    for i in list(list_of_stations.keys()):
        df_pollutants_f = pd.read_excel(BASE_DIR / 'Dashboard_data' / 'forecast_data' / f'{i}_forecast.xlsx')
        if 'index' in df_pollutants_f.columns:
            df_pollutants_f = df_pollutants_f.drop('index', axis=1)
        df_pollutants_f['station'] = list_of_stations[i]
        df_pollutants_f.columns = ['datetime', 'direct_radiation (W/m²)',	'PM25', 'PM10',	'SO2', 'O3', 'NO2',	'CO', 'RH',	'TMP',	'WDR',	'WSP',	'is_festival',	'is_weekend',	'AirQualityIndex', 'station']
        forecast_data = pd.concat([forecast_data, df_pollutants_f], ignore_index=True)

    # Page title and description
    st.title(get_text('information', lang))
    
    # Create two columns for best/worst time cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🌟 {get_text('best_time', lang)}\n\n"
                "**8:00 - 11:00**\n\n"
                f"{get_text('current_forecast', lang)}: Good")
    
    with col2:
        st.info(f"⚠️ {get_text('worst_time', lang)}\n\n"
                "**14:00 - 17:00**\n\n"
                f"{get_text('current_forecast', lang)}: Bad")
    
    # Create two columns for user selection of time and group
    col1, col2 = st.columns(2)
    
    with col1:
        option_time = st.selectbox(get_text('select_time', lang), ("06:00 - 09:00", "09:00 - 12:00", "12:00 - 15:00", "15:00 - 18:00", "18:00 - 21:00", "21:00 - 00:00", "00:00 - 03:00", "03:00 - 06:00"))
        st.write(get_text('selected', lang), option_time)
    
    with col2:
        option_group = st.selectbox(get_text('select_group', lang), (get_text('general_population', lang), get_text('children_and_pregnant', lang), get_text('people_cardiovascular', lang)))
        st.write(get_text('selected', lang), option_group)
    
    # Create the main recommendations table
    data = {
        'Time': ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00'],
        'Air Quality': ['Good', 'Bad', 'Bad'],
        'Risk Level': ['Low', 'High', 'High'],
        'Description of risk': ['The health risk is minimal or non-existent.', 'It is unlikely that health will be affected.', 'It is unlikely that health will be affected.'],
        'Messages': [
            'Enjoy outdoor activities',
            'Outdoor activities are possible. If you have symptoms such as coughing or shortness of breath, take more breaks and do less vigorous activities. Stay informed about the evolution of air quality.',
            'Outdoor activities are possible. If you have symptoms such as coughing or shortness of breath, take more breaks and do less vigorous activities. Stay informed about the evolution of air quality.'
        ]
    }
    
    df = pd.DataFrame(data)

    # Apply styling
    styled_df = df.style.applymap(color_risk, subset=['Risk Level']).applymap(color_air_quality, subset=['Air Quality'])
    
    # Display the table with custom CSS
    st.markdown("""
        <style>
        .stDataFrame {
            font-size: 16px;
        }
        .stDataFrame td {
            padding: 15px !important;
        }
        .stDataFrame th {
            background-color: #f0f2f6;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.table(styled_df)
    
    # Add explanatory notes
    st.markdown(get_text('notes', lang))

if __name__ == "__main__":
    st.set_page_config(
        page_title="Information",
        page_icon="🌎",
        layout="wide"
    )
    information_page()
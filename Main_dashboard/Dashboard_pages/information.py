import streamlit as st
import pandas as pd
from datetime import datetime, time

from scripts.language_utils import get_text
from scripts.data_handler import get_current_hour_data, get_all_stations

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

def information_page():
    lang = st.session_state.language

    # Get the selected station from the sidebar
    selected_station = st.session_state.selected_station

    # Get current data
    current_data = get_current_hour_data(selected_station)

    if not current_data:
        st.error("No data available")
        return

    # Page title and description
    st.title(get_text('information', lang))
    
    # Create two columns for best/worst time cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🌟 Best time to be outside\n\n"
                "**8:00 AM - 11:00 AM**\n\n"
                "Air quality: Good")
    
    with col2:
        st.info("⚠️ Worst time to be outside\n\n"
                  "**2:00 PM - 5:00 PM**\n\n"
                  "Air quality: Bad")
    
    # Create two columns for user selection of time and group
    col1, col2 = st.columns(2)
    
    with col1:
        option_time = st.selectbox(get_text('select_time', lang), ("6:00 AM - 9:00 AM", "9:00 AM - 12:00 AM", "12:00 PM - 3:00 PM", "3:00 PM - 6:00 PM", "6:00 PM - 9:00 PM", "9:00 PM - 12:00 AM", "12:00 AM - 3:00 AM", "3:00 AM - 6:00 AM"))
        st.write(get_text('selected', lang), option_time)
    
    with col2:
        option_group = st.selectbox(get_text('select_group', lang), get_text('genaral_population', lang), get_text('children_and_pregnant', lang), get_text('people_cardiovascular', lang))
        st.write(get_text('selected', lang), option_group)
    
    # Create the main recommendations table
    data = {
        'Time': ['6:00 AM - 7:00 AM', '7:00 AM - 8:00 AM', '8:00 AM - 9:00 AM'],
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
    st.markdown("""
    Data is sourced from the monitoring stations in Mexico City and the application is built following the [guidelines from the local authorities](https://dof.gob.mx/nota_detalle.php?codigo=5715154&fecha=25/01/2024#gsc.tab=0). The 24-hour forecast for the Air and Health Index is based on a machine learning model which has 85% accuracy. The Air and Health Index and associated messages are only for information purposes to warn the population. Please consider personal health conditions and stay up-to-date with local authorities and health providers.
    """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Information",
        page_icon="🌎",
        layout="wide"
    )
    information_page()
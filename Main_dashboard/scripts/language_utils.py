def get_text(key, language):
    translations = {
        'nav_title': {
            'en': 'Mexico AQI Monitor',
            'es': 'Monitor de AQI de México'
        },
        'select_page': {
            'en': 'Select Page',
            'es': 'Seleccionar página'
        },
        'page1': {
            'en': 'AQI Heatmap',
            'es': 'Mapa de Calor AQI'
        },
        'forecast': {
            'en': 'Forecast',
            'es': 'Pronostico'
        },
        'main': {
            'en': 'home',
            'es': 'Inicio'
        },
        'information': {
            'en': 'Information',
            'es': 'Informción'
        },
        'current_aqi': {
            'en': 'Current Air Quality Index',
            'es': 'Índice de Calidad del Aire Actual'
        },
        'pollutant_levels': {
            'en': 'Pollutant Levels',
            'es': 'Niveles de Contaminantes'
        },
        'station_aqi': {
            'en': 'Station AQI Levels',
            'es': 'Niveles de AQI por Estación'
        },
        'refresh_map': {
            'en': 'Refresh Map',
            'es': 'Actualizar Mapa'
        },
        'aqi_heatmap': {
            'en': 'AQI Heatmap of Mexico Monitoring Stations',
            'es': 'Mapa de Calor AQI de Estaciones de Monitoreo'
        },
        # AQI Status translations
        'good': {
            'en': 'Good',
            'es': 'Buena'
        },
        'acceptable': {
            'en': 'Acceptable',
            'es': 'Aceptable'
        },
        'bad': {
            'en': 'Bad',
            'es': 'Mala'
        },
        'verybad': {
            'en': 'Very Bad',
            'es': 'Muy Mala'
        },
        'extremelybad': {
            'en': 'Extremely Bad',
            'es': 'Extremadamente Mala'
        },
        'nodata': {
            'en': 'No data or under maintenance',
            'es': 'Sin datos o en mantenimiento'
            
        },
        # Station translations
        'Ajusco Medio': {
            'en': 'Ajusco Medio',
            'es': 'Ajusco Medio'
        },
        'Ajusco': {
            'en': 'Ajusco',
            'es': 'Ajusco'
        },
        'Benito Juarez': {
            'en': 'Benito Juarez',
            'es': 'Benito Juárez'
        },
        'Hospital General': {
            'en': 'General Hospital',
            'es': 'Hospital General de México'
        },
        'Merced': {
            'en': 'Merced',
            'es': 'Merced'
        },
        'Miguel Hidalgo': {
            'en': 'Miguel Hidalgo',
            'es': 'Miguel Hidalgo'
        },
        'Milpa Alta': {
            'en': 'Milpa Alta',
            'es': 'Milpa Alta'
        },
        'Pedregal': {
            'en': 'Pedregal',
            'es': 'Pedregal'
        },
        'San Agustin': {
            'en': 'San Agustin',
            'es': 'San Agustín'
        },
        'Santa Fe': {
            'en': 'Santa Fe',
            'es': 'Santa Fe'
        },
        'Tlalnepantla': {
            'en': 'Tlalnepantla',
            'es': 'Tlalnepantla'
        },
        'UAM Iztapalapa': {
            'en': 'UAM Iztapalapa',
            'es': 'UAM Iztapalapa'
        },
        'Xalostoc': {
            'en': 'Xalostoc',
            'es': 'Xalostoc'
        },
        'station': {
            'en': 'Station',
            'es': 'Estación'
        },
        'select_station': {
            'en': 'Select Station',
            'es': 'Seleccionar Estación'
        },
        'All Stations': {
            'en': 'All Stations',
            'es': 'Todas las Estaciones'
        },
        'current_forecast': {
            'en': 'Air Quality Forecast',
            'es': 'Pronostico de Calidad del Aire'
        },
        'air_quality_index': {
            'en': 'Air Quality Index',
            'es': 'Índice de calidad del aire'
        },
        ''
        'humidity': {
            'en': 'Humidity',
            'es': 'Humedad'
        },
        'pressure': {
            'en': 'Pressure',
            'es': 'Presión'
        },
        'wind_speed': {
            'en': 'Wind Speed',
            'es': 'Velocidad del viento'
        },
        'o3': {
            'en': 'Ozone',
            'es': 'Ozono'
        },
        'no2': {
            'en': 'Nitrogen Dioxide',
            'es': 'Dióxido de nitrógeno'
        },
        'pm10': {
            'en': 'PM10',
            'es': 'PM10'
        },
        'pm25': {
            'en': 'PM2.5',
            'es': 'PM2.5'
        },
        'co': {
            'en': 'CO',
            'es': 'CO'
        },
        'so2': {
            'en': 'SO2',
            'es': 'SO2'
        },
        'metric': {
            'en': 'Metric',
            'es': 'Métrica de medida'
        },
        'pollutants': {
            'en': 'Pollutants',
            'es': 'Contaminantes'
        },
        'temperature': {
            'en': 'Temperature',
            'es': 'Temperatura'
        },
        'time_of_day': {
            'en': 'Time of day',
            'es': 'Hora del día'
        },
        ### Main page
        # Title
        'title_mp': {
            'en': 'Actual Index of Air and Health Map',
            'es': 'Mapa del Índice Actual de Aire y Salud'
        },
        # messages for population
        'air_and_heath_index': {
            'en': 'Actual Air and Health Index:',
            'es': 'Índice de Aire y Salud Actual:'
        },
        'genaral_population': {
            'en': 'General Population:',
            'es': 'Población General:'
        },
        'sensitive_population': {
            'en': 'Sensitive Population:',
            'es': 'Población Sensible:'
        },
        'forecast_message': {
            'en': 'Forecast Air and Health Index of 24 hours:',
            'es': 'Pronóstico del Índice de Aire y Salud de 24 horas:'
        },
        'health_info': {
            'en': 'Index awareness - Health Information',
            'es': 'Índice del Aire - Información de salud'
        },
        'pollutantst': {
            'en': 'Other Pollutants',
            'es': 'Otros Contaminantes'
        },
        'pollutantst_text': {
            'en': 'Particulate Matter',
            'es': 'Material Particulado'
        },
        'second_col_poll': {
            'en': 'Actual levels',
            'es': 'Niveles actuales'
        },
        'tableop': {
            'en': 'Table of pollutants',
            'es': 'Tabla de contaminantes'
        },
        'health_more_details': {
            'en': 'Information about health:',
            'es': 'Información sobre salud:'
        },
        'click_here': {
            'en': 'Link for more details',
            'es': 'Enlace para más detalles'
        },
        'recommend': {
            'en': 'Recommendations for:',
            'es': 'Recomendaciones para:'
        },
        'municipality': {
            'en': 'Municipality',
            'es': 'Municipio'
        },
        'index': {
            'en': 'Index',
            'es': 'Índice'
        }, 
        'selectzone': {
            'en': 'Can you select the zone?',
            'es': '¿Puedes seleccionar la zona?'
        },
        'forexample': {
            'en': 'E.g. Benito Juarez',
            'es': 'Ej. Benito Juárez'
        },
        'mexicocity': {
            'en': 'Mexico City',
            'es': 'Ciudad de México'
        },  
    }
    
    return translations.get(key, {}).get(language, key) 
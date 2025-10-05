# app.py - VERSIÓN COMPLETA CON SINCRONIZACIÓN PERFECTA
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import numpy as np

from config.settings import PAGE_CONFIG, MEXICAN_CLIMATE_ZONES, VARIABLES, CIUDADES_NASA
from styles.custom_styles import get_custom_css, get_climate_badge
from components import (
    render_sidebar,
    render_map,
    render_climate_finder,
    render_metric_cards
)
from components.metricas import (
    render_precipitation_card, 
    render_wind_card,
    render_humidity_card,
    render_cloudiness_card
)
from components.mapa import render_interactive_cities_map

# IMPORTAR ANALIZADORES
from data.csv_processor_optimized import CSVProcessorOptimized
from data.precipitation_analyzer import PrecipitationAnalyzer, integrate_with_processor
from data.wind_analyzer import WindAnalyzer, integrate_wind_with_processor
from data.humidity_analyzer import HumidityAnalyzer, integrate_humidity_with_processor
from data.cloudiness_analyzer import CloudinessAnalyzer, integrate_cloudiness_with_processor

# Configuración de página
st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# ✅ INICIALIZAR SESSION STATE ANTES DE TODO
if 'selected_city_key' not in st.session_state:
    st.session_state.selected_city_key = 'veracruz'

# INICIALIZAR PROCESADORES
@st.cache_resource
def init_processor():
    processor = CSVProcessorOptimized()
    processor.load_all_csvs()
    return processor

@st.cache_resource
def init_precipitation_analyzer():
    return PrecipitationAnalyzer()

@st.cache_resource
def init_wind_analyzer():
    return WindAnalyzer()

@st.cache_resource
def init_humidity_analyzer():
    return HumidityAnalyzer()

@st.cache_resource
def init_cloudiness_analyzer():
    return CloudinessAnalyzer()

processor = init_processor()
precip_analyzer = init_precipitation_analyzer()
wind_analyzer = init_wind_analyzer()
humidity_analyzer = init_humidity_analyzer()
cloudiness_analyzer = init_cloudiness_analyzer()

# HEADER
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="margin-bottom: 0;">🛰️ NASA Climate Intelligence</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-top: 10px;">
        <em>Predicción de Condiciones Climáticas Extremas powered by NASA Earth Observation</em>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

if len(processor.data) > 0:
    total_vars = sum(len(vars_dict) for vars_dict in processor.data.values())
    st.success(f"✅ Datos NASA cargados: {len(processor.data)} ciudades | {total_vars} variables (1990-2024)")
else:
    st.error("❌ No se cargaron datos. Verifica la carpeta data/csv/")

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs([
    "🌍 Análisis por Ubicación",
    "🔍 Buscador de Destinos",
    "📊 Estadísticas Globales"
])

# TAB 3 - ESTADÍSTICAS GLOBALES
with tab3:
    st.header("📊 Estadísticas Globales por Ciudad")
    
    # Selector de fecha con calendario
    selected_date = st.date_input(
        "📅 Selecciona la fecha a analizar",
        value=datetime(2024, 6, 15),
        help="Elige el día que quieres analizar",
        key="global_date"
    )
    
    # Obtener mes y día de la fecha seleccionada
    month = selected_date.month
    day = selected_date.day
    
    # Mostrar el día de la semana
    day_name_spanish = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    day_name = day_name_spanish[selected_date.weekday()]
    
    st.markdown(f"""
    <div style="
        background: rgba(99, 102, 241, 0.2);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0 20px 0;
    ">
        <small style="color: rgba(255,255,255,0.7);">Día seleccionado:</small><br>
        <strong style="color: #00A6ED;">{day_name}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de parámetros climáticos
    selected_params = st.multiselect(
        "Selecciona los parámetros a analizar",
        ["Temperatura", "Precipitación", "Viento", "Humedad", "Nubosidad"],
        default=["Temperatura", "Precipitación"],
        key="global_params"
    )
    
    # Verificar si hay parámetros seleccionados
    if not selected_params:
        st.markdown("""
        <div style="
            background: rgba(99, 102, 241, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-top: 20px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        ">
            <h3 style="color: #00A6ED; margin-bottom: 15px; font-size: 1.2rem;">
                ℹ️ Selecciona Parámetros para Analizar
            </h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;">
                Elige uno o más parámetros del menú superior:
            </p>
            <div style="
                margin-top: 15px;
                display: inline-block;
                text-align: left;
                padding: 15px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            ">
                <div style="color: #00A6ED; font-size: 1.1rem;">
                    🌡️ Temperatura<br>
                    🌧️ Precipitación<br>
                    💨 Viento<br>
                    💧 Humedad<br>
                    ☁️ Nubosidad
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Contenedor para cada ciudad
        for city_key, city_info in processor.city_coords.items():
            with st.expander(f"🏙️ {city_info['name']}", expanded=True):
                results_cols = st.columns(len(selected_params))
                
                for idx, param in enumerate(selected_params):
                    with results_cols[idx]:
                        st.subheader(param)
                        lat, lon = city_info['lat'], city_info['lon']
                    
                    if param == "Temperatura":
                        temp_vals, _ = processor.get_historical_data(lat, lon, 'temperatura', month, day)
                        if temp_vals is not None and len(temp_vals) > 0:
                            stats = processor.get_statistics(temp_vals)
                            st.write(f"🌡️ Temperatura promedio: **{stats['mean']:.1f}°C**")
                            st.write(f"Rango: {stats['min']:.1f}°C - {stats['max']:.1f}°C")
                    
                    elif param == "Precipitación":
                        analysis = integrate_with_processor(
                            processor, precip_analyzer, lat, lon, month, day
                        )
                        if analysis:
                            st.write(precip_analyzer.get_rain_forecast_message(analysis, datetime(2024, month, day)))
                    
                    elif param == "Viento":
                        analysis = integrate_wind_with_processor(
                            processor, wind_analyzer, lat, lon, month, day
                        )
                        if analysis:
                            st.write(wind_analyzer.get_wind_forecast_message(analysis, datetime(2024, month, day)))
                    
                    elif param == "Humedad":
                        analysis = integrate_humidity_with_processor(
                            processor, humidity_analyzer, lat, lon, month, day
                        )
                        if analysis:
                            st.write(humidity_analyzer.get_humidity_message(analysis, datetime(2024, month, day)))
                    
                    elif param == "Nubosidad":
                        analysis = integrate_cloudiness_with_processor(
                            processor, cloudiness_analyzer, lat, lon, month, day
                        )
                        if analysis:
                            st.write(cloudiness_analyzer.get_cloudiness_message(analysis, datetime(2024, month, day)))

# TAB 1 - ANÁLISIS POR UBICACIÓN
with tab1:
    st.markdown("### 📍 Selecciona una ubicación para analizar")
    
    # 🎯 RENDERIZAR SIDEBAR - obtiene inputs del usuario
    user_inputs = render_sidebar()
    
    st.markdown("#### 🗺️ Mapa de Ciudades NASA")
    
    # Mensaje informativo
    st.markdown("""
    <div style="
        background: rgba(99, 102, 241, 0.15);
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
        margin-bottom: 20px;
    ">
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;">
            🖱️ <strong>Haz click en cualquier ciudad del mapa</strong> para seleccionarla automáticamente.
            También puedes usar el selector del sidebar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🗺️ RENDERIZAR MAPA INTERACTIVO
    # Pasar la ciudad actualmente seleccionada
    clicked_city = render_interactive_cities_map(
        selected_city_key=st.session_state.selected_city_key
    )
    
    # 🔄 SI SE HIZO CLICK EN EL MAPA, ACTUALIZAR SESSION STATE Y RECARGAR
    if clicked_city and clicked_city != st.session_state.selected_city_key:
        # Guardar la ciudad clickeada
        st.session_state.selected_city_key = clicked_city
        
        # Obtener información de la ciudad
        city_name = CIUDADES_NASA[clicked_city]['name']
        city_icon = CIUDADES_NASA[clicked_city]['icon']
        
        # 🔁 RECARGAR INMEDIATAMENTE para actualizar el sidebar
        st.rerun()
    
    st.markdown("---")
    
    # INFORMACIÓN DE LA CIUDAD SELECCIONADA
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        city_data = user_inputs['city_data']
        st.markdown(f"""
        <div class="metric-card animated" style="border-left: 4px solid {city_data['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {city_data['icon']}
            </div>
            <h3 style='color: {city_data['color']}; text-align: center; margin-bottom: 15px;'>
                {city_data['name']}
            </h3>
            <div style='margin: 10px 0;'>
                <p style='color: rgba(255,255,255,0.9); text-align: center; line-height: 1.6;'>
                    {city_data['description']}
                </p>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                <p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>
                    <strong style='color: #6366f1;'>📍 Estado:</strong> {city_data['state']}
                </p>
                <p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>
                    <strong style='color: #6366f1;'>🌐 Coordenadas:</strong><br>
                    Lat: {city_data['lat']}° | Lon: {city_data['lon']}°
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown(f"""
        <div class="metric-card animated">
            <h4 style='color: #00A6ED; margin-bottom: 20px;'>
                📅 Parámetros de Consulta
            </h4>
            <div style='margin: 10px 0;'>
                <strong style='color: #6366f1;'>📆 Fecha:</strong>
                <p style='color: white; margin: 5px 0 15px 0;'>
                    {user_inputs['date'].strftime('%d de %B, %Y')}
                </p>
            </div>
            <div style='margin: 10px 0;'>
                <strong style='color: #6366f1;'>🌡️ Variables:</strong>
                <p style='color: white; margin: 5px 0;'>
                    {'✅ Temperatura' if user_inputs['variables'].get('temperatura') else '⬜ Temperatura'}<br>
                    {'✅ Precipitación' if user_inputs['variables'].get('precipitacion') else '⬜ Precipitación'}<br>
                    {'✅ Viento' if user_inputs['variables'].get('viento') else '⬜ Viento'}<br>
                    {'✅ Humedad' if user_inputs['variables'].get('humedad') else '⬜ Humedad'}<br>
                    {'✅ Nubosidad' if user_inputs['variables'].get('nubosidad') else '⬜ Nubosidad'}
                </p>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.85rem; text-align: center;'>
                    🛰️ Datos de NASA GIOVANNI<br>
                    Período: 1990-2024 (~35 años)
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Análisis de Probabilidades")
    
    # ANÁLISIS DE DATOS
    if user_inputs['consultar']:
        if len(processor.data) == 0:
            st.error("❌ No hay datos cargados")
        else:
            with st.spinner('🛰️ Procesando datos históricos NASA GIOVANNI...'):
                lat = user_inputs['lat']
                lon = user_inputs['lon']
                fecha = user_inputs['date']
                month = fecha.month
                day = fecha.day
                
                results_temp = {}
                results_precip = None
                results_wind = None
                results_humidity = None
                results_cloudiness = None
                city_name = None
                
                # TEMPERATURA
                if user_inputs['variables'].get('temperatura'):
                    temp_vals, detected_city = processor.get_historical_data(
                        lat, lon, 'temperatura', month, day
                    )
                    
                    if detected_city:
                        city_name = detected_city
                    
                    if temp_vals is not None and len(temp_vals) > 0:
                        var_info = VARIABLES['temperatura']
                        avg_value = float(np.mean(temp_vals))
                        probability = processor.calculate_probability(
                            temp_vals,
                            threshold=var_info['threshold_extreme'],
                            condition='greater'
                        )
                        delta = avg_value - var_info['threshold_extreme']
                        
                        results_temp['temperatura'] = {
                            'value': round(avg_value, 1),
                            'delta': round(delta, 1),
                            'probability': probability
                        }
                
                # PRECIPITACIÓN
                if user_inputs['variables'].get('precipitacion'):
                    results_precip = integrate_with_processor(
                        processor, precip_analyzer, lat, lon, month, day
                    )
                    if results_precip and not city_name:
                        city_name = results_precip['city_name']
                
                # VIENTO
                if user_inputs['variables'].get('viento'):
                    results_wind = integrate_wind_with_processor(
                        processor, wind_analyzer, lat, lon, month, day
                    )
                    if results_wind and not city_name:
                        city_name = results_wind['city_name']
                
                # HUMEDAD
                if user_inputs['variables'].get('humedad'):
                    results_humidity = integrate_humidity_with_processor(
                        processor, humidity_analyzer, lat, lon, month, day
                    )
                    if results_humidity and not city_name:
                        city_name = results_humidity['city_name']
                
                # NUBOSIDAD
                if user_inputs['variables'].get('nubosidad'):
                    results_cloudiness = integrate_cloudiness_with_processor(
                        processor, cloudiness_analyzer, lat, lon, month, day
                    )
                    if results_cloudiness and not city_name:
                        city_name = results_cloudiness['city_name']
                
                # MOSTRAR RESULTADOS
                if any([results_temp, results_precip, results_wind, results_humidity, results_cloudiness]):
                    st.success(f"✅ Análisis completado - Ciudad NASA: **{city_name}**")
                    
                    if results_temp:
                        st.markdown("#### 🌡️ Temperatura")
                        render_metric_cards(results_temp)
                        st.markdown("---")
                    
                    if results_precip:
                        st.markdown("#### 🌧️ Precipitación")
                        render_precipitation_card(results_precip)
                        st.markdown("---")
                    
                    if results_wind:
                        st.markdown("#### 💨 Viento")
                        render_wind_card(results_wind)
                        st.markdown("---")
                    
                    if results_humidity:
                        st.markdown("#### 💧 Humedad")
                        render_humidity_card(results_humidity)
                        st.markdown("---")
                    
                    if results_cloudiness:
                        st.markdown("#### ☁️ Nubosidad")
                        render_cloudiness_card(results_cloudiness)
                        st.markdown("---")
                    
                    # Información adicional
                    st.markdown("### 📈 Detalles del Análisis")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("🏙️ Ciudad NASA", city_name)
                    with col_b:
                        st.metric("📅 Mes", fecha.strftime("%B"))
                    with col_c:
                        vars_count = len([v for v in [results_temp, results_precip, results_wind, results_humidity, results_cloudiness] if v])
                        st.metric("📊 Variables", vars_count)
                else:
                    st.warning("⚠️ Selecciona al menos una variable para analizar")
    
    else:
        st.markdown("""
        <div class="metric-card animated" style="text-align: center; padding: 40px;">
            <h3>⚙️ Configura tu análisis</h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 15px;">
                Usa el panel lateral para:<br><br>
                📍 Seleccionar ciudad (sidebar o mapa)<br>
                📅 Ajustar la fecha<br>
                🌡️ Seleccionar variables<br><br>
                Luego presiona <strong>"🔍 Consultar Datos NASA"</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2 - BUSCADOR DE DESTINOS
with tab2:
    st.markdown("### 🔍 Encuentra tu Destino Perfecto por Clima")
    render_climate_finder(processor)

# TAB 3 - ESTADÍSTICAS GLOBALES
with tab3:
    st.markdown("#### 🛰️ Ciudades con Datos NASA GIOVANNI")
    
    cols = st.columns(5)
    for idx, (city_key, city_info) in enumerate(CIUDADES_NASA.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {city_info['color']}; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">
                    {city_info['icon']}
                </div>
                <h4 style="color: {city_info['color']}; margin: 10px 0;">
                    {city_info['name']}
                </h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 10px 0;">
                    📍 {city_info['state']}<br>
                    🌐 {city_info['lat']}°, {city_info['lon']}°
                </p>
                <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <small style="color: rgba(255,255,255,0.6);">
                        ✅ 5 variables climáticas
                    </small>
                </div>
            </div>
            """, unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("""
<div class='footer animated'>
    <div style="margin-bottom: 20px;">
        <span style="font-size: 2rem;">🚀</span>
    </div>
    <h4 style="color: #00A6ED; margin-bottom: 10px;">
        NASA Space Apps Challenge 2024
    </h4>
    <p style="font-size: 1rem; opacity: 0.9;">
        Datos 100% reales de <strong>NASA GIOVANNI</strong> • MERRA-2 & GPM
    </p>
    <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 15px;">
        Proyecto: <strong>WIROMP Los Ubuntus</strong>
    </p>
</div>
""", unsafe_allow_html=True)
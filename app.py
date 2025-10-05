# app.py
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

from components.mapa import render_interactive_cities_map
from data.csv_processor import CSVProcessor

# Configuración de página
st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

# Aplicar estilos
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================
# INICIALIZAR SESSION STATE
# ============================================
if 'selected_city_key' not in st.session_state:
    st.session_state.selected_city_key = 'veracruz'

# ============================================
# INICIALIZAR PROCESADOR
# ============================================
@st.cache_resource
def init_processor():
    """Inicializa y carga los CSVs de NASA"""
    processor = CSVProcessor()
    processor.load_all_csvs()
    return processor

processor = init_processor()

# ============================================
# HEADER PRINCIPAL
# ============================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="margin-bottom: 0;">🛰️ NASA Climate Intelligence</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-top: 10px;">
        <em>Predicción de Condiciones Climáticas Extremas powered by NASA Earth Observation</em>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Mostrar estado
if len(processor.data) > 0:
    total_vars = sum(len(vars_dict) for vars_dict in processor.data.values())
    st.success(f"✅ Datos NASA cargados: {len(processor.data)} ciudades | {total_vars} variables con series temporales (1990-2024)")
else:
    st.error("❌ No se cargaron datos. Verifica la carpeta data/csv/")

st.markdown("---")

# ============================================
# TABS PRINCIPALES
# ============================================
tab1, tab2, tab3 = st.tabs([
    "🌍 Análisis por Ubicación",
    "🔍 Buscador de Destinos",
    "📊 Estadísticas Globales"
])

# ============================================
# TAB 1: ANÁLISIS POR UBICACIÓN
# ============================================
# REEMPLAZA COMPLETAMENTE EL CONTENIDO DE with tab1: en app.py

with tab1:
    st.markdown("### 🔍 Selecciona una ubicación para analizar")
    
    # ============================================
    # PASO 1: RENDERIZAR SIDEBAR
    # ============================================
    user_inputs = render_sidebar()
    
    # ============================================
    # PASO 2: MAPA INTERACTIVO
    # ============================================
    st.markdown("#### 🗺️ Mapa de Ciudades NASA")
    
    st.markdown("""
    <div style="
        background: rgba(99, 102, 241, 0.15);
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
        margin-bottom: 20px;
    ">
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;">
            💡 <strong>Tip:</strong> Haz click en cualquier ciudad del mapa para seleccionarla 
            y ver sus datos climáticos históricos de NASA GIOVANNI.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # RENDERIZAR MAPA Y CAPTURAR CLICKS
    clicked_city = render_interactive_cities_map(selected_city_key=user_inputs['city_key'])
    
    # ============================================
    # PASO 3: PROCESAR CLICK EN EL MAPA
    # ============================================
    if clicked_city and clicked_city != st.session_state.selected_city_key:
        # El usuario clickeó una ciudad DIFERENTE a la actual
        st.session_state.selected_city_key = clicked_city
        
        # Mostrar notificación de cambio
        city_name = CIUDADES_NASA[clicked_city]['name']
        st.success(f"🔄 **Ciudad seleccionada:** {city_name}")
        
        # Forzar recarga para actualizar toda la interfaz
        st.rerun()
    
    st.markdown("---")
    
    # ============================================
    # INFORMACIÓN DE LA CIUDAD SELECCIONADA
    # ============================================
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
                    {'✅ Precipitación' if user_inputs['variables'].get('precipitacion') else '⬜ Precipitación'}
                </p>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.85rem; text-align: center;'>
                    🛰️ Datos de NASA GIOVANNI<br>
                    Período: 1990-2024 (~320 registros)
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Análisis de Probabilidades")
    
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
                
                results = {}
                city_name = None
                
                # Procesar variables seleccionadas
                for var_key, is_selected in user_inputs['variables'].items():
                    if not is_selected:
                        continue
                    
                    if var_key not in ['temperatura', 'precipitacion']:
                        continue
                    
                    historical_data, detected_city = processor.get_historical_data(
                        lat, lon, var_key, month, day
                    )
                    
                    if detected_city:
                        city_name = detected_city
                    
                    if historical_data is not None and len(historical_data) > 0:
                        var_info = VARIABLES[var_key]
                        avg_value = float(np.mean(historical_data))
                        probability = processor.calculate_probability(
                            historical_data,
                            threshold=var_info['threshold_extreme'],
                            condition='greater'
                        )
                        delta = avg_value - var_info['threshold_extreme']
                        
                        results[var_key] = {
                            'value': round(avg_value, 1),
                            'delta': round(delta, 1),
                            'probability': probability
                        }
                
                # Mostrar resultados
                if results:
                    st.success(f"✅ Análisis completado - Ciudad NASA: **{city_name}**")
                    st.markdown("### 📊 Métricas Climáticas (Datos Reales NASA 1990-2024)")
                    render_metric_cards(results)
                    
                    st.markdown("---")
                    
                    # Info adicional
                    st.markdown("### 📈 Detalles del Análisis")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("🏙 Ciudad NASA", city_name)
                    with col_b:
                        st.metric("📅 Mes", fecha.strftime("%B"))
                    with col_c:
                        st.metric("📊 Variables", len(results))
                    
                    # Leyenda de interpretación
                    with st.expander("ℹ️ ¿Cómo interpretar estos resultados?"):
                        st.markdown("""
                        <div style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                            <p><strong style="color: #00A6ED;">📊 Valor promedio:</strong> 
                            Es el promedio histórico para este mes basado en 35 años de datos (1990-2024).</p>
                            
                            <p><strong style="color: #00A6ED;">📈 Probabilidad:</strong> 
                            Indica qué tan frecuente ha sido que se supere el umbral extremo en este mes.</p>
                            
                            <p><strong style="color: #00A6ED;">🎯 Umbrales extremos:</strong></p>
                            <ul>
                                <li>Temperatura: > 35°C (calor extremo)</li>
                                <li>Precipitación: > 50mm (lluvia intensa)</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Selecciona al menos 'Temperatura' o 'Precipitación' para analizar")
    
    else:
        st.markdown("""
        <div class="metric-card animated" style="text-align: center; padding: 40px;">
            <h3>👈 Configura tu análisis</h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 15px;">
                Usa el panel lateral para:<br><br>
                1️⃣ Ajustar la fecha<br>
                2️⃣ Seleccionar variables<br>
                3️⃣ Presionar <strong>"🔍 Consultar Datos NASA"</strong>
            </p>
            <br>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                💡 También puedes hacer click en cualquier ciudad del mapa arriba
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: BUSCADOR DE DESTINOS
# ============================================
with tab2:
    st.markdown("### 🔍 Encuentra tu Destino Perfecto por Clima")
    st.markdown("""
    <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin-bottom: 30px;">
        ¿Planeas unas vacaciones? Selecciona el clima que deseas y te mostraremos 
        los mejores destinos en México con mayor probabilidad de tener esas condiciones.
    </p>
    """, unsafe_allow_html=True)
    
    render_climate_finder()

# ============================================
# TAB 3: ESTADÍSTICAS GLOBALES
# ============================================
with tab3:
    st.markdown("### 📊 Estadísticas Climáticas de México")
    
    # Mostrar las 5 ciudades con datos
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
                        ✅ Datos disponibles:<br>
                        Temperatura & Precipitación
                    </small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #00A6ED;">🌎 Cobertura del Sistema</h4>
        <p style="color: rgba(255,255,255,0.9); line-height: 1.8;">
            Nuestro sistema analiza datos históricos de NASA GIOVANNI para <strong>5 ciudades principales</strong> 
            con series temporales completas de 1990 a 2024 (35 años de datos mensuales = ~320 registros por variable).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🛰️ Fuentes de Datos NASA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #6366f1;">📡 GIOVANNI - MERRA-2 & GPM</h4>
            <p style="color: rgba(255,255,255,0.9);">
                Modern-Era Retrospective analysis for Research and Applications
            </p>
            <ul style="color: rgba(255,255,255,0.8); line-height: 1.8;">
                <li>Datos satelitales NASA</li>
                <li>Resolución: Mensual</li>
                <li>Período: 1990-2024</li>
                <li>~320 registros por variable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #06b6d4;">🌍 Variables y Ciudades</h4>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 10px;">
                <strong>Variables disponibles:</strong>
            </p>
            <ul style="color: rgba(255,255,255,0.8); line-height: 1.6; margin-bottom: 15px;">
                <li>🌡️ Temperatura (MERRA-2)</li>
                <li>🌧️ Precipitación (GPM)</li>
            </ul>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 10px;">
                <strong>Ciudades:</strong>
            </p>
            <ul style="color: rgba(255,255,255,0.8); line-height: 1.6;">
                <li>🌊 Veracruz • 🏛️ CDMX • 🏖️ Cancún</li>
                <li>🏔️ Monterrey • 🌵 Tijuana</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
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
        Datos 100% reales de <strong>NASA GIOVANNI</strong> • MERRA-2 & GPM Datasets
    </p>
    <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 15px;">
        🌟 Proyecto: <strong>WIROMP Los Ubuntus</strong>
    </p>
    <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 10px;">
        Veracruz, México • 2024
    </p>
</div>
""", unsafe_allow_html=True)
# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import PAGE_CONFIG, MEXICAN_CLIMATE_ZONES
from styles.custom_styles import get_custom_css, get_climate_badge
from components import (
    render_sidebar,
    render_map,
    render_climate_finder
)

# Configuración de página
st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

# Aplicar estilos personalizados
st.markdown(get_custom_css(), unsafe_allow_html=True)

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

# ============================================
# TABS PRINCIPALES
# ============================================
tab1, tab2, tab3 = st.tabs([
    "🌍 Análisis por Ubicación",
    "🔍 Buscador de Destinos",
    "📊 Estadísticas Globales"
])

# ============================================
# TAB 1: ANÁLISIS POR UBICACIÓN (ORIGINAL)
# ============================================
with tab1:
    st.markdown("### 📍 Selecciona una ubicación para analizar")
    
    user_inputs = render_sidebar()
    
    # Layout en columnas
    col_map, col_info = st.columns([2, 1])
    
    with col_map:
        st.markdown("#### 🗺️ Ubicación en el Mapa")
        render_map(
            lat=user_inputs['lat'],
            lon=user_inputs['lon'],
            location_name=user_inputs['location_name']
        )
    
    with col_info:
        st.markdown(f"""
        <div class="metric-card animated">
            <h4 style='color: #00A6ED; margin-bottom: 20px;'>
                📊 Información de Ubicación
            </h4>
            <div style='margin: 10px 0;'>
                <strong style='color: #6366f1;'>📍 Lugar:</strong>
                <p style='color: white; margin: 5px 0 15px 0;'>{user_inputs['location_name']}</p>
            </div>
            <div style='margin: 10px 0;'>
                <strong style='color: #6366f1;'>🌐 Coordenadas:</strong>
                <p style='color: white; margin: 5px 0 15px 0;'>
                    Lat: {user_inputs['lat']}°<br>
                    Lon: {user_inputs['lon']}°
                </p>
            </div>
            <div style='margin: 10px 0;'>
                <strong style='color: #6366f1;'>📅 Fecha de Consulta:</strong>
                <p style='color: white; margin: 5px 0;'>
                    {user_inputs['date'].strftime('%d de %B, %Y')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sección de análisis
    st.markdown("### 📈 Análisis de Probabilidades")
    
    if user_inputs['consultar']:
        # Animación de carga
        with st.spinner('🛰️ Consultando datos de NASA GIOVANNI...'):
            import time
            time.sleep(1.5)  # Simulación de carga
        
        # Mensaje de desarrollo
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #F59E0B;">
            <h4>⚙️ Sistema en Desarrollo</h4>
            <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                El backend está siendo integrado con las APIs de NASA GIOVANNI.<br>
                Los datos climáticos se visualizarán aquí próximamente.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Variables que se analizarán
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #06b6d4;">🌡️ Variables Atmosféricas</h4>
                <ul style="color: rgba(255,255,255,0.9); line-height: 2;">
                    <li><strong>Temperatura:</strong> Extremas altas/bajas</li>
                    <li><strong>Precipitación:</strong> Intensidad de lluvia</li>
                    <li><strong>Cobertura de Nubes:</strong> Porcentaje nuboso</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color: #8b5cf6;">💨 Variables Dinámicas</h4>
                <ul style="color: rgba(255,255,255,0.9); line-height: 2;">
                    <li><strong>Viento:</strong> Velocidad y ráfagas</li>
                    <li><strong>Humedad Relativa:</strong> Nivel de humedad</li>
                    <li><strong>Índice de Confort:</strong> Condiciones combinadas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Ejemplo de visualización (placeholder)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 Vista Previa de Visualizaciones")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric(
                label="🌡️ Temperatura",
                value="Próximamente",
                delta="En desarrollo",
                delta_color="off"
            )
        
        with col_b:
            st.metric(
                label="🌧️ Precipitación",
                value="Próximamente",
                delta="En desarrollo",
                delta_color="off"
            )
        
        with col_c:
            st.metric(
                label="💨 Viento",
                value="Próximamente",
                delta="En desarrollo",
                delta_color="off"
            )
    
    else:
        st.markdown("""
        <div class="metric-card animated" style="text-align: center; padding: 40px;">
            <h3>👈 Comienza tu análisis</h3>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 15px;">
                Configura la ubicación y fecha en el panel lateral,<br>
                luego presiona <strong>"🔍 Consultar Datos"</strong> para ver las predicciones
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: BUSCADOR DE DESTINOS (INNOVACIÓN)
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
    
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #00A6ED;">🌎 Cobertura del Sistema</h4>
        <p style="color: rgba(255,255,255,0.9); line-height: 1.8;">
            Nuestro sistema analiza datos históricos de NASA GIOVANNI para <strong>28 ciudades</strong> 
            estratégicamente seleccionadas que representan los 5 tipos de clima principales de México.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mostrar las 5 categorías climáticas
    st.markdown("#### 🗺️ Zonas Climáticas Cubiertas")
    
    for zone_key, zone_data in MEXICAN_CLIMATE_ZONES.items():
        with st.expander(f"{zone_data['emoji']} {zone_data['nombre']} ({len(zone_data['cities'])} ciudades)"):
            st.markdown(f"**Descripción:** {zone_data['description']}")
            st.markdown("**Ciudades incluidas:**")
            
            cities_cols = st.columns(2)
            for idx, city in enumerate(zone_data['cities']):
                col_idx = idx % 2
                with cities_cols[col_idx]:
                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.05);
                        padding: 10px;
                        border-radius: 10px;
                        margin: 5px 0;
                        border-left: 3px solid {zone_data['color']};
                    ">
                        <strong>{city['name']}</strong><br>
                        <small style="color: rgba(255,255,255,0.7);">
                            {city['state']} • Alt: {city['alt']}m
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información sobre fuentes de datos
    st.markdown("#### 🛰️ Fuentes de Datos NASA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #6366f1;">📡 GIOVANNI</h4>
            <p style="color: rgba(255,255,255,0.9);">
                GES DISC Interactive Online Visualization and Analysis Infrastructure
            </p>
            <ul style="color: rgba(255,255,255,0.8); line-height: 1.8;">
                <li>Datos de múltiples satélites</li>
                <li>Resolución temporal: diaria</li>
                <li>Cobertura: 20+ años</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #06b6d4;">🌍 Variables Monitoreadas</h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li>🌡️ Temperatura del aire (2m)</li>
                <li>🌧️ Precipitación acumulada</li>
                <li>☁️ Cobertura de nubes</li>
                <li>💨 Velocidad del viento (10m)</li>
                <li>💧 Humedad relativa</li>
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
        Datos proporcionados por <strong>NASA Earth Observation</strong> • GIOVANNI Platform
    </p>
    <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 15px;">
        🌟 Proyecto desarrollado por: <strong>WIROMP Los Ubuntus</strong>
    </p>
    <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 10px;">
        Veracruz, México • 2024
    </p>
</div>
""", unsafe_allow_html=True)
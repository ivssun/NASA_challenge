# components/climate_finder_enhanced.py
"""
Buscador de Destinos MEJORADO - VERSIÓN CORREGIDA
✅ SOLUCIONA el problema del parpadeo sin mostrar resultados
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from config.settings import CIUDADES_NASA, COLORS
from data.destination_finder_enhanced import DestinationFinderEnhanced


def render_destination_map_enhanced(results, condition_info):
    """Renderiza mapa interactivo con destinos encontrados"""
    import folium
    from streamlit_folium import st_folium
    
    # Centro de México
    center_lat = 23.6345
    center_lon = -102.5528
    
    # Crear mapa oscuro estilo NASA
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO'
    )
    
    # Agregar marcadores por cada resultado
    for idx, result in enumerate(results):
        city_info = result['city_info']
        prob = result['overall_probability']
        
        # Color dinámico según probabilidad
        if prob >= 70:
            color = '#10B981'
            icon_color = 'green'
            badge = '🌟'
        elif prob >= 50:
            color = '#34D399'
            icon_color = 'lightgreen'
            badge = '✅'
        elif prob >= 30:
            color = '#FBBF24'
            icon_color = 'orange'
            badge = '⚠️'
        else:
            color = '#EF4444'
            icon_color = 'red'
            badge = '❌'
        
        # Crear popup con información detallada
        popup_html = f"""
        <div style="
            font-family: 'Arial', sans-serif; 
            padding: 15px; 
            min-width: 250px;
            background: linear-gradient(135deg, rgba(30,27,75,0.95) 0%, rgba(15,13,38,0.95) 100%);
            border-radius: 10px;
            border: 2px solid {color};
        ">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 10px;">
                {city_info['icon']}
            </div>
            <h3 style="
                margin: 0; 
                color: {color}; 
                text-align: center;
                font-size: 1.3rem;
            ">
                #{idx+1} {result['city_name']}
            </h3>
            <p style="
                margin: 8px 0; 
                text-align: center; 
                color: rgba(255,255,255,0.8);
                font-size: 0.9rem;
            ">
                📍 {city_info['state']}
            </p>
            
            <div style="
                background: {color}22; 
                padding: 15px; 
                border-radius: 8px; 
                margin-top: 15px;
                border: 1px solid {color}44;
            ">
                <h2 style="
                    margin: 0; 
                    color: {color}; 
                    text-align: center;
                    font-size: 2rem;
                ">
                    {badge} {prob}%
                </h2>
                <p style="
                    margin: 8px 0 0 0; 
                    text-align: center; 
                    font-size: 0.85rem;
                    color: rgba(255,255,255,0.9);
                ">
                    Probabilidad de {condition_info['nombre']}
                </p>
            </div>
            
            {"<div style='margin-top: 10px; padding: 8px; background: rgba(16,185,129,0.2); border-radius: 5px; text-align: center;'><small style='color: #10B981;'>⭐ Bonus Estacional</small></div>" if result.get('seasonal_bonus', False) else ""}
        </div>
        """
        
        # Agregar marcador
        folium.Marker(
            location=[city_info['lat'], city_info['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{result['city_name']} - {prob}% {badge}",
            icon=folium.Icon(color=icon_color, icon='location-dot', prefix='fa')
        ).add_to(m)
        
        # Círculo de influencia
        folium.Circle(
            [city_info['lat'], city_info['lon']],
            radius=40000,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.15,
            weight=2,
            opacity=0.8
        ).add_to(m)
    
    # Leyenda mejorada
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px;
        left: 30px;
        background: rgba(30, 27, 75, 0.98);
        padding: 18px;
        border-radius: 12px;
        border: 2px solid {condition_info['color']};
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        z-index: 1000;
        backdrop-filter: blur(10px);
    ">
        <div style="
            color: {condition_info['color']}; 
            font-weight: bold; 
            margin-bottom: 12px;
            font-size: 1.1rem;
            text-align: center;
        ">
            {condition_info['icon']} {condition_info['nombre']}
        </div>
        <div style="color: white; font-size: 0.9rem; line-height: 1.8;">
            🌟 Excelente (≥70%)<br>
            ✅ Buena opción (50-69%)<br>
            ⚠️ Moderada (30-49%)<br>
            ❌ Baja (<30%)
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Renderizar mapa
    st_folium(m, width=None, height=500, key="destination_map_enhanced")


# ============================================
# PARCHE RÁPIDO - REEMPLAZAR LA FUNCIÓN render_result_cards_enhanced
# Copiar TODA esta función en components/climate_finder_enhanced.py
# ============================================

def render_result_cards_enhanced(results, condition_info, show_details=True, max_results=5):
    """Renderiza tarjetas de resultados mejoradas - SIN ERRORES DE HTML"""
    
    # Limitar resultados
    display_results = results[:max_results]
    
    for idx, result in enumerate(display_results):
        city_info = result['city_info']
        prob = result['overall_probability']
        
        # Determinar badge y color
        if prob >= 70:
            badge = '🌟'
            badge_text = 'EXCELENTE'
            badge_color = '#10B981'
        elif prob >= 50:
            badge = '✅'
            badge_text = 'BUENA OPCIÓN'
            badge_color = '#34D399'
        elif prob >= 30:
            badge = '⚠️'
            badge_text = 'MODERADA'
            badge_color = '#FBBF24'
        else:
            badge = '❌'
            badge_text = 'BAJA'
            badge_color = '#EF4444'
        
        # ✅ SOLUCIÓN: Construir HTML de bonus por separado
        bonus_html = ""
        if result.get('seasonal_bonus', False):
            # Usar comillas dobles en lugar de simples
            bonus_html = """
<div style="margin-top: 15px; padding: 10px; background: rgba(16,185,129,0.15); 
            border-radius: 8px; border: 1px solid rgba(16,185,129,0.3); text-align: center;">
    <span style="color: #10B981; font-weight: 600;">⭐ Bonus Estacional - Mes ideal para esta condición</span>
</div>
"""
        
        # Tarjeta principal - USAR f-string con comillas dobles
        card_html = f"""
<div style="
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(30,27,75,0.15) 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 5px solid {city_info['color']};
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                <span style="font-size: 3rem;">{city_info['icon']}</span>
                <div>
                    <h2 style="
                        margin: 0; 
                        color: {city_info['color']};
                        font-size: 1.8rem;
                    ">
                        #{idx+1} {result['city_name']}
                    </h2>
                    <p style="
                        margin: 5px 0 0 0; 
                        color: rgba(255,255,255,0.7);
                        font-size: 1rem;
                    ">
                        📍 {city_info['state']} | 🌐 {city_info['lat']}°, {city_info['lon']}°
                    </p>
                </div>
            </div>
        </div>
        <div style="
            background: {badge_color}22;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid {badge_color}44;
            min-width: 150px;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 5px;">{badge}</div>
            <div style="
                color: {badge_color}; 
                font-size: 2rem; 
                font-weight: bold;
                margin: 5px 0;
            ">
                {prob}%
            </div>
            <div style="
                color: rgba(255,255,255,0.8); 
                font-size: 0.85rem;
                margin-top: 5px;
            ">
                {badge_text}
            </div>
        </div>
    </div>
    {bonus_html}
</div>
"""
        
        # Renderizar la tarjeta
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Detalles climáticos expandibles
        if show_details and result['average_values']:
            with st.expander(f"📊 Ver detalles climáticos de {result['city_name']}", expanded=(idx == 0)):
                
                # Crear columnas para métricas
                num_vars = len(result['average_values'])
                cols = st.columns(min(num_vars, 5))
                
                var_icons = {
                    'temperatura': ('🌡️', '°C', '#EF4444'),
                    'precipitacion': ('🌧️', 'mm', '#3B82F6'),
                    'viento': ('💨', 'km/h', '#06B6D4'),
                    'humedad': ('💧', '%', '#8B5CF6'),
                    'nubosidad': ('☁️', '%', '#6B7280')
                }
                
                for col_idx, (var_key, avg_val) in enumerate(result['average_values'].items()):
                    icon, unit, color = var_icons.get(var_key, ('📊', '', '#6366f1'))
                    var_prob = result['probabilities'].get(var_key, 0)
                    
                    with cols[col_idx % len(cols)]:
                        st.markdown(f"""
                        <div style="
                            background: {color}15;
                            padding: 15px;
                            border-radius: 10px;
                            border: 1px solid {color}33;
                            text-align: center;
                        ">
                            <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                            <div style="color: {color}; font-weight: 600; margin-bottom: 5px;">
                                {var_key.capitalize()}
                            </div>
                            <div style="color: white; font-size: 1.5rem; font-weight: bold;">
                                {avg_val}{unit}
                            </div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 5px;">
                                {var_prob}% probabilidad
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

def render_climate_finder_enhanced(processor=None):
    """
    Componente MEJORADO del buscador de destinos
    ✅ VERSIÓN CORREGIDA - Mantiene resultados persistentes
    """
    
    # ============================================
    # INICIALIZAR SESSION STATE
    # ============================================
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_condition_info' not in st.session_state:
        st.session_state.search_condition_info = None
    if 'search_date' not in st.session_state:
        st.session_state.search_date = None
    
    # ============================================
    # HEADER
    # ============================================
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #00A6ED; font-size: 2rem; margin-bottom: 10px;">
            🌍 Encuentra tu Destino Perfecto por Clima
        </h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">
            Busca el lugar ideal según las condiciones climáticas que deseas experimentar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not processor or len(processor.data) == 0:
        st.error("❌ No hay datos NASA cargados. Verifica la carpeta data/csv/")
        return
    
    # ============================================
    # SECCIÓN DE BÚSQUEDA
    # ============================================
    st.markdown("#### 🎯 Configura tu búsqueda perfecta")
    
    col_date, col_climate = st.columns([1, 1])
    
    with col_date:
        target_date = st.date_input(
            "📅 ¿Cuándo planeas viajar?",
            value=datetime(2025, 12, 24),  # Default: Navidad
            min_value=datetime.today(),
            max_value=datetime.today() + timedelta(days=365),
            help="Selecciona la fecha de tu viaje planeado",
            key="finder_target_date"
        )
        
        # Mostrar día de la semana
        day_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        day_name = day_names[target_date.weekday()]
        month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        st.markdown(f"""
        <div style="
            background: rgba(0,166,237,0.1); 
            padding: 10px; 
            border-radius: 8px;
            text-align: center;
            margin-top: 10px;
        ">
            <small style="color: rgba(255,255,255,0.7);">Fecha seleccionada:</small><br>
            <strong style="color: #00A6ED; font-size: 1.1rem;">
                {day_name}, {target_date.day} de {month_names[target_date.month-1]}
            </strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col_climate:
        st.markdown("❄️ **Tipo de clima que buscas:**")
        
        # Obtener condiciones del finder mejorado
        finder = DestinationFinderEnhanced(processor)
        all_conditions = finder.get_all_conditions()
        climate_options = {key: info['nombre'] for key, info in all_conditions.items()}
        
        selected_climate = st.selectbox(
            "Selecciona el tipo de clima",
            options=list(climate_options.keys()),
            format_func=lambda x: climate_options[x],
            label_visibility="collapsed",
            help="Elige las condiciones climáticas ideales para tu viaje",
            key="finder_climate"
        )
        
        # Mostrar meses recomendados
        recommended_months = finder.get_recommended_months(selected_climate)
        if recommended_months:
            month_names_short = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            recommended_text = ', '.join([month_names_short[m-1] for m in recommended_months])
            
            st.markdown(f"""
            <div style="
                background: rgba(16,185,129,0.1); 
                padding: 8px; 
                border-radius: 6px;
                margin-top: 10px;
                border: 1px solid rgba(16,185,129,0.2);
            ">
                <small style="color: #10B981;">
                    📅 Meses ideales: <strong>{recommended_text}</strong>
                </small>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================
    # OPCIONES AVANZADAS
    # ============================================
    with st.expander("⚙️ Opciones Avanzadas", expanded=False):
        col_prob, col_results = st.columns(2)
        
        with col_prob:
            min_probability = st.slider(
                "Probabilidad mínima (%)",
                0, 100, 20,
                step=5,
                help="Filtra destinos con probabilidad menor a este valor",
                key="finder_min_prob"
            )
        
        with col_results:
            max_results = st.slider(
                "Máximo de resultados",
                3, 10, 5,
                help="Número máximo de destinos a mostrar",
                key="finder_max_results"
            )
        
        col_map, col_details = st.columns(2)
        with col_map:
            show_map = st.checkbox("🗺️ Mostrar mapa interactivo", value=True, key="finder_show_map")
        with col_details:
            show_details = st.checkbox("📊 Mostrar detalles climáticos", value=True, key="finder_show_details")
    
    # ============================================
    # BOTÓN DE BÚSQUEDA
    # ============================================
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button(
        "🔍 Buscar Destinos Perfectos",
        use_container_width=True,
        type="primary",
        key="finder_search_button"
    )
    
    # ✅ EJECUTAR BÚSQUEDA Y GUARDAR EN SESSION STATE
    if search_button:
        with st.spinner('🛰️ Analizando 35 años de datos NASA GIOVANNI...'):
            # Buscar destinos
            results = finder.find_destinations(
                target_date=target_date,
                climate_condition=selected_climate,
                min_probability=min_probability
            )
            
            # GUARDAR EN SESSION STATE
            st.session_state.search_results = results
            st.session_state.search_condition_info = finder.get_condition_info(selected_climate)
            st.session_state.search_date = target_date
    
    st.markdown("---")
    
    # ============================================
    # MOSTRAR RESULTADOS DESDE SESSION STATE
    # ============================================
    if st.session_state.search_results is not None:
        results = st.session_state.search_results
        condition_info = st.session_state.search_condition_info
        saved_date = st.session_state.search_date
        
        # Header con la condición seleccionada
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {condition_info['color']}22 0%, {condition_info['color']}11 100%);
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid {condition_info['color']};
            text-align: center;
            margin-bottom: 30px;
        ">
            <div style="font-size: 4rem; margin-bottom: 15px;">{condition_info['icon']}</div>
            <h2 style="color: {condition_info['color']}; margin-bottom: 15px;">
                {condition_info['nombre']}
            </h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; max-width: 600px; margin: 0 auto 20px;">
                {condition_info['descripcion']}
            </p>
            <div style="
                background: rgba(255,255,255,0.1);
                display: inline-block;
                padding: 10px 20px;
                border-radius: 20px;
                margin-top: 10px;
            ">
                <span style="color: rgba(255,255,255,0.8);">
                    📅 Fecha: <strong style="color: white;">{saved_date.strftime('%d de %B, %Y')}</strong>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar resultados
        if len(results) == 0:
            st.warning(f"""
            ⚠️ No se encontraron destinos con probabilidad mayor a {min_probability}% 
            para las condiciones seleccionadas.
            
            **Sugerencias:**
            - Reduce la probabilidad mínima en opciones avanzadas
            - Prueba con otra condición climática
            - Selecciona una fecha en los meses recomendados
            """)
        else:
            st.success(f"🎯 Se encontraron **{len(results)} destinos** que cumplen tus criterios")
            
            # Mapa interactivo
            if show_map:
                st.markdown("### 🗺️ Mapa de Destinos")
                render_destination_map_enhanced(results, condition_info)
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Tarjetas de resultados
            st.markdown("### 🏆 Mejores Destinos")
            render_result_cards_enhanced(
                results, 
                condition_info, 
                show_details=show_details,
                max_results=max_results
            )
            
            # Resumen estadístico
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Destinos encontrados", len(results))
            with col2:
                avg_prob = np.mean([r['overall_probability'] for r in results])
                st.metric("Probabilidad promedio", f"{avg_prob:.1f}%")
            with col3:
                best_prob = results[0]['overall_probability'] if results else 0
                st.metric("Mejor opción", f"{best_prob:.1f}%")
            with col4:
                seasonal_count = sum(1 for r in results if r.get('seasonal_bonus', False))
                st.metric("Con bonus estacional", seasonal_count)
            
            # Botón para limpiar resultados
            if st.button("🔄 Nueva Búsqueda", key="clear_search"):
                st.session_state.search_results = None
                st.session_state.search_condition_info = None
                st.session_state.search_date = None
                st.rerun()
    
    else:
        # Vista inicial
        render_welcome_section_enhanced(processor, finder)


def render_welcome_section_enhanced(processor, finder):
    """Sección de bienvenida mejorada"""
    
    st.markdown("### 🌍 Descubre tu Destino Ideal")
    
    st.markdown(f"""
    <div style="
        background: rgba(99,102,241,0.1);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(99,102,241,0.2);
        margin-bottom: 30px;
    ">
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; line-height: 1.8; margin: 0;">
            Analiza <strong style="color: #00A6ED;">{len(CIUDADES_NASA)} ciudades mexicanas</strong> 
            con datos reales de <strong style="color: #00A6ED;">NASA GIOVANNI</strong> y encuentra 
            el destino perfecto según las condiciones climáticas que buscas.
            <br><br>
            📊 Basado en <strong>35 años de datos históricos</strong> (1990-2024)
            <br>
            🛰️ <strong>5 variables climáticas:</strong> Temperatura, Precipitación, Viento, Humedad, Nubosidad
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌤️ Condiciones Climáticas Disponibles")
    
    # Mostrar todas las condiciones en grid
    all_conditions = finder.get_all_conditions()
    
    # Crear filas de 3 columnas
    conditions_list = list(all_conditions.items())
    for i in range(0, len(conditions_list), 3):
        cols = st.columns(3)
        for col_idx, (key, info) in enumerate(conditions_list[i:i+3]):
            with cols[col_idx]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {info['color']}15 0%, {info['color']}05 100%);
                    padding: 20px;
                    border-radius: 12px;
                    border: 2px solid {info['color']}33;
                    text-align: center;
                    height: 200px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="font-size: 3rem; margin-bottom: 10px;">{info['icon']}</div>
                    <h4 style="color: {info['color']}; margin: 10px 0; font-size: 1rem;">
                        {info['nombre']}
                    </h4>
                    <p style="
                        color: rgba(255,255,255,0.7); 
                        font-size: 0.85rem; 
                        line-height: 1.4;
                        margin: 0;
                    ">
                        {info['descripcion'][:60]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div style="
        background: rgba(0,166,237,0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #00A6ED;
        margin-top: 20px;
    ">
        <h4 style="color: #00A6ED; margin-top: 0;">💡 ¿Cómo funciona?</h4>
        <p style="color: rgba(255,255,255,0.9); line-height: 1.8; margin: 0;">
            1️⃣ Selecciona la fecha de tu viaje<br>
            2️⃣ Elige el tipo de clima que buscas<br>
            3️⃣ El sistema analiza 35 años de datos históricos de NASA<br>
            4️⃣ Obtén destinos rankeados por probabilidad de tener esas condiciones<br><br>
            <strong>Los resultados se basan en patrones climáticos reales</strong>, 
            permitiéndote planear con confianza científica. 🛰️
        </p>
    </div>
    """, unsafe_allow_html=True)
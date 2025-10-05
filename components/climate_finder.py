# components/climate_finder.py
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from config.settings import MEXICAN_CLIMATE_ZONES, COLORS, CIUDADES_NASA
from styles.custom_styles import get_climate_badge
from data.destination_finder import DestinationFinder

def render_destination_map(results, condition_info):
    """Renderiza mapa con destinos encontrados"""
    import folium
    from streamlit_folium import st_folium
    from folium import plugins
    
    # Centro de México
    center_lat = 23.6345
    center_lon = -102.5528
    
    # Crear mapa
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO'
    )
    
    # Agregar marcadores para cada resultado
    for idx, result in enumerate(results):
        city_info = result['city_info']
        prob = result['overall_probability']
        
        # Color según probabilidad
        if prob >= 70:
            color = '#10B981'
            icon_color = 'green'
        elif prob >= 40:
            color = '#F59E0B'
            icon_color = 'orange'
        else:
            color = '#EF4444'
            icon_color = 'red'
        
        # Popup con información
        popup_html = f"""
        <div style="font-family: Arial; padding: 10px; min-width: 200px;">
            <div style="font-size: 2rem; text-align: center; margin-bottom: 10px;">
                {city_info['icon']}
            </div>
            <h3 style="margin: 0; color: {city_info['color']}; text-align: center;">
                #{idx+1} {result['city_name']}
            </h3>
            <p style="margin: 10px 0; text-align: center;">
                📍 {city_info['state']}
            </p>
            <div style="background: {color}22; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <h2 style="margin: 0; color: {color}; text-align: center;">
                    {prob:.2f}%
                </h2>
                <p style="margin: 5px 0; text-align: center; font-size: 0.85rem;">
                    Probabilidad
                </p>
            </div>
        </div>
        """
        
        # Marcador
        folium.Marker(
            location=[city_info['lat'], city_info['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{result['city_name']} - {prob:.2f}%",
            icon=folium.Icon(color=icon_color, icon='star', prefix='fa')
        ).add_to(m)
        
        # Círculo de área
        folium.Circle(
            [city_info['lat'], city_info['lon']],
            radius=30000,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.2,
            weight=2
        ).add_to(m)
    
    # Leyenda
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 40px;
        left: 25px;
        background: rgba(30, 27, 75, 0.95);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid {condition_info['color']};
        z-index: 1000;
    ">
        <div style="color: {condition_info['color']}; font-weight: bold; margin-bottom: 10px;">
            {condition_info['icon']} {condition_info['nombre']}
        </div>
        <div style="color: white; font-size: 0.85rem;">
            🟢 Alta probabilidad (≥70%)<br>
            🟡 Media probabilidad (40-69%)<br>
            🔴 Baja probabilidad (<40%)
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    st_folium(m, width=None, height=400, key="destination_map")


def render_climate_finder(processor=None):
    """
    Componente principal del buscador de destinos por clima deseado
    Conectado con datos reales de NASA GIOVANNI
    
    Args:
        processor: Instancia de CSVProcessorOptimized con datos cargados
    """
    
    # ============================================
    # SECCIÓN DE BÚSQUEDA
    # ============================================
    st.markdown("#### 🎯 Configura tu búsqueda")
    
    col_date, col_climate = st.columns([1, 1])
    
    with col_date:
        target_date = st.date_input(
            "📅 ¿Cuándo planeas viajar?",
            value=datetime(2025, 12, 24),
            min_value=datetime.today(),
            max_value=datetime.today() + timedelta(days=365),
            help="Selecciona la fecha de tu viaje"
        )
    
    with col_climate:
        # Selector de clima con badges visuales
        st.markdown("❄️ **Tipo de clima que buscas:**")
        
        # Obtener condiciones climáticas del DestinationFinder
        if processor:
            finder = DestinationFinder(processor)
            all_conditions = finder.get_all_conditions()
            climate_options = {key: info['nombre'] for key, info in all_conditions.items()}
        else:
            climate_options = {
                'frio_nevado': '❄️ Clima Frío/Nevado',
                'templado_seco': '🌤️ Clima Templado Seco',
                'calido_soleado': '☀️ Clima Cálido y Soleado',
                'playa_ideal': '🏖️ Clima de Playa Ideal'
            }
        
        selected_climate = st.selectbox(
            "Selecciona el tipo de clima",
            options=list(climate_options.keys()),
            format_func=lambda x: climate_options[x],
            label_visibility="collapsed"
        )
    
    # Opciones avanzadas
    with st.expander("⚙️ Opciones Avanzadas"):
        col_prob, col_results = st.columns(2)
        
        with col_prob:
            min_probability = st.slider(
                "Probabilidad mínima (%)",
                0, 100, 10,
                help="Filtra destinos con probabilidad menor a este valor"
            )
        
        with col_results:
            max_results = st.slider(
                "Máximo de resultados",
                3, 10, 5,
                help="Número máximo de destinos a mostrar"
            )
        
        show_map = st.checkbox("Mostrar mapa interactivo", value=True)
        show_temps = st.checkbox("Mostrar detalles climáticos", value=True)
    
    # Botón de búsqueda
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button(
        "🔍 Buscar Destinos Perfectos",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("---")
    
    # ============================================
    # RESULTADOS DE BÚSQUEDA
    # ============================================
    if search_button:
        if not processor or len(processor.data) == 0:
            st.error("❌ No hay datos NASA cargados. Verifica la carpeta data/csv/")
        else:
            with st.spinner('🛰️ Analizando datos históricos de NASA GIOVANNI...'):
                # Crear instancia del buscador
                finder = DestinationFinder(processor)
                
                # Buscar destinos
                results = finder.find_destinations(
                    target_date=target_date,
                    climate_condition=selected_climate,
                    min_probability=min_probability
                )
            
            # Obtener info de la condición
            condition_info = finder.get_condition_info(selected_climate)
            
            # Mostrar header con la condición seleccionada
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {condition_info['color']}; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 15px;">{condition_info['icon']}</div>
                <h3 style="color: {condition_info['color']};">{condition_info['nombre']}</h3>
                <p style="color: rgba(255,255,255,0.8); margin-top: 10px;">
                    {condition_info['descripcion']}
                </p>
                <p style="color: rgba(255,255,255,0.6); margin-top: 15px; font-size: 0.9rem;">
                    📅 Fecha: <strong>{target_date.strftime('%d de %B, %Y')}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Mostrar resultados
            if len(results) == 0:
                st.warning(f"⚠️ No se encontraron destinos con probabilidad mayor a {min_probability}% para las condiciones seleccionadas.")
                st.info("💡 Intenta reducir la probabilidad mínima en las opciones avanzadas")
            else:
                st.success(f"✅ Se encontraron {len(results)} destino(s) que cumplen tus criterios")
                
                # Mostrar mapa si está habilitado
                if show_map:
                    st.markdown("#### 🗺️ Mapa de Destinos Recomendados")
                    render_destination_map(results, condition_info)
                    st.markdown("---")
                
                # Mostrar lista de destinos
                st.markdown("#### 🎯 Destinos Recomendados (ordenados por probabilidad)")
                
                for idx, result in enumerate(results[:max_results]):
                    city_info = result['city_info']
                    
                    # Determinar color según probabilidad
                    prob = result['overall_probability']
                    if prob >= 70:
                        prob_color = '#10B981'
                        prob_emoji = '🟢'
                    elif prob >= 40:
                        prob_color = '#F59E0B'
                        prob_emoji = '🟡'
                    else:
                        prob_color = '#EF4444'
                        prob_emoji = '🔴'
                    
                    # Card de destino
                    col_city, col_prob = st.columns([2, 1])
                    
                    with col_city:
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.05);
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 4px solid {city_info['color']};
                            margin: 10px 0;
                        ">
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <div style="font-size: 2rem; margin-right: 15px;">{city_info['icon']}</div>
                                <div>
                                    <h3 style="margin: 0; color: {city_info['color']};">
                                        #{idx+1} {result['city_name']}
                                    </h3>
                                    <p style="margin: 5px 0; color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                                        📍 {city_info['state']} | 🌐 {city_info['lat']}°, {city_info['lon']}°
                                    </p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_prob:
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.05);
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            border: 2px solid {prob_color};
                            margin: 10px 0;
                        ">
                            <div style="font-size: 2rem; margin-bottom: 5px;">{prob_emoji}</div>
                            <h2 style="margin: 0; color: {prob_color};">{prob:.2f}%</h2>
                            <p style="margin: 5px 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">
                                Probabilidad
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Mostrar detalles climáticos si está habilitado
                    if show_temps and result['average_values']:
                        with st.expander(f"📊 Ver detalles climáticos de {result['city_name']}"):
                            cols = st.columns(len(result['average_values']))
                            
                            for col_idx, (var_key, avg_val) in enumerate(result['average_values'].items()):
                                var_info = {
                                    'temperatura': {'icon': '🌡️', 'unit': '°C', 'color': '#EF4444'},
                                    'precipitacion': {'icon': '🌧️', 'unit': 'mm', 'color': '#3B82F6'},
                                    'viento': {'icon': '💨', 'unit': 'km/h', 'color': '#06B6D4'},
                                    'humedad': {'icon': '💧', 'unit': '%', 'color': '#8B5CF6'},
                                    'nubosidad': {'icon': '☁️', 'unit': '%', 'color': '#6B7280'}
                                }.get(var_key, {'icon': '📊', 'unit': '', 'color': '#6366f1'})
                                
                                with cols[col_idx]:
                                    st.metric(
                                        label=f"{var_info['icon']} {var_key.capitalize()}",
                                        value=f"{avg_val}{var_info['unit']}",
                                        delta=f"{result['probabilities'].get(var_key, 0)}% prob."
                                    )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
    
    else:
        # Vista inicial con información
        render_welcome_cards(processor)


def render_welcome_cards(processor):
    """Tarjetas de bienvenida con información"""
    st.markdown("### 🌍 Encuentra tu Destino Ideal por Clima")
    
    if processor and len(processor.data) > 0:
        st.markdown(f"""
        <p style="color: rgba(255,255,255,0.8); margin-bottom: 30px;">
            Analiza las <strong>{len(CIUDADES_NASA)} ciudades</strong> con datos NASA GIOVANNI y descubre 
            el destino perfecto según las condiciones climáticas que buscas.
            Basado en <strong>datos históricos reales</strong> de 1990-2024.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No hay datos NASA cargados")
        return
    
    # Obtener condiciones disponibles
    finder = DestinationFinder(processor)
    conditions = finder.get_all_conditions()
    
    # Mostrar tarjetas de condiciones
    rows = [list(conditions.items())[i:i+3] for i in range(0, len(conditions), 3)]
    
    for row in rows:
        cols = st.columns(3)
        for col_idx, (key, info) in enumerate(row):
            with cols[col_idx]:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid {info['color']};">
                    <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                        {info['icon']}
                    </div>
                    <h3 style="text-align: center; color: {info['color']};">
                        {info['nombre']}
                    </h3>
                    <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6; min-height: 80px;">
                        {info['descripcion']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información adicional
    st.markdown("""
    <div class="metric-card" style="text-align: center;">
        <h4 style="color: #00A6ED; margin-bottom: 15px;">💡 ¿Cómo funciona?</h4>
        <p style="color: rgba(255,255,255,0.9); line-height: 1.8;">
            El sistema analiza <strong>datos históricos de NASA GIOVANNI</strong> para calcular 
            la probabilidad de que un destino tenga las condiciones climáticas que buscas 
            en la fecha específica que selecciones.
            <br><br>
            Los resultados se basan en <strong>patrones climáticos reales de más de 30 años</strong>, 
            permitiéndote planear con confianza científica.
        </p>
    </div>
    """, unsafe_allow_html=True)

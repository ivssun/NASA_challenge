# components/sidebar.py
import streamlit as st
from datetime import datetime
from config.settings import MAP_CONFIG, VARIABLES, COLORS, CIUDADES_NASA

def render_sidebar():
    """
    Renderiza el sidebar con controles de configuración
    SINCRONIZADO con el mapa interactivo mediante session_state
    """
    
    # Header del sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="
            color: #00A6ED;
            font-family: 'Orbitron', sans-serif;
            margin: 0;
            text-shadow: 0 0 10px rgba(0, 166, 237, 0.5);
        ">
            🎯 Configuración
        </h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 5px;">
            Parámetros de búsqueda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # ============================================
    # SECCIÓN: UBICACIÓN
    # ============================================
    st.sidebar.markdown("""
    <h3 style="
        color: #6366f1;
        font-size: 1.1rem;
        margin-bottom: 15px;
    ">
        📍 Ubicación
    </h3>
    """, unsafe_allow_html=True)
    
    # Inicializar session_state si no existe
    if 'selected_city_key' not in st.session_state:
        st.session_state.selected_city_key = 'veracruz'
    
    # Preparar datos para el selector
    ciudad_keys = list(CIUDADES_NASA.keys())
    ciudad_options = {key: info['display_name'] for key, info in CIUDADES_NASA.items()}
    
    # Calcular índice actual basado en session_state
    try:
        current_index = ciudad_keys.index(st.session_state.selected_city_key)
    except (ValueError, KeyError):
        current_index = 0
        st.session_state.selected_city_key = ciudad_keys[0]
    
    # Selectbox sincronizado con session_state
    selected_from_sidebar = st.sidebar.selectbox(
        "Selecciona una ciudad",
        options=ciudad_keys,
        format_func=lambda x: ciudad_options[x],
        index=current_index,
        key='city_selector_widget',
        help="💡 También puedes seleccionar ciudades haciendo click en el mapa abajo"
    )
    
    # Si el usuario selecciona desde el sidebar, actualizar session_state
    if selected_from_sidebar != st.session_state.selected_city_key:
        st.session_state.selected_city_key = selected_from_sidebar
        st.rerun()
    
    # Obtener datos de la ciudad actual
    city_data = CIUDADES_NASA[st.session_state.selected_city_key]
    location_name = city_data['name']
    lat = city_data['lat']
    lon = city_data['lon']
    
    # Tarjeta de información de la ciudad
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(99, 102, 241, 0.2);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid {city_data['color']};
        margin: 15px 0;
    ">
        <div style="font-size: 2rem; text-align: center; margin-bottom: 10px;">
            {city_data['icon']}
        </div>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; text-align: center; margin: 0;">
            {city_data['description']}
        </p>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
            <small style="color: rgba(255,255,255,0.7);">
                📍 {city_data['state']}<br>
                🌐 {lat}°, {lon}°
            </small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tip sobre selección desde mapa
    st.sidebar.markdown("""
    <div style="
        background: rgba(0, 166, 237, 0.15);
        padding: 10px;
        border-radius: 8px;
        border-left: 3px solid #00A6ED;
        margin: 10px 0;
    ">
        <small style="color: rgba(255,255,255,0.8);">
            💡 <strong>Tip:</strong> Puedes seleccionar ciudades 
            haciendo click directamente en el mapa interactivo.
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECCIÓN: FECHA
    # ============================================
    st.sidebar.markdown("""
    <h3 style="
        color: #6366f1;
        font-size: 1.1rem;
        margin-bottom: 15px;
    ">
        📅 Fecha de Consulta
    </h3>
    """, unsafe_allow_html=True)
    
    selected_date = st.sidebar.date_input(
        "Selecciona la fecha",
        value=datetime(2024, 6, 15),
        help="Elige el día que quieres analizar"
    )
    
    # Día de la semana en español
    day_name_spanish = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    day_name = day_name_spanish[selected_date.weekday()]
    
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(99, 102, 241, 0.2);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    ">
        <small style="color: rgba(255,255,255,0.7);">Día seleccionado:</small><br>
        <strong style="color: #00A6ED;">{day_name}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================
    # SECCIÓN: VARIABLES CLIMÁTICAS
    # ============================================
    st.sidebar.markdown("""
    <h3 style="
        color: #6366f1;
        font-size: 1.1rem;
        margin-bottom: 15px;
    ">
        🌡️ Variables a Analizar
    </h3>
    """, unsafe_allow_html=True)
    
    selected_vars = {}
    default_vars = ['temperatura', 'precipitacion']
    
    for var_key, var_info in VARIABLES.items():
        if var_key in ['temperatura', 'precipitacion']:
            selected_vars[var_key] = st.sidebar.checkbox(
                var_info['nombre'],
                value=(var_key in default_vars),
                help=f"{var_info['descripcion']} (Unidad: {var_info['unidad']})"
            )
            
            if selected_vars[var_key]:
                st.sidebar.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.05);
                    padding: 5px 10px;
                    border-radius: 5px;
                    border-left: 3px solid {var_info['color']};
                    margin: 5px 0 10px 20px;
                    font-size: 0.8rem;
                ">
                    <small style="color: rgba(255,255,255,0.6);">
                        Umbral extremo: <strong style="color: {var_info['color']};">
                        {var_info['threshold_extreme']} {var_info['unidad']}
                        </strong>
                    </small>
                </div>
                """, unsafe_allow_html=True)
        else:
            selected_vars[var_key] = False
    
    st.sidebar.markdown("---")
    
    # ============================================
    # BOTÓN DE CONSULTA
    # ============================================
    consultar = st.sidebar.button(
        "🔍 Consultar Datos NASA",
        use_container_width=True,
        type="primary",
        help="Obtén las probabilidades climáticas basadas en datos históricos"
    )
    
    if consultar:
        st.sidebar.markdown("""
        <div style="
            text-align: center;
            padding: 10px;
            background: linear-gradient(90deg, #6366f1, #00A6ED);
            border-radius: 10px;
            margin-top: 10px;
        ">
            <small style="color: white;">🛰️ Consultando satélites...</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # ============================================
    # INFORMACIÓN
    # ============================================
    st.sidebar.markdown("""
    <div style="
        background: rgba(99, 102, 241, 0.15);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid #6366f1;
    ">
        <h4 style="color: #00A6ED; margin-top: 0; font-size: 0.95rem;">
            💡 Datos Disponibles
        </h4>
        <ul style="
            color: rgba(255,255,255,0.8);
            font-size: 0.85rem;
            line-height: 1.6;
            padding-left: 20px;
        ">
            <li>🌡️ Temperatura (MERRA-2)</li>
            <li>🌧️ Precipitación (GPM)</li>
            <li>📅 Período: 1990-2024</li>
            <li>📊 ~320 registros mensuales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Contador de variables
    num_selected = sum(selected_vars.values())
    st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <small style="color: rgba(255,255,255,0.6);">
            Variables seleccionadas: <strong style="color: #00A6ED;">{num_selected}/2</strong>
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # RETORNAR DATOS
    # ============================================
    return {
        'location_name': location_name,
        'lat': lat,
        'lon': lon,
        'date': selected_date,
        'variables': selected_vars,
        'consultar': consultar,
        'city_key': st.session_state.selected_city_key,
        'city_data': city_data
    }
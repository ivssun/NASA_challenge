# components/sidebar.py
import streamlit as st
from datetime import datetime
from config.settings import MAP_CONFIG, VARIABLES, COLORS

def render_sidebar():
    """
    Renderiza el sidebar con controles de configuración
    Diseño espacial NASA elegante
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
    
    location_name = st.sidebar.text_input(
        "Nombre del lugar",
        value=MAP_CONFIG['default_location'],
        help="Escribe el nombre de la ciudad o ubicación",
        placeholder="Ej: Guadalajara, Cancún..."
    )
    
    # Coordenadas en columnas
    col1, col2 = st.sidebar.columns(2)
    with col1:
        lat = st.number_input(
            "Latitud",
            value=MAP_CONFIG['default_lat'],
            format="%.6f",
            help="Coordenada de latitud (-90 a 90)",
            step=0.01
        )
    with col2:
        lon = st.number_input(
            "Longitud",
            value=MAP_CONFIG['default_lon'],
            format="%.6f",
            help="Coordenada de longitud (-180 a 180)",
            step=0.01
        )
    
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
    
    # Mostrar día de la semana
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
    
    # Variables principales (seleccionadas por defecto)
    default_vars = ['temperatura', 'precipitacion', 'viento', 'humedad']
    
    for var_key, var_info in VARIABLES.items():
        # Checkbox con icono
        selected_vars[var_key] = st.sidebar.checkbox(
            var_info['nombre'],
            value=(var_key in default_vars),
            help=f"{var_info['descripcion']} (Unidad: {var_info['unidad']})"
        )
        
        # Si está seleccionado, mostrar umbral
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
    
    # Animación cuando se presiona
    if consultar:
        st.sidebar.markdown("""
        <div style="
            text-align: center;
            padding: 10px;
            background: linear-gradient(90deg, #6366f1, #00A6ED);
            border-radius: 10px;
            margin-top: 10px;
            animation: pulse 1s ease-in-out;
        ">
            <small style="color: white;">🛰️ Consultando satélites...</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # ============================================
    # INFORMACIÓN Y TIPS
    # ============================================
    st.sidebar.markdown("""
    <div style="
        background: rgba(99, 102, 241, 0.15);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid #6366f1;
    ">
        <h4 style="color: #00A6ED; margin-top: 0; font-size: 0.95rem;">
            💡 Tips de Uso
        </h4>
        <ul style="
            color: rgba(255,255,255,0.8);
            font-size: 0.85rem;
            line-height: 1.6;
            padding-left: 20px;
        ">
            <li>Ajusta las coordenadas para ubicaciones precisas</li>
            <li>Selecciona múltiples variables para análisis completo</li>
            <li>Los datos provienen de satélites NASA</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Contador de variables seleccionadas
    num_selected = sum(selected_vars.values())
    st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <small style="color: rgba(255,255,255,0.6);">
            Variables seleccionadas: <strong style="color: #00A6ED;">{num_selected}/5</strong>
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
        'consultar': consultar
    }
# components/climate_finder.py
import streamlit as st
from datetime import datetime, timedelta
from config.settings import MEXICAN_CLIMATE_ZONES, COLORS
from styles.custom_styles import get_climate_badge

def render_climate_finder():
    """
    Componente principal del buscador de destinos por clima deseado
    Versión sin datos simulados - Solo interfaz lista para backend
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
        
        climate_options = {
            'nevado': '🏔️ Nevado (ideal para nieve)',
            'frio_seco': '❄️ Frío Seco (aire fresco)',
            'templado': '🌤️ Templado (clima agradable)',
            'caluroso_seco': '🌵 Caluroso Seco (desierto)',
            'caluroso_humedo': '🏖️ Caluroso Húmedo (playa)'
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
                0, 100, 15,
                help="Filtra destinos con probabilidad menor a este valor"
            )
        
        with col_results:
            max_results = st.slider(
                "Máximo de resultados",
                3, 15, 10,
                help="Número máximo de destinos a mostrar"
            )
        
        show_map = st.checkbox("Mostrar mapa interactivo", value=True)
        show_temps = st.checkbox("Mostrar temperaturas esperadas", value=True)
    
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
        with st.spinner('🛰️ Analizando datos históricos de NASA GIOVANNI...'):
            import time
            time.sleep(1.5)  # Simulación de carga
        
        # Mostrar mensaje de backend en desarrollo
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #F59E0B; text-align: center; padding: 40px;">
            <h3 style="color: #F59E0B; margin-bottom: 20px;">⚙️ Backend en Desarrollo</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; line-height: 1.8;">
                Esta funcionalidad está lista para ser conectada con los datos reales de NASA GIOVANNI.
            </p>
            <br>
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h4 style="color: #00A6ED; margin-bottom: 15px;">📋 Parámetros de tu búsqueda:</h4>
                <p style="color: white; margin: 10px 0;">
                    <strong>📅 Fecha seleccionada:</strong> {target_date.strftime('%d de %B, %Y')}
                </p>
                <p style="color: white; margin: 10px 0;">
                    <strong>❄️ Clima deseado:</strong> {climate_options[selected_climate]}
                </p>
                <p style="color: white; margin: 10px 0;">
                    <strong>📊 Probabilidad mínima:</strong> {min_probability}%
                </p>
            </div>
            <br>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.95rem; margin-top: 20px;">
                Cuando se integre el backend, aquí se mostrarán:<br>
                • Lista de destinos ordenados por probabilidad<br>
                • Mapa interactivo con ubicaciones<br>
                • Gráficos comparativos de temperatura y probabilidad
            </p>
        </div>
        """.format(
            target_date=target_date,
            climate_options=climate_options,
            selected_climate=selected_climate,
            min_probability=min_probability
        ), unsafe_allow_html=True)
        
        # Mostrar zona climática seleccionada
        st.markdown("<br>", unsafe_allow_html=True)
        zone_info = MEXICAN_CLIMATE_ZONES[selected_climate]
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            {get_climate_badge(selected_climate, size='large')}
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar ciudades disponibles para ese clima
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #6366f1; margin-bottom: 15px;">
                🗺️ Ciudades disponibles en {zone_info['nombre']}:
            </h4>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 15px;">
                {zone_info['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Listar ciudades de esa zona climática
        cities_cols = st.columns(2)
        for idx, city in enumerate(zone_info['cities']):
            col_idx = idx % 2
            with cities_cols[col_idx]:
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    border-left: 3px solid {zone_info['color']};
                ">
                    <h4 style="margin: 0; color: white;">{city['name']}</h4>
                    <p style="color: rgba(255,255,255,0.7); margin: 5px 0; font-size: 0.9rem;">
                        📍 {city['state']}<br>
                        🏔️ Altitud: {city['alt']}m<br>
                        🌡️ Rango temp: {city.get('temp_range', ('N/A', 'N/A'))[0]}°C - {city.get('temp_range', ('N/A', 'N/A'))[1]}°C
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Vista inicial con información
        render_welcome_cards()


def render_welcome_cards():
    """Tarjetas de bienvenida con información de cada tipo de clima"""
    st.markdown("### 🌍 Explora los Climas de México")
    st.markdown("""
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 30px;">
        Selecciona el tipo de clima que buscas para tus próximas vacaciones y 
        descubre los mejores destinos basados en datos históricos de NASA.
    </p>
    """, unsafe_allow_html=True)
    
    # Primera fila: Nevado, Frío Seco, Templado
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {MEXICAN_CLIMATE_ZONES['nevado']['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {MEXICAN_CLIMATE_ZONES['nevado']['emoji']}
            </div>
            <h3 style="text-align: center; color: {MEXICAN_CLIMATE_ZONES['nevado']['color']};">
                Clima Nevado
            </h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6;">
                Perfecto para esquí, snowboard y paisajes invernales. 
                Temperaturas bajo cero y posibilidad de nieve.
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <small style="color: rgba(255,255,255,0.6);">
                    🏔️ {len(MEXICAN_CLIMATE_ZONES['nevado']['cities'])} destinos disponibles
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {MEXICAN_CLIMATE_ZONES['frio_seco']['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {MEXICAN_CLIMATE_ZONES['frio_seco']['emoji']}
            </div>
            <h3 style="text-align: center; color: {MEXICAN_CLIMATE_ZONES['frio_seco']['color']};">
                Clima Frío Seco
            </h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6;">
                Aire fresco y cielos despejados. Ideal para senderismo, 
                exploración de pueblos mágicos y turismo cultural.
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <small style="color: rgba(255,255,255,0.6);">
                    ❄️ {len(MEXICAN_CLIMATE_ZONES['frio_seco']['cities'])} destinos disponibles
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {MEXICAN_CLIMATE_ZONES['templado']['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {MEXICAN_CLIMATE_ZONES['templado']['emoji']}
            </div>
            <h3 style="text-align: center; color: {MEXICAN_CLIMATE_ZONES['templado']['color']};">
                Clima Templado
            </h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6;">
                Temperatura perfecta todo el año. Perfecto para turismo, 
                caminatas y actividades al aire libre sin extremos.
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <small style="color: rgba(255,255,255,0.6);">
                    🌤️ {len(MEXICAN_CLIMATE_ZONES['templado']['cities'])} destinos disponibles
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Segunda fila: Caluroso Seco, Caluroso Húmedo
    col4, col5, col_empty = st.columns(3)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {MEXICAN_CLIMATE_ZONES['caluroso_seco']['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {MEXICAN_CLIMATE_ZONES['caluroso_seco']['emoji']}
            </div>
            <h3 style="text-align: center; color: {MEXICAN_CLIMATE_ZONES['caluroso_seco']['color']};">
                Clima Caluroso Seco
            </h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6;">
                Desiertos y altas temperaturas con baja humedad. 
                Paisajes únicos y noches estrelladas espectaculares.
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <small style="color: rgba(255,255,255,0.6);">
                    🌵 {len(MEXICAN_CLIMATE_ZONES['caluroso_seco']['cities'])} destinos disponibles
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {MEXICAN_CLIMATE_ZONES['caluroso_humedo']['color']};">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 15px;">
                {MEXICAN_CLIMATE_ZONES['caluroso_humedo']['emoji']}
            </div>
            <h3 style="text-align: center; color: {MEXICAN_CLIMATE_ZONES['caluroso_humedo']['color']};">
                Clima Caluroso Húmedo
            </h3>
            <p style="color: rgba(255,255,255,0.8); text-align: center; line-height: 1.6;">
                Playas paradisíacas y clima tropical. Perfecto para 
                sol, playa, buceo y deportes acuáticos.
            </p>
            <div style="text-align: center; margin-top: 15px;">
                <small style="color: rgba(255,255,255,0.6);">
                    🏖️ {len(MEXICAN_CLIMATE_ZONES['caluroso_humedo']['cities'])} destinos disponibles
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_empty:
        pass
    
    st.markdown("---")
    
    # Información adicional
    st.markdown("""
    <div class="metric-card" style="text-align: center;">
        <h4 style="color: #00A6ED; margin-bottom: 15px;">💡 ¿Cómo funcionará?</h4>
        <p style="color: rgba(255,255,255,0.9); line-height: 1.8;">
            Cuando se conecte el backend con datos de NASA GIOVANNI, el sistema analizará 
            <strong>más de 20 años de datos históricos</strong> para calcular la probabilidad 
            de que un destino tenga las condiciones climáticas que buscas en la fecha específica que selecciones. 
            <br><br>
            Los resultados se basarán en patrones climáticos reales, lo que te permitirá 
            planear con <strong>meses de anticipación</strong> con confianza científica.
        </p>
    </div>
    """, unsafe_allow_html=True)
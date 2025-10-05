# components/metricas.py
import streamlit as st

def get_temperature_category(temp):
    """Categoriza la temperatura"""
    if temp < 10:
        return "Frío", "#60A5FA"
    elif temp < 18:
        return "Fresco", "#A5B4FC"
    elif temp < 25:
        return "Templado", "#34D399"
    elif temp < 30:
        return "Cálido", "#FBBF24"
    else:
        return "Caluroso", "#F87171"

def get_precipitation_category(precip):
    """Categoriza la precipitación"""
    if precip < 10:
        return "Muy seco", "#FBBF24"
    elif precip < 50:
        return "Seco", "#34D399"
    elif precip < 100:
        return "Moderado", "#60A5FA"
    elif precip < 200:
        return "Lluvioso", "#A5B4FC"
    else:
        return "Muy lluvioso", "#8B5CF6"

def get_risk_level(probability):
    """Determina el nivel de riesgo basado en probabilidad"""
    if probability < 0.1:
        return "Muy bajo", "#34D399"
    elif probability < 0.3:
        return "Bajo", "#FBBF24"
    elif probability < 0.6:
        return "Moderado", "#F59E0B"
    else:
        return "Alto", "#EF4444"

def render_metric_cards(data):
    """Renderiza tarjetas de métricas con categorías claras"""
    
    cols = st.columns(len(data))
    
    for idx, (var_key, var_data) in enumerate(data.items()):
        with cols[idx]:
            value = var_data['value']
            probability = var_data['probability']
            
            # Obtener categoría y color según la variable
            if var_key == 'temperatura':
                category, cat_color = get_temperature_category(value)
                icon = "🌡️"
                label = "Temperatura"
                unit = "°C"
                extreme_type = "calor extremo (>35°C)"
            elif var_key == 'precipitacion':
                category, cat_color = get_precipitation_category(value)
                icon = "🌧️"
                label = "Precipitación"
                unit = "mm"
                extreme_type = "lluvia intensa (>50mm)"
            else:
                category = "N/A"
                cat_color = "#6B7280"
                icon = "📊"
                label = var_key.capitalize()
                unit = ""
                extreme_type = "condición extrema"
            
            # Obtener nivel de riesgo
            risk_level, risk_color = get_risk_level(probability)
            
            # Renderizar tarjeta
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                padding: 20px;
                border-radius: 15px;
                border-left: 4px solid {cat_color};
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <h4 style="margin: 0; color: white; font-size: 1rem;">{label}</h4>
                <h2 style="margin: 10px 0; color: {cat_color}; font-size: 2.5rem; font-weight: 700;">
                    {value}{unit}
                </h2>
                <p style="
                    margin: 5px 0;
                    padding: 5px 10px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 5px;
                    color: {cat_color};
                    font-weight: 600;
                    font-size: 0.9rem;
                ">
                    {category}
                </p>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <p style="margin: 0; font-size: 0.85rem; color: rgba(255,255,255,0.7);">
                        Riesgo de {extreme_type}:
                    </p>
                    <p style="margin: 5px 0 0 0; color: {risk_color}; font-weight: 600; font-size: 1rem;">
                        {risk_level}
                    </p>
                    <p style="margin: 5px 0 0 0; font-size: 0.75rem; color: rgba(255,255,255,0.5);">
                        ({probability*100:.1f}% de ocurrencia histórica)
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_info_card(title, content, icon="📊"):
    st.markdown(f"""
    <div style='
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    '>
        <h3>{icon} {title}</h3>
        <div style='color: #666;'>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def get_probability_color(probability):
    if probability >= 0.7:
        return "#dc3545"
    elif probability >= 0.4:
        return "#ffc107"
    else:
        return "#28a745"


# ============================================
# VERSIÓN CORREGIDA DE PRECIPITACIÓN
# ============================================
def render_precipitation_card(analysis):
    """
    Tarjeta para precipitación DIARIA
    VERSIÓN CORREGIDA: Mezcla HTML simple + componentes Streamlit
    """
    
    prob = analysis['probability_rain_day']
    avg_mm = analysis['avg_mm_per_rainy_day']
    
    # Determinar color e icono
    if prob < 20:
        color = "#10B981"
        icon = "☀️"
        risk = "Muy bajo"
    elif prob < 50:
        color = "#F59E0B"
        icon = "⛅"
        risk = "Moderado"
    else:
        color = "#3B82F6"
        icon = "🌧️"
        risk = "Alto"
    
    # Header con icono y probabilidad
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid {color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    ">
        <div style="text-align: center; font-size: 3.5rem; margin-bottom: 15px;">
            {icon}
        </div>
        <h3 style="text-align: center; color: {color}; margin: 0;">
            {prob:.2f}% de Probabilidad de Lluvia
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales usando st.columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💧 Si llueve caerán",
            f"{avg_mm} mm",
            help="Milímetros esperados ese día"
        )
    
    with col2:
        st.metric(
            "📊 Intensidad",
            analysis['intensity_category'],
            help="Clasificación de la lluvia"
        )
    
    with col3:
        st.metric(
            "🌧️ Días lluviosos típicos",
            f"{analysis['expected_rainy_days_per_month']}",
            delta=f"de {analysis['total_days_in_month']} días",
            help="Cuántos días llueve en este mes"
        )
    
    # Información adicional
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    ">
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📈 <strong>Rango típico:</strong> {analysis['range_mm_per_day'][0]}-{analysis['range_mm_per_day'][1]} mm por día lluvioso
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📊 <strong>Años analizados:</strong> {analysis['historical_years_analyzed']} años de datos NASA
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            ⚠️ <strong>Nivel de riesgo:</strong> <span style="color: {color}; font-weight: 600;">{risk}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensaje descriptivo en info box
    st.info(f"**💬 Recomendación:** {analysis['message']}")

def render_wind_card(analysis):
    """
    Tarjeta especializada para viento
    """
    
    avg_wind = analysis['avg_wind_speed']
    category = analysis['wind_category']
    risk_level, risk_color = analysis['risk_level']
    
    # Icono según intensidad
    if avg_wind < 10:
        icon = "🍃"
        color = "#10B981"
    elif avg_wind < 20:
        icon = "🌤️"
        color = "#3B82F6"
    elif avg_wind < 40:
        icon = "💨"
        color = "#F59E0B"
    else:
        icon = "⚠️"
        color = "#EF4444"
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid {color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    ">
        <div style="text-align: center; font-size: 3.5rem; margin-bottom: 15px;">
            {icon}
        </div>
        <h3 style="text-align: center; color: {color}; margin: 0;">
            {avg_wind} km/h - {category}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💨 Velocidad promedio",
            f"{avg_wind} km/h",
            help="Velocidad típica del viento"
        )
    
    with col2:
        st.metric(
            "📊 Máximo esperado (P90)",
            f"{analysis['p90_wind']} km/h",
            help="El 90% del tiempo no superará esta velocidad"
        )
    
    with col3:
        st.metric(
            "⚠️ Viento fuerte",
            f"{analysis['prob_strong_wind']}%",
            help="Probabilidad de viento >40 km/h"
        )
    
    # Detalles
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    ">
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📈 <strong>Rango histórico:</strong> {analysis['min_wind_speed']}-{analysis['max_wind_speed']} km/h
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📊 <strong>Años analizados:</strong> {analysis['historical_years']}
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            ⚠️ <strong>Nivel de riesgo:</strong> <span style="color: {risk_color}; font-weight: 600;">{risk_level}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensaje
    st.info(f"**💬 Recomendación:** {analysis['message']}")


def render_humidity_card(analysis):
    """Tarjeta especializada para humedad"""
    
    avg_humidity = analysis['avg_humidity']
    category = analysis['humidity_category']
    comfort_level, comfort_color = analysis['comfort_level']
    
    # Icono según nivel
    if avg_humidity < 30:
        icon = "🏜️"
        color = "#F59E0B"
    elif avg_humidity < 70:
        icon = "💧"
        color = "#10B981"
    else:
        icon = "💦"
        color = "#3B82F6"
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid {color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    ">
        <div style="text-align: center; font-size: 3.5rem; margin-bottom: 15px;">
            {icon}
        </div>
        <h3 style="text-align: center; color: {color}; margin: 0;">
            {avg_humidity}% - {category}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💧 Humedad promedio",
            f"{avg_humidity}%",
            help="Humedad relativa típica"
        )
    
    with col2:
        st.metric(
            "📊 Rango histórico",
            f"{analysis['min_humidity']}-{analysis['max_humidity']}%",
            help="Mínimo y máximo registrado"
        )
    
    with col3:
        st.metric(
            "😊 Nivel de confort",
            comfort_level,
            help="Confort según la humedad"
        )
    
    # Detalles
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    ">
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📈 <strong>P90:</strong> {analysis['p90_humidity']}% (90% del tiempo por debajo)
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📊 <strong>Años analizados:</strong> {analysis['historical_years']}
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            😊 <strong>Confort:</strong> <span style="color: {comfort_color}; font-weight: 600;">{comfort_level}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"**💬 Recomendación:** {analysis['message']}")


# ============================================
# TARJETA DE NUBOSIDAD
# ============================================
def render_cloudiness_card(analysis):
    """Tarjeta especializada para nubosidad"""
    
    avg_cloud = analysis['avg_cloudiness']
    category = analysis['cloudiness_category']
    sky_condition, sky_color = analysis['sky_condition']
    
    # Icono según cobertura
    if avg_cloud < 25:
        icon = "☀️"
        color = "#F59E0B"
    elif avg_cloud < 50:
        icon = "⛅"
        color = "#10B981"
    elif avg_cloud < 75:
        icon = "☁️"
        color = "#3B82F6"
    else:
        icon = "🌥️"
        color = "#6B7280"
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid {color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    ">
        <div style="text-align: center; font-size: 3.5rem; margin-bottom: 15px;">
            {icon}
        </div>
        <h3 style="text-align: center; color: {color}; margin: 0;">
            {avg_cloud}% - {category}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "☁️ Cobertura promedio",
            f"{avg_cloud}%",
            help="Porcentaje de cielo cubierto"
        )
    
    with col2:
        st.metric(
            "☀️ Prob. cielo despejado",
            f"{analysis['prob_clear_sky']}%",
            help="Probabilidad de cielo despejado (<25% nubes)"
        )
    
    with col3:
        st.metric(
            "🌥️ Prob. nublado",
            f"{analysis['prob_overcast']}%",
            help="Probabilidad de cielo nublado (>75% nubes)"
        )
    
    # Detalles
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    ">
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📈 <strong>Rango histórico:</strong> {analysis['min_cloudiness']}-{analysis['max_cloudiness']}%
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            📊 <strong>Años analizados:</strong> {analysis['historical_years']}
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.95rem;">
            🌤️ <strong>Condición del cielo:</strong> <span style="color: {sky_color}; font-weight: 600;">{sky_condition}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"**💬 Recomendación:** {analysis['message']}")
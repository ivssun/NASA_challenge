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
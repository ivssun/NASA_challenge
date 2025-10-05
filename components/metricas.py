import streamlit as st

def render_metric_cards(data):
    col1, col2, col3, col4 = st.columns(4)
    
    if 'temperatura' in data:
        with col1:
            temp_data = data['temperatura']
            st.metric(
                label="🌡️ Temp. Extrema",
                value=f"{temp_data['value']}°C",
                delta=f"+{temp_data['delta']}°C",
                help="Probabilidad de temperatura > 32°C"
            )
            st.progress(temp_data['probability'])
            st.caption(f"{int(temp_data['probability']*100)}% de probabilidad")
    
    if 'precipitacion' in data:
        with col2:
            precip_data = data['precipitacion']
            st.metric(
                label="🌧️ Lluvia Intensa",
                value=f"{precip_data['value']}mm",
                delta=f"+{precip_data['delta']}mm",
                help="Probabilidad de precipitación > 30mm"
            )
            st.progress(precip_data['probability'])
            st.caption(f"{int(precip_data['probability']*100)}% de probabilidad")
    
    if 'viento' in data:
        with col3:
            wind_data = data['viento']
            st.metric(
                label="💨 Viento Fuerte",
                value=f"{wind_data['value']} km/h",
                delta=f"+{wind_data['delta']} km/h",
                help="Probabilidad de viento > 35 km/h"
            )
            st.progress(wind_data['probability'])
            st.caption(f"{int(wind_data['probability']*100)}% de probabilidad")
    
    if 'humedad' in data:
        with col4:
            humidity_data = data['humedad']
            st.metric(
                label="💧 Humedad Alta",
                value=f"{humidity_data['value']}%",
                delta=f"+{humidity_data['delta']}%",
                help="Probabilidad de humedad > 75%"
            )
            st.progress(humidity_data['probability'])
            st.caption(f"{int(humidity_data['probability']*100)}% de probabilidad")


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
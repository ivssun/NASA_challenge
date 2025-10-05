import streamlit as st
import pandas as pd
import json

def render_download_buttons(data, filename_prefix="clima"):
    st.subheader("💾 Descargar Datos")
    
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data
    
    col_csv, col_json = st.columns(2)
    
    with col_csv:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Descarga los datos en formato CSV (Excel)"
        )
    
    with col_json:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Descargar JSON",
            data=json_data,
            file_name=f"{filename_prefix}.json",
            mime="application/json",
            use_container_width=True,
            help="Descarga los datos en formato JSON"
        )


def create_summary_report(location_data, probability_data):
    report = f"""
    ========================================
    REPORTE CLIMÁTICO - NASA DASHBOARD
    ========================================
    
    📍 UBICACIÓN:
    Lugar: {location_data['name']}
    Latitud: {location_data['lat']}°
    Longitud: {location_data['lon']}°
    
    📅 FECHA CONSULTADA:
    {location_data['date']}
    
    📊 PROBABILIDADES DE CONDICIONES EXTREMAS:
    """
    
    for condition, prob in probability_data.items():
        report += f"\n    • {condition}: {prob*100:.1f}%"
    
    report += "\n\n    ========================================\n"
    report += "    Generado por NASA Space Apps Challenge\n"
    report += "    ========================================\n"
    
    return report
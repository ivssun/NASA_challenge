# components/mapa.py
import folium
from streamlit_folium import st_folium, folium_static
from folium import plugins
from config.settings import MAP_CONFIG, CIUDADES_NASA
import streamlit as st

def render_map(lat, lon, location_name):
    """
    Renderiza mapa principal con diseño mejorado
    """
    # Crear mapa base con estilo oscuro
    m = folium.Map(
        location=[lat, lon],
        zoom_start=MAP_CONFIG['default_zoom'],
        tiles=None
    )
    
    # Agregar capa de mapa oscuro
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO',
        name='Dark Matter',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Marcador principal
    folium.Marker(
        [lat, lon],
        popup=f"📍 {location_name}",
        tooltip=f"<b>{location_name}</b>",
        icon=folium.Icon(
            color="red",
            icon="satellite",
            prefix='fa',
            icon_color='white'
        )
    ).add_to(m)
    
    # Círculo de área
    folium.Circle(
        [lat, lon],
        radius=5000,
        color='#6366f1',
        fill=True,
        fillColor='#00A6ED',
        fillOpacity=0.15,
        weight=2
    ).add_to(m)
    
    # Controles
    plugins.Fullscreen(
        position='topright',
        title='Pantalla completa',
        title_cancel='Salir',
        force_separate_button=True
    ).add_to(m)
    
    folium_static(m, width=None, height=450)


def render_interactive_cities_map(selected_city_key=None):
    """
    🗺️ Mapa interactivo con SINCRONIZACIÓN PERFECTA
    Retorna la ciudad clickeada (city_key) o None
    """
    # Centro de México
    center_lat = 23.6345
    center_lon = -102.5528
    
    # Crear mapa base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO',
        zoom_control=True,
        scrollWheelZoom=True,
        dragging=True,
        doubleClickZoom=False
    )
    
    # Agregar marcadores clickeables para cada ciudad
    for city_key, city_info in CIUDADES_NASA.items():
        is_selected = (city_key == selected_city_key)
        
        # Configuración visual según si está seleccionada
        if is_selected:
            marker_color = city_info['color']
            radius = 22
            opacity = 1.0
            fill_opacity = 0.95
            weight = 6
            icon_html = f"""
                <div style="
                    background: {city_info['color']};
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    border: 3px solid white;
                    box-shadow: 0 0 15px rgba(0,166,237,0.8);
                    cursor: pointer;
                ">
                    {city_info['icon']}
                </div>
            """
        else:
            marker_color = '#6366f1'
            radius = 16
            opacity = 0.8
            fill_opacity = 0.6
            weight = 3
            icon_html = f"""
                <div style="
                    background: {marker_color};
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    border: 2px solid white;
                    cursor: pointer;
                ">
                    {city_info['icon']}
                </div>
            """
        
        # Popup con información de la ciudad
        popup_html = f"""
        <div style="
            font-family: Arial, sans-serif;
            padding: 12px;
            min-width: 180px;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 8px;">{city_info['icon']}</div>
            <h3 style="
                margin: 0 0 8px 0;
                color: {city_info['color']};
                font-size: 1.2rem;
            ">
                {city_info['name']}
            </h3>
            <p style="
                margin: 0 0 10px 0;
                font-size: 0.85rem;
                color: #666;
                line-height: 1.4;
            ">
                📍 {city_info['state']}<br>
                🌐 {city_info['lat']}°, {city_info['lon']}°
            </p>
            {'<div style="background: ' + city_info['color'] + '22; padding: 8px; border-radius: 5px; margin-top: 8px;"><strong style="color: ' + city_info['color'] + ';">⭐ CIUDAD SELECCIONADA</strong></div>' if is_selected else '<div style="background: #f0f0f0; padding: 6px; border-radius: 5px; margin-top: 8px;"><small style="color: #666;">🖱️ Click para seleccionar</small></div>'}
        </div>
        """
        
        # Tooltip simple
        tooltip_text = f"<b>{city_info['icon']} {city_info['name']}</b>"
        if is_selected:
            tooltip_text = f"⭐ {tooltip_text} ⭐"
        
        # Crear marcador usando DivIcon para mejor control
        folium.Marker(
            location=[city_info['lat'], city_info['lon']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=folium.Tooltip(tooltip_text, permanent=False),
            icon=folium.DivIcon(html=icon_html)
        ).add_to(m)
        
        # Agregar círculo de área solo para la ciudad seleccionada
        if is_selected:
            folium.Circle(
                [city_info['lat'], city_info['lon']],
                radius=35000,  # 35km de radio
                color=city_info['color'],
                fill=True,
                fillColor=city_info['color'],
                fillOpacity=0.1,
                weight=2,
                dashArray='5, 5'
            ).add_to(m)
    
    # Leyenda mejorada
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 40px;
        left: 25px;
        background: rgba(30, 27, 75, 0.95);
        backdrop-filter: blur(12px);
        padding: 15px 20px;
        border-radius: 12px;
        border: 2px solid rgba(99, 102, 241, 0.5);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        z-index: 1000;
        font-family: Arial, sans-serif;
    ">
        <div style="
            color: #00A6ED;
            font-weight: 700;
            margin-bottom: 12px;
            font-size: 1rem;
            text-shadow: 0 0 8px rgba(0,166,237,0.5);
        ">
            🛰️ Ciudades NASA GIOVANNI
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <span style="
                width: 16px;
                height: 16px;
                background: #6366f1;
                border-radius: 50%;
                margin-right: 10px;
                display: inline-block;
                border: 2px solid white;
            "></span>
            <span style="color: rgba(255,255,255,0.85); font-size: 0.85rem;">
                Ciudad disponible (click para seleccionar)
            </span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <span style="
                width: 20px;
                height: 20px;
                background: #00A6ED;
                border-radius: 50%;
                margin-right: 10px;
                display: inline-block;
                border: 3px solid white;
                box-shadow: 0 0 12px rgba(0, 166, 237, 0.8);
            "></span>
            <span style="
                color: #00A6ED;
                font-size: 0.85rem;
                font-weight: 600;
            ">
                Ciudad seleccionada
            </span>
        </div>
        <div style="
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.2);
        ">
            <small style="color: rgba(255,255,255,0.6); font-size: 0.75rem;">
                💡 Haz click en cualquier ciudad<br>
                para ver sus datos climáticos
            </small>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Agregar control de pantalla completa
    plugins.Fullscreen(
        position='topright',
        title='Pantalla completa',
        title_cancel='Salir',
        force_separate_button=True
    ).add_to(m)
    
    # 🔥 CAPTURAR CLICKS - KEY FIJO para evitar resets
    map_data = st_folium(
        m,
        width=None,
        height=500,
        returned_objects=["last_object_clicked", "last_clicked"],
        key="nasa_interactive_map"  # ✅ KEY FIJO - no cambia
    )
    
    # 🎯 DETECTAR QUÉ CIUDAD FUE CLICKEADA
    clicked_city_key = None
    
    if map_data and map_data.get("last_object_clicked"):
        clicked_coords = map_data["last_object_clicked"]
        
        if clicked_coords and "lat" in clicked_coords and "lng" in clicked_coords:
            clicked_lat = clicked_coords["lat"]
            clicked_lon = clicked_coords["lng"]
            
            # Buscar ciudad más cercana al click (tolerancia de 0.5 grados)
            min_distance = float('inf')
            
            for city_key, city_info in CIUDADES_NASA.items():
                # Calcular distancia euclidiana simple
                distance = ((city_info['lat'] - clicked_lat) ** 2 + 
                           (city_info['lon'] - clicked_lon) ** 2) ** 0.5
                
                if distance < min_distance and distance < 0.5:  # Tolerancia de 0.5 grados
                    min_distance = distance
                    clicked_city_key = city_key
    
    return clicked_city_key


def render_mini_map(lat, lon, zoom=8):
    """
    Renderiza un mapa pequeño para vistas compactas
    """
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO',
        dragging=False,
        scrollWheelZoom=False,
        doubleClickZoom=False,
        boxZoom=False,
        keyboard=False,
        zoomControl=False
    )
    
    folium.CircleMarker(
        [lat, lon],
        radius=8,
        color='#6366f1',
        fill=True,
        fillColor='#00A6ED',
        fillOpacity=0.8,
        weight=2
    ).add_to(m)
    
    folium_static(m, width=300, height=200)


def render_climate_zone_map(cities_data, highlight_city=None):
    """
    Renderiza un mapa con múltiples ciudades marcadas
    """
    center_lat = 23.6345
    center_lon = -102.5528
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO'
    )
    
    for city in cities_data:
        if highlight_city and city.get('name') == highlight_city:
            marker_color = 'red'
            radius = 15
        else:
            marker_color = 'blue'
            radius = 10
        
        popup_html = f"""
        <div style="font-family: Arial; padding: 5px;">
            <h4 style="margin: 0; color: #0B3D91;">{city.get('name', 'Unknown')}</h4>
            <p style="margin: 5px 0;">
                <b>Estado:</b> {city.get('state', 'N/A')}<br>
                <b>Altitud:</b> {city.get('alt', 'N/A')}m
            </p>
        </div>
        """
        
        folium.CircleMarker(
            location=[city.get('lat', 0), city.get('lon', 0)],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=city.get('name', 'Unknown'),
            color=marker_color,
            fill=True,
            fillColor=marker_color,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
    
    plugins.Fullscreen().add_to(m)
    
    folium_static(m, width=None, height=500)
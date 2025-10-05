# components/mapa.py
import folium
from streamlit_folium import folium_static
from folium import plugins
from config.settings import MAP_CONFIG

def render_map(lat, lon, location_name):
    """
    Renderiza mapa principal con diseño mejorado
    """
    # Crear mapa base con estilo oscuro
    m = folium.Map(
        location=[lat, lon],
        zoom_start=MAP_CONFIG['default_zoom'],
        tiles=None  # Deshabilitamos el tile por defecto
    )
    
    # Agregar capa de mapa oscuro (estilo espacial)
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Dark Matter',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Opción alternativa: mapa satelital
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # HTML personalizado para el popup con estilo espacial
    popup_html = f"""
    <div style="
        font-family: 'Exo 2', sans-serif;
        padding: 10px;
        min-width: 200px;
        background: linear-gradient(135deg, #1e1b4b 0%, #0a0e27 100%);
        border-radius: 10px;
        border: 2px solid #6366f1;
    ">
        <h4 style="
            color: #00A6ED;
            margin: 0 0 10px 0;
            font-size: 1.1rem;
            text-align: center;
        ">
            📍 {location_name}
        </h4>
        <div style="color: white; font-size: 0.9rem;">
            <p style="margin: 5px 0;">
                <strong style="color: #6366f1;">Latitud:</strong> {lat}°
            </p>
            <p style="margin: 5px 0;">
                <strong style="color: #6366f1;">Longitud:</strong> {lon}°
            </p>
        </div>
        <div style="
            text-align: center;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(99, 102, 241, 0.3);
        ">
            <small style="color: rgba(255,255,255,0.6);">
                🛰️ Ubicación NASA
            </small>
        </div>
    </div>
    """
    
    # Marcador principal con icono personalizado
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=folium.Tooltip(
            f"<b>{location_name}</b><br>Click para más detalles",
            permanent=False
        ),
        icon=folium.Icon(
            color="red",
            icon="satellite",
            prefix='fa',
            icon_color='white'
        )
    ).add_to(m)
    
    # Círculo de área de análisis con efecto brillante
    folium.Circle(
        [lat, lon],
        radius=5000,  # 5km
        color='#6366f1',
        fill=True,
        fillColor='#00A6ED',
        fillOpacity=0.15,
        weight=2,
        popup='Área de análisis (5km)',
        tooltip='Radio de cobertura: 5km'
    ).add_to(m)
    
    # Círculo interior más brillante
    folium.Circle(
        [lat, lon],
        radius=1000,  # 1km
        color='#00A6ED',
        fill=True,
        fillColor='#00A6ED',
        fillOpacity=0.3,
        weight=1
    ).add_to(m)
    
    # Agregar plugin de pantalla completa
    plugins.Fullscreen(
        position='topright',
        title='Pantalla completa',
        title_cancel='Salir de pantalla completa',
        force_separate_button=True
    ).add_to(m)
    
    # Agregar medidor de escala
    folium.plugins.MeasureControl(
        position='bottomleft',
        primary_length_unit='kilometers',
        secondary_length_unit='miles',
        primary_area_unit='sqkilometers',
        secondary_area_unit='acres'
    ).add_to(m)
    
    # Agregar control de capas
    folium.LayerControl().add_to(m)
    
    # Renderizar mapa
    folium_static(m, width=None, height=450)


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
    
    # Marcador simple
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
    Usado para visualizar zonas climáticas
    
    Args:
        cities_data: Lista de diccionarios con info de ciudades
        highlight_city: Nombre de ciudad a resaltar (opcional)
    """
    # Centro de México
    center_lat = 23.6345
    center_lon = -102.5528
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CARTO'
    )
    
    # Agregar marcadores para cada ciudad
    for city in cities_data:
        # Color según si está resaltada
        if highlight_city and city.get('name') == highlight_city:
            marker_color = 'red'
            icon_name = 'star'
            radius = 15
        else:
            marker_color = 'blue'
            icon_name = 'map-marker'
            radius = 10
        
        # Crear popup con información
        popup_html = f"""
        <div style="font-family: Arial; padding: 5px;">
            <h4 style="margin: 0; color: #0B3D91;">{city.get('name', 'Unknown')}</h4>
            <p style="margin: 5px 0;">
                <b>Estado:</b> {city.get('state', 'N/A')}<br>
                <b>Altitud:</b> {city.get('alt', 'N/A')}m<br>
                <b>Coords:</b> {city.get('lat', 0):.4f}, {city.get('lon', 0):.4f}
            </p>
        </div>
        """
        
        # Agregar marcador
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
    
    # Agregar control de pantalla completa
    plugins.Fullscreen().add_to(m)
    
    folium_static(m, width=None, height=500)
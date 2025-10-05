# config/settings.py

PAGE_CONFIG = {
    'page_title': 'NASA Climate Intelligence Platform',
    'page_icon': '🛰️',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Paleta de colores NASA espacial
COLORS = {
    'primary': '#0B3D91',        # Azul NASA oficial
    'secondary': '#00A6ED',      # Azul tecnológico
    'accent': '#FC3D21',         # Naranja NASA
    'success': '#10B981',        # Verde éxito
    'warning': '#F59E0B',        # Amarillo advertencia
    'danger': '#EF4444',         # Rojo peligro
    'text': '#FFFFFF',           # Blanco
    'text_dark': '#1F2937',      # Gris oscuro
    'card_bg': '#FFFFFF',        # Fondo tarjetas
    'space_dark': '#0a0e27',     # Azul espacial oscuro
    'space_purple': '#6366f1',   # Púrpura espacial
    'space_cyan': '#06b6d4',     # Cyan tecnológico
    'gradient_start': '#1e1b4b', # Gradiente inicio
    'gradient_end': '#7c3aed'    # Gradiente fin
}

MAP_CONFIG = {
    'default_location': 'Ciudad de México',
    'default_lat': 19.4326,
    'default_lon': -99.1332,
    'default_zoom': 6
}

# Ciudades con datos de NASA GIOVANNI
CIUDADES_NASA = {
    'veracruz': {
        'name': 'Veracruz',
        'display_name': '🌊 Veracruz',
        'lat': 19.20,
        'lon': -96.15,
        'state': 'Veracruz',
        'icon': '🌊',
        'color': '#06b6d4',
        'description': 'Puerto tropical del Golfo de México'
    },
    'cdmx': {
        'name': 'Ciudad de México',
        'display_name': '🏛️ Ciudad de México',
        'lat': 19.43,
        'lon': -99.13,
        'state': 'CDMX',
        'icon': '🏛️',
        'color': '#8b5cf6',
        'description': 'Capital del país, clima templado'
    },
    'cancun': {
        'name': 'Cancún',
        'display_name': '🏖️ Cancún',
        'lat': 21.16,
        'lon': -86.85,
        'state': 'Quintana Roo',
        'icon': '🏖️',
        'color': '#10b981',
        'description': 'Paraíso caribeño, clima tropical'
    },
    'monterrey': {
        'name': 'Monterrey',
        'display_name': '🏔️ Monterrey',
        'lat': 25.68,
        'lon': -100.31,
        'state': 'Nuevo León',
        'icon': '🏔️',
        'color': '#f59e0b',
        'description': 'Ciudad industrial del norte'
    },
    'tijuana': {
        'name': 'Tijuana',
        'display_name': '🌵 Tijuana',
        'lat': 32.52,
        'lon': -117.04,
        'state': 'Baja California',
        'icon': '🌵',
        'color': '#ef4444',
        'description': 'Frontera norte, clima mediterráneo'
    }
}

# Variables climáticas con iconos y descripciones mejoradas
VARIABLES = {
    'temperatura': {
        'nombre': '🌡️ Temperatura',
        'descripcion': 'Temperatura del aire a 2 metros de altura',
        'unidad': '°C',
        'threshold_extreme': 35,
        'color': '#EF4444'
    },
    'precipitacion': {
        'nombre': '🌧️ Precipitación',
        'descripcion': 'Cantidad de lluvia acumulada',
        'unidad': 'mm',
        'threshold_extreme': 50,
        'color': '#3B82F6'
    },
    'viento': {
        'nombre': '💨 Velocidad del Viento',
        'descripcion': 'Velocidad del viento a 10 metros de altura',
        'unidad': 'km/h',
        'threshold_extreme': 60,
        'color': '#06B6D4'
    },
    'humedad': {
        'nombre': '💧 Humedad Relativa',
        'descripcion': 'Porcentaje de humedad en el aire',
        'unidad': '%',
        'threshold_extreme': 80,
        'color': '#8B5CF6'
    },
    'nubosidad': {
        'nombre': '☁️ Cobertura de Nubes',
        'descripcion': 'Porcentaje de cobertura nubosa',
        'unidad': '%',
        'threshold_extreme': 90,
        'color': '#6B7280'
    }
}

# Ciudades mexicanas organizadas por clima
MEXICAN_CLIMATE_ZONES = {
    'nevado': {
        'emoji': '🏔️',
        'nombre': 'Clima Nevado',
        'description': 'Zonas con probabilidad de nevadas en invierno',
        'color': '#60A5FA',
        'cities': [
            {
                'name': 'Nevado de Toluca',
                'state': 'Estado de México',
                'lat': 19.1092,
                'lon': -99.7556,
                'alt': 4680,
                'temp_range': (-5, 15),
                'snow_months': [11, 12, 1, 2, 3]
            },
            {
                'name': 'Pico de Orizaba',
                'state': 'Veracruz/Puebla',
                'lat': 19.0303,
                'lon': -97.2679,
                'alt': 5636,
                'temp_range': (-10, 10),
                'snow_months': [10, 11, 12, 1, 2, 3, 4]
            },
            {
                'name': 'Arteaga',
                'state': 'Coahuila',
                'lat': 25.3833,
                'lon': -100.8167,
                'alt': 1650,
                'temp_range': (-3, 20),
                'snow_months': [12, 1, 2]
            },
            {
                'name': 'Creel',
                'state': 'Chihuahua',
                'lat': 27.7508,
                'lon': -107.6347,
                'alt': 2338,
                'temp_range': (-5, 25),
                'snow_months': [11, 12, 1, 2]
            },
            {
                'name': 'Madera',
                'state': 'Chihuahua',
                'lat': 29.1844,
                'lon': -108.1375,
                'alt': 2150,
                'temp_range': (-8, 28),
                'snow_months': [11, 12, 1, 2, 3]
            },
            {
                'name': 'Cumbres de Monterrey',
                'state': 'Nuevo León',
                'lat': 25.6166,
                'lon': -100.2500,
                'alt': 2260,
                'temp_range': (0, 22),
                'snow_months': [12, 1, 2]
            }
        ]
    },
    'frio_seco': {
        'emoji': '❄️',
        'nombre': 'Clima Frío Seco',
        'description': 'Clima frío con poca humedad',
        'color': '#A5B4FC',
        'cities': [
            {
                'name': 'Toluca',
                'state': 'Estado de México',
                'lat': 19.2827,
                'lon': -99.6557,
                'alt': 2680,
                'temp_range': (5, 20)
            },
            {
                'name': 'San Cristóbal de las Casas',
                'state': 'Chiapas',
                'lat': 16.7370,
                'lon': -92.6376,
                'alt': 2200,
                'temp_range': (8, 22)
            },
            {
                'name': 'Durango',
                'state': 'Durango',
                'lat': 24.0277,
                'lon': -104.6532,
                'alt': 1890,
                'temp_range': (5, 28)
            },
            {
                'name': 'Zacatecas',
                'state': 'Zacatecas',
                'lat': 22.7709,
                'lon': -102.5832,
                'alt': 2440,
                'temp_range': (6, 25)
            },
            {
                'name': 'Real de Catorce',
                'state': 'San Luis Potosí',
                'lat': 23.6833,
                'lon': -100.8833,
                'alt': 2750,
                'temp_range': (4, 23)
            }
        ]
    },
    'templado': {
        'emoji': '🌤️',
        'nombre': 'Clima Templado',
        'description': 'Temperaturas moderadas todo el año',
        'color': '#34D399',
        'cities': [
            {
                'name': 'Ciudad de México',
                'state': 'CDMX',
                'lat': 19.4326,
                'lon': -99.1332,
                'alt': 2240,
                'temp_range': (12, 26)
            },
            {
                'name': 'Guadalajara',
                'state': 'Jalisco',
                'lat': 20.6597,
                'lon': -103.3496,
                'alt': 1566,
                'temp_range': (14, 28)
            },
            {
                'name': 'Puebla',
                'state': 'Puebla',
                'lat': 19.0414,
                'lon': -98.2063,
                'alt': 2135,
                'temp_range': (13, 25)
            },
            {
                'name': 'Morelia',
                'state': 'Michoacán',
                'lat': 19.7060,
                'lon': -101.1949,
                'alt': 1920,
                'temp_range': (14, 26)
            },
            {
                'name': 'Querétaro',
                'state': 'Querétaro',
                'lat': 20.5888,
                'lon': -100.3899,
                'alt': 1820,
                'temp_range': (13, 27)
            },
            {
                'name': 'Xalapa',
                'state': 'Veracruz',
                'lat': 19.5438,
                'lon': -96.9102,
                'alt': 1460,
                'temp_range': (15, 24)
            }
        ]
    },
    'caluroso_seco': {
        'emoji': '🌵',
        'nombre': 'Clima Caluroso Seco',
        'description': 'Altas temperaturas con baja humedad',
        'color': '#FBBF24',
        'cities': [
            {
                'name': 'Hermosillo',
                'state': 'Sonora',
                'lat': 29.0729,
                'lon': -110.9559,
                'alt': 210,
                'temp_range': (18, 42)
            },
            {
                'name': 'Mexicali',
                'state': 'Baja California',
                'lat': 32.6245,
                'lon': -115.4523,
                'alt': 10,
                'temp_range': (16, 44)
            },
            {
                'name': 'Chihuahua',
                'state': 'Chihuahua',
                'lat': 28.6353,
                'lon': -106.0889,
                'alt': 1440,
                'temp_range': (10, 36)
            },
            {
                'name': 'Torreón',
                'state': 'Coahuila',
                'lat': 25.5428,
                'lon': -103.4068,
                'alt': 1120,
                'temp_range': (14, 38)
            },
            {
                'name': 'Saltillo',
                'state': 'Coahuila',
                'lat': 25.4260,
                'lon': -101.0053,
                'alt': 1600,
                'temp_range': (12, 34)
            }
        ]
    },
    'caluroso_humedo': {
        'emoji': '🏖️',
        'nombre': 'Clima Caluroso Húmedo',
        'description': 'Altas temperaturas con alta humedad',
        'color': '#F87171',
        'cities': [
            {
                'name': 'Mérida',
                'state': 'Yucatán',
                'lat': 20.9674,
                'lon': -89.5926,
                'alt': 10,
                'temp_range': (22, 36)
            },
            {
                'name': 'Cancún',
                'state': 'Quintana Roo',
                'lat': 21.1619,
                'lon': -86.8515,
                'alt': 10,
                'temp_range': (23, 34)
            },
            {
                'name': 'Veracruz',
                'state': 'Veracruz',
                'lat': 19.1738,
                'lon': -96.1342,
                'alt': 10,
                'temp_range': (22, 32)
            },
            {
                'name': 'Villahermosa',
                'state': 'Tabasco',
                'lat': 17.9892,
                'lon': -92.9475,
                'alt': 10,
                'temp_range': (23, 35)
            },
            {
                'name': 'Acapulco',
                'state': 'Guerrero',
                'lat': 16.8531,
                'lon': -99.8237,
                'alt': 3,
                'temp_range': (24, 33)
            },
            {
                'name': 'Mazatlán',
                'state': 'Sinaloa',
                'lat': 23.2494,
                'lon': -106.4111,
                'alt': 10,
                'temp_range': (20, 32)
            }
        ]
    }
}
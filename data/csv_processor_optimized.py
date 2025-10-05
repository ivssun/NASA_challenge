# data/csv_processor_optimized.py
"""
CSV Processor Optimizado
=========================
Versión mejorada con soporte para 5 variables: temperatura, precipitación, viento, humedad, nubosidad
"""

import pandas as pd
import numpy as np
import os
from functools import lru_cache

class CSVProcessorOptimized:
    """Procesador optimizado para NASA Space Apps Challenge"""
    
    def __init__(self, csv_folder='data/csv'):
        self.csv_folder = csv_folder
        self.data = {}
        
        self.city_coords = {
            'veracruz': {'lat': 19.20, 'lon': -96.15, 'name': 'Veracruz'},
            'cdmx': {'lat': 19.43, 'lon': -99.13, 'name': 'Ciudad de México'},
            'cancun': {'lat': 21.16, 'lon': -86.85, 'name': 'Cancún'},
            'monterrey': {'lat': 25.68, 'lon': -100.31, 'name': 'Monterrey'},
            'tijuana': {'lat': 32.52, 'lon': -117.04, 'name': 'Tijuana'}
        }
        
        # Mapeo de nombres de archivos
        self.file_mapping = {
            'temperatura': 'temperatura',
            'precipitacion': 'precipitacion',
            'viento': 'viento',
            'humedad': 'QV2M',
            'nubosidad': 'MODIS'
        }
    
    def load_all_csvs(self):
        """Carga CSVs y PRE-CALCULA agrupaciones por mes"""
        print("\n🚀 CARGANDO CSVs (MODO OPTIMIZADO)...")
        print("=" * 70)
        
        variables = ['temperatura', 'precipitacion', 'viento', 'humedad', 'nubosidad']
        
        for city_key in self.city_coords.keys():
            self.data[city_key] = {}
            
            for var in variables:
                try:
                    # Obtener nombre de archivo correcto
                    file_prefix = self.file_mapping[var]
                    filepath = os.path.join(self.csv_folder, f"{file_prefix}_{city_key}.csv")
                    
                    if not os.path.exists(filepath):
                        continue
                    
                    # Leer CSV
                    df = pd.read_csv(filepath, skiprows=9)
                    df.columns = ['time', var]
                    
                    # Convertir tipos
                    df['time'] = pd.to_datetime(df['time'])
                    df[var] = pd.to_numeric(df[var], errors='coerce')
                    
                    # CONVERSIONES DE UNIDADES
                    if var == 'viento':
                        df[var] = df[var] * 3.6  # m/s → km/h
                    
                    elif var == 'nubosidad':
                        df[var] = df[var] * 100  # fracción → porcentaje
                    
                    # humedad se queda en kg/kg (se convierte en humidity_analyzer)
                    
                    # Agregar columnas útiles
                    df['month'] = df['time'].dt.month
                    df['year'] = df['time'].dt.year
                    
                    # Eliminar NaN
                    df = df.dropna(subset=[var])
                    
                    # PRE-AGRUPAR POR MES
                    df_by_month = {}
                    for month in range(1, 13):
                        df_month = df[df['month'] == month]
                        df_by_month[month] = df_month[var].values
                    
                    # Guardar
                    self.data[city_key][var] = {
                        'df': df,
                        'by_month': df_by_month
                    }
                    
                    years_range = f"{df['year'].min()}-{df['year'].max()}"
                    
                    # Mostrar unidad
                    units = {
                        'temperatura': '°C',
                        'precipitacion': 'mm',
                        'viento': 'km/h',
                        'humedad': 'kg/kg',
                        'nubosidad': '%'
                    }
                    
                    print(f"✅ {city_key}/{var}: {len(df)} registros ({years_range}) [{units[var]}]")
                
                except Exception as e:
                    print(f"❌ {city_key}/{var}: {e}")
        
        print("=" * 70)
        total = sum(len(v) for v in self.data.values())
        print(f"✅ Cargadas {total} variables\n")
        
        return len(self.data) > 0
    
    def find_nearest_city(self, lat, lon):
        """Encuentra ciudad más cercana"""
        min_dist = float('inf')
        nearest = None
        
        for city_key, coords in self.city_coords.items():
            dist = (lat - coords['lat'])**2 + (lon - coords['lon'])**2
            if dist < min_dist:
                min_dist = dist
                nearest = city_key
        
        return nearest, min_dist
    
    def get_historical_data(self, lat, lon, variable, month, day):
        """Obtiene datos históricos para un mes"""
        city_key, _ = self.find_nearest_city(lat, lon)
        
        if city_key not in self.data:
            return None, None
        
        if variable not in self.data[city_key]:
            return None, self.city_coords[city_key]['name']
        
        values = self.data[city_key][variable]['by_month'].get(month)
        city_name = self.city_coords[city_key]['name']
        
        return values, city_name
    
    def calculate_probability(self, values, threshold, condition='greater'):
        """Calcula probabilidad"""
        if values is None or len(values) == 0:
            return 0.0
        
        if condition == 'greater':
            return float(np.mean(values > threshold))
        else:
            return float(np.mean(values < threshold))
    
    def get_statistics(self, values):
        """Estadísticas básicas"""
        if values is None or len(values) == 0:
            return None
        
        return {
            'mean': float(np.mean(values)),
            'median': float(np.median(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'count': len(values)
        }
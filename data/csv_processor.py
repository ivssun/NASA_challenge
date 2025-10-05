"""
CSV Processor
=============
Lee archivos CSV de temperatura y precipitación de NASA GIOVANNI
"""

import pandas as pd
import numpy as np
import os

class CSVProcessor:
    """Procesa archivos CSV con series temporales de NASA"""
    
    def __init__(self, csv_folder='data/csv'):
        self.csv_folder = csv_folder
        self.data = {}
        
        # Archivos de temperatura
        self.temp_files = {
            'veracruz': 'temperatura_veracruz.csv',
            'cdmx': 'temperatura_cdmx.csv',
            'cancun': 'temperatura_cancun.csv',
            'monterrey': 'temperatura_monterrey.csv',
            'tijuana': 'temperatura_tijuana.csv'
        }
        
        # Archivos de precipitación
        self.precip_files = {
            'veracruz': 'precipitacion_veracruz.csv',
            'cdmx': 'precipitacion_cdmx.csv',
            'cancun': 'precipitacion_cancun.csv',
            'monterrey': 'precipitacion_monterrey.csv',
            'tijuana': 'precipitacion_tijuana.csv'
        }
        
        self.city_coords = {
            'veracruz': {'lat': 19.20, 'lon': -96.15, 'name': 'Veracruz'},
            'cdmx': {'lat': 19.43, 'lon': -99.13, 'name': 'Ciudad de México'},
            'cancun': {'lat': 21.16, 'lon': -86.85, 'name': 'Cancún'},
            'monterrey': {'lat': 25.68, 'lon': -100.31, 'name': 'Monterrey'},
            'tijuana': {'lat': 32.52, 'lon': -117.04, 'name': 'Tijuana'}
        }
    
    def load_all_csvs(self):
        """Carga todos los archivos CSV de temperatura y precipitación"""
        print("\n📂 CARGANDO ARCHIVOS CSV...")
        print("=" * 70)
        
        # Estructura: self.data[city_key][variable] = DataFrame
        for city_key in self.temp_files.keys():
            self.data[city_key] = {}
            
            # Cargar temperatura
            try:
                temp_file = self.temp_files[city_key]
                filepath = os.path.join(self.csv_folder, temp_file)
                
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath, skiprows=9)
                    df.columns = ['time', 'temperature']
                    df['time'] = pd.to_datetime(df['time'])
                    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
                    self.data[city_key]['temperatura'] = df
                    print(f"📄 {city_key} - temperatura: ✅ {len(df)} registros")
            except Exception as e:
                print(f"❌ {city_key} - temperatura: Error {e}")
            
            # Cargar precipitación
            try:
                precip_file = self.precip_files[city_key]
                filepath = os.path.join(self.csv_folder, precip_file)
                
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath, skiprows=9)
                    df.columns = ['time', 'precipitation']
                    df['time'] = pd.to_datetime(df['time'])
                    df['precipitation'] = pd.to_numeric(df['precipitation'], errors='coerce')
                    self.data[city_key]['precipitacion'] = df
                    print(f"📄 {city_key} - precipitación: ✅ {len(df)} registros")
            except Exception as e:
                print(f"❌ {city_key} - precipitación: Error {e}")
        
        print("=" * 70)
        total_vars = sum(len(vars_dict) for vars_dict in self.data.values())
        print(f"✅ Variables cargadas: {total_vars}\n")
        
        return len(self.data) > 0
    
    def find_nearest_city(self, lat, lon):
        """Encuentra la ciudad más cercana"""
        min_distance = float('inf')
        nearest_city = None
        
        for city_key, coords in self.city_coords.items():
            distance = np.sqrt(
                (lat - coords['lat'])**2 + 
                (lon - coords['lon'])**2
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_city = city_key
        
        return nearest_city, min_distance
    
    def get_historical_data(self, lat, lon, variable, month, day):
        """
        Obtiene datos históricos para una ubicación y variable
        
        Args:
            lat: Latitud
            lon: Longitud
            variable: 'temperatura' o 'precipitacion'
            month: Mes (1-12)
            day: Día (no usado por ahora, datos mensuales)
        
        Returns:
            (values, city_name)
        """
        city_key, distance = self.find_nearest_city(lat, lon)
        
        if city_key not in self.data:
            return None, None
        
        if variable not in self.data[city_key]:
            return None, self.city_coords[city_key]['name']
        
        df = self.data[city_key][variable]
        city_name = self.city_coords[city_key]['name']
        
        # Filtrar por mes
        df_filtered = df[df['time'].dt.month == month].copy()
        
        if len(df_filtered) == 0:
            return None, city_name
        
        # Extraer valores según la variable
        if variable == 'temperatura':
            values = df_filtered['temperature'].values
        elif variable == 'precipitacion':
            values = df_filtered['precipitation'].values
        else:
            return None, city_name
        
        # Remover NaN
        values = values[~np.isnan(values)]
        
        return values, city_name
    
    def calculate_probability(self, values, threshold, condition='greater'):
        """Calcula probabilidad de exceder un umbral"""
        if values is None or len(values) == 0:
            return 0.0
        
        if condition == 'greater':
            count = np.sum(values > threshold)
        else:
            count = np.sum(values < threshold)
        
        return float(count / len(values))
    
    def get_statistics(self, values):
        """Calcula estadísticas"""
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


# CÓDIGO DE PRUEBA
if __name__ == "__main__":
    print("\n🧪 PROBANDO CSV PROCESSOR")
    print("=" * 70)
    
    processor = CSVProcessor()
    success = processor.load_all_csvs()
    
    if success:
        print("\n🔍 PRUEBA: Veracruz en enero")
        print("-" * 70)
        
        # Temperatura
        temp_vals, city = processor.get_historical_data(19.20, -96.15, 'temperatura', 1, 1)
        if temp_vals is not None:
            stats = processor.get_statistics(temp_vals)
            print(f"🌡️ Temperatura promedio: {stats['mean']:.2f}°C")
        
        # Precipitación
        precip_vals, city = processor.get_historical_data(19.20, -96.15, 'precipitacion', 1, 1)
        if precip_vals is not None:
            stats = processor.get_statistics(precip_vals)
            print(f"🌧️ Precipitación promedio: {stats['mean']:.2f}mm")
# data/humidity_analyzer.py
"""
Analizador de Humedad
====================
Convierte humedad específica (QV2M en kg/kg) a humedad relativa (%).
Requiere datos de temperatura para la conversión.
"""

import numpy as np
from datetime import datetime

class HumidityAnalyzer:
    """Analiza y convierte datos de humedad"""
    
    def __init__(self):
        pass
    
    def specific_to_relative_humidity(self, q_values, temp_values, pressure=101325):
        """
        Convierte humedad específica a humedad relativa
        
        Fórmula:
        1. Calcular presión de vapor: e = (q * P) / (0.622 + q)
        2. Calcular presión de saturación: es = 611 * exp((17.27 * T) / (T + 237.3))
        3. Humedad relativa: RH = (e / es) * 100
        
        Args:
            q_values: humedad específica (kg/kg)
            temp_values: temperatura (°C)
            pressure: presión atmosférica (Pa), default 101325 Pa (nivel del mar)
        
        Returns:
            numpy array con humedad relativa (%)
        """
        if len(q_values) != len(temp_values):
            return None
        
        # Constantes
        e0 = 611  # Pa
        Rv = 461.5  # J/(kg·K)
        
        # Arrays de salida
        rh_values = np.zeros(len(q_values))
        
        for i in range(len(q_values)):
            q = q_values[i]
            T = temp_values[i]
            
            # Presión de vapor actual
            e = (q * pressure) / (0.622 + q)
            
            # Presión de vapor de saturación (ecuación de Magnus)
            es = e0 * np.exp((17.27 * T) / (T + 237.3))
            
            # Humedad relativa
            rh = (e / es) * 100
            
            # Limitar a 0-100%
            rh_values[i] = np.clip(rh, 0, 100)
        
        return rh_values
    
    def analyze_monthly_data(self, monthly_humidity_values, monthly_temp_values, city_key, month):
        """
        Analiza datos mensuales de humedad
        
        Args:
            monthly_humidity_values: QV2M en kg/kg
            monthly_temp_values: temperatura en °C
            city_key: ciudad
            month: mes
        
        Returns:
            dict con análisis
        """
        if monthly_humidity_values is None or len(monthly_humidity_values) == 0:
            return None
        
        if monthly_temp_values is None or len(monthly_temp_values) == 0:
            return None
        
        # Convertir a humedad relativa
        rh_values = self.specific_to_relative_humidity(
            monthly_humidity_values, 
            monthly_temp_values
        )
        
        if rh_values is None:
            return None
        
        # Estadísticas
        avg_rh = float(np.mean(rh_values))
        max_rh = float(np.max(rh_values))
        min_rh = float(np.min(rh_values))
        
        # Percentiles
        p25 = float(np.percentile(rh_values, 25))
        p75 = float(np.percentile(rh_values, 75))
        p90 = float(np.percentile(rh_values, 90))
        
        # Categorización
        category = self._categorize_humidity(avg_rh)
        comfort_level = self._get_comfort_level(avg_rh)
        
        return {
            'avg_humidity': round(avg_rh, 1),
            'min_humidity': round(min_rh, 1),
            'max_humidity': round(max_rh, 1),
            'p25_humidity': round(p25, 1),
            'p75_humidity': round(p75, 1),
            'p90_humidity': round(p90, 1),
            'humidity_category': category,
            'comfort_level': comfort_level,
            'historical_years': len(rh_values)
        }
    
    def _categorize_humidity(self, rh):
        """Categoriza nivel de humedad"""
        if rh < 30:
            return "Muy seco"
        elif rh < 50:
            return "Seco"
        elif rh < 70:
            return "Confortable"
        elif rh < 85:
            return "Húmedo"
        else:
            return "Muy húmedo"
    
    def _get_comfort_level(self, rh):
        """Determina nivel de confort"""
        if 40 <= rh <= 60:
            return "Ideal", "#10B981"
        elif 30 <= rh <= 70:
            return "Confortable", "#F59E0B"
        else:
            return "Incómodo", "#EF4444"
    
    def get_humidity_message(self, analysis, date):
        """Genera mensaje descriptivo"""
        if not analysis:
            return "No hay datos suficientes"
        
        avg_rh = analysis['avg_humidity']
        category = analysis['humidity_category']
        
        if avg_rh < 30:
            message = f"Ambiente muy seco ({avg_rh}%). Puede causar irritación en piel y vías respiratorias. Recomendación: hidratarse frecuentemente."
        elif avg_rh < 50:
            message = f"Ambiente seco ({avg_rh}%). Condiciones confortables para la mayoría de actividades."
        elif avg_rh < 70:
            message = f"Humedad confortable ({avg_rh}%). Condiciones ideales para actividades al aire libre."
        elif avg_rh < 85:
            message = f"Ambiente húmedo ({avg_rh}%). Puede sentirse bochornoso en días calurosos."
        else:
            message = f"Muy húmedo ({avg_rh}%). Sensación de bochorno. Dificulta la evaporación del sudor."
        
        return message


def integrate_humidity_with_processor(processor, humidity_analyzer, lat, lon, month, day):
    """Integra analizador de humedad con procesador"""
    # Obtener humedad específica
    humidity_values, city_name = processor.get_historical_data(
        lat, lon, 'humedad', month, day
    )
    
    # Obtener temperatura (necesaria para conversión)
    temp_values, _ = processor.get_historical_data(
        lat, lon, 'temperatura', month, day
    )
    
    if humidity_values is None or temp_values is None:
        return None
    
    city_key = processor.find_nearest_city(lat, lon)[0]
    date = datetime(2024, month, day)
    
    analysis = humidity_analyzer.analyze_monthly_data(
        humidity_values, temp_values, city_key, month
    )
    
    if analysis:
        analysis['message'] = humidity_analyzer.get_humidity_message(analysis, date)
        analysis['city_name'] = city_name
    
    return analysis
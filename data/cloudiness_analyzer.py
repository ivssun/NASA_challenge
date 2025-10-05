# data/cloudiness_analyzer.py
"""
Analizador de Nubosidad
=======================
Convierte fracción de nubes MODIS (0-1) a porcentaje (0-100%).
"""

import numpy as np
from datetime import datetime

class CloudinessAnalyzer:
    """Analiza cobertura de nubes"""
    
    def __init__(self):
        pass
    
    def analyze_monthly_data(self, monthly_cloud_values, city_key, month):
        """
        Analiza datos mensuales de nubosidad
        
        Args:
            monthly_cloud_values: fracción de nubes (0-1)
            city_key: ciudad
            month: mes
        
        Returns:
            dict con análisis
        """
        if monthly_cloud_values is None or len(monthly_cloud_values) == 0:
            return None
        
        # Convertir fracción a porcentaje
        cloud_percent = monthly_cloud_values
        
        # Estadísticas
        avg_cloud = float(np.mean(cloud_percent))
        max_cloud = float(np.max(cloud_percent))
        min_cloud = float(np.min(cloud_percent))
        
        # Percentiles
        p25 = float(np.percentile(cloud_percent, 25))
        p75 = float(np.percentile(cloud_percent, 75))
        p90 = float(np.percentile(cloud_percent, 90))
        
        # Probabilidades
        prob_clear = float(np.mean(cloud_percent < 25))
        prob_partly = float(np.mean((cloud_percent >= 25) & (cloud_percent < 75)))
        prob_overcast = float(np.mean(cloud_percent >= 75))
        
        # Categorización
        category = self._categorize_cloudiness(avg_cloud)
        sky_condition = self._get_sky_condition(avg_cloud)
        
        return {
            'avg_cloudiness': round(avg_cloud, 1),
            'min_cloudiness': round(min_cloud, 1),
            'max_cloudiness': round(max_cloud, 1),
            'p25_cloudiness': round(p25, 1),
            'p75_cloudiness': round(p75, 1),
            'p90_cloudiness': round(p90, 1),
            'prob_clear_sky': round(prob_clear * 100, 1),
            'prob_partly_cloudy': round(prob_partly * 100, 1),
            'prob_overcast': round(prob_overcast * 100, 1),
            'cloudiness_category': category,
            'sky_condition': sky_condition,
            'historical_years': len(cloud_percent)
        }
    
    def _categorize_cloudiness(self, cloud_percent):
        """Categoriza cobertura de nubes"""
        if cloud_percent < 25:
            return "Cielo despejado"
        elif cloud_percent < 50:
            return "Parcialmente nublado"
        elif cloud_percent < 75:
            return "Mayormente nublado"
        else:
            return "Nublado"
    
    def _get_sky_condition(self, cloud_percent):
        """Determina condición del cielo"""
        if cloud_percent < 25:
            return "Excelente", "#10B981"
        elif cloud_percent < 50:
            return "Bueno", "#F59E0B"
        elif cloud_percent < 75:
            return "Regular", "#F97316"
        else:
            return "Pobre", "#6B7280"
    
    def get_cloudiness_message(self, analysis, date):
        """Genera mensaje descriptivo"""
        if not analysis:
            return "No hay datos suficientes"
        
        avg_cloud = analysis['avg_cloudiness']
        category = analysis['cloudiness_category']
        
        if avg_cloud < 25:
            message = f"Cielo mayormente despejado ({avg_cloud}% de nubes). Excelente para actividades al aire libre y fotografía."
        elif avg_cloud < 50:
            message = f"Parcialmente nublado ({avg_cloud}%). Buenas condiciones con algo de sombra natural."
        elif avg_cloud < 75:
            message = f"Mayormente nublado ({avg_cloud}%). Cielo cubierto en gran parte del tiempo."
        else:
            message = f"Cielo nublado ({avg_cloud}%). Poca visibilidad del sol. Puede afectar actividades que requieren luz solar directa."
        
        return message


def integrate_cloudiness_with_processor(processor, cloudiness_analyzer, lat, lon, month, day):
    """Integra analizador de nubosidad con procesador"""
    cloud_values, city_name = processor.get_historical_data(
        lat, lon, 'nubosidad', month, day
    )
    
    if cloud_values is None:
        return None
    
    city_key = processor.find_nearest_city(lat, lon)[0]
    date = datetime(2024, month, day)
    
    analysis = cloudiness_analyzer.analyze_monthly_data(
        cloud_values, city_key, month
    )
    
    if analysis:
        analysis['message'] = cloudiness_analyzer.get_cloudiness_message(analysis, date)
        analysis['city_name'] = city_name
    
    return analysis
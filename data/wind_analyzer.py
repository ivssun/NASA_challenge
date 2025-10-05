# data/wind_analyzer.py
"""
Analizador de Viento
====================
Analiza velocidad del viento y calcula probabilidades de viento fuerte.

POR QUÉ EXISTE:
- NASA GIOVANNI da velocidad promedio mensual
- El usuario quiere saber si habrá viento fuerte ese día
- Este módulo calcula probabilidad de diferentes intensidades
"""

import numpy as np
from datetime import datetime

class WindAnalyzer:
    """
    Analiza datos de viento y categoriza intensidades
    """
    
    def __init__(self):
        """
        Categorías de viento basadas en escala Beaufort adaptada para México
        """
        self.wind_categories = {
            'calmo': (0, 10),           # < 10 km/h
            'ligero': (10, 20),         # 10-20 km/h
            'moderado': (20, 40),       # 20-40 km/h
            'fuerte': (40, 60),         # 40-60 km/h
            'muy_fuerte': (60, 100)     # > 60 km/h
        }
    
    def analyze_monthly_data(self, monthly_wind_values, city_key, month):
        """
        Analiza datos mensuales de viento
        
        CÓMO FUNCIONA:
        1. Recibe velocidades promedio mensuales de 30+ años
        2. Calcula estadísticas (promedio, máximo, percentiles)
        3. Determina probabilidad de viento fuerte
        4. Categoriza la intensidad esperada
        
        Args:
            monthly_wind_values: numpy array con velocidad del viento (km/h)
            city_key: ciudad
            month: mes (1-12)
        
        Returns:
            dict con análisis completo
        """
        if monthly_wind_values is None or len(monthly_wind_values) == 0:
            return None
        
        # Filtrar valores válidos (>= 0)
        monthly_wind_values = monthly_wind_values[monthly_wind_values >= 0]
        
        if len(monthly_wind_values) == 0:
            return None
        
        # Estadísticas básicas
        avg_wind = float(np.mean(monthly_wind_values))
        max_wind = float(np.max(monthly_wind_values))
        min_wind = float(np.min(monthly_wind_values))
        std_wind = float(np.std(monthly_wind_values))
        
        # Percentiles
        p50 = float(np.percentile(monthly_wind_values, 50))
        p75 = float(np.percentile(monthly_wind_values, 75))
        p90 = float(np.percentile(monthly_wind_values, 90))
        p95 = float(np.percentile(monthly_wind_values, 95))
        
        # Probabilidades de cada categoría
        prob_fuerte = float(np.mean(monthly_wind_values >= 40))  # > 40 km/h
        prob_moderado = float(np.mean((monthly_wind_values >= 20) & (monthly_wind_values < 40)))
        prob_ligero = float(np.mean((monthly_wind_values >= 10) & (monthly_wind_values < 20)))
        prob_calmo = float(np.mean(monthly_wind_values < 10))
        
        # Categoría más probable
        category = self._categorize_wind(avg_wind)
        
        # Nivel de riesgo
        risk_level = self._get_risk_level(avg_wind, p90)
        
        return {
            # Velocidad esperada
            'avg_wind_speed': round(avg_wind, 1),
            'median_wind_speed': round(p50, 1),
            'max_wind_speed': round(max_wind, 1),
            'min_wind_speed': round(min_wind, 1),
            
            # Percentiles
            'p75_wind': round(p75, 1),
            'p90_wind': round(p90, 1),
            'p95_wind': round(p95, 1),
            
            # Probabilidades
            'prob_strong_wind': round(prob_fuerte * 100, 1),  # > 40 km/h
            'prob_moderate_wind': round(prob_moderado * 100, 1),
            'prob_light_wind': round(prob_ligero * 100, 1),
            'prob_calm': round(prob_calmo * 100, 1),
            
            # Categorización
            'wind_category': category,
            'risk_level': risk_level,
            
            # Datos históricos
            'historical_years': len(monthly_wind_values),
            'variability': round(std_wind, 1)
        }
    
    def _categorize_wind(self, wind_speed):
        """Categoriza velocidad del viento"""
        if wind_speed < 10:
            return "Calmo"
        elif wind_speed < 20:
            return "Viento ligero"
        elif wind_speed < 40:
            return "Viento moderado"
        elif wind_speed < 60:
            return "Viento fuerte"
        else:
            return "Viento muy fuerte"
    
    def _get_risk_level(self, avg_wind, p90_wind):
        """Determina nivel de riesgo para actividades al aire libre"""
        if p90_wind < 20:
            return "Muy bajo", "#10B981"  # Verde
        elif p90_wind < 40:
            return "Bajo", "#F59E0B"  # Amarillo
        elif p90_wind < 60:
            return "Moderado", "#F97316"  # Naranja
        else:
            return "Alto", "#EF4444"  # Rojo
    
    def get_wind_forecast_message(self, analysis, date):
        """
        Genera mensaje descriptivo para el usuario
        
        Args:
            analysis: dict resultado de analyze_monthly_data
            date: datetime del día consultado
        
        Returns:
            str mensaje
        """
        if not analysis:
            return "No hay datos suficientes para esta fecha"
        
        avg_wind = analysis['avg_wind_speed']
        category = analysis['wind_category']
        prob_strong = analysis['prob_strong_wind']
        p90 = analysis['p90_wind']
        
        month_name = date.strftime('%B')
        
        # Construir mensaje según intensidad
        if avg_wind < 10:
            message = f"🍃 **Condiciones de calma** en {month_name}.\n\n"
            message += f"Velocidad típica: **{avg_wind} km/h**. Ideal para actividades al aire libre."
        
        elif avg_wind < 20:
            message = f"🌤️ **Viento ligero** esperado en {month_name}.\n\n"
            message += f"Velocidad típica: **{avg_wind} km/h**. Perfecto para actividades como picnic, caminatas o deportes."
        
        elif avg_wind < 40:
            message = f"💨 **Viento moderado** en {month_name}.\n\n"
            message += f"Velocidad típica: **{avg_wind} km/h**. Puede afectar sombrillas o estructuras ligeras. "
            message += f"El 90% del tiempo no superará {p90} km/h."
        
        else:
            message = f"⚠️ **Viento fuerte** probable en {month_name}.\n\n"
            message += f"Velocidad típica: **{avg_wind} km/h** ({category.lower()}).\n"
            message += f"Probabilidad de viento >40 km/h: **{prob_strong}%**\n\n"
            message += "⚠️ Precaución: Puede dificultar actividades al aire libre. "
            message += "Asegura objetos ligeros y considera actividades bajo techo."
        
        return message


def integrate_wind_with_processor(processor, wind_analyzer, lat, lon, month, day):
    """
    Integra analizador de viento con el procesador de CSVs
    
    Args:
        processor: CSVProcessorOptimized
        wind_analyzer: WindAnalyzer
        lat, lon: coordenadas
        month, day: fecha
    
    Returns:
        dict con análisis completo de viento
    """
    # Obtener datos mensuales de viento
    wind_values, city_name = processor.get_historical_data(
        lat, lon, 'viento', month, day
    )
    
    if wind_values is None:
        return None
    
    # Determinar city_key
    city_key = processor.find_nearest_city(lat, lon)[0]
    
    # Analizar
    date = datetime(2024, month, day)
    
    analysis = wind_analyzer.analyze_monthly_data(
        wind_values, city_key, month
    )
    
    if analysis:
        analysis['message'] = wind_analyzer.get_wind_forecast_message(
            analysis, date
        )
        analysis['city_name'] = city_name
    
    return analysis


# PRUEBA
if __name__ == "__main__":
    print("\n🧪 PROBANDO WIND ANALYZER")
    print("=" * 70)
    
    # Simular datos de viento de Veracruz en Marzo (Nortes)
    wind_data = np.array([
        15, 18, 22, 25, 30, 28, 20, 35, 40, 32,
        18, 22, 25, 28, 20, 24, 30, 35, 25, 22,
        28, 32, 24, 20, 18, 25, 30, 28, 22, 20,
        25, 28, 30
    ])
    
    analyzer = WindAnalyzer()
    result = analyzer.analyze_monthly_data(wind_data, 'veracruz', 3)
    
    print("\n📊 RESULTADOS:")
    print(f"Velocidad promedio: {result['avg_wind_speed']} km/h")
    print(f"Categoría: {result['wind_category']}")
    print(f"Probabilidad viento fuerte (>40 km/h): {result['prob_strong_wind']}%")
    print(f"Nivel de riesgo: {result['risk_level'][0]}")
    
    date = datetime(2024, 3, 15)
    message = analyzer.get_wind_forecast_message(result, date)
    print(f"\n💬 MENSAJE:\n{message}")
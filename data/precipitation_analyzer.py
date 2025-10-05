# data/precipitation_analyzer.py
"""
Analizador de Precipitación Diaria
===================================
Convierte datos mensuales acumulados de NASA a estimaciones diarias.

POR QUÉ EXISTE:
- NASA GIOVANNI da datos MENSUALES (ej: "Mayo 2020: 85mm total")
- El usuario quiere saber probabilidad DIARIA ("15 Mayo: ¿lloverá?")
- Este módulo hace la conversión usando climatología real de México
"""

import numpy as np
import pandas as pd
from datetime import datetime

class PrecipitationAnalyzer:
    """
    Transforma precipitación mensual → análisis diario
    """
    
    def __init__(self):
        """
        Inicializa con patrones climatológicos de México
        
        POR QUÉ ESTOS DATOS:
        Basados en estadísticas del Servicio Meteorológico Nacional (SMN)
        que indican cuántos días LLUEVE en promedio cada mes en cada región
        """
        
        # Días lluviosos promedio por mes en cada ciudad
        # Fuente: SMN - Normales Climatológicas
        self.rainy_days_patterns = {
            'veracruz': {  # Costa del Golfo - húmedo
                1: 8, 2: 6, 3: 5, 4: 4, 5: 6, 6: 12,
                7: 14, 8: 14, 9: 14, 10: 10, 11: 9, 12: 8
            },
            'cdmx': {  # Altiplano - lluvia en verano
                1: 3, 2: 3, 3: 4, 4: 6, 5: 10, 6: 15,
                7: 18, 8: 18, 9: 16, 10: 8, 11: 4, 12: 2
            },
            'cancun': {  # Caribe - tropical
                1: 6, 2: 4, 3: 3, 4: 3, 5: 6, 6: 10,
                7: 10, 8: 11, 9: 14, 10: 12, 11: 8, 12: 7
            },
            'monterrey': {  # Norte semiárido
                1: 4, 2: 3, 3: 3, 4: 4, 5: 6, 6: 7,
                7: 6, 8: 7, 9: 8, 10: 6, 11: 4, 12: 4
            },
            'tijuana': {  # Mediterráneo - lluvia en invierno
                1: 6, 2: 6, 3: 6, 4: 3, 5: 2, 6: 1,
                7: 1, 8: 1, 9: 2, 10: 3, 11: 4, 12: 6
            }
        }
        
        # Días en cada mes
        self.days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
    
    def analyze_monthly_data(self, monthly_precip_values, city_key, month):
        """
        FUNCIÓN PRINCIPAL: Analiza datos mensuales y calcula estadísticas diarias
        
        CÓMO FUNCIONA:
        1. Recibe: array de precipitación mensual de 30+ años
           Ejemplo: [85mm, 92mm, 78mm, 105mm, ...] (uno por año)
        
        2. Calcula:
           - ¿En cuántos años llovió significativamente?
           - ¿Cuántos días llueve típicamente en este mes? (climatología)
           - Probabilidad de que llueva UN DÍA específico
           - Si llueve, ¿cuántos mm caen ese día?
        
        Args:
            monthly_precip_values: numpy array con mm mensuales (1 valor por año)
            city_key: 'veracruz', 'cdmx', 'cancun', 'monterrey', 'tijuana'
            month: mes (1-12)
        
        Returns:
            dict con todas las estadísticas diarias
        """
        
        # Validar entrada
        if monthly_precip_values is None or len(monthly_precip_values) == 0:
            return None
        
        # Filtrar valores válidos
        monthly_precip_values = monthly_precip_values[monthly_precip_values >= 0]
        
        if len(monthly_precip_values) == 0:
            return None
        
        # ==========================================
        # PASO 1: ¿En cuántos años llovió?
        # ==========================================
        # Consideramos "lluvia significativa" si cayeron >5mm en el mes
        years_with_rain = np.sum(monthly_precip_values > 5)
        total_years = len(monthly_precip_values)
        prob_rain_in_month = years_with_rain / total_years
        
        # ==========================================
        # PASO 2: Días lluviosos según climatología
        # ==========================================
        # De los patrones del SMN, ¿cuántos días llueve en este mes?
        expected_rainy_days = self.rainy_days_patterns.get(city_key, {}).get(month, 10)
        total_days = self.days_in_month[month]
        
        # ==========================================
        # PASO 3: Probabilidad de lluvia POR DÍA
        # ==========================================
        # Lógica:
        # - Si llueve 12 días de 30 → P(lluvia en un día) = 12/30 = 40%
        # - Pero ajustamos por frecuencia histórica (no todos los años llueve igual)
        prob_rain_per_day = expected_rainy_days / total_days
        prob_rain_per_day_adjusted = prob_rain_per_day * prob_rain_in_month
        
        # ==========================================
        # PASO 4: Intensidad cuando LLUEVE
        # ==========================================
        # Solo consideramos años con lluvia significativa
        rainy_months = monthly_precip_values[monthly_precip_values > 5]
        
        if len(rainy_months) > 0:
            # Precipitación promedio en meses lluviosos
            avg_precip_when_rains = np.mean(rainy_months)
            
            # CLAVE: Distribuir el total mensual entre los días lluviosos
            # Ejemplo: Si en mayo caen 120mm en 12 días → 120/12 = 10mm/día
            avg_precip_per_rainy_day = avg_precip_when_rains / expected_rainy_days
            
            # Calcular variabilidad
            std_precip_monthly = np.std(rainy_months)
            std_precip_daily = std_precip_monthly / np.sqrt(expected_rainy_days)
            
            # Rango típico (percentiles aproximados)
            p25_daily = max(0, avg_precip_per_rainy_day - std_precip_daily)
            p75_daily = avg_precip_per_rainy_day + std_precip_daily
        else:
            # No hay datos de lluvia
            avg_precip_per_rainy_day = 0
            p25_daily = 0
            p75_daily = 0
        
        # ==========================================
        # PASO 5: Categorizar intensidad
        # ==========================================
        intensity_category = self._categorize_intensity(avg_precip_per_rainy_day)
        
        # ==========================================
        # RETORNAR RESULTADOS COMPLETOS
        # ==========================================
        return {
            # ===== PARA EL USUARIO =====
            'probability_rain_day': round(prob_rain_per_day_adjusted * 100, 1),  # % de lluvia ESE DÍA
            'avg_mm_per_rainy_day': round(avg_precip_per_rainy_day, 1),  # mm si llueve
            'range_mm_per_day': (round(p25_daily, 1), round(p75_daily, 1)),  # rango
            'intensity_category': intensity_category,  # "Lluvia moderada", etc.
            
            # ===== CONTEXTO =====
            'probability_rain_month': round(prob_rain_in_month * 100, 1),  # % de que llueva EN EL MES
            'expected_rainy_days_per_month': expected_rainy_days,
            'total_days_in_month': total_days,
            
            # ===== DATOS HISTÓRICOS =====
            'historical_years_analyzed': total_years,
            'years_with_significant_rain': int(years_with_rain),
            'avg_monthly_precip': round(np.mean(monthly_precip_values), 1),
            'max_monthly_precip': round(np.max(monthly_precip_values), 1),
            'min_monthly_precip': round(np.min(monthly_precip_values), 1)
        }
    
    def _categorize_intensity(self, mm_per_day):
        """
        Categoriza intensidad según mm/día
        
        Escala basada en SMN:
        - <2mm: Llovizna
        - 2-5mm: Lluvia ligera
        - 5-15mm: Lluvia moderada
        - 15-30mm: Lluvia fuerte
        - >30mm: Lluvia muy fuerte/torrencial
        """
        if mm_per_day < 2:
            return "Llovizna ligera"
        elif mm_per_day < 5:
            return "Lluvia ligera"
        elif mm_per_day < 15:
            return "Lluvia moderada"
        elif mm_per_day < 30:
            return "Lluvia fuerte"
        else:
            return "Lluvia muy fuerte"
    
    def get_rain_forecast_message(self, analysis, date):
        """
        Genera mensaje amigable para el usuario
        
        POR QUÉ:
        En lugar de mostrar solo números, creamos un mensaje descriptivo
        que el usuario pueda entender fácilmente.
        
        Args:
            analysis: dict resultado de analyze_monthly_data
            date: datetime del día consultado
        
        Returns:
            str mensaje listo para mostrar
        """
        if not analysis:
            return "No hay datos suficientes para esta fecha"
        
        prob = analysis['probability_rain_day']
        avg_mm = analysis['avg_mm_per_rainy_day']
        intensity = analysis['intensity_category']
        
        month_name = date.strftime('%B')
        
        # Construir mensaje según probabilidad
        if prob < 10:
            message = f"☀️ **Muy baja probabilidad de lluvia** ({prob:.2f}%) en {month_name}.\n\n"
            message += "Es muy probable que tengas un día seco. Perfecto para actividades al aire libre."
        
        elif prob < 30:
            message = f"🌤️ **Baja probabilidad de lluvia** ({prob:.2f}%) en {month_name}.\n\n"
            message += f"Si llegara a llover, se esperan **{avg_mm}mm** ({intensity.lower()}).\n"
            message += "Lleva un paraguas ligero por si acaso."
        
        elif prob < 60:
            message = f"⛅ **Probabilidad moderada de lluvia** ({prob:.2f}%) en {month_name}.\n\n"
            message += f"Si llueve, se esperan **{avg_mm}mm** ({intensity.lower()}).\n"
            message += f"Rango típico: {analysis['range_mm_per_day'][0]}-{analysis['range_mm_per_day'][1]}mm\n\n"
            message += "Recomendación: Ten plan B para actividades."
        
        else:
            message = f"🌧️ **Alta probabilidad de lluvia** ({prob:.2f}%) en {month_name}.\n\n"
            message += f"Se esperan **{avg_mm}mm** de precipitación ({intensity.lower()}).\n"
            message += f"Rango típico: {analysis['range_mm_per_day'][0]}-{analysis['range_mm_per_day'][1]}mm\n\n"
            message += f"📊 Históricamente, llueve ~{analysis['expected_rainy_days_per_month']} días en este mes.\n"
            message += "Recomendación: Lleva impermeable y planea actividades bajo techo."
        
        return message


# ============================================
# FUNCIÓN DE INTEGRACIÓN
# ============================================
def integrate_with_processor(processor, precipitation_analyzer, lat, lon, month, day):
    """
    FUNCIÓN PUENTE: Conecta tu procesador existente con el analizador nuevo
    
    POR QUÉ:
    Tu procesador (csv_processor.py) ya obtiene datos mensuales.
    Esta función toma esos datos y los pasa al analizador para 
    convertirlos en probabilidades diarias.
    
    Args:
        processor: tu CSVProcessor o CSVProcessorOptimized
        precipitation_analyzer: instancia de PrecipitationAnalyzer
        lat, lon: coordenadas
        month, day: fecha
    
    Returns:
        dict con análisis completo listo para mostrar
    """
    # 1. Obtener datos mensuales históricos de tu procesador
    precip_values, city_name = processor.get_historical_data(
        lat, lon, 'precipitacion', month, day
    )
    
    if precip_values is None:
        return None
    
    # 2. Determinar qué ciudad es
    city_key = processor.find_nearest_city(lat, lon)[0]
    
    # 3. Analizar con el nuevo analizador
    date = datetime(2024, month, day)
    
    analysis = precipitation_analyzer.analyze_monthly_data(
        precip_values, city_key, month
    )
    
    # 4. Agregar mensaje y nombre de ciudad
    if analysis:
        analysis['message'] = precipitation_analyzer.get_rain_forecast_message(
            analysis, date
        )
        analysis['city_name'] = city_name
    
    return analysis


# ============================================
# PRUEBA
# ============================================
if __name__ == "__main__":
    print("\n🧪 PROBANDO PRECIPITATION ANALYZER")
    print("=" * 70)
    
    # Simular 33 a  ños de datos mensuales de Veracruz en Junio
    monthly_data = np.array([
        120, 145, 98, 156, 134, 189, 145, 167, 201, 178, 
        156, 134, 145, 123, 198, 167, 145, 134, 156, 178, 
        145, 167, 189, 134, 156, 145, 178, 167, 145, 134, 
        156, 189, 178
    ])
    
    analyzer = PrecipitationAnalyzer()
    result = analyzer.analyze_monthly_data(monthly_data, 'veracruz', 6)
    
    print("\n📊 RESULTADOS:")
    print(f"Probabilidad de lluvia ese día: {result['probability_rain_day']}%")
    print(f"Si llueve, caerán: {result['avg_mm_per_rainy_day']} mm")
    print(f"Categoría: {result['intensity_category']}")
    print(f"Rango: {result['range_mm_per_day'][0]}-{result['range_mm_per_day'][1]} mm")
    
    date = datetime(2024, 6, 15)
    message = analyzer.get_rain_forecast_message(result, date)
    print(f"\n💬 MENSAJE:\n{message}")
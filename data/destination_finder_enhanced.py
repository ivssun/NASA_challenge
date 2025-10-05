# data/destination_finder_enhanced.py
"""
Sistema MEJORADO de búsqueda de destinos por clima
Versión optimizada para NASA Space Apps Challenge 2024
Integración completa con datos GIOVANNI de 5 variables
"""

import numpy as np
from datetime import datetime
from config.settings import CIUDADES_NASA, VARIABLES

class DestinationFinderEnhanced:
    """
    Buscador de destinos mejorado con más condiciones climáticas
    y mejor análisis de datos históricos NASA
    """
    
    # ============================================
    # CONDICIONES CLIMÁTICAS AMPLIADAS
    # ============================================
    CLIMATE_CONDITIONS = {
        'nevado': {
            'nombre': '❄️ Clima Nevado/Frío Extremo',
            'descripcion': 'Temperaturas muy bajas con alta probabilidad de nieve o lluvia intensa. Ideal para turismo invernal.',
            'icon': '🏔️',
            'color': '#60A5FA',
            'conditions': {
                'temperatura': {'max': 8, 'operator': 'less'},
                'precipitacion': {'min': 20, 'operator': 'greater'},
                'nubosidad': {'min': 60, 'operator': 'greater'}
            },
            'months': [11, 12, 1, 2, 3]  # Meses más probables
        },
        
        'frio_seco': {
            'nombre': '🌨️ Clima Frío y Seco',
            'descripcion': 'Temperaturas bajas sin precipitación, cielos despejados. Perfecto para montañismo.',
            'icon': '🌨️',
            'color': '#93C5FD',
            'conditions': {
                'temperatura': {'max': 12, 'operator': 'less'},
                'precipitacion': {'max': 10, 'operator': 'less'},
                'nubosidad': {'max': 40, 'operator': 'less'}
            },
            'months': [11, 12, 1, 2]
        },
        
        'templado_perfecto': {
            'nombre': '🌤️ Clima Templado Ideal',
            'descripcion': 'Temperaturas agradables (15-25°C) con poca lluvia y cielos despejados. Perfecto para turismo.',
            'icon': '🌤️',
            'color': '#34D399',
            'conditions': {
                'temperatura': {'min': 15, 'max': 25, 'operator': 'between'},
                'precipitacion': {'max': 15, 'operator': 'less'},
                'nubosidad': {'max': 50, 'operator': 'less'},
                'humedad': {'max': 70, 'operator': 'less'}
            },
            'months': [3, 4, 5, 9, 10, 11]
        },
        
        'calido_soleado': {
            'nombre': '☀️ Clima Cálido y Soleado',
            'descripcion': 'Temperaturas altas (>28°C) con cielos despejados y baja humedad. Ideal para playa.',
            'icon': '☀️',
            'color': '#FBBF24',
            'conditions': {
                'temperatura': {'min': 28, 'operator': 'greater'},
                'nubosidad': {'max': 40, 'operator': 'less'},
                'precipitacion': {'max': 20, 'operator': 'less'}
            },
            'months': [4, 5, 6, 7, 8]
        },
        
        'playa_tropical': {
            'nombre': '🏖️ Clima Tropical de Playa',
            'descripcion': 'Cálido (26-32°C), húmedo y con viento suave. El clima perfecto de playa caribeña.',
            'icon': '🏖️',
            'color': '#F87171',
            'conditions': {
                'temperatura': {'min': 26, 'max': 32, 'operator': 'between'},
                'humedad': {'min': 60, 'max': 85, 'operator': 'between'},
                'nubosidad': {'max': 60, 'operator': 'less'},
                'viento': {'max': 30, 'operator': 'less'}
            },
            'months': [3, 4, 5, 6, 11, 12]
        },
        
        'lluvioso_tropical': {
            'nombre': '🌧️ Clima Lluvioso Tropical',
            'descripcion': 'Alta probabilidad de lluvias intensas. Exuberante vegetación.',
            'icon': '🌧️',
            'color': '#3B82F6',
            'conditions': {
                'precipitacion': {'min': 40, 'operator': 'greater'},
                'humedad': {'min': 75, 'operator': 'greater'},
                'nubosidad': {'min': 70, 'operator': 'greater'}
            },
            'months': [6, 7, 8, 9, 10]
        },
        
        'ventoso_extremo': {
            'nombre': '💨 Clima Ventoso',
            'descripcion': 'Vientos fuertes (>35 km/h). Ideal para windsurf, kitesurf y deportes de viento.',
            'icon': '💨',
            'color': '#06B6D4',
            'conditions': {
                'viento': {'min': 35, 'operator': 'greater'}
            },
            'months': [11, 12, 1, 2, 3]
        },
        
        'desertico_extremo': {
            'nombre': '🌵 Clima Desértico Extremo',
            'descripcion': 'Muy caluroso (>35°C), extremadamente seco y soleado. Aventura en el desierto.',
            'icon': '🌵',
            'color': '#F59E0B',
            'conditions': {
                'temperatura': {'min': 35, 'operator': 'greater'},
                'precipitacion': {'max': 5, 'operator': 'less'},
                'humedad': {'max': 30, 'operator': 'less'},
                'nubosidad': {'max': 20, 'operator': 'less'}
            },
            'months': [5, 6, 7, 8]
        }
    }
    
    def __init__(self, processor):
        """
        Args:
            processor: Instancia de CSVProcessorOptimized con datos cargados
        """
        self.processor = processor
    
    def find_destinations(self, target_date, climate_condition, min_probability=10):
        """
        Busca destinos que cumplan con una condición climática específica
        
        Args:
            target_date: Fecha objetivo (datetime o date)
            climate_condition: Tipo de clima deseado (key de CLIMATE_CONDITIONS)
            min_probability: Probabilidad mínima para filtrar resultados (%)
            
        Returns:
            Lista de destinos ordenados por probabilidad (mayor a menor)
        """
        if climate_condition not in self.CLIMATE_CONDITIONS:
            return []
        
        condition_info = self.CLIMATE_CONDITIONS[climate_condition]
        conditions = condition_info['conditions']
        
        # Extraer mes y día
        if isinstance(target_date, datetime):
            month = target_date.month
            day = target_date.day
        else:
            month = target_date.month
            day = target_date.day
        
        results = []
        
        # Analizar cada ciudad
        for city_key, city_info in CIUDADES_NASA.items():
            city_result = {
                'city_key': city_key,
                'city_name': city_info['name'],
                'city_info': city_info,
                'probabilities': {},
                'average_values': {},
                'overall_probability': 0.0
            }
            
            variable_probabilities = []
            
            # Evaluar cada condición
            for var_key, condition in conditions.items():
                # Obtener datos históricos
                values, _ = self.processor.get_historical_data(
                    city_info['lat'], 
                    city_info['lon'], 
                    var_key, 
                    month, 
                    day
                )
                
                if values is None or len(values) == 0:
                    continue
                
                # Calcular promedio para mostrar
                city_result['average_values'][var_key] = round(float(np.mean(values)), 1)
                
                # Calcular probabilidad según el operador
                operator = condition['operator']
                probability = 0.0
                
                if operator == 'less':
                    threshold = condition['max']
                    probability = self.processor.calculate_probability(
                        values, threshold, 'less'
                    ) * 100
                    
                elif operator == 'greater':
                    threshold = condition['min']
                    probability = self.processor.calculate_probability(
                        values, threshold, 'greater'
                    ) * 100
                    
                elif operator == 'between':
                    min_val = condition['min']
                    max_val = condition['max']
                    count_in_range = np.sum((values >= min_val) & (values <= max_val))
                    probability = (count_in_range / len(values)) * 100
                
                city_result['probabilities'][var_key] = round(probability, 1)
                variable_probabilities.append(probability)
            
            # Calcular probabilidad general
            # Usamos promedio ponderado: las variables críticas pesan más
            if variable_probabilities:
                city_result['overall_probability'] = round(
                    np.mean(variable_probabilities), 1
                )
                
                # BONUS: Si el mes está en los meses favorables, aumentar probabilidad
                if 'months' in condition_info and month in condition_info['months']:
                    city_result['overall_probability'] = min(
                        100, 
                        city_result['overall_probability'] * 1.15
                    )
                    city_result['seasonal_bonus'] = True
                else:
                    city_result['seasonal_bonus'] = False
            
            # Filtrar por probabilidad mínima
            if city_result['overall_probability'] >= min_probability:
                results.append(city_result)
        
        # Ordenar por probabilidad descendente
        results.sort(key=lambda x: x['overall_probability'], reverse=True)
        
        return results
    
    def get_condition_info(self, climate_condition):
        """Obtiene información detallada de una condición climática"""
        return self.CLIMATE_CONDITIONS.get(climate_condition, None)
    
    def get_all_conditions(self):
        """Retorna todas las condiciones climáticas disponibles"""
        return self.CLIMATE_CONDITIONS
    
    def get_recommended_months(self, climate_condition):
        """Retorna los meses recomendados para una condición climática"""
        if climate_condition in self.CLIMATE_CONDITIONS:
            return self.CLIMATE_CONDITIONS[climate_condition].get('months', [])
        return []
    
    def analyze_specific_destination(self, city_key, target_date, climate_condition):
        """
        Análisis detallado de un destino específico para una condición climática
        
        Args:
            city_key: Clave de la ciudad (ej: 'veracruz')
            target_date: Fecha objetivo
            climate_condition: Tipo de clima deseado
            
        Returns:
            Dict con análisis detallado
        """
        if city_key not in CIUDADES_NASA:
            return None
        
        if climate_condition not in self.CLIMATE_CONDITIONS:
            return None
        
        city_info = CIUDADES_NASA[city_key]
        condition_info = self.CLIMATE_CONDITIONS[climate_condition]
        
        month = target_date.month if hasattr(target_date, 'month') else target_date.month
        day = target_date.day if hasattr(target_date, 'day') else target_date.day
        
        analysis = {
            'city_name': city_info['name'],
            'condition_name': condition_info['nombre'],
            'variables': {},
            'overall_score': 0.0,
            'recommendation': ''
        }
        
        scores = []
        
        for var_key, condition in condition_info['conditions'].items():
            values, _ = self.processor.get_historical_data(
                city_info['lat'], city_info['lon'], var_key, month, day
            )
            
            if values is None:
                continue
            
            stats = self.processor.get_statistics(values)
            
            # Calcular probabilidad
            operator = condition['operator']
            if operator == 'less':
                prob = self.processor.calculate_probability(
                    values, condition['max'], 'less'
                ) * 100
            elif operator == 'greater':
                prob = self.processor.calculate_probability(
                    values, condition['min'], 'greater'
                ) * 100
            else:  # between
                count = np.sum((values >= condition['min']) & (values <= condition['max']))
                prob = (count / len(values)) * 100
            
            analysis['variables'][var_key] = {
                'average': round(stats['mean'], 1),
                'min': round(stats['min'], 1),
                'max': round(stats['max'], 1),
                'probability': round(prob, 1),
                'condition': condition
            }
            
            scores.append(prob)
        
        if scores:
            analysis['overall_score'] = round(np.mean(scores), 1)
            
            # Generar recomendación
            if analysis['overall_score'] >= 70:
                analysis['recommendation'] = '🌟 Excelente elección'
            elif analysis['overall_score'] >= 50:
                analysis['recommendation'] = '✅ Buena opción'
            elif analysis['overall_score'] >= 30:
                analysis['recommendation'] = '⚠️ Opción moderada'
            else:
                analysis['recommendation'] = '❌ No recomendado'
        
        return analysis


def integrate_destination_finder_enhanced(processor):
    """
    Función helper para integrar el buscador mejorado
    
    Args:
        processor: Instancia de CSVProcessorOptimized
        
    Returns:
        Instancia de DestinationFinderEnhanced
    """
    return DestinationFinderEnhanced(processor)
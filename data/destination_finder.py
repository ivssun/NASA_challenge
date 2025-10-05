# data/destination_finder.py
"""
Sistema de búsqueda de destinos basado en condiciones climáticas reales
Utiliza datos históricos de NASA GIOVANNI para calcular probabilidades
"""

import numpy as np
from datetime import datetime
from config.settings import CIUDADES_NASA, VARIABLES

class DestinationFinder:
    """
    Encuentra los mejores destinos basándose en condiciones climáticas deseadas
    """
    
    # Definición de condiciones climáticas
    CLIMATE_CONDITIONS = {
        'frio_nevado': {
            'nombre': '❄️ Clima Frío/Nevado',
            'descripcion': 'Temperaturas bajas con posibilidad de nieve o lluvia invernal',
            'icon': '🏔️',
            'color': '#60A5FA',
            'conditions': {
                'temperatura': {'max': 10, 'operator': 'less'},
                'precipitacion': {'min': 15, 'operator': 'greater'}
            }
        },
        'templado_seco': {
            'nombre': '🌤️ Clima Templado Seco',
            'descripcion': 'Temperaturas agradables con poca lluvia',
            'icon': '🌤️',
            'color': '#34D399',
            'conditions': {
                'temperatura': {'min': 15, 'max': 25, 'operator': 'between'},
                'precipitacion': {'max': 20, 'operator': 'less'},
                'nubosidad': {'max': 50, 'operator': 'less'}
            }
        },
        'calido_soleado': {
            'nombre': '☀️ Clima Cálido y Soleado',
            'descripcion': 'Temperaturas altas con cielos despejados',
            'icon': '☀️',
            'color': '#FBBF24',
            'conditions': {
                'temperatura': {'min': 28, 'operator': 'greater'},
                'nubosidad': {'max': 40, 'operator': 'less'}
            }
        },
        'playa_ideal': {
            'nombre': '🏖️ Clima de Playa Ideal',
            'descripcion': 'Cálido, húmedo y con poco nublado - perfecto para playa',
            'icon': '🏖️',
            'color': '#F87171',
            'conditions': {
                'temperatura': {'min': 26, 'operator': 'greater'},
                'humedad': {'min': 60, 'operator': 'greater'},
                'nubosidad': {'max': 50, 'operator': 'less'}
            }
        },
        'lluvioso': {
            'nombre': '🌧️ Clima Lluvioso',
            'descripcion': 'Alta probabilidad de precipitación',
            'icon': '🌧️',
            'color': '#3B82F6',
            'conditions': {
                'precipitacion': {'min': 30, 'operator': 'greater'}
            }
        },
        'ventoso': {
            'nombre': '💨 Clima Ventoso',
            'descripcion': 'Vientos fuertes - ideal para deportes de viento',
            'icon': '💨',
            'color': '#06B6D4',
            'conditions': {
                'viento': {'min': 25, 'operator': 'greater'}
            }
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
            target_date: Fecha objetivo (datetime)
            climate_condition: Tipo de clima deseado (key de CLIMATE_CONDITIONS)
            min_probability: Probabilidad mínima para filtrar (%)
            
        Returns:
            Lista de destinos ordenados por probabilidad descendente
        """
        if climate_condition not in self.CLIMATE_CONDITIONS:
            raise ValueError(f"Condición climática '{climate_condition}' no reconocida")
        
        condition_info = self.CLIMATE_CONDITIONS[climate_condition]
        conditions = condition_info['conditions']
        
        results = []
        month = target_date.month
        day = target_date.day
        
        # Analizar cada ciudad NASA
        for city_key, city_info in CIUDADES_NASA.items():
            lat = city_info['lat']
            lon = city_info['lon']
            
            city_result = {
                'city_key': city_key,
                'city_name': city_info['name'],
                'city_info': city_info,
                'probabilities': {},
                'average_values': {},
                'overall_probability': 0,
                'meets_conditions': True
            }
            
            variable_probabilities = []
            
            # Evaluar cada condición de la variable
            for var_key, condition in conditions.items():
                # Obtener datos históricos
                values, detected_city = self.processor.get_historical_data(
                    lat, lon, var_key, month, day
                )
                
                if values is None or len(values) == 0:
                    city_result['meets_conditions'] = False
                    continue
                
                avg_value = float(np.mean(values))
                city_result['average_values'][var_key] = round(avg_value, 1)
                
                # Calcular probabilidad según el operador
                operator = condition['operator']
                probability = 0
                
                if operator == 'less':
                    threshold = condition['max']
                    probability = self.processor.calculate_probability(
                        values, threshold, 'less'
                    )
                elif operator == 'greater':
                    threshold = condition['min']
                    probability = self.processor.calculate_probability(
                        values, threshold, 'greater'
                    )
                elif operator == 'between':
                    min_val = condition['min']
                    max_val = condition['max']
                    # Contar valores dentro del rango
                    count_in_range = np.sum((values >= min_val) & (values <= max_val))
                    probability = (count_in_range / len(values)) * 100
                
                city_result['probabilities'][var_key] = round(probability, 1)
                variable_probabilities.append(probability)
            
            # Calcular probabilidad general (promedio de todas las condiciones)
            if variable_probabilities:
                city_result['overall_probability'] = round(
                    np.mean(variable_probabilities), 1
                )
            
            # Filtrar por probabilidad mínima
            if city_result['overall_probability'] >= min_probability:
                results.append(city_result)
        
        # Ordenar por probabilidad descendente
        results.sort(key=lambda x: x['overall_probability'], reverse=True)
        
        return results
    
    def get_condition_info(self, climate_condition):
        """Obtiene información de una condición climática"""
        return self.CLIMATE_CONDITIONS.get(climate_condition, None)
    
    def get_all_conditions(self):
        """Retorna todas las condiciones climáticas disponibles"""
        return self.CLIMATE_CONDITIONS


def integrate_destination_finder(processor):
    """
    Función helper para integrar el buscador de destinos con el procesador
    
    Args:
        processor: Instancia de CSVProcessorOptimized
        
    Returns:
        Instancia de DestinationFinder
    """
    return DestinationFinder(processor)

# diagnostico_nubosidad.py
"""
Script de diagnóstico para detectar y corregir problemas con datos de nubosidad
"""

import pandas as pd
import os

def diagnosticar_nubosidad():
    print("\n" + "="*70)
    print("DIAGNÓSTICO DE DATOS DE NUBOSIDAD")
    print("="*70 + "\n")
    
    csv_folder = 'data/csv'
    ciudades = ['veracruz', 'cdmx', 'cancun', 'monterrey', 'tijuana']
    
    resultados = {}
    
    for ciudad in ciudades:
        filepath = os.path.join(csv_folder, f'MODIS_{ciudad}.csv')
        
        if not os.path.exists(filepath):
            print(f"⚠️  {ciudad}: Archivo no encontrado")
            continue
        
        try:
            df = pd.read_csv(filepath, skiprows=9)
            valores = df.iloc[:, 1]  # Segunda columna
            
            min_val = valores.min()
            max_val = valores.max()
            mean_val = valores.mean()
            
            resultados[ciudad] = {
                'min': min_val,
                'max': max_val,
                'mean': mean_val
            }
            
            print(f"📊 {ciudad.upper()}:")
            print(f"   Mínimo: {min_val:.4f}")
            print(f"   Máximo: {max_val:.4f}")
            print(f"   Promedio: {mean_val:.4f}")
            print()
        
        except Exception as e:
            print(f"❌ {ciudad}: Error - {e}\n")
    
    # Analizar rango general
    if resultados:
        max_global = max(r['max'] for r in resultados.values())
        min_global = min(r['min'] for r in resultados.values())
        
        print("="*70)
        print("DIAGNÓSTICO:")
        print("="*70)
        
        if max_global <= 1.0:
            print("✅ Formato detectado: FRACCIÓN (0-1)")
            print("   Conversión necesaria: multiplicar por 100")
            factor = 100
        elif max_global <= 100:
            print("✅ Formato detectado: PORCENTAJE (0-100)")
            print("   Conversión necesaria: NINGUNA")
            factor = 1
        else:
            print("⚠️  Formato detectado: CON FACTOR DE ESCALA")
            print(f"   Valor máximo: {max_global}")
            # Calcular factor aproximado
            factor = 1 / (max_global / 100)
            print(f"   Conversión sugerida: multiplicar por {factor:.6f}")
        
        print("="*70)
        return factor
    else:
        print("❌ No se encontraron archivos MODIS")
        return None

if __name__ == "__main__":
    factor_correccion = diagnosticar_nubosidad()
    
    if factor_correccion is not None:
        print(f"\n💡 ACCIÓN REQUERIDA:")
        print(f"   Modificar csv_processor_optimized.py")
        print(f"   Cambiar: df[var] = df[var] * 100")
        print(f"   Por: df[var] = df[var] * {factor_correccion}")
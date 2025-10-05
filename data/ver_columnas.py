import pandas as pd

# Leer uno de los CSVs
df = pd.read_csv('data/csv/temperatura_cdmx.csv')

print("\n📋 COLUMNAS DEL CSV:")
print("=" * 70)
for col in df.columns:
    print(f"  - {col}")

print("\n📊 PRIMERAS 5 FILAS:")
print(df.head())

print("\n📈 INFO DEL DATAFRAME:")
print(df.info())
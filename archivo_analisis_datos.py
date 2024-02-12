import pandas as pd
import json

def cargar_mapeo(ruta_json):

    with open(ruta_json, 'r') as archivo:
        mapeo = json.load(archivo)
    return {col: {int(k): v for k, v in submap.items()} for col, submap in mapeo.items()}

def normalizar_datos(df, mapeo):

    for columna, mapeo_columna in mapeo.items():
        if columna in df.columns:
            df[columna] = df[columna].map(mapeo_columna).fillna(df[columna])
    return df

def main():
    ruta_csv = './personas.csv'  
    ruta_json = './mapeo_codigos.json'  

    try:
        datos = pd.read_csv(ruta_csv)
        mapeo = cargar_mapeo(ruta_json)
        # print(mapeo)
        datos_normalizados = normalizar_datos(datos, mapeo)
        print("Datos normalizados con éxito.")
        
        ruta_salida_csv = './datos_normalizados.csv'  
        datos_normalizados.to_csv(ruta_salida_csv, index=False)
        print(f"Datos normalizados guardados en {ruta_salida_csv}")
    except Exception as e:
        print(f"Error al procesar los datos: {e}")

if __name__ == "__main__":
    main()

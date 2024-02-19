import os
import json
import pandas as pd
from typing import List, Dict, Any

def read_json_files(folder_path: str) -> List[Dict[str, Any]]:
    """
    Lee todos los archivos JSON en la carpeta especificada y extrae los datos relevantes.
    
    :param folder_path: Ruta de la carpeta que contiene los archivos JSON.
    :return: Lista de diccionarios con los datos extraídos de cada archivo JSON.
    """
    data_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r') as file:
                    json_data = json.load(file)
                    data = extract_data(json_data)
                    data_list.append(data)
            except Exception as e:
                print(f"Error al leer {file_path}: {e}")
    return data_list

def extract_data(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae los datos relevantes de un objeto JSON de una encuesta.
    
    :param json_data: Objeto JSON cargado de un archivo.
    :return: Diccionario con los datos relevantes extraídos.
    """
    return {
        'file_id': json_data.get('file_id', ''),
        'label': json_data.get('labl', ''),
        'question_text': json_data.get('var_qstn_qstnlit', ''),
        'universe': json_data.get('var_universe', ''),
        'response_options': {category['value']: category['labl'] for category in json_data.get('var_catgry', [])},
        'min_value': json_data.get('var_val_range', {}).get('min', ''),
        'max_value': json_data.get('var_val_range', {}).get('max', ''),
        'survey_id': json_data.get('survey_idno', '')
    }

def generate_excel(data_list: List[Dict[str, Any]], output_path: str) -> None:
    """
    Genera un archivo Excel a partir de una lista de diccionarios con datos de encuestas.
    
    :param data_list: Lista de diccionarios con los datos de las encuestas.
    :param output_path: Ruta del archivo Excel de salida.
    """
    df = pd.DataFrame(data_list)
    try:
        df.to_excel(output_path, index=False)
        print(f"Archivo Excel generado con éxito en: {output_path}")
    except Exception as e:
        print(f"Error al generar el archivo Excel: {e}")

# Ruta de la carpeta que contiene los archivos JSON (ajustar según sea necesario)
folder_path = './datos'

# Ruta del archivo Excel de salida (ajustar según sea necesario)
excel_output_path = './output/survey_questions.xlsx'

# Proceso principal
if __name__ == "__main__":
    data_list = read_json_files(folder_path)
    generate_excel(data_list, excel_output_path)

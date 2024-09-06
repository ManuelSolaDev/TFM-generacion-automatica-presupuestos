import os
import yaml
import pandas as pd

    

def load_config(file_path):
    # Define default values
    default_values = {
        'SERPER_API_KEY': 'default_serper_api_key',
        'SERPER_API_KEY': 'default_groq_api_key',
        'OPENAI_API_KEY': 'default_openai_api_key',
    }
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            if not value:
                os.environ[key] = default_values.get(key, '')
            else:
                os.environ[key] = value


def check_for_content(var):
    if var:
        try:
            var = var.content
            return var.content
        except:
            return var
    else:
        var


def create_excel_from_budget(llm_response):
    # Extraemos la información de la respuesta del LLM
    resumen = llm_response.resumen
    total_horas = llm_response.total_horas
    total_costo = llm_response.total_costo
    total_costo_con_margen_adicional = llm_response.total_costo_con_margen_adicional
    consideraciones = llm_response.consideraciones

    # Creamos una lista de diccionarios para los gastos
    datos_gastos = []
    for gasto in llm_response.gastos:
        datos_gastos.append({
            "Área": gasto.area,
            "Nombre del Gasto": gasto.nombre,
            "Descripción": gasto.descripcion,
            "Horas": gasto.horas,
            "Costo": gasto.costo
        })

    # Creamos el DataFrame para los gastos
    df_gastos = pd.DataFrame(datos_gastos)

    # Creamos un DataFrame para el resumen general
    df_resumen = pd.DataFrame({
        "Resumen": [resumen],
        "Total Horas": [total_horas],
        "Total Costo": [total_costo],
        "Total Costo con Margen Adicional": [total_costo_con_margen_adicional],
        "Consideraciones": [consideraciones]
    })

    # Escribimos ambos DataFrames a un archivo Excel
    with pd.ExcelWriter('budgets/budget.xlsx', engine='xlsxwriter') as writer:
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
        df_gastos.to_excel(writer, sheet_name='Gastos', index=False)

    print("El archivo Excel ha sido creado con éxito.")
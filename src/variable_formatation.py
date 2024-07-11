import datetime
import numpy as np
import pandas as pd
from parameters import USE_RANGES, FAIXAS_EXTRAVIO, FAIXAS_ATRASO, FAIXAS_DANO

def generate_range(value, interval_values=[]):
    if type(value) == str:
        print("Valor não reconhecido:", value)
        return value
    for i, interval in enumerate(interval_values):
        if value < interval:
            return i
    return len(interval_values)

def hour_to_float(value):
    splits = value.split(":")
    last = len(splits) - 1
    try:
        minutes = float(splits[-last].strip()) / 60
        hours = float(splits[-(last + 1)].strip())
    except:
        print("Valor não reconhecido:", value)
        return 0
    f_value = hours + minutes
    return f_value

def format_comma_strings(value,):
    if ',' in value:
        f_value = float(value.replace(',', '.'))
    else:
        f_value = float(value)
    return f_value

def format_binario(value, anomaly=0, yes=1, no=0):
    if type(value) == float:
        if np.isnan(value):
            return anomaly
    if value in ['S', 's', 'Y', 'y', 'Sim', 'sim', 'SIM', 'YES', 'Yes', 'yes', '1']:
        return yes
    if value in ['N', 'n', 'Não', 'não', 'NÃO', 'NO', 'No', 'no', '0']:
        return no
    if value in ['-', '', ' ']:
        return anomaly

def format_intervalo(value, interval_values=[]):
    if type(value) == int:
        pass
    elif type(value) == float:
        if np.isnan(value):
            value = 0
    elif type(value) == datetime.time or type(value) == datetime.datetime:
        value = float(value.hour + value.minute / 60)
    elif value in ['-', '', ' ', '--']:
        value = 0
    elif ',' in value:
        value = format_comma_strings(value)
    elif ':' in value:
        value = hour_to_float(value)
    elif '.' in value:
        value = float(value)
    else:
        print("Valor não reconhecido:", value)
        return value
    return generate_range(value, interval_values)

FUNCTIONS = {
    'sentença': lambda x: x,
    'direito_de_arrependimento': lambda x: format_binario(x),
    'descumprimento_de_oferta': lambda x: format_binario(x),
    'extravio_definitivo': lambda x: format_binario(x),
    'extravio_temporário': lambda x: format_binario(x),
    'intervalo_extravio_temporário': lambda x: format_intervalo(x, FAIXAS_EXTRAVIO),
    'faixa_intervalo_extravio_temporário': lambda x: int(x),
    'violação_furto_avaria': lambda x: format_binario(x),
    'cancelamento/alteração_destino': lambda x: format_binario(x),
    'atraso': lambda x: format_binario(x),
    'intervalo_atraso': lambda x: format_intervalo(x, FAIXAS_ATRASO),
    'faixa_intervalo_atraso': lambda x: int(x),
    'culpa_exclusiva_consumidor': lambda x: format_binario(x),
    'condições_climáticas/fechamento_aeroporto': lambda x: format_binario(x),
    'noshow': lambda x: format_binario(x),
    'overbooking': lambda x: format_binario(x),
    'assistência_cia_aérea': lambda x: format_binario(x, -1),
    'hipervulnerável': lambda x: format_binario(x),
    'dano_moral_individual': lambda x: format_comma_strings(x, FAIXAS_DANO),
    'faixa_dano_moral_individual': lambda x: int(x)
}

def format_data(csv_file:str):
    df = pd.read_excel(csv_file, engine='openpyxl')
    # Aplicar a função de reformatação aos valores float nas colunas
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(FUNCTIONS[coluna])
    new_file = csv_file.replace(".xlsx", "__NEW.csv")
    df.to_csv(new_file, index=False)
    return df

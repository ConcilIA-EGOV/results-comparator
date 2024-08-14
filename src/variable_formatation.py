import datetime
import numpy as np
import pandas as pd
from parameters import FAIXAS_EXTRAVIO, FAIXAS_ATRASO, FAIXAS_DANO
from parameters import DATA_VARS, USE_RANGES, CREATE_RANGES
# from parameters import SOURCE, TEST, ARQUIVO_DE_SAIDA

def generate_range(value, interval_values=[]):
    if not CREATE_RANGES:
        return value
    if type(value) == str:
        print("Valor não reconhecido ao criar faixas:", value)
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
        print("Valor não reconhecido ao converter para hora:", value)
        return 0
    f_value = hours + minutes
    return f_value

def format_string(value, interval_values=[]):
    if '$' in value:
        value = value.replace('R$ ', '')
    if ',' in value:
        value = value.replace(',', '.')
    if value[-3] == '.':
        value = value[:-3]
        if '.' in value:
            value = value.replace('.', '')
        return int(value)
    try:
        f_value = float(value)   
    except:
        print("Valor não reconhecido ao formatar string:", value)
        return value
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
    elif ':' in value:
        value = hour_to_float(value)
    elif ',' in value or '.' in value:
        value = format_string(value)
    else:
        try:
            value = float(value)
        except:
            print("Valor não reconhecido ao formatar intervalo:", value)
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
    'dano_moral_individual': lambda x: format_intervalo(x, FAIXAS_DANO),
    'faixa_dano_moral_individual': lambda x: int(x)
}

def format_data(excel_file:str):
    df = pd.read_excel(excel_file, engine='openpyxl')
    # Aplicar a função de reformatação aos valores float nas colunas
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(FUNCTIONS[coluna])
    new_file = excel_file.replace(".xlsx", "__NEW.csv")
    df.to_csv(new_file, index=False)
    return df


def trim_columns(df: pd.DataFrame):
    """
    Remove colunas não relacionadas ao experimento
    """
    remove_columns = [col for col in df.columns if col not in DATA_VARS]
    df = df.drop(columns=remove_columns)
    results_columns = "dano_moral_individual"
    if USE_RANGES:
        results_columns = "faixa_dano_moral_individual"
    target_column = df.columns.get_loc(results_columns)
    if target_column != df.shape[1] - 1:
        # Mover a coluna alvo para a última posição
        tc = df.columns[target_column]
        x1 = list(df.columns[:target_column])
        x2 = list(df.columns[target_column + 1:])
        new_cols = x1 + x2 + [tc]
        df = df[new_cols]

    return df

if __name__ == "__main__":
    try:
        csv_file = "tables/format.csv"
        # Ler o arquivo CSV usando pandas
        data = pd.read_csv(csv_file)
        # Remover colunas não relacionadas ao experimento
        data = trim_columns(data)
        # Formatar os dados
        # Aplicar a função de reformatação aos valores float nas colunas
        for coluna in data.columns:
            # print(coluna, '->', end=" ")
            data[coluna] = data[coluna].apply(FUNCTIONS[coluna])
            # print('ok')
        # Salvar o DataFrame modificado de volta ao arquivo CSV
        new_file = csv_file.replace(".csv", "__NEW.csv")
        data.to_csv(new_file, index=False)
    except Exception as e:
        print(e)
        print("Arquivo não encontrado ou mal formatado,",
              f"deveria chamar-se {csv_file}")


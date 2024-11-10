import numpy as np
import pandas as pd
from parameters import FAIXAS_EXTRAVIO, FAIXAS_ATRASO, FAIXAS_DANO
from parameters import DATA_VARS, CREATE_RANGES
# from parameters import SOURCE, TEST, ARQUIVO_DE_SAIDA
from file_operations import log_file
current_column = ""

def hour_to_float(value):
    splits = value.split(":")
    last = len(splits) - 1
    try:
        minutes = float(splits[-last].strip()) / 60
        hours = float(splits[-(last + 1)].strip())
    except:
        global current_column
        log_file.write(f"\nColuna: {current_column}: Valor não reconhecido: {value}\n")
        return 0
    f_value = hours + minutes
    return f_value

def format_string(value):
    if '$' in value:
        value = value.replace('R$ ', '')
    if ',' in value:
        value = value.replace(',', '.')
    if value[-3] == '.':
        if value[-3:] == '.00':
            value = value[:-3]
            if '.' in value:
                value = value.replace('.', '')
            return float(value)
    try:
        f_value = float(value)   
    except:
        global current_column
        log_file.write(f"\nColuna: {current_column}: Valor não reconhecido: {value}\n")
        return 0
    return f_value

def format_binario(value, anomaly=0, yes=1, no=0):
    if type(value) == float:
        if np.isnan(value):
            return anomaly
    if value in ['S', 's', 'Y', 'y', 'Sim', 'sim', 'SIM', 'YES', 'Yes', 'yes', '1']:
        return yes
    elif value in ['N', 'n', 'Não', 'não', 'NÃO', 'NO', 'No', 'no', '0']:
        return no
    else:
        return anomaly

def generate_range(value, interval_values=[]):
    if not CREATE_RANGES:
        return float(value)
    if type(value) != int and type(value) != float:
        global current_column
        log_file.write(f"\nColuna: {current_column}: Valor não reconhecido: {value}\n")
        return 0
    if value == -1:
        return 0
    for i, interval in enumerate(interval_values):
        if value < interval:
            return i
    return len(interval_values)

def format_intervalo(value, interval_values=[]):
    if type(value) == int:
        pass
    elif type(value) == float:
        if np.isnan(value):
            value = 0
    elif value in ['-', '', ' ', '--']:
        value = 0
    elif ':' in value:
        value = hour_to_float(value)
    elif ',' in value or '.' in value:
        value = format_string(value)
    elif type(value) == str and value.isnumeric():
        value = float(value)
    else:
        try:
            value = float(value)
        except:
            global current_column
            log_file.write(f"\nColuna: {current_column}: Valor não reconhecido: {value}\n")
            value = 0
    return generate_range(value, interval_values)

FUNCTIONS = {
    'sentenca': lambda x: x,
    'direito_de_arrependimento': lambda x: format_binario(x),
    'descumprimento_de_oferta': lambda x: format_binario(x),
    'extravio_definitivo': lambda x: format_binario(x),
    'extravio_temporario': lambda x: format_binario(x),
    'intervalo_extravio_temporario': lambda x: format_intervalo(x, FAIXAS_EXTRAVIO),
    'faixa_intervalo_extravio_temporario': lambda x: int(x),
    'violacao_furto_avaria': lambda x: format_binario(x),
    'cancelamento/alteracao_destino': lambda x: format_binario(x),
    'atraso': lambda x: format_binario(x),
    'intervalo_atraso': lambda x: format_intervalo(x, FAIXAS_ATRASO),
    'faixa_intervalo_atraso': lambda x: int(x),
    'culpa_exclusiva_consumidor': lambda x: format_binario(x),
    'condicoes_climaticas/fechamento_aeroporto': lambda x: format_binario(x),
    'noshow': lambda x: format_binario(x),
    'overbooking': lambda x: format_binario(x),
    'assistencia_cia_aerea': lambda x: format_binario(x, -1),
    'hipervulneravel': lambda x: format_binario(x),
    'dano_moral_individual': lambda x: format_intervalo(x, FAIXAS_DANO),
    'faixa_dano_moral_individual': lambda x: int(x)
}

def trim_columns(df: pd.DataFrame):
    """
    Remove colunas não relacionadas ao experimento
    """
    remove_columns = [col for col in df.columns if col not in DATA_VARS]
    log_file.write(f"Colunas removidas: {remove_columns}\n")
    df = df.drop(columns=remove_columns)
    # log_file.write(f"Colunas restantes: {df.columns.to_list()}\n")
    return df

def format_data(csv_file:str):
    # Remover colunas não relacionadas ao experimento
    try:
        log_file.write(f"\n---\nArquivo: {csv_file}\n")
        df = pd.read_csv(csv_file)
        df = trim_columns(df)
    except Exception as e:
        log_file.write(str(e) + "\n")
        log_file.write("Arquivo não encontrado ou mal formatado\n")
        return df
    # Aplicar a função de reformatação aos valores float nas colunas
    for coluna in df.columns:
        global current_column
        current_column = coluna
        try:
            df[coluna] = df[coluna].apply(FUNCTIONS[coluna])
        except Exception as e:
            log_file.write(str(e) + '\n')
            log_file.write(f"Erro ao formatar a coluna: {coluna}\n")
    return df


import matplotlib.pyplot as plt
"""
reads a csv file with 2 columns, Projecao-Ortogonal (x) and Dano-Moral (y),
and plot a graphic comparing them 
"""
def plot_graphic_from_csv(csv_file:str,
                          col1:str,
                          col2:str,
                          title:str):
    data = pd.read_csv(csv_file)
    x = data[col1]
    y = data[col2]
    plt.scatter(x, y)
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title(title)
    plt.show()

def project_to_2d_space(df: pd.DataFrame):
    # converts the dataframe to a numpy array
    np_array = df.to_numpy()
    # makes a ortogonal projection of all variables
    # to 2D space, using Pitagoras theorem
    np_array = np_array**2
    np_array = np_array.sum(axis=1)
    np_array = np_array**0.5
    return np_array


if __name__ == "__main__":
    try:
        csv_file = 'projecao/full.csv'
        df = pd.read_csv(csv_file)
        # converts the values on result_col from money to float
        result_col = df['dano_moral_individual'].apply(format_string)
        # format the data
        df = format_data(csv_file)
        df = df.drop(columns=['sentenca'])
        df.to_csv('projecao/formated.csv', index=False)
        for col in df.columns:
            np_array = df[col].to_numpy()
            col = col.replace('/', '_')
            proj_col = col
            res_col = 'Dano-Moral'
            new_file = 'projecao/{}.csv'.format(col)
            title = "{} x {}".format(col, res_col)
            # creates a new matrix with the ortogonal projection and the result
            new_matrix = np.column_stack((np_array, result_col))
            new_df = pd.DataFrame(new_matrix, columns=[proj_col, res_col])
            # writes the result to a new csv file        
            new_df.to_csv(new_file, index=False)
            plot_graphic_from_csv(new_file, proj_col, res_col, title)
        # projects the data to 2D space
        np_array = project_to_2d_space(df)
        new_matrix = np.column_stack((np_array, result_col))
        new_df = pd.DataFrame(new_matrix, columns=['Projecao-Pitagoras', 'Dano-Moral'])
        new_df.to_csv('projecao/Pitagoras.csv', index=False)
        plot_graphic_from_csv('projecao/Pitagoras.csv', 'Projecao-Pitagoras', 'Dano-Moral', 'Projecao Pitagoras x Dano Moral')
    except Exception as e:
        print(e)


import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def count_frequencies(df0: pd.DataFrame, times: int, index) -> pd.DataFrame:
    freq_row = pd.DataFrame(columns=df0.columns)
    
    # Adiciona uma linha vazia
    freq_row = freq_row._append(pd.Series(), ignore_index=True)
    
    for c in df0.columns:
        if c == 'Sentença':
            freq_row[c] = df0.iloc[index][c]
            continue
            
        # Contabiliza frequências dos valores
        values = {}
        for i in range(times):
            cell = df0.iloc[index + i - (times - 1)][c]
            if cell in values:
                values[cell] += 1
            else:
                values[cell] = 1
                
        # Encontra o mais frequente    
        max_freq = 0
        frequent_value = None
        for value, freq in values.items():
            if freq > max_freq:
                frequent_value = value
                max_freq = freq

        if type(frequent_value) == float or type(frequent_value) == int:
            frequent_value = round(float(frequent_value), 2)
        # Atribui o mais frequente
        freq_row[c] = frequent_value

    return freq_row

def get_average_sheet(df0: pd.DataFrame) -> pd.DataFrame:
    df_out = pd.DataFrame(columns=df0.columns)
    sentence = ''
    times = 0
    
    for index, row in df0.iterrows():
        if sentence != row['Sentença']:
            # nova sentença
            if times > 0:
                # Quando mudar de sentença, o times terá
                # o número de repetições da sentença anterior
                freq_row = count_frequencies(df0, times, index-1) 
                df_out = df_out._append(freq_row, ignore_index=True)
            
            sentence = row['Sentença']
            # times é reiniciado para a próxima sentença
            times = 1
            
        else:
            times += 1

    if times > 0:
        # Processa última sentença
        freq_row = count_frequencies(df0, times, index)
        df_out = df_out._append(freq_row, ignore_index=True)

    df_out.to_excel('Results/averaged_sheet.xlsx', index=False)
    return df_out

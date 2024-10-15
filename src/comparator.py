import glob
import os
import pandas as pd
import openpyxl
from collections import defaultdict

import variable_formatation as vf
from parameters import SOURCE, TEST, RESULTADOS, DATA_VARS, ACURACIA
from value_comparation import COMPARISONS

def fill_cell(df, row, col):
    cell = df.cell(row=row+2, column=col+1)
    cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
    

# Receives 2 excel sheets and compares them
def compare(src: pd.DataFrame, dst: pd.DataFrame, name=RESULTADOS
            ) -> tuple[int, int, list[int], list[int]]:

    # receiving dataframes sizes
    num_rows1, num_cols1 = src.shape
    num_rows2, num_cols2 = dst.shape
    
    if num_cols1 != num_cols2:
        print('Número de colunas diferentes',
              num_cols1, num_cols2)
        return -1, -1, [-1], [-1]

    if (num_rows1) != num_rows2:
        print('Número de linhas diferentes',
              num_rows1, num_rows2)
        return -2, -2, [-2], [-2]

    total_errors = 0
    line_errors = 0
    col_errors = [0 for _ in range(num_cols1 - 1)]
    var_errors = dict()
    errors_per_line = [0 for i in range(num_rows1)]
    
    # opens the excel file to write the results
    writer = pd.ExcelWriter(name, engine='openpyxl')
    book = writer.book
    
    # Obtém a planilha para poder alterar cores
    sheet = book.active
    if sheet is None:
        sheet = book.create_sheet('Sheet1')

    # Percorre as células comparando valores
    names = src.columns
    for c in range(1, num_cols1):
        func = COMPARISONS[names[c]]
        var_errors[names[c]] = defaultdict(int)
        for r1 in range(num_rows1):
            v1 = src.iloc[r1, c]
            v2 = dst.iloc[r1, c]
            result = func(v1, v2)
            if type(result) == float:
                error = result > 4
                if type(var_errors[names[c]]) == defaultdict:
                    var_errors[names[c]] = 0
                var_errors[names[c]] += result
            else:
                error = result != 'TP' and result != 'TN'
                var_errors[names[c]][result] += 1
            if error:
                fill_cell(sheet, r1, c)
                col_errors[c-1] += 1
                errors_per_line[r1] += 1
                total_errors += 1
                if errors_per_line[r1] == 1:
                    fill_cell(sheet, r1, 0)
                    line_errors += 1
        if type(var_errors[names[c]]) == defaultdict:
            if 'TP' not in var_errors[names[c]]:
                var_errors[names[c]]['TP'] = 0
            if 'TN' not in var_errors[names[c]]:
                var_errors[names[c]]['TN'] = 0
            if 'FP' not in var_errors[names[c]]:
                var_errors[names[c]]['FP'] = 0
            if 'FN' not in var_errors[names[c]]:
                var_errors[names[c]]['FN'] = 0
            

    # Exporta o dataframe modificado
    dst.to_excel(writer, index=False) 
    writer._save()

    return total_errors, line_errors, col_errors, errors_per_line, var_errors

def get_percentage(value, total):
    num = (1 - (value/total)) * 100
    num_int = int(num)
    dec_num = round(num - num_int, 2)*100
    if dec_num == 100:
        dec_num = 0
        num += 1
    return ('%.2d,%.2d%%' % (num, dec_num))

def print_results(total_errors, sentence_errors, errors_per_col,
                  errors_per_line, n_sentences, n_variaveis,
                  variaveis, var_errors):
    total_values = n_sentences * n_variaveis
    ac_total = get_percentage(total_errors, total_values)
    ac_total_sent = get_percentage(sentence_errors, n_sentences)
    csv_line = [ac_total, ac_total_sent]

    output = f"Nº de Sentenças: {n_sentences} | Nº de Variáveis: {n_variaveis} | Nº Total de Valores: {total_values}\n"

    # Imprime resultados
    output += ('\nAcurácia por Variável:\n')
    media_de_erros_por_variavel = 0
    var_idx = 0
    for i in range(n_variaveis):
        var_idx += 1
        while variaveis[i] != DATA_VARS[var_idx]:
            csv_line.append('////')
            if 'intervalo' in DATA_VARS[var_idx]:
                csv_line.append('////')
            else:
                for _ in range(4):
                    csv_line.append('////')
            var_idx += 1
        ac = get_percentage(errors_per_col[i], n_sentences)
        csv_line.append(ac)
        media_de_erros_por_variavel += errors_per_col[i]
        resultado = 'Acertos: ' + ac
        log = var_errors[variaveis[i]]
        log_str = ' |'
        if type(log) != float:
            keys = list(log.keys())
            keys.sort()
            keys.reverse()
            for key in keys:
                str_key = str(key).rjust(2)
                val = log[key]
                str_log = str(val).rjust(3)
                csv_line.append(val)
                log_str += ' ' + str_key + ': ' + str_log + ' |'
        else:
            log = round(log/n_sentences, 2)
            csv_line.append(log)
            log_str += ' Erro Médio (horas): {} |'.format(log)
        # formats the variable name to fit 42 caracteres, filling with white spaces
        output += ' ' + variaveis[i].ljust(41) + ' : ' + resultado + log_str + '\n'

    # media_de_erros_por_sentenca = sum(errors_per_line)/n_sentences
    # media_de_erros_por_variavel = sum(errors_per_col)//n_variaveis
    # ac_med_var = get_percentage(media_de_erros_por_variavel , n_sentences)
    # ac_med_sent = get_percentage(media_de_erros_por_sentenca, n_variaveis)
    # output += ("-------------------------------------------\n")
    # output += ('Acurácia Média das Variáveis: %s\n' % ac_med_var)
    # output += ('Acurácia Média das Sentenças: %s\n' % ac_med_sent)
    output += ("-------------------------------------------\n")
    output += ('>> Acurácia Total das Sentenças: %s\n' % ac_total_sent)
    output += (">> Acurácia Total: %s\n" % ac_total)
    return csv_line, output

def main(source, test):
    # Lê arquivos
    df1 = vf.format_data(source)
    df2 = vf.format_data(test)
    
    # Compara arquivos
    name = get_prompt_name(test)
    saida_excel = RESULTADOS + name
    # creates the folder if it doesn't exist
    os.makedirs(saida_excel, exist_ok=True)
    saida_excel += '/' + name + '.xlsx'
    (total_errors, sentence_errors,
     errors_per_col, errors_per_line, var_errors) = compare(df1, df2, saida_excel)

    if total_errors < 0:
        return -1
    n_sentences= df1.shape[0]
    # Por causa da coluna da sentença
    variaveis = df1.columns[1:]
    n_variaveis = len(variaveis)
    return print_results(total_errors, sentence_errors, errors_per_col,
                  errors_per_line, n_sentences, n_variaveis,
                  variaveis, var_errors)
    # print(var_errors)


def get_experiments():
    experiments = []
    # gets all csv files on the folderds tables/sorce and tables/teste
    try:
        source = sorted(glob.glob(SOURCE))
        teste = sorted(glob.glob(TEST))
        for s, t in zip(source, teste):
            experiments.append((s, t))
    except Exception as e:
        print(e)
        print("Arquivos não encontrados")
    return experiments

def get_prompt_name(file):
    name = file.split('/')[-1].split('.')[0]
    return name


if __name__ == '__main__':
    experimentos = []
    for src, teste in get_experiments():
        csv_line, log = main(src, teste)
        name = get_prompt_name(teste)
        log_file = open(RESULTADOS + name + '/' + name + '.txt', 'w')
        log_file.write(log)
        log_file.close()
        '''print("\n##########################################################################\n",
              log, end='')'''
        experimentos.append([name, '-------'] + csv_line)
    
    vars = []
    for i in DATA_VARS[1:]:
        if 'intervalo' in i:
            vars.append('AC - ' + i)
            vars.append('Err-med (h) - ' + i)
        else:
            vars.append('AC - ' + i)
            vars.append('TP - ' + i)
            vars.append('TN - ' + i)
            vars.append('FP - ' + i)
            vars.append('FN - ' + i)  
    
    csv_header = ['Prompt', 'Descrição', 'Acurácia Total', 'Acurácia por Sentença'] + vars
    print(experimentos)
    try:
        pd.DataFrame(experimentos, columns=csv_header).to_csv(ACURACIA, index=False)
    except Exception as e:
        print(e)
        print("Erro ao salvar os resultados")
    

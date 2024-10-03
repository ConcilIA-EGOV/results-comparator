import pandas as pd
import openpyxl
from collections import defaultdict
import variable_formatation as vf
from parameters import SOURCE, TEST, ARQUIVO_DE_SAIDA
from value_comparation import COMPARISONS

def fill_cell(df, row, col):
    cell = df.cell(row=row+2, column=col+1)
    cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
    

# Receives 2 excel sheets and compares them
def compare(src: pd.DataFrame, dst: pd.DataFrame
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
    col_errors = [0 for _ in range(num_cols1)]
    var_errors = dict()
    errors_per_line = [0 for i in range(num_rows1)]
    
    # opens the excel file to write the results
    writer = pd.ExcelWriter(ARQUIVO_DE_SAIDA,
                            engine='openpyxl')
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
            var_errors[names[c]][result] += 1
            error = True
            if type(result) == int:
                if result == 0:
                    error = False
            else:
                error = result != 'TP' and result != 'TN'
            if error:
                fill_cell(sheet, r1, c)
                col_errors[c] += 1
                errors_per_line[r1] += 1
                total_errors += 1
                if errors_per_line[r1] == 1:
                    fill_cell(sheet, r1, 0)
                    line_errors += 1
        if any(type(i) == str for i in var_errors[names[c]].keys()):
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

def print_results(total_errors, sentence_errors, errors_per_col,
                  errors_per_line, n_sentences, n_variaveis,
                  variaveis, var_errors):
    total_values = n_sentences * n_variaveis
    print("Nº de Sentenças:", n_sentences,
          "| Nº de Variáveis:", n_variaveis,
          "| Nº Total de Valores:", total_values)

    # Imprime resultados
    media_de_erros_por_sentenca = 0
    maior_erro_em_uma_sentenca = 0

    for r in range(n_sentences):
        id = ' - %.3d' % errors_per_line[r]
        media_de_erros_por_sentenca += errors_per_line[r]
        if errors_per_line[r] > maior_erro_em_uma_sentenca:
            maior_erro_em_uma_sentenca = errors_per_line[r]
    media_de_erros_por_sentenca /= n_sentences
    col_errors = 0
    for i in errors_per_col:
        col_errors += int(i > 0)
    print('\nAcurácia por Variável:')
    media_de_erros_por_variavel = 0
    maior_erro_em_uma_variavel = 0
    for i in range(1, n_variaveis + 1):
        media_de_erros_por_variavel += errors_per_col[i]
        if errors_per_col[i] > maior_erro_em_uma_variavel:
            maior_erro_em_uma_variavel = errors_per_col[i]
        number = (1 - (errors_per_col[i]/n_sentences)) * 100
        num_int = int(number)
        dec_num = round(number - num_int, 2)*100
        if dec_num == 100:
            dec_num = 0
            number += 1
        resultado = 'Acertos: %.2d.%.2d%%' % (number, dec_num)
        log = dict(var_errors[variaveis[i]])
        log_str = ''
        keys = list(log.keys())
        keys.sort()
        for key in keys:
            str_key = str(key).rjust(2)
            str_log = str(log[key]).rjust(3)
            log_str += ' | ' + str_key + ': ' + str_log

        # formats the variable name to fit 42 caracteres, filling with white spaces
        var = ' ' + variaveis[i].ljust(41)
        print(var, ':', resultado, log_str)
    media_de_erros_por_variavel //= n_variaveis
    print('\nMaior Número de Erros em uma Variável:',
          maior_erro_em_uma_variavel, '--> %.2f%%' %
          ((maior_erro_em_uma_variavel/n_sentences) * 100))
    print('Maior nº de Erros em uma Sentença:', maior_erro_em_uma_sentenca,
          ('--> %.2f%%' % (maior_erro_em_uma_sentenca/(n_variaveis) * 100)))
    print("-------------------------------------------")
    print('Acurácia Média das Variáveis: %.2f%%' %
          ((1 - (media_de_erros_por_variavel/n_sentences)) * 100))
    print('Acurácia Média das Sentenças: %.2f%%' %
          ((1 - (media_de_erros_por_sentenca/n_variaveis)) * 100))
    print("-------------------------------------------")
    print('>> Acurácia Total das Variáveis: %.2f%%' %
          ((1 - (col_errors/n_variaveis)) * 100))
    print('>> Acurácia Total das Sentenças: %.2f%%' %
          ((1 - (sentence_errors/n_sentences)) * 100))
    print(">> Acurácia Total: %.2f%%" %
          (100 - ((total_errors/total_values) * 100)))
    
def main():
    # Lê arquivos
    df1 = vf.format_data(SOURCE)
    df2 = vf.format_data(TEST)
    
    # Compara arquivos
    (total_errors, sentence_errors,
     errors_per_col, errors_per_line, var_errors) = compare(df1, df2)

    if total_errors < 0:
        return -1
    n_sentences, n_variaveis = df1.shape
    # Por causa da coluna com o id da sentença
    n_variaveis -= 1
    variaveis = df1.columns
    print_results(total_errors, sentence_errors, errors_per_col,
                  errors_per_line, n_sentences, n_variaveis,
                  variaveis, var_errors)
#    print(var_errors)
    return 0

if __name__ == '__main__':
    main()

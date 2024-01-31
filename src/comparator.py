import pandas as pd
import openpyxl
import modulator as md


VARIAVEIS = ["Sentença", "direito de arrependimento", "descumprimento de oferta", "extravio definitivo", "extravio temporário", "intervalo de extravio", "violação", "cancelamento (sem realocação)/alteração de destino", "atraso de voo", "intervalo de atraso", "culpa exclusiva do consumidor", "inoperabilidade do aeroporto", "no show", "overbooking", "assistência da companhia aérea", "hipervulnerabilidade"]

ARQUIVO_DE_SAIDA = 'Resultados/resultado.xlsx'
SOURCE = 'tables/source.xlsx'
TEST = 'tables/test.xlsx'

# Receives 2 excel sheets and compares them
def compare(df1: pd.DataFrame, df2: pd.DataFrame) -> (int, int, [int], [int]):

    # receiving dataframes sizes
    num_rows1, num_cols1 = df1.shape
    num_rows2, num_cols2 = df2.shape
    
    if num_cols1 != num_cols2:
        print('Número de colunas diferentes', num_cols1, num_cols2)
        return -1, -1, [-1], [-1]

    if (num_rows1) != num_rows2:
        print('Número de linhas diferentes', num_rows1, num_rows2)
        return -2, -2, [-2], [-2]

    total_errors = 0
    line_errors = 0
    col_errors = [0 for i in range(num_cols1)]
    errors_per_line = [0 for i in range(num_rows1)]
    
    # opens the excel file to write the results
    writer = pd.ExcelWriter(ARQUIVO_DE_SAIDA, engine='openpyxl')
    book = writer.book
    
    # Obtém a planilha para poder alterar cores
    sheet = book.active
    if sheet is None:
        sheet = book.create_sheet('Sheet1')

    # Percorre as células comparando valores
    for r1 in range(num_rows1):
        for c in range(1, num_cols1):
            v1 = df1.iloc[r1, c]
            v2 = df2.iloc[r1, c]
            if v1 != v2:
                try:
                    v2 = round(float(v2), 2)
                    v1 = round(float(v1), 2)
                    # Se for float, arredonda para 2 casas decimais
                    if v1 == v2:
                        continue
                except:
                    pass
                errors_per_line[r1] += 1
                cell = sheet.cell(row=r1+2, column=c+1)
                cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
                total_errors += 1
                col_errors[c] += 1
        if errors_per_line[r1] > 0:
            cell = sheet.cell(row=r1+2, column=1)
            cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
            line_errors += 1
            

    # Exporta o dataframe modificado
    df2.to_excel(writer, index=False) 
    writer._save()

    return total_errors, line_errors, col_errors, errors_per_line

def main(variaveis):
    # Lê arquivos
    df1 = pd.read_excel(SOURCE)
    df_temp = pd.read_excel(TEST)
    df2 = md.get_average_sheet(df_temp)

    # Compara arquivos
    (total_errors, line_errors, errors_per_col, errors_per_line) = compare(df1, df2)

    if total_errors < 0:
        return -1

    n_sentences, n_variaveis = df1.shape
    n_lines, n_variaveis = df2.shape
    # Por causa da coluna com o id da sentença
    n_variaveis -= 1
    total_values = n_sentences * (n_variaveis)

    print("Número de sentenças:", n_sentences)
    print("Número de variáveis:", n_variaveis)
    print("Número total de valores:", total_values, end='\n\n')

    # Imprime resultados
    print('Número Total de Erros:', total_errors)
    print("Porcentagem Total de Erros: %.2f%%" % (total_errors/total_values * 100))
    print('\nNúmero de Linhas com Erros:', line_errors)
    print("Porcentagem de Linhas com Erros: %.2f%%" % (line_errors/n_lines * 100))
    print('\nErros por Sentença:\n')
    for r in range(n_sentences):
        id = ' - %.2d' % errors_per_line[r]
        number = (errors_per_line[r]/(n_variaveis) * 100)
        num_int = int(number)
        dec_num = round(number - num_int, 2)*100
        resultado = 'erros, %.2d.%.2d%% de erro' % (number, dec_num)
        print(id, resultado)
    col_errors = 0
    for i in errors_per_col:
        col_errors += int(i > 0)
    print('\nNúmero de Variáveis com Erros:', col_errors)
    print("Porcentagem de Variáveis com Erros: %.2f%%" % (col_errors/n_variaveis * 100))
    print('\nErros por Variável:\n')
    for i in range(1, n_variaveis + 1):
        id = ("%.2d" % i) + (' - %.2d' % errors_per_col[i])
        number = (errors_per_col[i]/n_lines * 100)
        num_int = int(number)
        dec_num = round(number - num_int, 2)*100
        resultado = 'erros, %.2d.%.2d%% do total' % (number, dec_num)
        print(id, resultado, ':', variaveis[i])

    return 0

main(VARIAVEIS)

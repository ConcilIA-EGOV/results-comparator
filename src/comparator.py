import pandas as pd
import openpyxl

# labels para cada variável
variaveis = ["Sentença", "direito de arrependimento", "descumprimento de oferta", "extravio definitivo", "extravio temporário", "intervalo de extravio", "violação", "cancelamento (sem realocação)/alteração de destino", "atraso de voo", "intervalo de atraso", "culpa exclusiva do consumidor", "inoperabilidade do aeroporto", "no show", "overbooking", "assistência da companhia aérea", "agência de viagem", "hipervulnerabilidade"]

# Receives 2 excel sheets and compares them
# Also receives the number of times each sentence
# is repeated in the sheets
def compare(df1, df2, times=1):

    # Inicializa variáveis
    num_rows1, num_cols1 = df1.shape
    num_rows2, num_cols2 = df2.shape
    
    if num_cols1 != num_cols2:
        print('Número de colunas diferentes', num_cols1, num_cols2)
        return -1, -1, -1, [-1], [-1]

    if (num_rows1)*times != num_rows2:
        print('Número de linhas diferentes', num_rows1, num_rows2)
        return -2, -2, -1, [-2], [-2]

    total_errors = 0
    line_errors = 0
    errors_per_line = [0 for i in range(num_rows2)]
    col_errors = [0 for i in range(num_cols1)]
    errors_per_sentence = [0 for i in range(num_rows1)]
    wrong_sentences = 0
    
    # Abre o arquivo Excel
    writer = pd.ExcelWriter('Results/resultado.xlsx', engine='openpyxl')
    book = writer.book
    
    # Obtém a planilha para poder alterar cores
    sheet = book.active
    if sheet is None:
        sheet = book.create_sheet('Sheet1')

    r2 = -1
    # Percorre as células comparando valores
    for r1 in range(num_rows1):
        for _ in range(times):
            r2 += 1
            for c in range(1, num_cols1):
                # print("r1 =", r1, "c =", c, "celula =", df1.iloc[r1, c])
                if df1.iloc[r1, c] != df2.iloc[r2, c]:
                    errors_per_line[r2] += 1
                    errors_per_sentence[r1] += 1
                    cell = sheet.cell(row=r2+2, column=c+1)
                    cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
                    total_errors += 1
                    col_errors[c] += 1
            if errors_per_line[r2] > 0:
                cell = sheet.cell(row=r2+2, column=1)
                cell.fill = openpyxl.styles.PatternFill(fgColor="FFFF00", fill_type = "solid")
                line_errors += 1
        if errors_per_sentence[r1] > 0:
            wrong_sentences += 1
            

    # Exporta o dataframe modificado
    df2.to_excel(writer, index=False) 
    writer._save()

    return total_errors, line_errors, col_errors, errors_per_line, errors_per_sentence, wrong_sentences

def main(variaveis):
    # Lê arquivos
    df1 = pd.read_excel('tables/source.xlsx')
    df2 = pd.read_excel('tables/test.xlsx')

# cálculo do número de vezes que cada sentença se repete
    times = 1
    s1 = df2.iloc[0, 0]
    while True:
        s2 = df2.iloc[times, 0]
        if s1 == s2:
            times += 1
        else:
            break
    

    # Compara arquivos
    (total_errors, line_errors, col_errors, errors_per_line,
     errors_per_sentence, wrong_sentences) = compare(df1, df2, times)
    if total_errors < 0:
        return -1

    n_sentences, n_variaveis = df1.shape
    n_lines, n_variaveis = df2.shape
    n_variaveis -= 1
    # Po causa da coluna com o id da sentença
    total_values = n_sentences * (n_variaveis) * times
    print("Número de sentenças:", n_sentences, "--> repetidas", times, "vezes cada")
    print("Número de variáveis:", n_variaveis)
    print("Número total de valores:", total_values, end='\n\n')

    # Imprime resultados
    print('Número Total de Erros:', total_errors)
    print("Porcentagem Total de Erros: %.2f%%" % (total_errors/total_values * 100))
    print('\nNúmero de Linhas com Erros:', line_errors)
    print("Porcentagem de Linhas com Erros: %.2f%%" % (line_errors/n_lines * 100))
    print('Número de Sentenças Erradas:', wrong_sentences)
    print("Porcentagem de Sentenças com Erros: %.2f%%" % (wrong_sentences/n_sentences * 100))
    print('\nErros por Sentença:\n')
    for r in range(n_sentences):
        id = ' - %.2d' % errors_per_sentence[r]
        number = (errors_per_sentence[r]/(n_variaveis) * 100)
        num_int = int(number)
        dec_num = round(number - num_int, 2)*100
        resultado = 'erros, %.2d.%.2d%% de erro' % (number, dec_num)
        print(id, resultado)
    print('\nErros por Variável:\n')
    for i in range(1, n_variaveis + 1):
        id = ("%.2d" % i) + (' - %.2d' % col_errors[i])
        number = (col_errors[i]/n_lines * 100)
        num_int = int(number)
        dec_num = round(number - num_int, 2)*100
        resultado = 'erros, %.2d.%.2d%% do total' % (number, dec_num)
        print(id, resultado, ':', variaveis[i])

main(variaveis)

As instruções de uso podem ser obtidas digitando "make" no terminal.

As tabelas de input devem ser baixadas em formato ".csv" na pasta entrada
 - As tabelas gabarito devem ficar na pasta gabarito e a tabela testada na pasta teste.
 - Elas devem preferencialmente ter o mesmo nome (mas basta que estejam na mesma posição em ordem alfabética).

Sempre que o programa for rodado, será gerada uma pasta Resultados:
 - Dentro dela, haverá um arquivo debug_comparacao.txt com os erros encontrados.
 - Também haverão 2 arquivos csv com um comparativo de acurácia entre todos os prompts testados.
    - o arquivo Acuracia-F1-Score possui a acurácia total e por variável, bem como o F1-score e/ou RMSE.
    - o arquivo Acuracia-ConfusionMatrix inclui também os valores de Verdadeiros-Positivos, Negativos ...

Cada par teste-gabarito vai gerar uma subpasta (nomeada como a tabela gabarito) dentro de uma pasta Resultados, com:
 - Uma tabela xlsx formatada para que as células diferentes em relação ao gabarito fiquem em amarelo.
 - Um arquivo txt com detalhes da comparação de cada tabela.

Se pretende-se testar planilhas com repetição (ou seja, múltiplas planilhas do mesmo prompt para o mesmo gabarito):
 - É necessário colocar, ao invés de um arquivo csv, uma pasta de mesmo nome, com as planilhas repetidas dentro
 - Deve-se também modificar o parâmetro AVG_SHEET no arquivo parameters.py para True.

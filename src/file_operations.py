import glob
import os
from parameters import SOURCE, TEST, RESULTADOS, LOG_VAR
os.makedirs(RESULTADOS[:-1], exist_ok=True)
log_file = open(LOG_VAR, 'w')

def get_prompt_name(file_name: str):
    name = file_name.split('/')[-1].split('.')[0]
    return name

def get_experiments():
    """
    gets all csv files on the folderds tables/sorce and tables/teste
    """
    experiments = []
    try:
        source = sorted(glob.glob(SOURCE))
        teste = sorted(glob.glob(TEST))
        for s, t in zip(source, teste):
            experiments.append((s, t))
            # creates the results folder if it doesn't exist
            folder = RESULTADOS + get_prompt_name(t)
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        print(e)
        print("Arquivos não encontrados")
    return experiments


def get_save_path(file):
    name = get_prompt_name(file)
    saida = RESULTADOS + name + '/' + name
    saida_excel = saida + '.xlsx'
    saida_txt = saida + '.txt'
    return saida_excel, saida_txt

def write_log(log_file, log):
    log_file = open(log_file, 'w')
    log_file.write(log)
    log_file.close()


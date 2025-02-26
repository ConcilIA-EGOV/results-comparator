import glob
import os
from parameters import SOURCE, TEST, RESULTADOS, LOG_VAR, AVG_SHEET
import modulador as md

os.makedirs(RESULTADOS[:-1], exist_ok=True)
log_file = open(LOG_VAR, 'w')

def get_prompt_name(file_name: str):
    name = file_name.split('/')[-1].split('.')[0]
    return name

def get_experiments():
    """
    gets all csv files on the folders entrada/gabarito and entrada/teste
    """
    experiments = []
    # para garantir a ordem alfabética dos arquivos
    source = sorted(glob.glob(SOURCE))
    teste = sorted(glob.glob(TEST))
    for s, t in zip(source, teste):
        if AVG_SHEET:
            t = get_avg_sheet(t)
        experiments.append((s, t))
        # creates the results folder if it doesn't exist
        folder = RESULTADOS + get_prompt_name(t)
        os.makedirs(folder, exist_ok=True)
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

def get_avg_sheet(folder_name: str) -> str:
    """
    Receives a folder name, reads all the csv files in it,
    gets the average sheet and saves it in a csv file
    """
    # verifies if the folder exists and is a folder and not a file
    if not os.path.isdir(folder_name):
        print(f"Tentando transformar em média um arquivo que não é uma pasta: {folder_name}")
        return folder_name
    # gets all csv files in the folder
    files = glob.glob(folder_name + '/*.csv')
    # gets the average sheet
    avg_sheet = md.get_avg_sheet(files)
    # saves the average sheet
    f_name = folder_name.split('/')[-1]
    file_name = folder_name + '/' + f_name + '.csv'
    avg_sheet.to_csv(file_name, index=False)
    return file_name    

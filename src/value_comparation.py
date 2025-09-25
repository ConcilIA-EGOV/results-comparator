
from typing import Callable


def compare_binario(src, dst) -> tuple[str, bool]:
    if src == 1:
        if dst == 1:
            return 'TP', False
        if dst == 0:
            return 'FN', True
        if dst == -1:
            return 'FN', True
    if src == 0:
        if dst == 1:
            return 'FP', True
        if dst == 0:
            return 'TN', False
        if dst == -1:
            return 'FN', True
    if src == -1:
        if dst == 1:
            return 'FP', True
        if dst == 0:
            return 'FN', True
        if dst == -1:
            return 'TN', False
    print(f'Valor inesperado na comparação binária: src={src}, dst={dst}')
    return 'TN', False

def compare_intervalo(src, dst) -> tuple[float, bool]:
    margin = abs(src - dst)
    erro = margin > 1
    return float(margin**2), erro

def comparisons(name)-> Callable:
    '''
    Retorna a função de comparação adequada para a variável
    '''
    if name in BIN_VARS:
        return compare_binario
    elif name in INTERVAL_VARS:
        return compare_intervalo
    else:
        return lambda x, y: (0.0, False)

# variáveis binárias
BIN_VARS = [
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'violacao_furto_avaria',
    'cancelamento/alteracao_destino',
    'atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]

# variáveis contínuas ou categóricas
INTERVAL_VARS = [
    'faixa_intervalo_extravio_temporario',
    'faixa_intervalo_atraso',
    'intervalo_extravio_temporario',
    'intervalo_atraso'
]



def compare_binario(src, dst):
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

def compare_intervalo(src, dst):
    margin = abs(src - dst)
    erro = margin > 1
    return float(margin**2), erro

COMPARISONS = {
    'direito_de_arrependimento': lambda x, y: compare_binario(x, y),
    'descumprimento_de_oferta': lambda x, y: compare_binario(x, y),
    'extravio_definitivo': lambda x, y: compare_binario(x, y),
    'extravio_temporario': lambda x, y: compare_binario(x, y),
    'faixa_intervalo_extravio_temporario': lambda x, y: compare_intervalo(x, y),
    'faixa_intervalo_atraso': lambda x, y: compare_intervalo(x, y),
    'intervalo_extravio_temporario': lambda x, y: compare_intervalo(x, y),
    'violacao_furto_avaria': lambda x, y: compare_binario(x, y),
    'cancelamento/alteracao_destino': lambda x, y: compare_binario(x, y),
    'atraso': lambda x, y: compare_binario(x, y),
    'intervalo_atraso': lambda x, y: compare_intervalo(x, y),
    'culpa_exclusiva_consumidor': lambda x, y: compare_binario(x, y),
    'condicoes_climaticas/fechamento_aeroporto': lambda x, y: compare_binario(x, y),
    'noshow': lambda x, y: compare_binario(x, y),
    'overbooking': lambda x, y: compare_binario(x, y),
    'assistencia_cia_aerea': lambda x, y: compare_binario(x, y),
    'hipervulneravel': lambda x, y: compare_binario(x, y),
}

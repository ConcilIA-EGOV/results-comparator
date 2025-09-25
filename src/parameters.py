# caminhos para os arquivos de dados e modelos
RESULTADOS = 'Resultados/'
ACURACIA = 'Resultados/Acuracia-F1-Score.csv'
LOG_VAR = 'Resultados/debug_comparacao.txt'
SOURCE = 'entrada/gabarito/*.csv'
TEST = 'entrada/teste/*'


CREATE_RANGES = False
AVG_SHEET = False

FAIXAS_EXTRAVIO = [1, 24, 72, 168]
FAIXAS_ATRASO = [1, 4, 8, 12, 16, 24, 28]
FAIXAS_DANO = [1, 2000, 4000, 6000, 8000, 10000]

DATA_VARS = [
    "sentenca",
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'faixa_intervalo_extravio_temporario',
    #'intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'cancelamento',
    'atraso',
    #'intervalo_atraso',
    'faixa_intervalo_atraso',
    'culpa_exclusiva_consumidor',
    # 'fechamento_aeroporto',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel',
    'Dano-Moral',
]

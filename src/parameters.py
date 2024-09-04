# caminhos para os arquivos de dados e modelos
ARQUIVO_DE_SAIDA = 'Resultados/resultado.xlsx'
SOURCE = 'tables/source.xlsx'
TEST = 'tables/test.xlsx'


USE_RANGES = True
CREATE_RANGES = True

# Variáveis categorizadas
DATA_VARS_RANGE = [
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'faixa_intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'cancelamento/alteracao_destino',
    'atraso',
    'faixa_intervalo_atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]
FAIXAS_EXTRAVIO = [1, 24, 72, 168]
FAIXAS_ATRASO = [1, 4, 8, 12, 16, 24, 28]
FAIXAS_DANO = [1, 2000, 4000, 6000, 8000, 10000]

# Variáveis contínuas
DATA_VARS_CONTINUOUS = [
    "sentenca",
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'cancelamento/alteracao_destino',
    'atraso',
    'intervalo_atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]

# DATA_VARS = DATA_VARS_RANGE if USE_RANGES else DATA_VARS_CONTINUOUS

DATA_VARS = DATA_VARS_CONTINUOUS

ATRASO2 = [
    "sentenca",
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'atraso',
    'intervalo_atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]
ATRASO5 = [
    "sentenca",
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'extravio_temporario',
    'intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'intervalo_atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]

EXTRAVIO2 = [
    "sentenca",
    'direito_de_arrependimento',
    'descumprimento_de_oferta',
    'extravio_definitivo',
    'intervalo_extravio_temporario',
    'violacao_furto_avaria',
    'cancelamento/alteracao_destino',
    'atraso',
    'intervalo_atraso',
    'culpa_exclusiva_consumidor',
    'condicoes_climaticas/fechamento_aeroporto',
    'noshow',
    'overbooking',
    'assistencia_cia_aerea',
    'hipervulneravel'
]

DATA_VARS = ATRASO5

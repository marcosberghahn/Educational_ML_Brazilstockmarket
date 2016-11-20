###############################################################################
#Funcao para puxar os dados da Bovespa a partir do .txt padrao disponibilizado no site www.bmfbovespa.com.br.
#Donwload do .txt tem que ser manual, existe um captcha para poder baixar os arquivos.
###############################################################################
   
import pandas as pd
import numpy as np

def offline_bvsp_retrive(ano_inicial,ano_final):

    #Dados somente ate 1995. Primeiro ano da moeda R$.
    LOCAL_DADOS_ESTATICOS = 'DADOS_ESTATICOS'
    NOME_ARQ_PADRAO = 'COTAHIST_A'
    filelist = []
    DADOS_BOVESPA = pd.DataFrame()
    tmp_frames = []

    #Padrao das divisoes dos dados obtidos no site:
    #fonte: http://www.bmfbovespa.com.br/pt_br/servicos/market-data/historico/mercado-a-vista/cotacoes-historicas/.
    fixed_width_Bovespa = [2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,18,13,1,8,7,13,12,3]
    column_names_Bovespa = ['TIPREG','DATA','CODBDI','CODNEG','TPMERC','NOMRES','ESPECI','PRAZOT','MODREF','PREABE','PREMAX','PREMIN','PREMED','PREULT','PREOFC','PREOFV','TOTNEG','QUATOT','VOLTOT','PREEXE','INDOPC','DATVEN','FATCOT','PTOEXE','CODISI','DISMES']

    for ano in range(ano_inicial,ano_final+1):
        s = LOCAL_DADOS_ESTATICOS + '/' + NOME_ARQ_PADRAO + str(ano) + '.TXT'
        filelist.append(s)

    for file in filelist:

        #A primeira e a ultima linha do arquivo padrao das cotas historicas tem informacoes nao necessarias.
        #Portanto a utilizacao do skiprows = 1 e skipfooter = 1
        frame = pd.read_fwf(file, widths = fixed_width_Bovespa, Header=None, names = column_names_Bovespa, \
                            skiprows = 1, skipfooter = 1)
    
        tmp_frames.append(frame)
    
    DADOS_BOVESPA = pd.concat(tmp_frames)

    #Estrutura de tempo do pandas nao suporta datas acima de 11/04/2262. Estamos colocando essas datas como #N/A
    DADOS_BOVESPA.ix[DADOS_BOVESPA.DATVEN > 22620411, 'DATVEN'] =  pd.NaT
    DADOS_BOVESPA.ix[DADOS_BOVESPA.DATVEN > 22620411, 'DATA'] =  pd.NaT

    #Transformando as datas tipo 20160104 para formato datetime64[ns]
    DADOS_BOVESPA['DATA'] = pd.to_datetime(DADOS_BOVESPA['DATA'], format="%Y%m%d")
    DADOS_BOVESPA['DATVEN'] = pd.to_datetime(DADOS_BOVESPA['DATVEN'], format="%Y%m%d")

    #Transformando o tipo de cada coluna da base da Bovespa
    #Colunas com preço devem ser dividas por 100. 
    #ex: .TXT padrao traz o preco 1121 como string, e na verdade o preco 11.21. Por isso /100.
    DADOS_BOVESPA['TIPREG'] = DADOS_BOVESPA['TIPREG'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['CODBDI'] = DADOS_BOVESPA['CODBDI'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['CODNEG'] = DADOS_BOVESPA['CODNEG'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['TPMERC'] = DADOS_BOVESPA['TPMERC'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['NOMRES'] = DADOS_BOVESPA['NOMRES'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['ESPECI'] = DADOS_BOVESPA['ESPECI'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['PRAZOT'] = DADOS_BOVESPA['PRAZOT'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['MODREF'] = DADOS_BOVESPA['MODREF'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['PREABE'] = DADOS_BOVESPA['PREABE'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREABE'] = DADOS_BOVESPA['PREABE'] / 100
    DADOS_BOVESPA['PREMAX'] = DADOS_BOVESPA['PREMAX'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREMAX'] = DADOS_BOVESPA['PREMAX'] / 100
    DADOS_BOVESPA['PREMIN'] = DADOS_BOVESPA['PREMIN'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREMIN'] = DADOS_BOVESPA['PREMIN'] / 100
    DADOS_BOVESPA['PREMED'] = DADOS_BOVESPA['PREMED'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREMED'] = DADOS_BOVESPA['PREMED'] / 100
    DADOS_BOVESPA['PREULT'] = DADOS_BOVESPA['PREULT'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREULT'] = DADOS_BOVESPA['PREULT'] / 100
    DADOS_BOVESPA['PREOFC'] = DADOS_BOVESPA['PREOFC'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREOFC'] = DADOS_BOVESPA['PREOFC'] / 100
    DADOS_BOVESPA['PREOFV'] = DADOS_BOVESPA['PREOFV'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREOFV'] = DADOS_BOVESPA['PREOFV'] / 100
    DADOS_BOVESPA['TOTNEG'] = DADOS_BOVESPA['TOTNEG'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['QUATOT'] = DADOS_BOVESPA['QUATOT'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['VOLTOT'] = DADOS_BOVESPA['VOLTOT'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['VOLTOT'] = DADOS_BOVESPA['VOLTOT'] / 100
    DADOS_BOVESPA['PREEXE'] = DADOS_BOVESPA['PREEXE'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PREEXE'] = DADOS_BOVESPA['PREEXE'] / 100
    DADOS_BOVESPA['INDOPC'] = DADOS_BOVESPA['INDOPC'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['FATCOT'] = DADOS_BOVESPA['FATCOT'].astype(np.int64,casting='safe',copy='false')
    DADOS_BOVESPA['PTOEXE'] = DADOS_BOVESPA['PTOEXE'].astype(np.float64,casting='safe',copy='false')
    DADOS_BOVESPA['PTOEXE'] = DADOS_BOVESPA['PTOEXE'] / 100
    DADOS_BOVESPA['CODISI'] = DADOS_BOVESPA['CODISI'].astype(object,casting='safe',copy='false')
    DADOS_BOVESPA['DISMES'] = DADOS_BOVESPA['DISMES'].astype(np.int64,casting='safe',copy='false')

    return DADOS_BOVESPA
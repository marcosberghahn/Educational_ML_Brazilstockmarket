
#Pacotes externos
import numpy as np
import pandas as pd
import matplotlib as plt

#Pacotes do próprio projeto.
import offline_bvps_data as off_data

DADOS_BVPS = pd.DataFrame()

#Periodo total
ano_inicial = 1986
ano_final = 2016

DADOS_BVPS = off_data.offline_bvsp_retrive(ano_inicial,ano_final)



    

"""
Created on Thu Nov 17 18:32:32 2016

@author: Vitor Freitas de Almeida
"""

import pandas_datareader.data
import datetime
import requests_cache

expire_after = datetime.timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

def get_data_yahoo(symbl,start,end):
    
    return pandas_datareader.data.DataReader(symbl, 'yahoo', start, end, session=session)
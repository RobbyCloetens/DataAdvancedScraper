import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
import time 
while(True):
    url = "https://www.blockchain.com/btc/unconfirmed-transactions"
    request = requests.get(url)
    bitcoininfo = BeautifulSoup(request.text, features="html.parser")
    info = bitcoininfo.findAll('div', attrs={"class" : "sc-1g6z4xm-0 hXyplo"})
    bitcoinlines = []
    for i in range(0,50):
        line = info[i]
        regex1 = re.sub(r"Hash", '', line.text)
        regex2 = re.sub(r"Time", ';', regex1)
        regex3 = re.sub(r"Amount \(BTC\)", ';', regex2)
        bitcoinline = re.sub(r"BTCAmount \(USD\)", ';', regex3)
        bitcoinlines.append(bitcoinline)
        #print(bitcoinline)

    bitcointijdelijk = []
    for i in range(0, 50):
        bitcoinlinesplit = bitcoinlines[i].split(';')
        #print(bitcoinlinesplit)
        #print(hash, time, btc, usd)
        bitcointijdelijk.append(bitcoinlinesplit)
        
    #print(bitcointijdelijk)

    #print(bitcointijdelijk)    
    bitcoindata = pd.DataFrame (bitcointijdelijk, columns = ['Hash', 'Time', 'BTC', 'USD'])
    bitcoindata = bitcoindata.astype({'Hash': str, 'Time': str, 'BTC': float, 'USD': str})
    #print(bitcoindata)

    bitcoindata = bitcoindata.sort_values(by=['BTC'], ascending=False, ignore_index=True)
    print(bitcoindata[0:5])
    time.sleep(60)
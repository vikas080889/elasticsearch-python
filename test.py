import requests
import re
import json
from bs4 import BeautifulSoup , Comment
from datetime import date
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

"""
data = requests.get('https://frapi.marketsmojo.com/stocks_dashboard/stockinfo?sid=541728&callback=jQuery21105692901213009467_1536953494358')
data = data.text
data = json.loads(data[41:-1])
#print(data)
jo_status = data['data']['stocklabel']['text']
#print(jo_status)
"""


ltp_url ='https://json.bselivefeeds.indiatimes.com/ET_Community/companypagedata?companyid='+'15279'+'&companytype=&callback=ets.hitMarketResponse'
ltp = requests.get(ltp_url)
ltp = ltp.text
ltp_data = ltp[22:-2]
ltp_dict = json.loads(ltp_data)

print(ltp_dict['bseNseJson'][0]['lastTradedPrice'])



for i in range(16,21):
    print(i)

today = date.today().strftime('%b-%d-%Y')
print(date.today().strftime('%b-%d-%Y'))

doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }
data = es.search(index='ema_50_analysis', doc_type='blog', body=doc)

data_dict =data['hits']['hits']
print(len(data_dict))
for i in data_dict:
    print( i['_id'])

#15279


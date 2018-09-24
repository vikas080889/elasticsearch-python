import requests
import json
from datetime import date
from elasticsearch import Elasticsearch
headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'https://economictimes.indiatimes.com/marketstats/company-true,ctype-BOLLINGER,exchange-50,indexid-2365,pageno-1,pid-241,sortby-volume,sortorder-desc.cms'}

url = 'https://sas.indiatimes.com/TechnicalsClient/getEMA.htm?crossovertype=CROSSED_ABOVE_EMA_50&pagesize=150&pid=220&exchange=50&pageno=1&sortby=volume&sortorder=desc&indexid=2365&company=true&ctype=EMA&callback=ajaxResponse&totalpages=4&col_show=50'

es = Elasticsearch(['http://localhost:9200'])


def store_to_es(stock,ltp,EMA50,crossing_day_price,diff_with_ema_crossingday,diff_with_ema_today,entry_date,cid):
    try:

        es.index(index='ema_50_analysis', doc_type='blog', id=cid, body={
            'stock': stock,
            'ltp': ltp,
            'EMA50':EMA50,
            'crossing_day_price':crossing_day_price,
            'diff_with_ema_crossingday':diff_with_ema_crossingday,
            'diff_with_ema_today':diff_with_ema_today,
            'entry_date' : entry_date
        })
    except:
        print("some issue is there")



def get_daily_close_price(cid):
    ltp_url ='https://json.bselivefeeds.indiatimes.com/ET_Community/companypagedata?companyid='+cid+'&companytype=&callback=ets.hitMarketResponse'
    ltp = requests.get(ltp_url)
    ltp = ltp.text
    ltp_data = ltp[22:-2]
    ltp_dict = json.loads(ltp_data)
    return ltp_dict['bseNseJson'][0]['lastTradedPrice']

def fetch_data_with_cid_store():
    doc = {
        'size': 10000,
        'query': {
            'match_all': {}
        }
    }
    data = es.search(index='ema_50_analysis', doc_type='blog', body=doc)
    data_dict =data['hits']['hits']
    for i in data_dict:
        close_price =float(get_daily_close_price(i['_id']))
        print(i['_id'],close_price,i['_source']['EMA50'])
        try:
             es.update(index='ema_50_analysis', doc_type='blog', id=i['_id'], body={"doc": {"ltp":close_price,'diff_with_ema_today':round(close_price-i['_source']['EMA50'])}})
        except:
            print('na')


fetch_data_with_cid_store()



#print((list(y)[2][0]['lastTradedPrice']))
indexurl = requests.get(url=url, headers=headers)

#print (indexurl.text[13 :-1])

m_string = indexurl.text[13:-1]


m_dict = json.loads(m_string)
#print(m_dict)

data = m_dict['searchResult']
entry_date=date.today().strftime('%b-%d-%Y')


#print(data[-1:])
for i in data :
    if((float(i['volume'])>=20000) and (float(i['currentPrice'])>30)):
         stock,companyId,EMA50,crossing_day_price,diff_with_ema_crossingday= i['companyName'],i['companyId'],i['currentEma50'],i['currentPrice'],round(float(i['currentPrice'])-float(i['currentEma50']),2)
         lt_dict = get_daily_close_price(companyId)


         #print(lt_dict)
         #price = myprint(lt_dict)
         ltp = float(lt_dict)
         diff_with_ema_today = round(ltp-EMA50,2)
         store_to_es(stock,ltp,EMA50,crossing_day_price,diff_with_ema_crossingday,diff_with_ema_today,entry_date,companyId)




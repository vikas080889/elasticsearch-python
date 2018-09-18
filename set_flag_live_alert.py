import re
import requests
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import smtplib
import urllib3
import constants
from elasticsearch import Elasticsearch
from datetime import datetime ,date

headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'https: // www.nseindia.com / live_market / dynaContent / live_watch / get_quote / GetQuote.jsp?symbol = TCS'}

es = Elasticsearch(['http://localhost:9200'])
#print(time.time())


for k in range(1):

    try :
        for j in constants.s_code:
            args = {"symbol":j, "series": "EQ"}
            #print(args)

            url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?{}".format(
            urllib3.request.urlencode(args))
            #print(url)

            quote_eq_url = requests.get(url=url, headers=headers)

            response = BeautifulSoup(quote_eq_url.text, "lxml") #print(type(response))

            s_res = str(response)
            #print(s_res)

            # m = re.match(r"(.*)lastPrice\":\"(\d+\.\d+)", s_res)
            m = re.match(r"(.*)lastPrice\":\"(\d+(.*?)[.]\d+)", s_res)
            #print(m)
            if m:
            #print(m.group(2))
                ltr = float(m.group(2).replace(',',''))
                #print(j,ltr)
            try :
                descision = es.get(index='alerting', doc_type='blog', id=j)
                down = descision.get('_source')['Flag_Down']
                up = descision.get('_source')['Flag_UP']
               # print(j,flag, not flag)
               # ltr = descision.get('_source')['LTR']
                ltr = ltr


                data = es.get(index='stocks_data', doc_type='blog', id=j)
                ma_50 = data.get('_source')['50MA']
               # print(j, flag, not flag,ltr,fifty)
            except:
                print("lolz")

            if (ltr < ma_50):
                if (down):
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_Down": True,'diff':round(ltr-ma_50,2)}})

                    #print("already set", j)
                if (not down):
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_Down": True,'change_date':date.today().strftime('%b-%d-%Y'),'log':'Bearish Ltr below 50 MA','diff':round(ltr-ma_50,2)}})
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_UP": False,'change_date':date.today().strftime('%b-%d-%Y'),'log':'Bearish Ltr below 50 MA','diff':round(ltr-ma_50,2)}})
                    print(str(datetime.now()))

                    print("updated price ghati hai ", j)
            if (ltr > ma_50):
                if (up):
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_UP": True,'diff':ltr-ma_50}})

                    # print("already set", j)
                if (not up):
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_UP": True,'change_date':date.today().strftime('%b-%d-%Y'),'log':'Bullish Ltr Above 50 MA','diff':round(ltr-ma_50,2)}})
                    es.update(index='alerting', doc_type='blog', id=j, body={"doc": {"Flag_Down": False,'change_date':date.today().strftime('%b-%d-%Y'),'log':'Bullish Ltr Above 50 MA','diff':round(ltr-ma_50,2)}})
                    print(str(datetime.now()))

                    print("updated up walla price badhi hqi ", j)
    except:
        print("something went wrong")

    #time.sleep(900)

   # print(alert)

#print(ma50)

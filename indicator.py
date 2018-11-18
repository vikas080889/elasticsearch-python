from elasticsearch import Elasticsearch
import elasticsearch
import constants
import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import date
from datetime import timedelta
import re
import time

es = Elasticsearch(['http://localhost:9200'])

now = date.today()
#print(now)
#round(stock.Close_Price.rolling(window=9).mean()[8],2)
#stock = get_history(symbol='SBIN',start=(now -timedelta(69)), end=(now -timedelta(30)))

#print(stock[0:1])
#print(stock[-1:])

headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'https: // www.nseindia.com / live_market / dynaContent / live_watch / get_quote / GetQuote.jsp?symbol = TCS'}






#nine_MA = round(stock.Close_Price.rolling(window=9).mean()[k],2)
#twenty_MA = round(stock.Close_Price.rolling(window=20).mean()[k],2)
j=0
for x in constants.s_code:
    '''
    stock = get_history(symbol=constants.s_code[j], start=(now - timedelta(3)), end=now)
#                   time.sleep(1)
    short_stock = stock.loc[:, 'Symbol':'Volume']
    # print(short_stock.columns)
    short_stock.columns = ['Symbol', 'Series', 'PrevClose', 'OpenPrice', 'HighPrice', 'LowPrice', 'LastPrice',
                           'ClosePrice', 'AveragePrice', 'Vol']

    short = short_stock.Symbol
    '''
    payload = {'pairID': constants.s_id[j], 'period': '86400', 'viewType': 'normal'}
    hourpay = {'pairID': constants.s_id[j], 'period': 'month', 'viewType': 'normal'}
    pay_pivot= {'pairID': constants.s_id[j], 'period': 'month', 'viewType': 'normal'}


    #-----------------------------------------------------------------------
    # uncomment when macd and other stuff is required

    try :

        rsi_req = requests.post(url='https://in.investing.com/instruments/Service/GetTechincalData',
                                           data=payload, headers={'X-Requested-With': 'XMLHttpRequest',
                                                                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
        rsi_req = BeautifulSoup(rsi_req.content, "lxml")
        day_RSI = rsi_req.find("td", text="RSI(14)").find_next_sibling("td").text
        day_RSI = float(day_RSI)
        fifty_MA = rsi_req.find("td", text="MA50").find_next_sibling("td").text
        fifty_MA = re.sub('\s+', '', fifty_MA)
        match = re.match(r"([\d+\.\d]+)([a-z]+)", fifty_MA, re.I)
        if match:
            fifty_MA_items = match.groups()
            # print(type(thirty_min_items[0]))
            fifty_ma_int = float(fifty_MA_items[0].replace(',', ''))
            #print(fifty_MA_items)
        twenty_MA = rsi_req.find("td", text="MA20").find_next_sibling("td").text
        twenty_MA = re.sub('\s+', '', twenty_MA)
        match = re.match(r"([\d+\.\d]+)([a-z]+)", twenty_MA, re.I)
        if match:
            twenty_MA_items = match.groups()
            # print(type(thirty_min_items[0]))
            twenty_MA_int = float(twenty_MA_items[0].replace(',', ''))
            # print(fifty_MA_items)

        macd = rsi_req.find("td", text="MACD(12,26)").find_next_sibling("td").text
        macd = float(macd)
    except :
        print("issue with investing")
    #------------------------------------------------


    #-------------------------------------------------------------------------
    #uncomment when Pivot is required
    try :
    
        pay_pivot =requests.post(url='https://in.investing.com/instruments/Service/GetTechincalData',
                                           data=pay_pivot, headers={'X-Requested-With': 'XMLHttpRequest',
                                                                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
        pivot_req = BeautifulSoup(pay_pivot.content, "lxml")
        pivot_array = pivot_req.findChildren("td", {'class': 'first left bold noWrap'})
        list = []
        for siblings in pivot_array[1].next_siblings:
            if siblings == '\n':
                print("ooooo")
            else:
                list.append(float(siblings.contents[0].replace(',', '')))
                #print(list)
        sup3 = list[0]
        sup2 = list[1]
        sup1 = list[2]
        pivot = list[3]
        res1 = list[4]
        res2 = list[5]
        res3 = list[6]
    except:
        print("issue with pivot")

    #---------------------------------------------------------------------
    # uncomment when MA data is required

    '''
    hour_req = requests.post(url='https://in.investing.com/instruments/Service/GetTechincalData',
                            data=hourpay, headers={'X-Requested-With': 'XMLHttpRequest',
                                                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})

    hour_req = BeautifulSoup(hour_req.content, "lxml")

    h_50 = hour_req.find("td", text="MA50").find_next_sibling("td").text
    h_50 = re.sub('\s+', '', h_50)
    match = re.match(r"([\d+\.\d]+)([a-z]+)", h_50, re.I)
    if match:
        h_50_items = match.groups()
        # print(type(thirty_min_items[0]))
        h_50_int = float(h_50_items[0].replace(',', ''))
    '''
    

    #--------------------------------------------------------------------------------
    #get live price
    try :
        args = {"symbol":constants.s_code[j], "series": "EQ"}
        url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?{}".format(
            urllib3.request.urlencode(args))
        quote_eq_url = requests.get(url=url, headers=headers)
        response = BeautifulSoup(quote_eq_url.text, "lxml")  # print(type(response))

        s_res = str(response)
        # print(s_res)

        # m = re.match(r"(.*)lastPrice\":\"(\d+\.\d+)", s_res)
        m = re.match(r"(.*)lastPrice\":\"(\d+(.*?)[.]\d+)", s_res)
        # print(m)
        if m:
            # print(m.group(2))
            ltr = float(m.group(2).replace(',', ''))
            print(ltr,constants.s_code[j],pivot)
    except :
        print("isse with nse")
    #----------------------------

    #uncomment when data from NSE is required
    #print(short_stock.index[0])
    '''
    k = 0
    for i in short:
       # print((i))
        cp = float(short_stock.ClosePrice[k])
        print(short_stock.Symbol[k],cp)
        previous_1 = float(short_stock.ClosePrice[k-1])
        #print(previous)
        pr_cp_1  = float(previous_1)
        if (math.isnan(pr_cp_1)):
            pr_cp = -999999

#item['Adj Close'].rolling(window=20).std()
        op = float(short_stock.OpenPrice[k])

        per_change = round((cp -pr_cp_1)*100/pr_cp_1,2)

        #nine_MA = float(round(short_stock.ClosePrice.rolling(window=9).mean()[k], 2))
        #if (math.isnan(nine_MA)):
         #   nine_MA=-999999
       # s_dev = float(round(short_stock.ClosePrice.rolling(window=20).std()[k], 2))


       # twenty_MA = float(round(short_stock.ClosePrice.rolling(window=20).mean()[k], 2))
        #if (math.isnan(twenty_MA)):
        #    twenty_MA = -999999


        position = cp - twenty_MA_int

        pos_var = np.where(position<0,'s','b')
        #print(pos_var)

        # print(nine_MA,twenty_MA)
        #print(es)
        #es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
        #es.delete(index='stocks_data', doc_type='SBI', id=now.day)
        es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
    # es.delete(index='stocks_data', doc_type='SBI', id=now.day)
'''
    try:
        '''
        es.update(index='stocks_data', doc_type='blog', id=constants.s_code[j], body={"doc":{
        'Close_Price': ltr,
        'Open_price': 999999,
        #'Prv_Close': pr_cp_1,
        '20_MA': twenty_MA_int,
        'PoS': 'na',
        'Hourly_50_MA' : h_50_int,
        'change'+'@'+str(now):0.0,
        'RSI':day_RSI,
        'MACD':macd,
        '50MA':fifty_ma_int,
        'S1':sup1,
        'S2':sup2,
        'S3':sup3,
        'Pivot': pivot,
        'R1':res1,
        'R2':res2,
        'R3':res3
        }})
        '''

        es.update(index='stocks_data', doc_type='blog', id=constants.s_code[j], body={"doc":{
        'Close_Price': ltr,
        #'Open_price': 999999,
        #'Prv_Close': pr_cp_1,
        #'20_MA': twenty_MA_int,
        #'PoS': 'na',
        #'Hourly_50_MA' : h_50_int,
        #'change'+'@'+str(now):0.0,
        #'RSI':day_RSI,
        #'MACD':macd,
        '50MA':fifty_ma_int,
        'S1':sup1,
        'S2':sup2,
        'S3':sup3,
        'Pivot': pivot,
        'R1':res1,
        'R2':res2,
        'R3':res3
        }})

    except:
        print("no update")


    j +=1
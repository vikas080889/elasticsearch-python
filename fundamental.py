import requests
import re
from elasticsearch import Elasticsearch

from bs4 import BeautifulSoup , Comment
es = Elasticsearch(['http://localhost:9200'])

for x in range(21):
    url = 'https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=gainer*all$all$&Page='+str(x+1)
    #url  = 'https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=loser*all$all$&Page='+str(x+1)
    #print(url)

    data = requests.get(url)
    data = BeautifulSoup(data.text ,'lxml')

    #print(data)
    data_1 = data.find_all('tr',{'class':'TTRow'})


    for i in data_1:
        try:
            #print(i)
            print(i.td.next_sibling.text)
            #print(i.a.get('href'))
            murl = 'https://h.marketsmojo.com/stocks/fin_trend/'+i.td.text+'.html'
            res = requests.get(murl)
            res = BeautifulSoup(res.text,'lxml')
            #print(res)

            pd = res.find('div',{'class':'fin-bottomright'})
            pd = pd.get('onclick')[13:-2]


            verdict = res.find('div', {'class': 'scorehead'})
            descrptn = res.find('div', {'class': 'lefthead'})
            ver = re.sub('\s+', '', verdict.text)
            ver1 = re.sub('\t+', '', descrptn.text)
            ver1 = ver1.lstrip()
            name = ver1.split()[:2]
            y = " ".join(ver1.split()[:2])

            #print(ver, ':', y, ':', ver1)



            m = re.search(r'(.*?)StockId=(.*?)&Exchange', pd).group(2)
            print(m)
            print(pd)
            url_1 = 'https://www.marketsmojo.com/Stocks?StockId='+m+'&Exchange=0#!#navDashboard'
            print(url_1)
            data = requests.get(url_1)
            data = BeautifulSoup(data.text, 'lxml')
            # print(data.find_all('div', class_='switch-market'))

            ele = []

            df = data.find_all(text=lambda text: isinstance(text, Comment))
            df = df[15].string
            df = re.sub('\s+', '', df)
            #print((df))

            quality = re.search(r'(.*?)Quality</h6><pclass=(.*?)>(.*?)</p></aside', df).group(3)
            valuation = re.search(r'(.*?)Valuation</h6><pclass="(.*?)">(.*?)</p></aside', df).group(3)
            fintrend = re.search(r'(.*?)FinTrend</h6><pclass="(.*?)">(.*?)</p>', df).group(3)

            print(url_1,quality, valuation, fintrend)

            es.index(index='mojomojo', doc_type='blog', id=i.td.next_sibling.text, body={
                'quality': quality,
                'valuation': valuation,
                'fintrend':fintrend,
                'url': url_1
            })


        except:
            print("no analysis available")










































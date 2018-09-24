import requests
import re
from bs4 import BeautifulSoup , Comment
import json


urllist = ['https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=gainer*all$all$&Page=',
           'https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=loser*all$all$&Page=']


def get_bse_gainer_data(x):
    gainer = 'https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=gainer*all$all$&Page='
    gainer_url = gainer + str(x+1)
    data = requests.get(gainer_url)
    data = BeautifulSoup(data.text, 'lxml') # print(data)
    data = data.find_all('tr', {'class': 'TTRow'})
    return (data)


def get_bse_loser_data(x):
    loser = 'https://www.bseindia.com/markets/equity/EQReports/MktWatchR.aspx?filter=loser*all$all$&Page='
    loser_url = loser + str(x+1)
    data = requests.get(loser_url)
    data = BeautifulSoup(data.text, 'lxml') # print(data)
    data = data.find_all('tr', {'class': 'TTRow'})
    return (data)



def stock_details(myList):
    name =[]
    murl = []
    try:
        for i in myList:
            name.append(i.td.next_sibling.text)
            murl.append('https://h.marketsmojo.com/stocks/fin_trend/'+i.td.text+'.html')
        return name ,murl
    except:
        return "NA","NA"


def get_jojo_url(mystr):
    try:
        res = requests.get(mystr)
        #print(res.text)
        res = BeautifulSoup(res.text, 'lxml')  # print(res)
        pd = res.find('div', {'class': 'fin-bottomright'})
        pd = pd.get('onclick')[13:-2]
        m = re.search(r'(.*?)StockId=(.*?)&Exchange', pd).group(2)
        jojo_quality = 'https://www.marketsmojo.com/Stocks?StockId='+m+'&Exchange=0#!#navDashboard'
        jojo_summary = 'https://frapi.marketsmojo.com/stocks_dashboard/stockinfo?sid='+m+'&callback=jQuery21105692901213009467_1536953494358'
        return jojo_quality ,jojo_summary
    except:
        return "NA","NA"



def fetch_quality_info(myurl):
    try :
        data = requests.get(myurl)
        data = BeautifulSoup(data.text, 'lxml')
        #3mojo_info = data.find('td',{'class':'topbgcolum'}).text
        #print(mojo_info)
        df = data.find_all(text=lambda text: isinstance(text, Comment))

        df = df[15].string
        df = re.sub('\s+', '', df)
        # print((df))

        quality = re.search(r'(.*?)Quality</h6><pclass=(.*?)>(.*?)</p></aside', df).group(3)
        valuation = re.search(r'(.*?)Valuation</h6><pclass="(.*?)">(.*?)</p></aside', df).group(3)
        fintrend = re.search(r'(.*?)FinTrend</h6><pclass="(.*?)">(.*?)</p>', df).group(3)

        return quality,valuation,fintrend
    except:
        return "NA","NA","NA"

def fetch_summary(myurl):
    try:
        data = requests.get(myurl)
        data = data.text
        data = json.loads(data[41:-1])
        jo_stock_label = data['data']['stocklabel']['text']
        return jo_stock_label
    except:
        return "NA"





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
    #print(loser_url)
    data = requests.get(loser_url)
    data = BeautifulSoup(data.text, 'lxml') # print(data)
    data = data.find_all('tr', {'class': 'TTRow'})
    #print(data)
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
        jojo_technical = 'https://www.marketsmojo.com/technical?sid='+m+'&exchange=0'
        return jojo_quality,jojo_summary,jojo_technical
    except:
        return "NA","NA","NA"



def get_volume_from_technical(url):
    try:
        data = requests.get(url)

        soup = BeautifulSoup(data.text, "lxml")
        size = soup.find('div', {'id': 'topsensex'})
        chlist = []
        for i in size.children:
            chlist.append(i)
        com_size = str(chlist[-2:])
        #print(com_size)
        com_size = re.search(r'<span>MARKET CAP:  <strong2> Rs (.*)\s+\((.*)\)</strong2></span>', com_size)
        com_size = com_size.group(2)
        vol = soup.find("span", {'class': "volval"})
        vol_fig = vol.get('ng-init')
        vol_fig = re.match(r'total_vol = \'(\d+\.\d+)\s(.*?)\'', vol_fig)
        vol_unit = vol_fig.group(2)
        number = float(vol_fig.group(1))
        qp_data = soup.findAll("h6")
        Quality = (qp_data[0].span.text).strip('\':\s+\n').replace(' ','')
        Valuation=qp_data[1].span.text.strip('\':\s+\n').replace(' ','')
        Fintrend = qp_data[2].span.text[:-11].strip('\':\s+\n').replace(' ','')
        if vol_unit=='k':
            actual_vol = round(number*1000,0)
        elif vol_unit=='lacs':
            actual_vol = round(number * 100000,0)
        elif vol_unit=='cr':
            actual_vol = round(number * 10000000,0)
        return actual_vol,Quality,Valuation,Fintrend,url,com_size
    except:
        return "NA","NA","NA","NA","NA","NA"




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





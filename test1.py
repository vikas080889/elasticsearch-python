import requests
from bs4 import  BeautifulSoup
import re

url = 'https://www.marketsmojo.com/technical?sid=347516&exchange=0'


data = requests.get(url)

soup = BeautifulSoup(data.text, "lxml")
size = soup.find('div',{'id':'topsensex'})
'''
for i in size.next_siblings:
    print (i)
    
for i in size.span.next_siblings:
    print (i)    
'''
chlist =[]
for i in size.children:
    chlist.append(i)
com_size=str(chlist[-2:])
print(com_size)
com_size = re.search(r'<span>MARKET CAP:  <strong2> Rs (.*)\s+\((.*)\)</strong2></span>',com_size)
com_size =com_size.group(2)

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
print(actual_vol,Quality,Valuation,Fintrend,url)

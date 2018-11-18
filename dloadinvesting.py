from elasticsearch import Elasticsearch
import elasticsearch
import constants
import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import date
from datetime import timedelta
import re
import pandas as pd

headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, br',
         'Connection':'keep-alive',
         'Accept-Language':'en-US,en;q=0.9,und;q=0.8',
         'Cookie':'adBlockerNewUserDomains=1514954803; optimizelyEndUserId=oeu1514954811265r0.7912466619640768; optimizelyBuckets=%7B%7D; r_p_s=1; _ga=GA1.2.104903267.1514954812; __gads=ID=3b7c28fb670fc772:T=1514954806:S=ALNI_MYKZHBelVzwN9V1z8M51kZIp2SrtA; __qca=P0-1663801976-1514954813833; G_ENABLED_IDPS=google; isUserNoticedNewAlertPopup=1; emailAlertSetting=1; optimizelySegments=%7B%224225444387%22%3A%22gc%22%2C%224226973206%22%3A%22referral%22%2C%224232593061%22%3A%22false%22%2C%225010352657%22%3A%22email%2520alerts%22%7D; r_p_s_n=1; _gid=GA1.2.1055916934.1539770885; PHPSESSID=g1j0p8tnj6nmnpc3bt688di7b6; comment_notification_200448455=1; geoC=IN; StickySession=id.28756343114.228in.investing.com; gtmFired=OK; UserReactions=true; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22946649%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A39%3A%22%2Fequities%2Ftalwalkars-better-val-fitness%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2218376%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A29%3A%22%2Fequities%2Fstate-bank-of-india%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2217998%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A24%3A%22%2Fequities%2Fambuja-cements%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2218100%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A13%3A%22%2Fequities%2Fdlf%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2217940%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Findices%2Fs-p-cnx-nifty%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2218467%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fequities%2Fwipro-ltd%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2217949%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A16%3A%22%2Findices%2Fcnx-200%22%3B%7D%7D%7D%7D; _gat=1; _gat_allSitesTracker=1; billboardCounter_56=1; nyxDorf=MTVmN2QwN3VmMWFqbjowLGM3NGcyKzc0NDczOQ%3D%3D; ses_id=NnhkJTE%2BMTkydj07ZTQxM2MyNGs%2BPTsxNzJhZ2NhZXMxJTY4NWI3cTY5byFlZmV5NDNmZDdjNDc0YWc5YzQ3ZjZlZDcxMTFtMmE9MGVkMWFjYzRnPjw7MTc3YWdjYmU9MTU2YzU2NzI2aG9iZWtlbjQmZno3czQlNGZnN2MiN3A2OWQlMWIxPzI3PTZlNTEzYzo0Oj4%2FOz83NGFjY2ZlfTF6',
          'Referer':'https://in.investing.com/indices/cnx-200-components',
         'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
'''
url ='https://in.investing.com/indices/service/TechnicalInstrument?pairid=17949&sid=0.5172290647136841&smlID=2036491&category=Technical&download=true&sort_col=name&sort_ord=a'
rsi_req = requests.get(url=url,headers=headers,stream=True)

with open('nifty200.csv', "wb") as csv:
    for chunk in rsi_req.iter_content(chunk_size=1024):

        # writing one chunk at a time to pdf file
        if chunk:
            csv.write(chunk)
#print(rsi_req.content)
'''
df = pd.read_csv('nifty200.csv')
for i,row in df.iterrows():
   print(df.iloc[i,[0,2]])



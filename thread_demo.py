import requests ,json ,re
from elasticsearch import Elasticsearch
import queue
import time

import threading

es = Elasticsearch(['http://localhost:9200'])


def load_es(mojo_tech_url,name,industry,market_cap,volume,vol_msg,pe_ratio,ind_pe,quality,valuation,fin_trend,ltp):
    time.sleep(2)
    es.index(index="thread_test",doc_type="blog",id=name,body={
        'URL': mojo_tech_url,
        'industry': industry,
        'market_cap': market_cap,
        'volume': int(volume),
        'vol_msg': vol_msg,
        'pe_ratio': float(pe_ratio),
        'ind_pe': float(ind_pe),
        'quality': quality,
        'valuation': valuation,
        'fin_trend': fin_trend,
        'LTP':ltp
    })

#https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=gainer&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all
#https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=loser&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all
def get_bse_losing_stocks(status):
    url= f"https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype={status}&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
    data = requests.get(url)
    data = json.loads(data.text)
    stock_list = data["Table"]
    return stock_list


def get_individual_stock_details(stock_list):
    try:
        #for i in stock_list:
        stock_code=stock_list['scrip_cd']
        #print(stock_code)
        bse_mojo_url="https://h.marketsmojo.com/stocks/fin_trend/"+str(stock_code)+".html"
        mojo_url = requests.get(bse_mojo_url)
        mojo_code = re.findall(r'\d+', mojo_url.text)
        #print(mojo_code)
        mojo_code=mojo_code[0]
        #print(type(mojo_code))
        mojo_details_url ="https://www.marketsmojo.com/portfolio-plus/headerdetails?sid="+mojo_code+"&exchange=1&return=1"
        #print(mojo_details_url)
        mojo_tech_url = "https://www.marketsmojo.com/technical?sid="+mojo_code+"&exchange=0"
        #print(mojo_tech_url)
        mojo_data = requests.get(mojo_details_url)
        mojo_data = json.loads(mojo_data.text)
        #print(mojo_data)
        name = mojo_data['data']['stock_details']['short_name']
        #print(name)
        industry = mojo_data['data']['stock_details']['ind_name']
        market_cap = mojo_data['data']['nse']['mcap_class']
        volume = stock_list['trd_vol']
        ltp = float(stock_list['ltradert'])
        #volume = re.findall(r'\d+.\d+',volume)
        vol_msg = mojo_data['data']['nse']['vol_msg']
        pe_ratio = mojo_data['data']['nse']['pe_ratio']
        ind_pe  = mojo_data['data']['nse']['ind_pe_ratio']
        quality = mojo_data['data']['stock_details']['dot_summary']['quality_text']
        valuation = mojo_data['data']['stock_details']['dot_summary']['valuation_text']
        fin_trend = mojo_data['data']['stock_details']['dot_summary']['fin_trend_text']
        print(mojo_tech_url,name,industry,market_cap,volume,vol_msg,pe_ratio,ind_pe,quality,valuation,fin_trend,ltp)
        #out_queue.put((mojo_tech_url,name,industry,market_cap,volume,vol_msg,pe_ratio,ind_pe,quality,valuation,fin_trend,ltp))

        load_es(mojo_tech_url,name,industry,market_cap,float(volume),vol_msg,float(pe_ratio),float(ind_pe),quality,valuation,fin_trend,ltp)
    #yield (mojo_tech_url,name,industry,market_cap,volume,vol_msg,pe_ratio,ind_pe,quality,valuation,fin_trend)
    except:
        pass


if __name__== "__main__":
    #my_queue = queue.Queue()
    for st in ['loser','gainer']:
        stock_list = get_bse_losing_stocks(st)
        dlist =[]



        for count,i in enumerate(stock_list):
            while(threading.active_count()>8):
                time.sleep(5)
            try:
                worker = threading.Thread(target=get_individual_stock_details,args=(i,))

                worker.start()
                print(threading.active_count())

                #worker.my_queue.get()


            except:
                pass

        #time.sleep(1)
        #print("done")










'''
bse_mojo_url="https://h.marketsmojo.com/stocks/fin_trend/"+"541771"+".html"
mojo_url=requests.get(bse_mojo_url)

mojo_code=re.findall(r'\d+',mojo_url.text)

print(mojo_code[0])

mojo_details_url ="https://www.marketsmojo.com/portfolio-plus/headerdetails?sid="+mojo_code[0]+"&exchange=1&return=1"
data = requests.get(mojo_details_url)
must=json.loads(data.text)
print(must['data']['nse']['mcap_class'],must['data']['nse']['vol_msg'],must['data']['nse']['vol_msg'],must['data']['nse']['pe_ratio'],must['data']['nse']['ind_pe_ratio'])

print(must['data']['stock_details']['short_name'],must['data']['stock_details']['ind_name'])
print(must['data']['stock_details']['dot_summary']['quality_text'],must['data']['stock_details']['dot_summary']['valuation_text'],must['data']['stock_details']['dot_summary']['fin_trend_text'])
'''

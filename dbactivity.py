import bse
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])


def run_test_loser_volume():
    for i in range(0,21):
        loser_list = bse.get_bse_loser_data(i)
       # print(loser_list)

        stock_name,bse_url = bse.stock_details(loser_list)
        #print(bse_url)

        for i, y in enumerate(bse_url):
            #print(y)
            url_quality,url_stock_label ,url_volume= bse.get_jojo_url(y)
            actual_vol, Quality, Valuation, Fintrend,url ,com_size= bse.get_volume_from_technical(url_volume)
            stock = stock_name[i]
            #print(actual_vol, Quality, Valuation, Fintrend,url)
            yield (actual_vol,Quality,Valuation,Fintrend,stock,url,com_size)



def run_test_gainer_volume():
    for i in range(0,21):
        gainer_list = bse.get_bse_gainer_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(gainer_list)
       # print(bse_url)

        for i, y in enumerate(bse_url):
            #print(y)
            url_quality,url_stock_label ,url_volume= bse.get_jojo_url(y)
            actual_vol, Quality, Valuation, Fintrend,url,com_size = bse.get_volume_from_technical(url_volume)
            stock = stock_name[i]
            yield (actual_vol,Quality,Valuation,Fintrend,stock,url,com_size)





def run_test_gainer():
    for i in range(0,21):
        gainers_list = bse.get_bse_gainer_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(gainers_list)
       # print(bse_url)

        for i,y in enumerate(bse_url):
            url_quality,url_stock_label,jojo_technical = bse.get_jojo_url(y)
            label = bse.fetch_summary(url_stock_label)
            stock = stock_name[i]
            yield (label,url_quality,stock)

def run_test_loser():
    for i in range(0,21):
        loser_list = bse.get_bse_loser_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(loser_list)
       # print(bse_url)

        for i, y in enumerate(bse_url):
            #print(y)
            url_quality,url_stock_label,jojo_technical = bse.get_jojo_url(y)
            label = bse.fetch_summary(url_stock_label)
            stock = stock_name[i]
            yield (label,url_quality,stock)



def load_es_volume(mydata):
    try:
        #print(mydata[0],mydata[1],mydata[2],mydata[3],mydata[4],mydata[5],mydata[6])
        es.index(index='volume_mojo', doc_type='blog', id=mydata[4], body={
            'volume':mydata[0],
            'quality':mydata[1],
            'valuation':mydata[2],
            'fintrend':mydata[3],
            #'stock_label': mydata[4],
            'url': mydata[5],
            'com_size':mydata[6]
        })
    except:
        print("some issue is there")

def load_es(mydata):
    try:
        #print(mydata[0],mydata[1],mydata[2])
        es.index(index='mojostockslist', doc_type='blog', id=mydata[2], body={
            'stock_label': mydata[0],
            'url': mydata[1]
        })
    except:
        print("some issue is there")

if __name__ == "__main__":

    z = run_test_loser_volume()
    # print(z)
    for d in z:
        d = list(d)
        print(d)
        load_es_volume(d)

    y = run_test_gainer_volume()
    for d in y:
        d = list(d)
        print(d)
        load_es_volume(d)

    x = run_test_loser()
    for i in x:
        i = list(i)
        print(i[0], i[1], i[2])
        load_es(i)

    p = run_test_gainer()
    for d in p:
        d = list(d)
        print(d)
        load_es(d)



























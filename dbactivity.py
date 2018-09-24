import bse
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])


#---------------
#uncomment when stock labael is required

def run_test_gainer():
    for i in range(0,21):
        gainers_list = bse.get_bse_gainer_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(gainers_list)
       # print(bse_url)

        for i,y in enumerate(bse_url):
            url_quality,url_stock_label = bse.get_jojo_url(y)
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
            url_quality,url_stock_label = bse.get_jojo_url(y)
            label = bse.fetch_summary(url_stock_label)
            stock = stock_name[i]
            yield (label,url_quality,stock)

#----------------------------------------
'''
def run_test_gainer():
    for i in range(0,21):
        gainers_list = bse.get_bse_gainer_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(gainers_list)
       # print(bse_url)

        for i,y in enumerate(bse_url):
            url_quality,url_stock_label = bse.get_jojo_url(y)
            label = bse.fetch_quality_info(url_quality)
            stock = stock_name[i]
            yield (label,url_quality,stock)


def run_test_loser():
    for i in range(15):
        loser_list = bse.get_bse_loser_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(loser_list)
       # print(bse_url)

        for i, y in enumerate(bse_url):
            #print(y)
            url_quality,url_stock_label = bse.get_jojo_url(y)
            label = bse.fetch_quality_info(url_quality)
            stock = stock_name[i]
            yield (label,url_quality,stock)

'''










def load_es(mydata):
    try:
        print(mydata[0],mydata[1],mydata[2])
        es.index(index='mojostockslist', doc_type='blog', id=mydata[2], body={
            'stock_label': mydata[0],
            'url': mydata[1]
        })
    except:
        print("some issue is there")



if __name__ == "__main__":
    y = run_test_gainer()
    for d in y:
        d = list(d)
        # print(d)
        load_es(d)

    x = run_test_loser()
    for i in x:
        i = list(i)
        #print(i[0],i[1],i[2])
        load_es(i)



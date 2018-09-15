import bse
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from  _thread import start_new_thread

def run_test():
    for i in range(15):
        gainers_list = bse.get_bse_gainer_data(i)
        #print(gainers_list)

        stock_name,bse_url = bse.stock_details(gainers_list)
       # print(bse_url)

        for y in bse_url:
            url_quality,url_stock_label = bse.get_jojo_url(y)
            label = bse.fetch_summary(url_stock_label)
            yield (label,url_quality)


if __name__ == "__main__":
    x = run_test()
    for i in x:
        print(list(i))
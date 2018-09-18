from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
from datetime import date

doc_2 = {
    'size' : 10000,
    "query" : {

    "bool":{
          "should":[

              { "match": {"stock_label":'Mojo Stock'}},
              {"match" :{"stock_label":'Potential Turnaround'}}]
    }}
}
data_2 = es.search(index='mojostockslist', doc_type='blog',body=doc_2)

store_data = data_2['hits']['hits']
for i in store_data:
    es.index(index='snapshot_mojo_stock',doc_type='blog',id=i['_id'],body={
        "URL":i['_source']['url'],
        "Label":i['_source']['stock_label'],
        "Entry_Date":date.today().strftime('%b-%d-%Y')
    }
             )
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])



doc = {
        'size' : 10,
        'query': {
            'match_all' : {}
       }
   }


doc_1 = {
    'size' : 50,
    "query" : {

        "match" : {"stock_label":'Mojo Stock'}
    }
}


doc_2 = {
    'size' : 10000,
    "query" : {

    "bool":{
          "should":[

              { "match": {"quality":'Excellent'}},
              {"match" :{"quality":'Good'}}]
    }}
}

# code to get all records from elastic search
data = es.search(index='mojostockslist', doc_type='blog',body=doc)
# code to get records with a filed variable
data_1 = es.search(index='mojostockslist', doc_type='blog',body=doc_1)
#code to apply or condition in elastic search
data_2 = es.search(index='mojomojo', doc_type='blog',body=doc_2)

#ds = data[0].get('_source')['stock_label']

#print(data_2)

result_1 = data_1

#print(data_1)

result = data_2['hits']['hits']

for i in result:
    quality = i['_source']['quality']
    id = i['_id']

    stock_label= es.search(index='mojostockslist', doc_type='blog',body={
        "_source": ['stock_label','url'],
        "query": {
             "terms":
                 {   "_id": [id]}


                 }
    }
                )
    print(stock_label)




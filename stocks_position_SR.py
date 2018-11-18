from elasticsearch import Elasticsearch
import constants
import elasticsearch
import pandas as pd
import datetime
from nsepy import get_history
from datetime import date
from datetime import timedelta

es = Elasticsearch(['http://localhost:9200'])

#print(now)


downtrend = []
uptrend =[]



def ltp(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        return cprice
    except:
        return '404'



def between_s3_s2(stock):
    try:

        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])

        s3 = data.get('_source')['S3']
        s2 = data.get('_source')['S2']

        if (cprice > s3 and cprice < s2):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'



def between_R1_Pivot(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])

        pivot = data.get('_source')['Pivot']

        R1 = data.get('_source')['R1']

        if (cprice > pivot and cprice < R1):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'













def between_R3_R2(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)

        r3 = data.get('_source')['R3']
        r2 = data.get('_source')['R2']

        if (cprice < r3 and cprice > r2):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'



def belowMA50(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)
        fifty = data.get('_source')['50MA']

        if (cprice < fifty):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'

def between_pivot_S1(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)
        fifty = data.get('_source')['Hourly_50_MA']
        pivot = data.get('_source')['Pivot']
        S1= data.get('_source')['S1']
        S2 = data.get('_source')['S2']
        #change = data.get('_source')['change@2018-08-09']
        pos = data.get('_source')['PoS']
        if (cprice < pivot and cprice>S1):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'



def between_S1_S2(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)
        fifty = data.get('_source')['Hourly_50_MA']
        S3 = data.get('_source')['S3']
        S1= data.get('_source')['S1']
        S2 = data.get('_source')['S2']
        #change = data.get('_source')['change@2018-08-09']
        pos = data.get('_source')['PoS']
        if (cprice<S1 and cprice>S2):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'




def between_R1_R2(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)

        R1 = data.get('_source')['R1']
        R2= data.get('_source')['R2']

        if (cprice<R2 and cprice>R1):
            #list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'

def below_s3(stock):
    try:
        list = []
        data = es.get(index='stocks_data', doc_type='blog', id=stock)
        # print(data)
        # ma = es.get(index='stocks_data', doc_type='blog', id=constants.s_code[j])
        cprice = float(data.get('_source')['Close_Price'])
        # print(cprice)

        S3 = data.get('_source')['S3']
        R2 = data.get('_source')['R2']

        if (cprice < S3):
            # list.append(stock)
            return "Yes"
        else:
            return "No"
    except:
        return '404'

'''
def comparison(stock):
    descision = es.get(index='cloaseprice', doc_type='blog', id=stock)

    return descision.get('_source')['Flag']
'''

for j in constants.s_code:

    es.update(index='technical',doc_type='blog',id=j,body={'doc':{
        "LTP":ltp(j),
        "Bn_R3_R2":between_R3_R2(j),
        "Bn_R2_R1": between_R1_R2(j),
        "Bn_R1_Piv":between_R1_Pivot(j),
        "Bn_Piv_S1": between_pivot_S1(j),
        "Bn_S1_S2": between_S1_S2(j),
        "Bn_S2_S3": between_s3_s2(j),
        "Bl_MA_50" :belowMA50(j),
        "BL_S3": below_s3(j)}

    })
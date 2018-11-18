import requests
import json
from scipy.stats import rankdata
import numpy


from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

def get_bse_gainer_details():

    url_1 = 'https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=loser&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all'
    data = requests.get(url_1)
    data = json.loads(data.text)
    #print(type(data))
    data = data['Table']
    #print(data)
    return data

def get_scrip_details(myList):
    for i in myList:
        #print(i)
        code = str(i['scrip_cd'])
        name = i['scripname']
        ltp = i['ltradert']
        vol= int(i['trd_vol'])
        url = i['URL']
        yield code,name,ltp,vol,url

def peer_comparison():
    stock_list = get_bse_gainer_details()
    stock_details_yield = get_scrip_details(stock_list)
    print("Stock", "Promo","Public", "FII", "DII")

    for i in stock_details_yield:
        try :
            i = list(i)
            scode =i[0]
            url = "https://api.bseindia.com/BseIndiaAPI/api/PeerGpCom/w?scripcode="+scode+"&scripcomare="
            url = requests.get(url)
            p_data = json.loads(url.text)
            json_data = p_data['Table']
            #print(json_data)
            holdings=[]
            name = []
            opm = []
            pe=[]
        except:
            pass

        try :
            for k in json_data:
                name.append(k['Name'])
                #print(name)
                try:
                    holdings.append((k['PnPGrp'],k['Public'],k['Institution'],k['FII'],k['DII']))
                except:
                    print("issue in holding")
                try:
                    opm.append(k['OPM'])
                except:
                    opm.append(9999999)
                try:
                    pe.append(k['PE'])
                except:
                    pe.append(9999999)
            #print((holdings[0]))
            rankwrtopm = opm_rank(opm)
            rankwrtope = pe_rank(pe)
            #print(rankwrtope)

            for count,(name,rankwrtopm,rankwrtope) in enumerate(zip(name,rankwrtopm,rankwrtope)):
                #print(name)
                #print(holdings[count])

                promoter_perc, public_perc,fii_perc, dii_perc = share_holding(holdings[count])
                print(name,promoter_perc, public_perc,fii_perc, dii_perc,"rank_pe",rankwrtope,"rank_opm: ",rankwrtopm)
            print(":::::::::::::::::::::::::::::::::::::::::::::")
        except:
            print("some issue")

        #promoter_perc, public_perc, fii_perc, dii_perc=share_holding(holdings)
        #print(name,'\n',promoter_perc, public_perc, fii_perc, dii_perc)

def share_holding(stock):
    promoter,public,institution,fii,dii =stock[0],stock[1],stock[2],stock[3],stock[4]
    promoter_percentage=round((stock[0]*100/(stock[0]+stock[1])),2)
    public_percentage = round((stock[1] * 100 / (stock[0] + stock[1])),2)
    fii_percentage = round((stock[3] * 100 / (stock[0] + stock[1])),2)
    dii_percentage = round((stock[4] * 100 / (stock[0] + stock[1])),2)
    return promoter_percentage,public_percentage,fii_percentage,dii_percentage

def opm_rank(opm):
    try:
        rank_op = rankdata(opm)
        return rank_op
    except:
        rank_op =[0,0,0,0]

def pe_rank(pe):
    try:
        rank_pe = rankdata(pe)
        return rank_pe
    except:
        rank_pe =[0,0,0,0]




if __name__=="__main__":
    peer_comparison()
    #promoter_perc, public_perc, fii_perc, dii_perc=share_holding((2591630.0, 2083499.0, 0.0, 0.0, 0.0))
    #print(promoter_perc, public_perc,fii_perc, dii_perc)





'''
rev_arr=[]
pat_arr= []
eps_arr=[]
pe_arr=[]
for i in json_data:
    rev_arr.append(i['Revenue'])
    pat_arr.append(i['PAT'])
    pe_arr.append(i['PE'])
    eps_arr.append(i['EPS'])

#print(json_data[0])

rank_pat = rankdata(eps_arr)

print(rank_pat)
print(type(rank_pat[0]))
'''





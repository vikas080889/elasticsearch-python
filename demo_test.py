import requests
import re
from scipy.stats import rankdata
from datetime import datetime, date
from bs4 import BeautifulSoup
import time

id_short = ['18294', '17998', '18005', '18008', '18036', '18040', '18041', '39852', '18055', '18057', '18075', '18080', '978762', '18094', '18122', '18137', '39867', '18180', '18187', '18184', '18186', '18198', '991131', '18209', '18213', '18224', '18226', '18276', '18334', '18361', '18364', '18376', '39910', '18422', '18436', '18467']
name_short = ['Adani Port and Special Economic Zone Ltd', 'Ambuja Cements Ltd.', 'Apollo Tyres Ltd', 'Arvind Ltd.', 'Berger Paints India Ltd', 'Bharat Petroleum Corp. Ltd.', 'Bharti Airtel Ltd.', 'Bharti Infratel Ltd', 'Cadila Healthcare Ltd.', 'Canara Bank Ltd', 'Coal India Ltd', 'Coromandel International Ltd', 'Crompton Greaves Consumer Electricals Ltd', 'Dewan Housing Finance Corp. Ltd.', 'Exide Industries Ltd.', 'GAIL Ltd', 'GRUH Finance Ltd', 'Hexaware Technologies Ltd.', 'Hindalco Industries Ltd.', 'Hindustan Petroleum Corporation Ltd', 'Hindustan Zinc Ltd.', 'ICICI Bank Ltd', 'ICICI Prudential Life Insurance Company Ltd', 'Indian Bank', 'Indraprastha Gas Ltd', 'ITC Ltd', 'JSW Steel Ltd', 'Marico Ltd', 'Petronet LNG Ltd', 'Reliance Capital Ltd', 'Reliance Infrastructure Ltd', 'State Bank Of India', 'Sun Pharma Advanced Research Company Ltd', 'Tata Global Beverages Ltd', 'Torrent Power Ltd', 'Wipro Ltd']

stock_href =['/equities/abb-limited', '/equities/acc', '/equities/mundra-port-special-eco.-zone', '/equities/adani-enterprises', '/equities/adani-power', '/equities/pantaloons-fashion-retail', '/equities/aia-engineering', '/equities/ajanta-pharma-ltd', '/equities/alkem-laboratories-ltd', '/equities/amara-raja-batteries', '/equities/ambuja-cements', '/equities/apollo-hospitals', '/equities/apollo-tyres', '/equities/arvind', '/equities/ashok-leyland', '/equities/asian-paints', '/equities/au-small-finance-bank-ltd', '/equities/aurobindo-pharma', '/equities/avenue-supermarts-ltd', '/equities/axis-bank', '/equities/bajaj-auto', '/equities/bajaj-finance', '/equities/bajaj-finserv-limited', '/equities/balkrishna-industries-ltd', '/equities/bank-of-baroda', '/equities/bank-of-india', '/equities/bata-india', '/equities/berger-paints-(i)', '/equities/bharat-electronics', '/equities/sks-microfinance', '/equities/bharat-forge', '/equities/bharat-heavy-electricals', '/equities/bharat-petroleum', '/equities/bharti-airtel', '/equities/bharti-infratel-ltd', '/equities/biocon', '/equities/bosch', '/equities/britannia-industries', '/equities/cadila-healthcare', '/equities/canara-bank', '/equities/castrol-india', '/equities/central-bank-of-india', '/equities/century-textiles---industries', '/equities/cholamandalam-inv.-and-finance', '/equities/cipla', '/equities/coal-india', '/equities/colgate-palmo?cid=18076', '/equities/container-corporation-of-india', '/equities/coromandel-international', '/equities/crisil', '/equities/crompton-greaves-consumer-electric', '/equities/cummins-inc?cid=18084', '/equities/dabur-india', '/equities/dalmia-bharat-ltd', '/equities/dewan-housing-finance', '/equities/dish-tv-india-limited', '/equities/divis-laboratories', '/equities/dlf', '/equities/dr-lal-pathlabs-ltd', '/equities/dr-reddys-laboratories', '/equities/edelweiss-financial-services', '/equities/eicher-motors', '/equities/emami', '/equities/endurance-technologies-cn-ltd', '/equities/engineers-india', '/equities/exide-industries', '/equities/the-federal-bank', '/equities/gail-(india)', '/equities/gsk-consumer-healthcare', '/equities/gsk-pharmaceuticals', '/equities/glenmark-pharmaceuticals', '/equities/gmr-infrastructure', '/equities/godrej-consumer-products', '/equities/godrej-industries', '/equities/gruh-finance-ltd', '/equities/gujarat-pipavav-port', '/equities/gujarat-state-petronet', '/equities/havells-india', '/equities/hcl-technologies', '/equities/hdfc-bank-ltd', '/equities/hero-motocorp', '/equities/hexaware-technologies', '/equities/hindalco-industries', '/equities/hindustan-petroleum', '/equities/hindustan-unilever', '/equities/hindustan-zinc', '/equities/housing-development-finance', '/equities/housing-and-urban-development', '/equities/icici-bank-ltd', '/equities/icici-prudential-life-insurance-com', '/equities/idbi-bank', '/equities/idea-cellular', '/equities/idfc-limited', '/equities/idfc-bank-ltd', '/equities/indiabulls', '/equities/indian-bank', '/equities/the-indian-hotels', '/equities/indian-oil-corporation', '/equities/indraprastha-gas', '/equities/indusind-bank', '/equities/info-edge-(india)', '/equities/infosys', '/equities/interglobe-aviation-ltd', '/equities/ipca-laboratories', '/equities/irb-infrastructure-developers', '/equities/itc', '/equities/jindal-steel---power', '/equities/jsw-energy', '/equities/jsw-steel', '/equities/jubilant-foodworks', '/equities/jubilant-life-sciences', '/equities/karur-vysya-bank', '/equities/kotak-mahindra-bank', '/equities/lt-finance-holdings-ltd', '/equities/larsen---toubro', '/equities/lic-housing-finance', '/equities/lupin', '/equities/mrf', '/equities/mahanagar-gas-ltd-ns', '/equities/mahindra---mahindra', '/equities/mahindra---mahindra-financials', '/equities/manappuram-finance-ltd', '/equities/mangalore-refinery-and-petro.', '/equities/marico', '/equities/maruti-suzuki-india', '/equities/max-india', '/equities/mindtree', '/equities/motherson-sumi-systems', '/equities/mphasis', '/equities/muthoot-finance-ltd', '/equities/natco-pharma-ltd', '/equities/national-aluminium', '/equities/national-bu', '/equities/nhpc', '/equities/nmdc', '/equities/ntpc', '/equities/oberoi-realty', '/equities/oil---natural-gas-corporation', '/equities/oil-india', '/equities/oracle-financial-software', '/equities/page-industries', '/equities/pc-jeweller-ltd', '/equities/petronet-lng', '/equities/p-i-industr', '/equities/pidilite-industries', '/equities/piramal-healthcare', '/equities/pnb-housing-finance-ltd', '/equities/power-finance-corporation', '/equities/power-grid-corp.-of-india', '/equities/prestige-estates-projects', '/equities/procter-gamble?cid=18346', '/equities/punjab-national-bank', '/equities/rajesh-exports', '/equities/rbl-bank-ltd', '/equities/reliance-capital', '/equities/reliance-communications', '/equities/reliance-industries', '/equities/reliance-infrastructure', '/equities/reliance-power', '/equities/rural-electrification', '/equities/state-bank-of-india', '/equities/shree-cements', '/equities/shriram-transport-finance', '/equities/siemens?cid=18387', '/equities/srf', '/equities/steel-authority-of-india', '/equities/sun-pharma-advanced-research', '/equities/sun-pharma-adv.-research', '/equities/sun-tv-network', '/equities/suzlon-energy', '/equities/syndicate-bank', '/equities/syngene-international-ltd', '/equities/tata-chemicals', '/equities/tata-communications', '/equities/tata-consultancy-services', '/equities/tata-global-beverages', '/equities/tata-motors-ltd', '/equities/tata-motors-dv-ltd', '/equities/tata-power-company', '/equities/tata-steel', '/equities/tech-mahindra', '/equities/madras-cements', '/equities/titan-industries', '/equities/torrent-pharmaceuticals', '/equities/torrent-power', '/equities/tv18-broadcast', '/equities/tvs-motor-company', '/equities/ultratech-cement', '/equities/union-bank-of-india', '/equities/united-breweries', '/equities/united-spirits', '/equities/united-phosphorus', '/equities/v-guard-industries-ltd', '/equities/vakrangee-softwares-ltd', '/equities/sesa-goa', '/equities/voltas', '/equities/welspun-ind', '/equities/wipro-ltd', '/equities/wockhardt', '/equities/yes-bank', '/equities/zee-entertainment-enterprises']
id_list = ['17979', '17980', '18294', '17984', '17985', '946826', '17989', '947273', '962425', '17997', '17998', '18004', '18005', '18008', '18010', '18011', '1014099', '18014', '997883', '18017', '18020', '18022', '18023', '39853', '18047', '18031', '18034', '18036', '18043', '18391', '18039', '18042', '18040', '18041', '39852', '18045', '18052', '18054', '18055', '18057', '18061', '18062', '18065', '18070', '18071', '18075', '18076', '18077', '18080', '18082', '978762', '18084', '18086', '39857', '18094', '18097', '18099', '18100', '962426', '18101', '18106', '18108', '18113', '992809', '18114', '18122', '18125', '18137', '18148', '18147', '18149', '18150', '18152', '18153', '39867', '18169', '18170', '18174', '18176', '18177', '18179', '18180', '18187', '18184', '18185', '18186', '18191', '1010531', '18198', '991131', '18199', '18200', '18219', '960765', '100254', '18209', '18210', '18197', '18213', '18215', '18216', '18217', '961701', '18222', '18223', '18224', '18241', '18244', '18226', '18247', '18246', '18256', '18260', '39882', '18268', '18269', '18270', '18291', '985843', '18273', '18271', '39888', '18292', '18276', '18277', '18279', '18283', '18288', '18290', '39890', '39891', '18299', '100271', '18307', '18309', '18297', '18312', '18311', '18313', '18316', '18325', '39896', '18334', '100258', '18337', '18339', '993203', '18341', '18342', '18344', '18346', '18350', '18353', '987147', '18361', '18362', '18367', '18364', '18366', '18371', '18376', '18383', '18386', '18387', '18397', '18399', '18405', '39910', '18406', '18413', '18415', '958336', '18417', '18419', '18420', '18422', '18425', '947268', '18426', '18428', '18429', '18272', '18433', '18435', '18436', '18441', '18442', '18445', '18447', '18449', '18451', '18450', '39926', '39923', '18377', '18462', '100273', '18467', '18468', '18470', '18471']
list_code=['ABB', 'ACC', 'ADANIPORTS', 'ADANIENT', 'ADANIPOWER', 'ABFRL', 'AIAENG', 'AJANTPHARM', 'ALKEM', 'AMARAJABAT', 'AMBUJACEM', 'APOLLOHOSP', 'APOLLOTYRE', 'ARVIND', 'ASHOKLEY', 'ASIANPAINT', 'AUBANK', 'AUROPHARMA', 'DMART', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BALKRISIND', 'BANKBARODA', 'BANKINDIA', 'BATAINDIA', 'BERGEPAINT', 'BEL', 'BHARATFIN', 'BHARATFORG', 'BHEL', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BIOCON', 'BOSCHLTD', 'BRITANNIA', 'CADILAHC', 'CANBK', 'CASTROLIND', 'CENTRALBK', 'CENTURYTEX', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'CONCOR', 'COROMANDEL', 'CRISIL', 'CROMPTON', 'CUMMINSIND', 'DABUR', 'DALMIABHA', 'DHFL', 'DISHTV', 'DIVISLAB', 'DLF', 'LALPATHLAB', 'DRREDDY', 'EDELWEISS', 'EICHERMOT', 'EMAMILTD', 'ENDURANCE', 'ENGINERSIN', 'EXIDEIND', 'FEDERALBNK', 'GAIL', 'GSKCONS', 'GLAXO', 'GLENMARK', 'GMRINFRA', 'GODREJCP', 'GODREJIND', 'GRUH', 'GPPL', 'GSPL', 'HAVELLS', 'HCLTECH', 'HDFCBANK', 'HEROMOTOCO', 'HEXAWARE', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HDFC', 'HUDCO', 'ICICIBANK', 'ICICIPRULI', 'IDBI', 'IDEA', 'IDFC', 'IDFCBANK', 'IBULHSGFIN', 'INDIANB', 'INDHOTEL', 'IOC', 'IGL', 'INDUSINDBK', 'NAUKRI', 'INFY', 'INDIGO', 'IPCALAB', 'IRB', 'ITC', 'JINDALSTEL', 'JSWENERGY', 'JSWSTEEL', 'JUBLFOOD', 'JUBILANT', 'KARURVYSYA', 'KOTAKBANK', 'L&TFH', 'LT', 'LICHSGFIN', 'LUPIN', 'MRF', 'MGL', 'M&M', 'M&MFIN', 'MANAPPURAM', 'MRPL', 'MARICO', 'MARUTI', 'MFSL', 'MINDTREE', 'MOTHERSUMI', 'MPHASIS', 'MUTHOOTFIN', 'NATCOPHARM', 'NATIONALUM', 'NBCC', 'NHPC', 'NMDC', 'NTPC', 'OBEROIRLTY', 'ONGC', 'OIL', 'OFSS', 'PAGEIND', 'PCJEWELLER', 'PETRONET', 'PIIND', 'PIDILITIND', 'PEL', 'PNBHOUSING', 'PFC', 'POWERGRID', 'PRESTIGE', 'PGHH', 'PNB', 'RAJESHEXPO', 'RBLBANK', 'RELCAPITAL', 'RCOM', 'RELIANCE', 'RELINFRA', 'RPOWER', 'RECLTD', 'SBIN', 'SHREECEM', 'SRTRANSFIN', 'SIEMENS', 'SRF', 'SAIL', 'SUNPHARMA', 'SPARC', 'SUNTV', 'SUZLON', 'SYNDIBANK', 'SYNGENE', 'TATACHEM', 'TATACOMM', 'TCS', 'TATAGLOBAL', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'RAMCOCEM', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TV18BRDCST', 'TVSMOTOR', 'ULTRACEMCO', 'UNIONBANK', 'UBL', 'MCDOWELL-N', 'UPL', 'VGUARD', 'VAKRANGEE', 'VEDL', 'VOLTAS', 'WELSPUNIND', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL']

com_list = []
print(len(id_short),len(id_list))

for i,j in zip(id_list,list_code):
    if i in id_short:
        com_list.append((i,j))

print(com_list)
id = []
code = []

for i in com_list:
    i = list(i)
    id.append(i[0])
    code.append(i[1])
print(id,code)



































'''
#for i ,name in zip (id_short ,name_short):
url = "https://in.investing.com/indices/cnx-200-components"
data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
soup = BeautifulSoup(data.text, 'lxml')
payload = {'pairID': '18294', 'period': '3600', 'viewType': 'normal'}
tech_url = requests.post(url='https://in.investing.com/instruments/Service/GetTechincalData',
                             data=payload, headers={'X-Requested-With': 'XMLHttpRequest',
                                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
tech_url = BeautifulSoup(tech_url.content, "lxml")
print(tech_url)
ten_ma = tech_url.find("td", text="MA10").find_next_sibling("td").text
print(ten_ma)
ten_ma = re.sub('\s+', '',ten_ma)
#print(ten_ma,name)
pattern = re.compile(r'(\d+\.\d+)(\w+)')
matches = pattern.finditer(ten_ma)

for match in matches:
    ten_ma, verdict = round(float(match.group(1)),2), match.group(2)
ltp = float(soup.find('td', {'class': 'pid-' + i + '-last'}).text.replace(',', ''))	

if(ltp<ten_ma):
    print(name,verdict,ten_ma,ltp)
time.sleep(5)
'''
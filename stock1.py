import requests
from bs4 import BeautifulSoup
import traceback
import re

Slist = []
stock_url = 'http://quote.eastmoney.com/stock_list.html'
stock_info = 'https://www.laohu8.com/stock/'
output_file = 'C://Users//Shinelon//Desktop//list.txt'

r = requests.get(stock_url, timeout = 30)
r.raise_for_status()
r.encoding = r.apparent_encoding

html = r.text  #Get Stock Code
soup = BeautifulSoup(html, 'html.parser')
a = soup.find_all('a')
for i in a:
    try:
        href = i.attrs['href']
        Slist.append((re.findall(r'[sh][sz]\d{6}',href))[0][2:])
    except:
        continue
Slist=Slist[1500:1600]

infoDict_name = [] #initial list
infoDict_price = []
#Smlist = Slist[:10]
for stock in Slist:
    url = stock_info + stock
    A = len(infoDict_name)
    r = requests.get(url, timeout = 30)
    #r.raise_for_status()
    r.encoding = r.apparent_encoding
    html = r.text
    
    try:
        if r.status_code == 404:
            continue
        text = []
        soup = BeautifulSoup(html,'html.parser')

        k = (soup.find('h1',attrs = {'class':'name'})) #Stock name
        for i in k:
            if u'\u4e00' <= i <= u'\u9fff':
                infoDict_name.append(i)
            else:
                break
        B = len(infoDict_name)
               
        if A==B:
            continue
        else:
            s = soup.find('span',attrs = {'class':'latest'})
            for i in s:
                infoDict_price.append(i)#Stock Price 
    except:
        traceback.print_exc()
        continue

with open(output_file,'a',encoding='utf-8') as f: #save file
    for j in range(len(infoDict_name)):
                   f.write(infoDict_name[j]+','+infoDict_price[j]+'\n')
                   
       

#for j in range(len(infoDict_name)):
   # print('{0:}:{1:}'.format(infoDict_name[j],infoDict_price[j]))
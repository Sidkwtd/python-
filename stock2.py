import requests
from bs4 import BeautifulSoup
import traceback
import re
import bs4

def getHTMLtext(url):
	try:
		r=requests.get(url,timeout = 30)
		#r.raise_for_status()
		#因有些网页存在404错误，故关闭
		r.encoding=r.apparent_encoding
		return r.text
	except:
		print("")

def getStockList(lst,stockURL):
	html=getHTMLtext(stockURL)
	soup=BeautifulSoup(html,'html.parser')
	a=soup('a')
	for i in a:
		try:
			href=i.attrs['href']
			lst.append((re.findall(r'[sh][sz]\d{6}',href))[0][2:])#因网址中只需要编号，故修改了正则表达式
		except:
			continue

def getStockInfo(lst,stockURL,fpath):
	count = 0
	for stock in lst:
		url=stockURL+stock
		#print(url)
		html=getHTMLtext(url)
		try:
			if html=="":
				continue
			infoDict={}
			soup=BeautifulSoup(html,"html.parser")
			stockInfo=soup.find('div',attrs={'class':'stock-info'})
			if isinstance(stockInfo, bs4.element.Tag):
				name=stockInfo.find_all(attrs={'class':'name'})[0]
				infoDict.update({'股票名称':name.text.split()[0]})
				keyList = stockInfo.find_all('dt')
				valueList = stockInfo.find_all('dd')
				for i in range(len(keyList)):
					if valueList[i].text != "--":#只保留值不为空的键值对
						key=keyList[i].text
						val=valueList[i].text
						infoDict[key]=val

			with open(fpath,'a',encoding='utf-8') as f:
			    f.write(str(infoDict)+'\n')
			    count+=1
			    print('\r当前进度:{:.2f}%'.format(count*100/len(lst)),end='')
			#\r覆盖，使用command命令行
		except:
			#traceback.print_exc()
			count+=1
			print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
			continue
def main():
	stock_list_url='http://quote.eastmoney.com/stock_list.html'
	stock_info_url='https://www.laohu8.com/stock/'
	output_file='C://Users//Shinelon//Desktop//stock.txt'
	slist=[]
	getStockList(slist,stock_list_url)
	slist=slist[:10]#只输出10条
	getStockInfo(slist,stock_info_url,output_file)

main()

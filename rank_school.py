import requests
from bs4 import BeautifulSoup
import bs4
import os
import xlwt
root="C://Users//Shinelon//Desktop//"
path=root+"text"

def getHtmlText(url):
	try:
		r=requests.get(url,timeout=30)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		return r.text
	except Exception as e:
		raise ""

def fillUnivList(ulist,html):
	soup=BeautifulSoup(html,"html.parser")
	for tr in soup.find('tbody').children:
		if isinstance(tr,bs4.element.Tag):
			tds=tr('td')
			ulist.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string])

def printUnivList(ulist,num):
	tplt="{0:^10}\t{1:{4}^10}\t{2:^10}\t{3:^10}"
	print(tplt.format("排名","学校","地址","成绩",chr(12288)))
	for i in range(num):
		u=ulist[i]
		print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))

def storeToXls(ulist):
	book = xlwt.Workbook()
	sheet1 = book.add_sheet('sheet1', cell_overwrite_ok = True)
	heads = ['排名', '学校', '地址','成绩']
	i = 0
	for head in heads:
	        #依次将heades列表的每一个元素写入表格中
	        sheet1.write(0, i, head)
	        i += 1
	#从第1行开始写入信息
	m = 1
	#对大列表里每一个小列表进行遍历
	for list in ulist:
	        n = 0
	        #对小列表里每个元素进行遍历
	        for info in list:
	                #将每个元素写入表格
	                sheet1.write(m, n, info)
	                n += 1
	        m += 1
	book.save('rank_school.xlsx')

def main():
	uinfo=[]
	url='http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html'
	html=getHtmlText(url)
	fillUnivList(uinfo,html)
	printUnivList(uinfo,20)
	storeToXls(uinfo)

main()

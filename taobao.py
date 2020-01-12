import requests
import re
import os
import xlwt

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Cookie':'thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; t=ae6a40b613a5dc028dd356335facc35a; _m_h5_tk=aa0bfbbe699731b83b1030e1a1823bf1_1578586357430; _m_h5_tk_enc=e6c0b90c7eeb7220458d9081ebe31343; _uab_collina=157867843973779518423171; cna=lD9QFUjoECwCAXU7VBI5NVpr; uc3=nk2=F5REOWL6izBK%2Bg%3D%3D&id2=UUphyuFAMyHwO3omPQ%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dBxdkMJw57CvyKMaM%3D; lgc=tb17777641; uc4=id4=0%40U2grEadIaZjNGxl12kSrCrBbFdNravoV&nk4=0%40FY4Paw7UZ9l32eeb56jpPZELqS%2Bu; tracknick=tb17777641; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=-1_1; enc=mW8nKIjibaJtbJRiQnq5%2FNXD%2Fx%2FXOSs%2FrRTI43F8iKm91aoW5LXWOvdXsKtzjR21BYNYU6H0BuIBuR8IFifVUA%3D%3D; uc1=cookie14=UoTbldVRVvGMaw%3D%3D; v=0; cookie2=1b6543e99b284c44e5d261aa92be926c; _tb_token_=f63ee68b3356; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; x5sec=7b227365617263686170703b32223a2233393163393264623265343530636335646430666438363062626239386539654349726b35664146454b3235786f335a78724f4952686f504d6a49774d4467774d7a4d794d6a6b304d7a7378227d; JSESSIONID=FCA5478CDF4537299ED84F7EC3AA6B5E; l=dBahggt4QNgzgi0CBOCZlurza77TcIRf_uPzaNbMi_5BP6Ys_h_OoAZGpFv6cjWAM9Yp43ral1ytUFS4JsuKHdGJ4AadZzD2B; isg=BLOzZMr76UODvaWW6R9NUEj6Qrddc0eqmvDVt2VQaFIJZNIG7bs--lW2GtQvQ5-i'
} #替换成自己的cookie

def getHtmlText(url):
	try:
		r=requests.get(url,timeout=30,headers=headers)
		r.raise_for_status()
		r.encoding=r.apparent_encoding
		return r.text
	except:
		return "错误"

def parsePage(ilt,html):
	try:
		plt=re.findall(r'"view_price":"[\d.]*"',html)
		tlt=re.findall(r'"raw_title":".*?"',html)
		for i in range(len(plt)):
			price=eval(plt[i].split(':')[1])
			title=eval(tlt[i].split(':')[1])
			ilt.append([price,title])
	except:
		print("error")

def printGoodsList(ilt):
	tplt="{:4}\t{:8}\t{:16}"
	print(tplt.format("序号","价格","商品名称"))
	count=0
	for g in ilt:
		count=count+1
		print(tplt.format(count,g[0],g[1]))

def storeToXls(ulist):
	book = xlwt.Workbook()
	sheet1 = book.add_sheet('sheet1', cell_overwrite_ok = True)
	heads = ['序号', '价格', '商品名称']
	i = 0
	for head in heads:
	        #依次将heades列表的每一个元素写入表格中
	        sheet1.write(0, i, head)
	        i += 1
	#从第1行开始写入信息
	m = 1
	#对大列表里每一个小列表进行遍历
	for list in ulist:
	        sheet1.write(m,0,m)
	        n=1
	        #对小列表里每个元素进行遍历
	        for info in list:
	                #将每个元素写入表格
	                sheet1.write(m, n, info)
	                n += 1
	        m += 1
	book.save('bags.xls')

def main():
	goods='书包'
	depth=2
	start_url='https://s.taobao.com/search?q='+goods
	infoList=[]
	for i in range(depth):
		try:
			url=start_url+'&s='+str(44*i)
			html=getHtmlText(url)
			parsePage(infoList,html)
		except:
			continue
	storeToXls(infoList)

main()
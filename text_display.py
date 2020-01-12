import requests
path='C://Users//Shinelon//Desktop//test'
url='http://quote.eastmoney.com/stock_list.html'
r = requests.get(url)
r.encoding='gbk'#网页解码
with open(path, 'wt', encoding='utf-8') as f:
    f.write(r.text)

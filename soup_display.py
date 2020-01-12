import requests
from bs4 import BeautifulSoup
root="C://Users//Shinelon//Desktop//"
path=root+"soup"

url ='https://www.laohu8.com/stock/150028'
r = requests.get(url)
html = r.text
soup=BeautifulSoup(html,"html.parser")
text=soup.prettify()

with open(path,'wb') as f:
    f.write(text.encode('utf-8'))
    f.close()
    print("文件保存成功")
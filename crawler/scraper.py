import requests 
from bs4 import BeautifulSoup
import re
import json

url = 'https://actionpress.news/home.html'

def getURlsFromMenu(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    menu = [
    {'class' : re.compile('.*submenu.*')},
    ]
    for p in menu:
        newM = soup.find_all(**p)
    
    menuURLS = ['home.html']
    for i in newM:
        for child in i.find_all('a'):
            menuURLS.append(child.get('href'))

    return menuURLS


def subPagesData(url):
    updatedURL = f'https://actionpress.news/{url}'
    res = requests.get(updatedURL)
    soup = BeautifulSoup(res.content,'html.parser')
    news = [x for x in soup.find_all('h2',itemprop="name")]
    urls = []
    for h2 in news:
        if h2.find('a'):
            urls.append(h2.find('a').get('href'))
    return (list(set(urls)))


if __name__=='__main__':
    res1 = getURlsFromMenu(url)
    result=[]
    for i in res1:
        urlsFromPages = subPagesData(i)
        for j in urlsFromPages:
            result.append(j)
    json_obj= json.dumps(result, indent=4)
    with open('urls.json', 'w') as file:
        file.write(json_obj)

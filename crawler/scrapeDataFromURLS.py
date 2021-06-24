import json
import requests 
from bs4 import BeautifulSoup
import re
import json
import csv

result = []

with open('urls.json',) as file:
    content = json.load(file)
    uniqueURLS = list(set(content))

json_obj= json.dumps(uniqueURLS, indent=4)
with open('uniqueURLS.json', 'w') as file:
    file.write(json_obj)

def getDataFromUniqueURLS():
    with open('uniqueURLS.json',) as file:
        content = json.load(file)
        return content

def scrapeDataFromSubPages(url,urlWithoutDomain):
    data = [urlWithoutDomain]
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    title = soup.find('h1',itemprop="name").text
    data.append(title)
    figure = soup.find_all('figure',class_="image_container")
    for i in figure:
        if i.find('p',class_="caption"):
            imageSrc= i.find('img', itemprop="image").get('src')
            data.append(imageSrc)
    if len(data) == 2:
        data.append('Not Found, OR Cannot be extracted using crawler')

    subTitle = soup.find_all('div',class_="col-xl-4")
    for i in subTitle:
        if i.find('strong'):
                data.append(i.find('strong').text)
    if len(data) == 5:
        del data[3]


    result.append(data)



if __name__=='__main__':
    data = getDataFromUniqueURLS()
    for i in data:
        scrapeDataFromSubPages('https://actionpress.news/'+i,i)
    # scrapeDataFromSubPages('https://actionpress.news/'+data[0],data[0])
    print(result)
    fields = ['URL','Title', 'Image-source', 'Sub-title']
    with open('data.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(result)

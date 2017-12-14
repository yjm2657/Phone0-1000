# -*- coding:utf-8 -*-
# coding=utf-8
from bs4 import BeautifulSoup
import requests
import random
import sys
sys.path.append("/usr/local/var/pyenv/versions/3.6.1/bin/python")
import matplotlib.pyplot as plt
# import sys
# from elasticsearch import Elasticsearch
# print sys.getdefaultencoding();


#uer_agent库，随机选取，防止被禁
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def getResponse(url):
    headers = {'user-agent':random.choice(USER_AGENT_LIST)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # soup = BeautifulSoup(response.content, 'lxml')
    soup = BeautifulSoup(response.content)
    return soup

def getPhoneUrl(page):
    url = 'http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_0-1000_0_1_2_0_%s.html'%str(page)
    soup = getResponse(url)
    phone_div = soup.find('ul', attrs={'class':'clearfix'})
    phones = phone_div.find_all('li')
    urls = []
    for phone in phones:
        phone_a = phone.find('a')
        urls += [phone_a['href']]
    print('getinfo=%s' % page, urls)
    return urls

def getPhoneInfo(phoneUrl):
    soup = getResponse(phoneUrl)

    phone_name = soup.find('h1', attrs={'class':'product-model__name'}).text
    print (phone_name)
    phone_price_jd_dd = soup.find('dd', attrs={'id':'_j_local_price'})
    phone_price = phone_price_jd_dd.find('a').text.replace('¥','')


    phone_div = soup.find('div', attrs={'class':'section-content'})
    phone_lis = phone_div.find_all('li')

    phone_info = ''
    for phone_li in phone_lis:
        phone_info = phone_info + phone_li.p.text

    phone_model = {}
    phone_model['name'] = phone_name
    phone_model['price'] = phone_price
    phone_model['info'] = phone_info
    print (phone_model)
    return phone_model

def showWithDataArr(dataArr):
    price_0_200 = []
    price_200_400 = []
    price_400_600 = []
    price_600_800 = []
    price_800_1000 = []
    price_1000_max = []
    for phone_model in dataArr:
        price = int(phone_model['price'])
        if price>0 and price<200:
            price_0_200.append(phone_model)
        elif price>=200 and price<400:
            price_200_400.append(phone_model)
        elif price>=400 and price<600:
            price_400_600.append(phone_model)
        elif price>=600 and price<800:
            price_600_800.append(phone_model)
        elif price>=800 and price<1000:
            price_800_1000.append(phone_model)
        else:
            price_1000_max.append(phone_model)

    priceArr = ['0~200', '200~400', '400~600', '600~800', '800~1000', '1000~max']
    price_exArr = [0.05, 0, 0, 0, 0, 0]
    priceNumArr = [len(price_0_200), len(price_200_400), len(price_400_600), len(price_600_800), len(price_800_1000), len(price_1000_max)]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'red', 'green', 'purple']
    patchs, l_texts, p_texts = plt.pie(priceNumArr, explode=price_exArr, labels=priceArr, labeldistance=1.1, autopct='%2.1f%%',shadow=False, startangle=0,pctdistance=0.6)
    plt.legend()  # 图例
    plt.show()








if __name__ == '__main__':
    all_urls = []
    for page in range(1,5):
        urls = getPhoneUrl(page)
        all_urls = all_urls + urls
    print ('获取到的链接:',len(all_urls))

    out = ''
    dataArr = []
    for url in all_urls:
        try:
            #http: // detail.zol.com.cn / cell_phone / index1154014.shtml
            newUrl = 'http://detail.zol.com.cn'+url
            info = getPhoneInfo(newUrl)
        except Exception as e:
            print (e)
            continue
        dataArr = dataArr + [info]
    showWithDataArr(dataArr)
        # out = out+str(info)+'\n'
    # 写入text文件
    # with open('phone0~1000.text', 'w') as f:
    #     f.write(out)

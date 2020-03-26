#!/usr/bin/env python
# coding: utf-8

# In[24]:


import requests
import lxml
import re
import json
import time
from bs4 import BeautifulSoup


# In[2]:


def soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8' #根据网页编码选择 gb2312, gbk, utf-8 
#     r.encoding = 'gbk' #根据网页编码选择 gb2312, gbk, utf-8 
#     r.encoding = 'gb2312' #根据网页编码选择 gb2312, gbk, utf-8 
#     r.encoding = 'gbk' #根据网页编码选择 gb2312, gbk, utf-8 
    #r.status_code
    soup = BeautifulSoup(r.text, "lxml")
    return soup


# In[3]:


def soupb(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r = requests.get(url,headers=headers)
    return r.content


# In[4]:


def getIds(url):    
    a_s = soup(url).select('.sound-list ul li a')
#     print(a_s)
    for a in a_s[:30]:
#         print(a)
#         num+=1
        track_id = a['href'].split('/')[-1]
        title = a['title']
        print(track_id,title)
        downMedia(track_id, title)
    return
# url ='https://www.ximalaya.com/yinyue/24822529/'
# getIds(url)


# In[19]:


def downMedia(track_id, title):
    url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(track_id)
#     print(url)
    src = json.loads(soup(url).text)
    print(src['data']['src'])
    url =  src['data']['src']
    with open(title+'.m4a', 'wb') as f:
        f.write(soupb(url))
    return   
# track_id = '195046649'  
# title = 'yueguang'
# downMedia(track_id, title)


# In[32]:


def Main():
    url = input('请输入喜马拉雅专辑的网址：')
    alum = soup(url).select('h1')[0].text
    page = int(soup(url).select('.page-link')[-2].text)
    total = re.search('\d+',soup(url).select('h2')[0].text).group(0)
    print('找到专辑<{}>,  共{}页， 共{}个音频，开始下载。。。'.format(alum, page, total))
#     global num
#     num = 0
    for page in range(1,page):
        url = 'https://www.ximalaya.com/xiangsheng/27909622/p{}/'.format(page)
        getIds(url)  


# In[33]:


if __name__ == '__main__':    
    t1 = time.time()
    Main()
    t2 = time.time()
    print('程序耗时：',t2-t1)


# In[31]:


url = 'https://www.ximalaya.com/xiangsheng/27909622/'
# # print(soup(url).select('h2')[0].text)
# # a=soup(url).select('h2')[0].text
re.search('\d+',soup(url).select('h2')[0].text).group(0)


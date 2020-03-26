#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import lxml
import re
import time
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


def getInput(job):

#     if det is None
#         print('请重新输入')
#         goto .begin
    result = []
    url = 'http://www.chenhr.com/so/29-kj'+job+ '-sm1-p1.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r = requests.get(url,headers=headers)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, "lxml")
   
    num = re.search('\d+',soup.select('strong')[1].text).group(0)
    list_page = int(soup.em.text.split('/')[1])
    
    print('找到{}个结果'.format(num))
    print('-------------------------------')
    result = {
        'totalnum': num,
        'list_page': list_page
    }
    return result


# In[3]:


def getUrls(url):
#     url = 'http://www.chenhr.com/so/29-kj动力-sm1-p1.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r = requests.get(url,headers=headers)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, "lxml")
    
    urls = []
    
    for i in range(0,len(soup.select('.td_sp1 a'))):
#         print(i)
        url = soup.select('.td_sp1 a')[i]['href']
#         print(url)
        url = 'http://www.chenhr.com'+str(url)
#         print(url)
        urls.append(url)        
    
    return urls
# print(getUrls(url))
    


# In[4]:


def getMaininfo(url):#抓取一条新闻的详情 返回一个列表
    result=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r = requests.get(url,headers=headers)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, "lxml")
       
    try:
        job_name = soup.select('h1')[0].text
        company_name = soup.select('h3 a')[0].text
        company_info_qyxz = soup.select('.company_info li')[0].text.split('：')[1]
        company_info_gsgm = soup.select('.company_info li')[1].text.split('：')[1]
        company_info_gzdd = soup.select('.company_info li')[2].text.split('：')[1]
        job_info_gzxz = soup.select('.job_info li')[0].text.split('：')[1]
        job_info_xlyq = soup.select('.job_info li')[1].text.split('：')[1]
        job_info_jingyan = soup.select('.job_info li')[2].text.split('：')[1]
        job_info_mager = soup.select('.job_info li')[3].text.split('：')[1]
        job_info_english = soup.select('.job_info li')[4].text.split('：')[1]
        salery1 = soup.select('.job_info li')[5].text.split('：')[1].strip('\n ')
        if re.search('面议',salery1):
            job_info_salery = '面议'
            print(job_info_salery)
        else:
            salery_low = int(re.search('(\d+)～',salery1).group(1))
            salery_high = int(re.search('～(\d+)',salery1).group(1))
    #         rate = 0.3
            job_info_salery = salery_low+(salery_high-salery_low)*rate
            print(job_info_salery)
     
        job_info_zhicheng = soup.select('.job_info li')[6].text.split('：')[1]
        job_info_num = soup.select('.job_info li')[7].text.split('：')[1]
        job_info_date = soup.select('.job_info li')[8].text.split('：')[1]
        job_info_detail = soup.select('.zxd_jobinfo')[0].text
    except:
        print(url+'页面非常规')
    result = [job_name, company_name, company_info_qyxz, company_info_gsgm, company_info_gzdd,job_info_gzxz,  
              job_info_xlyq, job_info_jingyan, job_info_mager, job_info_english, job_info_salery, job_info_zhicheng,  
              job_info_num, job_info_date, job_info_detail ]        
    
    return result


# In[5]:


# if __name__ == '__main__':
#     det = input('输入职位关键字（例如热工）：')
#     if det is None
#         print('请重新输入')
#         goto .begin

job = input('请输入关键词：')   
t0 = time.time()
rate = 0.3
file_name = 'chenhr'+job+'.xlsx'
job_name = []
company_name = []
company_info_qyxz = []
company_info_gsgm = []
company_info_gzdd = []
job_info_gzxz = []
job_info_xlyq = []
job_info_jingyan = []
job_info_mager = []
job_info_english = []
salery1 = []
job_info_salery = []
job_info_zhicheng = []
job_info_num = []
job_info_date = []
job_info_detail = []

info = getInput(job)
print(info)
k=0

for i in range(0,info['list_page']):
    url = 'http://www.chenhr.com/so/29-kj'+job+ '-sm1-p{}.html'.format(i+1)
    print(url)
    links = getUrls(url)
    for link in links:
        k+=1
        print(k, link)
        info = getMaininfo(link)
        job_name.append(info[0])
        company_name.append(info[1])
        company_info_qyxz.append(info[2])
        company_info_gsgm.append(info[3])
        company_info_gzdd.append(info[4])
        job_info_gzxz.append(info[5])
        job_info_xlyq.append(info[6])
        job_info_jingyan.append(info[7])
        job_info_mager.append(info[8])
        job_info_english.append(info[9])
        job_info_salery.append(info[10])
        job_info_zhicheng.append(info[11])
        job_info_num.append(info[12])
        job_info_date.append(info[13])
        job_info_detail.append(info[14])    

        
result = {
    '需求岗位': job_name,
    '公司名称': company_name,
    '企业性质': company_info_qyxz,
    '公司规模': company_info_gsgm,
    '工作地点': company_info_gzdd,
    '工作性质': job_info_gzxz,
    '学历要求': job_info_xlyq,
    '经验要求': job_info_jingyan,
    '专业要求': job_info_mager,
    '外语要求': job_info_english,
    '薪资水平': job_info_salery,
    '职称要求': job_info_zhicheng,
    '岗位人数': job_info_num,
    '发布日期': job_info_date,
    '具体要求': job_info_detail
 }


# In[6]:


df=pd.DataFrame(result)
df.head()


# In[7]:


df.to_excel(file_name)


# In[8]:


t1 = time.time()
print('程序运行时间为%f'%(t1-t0))


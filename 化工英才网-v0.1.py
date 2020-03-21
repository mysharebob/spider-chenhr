#!/usr/bin/env python
# coding: utf-8

# In[107]:


import requests
import lxml
import re
# import json
from bs4 import BeautifulSoup
import pandas  as pd
# from pandas import DataFrame


# # 关键词生成URL

# In[111]:


det = input('搜索目标：')
url = 'http://www.chenhr.com/so/29-kj'+det+ '-sm1-p1.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
r = requests.get(url,headers=headers)
r.encoding = 'gb2312'
soup = BeautifulSoup(r.text, "lxml")

list_page = int(soup.em.text.split('/')[1])
list_page


# In[112]:





# # 生成list页

# In[113]:


num = 0
for i in range(0,list_page):
    list_url = 'http://www.chenhr.com/so/29-kj{}-sm1-p{}.html'.format(det,i+1)
    print(list_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    r_list = requests.get(list_url,headers=headers)
    r_list.encoding = 'gb2312'
    soup_list = BeautifulSoup(r_list.text, "lxml")

    for j in range(len(soup_list.select('.td_sp1 a'))):
        job_url = soup_list.select('.td_sp1 a')[j]['href']
        job_url = 'http://www.chenhr.com'+job_url
        print(job_url)

        r_job = requests.get(job_url,headers=headers)
        r_list.encoding = 'gb2312'
        soup_job = BeautifulSoup(r_job.text, "lxml")

        job_name = soup_job.select('h1')[0].text
        company_name = soup_job.select('h3 a')[0].text
        company_info_qyxz = soup_job.select('.company_info li')[0].text.split('：')[1]
        company_info_gsgm = soup_job.select('.company_info li')[1].text.split('：')[1]
        company_info_gzdd = soup_job.select('.company_info li')[2].text.split('：')[1]
        job_info_gzxz = soup_job.select('.job_info li')[0].text.split('：')[1]
        job_info_xlyq = soup_job.select('.job_info li')[1].text.split('：')[1]
        job_info_jingyan = soup_job.select('.job_info li')[2].text.split('：')[1]
        job_info_mager = soup_job.select('.job_info li')[3].text.split('：')[1]
        job_info_english = soup_job.select('.job_info li')[4].text.split('：')[1]
        job_info_salery = soup_job.select('.job_info li')[5].text.split('：')[1].strip('\n ')
        job_info_zhicheng = soup_job.select('.job_info li')[6].text.split('：')[1]
        job_info_num = soup_job.select('.job_info li')[7].text.split('：')[1]
        job_info_date = soup_job.select('.job_info li')[8].text.split('：')[1]
        job_info_detail = soup_job.select('.zxd_jobinfo')[0].text
        data = [job_name, company_name, company_info_qyxz, company_info_gsgm, company_info_gzdd, job_info_gzxz, job_info_xlyq, job_info_jingyan,  job_info_mager, job_info_english, job_info_salery, job_info_zhicheng,job_info_num, job_info_date,job_info_detail]
        print(data)
        num+=1
        with open('D:\python\jiaoben\job_'+det+'.txt','a+') as f:
            f.write(str(data)+'\n\n')
            f.close()
        print('已获取第'+ str(num) + '条数据。')
        
print('finished')


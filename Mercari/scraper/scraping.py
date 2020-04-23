#!/usr/bin/env python
# coding: utf-8

# In[73]:


import sys
import os
from selenium import webdriver
import pandas
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request


# In[74]:


headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }


# In[75]:


# imgフォルダの作成
os.makedirs("img")
# 取得した画像をループして保存


# In[76]:


df = pd.DataFrame(columns=['title','price','sold','url'])


# In[77]:


browser = webdriver.Chrome('/Users/kanka/Desktop/Selenium/chromedriver')


# In[78]:


#query = "オルチャン"


# In[79]:


#browser.get("https://www.mercari.com/jp/search/?sort_order=price_desc&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=".format(query))
browser.get("https://www.mercari.com/jp/search/?sort_order=&keyword=オルチャン&category_root=1&category_child=12&brand_name=&brand_id=&size_group=&price_min=&price_max=&status_trading_sold_out=1")


# In[80]:


page = 1
n = 0


# In[81]:


while True: #continue until getting the last page

    #5-1

    if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        #5-1-2

        posts = browser.find_elements_by_css_selector(".items-box")

        #5-1-3

        for post in posts:
            title = post.find_element_by_css_selector("h3.items-box-name").text

            #5-1-3-1

            price = post.find_element_by_css_selector(".items-box-price").text
            price = price.replace('¥', '')

            #5-1-3-2

            sold = 0
            if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
                sold = 1

            url = post.find_element_by_css_selector("a").get_attribute("href")
            se = pandas.Series([title, price, sold,url],['title','price','sold','url'])
            df = df.append(se, ignore_index=True)

        #5-1-4
#------------------------------------------------------------------#
        current_url = browser.current_url
        html = requests.get(current_url, headers = headers)
        bs = BeautifulSoup(html.text, "lxml")
        images = bs.find_all("img", class_="lazyload")
        
        for i,img in enumerate(images, start=1):
          src  = img.get("data-src")
          responce = requests.get(src)
          with open("img/" + "{}.jpg".format(n), "wb") as f:
            f.write(responce.content)
          n += 1
#------------------------------------------------------------------#        

        page+=1

        btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        print("Moving to next page......")

    #5-2

    else:
        print("no pager exist anymore")
        break


# In[82]:


df.to_csv("オルチャン_トップス.csv")


# In[83]:


df


# In[ ]:





# In[ ]:





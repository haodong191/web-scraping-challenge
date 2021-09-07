from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#NASA Mars News


# In[4]:


browser.visit('https://redplanetscience.com/')
time.sleep(5)


# In[5]:


news_html = browser.html
soup = BeautifulSoup(news_html, 'html.parser')


# In[6]:


results = soup.find_all('div', class_='list_text')


# In[7]:


for result in results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        
        print('-----------------')
        print(news_title)
        print(news_p)


# In[8]:


#JPL Mars Space Images below


# In[9]:


browser.visit('https://spaceimages-mars.com/')


# In[10]:


baseurl = 'https://spaceimages-mars.com/'


# In[11]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[12]:


image_html = browser.html
image_soup = BeautifulSoup(image_html, 'html.parser')


# In[13]:


image_results = image_soup.find('img', class_='fancybox-image')['src']


# In[14]:


featured_image_url = baseurl + image_results
featured_image_url 


# In[15]:


#Mars Facts


# In[16]:


browser.visit('https://galaxyfacts-mars.com')


# In[17]:


facts=pd.read_html('https://galaxyfacts-mars.com')
facts


# In[18]:


mars_facts= facts[1]
mars_facts


# In[19]:


mars_fact_table = mars_facts.to_html()


# In[20]:


print(mars_fact_table)


# In[21]:


#Mars Hemispheres


# In[22]:


url = 'https://marshemispheres.com/'
browser.visit(url)


# In[23]:


hemispheres_html = browser.html
soup = BeautifulSoup(hemispheres_html, 'html.parser')
hemisphere_image_urls = []


# In[24]:


hemispheres = soup.find_all('div', class_='item')


# In[25]:


for hemisphere in hemispheres:
    hemisphere_header = hemisphere.h3.text.strip()
    hemisphere_url = hemisphere.a['href']
    browser.visit(url + hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
    hemisphere_finder = hemisphere_soup.find('div', id='wide-image')
    hemisphere_finder2 = hemisphere_finder.find('a', target='_blank')['href']
    hemisphere_image_url = url +  hemisphere_finder2
    hemisphere_image_urls.append({"title":hemisphere_header, "img_url":hemisphere_image_url})
    browser.links.find_by_partial_text('Back').click()
    time.sleep(1)
        
hemisphere_image_urls


# In[26]:


mars_html = {
"news_title":news_title,
"news_p": news_p,
"featured_img_url": featured_image_url,
"facts":mars_fact_table,
"hemispheres":hemisphere_image_urls
}


# In[27]:


mars_html

browser.quit()


#Import to Mongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

facts = db.facts

db.facts.drop()

post = mars_html

facts.insert_one(post)

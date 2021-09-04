
## CONVERTED USING jupyter nbconvert --to script
#!/usr/bin/env python
# coding: utf-8

# In[5]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[6]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[7]:


#NASA Mars News blow


# In[9]:


#wait 5-10 seconds after running this cell for the page itself to load. The html will not parse all code if the next cell is clicked to quickly.
browser.visit('https://redplanetscience.com/')
time.sleep(5)


# In[10]:


news_html = browser.html
soup = BeautifulSoup(news_html, 'html.parser')


# In[11]:


results = soup.find_all('div', class_='list_text')


# In[12]:


for result in results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        
        print('-----------------')
        print(news_title)
        print(news_p)


# In[13]:


#JPL Mars Space Images below


# In[14]:


browser.visit('https://spaceimages-mars.com/')


# In[15]:


baseurl = 'https://spaceimages-mars.com/'


# In[16]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[17]:


image_html = browser.html
image_soup = BeautifulSoup(image_html, 'html.parser')


# In[18]:


image_results = image_soup.find('img', class_='fancybox-image')['src']


# In[38]:


featured_image_url = baseurl + image_results
featured_image_url 


# In[20]:


#Mars Facts


# In[21]:


browser.visit('https://galaxyfacts-mars.com')


# In[25]:


facts=pd.read_html('https://galaxyfacts-mars.com')
facts


# In[29]:


mars_facts= facts[1]
mars_facts


# In[30]:


mars_fact_table = mars_facts.to_html()


# In[31]:


print(mars_fact_table)


# In[ ]:


#Mars Hemispheres


# In[33]:


url = 'https://marshemispheres.com/'
browser.visit(url)


# In[34]:


hemispheres_html = browser.html
soup = BeautifulSoup(hemispheres_html, 'html.parser')
hemisphere_image_urls = []


# In[35]:


hemispheres = soup.find_all('div', class_='item')


# In[36]:


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


# In[ ]:





# In[ ]:





# In[ ]:





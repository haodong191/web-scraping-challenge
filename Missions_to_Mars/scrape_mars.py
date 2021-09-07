from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    #NASA Mars News
    browser.visit('https://redplanetscience.com/')
    time.sleep(5)

    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')
    results = soup.find_all('div', class_='list_text')

    for result in results:
            news_title = result.find('div', class_='content_title').text
            news_p = result.find('div', class_='article_teaser_body').text
            
            print('-----------------')
            print(news_title)
            print(news_p)


    #JPL Mars Space Images below
    browser.visit('https://spaceimages-mars.com/')
    baseurl = 'https://spaceimages-mars.com/'
    browser.links.find_by_partial_text('FULL IMAGE').click()
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    image_results = image_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = baseurl + image_results
    featured_image_url 

    #Mars Facts
    browser.visit('https://galaxyfacts-mars.com')
    facts=pd.read_html('https://galaxyfacts-mars.com')
    facts
    mars_facts= facts[1]
    mars_facts
    mars_fact_table = mars_facts.to_html()
    print(mars_fact_table)

    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')
    hemisphere_image_urls = []
    hemispheres = soup.find_all('div', class_='item')

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

    mars_html = {
    "news_title":news_title,
    "news_p": news_p,
    "featured_img_url": featured_image_url,
    "facts":mars_fact_table,
    "hemispheres":hemisphere_image_urls
    }

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

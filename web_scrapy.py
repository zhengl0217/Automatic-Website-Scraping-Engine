#!/usr/bin/env python 
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
import os

path = os.getcwd()
if os.path.exists(path + '/data.csv'):
    os.system('rm -r data.csv')

driver = webdriver.Chrome('/Applications/chromedriver')
driver.implicitly_wait(20)

class WebSpider(scrapy.Spider):
    start_urls = ['https://doaj.org/search?ref=homepage-box&source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22Oxygen%20reduction%20reaction%22%2C%22default_operator%22%3A%22AND%22%7D%7D%2C%22from%22%3A0%7D']
    def __init__(self):
        self.infile = open("data.csv","a",newline="")
        writer = csv.writer(self.infile)
        writer.writerow(['title', 'journal', 'date', 'abstract'])

    def parse(self, response):  
        url_page = 'https://doaj.org/search?ref=homepage-box&source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22Oxygen%20reduction%20reaction%22%2C%22default_operator%22%3A%22AND%22%7D%7D%2C%22from%22%3A'+'#'+'%7D'
        url_l = ['//*[@id="results"]/div/div/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span/a',
                 '//*[@id="results"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/span/a']

        page = 105

        if page == 0:
            url_page_ = url_page.replace('#', str(page))
        else:
            url_page_ = url_page.replace('#', str(page)+'0')

        driver.get(url_page_)
        for xpath_link in url_l:
            url = driver.find_element_by_xpath(xpath_link).get_attribute('href')
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for info in response.css('div.col-md-12'):
            title = info.css('h1::text').extract()[0]
            journal = info.css('a::text').extract()[0]                                                         
            date = info.css('p::text').extract()[1].split("\n")[0].split(" ")[1].split(";")[0]                 

        abstract = response.css('div.col-md-10').css('p::text').extract()[-1].replace('\n', '')
        
        yield {
            'title': title,
            'journal': journal,                                                                            
            'date': date,                                                                                  
            'abstract': abstract,                                                                          
            }

        writer = csv.writer(self.infile)
        writer.writerow([title ,journal, date, abstract])

process = CrawlerProcess()
process.crawl(WebSpider)
process.start()


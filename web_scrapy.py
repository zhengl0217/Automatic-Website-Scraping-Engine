"""
This module defines a wrapper function to automatically extract the information that are contained in HTML files.
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
import csv

__author__ = "Zheng Li"
__email__ = "zhengl@vt.edu"
__date__ = "Nov. 13, 2019"

# install the chrome website driver and put it under the Applications fold at your local PC
driver = webdriver.Chrome('/Applications/chromedriver')
# define waiting period to ensure a complete scrapying percedure
driver.implicitly_wait(20)

class WebSpider(scrapy.Spider):
    """
    A class to detect and enter all the journal links in a repository page and extract the corresponding information.
    """
    # the link of starting page of Directory of Open Access Journals (DOAJ)
    start_urls = ['https://doaj.org/search?ref=homepage-box&source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22Oxygen%20reduction%20reaction%22%2C%22default_operator%22%3A%22AND%22%7D%7D%2C%22from%22%3A0%7D']
    # define csv file for module output
    def __init__(self):
        self.infile = open("data.csv","a",newline="")
        writer = csv.writer(self.infile)
        writer.writerow(['title', 'journal', 'date', 'abstract'])

    def parse(self, response):  
        """
        Identify the all the links on a website page by providing XPaths. Note that the XPaths can bed found by inspectig the google chrome.
        """
        # define page variable
        url_page = 'https://doaj.org/search?ref=homepage-box&source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22Oxygen%20reduction%20reaction%22%2C%22default_operator%22%3A%22AND%22%7D%7D%2C%22from%22%3A'+'#'+'%7D'
        # XPaths list for all the journal links in a page. As there is no general rules for thest paths, I copy all the XPaths here.
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
        # the desired page number 
        page = 0
        # update the page urls
        if page == 0:
            url_page_ = url_page.replace('#', str(page))
        else:
            url_page_ = url_page.replace('#', str(page)+'0')
        # execute the web spider to visit all the journal links and extract information at the "secondary level" via request action
        driver.get(url_page_)
        for xpath_link in url_l:
            url = driver.find_element_by_xpath(xpath_link).get_attribute('href')
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        """
        Locate the information in the HTML structrue and grape them.
        """
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
        # save the extracted information in csv file
        writer = csv.writer(self.infile)
        writer.writerow([title ,journal, date, abstract])

process = CrawlerProcess()
process.crawl(WebSpider)
process.start()


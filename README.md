# Python wrapper function for processing and extracting the literature texts from open source reporsitory

This repository contains a python file, named as **web_scrapy**, for extracting the key journal information 
(e.g., journal title, publication sources, publication date and abstract) that are related to "oxygen evolution reaction" 
from [Directory of Open Access Journals (DOAJ)](https://doaj.org/) in an automatic fashion. The script that I designed integrates 
two important components:(1) an open-source web scraping framework [Scrapy](https://docs.scrapy.org/en/latest/) and 
(2)[ChromeDriver](https://chromedriver.chromium.org/). Note that the latest version of ChromeDriver has a limitation on 
the processing page number. In addition, the website administrator may change the HTML files and the corresponding architecture 
every few months. Therefore, you may have to update the 'XPath'to the appropriate container accordingly. This code only provides 
a template for your research and study. 


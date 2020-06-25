from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from numpy.random import randint
from random import sample
import time


class userAgent:

    terms = ['python',   'selenium', 'browser', 'gns3', 
             'networks', 'suricata', 'pfsense', 'virtual',
             'topology', 'request' , 'ssh']
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)
        
    def store_page(self):
        self.source = self.browser.page_source
            
    def google_query(self, query):
        self.browser.get('https://www.google.com')
        elem = self.browser.find_element_by_name('q')
        elem.send_keys(query + Keys.RETURN)
        self.store_page()
        print(self.source[:300])
#         time.sleep(10)
    
    def get_page(self, url):
        self.browser.get(url)
        self.store_page()
        print(self.source[:300])

    def close_browser(self):
        self.browser.quit()
        
    def random_query(self):
        query = " ".join(sample(self.terms, k=randint(3) + 1))
        print(query)
        self.google_query(query)
#         print(self.get_urls_in_page())
    
    def get_urls_in_page(self):
#         links = self.browser.find_elements_by_xpath("//a[@href]")bea
        html = BeautifulSoup(self.source,features="html5lib")
        divs = html.findAll('div',attrs={'class':'r'})
        print(divs)
        links = [d.findAll('a') for d in divs]
#         links = list([link.get('href') for link in html.findAll('a')])
        return links

# ua.close_browser()
ua = userAgent()
ua.random_query()
ua.get_urls_in_page()

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from numpy.random import randint
from random import sample
import time


class userAgent:

    terms = [
        "python",
        "selenium",
        "browser",
        "gns3",
        "networks",
        "suricata",
        "pfsense",
        "virtual",
        "topology",
        "request",
        "ssh",
    ]

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)

    def store_page(self):
        self.source = self.browser.page_source

    def google_query(self, query):
        results_url = f"https://duckduckgo.com/html?q={query}&t=h_&ia=web"
        self.browser.get(results_url)

    def get_page(self, url):
        self.browser.get(url)
        self.store_page()
        print(self.source[:300])

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def random_query(self):
        query = "+".join(sample(self.terms, k=randint(3) + 1))
        print(query)
        self.google_query(query)

    def get_urls_in_page(self):
        self.results = self.browser.find_elements_by_xpath(
            "//div[@id='links']/div/div/div[1]"
        )
        print([self.results[i].text for i in range(len(self.results))])

    def random_click(self):
        self.results[randint(len(self.results))].click()
        print(self.browser.page_source)

ua = userAgent()
ua.random_query()
ua.get_urls_in_page()
ua.random_click()
ua.close_browser()

#If .queries does not exist, create it and write '0' into it.
try:
    f=open(".queries","x")
    f.close()
    f=open(".queries","w")
    f.write("0")
    f.close()
except:
    pass

#Add one to the number stored in .queries and write the number back into .queries. This records the number of times a query has been made on the machine.
f=open(".queries","r")
n=int(f.read().strip())
f.close()
f=open(".queries","w")
n+=1
f.write(str(n))
f.close()


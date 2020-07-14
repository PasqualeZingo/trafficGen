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
        results = self.browser.find_elements_by_xpath(
            "//div[@id='links']/div/div/div[1]"
        )
        print([results[i].text for i in range(len(results))])

    def get_page(self, url):
        self.browser.get(url)
        self.store_page()
        print(self.source[:300])

    def close_browser(self):
        self.browser.quit()

    def random_query(self):
        query = "+".join(sample(self.terms, k=randint(3) + 1))
        print(query)
        self.google_query(query)

    #         print(self.get_urls_in_page())

    def get_urls_in_page(self):
        results = self.browser.find_elements_by_id("links")
        num_page_items = len(results)
        for i in range(num_page_items):
            print(results[i].text)
            print(len(results))


# ua.close_browser()
ua = userAgent()
ua.random_query()
# ua.get_urls_in_page()

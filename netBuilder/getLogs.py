from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import time

class Req:
	
	def __init__(self):
		options = Options()
		options.add_argument("--headless")
		self.browser = webdriver.Firefox(options=options)
	def store_page(self):
		self.source = self.browser.page_source

	def Connect(self):
		query = "https://192.168.1.1"
		self.browser.get(query)
	
	def Auth(self):
		username_box = self.browser.find_element_by_name("usernamefld")
		password_box = self.browser.find_element_by_name("passwordfld")
		login = self.browser.find_element_by_name("login")
		username_box.clear()
		username_box.send_keys("admin")
		password_box.clear()
		password_box.send_keys("pfsense")
		login.click()

	def close_browser(self):
		self.browser.close()
		self.browser.quit()

R = Req()

R.Connect()

R.Auth()

time.sleep(10)

R.store_page()

print(R.source)

R.close_browser()

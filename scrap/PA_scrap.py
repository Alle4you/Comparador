import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome()
url = "https://www.paloaltonetworks.com/products/product-selection.html"
driver.get(url)
time.sleep(3)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
divs = soup.find_all("div", class_="col-md-8")

log = open('scrap\pa.txt', 'a')
log.write(str(divs))


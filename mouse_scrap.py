from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

products = []
prices   = []
ratings   = []

driver.get("https://www.pccomponentes.com/ratones")


content = driver.page_source
soup    = BeautifulSoup(content)
for a in soup.findAll('div', attrs={'class':'c-product-card__content'}):
    name   = a.find('h3', attrs={'class':'c-product-card__title'})
    price  = a.find('div', attrs={'class':'c-product-card__prices-actual'})
    rating = a.find('span', attrs={'class':'c-star-rating__text'})

    products.append(name.a.text)
    prices.append(price.text)
    if rating!=None:
        ratings.append(rating.text)
    else:
        ratings.append("0")
    
df = pd.DataFrame({'Price':prices,'Rating':ratings,'Product Name':products}) 
df.to_csv('products.csv', index=False, encoding='utf-8')
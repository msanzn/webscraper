from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import statistics

Titles    = []
Ratings   = []
Names     = []
Countries = []
Dates     = []
Bodies    = []
Verified  = []

url_main = 'https://www.airlinequality.com/airport-reviews/london-heathrow-airport'
page = '/page/'
options= '/?sortby=post_date%3ADesc&pagesize=100'
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

url = url_main + page + "1" +options; 
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

n_total_reviews = int(soup.find('span',{'itemprop':'reviewCount'}).text)
n_pages = n_total_reviews//100 +1

for ii in range(n_pages):
    page_number= str(ii+1)
    url = url_main + page + page_number +options; 
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    allarticles = soup.findAll('article')
    articles = allarticles[0].findAll('article')

    if len(articles)>0: 
        for idx, one in enumerate(articles):
            title = one.find('h2',{'class': 'text_header'}).text
            if title[0]=='"':
                title=title[1:-1]
            if(one.find('span',{'itemprop': 'ratingValue'})==None):
                rating = 0
            else:
                rating = int(one.find('span',{'itemprop': 'ratingValue'}).text)
            name = one.find('span',{'itemprop': 'name'}).text
            country = one.find('h3',{'class': 'text_sub_header'}).text
            country= re.findall("\((.*?)\)", country)
            if(country):
                country = country[0]
            else:
                country = ""
            date = one.find('time',{'itemprop': 'datePublished'}).text
            body =one.find('div',{'itemprop': 'reviewBody'}).text
            bod=body.split("|")
            if len(bod)>1:
                verification = bod[0]
                body = bod[1]
            else:
                body = bod[0]
                verification = "unverified"

            Titles.append(title)
            Ratings.append(rating) 
            Names.append(name)
            Countries.append(country)
            Dates.append(date)
            Bodies.append(body)
            Verified.append(verification)
Ratings_mean = []
for ii in range(len(Ratings)):
    Ratings_mean.append(statistics.mean(Ratings[0:(ii+1)]))

plt.figure()
plt.plot(Ratings_mean)
plt.savefig('figura.pdf')
plt.show()
df = pd.DataFrame({'Title':Titles,'Rating':Ratings,'Name':Names, 'Country': Countries, 'Date': Dates, 'Verification': Verified, 'Body':Bodies}) 
df.to_csv('Airport_review.csv', index=False, encoding='utf-8')
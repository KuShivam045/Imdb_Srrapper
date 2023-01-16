from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.request import urlopen as urReq
from bs4 import BeautifulSoup as bs

imdb_url = "https://www.imdb.com/search/title/?release_date=2018-01-01,2018-12-31"
response_website = urReq(imdb_url)
data_imdb = response_website.read()
beautifyd_html = bs(data_imdb, "html.parser")
bigbox = beautifyd_html.find_all("div", {"class":"lister list detail sub-list"})    
content = bigbox[0].div.find_all("div",{"class" : "lister-item mode-advanced"})
imdb_data = []

for i in range(0,len(content)):
    data = dict(Movie_Name = content[i].h3.a.text,
    Release_year = content[i].h3.find('span', class_ = 'lister-item-year').text,
    Duration = content[i].p.find("span",{"class" : "runtime"}),
    Movie_about = content[i].p.find("span",{"class" : "genre"}).text.strip("\n"),
    Ratings= float(content[i].strong.text),
    Description = content[i].find_all("p",{"class" : "text-muted"})[1].text.strip("\n"),
    Votes = int(content[i].find('span', attrs = {'name':'nv'})['data-value']))
    
    imdb_data.append(data)

df = pd.DataFrame(imdb_data)
print(df)
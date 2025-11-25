import urllib
from bs4 import BeautifulSoup
import os
import time
import random

"""
First, we will scrape our website to a html file
"""
#Our website
url_main = "https://www.joodsmonument.nl/en/page/344139/sinti-en-roma-namenlijst"
    
#Appearing as another user (for both rounds of scraping)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

#Scraping the website to a html file
try:
    name = url_main.split('/')[-1]
    request = urllib.request.Request( url_main, None, headers )
    response = urllib.request.urlopen( request )
    with open(name+".html", 'w',encoding="utf-8") as f:
        f.write(str(response.read().decode('utf-8')))
except urllib.error.HTTPError as e:
    print(e)

"""
Now we will scrape each of the links on the website to seperate html files
"""
#Creates folder
os.mkdir("sinti-en-roma-namenlijst")

#Finding all the names/pages we need to scrape using BeautifulSoup
page = open('sinti-en-roma-namenlijst.html','r',encoding='utf-8').read()
soup = BeautifulSoup(page,features="html")
#The class of the part we are intrested in
names = soup.findAll('h3',attrs={'class':'c-card-tiny__title'})

#For each name/page we want to scrape
for name in names:
    #defining the link, it starts after a
    link = name.find('a')
    #defining the name, just the text in the link
    name = link.text
    try:
        print("Getting the file for:",name)
        #defining the url
        url = 'https://www.joodsmonument.nl'+link['href']
        #scrapes to html files
        request = urllib.request.Request(url, None, headers )
        response = urllib.request.urlopen( request )
        #we save the files in our folder, we name it the persons ID (from url)
        #as well as their name
        with open("sinti-en-roma-namenlijst/"+url.split('/')[-2]+"-"+
                  name.replace('/','-')+".html",'w',encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        #Waits before scraping the next page
        time.sleep(random.randint(1, 2))
        
    except KeyError:
        print("Name is not available:",name)
    except urllib.error.HTTPError as e:
        print(e)
        

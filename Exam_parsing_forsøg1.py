# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 12:32:52 2025

@author: jonas
"""

import os
from bs4 import BeautifulSoup
import pandas

data = []

files = sorted(os.listdir('sinti-en-roma-namenlijst'))
for file in files:
    text = open('sinti-en-roma-namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    # pID, name, date of birth and death, place of birth and death og alder
 #   matchday = file[:-6] 
    names = soup.findAll('header',attrs={'class':'c-warvictim-intro'})
    for name in names:
        #makes a list
        person = []
        person_info = name.find('p',attrs={'class':'c-warvictim-intro__sub'}).text
        person_info = person_info.strip()
        person_info = " ".join(person_info.split())
#få den  til at stoppe ved - og splitte fødselssted ved første , komma
        print(person_info)
        
        #looks at html files and takes their person ID
        pID = file.split("-")[0]
        person.append(pID)
        #looks at our html files and takes their names
        pName = file.replace(pID+'-',"")
        pName = pName.replace(".html","")
        person.append(pName)
        

   


#birthdate.strip()
       # birthplace = name.find()
     #   date = day.find('div',attrs={'class':'kick__v100-gameList__header'}).text
      #  date = date.strip().split(", ")[1]
       # matches = day.findAll('div',attrs={'kick__v100-gameList__gameRow'})
        #for m in matches:
         #   #home team
          #  teams = m.findAll('div',attrs={'kick__v100-gameCell__team__name'})
           # home_team = teams[0].text
            #away_team = teams[1].text
            #goals = m.findAll('div',attrs={'kick__v100-scoreBoard__scoreHolder__score'})
          #  home_goals = goals[0].text
           # away_goals = goals[1].text
           # data.append([matchday,date,home_team,away_team,home_goals,away_goals])

#df = pandas.DataFrame(data,columns = ['matchday','date','home team','away team','home goals','away goals'])
#df.to_csv('results.csv', index=False, encoding='utf-8')
